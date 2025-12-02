# Drift Monitor Migration Progress

## Completed: CASCADE Core (CRITICAL)

### ✅ File: empirica/core/metacognitive_cascade/metacognitive_cascade.py

**Changes made:**
1. Removed import: `from empirica.calibration.parallel_reasoning import ParallelReasoningSystem, DriftMonitor`
2. Added import: `from empirica.core.drift import MirrorDriftMonitor`
3. Removed ParallelReasoningSystem initialization (was deprecated heuristic system)
4. Updated drift monitor initialization to use MirrorDriftMonitor
5. Replaced behavioral drift analysis (sycophancy, tension) with epistemic temporal comparison
6. Updated drift detection to use git checkpoint history comparison
7. Removed all sycophancy/tension references

**Result:** CASCADE now uses MirrorDriftMonitor (NO HEURISTICS) ✅

---

## Remaining Files (11 total)

### Bootstrap Files (2 files):
- [ ] empirica/bootstraps/optimal_metacognitive_bootstrap.py
- [ ] empirica/bootstraps/extended_metacognitive_bootstrap.py

### CLI Handlers (6 files - may just be unused imports):
- [ ] empirica/cli/command_handlers/cascade_commands.py
- [ ] empirica/cli/command_handlers/assessment_commands.py
- [ ] empirica/cli/command_handlers/bootstrap_commands.py
- [ ] empirica/cli/command_handlers/utility_commands.py (2 places)
- [ ] empirica/cli/command_handlers/modality_commands.py

### Comments/Documentation (1 file):
- [ ] empirica/data/session_json_handler.py (just comment)

---

**Status:** 1 of 12 files complete  
**Critical file (CASCADE) done!** ✅  
**Next:** Bootstrap files or test first?
