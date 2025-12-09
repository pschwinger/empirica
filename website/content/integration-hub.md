# Integration Hub - CLI, MCP, Python API

**Three ways to integrate Empirica into your AI workflow**

[Back to Home](index.md) | [Architecture →](architecture.md)

---

## Overview

Empirica provides three integration methods, each optimized for different use cases:

1. **📟 CLI Interface** - Command-line tools for human operators and scripts
2. **🔌 MCP Integration** - Model Context Protocol for AI assistants (Claude, etc.)
3. **🐍 Python API** - Programmatic access for custom applications

**All three share the same underlying CASCADE workflow and storage architecture.**

---

## 1. CLI Interface

**For:** Human operators, shell scripts, CI/CD pipelines

### Quick Start

```bash
# Install
pip install empirica-sdk

# Create session
empirica session-create --ai-id myai --output json

# Run CASCADE workflow
empirica preflight --session-id <ID> --prompt "Task description"
empirica preflight-submit --session-id <ID> --vectors '{"know":0.7,...}'

# Create goal
empirica goals-create --session-id <ID> --objective "Build auth system"

# Complete work
empirica postflight --session-id <ID>
```

### Key Commands

**Session Management:**
- `session-create` - Start new session
- `sessions-list` - List all sessions
- `sessions-resume` - Resume previous session

**CASCADE Workflow:**
- `preflight` / `preflight-submit` - Before starting
- `check` / `check-submit` - Mid-work gate
- `postflight` / `postflight-submit` - After completion

**Goals & Tracking:**
- `goals-create` - Create goal with scope
- `goals-add-subtask` - Add subtask
- `goals-complete-subtask` - Mark complete
- `goals-progress` - Check completion %

**Continuity:**
- `checkpoint-create` - Save state to git notes
- `checkpoint-load` - Resume from checkpoint
- `handoff-create` - Create session summary
- `handoff-query` - Get previous context

**Mistakes Tracking:** (New in v4.1)
- `mistake-log` - Record mistakes made
- `mistake-query` - Query past mistakes

[Full CLI Reference →](cli-interface.md)

---

## 2. MCP Integration

**For:** AI assistants (Claude Desktop, Cline, other MCP-compatible tools)

### What is MCP?

**Model Context Protocol** (by Anthropic) enables AI assistants to access external tools and data sources.

**Empirica's MCP server** exposes all CASCADE functionality as tool calls.

### Setup

#### 1. Add to Claude Desktop Config

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "empirica": {
      "command": "python",
      "args": [
        "-m",
        "empirica.mcp_server"
      ],
      "env": {
        "EMPIRICA_DB_PATH": "/path/to/.empirica/sessions/sessions.db"
      }
    }
  }
}
```

#### 2. Restart Claude Desktop

The Empirica tools will appear in Claude's tool palette.

### Available MCP Tools

**Session Management:**
- `session_create(ai_id, bootstrap_level, session_type)`
- `get_session_summary(session_id)`
- `get_epistemic_state(session_id)`

**CASCADE Workflow:**
- `execute_preflight(session_id, prompt)`
- `submit_preflight_assessment(session_id, vectors, reasoning)`
- `execute_check(session_id, findings, unknowns, confidence)`
- `submit_check_assessment(session_id, vectors, decision, reasoning)`
- `execute_postflight(session_id, task_summary)`
- `submit_postflight_assessment(session_id, vectors, reasoning)`

**Goals & Tasks:**
- `create_goal(session_id, objective, scope, success_criteria)`
- `add_subtask(goal_id, description, importance)`
- `complete_subtask(task_id, evidence)`
- `get_goal_progress(goal_id)`
- `get_goal_subtasks(goal_id)` - **Critical for resumption**
- `list_goals(session_id)`

**Continuity:**
- `create_git_checkpoint(session_id, phase, vectors)`
- `load_git_checkpoint(session_id)` - Use alias: `latest:active:ai-id`
- `create_handoff_report(session_id, task_summary, findings, unknowns)`
- `query_handoff_reports(session_id or ai_id, limit)` - **Critical for resumption**

**Edit Guard:** (Metacognitive File Editing)
- `edit_with_confidence(file_path, old_str, new_str, context_source, session_id)`

[Full MCP Reference →](mcp-integration.md)

---

## 3. Python API

**For:** Custom applications, research tools, advanced integrations

### Quick Start

```python
from empirica.data.session_database import SessionDatabase
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger

