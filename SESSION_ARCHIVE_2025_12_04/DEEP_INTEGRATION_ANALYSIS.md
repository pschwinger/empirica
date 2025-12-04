# Deep Integration Analysis - Storage Flow Compliance

## Documented Flow (from STORAGE_ARCHITECTURE_COMPLETE.md)

```
EPISTEMIC EVENT (PREFLIGHT/CHECK/ACT/POSTFLIGHT)
    ↓
GitEnhancedReflexLogger.add_checkpoint(phase, round, vectors, metadata)
    ↓
    ├─→ SQLite (reflexes table) - queryable, structured
    ├─→ Git Notes (compressed ~450 tokens) - distributed, signable
    └─→ JSON Files (full ~6500 tokens) - audit trail
```

**Key Principle:** ALL epistemic events MUST flow through GitEnhancedReflexLogger

## Investigation: Do Commands Follow the Flow?

Let me trace each command type...

## 🚨 CRITICAL FINDING #1: Storage Flow Violation

### Expected Flow (from docs):
```
EPISTEMIC EVENT → GitEnhancedReflexLogger.add_checkpoint() → [SQLite + Git Notes + JSON]
```

### Actual Flow (from code):
```
preflight-submit → SessionDatabase.log_preflight_assessment() → SQLite ONLY ❌
check-submit → SessionDatabase.log_check_phase_assessment() → SQLite ONLY ❌
postflight-submit → SessionDatabase.log_postflight_assessment() → SQLite ONLY ❌
```

### Problem:
**workflow_commands.py BYPASSES GitEnhancedReflexLogger completely!**

- preflight/check/postflight commands write directly to SQLite
- No Git Notes created (breaking distributed/cross-AI features)
- No JSON audit logs created (breaking debugging trail)
- No compression happening (full vectors stored, not 450-token compressed)

### Impact:
- ❌ Checkpoints cannot be loaded (git notes missing)
- ❌ Cross-AI discovery broken (no git notes to share)
- ❌ Handoffs broken (no git notes to read)
- ❌ Crypto signing broken (nothing to sign - no git note SHA)
- ❌ Token efficiency lost (not using compression)

### Root Cause:
`workflow_commands.py` uses OLD API:
```python
db.log_preflight_assessment()  # OLD - SQLite only
db.log_check_phase_assessment()  # OLD - SQLite only
db.log_postflight_assessment()  # OLD - SQLite only
```

Should use NEW API:
```python
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
logger = GitEnhancedReflexLogger(session_id=session_id)
logger.add_checkpoint(phase="PREFLIGHT", vectors=vectors, metadata=...)
```

---

## 🚨 CRITICAL FINDING #2: Checkpoint Commands Follow Correct Flow

### checkpoint-create DOES use GitEnhancedReflexLogger:
```python
# empirica/cli/command_handlers/checkpoint_commands.py line 101
git_logger = GitEnhancedReflexLogger(session_id=session_id)
checkpoint_id = git_logger.add_checkpoint(
    phase=phase,
    round=round,
    vectors=vectors,
    metadata=metadata
)
```

### Result:
- ✅ checkpoint-create works correctly (3-layer storage)
- ❌ preflight/check/postflight broken (SQLite only)

**Inconsistency:** Two different storage paths in the same codebase!

---


## Investigation: What does store_vectors() do?

Looking at session_database.py line 1499-1547:

```python
def store_vectors(self, session_id, phase, vectors, cascade_id, round_num):
    # Writes to SQLite reflexes table ONLY
    # Does NOT call GitEnhancedReflexLogger
    # Does NOT create git notes
    # Does NOT create JSON audit logs
```

**Conclusion:** `store_vectors()` is a LOW-LEVEL SQLite-only function.

---

## 🚨 CRITICAL FINDING #3: Two Competing APIs

### API 1: OLD (SQLite-only) ❌
```python
# Used by: workflow_commands.py
SessionDatabase.log_preflight_assessment()
SessionDatabase.log_check_phase_assessment()
SessionDatabase.log_postflight_assessment()
SessionDatabase.store_vectors()
```
**Result:** Only writes to SQLite, no git notes, no JSON logs

### API 2: NEW (3-layer storage) ✅
```python
# Used by: checkpoint_commands.py
GitEnhancedReflexLogger.add_checkpoint()
```
**Result:** Writes to all 3 layers (SQLite + Git Notes + JSON)

### Why Two APIs Exist?
Likely evolution:
1. Started with SQLite-only (old API)
2. Added GitEnhancedReflexLogger for proper flow (new API)
3. **Forgot to migrate workflow_commands.py** ❌

---

## 🚨 CRITICAL FINDING #4: What Breaks?

### Broken User Flow:
```bash
# User runs normal workflow
empirica bootstrap --ai-id test
empirica preflight --session-id abc --prompt "task"
empirica preflight-submit --session-id abc --vectors {...}
  ↓ writes to SQLite ONLY
  
empirica checkpoint-load --session-id abc
  ↓ tries to read from git notes
  ↓ ERROR: No git notes found! ❌
```

### Why checkpoint-load fails:
- `preflight-submit` wrote to SQLite only
- `checkpoint-load` reads from git notes
- Git notes don't exist → failure

### Why handoff-create fails:
```bash
empirica handoff-create --session-id abc
  ↓ reads from git notes for epistemic data
  ↓ ERROR: No checkpoints in git notes! ❌
```

