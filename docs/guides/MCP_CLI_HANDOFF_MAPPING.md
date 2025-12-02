# MCP-CLI Handoff Mapping Reference

**Status:** ✅ **Homologous** - Mapping is consistent and working correctly  
**Last Updated:** 2025-12-02  
**Issue:** None - error was user workflow, not mapping

---

## Overview

The MCP server and CLI handoff commands are **fully homologous** - parameters map 1:1 with appropriate naming conventions (snake_case → kebab-case).

---

## Parameter Mapping

### `create_handoff_report` MCP Tool → `handoff-create` CLI Command

| MCP Parameter (snake_case) | CLI Flag (kebab-case) | Type | Required | Description |
|----------------------------|----------------------|------|----------|-------------|
| `session_id` | `--session-id` | string | ✅ | Session UUID or alias (e.g., `latest:active:copilot`) |
| `task_summary` | `--task-summary` | string | ✅ | What was accomplished (2-3 sentences) |
| `key_findings` | `--key-findings` | JSON array | ✅ | Key learnings from session |
| `remaining_unknowns` | `--remaining-unknowns` | JSON array | ❌ | What's still unclear |
| `next_session_context` | `--next-session-context` | string | ✅ | Critical context for next session |
| `artifacts_created` | `--artifacts` | JSON array | ❌ | Files created (e.g., `["src/fix.py", "docs/updated.md"]`) |

### `query_handoff_reports` MCP Tool → `handoff-query` CLI Command

| MCP Parameter | CLI Flag | Type | Required | Description |
|--------------|----------|------|----------|-------------|
| `session_id` | `--session-id` | string | ❌ | Specific session UUID |
| `ai_id` | `--ai-id` | string | ❌ | Filter by AI ID |
| `limit` | `--limit` | integer | ❌ | Number of results (default: 5) |

---

## Example Usage

### MCP Tool Call (Python/JSON)

```python
# Via MCP tool
create_handoff_report(
    session_id="latest:active:copilot",
    task_summary="Fixed MCP-CLI handoff parameter mapping inconsistencies",
    key_findings=[
        "Mapping was already correct - arrays convert properly",
        "Error was workflow-related, not technical",
        "Improved error messages for missing assessments"
    ],
    remaining_unknowns=[
        "Need to test edge cases with complex session aliases"
    ],
    next_session_context="Handoff system fully validated and documented",
    artifacts_created=[
        "docs/guides/MCP_CLI_HANDOFF_MAPPING.md",
        "empirica/core/handoff/report_generator.py"
    ]
)
```

### CLI Command (Bash)

```bash
empirica handoff-create \
  --session-id "latest:active:copilot" \
  --task-summary "Fixed MCP-CLI handoff parameter mapping inconsistencies" \
  --key-findings '["Mapping was already correct - arrays convert properly", "Error was workflow-related, not technical"]' \
  --remaining-unknowns '["Need to test edge cases with complex session aliases"]' \
  --next-session-context "Handoff system fully validated and documented" \
  --artifacts '["docs/guides/MCP_CLI_HANDOFF_MAPPING.md", "empirica/core/handoff/report_generator.py"]' \
  --output json
```

**Key Points:**
- JSON arrays must be properly quoted in CLI
- MCP server automatically converts arrays to JSON strings
- CLI handler automatically parses JSON strings back to arrays
- The round-trip is **lossless**

---

## How MCP → CLI Conversion Works

### 1. MCP Tool Call (User's AI)

```python
arguments = {
    "session_id": "latest:active:copilot",
    "key_findings": ["Finding 1", "Finding 2"],  # Python array
    "artifacts_created": ["file1.py"]
}
```

### 2. MCP Server Builds CLI Command

```python
# From mcp_local/empirica_mcp_server.py build_cli_command()
arg_map = {
    "key_findings": "key-findings",
    "remaining_unknowns": "remaining-unknowns",
    "next_session_context": "next-session-context",
    "artifacts_created": "artifacts",
}

# Converts to:
cmd = [
    "empirica", "handoff-create",
    "--session-id", "latest:active:copilot",
    "--key-findings", '["Finding 1", "Finding 2"]',  # JSON string
    "--artifacts", '["file1.py"]'
]
```

### 3. CLI Handler Parses Arguments

