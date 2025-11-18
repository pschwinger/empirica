# Goal Architecture Testing - Handoff to Minimax

**Status:** Core implementation complete, ready for testing  
**Assignee:** Minimax  
**Priority:** HIGH  
**Estimated Time:** 2-3 hours  
**Blockers Fixed:** ✅ canonical_epistemic_assessment.py profile parameter fix (all tests passing)

---

## IMPORTANT: Blocker Was Fixed ✅

**Issue:** `NameError: name 'profile' is not defined` in canonical_epistemic_assessment.py  
**Status:** ✅ FIXED (all 9 canonical assessor tests now pass)  
**Impact:** No longer blocking - you can proceed with testing

---

## What Was Implemented

### 1. Session Type Validation Fix ✅
- **File:** `mcp_local/empirica_mcp_server.py`
- **Change:** Made `session_type` free-form instead of enum-restricted
- **Added:** Smart `bootstrap_level` inference (0=minimal, 1=standard, 2=full)
- **Impact:** AIs can now use contextual labels like "research", "teaching", "interactive"

### 2. Core Goal Architecture ✅
**New Modules Created:**
- `empirica/core/goals/` - Goal management (types, repository, validation)
- `empirica/core/tasks/` - Task decomposition (types, repository)
- `empirica/core/completion/` - Completion tracking (types, tracker)

**Total:** 10 new Python files, all compile successfully

### 3. MCP Tool Integration ✅
**New Tools:**
- `create_goal` - Create structured goals with success criteria
- `add_subtask` - Break goals into actionable tasks
- `complete_subtask` - Mark tasks complete with evidence
- `get_goal_progress` - Track completion percentage
- `list_goals` - Query goals with filters

### 4. Input Validation ✅
- **File:** `empirica/core/goals/validation.py`
- **Validates:** Objectives, success criteria, complexity, epistemic importance
- **Integrated:** Into MCP handlers with clear error messages

### 5. Git Parsing (Phase 1) ✅
- **File:** `empirica/core/completion/tracker.py`
- **Feature:** `auto_update_from_recent_commits()` method
- **Commit Patterns:** `✅ [TASK:uuid]`, `[COMPLETE:uuid]`, `Addresses subtask uuid`
- **Benefit:** Automatic task completion from git commits

### 6. Comprehensive Tests ✅
- **File:** `tests/integration/test_goal_architecture_e2e.py`
- **Coverage:** Complete workflow, input validation, serialization, querying

## Your Mission: Test Everything

### Test 1: Run the Test Suite

```bash
cd /home/yogapad/empirical-ai/empirica
pytest tests/integration/test_goal_architecture_e2e.py -v
```

**Expected:** All tests pass ✅

**If tests fail:**
- Check error messages
- Verify database initialization
- Check imports

### Test 2: Test MCP Tools End-to-End

**Manual test using the new MCP tools:**

```python
# Bootstrap a session
bootstrap_session(
    ai_id="minimax-tester",
    session_type="testing",  # Now accepts any string!
    ai_model="minimax-1.0"
)

# Test 1: Create a goal
result = create_goal(
    session_id="<your-session-id>",
    objective="Test the new Goal Architecture MCP tools",
    success_criteria=[
        {
            "description": "All MCP tools respond correctly",
            "validation_method": "completion"
        },
        {
            "description": "Test coverage >= 80%",
            "validation_method": "metric_threshold",
            "threshold": 0.8
        }
    ],
    scope="task_specific",
    estimated_complexity=0.5
)

# Extract goal_id from result
goal_id = result['goal_id']

# Test 2: Add subtasks
subtask1 = add_subtask(
    goal_id=goal_id,
    description="Test create_goal tool",
    epistemic_importance="critical",
    estimated_tokens=500
)

subtask2 = add_subtask(
    goal_id=goal_id,
    description="Test add_subtask tool",
    epistemic_importance="high",
    estimated_tokens=300
)

subtask3 = add_subtask(
    goal_id=goal_id,
    description="Test complete_subtask tool",
    epistemic_importance="high",
    estimated_tokens=400
)

# Test 3: Check initial progress
progress = get_goal_progress(goal_id=goal_id)
assert progress['completion_percentage'] == 0.0
assert len(progress['remaining_subtasks']) == 3

# Test 4: Complete a subtask
complete_subtask(
    subtask_id=subtask1['subtask_id'],
    evidence="manual-test-completion"
)

# Test 5: Check updated progress
progress = get_goal_progress(goal_id=goal_id)
assert progress['completion_percentage'] == 0.33  # 1/3 complete
assert len(progress['completed_subtasks']) == 1
assert len(progress['remaining_subtasks']) == 2

# Test 6: Complete remaining subtasks
complete_subtask(subtask_id=subtask2['subtask_id'])
complete_subtask(subtask_id=subtask3['subtask_id'])

# Test 7: Verify 100% completion
progress = get_goal_progress(goal_id=goal_id)
assert progress['completion_percentage'] == 1.0

# Test 8: List goals
goals = list_goals(session_id="<your-session-id>", is_completed=True)
assert len(goals['goals']) >= 1
```

