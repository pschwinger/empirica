# Production Docs Refactoring Needed

## Files Removed Today (Need to Remove from Docs):

1. **metacognition_12d_monitor/** (2,459 lines)
   - TwelveVectorSelfAwareness
   - MetacognitionMonitor
   - UVL protocol (old version)

2. **calibration/** (1,493 lines)
   - AdaptiveUncertaintyCalibration
   - ParallelReasoning
   - Bayesian belief tracker

3. **auto_tracker.py** (497 lines)
   - EmpericaTracker

4. **Bootstrap** (simplified from 1,216 → 130 lines)
   - No more component loading
   - Just session creation
   - OptimalMetacognitiveBootstrap (now thin wrapper)
   - ExtendedMetacognitiveBootstrap (now identical)

## Docs to Update:

### High Priority:
1. **05_EPISTEMIC_VECTORS.md** - Remove 12-vector references, confirm 13-vector standard
2. **08_BAYESIAN_GUARDIAN.md** - Remove if references calibration
3. **09_DRIFT_MONITOR.md** - Check if references removed components
4. **03_BASIC_USAGE.md** - Update bootstrap examples
5. **13_PYTHON_API.md** - Update API examples (SessionDatabase, bootstrap)

### Medium Priority:
6. **20_TOOL_CATALOG.md** - Remove deprecated tools
7. **19_API_REFERENCE.md** - Update API signatures
8. **14_CUSTOM_PLUGINS.md** - Check component references

### Files to Check for Mentions:
