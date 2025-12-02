# Migration Tests & Handoff Plan

**Status:** CASCADE core migration COMPLETE and TESTED ✅

---

## Test Results: CASCADE Core

### ✅ All Tests Passing (12/12)

**PREFLIGHT Tests:** 6/6 passed
- test_preflight_phase_initialization
- test_preflight_assessment_generation
- test_preflight_assessment_specifics
- test_preflight_delta_calculation
- test_preflight_calibration_check
- test_preflight_guidance_generation

**Drift Integration Tests:** 6/6 passed
- test_no_drift_stable_assessment
- test_moderate_drift_warning
- test_severe_drift_blocks_act
- test_drift_detection_response_structure
- test_insufficient_history_graceful_handling
- test_drift_detection_error_handling

**Manual Verification:** ✅ MirrorDriftMonitor loads and initializes correctly

---

## Remaining Migration Work (11 files)

### HIGH PRIORITY: Bootstrap Files (2 files)

**Files:**
1. `empirica/bootstraps/optimal_metacognitive_bootstrap.py`
2. `empirica/bootstraps/extended_metacognitive_bootstrap.py`

**Issue:** Import deprecated `AdaptiveUncertaintyCalibration`, `BayesianBeliefTracker`, `ParallelReasoningSystem`

**Action Required:**
- Remove deprecated imports
- Update any initialization code
- Test bootstrap works without deprecated modules

**Test Plan:**
```python
# Test: Bootstrap without deprecated modules
from empirica.bootstraps import optimal_metacognitive_bootstrap

session = optimal_metacognitive_bootstrap.bootstrap(
    ai_id="test-ai",
    session_id="test-session"
)
# Should succeed without importing calibration/
```

**For Gemini/Qwen:**
- Remove imports from `empirica.calibration`
- If functionality needed, use MirrorDriftMonitor instead
- Run: `pytest tests/unit/test_bootstrap_direct.py -v`

---

### MEDIUM PRIORITY: CLI Handler Cleanup (6 files)

**Files:**
1. `empirica/cli/command_handlers/cascade_commands.py`
2. `empirica/cli/command_handlers/assessment_commands.py`
3. `empirica/cli/command_handlers/bootstrap_commands.py`
4. `empirica/cli/command_handlers/utility_commands.py` (2 places)
5. `empirica/cli/command_handlers/modality_commands.py`

**Issue:** Import `AdaptiveUncertaintyCalibration` but may not actually use it

**Action Required:**
- Check if imports are actually used
- Remove if unused (likely just dead imports)
- If used, replace with MirrorDriftMonitor or remove feature

**Test Plan:**
```bash
# For each handler, verify commands still work:
empirica preflight "test task"
empirica check <session-id>
empirica postflight <session-id>
```

**For Gemini/Qwen:**
- Search for actual usage of AdaptiveUncertaintyCalibration in each file
- If used: Replace with MirrorDriftMonitor or comment out
- If unused: Simply remove import
- Run: `pytest tests/mcp/ -v` to verify MCP tools still work

---

### LOW PRIORITY: Comment Reference (1 file)

**File:** `empirica/data/session_json_handler.py`

**Issue:** Comment mentions DriftMonitor

**Action:** Update comment to reference MirrorDriftMonitor

---

### DEPRECATION: Old calibration/ Module (3 files)

**Files:**
1. `empirica/calibration/parallel_reasoning.py`
2. `empirica/calibration/adaptive_uncertainty_calibration/`
3. Any other calibration/ files

**Action:** Mark as deprecated, move to empirica-dev after migration complete

---

## Test Specifications for Handoff

### Unit Tests Needed

**Test 1: Bootstrap without Heuristics**
```python
# tests/unit/test_bootstrap_no_heuristics.py
def test_optimal_bootstrap_no_deprecated_imports():
    """Verify optimal bootstrap doesn't import deprecated modules"""
    import sys
    # Remove calibration from sys.modules if present
    for mod in list(sys.modules.keys()):
        if 'calibration' in mod:
            del sys.modules[mod]
    
    # This should not trigger calibration imports
    from empirica.bootstraps import optimal_metacognitive_bootstrap
    
    # Verify no calibration modules loaded
    assert not any('calibration' in mod for mod in sys.modules.keys())

def test_extended_bootstrap_no_deprecated_imports():
    """Verify extended bootstrap doesn't import deprecated modules"""
    # Similar test for extended bootstrap
```

**Test 2: CLI Handlers Work Without Deprecated Code**
```python
# tests/unit/cli/test_handlers_no_heuristics.py
def test_cascade_commands_no_calibration():
    """Verify cascade commands work without calibration imports"""
    from empirica.cli.command_handlers import cascade_commands
    # Should not raise ImportError
    assert hasattr(cascade_commands, 'handle_preflight')

def test_assessment_commands_no_calibration():
    """Verify assessment commands work without calibration imports"""
    from empirica.cli.command_handlers import assessment_commands
    assert hasattr(assessment_commands, 'handle_submit_preflight_assessment')
```

