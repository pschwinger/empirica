# MCP Integration - Model Context Protocol

**Connect Empirica to AI assistants like Claude Desktop, Cline, and other MCP-compatible tools**

[← Back to Integration Hub](integration-hub.md) | [Python API →](api-reference.md)

---

## What is MCP?

**Model Context Protocol** (by Anthropic) is a standard that enables AI assistants to access external tools and data sources.

**Empirica's MCP server** exposes all CASCADE workflow functionality as tool calls, giving AI assistants:
- ✅ Epistemic self-awareness (13 vectors)
- ✅ Session continuity (checkpoints, handoffs)
- ✅ Goal tracking (findings, unknowns, dead ends)
- ✅ Mirror drift monitoring (calibration tracking)

---

## Installation

```bash
# Install Empirica
pip install empirica-sdk

# Verify MCP server is available
python -m empirica.mcp_server --help
```

---

## Setup for Claude Desktop

### 1. Locate Config File

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

### 2. Add Empirica MCP Server

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

**Note:** Replace `/path/to/.empirica/` with your actual Empirica database path. Default: `~/.empirica/`

### 3. Restart Claude Desktop

The Empirica tools will appear in Claude's tool palette.

---

## Available MCP Tools

### Session Management

**`session_create(ai_id, bootstrap_level, session_type)`**
- Create new Empirica session
- Returns session_id for use in all other tools
- Example: `session_create("claude-code", 1, "development")`

**`get_session_summary(session_id)`**
- Get session metadata and current state
- Returns: ai_id, created_at, epistemic_state, goal_progress

**`get_epistemic_state(session_id)`**
- Get current epistemic vectors (13D)
- Returns: KNOW, DO, UNCERTAINTY, CONTEXT, etc.

---

### CASCADE Workflow

#### PREFLIGHT (Before Starting)

**`execute_preflight(session_id, prompt)`**
- Generate self-assessment prompt as JSON
- AI performs genuine self-assessment (13 vectors)
- Returns: Assessment prompt for AI to complete

**`submit_preflight_assessment(session_id, vectors, reasoning)`**
- Submit PREFLIGHT epistemic assessment
- Stores in reflexes table + git notes + JSON
- Example vectors: `{"engagement":0.8, "know":0.6, "do":0.7, "uncertainty":0.3, ...}`

#### CHECK (Mid-Work Gate)

**`execute_check(session_id, findings, unknowns, confidence)`**
- Gate decision: proceed or investigate more?
- Findings: What you learned (validated knowledge)
- Unknowns: What's still unclear (breadcrumbs for investigation)
- Confidence: 0.0-1.0 (≥0.7 = proceed, <0.7 = investigate)

**`submit_check_assessment(session_id, vectors, decision, reasoning)`**
- Submit CHECK assessment with updated epistemic state
- Decision: "proceed" (high confidence) or "investigate" (more work needed)
- Triggers calibration tracking if drift detected

#### POSTFLIGHT (After Completion)

**`execute_postflight(session_id, task_summary)`**
- Generate final self-assessment prompt
- Measures learning: PREFLIGHT → POSTFLIGHT delta

**`submit_postflight_assessment(session_id, vectors, reasoning)`**
- Submit final epistemic assessment
- Calibration: Compare predicted vs actual learning
- Well-calibrated agent = predictions match reality

---

### Goals & Subtasks (Investigation Tracking)

**`create_goal(session_id, objective, scope, success_criteria)`**
- Create goal with scope vectors (breadth, duration, coordination)
- Scope: 0.0-1.0 (breadth: single function → entire codebase)
- Returns: goal_id

**`add_subtask(goal_id, description, importance)`**
- Add subtask to goal
- Importance: 'critical' | 'high' | 'medium' | 'low'
- Tracks findings, unknowns, dead ends

**`complete_subtask(task_id, evidence)`**
- Mark subtask complete with evidence
- Evidence: commit hash, file path, test results

**`get_goal_progress(goal_id)`**
- Get completion percentage
- Shows completed vs pending subtasks