```python
# From empirica/cli/command_handlers/handoff_commands.py
key_findings = json.loads(args.key_findings) 
# Converts back to: ["Finding 1", "Finding 2"]

artifacts = json.loads(args.artifacts) if args.artifacts else []
# Converts back to: ["file1.py"]
```

### 4. Core Function Receives Native Types

```python
# From empirica/core/handoff/report_generator.py
generator.generate_handoff_report(
    session_id=session_id,
    key_findings=key_findings,  # Python list
    artifacts_created=artifacts  # Python list
)
```

**Result:** ✅ **Lossless round-trip** - Arrays stay as arrays throughout the pipeline

---

## Common Issues

### ❌ Issue: Missing Assessments Error

```bash
❌ Handoff create error: Missing assessments for session latest:active:copilot. 
PREFLIGHT: False, POSTFLIGHT: False
```

**Cause:** Handoff reports require completed CASCADE workflow

**Solution:** Complete the full workflow:

```python
# 1. Bootstrap session
bootstrap_session(ai_id="copilot")  # Returns session_id

# 2. Execute PREFLIGHT
execute_preflight(session_id, prompt="Task description")
submit_preflight_assessment(session_id, vectors={...}, reasoning="...")

# 3. Do your work (investigate, act, check, etc.)

# 4. Execute POSTFLIGHT
execute_postflight(session_id, task_summary="What was done")
submit_postflight_assessment(session_id, vectors={...}, reasoning="...")

# 5. NOW create handoff
create_handoff_report(
    session_id=session_id,
    task_summary="...",
    key_findings=[...],
    next_session_context="..."
)
```

**Why?** Handoff reports measure epistemic deltas (POSTFLIGHT - PREFLIGHT). Without assessments, there's no delta to measure.

---

## Verification

### Test Command Generation

```python
import json

# Simulate MCP tool call
arguments = {
    "session_id": "test-123",
    "key_findings": ["Finding 1", "Finding 2"],
    "artifacts_created": ["file.py"]
}

# What MCP generates
for key, value in arguments.items():
    if isinstance(value, list):
        print(f"--{key.replace('_', '-')} '{json.dumps(value)}'")
    else:
        print(f"--{key.replace('_', '-')} {value}")
```

**Output:**
```bash
--session-id test-123
--key-findings '["Finding 1", "Finding 2"]'
--artifacts-created '["file.py"]'
```

### Test CLI Parsing

```bash
# Run actual CLI command
empirica handoff-create \
  --session-id "test-123" \
  --task-summary "Test" \
  --key-findings '["Finding 1"]' \
  --next-session-context "Test" \
  --output json
```

---

## Architecture Notes

### Why This Design?

**MCP Layer (Python types):**
- AI agents work with native Python data structures
- Type hints provide clarity: `List[str]`, `Dict[str, Any]`
- No manual JSON encoding required

**CLI Layer (JSON strings):**
- Shell arguments are always strings
- Complex types (arrays, objects) encoded as JSON strings
- Follows standard CLI conventions (e.g., `kubectl`, `aws`)

**Core Layer (Python types):**
- Business logic works with native types
- No awareness of transport layer (MCP vs CLI vs API)
- Type safety enforced with Pydantic models

### Benefits

1. **Type Safety:** MCP schemas enforce correct types at API boundary
2. **CLI Compatibility:** JSON strings work across all shells (bash, zsh, fish)
3. **Homologous Mapping:** 1:1 correspondence makes debugging trivial
4. **Lossless Conversion:** Round-trip preserves exact data structures
5. **Extensible:** New parameters added in both places with same pattern

---

## Related Documentation

- [Session Aliases Guide](SESSION_ALIASES.md) - Understanding session ID resolution
- [Git Checkpoints Guide](GIT_CHECKPOINTS_GUIDE.md) - Phase 1.5 checkpointing system
- [CASCADE Workflow](../production/06_CASCADE_FLOW.md) - Full workflow explanation

---

## Summary

✅ **MCP-CLI handoff mapping is homologous and working correctly**  
✅ **Error was workflow-related (missing assessments), not technical**  
✅ **Documentation and error messages improved**  
✅ **No code changes needed to mapping logic**

The system is production-ready for multi-agent handoff coordination.
