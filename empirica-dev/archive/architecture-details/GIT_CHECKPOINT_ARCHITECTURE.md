# Git Checkpoint Architecture - How It Maps to CASCADE

## TL;DR

**Git checkpoints are SEPARATE from PREFLIGHT/CHECK/POSTFLIGHT** - they are manual snapshots you create during the CASCADE workflow.

---

## Understanding Two Orthogonal Systems

Empirica has **two independent layers** working together:

### 1. Self-Assessment Layer (OUTER LOOP)
```
PREFLIGHT → CHECK(s) → POSTFLIGHT
```
Tracks **epistemic awareness** across entire task using 13 vectors (KNOW, DO, CONTEXT, etc.)

### 2. CASCADE Workflow Layer (INNER LOOP)
```
CASCADE rounds: 0 → 1 → 2 → ... → N
```
Tracks **iterative work** happening WITHIN the assessment phases. Git checkpoints track these rounds.

**Key insight:** Git checkpoints track CASCADE work happening *between* PREFLIGHT/CHECK/POSTFLIGHT assessments, not the assessments themselves.

---

## Dual-Tier Storage Architecture

### PRIMARY Tier: checkpoint_manager
- **Storage:** `refs/notes/empirica/checkpoints`
- **Size:** ~200 bytes (~85% reduction)
- **Purpose:** Drift detection via MirrorDriftMonitor
- **Automatic:** Created by CASCADE

### SECONDARY Tier: git_enhanced_reflex_logger
- **Storage:** `empirica/session/{session_id}`
- **Size:** ~2-3KB (80-90% compression)
- **Purpose:** Debugging, session reconstruction
- **Optional:** Can be disabled

See [GIT_NOTES_CONSOLIDATION_PLAN.md](../../GIT_NOTES_CONSOLIDATION_PLAN.md) for detailed comparison.

## Architecture Overview

```
CASCADE Phases          Git Storage          CLI Commands
─────────────────────────────────────────────────────────────
PREFLIGHT              SQLite + JSON        empirica preflight
  ↓                        ↓                 empirica preflight-submit
  ├─> Vectors stored   sessions.db          
  └─> Optional git     git notes            empirica checkpoint-create --phase=PREFLIGHT
      checkpoint       (compressed)
  
INVESTIGATE            JSON logs            (no CLI command - manual work)
  ↓                        ↓
  └─> Optional git     git notes            empirica checkpoint-create --phase=INVESTIGATE
      checkpoint       (compressed)
  
CHECK                  SQLite + JSON        empirica check
  ↓                        ↓                 empirica check-submit
  ├─> Decision stored  sessions.db
  └─> Optional git     git notes            empirica checkpoint-create --phase=CHECK
      checkpoint       (compressed)
  
ACT                    JSON logs            (no CLI command - actual work)
  ↓                        ↓
  └─> Optional git     git notes            empirica checkpoint-create --phase=ACT
      checkpoint       (compressed)
  
POSTFLIGHT             SQLite + JSON        empirica postflight
  ↓                        ↓                 empirica postflight-submit
  ├─> Vectors stored   sessions.db
  ├─> Deltas computed  (PREFLIGHT vs POSTFLIGHT)
  └─> Optional git     git notes            empirica checkpoint-create --phase=POSTFLIGHT
      checkpoint       (compressed)
```

## Three Storage Layers

### 1. SQLite Database (`.empirica/sessions/sessions.db`)
**Purpose:** Session metadata and epistemic state  
**Stores:**
- Session creation (`ai_id`, `session_id`, `bootstrap_level`)
- PREFLIGHT vectors (13 epistemic dimensions)
- CHECK decisions (`proceed` / `investigate`)
- POSTFLIGHT vectors (13 epistemic dimensions)
- Calibration deltas (PREFLIGHT → POSTFLIGHT)

**Written by:**
- `empirica preflight-submit`
- `empirica check-submit`
- `empirica postflight-submit`

