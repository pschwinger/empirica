"""
Session Management Commands - Query and manage Empirica sessions

Provides commands for:
- Listing all sessions
- Showing detailed session info with epistemic vectors
- Exporting session data to JSON
"""

import json
import logging
from datetime import datetime
from ..cli_utils import handle_cli_error, print_header

# Set up logging for session commands
logger = logging.getLogger(__name__)


def handle_sessions_list_command(args):
    """List all sessions with summary information"""
    try:
        print_header("📋 Empirica Sessions")
        
        from empirica.data.session_database import SessionDatabase
        
        db = SessionDatabase(db_path=".empirica/sessions/sessions.db")
        cursor = db.conn.cursor()
        
        # Query all sessions
        cursor.execute("""
            SELECT 
                session_id, ai_id, user_id, start_time, end_time,
                total_cascades, avg_confidence, drift_detected
            FROM sessions
            ORDER BY start_time DESC
            LIMIT ?
        """, (args.limit if hasattr(args, 'limit') else 50,))
        
        sessions = cursor.fetchall()
        
        logger.info(f"Found {len(sessions)} sessions to display")
        
        if not sessions:
            logger.info("No sessions found in database")
            print("\n📭 No sessions found")
            print("💡 Create a session with: empirica preflight <task>")
            db.close()
            return
        
        print(f"\n📊 Found {len(sessions)} sessions:\n")
        
        for row in sessions:
            session_id, ai_id, user_id, start_time, end_time, cascades, conf, drift = row
            
            # Format timestamps
            start = datetime.fromisoformat(start_time).strftime("%Y-%m-%d %H:%M") if start_time else "N/A"
            end = datetime.fromisoformat(end_time).strftime("%Y-%m-%d %H:%M") if end_time else "Active"
            
            # Status indicator
            status = "✅" if end_time else "⏳"
            drift_icon = "⚠️" if drift else ""
            
            print(f"{status} {session_id[:8]}")
            print(f"   🤖 AI: {ai_id}")
            if user_id:
                print(f"   👤 User: {user_id}")
            print(f"   📅 Started: {start}")
            print(f"   🏁 Ended: {end}")
            print(f"   🔄 Cascades: {cascades}")
            if conf:
                print(f"   📊 Avg Confidence: {conf:.2f}")
            if drift:
                print(f"   {drift_icon} Drift Detected")
            print()
        
        if len(sessions) >= 50 and not hasattr(args, 'limit'):
            print("💡 Showing 50 most recent sessions. Use --limit to see more.")
        
        print(f"💡 View details: empirica sessions show <session_id>")
        
        db.close()
        
    except Exception as e:
        handle_cli_error(e, "Listing sessions", getattr(args, 'verbose', False))


