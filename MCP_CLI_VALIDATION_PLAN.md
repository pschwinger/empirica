# MCP/CLI Validation & Unified Storage Clarity Plan

**Session:** 7e86fe6a-20fe-41e0-9dc7-e3b4ccc6c37a  
**Date:** 2025-12-06  
**Purpose:** Evidence-based plan for MCP/CLI completeness and unified storage architecture clarity

---

## Discovery Results (Evidence from Codebase)

### 1. MCP Tools Implemented (29 tools)

**Source:** `mcp_local/empirica_mcp_server.py`

**Documentation & Guidance (3):**
1. get_empirica_introduction
2. get_workflow_guidance  
3. cli_help

**Session Management (4):**
4. session_create
5. get_epistemic_state
6. get_session_summary
7. resume_previous_session

**CASCADE Workflow (6):**
8. execute_preflight
9. submit_preflight_assessment
10. execute_check
11. submit_check_assessment
12. execute_postflight
13. submit_postflight_assessment

**Goals/Subtasks (5):**
14. create_goal
15. add_subtask
16. complete_subtask
17. get_goal_progress
18. list_goals

**Checkpoints (2):**
19. create_git_checkpoint
20. load_git_checkpoint

**Handoffs (2):**
21. create_handoff_report
22. query_handoff_reports

**Goal Discovery/Resume (2):**
23. discover_goals
24. resume_goal

**Identity/Crypto (4):**
25. create_identity
26. list_identities
27. export_public_key
28. verify_signature

**Calibration (1):**
29. get_calibration_report

---

### 2. CLI Commands Implemented (37+ commands)

**Source:** `empirica/cli/cli_core.py` + help output

**Session Management (5):**
- session-create
- sessions-list
- sessions-show
- sessions-export
- sessions-resume

**CASCADE Workflow (7):**
- preflight
- preflight-submit
- check
- check-submit
- postflight
- postflight-submit
- workflow

**Goals/Subtasks (7):**
- goals-create
- goals-add-subtask
- goals-complete-subtask
- goals-progress
- goals-list
- goals-discover
- goals-resume

**Checkpoints (7):**
- checkpoint-create
- checkpoint-load
- checkpoint-list
- checkpoint-diff
- checkpoint-sign
- checkpoint-verify
- checkpoint-signatures

**Handoffs (2):**
- handoff-create
- handoff-query

**Identity/Crypto (4):**
- identity-create
- identity-list
- identity-export
- identity-verify

**Monitoring & Logging (5):**
- monitor
- investigate-log
- act-log
- performance
- efficiency-report

**Configuration (5):**
- config
- profile-list
- profile-show
- profile-create
- profile-set-default

**Interactive (3):**
- onboard
- ask
- chat

**Investigation (2):**
- investigate
- goal-analysis

---

### 3. Unified Storage Architecture

**Core Component:** `GitEnhancedReflexLogger`  
**Location:** `empirica/core/canonical/git_enhanced_reflex_logger.py`

**3-Layer Atomic Write:**

```python
GitEnhancedReflexLogger.add_checkpoint()
    ↓
    ├─→ Layer 1: SQLite reflexes table
    │   • File: empirica/data/session_database.py
    │   • Method: store_vectors()
    │   • Queryable, structured data
    │
    ├─→ Layer 2: Git notes (compressed)
    │   • File: empirica/core/canonical/empirica_git/checkpoint_manager.py
    │   • Refs: refs/notes/empirica/session/{id}/{phase}/{round}
    │   • 97.5% token reduction (46 vs 1,821 tokens)
    │
    └─→ Layer 3: JSON logs (full detail)
        • Directory: .empirica_reflex_logs/{date}/{ai}/{session}/
        • Complete audit trail
        • Human-readable backups
```

**Supporting Components:**
- **Goal Storage:** `empirica/core/canonical/empirica_git/goal_store.py`
- **Session Sync:** `empirica/core/canonical/empirica_git/session_sync.py`
- **Sentinel Hooks:** `empirica/core/canonical/empirica_git/sentinel_hooks.py`

---

### 4. Visualization Components

**Statusline:**
- **File:** `scripts/statusline_empirica.py`
- **Purpose:** Real-time epistemic state in status bar
- **Shows:** Current vectors, session state

