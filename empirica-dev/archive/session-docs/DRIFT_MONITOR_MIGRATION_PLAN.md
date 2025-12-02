# Drift Monitor Migration Plan - Remove Heuristics

**Goal:** Migrate from deprecated DriftMonitor (has heuristics) to MirrorDriftMonitor (no heuristics)

---

## Migration Strategy

### Phase 1: Understand MirrorDriftMonitor API (5 min)
- Check MirrorDriftMonitor interface
- Understand what it needs (checkpoint history)
- Compare to old DriftMonitor API

### Phase 2: Update Core CASCADE (15 min) - CRITICAL
1. Replace import in metacognitive_cascade.py
2. Update instantiation
3. Update usage pattern
4. Test that it works

### Phase 3: Update Bootstrap Files (10 min)
1. optimal_metacognitive_bootstrap.py
2. extended_metacognitive_bootstrap.py
3. Remove AdaptiveUncertaintyCalibration references

### Phase 4: Update CLI Handlers (10 min)
1. Remove AdaptiveUncertaintyCalibration imports (6 files)
2. These may not even use it - just imported

### Phase 5: Test & Verify (10 min)
1. Run drift detection tests
2. Verify no regressions
3. Update any failing tests

**Total time:** ~50 minutes

---

## Files to Update (12 total)

### CRITICAL (Core System):
1. ✅ empirica/core/metacognitive_cascade/metacognitive_cascade.py
2. ✅ empirica/bootstraps/optimal_metacognitive_bootstrap.py
3. ✅ empirica/bootstraps/extended_metacognitive_bootstrap.py

### MEDIUM (CLI - may just be unused imports):
4. ✅ empirica/cli/command_handlers/cascade_commands.py
5. ✅ empirica/cli/command_handlers/assessment_commands.py
6. ✅ empirica/cli/command_handlers/bootstrap_commands.py
7. ✅ empirica/cli/command_handlers/utility_commands.py (2 places)
8. ✅ empirica/cli/command_handlers/modality_commands.py

### LOW (Comments only):
9. ✅ empirica/data/session_json_handler.py (just comment reference)

---

## Execution Order

1. Check MirrorDriftMonitor API first
2. Start with CASCADE (most critical)
3. Then bootstraps
4. Then CLI handlers (may be simple)
5. Test everything
6. Remove deprecated calibration/ if nothing else uses it

---

**Status:** Ready to execute
**Estimated time:** 50 minutes
**Risk:** Low - MirrorDriftMonitor already exists and is designed for this
