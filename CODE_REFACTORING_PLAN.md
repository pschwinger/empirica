# Code Refactoring Plan - Step 3

**Goal:** Remove explicit phase tracking, make CASCADE guidance-only
**Status:** Documentation complete, ready for code refactoring

---

## Issues Found in Code

### 1. metacognitive_cascade.py (MAJOR)

**Line 90:** `class CascadePhase(Enum)` 
```python
class CascadePhase(Enum):
    PREFLIGHT = "PREFLIGHT"
    THINK = "THINK"
    PLAN = "PLAN"
    INVESTIGATE = "INVESTIGATE"
    CHECK = "CHECK"
    ACT = "ACT"
    POSTFLIGHT = "POSTFLIGHT"
```

**Problem:** Treats CASCADE as explicit state machine phases

**Line 105:** `current_phase: CascadePhase` - Tracking phase as state

**Lines with _enter_phase():**
- Line 420: `_enter_phase(CascadePhase.PREFLIGHT)`
- Line 523: `_enter_phase(CascadePhase.THINK)`
- Line 809: `_enter_phase(CascadePhase.INVESTIGATE)`
- Line 861: `_enter_phase(CascadePhase.CHECK)`
- Line 904: `_enter_phase(CascadePhase.ACT)`
- Line 974: `_enter_phase(CascadePhase.POSTFLIGHT)`

**Line 2178:** `def _enter_phase()` - Phase transition logic

**Problem:** Explicit phase state machine instead of implicit workflow

### 2. epistemic_assessment.py

**Line 21:** `class CascadePhase(Enum)` - Same phase enum

**Problem:** Should be `AssessmentType(PRE, CHECK, POST)` not phases

### 3. protocols.yaml

**Likely has:** `phase` enum with CASCADE phases

**Problem:** Should distinguish assessment types from workflow guidance

---

## Refactoring Strategy

### Option 1: Minimal Change (Keep backward compatibility)
**Approach:**
- Rename `CascadePhase` → `AssessmentType` 
- Keep only: `PRE`, `CHECK`, `POST`
- Add `current_work_type` (optional, for logging): "thinking", "investigating", "acting"
- Remove `_enter_phase()` enforcement
- Make phase tracking optional/internal

**Pros:** Easier migration, less breakage
**Cons:** Still tracks some state

### Option 2: Full Removal (Align with philosophy)
**Approach:**
- Remove `CascadePhase` enum entirely
- Remove `current_phase` tracking
- Remove `_enter_phase()` method
- Track only: `current_assessment` (PRE/CHECK/POST)
- Workflow (think/investigate/act) is implicit, not tracked

**Pros:** Fully aligns with "CASCADE is guidance" philosophy
**Cons:** Breaking change, more refactoring needed

### Option 3: Hybrid (Recommended)
**Approach:**
- Keep `AssessmentType(PRE, CHECK, POST)` for explicit checkpoints
- Add optional `work_context` string for logging (not enforced)
- Remove phase transitions and state machine logic
- Let AI indicate current work type via metadata (optional)

**Pros:** Clear separation, minimal breaking changes, aligns with philosophy
**Cons:** Requires careful refactoring

---

## Recommended: Option 3 (Hybrid)

### Changes Needed:

#### 1. Create New Enum (epistemic_assessment.py)
```python
class AssessmentType(Enum):
    """Explicit epistemic assessment checkpoints"""
    PRE = "PRE"          # Session start baseline
    CHECK = "CHECK"      # Decision point (0-N times)
    POST = "POST"        # Session end calibration

# Deprecated (for migration)
class CascadePhase(Enum):
    """DEPRECATED: Use AssessmentType instead"""
    PREFLIGHT = "PRE"
    CHECK = "CHECK"
    POSTFLIGHT = "POST"
```

