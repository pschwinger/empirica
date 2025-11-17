# Multi-Agent Checkpoint Strategy

**Date:** 2025-11-16  
**Status:** Architectural Design

---

## Your Questions Answered

### Q1: Does the agent check its uncertainty at each checkpoint?

**YES!** Every checkpoint captures **all 13 epistemic vectors**, including uncertainty:

```json
{
  "session_id": "agent-alpha-123",
  "phase": "CHECK",
  "round": 3,
  "vectors": {
    "know": 0.85,
    "do": 0.90,
    "context": 0.88,
    "clarity": 0.82,
    "coherence": 0.87,
    "signal": 0.79,
    "density": 0.65,
    "state": 0.83,
    "change": 0.81,
    "completion": 0.72,
    "impact": 0.76,
    "engagement": 0.92,
    "uncertainty": 0.25  ← TRACKED!
  },
  "overall_confidence": 0.877,
  "meta": {
    "confidence_to_proceed": 0.88
  }
}
```

**What this means:**
- ✅ Uncertainty trajectory is tracked across the session
- ✅ Each checkpoint shows epistemic state at that moment
- ✅ Can detect if uncertainty is increasing (bad) or decreasing (good)
- ✅ Multi-agent handoffs can read uncertainty levels

---

### Q2: How do we manage multi-agent sessions?

You're already doing it right with **git branches**! Here's the full strategy:

---

## Multi-Agent Session Strategy

### Approach A: Shared Session (Sequential Handoff)

**Use case:** Agents work on same task sequentially (relay race)

```
Agent A (Claude Code):
├─ PREFLIGHT (session_abc123, branch: main)
├─ INVESTIGATE (5 rounds)
├─ CHECK (confidence: 0.85)
├─ Create checkpoint → Git note on main branch
└─ Handoff to Agent B

Agent B (Qwen Coder):
├─ Load checkpoint from main branch
├─ Continue ACT phase
├─ Create checkpoint → Git note on main branch
└─ Handoff to Agent C

Agent C (Minimax):
├─ Load checkpoint from main branch
├─ POSTFLIGHT (measure total learning)
└─ Session complete
```

**Session ownership:** Shared session ID, sequential ownership

**PREFLIGHT/POSTFLIGHT:**
- **First agent:** Runs PREFLIGHT (baseline)
- **Middle agents:** Resume from checkpoint (no PREFLIGHT)
- **Last agent:** Runs POSTFLIGHT (measures total delta)

**Git strategy:**
```bash
# All agents work on main branch
main: A-checkpoint → B-checkpoint → C-checkpoint
```

---

### Approach B: Parallel Sessions (Git Branches)

**Use case:** Agents work independently, then merge (your current approach)

```
Agent A (branch: agent-a):
├─ PREFLIGHT (session_a, branch: agent-a)
├─ INVESTIGATE
├─ ACT (implement feature X)
├─ POSTFLIGHT
└─ Create checkpoint → Git note on agent-a branch

Agent B (branch: agent-b):
├─ PREFLIGHT (session_b, branch: agent-b)
├─ INVESTIGATE
├─ ACT (implement feature Y)
├─ POSTFLIGHT
└─ Create checkpoint → Git note on agent-b branch

Sentinel (orchestrator):
├─ Read checkpoints from both branches
├─ Analyze epistemic deltas:
│  - Agent A: know 0.4→0.9 (+0.5)
│  - Agent B: know 0.5→0.92 (+0.42)
├─ Merge branches
└─ Create combined POSTFLIGHT
```

**Session ownership:** Each agent has its own session ID

**PREFLIGHT/POSTFLIGHT:**
- **Each agent:** Runs its own PREFLIGHT + POSTFLIGHT
- **Sentinel:** Aggregates results, measures combined learning

**Git strategy:**
```bash
# Each agent gets a branch
main
├─ agent-a: A-preflight → A-checkpoint → A-postflight
└─ agent-b: B-preflight → B-checkpoint → B-postflight

# Merge creates combined state
main (merged): Combined epistemic state
```

---

### Approach C: Hybrid (Parallel + Handoff)

**Use case:** Parallel work, then sequential refinement

```
Phase 1: Parallel Investigation
├─ Agent A (branch: agent-a, session_a)
│  └─ INVESTIGATE architecture
└─ Agent B (branch: agent-b, session_b)
   └─ INVESTIGATE security

Phase 2: Sequential Implementation
├─ Sentinel merges findings → session_shared (branch: main)
├─ Agent C resumes session_shared
│  └─ ACT on combined insights
└─ Agent D resumes session_shared
   └─ POSTFLIGHT final verification
```

**Session ownership:** Parallel → Shared

---

## Checkpoint Isolation Strategy

### Git Branch Isolation (Current Approach)

```bash
# Agent A sandbox (branch: agent-a)
git checkout -b agent-a
empirica bootstrap --session-id agent-a-session
empirica preflight "Implement OAuth2"
# Work happens...
empirica checkpoint-create --phase ACT
git add . && git commit -m "Agent A checkpoint"

# Checkpoint stored in git note on agent-a branch
git notes --ref=empirica-checkpoints list HEAD
```