**`get_goal_subtasks(goal_id)`** ⚠️ **CRITICAL FOR RESUMPTION**
- Get detailed subtask list with status
- Shows: completed work (don't redo!), pending work, findings, unknowns
- **Always query this when resuming work**

**`list_goals(session_id)`**
- List all goals for session
- Returns: goal_id, objective, scope, progress

---

### Session Continuity (Epistemic Handoffs)

**`create_git_checkpoint(session_id, phase, vectors, metadata)`**
- Save compressed checkpoint to git notes
- **75%+ token reduction** vs full context
- Checkpoint size: ~65 tokens vs ~2600 baseline

**`load_git_checkpoint(session_id)`**
- Load latest checkpoint
- **Use alias:** `"latest:active:ai-id"` (e.g., `"latest:active:claude-code"`)
- Returns: Full epistemic state at checkpoint

**`create_handoff_report(session_id, task_summary, findings, unknowns, next_context)`**
- Create session handoff report
- **75%+ token reduction** vs full context  
- Handoff size: ~238 tokens vs full session context
- Includes: task summary, key findings, remaining unknowns, next steps

**`query_handoff_reports(session_id OR ai_id, limit)`** ⚠️ **CRITICAL FOR RESUMPTION**
- Query previous handoffs by session_id or ai_id
- **Always query this when resuming work**
- Returns: findings (what you learned), unknowns (what to investigate), artifacts (files created)
- Example: `query_handoff_reports(ai_id="claude-code", limit=1)`

---

### Mistakes Tracking (Learning System)

**`mistake_log(session_id, mistake, why_wrong, prevention, cost_estimate)`**
- Record mistakes made during work
- Why wrong: Root cause analysis
- Prevention: How to avoid in future
- Cost estimate: Time wasted

**`mistake_query(session_id OR ai_id, limit)`**
- Query past mistakes to learn from
- **Query before starting similar work**
- Prevents repeating known failure patterns

---

### Edit Guard (Metacognitive File Editing)

**`edit_with_confidence(file_path, old_str, new_str, context_source, session_id)`**
- Edit files with epistemic confidence assessment
- Prevents 80% of edit failures (4.7x higher success rate)
- Context sources:
  - `"view_output"` - Just read this file (high confidence)
  - `"fresh_read"` - Read 1-2 turns ago (medium confidence)
  - `"memory"` - Working from memory (triggers re-read)
- Selects optimal strategy: atomic_edit (≥0.70), bash_fallback (≥0.40), re_read_first (<0.40)
- Returns: success status, strategy used, confidence score

---

## Workflow Example

### Typical MCP Workflow

```python
# 1. Create session
session_id = session_create("claude-code", 1, "development")

# 2. PREFLIGHT assessment
preflight = execute_preflight(session_id, "Implement OAuth2 authentication")
# AI self-assesses 13 vectors
submit_preflight_assessment(
    session_id, 
    vectors={"engagement":0.8, "know":0.6, "do":0.7, "uncertainty":0.35, ...},
    reasoning="Starting with moderate knowledge, high uncertainty about token refresh"
)

# 3. Create goal
goal_id = create_goal(
    session_id,
    objective="Implement OAuth2 with PKCE",
    scope={"breadth": 0.3, "duration": 0.4, "coordination": 0.1},
    success_criteria=["Auth flow works", "Tokens refresh securely", "Tests pass"]
)

# 4. Add subtasks
add_subtask(goal_id, "Research OAuth2 PKCE flow", importance="high")
add_subtask(goal_id, "Implement token exchange", importance="critical")
add_subtask(goal_id, "Write tests", importance="high")

# 5. Investigate (as needed)
# Work, learn, track findings/unknowns

# 6. CHECK gate (before implementing)
execute_check(
    session_id,
    findings=["PKCE prevents auth code interception", "Refresh rotation required"],
    unknowns=["Token revocation strategy"],
    confidence=0.75
)
submit_check_assessment(
    session_id,
    vectors={"know":0.75, "do":0.8, "uncertainty":0.2, ...},
    decision="proceed"
)

# 7. Do the work
# Implement, test, iterate

# 8. POSTFLIGHT assessment
execute_postflight(session_id, "OAuth2 with PKCE complete, refresh rotation working")
submit_postflight_assessment(
    session_id,
    vectors={"engagement":0.9, "know":0.85, "do":0.9, "uncertainty":0.15, ...},
    reasoning="Learned token rotation prevents theft, confident in implementation"
)

# 9. Create handoff for next session
create_handoff_report(
    session_id,
    task_summary="OAuth2 authentication with PKCE and refresh token rotation",
    findings=[
        "PKCE prevents authorization code interception",
        "Refresh token rotation mitigates theft risk",
        "Secure storage required for refresh tokens"
    ],
    unknowns=["Token revocation at scale"],
    next_context="Auth system functional, next: build authorization layer"
)
```

---

## Resuming Work (Critical Pattern)

**When resuming work, ALWAYS query to get context:**

```python
# 1. Query handoff for breadcrumbs
reports = query_handoff_reports(ai_id="claude-code", limit=1)
# Returns: findings, unknowns, artifacts, next_context

# 2. Get goal details
goals = list_goals(session_id)
subtasks = get_goal_subtasks(goal_id)
# Returns: completed (don't redo!), pending, findings, unknowns

# 3. Load checkpoint (optional)
state = load_git_checkpoint("latest:active:claude-code")
# Returns: Full epistemic state at checkpoint

# 4. Query mistakes (learn from past errors)
mistakes = mistake_query(ai_id="claude-code", limit=5)
# Avoid repeating known failure patterns
```

**Why This Matters:**
- **Findings** = Validated knowledge (build on this!)
- **Unknowns** = Investigation targets (breadcrumbs!)
- **Subtasks** = Work structure (avoid duplication!)
- **Mistakes** = Failure patterns (don't repeat!)

---

## Session Aliases (Convenience)

Instead of UUID, use aliases:

- `latest` - Most recent session (any AI, any status)
- `latest:active` - Most recent active (not ended) session
- `latest:active:<ai-id>` - Most recent active for specific AI

Example:
```python
# Load checkpoint using alias
state = load_git_checkpoint("latest:active:claude-code")
```

---

## Integration Patterns

### Pattern 1: Single-Session Workflow

```python
# Simple task, complete in one session
session_create() → preflight → goal → work → postflight
```

### Pattern 2: Multi-Session Workflow

```python
# Day 1: Investigation
session_create() → preflight → goal → investigate → check → handoff

# Day 2: Implementation
query_handoff() → resume → work → postflight
```

### Pattern 3: Multi-Agent Coordination

```python
# AI 1: Research
session_create() → goal → investigate → handoff

# AI 2: Implementation (queries AI 1's handoff)
query_handoff(ai_id="ai1") → goal_resume() → work
```

---

## Troubleshooting

### Tools Not Appearing in Claude

1. Check config file location is correct
2. Verify JSON syntax (use https://jsonlint.com/)
3. Restart Claude Desktop completely
4. Check logs: `~/.config/Claude/logs/mcp.log`

### Database Path Issues

```json
{
  "env": {
    "EMPIRICA_DB_PATH": "/full/path/to/.empirica/sessions/sessions.db"
  }
}
```

Use absolute paths, not `~` or `$HOME`.

### Session Alias Not Found

```python
# If alias fails, use UUID directly
sessions = list_sessions()  # Get list of sessions
session_id = sessions[0]['session_id']  # Use first session
```

---

## Next Steps

1. **Setup:** Add Empirica to Claude Desktop config
2. **Create Session:** Use `session_create()`
3. **Run CASCADE:** PREFLIGHT → work → POSTFLIGHT
4. **Track Goals:** Create goals with scope and subtasks
5. **Resume Efficiently:** Query handoffs and mistakes

**Learn More:**
- [CLI Interface](cli-interface.md) - Command-line tools
- [Python API](api-reference.md) - Programmatic access
- [Integration Hub](integration-hub.md) - Choose your integration
- [Getting Started](getting-started.md) - Quick start guide

---

**MCP brings epistemic self-awareness directly to AI assistants. No context switching, no manual tracking.** 🚀