#### 2. Update metacognitive_cascade.py
```python
class CascadeState:
    """
    Tracks explicit assessments only.
    Workflow (think/investigate/act) is implicit guidance.
    """
    current_assessment: Optional[AssessmentType] = None
    work_context: Optional[str] = None  # Optional: "investigating", "acting", etc.
    
    # Remove: current_phase, _enter_phase()
```

#### 3. Replace _enter_phase() calls
```python
# Before:
self._enter_phase(CascadePhase.PREFLIGHT)

# After:
self.current_assessment = AssessmentType.PRE
self.work_context = "assessing"  # Optional metadata
```

#### 4. Update method signatures
```python
# Before:
def preflight(self, prompt: str) -> EpistemicAssessment:
    self._enter_phase(CascadePhase.PREFLIGHT)
    ...

# After:
def pre_assessment(self, prompt: str) -> EpistemicAssessment:
    """PRE assessment at session start"""
    self.current_assessment = AssessmentType.PRE
    # No enforcement, just tracking for logging
    ...
```

#### 5. Update protocols.yaml
```yaml
# Before:
phase:
  enum: ["PREFLIGHT", "THINK", "INVESTIGATE", "CHECK", "ACT", "POSTFLIGHT"]

# After:
assessment_type:
  enum: ["PRE", "CHECK", "POST"]
  description: "Explicit epistemic assessment checkpoints"

work_context:  # Optional, for logging only
  type: string
  description: "Current work type (thinking, investigating, acting) - not enforced"
  examples: ["thinking", "investigating", "acting", "planning"]
```

---

## Migration Strategy

### Phase 1: Add New, Keep Old (Backward Compatible)
1. Add `AssessmentType` enum
2. Add `current_assessment` field
3. Keep `CascadePhase` and `current_phase` (deprecated)
4. Both work simultaneously

### Phase 2: Update Internals
1. Replace internal usage of `CascadePhase` with `AssessmentType`
2. Update method names (preflight → pre_assessment) as aliases
3. Keep old names as deprecated wrappers

### Phase 3: Deprecation Warnings
1. Add deprecation warnings to old enums/methods
2. Update all documentation references
3. Update examples

### Phase 4: Remove (Future)
1. Remove deprecated code after migration period
2. Final cleanup

---

## Testing Strategy

1. **Unit tests:** Update cascade tests to use AssessmentType
2. **Integration tests:** Verify backward compatibility
3. **E2E tests:** Ensure workflow still functions
4. **MCP tests:** Verify tool interfaces unchanged

---

## Files to Modify

### Core:
- `empirica/core/metacognitive_cascade/metacognitive_cascade.py` (MAJOR)
- `empirica/core/schemas/epistemic_assessment.py` (MINOR)

### Config:
- `empirica/config/mco/protocols.yaml` (MINOR)

### Tests:
- `tests/unit/cascade/*.py` (UPDATE)
- `tests/integration/test_complete_workflow.py` (UPDATE)

### CLI (if needed):
- `empirica/cli/command_handlers/cascade_commands.py` (CHECK)

---

## Estimated Effort

- **Phase 1 (Add new):** 2-3 hours
- **Phase 2 (Update internals):** 3-4 hours
- **Phase 3 (Deprecation):** 1-2 hours
- **Testing:** 2-3 hours

**Total:** ~10-12 hours of focused refactoring

---

## Risk Assessment

**Low Risk:**
- Additive changes (Phase 1)
- Backward compatible

**Medium Risk:**
- Internal refactoring (Phase 2)
- Test updates needed

**High Risk:**
- Breaking changes (Phase 4)
- User code may break

**Mitigation:**
- Phased approach with deprecation period
- Comprehensive testing
- Clear migration guide

---

## Next Steps

1. **Review this plan** - Confirm approach
2. **Start Phase 1** - Add AssessmentType, keep backward compatibility
3. **Update tests** - Ensure nothing breaks
4. **Document migration** - Guide for users

---

**Status:** Ready to begin refactoring
**Approach:** Hybrid (Option 3) with phased migration
**Priority:** Align code with documentation and philosophy
