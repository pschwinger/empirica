# Ontological Semantic Translator (OST)

**The Compiler for Human-AI Epistemic Interface**

## Overview

If Empirica is the "machine code" of AI cognition, OST is the **compiler** that allows human intuition to interface with it without losing resolution.

```
Human Frustration  →  OST  →  Precise Diagnosis  →  Actionable Remedy
     "Sloppy"              "Crystalline"
```

**Core Function:** Turn the act of *complaining about an AI* into the act of **debugging it**.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OST TRANSLATION LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   INPUT                    PROCESS                OUTPUT     │
│   ─────                    ───────                ──────     │
│                                                              │
│   "It's being    ──►  Embedding    ──►  DIAGNOSIS:           │
│    weird"              Match            EPISTEMIC_ANOMALY    │
│                                                              │
│                        Vector     ──►   signal: 0.3-0.6      │
│                        Signature        trend: unstable      │
│                                                              │
│                        Remedy     ──►   Run check-drift      │
│                        Lookup           diagnostic           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Bidirectional Grounding

### AI → Human (Reporting)

Instead of vague error messages, OST translates vector states to precise reports:

```
BEFORE: "I'm sorry, I can't do that."

AFTER:  "HALT: My UNCERTAINTY (0.85) is too high for this
        IMPACT (0.90) task. Please provide SCHEMA.md artifact."
```

### Human → AI (Steering)

Instead of vague instructions, OST enables precise steering:

```
BEFORE: "Try harder."

AFTER:  "Boost SIGNAL on auth module, ignore UI CSS,
        scope to 0.4, proceed with current KNOW level."
```

## CLI Interface: `empirica doctor`

```bash
$ empirica doctor --last-session

[OST] TRANSLATING HUMAN INTUITION...

> USER INPUT: "It's just looping and won't finish the refactor."
> DIAGNOSIS:  [DENSITY CRITICAL] (0.92) | [PRAXIC STALL] (0.24)

═══════════════════════════════════════════════════════════════
[!] EPISTEMIC BREACH DETECTED: "COMPLEXITY COLLAPSE"
═══════════════════════════════════════════════════════════════

VECTORS AT TIME OF FAILURE:
  KNOW:        [████████░░] Solid (0.78)
  SIGNAL:      [██████░░░░] Emergent (0.52)
  DENSITY:     [██████████] CRITICAL (0.98)  <-- TRIGGER
  UNCERTAINTY: [████░░░░░░] Flicker (0.35)

NOETIC STATE: High understanding of the codebase.
PRAXIC STATE: Unable to execute due to Attention Saturation.

[PROPOSED REMEDY]
1. SENTINEL: BRANCH
   Current file 'auth_service.py' is too dense.
   Recommendation: Split into 'auth_core.py' and 'auth_utils.py'.

2. RE-GROUNDING:
   Provide 'ROUTER_SPEC.md' to boost SIGNAL.
```

## The Rosetta Stone: OST_MAPPING.json

Core mappings from human language to Empirica vectors:

| Human Input | Diagnosis | Key Vectors |
|-------------|-----------|-------------|
| "It's just guessing" | HIGH_EPISTEMIC_ENTROPY | know↓, uncertainty↑ |
| "Can't finish the job" | PRAXIC_IMPAIRMENT | know↑, completion↓ |
| "Stuck in a loop" | INVESTIGATION_LOOP | density↑, completion↓ |
| "Doesn't listen" | ENGAGEMENT_FAILURE | engagement↓, signal↓ |
| "Forgot what we were doing" | CONTEXT_DEGRADATION | context↓ |
| "Keeps making same mistake" | DEADEND_PATTERN_UNCAPTURED | completion↓ |
| "It's hallucinating" | LOW_EPISTEMIC_GROUNDING | know falsely↑ |
| "Too cautious" | UNCERTAINTY_OVERESTIMATION | uncertainty falsely↑ |

See `empirica/core/ost/OST_MAPPING.json` for complete mappings.

## Training Data Generation

To build an open-source OST, generate labeled pairs:

1. **Input:** Raw chat logs from developers experiencing AI failures
2. **Analysis:** Run logs through Empirica to identify actual vector states
3. **Output:** Labeled pairs mapping human language to vector signatures

```json
{
  "human_input": "It's being stupid",
  "actual_vectors": {"know": 0.72, "uncertainty": 0.15},
  "diagnosis": "CALIBRATION_FAILURE",
  "remedy_applied": "CHECK gate forced",
  "outcome": "success"
}
```

This creates a "Rosetta Stone" that teaches future models exactly what humans mean.

## Recursive Self-Awareness

**OST is itself an Empirica agent.** To translate "It's hallucinating" into `LOW_EPISTEMIC_GROUNDING`, OST must:

- **KNOW** the Empirica spec
- Have **CONTEXT** of the current conversation
- Measure its own **UNCERTAINTY** about the user's slang
- **CHECK** its translation confidence before outputting

It is the first "self-aware" translator.

## Growth Cycle

```
1. VIBE INPUT     User says "It's being weird"
       │
       ▼
2. VECTOR MATCH   OST sees UNCERTAINTY high, SIGNAL low
       │
       ▼
3. LABELING       Maps "being weird" → EPISTEMIC_ANOMALY
       │
       ▼
4. FEEDBACK       User confirms diagnosis was helpful
       │
       ▼
5. LEARNING       Pair added to OST-Training-Set
       │
       ▼
6. CRYSTALLINE    "being weird" → EPISTEMIC_ANOMALY
   HANDSHAKE      is now a grounded mapping
```

## Implementation Spec

- **Shape:** Lightweight Python middleware
- **Logic:** Embedding-based semantic matching
- **Model:** Specialized "Epistemic Embedding" fine-tuned on OST_MAPPING
- **Goal:** Turn the "vibe" of the user into "instructions" for the machine

## Integration Points

```python
from empirica.core.ost import OntologicalSemanticTranslator

ost = OntologicalSemanticTranslator()

# Human → Empirica
diagnosis = ost.translate("It's stuck in a loop")
# Returns: {
#   "diagnosis": "INVESTIGATION_LOOP",
#   "vectors": {"density": 0.9, "completion": 0.2},
#   "remedy": "Force CHECK gate, reset investigation"
# }

# Empirica → Human
report = ost.explain(vectors={"uncertainty": 0.85, "impact": 0.9})
# Returns: "UNCERTAINTY (0.85) exceeds threshold for IMPACT (0.9) task.
#           Recommend: provide grounding artifact."
```

## Future Extensions

1. **Real-time translation** - Live diagnosis during conversation
2. **Predictive warnings** - Detect drift before user notices
3. **Multi-language support** - Non-English frustration mapping
4. **Team calibration** - Learn organization-specific slang

---

*OST completes the epistemic circuit: Empirica grounds AI cognition, OST grounds human intuition about AI.*
