"""
Empirica Phase 3: Multi-Persona Epistemic Intelligence

This module implements specialized AI personas with:
- Epistemic priors (domain-specific starting knowledge)
- Custom thresholds and weights
- Cryptographic signing (Phase 2 integration)
- Sentinel orchestration
- Parallel CASCADE execution
- Epistemic composition (COMPOSE operation)

Components:
- PersonaProfile: Persona configuration and validation
- PersonaManager: Create, load, validate personas
- PersonaHarness: Runtime container for persona execution
- SentinelOrchestrator: Manages multi-persona coordination
- Protocol: Persona <-> Sentinel communication

Usage:
    from empirica.core.persona import PersonaProfile, PersonaManager

    # Create security expert persona
    profile = PersonaProfile(
        persona_id="security_expert",
        name="Security Expert",
        epistemic_priors={"know": 0.90, "uncertainty": 0.15},
        focus_domains=["security", "vulnerabilities"]
    )

    manager = PersonaManager()
    manager.save_persona(profile)
"""

from .persona_profile import PersonaProfile, EpistemicConfig, SigningIdentityConfig
from .persona_manager import PersonaManager
from .validation import validate_persona_profile, ValidationError

__all__ = [
    'PersonaProfile',
    'EpistemicConfig',
    'SigningIdentityConfig',
    'PersonaManager',
    'validate_persona_profile',
    'ValidationError'
]

__version__ = '3.0.0'  # Phase 3
