#!/usr/bin/env python3
"""
Empirica Bootstrap - Simplified Session Creation

Creates a session in the database for tracking epistemic work.
Components (assessor, cascade, orchestrator) are created on-demand by MCP/CLI tools.

This is a convenience wrapper - MCP tools can auto-create sessions if preferred.
"""

from typing import Optional
from empirica.data.session_database import SessionDatabase


def bootstrap_session(
    ai_id: str,
    level: str = "standard",
    session_type: str = "development"
) -> str:
    """
    Create an Empirica session.
    
    Args:
        ai_id: AI identifier
        level: Bootstrap level (minimal, standard, complete) - stored as metadata
        session_type: Session type (development, production, research)
        
    Returns:
        session_id: UUID of created session
        
    Note:
        Components (CanonicalEpistemicAssessor, GoalOrchestrator, etc) are created
        on-demand by MCP tools and CLI commands. No pre-loading needed.
    """
    # Normalize level
    level_map = {"0": "minimal", "1": "standard", "2": "complete", "3": "complete", "4": "complete"}
    if level in level_map:
        level = level_map[level]
    
    # Valid levels
    if level not in ["minimal", "standard", "extended", "complete"]:
        level = "standard"
    
    # Create session
    db = SessionDatabase()
    session_id = db.create_session(
        ai_id=ai_id,
        bootstrap_level=level,
        components_loaded=0  # Components created on-demand
    )
    
    # Print confirmation
    print(f"🚀 Empirica session created")
    print(f"   Session ID: {session_id}")
    print(f"   AI ID: {ai_id}")
    print(f"   Level: {level}")
    print(f"   Type: {session_type}")
    print()
    print("💡 Components created on-demand by MCP/CLI tools")
    
    db.close()
    return session_id


# Alias for backwards compatibility
def bootstrap_metacognition(ai_id: str, level: str = "standard", **kwargs) -> str:
    """
    Alias for bootstrap_session (backwards compatibility).
    
    Legacy function signature - redirects to simplified bootstrap.
    """
    return bootstrap_session(ai_id=ai_id, level=level, session_type=kwargs.get("session_type", "development"))


class OptimalMetacognitiveBootstrap:
    """
    Legacy class wrapper for backwards compatibility.
    
    Just creates session - components created on-demand.
    """
    
    def __init__(self, ai_id: str, level: str = "standard", **kwargs):
        self.ai_id = ai_id
        self.level = level
        self.session_id = None
    
    def bootstrap(self):
        """Create session and return empty components dict for compatibility"""
        self.session_id = bootstrap_session(ai_id=self.ai_id, level=self.level)
        # Return empty dict for backwards compatibility (components created on-demand)
        return {"session_id": self.session_id}
    
    def bootstrap_minimal(self):
        """Alias for bootstrap()"""
        return self.bootstrap()
    
    def bootstrap_standard(self):
        """Alias for bootstrap()"""
        return self.bootstrap()
    
    def bootstrap_full(self):
        """Alias for bootstrap()"""
        return self.bootstrap()


class ExtendedMetacognitiveBootstrap(OptimalMetacognitiveBootstrap):
    """
    Legacy extended bootstrap - now identical to optimal.
    
    Kept for backwards compatibility only.
    """
    pass


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Empirica Bootstrap")
    parser.add_argument('--ai-id', default='test_ai', help='AI identifier')
    parser.add_argument('--level', default='standard', help='Bootstrap level')
    args = parser.parse_args()
    
    session_id = bootstrap_session(ai_id=args.ai_id, level=args.level)
    print(f"✅ Session ready: {session_id}")
