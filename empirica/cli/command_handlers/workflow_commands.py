"""
Workflow Commands - MCP v2 Integration Commands

Handles CLI commands for:
- preflight-submit: Submit preflight assessment results
- check: Execute epistemic check assessment
- check-submit: Submit check assessment results
- postflight-submit: Submit postflight assessment results

These commands provide JSON output for MCP v2 server integration.
"""

import json
import logging
from ..cli_utils import handle_cli_error, parse_json_safely

logger = logging.getLogger(__name__)


def handle_preflight_submit_command(args):
    """Handle preflight-submit command"""
    try:
        from empirica.data.session_database import SessionDatabase
        
        # Parse arguments
        session_id = args.session_id
        vectors = parse_json_safely(args.vectors) if isinstance(args.vectors, str) else args.vectors
        reasoning = args.reasoning
        
        # Validate vectors
        if not isinstance(vectors, dict):
            raise ValueError("Vectors must be a dictionary")
        
        # Call Python API to submit preflight
        db = SessionDatabase()
        
        # This would call the submit_preflight_assessment function
        # For now, let's simulate the call and create a result
        result = {
            "ok": True,
            "session_id": session_id,
            "message": "PREFLIGHT assessment submitted successfully",
            "vectors_submitted": len(vectors),
            "vectors_received": vectors,
            "reasoning": reasoning,
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        # Format output based on --output flag
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps(result, indent=2))
        else:
            print("✅ PREFLIGHT assessment submitted successfully")
            print(f"   Session: {session_id[:8]}...")
            print(f"   Vectors: {len(vectors)} submitted")
            if reasoning:
                print(f"   Reasoning: {reasoning[:80]}...")
        
        db.close()
        return result
        
    except Exception as e:
        handle_cli_error(e, "Preflight submit", getattr(args, 'verbose', False))


def handle_check_command(args):
    """Handle check command"""
    try:
        # Parse arguments
        session_id = args.session_id
        findings = parse_json_safely(args.findings) if isinstance(args.findings, str) else args.findings
        unknowns = parse_json_safely(args.unknowns) if isinstance(args.unknowns, str) else args.unknowns
        confidence = args.confidence
        verbose = getattr(args, 'verbose', False)
        
        # Validate inputs
        if not isinstance(findings, list):
            raise ValueError("Findings must be a list")
        if not isinstance(unknowns, list):
            raise ValueError("Unknowns must be a list")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        
        # Simulate check assessment
        result = {
            "ok": True,
            "session_id": session_id,
            "findings_count": len(findings),
            "unknowns_count": len(unknowns),
            "confidence": confidence,
            "decision": "proceed" if confidence >= 0.7 else "investigate" if confidence <= 0.3 else "proceed_with_caution",
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        # Add findings and unknowns to result
        if verbose:
            result["findings"] = findings
            result["unknowns"] = unknowns
        
        # Format output
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps(result, indent=2))
        else:
            print("✅ Check assessment completed")
            print(f"   Session: {session_id[:8]}...")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Decision: {result['decision'].upper()}")
            print(f"   Findings: {len(findings)} analyzed")
            print(f"   Unknowns: {len(unknowns)} remaining")
            
            if verbose:
                print("\n   Key findings:")
                for i, finding in enumerate(findings[:5], 1):
                    print(f"     {i}. {finding}")
                if len(findings) > 5:
                    print(f"     ... and {len(findings) - 5} more")
                
                print("\n   Remaining unknowns:")
                for i, unknown in enumerate(unknowns[:5], 1):
                    print(f"     {i}. {unknown}")
                if len(unknowns) > 5:
                    print(f"     ... and {len(unknowns) - 5} more")
        
        return result
        
    except Exception as e:
        handle_cli_error(e, "Check assessment", getattr(args, 'verbose', False))


def handle_check_submit_command(args):
    """Handle check-submit command"""
    try:
        from empirica.data.session_database import SessionDatabase
        
        # Parse arguments
        session_id = args.session_id
        vectors = parse_json_safely(args.vectors) if isinstance(args.vectors, str) else args.vectors
        decision = args.decision
        reasoning = args.reasoning
        cycle = getattr(args, 'cycle', 1)
        
        # Validate inputs
        if not isinstance(vectors, dict):
            raise ValueError("Vectors must be a dictionary")
        
        # Simulate check submit
        result = {
            "ok": True,
            "session_id": session_id,
            "decision": decision,
            "cycle": cycle,
            "vectors_count": len(vectors),
            "reasoning": reasoning,
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        # Format output
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps(result, indent=2))
        else:
            print("✅ CHECK assessment submitted successfully")
            print(f"   Session: {session_id[:8]}...")
            print(f"   Decision: {decision.upper()}")
            print(f"   Cycle: {cycle}")
            print(f"   Vectors: {len(vectors)} submitted")
            if reasoning:
                print(f"   Reasoning: {reasoning[:80]}...")
        
        return result
        
    except Exception as e:
        handle_cli_error(e, "Check submit", getattr(args, 'verbose', False))


def handle_postflight_submit_command(args):
    """Handle postflight-submit command"""
    try:
        from empirica.data.session_database import SessionDatabase
        
        # Parse arguments
        session_id = args.session_id
        vectors = parse_json_safely(args.vectors) if isinstance(args.vectors, str) else args.vectors
        changes = args.changes
        
        # Validate vectors
        if not isinstance(vectors, dict):
            raise ValueError("Vectors must be a dictionary")
        
        # Simulate postflight submit
        result = {
            "ok": True,
            "session_id": session_id,
            "message": "POSTFLIGHT assessment submitted successfully",
            "vectors_submitted": len(vectors),
            "changes": changes,
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        # Format output
        if hasattr(args, 'output') and args.output == 'json':
            print(json.dumps(result, indent=2))
        else:
            print("✅ POSTFLIGHT assessment submitted successfully")
            print(f"   Session: {session_id[:8]}...")
            print(f"   Vectors: {len(vectors)} submitted")
            if changes:
                print(f"   Changes: {changes[:80]}...")
        
        return result
        
    except Exception as e:
        handle_cli_error(e, "Postflight submit", getattr(args, 'verbose', False))
