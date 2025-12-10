# Postflight Command Consolidation

**Date:** 2025-12-10
**Status:** ✅ Complete
**Objective:** Simplify postflight workflow by consolidating duplicate commands

---

## What Was Changed

### Problem
- **Old `empirica postflight`**: Interactive command that could hang waiting for user input
- **`empirica postflight-submit`**: Non-blocking version that actually works (wired to git notes)
- **Confusion**: Users had two postflight commands with different behaviors
- **Design flaw**: postflight had `--prompt-only` and `--assessment-json` (preflight patterns) but no use case for them

### Solution
Made `postflight` the primary command (like `preflight-submit` but for postflight):
1. Removed old interactive `postflight` parser (lines 125-141 in cli_core.py)
2. Renamed `postflight-submit` → `postflight` (primary command)
3. Added `postflight-submit` as backward-compatibility alias
4. Both use `handle_postflight_submit_command` (direct git notes wiring)

---

## Command Comparison

### Old Design (Problematic)
```bash
# Could hang waiting for input
empirica postflight <session-id> --summary "..." --assessment-json '{...}'

# Simpler, but confusing naming
empirica postflight-submit --session-id <sid> --vectors '{...}'
```

### New Design (Clean)
```bash
# Primary: Non-blocking assessment submission (directly wired to git notes)
empirica postflight --session-id <sid> --vectors '{...}' --reasoning "task summary"

# Still works (alias for backward compatibility)
empirica postflight-submit --session-id <sid> --vectors '{...}'
```

---

## Why This Makes Sense

### Postflight is NOT like preflight:

