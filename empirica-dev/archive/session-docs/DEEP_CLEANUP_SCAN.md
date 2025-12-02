# Deep Cleanup Scan - Round 2

**Goal:** Find all deprecation candidates for super clean codebase

---

## Scan 1: Checking for TODO/DEPRECATED markers in code


## Scan 2: Looking for duplicate/similar functionality

Checking for multiple implementations of same feature...

### Goal Orchestrators:

## Scan 3: Checking imports to find isolated modules

Finding modules that import nothing from empirica (might be standalone/unused)...


## Scan 4: Check for old/new versions of same functionality

Looking for files with "old", "new", "legacy", "v2" in names...


## Scan 5: Check for experimental features

Finding "experimental" markers...


---

## ANALYSIS: Major Cleanup Opportunities Found

### 🔴 CRITICAL: Deprecated Code Still Referenced

**Found in CLI handlers (already marked DEPRECATED):**
- assessment_commands.py - 3 DEPRECATED markers
- bootstrap_commands.py - 3 DEPRECATED markers  
- utility_commands.py - 6 DEPRECATED markers

**Action:** Qwen is handling this (CLI cleanup task) ✅

---

### 🟡 HIGH PRIORITY: Isolated Components (No empirica imports)

**12 Component files that don't import from empirica:**

These are standalone components not integrated:
1. empirical_performance_analyzer.py (977 lines!)
2. code_intelligence_analyzer.py (1338 lines!)
3. intelligent_navigation.py (748 lines)
4. security_monitoring.py (220 lines)
5. environment_stabilization.py (362 lines)
6. procedural_analysis.py (253 lines)
7. workspace_awareness.py (172 lines)
8. runtime_validation.py (251 lines)
9. context_validation.py (345 lines)

**Total:** ~4,666 lines of isolated component code

**Analysis:** These are designed as standalone components but not integrated into core
**Decision needed:** Keep as optional components or move to empirica-dev?

---

### 🟢 MEDIUM PRIORITY: Duplicate Thresholds

**Files:**
- empirica/config/threshold_loader.py
- empirica/core/thresholds.py

**Action:** Check if both needed or if one can be removed

---

### 🔵 LOW PRIORITY: TODOs to Track

**Found 8 TODO items:**
1. Identity commands - signature storage (2 TODOs)
2. Goal discovery - import to local database
3. Chat handler - get candidates from switcher
4. Sentinel - async execution
5. Session sync - detect updates
6. Handoff storage - sync to database
7. Modality switcher - self-assessment API call

**Action:** Document as future enhancements, not blockers

---

## RECOMMENDATIONS

### Immediate Actions:

**1. Move Isolated Components to empirica-dev/components-standalone/**
```bash
# These 9 components don't integrate with core
mv empirica/components/empirical_performance_analyzer ../empirica-dev/components-standalone/
mv empirica/components/code_intelligence_analyzer ../empirica-dev/components-standalone/
mv empirica/components/intelligent_navigation ../empirica-dev/components-standalone/
mv empirica/components/security_monitoring ../empirica-dev/components-standalone/
mv empirica/components/environment_stabilization ../empirica-dev/components-standalone/
mv empirica/components/procedural_analysis ../empirica-dev/components-standalone/
mv empirica/components/workspace_awareness ../empirica-dev/components-standalone/
mv empirica/components/runtime_validation ../empirica-dev/components-standalone/
mv empirica/components/context_validation ../empirica-dev/components-standalone/
```

**Result:** ~4,666 lines moved, cleaner component directory

---

**2. Check Thresholds Duplication**

Compare:
- empirica/config/threshold_loader.py (loads from config)
- empirica/core/thresholds.py (default values)

**Action:** Verify both needed

---

**3. Mark Experimental Features Clearly**

Files marked EXPERIMENTAL:
- modality_commands.py (already marked ✅)
- mcp_commands.py (marked experimental)

**Action:** Ensure docs reflect experimental status

---

## Expected Results After Full Cleanup

**Current state:**
- 168 Python files in empirica/
- ~4,666 lines in isolated components
- Deprecated code markers everywhere

**After cleanup:**
- ~158-160 Python files (remove 9 component files)
- Clear separation: core vs experimental vs standalone
- Clean codebase ready for documentation

---

## Questions for User

### Question 1: Isolated Components (9 files, 4,666 lines)
**Files:** All the standalone component analyzers  
**Status:** No imports from empirica, not integrated  
**Options:**
- A) Move to empirica-dev/components-standalone/ (recommended)
- B) Keep (mark as "available but not integrated")

### Question 2: Thresholds Files (2 files)
**Files:** threshold_loader.py vs thresholds.py  
**Status:** Possible duplication  
**Options:**
- A) Check if both needed
- B) Keep both (one loads config, one has defaults)

### Question 3: Experimental Features
**Files:** modality_commands.py, mcp_commands.py  
**Status:** Already marked experimental  
**Action:** Just ensure docs reflect this ✅

---

## Summary

**Found for removal:**
- 9 isolated component files (~4,666 lines)
- Possible duplicate thresholds (need to check)

**Already handled:**
- Deprecated markers (Qwen cleaning up)
- Experimental markers (already present)
- TODOs (documented, not blockers)

**Potential impact:**
- 168 → ~158 files (another 10 files moved)
- Even cleaner, more focused codebase
- Clear separation of core vs optional

