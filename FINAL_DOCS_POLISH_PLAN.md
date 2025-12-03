# Final Documentation Polish Plan

**Remaining work:** Minor improvements for completeness
**Effort:** ~10 iterations

---

## Task 1: Add Minimal Goal/Git References (Low Priority)

### Docs without goal/git mentions:
These could benefit from a one-liner reference, but it's not critical:
- Check which production docs truly need it
- Add only where relevant (workflow, coordination docs)

**Approach:** Add footer note:
```markdown
---
**Note:** Empirica stores goals (with vectorial scope) and checkpoints in git notes for automatic cross-AI coordination and session continuity. See [Storage Architecture](../architecture/STORAGE_ARCHITECTURE_COMPLETE.md).
```

**Estimated:** 2-3 iterations

---

## Task 2: Clarify Threshold Language (Medium Priority)

### Pattern to find and fix:
```
❌ "MUST exceed 0.7"
❌ "REQUIRED: KNOW ≥ 0.6"
❌ "IF UNCERTAINTY > 0.5 THEN investigate"

✅ "Guidance: Consider investigating if UNCERTAINTY > 0.5 (configurable via thresholds.yaml)"
✅ "Typical threshold: 0.7 (adjustable by Sentinel/advanced users based on domain)"
✅ "AI self-assesses readiness; threshold provides guidance, not enforcement"
```

### Files to check:
- production/07_INVESTIGATION_SYSTEM.md (likely has guidance language)
- production/08_BAYESIAN_GUARDIAN.md (drift thresholds)
- production/16_TUNING_THRESHOLDS.md (should explain configurability)
- production/28_DECISION_LOGIC.md (decision thresholds)

**Approach:** Add context about configurability
**Estimated:** 3-5 iterations

---

## Task 3: Code Audit (Preparation for Step 3)

### Files to audit for refactoring:
1. `empirica/core/metacognitive_cascade/metacognitive_cascade.py`
   - Check for explicit phase tracking (CascadePhase enum)
   - Check for _enter_phase() calls
   - Check for phase state machine logic

2. `empirica/core/schemas/epistemic_assessment.py`
   - Check CascadePhase enum
   - Should be AssessmentType(PRE/CHECK/POST)

3. `empirica/config/mco/protocols.yaml`
   - Check phase enum
   - Update to assessment types

**Estimated:** 2-3 iterations

---

## Recommended Execution

### Priority 1: Code Audit (Most Important)
- Understand what needs refactoring
- Create refactoring plan for Step 3

### Priority 2: Threshold Language
- Fix most egregious "MUST" language
- Add configurability notes

### Priority 3: Minimal References (Optional)
- Only if time permits
- Low value-add (docs already comprehensive)

---

## Expected Outcome

After this polish:
- ✅ Documentation: 100% aligned and comprehensive
- ✅ Thresholds: Clarified as configurable guidance
- ✅ Code audit: Clear refactoring plan for Step 3
- ✅ Professional: Production-ready documentation

---

**Estimated total:** 7-10 iterations
**Tokens available:** ~52K (plenty!)
