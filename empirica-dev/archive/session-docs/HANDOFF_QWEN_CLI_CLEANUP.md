# HANDOFF: CLI Handler Cleanup - Remove Dead Imports

**For:** Qwen  
**Task:** Remove unused deprecated imports from CLI command handlers  
**Priority:** MEDIUM - Cleanup after core migration  
**Estimated Time:** 1-2 hours

---

## Your Mission

Remove unused `AdaptiveUncertaintyCalibration` imports from 6 CLI handler files. These are likely just dead imports (imported but never used).

---

## Context

**What we fixed:** CASCADE core now uses MirrorDriftMonitor (no heuristics).

**Your job:** Clean up CLI handlers that imported the old calibration system but probably never used it.

---

## Files to Clean (6 total)

All in `empirica/cli/command_handlers/`:

1. cascade_commands.py
2. assessment_commands.py
3. bootstrap_commands.py
4. utility_commands.py (has 2 import lines)
5. modality_commands.py

---

## Step-by-Step Process (Same for All Files)

### For Each File:

**Step 1: Check if import exists**
```bash
grep -n "from empirica.calibration" empirica/cli/command_handlers/<filename>.py
```

**Step 2: Check if actually used**
```bash
grep -n "AdaptiveUncertaintyCalibration" empirica/cli/command_handlers/<filename>.py
```

**Step 3A: If only 1 match (just the import line)**
→ **It's unused!** Just remove the import line.

**Step 3B: If multiple matches (import + usage)**
→ **It's used.** Comment out the usage with deprecation note.

**Step 4: Verify file still works**
```bash
python3 -c "from empirica.cli.command_handlers import <module_name>; print('✅ OK')"
```

---

## Detailed Instructions Per File

### 1. cascade_commands.py

```bash
# Check
grep -n "AdaptiveUncertaintyCalibration" empirica/cli/command_handlers/cascade_commands.py
```

If only import line appears → Remove it  
If code uses it → Comment out that code section

### 2. assessment_commands.py

Same process. Likely just unused import.

### 3. bootstrap_commands.py

Same process. Likely just unused import.

### 4. utility_commands.py

**NOTE:** This file has **2 separate imports** of AdaptiveUncertaintyCalibration.

Check both and remove/comment as needed.

### 5. modality_commands.py

Same process. Likely just unused import.

---

## Testing Strategy

### Test 1: Each module imports successfully
```bash
python3 -c "
from empirica.cli.command_handlers import cascade_commands
from empirica.cli.command_handlers import assessment_commands
from empirica.cli.command_handlers import bootstrap_commands
from empirica.cli.command_handlers import utility_commands
from empirica.cli.command_handlers import modality_commands
print('✅ All handlers import successfully')
"
```

### Test 2: CLI commands still work
```bash
# Test a few key commands
empirica --help
empirica preflight --help
empirica check --help
empirica bootstrap --help
```

Should all work without errors.

### Test 3: MCP server still works
```bash
pytest tests/mcp/ -v
```

Should pass (these test the MCP tool exposure).

### Test 4: CLI tests pass
```bash
pytest tests/unit/cli/ -v
```

Should pass.

---

## Example: Removing Unused Import

**Before:**
```python
from empirica.calibration.adaptive_uncertainty_calibration import AdaptiveUncertaintyCalibration
from empirica.core.metacognitive_cascade import CanonicalEpistemicCascade
```

**After:**
```python
from empirica.core.metacognitive_cascade import CanonicalEpistemicCascade
```

Simple! Just delete the line.

---

## Example: Commenting Out Used Code

If code actually uses it:

**Before:**
```python
from empirica.calibration.adaptive_uncertainty_calibration import AdaptiveUncertaintyCalibration

def some_function():
    calibrator = AdaptiveUncertaintyCalibration()
    result = calibrator.calibrate()
    return result
```

**After:**
```python
# DEPRECATED: AdaptiveUncertaintyCalibration removed (used heuristics)
# from empirica.calibration.adaptive_uncertainty_calibration import AdaptiveUncertaintyCalibration

def some_function():
    # DEPRECATED: This calibration feature used heuristics
    # Removed as part of no-heuristics migration
    # TODO: Replace with MirrorDriftMonitor if needed
    # calibrator = AdaptiveUncertaintyCalibration()
    # result = calibrator.calibrate()
    # return result
    return None  # Feature disabled
```

---

## Success Criteria

- [ ] All 6 files cleaned (no calibration imports)
- [ ] All handlers import successfully
- [ ] CLI commands work (--help at minimum)
- [ ] MCP tests pass
- [ ] CLI unit tests pass

---

## Tracking Your Progress

Use this checklist:

```
CASCADE COMMANDS:
- [ ] Checked for usage
- [ ] Removed/commented import
- [ ] Verified imports OK
- [ ] Notes: ___________

ASSESSMENT COMMANDS:
- [ ] Checked for usage
- [ ] Removed/commented import
- [ ] Verified imports OK
- [ ] Notes: ___________

BOOTSTRAP COMMANDS:
- [ ] Checked for usage
- [ ] Removed/commented import
- [ ] Verified imports OK
- [ ] Notes: ___________

UTILITY COMMANDS:
- [ ] Checked for usage (2 imports!)
- [ ] Removed/commented imports
- [ ] Verified imports OK
- [ ] Notes: ___________

MODALITY COMMANDS:
- [ ] Checked for usage
- [ ] Removed/commented import
- [ ] Verified imports OK
- [ ] Notes: ___________
```

---

## Report Back

When done, report:

```
✅ CLI HANDLER CLEANUP COMPLETE

Files cleaned:
- cascade_commands.py: [removed import / commented usage]
- assessment_commands.py: [removed import / commented usage]
- bootstrap_commands.py: [removed import / commented usage]
- utility_commands.py: [removed 2 imports / commented usage]
- modality_commands.py: [removed import / commented usage]

Tests:
- Import test: ✅ PASS
- CLI commands: ✅ WORK
- MCP tests: ✅ PASS (X/X)
- CLI unit tests: ✅ PASS (X/X)

Issues encountered: [None / describe any]

Ready for next task: YES
```

---

## Quick Reference

**Find deprecated imports:**
```bash
grep -r "from empirica.calibration" empirica/cli/command_handlers/
```

**Check if actually used:**
```bash
grep -n "AdaptiveUncertaintyCalibration" <filename>
```

**Test import works:**
```bash
python3 -c "from empirica.cli.command_handlers import <module>; print('OK')"
```

**Run tests:**
```bash
pytest tests/mcp/ -v
pytest tests/unit/cli/ -v
```

---

**You got this! Most of these are probably just dead imports. Easy cleanup.** 🚀
