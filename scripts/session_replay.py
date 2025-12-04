#!/usr/bin/env python3
"""
Session Replay for Statusline Testing

Replays a historical session with preserved temporal relationships.
Useful for:
1. Testing statusline signal accuracy against real data
2. Validating metacognitive cascade workflows
3. Demonstrating signal detection reliability

Usage:
    python3 session_replay.py <session_id> [--compressed] [--timeline]

Options:
    --compressed: Replay at 10x speed (compressed timeline)
    --timeline: Show timeline of events during replay
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add empirica to path
EMPIRICA_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(EMPIRICA_ROOT))

from empirica.data.session_database import SessionDatabase


def export_session_data(session_id: str) -> dict:
    """Export complete session data with temporal information."""
    db = SessionDatabase()
    cursor = db.conn.cursor()

    # Get session info
    cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
    session_cols = [description[0] for description in cursor.description]
    session = dict(zip(session_cols, cursor.fetchone() or []))

    # Get goals
    cursor.execute("SELECT * FROM goals WHERE session_id = ?", (session_id,))
    goal_cols = [description[0] for description in cursor.description]
    goals = [dict(zip(goal_cols, row)) for row in cursor.fetchall()]

    # Get cascades with assessments
    cursor.execute("""
        SELECT c.*, ea.phase, ea.assessed_at
        FROM cascades c
        LEFT JOIN epistemic_assessments ea ON c.cascade_id = ea.cascade_id
        WHERE c.session_id = ?
        ORDER BY c.started_at
    """, (session_id,))
    cascade_cols = [description[0] for description in cursor.description]
    cascades = [dict(zip(cascade_cols, row)) for row in cursor.fetchall()]

    # Get subtasks
    cursor.execute("""
        SELECT s.* FROM subtasks s
        JOIN goals g ON s.goal_id = g.id
        WHERE g.session_id = ?
        ORDER BY s.completed_timestamp
    """, (session_id,))
    subtask_cols = [description[0] for description in cursor.description]
    subtasks = [dict(zip(subtask_cols, row)) for row in cursor.fetchall()]

    db.close()

    return {
        "session": session,
        "goals": goals,
        "cascades": cascades,
        "subtasks": subtasks,
    }


def calculate_timeline(data: dict) -> list:
    """Calculate timeline of events with relative times."""
    events = []

    # Add goal creation events
    for goal in data["goals"]:
        events.append({
            "type": "goal_created",
            "time": goal.get("created_timestamp", 0),
            "data": goal,
        })

    # Add subtask completion events
    for subtask in data["subtasks"]:
        if subtask.get("completed_timestamp"):
            events.append({
                "type": "subtask_completed",
                "time": subtask.get("completed_timestamp"),
                "data": subtask,
            })

    # Add cascade events
    for cascade in data["cascades"]:
        events.append({
            "type": "cascade_started",
            "time": cascade.get("started_at"),
            "data": cascade,
        })
        if cascade.get("completed_at"):
            events.append({
                "type": "cascade_completed",
                "time": cascade.get("completed_at"),
                "data": cascade,
            })

    # Sort by time
    events.sort(key=lambda e: float(e["time"] or 0) if e["time"] else 0)

    # Calculate relative times (compress from start)
    if events:
        start_time = float(events[0]["time"] or 0)
        for event in events:
            current_time = float(event["time"] or 0)
            event["relative_time"] = current_time - start_time
            event["time_elapsed"] = event["relative_time"]

    return events


def replay_session(session_id: str, compressed: bool = False, show_timeline: bool = False):
    """Replay a session with proper timing."""
    print(f"\n📊 Session Replay: {session_id[:8]}...")
    print("=" * 70)

    # Export data
    data = export_session_data(session_id)
    if not data["session"]:
        print("❌ Session not found")
        return

    # Calculate timeline
    events = calculate_timeline(data)
    if not events:
        print("❌ No events in session")
        return

    # Show summary
    session_info = data["session"]
    print(f"\n📋 Session Info:")
    print(f"   AI: {session_info.get('ai_id', 'unknown')}")
    start_time = session_info.get('start_time', 0)
    if isinstance(start_time, str):
        print(f"   Start: {start_time}")
    else:
        print(f"   Start: {datetime.fromtimestamp(float(start_time))}")
    print(f"   Bootstrap: {session_info.get('bootstrap_level', 0)}")

    print(f"\n📈 Timeline ({len(events)} events):")
    for i, event in enumerate(events, 1):
        event_type = event["type"]
        elapsed = event["time_elapsed"]

        if event_type == "goal_created":
            print(f"   {i}. [{elapsed:.1f}s] GOAL: {event['data'].get('objective', 'unnamed')[:50]}")
        elif event_type == "subtask_completed":
            desc = event["data"].get("description", "")[:40]
            print(f"   {i}. [{elapsed:.1f}s] ✓ TASK: {desc}")
        elif event_type == "cascade_started":
            phase = event["data"].get("phase", "unknown")
            task = event["data"].get("task", "")[:40]
            print(f"   {i}. [{elapsed:.1f}s] ▶ {phase}: {task}")
        elif event_type == "cascade_completed":
            print(f"   {i}. [{elapsed:.1f}s] ◀ CASCADE DONE")

    if show_timeline:
        print(f"\n⏱️  Replay Timeline (compressed={compressed}):")

        # Calculate total time
        total_time = max(e["time_elapsed"] for e in events)
        compression_factor = 10 if compressed else 1
        replay_duration = total_time / compression_factor

        print(f"   Real duration: {total_time:.1f}s")
        print(f"   Replay duration: {replay_duration:.1f}s (compression: {compression_factor}x)")
        print(f"   Events/second: {len(events) / replay_duration:.2f}")

    # Show CASCADE phases
    phases = {}
    for cascade in data["cascades"]:
        phase = cascade.get("phase", "UNKNOWN")
        if phase and phase not in ["", None]:
            if phase not in phases:
                phases[phase] = []
            phases[phase].append(cascade)

    if phases:
        print(f"\n🎯 CASCADE Phases:")
        for phase in ["PREFLIGHT", "CHECK", "POSTFLIGHT"]:
            if phase in phases:
                count = len(phases[phase])
                print(f"   {phase}: {count} assessment(s)")

    # Show goals and completion
    completed_goals = sum(1 for g in data["goals"] if g.get("is_completed"))
    total_goals = len(data["goals"])
    completed_tasks = sum(1 for s in data["subtasks"] if s.get("status") == "completed")
    total_tasks = len(data["subtasks"])

    print(f"\n📊 Completion Stats:")
    print(f"   Goals: {completed_goals}/{total_goals}")
    print(f"   Tasks: {completed_tasks}/{total_tasks}")

    print("\n" + "=" * 70)
    print("✅ Session replay analysis complete")
    print(f"\nTo test statusline with this session:")
    print(f"   python3 /home/yogapad/empirical-ai/empirica/scripts/statusline_empirica.py")
    print(f"\nStatusline will automatically detect the latest active session:")
    print(f"   Session ID: {session_id[:8]}...")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 session_replay.py <session_id> [--compressed] [--timeline]")
        print("\nExample:")
        print("  python3 session_replay.py 291e0f6d-5361-4412-ad21-bd0162881446 --timeline")
        sys.exit(1)

    session_id = sys.argv[1]
    compressed = "--compressed" in sys.argv
    show_timeline = "--timeline" in sys.argv

    replay_session(session_id, compressed=compressed, show_timeline=show_timeline)
