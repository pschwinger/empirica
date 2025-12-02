# Bootstrap Cleanup Task - For Qwen

**Date:** 2025-12-01  
**Issue:** Bootstrap files reference 12 removed/moved components  
**Status:** Bootstrap works (MCP fallback) but has dead code  
**Priority:** Medium - Cleanup needed

---

## Current Situation

### Bootstrap Command Status
✅ **`empirica bootstrap` WORKS** (uses MCP server fallback)  
⚠️ **Local bootstrap has dead imports** (12 missing components)  
✅ **Loads 6 core components** (correct behavior)

### Test Results
```bash
$ empirica bootstrap --test
✅ Bootstrap complete!
   📊 Components loaded: 6
   ⏱️ Bootstrap time: 91μs
   🎯 Level: standard
   🎭 Profile: auto-selected
   ✅ Tests passed: 2/4
```

---

## Components Intentionally Removed (12 total)

These were moved/removed as **non-core** components:

### Missing Files (Should Be Removed from Bootstrap)

1. **`empirica.core.metacognition_12d_monitor.TwelveVectorMonitor`**
   - ❌ Old path: `empirica/core/metacognition_12d_monitor.py`
   - ✅ New path: `empirica/core/metacognition_12d_monitor/` (directory)
   - Action: Update import path

2. **`empirica.calibration.adaptive_uncertainty_calibration.AdaptiveUncertaintyCalibration`**
   - ❌ Entire module missing
   - Action: Remove from bootstrap

3. **`empirica.core.metacognitive_cascade.CanonicalEpistemicCascade`**
   - ❌ Old path: `empirica/core/metacognitive_cascade.py`
   - ✅ New path: `empirica/core/metacognitive_cascade/` (directory)
   - Action: Update import path

4. **`empirica.components.context_validation.ContextValidationComponent`**
   - ❌ File missing
   - Action: Remove from bootstrap

5. **`empirica.components.runtime_validation.RuntimeValidationComponent`**
   - ❌ File missing
   - Action: Remove from bootstrap

6. **`empirica.components.environment_stabilization.EnvironmentStabilizationComponent`**
   - ❌ File missing
   - Action: Remove from bootstrap

7. **`empirica.components.workspace_awareness.WorkspaceAwarenessComponent`**
   - ❌ File missing
   - Action: Remove from bootstrap

8. **`empirica.components.empirical_performance_analyzer.EmpiricalPerformanceAnalyzer`**
   - ❌ File missing
   - Action: Remove from bootstrap

9. **`empirica.components.intelligent_navigation.IntelligentNavigationComponent`**
   - ❌ File missing
   - Action: Remove from bootstrap

10. **`empirica.components.security_monitoring.SecurityMonitoringComponent`**
    - ❌ File missing
    - Action: Remove from bootstrap

11. **`empirica.components.procedural_analysis.ProceduralAnalysisComponent`**
    - ❌ File missing
    - Action: Remove from bootstrap

12. **`empirica.auto_tracker.EmpericaTracker`**
    - ⚠️ File exists but import fails
    - Action: Fix import or remove

---

## Files That Need Cleanup

### 1. `empirica/bootstraps/optimal_metacognitive_bootstrap.py`

**Lines to Fix:**

```python
# Line 46 - Fix or remove
from empirica.auto_tracker import EmpericaTracker  # IMPORT FAILS

# Line 178 - Update path (moved to directory)
from empirica.core.metacognition_12d_monitor import (  # ❌ OLD PATH
    TwelveVectorMonitor,
    VectorState,
    MetacognitionStatus
)
# Should be:
from empirica.core.metacognition_12d_monitor.metacognition_12d_monitor import (
    TwelveVectorMonitor,
    VectorState,
    MetacognitionStatus
)

# Line 194 - Remove (component deleted)
from empirica.calibration.adaptive_uncertainty_calibration import (  # ❌ MISSING
    AdaptiveUncertaintyCalibration,
    CalibrationMode,
    FeedbackOutcome
)

# Line 283 - Update path (moved to directory)
from empirica.core.metacognitive_cascade import CanonicalEpistemicCascade  # ❌ OLD PATH
# Should be:
from empirica.core.metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade
```

### 2. `empirica/bootstraps/extended_metacognitive_bootstrap.py`

**Lines to Fix:**

```python
# Line 105 - Fix or remove
from empirica.auto_tracker import EmpericaTracker  # IMPORT FAILS

# Lines 376-427 - Remove all (components deleted)
from empirica.components.context_validation import (  # ❌ MISSING
    ContextValidationComponent,
)
from empirica.components.runtime_validation import (  # ❌ MISSING
    RuntimeValidationComponent,
)
from empirica.components.environment_stabilization import (  # ❌ MISSING
    EnvironmentStabilizationComponent,
)
from empirica.components.workspace_awareness import (  # ❌ MISSING
    WorkspaceAwarenessComponent,
)

# Lines 551-603 - Remove all (components deleted)
from empirica.components.empirical_performance_analyzer import (  # ❌ MISSING
    EmpiricalPerformanceAnalyzer,
)
from empirica.components.intelligent_navigation import (  # ❌ MISSING
    IntelligentNavigationComponent,
)
from empirica.components.security_monitoring import (  # ❌ MISSING
    SecurityMonitoringComponent,
)
from empirica.components.procedural_analysis import (  # ❌ MISSING
    ProceduralAnalysisComponent,
)
```

---

## Recommended Cleanup Strategy

### Phase 1: Remove Dead Imports ✅

