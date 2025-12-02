# Epistemic Handoff: Bugs Found in Goals & Checkpoint Systems

**From:** claude-code  
**To:** Qwen (Bug Fixing)  
**Date:** 2025-12-01  
**Session ID:** 5c6e00d1-f441-4112-be78-072dd8464fc8  
**Task:** Fix critical bugs in checkpoint and database systems

---

## Executive Summary

Audited Empirica goals system and MCP tools. **Goals system works well** ✅ but found **2 critical bugs** ❌ requiring fixes.

**Working Systems:**
- ✅ Goals CRUD (create, list, add-subtask, complete-subtask, progress)
- ✅ MCP tools (29 tools, all accessible via MCP server)
- ✅ CLI commands (55 commands, comprehensive coverage)
- ✅ Identity management (20 identities found, working)
- ✅ Checkpoint creation (creates git notes successfully)

**Broken Systems:**
- ❌ Checkpoint listing (missing method)
- ❌ Database schema (missing `reflexes` table)

---

## Part 1: Critical Bugs Found

### Bug #1: Missing `list_checkpoints` Method ⚠️ CRITICAL

**Location:** `empirica/core/reflex/git_reflex_logger.py`

**Error:**
```bash
$ empirica checkpoint-list --session-id "5c6e00d1-f441-4112-be78-072dd8464fc8"

AttributeError: 'GitEnhancedReflexLogger' object has no attribute 'list_checkpoints'. 
Did you mean: 'add_checkpoint'?
```

**Root Cause:**
- CLI command handler calls: `git_logger.list_checkpoints(limit=limit, phase=phase)`
- But `GitEnhancedReflexLogger` class doesn't have this method
- Only has: `add_checkpoint()` method

**File:** `empirica/cli/command_handlers/checkpoint_commands.py:268`

**Expected Behavior:**
```python
# Should be able to call:
checkpoints = git_logger.list_checkpoints(limit=10, phase="CHECK")

# Should return list of checkpoint metadata from git notes
```

**Impact:** Users cannot view checkpoint history via CLI

**Priority:** HIGH (breaks checkpoint workflow transparency)

---

### Bug #2: Missing `reflexes` Database Table ⚠️ CRITICAL

**Error:**
```bash
$ empirica checkpoint-create --session-id "..." --phase "CHECK" --round 1

Could not load vectors from session: no such table: reflexes
⚠️  Could not load vectors from session: no such table: reflexes
   Creating checkpoint with empty vectors
✅ Checkpoint created successfully
```

**Root Cause:**
- Checkpoint creation tries to load epistemic vectors from `reflexes` table
- Table doesn't exist in database schema
- Checkpoint still succeeds but has **empty vectors** (defeats purpose!)

**Impact:** 
- ❌ Checkpoints created without epistemic state
- ❌ Cannot measure learning deltas from checkpoints
- ❌ ~85% token reduction claim invalid if vectors missing

**Expected Behavior:**
```python
# Should load vectors from database:
vectors = session_db.get_latest_vectors(session_id)

# Checkpoint should contain:
{
  "phase": "CHECK",
  "round": 1,
  "vectors": {
    "know": 0.65,
    "do": 0.80,
    "uncertainty": 0.35,
    # ... all 13 vectors
  }
}
```

**Priority:** CRITICAL (checkpoints useless without vectors)

---

## Part 2: Schema Investigation Needed

**Question for Qwen:** Where should epistemic vectors be stored?

**Options:**
1. **`reflexes` table** - Current code expects this
2. **`assessments` table** - Alternative storage
3. **Session metadata** - Embedded in session record
4. **Separate `vectors` table** - New normalized table

**Current database tables (need verification):**
```sql
-- Confirm which tables exist:
SELECT name FROM sqlite_master WHERE type='table';

-- Expected tables:
-- sessions
-- cascades
-- assessments (?)
-- reflexes (MISSING!)
-- checkpoints (?)
-- goals
-- subtasks
```

**Investigation tasks for Qwen:**
1. Check actual database schema: `sqlite3 .empirica/sessions/sessions.db ".schema"`
2. Find where vectors are actually stored
3. Either:
   - Create missing `reflexes` table, OR
   - Fix checkpoint code to read from correct table

---

## Part 3: What Works (Don't Break This!)

### Goals System: Fully Functional ✅

