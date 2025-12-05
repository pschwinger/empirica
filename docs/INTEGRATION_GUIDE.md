# Epistemic Validation System - Integration Guide

**Version:** 3.0 (Phase 3)  
**Status:** Production Ready  
**Target:** Developers integrating validation into CASCADE workflows

---

## Overview

The Epistemic Validation System provides **self-healing multi-AI coordination** through three components:

1. **CoherenceValidator** - "Did I do my work honestly?" (self-validation before handoff)
2. **EpistemicRehydration** - "Next AI, here's what I learned" (context inheritance)
3. **HandoffValidator** - "I trust your work because I verified it" (mutual validation)

**Key Principle:** Each AI validates itself and others. No external Sentinel needed.

---

## When to Use Each Component

| Component | Phase | Who Calls | Purpose |
|-----------|-------|-----------|---------|
| **CoherenceValidator** | POSTFLIGHT | Current AI | Validate my work before handoff |
| **HandoffValidator** | PREFLIGHT | Next AI | Validate incoming checkpoint |
| **EpistemicRehydration** | PREFLIGHT | Next AI | Calibrate from previous context |

---

## Integration Pattern 1: POSTFLIGHT Phase (Current AI)

### Before Handing Off to Next AI

After completing POSTFLIGHT assessment, validate your work:

```python
from empirica.core.validation.coherence_validator import CoherenceValidator

# Initialize validator
validator = CoherenceValidator(
    session_id=my_session_id,
    ai_id="claude-code"  # Your AI identifier
)

# Validate before handoff
result = validator.validate_before_handoff(
    preflight_vectors={
        "know": 0.7,
        "do": 0.75,
        "context": 0.65,
        "clarity": 0.8,
        "uncertainty": 0.4,
        # ... all 13 vectors from PREFLIGHT
    },
    postflight_vectors={
        "know": 0.85,
        "do": 0.85,
        "context": 0.8,
        "clarity": 0.9,
        "uncertainty": 0.2,
        # ... all 13 vectors from POSTFLIGHT
    },
    preflight_plan={
        "scope_estimate": "medium",  # What you planned
        "task_description": "Refactor authentication module"
    },
    findings=[
        {
            "key": "jwt_token_design",
            "value": "Refresh tokens with 7-day expiry",
            "domain": "authentication",
            "reasoning": "Security requirements + UX balance",
            "discovered_by": "claude-code",
            "timestamp": 1704067200,
            "certainty": 0.85
        }
    ],
    unknowns=[
        {
            "key": "database_orm_choice",
            "description": "SQLAlchemy vs Tortoise vs Django ORM",
            "domain": "database",
            "impact": "high",
            "discovered_by": "claude-code",
            "timestamp": 1704067200,
            "notes": "3 viable options, needs architecture review"
        }
    ]
)

# Handle validation result
if result['coherent']:
    print(f"✅ {result['message']}")
    # Proceed with handoff - create checkpoint with epistemic_tags
    from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
    
    logger = GitEnhancedReflexLogger(session_id=my_session_id)
    logger.add_checkpoint(
        phase="POSTFLIGHT",
        vectors=postflight_vectors,
        metadata={
            "task": "Authentication refactor",
            "validation": result
        },
        epistemic_tags={
            "findings": findings,
            "unknowns": unknowns,
            "deadends": []  # Optional: approaches that didn't work
        }
    )
else:
    print(f"⚠️ {result['message']}")
    print(f"Concerns: {result['concerns']}")
    
    if result['recommendation'] == 'reenter_check':
        # Return to CHECK phase - investigate further
        print("→ Returning to CHECK phase for additional investigation")
    elif result['recommendation'] == 'reassess':
        # Re-run POSTFLIGHT assessment
        print("→ Re-running POSTFLIGHT assessment")
```

### What Gets Validated

1. **Scope Match:** Did you do what you planned?
2. **Trajectory:** Is your learning progression coherent?
3. **Findings Honesty:** Are your findings appropriately confident?

---

## Integration Pattern 2: PREFLIGHT Phase (Next AI)

### When Receiving a Checkpoint

When resuming from another AI's checkpoint:

