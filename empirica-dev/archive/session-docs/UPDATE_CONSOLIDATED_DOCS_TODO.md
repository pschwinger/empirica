# Update Consolidated Docs to Match Current Architecture Understanding

**Created:** 2025-01-XX  
**Goal:** Enhance the 6 canonical docs we created in Phase 1A with deeper architecture details

---

## Files to Update

### 1. docs/installation.md
**Current:** 13K, comprehensive cross-platform guide  
**Enhancement needed:**
- ✅ Already covers: Prerequisites, MCP setup, CLI setup, Git initialization
- ➕ Add: Git notes initialization (refs/notes/empirica structure)
- ➕ Add: Section on cross-AI coordination setup
- ➕ Add: Mention of .empirica/ directory structure (SQLite + JSON + Git)

### 2. docs/architecture.md
**Current:** 11K, user-friendly overview  
**Enhancement needed:**
- ✅ Already covers: Core components, storage layers
- ➕ Add: Git notes integration section (cross-AI coordination)
- ➕ Add: Unified drift monitor (MirrorDriftMonitor vs old approach)
- ➕ Add: Session structure diagram (BOOTSTRAP → GOAL → CASCADE)
- ➕ Add: Storage architecture diagram (SQLite + JSON + Git notes)
- ➕ Reference: Link to architecture-technical.md for deep dive

### 3. docs/getting-started.md
**Current:** 7.4K, step-by-step tutorial  
**Enhancement needed:**
- ✅ Already covers: Basic workflow, first CASCADE
- ➕ Add: Git checkpoint automatic creation (PREFLIGHT/CHECK/POSTFLIGHT)
- ➕ Add: Simple cross-AI example (discover goals from another AI)
- ➕ Add: Note about --ai-id flag importance
- ➕ Add: Section on session continuity (resume from git checkpoints)

### 4. docs/reference/architecture-technical.md
**Current:** Deep technical dive  
**Enhancement needed:**
- ✅ Already comprehensive (874 lines)
- ➕ Add: Section on empirica/core/canonical/empirica_git/ (checkpoint_manager, goal_store, session_sync)
- ➕ Add: Section on empirica/core/drift/mirror_drift_monitor.py
- ➕ Add: Migration note about old DriftMonitor → MirrorDriftMonitor
- ➕ Add: Cross-reference to CANONICAL_DIRECTORY_STRUCTURE_V2.md

### 5. docs/reference/command-reference.md
**Current:** Command cheat sheet  
**Enhancement needed:**
- ✅ Already covers: CLI commands
- ➕ Add: Git checkpoint commands (load-checkpoint, etc.)
- ➕ Add: Goal discovery commands (goals-discover, goals-resume)
- ➕ Add: Identity commands (identity-create, identity-export, identity-verify)
- ➕ Add: --ai-id flag documentation (importance for cross-AI coordination)
- ➕ Add: --no-git flag (skip git checkpoints for testing)

### 6. docs/reference/CANONICAL_DIRECTORY_STRUCTURE_V2.md
**Current:** ✅ Already created with full depth (current codebase map)  
**No changes needed** - This is the source of truth

---

## Enhancement Priority

**High Priority (Essential for users):**
1. docs/getting-started.md - Add git checkpoint + cross-AI basics
2. docs/architecture.md - Add git notes + session structure
3. docs/installation.md - Add git notes initialization

**Medium Priority (For developers):**
4. docs/reference/command-reference.md - Add git/cross-AI commands
5. docs/reference/architecture-technical.md - Add empirica_git/ details

**Low Priority (Already comprehensive):**
6. CANONICAL_DIRECTORY_STRUCTURE_V2.md - No changes needed

---

## Content to Add

### Git Checkpoints Section (for getting-started.md & architecture.md)