**Tested commands:**
```bash
# Create goal
empirica goals-create \
  --session-id "5c6e00d1-f441-4112-be78-072dd8464fc8" \
  --objective "Test goal" \
  --scope-breadth 0.4 \
  --scope-duration 0.3 \
  --scope-coordination 0.2 \
  --estimated-complexity 0.5 \
  --success-criteria '["Criterion 1", "Criterion 2"]'

# Add subtasks
empirica goals-add-subtask \
  --goal-id "84b45de9-..." \
  --description "Task description" \
  --importance "high"

# Complete subtask
empirica goals-complete-subtask \
  --task-id "ef240507-..." \
  --evidence "Evidence of completion"

# List goals
empirica goals-list --session-id "5c6e00d1-..."

# Get progress
empirica goals-progress --goal-id "84b45de9-..."
```

**Output (all working):**
```json
{
  "ok": true,
  "goal_id": "84b45de9-e0d6-4c3f-90d9-2b48268de33b",
  "completion_percentage": 66.67,
  "total_subtasks": 3,
  "completed_subtasks": 2
}
```

**Don't change:** Goals database schema, CRUD operations

---

### MCP Tools: All 29 Accessible ✅

**Verified tools list:**
```
1. get_empirica_introduction      16. get_epistemic_state
2. get_workflow_guidance          17. get_session_summary
3. cli_help                       18. get_calibration_report
4. bootstrap_session              19. resume_previous_session
5. execute_preflight              20. create_git_checkpoint
6. submit_preflight_assessment    21. load_git_checkpoint
7. execute_check                  22. create_handoff_report
8. submit_check_assessment        23. query_handoff_reports
9. execute_postflight             24. discover_goals
10. submit_postflight_assessment  25. resume_goal
11. create_goal                   26. create_identity
12. add_subtask                   27. list_identities
13. complete_subtask              28. export_public_key
14. get_goal_progress             29. verify_signature
15. list_goals
```

**File:** `mcp_local/empirica_mcp_server.py`

**Architecture:** Routes to CLI via subprocess (thin wrapper)

**Don't change:** MCP tool definitions, routing logic

---

### CLI Commands: 55 Total ✅

**Categorized by function:**

**Core Workflow (8):**
- bootstrap, preflight, check, postflight
- preflight-submit, check-submit, postflight-submit
- workflow

**Assessment (5):**
- assess, self-awareness, metacognitive, calibration, uvl

**Goals & Tasks (7):**
- goals-create, goals-add-subtask, goals-complete-subtask
- goals-progress, goals-list, goals-discover, goals-resume
- goal-analysis

**Session Management (4):**
- sessions-list, sessions-show, sessions-export, sessions-resume

**Git Checkpoints (4):**
- checkpoint-create ✅
- checkpoint-load ✅
- checkpoint-list ❌ BROKEN
- checkpoint-diff ✅ (probably broken too if list is broken)

**Handoffs (2):**
- handoff-create, handoff-query

**Identity (4):**
- identity-create, identity-list, identity-export, identity-verify

**Investigation (2):**
- investigate, investigate-log

**Actions (1):**
- act-log

**Decision Making (3):**
- decision, decision-batch, feedback

**Performance (2):**
- performance, efficiency-report

**Monitoring (1):**
- monitor

**Configuration (5):**
- config, profile-list, profile-show, profile-create, profile-set-default

**Components (3):**
- list, explain, demo

**User Interfaces (2):**
- ask, chat

**Total:** 55 commands (not 60+ as initially estimated)

---

## Part 4: Fix Instructions for Qwen

### Fix #1: Implement `list_checkpoints` Method

**File to modify:** `empirica/core/reflex/git_reflex_logger.py`

**Add this method to `GitEnhancedReflexLogger` class:**