### 2. JSON Logs (`.empirica_reflex_logs/`)
**Purpose:** Detailed workflow logs and history  
**Stores:**
- Full assessment objects
- Timestamps and workflow progression
- Investigation findings
- Human-readable logs

**Written by:**
- All CASCADE commands
- Reflex logger (automatic)

### 3. Git Notes (Compressed Checkpoints)
**Purpose:** ~85% token-reduced resumption points  
**Stores:**
- Compressed epistemic state snapshots
- Phase + round number
- Essential vectors only
- Metadata (progress, notes)

**Written by:**
- `empirica checkpoint-create` (MANUAL)
- NOT automatic - you must call it explicitly

## Key Insight: Checkpoints Are Optional

```python
# PREFLIGHT is automatic (stores to SQLite + JSON)
empirica preflight "Task description" --ai-id claude-code

# Checkpoint is OPTIONAL (stores to git notes)
empirica checkpoint-create --session-id latest:active:claude-code \
    --phase PREFLIGHT --round 1 --metadata '{"note": "Initial assessment"}'
```

## When to Create Git Checkpoints

✅ **Create checkpoints when:**
- Long-running tasks (>30 min)
- Before context window might fill up
- Natural breakpoints in workflow
- Before risky operations
- End of session for resumption

❌ **Don't create checkpoints when:**
- Simple tasks (<10 min)
- Already at end of session
- No risk of interruption

## MCP Tool Mapping

### MCP Tools → CLI Commands

```json
{
  "bootstrap_session": "empirica bootstrap --ai-id X",
  "execute_preflight": "empirica preflight 'task' --prompt-only",
  "submit_preflight_assessment": "empirica preflight-submit --session-id X --vectors {}",
  "execute_check": "empirica check --session-id X",
  "submit_check_assessment": "empirica check-submit --session-id X --decision proceed",
  "execute_postflight": "empirica postflight X --prompt-only",
  "submit_postflight_assessment": "empirica postflight-submit --session-id X --vectors {}",
  "create_git_checkpoint": "empirica checkpoint-create --session-id X --phase ACT",
  "load_git_checkpoint": "empirica checkpoint-load X"
}
```

### Stateless vs Stateful

**Stateless (handled in MCP):**
- `get_empirica_introduction()` - Returns markdown intro
- `get_workflow_guidance()` - Returns phase guidance
- `cli_help()` - Returns CLI help text

**Stateful (routed to CLI):**
- All workflow commands (preflight, check, postflight)
- All goal/task commands
- All checkpoint commands
- All session commands

## The --ai-id Fix Impact

### Before Fix
```bash
# Session created with session_id as ai_id (confusing!)
empirica preflight "task"
# → Creates session with ai_id = <random-uuid>
```

### After Fix
```bash
# Session created with specified ai_id (correct!)
empirica preflight "task" --ai-id claude-code
# → Creates session with ai_id = "claude-code"

# Default still works (backward compatible)
empirica preflight "task"
# → Creates session with ai_id = "empirica_cli"
```

### Why This Matters

**Multi-AI tracking:**
```sql
-- Before: All sessions had random UUIDs as ai_id
SELECT ai_id, session_id FROM sessions;
-- 88dbf132-cc7c-4a4b-9b59-77df3b13dbd2 | abc123
-- a89b9d94-d907-4a95-ab8d-df8824990bec | def456

-- After: Sessions grouped by AI agent
SELECT ai_id, session_id FROM sessions;
-- claude-code    | abc123
-- mini-agent     | def456
-- gemini-flash   | ghi789
```

**Resume by AI:**
```bash
# Find last session for specific AI
empirica sessions-resume --ai-id claude-code --count 1

# Use alias for commands
empirica checkpoint-load latest:active:claude-code
```

## Complete Workflow Example

