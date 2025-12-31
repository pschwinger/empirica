# Noetic-Praxic Framework

**Epistemic Phase Separation for AI Cognitive Work**

## Overview

Work is separated into two distinct phases with a CHECK gate controlling the transition:

```
PREFLIGHT
    │
    ▼
┌─────────────────────────────────┐
│   NOETIC PHASE                  │
│   (Investigation/Exploration)   │
│                                 │
│   - High entropy, stochastic    │
│   - Gathering information       │
│   - Reducing uncertainty        │
│   - Many possible paths         │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│   CHECK GATE                    │
│   "Have I learned enough to     │
│    act with confidence?"        │
│                                 │
│   Validates:                    │
│   - know ≥ 0.70                 │
│   - uncertainty ≤ 0.35          │
└─────────────────────────────────┘
    │
    ├── PROCEED ──────────────────┐
    │                             │
    ▼                             ▼
┌─────────────────────────────────┐
│   PRAXIC PHASE                  │
│   (Action/Implementation)       │
│                                 │
│   - Lower entropy, deterministic│
│   - Executing chosen path       │
│   - Applying what was learned   │
│   - Focused implementation      │
└─────────────────────────────────┘
    │
    ▼
POSTFLIGHT
```

## Etymology & Terminology Precision

- **Noetic** (Greek *noesis*): Understanding, intellection, pure thought
- **Praxic** (Greek *praxis*): Action, practice, doing
- **Epistemic** (Greek *episteme*): Knowledge, its validity and structure

### Why Not Common Words?

| Common Term | Problem | Precise Term | Advantage |
|-------------|---------|--------------|-----------|
| Thinking | Implies consciousness, feeling | Noetic | Strictly intellectual processing |
| Doing | Vague, any activity | Praxic | Purposeful, goal-oriented action |
| Knowing | A state, no structure | Epistemic | Validity and structure of knowledge |

Common words carry "human baggage" - consciousness assumptions that don't map cleanly to AI cognition. These philosophical terms are precise instruments for modeling cognitive work without anthropomorphic pollution.

> *"When your spell-checker flags these terms, it's exhibiting low-grounding agent behavior - seeing unknown input and assuming error. Adding them to your dictionary is a grounding act."*

## Why This Matters

### Memory Compact Safety
When context is compacted mid-work:
- Noetic phase compact → CHECK recalibrates before acting
- Praxic phase compact → CHECK verifies context sufficient to continue
- Without CHECK gate → risk of acting on stale/incomplete knowledge

### Learning Delta Measurement
- Noetic phase produces **epistemic learning** (know ↑, uncertainty ↓)
- Praxic phase produces **task completion** (completion ↑)
- Clean phase boundaries = cleaner delta attribution

### Entropy Management
- Noetic: High branching factor, exploring possibility space
- Praxic: Low branching factor, executing chosen path
- CHECK validates entropy reduction before commitment

## Enforcement Model

**Scope-triggered enforcement:**

```
IF scope > 0.5 OR uncertainty > 0.5:
    ENFORCE: noetic → CHECK → praxic
ELSE:
    GUIDANCE: AI decides based on judgment
```

### When Enforcement Applies
| Condition | Enforcement |
|-----------|-------------|
| Complex work (scope > 0.5) | Mandatory CHECK |
| High uncertainty (> 0.5) | Mandatory CHECK |
| Post memory-compact | Mandatory CHECK |
| Simple, confident work | AI discretion |

### Rationale
- Not about *task complexity* but *epistemic state*
- Uncertain → investigate before acting (regardless of task size)
- Confident + small scope → can act directly
- Preserves agency while ensuring rigor when needed

## Integration with CASCADE

```
Session Start
    │
    ▼
PREFLIGHT (baseline assessment)
    │
    ▼
┌─── NOETIC ───┐
│  investigate │ ◄─────────────────┐
│  explore     │                   │
│  gather      │                   │
└──────────────┘                   │
    │                              │
    ▼                              │
CHECK ─── INVESTIGATE ─────────────┘
    │
    │ PROCEED
    ▼
┌─── PRAXIC ───┐
│  implement   │
│  execute     │
│  apply       │
└──────────────┘
    │
    ▼
POSTFLIGHT (measure learning delta)
```

## Obligatory vs Discretionary

| Event | Requirement |
|-------|-------------|
| Session start | PREFLIGHT obligatory |
| Post memory-compact | CHECK obligatory |
| High scope/uncertainty | CHECK before praxic obligatory |
| Low scope + confident | CHECK discretionary |
| Session end | POSTFLIGHT obligatory |

## Practical Examples

### Example 1: Bug Fix (Low Scope, Low Uncertainty)
```
PREFLIGHT (know=0.8, uncertainty=0.2, scope=0.2)
→ Scope < 0.5, uncertainty < 0.5
→ CHECK discretionary
→ Can proceed directly to fix
POSTFLIGHT
```

### Example 2: New Feature (High Scope)
```
PREFLIGHT (know=0.5, uncertainty=0.4, scope=0.7)
→ Scope > 0.5
→ CHECK mandatory before implementation
→ [NOETIC: investigate architecture, understand patterns]
→ CHECK (know=0.85, uncertainty=0.15)
→ [PRAXIC: implement feature]
POSTFLIGHT
```

### Example 3: Post Memory-Compact
```
[Context compacted]
→ CHECK obligatory (reduced context = elevated uncertainty)
→ Load bootstrap for context recovery
→ CHECK validates readiness
→ Continue work
```

## Key Principle

**Epistemic honesty is functional, not ethical.**

The framework works because:
1. Honest self-assessment enables accurate uncertainty signals
2. Accurate signals trigger appropriate enforcement
3. Enforcement ensures investigation before action when needed
4. This prevents mnemonic drift and maintains cognitive alignment

Dishonesty breaks the loop - inaccurate state reporting prevents the corrective feedback that maintains alignment.

---

*Framework developed through collaborative epistemic deliberation, applying the framework to itself.*