# Create session
db = SessionDatabase()
session_id = db.create_session(ai_id="myai", bootstrap_level=1)

# PREFLIGHT assessment
logger = GitEnhancedReflexLogger(session_id=session_id)
vectors = {
    'engagement': 0.8,
    'know': 0.65,
    'do': 0.7,
    'uncertainty': 0.35,
    # ... all 13 vectors
}
logger.add_checkpoint(
    phase='PREFLIGHT',
    round_num=1,
    vectors=vectors,
    reasoning="Starting with moderate knowledge"
)

# Do work...

# POSTFLIGHT assessment
logger.add_checkpoint(
    phase='POSTFLIGHT',
    round_num=1,
    vectors=updated_vectors,
    reasoning="Learning complete"
)

db.close()
```

### Core Classes

**SessionDatabase** (`empirica.data.session_database`)
- `create_session(ai_id, bootstrap_level)` - Create session
- `store_vectors(session_id, phase, vectors)` - Store epistemic state
- `query_unknowns_summary(session_id)` - Get unknowns for CHECK phase
- `get_epistemic_state(session_id)` - Get current vectors
- `get_calibration_data(session_id)` - Analyze learning

**GitEnhancedReflexLogger** (`empirica.core.canonical.git_enhanced_reflex_logger`)
- `add_checkpoint(phase, round_num, vectors, reasoning)` - Atomic write to 3 layers
- Storage: SQLite + Git Notes + JSON (atomic)

**EpistemicHandoffReportGenerator** (`empirica.core.handoff`)
- `generate_handoff_report(session_id, task_summary, findings, unknowns)` - Create handoff
- 90%+ token reduction

[Full Python API Reference →](api-reference.md)

---

## Choosing the Right Integration

| Use Case | Best Choice | Why |
|----------|-------------|-----|
| Human operator | **CLI** | Direct shell access, scriptable |
| AI assistant (Claude) | **MCP** | Native tool integration |
| Custom application | **Python API** | Full programmatic control |
| CI/CD pipeline | **CLI** | Shell scripts, exit codes |
| Research analysis | **Python API** | Direct DB access, analytics |
| Multi-agent system | **MCP + Python** | MCP for AIs, Python for orchestration |

---

## Common Integration Patterns

### Pattern 1: CLI + Git Workflow

```bash
# In git pre-commit hook
empirica checkpoint-create --session-id $SESSION_ID
git add .empirica/
git commit -m "Checkpoint: $(date)"
```

### Pattern 2: MCP + Handoff Query

```python
# AI 1 completes work
handoff = create_handoff_report(
    session_id=session1,
    task_summary="Auth implementation complete",
    findings=["OAuth2 flow working", "Token refresh secure"],
    unknowns=["Revocation at scale"]
)

# AI 2 queries and resumes
reports = query_handoff_reports(ai_id="ai1", limit=1)
# AI 2 now has full context
```

### Pattern 3: Python API + Research

```python
# Analyze calibration across sessions
db = SessionDatabase()
sessions = db.query("SELECT * FROM reflexes WHERE phase='POSTFLIGHT'")

learning_deltas = []
for session in sessions:
    preflight = db.get_vectors(session_id, phase='PREFLIGHT')
    postflight = db.get_vectors(session_id, phase='POSTFLIGHT')
    delta = postflight['know'] - preflight['know']
    learning_deltas.append(delta)

avg_learning = sum(learning_deltas) / len(learning_deltas)
print(f"Average KNOW increase: {avg_learning:.2f}")
```

---

## Next Steps

1. **Choose your integration method**
2. **Follow the quick start guide**
3. **Run your first CASCADE workflow**
4. **Explore advanced features** (goals, handoffs, checkpoints)

**Get Started:**
- [CLI Interface Guide](cli-interface.md)
- [MCP Integration Guide](mcp-integration.md)
- [Python API Reference](api-reference.md)
- [Getting Started](getting-started.md)

---

**All roads lead to the same place: epistemic transparency for AI. Pick your path.** 🚀
