# Unused Python Files Audit - Cleanup for Sanity

**Goal:** Remove files not used in production system

---

## Strategy

1. Find all .py files
2. Check if imported anywhere
3. Check if executed directly
4. Mark for removal if unused

---

## Scanning for unused files...

## Potentially Unused Files Found

### Check these files:


## Known Candidates for Removal/Deprecation

### 1. calibration/ Module (3-4 files) - DEPRECATED
**Reason:** Replaced by MirrorDriftMonitor (no heuristics)

**Files:**
- empirica/calibration/parallel_reasoning.py (old DriftMonitor)
- empirica/calibration/adaptive_uncertainty_calibration/ (whole directory)

**Action:** Move to empirica-dev/deprecated-modules/ after migration complete

**Status:** Keep for now (2 bootstrap files + 6 CLI handlers still import)  
**Remove after:** Gemini + Qwen complete their tasks

---

### 2. Root test files (3 files) - SHOULD BE IN tests/
**Files found in root:**
- test_goal_creation_integration.py
- test_mirror_drift_monitor.py
- test_subtask_integration.py

**Action:** Move to tests/integration/ or delete if redundant

---

### 3. Checking for other unused files...
⚠️ Potentially unused: empirica/cognitive_benchmarking/erb/erb_cloud_cli_runner.py
⚠️ Potentially unused: empirica/cognitive_benchmarking/erb/erb_real_model_runner.py
⚠️ Potentially unused: empirica/cognitive_benchmarking/erb/run_manual_test.py
⚠️ Potentially unused: empirica/cognitive_benchmarking/erb/test_enhanced_cascade.py
⚠️ Potentially unused: empirica/scripts/migrate_handoff_storage.py
