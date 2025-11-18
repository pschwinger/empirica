# Minimax Phase 2 Validation Tasks (CORRECTED)
**Date:** 2025-11-17
**Prepared By:** Claude (Co-Lead)
**Corrected By:** Claude (based on Minimax's accurate assessment)
**Status:** Ready for Validation
**Priority:** HIGH - Final validation before Nov 20 launch

---

## ⚠️ CORRECTIONS FROM ORIGINAL DOCUMENT

**Thanks to Minimax's thorough review, the following corrections were made:**

### ❌ INCORRECT: "JSON Import Bug"
**Original Claim:** Missing `import json` on line 15 of tracker.py
**Reality:** `import json` is **already present** on line 15
**Conclusion:** No bug exists - either already fixed by RovoDev or never was an issue

### ⚠️ INCORRECT: MCP Tool Names
**Original Claims:**
- `query_goal_timeline` ❌
- `query_commits_by_date` ❌

**Actual Implementation:**
- `query_git_progress` ✅
- `get_unified_timeline` ✅

**Source:** Verified in `mcp_local/empirica_mcp_server.py`

---

## Executive Summary

**Phase 2 Complete:** ✅ Git Notes Integration for Multi-Agent Coordination
**Code Status:** ✅ Working (no outstanding bugs)
**MCP Tools:** ✅ 3 new tools registered with correct names
**Ready For:** ✅ Minimax validation of Phase 2 functionality

---

## What Was Added (Phase 2)

### 🆕 New Features:

1. **Git Notes Integration** - Store task metadata in git for team coordination
2. **Git Query Tools** - Lead AIs can query git for progress tracking
3. **Team Progress API** - Multi-goal tracking across agents
4. **Unified Timeline** - Historical view with task metadata

### 🆕 New Files:

```
empirica/core/completion/
├── git_query.py          # NEW: GitProgressQuery class
├── tracker.py            # EXISTING: No changes needed (json already imported)
└── types.py              # EXISTING: CompletionRecord, CompletionMetrics
```

### 🆕 New MCP Tools (3 additional):

**From Phase 1 (already validated):**
1. `create_goal` - Create structured goal
2. `create_subtask` - Create task under goal
3. `update_subtask_status` - Mark tasks complete
4. `track_goal_progress` - Get completion percentage
5. `query_session_goals` - List goals for session

**Phase 2 Additions (CORRECTED NAMES):**
6. **`query_git_progress`** - Get commits with task metadata for a goal
7. **`get_team_progress`** - Track progress across multiple goals
8. **`get_unified_timeline`** - Unified timeline view with task metadata

---

## API Reference for Phase 2 (CORRECTED)

### GitProgressQuery Class

```python
from empirica.core.completion.git_query import GitProgressQuery

query = GitProgressQuery()

# 1. Get git progress for specific goal
git_progress = query.get_goal_timeline(
    goal_id="goal-uuid",
    max_commits=100  # default: 100
)
# Returns: {'goal_id': str, 'commits': [{'hash': str, 'message': str, 'date': str, 'task_metadata': dict}]}
# MCP Tool: query_git_progress

# 2. Get team progress across multiple goals
team_status = query.get_team_progress(
    goal_ids=["goal1", "goal2", "goal3"]
)
# Returns: {'goals': [{'goal_id': str, 'commit_count': int, 'task_count': int, 'commits': [...]}]}
# MCP Tool: get_team_progress

# 3. Get unified timeline (combines multiple queries)
unified = query.get_unified_timeline(
    goal_ids=["goal1", "goal2"],
    max_commits=50
)
# Returns: Combined timeline across goals
# MCP Tool: get_unified_timeline
```

---

## Validation Tests for Minimax

### Test 1: GitProgressQuery Functionality

**Objective:** Verify Phase 2 git query class works

**Test:**
```python
from empirica.core.completion.git_query import GitProgressQuery
from empirica.core.goals.types import Goal, SuccessCriterion, GoalScope
from empirica.core.tasks.types import SubTask, EpistemicImportance
import uuid

# Create test goal
goal = Goal.create(
    objective="Phase 2 Validation Test",
    scope=GoalScope.TASK_SPECIFIC,
    success_criteria=[
        SuccessCriterion(
            id=str(uuid.uuid4()),
            description="Git query tools work",
            validation_method="manual"
        )
    ]
)
print(f"✅ Goal: {goal.id[:8]}")

# Create subtask
subtask = SubTask.create(
    goal_id=goal.id,
    description="Validate git query functionality",
    epistemic_importance=EpistemicImportance.HIGH
)
print(f"✅ Subtask: {subtask.id[:8]}")

# Test GitProgressQuery
query = GitProgressQuery()
print(f"Git available: {query.git_available}")

# Test 1: Get goal timeline (MCP: query_git_progress)
timeline = query.get_goal_timeline(goal.id, max_commits=10)
assert 'commits' in timeline
assert isinstance(timeline['commits'], list)
print(f"✅ query_git_progress: {len(timeline['commits'])} commits")

# Test 2: Get team progress (MCP: get_team_progress)
team_status = query.get_team_progress([goal.id])
assert 'goals' in team_status
print(f"✅ get_team_progress: {len(team_status['goals'])} goals")

# Test 3: Get unified timeline (MCP: get_unified_timeline)
unified = query.get_unified_timeline([goal.id], max_commits=10)
assert 'goals' in unified
print(f"✅ get_unified_timeline: {len(unified['goals'])} goals")

print("\n✅ ALL GIT QUERY TOOLS VALIDATED!")
```

**Expected:** All assertions pass, no errors
**Status:** ⚠️ NEEDS VALIDATION by Minimax

---

### Test 2: MCP Tool Registration

**Objective:** Verify MCP tools are registered with correct names

**Test:**
```python
# Check MCP server registration
import subprocess
import json

# Query MCP server for tools list
result = subprocess.run(
    ['python', 'mcp_local/empirica_mcp_server.py', '--list-tools'],
    capture_output=True,
    text=True,
    timeout=10
)

# Parse tool names
tools = []  # Parse from result.stdout

# Verify Phase 2 tools exist with correct names
phase2_tools = [
    'query_git_progress',     # ✅ CORRECT NAME
    'get_team_progress',      # ✅ CORRECT NAME
    'get_unified_timeline'    # ✅ CORRECT NAME
]

for tool_name in phase2_tools:
    assert tool_name in tools, f"Missing: {tool_name}"
    print(f"✅ MCP tool registered: {tool_name}")

print("\n✅ ALL PHASE 2 MCP TOOLS REGISTERED!")
```

**Expected:** All 3 tools found
**Status:** ⚠️ NEEDS VALIDATION by Minimax

---

### Test 3: Integration with Phase 1

**Objective:** Verify Phase 2 builds on Phase 1 without breaking changes

**Test:**
```python
from empirica.core.goals.types import Goal, GoalScope, SuccessCriterion
from empirica.core.tasks.types import SubTask, TaskStatus, EpistemicImportance
from empirica.core.completion.tracker import CompletionTracker
from empirica.core.completion.git_query import GitProgressQuery
import uuid

# Phase 1: Create goal and track progress
goal = Goal.create(
    objective="Integration Test",
    scope=GoalScope.TASK_SPECIFIC,
    success_criteria=[
        SuccessCriterion(
            id=str(uuid.uuid4()),
            description="Phase 1 + 2 work together",
            validation_method="manual"
        )
    ]
)

subtask = SubTask.create(
    goal_id=goal.id,
    description="Test integration",
    epistemic_importance=EpistemicImportance.HIGH
)

# Phase 1: Track progress
tracker = CompletionTracker(enable_git_notes=True)
progress = tracker.track_progress(goal.id)
print(f"✅ Phase 1 progress tracking: {progress.completion_percentage:.1f}%")

# Mark complete
tracker.task_repo.update_subtask_status(
    subtask.id,
    TaskStatus.COMPLETED,
    completion_evidence="Integration validated"
)

# Phase 2: Query git for progress
query = GitProgressQuery()
timeline = query.get_goal_timeline(goal.id)
print(f"✅ Phase 2 git query: {len(timeline['commits'])} commits")

# Phase 2: Team progress
team = query.get_team_progress([goal.id])
print(f"✅ Phase 2 team tracking: {len(team['goals'])} goals")

print("\n✅ PHASE 1 + PHASE 2 INTEGRATION VALIDATED!")
```

**Expected:** Both Phase 1 and Phase 2 functionality work together
**Status:** ⚠️ NEEDS VALIDATION by Minimax

---

## What Minimax Already Validated (Phase 1)

✅ **Goal creation working**
✅ **SubTask creation working**
✅ **Status updates working**
✅ **Progress tracking working** (<15ms performance)
✅ **Input validation comprehensive**

**These DO NOT need re-validation** - already confirmed in Phase 1

---

## New Validation Checklist (Phase 2 Only)

- [ ] **GitProgressQuery class instantiates**
- [ ] **get_goal_timeline() returns valid data**
- [ ] **get_team_progress() handles multiple goals**
- [ ] **get_unified_timeline() combines data correctly**
- [ ] **MCP tools registered with correct names:**
  - [ ] `query_git_progress`
  - [ ] `get_team_progress`
  - [ ] `get_unified_timeline`
- [ ] **Git notes contain task metadata (if git available)**
- [ ] **Integration with Phase 1 works** (no breaking changes)
- [ ] **Performance acceptable** (<100ms for queries)
- [ ] **Graceful fallback** (no git = empty results, no errors)

---

## Known Limitations (Not Bugs)

### 1. Git Availability

**Behavior:** Git query tools require git repository
**Impact:** Returns empty results if git not available
**Mitigation:** Check `query.git_available` flag
**Not a bug:** Graceful fallback by design

### 2. Git Notes Population

**Behavior:** Notes added by `auto_update_from_recent_commits()`
**Timing:** On-demand (not automatic)
**Impact:** Requires explicit call to annotate commits
**Not a bug:** Design choice for control

### 3. Query Performance

**Behavior:** Git operations can be slow with large histories
**Impact:** May take >50ms for 100+ commits
**Mitigation:** Use `max_commits` parameter
**Not a bug:** Git performance characteristic

---

## Corrected Success Criteria

### Critical (Must Pass):
1. ✅ ~~JSON import fix~~ (not needed - already present)
2. ⚠️ All 3 git query tools functional
3. ⚠️ MCP tools use correct names (`query_git_progress`, etc.)
4. ⚠️ Phase 1 + Phase 2 integration works
5. ⚠️ End-to-end workflow completes

### Important (Should Pass):
6. ⚠️ Performance <100ms for queries
7. ⚠️ Graceful fallback when git unavailable
8. ⚠️ Git notes contain proper metadata

---

## Recommended Testing Approach (Corrected)

### Step 1: Import Validation (2 min)
```python
from empirica.core.completion.git_query import GitProgressQuery
query = GitProgressQuery()
print(f"✅ Git available: {query.git_available}")
```

### Step 2: API Validation (10 min)
Test each method: `get_goal_timeline()`, `get_team_progress()`, `get_unified_timeline()`

### Step 3: MCP Tool Names (5 min)
Verify tools are registered as:
- `query_git_progress` (not `query_goal_timeline`)
- `get_team_progress`
- `get_unified_timeline` (not `query_commits_by_date`)

### Step 4: Integration Test (15 min)
Run Phase 1 + Phase 2 together (test script above)

### Step 5: Performance Check (10 min)
Measure query times with realistic data

**Total Estimated Time:** 42 minutes (reduced from 50)

---

## What Minimax Correctly Identified

✅ **JSON import already present** - Not a bug
✅ **MCP tool naming discrepancies** - Corrected above
✅ **Phase 2 document accurate in spirit** - Core functionality exists
✅ **Testing approach sound** - Aligns with Phase 1 methodology

**Excellent attention to detail!** These corrections make the validation more accurate.

---

## Final Recommendation (Updated)

**Phase 2 Status:** ✅ **READY FOR VALIDATION** (no bugs blocking)

**Critical Path:**
1. Verify GitProgressQuery works (10 min)
2. Check MCP tool names correct (5 min)
3. Test Phase 1 + Phase 2 integration (15 min)
4. Performance validation (10 min)
5. Report findings (10 min)

**Total Time:** ~50 minutes

**Expected Outcome:** Phase 2 validated for production launch Nov 20

---

**Prepared by:** Claude (Co-Lead)
**Corrected based on:** Minimax's accurate assessment
**Status:** All corrections applied, ready for validation
**Date:** 2025-11-17
