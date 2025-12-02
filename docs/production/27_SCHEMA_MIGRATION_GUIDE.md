# 27. Schema Migration Guide

**Transition from OLD to NEW EpistemicAssessmentSchema**

---

## Migration Status

**Current Status**: 90% Complete ✅  
**Production Ready**: Yes (backwards compatible)  
**Tests**: 85 passing, 0 failures  
**Breaking Changes**: Zero (wrapper pattern maintains compatibility)

---

## Overview

Empirica is migrating from the OLD schema (`reflex_frame.py`) to the NEW schema (`epistemic_assessment.py`) with improved field naming and structure.

**Key Changes:**
1. Field names now use tier prefixes (`foundation_`, `comprehension_`, `execution_`)
2. Improved metadata structure
3. Better type safety and validation
4. Enhanced serialization

**Backwards Compatibility**: OLD field names still work via automatic conversion.

---

## Field Name Mapping

### Foundation Tier

| OLD Name | NEW Name | Description |
|----------|----------|-------------|
| `know` | `foundation_know` | Domain knowledge |
| `do` | `foundation_do` | Execution capability |
| `context` | `foundation_context` | Environmental awareness |

### Comprehension Tier

| OLD Name | NEW Name | Description |
|----------|----------|-------------|
| `clarity` | `comprehension_clarity` | Request clarity |
| `coherence` | `comprehension_coherence` | Logical coherence |
| `signal` | `comprehension_signal` | Signal vs noise |
| `density` | `comprehension_density` | Information density |

### Execution Tier

| OLD Name | NEW Name | Description |
|----------|----------|-------------|
| `state` | `execution_state` | Current state understanding |
| `change` | `execution_change` | Change tracking |
| `completion` | `execution_completion` | Path to completion |
| `impact` | `execution_impact` | Consequence prediction |

### Unchanged

| Name | Description |
|------|-------------|
| `engagement` | Collaborative intelligence (gate) |
| `uncertainty` | Meta-epistemic uncertainty |

---

## Usage Examples

### Using OLD Schema (Still Works)

```python
from empirica.core.canonical.reflex_frame import EpistemicAssessment, VectorState

# Create assessment with OLD field names
assessment = EpistemicAssessment(
    engagement=VectorState(0.75, "Good engagement"),
    know=VectorState(0.65, "Moderate knowledge"),
    do=VectorState(0.70, "Can execute"),
    context=VectorState(0.60, "Some context"),
    clarity=VectorState(0.85, "Clear request"),
    # ... other vectors
)

# Access with OLD names
print(f"Knowledge: {assessment.know.score}")
print(f"Clarity: {assessment.clarity.score}")
```

**Status**: ✅ Works (backwards compatible via wrappers)

---

### Using NEW Schema (Recommended)

```python
from empirica.core.schemas.epistemic_assessment import (
    EpistemicAssessmentSchema,
    VectorAssessment
)

# Create assessment with NEW field names
assessment = EpistemicAssessmentSchema(
    engagement=VectorAssessment(0.75, "Good engagement"),
    foundation_know=VectorAssessment(0.65, "Moderate knowledge"),
    foundation_do=VectorAssessment(0.70, "Can execute"),
    foundation_context=VectorAssessment(0.60, "Some context"),
    comprehension_clarity=VectorAssessment(0.85, "Clear request"),
    # ... other vectors
)

# Access with NEW names
print(f"Knowledge: {assessment.foundation_know.score}")
print(f"Clarity: {assessment.comprehension_clarity.score}")

# Calculate tier confidences
tier_confidences = assessment.calculate_tier_confidences()
print(f"Foundation: {tier_confidences['foundation']:.2f}")
print(f"Comprehension: {tier_confidences['comprehension']:.2f}")
print(f"Execution: {tier_confidences['execution']:.2f}")
```

**Status**: ✅ Recommended for new code

---

## Automatic Conversion

### OLD → NEW Conversion

```python
from empirica.core.schemas.assessment_converters import convert_old_to_new
from empirica.core.canonical.reflex_frame import EpistemicAssessment

# Create OLD assessment
old_assessment = EpistemicAssessment(...)

# Convert to NEW
new_assessment = convert_old_to_new(old_assessment)

# Now has NEW field names
print(new_assessment.foundation_know.score)
```

### NEW → OLD Conversion

```python
from empirica.core.schemas.assessment_converters import convert_new_to_old
from empirica.core.schemas.epistemic_assessment import EpistemicAssessmentSchema

# Create NEW assessment
new_assessment = EpistemicAssessmentSchema(...)

# Convert to OLD (for backwards compatibility)
old_assessment = convert_new_to_old(new_assessment)

# Now has OLD field names
print(old_assessment.know.score)
```

---

## Migration Phases

### Completed (90%)

1. ✅ **Phase 1: Converters** - Bidirectional conversion (21 tests)
2. ✅ **Phase 2: Assessor** - NEW schema parsing (14 tests)
3. ✅ **Phase 3: CASCADE** - Internal NEW schema usage (42 tests)
4. ✅ **Phase 4: PersonaHarness** - Prior blending with NEW schema
5. ✅ **Phase 5: CLI/MCP** - No changes needed (wrappers handle it)
6. ✅ **Phase 6: Test Mocks** - Optimized fixtures
7. ✅ **Phase 7: Documentation** - Core docs updated
8. ✅ **Phase 8: Integration Tests** - E2E verification (8 tests)
9. ⏳ **Phase 9: Cleanup** - OLD schema marked deprecated (in progress)

