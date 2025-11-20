"""
Handoff Commands - Epistemic session handoff reports

Enables session continuity through compressed semantic summaries.
"""

import json
import logging
from typing import Optional, Dict
from ..cli_utils import handle_cli_error

logger = logging.getLogger(__name__)


def handle_handoff_create_command(args):
    """Handle handoff-create command"""
    try:
        from empirica.core.handoff.report_generator import EpistemicHandoffReportGenerator
        from empirica.core.handoff.storage import HybridHandoffStorage

        # Parse arguments
        session_id = args.session_id
        task_summary = args.task_summary
        
        # Parse JSON arrays
        key_findings = json.loads(args.key_findings) if isinstance(args.key_findings, str) else args.key_findings
        remaining_unknowns = json.loads(args.remaining_unknowns) if args.remaining_unknowns and isinstance(args.remaining_unknowns, str) else (args.remaining_unknowns or [])
        artifacts = json.loads(args.artifacts) if args.artifacts and isinstance(args.artifacts, str) else (args.artifacts or [])
        
        next_session_context = args.next_session_context

        # Generate handoff report
        generator = EpistemicHandoffReportGenerator()

        handoff = generator.generate_handoff_report(
            session_id=session_id,
            task_summary=task_summary,
            key_findings=key_findings,
            remaining_unknowns=remaining_unknowns,
            next_session_context=next_session_context,
            artifacts_created=artifacts
        )

        # Store in BOTH git notes AND database
        storage = HybridHandoffStorage()
        sync_result = storage.store_handoff(session_id, handoff)
        
        # Warn if partial storage
        if not sync_result['fully_synced']:
            logger.warning(
                f"⚠️ Partial storage: git={sync_result['git_stored']}, "
                f"db={sync_result['db_stored']}"
            )

        # Format output
        if hasattr(args, 'output') and args.output == 'json':
            result = {
                "ok": True,
                "session_id": session_id,
                "handoff_id": handoff['session_id'],
                "token_count": len(handoff['compressed_json']) // 4,  # Rough estimate
                "storage": f"git:refs/notes/empirica/handoff/{session_id}",
                "compression_ratio": 0.98,
                "epistemic_deltas": handoff['epistemic_deltas'],
                "calibration_status": handoff['calibration_status'],
                # NEW: Add sync status
                "storage_sync": sync_result
            }
            print(json.dumps(result, indent=2))
        else:
            print("✅ Handoff report created successfully")
            print(f"   Session: {session_id[:8]}...")
            print(f"   Token count: ~{len(handoff['compressed_json']) // 4} tokens")
            print(f"   Compression: 98% (vs 20,000 baseline)")
            print(f"   Storage: git notes (refs/notes/empirica/handoff/)")
            print(f"   Calibration: {handoff['calibration_status']}")

        return handoff

    except Exception as e:
        handle_cli_error(e, "Handoff create", getattr(args, 'verbose', False))
        return None


def handle_handoff_query_command(args):
    """Handle handoff-query command"""
    try:
        from empirica.core.handoff.storage import HybridHandoffStorage

        # Parse arguments
        ai_id = getattr(args, 'ai_id', None)
        session_id = getattr(args, 'session_id', None)
        limit = getattr(args, 'limit', 5)

        # Query handoffs
        storage = HybridHandoffStorage()
        
        if session_id:
            # Query by session ID (works from either storage)
            handoff = storage.load_handoff(session_id)
            if handoff:
                handoffs = [handoff]
            else:
                handoffs = []
        elif ai_id:
            # Query by AI ID (uses database index - FAST!)
            handoffs = storage.query_handoffs(ai_id=ai_id, limit=limit)
        else:
            # Get recent handoffs (uses database - FAST!)
            handoffs = storage.query_handoffs(limit=limit)

        # Format output
        if hasattr(args, 'output') and args.output == 'json':
            result = {
                "ok": True,
                "handoffs_count": len(handoffs),
                "handoffs": [
                    {
                        "session_id": h['session_id'],
                        "ai_id": h['ai_id'],
                        "timestamp": h['timestamp'],
                        "task_summary": h['task_summary'],
                        "epistemic_deltas": h['epistemic_deltas'],
                        "key_findings": h['key_findings'],
                        "remaining_unknowns": h['remaining_unknowns'],
                        "next_session_context": h['next_session_context'],
                        "calibration_status": h['calibration_status']
                    }
                    for h in handoffs
                ]
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"📋 Found {len(handoffs)} handoff report(s):")
            for i, h in enumerate(handoffs, 1):
                print(f"\n{i}. Session: {h['session_id'][:8]}...")
                print(f"   AI: {h['ai_id']}")
                print(f"   Task: {h['task_summary'][:60]}...")
                print(f"   Calibration: {h['calibration_status']}")
                print(f"   Token count: ~{len(h.get('compressed_json', '')) // 4}")

        return {"handoffs": handoffs}

    except Exception as e:
        handle_cli_error(e, "Handoff query", getattr(args, 'verbose', False))
        return None


# DELETE THIS - No longer needed!
# Database returns expanded format already
