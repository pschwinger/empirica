# Production Docs Refactoring Plan

## Files Needing Updates (10 files):

### High Priority (References to Removed Code):
1. ✅ **03_BASIC_USAGE.md** - Update bootstrap examples (no component loading)
2. ✅ **05_EPISTEMIC_VECTORS.md** - Remove 12-vector, confirm 13-vector standard
3. ✅ **08_BAYESIAN_GUARDIAN.md** - Remove calibration references
4. ✅ **12_SESSION_DATABASE.md** - Update create_session() signature (optional params)
5. ✅ **13_PYTHON_API.md** - Update API examples (bootstrap, SessionDatabase)

### Medium Priority (May Reference Removed Components):
6. ✅ **11_DASHBOARD_MONITORING.md** - Check 12-vector references
7. ✅ **15_CONFIGURATION.md** - Check calibration config
8. ✅ **18_MONITORING_LOGGING.md** - Check auto_tracker references
9. ✅ **20_TOOL_CATALOG.md** - Remove deprecated tools (assess, calibration)
10. ✅ **22_FAQ.md** - Update any outdated answers

### Also Check:
- **00_COMPLETE_SUMMARY.md** - Update summary to reflect changes
- **19_API_REFERENCE.md** - Update API signatures
- **21_TROUBLESHOOTING.md** - Remove troubleshooting for removed components

---

## Changes Needed:

### 1. Remove References to Deleted Code:
- ❌ metacognition_12d_monitor (2,459 lines)
- ❌ TwelveVectorSelfAwareness
- ❌ MetacognitionMonitor
- ❌ calibration module (1,493 lines)
- ❌ AdaptiveUncertaintyCalibration
- ❌ ParallelReasoning
- ❌ auto_tracker (497 lines)

### 2. Update to Current Reality:
- ✅ 13-vector canonical system (ONLY)
- ✅ CanonicalEpistemicAssessor (standard)
- ✅ Simplified bootstrap (session creation only)
- ✅ SessionDatabase.create_session(ai_id, bootstrap_level=0, components_loaded=0)
- ✅ Components created on-demand (no pre-loading)

### 3. Remove Deprecated Commands:
- ❌ `empirica assess` (heuristic-based, deprecated)
- ❌ `empirica calibration` (module removed)
- ❌ Old 12-vector commands

---

## Execution Plan:

### Quick Pass (Search & Note):
Find all mentions and create replacement list

### Systematic Updates:
Go file by file, update references

### Validation:
Ensure no broken references remain

---

**Start with:** 05_EPISTEMIC_VECTORS.md (most critical - defines the standard)