```bash
# 1. Bootstrap session (creates in SQLite)
empirica bootstrap --ai-id mini-agent --level 2

# 2. PREFLIGHT (stores to SQLite + JSON)
empirica preflight "Implement feature X" --ai-id mini-agent --session-id latest:active:mini-agent
empirica preflight-submit --session-id latest:active:mini-agent \
    --vectors '{"engagement": 0.8, "know": 0.4, ...}'

# 3. OPTIONAL: Create git checkpoint
empirica checkpoint-create --session-id latest:active:mini-agent \
    --phase PREFLIGHT --round 1

# 4. INVESTIGATE (manual work - logs to JSON)
# ... research, code exploration, etc ...

# 5. OPTIONAL: Create git checkpoint after investigation
empirica checkpoint-create --session-id latest:active:mini-agent \
    --phase INVESTIGATE --round 1 --metadata '{"findings": "3 key insights"}'

# 6. CHECK (stores to SQLite + JSON)
empirica check --session-id latest:active:mini-agent
empirica check-submit --session-id latest:active:mini-agent \
    --decision proceed --vectors '{...}'

# 7. ACT (manual work - logs to JSON)
# ... implement the feature ...

# 8. OPTIONAL: Create git checkpoint during ACT
empirica checkpoint-create --session-id latest:active:mini-agent \
    --phase ACT --round 1 --metadata '{"progress": "50%"}'

# 9. POSTFLIGHT (stores to SQLite + JSON, computes deltas)
empirica postflight latest:active:mini-agent
empirica postflight-submit --session-id latest:active:mini-agent \
    --vectors '{"engagement": 0.9, "know": 0.8, ...}'

# 10. OPTIONAL: Final checkpoint
empirica checkpoint-create --session-id latest:active:mini-agent \
    --phase POSTFLIGHT --round 1
```

## Resumption Flow

```bash
# Session interrupted? Resume from checkpoint:

# 1. Load last checkpoint (from git notes)
empirica checkpoint-load latest:active:mini-agent
# → Returns: last phase, round, vectors, metadata

# 2. Query session state (from SQLite)
empirica sessions-show latest:active:mini-agent
# → Returns: full session history, all assessments

# 3. Resume workflow from where you left off
empirica check --session-id latest:active:mini-agent
```

## Token Savings

### Without Git Checkpoints
- Full session context: ~50,000 tokens
- All logs, all history, all assessments

### With Git Checkpoints
- Compressed checkpoint: ~1,250 tokens (~85% reduction!)
- Essential state only
- Reconstruct full context on-demand from SQLite/JSON

## Summary

| Feature | Storage | Automatic? | CLI Command |
|---------|---------|------------|-------------|
| **PREFLIGHT vectors** | SQLite + JSON | ✅ Yes | `preflight-submit` |
| **CHECK decision** | SQLite + JSON | ✅ Yes | `check-submit` |
| **POSTFLIGHT vectors** | SQLite + JSON | ✅ Yes | `postflight-submit` |
| **Calibration deltas** | SQLite | ✅ Yes | (computed automatically) |
| **Git checkpoints** | git notes | ❌ No | `checkpoint-create` (manual) |
| **Reflex logs** | JSON | ✅ Yes | (automatic) |

**Key Takeaway:** Git checkpoints are an OPTIONAL optimization for long-running sessions, not a required part of CASCADE workflow. Use them when you need efficient resumption or context management.

---

**Updated:** 2025-11-27  
**Status:** Accurate post-fix analysis

---

## Current Implementation Status (2025-01-XX)

### ✅ Implemented and Working

**Git Notes Storage (`empirica/core/canonical/empirica_git/`):**

1. **checkpoint_manager.py** ✅
   - Creates checkpoints on PREFLIGHT, CHECK, POSTFLIGHT
   - Stores to `refs/notes/empirica/checkpoints/<commit-hash>`
   - ~85% token compression
   - Auto-creates on assessment commands

2. **goal_store.py** ✅
   - Stores goals to `refs/notes/empirica/goals/<goal-id>`
   - Cross-AI goal discovery
   - Lineage tracking (who created/resumed)
   - Auto-stores on goal creation

