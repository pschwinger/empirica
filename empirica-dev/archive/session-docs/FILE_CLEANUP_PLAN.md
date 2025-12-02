# File Cleanup Plan - Remove Unused Code

**Found:** 20+ unused Python files  
**Goal:** Move to empirica-dev for sanity and clarity

---

## Category 1: Root Test Files (MOVE NOW)

**Files in wrong location:**
- test_goal_creation_integration.py
- test_mirror_drift_monitor.py
- test_subtask_integration.py

**Action:** Move to tests/integration/
```bash
mv test_*.py tests/integration/
```

---

## Category 2: Deprecated calibration/ (MOVE AFTER MIGRATION)

**Wait for Gemini + Qwen to finish, then move:**
- empirica/calibration/parallel_reasoning.py
- empirica/calibration/adaptive_uncertainty_calibration/

**Action:** Move to empirica-dev/deprecated-modules/
```bash
mv empirica/calibration/ ../empirica-dev/deprecated-modules/
```

---

## Category 3: Unused Components (MOVE NOW)

**Tool management (not imported):**
- empirica/components/tool_management/meta_mcp_registry.py
- empirica/components/tool_management/epistemic_tool_selector_minimal.py
- empirica/components/tool_management/enhanced_file_tools.py
- empirica/components/tool_management/enhanced_bash_tools.py

**Decision needed:** Are these planned features or dead code?
- If planned: Keep but document as "not yet integrated"
- If dead: Move to empirica-dev/unused-components/

---

## Category 4: Unused CLI Components (CHECK FIRST)

**Potentially unused:**
- empirica/cli/__main__.py (may be entry point - CHECK!)
- empirica/cli/simple_session_server.py (lightweight server - may be used)
- empirica/cli/command_handlers/onboard_handler.py (onboarding - may be called)

**Action:** Verify not used, then move or keep

---

## Category 5: Benchmarking/Testing Tools (MOVE NOW)

**Cognitive benchmarking:**
- empirica/cognitive_benchmarking/erb/erb_real_model_runner.py
- empirica/cognitive_benchmarking/erb/erb_cloud_cli_runner.py
- empirica/cognitive_benchmarking/erb/run_manual_test.py
- empirica/cognitive_benchmarking/erb/test_enhanced_cascade.py

**Action:** Move to empirica-dev/benchmarking-tools/
```bash
mv empirica/cognitive_benchmarking/ ../empirica-dev/benchmarking-tools/
```

---

## Category 6: Unused Config Loaders (CHECK FIRST)

**File:**
- empirica/config/goal_scope_loader.py

**Action:** Check if goal scopes are still used (ScopeVector system)
- If yes: Keep (it's loaded dynamically)
- If no: Move to empirica-dev

---

## Category 7: Dashboard Components (MOVE OR MARK EXPERIMENTAL)

**Files:**
- empirica/dashboard/cascade_monitor.py
- empirica/plugins/dashboard_spawner.py

**Decision:** These are optional/experimental features
- Move to empirica-dev/experimental-features/
- Or keep but mark clearly as experimental in docs

---

## Category 8: Unused Handoff/Plugin Components (MOVE NOW)

**Files:**
- empirica/core/handoff/auto_generator.py
- empirica/plugins/base_plugin.py (may be base class - CHECK!)
- empirica/plugins/modality_switcher/genuine_self_assessment.py
- empirica/plugins/modality_switcher/domain_vectors.py
- empirica/plugins/modality_switcher/epistemic_router.py
- empirica/plugins/modality_switcher/epistemic_extractor.py
- empirica/plugins/modality_switcher/domain_vectors_custom/example_chemistry.py

**Action:** These look like modality switcher (experimental)
- Move entire modality_switcher/ to empirica-dev/experimental-features/
- Or keep but mark as experimental

---

## Category 9: Migration Scripts (MOVE NOW)

**Files:**
- empirica/scripts/migrate_handoff_storage.py (one-time migration - done)

**Action:** Move to empirica-dev/migration-scripts/

---

## Immediate Actions (Safe to Move Now)

### Move #1: Root test files
```bash
mv test_goal_creation_integration.py tests/integration/
mv test_mirror_drift_monitor.py tests/integration/
mv test_subtask_integration.py tests/integration/
```

### Move #2: Migration scripts
```bash
mkdir -p ../empirica-dev/migration-scripts/
mv empirica/scripts/migrate_handoff_storage.py ../empirica-dev/migration-scripts/
```

### Move #3: Benchmarking tools
```bash
mkdir -p ../empirica-dev/benchmarking-tools/
mv empirica/cognitive_benchmarking ../empirica-dev/benchmarking-tools/
```

---

## Decisions Needed from User

### Question 1: Components
**Files:** tool_management/*.py (4 files)  
**Status:** Not imported anywhere  
**Options:**
- A) Move to empirica-dev (dead code)
- B) Keep (planned feature, not integrated yet)

### Question 2: Dashboard
**Files:** dashboard/*.py, dashboard_spawner.py  
**Status:** Not imported in core  
**Options:**
- A) Move to empirica-dev/experimental/
- B) Keep but mark as experimental in docs

### Question 3: Modality Switcher
**Files:** plugins/modality_switcher/*.py (multiple files)  
**Status:** Experimental multi-AI routing  
**Options:**
- A) Move to empirica-dev/experimental/
- B) Keep (advanced feature, working but optional)

### Question 4: CLI Components
**Files:** __main__.py, simple_session_server.py, onboard_handler.py  
**Status:** May be used indirectly  
**Options:**
- A) Verify not used, then move
- B) Keep (may be CLI entry points)

---

## Summary

**Definitely move (safe):**
- 3 root test files → tests/integration/
- 1 migration script → empirica-dev/
- Benchmarking tools → empirica-dev/

**After migration complete:**
- calibration/ → empirica-dev/deprecated/

**Need user decision:**
- Components (4 files)
- Dashboard (2 files)  
- Modality switcher (6+ files)
- CLI components (3 files)

**Total cleanup:** ~25-30 files can be moved

---

## Expected Result

**Before:** 187 Python files  
**After:** ~155-160 Python files in core  
**Moved:** ~25-30 files to empirica-dev

**Benefit:** Clearer codebase, easier to understand what's actually used

---

**Ready to execute safe moves?** (3 categories, ~10 files)
