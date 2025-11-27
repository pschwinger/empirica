# MCP Server Integration

**Enhance Any AI Environment with Epistemic Intelligence.**

Works with **Claude Desktop**, **Cursor**, **Windsurf**, and **Antigravity**.

---

## Available Tools (23 Total)

<!-- BENTO_START -->

## 🛠️ Session Management
**Control your epistemic lifecycle.**

- `bootstrap_session`: Initialize session.
- `resume_previous_session`: Load context.
- `get_epistemic_state`: Check vectors.

## 🔄 Assessment Workflow
**Run the CASCADE.**

- `execute_preflight`: Initial assessment.
- `execute_check`: Validate readiness.
- `execute_postflight`: Final reflection.

## 🎯 Goals & Continuity
**Track progress and state.**

- `create_goal`: Define objectives.
- `create_git_checkpoint`: Save to git notes.
- `create_handoff_report`: Generate summary.

<!-- BENTO_END -->

---

## Setup Instructions

### 1. Configure MCP Client
Add to your config (e.g., `claude_desktop_config.json`):

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

### 2. Restart Client
Restart your IDE or MCP client. Tools will appear immediately.

---

## Usage Examples

### Starting a Session
**User:** "Debug auth issue."
**AI:** Calls `bootstrap_session` -> `execute_preflight`.

### Strategic Investigation
**User:** "Check token logic."
**AI:** Calls `create_goal` -> `add_subtask` -> Investigates.

### Handoff
**User:** "Pause here."
**AI:** Calls `execute_postflight` -> `create_handoff_report`.

---

**Next Steps:**
- [Learn about Skills](skills.md)
- [System Prompts](developers/system-prompts.md)
- [CLI Interface](developers/cli-interface.md)
