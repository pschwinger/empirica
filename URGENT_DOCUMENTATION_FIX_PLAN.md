# URGENT: Documentation Fix for All System Prompts

## 🚨 CRITICAL ISSUE

**ALL system prompts and user guides reference non-existent `generate_goals` command!**

This will break user trust immediately on launch.

---

## 📊 FILES REQUIRING FIX (12 files)

### System Prompts
1. `/home/yogapad/.rovodev/config_empirica.yml` - Rovo Dev system prompt
2. `docs/user-guides/GENERIC_EMPIRICA_SYSTEM_PROMPT.md` - Base template
3. `docs/user-guides/SYSTEM_PROMPT_QUICK_REFERENCE.md`
4. `docs/user-guides/SYSTEM_PROMPT_ADDITION_SESSION_CASCADE.md`
5. `docs/user-guides/SYSTEM_PROMPTS_FOR_AI_AGENTS.md`

### Platform-Specific Guides
6. `docs/user-guides/CLAUDE.md`
7. `docs/user-guides/COPILOT_CLAUDE.md`
8. `docs/user-guides/GEMINI.md`
9. `docs/user-guides/QWEN.md`
10. `docs/user-guides/MINIMAX.md`

### Documentation
11. `docs/user-guides/ROVODEV.md`
12. `docs/user-guides/COMPLETE_MCP_TOOL_REFERENCE.md`

---

## 🔧 FIND & REPLACE OPERATIONS

### Replace Pattern 1: generate_goals MCP tool
```bash
# FIND:
generate_goals(
    session_id=session_id,
    conversation_context="...",
    use_epistemic_state=True
)

# REPLACE WITH:
create_goal(
    session_id=session_id,
    objective="Your goal description",
    scope="task_specific",
    success_criteria=["Criteria 1", "Criteria 2"]
)
```

### Replace Pattern 2: query_goal_orchestrator
```bash
# FIND:
from empirica.cli import query_goal_orchestrator
goals = query_goal_orchestrator(session_id=session_id)

# REPLACE WITH:
# Goals are created explicitly via MCP tools:
# create_goal(), add_subtask(), complete_subtask()
# Query via: empirica goals-list --session-id <id>
```

### Replace Pattern 3: "Goal orchestrator" terminology
```bash
# FIND: "Goal orchestrator"
# REPLACE WITH: "Goal management (explicit)"
```

### Replace Pattern 4: Automatic language
```bash
# FIND: "generates systematic investigation goals"
# REPLACE WITH: "Create goals explicitly when you identify work"

# FIND: "Use goal orchestrator"
# REPLACE WITH: "Create goals explicitly"
```

---

## 🚀 FAST FIX SCRIPT

```bash
#!/bin/bash
# Fix all documentation files at once

FILES=(
    "/home/yogapad/.rovodev/config_empirica.yml"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/GENERIC_EMPIRICA_SYSTEM_PROMPT.md"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/CLAUDE.md"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/GEMINI.md"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/QWEN.md"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/MINIMAX.md"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/ROVODEV.md"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/COPILOT_CLAUDE.md"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/SYSTEM_PROMPT_QUICK_REFERENCE.md"
    "/home/yogapad/empirical-ai/empirica/docs/user-guides/COMPLETE_MCP_TOOL_REFERENCE.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Fixing: $file"
        
        # Replace generate_goals with create_goal
        sed -i 's/generate_goals(/create_goal(/g' "$file"
        
        # Replace query_goal_orchestrator with goals-list
        sed -i 's/query_goal_orchestrator/goals-list/g' "$file"
        
        # Replace "Goal orchestrator" with "Goal management"
        sed -i 's/Goal orchestrator/Goal management/g' "$file"
        sed -i 's/goal orchestrator/goal management/g' "$file"
        
        # Update descriptions
        sed -i 's/Generates systematic investigation goals/Create goals explicitly when you identify work/g' "$file"
        sed -i 's/generates systematic/creates/g' "$file"
        
        echo "  ✅ Fixed"
    fi
done

echo ""
echo "✅ All files fixed!"
```

---

## ⚠️ MANUAL VERIFICATION NEEDED

After running the script, manually verify:

1. **Context makes sense** - Automatic sed might break some sentences
2. **Code examples are correct** - Ensure create_goal has right parameters
3. **MCP vs CLI distinction** - Some places need MCP tools, others need CLI commands

---

## 🎯 PRIORITY ORDER

### Critical (Must fix before launch)
1. `/home/yogapad/.rovodev/config_empirica.yml` - Active system prompt
2. `GENERIC_EMPIRICA_SYSTEM_PROMPT.md` - Base template
3. `CLAUDE.md`, `GEMINI.md` - Most popular platforms

### Important (Fix soon after launch)
4. `QWEN.md`, `MINIMAX.md` - Other platforms
5. `COMPLETE_MCP_TOOL_REFERENCE.md` - Developer docs

### Nice to have
6. Other documentation files

---

## 📝 CORRECT EXAMPLES TO USE

### MCP Tool Usage (Python in IDE)
```python
# Create goal explicitly
create_goal(
    session_id=session_id,
    objective="Fix authentication bug",
    scope="task_specific",
    success_criteria=["Auth works", "Tests pass"]
)

# Add subtasks
add_subtask(
    goal_id=goal_id,
    description="Update token validation",
    epistemic_importance=0.8
)

# Complete subtask
complete_subtask(
    subtask_id=task_id,
    evidence="Implemented and all tests passing"
)
```

### CLI Usage (Bash)
```bash
# Create goal
empirica goals-create --session-id <id> --objective "Fix bug"

# List goals
empirica goals-list --session-id <id>

# Add subtask
empirica goals-add-subtask --goal-id <goal-id> --description "..."

# Complete subtask
empirica goals-complete-subtask --subtask-id <task-id> --evidence "..."
```

---

## ⏱️ TIME ESTIMATE

- **Automated sed script:** 5 minutes
- **Manual verification:** 30 minutes
- **Testing:** 15 minutes
- **Total:** ~50 minutes

---

## 🚨 RECOMMENDATION

**Run the sed script NOW to fix all files at once, then manually verify critical ones.**

This is a blocking issue for launch - users will immediately encounter commands that don't exist.

**Priority:** CRITICAL ⚠️⚠️⚠️
