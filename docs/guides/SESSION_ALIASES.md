# Session Aliases - Quick Reference Guide

## Overview

Session aliases provide an easy way to reference sessions without remembering full UUIDs. This is especially useful after memory compression when you want to resume your most recent work.

## Quick Start

Instead of:
```bash
empirica sessions-show 88dbf132-cc7c-4a4b-9b59-77df3b13dbd2
```

Use:
```bash
empirica sessions-show latest
```

## Supported Aliases

### Basic Aliases

- **`latest`** - Most recent session (any AI, any status)
- **`last`** - Synonym for `latest`

### Filtered Aliases

- **`latest:active`** - Most recent active session (not ended)
- **`latest:<ai_id>`** - Most recent session for specific AI
  - Examples: `latest:claude-code`, `latest:minimax`, `latest:qwen`
- **`latest:active:<ai_id>`** - Most recent active session for specific AI
  - Example: `latest:active:claude-code`

## Where Aliases Work

### CLI Commands

```bash
# Session management
empirica sessions-show latest
empirica sessions-show latest:active
empirica sessions-show latest:claude-code
empirica sessions-export latest:active:claude-code -o current.json

# Checkpoint management
empirica checkpoint-load --session-id latest:active
empirica checkpoint-list --session-id latest
```

### MCP Tools

```python
# Load checkpoint
load_git_checkpoint(session_id="latest:active:claude-code")

# Get epistemic state
get_epistemic_state(session_id="latest")

# Get calibration report
get_calibration_report(session_id="latest:active")

# Get session summary
get_session_summary(session_id="latest:claude-code")
```

### Python API

```python
from empirica.utils.session_resolver import resolve_session_id, get_latest_session_id

# Resolve any alias to UUID
session_id = resolve_session_id("latest:active:claude-code")

# Convenience function
session_id = get_latest_session_id(ai_id="claude-code", active_only=True)
```

## Use Cases

### After Memory Compression

When Claude Code compresses conversation history, you can immediately resume:

```python
# In new conversation after compression
checkpoint = load_git_checkpoint("latest:active:claude-code")

# Continue work from where you left off
```

### In System Prompts

Add to your Claude Code system prompt:

```markdown
After memory compression, resume work:
1. Call: load_git_checkpoint("latest:active:claude-code")
2. If found: Continue from checkpoint
3. If not found: Bootstrap new session
```

### Quick Session Inspection

```bash
# Check your latest session
empirica sessions-show latest

# Export active session for analysis
empirica sessions-export latest:active -o analysis.json

# View recent work
empirica sessions-list --limit 5
```

## Examples

### Example 1: Resume Latest Work

```bash
# See what you were working on
empirica sessions-show latest:active:claude-code

# Export for reference
empirica sessions-export latest:active:claude-code -o last_session.json
```

### Example 2: Compare Sessions

```bash
# Show latest session
empirica sessions-show latest

# Show latest active session (might be different if some ended)
empirica sessions-show latest:active
```

### Example 3: AI-Specific Sessions

```bash
# Claude's latest session
empirica sessions-show latest:claude-code

# Minimax's latest session
empirica sessions-show latest:minimax

# Qwen's latest active session
empirica sessions-show latest:active:qwen
```

## How It Works

1. **Alias Detection**: System checks if input starts with "latest" or equals "last"
2. **Filter Parsing**: Extracts filters from alias parts (`:active`, `:<ai_id>`)
3. **Database Query**: Queries `.empirica/sessions/sessions.db` with filters
4. **UUID Return**: Returns full UUID of most recent matching session

### Resolution Logic

```
latest → SELECT session_id FROM sessions ORDER BY start_time DESC LIMIT 1

latest:active → WHERE end_time IS NULL ORDER BY start_time DESC LIMIT 1

latest:claude-code → WHERE ai_id = 'claude-code' ORDER BY start_time DESC LIMIT 1

latest:active:claude-code → WHERE end_time IS NULL AND ai_id = 'claude-code'
                            ORDER BY start_time DESC LIMIT 1
```

## Backward Compatibility

- ✅ Full UUIDs continue to work: `88dbf132-cc7c-4a4b-9b59-77df3b13dbd2`
- ✅ Partial UUIDs continue to work: `88dbf132` (resolves to full UUID)
- ✅ New aliases are opt-in (optional feature)
- ✅ No breaking changes to existing code

## Error Handling

### No Sessions Found

```bash
$ empirica sessions-show latest:active:nonexistent-ai

❌ No session found for alias: latest:active:nonexistent-ai (ai_id: nonexistent-ai) (active only)
💡 Provided: latest:active:nonexistent-ai
💡 List sessions with: empirica sessions-list
```

### Ambiguous Partial UUID

```bash
$ empirica sessions-show 88d

# If multiple sessions start with "88d", uses most recent
⚠️  Multiple sessions match '88d' - using most recent
```

## Implementation Details

### Files Modified

1. **`empirica/utils/session_resolver.py`** - Core resolver logic
2. **`mcp_local/empirica_mcp_server.py`** - MCP tool integration
3. **`empirica/cli/command_handlers/session_commands.py`** - CLI integration
4. **`empirica/cli/cli_core.py`** - Help text updates

### Functions

```python
# Main resolver
resolve_session_id(session_id_or_alias: str, ai_id: Optional[str] = None) -> str

# Convenience function
get_latest_session_id(ai_id: Optional[str] = None, active_only: bool = False) -> str

# Alias detection
is_session_alias(session_id_or_alias: str) -> bool
```

## Testing

Run tests:
```bash
pytest tests/test_session_resolver.py -v
```

All 11 tests passing:
- ✅ Alias detection
- ✅ Full UUID passthrough
- ✅ Partial UUID resolution
- ✅ `latest` / `last` aliases
- ✅ `latest:active` filter
- ✅ `latest:<ai_id>` filter
- ✅ Compound aliases
- ✅ Convenience function
- ✅ Error handling

## FAQ

### Q: What if multiple sessions match?

**A:** Always returns the most recent (newest `start_time`).

### Q: Can I use partial UUIDs with aliases?

**A:** No. Use either full/partial UUID OR alias, not both. Aliases are complete identifiers.

### Q: What if session database doesn't exist?

**A:** Raises `ValueError` - you need at least one session for aliases to work.

### Q: How do I list all AIs with sessions?

**A:** Use `empirica sessions-list` and look at the AI column.

### Q: Can I create custom aliases?

**A:** Not yet. Currently only `latest`, `last`, and filtered variants are supported.

## Related Documentation

- [CASCADE Workflow](../production/06_CASCADE_FLOW.md)
- [Git Checkpoints Guide](./GIT_CHECKPOINTS_GUIDE.md)
- [Session Continuity](../production/23_SESSION_CONTINUITY.md)

## Summary

Session aliases solve the session continuity problem:
- ✅ No need to track UUIDs across memory compression
- ✅ Simple, intuitive syntax (`latest`, `latest:active`, etc.)
- ✅ Works everywhere session_id is accepted (CLI, MCP, Python)
- ✅ Fully tested and backward compatible

**Start using:** Just replace any session UUID with `latest` and you're done!
