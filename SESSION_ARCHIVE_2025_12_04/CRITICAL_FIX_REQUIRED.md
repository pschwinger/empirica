# 🚨 CRITICAL: Storage Flow Violation Found

## Executive Summary

**URGENT ISSUE DISCOVERED:** The main workflow commands (preflight-submit, check-submit, postflight-submit) **bypass the documented storage architecture**.

This breaks:
- ❌ Cross-AI coordination (no git notes)
- ❌ Handoff reports (can't read epistemic data)
- ❌ Checkpoint loading (git notes missing)
- ❌ Crypto signing (nothing to sign)
- ❌ Token efficiency (no compression)

## The Problem

### Documented Architecture:
```
EPISTEMIC EVENT → GitEnhancedReflexLogger.add_checkpoint()
    ↓
    ├─→ SQLite (queryable)
    ├─→ Git Notes (distributed)
    └─→ JSON (audit trail)
```

### Actual Implementation:
```
preflight-submit → SessionDatabase.log_preflight_assessment() → SQLite ONLY ❌
check-submit → SessionDatabase.log_check_phase_assessment() → SQLite ONLY ❌
postflight-submit → SessionDatabase.log_postflight_assessment() → SQLite ONLY ❌
```

**Result:** Git notes and JSON logs NEVER created by normal workflow!

## Impact Analysis

### What Works:
- ✅ `checkpoint-create` (uses correct flow)
- ✅ SQLite queries (data is there)
- ✅ sessions-list (SQLite only)

### What's Broken:
- ❌ `checkpoint-load` (reads from empty git notes)
- ❌ `handoff-create` (reads from empty git notes)
- ❌ `goals-discover` (reads from empty git notes)
- ❌ Cross-AI features (no git notes to share)
- ❌ Crypto signing (no git SHA to sign)

## The Fix (1-2 hours)

**File:** `empirica/cli/command_handlers/workflow_commands.py`

**Change all 3 functions to use GitEnhancedReflexLogger:**

```python
# REPLACE THIS (3 places):
from empirica.data.session_database import SessionDatabase
db = SessionDatabase()
assessment_id = db.log_preflight_assessment(...)

# WITH THIS:
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
logger = GitEnhancedReflexLogger(session_id=session_id)
checkpoint_id = logger.add_checkpoint(
    phase="PREFLIGHT",  # or CHECK, POSTFLIGHT
    round_num=1,
    vectors=vectors,
    metadata={"reasoning": reasoning, ...}
)
```

**Functions to fix:**
1. `handle_preflight_submit_command` (line 19)
2. `handle_check_submit_command` (line 153)
3. `handle_postflight_submit_command` (line 391)

## Testing

After fix, verify:
```bash
# 1. Run workflow
empirica bootstrap --ai-id test
empirica preflight-submit --session-id abc --vectors {...}

# 2. Check SQLite
empirica sessions-show --session-id abc
# Should show data ✅

# 3. Check git notes
git notes list refs/notes/empirica/session/abc/PREFLIGHT/1
# Should exist ✅

# 4. Check JSON logs
ls .empirica_reflex_logs/*/test/abc/
# Should have files ✅

# 5. Load checkpoint
empirica checkpoint-load --session-id abc
# Should work ✅
```

## Priority

**CRITICAL - Do this FIRST** before any parameter simplification.

All other issues (parameter bloat, --output json, etc.) are lower priority than this.

---

**Status:** Ready for immediate fix
**Assignee:** Other Claude (AI Agent 1)
**Estimated time:** 1-2 hours
**Risk:** LOW (GitEnhancedReflexLogger is tested)