### Why cross-AI discovery fails:
```bash
empirica goals-discover --from-ai-id other-ai
  ↓ reads git notes from .git/notes/empirica/
  ↓ ERROR: No epistemic checkpoints found! ❌
```

---

## 🚨 CRITICAL FINDING #5: Data Duplication

### What happens if you manually create checkpoint?
```bash
empirica preflight-submit --session-id abc --vectors {...}
  ↓ SQLite: reflexes table row created
  
empirica checkpoint-create --session-id abc --phase PREFLIGHT --round 1
  ↓ SQLite: ANOTHER reflexes table row created
  ↓ Git Notes: checkpoint created
  ↓ JSON: audit log created
```

**Result:** DUPLICATE data in SQLite! ❌

### Current State:
- `reflexes` table has data from BOTH paths
- Git notes only has data from checkpoint-create
- JSON logs only has data from checkpoint-create

**Inconsistency:** SQLite has more data than git notes!

---

## Summary of Integration Issues

### 🔴 CRITICAL Issues:

1. **Workflow commands bypass storage architecture** (preflight/check/postflight)
   - Only write to SQLite
   - Break cross-AI features (no git notes)
   - Break audit trail (no JSON logs)
   - Break crypto signing (no git SHA)

2. **Two competing APIs coexist** (old vs new)
   - workflow_commands.py uses old API
   - checkpoint_commands.py uses new API
   - Inconsistent behavior across commands

3. **Data duplication possible**
   - Can write same checkpoint via both paths
   - SQLite gets duplicate rows
   - Git notes incomplete

4. **User workflows broken**
   - checkpoint-load fails (no git notes)
   - handoff-create fails (no git notes)
   - goals-discover fails (no git notes)

### 🟡 MEDIUM Issues:

5. **Parameter bloat** (as documented earlier)
   - Too many flags
   - Inconsistent naming
   - MCP-CLI mismatches

6. **Missing --output json** (as documented earlier)
   - 3 commands missing flag
   - Inconsistent interface

---

## Recommended Fixes (Priority Order)

### Priority 1: FIX STORAGE FLOW VIOLATION ⚡⚡⚡ URGENT
**Impact:** Breaks core features (cross-AI, handoffs, signing)

**Fix:** Migrate workflow_commands.py to use GitEnhancedReflexLogger

**Files to change:**
- `empirica/cli/command_handlers/workflow_commands.py`

**Changes needed:**
```python
# BEFORE (line 34-49):
db = SessionDatabase()
assessment_id = db.log_preflight_assessment(
    session_id=session_id,
    cascade_id=cascade_id,
    prompt_summary=prompt_summary,
    vectors=vectors,
    uncertainty_notes=uncertainty_notes
)

# AFTER:
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
logger = GitEnhancedReflexLogger(session_id=session_id)
checkpoint_id = logger.add_checkpoint(
    phase="PREFLIGHT",
    round_num=1,
    vectors=vectors,
    metadata={"reasoning": reasoning, "prompt": prompt_summary}
)
```

Apply same fix to:
- handle_preflight_submit_command (line 19-87)
- handle_check_submit_command (line 153-299)
- handle_postflight_submit_command (line 391-527)

**Estimated time:** 1-2 hours
**Risk:** LOW (new API is well-tested)
**Test:** Run full workflow, verify git notes + SQLite + JSON all populated

---

### Priority 2: DEPRECATE OLD API 🔧
**Impact:** Prevents future confusion

**Fix:** Mark old API as deprecated

**Files to change:**
- `empirica/data/session_database.py`

**Changes:**
```python
def log_preflight_assessment(self, ...):
    """
    DEPRECATED: Use GitEnhancedReflexLogger.add_checkpoint() instead.
    
    This method only writes to SQLite and bypasses git notes and JSON logs.
    Kept for backwards compatibility only.
    """
    import warnings
    warnings.warn(
        "log_preflight_assessment is deprecated. Use GitEnhancedReflexLogger.add_checkpoint()",
        DeprecationWarning,
        stacklevel=2
    )
    # ... existing implementation
```

**Estimated time:** 30 min
**Risk:** NONE (just warnings)

---

### Priority 3: ADD INTEGRATION TEST 🧪
**Impact:** Prevents regression

**Fix:** Add test to verify storage flow compliance

**Files to create:**
- `tests/integration/test_storage_flow_compliance.py`

**Test:**
```python
def test_preflight_creates_all_three_storages():
    """Verify preflight-submit writes to SQLite + Git Notes + JSON"""
    session_id = bootstrap_test_session()
    
    run_cli(f"empirica preflight-submit --session-id {session_id} --vectors '{...}'")
    
    # Check SQLite
    db = SessionDatabase()
    assert db.get_latest_vectors(session_id, "PREFLIGHT") is not None
    
    # Check Git Notes
    logger = GitEnhancedReflexLogger(session_id=session_id)
    checkpoint = logger.get_last_checkpoint()
    assert checkpoint is not None
    assert checkpoint['phase'] == 'PREFLIGHT'
    
    # Check JSON logs exist
    log_path = f".empirica_reflex_logs/{date}/{ai_id}/{session_id}/"
    assert os.path.exists(log_path)
    assert len(os.listdir(log_path)) > 0
```

**Estimated time:** 1 hour
**Risk:** NONE

---