**Dashboards:**
- **Location:** `scripts/dashboards/` + `empirica/dashboard/`
- **Components:**
  - `cascade_monitor.py` - Real-time CASCADE monitoring
  - `snapshot_monitor.py` - Epistemic snapshots
  - `scripts/dashboards/empirica.sh` - Main dashboard
  - `scripts/dashboards/leaderboard.sh` - Leaderboard display
  - `scripts/dashboards/status.sh` - Status dashboard
  - `scripts/dashboards/empirica-goals-dashboard.sh` - Goals visualization
  - `scripts/dashboards/empirica-git-stats.sh` - Git statistics

**Session Replay:**
- **File:** `scripts/session_replay.py`
- **Purpose:** Replay session history with visualization

---

## Validation Needed (Next Session Tasks)

### Task 1: MCP Tools vs Documentation

**Check:**
- Does docs mention all 29 tools?
- Are tool descriptions accurate?
- Are examples correct?

**Files to Review:**
- `docs/04_MCP_QUICKSTART.md`
- `docs/production/00_DOCUMENTATION_MAP.md` (MCP section)
- `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`

**Evidence Check:**
```bash
# Count MCP tool mentions in docs
grep -c "session_create\|execute_preflight\|create_goal" docs/*.md docs/production/*.md
```

---

### Task 2: CLI Commands vs Documentation

**Check:**
- Does docs mention all 37+ commands?
- Are command examples accurate?
- Are parameter descriptions correct?

**Files to Review:**
- `docs/03_CLI_QUICKSTART.md`
- `docs/production/00_DOCUMENTATION_MAP.md` (CLI section)
- `docs/production/19_API_REFERENCE.md`

**Evidence Check:**
```bash
# Compare CLI help vs documented commands
python3 -m empirica.cli --help > actual_commands.txt
grep "empirica " docs/*.md > documented_commands.txt
diff actual_commands.txt documented_commands.txt
```

---

### Task 3: API Documentation vs Implementation

**Check:**
- Does 13_PYTHON_API.md document all SessionDatabase methods?
- Are method signatures accurate?
- Are examples correct?

**Files to Review:**
- `docs/production/13_PYTHON_API.md`
- `docs/production/19_API_REFERENCE.md`

**Evidence Check:**
```python
# Extract SessionDatabase public methods
import inspect
from empirica.data.session_database import SessionDatabase

db = SessionDatabase()
methods = [m for m in dir(db) if not m.startswith('_')]
print(f"Public methods: {len(methods)}")
# Compare vs documented methods
```

---

### Task 4: Unified Storage Architecture Documentation

**Current Documentation:**
- `docs/architecture/STORAGE_ARCHITECTURE_COMPLETE.md` - Exists ✅
- `docs/architecture/storage_architecture_flow.svg` - Exists ✅
- Mentions in `docs/production/12_SESSION_DATABASE.md`

**Needs Emphasis:**
1. **In 00_DOCUMENTATION_MAP.md:**
   - Add "Unified Storage Architecture" section early
   - Explain 3-layer atomic write prominently
   - Show how it enables dashboards/statuslines

2. **In CANONICAL_SYSTEM_PROMPT.md:**
   - Section III currently has storage architecture
   - Check if it emphasizes git notes → dashboards connection

3. **In README.md:**
   - Add brief "How It Works" section showing storage flow
   - Visual diagram reference

**What to Add (Simplification, not more content):**
- Short visual flow: `PREFLIGHT → 3-Layer Storage → Dashboards/Statuslines`
- Emphasize "write once, query everywhere" pattern
- Show concrete examples of using stored data

---

### Task 5: Dashboard/Statusline/Leaderboard Documentation

**Current State:**
- ❌ Scripts exist but likely undocumented
- ❌ No user guide for dashboards
- ❌ No examples of statusline integration

**Needs Creation (Minimal):**
1. **Quick Start Guide:**
   ```bash
   # Show epistemic state in status bar
   scripts/statusline_empirica.py --session-id <ID>
   
   # Launch dashboard
   scripts/dashboards/empirica.sh
   
   # View leaderboard
   scripts/dashboards/leaderboard.sh
   ```

2. **In 00_DOCUMENTATION_MAP.md:**
   - Add "Visualization" section
   - List available dashboards/scripts
   - One-line description each

