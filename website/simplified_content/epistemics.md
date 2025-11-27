# Epistemics: The Foundation

**Why measuring what AIs know—and don't know—is critical.**

---

## The 13 Epistemic Vectors

Empirica measures AI knowledge state across **13 dimensions** to ensure genuine self-awareness.

<!-- BENTO_START -->

## 🚪 Gate: ENGAGEMENT
**Must pass (≥0.60) to proceed.**

Verifies meaningful task understanding.
- **Clarity:** Does AI understand the ask?
- **Relevance:** Is it capable?
- **Readiness:** Is it prepared?

## 🏗️ Foundation
**Core knowledge (35% weight).**

- **KNOW:** Domain knowledge confidence.
- **DO:** Execution capability.
- **CONTEXT:** Environmental awareness.

## 🔮 Meta: UNCERTAINTY
**"Know what you don't know".**

Explicitly tracks unknowns.
- **Low (<0.3):** Confident, few unknowns.
- **High (>0.7):** Significant gaps -> **INVESTIGATE**.

<!-- BENTO_END -->

---

## Detailed Breakdown

### Comprehension (25%)
- **CLARITY:** Task semantic understanding.
- **COHERENCE:** Logical consistency (Critical < 0.5 -> RESET).
- **SIGNAL:** Information quality ratio.
- **DENSITY:** Cognitive load (Critical > 0.9 -> RESET).

### Execution (25%)
- **STATE:** Current readiness.
- **CHANGE:** Progress tracking (Critical < 0.5 -> STOP).
- **COMPLETION:** Goal proximity.
- **IMPACT:** Consequence awareness.

---

## Calibration: The Differentiator

**PREFLIGHT vs POSTFLIGHT** comparison measures learning.

```
PREFLIGHT:   KNOW: 0.35, UNCERTAINTY: 0.75
↓ [INVESTIGATE] ↓
POSTFLIGHT:  KNOW: 0.90, UNCERTAINTY: 0.15

Result: +0.55 Knowledge Gain, -0.60 Uncertainty Reduction.
```

We measure **Epistemic Delta**, not just final confidence.

---

## Critical Thresholds

Safety rails to prevent unsafe operation:

| Threshold | Value | Consequence |
|-----------|-------|-------------|
| **ENGAGEMENT** | < 0.60 | Stop (Clarify) |
| **COHERENCE** | < 0.50 | Reset (Incoherent) |
| **DENSITY** | > 0.90 | Reset (Overload) |
| **UNCERTAINTY** | > 0.80 | Investigate |

---

**Next Steps:**
- [Cross-AI Collaboration](developers/collaboration.md)
- [AI vs Agent Patterns](ai_vs_agent.md)
- [Architecture](developers/architecture.md)