```python
def list_checkpoints(
    self,
    session_id: Optional[str] = None,
    limit: Optional[int] = None,
    phase: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List checkpoints from git notes.
    
    Args:
        session_id: Filter by session (optional)
        limit: Maximum number to return (optional)
        phase: Filter by phase (PREFLIGHT, CHECK, ACT, POSTFLIGHT) (optional)
    
    Returns:
        List of checkpoint metadata dicts
    """
    checkpoints = []
    
    # Get all git notes in empirica/checkpoint/* namespace
    result = subprocess.run(
        ["git", "notes", "list", "refs/notes/empirica/checkpoint"],
        capture_output=True,
        text=True,
        cwd=self.repo_root
    )
    
    if result.returncode != 0:
        return []
    
    # Parse each note
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        
        note_id = line.split()[0]
        
        # Get note content
        note_result = subprocess.run(
            ["git", "notes", "show", note_id, "--ref=refs/notes/empirica/checkpoint"],
            capture_output=True,
            text=True,
            cwd=self.repo_root
        )
        
        if note_result.returncode == 0:
            try:
                checkpoint = json.loads(note_result.stdout)
                
                # Apply filters
                if session_id and checkpoint.get("session_id") != session_id:
                    continue
                if phase and checkpoint.get("phase") != phase:
                    continue
                
                checkpoints.append(checkpoint)
            except json.JSONDecodeError:
                continue
    
    # Sort by timestamp descending
    checkpoints.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
    
    # Apply limit
    if limit:
        checkpoints = checkpoints[:limit]
    
    return checkpoints
```

**Test after fix:**
```bash
empirica checkpoint-create --session-id "..." --phase "CHECK" --round 1
empirica checkpoint-list --session-id "..."
# Should show checkpoint created above
```

---

### Fix #2: Create `reflexes` Table OR Fix Vector Loading

**Option A: Create missing table**

**File to modify:** `empirica/core/reflex/session_db.py` (or wherever schema is defined)

**Add migration:**
```sql
CREATE TABLE IF NOT EXISTS reflexes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    cascade_id TEXT,
    phase TEXT NOT NULL,  -- PREFLIGHT, CHECK, POSTFLIGHT
    round INTEGER DEFAULT 1,
    timestamp REAL NOT NULL,
    
    -- 13 epistemic vectors
    engagement REAL,
    know REAL,
    do REAL,
    context REAL,
    clarity REAL,
    coherence REAL,
    signal REAL,
    density REAL,
    state REAL,
    change REAL,
    completion REAL,
    impact REAL,
    uncertainty REAL,
    
    -- Metadata
    reasoning TEXT,
    evidence TEXT,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE INDEX IF NOT EXISTS idx_reflexes_session ON reflexes(session_id);
CREATE INDEX IF NOT EXISTS idx_reflexes_phase ON reflexes(phase);
```

**Option B: Fix checkpoint code to use existing table**

**File to modify:** `empirica/cli/command_handlers/checkpoint_commands.py`

**Change line ~260:**
```python
# OLD (broken):
vectors = session_db.load_vectors_from_reflexes(session_id)

# NEW (if using assessments table):
vectors = session_db.get_latest_assessment_vectors(session_id)

# OR (if embedded in session):
session = session_db.get_session(session_id)
vectors = session.get("latest_vectors", {})
```

**Investigation needed:**
```bash
# Check actual schema
sqlite3 .empirica/sessions/sessions.db ".schema" | grep -A20 "CREATE TABLE"

# Find where PREFLIGHT vectors are stored
sqlite3 .empirica/sessions/sessions.db "SELECT name FROM sqlite_master WHERE type='table';"

# Check if assessments table has vectors
sqlite3 .empirica/sessions/sessions.db ".schema assessments"
```

---

## Part 5: Testing Checklist for Qwen

### Automated Regression Tests (MUST PASS!)

**Created 2 new test files:**

1. **`tests/integrity/test_checkpoint_bugs_regression.py`** - 350+ lines
   - Tests for missing list_checkpoints method
   - Tests for missing reflexes table
   - Tests for empty vectors bug
   - Tests CLI command integration

2. **`tests/integration/test_e2e_workflows.py`** - 300+ lines
   - End-to-end checkpoint workflow test
   - End-to-end goals workflow test
   - Database integrity checks

**Run these tests after fixing bugs:**

```bash
# Run regression tests (must all pass!)
pytest tests/integrity/test_checkpoint_bugs_regression.py -v

# Run integration tests
pytest tests/integration/test_e2e_workflows.py -v

# Run all checkpoint-related tests
pytest -k "checkpoint" -v

# Run specific bug tests
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointListMethod -v
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestReflexesTableSchema -v
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointVectorStorage -v
```

### Manual Testing (After Automated Tests Pass)

**Checkpoint System:**
```bash
# 1. Create checkpoint with vectors
empirica checkpoint-create --session-id "$SID" --phase "CHECK" --round 1

# 2. List checkpoints (should work now!)
empirica checkpoint-list --session-id "$SID"

# 3. Verify checkpoint has vectors (not empty!)
empirica checkpoint-load --session-id "$SID"
# Should show: "vectors": {"know": 0.65, "do": 0.80, ...}

# 4. Test git notes directly
git notes show --ref=refs/notes/empirica/checkpoint/<commit>
# Should contain full vector data
```

