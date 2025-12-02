# HANDOFF: Bootstrap Migration - Remove Heuristics

**For:** Gemini  
**Task:** Migrate bootstrap files to remove deprecated heuristic-based code  
**Priority:** HIGH - Blocks "no heuristics" claim  
**Estimated Time:** 1-2 hours

---

## Your Mission

Remove deprecated `empirica.calibration` imports from 2 bootstrap files and ensure they work with the new MirrorDriftMonitor system.

---

## Context

**What we fixed:** CASCADE core now uses MirrorDriftMonitor (no heuristics) instead of old DriftMonitor (had behavioral heuristics like sycophancy detection).

**Your job:** Update bootstrap files to remove deprecated imports.

---

## Files to Update (2 total)

### 1. empirica/bootstraps/optimal_metacognitive_bootstrap.py
**Current imports (deprecated):**
- `from empirica.calibration.adaptive_uncertainty_calibration import AdaptiveUncertaintyCalibration`

**Actions:**
1. Remove the import
2. Search for any usage of `AdaptiveUncertaintyCalibration` in the file
3. If used: Comment out that functionality (it's experimental anyway)
4. If just imported but unused: Simply remove import line

### 2. empirica/bootstraps/extended_metacognitive_bootstrap.py
**Current imports (deprecated):**
- `from empirica.calibration.adaptive_uncertainty_calibration.bayesian_belief_tracker import BayesianBeliefTracker`
- `from empirica.calibration.parallel_reasoning import ParallelReasoningSystem, DriftMonitor`

**Actions:**
1. Remove all three imports
2. Search for usage of `BayesianBeliefTracker`, `ParallelReasoningSystem`, `DriftMonitor`
3. Comment out or remove any code using these (they're experimental features)
4. The bootstrap should work without these - they were optional additions

---

## Step-by-Step Instructions

### Step 1: Open optimal_metacognitive_bootstrap.py
```bash
# Find the import
grep -n "from empirica.calibration" empirica/bootstraps/optimal_metacognitive_bootstrap.py
```

### Step 2: Remove the import
Use find_and_replace to remove:
```python
from empirica.calibration.adaptive_uncertainty_calibration import AdaptiveUncertaintyCalibration
```

### Step 3: Check if it's actually used
```bash
grep -n "AdaptiveUncertaintyCalibration" empirica/bootstraps/optimal_metacognitive_bootstrap.py
```

If found, comment out or remove that code section.

### Step 4: Test it works
```bash
python3 -c "
from empirica.bootstraps import optimal_metacognitive_bootstrap
print('✅ Import successful')
"
```

### Step 5: Repeat for extended_metacognitive_bootstrap.py

Remove these three imports and any usage.

---

## Testing

### Test 1: Import Works
```bash
python3 -c "
from empirica.bootstraps import optimal_metacognitive_bootstrap
from empirica.bootstraps import extended_metacognitive_bootstrap
print('✅ Both bootstrap imports successful')
"
```

### Test 2: No calibration imports
```bash
python3 -c "
import sys
# Remove any existing calibration imports
for mod in list(sys.modules.keys()):
    if 'calibration' in mod:
        del sys.modules[mod]

# Import bootstraps - should not trigger calibration imports
from empirica.bootstraps import optimal_metacognitive_bootstrap
from empirica.bootstraps import extended_metacognitive_bootstrap

# Verify
assert not any('calibration' in mod for mod in sys.modules.keys()), 'calibration module was imported!'
print('✅ No deprecated calibration imports detected')
"
```

### Test 3: Run existing tests
```bash
pytest tests/unit/test_bootstrap_direct.py -v
```

All tests should pass.

---

## Success Criteria

- [ ] No imports from `empirica.calibration` in either file
- [ ] Both files import successfully
- [ ] Test script confirms no calibration imports
- [ ] Existing bootstrap tests pass
- [ ] Manual test: `empirica bootstrap --ai-id test` works

---

## If You Get Stuck

**Problem:** Code actually uses the deprecated classes  
**Solution:** Comment out that section with:
```python
# DEPRECATED: This feature used heuristic-based calibration
# Removed as part of migration to no-heuristics architecture
# See: MirrorDriftMonitor for new drift detection
# if False:  # Disabled deprecated feature
#     [old code here]
```

**Problem:** Tests fail  
**Solution:** Check error message. If it's about missing calibration imports, that's expected. Update the test to not expect those features.

---

## Questions?

If uncertain, ask user for clarification. These are experimental features so it's safe to remove them.

---

## Report Back

When done, report:
1. What you removed
2. What tests passed
3. Any issues encountered

**Format:**
```
✅ BOOTSTRAP MIGRATION COMPLETE

Files updated:
- optimal_metacognitive_bootstrap.py: Removed AdaptiveUncertaintyCalibration import
- extended_metacognitive_bootstrap.py: Removed 3 deprecated imports

Tests:
- Import test: ✅ PASS
- No calibration test: ✅ PASS
- Existing tests: ✅ PASS (or list failures)

Manual verification:
- Bootstrap command: ✅ WORKS

Ready for next task: YES
```
