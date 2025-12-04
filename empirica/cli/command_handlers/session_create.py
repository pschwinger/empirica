"""
Session Create Command - Explicit session creation
"""

import json
import sys
from ..cli_utils import handle_cli_error


def handle_session_create_command(args):
    """Create a new session"""
    try:
        from empirica.data.session_database import SessionDatabase
        
        ai_id = args.ai_id
        user_id = getattr(args, 'user_id', None)
        bootstrap_level = getattr(args, 'bootstrap_level', 1)
        output_format = getattr(args, 'output', 'default')
        
        db = SessionDatabase()
        session_id = db.create_session(
            ai_id=ai_id,
            bootstrap_level=bootstrap_level,
            components_loaded=6  # Standard component count
        )
        db.close()
        
        if output_format == 'json':
            result = {
                "ok": True,
                "session_id": session_id,
                "ai_id": ai_id,
                "user_id": user_id,
                "bootstrap_level": bootstrap_level,
                "message": "Session created successfully"
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"✅ Session created successfully!")
            print(f"   📋 Session ID: {session_id}")
            print(f"   🤖 AI ID: {ai_id}")
            print(f"   📊 Bootstrap Level: {bootstrap_level}")
            print(f"\nNext steps:")
            print(f"   empirica preflight --session-id {session_id} --prompt \"Your task\"")
        
    except Exception as e:
        if getattr(args, 'output', 'default') == 'json':
            print(json.dumps({"ok": False, "error": str(e)}, indent=2))
        else:
            print(f"❌ Failed to create session: {e}")
        handle_cli_error(e, "Session create", getattr(args, 'verbose', False))
        sys.exit(1)
