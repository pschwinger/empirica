# System Prompt Clarification Needed

## Current System Prompt
- Generic Empirica prompt describing MCP tools
- Mentions CASCADE workflow (correct)
- Shows MCP tool usage examples (correct)

## Potential Confusion Points

### 1. "generate_goals" vs "create_goal"
**System prompt says:**
```python
goals_result = generate_goals(
    session_id=session_id,
    conversation_context="...",
    use_epistemic_state=True
)
```

**What this actually means:**
- This is NOT automatic goal generation
- AI should call `create_goal` MCP tool explicitly when it identifies a goal
- Goals are created on-demand, not automatically from findings

### 2. Goals vs Investigation
**System prompt suggests:** Goals are generated for investigation
**Reality:** 
- Investigation can happen without goals (via investigate-log)
- Goals are for trackable work (via create_goal, add_subtask)
- AI decides when goals are needed

## Recommendation

Add clarification section to system prompt:

```markdown
## Goal Management

Goals are created **explicitly by you** when you identify work that needs tracking:

```python
# When you identify a goal during investigation:
create_goal(
    session_id=session_id,
    objective="Fix database column mismatch",
    scope="task_specific",
    success_criteria=["All queries work", "Tests pass"]
)

# Break into subtasks:
add_subtask(
    goal_id="goal-123",
    description="Update utility_commands.py",
    epistemic_importance=0.8
)

# As you complete work:
complete_subtask(subtask_id="task-456", evidence="Fixed and tested")
```

**Key:** Goals are not automatically generated. You create them when needed.
```

## Files That Need Updates
1. `/home/yogapad/.rovodev/config_empirica.yml` - Add clarification section
2. `docs/user-guides/ROVODEV.md` - Update if it exists

