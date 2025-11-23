# MCP Server Integration

**Enhance Your IDE with Epistemic Intelligence**

[← Back to CLI](cli-interface.md) | [Skills](skills.md) | [System Prompts](system-prompts.md)

---

## Overview

The Model Context Protocol (MCP) Server is the bridge between Empirica and your AI assistant (like Claude Desktop). It exposes Empirica's metacognitive capabilities directly to the AI, allowing it to "think" using the Empirica framework.

**Key Benefits:**
- **Seamless Integration:** Works natively within Claude Desktop.
- **Context Awareness:** The AI knows your project's epistemic state.
- **Tool Access:** Gives the AI 23+ specialized tools for assessment and investigation.
- **Session Persistence:** Maintains context across chat sessions.

---

## Installation & Setup

### 1. Prerequisite
Ensure you have Empirica installed:
```bash
pip install empirica
```

### 2. Configure Claude Desktop
Add the following to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, or equivalent on Windows/Linux):

```json
{
  "mcpServers": {
    "empirica": {
      "command": "empirica",
      "args": ["mcp", "start"]
    }
  }
}
```

### 3. Restart Claude
Restart the Claude Desktop application. You should see a connection confirmation or the tools becoming available.

---

## Available MCP Tools (23 Total)

The MCP server exposes a comprehensive suite of tools organized by function:

### Session Management
- `bootstrap_session(ai_id, session_type, profile)`: Initialize a new metacognitive session.
- `resume_previous_session(ai_id, count)`: Load context from past work.
- `get_session_summary(session_id)`: Retrieve high-level session data.
- `get_epistemic_state(session_id)`: Check current vector values.

### Assessment Workflow (CASCADE)
- `execute_preflight(session_id, prompt)`: Run initial assessment.
- `submit_preflight_assessment(session_id, vectors)`: Record initial state.
- `execute_check(session_id, findings, ...)`: Validate readiness.
- `submit_check_assessment(session_id, vectors, ...)`: Record check state.
- `execute_postflight(session_id, task_summary)`: Run final reflection.
- `submit_postflight_assessment(session_id, vectors)`: Record learning.

### Goals & Subtasks
- `create_goal(session_id, objective, ...)`: Define a new objective.
- `add_subtask(goal_id, description, ...)`: Break down goals.
- `complete_subtask(task_id, evidence)`: Mark work as done.
- `get_goal_progress(goal_id)`: Check completion status.
- `list_goals(session_id)`: View all goals.

### Continuity
- `create_git_checkpoint(session_id, ...)`: Save state to git notes.
- `load_git_checkpoint(session_id)`: Restore state.
- `create_handoff_report(...)`: Generate a summary for the next AI.
- `query_handoff_reports(...)`: Search past handoffs.

### Help & Guidance
- `get_empirica_introduction()`: Primer on the framework.
- `get_workflow_guidance(phase)`: Instructions for specific phases.
- `cli_help()`: CLI command reference.

---

## Usage Examples

### 1. Starting a Session
**User:** "I need to debug this authentication issue."
**AI (using MCP):**
1. Calls `bootstrap_session(ai_id="claude", session_type="development")`.
2. Calls `execute_preflight(prompt="Debug auth issue")`.
3. Assesses its own knowledge and submits `submit_preflight_assessment`.

### 2. Strategic Investigation
**User:** "The error seems related to the token refresh logic."
**AI (using MCP):**
1. Creates a goal: `create_goal(objective="Fix token refresh bug")`.
2. Adds subtasks: `add_subtask(description="Analyze refresh_token function")`.
3. Investigates and updates state.

### 3. Handoff
**User:** "Let's pause here."
**AI (using MCP):**
1. Calls `execute_postflight`.
2. Calls `create_handoff_report` to save its learnings for the next session.

---

## Troubleshooting

**Server not connecting?**
- Check the path to the `empirica` executable. You may need to use the full path in the config JSON (e.g., `/Users/username/project/.venv/bin/empirica`).
- Verify `empirica mcp start` runs correctly in your terminal.

**Tools not showing?**
- Ensure you are in a project directory where Empirica is installed.
- Check Claude Desktop logs for errors.

---

**Next Steps:**
- [Learn about Skills](skills.md) that the MCP server injects
- [Review System Prompts](system-prompts.md) used by the server
- [See CLI Interface](cli-interface.md) for manual control