def handle_sessions_show_command(args):
    """Show detailed session information including epistemic vectors"""
    try:
        from empirica.data.session_database import SessionDatabase
        from empirica.utils.session_resolver import resolve_session_id

        # Resolve session alias to UUID
        try:
            session_id = resolve_session_id(args.session_id)
        except ValueError as e:
            print(f"\n❌ {str(e)}")
            print(f"💡 Provided: {args.session_id}")
            print(f"💡 List sessions with: empirica sessions-list")
            return

        print_header(f"📊 Session Details: {session_id[:8]}")

        db = SessionDatabase(db_path=".empirica/sessions/sessions.db")

        # Get session summary (use resolved session_id)
        summary = db.get_session_summary(session_id, detail_level="detailed")
        
        if not summary:
            logger.warning(f"Session not found: {args.session_id}")
            print(f"\n❌ Session not found: {args.session_id}")
            print(f"💡 List sessions with: empirica sessions list")
            db.close()
            return
        
        # Basic info
        print(f"\n🆔 Session ID: {summary['session_id']}")
        print(f"🤖 AI: {summary['ai_id']}")
        print(f"📅 Started: {summary['start_time']}")
        if summary.get('end_time'):
            print(f"🏁 Ended: {summary['end_time']}")
        else:
            print(f"⏳ Status: Active")
        
        # Cascades
        print(f"\n🔄 Total Cascades: {summary['total_cascades']}")
        if summary.get('avg_confidence'):
            print(f"📊 Average Confidence: {summary['avg_confidence']:.2f}")
        
        # Show cascade tasks
        if args.verbose and isinstance(summary.get('cascades'), list):
            print(f"\n📋 Cascade Tasks:")
            for i, cascade in enumerate(summary['cascades'][:10], 1):
                if isinstance(cascade, dict):
                    task = cascade.get('task', 'Unknown')
                    conf = cascade.get('final_confidence')
                    print(f"   {i}. {task}")
                    if conf:
                        print(f"      Confidence: {conf:.2f}")
                else:
                    print(f"   {i}. {cascade}")
            
            if summary['total_cascades'] > 10:
                print(f"   ... and {summary['total_cascades'] - 10} more")
        
        # Epistemic vectors (preflight)
        if summary.get('preflight'):
            print(f"\n🚀 Preflight Epistemic State:")
            vectors = summary['preflight']
            print(f"   • KNOW:    {vectors.get('know', 0.5):.2f}")
            print(f"   • DO:      {vectors.get('do', 0.5):.2f}")
            print(f"   • CONTEXT: {vectors.get('context', 0.5):.2f}")
            
            if args.verbose:
                print(f"\n   Comprehension:")
                print(f"   • CLARITY:   {vectors.get('clarity', 0.5):.2f}")
                print(f"   • COHERENCE: {vectors.get('coherence', 0.5):.2f}")
                print(f"   • SIGNAL:    {vectors.get('signal', 0.5):.2f}")
                print(f"   • DENSITY:   {vectors.get('density', 0.5):.2f}")
                
                print(f"\n   Execution:")
                print(f"   • STATE:      {vectors.get('state', 0.5):.2f}")
                print(f"   • CHANGE:     {vectors.get('change', 0.5):.2f}")
                print(f"   • COMPLETION: {vectors.get('completion', 0.5):.2f}")
                print(f"   • IMPACT:     {vectors.get('impact', 0.5):.2f}")
                
                print(f"\n   Meta-Cognitive:")
                print(f"   • ENGAGEMENT:  {vectors.get('engagement', 0.5):.2f}")
                print(f"   • UNCERTAINTY: {vectors.get('uncertainty', 0.5):.2f}")
        
        # Epistemic vectors (postflight)
        if summary.get('postflight'):
            print(f"\n🏁 Postflight Epistemic State:")
            vectors = summary['postflight']
            print(f"   • KNOW:    {vectors.get('know', 0.5):.2f}")
            print(f"   • DO:      {vectors.get('do', 0.5):.2f}")
            print(f"   • CONTEXT: {vectors.get('context', 0.5):.2f}")
            
            if args.verbose:
                print(f"\n   Comprehension:")
                print(f"   • CLARITY:   {vectors.get('clarity', 0.5):.2f}")
                print(f"   • COHERENCE: {vectors.get('coherence', 0.5):.2f}")
                print(f"   • SIGNAL:    {vectors.get('signal', 0.5):.2f}")
                print(f"   • DENSITY:   {vectors.get('density', 0.5):.2f}")
                
                print(f"\n   Execution:")
                print(f"   • STATE:      {vectors.get('state', 0.5):.2f}")
                print(f"   • CHANGE:     {vectors.get('change', 0.5):.2f}")
                print(f"   • COMPLETION: {vectors.get('completion', 0.5):.2f}")
                print(f"   • IMPACT:     {vectors.get('impact', 0.5):.2f}")
                
                print(f"\n   Meta-Cognitive:")
                print(f"   • ENGAGEMENT:  {vectors.get('engagement', 0.5):.2f}")
                print(f"   • UNCERTAINTY: {vectors.get('uncertainty', 0.5):.2f}")
        
        # Epistemic delta (learning)
        if summary.get('epistemic_delta'):
            print(f"\n📈 Learning Delta (Preflight → Postflight):")
            delta = summary['epistemic_delta']
            
            # Show significant changes
            significant = {k: v for k, v in delta.items() if abs(v) >= 0.05}
            
            if significant:
                for key, value in sorted(significant.items(), key=lambda x: abs(x[1]), reverse=True):
                    icon = "↗" if value > 0 else "↘"
                    print(f"   {icon} {key.upper():12s} {value:+.2f}")
            else:
                print(f"   ➖ Minimal change (all < ±0.05)")
        
        # Tools used
        if summary.get('tools_used'):
            print(f"\n🔧 Investigation Tools Used:")
            for tool in summary['tools_used']:
                print(f"   • {tool['tool']}: {tool['count']} times")
        
        # Export hint
        print(f"\n💡 Export to JSON: empirica sessions export {args.session_id}")
        
        db.close()
        
    except Exception as e:
        handle_cli_error(e, "Showing session details", getattr(args, 'verbose', False))