### Integration Tests Needed

**Test 3: Full CASCADE Without Deprecated Modules**
```python
# tests/integration/test_cascade_no_heuristics.py
def test_full_cascade_workflow_no_heuristics():
    """Verify complete CASCADE workflow uses only MirrorDriftMonitor"""
    cascade = CanonicalEpistemicCascade(
        session_id="test-full-workflow",
        enable_drift_monitor=True
    )
    
    # PREFLIGHT
    preflight_result = cascade.execute_preflight("test task")
    assert preflight_result['success']
    
    # CHECK
    check_result = cascade.execute_check()
    assert check_result['success']
    
    # Verify drift monitor is MirrorDriftMonitor
    assert type(cascade.drift_monitor).__name__ == 'MirrorDriftMonitor'
    
    # POSTFLIGHT
    postflight_result = cascade.execute_postflight("completed")
    assert postflight_result['success']
```

### Security/Integrity Tests

**Test 4: No Heuristic Code Paths**
```python
# tests/integrity/test_no_heuristics_verify.py
def test_no_sycophancy_detection():
    """Verify no sycophancy detection code is executed"""
    import logging
    
    # Capture all log messages
    with LogCapture() as logs:
        cascade = CanonicalEpistemicCascade(
            session_id="test-no-sycophancy",
            enable_drift_monitor=True
        )
        cascade.execute_check()
    
    # Verify no "sycophancy" or "tension" in logs
    log_text = str(logs)
    assert 'sycophancy' not in log_text.lower()
    assert 'tension avoidance' not in log_text.lower()

def test_only_temporal_comparison():
    """Verify drift detection uses only temporal comparison"""
    cascade = CanonicalEpistemicCascade(
        session_id="test-temporal-only",
        enable_drift_monitor=True
    )
    
    # Drift monitor should be MirrorDriftMonitor
    assert cascade.drift_monitor.__class__.__module__ == 'empirica.core.drift.mirror_drift_monitor'
```

---

## Handoff Instructions for Gemini/Qwen

### Task 1: Bootstrap Migration (Gemini)

**Objective:** Remove deprecated imports from bootstrap files

**Steps:**
1. Open `empirica/bootstraps/optimal_metacognitive_bootstrap.py`
2. Search for imports from `empirica.calibration`
3. Remove or replace with MirrorDriftMonitor
4. Test: `pytest tests/unit/test_bootstrap_direct.py -v`
5. Repeat for `extended_metacognitive_bootstrap.py`

**Success Criteria:**
- No imports from `empirica.calibration`
- All bootstrap tests pass
- Manual test: `empirica bootstrap --ai-id test` works

---

### Task 2: CLI Handler Cleanup (Qwen)

**Objective:** Remove unused deprecated imports from CLI handlers

**Steps:**
1. For each of 6 CLI handler files:
   - Search for `AdaptiveUncertaintyCalibration`
   - Check if actually used in code (not just imported)
   - If unused: Remove import
   - If used: Replace or comment out feature
2. Test: `pytest tests/mcp/ -v`
3. Test: `pytest tests/unit/cli/ -v`

**Success Criteria:**
- No imports from `empirica.calibration` 
- All MCP tests pass
- All CLI tests pass
- Manual verification: Core CLI commands work

---

### Task 3: Write New Tests (Both)

**Objective:** Create test suite verifying no heuristics

**Steps:**
1. Create `tests/integrity/test_no_heuristics_complete.py`
2. Implement 4 test functions from specifications above
3. Run: `pytest tests/integrity/test_no_heuristics_complete.py -v`
4. All should pass

**Success Criteria:**
- 4 new tests created
- All tests pass
- No heuristic code paths detected

---

## Final Verification Checklist

**Before marking complete:**
- [ ] All 12 files migrated (CASCADE + 11 remaining)
- [ ] All existing tests still pass
- [ ] 4 new integrity tests pass
- [ ] Bootstrap works without deprecated modules
- [ ] CLI commands work without deprecated modules
- [ ] Manual smoke test: Full CASCADE workflow
- [ ] No "sycophancy" or "tension avoidance" in logs
- [ ] Documentation updated (mark calibration/ as deprecated)

---

## Deprecation Plan for calibration/

**After all 12 files migrated:**

1. Add deprecation warning to calibration/__init__.py
2. Move calibration/ to empirica-dev/deprecated-modules/
3. Update CHANGELOG.md
4. Update production docs to remove references
5. Update user docs to mention MirrorDriftMonitor only

---

**Status:** CASCADE core complete ✅  
**Remaining work:** 11 files, 4 new tests  
**Estimated time:** 2-3 hours (with Gemini + Qwen in parallel)  
**Ready for handoff:** Yes ✅