### Remaining (10%)

10. ⏳ **Phase 10: Final Validation** - Complete verification
11. ⏳ **Phase 11: Deprecation Removal** - Remove OLD schema (future)

---

## Transition Guidelines

### For New Code

**✅ Use NEW schema:**
```python
from empirica.core.schemas.epistemic_assessment import EpistemicAssessmentSchema
```

### For Existing Code

**✅ No changes required** - OLD schema still works:
```python
from empirica.core.canonical.reflex_frame import EpistemicAssessment
```

**Optional**: Migrate to NEW schema for better type safety and features.

### For API Consumers

**MCP Tools**: No changes needed - tools handle both schemas transparently.

**CLI Commands**: No changes needed - commands work with both schemas.

**Python API**: Choose OLD or NEW based on preference.

---

## Key Differences

### 1. Field Naming

**OLD**: Flat names (`know`, `clarity`, `state`)  
**NEW**: Tier-prefixed names (`foundation_know`, `comprehension_clarity`, `execution_state`)

**Benefit**: Clearer organization and semantic grouping.

### 2. Tier Confidence Calculation

**NEW schema only:**
```python
tier_confidences = assessment.calculate_tier_confidences()

print(tier_confidences)
# {
#     'foundation': 0.72,
#     'comprehension': 0.78,
#     'execution': 0.65
# }
```

**OLD schema**: No tier calculation method.

### 3. Action Determination

**NEW schema only:**
```python
action = assessment.determine_action()
# Returns: 'investigate' or 'proceed'
```

**OLD schema**: Action determined by CASCADE, not schema.

### 4. Metadata Structure

**NEW schema**: Enhanced metadata with timestamps, version info.  
**OLD schema**: Basic metadata.

---

## Common Patterns

### Pattern 1: Gradual Migration

```python
# Start with OLD
from empirica.core.canonical.reflex_frame import EpistemicAssessment

# Create assessment (OLD)
old_assessment = create_assessment_old()

# Convert to NEW for new features
from empirica.core.schemas.assessment_converters import convert_old_to_new
new_assessment = convert_old_to_new(old_assessment)

# Use NEW features
tier_confidences = new_assessment.calculate_tier_confidences()
```

### Pattern 2: Wrapper Pattern

```python
# Internal implementation uses NEW
def _assess_internal() -> EpistemicAssessmentSchema:
    # Use NEW schema internally
    return EpistemicAssessmentSchema(...)

# Public API returns OLD for backwards compat
def assess() -> EpistemicAssessment:
    new_assessment = _assess_internal()
    return convert_new_to_old(new_assessment)
```

### Pattern 3: Full Migration

```python
# Replace all imports
# OLD:
# from empirica.core.canonical.reflex_frame import EpistemicAssessment

# NEW:
from empirica.core.schemas.epistemic_assessment import EpistemicAssessmentSchema

# Update field names
# OLD: assessment.know.score
# NEW: assessment.foundation_know.score

# Use new features
tier_confidences = assessment.calculate_tier_confidences()
action = assessment.determine_action()
```

---

## Testing

### Both Schemas Tested

```bash
# Run all tests
pytest tests/unit/

# Converter tests (21 tests)
pytest tests/unit/schemas/test_assessment_converters.py

# NEW schema tests (14 tests)
pytest tests/unit/canonical/test_assessor_new_schema.py

# CASCADE tests (42 tests - use both schemas)
pytest tests/unit/cascade/
```

**Current Status**: 85 tests passing, 0 failures ✅

---

## Deprecation Timeline

### Current (v2.0)

- ✅ NEW schema fully implemented
- ✅ OLD schema marked deprecated
- ✅ Both schemas work (backwards compatible)
- ✅ Converters available

### Future (v2.1+)

- ⏳ OLD schema removal planned
- ⏳ Wrappers removed
- ⏳ NEW schema becomes only schema

**Recommendation**: Migrate to NEW schema when convenient, but no urgency.

---

## FAQ

### Q: Do I need to update my code?

**A**: No, OLD schema still works. Update when convenient.

### Q: What if I use MCP tools?

**A**: No changes needed - tools handle both schemas.

### Q: Performance impact?

**A**: Negligible - converters are lightweight.

### Q: Can I mix OLD and NEW?

**A**: Yes, converters allow seamless mixing.

### Q: When will OLD schema be removed?

**A**: Not scheduled yet - will provide advance notice.

---

## Next Reading

- **Epistemic Vectors**: [05_EPISTEMIC_VECTORS.md](file:///home/yogapad/empirical-ai/empirica/docs/production/05_EPISTEMIC_VECTORS.md)
- **Python API**: [13_PYTHON_API.md](file:///home/yogapad/empirical-ai/empirica/docs/production/13_PYTHON_API.md)
- **CASCADE Flow**: [06_CASCADE_FLOW.md](file:///home/yogapad/empirical-ai/empirica/docs/production/06_CASCADE_FLOW.md)

---

**Schema Migration - Smooth, Backwards Compatible, Production Ready** ✅