Remove all imports for deleted components:
- adaptive_uncertainty_calibration
- context_validation
- runtime_validation
- environment_stabilization
- workspace_awareness
- empirical_performance_analyzer
- intelligent_navigation
- security_monitoring
- procedural_analysis

### Phase 2: Fix Moved Component Paths ✅

Update import paths for components that moved to directories:
- `metacognition_12d_monitor` → `metacognition_12d_monitor.metacognition_12d_monitor`
- `metacognitive_cascade` → `metacognitive_cascade.metacognitive_cascade`

### Phase 3: Fix or Remove EmpericaTracker ✅

Either:
- Fix the import issue in `auto_tracker.py`, OR
- Remove it from bootstrap if not needed

### Phase 4: Update Component Loading Logic ✅

Remove code that tries to instantiate deleted components.

---

## Testing Requirements

### Unit Tests to Run

**File:** `tests/unit/test_all_cli_commands.py`

```bash
# Test bootstrap command
pytest tests/unit/test_all_cli_commands.py::TestCoreWorkflowCommands::test_bootstrap_help -v

# Should pass after cleanup
```

### Manual Tests

```bash
# Test basic bootstrap
empirica bootstrap

# Test with test flag
empirica bootstrap --test

# Test verbose mode
empirica bootstrap --verbose

# Should all work without import errors
```

### Expected Output

```
✅ Bootstrap complete!
   📊 Components loaded: 6-8 (depends on level)
   ⏱️ Bootstrap time: <100μs
   🎯 Level: standard
   🎭 Profile: auto-selected
```

---

## Files to Modify

1. ✅ `empirica/bootstraps/optimal_metacognitive_bootstrap.py`
   - Remove 3 dead imports
   - Fix 2 import paths
   - Remove component instantiation code

2. ✅ `empirica/bootstraps/extended_metacognitive_bootstrap.py`
   - Remove 10 dead imports
   - Remove component instantiation code

3. ⚠️ `empirica/auto_tracker.py` (optional)
   - Fix import if keeping
   - Or remove entirely if not used

---

## Impact Analysis

### Current Behavior
- ✅ Bootstrap works (falls back to MCP server)
- ⚠️ Import errors printed but caught
- ✅ Loads correct 6 core components

### After Cleanup
- ✅ Bootstrap works (cleaner code)
- ✅ No import errors
- ✅ Faster bootstrap (no failed imports)
- ✅ Easier to maintain

### Risk Level
**LOW** - MCP server is primary bootstrap path, local bootstrap is fallback

---

## Success Criteria

### Must Pass
- [ ] `empirica bootstrap` works without errors
- [ ] `empirica bootstrap --test` passes all tests
- [ ] No import errors in stdout/stderr
- [ ] Unit tests pass: `pytest tests/unit/test_all_cli_commands.py::TestCoreWorkflowCommands`

### Should Work
- [ ] Bootstrap time < 200μs
- [ ] Loads 6-8 components (depending on level)
- [ ] Verbose mode shows loaded components

---

## Implementation Checklist

### Step 1: Backup
```bash
cp empirica/bootstraps/optimal_metacognitive_bootstrap.py empirica/bootstraps/optimal_metacognitive_bootstrap.py.bak
cp empirica/bootstraps/extended_metacognitive_bootstrap.py empirica/bootstraps/extended_metacognitive_bootstrap.py.bak
```

### Step 2: Remove Dead Imports
- [ ] Remove `adaptive_uncertainty_calibration` imports
- [ ] Remove `context_validation` imports
- [ ] Remove `runtime_validation` imports
- [ ] Remove `environment_stabilization` imports
- [ ] Remove `workspace_awareness` imports
- [ ] Remove `empirical_performance_analyzer` imports
- [ ] Remove `intelligent_navigation` imports
- [ ] Remove `security_monitoring` imports
- [ ] Remove `procedural_analysis` imports

### Step 3: Fix Moved Imports
- [ ] Update `metacognition_12d_monitor` import path
- [ ] Update `metacognitive_cascade` import path

### Step 4: Remove Component Initialization
- [ ] Remove code that instantiates deleted components
- [ ] Update component count expectations

### Step 5: Fix auto_tracker
- [ ] Investigate `auto_tracker.py` import issue
- [ ] Either fix or remove

### Step 6: Test
- [ ] Run `empirica bootstrap`
- [ ] Run `empirica bootstrap --test`
- [ ] Run unit tests
- [ ] Check for any import errors

### Step 7: Verify
- [ ] Components loaded: 6-8 ✅
- [ ] No stderr output ✅
- [ ] Fast bootstrap time ✅

---

## Additional Context

### Why These Components Were Removed

These were **"extra" components** not part of the **core** Empirica framework:
- Moved to keep core minimal
- Reduced complexity
- Focused on essential epistemic tracking
- Extra components can be loaded separately if needed

### Core Components (Should Remain)

These 6 components ARE loaded and correct:
1. Session management
2. Epistemic assessment
3. Goal orchestration
4. Handoff reports
5. Git checkpoints
6. Profile configuration

---

## For Qwen

**Your task:**
1. Clean up dead imports from bootstrap files
2. Fix import paths for moved components
3. Remove component initialization for deleted components
4. Test that bootstrap still works
5. Run unit tests to verify

**Time estimate:** 30-60 minutes  
**Difficulty:** Low (mostly deletions)  
**Risk:** Low (MCP server is fallback)

**When done, verify:**
```bash
empirica bootstrap --test
pytest tests/unit/test_all_cli_commands.py::TestCoreWorkflowCommands -v
```

Both should pass without import errors.

---

**Created by:** claude-code  
**Session:** 5c6e00d1-f441-4112-be78-072dd8464fc8  
**Date:** 2025-12-01