def handle_sessions_export_command(args):
    """Export session data to JSON file"""
    try:
        from empirica.data.session_database import SessionDatabase
        from empirica.utils.session_resolver import resolve_session_id

        # Resolve session alias to UUID
        try:
            session_id = resolve_session_id(args.session_id)
        except ValueError as e:
            print(f"\n❌ {str(e)}")
            print(f"💡 Provided: {args.session_id}")
            return

        print_header(f"📦 Exporting Session: {session_id[:8]}")

        db = SessionDatabase(db_path=".empirica/sessions/sessions.db")

        # Get full session summary (use resolved session_id)
        summary = db.get_session_summary(session_id, detail_level="full")
        
        if not summary:
            logger.warning(f"Session not found for export: {args.session_id}")
            print(f"\n❌ Session not found: {args.session_id}")
            db.close()
            return
        
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            output_file = f"session_{args.session_id[:8]}.json"
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Session data exported to {output_file}")
        
        print(f"\n✅ Session exported successfully")
        print(f"📄 File: {output_file}")
        print(f"📊 Size: {len(json.dumps(summary, default=str))} bytes")
        
        # Summary stats
        print(f"\n📋 Exported Data:")
        print(f"   • Session ID: {summary['session_id']}")
        print(f"   • AI: {summary['ai_id']}")
        print(f"   • Cascades: {summary['total_cascades']}")
        if summary.get('preflight'):
            print(f"   • Preflight vectors: ✅")
        if summary.get('postflight'):
            print(f"   • Postflight vectors: ✅")
        if summary.get('epistemic_delta'):
            print(f"   • Learning delta: ✅")
        
        db.close()
        
    except Exception as e:
        handle_cli_error(e, "Exporting session", getattr(args, 'verbose', False))

