# Empirica E2E Testing - Issues Found
**Date:** 2025-12-04  
**Tester:** Claude (fixing own code)

## Critical Issues

### Issue 1: sessions-list ignores --output json flag
**Severity:** HIGH  
**Location:** `empirica/cli/command_handlers/session_commands.py`  
**Problem:** Handler always calls `print_header()` before checking output format  
**Expected:** Should check `args.output == 'json'` first and skip pretty printing  
**Fix:** Move output format check to top of function

### Issue 2: Bootstrap doesn't create session
**Severity:** HIGH  
**Location:** `empirica/cli/command_handlers/bootstrap_commands.py`  
**Problem:** `empirica bootstrap` only loads components, doesn't create session in SQLite  
**Expected:** Should create session record for tracking  
**Question:** Is this intentional? MCP bootstrap_session does create session  
**Fix Options:**  
  A. Make CLI bootstrap create session (match MCP behavior)  
  B. Document that bootstrap is just component loading (clarify docs)

### Issue 3: SessionDatabase.create_session() API mismatch
**Severity:** HIGH  
**Location:** `empirica/data/session_database.py`  
**Problem:** Signature requires `bootstrap_level` and `components_loaded` but MCP doesn't pass these  
**Current signature:** `create_session(ai_id, bootstrap_level, components_loaded, user_id=None)`  
**MCP expects:** `create_session(session_id, ai_id, user_id)`  
**Fix:** Need to align signatures or make params optional

### Issue 4: sessions-list has timestamp parsing bug (ALREADY FIXED)
**Status:** ✅ FIXED  
**Evidence:** Previous session fixed this with `format_timestamp()` function  
**Verify:** Needs testing with actual data

## Medium Issues

### Issue 5: Bootstrap doesn't support --output json
**Severity:** MEDIUM  
**Location:** `empirica/cli/cli_core.py` - bootstrap parser  
**Problem:** Parser doesn't accept --output flag  
**Fix:** Add `--output` argument to bootstrap parser

### Issue 6: assess command still exists (deprecated)
**Severity:** MEDIUM - Bloat  
**Location:** CLI parsers + handlers  
**Problem:** Deprecated heuristics-based command still registered  
**Fix:** Remove entirely from CLI (as discussed)

### Issue 7: calibration CLI command still exists (deprecated)
**Severity:** MEDIUM - Bloat  
**Location:** CLI parsers + handlers  
**Problem:** Deprecated, but CLI command still exists  
**Note:** MCP tool correctly uses SQLite now (fixed in this session)  
**Fix:** Remove CLI command or update to query SQLite

## API Design Questions

### Question 1: Bootstrap vs Session Creation
Should `empirica bootstrap` create a session or just load components?  
- **Current:** Just loads components (returns component list)  
- **MCP:** Creates session + loads components  
- **Recommendation:** ?

### Question 2: SessionDatabase API
What's the minimal session creation API?  
- **Option A:** `create_session(ai_id)` returns session_id (simple)  
- **Option B:** `create_session(ai_id, bootstrap_level, components_loaded)` (detailed)  
- **Option C:** Keep both - add session_id param for explicit ID  
- **Recommendation:** ?

## Test Coverage Gaps

1. ❌ No integration test for full CASCADE workflow  
2. ❌ No test for MCP → CLI parameter mapping  
3. ❌ No test for SQLite → Git Notes sync  
4. ⚠️  Handoff report generation not tested end-to-end

## Summary

**High Priority (Must Fix):**
1. sessions-list JSON output
2. SessionDatabase API alignment
3. Bootstrap session creation clarity

**Medium Priority (Should Fix):**
4. Remove deprecated commands (assess, old calibration)
5. Add --output json to bootstrap
6. Document bootstrap vs session creation

**Tests Needed:**
7. Full CASCADE workflow integration test
8. MCP-CLI parity test suite