```python
from empirica.core.validation.handoff_validator import HandoffValidator
from empirica.core.validation.rehydration import EpistemicRehydration
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger

# Load checkpoint
logger = GitEnhancedReflexLogger(session_id=incoming_session_id)
checkpoint_data = logger.get_latest_checkpoint()

if not checkpoint_data:
    print("No checkpoint found - starting fresh")
    # Run normal PREFLIGHT
else:
    # Step 1: Validate incoming checkpoint
    validator = HandoffValidator(
        session_id=incoming_session_id,
        ai_id="qwen-coder"  # Your AI identifier
    )
    
    validation = validator.validate_handoff(
        checkpoint_data=checkpoint_data,
        previous_ai_id=checkpoint_data.get("ai_id", "unknown")
    )
    
    print(f"📋 Validation result: {validation['message']}")
    
    if validation['should_investigate']:
        print("⚠️ Previous work needs verification:")
        for issue in validation['issues']:
            print(f"  - {issue}")
        print("→ Entering extended CHECK phase before trusting checkpoint")
    
    # Step 2: Rehydrate from findings/unknowns
    rehydrator = EpistemicRehydration(
        session_id=incoming_session_id,
        ai_id="qwen-coder"
    )
    
    # My honest base assessment (before seeing their work)
    my_base_assessment = {
        "know": 0.6,        # My domain knowledge
        "do": 0.75,         # My capability
        "context": 0.5,     # My environmental awareness
        "clarity": 0.7,
        "uncertainty": 0.5
    }
    
    rehydration = rehydrator.rehydrate_from_checkpoint(
        checkpoint_data=checkpoint_data,
        my_knowledge_assessment=my_base_assessment
    )
    
    print(f"📊 Rehydration results:")
    print(f"  Understanding ratio: {rehydration['understanding_ratio']:.2f}")
    print(f"  Confidence boost: +{rehydration['confidence_adjustment']:.2f}")
    print(f"  Inherited findings: {len(rehydration['inherited_findings'])}")
    print(f"  Inherited unknowns: {len(rehydration['inherited_unknowns'])}")
    
    if not rehydration['ready_to_proceed']:
        print(f"⚠️ {rehydration['message']}")
        for warning in rehydration['warnings']:
            print(f"  - {warning}")
    
    # Step 3: Calculate adjusted PREFLIGHT vectors
    adjusted_preflight = rehydrator.calculate_adjusted_preflight(
        checkpoint_data=checkpoint_data,
        my_base_assessment=my_base_assessment
    )
    
    print(f"📈 Adjusted PREFLIGHT:")
    print(f"  KNOW: {my_base_assessment['know']:.2f} → {adjusted_preflight['know']:.2f}")
    print(f"  CONTEXT: {my_base_assessment['context']:.2f} → {adjusted_preflight['context']:.2f}")
    print(f"  UNCERTAINTY: {my_base_assessment['uncertainty']:.2f} → {adjusted_preflight['uncertainty']:.2f}")
    
    # Step 4: Use adjusted vectors for PREFLIGHT
    # Submit PREFLIGHT with calibrated confidence
    from empirica.cli import empirica_cli
    
    empirica_cli.preflight_submit(
        session_id=incoming_session_id,
        vectors=adjusted_preflight,
        reasoning=f"Rehydrated from {checkpoint_data.get('ai_id')}'s checkpoint. "
                 f"Inherited {len(rehydration['inherited_findings'])} findings, "
                 f"{len(rehydration['inherited_unknowns'])} unknowns. "
                 f"Confidence adjusted by +{rehydration['confidence_adjustment']:.2f}"
    )
```

### What Gets Validated

1. **Claim vs Reality:** Does git diff match claimed work?
2. **Findings Credibility:** Do findings make sense given assessment?
3. **Unknowns Reasonableness:** Are remaining unknowns appropriate?
4. **Overall Coherence:** Does checkpoint hang together?

---

## Integration Pattern 3: Complete CASCADE Workflow

### Full Multi-AI Session with Validation

```python
from empirica.core.validation import CoherenceValidator, HandoffValidator, EpistemicRehydration
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger

# ============= AI 1: Initial Work =============

# 1. PREFLIGHT
session_id = create_session(ai_id="claude-code")
preflight_vectors = run_preflight_assessment(session_id, task="Build authentication")

# 2. Work Phase (investigate, plan, act, CHECK cycles)
findings = []
unknowns = []

# ... do work, track findings/unknowns ...

# 3. POSTFLIGHT
postflight_vectors = run_postflight_assessment(session_id)

# 4. Validate before handoff
validator = CoherenceValidator(session_id, ai_id="claude-code")
coherence = validator.validate_before_handoff(
    preflight_vectors=preflight_vectors,
    postflight_vectors=postflight_vectors,
    findings=findings,
    unknowns=unknowns
)

if not coherence['coherent']:
    # Re-enter CHECK phase
    print("Coherence check failed - returning to CHECK")
    # ... re-investigate ...

# 5. Create checkpoint with epistemic_tags
logger = GitEnhancedReflexLogger(session_id)
logger.add_checkpoint(
    phase="POSTFLIGHT",
    vectors=postflight_vectors,
    metadata={"task": "Authentication completed"},
    epistemic_tags={
        "findings": findings,
        "unknowns": unknowns,
        "deadends": []
    }
)

# ============= AI 2: Resume Work =============

# 1. Load checkpoint
checkpoint = logger.get_latest_checkpoint()

# 2. Validate handoff
handoff_validator = HandoffValidator(session_id, ai_id="qwen-coder")
validation = handoff_validator.validate_handoff(checkpoint, previous_ai_id="claude-code")

if validation['should_investigate']:
    print("Extended CHECK phase required")

# 3. Rehydrate context
rehydrator = EpistemicRehydration(session_id, ai_id="qwen-coder")
my_base = {"know": 0.65, "do": 0.7, "context": 0.5, "uncertainty": 0.45}

rehydration = rehydrator.rehydrate_from_checkpoint(checkpoint, my_base)
adjusted_preflight = rehydrator.calculate_adjusted_preflight(checkpoint, my_base)

# 4. Run PREFLIGHT with adjusted vectors
run_preflight_assessment(session_id, vectors=adjusted_preflight)

# 5. Continue work...
```