3. **Don't Create:**
   - Detailed dashboard customization guide (too much content)
   - Advanced scripting guide (out of scope)
   - Just: "These exist, here's how to run them"

---

## Action Plan for Next Session

### Priority 1: Validate MCP/CLI Completeness (Critical)

**Sub-tasks:**
1. Extract all 29 MCP tools → check each in docs
2. Extract all 37 CLI commands → check each in docs  
3. Create missing documentation (one-liners, not essays)
4. Fix incorrect examples

**Estimated Time:** 30-45 minutes

---

### Priority 2: Unified Storage Emphasis (High)

**Sub-tasks:**
1. Add "Unified Storage Architecture" section to 00_DOCUMENTATION_MAP.md
2. Add brief "How It Works" to README.md with flow diagram reference
3. Verify CANONICAL_SYSTEM_PROMPT.md has complete storage explanation
4. Simplify (don't expand) STORAGE_ARCHITECTURE_COMPLETE.md if needed

**Estimated Time:** 20-30 minutes

---

### Priority 3: Dashboard/Statusline Documentation (High)

**Sub-tasks:**
1. Create simple "Visualization Tools" section in 00_DOCUMENTATION_MAP.md
2. List all dashboard scripts with one-line descriptions
3. Add quick start examples (3-5 commands total)
4. Reference from README.md

**Estimated Time:** 15-20 minutes

---

### Priority 4: API Verification (Medium)

**Sub-tasks:**
1. Extract SessionDatabase public methods
2. Compare vs 13_PYTHON_API.md
3. Add missing methods (one-liners)
4. Fix incorrect signatures

**Estimated Time:** 20-30 minutes

---

## Key Principles for Next Session

### 1. **Validation Over Creation**
- Check what exists vs what's documented
- Fix gaps, don't write essays
- One-line additions acceptable, paragraphs not

### 2. **Simplification Over Expansion**
- If something is too verbose, trim it
- Prefer examples over explanations
- Prefer lists over paragraphs

### 3. **Evidence-Based**
- Every change must reference actual code
- No documenting aspirational features
- Grep/Python checks before writing

### 4. **User/AI Interface First**
- MCP tools = how AIs interact
- CLI commands = how users interact
- These must be 100% accurate and complete

### 5. **Unified Storage as Central Concept**
- This is the "secret sauce" of Empirica
- Metacognitive states → git → queryable
- Enables dashboards, leaderboards, statuslines
- Must be prominent, not buried

---

## Success Criteria

✅ **MCP Tools:** All 29 tools documented with correct signatures  
✅ **CLI Commands:** All 37+ commands documented with examples  
✅ **API Methods:** SessionDatabase methods match docs  
✅ **Storage Architecture:** Prominent in README and DOCUMENTATION_MAP  
✅ **Dashboards:** Listed and runnable (quick start only)  
✅ **No Bloat:** Documentation is shorter or same length, not longer  

---

## Files to Update (Predicted)

### Definitely Update:
1. `docs/production/00_DOCUMENTATION_MAP.md` - Add storage + visualization sections
2. `README.md` - Add "How It Works" with storage flow
3. `docs/04_MCP_QUICKSTART.md` - Verify 29 tools covered
4. `docs/03_CLI_QUICKSTART.md` - Verify 37 commands covered

### Probably Update:
5. `docs/production/13_PYTHON_API.md` - Verify method coverage
6. `docs/production/19_API_REFERENCE.md` - Check signatures
7. `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md` - Verify storage emphasis

### Maybe Update (Check First):
8. `docs/architecture/STORAGE_ARCHITECTURE_COMPLETE.md` - Simplify if needed
9. `docs/production/12_SESSION_DATABASE.md` - Check storage explanation

---

## Estimated Total Time

**Discovery (Done):** This session  
**Validation:** 30-45 minutes  
**Storage Emphasis:** 20-30 minutes  
**Dashboards:** 15-20 minutes  
**API Verification:** 20-30 minutes  
**Total:** 85-125 minutes (1.5-2 hours)

---

**Status:** Ready for execution  
**Next:** Run validation checks, then update docs systematically  
**Focus:** MCP/CLI completeness + Storage architecture prominence