**Vector Storage:**
```bash
# 5. Submit PREFLIGHT assessment
empirica preflight "test task" --ai-id "test"

# 6. Check vectors stored in database
sqlite3 .empirica/sessions/sessions.db "SELECT * FROM reflexes ORDER BY timestamp DESC LIMIT 1;"
# OR
sqlite3 .empirica/sessions/sessions.db "SELECT * FROM assessments ORDER BY timestamp DESC LIMIT 1;"

# 7. Verify checkpoint loads these vectors
empirica checkpoint-create --session-id "$SID" --phase "PREFLIGHT" --round 1
git notes show <commit> --ref=refs/notes/empirica/checkpoint
# Should contain vectors from assessment
```

### Test Coverage Summary

**Regression Tests Cover:**
- ✅ `list_checkpoints()` method exists and works
- ✅ `list_checkpoints()` filters by session_id, phase, limit
- ✅ `list_checkpoints()` returns sorted results (newest first)
- ✅ `reflexes` table exists in database
- ✅ `reflexes` table has all 13 epistemic vector columns
- ✅ Checkpoints load vectors from database
- ✅ Checkpoints include non-empty vectors
- ✅ CLI commands don't crash with AttributeError
- ✅ End-to-end workflow: bootstrap → preflight → checkpoint → list

**Why These Tests Matter:**
- Previous tests mocked database calls (didn't catch missing table)
- Previous tests didn't test `list_checkpoints` (didn't catch missing method)
- Previous tests didn't verify vector persistence (didn't catch empty vectors)
- These tests verify ACTUAL behavior, not mocked behavior

---

## Part 6: Documentation Updates Needed

After fixes, update these docs:

**1. `docs/production/20_TOOL_CATALOG.md`**
- Add checkpoint-list usage example
- Document vector storage mechanism
- Clarify reflexes table purpose

**2. `docs/guides/GIT_CHECKPOINTS_GUIDE.md`**
- Show checkpoint-list examples
- Explain vector preservation
- Add troubleshooting section

**3. `docs/COMPREHENSIVE_EMPIRICA_UNDERSTANDING.md`**
- Update checkpoint section (lines 38-46)
- Verify "Git checkpoint created ✅" claims are accurate
- Add note about vector storage requirements

---

## Part 7: Epistemic Self-Assessment (PREFLIGHT → Investigation)

**What I Know (0.8):**
- ✅ Goals system works perfectly
- ✅ MCP tools all accessible
- ✅ CLI has 55 commands, 29 MCP tools
- ✅ Checkpoint creation succeeds
- ✅ Identity management functional

**What I Found Broken (0.9 confidence):**
- ❌ `list_checkpoints` method missing (100% certain)
- ❌ `reflexes` table missing (100% certain)
- ⚠️ Checkpoints created with empty vectors (99% certain)

**What I Don't Know (0.4 uncertainty):**
- ⚠️ Where vectors SHOULD be stored (need schema investigation)
- ⚠️ Whether `checkpoint-diff` also broken (likely yes)
- ⚠️ If other commands depend on reflexes table
- ⚠️ Database migration strategy (auto-migrate? manual?)

**Recommended Next Steps:**
1. Qwen investigates database schema (30 min)
2. Qwen implements `list_checkpoints` (1 hour)
3. Qwen fixes vector storage (2-3 hours, depends on architecture)
4. Qwen tests thoroughly (1 hour)
5. I update documentation (1 hour)

**Total effort:** ~5-6 hours

---

## Part 8: Context for Qwen

**You're working with:**
- Codebase: `/home/yogapad/empirical-ai/empirica/`
- Database: `.empirica/sessions/sessions.db` (SQLite)
- Git notes: `refs/notes/empirica/checkpoint/*`
- CLI handlers: `empirica/cli/command_handlers/`
- Core logic: `empirica/core/reflex/`

**Key files to review:**
1. `empirica/core/reflex/git_reflex_logger.py` - Add list_checkpoints
2. `empirica/core/reflex/session_db.py` - Check schema, add reflexes table
3. `empirica/cli/command_handlers/checkpoint_commands.py` - Verify usage
4. `.empirica/sessions/sessions.db` - Inspect actual schema