---

## Error Handling

### Git Diff Failures

If git operations fail, validators gracefully degrade:

```python
result = validator.validate_before_handoff(...)

if result.get('checks', {}).get('scope_match') == "git_error":
    print("⚠️ Git diff unavailable - skipping scope validation")
    # Validator still checks trajectory and findings
```

### Missing Epistemic Tags

Validators handle missing tags gracefully:

```python
# If checkpoint has no epistemic_tags:
checkpoint_data = {
    "phase": "POSTFLIGHT",
    "vectors": {...},
    "epistemic_tags": {}  # Empty - no findings/unknowns
}

# Rehydration works but gives conservative boost
rehydration = rehydrator.rehydrate_from_checkpoint(checkpoint_data, my_base)
# confidence_adjustment will be minimal (0.0-0.05)
```

### Old Checkpoints

When resuming from old checkpoints:

```python
rehydration = rehydrator.rehydrate_from_checkpoint(checkpoint_data, my_base)

if checkpoint_age_hours > 24:
    print("⚠️ Checkpoint is >24 hours old - consider full investigation")
    # Rehydration still works but recommends caution
```

---

## Best Practices

### 1. Always Validate Before Handoff

```python
# ❌ DON'T: Skip validation
logger.add_checkpoint(phase="POSTFLIGHT", vectors=vectors)

# ✅ DO: Always validate first
validator = CoherenceValidator(session_id, ai_id)
result = validator.validate_before_handoff(preflight, postflight, findings, unknowns)
if result['coherent']:
    logger.add_checkpoint(phase="POSTFLIGHT", vectors=vectors, epistemic_tags={...})
```

### 2. Use Epistemic Tags Consistently

```python
# ✅ Good: Structured tags with all fields
finding = {
    "key": "auth_pattern",
    "value": "JWT with refresh tokens",
    "domain": "authentication",
    "reasoning": "Security + UX balance",
    "discovered_by": "claude-code",
    "timestamp": time.time(),
    "certainty": 0.85
}
```

### 3. Rehydrate Before PREFLIGHT

```python
# ✅ DO: Rehydrate first, then run PREFLIGHT
rehydration = rehydrator.rehydrate_from_checkpoint(checkpoint, my_base)
adjusted_preflight = rehydrator.calculate_adjusted_preflight(checkpoint, my_base)
run_preflight(vectors=adjusted_preflight)

# ❌ DON'T: Run PREFLIGHT then try to adjust
run_preflight(vectors=my_base)  # Too late to benefit from context
```

### 4. Handle Validation Failures Gracefully

```python
coherence = validator.validate_before_handoff(...)

if not coherence['coherent']:
    if coherence['recommendation'] == 'reenter_check':
        # More investigation needed
        return_to_check_phase()
    elif coherence['recommendation'] == 'reassess':
        # Re-run assessment
        rerun_postflight_assessment()
```

---

## CLI Integration (Optional)

Validators can be called from CLI:

```bash
# Validate current session before handoff
empirica coherence-validate \
  --session-id abc123 \
  --preflight-vectors preflight.json \
  --postflight-vectors postflight.json

# Validate incoming checkpoint
empirica handoff-validate \
  --session-id abc123 \
  --checkpoint checkpoint.json

# Rehydrate from checkpoint
empirica rehydrate \
  --session-id abc123 \
  --checkpoint checkpoint.json \
  --my-knowledge my_base.json
```

---

## Next Steps

- **Understand validation logic:** See `VALIDATION_LOGIC.md`
- **Learn tag format:** See `SEMANTIC_TAGS.md`
- **Study examples:** See `VALIDATION_EXAMPLES.md`
- **API reference:** See `API_REFERENCE.md`

---

**Questions?** Check `/tmp/self_healing_epistemic_system.md` for design rationale.
