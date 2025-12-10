# GPT-5 CLI Argparse Issues: Fixed

**Date:** 2025-12-10
**Status:** ✅ Resolved
**Issue:** Unknown commands (skill-fetch, profile-list, etc.) showing in argparse

---

## What Was Wrong

GPT-5 was seeing these errors:

```
❌ Unknown command: skill-fetch
❌ Unknown command: profile-list
❌ Missing module 'qdrant_client'
```

**Root causes:**

1. **Unimplemented command parsers defined but not registered**
   - `skill-suggest`, `skill-fetch` parsers defined in cli_core.py
   - But NOT registered in the command_map dispatcher
   - Argparse showed them as valid, but execution failed

2. **Profile commands also unimplemented**
   - `profile-list`, `profile-show`, `profile-create`, `profile-set-default`
   - Same issue: parsers defined but not registered

3. **Missing dependencies**
   - `qdrant_client` needed for project-search
   - `pyyaml` and `requests` needed for other commands

---

## What Was Fixed

### 1. Removed Unimplemented Command Parsers
**File:** `empirica/cli/cli_core.py`

Removed these placeholder command definitions to prevent confusion:
- `skill-suggest` parser (not registered)
- `skill-fetch` parser (not registered)
- `profile-list` parser (not registered)
- `profile-show` parser (not registered)
- `profile-create` parser (not registered)
- `profile-set-default` parser (not registered)

**Before:** Users saw these commands in `--help` but couldn't use them
**After:** Clean help output with only implemented commands

### 2. Installed Missing Dependencies
```bash
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m pip install qdrant-client pyyaml requests
```

Now available:
- ✅ `qdrant_client` - for semantic search
- ✅ `pyyaml` - for config handling
- ✅ `requests` - for HTTP operations

### 3. Verified Clean CLI
```bash
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli --help
# ✅ No unimplemented commands
# ✅ Clean command list
# ✅ No "Unknown command" errors
```

---

## Implemented vs Planned

### ✅ Implemented Commands (Available Now)
```
Session management:
  session-create, sessions-list, sessions-show, sessions-export, sessions-resume

Epistemic assessment (CASCADE):
  preflight, postflight, preflight-submit, check, check-submit, postflight-submit

Investigation/Branching:
  investigate, investigate-create-branch, investigate-checkpoint-branch, investigate-merge-branches

Project tracking:
  project-create, project-handoff, project-list, project-bootstrap, project-search, project-embed

Goal/Subtask management:
  goals-create, goals-add-subtask, goals-complete-subtask, goals-list, goals-discover, goals-resume

Checkpointing:
  checkpoint-create, checkpoint-load, checkpoint-list, checkpoint-diff

Handoff reports:
  handoff-create, handoff-query

Mistake logging:
  mistake-log, mistake-query

Utilities:
  config, monitor, onboard, ask, chat
```

### ⏳ Planned (Phase 4)
```
Skill management:
  skill-suggest, skill-fetch - TO BE IMPLEMENTED

Profile management:
  profile-list, profile-show, profile-create, profile-set-default - TO BE IMPLEMENTED
```

---

## For GPT-5

You can now:

1. **Use all working commands directly**
```bash
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli session-create --ai-id gpt-5
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli project-search --project-id <id> --task "your task"
```

2. **Don't use these commands (not implemented yet)**
```bash
❌ skill-fetch
❌ skill-suggest
❌ profile-list
❌ profile-show
❌ profile-create
❌ profile-set-default
```

3. **Use alternatives**
   - Instead of `skill-suggest`: Use `project-bootstrap --project-id <id>`
   - Instead of `skill-fetch`: Add skills manually to project_skills/
   - Instead of `profile-*`: Use session context instead

---

## Verification

```bash
# Test that unimplemented commands are gone
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli --help 2>&1 | grep -E "skill-|profile-"
# Returns: (nothing) ✅

# Test a working command
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli session-create --ai-id gpt-5 --output json
# Should work without "Unknown command" error ✅

# Test dependencies
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -c "import qdrant_client, yaml; print('✅ Dependencies OK')"
# Output: ✅ Dependencies OK
```

---

## Next Steps

1. **Short term:** Use working commands only
2. **Medium term (Phase 4):** Implement skill and profile commands if needed
3. **Long term:** May not need these commands (project-bootstrap covers most use cases)

---

**Status:** CLI is clean, working, and unambiguous. GPT-5 can use it for all implemented features.
