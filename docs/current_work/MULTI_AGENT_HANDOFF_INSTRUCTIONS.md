# Multi-Agent Goal Handoff - Quick Start

## For Rovo Dev

**Your Goal ID:** `b987fceb-9df1-47c8-90ec-2be65ea774a0`

**Your Tasks:**
1. Auto-drift detection in CHECK phase
2. Actionable error messages in all MCP tools

**Spec:** `docs/current_work/EMPIRICA_RELIABILITY_IMPROVEMENTS_SPEC.md`

### Start Working

```python
# 1. Bootstrap YOUR session
result = bootstrap_session(
    ai_id="rovodev",
    session_type="development",
    bootstrap_level=2  # INTEGER, not string!
)
session_id = result['session_id']

# 2. Execute PREFLIGHT
execute_preflight(session_id=session_id, prompt="...")
submit_preflight_assessment(session_id=session_id, vectors={...}, reasoning="...")

# 3. Adopt the goal
from empirica.core.goals.repository import GoalRepository

repo = GoalRepository()
goal = repo.get_goal('b987fceb-9df1-47c8-90ec-2be65ea774a0')
repo.save_goal(goal, session_id)  # Links goal to YOUR session
repo.close()

# 4. Verify and see your subtasks
my_goals = list_goals(session_id=session_id)
progress = get_goal_progress(goal_id='b987fceb-9df1-47c8-90ec-2be65ea774a0')

# 5. Get detailed subtask info
from empirica.core.tasks.repository import TaskRepository

task_repo = TaskRepository()
subtasks = task_repo.get_goal_subtasks('b987fceb-9df1-47c8-90ec-2be65ea774a0')

for st in subtasks:
    print(f'{st.description}')
    print(f'  Status: {st.status.value}')
    print(f'  ID: {st.id}')

task_repo.close()

# 6. Complete subtasks as you work
complete_subtask(subtask_id='subtask-id', evidence='commit hash or file path')
```

**Your 5 Subtasks:**
1. Modify execute_check to automatically call check_drift_monitor (CRITICAL)
2. Add logic to block ACT phase if severe drift detected (HIGH)
3. Create tests for drift detection integration (HIGH)
4. Add structured error responses to all MCP tools (HIGH)
5. Create troubleshooting documentation (MEDIUM)

---

## For Mini-agent

**Your Goal ID:** `16ae0d29-2919-49e5-b67f-3853e02e0297`

**Your Tasks:**
1. Auto-goal generation from PREFLIGHT
2. Update system prompts with decision criteria

**Spec:** `docs/current_work/EMPIRICA_RELIABILITY_IMPROVEMENTS_SPEC.md`

### Start Working

```python
# 1. Bootstrap YOUR session
result = bootstrap_session(
    ai_id="mini-agent",
    session_type="development",
    bootstrap_level=2  # INTEGER, not string!
)
session_id = result['session_id']

# 2. Execute PREFLIGHT
execute_preflight(session_id=session_id, prompt="...")
submit_preflight_assessment(session_id=session_id, vectors={...}, reasoning="...")

# 3. Adopt the goal
from empirica.core.goals.repository import GoalRepository

repo = GoalRepository()
goal = repo.get_goal('16ae0d29-2919-49e5-b67f-3853e02e0297')
repo.save_goal(goal, session_id)  # Links goal to YOUR session
repo.close()

# 4. Verify and see your subtasks
my_goals = list_goals(session_id=session_id)
progress = get_goal_progress(goal_id='16ae0d29-2919-49e5-b67f-3853e02e0297')

# 5. Get detailed subtask info
from empirica.core.tasks.repository import TaskRepository

task_repo = TaskRepository()
subtasks = task_repo.get_goal_subtasks('16ae0d29-2919-49e5-b67f-3853e02e0297')

for st in subtasks:
    print(f'{st.description}')
    print(f'  Status: {st.status.value}')
    print(f'  ID: {st.id}')

task_repo.close()

# 6. Complete subtasks as you work
complete_subtask(subtask_id='subtask-id', evidence='commit hash or file path')
```

**Your 5 Subtasks:**
1. Modify execute_preflight to auto-call generate_goals if uncertainty > 0.6 (CRITICAL)
2. Include auto-generated goals in PREFLIGHT response (HIGH)
3. Create tests for auto-goal generation logic (HIGH)
4. Update all 7 AI system prompts with decision criteria (MEDIUM)
5. Add YES/NO examples to each system prompt (MEDIUM)

---

## Common Errors to Avoid

❌ **DON'T:** Query goals before bootstrapping your session
❌ **DON'T:** Use `bootstrap_level="optimal"` (it's an integer 0, 1, or 2!)
❌ **DON'T:** Try to access database tables directly
❌ **DON'T:** Assume goals are automatically linked to your session

✅ **DO:** Bootstrap → PREFLIGHT → Adopt goal → Verify → Work
✅ **DO:** Use GoalRepository and TaskRepository for database access
✅ **DO:** Verify access with MCP tools before starting work
✅ **DO:** Mark subtasks complete as you finish them

---

## Architecture Notes

- **Goals table**: Has `session_id` column for linking goals to sessions
- **Subtasks table**: Linked to goals via `goal_id` (no session_id needed)
- **Repositories**: Provide safe, abstracted database access
- **MCP tools**: Use repositories under the hood

When you adopt a goal by updating its `session_id`, all its subtasks automatically become accessible through your session.

---

## For Claude Code (Already in Session)

**My Goal ID:** `3ba2532e-d268-414a-a493-fc485fd8369d`

**My Tasks:**
1. Session aliases in remaining 35 MCP tools
2. Graceful degradation for checkpoint storage

I'm already bootstrapped and working. Can pick this up anytime.

---

**Total Project:** 6 improvements, 270-370 min, 52k tokens estimated across 3 agents

**Dogfooding:** We're using Empirica to make Empirica bulletproof! 🎯