**Test session for debugging:**
- Session ID: `5c6e00d1-f441-4112-be78-072dd8464fc8`
- AI: `claude-code`
- Has PREFLIGHT assessment submitted
- Has 1 checkpoint created (with empty vectors - bug!)

**Git checkpoint created:**
- Commit: `fbf8047503c155ff93d00bf2f05f2075e3aa62c2`
- Phase: CHECK
- Round: 1
- Note: Contains empty vectors (need to fix!)

---

## Questions for User (Rovodev)

Before Qwen starts, clarify:

1. **Vector storage:** Should we create `reflexes` table or use existing table?
2. **Migration:** Auto-migrate database or require manual migration?
3. **Backward compatibility:** Do we need to support old checkpoints without vectors?
4. **Priority:** Fix bugs before doc consolidation, or parallel work?

---

---

## Part 9: Test Suite Created (NEW!)

**Created 3 comprehensive test files:**

### 1. `tests/integrity/test_checkpoint_bugs_regression.py` (350+ lines)
**Purpose:** Catch the specific bugs we found

**Test Coverage:**
- Missing `list_checkpoints` method (7 tests)
- Missing `reflexes` table (3 tests)
- Empty vectors in checkpoints (3 tests)
- CLI command integration (3 tests)

**Total:** 16+ test methods across 4 test classes

### 2. `tests/integration/test_e2e_workflows.py` (300+ lines)
**Purpose:** Test complete user workflows

**Test Coverage:**
- Full checkpoint workflow (bootstrap → preflight → checkpoint → list)
- Full goals workflow (create → subtasks → complete → progress)
- Database integrity checks
- MCP tools integration (placeholder)

**Total:** 5+ test methods across 4 test classes

### 3. `tests/CHECKPOINT_GOALS_TESTS_README.md`
**Purpose:** Guide for Qwen on how to use tests

**Contents:**
- Why existing tests didn't catch these bugs
- How to run tests (quick + full suites)
- Test file structure explanation
- Expected results (before/after fixes)
- TDD workflow for Qwen
- Troubleshooting guide

---

## Part 10: Why We Needed New Tests

**Existing tests missed these bugs because:**

1. **Database mocking** - Tests mocked database calls, didn't verify actual schema
2. **Incomplete coverage** - Never tested `list_checkpoints` (method didn't exist!)
3. **No vector validation** - Created checkpoints but never verified vectors populated
4. **No end-to-end tests** - Tested components in isolation, not full workflows

**New tests fix this by:**

1. ✅ Testing REAL database (no mocks for schema tests)
2. ✅ Explicitly testing `list_checkpoints` method
3. ✅ Verifying vectors are NOT empty (assert len == 13)
4. ✅ Running complete user workflows end-to-end

---

## Part 11: Qwen's TDD Workflow

### Recommended Approach

**For Bug #1 (list_checkpoints):**
```bash
# 1. Run test (should FAIL)
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointListMethod::test_list_checkpoints_method_exists -v

# 2. Implement fix (add method to git_reflex_logger.py)

# 3. Run test again (should PASS)
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointListMethod::test_list_checkpoints_method_exists -v

# 4. Run all related tests
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointListMethod -v

# 5. All 7 tests should pass
```

**For Bug #2 (reflexes table):**
```bash
# 1. Run test (should FAIL)
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestReflexesTableSchema -v

# 2. Implement fix (create table migration)

# 3. Run test again (should PASS)

# 4. All 3 tests should pass
```

**For Bug #3 (vector storage):**
```bash
# 1. Run test (should FAIL)
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointVectorStorage -v

# 2. Fix vector loading code

# 3. Run test again (should PASS)

# 4. All 3 tests should pass
```

**Final validation:**
```bash
# Run ALL new tests
pytest tests/integrity/test_checkpoint_bugs_regression.py -v
pytest tests/integration/test_e2e_workflows.py -v

# Should see: 20+ tests PASSED
```

---

**Status:** Investigation complete, bugs identified, fix plan ready, **tests created**  
**Next:** Hand off to Qwen for implementation (with TDD guidance)  
**Estimated fix time:** 5-6 hours  
**Priority:** HIGH (checkpoints are core feature, currently broken)

**Test files:**
- ✅ `tests/integrity/test_checkpoint_bugs_regression.py`
- ✅ `tests/integration/test_e2e_workflows.py`
- ✅ `tests/CHECKPOINT_GOALS_TESTS_README.md`

---

**Claude-code signing off** 🚀
