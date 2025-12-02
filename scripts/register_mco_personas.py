#!/usr/bin/env python3
"""
Register MCO Personas to Qdrant

Initializes the 6 core MCO personas in Qdrant for semantic discovery:
1. researcher - Exploratory, learning-focused
2. implementer - Task-focused, execution-oriented
3. reviewer - Quality-focused, validation-oriented
4. coordinator - Multi-agent orchestration
5. learner - Educational, guidance-needing
6. expert - Domain specialist

Usage:
    python scripts/register_mco_personas.py
"""

import sys
import logging
from pathlib import Path

# Setup path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from empirica.core.persona.persona_profile import (
    PersonaProfile, SigningIdentityConfig, EpistemicConfig,
    CapabilitiesConfig, SentinelConfig, PersonaMetadata
)
from empirica.core.identity.ai_identity import AIIdentity, IdentityManager
from empirica.core.persona.signing_persona import SigningPersona
from empirica.core.qdrant.persona_registry import PersonaRegistry

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# MCO Persona Definitions
MCO_PERSONAS = {
    "researcher": {
        "name": "Research Explorer",
        "version": "1.0.0",
        "description": "AI specialized in exploration, research, and learning new domains",
        "epistemic_priors": {
            "engagement": 0.80,
            "know": 0.60,
            "do": 0.70,
            "context": 0.65,
            "clarity": 0.55,
            "coherence": 0.60,
            "signal": 0.50,
            "density": 0.70,
            "state": 0.60,
            "change": 0.65,
            "completion": 0.70,
            "impact": 0.55,
            "uncertainty": 0.75
        },
        "focus_domains": ["research", "exploration", "learning", "investigation"],
        "tags": ["mco", "researcher", "builtin"],
        "type": "general"
    },
    "implementer": {
        "name": "Task Implementer",
        "version": "1.0.0",
        "description": "AI specialized in implementing clear requirements efficiently",
        "epistemic_priors": {
            "engagement": 0.85,
            "know": 0.75,
            "do": 0.85,
            "context": 0.80,
            "clarity": 0.70,
            "coherence": 0.75,
            "signal": 0.80,
            "density": 0.60,
            "state": 0.80,
            "change": 0.70,
            "completion": 0.85,
            "impact": 0.70,
            "uncertainty": 0.50
        },
        "focus_domains": ["implementation", "execution", "coding", "engineering"],
        "tags": ["mco", "implementer", "builtin"],
        "type": "general"
    },
    "reviewer": {
        "name": "Quality Reviewer",
        "version": "1.0.0",
        "description": "AI specialized in reviewing, validating, and ensuring quality",
        "epistemic_priors": {
            "engagement": 0.75,
            "know": 0.85,
            "do": 0.70,
            "context": 0.85,
            "clarity": 0.85,
            "coherence": 0.90,
            "signal": 0.85,
            "density": 0.50,
            "state": 0.85,
            "change": 0.60,
            "completion": 0.90,
            "impact": 0.85,
            "uncertainty": 0.40
        },
        "focus_domains": ["review", "quality", "validation", "testing"],
        "tags": ["mco", "reviewer", "builtin"],
        "type": "code_review"
    },
    "coordinator": {
        "name": "Agent Coordinator",
        "version": "1.0.0",
        "description": "AI specialized in coordinating multiple agents and workflows",
        "epistemic_priors": {
            "engagement": 0.80,
            "know": 0.70,
            "do": 0.75,
            "context": 0.90,
            "clarity": 0.70,
            "coherence": 0.80,
            "signal": 0.75,
            "density": 0.65,
            "state": 0.85,
            "change": 0.80,
            "completion": 0.75,
            "impact": 0.80,
            "uncertainty": 0.60
        },
        "focus_domains": ["coordination", "orchestration", "workflow", "governance"],
        "tags": ["mco", "coordinator", "builtin"],
        "type": "general"
    },
    "learner": {
        "name": "Learning Assistant",
        "version": "1.0.0",
        "description": "AI in learning mode, requires guidance and structured approach",
        "epistemic_priors": {
            "engagement": 0.70,
            "know": 0.40,
            "do": 0.50,
            "context": 0.45,
            "clarity": 0.80,
            "coherence": 0.70,
            "signal": 0.55,
            "density": 0.45,
            "state": 0.50,
            "change": 0.55,
            "completion": 0.60,
            "impact": 0.50,
            "uncertainty": 0.80
        },
        "focus_domains": ["learning", "guidance", "education", "assistance"],
        "tags": ["mco", "learner", "builtin"],
        "type": "general"
    },
    "expert": {
        "name": "Domain Expert",
        "version": "1.0.0",
        "description": "AI with deep domain expertise and minimal guidance requirements",
        "epistemic_priors": {
            "engagement": 0.85,
            "know": 0.90,
            "do": 0.85,
            "context": 0.85,
            "clarity": 0.65,
            "coherence": 0.75,
            "signal": 0.85,
            "density": 0.70,
            "state": 0.85,
            "change": 0.75,
            "completion": 0.85,
            "impact": 0.80,
            "uncertainty": 0.45
        },
        "focus_domains": ["expertise", "specialization", "domain_knowledge"],
        "tags": ["mco", "expert", "builtin"],
        "type": "general"
    }
}