3. **session_sync.py** ✅
   - Stores session metadata to `refs/notes/empirica/session/<session-id>`
   - Session state tracking

4. **sentinel_hooks.py** ✅
   - Cognitive vault integration
   - Routing decisions based on epistemic state

**Verified Active:**
- 1 checkpoint in refs/notes/empirica/checkpoints
- 16 goals in refs/notes/empirica/goals/*
- 5 sessions in refs/notes/empirica/session/*
- 6 tasks in refs/notes/empirica/tasks/*

---

## Session Structure (Corrected 2025-01-XX)

### CASCADE Architecture

```
SESSION (work period):
  │
  ├─ BOOTSTRAP (once per session)
  │   └─ Initialize: persona, model profile, thresholds
  │   └─ Restore: context from prior sessions if continuing
  │
  └─ GOAL/WORK (per coherent task):
      │
      ├─ PREFLIGHT (assess before work)
      │   └─ 13 epistemic vectors (honest self-assessment)
      │   └─ Git checkpoint created ✅
      │
      ├─ CASCADE (implicit AI reasoning loop)
      │   ├─ investigate (implicit)
      │   ├─ plan (implicit)
      │   ├─ act (explicit)
      │   └─ CHECK (explicit gate, 0-N times)
      │       └─ Git checkpoint created ✅
      │   └─ [loop until complete or blocked]
      │
      └─ POSTFLIGHT (calibrate after work)
          └─ Re-assess 13 vectors
          └─ Git checkpoint created ✅
          └─ Training data: PREFLIGHT → [CHECKs] → POSTFLIGHT deltas
```

**Key Points:**
- BOOTSTRAP is session-level only (not per goal)
- CHECK can happen 0-N times (provides intermediate calibration)
- Git checkpoints created automatically on PREFLIGHT, CHECK, POSTFLIGHT
- Deltas calculated retrospectively from stored checkpoints

---

## Drift Detection (Updated 2025-01-XX)

### New: Mirror Drift Monitor (No Heuristics)

**Location:** `empirica/core/drift/mirror_drift_monitor.py`

**Philosophy:**
- **Increases are expected** (learning)
- **Decreases without investigation are drift** (memory corruption)
- Compare to recent history (not single point)
- **NO HEURISTICS** - pure temporal self-validation

**How it works:**
1. Load recent checkpoints from git notes
2. Compare current vectors to historical baseline
3. Detect unexpected decreases in know/clarity/engagement
4. Report drift severity and recommended action

**Replaces:**
- ❌ `empirica/calibration/parallel_reasoning.py::DriftMonitor` (had heuristics)
- ❌ `empirica/calibration/adaptive_uncertainty_calibration/` (too complex)

**Migration Status:** CASCADE still uses old DriftMonitor - needs update

---

## Cross-AI Coordination

### Goal Discovery & Resume

**Flow:**
```
AI-1 creates goal:
  └─ empirica goals-create --objective "Implement auth" --ai-id ai-1
      └─ Stored to refs/notes/empirica/goals/<goal-id>
      └─ Includes: objective, subtasks, epistemic state, lineage

AI-2 discovers goals:
  └─ empirica goals-discover --from-ai-id ai-1
      └─ Returns: All goals created by ai-1
      └─ Shows: Objective, ai-1's epistemic state, lineage

AI-2 resumes goal:
  └─ empirica goals-resume <goal-id> --ai-id ai-2
      └─ Adds lineage: {ai: ai-2, action: resumed, timestamp}
      └─ Loads ai-1's epistemic context for handoff
      └─ AI-2 continues work with full context
```

**Benefits:**
- Distributed coordination (git pull syncs goals)
- Epistemic handoff (know ai-1's confidence levels)
- Lineage tracking (audit trail of who worked on what)
- Version controlled (can revert/branch goals)

---

## Storage Map (Current)

```
Git Repository
│
├── Code Changes (normal git commits)
│   └── Your source code
│
└── Git Notes (Empirica metadata)
    │
    ├── refs/notes/empirica/checkpoints/<commit-hash>
    │   └── {session, ai, phase, vectors, metadata}
    │   └── Created automatically on PREFLIGHT/CHECK/POSTFLIGHT
    │
    ├── refs/notes/empirica/goals/<goal-id>
    │   └── {objective, subtasks, epistemic_state, lineage}
    │   └── Created automatically on goals-create
    │
    ├── refs/notes/empirica/session/<session-id>
    │   └── {ai_id, started, status}
    │   └── Created automatically on bootstrap
    │
    └── refs/notes/empirica/tasks/<task-id>
        └── {task metadata}
        └── Created automatically on add-subtask
```

**Current active data:**
- 1 checkpoint
- 16 goals
- 5 sessions
- 6 tasks

---

## CLI Commands for Git Integration

### Checkpoint Management
```bash
# Auto-creates checkpoint
empirica preflight "task" --ai-id your-ai

# Load latest checkpoint
empirica load-checkpoint <session-id>

# Disable git (for testing)
empirica preflight "task" --no-git
```

### Goal Discovery
```bash
# Discover goals from another AI
empirica goals-discover --from-ai-id other-ai

# Resume another AI's goal
empirica goals-resume <goal-id> --ai-id your-ai

# View goal details (includes epistemic handoff)
empirica goals-list --session-id <session-id>
```

### Identity Management
```bash
# Create AI identity (Ed25519 keypair)
empirica identity-create --ai-id your-ai

# Export public key for sharing
empirica identity-export --ai-id your-ai

# Verify signed session
empirica identity-verify --session-id <session-id>
```

---

## Best Practices

### 1. Always Use --ai-id
```bash
empirica preflight "task" --ai-id your-ai  # ✅ Good
empirica preflight "task"                  # ⚠️ Uses default 'empirica_cli'
```

### 2. Check for Existing Goals Before Creating
```bash
# Avoid duplicate work
empirica goals-discover --from-ai-id other-ai
# If goal exists, resume instead of creating new
```

### 3. Use Lineage for Context
```bash
# When resuming, review original AI's state
empirica goals-resume <goal-id> --ai-id your-ai
# Shows their know/uncertainty/clarity levels
```

### 4. Disable Git for Quick Tests
```bash
# Skip git overhead during experimentation
empirica preflight "quick test" --no-git
```

---

## Troubleshooting

### "Not in git repository"
**Cause:** Git checkpoints only work in git repos  
**Solution:** `git init` in workspace, or use `--no-git` flag  
**Impact:** Commands still work, just no git storage

### "Git notes not found"
**Cause:** Notes not fetched from remote  
**Solution:** `git fetch origin refs/notes/*:refs/notes/*`  
**Check:** `git notes list`

### "Goals not discoverable"
**Cause:** Goal not stored in git notes  
**Solution:** Verify with `git notes list | grep empirica/goals`  
**Push:** `git push origin refs/notes/empirica/*` to share

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ AI Agent Working Session                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   BOOTSTRAP     │ (session-level, once)
                    │  Load persona   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PREFLIGHT     │ ◄──── Git checkpoint created
                    │ Assess vectors  │       refs/notes/empirica/checkpoints
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   CREATE GOAL   │ ◄──── Git goal stored
                    │   Define work   │       refs/notes/empirica/goals
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    CASCADE      │
                    │ investigate →   │
                    │   plan →        │
                    │   act →         │
                    │   CHECK ────────┼──── Git checkpoint (0-N times)
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  POSTFLIGHT     │ ◄──── Git checkpoint created
                    │ Calibrate delta │       + training data
                    └─────────────────┘
```

---

**Status:** ✅ Current and working  
**Last Verified:** 2025-01-XX  
**Implementation:** empirica/core/canonical/empirica_git/
