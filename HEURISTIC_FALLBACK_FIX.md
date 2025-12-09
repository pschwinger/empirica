# Heuristic Fallback Fix

**Date:** 2025-12-08  
**Issue:** Investigation handoffs showed "No genuine calibration... - using heuristic fallback" warning  
**Status:** ✅ Fixed

---

## Problem

When creating investigation handoffs (PREFLIGHT→CHECK), the system showed:
```
No genuine calibration for 30f66c66... - using heuristic fallback
```

Even though the handoff was created successfully.

---

## Root Cause

The `_check_calibration()` method was trying to fetch POSTFLIGHT calibration data for all handoffs, including investigation handoffs.

**Issue:** Investigation handoffs use CHECK phase, which doesn't have `calibration_accuracy` in metadata because:
- CHECK is a **decision gate**, not a learning measurement
- Calibration measures PREFLIGHT→POSTFLIGHT learning accuracy
- Investigation handoffs are PREFLIGHT→CHECK (no POSTFLIGHT yet)

---

## Solution

Updated `empirica/core/handoff/report_generator.py` to:

1. **Detect investigation handoffs** by checking if `end_assessment.get('phase') == 'CHECK'`
2. **Skip calibration** for investigation handoffs (return 'investigation-only' status)
3. **Remove warning** for investigation handoffs (calibration not applicable)

### Code Changes

```python
def _check_calibration(self, session_id: str, deltas: Dict[str, float], end_assessment: Dict) -> Dict:
    """
    Get calibration status - prioritize genuine introspection, validate with heuristics
    
    For investigation handoffs (PREFLIGHT→CHECK), calibration is not applicable
    since CHECK is a decision gate, not a learning measurement.
    """
    # NEW: Check if this is investigation handoff (CHECK phase)
    if end_assessment and end_assessment.get('phase') == 'CHECK':
        return {
            'status': 'investigation-only',
            'reasoning': 'Investigation handoff (PREFLIGHT→CHECK) - calibration not applicable',
            'source': 'n/a'
        }
    
    # ... rest of calibration logic for complete handoffs ...
```

### Key Fix

**Before:** `if end_assessment.get('vectors', {}).get('phase') == 'CHECK':`  
**After:** `if end_assessment.get('phase') == 'CHECK':`

**Reason:** `phase` is a top-level key in assessment dict, not inside `vectors`.

---

## Validation

**Test case:**
```python
# Investigation handoff (PREFLIGHT→CHECK)
session_id = "30f66c66-f4c8-4857-94f7-fc091c85d40d"
generator = EpistemicHandoffReportGenerator()

checks = generator.db.get_check_phase_assessments(session_id)
check = checks[-1]  # Most recent CHECK

calibration = generator._check_calibration(session_id, deltas, check)
# Expected: {'status': 'investigation-only', 'source': 'n/a'}
```

**Result:** ✅ No heuristic fallback warning for investigation handoffs

---

## Impact

**Before:**
- Every investigation handoff showed confusing warning
- Users might think something was wrong
- Warning logs cluttered output

**After:**
- ✅ Investigation handoffs: Clean output, no warnings
- ✅ Complete handoffs: Still use genuine calibration from POSTFLIGHT
- ✅ Clear distinction between handoff types

---

## Handoff Types and Calibration

| Handoff Type | Pattern | Calibration |
|--------------|---------|-------------|
| Investigation | PREFLIGHT→CHECK | Not applicable (decision gate) |
| Complete | PREFLIGHT→POSTFLIGHT | Measured (learning accuracy) |
| Planning | No CASCADE | Not applicable (documentation) |

---

## Files Modified

- `empirica/core/handoff/report_generator.py` - Fixed `_check_calibration()` method

**Changes:**
1. Added CHECK phase detection
2. Return 'investigation-only' status for investigation handoffs
3. Fixed phase detection logic (top-level key)
4. Removed warning for investigation handoffs
5. Added check for `isinstance(metadata, dict)` to prevent NoneType errors

---

## Related Issues

This fix also addressed a related bug we fixed earlier:
- Removed `actual_confidence` field reference that didn't exist (line 367)
- That was causing the first fallback trigger

Both fixes ensure investigation handoffs work cleanly without spurious warnings.

---

**Status:** Complete and tested ✅  
**Confidence:** High - proper detection of handoff type