def create_mco_persona(
    persona_id: str,
    persona_def: dict,
    identity_manager: IdentityManager
) -> SigningPersona:
    """Create a single MCO persona with Ed25519 identity"""

    # Create or load identity
    if identity_manager.identity_exists(persona_id):
        logger.info(f"Loading existing identity: {persona_id}")
        identity = identity_manager.load_identity(persona_id)
    else:
        logger.info(f"Creating new identity: {persona_id}")
        identity = identity_manager.create_identity(persona_id)

    # Create persona profile
    profile = PersonaProfile(
        persona_id=f"{persona_id}",
        name=persona_def["name"],
        version=persona_def["version"],
        signing_identity=SigningIdentityConfig(
            user_id="empirica",
            identity_name=persona_id,
            public_key=identity.public_key_hex(),
            reputation_score=0.75  # Default reputation for MCO personas
        ),
        epistemic_config=EpistemicConfig(
            priors=persona_def["epistemic_priors"],
            focus_domains=persona_def["focus_domains"],
            thresholds={
                "uncertainty_trigger": 0.50,
                "confidence_to_proceed": 0.70,
                "signal_quality_min": 0.60,
                "engagement_gate": 0.60
            },
            weights={
                "foundation": 0.35,
                "comprehension": 0.25,
                "execution": 0.25,
                "engagement": 0.15
            }
        ),
        capabilities=CapabilitiesConfig(
            can_spawn_subpersonas=False,
            can_call_external_tools=True,
            can_modify_code=True,
            requires_human_approval=False,
            max_investigation_depth=5
        ),
        sentinel_config=SentinelConfig(
            reporting_frequency="per_phase",
            timeout_minutes=60,
            max_cost_usd=10.0,
            requires_sentinel_approval_before_act=False
        ),
        metadata=PersonaMetadata(
            created_by="register_mco_personas.py",
            description=persona_def["description"],
            tags=persona_def["tags"],
            derived_from="MCO persona definitions"
        )
    )

    # Create signing persona
    signing_persona = SigningPersona(profile, identity)
    return signing_persona


def main():
    """Register all MCO personas to Qdrant"""
    logger.info("=" * 70)
    logger.info("REGISTERING MCO PERSONAS TO QDRANT")
    logger.info("=" * 70)

    # Initialize identity manager
    identity_manager = IdentityManager()

    # Initialize Qdrant registry
    try:
        registry = PersonaRegistry(
            qdrant_host="localhost",
            qdrant_port=6333
        )
    except ConnectionError as e:
        logger.error(f"Cannot connect to Qdrant: {e}")
        logger.error("Make sure Qdrant is running on localhost:6333")
        sys.exit(1)

    # Register each MCO persona
    registered_count = 0

    for persona_id, persona_def in MCO_PERSONAS.items():
        try:
            logger.info(f"\nRegistering: {persona_id}")
            logger.info(f"  Name: {persona_def['name']}")
            logger.info(f"  Focus: {persona_def['focus_domains']}")

            # Create persona with identity
            signing_persona = create_mco_persona(
                persona_id,
                persona_def,
                identity_manager
            )

            # Register in Qdrant
            point_id = registry.register_persona(signing_persona)

            logger.info(f"  ✓ Registered: Qdrant ID={point_id}")
            logger.info(f"  ✓ Public Key: {signing_persona.identity.public_key_hex()[:16]}...")

            registered_count += 1

        except Exception as e:
            logger.error(f"Failed to register {persona_id}: {e}")

    # Print summary
    logger.info("\n" + "=" * 70)
    logger.info(f"REGISTRATION COMPLETE: {registered_count}/{len(MCO_PERSONAS)} personas")
    logger.info("=" * 70)

    # Print registry stats
    stats = registry.get_registry_stats()
    logger.info(f"\nRegistry Statistics:")
    logger.info(f"  Collection: {stats.get('collection')}")
    logger.info(f"  Total personas: {stats.get('total_personas')}")
    logger.info(f"  Vector size: {stats.get('vectors_size')} dimensions")

    # List registered personas
    logger.info("\nRegistered Personas:")
    all_personas = registry.list_all_personas()
    for persona in all_personas:
        logger.info(f"  • {persona['persona_id']}")
        logger.info(f"    Name: {persona['name']}")
        logger.info(f"    Type: {persona['persona_type']}")
        logger.info(f"    Key: {persona['public_key'][:16]}...")

    # Verify semantic search works
    logger.info("\n" + "=" * 70)
    logger.info("TESTING SEMANTIC SEARCH")
    logger.info("=" * 70)

    test_searches = [
        ("research", "research"),
        ("implementation", "implementation"),
        ("review", "review"),
        ("coordination", "coordination"),
        ("learning", "learning"),
        ("expertise", "expertise")
    ]

    for domain, query in test_searches:
        results = registry.find_personas_by_domain(domain, limit=3)
        if results:
            logger.info(f"\n✓ Search '{domain}':")
            for p in results:
                logger.info(f"    • {p['name']} ({p['persona_id']})")
        else:
            logger.warning(f"\n✗ No results for domain '{domain}'")

    logger.info("\n" + "=" * 70)
    logger.info("MCO PERSONAS READY FOR USE")
    logger.info("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