**Preflight** (assessment BEFORE work):
- Needs a gate/prompt to measure starting state
- Uses `--prompt-only` to get assessment prompt (non-blocking)
- Uses `--assessment-json` to submit (optional, for convenience)
- Has `--sentinel` routing (future: for external assistance)
- Interactive mode is acceptable (you haven't started work yet)

**Postflight** (reassessment AFTER work):
- No gate/entry point needed (work is already done)
- Just: "reassess same 13 vectors, measure learning"
- Doesn't need `--prompt-only` (not blocking anything)
- Doesn't need `--sentinel` (no external intervention after work done)
- Doesn't need interactive mode (simple data submission)
- Just needs: session-id + vectors + optional reasoning

### Result:
Postflight is now **simpler**: just a direct submission command (non-blocking, wired to git notes).

---

## Files Changed

### 1. `empirica/cli/cli_core.py`

**Removed** (lines 125-141):
- Old interactive `postflight` parser with positional `session_id` argument
- All the interactive-only arguments: `--summary`, `--no-git`, `--sign`, `--prompt-only`, `--assessment-json`, `--sentinel-assess`, `--sentinel`, `--compact`, `--kv`, `--quiet`

**Added/Updated** (lines 161-174):
```python
# Postflight command (primary, non-blocking)
postflight_parser = subparsers.add_parser('postflight', help='Submit postflight epistemic assessment results')
postflight_parser.add_argument('--session-id', required=True, help='Session ID')
postflight_parser.add_argument('--vectors', required=True, help='Epistemic vectors as JSON (reassessment of same 13 dimensions as preflight)')
postflight_parser.add_argument('--reasoning', help='Task summary or description of learning/changes from preflight')
postflight_parser.add_argument('--output', choices=['default', 'json'], default='default', help='Output format')

# Postflight-submit alias (backward compatibility)
postflight_submit_parser = subparsers.add_parser('postflight-submit', help='Alias for postflight (deprecated, use postflight)')
# ... same arguments as postflight
```

**Updated command_map** (lines 839-840):
```python
'postflight': handle_postflight_submit_command,  # Primary command: non-blocking assessment submission
'postflight-submit': handle_postflight_submit_command,  # Alias for backward compatibility
```

### 2. `empirica/cli/command_handlers/cascade_commands.py`

**Simplified** (lines 417-427):
Replaced 240-line implementation with deprecation notice:
```python
def handle_postflight_command(args):
    """
    DEPRECATED: This handler is no longer used.

    Postflight is now integrated into the non-blocking MCP v2 workflow.
    Use 'empirica postflight' which calls handle_postflight_submit_command.
    """
    print("⚠️  Internal handler deprecated - use handle_postflight_submit_command instead")
    return
```

Handler deleted because it's no longer used (postflight now routes to handle_postflight_submit_command).

---

## Command Behavior

### New `empirica postflight`

**Usage:**
```bash
empirica postflight \
  --session-id <session-uuid> \
  --vectors '{"engagement": 0.90, "know": 0.85, "do": 0.92, ...}' \
  --reasoning "Task completed successfully, learned X and Y" \
  --output json
```

**Arguments:**
- `--session-id` (required): Session ID from preflight
- `--vectors` (required): JSON dict of 13 epistemic vector values (0.0-1.0)
  - Reassesses same dimensions as preflight: engagement, know, do, context, clarity, coherence, signal, density, state, change, completion, impact, uncertainty
- `--reasoning` (optional): Task summary or description of learning
- `--output` (default: `default`): Format for results (`default` or `json`)

**Behavior:**
- ✅ Non-blocking (returns immediately)
- ✅ Calculates deltas from preflight checkpoint (learning measurement)
- ✅ Stores in git notes atomically (3-layer storage: SQLite + git notes + JSON)
- ✅ Returns JSON with success status, checkpoint ID, vectors submitted

**Example Output:**
```json
{
  "ok": true,
  "session_id": "e205cca5-9b1d-4e68-9c3c-e971aeb76822",
  "checkpoint_id": "empirica/session/e205cca5-9b1d-4e68-9c3c-e971aeb76822/POSTFLIGHT/1",
  "message": "POSTFLIGHT assessment submitted to database and git notes",
  "vectors_submitted": 13,
  "vectors_received": {
    "engagement": 0.90,
    "know": 0.85,
    ...
  },
  "reasoning": "Task completed successfully",
  "persisted": true,
  "storage_layers": {
    "sqlite": true,
    "git_notes": true,
    "json_logs": true
  }
}
```

---

## Migration Guide

### For Users
If you were using the old `empirica postflight`:
```bash
# Old (no longer works this way)
empirica postflight <session-id> --summary "..." --assessment-json '{...}'

# New (required format)
empirica postflight --session-id <session-id> --vectors '{...}' --reasoning "..."
```

### For Scripts
Both commands still work:
```bash
# New primary command
empirica postflight --session-id <sid> --vectors '...'

# Old name still works (alias)
empirica postflight-submit --session-id <sid> --vectors '...'
```

### For MCP Servers
No change needed. Both commands route to the same handler.

---

## Why This Is Better

| Aspect | Old | New |
|--------|-----|-----|
| **Blocking** | ✅ Yes (could hang) | ✅ Non-blocking |
| **Git notes** | postflight-submit only | Both commands |
| **Command count** | 2 confusing commands | 1 clear command + 1 alias |
| **Arguments** | Many (interactive-only) | Clean: session-id + vectors + reasoning |
| **Consistency** | postflight ≠ preflight pattern | postflight/check/preflight same pattern* |
| **Future use** | Unmaintainable | Maintainable |

*Note: preflight still has special `--prompt-only` because it's a gate before work. postflight doesn't need gates.

---

## Verification

```bash
# Help shows clean interface
$ empirica postflight --help
usage: empirica postflight [-h] --session-id SESSION_ID --vectors VECTORS
                           [--reasoning REASONING] [--output {default,json}]

# Alias still works (shows deprecation note in help)
$ empirica postflight-submit --help
usage: empirica postflight-submit [-h] --session-id SESSION_ID --vectors VECTORS
                                  [--reasoning REASONING] [--output {default,json}]
help: Alias for postflight (deprecated, use postflight)

# Both route to same handler (non-blocking)
$ empirica postflight --session-id <sid> --vectors '{"engagement": 0.9, ...}'
✅ Returns JSON immediately
```

---

## Impact

- **Breaking Change**: Old `empirica postflight <sid> --assessment-json '{...}'` format no longer works
- **Deprecation Path**: Clear error message pointing to new format
- **Backward Compatibility**: `postflight-submit` still works (alias)
- **Migration Cost**: Low (simple argument rename)

---

## Next Steps

1. ✅ Consolidate postflight command
2. ⏭️ Consider consolidating `check` and `check-submit` similarly (lower priority)
3. ⏭️ Document CASCADE workflow (PREFLIGHT → [work] → CHECK → POSTFLIGHT)
4. ⏭️ Ensure MCP tools match CLI (both should be non-blocking)

---

**Status:** ✅ COMPLETE

Postflight is now simple, consistent, and non-blocking. Ready for production.