**Advantages:**
- ✅ Full isolation (agents can't interfere)
- ✅ Easy rollback (git branch management)
- ✅ Clear audit trail (git log + git notes)
- ✅ Parallel work without conflicts

**How checkpoints work:**
```bash
# Git notes are branch-specific
agent-a branch: 
  commit abc123 → git note: {checkpoint for agent A}

agent-b branch:
  commit def456 → git note: {checkpoint for agent B}

# Merge branches → combine checkpoints
main branch (merged):
  commit abc123 (from A) → git note: {checkpoint for agent A}
  commit def456 (from B) → git note: {checkpoint for agent B}
```

---

## Multi-Agent Uncertainty Management

### Tracking Uncertainty Across Handoffs

**Scenario:** Agent A → Agent B handoff

```python
# Agent A creates checkpoint
checkpoint_a = {
    "session_id": "shared-session",
    "phase": "CHECK",
    "agent_id": "claude-code",
    "vectors": {
        "uncertainty": 0.35,  # Some uncertainty remains
        "know": 0.82,
        "do": 0.88
    }
}

# Agent B loads checkpoint
checkpoint = load_checkpoint("shared-session")

# Agent B sees Agent A's uncertainty
if checkpoint['vectors']['uncertainty'] > 0.4:
    print("⚠️ High uncertainty from Agent A - need investigation!")
    # Run additional investigation before continuing
else:
    print("✅ Agent A was confident - safe to proceed")
```

### Uncertainty Thresholds for Handoff

**Policy rules:**

| Uncertainty | Handoff Policy |
|------------|----------------|
| < 0.3 | ✅ Safe handoff - high confidence |
| 0.3 - 0.5 | ⚠️ Acceptable - document unknowns |
| 0.5 - 0.7 | ⛔ Risky - investigate more first |
| > 0.7 | 🚫 BLOCK - too uncertain for handoff |

**Implementation:**
```python
def can_handoff(checkpoint):
    uncertainty = checkpoint['vectors']['uncertainty']
    
    if uncertainty < 0.3:
        return True, "Safe handoff"
    elif uncertainty < 0.5:
        return True, f"Acceptable but document unknowns: {checkpoint['meta'].get('remaining_unknowns', [])}"
    elif uncertainty < 0.7:
        return False, "Too uncertain - investigate more before handoff"
    else:
        return False, "BLOCKED - uncertainty too high for safe handoff"
```

---

## PREFLIGHT/POSTFLIGHT Strategy by Scenario

### Scenario 1: Sequential Relay (Shared Session)

```
Agent A:
  ✅ PREFLIGHT (baseline)
  Work...
  Checkpoint
  Handoff

Agent B:
  ❌ NO PREFLIGHT (resume from checkpoint)
  Work...
  Checkpoint
  Handoff

Agent C:
  ❌ NO PREFLIGHT (resume from checkpoint)
  Work...
  ✅ POSTFLIGHT (measure total delta from Agent A's PREFLIGHT)
```

**Learning measured:** Agent A PREFLIGHT → Agent C POSTFLIGHT = Total team learning

---

### Scenario 2: Parallel Independent (Your Approach)

```
Agent A (branch: agent-a):
  ✅ PREFLIGHT (baseline for A)
  Work...
  ✅ POSTFLIGHT (measure A's learning)

Agent B (branch: agent-b):
  ✅ PREFLIGHT (baseline for B)
  Work...
  ✅ POSTFLIGHT (measure B's learning)

Sentinel (orchestrator):
  Read both POSTFLIGHT results
  Calculate combined learning:
    - Agent A delta: +0.5 KNOW
    - Agent B delta: +0.42 KNOW
    - Combined team learning: +0.92 KNOW (if non-overlapping)
```

**Learning measured:** Each agent measures its own learning, Sentinel aggregates

---

### Scenario 3: Hybrid (Parallel → Sequential)

```
Phase 1: Parallel (Branches)
  Agent A: PREFLIGHT → Work → POSTFLIGHT
  Agent B: PREFLIGHT → Work → POSTFLIGHT

Phase 2: Merge (Main Branch)
  Sentinel: Merge branches, create shared session
  
  Agent C: 
    ✅ PREFLIGHT (baseline for integration phase)
    Work on merged results
    ✅ POSTFLIGHT (measure integration learning)
```

**Learning measured:** 
- Phase 1: Individual learning (A and B separate)
- Phase 2: Integration learning (C measures synthesis)

---

## Epistemic Delta Transfer (Sentinel-Orchestrated)

### The Security Model

From `EPISTEMIC_DELTA_SECURITY.md`:

**Key principle:** Transfer epistemic state, NOT data

```python
class SentinelHandoff:
    def transfer_epistemic_state(self, from_agent, to_agent):
        """Secure epistemic transfer without data leakage"""
        
        # Read from_agent's checkpoint
        checkpoint = load_checkpoint(from_agent.session_id)
        
        # Extract ONLY epistemic state
        epistemic_state = {
            "vectors": checkpoint['vectors'],  # All 13 vectors
            "phase": checkpoint['phase'],
            "confidence": checkpoint['overall_confidence'],
            "uncertainty": checkpoint['vectors']['uncertainty'],
            "meta": {
                "task": checkpoint['meta']['task'],  # Task description OK
                # NO sensitive data, NO specifics, NO code
            }
        }
        
        # Policy check
        if epistemic_state['uncertainty'] > 0.5:
            return DENY("Too uncertain for safe handoff")
        
        if epistemic_state['vectors']['know'] < 0.7:
            return DENY("Insufficient knowledge for handoff")
        
        # Transfer epistemic state to to_agent
        to_agent.load_epistemic_state(epistemic_state)
        
        return ALLOW("Safe epistemic transfer")
```

### Multi-Agent Coordination Patterns

#### Pattern 1: Expert Consultation

```
Agent A (Generalist):
  uncertainty=0.6 (hit knowledge limit)
  → Request specialist help

Agent B (Security Expert):
  Load Agent A's epistemic state
  See: uncertainty=0.6, area="OAuth2 security"
  → Run focused investigation
  → Create checkpoint: uncertainty=0.15
  → Transfer back to Agent A

Agent A (Generalist):
  Load Agent B's checkpoint
  See: uncertainty=0.15 (expert validated)
  → Continue with confidence
```

#### Pattern 2: Validation Pipeline

```
Agent A (Implementation):
  PREFLIGHT → ACT → Checkpoint (know=0.85)

Agent B (Testing):
  Load Agent A's checkpoint
  Validate implementation
  Update: know=0.92 (validated)

Agent C (Security Audit):
  Load Agent B's checkpoint
  Security review
  Update: know=0.94, impact=0.88 (risks assessed)
```

#### Pattern 3: Parallel Specialization

```
Agent A (Frontend):
  Branch: feature/ui
  Checkpoint: know=0.9 (UI complete)

Agent B (Backend):
  Branch: feature/api
  Checkpoint: know=0.88 (API complete)

Agent C (Integration):
  Merge branches
  Load both checkpoints
  See: Both agents confident
  → Proceed with integration
```

---

## Checkpoint Strategy Recommendations

### When to Create Checkpoints

**Always:**
1. End of PREFLIGHT (baseline)
2. After each CHECK (decision point)
3. Before handoff to another agent
4. End of session / POSTFLIGHT

**Optional:**
- During long ACT phases (every 30 min)
- Before risky operations
- After major discoveries in INVESTIGATE

---

### Multi-Agent Checkpoint Naming

```bash
# Single-agent session
session_id: "agent-a-feature-x"
checkpoints: 
  - PREFLIGHT_round1
  - CHECK_round3
  - ACT_round5
  - POSTFLIGHT_round7

# Multi-agent shared session
session_id: "team-oauth2-impl"
checkpoints:
  - agent-a_PREFLIGHT_round1
  - agent-a_CHECK_round3
  - agent-b_CHECK_round5  # Handoff point
  - agent-b_ACT_round7
  - agent-c_POSTFLIGHT_round9

# Multi-agent parallel (git branches)
session_a: "agent-a-session" (branch: agent-a)
session_b: "agent-b-session" (branch: agent-b)
# Each has its own checkpoint sequence
```

---

## Summary

### Q1: Does agent check uncertainty at each checkpoint?

**YES!** Uncertainty is one of the 13 vectors tracked in EVERY checkpoint.

```json
{
  "vectors": {
    "uncertainty": 0.25,  ← Always tracked
    "know": 0.85,
    "do": 0.90,
    // ... 10 more vectors
  }
}
```

### Q2: How to manage multi-agent trajectories?

**Three approaches:**

1. **Shared Session (Sequential):** 
   - One session ID, agents take turns
   - First agent: PREFLIGHT
   - Last agent: POSTFLIGHT
   - Git: All on main branch

2. **Parallel Sessions (Your Approach):**
   - Each agent: Own session ID + branch
   - Each agent: Own PREFLIGHT + POSTFLIGHT
   - Git: agent-a, agent-b branches
   - Sentinel: Merge and aggregate learning

3. **Hybrid (Parallel → Sequential):**
   - Phase 1: Parallel branches
   - Phase 2: Merge to shared session
   - Git: Branches → main

**Your git branch isolation is perfect!** Checkpoints are branch-specific, so each agent has clean isolation.

---

## Next Steps

1. **Test multi-agent handoff:**
   ```bash
   # Agent A
   empirica bootstrap --session-id shared-123
   empirica preflight "Task description"
   # Work...
   empirica checkpoint-create --phase CHECK
   
   # Agent B
   empirica checkpoint-load --session-id shared-123
   # Continue work...
   ```

2. **Implement uncertainty threshold checks:**
   ```python
   checkpoint = load_checkpoint(session_id)
   if checkpoint['vectors']['uncertainty'] > 0.5:
       print("⚠️ Too uncertain for safe handoff!")
   ```

3. **Add Sentinel orchestration:**
   - Read checkpoints from all agent branches
   - Aggregate epistemic deltas
   - Policy enforcement (uncertainty thresholds)

---

**Key Insight:** Git branches + checkpoints = Perfect multi-agent isolation with epistemic transparency! 🚀