def handle_session_end_command(args):
    """Handle session-end command - close session and create handoff report"""
    try:
        from empirica.core.handoff.auto_generator import auto_generate_handoff, close_session
        from empirica.core.handoff.storage import HybridHandoffStorage
        import subprocess
        
        session_id = args.session_id
        create_commit = getattr(args, 'commit', False)
        manual = getattr(args, 'manual', False)
        
        logger.info(f"🏁 Ending session: {session_id[:8]}...")
        
        # 1. Close session (set end_time)
        close_session(session_id)
        logger.info("   ✅ Session closed")
        
        # 2. Generate handoff report
        if manual:
            # Manual mode: user provides all data
            task_summary = args.summary
            key_findings = json.loads(args.findings) if hasattr(args, 'findings') and args.findings else []
            remaining_unknowns = json.loads(args.unknowns) if hasattr(args, 'unknowns') and args.unknowns else []
            next_context = args.context if hasattr(args, 'context') else "Session ended"
            artifacts = json.loads(args.artifacts) if hasattr(args, 'artifacts') and args.artifacts else []
            
            handoff_data = {
                'session_id': session_id,
                'task_summary': task_summary,
                'key_findings': key_findings,
                'remaining_unknowns': remaining_unknowns,
                'next_session_context': next_context,
                'artifacts_created': artifacts,
                'epistemic_deltas': {},
                'duration_seconds': 0
            }
        else:
            # Auto-generate from cascades
            handoff_data = auto_generate_handoff(session_id)
            
            # Allow overrides
            if hasattr(args, 'summary') and args.summary:
                handoff_data['task_summary'] = args.summary
            if hasattr(args, 'findings') and args.findings:
                additional_findings = json.loads(args.findings)
                handoff_data['key_findings'].extend(additional_findings)
        
        logger.info("   ✅ Handoff report generated")
        
        # 3. Store handoff report
        storage = HybridHandoffStorage()
        storage.store_handoff(session_id, handoff_data)
        logger.info("   ✅ Handoff stored (database + git notes)")
        
        # 4. Optional: Create git commit
        if create_commit:
            commit_message = f"[empirica] Session {session_id[:8]}: {handoff_data['task_summary'][:60]}"
            try:
                subprocess.run(['git', 'add', '-A'], check=True, timeout=5)
                subprocess.run(['git', 'commit', '-m', commit_message], check=True, timeout=5)
                logger.info(f"   ✅ Git commit created: {commit_message}")
            except Exception as e:
                logger.warning(f"   ⚠️  Git commit failed: {e}")
        
        # 5. Display summary
        print("\n" + "=" * 60)
        print("SESSION END SUMMARY")
        print("=" * 60)
        print(f"Session ID: {session_id}")
        print(f"Cascades: {handoff_data.get('cascades_completed', 0)}")
        print(f"Duration: {handoff_data.get('duration_seconds', 0) / 60:.1f} minutes")
        print(f"\nTask: {handoff_data['task_summary']}")
        print(f"\nKey Findings ({len(handoff_data['key_findings'])}):")
        for i, finding in enumerate(handoff_data['key_findings'][:5], 1):
            print(f"  {i}. {finding}")
        
        if handoff_data['remaining_unknowns']:
            print(f"\nRemaining Unknowns ({len(handoff_data['remaining_unknowns'])}):")
            for i, unknown in enumerate(handoff_data['remaining_unknowns'], 1):
                print(f"  {i}. {unknown}")
        
        print(f"\nNext Session Context:")
        print(f"  {handoff_data['next_session_context']}")
        
        if handoff_data.get('epistemic_deltas', {}).get('knowledge_trajectory'):
            print(f"\nEpistemic Trajectory:")
            print(f"  Knowledge: {handoff_data['epistemic_deltas']['knowledge_trajectory']}")
            print(f"  Overall: {handoff_data['epistemic_deltas'].get('overall_delta', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("✅ Session ended successfully")
        print(f"📋 Query handoff: empirica handoff-query --session-id {session_id}")
        print("=" * 60)
        
    except Exception as e:
        handle_cli_error(e, "Session end", getattr(args, 'verbose', False))



def handle_session_end_command(args):
    """Handle session-end command - close session and create handoff report"""
    try:
        from empirica.core.handoff.auto_generator import auto_generate_handoff, close_session
        from empirica.core.handoff.storage import HybridHandoffStorage
        import subprocess
        
        session_id = args.session_id
        create_commit = getattr(args, 'commit', False)
        manual = getattr(args, 'manual', False)
        
        print(f"🏁 Ending session: {session_id[:8]}...")
        
        # 1. Close session (set end_time)
        close_session(session_id)
        print("   ✅ Session closed")
        
        # 2. Generate handoff report
        if manual:
            # Manual mode: user provides all data
            task_summary = args.summary
            key_findings = json.loads(args.findings) if hasattr(args, 'findings') and args.findings else []
            remaining_unknowns = json.loads(args.unknowns) if hasattr(args, 'unknowns') and args.unknowns else []
            next_context = args.context if hasattr(args, 'context') else "Session ended"
            artifacts = json.loads(args.artifacts) if hasattr(args, 'artifacts') and args.artifacts else []
            
            handoff_data = {
                'session_id': session_id,
                'task_summary': task_summary,
                'key_findings': key_findings,
                'remaining_unknowns': remaining_unknowns,
                'next_session_context': next_context,
                'artifacts_created': artifacts,
                'epistemic_deltas': {},
                'duration_seconds': 0
            }
        else:
            # Auto-generate from cascades
            handoff_data = auto_generate_handoff(session_id)
            
            # Allow overrides
            if hasattr(args, 'summary') and args.summary:
                handoff_data['task_summary'] = args.summary
            if hasattr(args, 'findings') and args.findings:
                additional_findings = json.loads(args.findings)
                handoff_data['key_findings'].extend(additional_findings)
        
        print("   ✅ Handoff report generated")
        
        # 3. Store handoff report
        storage = HybridHandoffStorage()
        storage.store_handoff(session_id, handoff_data)
        print("   ✅ Handoff stored (database + git notes)")
        
        # 4. Optional: Create git commit
        if create_commit:
            commit_message = f"[empirica] Session {session_id[:8]}: {handoff_data['task_summary'][:60]}"
            try:
                subprocess.run(['git', 'add', '-A'], check=True, timeout=5)
                subprocess.run(['git', 'commit', '-m', commit_message], check=True, timeout=5)
                print(f"   ✅ Git commit created: {commit_message}")
            except Exception as e:
                print(f"   ⚠️  Git commit failed: {e}")
        
        # 5. Display summary
        print("\n" + "=" * 60)
        print("SESSION END SUMMARY")
        print("=" * 60)
        print(f"Session ID: {session_id}")
        print(f"Cascades: {handoff_data.get('cascades_completed', 0)}")
        print(f"Duration: {handoff_data.get('duration_seconds', 0) / 60:.1f} minutes")
        print(f"\nTask: {handoff_data['task_summary']}")
        print(f"\nKey Findings ({len(handoff_data['key_findings'])}):")
        for i, finding in enumerate(handoff_data['key_findings'][:5], 1):
            print(f"  {i}. {finding}")
        
        if handoff_data['remaining_unknowns']:
            print(f"\nRemaining Unknowns ({len(handoff_data['remaining_unknowns'])}):")
            for i, unknown in enumerate(handoff_data['remaining_unknowns'], 1):
                print(f"  {i}. {unknown}")
        
        print(f"\nNext Session Context:")
        print(f"  {handoff_data['next_session_context']}")
        
        if handoff_data.get('epistemic_deltas', {}).get('knowledge_trajectory'):
            print(f"\nEpistemic Trajectory:")
            print(f"  Knowledge: {handoff_data['epistemic_deltas']['knowledge_trajectory']}")
            print(f"  Overall: {handoff_data['epistemic_deltas'].get('overall_delta', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("✅ Session ended successfully")
        print(f"📋 Query handoff: empirica handoff-query --session-id {session_id}")
        print("=" * 60)
        
    except Exception as e:
        handle_cli_error(e, "Session end", getattr(args, 'verbose', False))
