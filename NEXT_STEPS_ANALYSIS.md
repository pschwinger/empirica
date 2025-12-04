# Next Steps Analysis - Testing & Simplification

## Current Status:

✅ Integration tests: DONE (7 tests)
✅ Storage flow: VALIDATED
✅ 6,136 lines removed
⏳ Unit tests: Need updating (25 files reference removed code)
⏳ Command simplification: Partially done
⏳ Documentation: 10 files need updates

---

## 1. Unit Test Status

### Tests Needing Updates: 25 files
**Why:** Reference removed code (ReflexLogger, metacognition_12d_monitor, calibration, auto_tracker)

**Files:** 
- tests/test_bootstrap_direct.py
- tests/unit/canonical/test_*.py
- tests/unit/cascade/test_*.py
- tests/integration/test_*.py

**Impact:** Tests may fail or have unused imports

**Fix Time:** ~30-60 minutes
- Remove ReflexLogger → Use GitEnhancedReflexLogger
- Remove metacognition_12d_monitor references
- Remove calibration/auto_tracker imports
- Update bootstrap test expectations

**Priority:** MEDIUM (tests exist but need cleanup)

---

## 2. MCP Tool Testing

### Current Coverage:
- ✅ test_storage_flow_compliance.py (7 tests) - integration
- ✅ test_mcp_tools.py - basic MCP tests
- ✅ test_mcp_arg_map.py - parameter mapping
- ⚠️ Individual tool coverage - sparse

### Missing Coverage:
- Individual MCP tool validation
- All 30+ MCP tools exercised
- Edge cases and error handling

**Recommendation:** 
NOT CRITICAL - Integration tests validate the flow.
Unit tests for individual tools are nice-to-have but not blocking.

**If we do it:**
- Create test_mcp_tools_comprehensive.py
- Test each tool with valid/invalid inputs
- Time: 1-2 hours

---

## 3. CLI Command Testing

### Current Coverage:
- ✅ test_all_cli_commands.py - smoke tests
- ✅ test_workflow_commands_delta_fix.py - specific fix validation
- ⚠️ Individual command coverage - sparse

### Missing Coverage:
- All 40+ CLI commands with all flags
- Flag combination testing
- Error handling

**Recommendation:**
NOT CRITICAL - Commands work, just not exhaustively tested.

**If we do it:**
- Expand test_all_cli_commands.py
- Test each command with --help and basic usage
- Time: 1-2 hours

---

## 4. Command Simplification Status

### Already Simplified:
✅ MCP arg_map (parameter names unified)
✅ Bootstrap (1,216 → 130 lines)
✅ Removed deprecated commands (assess heuristics)

### Still Complex (From Earlier Analysis):

#### A. Goal Commands - Parameter Bloat
**Current:**
```bash
empirica goals-create \
  --session-id X \
  --objective "..." \
  --scope-breadth 0.7 \
  --scope-duration 0.5 \
  --scope-coordination 0.3 \
  --success-criteria '["a","b"]' \
  --estimated-complexity 0.8
```

**Could be:**
```bash
empirica goals-create \
  --session-id X \
  --objective "..." \
  --spec '{"scope":{"breadth":0.7,"duration":0.5,"coordination":0.3},"complexity":0.8,"success":["a","b"]}'
```

**Impact:** Less typing, cleaner API
**Time:** 1-2 hours
**Priority:** MEDIUM (works fine as-is, but could be cleaner)

#### B. Checkpoint Commands - Auto-infer Parameters
**Current:**
```bash
empirica checkpoint-create \
  --session-id abc \
  --phase ACT \
  --round 3 \
  --metadata '{...}'
```

**Could be:**
```bash
empirica checkpoint-create --session-id abc
# Auto-infers phase/round from session state
```

**Impact:** Less ceremony, smarter defaults
**Time:** 1-2 hours
**Priority:** MEDIUM (convenience, not critical)

#### C. Missing --output json (3 commands)
**Commands:**
- profile-list
- checkpoint-list  
- assess

**Impact:** Inconsistent CLI interface
**Time:** 30 minutes
**Priority:** LOW (not heavily used commands)

---

## Recommendations by Priority:

### HIGH Priority (Do Now):
1. ✅ **Update 10 production docs** (~30 min)
   - Remove references to deleted code
   - Update API signatures
   - Clarify 13-vector standard

### MEDIUM Priority (Do Soon):
2. ⏳ **Update unit tests** (~30-60 min)
   - Fix 25 tests referencing removed code
   - Remove unused imports
   - Update expectations

3. ⏳ **Add --output json to 3 commands** (~30 min)
   - Consistency improvement
   - Easy win

### LOW Priority (Nice to Have):
4. ⏸️ **Parameter consolidation** (~2 hours)
   - Scope flags → JSON
   - Auto-infer phase/round
   - Cleaner but not critical

5. ⏸️ **Comprehensive MCP/CLI testing** (~2-4 hours)
   - Individual tool tests
   - All flag combinations
   - Edge cases

---

## My Recommendations:

### Option A: Finish Strong (1 hour)
1. ✅ Update 10 production docs (30 min)
2. ✅ Update 25 unit tests (30 min)
3. ✅ Add --output json to 3 commands (15 min)

**Result:** Complete, production-ready, well-documented

### Option B: Core Only (30 min)
1. ✅ Update 10 production docs only

**Result:** Documentation accurate, tests can wait

### Option C: Keep Going (3 hours)
1. ✅ Update docs (30 min)
2. ✅ Update tests (30 min)
3. ✅ Add --output json (15 min)
4. ✅ Parameter consolidation (1-2 hours)

**Result:** Ultimate simplification achieved

---

## Your Call:

**What's your priority?**
A. Finish documentation (docs are customer-facing)
B. Fix unit tests (internal code quality)
C. Simplify commands further (convenience)
D. We've done enough - ship it!

**My vote:** Option A (finish strong) - 1 hour to complete everything critical.