### Test 3: Test Input Validation

**Test invalid inputs to verify validation works:**

```python
# Should FAIL: Empty objective
try:
    create_goal(
        objective="",  # Invalid!
        success_criteria=[{"description": "Test", "validation_method": "completion"}]
    )
    assert False, "Should have raised validation error"
except Exception as e:
    assert "empty" in str(e).lower()

# Should FAIL: Invalid scope
try:
    create_goal(
        objective="Test",
        success_criteria=[{"description": "Test", "validation_method": "completion"}],
        scope="invalid_scope"  # Invalid!
    )
    assert False, "Should have raised validation error"
except Exception as e:
    assert "scope" in str(e).lower()

# Should FAIL: Missing validation_method
try:
    create_goal(
        objective="Test",
        success_criteria=[{"description": "Test"}]  # Missing validation_method!
    )
    assert False, "Should have raised validation error"
except Exception as e:
    assert "validation_method" in str(e).lower()

# Should FAIL: metric_threshold without threshold
try:
    create_goal(
        objective="Test",
        success_criteria=[{
            "description": "Test",
            "validation_method": "metric_threshold"  # Missing threshold!
        }]
    )
    assert False, "Should have raised validation error"
except Exception as e:
    assert "threshold" in str(e).lower()
```

### Test 4: Test Git Parsing (Optional)

**If you want to test git commit tracking:**

```bash
# Create a test goal and subtask
goal_id="<your-goal-id>"
subtask_id="<your-subtask-id>"

# Make a commit with the subtask ID
git commit -m "✅ [TASK:${subtask_id}] Implement test feature

This commit completes the test subtask.
"

# Run auto-update
python3 -c "
from empirica.core.completion.tracker import CompletionTracker
tracker = CompletionTracker()
count = tracker.auto_update_from_recent_commits('${goal_id}', since='1 minute ago')
print(f'Auto-completed {count} tasks')
tracker.close()
"

# Verify subtask was auto-completed
get_goal_progress(goal_id=goal_id)
# Should show the subtask as completed with evidence "commit:abc1234"
```

## Expected Issues & How to Fix

### Issue 1: Database Connection Error
**Symptom:** `sqlite3.OperationalError: unable to open database file`  
**Fix:** Check database path, ensure write permissions

### Issue 2: Import Errors
**Symptom:** `ModuleNotFoundError: No module named 'empirica.core.goals'`  
**Fix:** Run `pip install -e .` from empirica root directory

### Issue 3: MCP Server Not Responding
**Symptom:** MCP tools return errors  
**Fix:** Restart MCP server: `python mcp_local/empirica_mcp_server.py`

### Issue 4: Git Parsing Fails
**Symptom:** `auto_update_from_recent_commits` returns 0  
**Fix:** 
- Ensure you're in a git repository
- Check commit message format includes task ID
- Verify `since` parameter is correct

## Success Criteria

✅ **Test 1:** All pytest tests pass  
✅ **Test 2:** Can create goal, add 3 subtasks, complete them, track progress  
✅ **Test 3:** Input validation catches all invalid inputs  
✅ **Test 4 (Optional):** Git parsing auto-completes tasks from commits  

## Deliverables

When done, please create:

1. **Test Results Document**
   - File: `docs/current_work/GOAL_ARCHITECTURE_TEST_RESULTS.md`
   - Include: Test outputs, any failures, edge cases discovered

2. **Bug Report (if any issues)**
   - File: `docs/current_work/GOAL_ARCHITECTURE_BUGS.md`
   - Include: Steps to reproduce, expected vs actual behavior

3. **Performance Notes**
   - How fast are database operations?
   - Any bottlenecks with large goal sets?
   - Token efficiency observations?

## Integration with Existing Systems

**Already Compatible:**
- ✅ Works with existing `SessionDatabase`
- ✅ Coexists with `canonical_goal_orchestrator` (no conflicts)
- ✅ Uses same database file as other Empirica components
- ✅ MCP server integrated seamlessly

**Future Work (NOT for this test):**
- Phase 2: Git notes integration
- Phase 3: Multi-agent coordination
- Phase 4: Automatic task decomposition (LLM-based)

## Questions to Answer During Testing

1. **Usability:** Are the MCP tool interfaces intuitive?
2. **Performance:** How long does `track_progress` take with 100 subtasks?
3. **Robustness:** Does validation catch all edge cases?
4. **Git Integration:** Does commit parsing work reliably?
5. **Documentation:** Is the design doc clear enough?

## Resources

- **Design Doc:** `docs/current_work/GIT_PARSING_GOAL_TRACKING_DESIGN.md`
- **Architecture Doc:** `docs/current_work/ROVODEV_MINIMAX_GOAL_ARCHITECTURE_HANDOFF.md`
- **Tests:** `tests/integration/test_goal_architecture_e2e.py`
- **Code:** `empirica/core/{goals,tasks,completion}/`

## Contact

If you encounter issues or have questions:
- Check existing documentation in `docs/current_work/`
- Review implementation in source files
- Document any ambiguities for future clarification

**Good luck, Minimax! Let's validate this architecture! 🚀**
