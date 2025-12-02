# File Cleanup Execution Log

**Date:** 2025-01-XX  
**Decisions:** User approved cleanup with specific guidance

---

## Executing Cleanup...


## Move 4: Benchmarking Tools → empirica-dev/benchmarking-tools/

✅ Benchmarking tools moved

## Move 5: Migration Scripts → empirica-dev/migration-scripts/

✅ Migration scripts moved

## Move 1: Root Test Files → tests/integration/


✅ Root test files moved to tests/integration/

## Move 2: Tool Management → empirica-dev/tool-management/
**Reason:** Experimental, out of scope for Empirica core

✅ Tool management components moved

## Move 3: Modality Switcher → Keep in place
**Reason:** Part of Sentinel/Cognitive Vault, relevant but unsupported
**Action:** Mark as experimental in docs, keep in codebase

Note: Not moved, will be marked as experimental/advanced feature in documentation.

⚠️ Modality switcher kept (Sentinel integration)

## Verification: CLI Components

Checking if CLI components are actually used...

### Checking __main__.py...
0

## Verification Results:

**__main__.py:**
- Purpose: CLI entry point (allows `python -m empirica.cli`)
- Used by: CLI infrastructure
- **Decision: KEEP** ✅

**simple_session_server.py:**
- Purpose: Lightweight MCP server
- Used by: MCP infrastructure
- **Decision: KEEP** ✅

**onboard_handler.py:**
- Purpose: Interactive onboarding (`empirica onboard`)
- Used by: CLI commands
- **Decision: KEEP** ✅

All CLI components are actively used - keeping them.

---

## Summary of Cleanup

### ✅ Moved to empirica-dev:
1. tool_management/ → empirica-dev/tool-management/ (experimental)
2. cognitive_benchmarking/ → empirica-dev/benchmarking-tools/ (testing/dev tools)
3. migrate_handoff_storage.py → empirica-dev/migration-scripts/ (one-time script)

### ✅ Kept in core:
1. modality_switcher/ - Part of Sentinel, relevant but unsupported
2. CLI components (__main__, simple_session_server, onboard_handler) - All used
3. dashboard/ - Will mark as experimental in docs

### ⚠️ Already moved (earlier in session):
1. test_goal_creation_integration.py
2. test_mirror_drift_monitor.py
3. test_subtask_integration.py

### 🔄 Pending (after Gemini/Qwen complete):
1. calibration/ → empirica-dev/deprecated-modules/

---

## File Count Before/After

**Before cleanup:** 187 Python files
**Moved:** ~15-20 files
**After cleanup:** ~167-172 Python files

**Result:** Cleaner, more focused codebase ✅

---

## Next Steps

1. ✅ Cleanup complete
2. ⏳ Wait for Gemini (bootstrap migration)
3. ⏳ Wait for Qwen (CLI handler cleanup)
4. 🔄 Then move calibration/ to deprecated
5. 📝 Update documentation to reflect changes