```markdown
## Git Checkpoints: Automatic Epistemic Memory

Empirica automatically creates **git checkpoints** at key workflow points:

**When checkpoints are created:**
- **PREFLIGHT** - Before work begins (baseline state)
- **CHECK** - During work (0-N times, decision gates)
- **POSTFLIGHT** - After work completes (final state)

**What's stored:**
- 13 epistemic vectors (know, do, clarity, uncertainty, etc.)
- Session and AI metadata
- Phase and round number
- ~85% token compressed (~3K → ~450)

**Where stored:**
- Git notes: `refs/notes/empirica/checkpoints/<commit-hash>`
- SQLite: `.empirica/sessions/sessions.db`
- JSON logs: `.empirica_reflex_logs/<session-id>.json`

**Why three layers?**
- **Git notes**: Cross-AI coordination, version controlled
- **SQLite**: Fast queries
- **JSON**: Full fidelity temporal replay

**Usage:**
```bash
# Auto-creates checkpoint
empirica preflight "task" --ai-id your-ai

# Load latest checkpoint
empirica load-checkpoint <session-id>

# Skip git (for testing)
empirica preflight "task" --no-git
```

**Benefits:**
- Resume work from any checkpoint
- Cross-AI can see your epistemic state
- Training data for future calibration
- Full audit trail
```

---

### Cross-AI Coordination Section (for getting-started.md)

```markdown
## Cross-AI Coordination: Discover & Resume Goals

Empirica enables multiple AIs to collaborate on goals:

**AI-1 creates goal:**
```bash
empirica goals-create \
  --objective "Implement authentication" \
  --scope project_wide \
  --ai-id ai-1

# Goal stored in refs/notes/empirica/goals/<goal-id>
```

**AI-2 discovers goals:**
```bash
empirica goals-discover --from-ai-id ai-1

# Returns: All goals created by ai-1
# Shows: Objective, ai-1's epistemic state, lineage
```

**AI-2 resumes goal:**
```bash
empirica goals-resume <goal-id> --ai-id ai-2

# Adds lineage: {ai: ai-2, action: resumed}
# Loads ai-1's epistemic context
```

**Benefits:**
- Distributed coordination (git pull syncs goals)
- Epistemic handoff (know ai-1's confidence levels)
- Lineage tracking (audit trail)
- Version controlled
```

---

### Session Structure Section (for architecture.md)

```markdown
## Session Structure

**Corrected Architecture (2025):**

```
SESSION (work period):
  │
  ├─ BOOTSTRAP (once per session)
  │   └─ Initialize: persona, model profile, thresholds
  │   └─ Restore: context from prior sessions (if continuing)
  │
  └─ GOAL/WORK (per coherent task):
      │
      ├─ PREFLIGHT (assess before work)
      │   └─ 13 epistemic vectors
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
- CHECK can happen 0-N times (intermediate calibration)
- Git checkpoints created automatically
- Training data emerges from deltas
```

---

### Drift Monitor Section (for architecture.md)

```markdown
## Unified Drift Monitor

**Philosophy:** Temporal self-validation without heuristics

**How it works:**
- **Increases expected** (learning)
- **Decreases without investigation are drift** (memory corruption)
- Compare current state to git checkpoint history
- No heuristics, pure temporal comparison

**Implementation:**
- `empirica/core/drift/mirror_drift_monitor.py::MirrorDriftMonitor`
- Replaces old `calibration/parallel_reasoning.py::DriftMonitor`

**Usage:**
```python
from empirica.core.drift import MirrorDriftMonitor

monitor = MirrorDriftMonitor()
drift_detected = monitor.detect_drift(current_vectors, checkpoint_history)
```

**Note:** CASCADE migration in progress (currently uses old DriftMonitor)
```

---

## Action Plan

**For Acting AI (or me in next session):**

1. **Read each file** (installation.md, architecture.md, getting-started.md)
2. **Identify insertion points** for new sections
3. **Add content** from templates above
4. **Update cross-references** (link to related docs)
5. **Verify accuracy** (test commands, check code references)

**Estimated time:** 2-3 hours

---

## Success Criteria

**After updates:**
- ✅ All 6 canonical docs mention git checkpoints
- ✅ Users understand automatic checkpoint creation
- ✅ Cross-AI coordination explained with examples
- ✅ Session structure diagram included
- ✅ Drift monitor philosophy explained
- ✅ Consistent depth across all docs

---

**Status:** TODO - Ready for acting AI or next session  
**Priority:** Medium (enhances existing docs, not critical path)
