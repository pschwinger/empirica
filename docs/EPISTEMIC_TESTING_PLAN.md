# Epistemic Checking Validation Plan

## Overview

Test the proactive epistemic checking system to validate:
1. Hallucination detection accuracy
2. Self-correction appropriateness
3. Evidence grounding effectiveness
4. External peer review validation

---

## Phase 1: Evidence Base Accumulation (Sessions 1-5)

### Session 1: CLI Verbose Flag Fix
**Task:** Fix --verbose flag inconsistency (existing plan)

**CASCADE Workflow:**
```bash
# PREFLIGHT
echo '{
  "session_id": "<ID>",
  "phase": "PREFLIGHT",
  "vectors": {
    "engagement": 0.8,
    "know": 0.6,
    "do": 0.7,
    "context": 0.8,
    "clarity": 0.9,
    "coherence": 0.8,
    "signal": 0.7,
    "density": 0.6,
    "state": 0.8,
    "change": 0.2,
    "completion": 0.0,
    "impact": 0.4,
    "uncertainty": 0.3
  },
  "reasoning": "Clear task (add --verbose to 40 commands), know existing codebase structure, low uncertainty about approach. Low impact (quality of life improvement). Starting from scratch (completion=0.0)."
}' | empirica preflight-submit -

# WORK
# Log findings as you discover them:
empirica finding-log --finding "Verbose flag pattern: parser.add_argument('--verbose', action='store_true')"
empirica finding-log --finding "Handlers check with: verbose = getattr(args, 'verbose', False)"
empirica unknown-log --unknown "Should verbose output go to stdout or stderr?"

# CHECK (before implementing)
empirica check-submit -

# POSTFLIGHT
empirica postflight-submit -
```

**Expected findings:** 10-15 (CLI patterns, handler structure, testing approach)

---

### Session 2: Proactive Epistemic Checking Tool
**Task:** Build the automated epistemic checker

**What to build:**
```python
# empirica/tools/epistemic_checker.py

def check_document(document_path, evidence_base=None):
    """
    Proactive epistemic checking on document

    Returns:
    - claims: List of empirical claims found
    - assessments: Epistemic state for each claim
    - flagged: Claims that need revision
    - report: Markdown verification report
    """
    pass

def extract_empirical_claims(text):
    """Find quantitative/causal/comparative claims"""
    pass

def assess_claim(claim, evidence_base):
    """
    Assess epistemic state:
    - know: 0.0-1.0
    - uncertainty: 0.0-1.0
    - evidence: List of supporting findings
    """
    pass
```

**CASCADE Workflow:**
- PREFLIGHT: know=0.5 (theory clear, implementation uncertain)
- Log findings about claim patterns, assessment heuristics
- CHECK: before finalizing algorithm
- POSTFLIGHT: measure learning delta

**Expected findings:** 15-20 (claim extraction patterns, assessment logic, testing results)

---

### Session 3: Test on Academic Paper Corpus
**Task:** Run checker on sample papers, measure detection

**Test corpus:**
```
papers/
├── verified/
│   ├── paper1.pdf (known good - no hallucinations)
│   ├── paper2.pdf (known good)
│   └── paper3.pdf (known good)
└── flawed/
    ├── paper4.pdf (known hallucinations - retracted)
    ├── paper5.pdf (unverified claims)
    └── paper6.pdf (our original paper draft!)
```

**Metrics to measure:**
```python
# True positives: Correctly flagged hallucinations
# False positives: Flagged valid claims
# True negatives: Didn't flag valid claims
# False negatives: Missed hallucinations

precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1_score = 2 * (precision * recall) / (precision + recall)
```

**CASCADE Workflow:**
- PREFLIGHT: know=0.4 (tool built but untested)
- Log findings: detection patterns, common false positives
- Unknown: What's the right uncertainty threshold?
- CHECK: Do we have enough test cases?
- POSTFLIGHT: Measured performance

**Expected findings:** 15-20 (detection accuracy, failure modes, threshold tuning)

---

### Session 4: Hallucination Detection Validation
**Task:** Controlled test with known hallucinations

**Test setup:**
1. Create 50 claims (25 grounded, 25 hallucinated)
2. Run epistemic checker
3. Measure detection accuracy

**Example test cases:**
```json
{
  "claim": "88% hallucination reduction measured",
  "ground_truth": "hallucination",
  "expected_assessment": {
    "know": 0.1,
    "uncertainty": 0.9,
    "evidence": null
  }
},
{
  "claim": "Perpetual continuity demonstrated across memory compact",
  "ground_truth": "verified",
  "expected_assessment": {
    "know": 0.95,
    "uncertainty": 0.1,
    "evidence": ["Finding #XX: Pre-summary snapshot loaded"]
  }
}
```

**CASCADE Workflow:**
- PREFLIGHT: know=0.6 (tool tested, validation uncertain)
- Log findings: accuracy metrics, calibration results
- Dead ends: Approaches that didn't improve detection
- CHECK: Is accuracy sufficient for publication?
- POSTFLIGHT: Confidence in system

**Expected findings:** 10-15 (accuracy results, calibration insights)

---

### Session 5: Write Validation Report
**Task:** Document results with evidence from prior sessions

**This is the critical test:**
- Write empirical claims about detection accuracy
- Run proactive checker on own report
- **Should reference logged findings from Sessions 1-4**
- Example: "Detection accuracy 85% (Finding #47, Session 4)"

**CASCADE Workflow:**
- PREFLIGHT: know=0.8 (rich evidence base accumulated)
- Log findings: Final validation results
- CHECK: Are all claims grounded in evidence?
- POSTFLIGHT: Completion=0.95 (validation complete)

**Expected findings:** 5-10 (validation conclusions)

**Total accumulated:** 55-80 findings across 5 sessions

---

## Phase 2: Proactive Checking With Evidence Base

### Demonstration: Before vs After

**Before (Session 1 - No Evidence Base):**
```
Write: "The --verbose flag improves debugging efficiency by 50%"

Proactive check:
- Claim: "50% improvement"
- Assessment: know=0.2, uncertainty=0.8, evidence=none
- Flag: HALLUCINATION (no supporting data)

Self-correction: Remove claim (no evidence to support it)
```

**After (Session 5 - Rich Evidence Base):**
```
Write: "Detection accuracy was 85% across 50 test cases"

Proactive check:
- Claim: "85% accuracy"
- Assessment: know=0.9, uncertainty=0.15
- Evidence: Finding #47 (Session 4): "Measured 42.5/50 correct = 85%"
- Status: VERIFIED

No correction needed (grounded in logged findings)
```

**Key difference:** With evidence base, claims can be grounded in logged findings rather than just flagged.

---

## Phase 3: External Validation (Peer Review Simulation)

### Setup: Epistemic Audit Trail

**For each correction, log:**
```json
{
  "claim": "88% hallucination reduction",
  "original_location": "line 455",
  "epistemic_assessment": {
    "know": 0.1,
    "uncertainty": 0.9,
    "evidence": null,
    "reasoning": "No testing performed, pattern-matched from theory"
  },
  "correction_applied": {
    "action": "moved_to_theoretical_predictions",
    "new_location": "section 6.3.1",
    "marked_as": "Predicted (needs empirical testing)"
  },
  "reviewer_validation": {
    "assessor": "external_reviewer",
    "agrees_with_assessment": true/false,
    "agrees_with_correction": true/false,
    "notes": "..."
  }
}
```

### External Reviewer Questions

**For each flagged claim, reviewer validates:**

1. **Was uncertainty assessment accurate?**
   - AI said: uncertainty=0.9
   - Evidence: None logged, no testing performed
   - Reviewer: "Yes, 0.9 is appropriate given no data"

2. **Was correction appropriate?**
   - AI action: Moved to "Theoretical Predictions" section
   - Alternative: Remove entirely
   - Reviewer: "Yes, marking as theoretical is appropriate"

3. **Would human expert flag this?**
   - Claim: "88% reduction"
   - Human expert: "Yes, would require citation or data"
   - Reviewer: "AI assessment aligned with expert judgment"

### Validation Metrics

```python
# Inter-rater reliability: AI vs Human Expert
agreement_rate = (AI_flags ∩ Human_flags) / (AI_flags ∪ Human_flags)

# Correction quality: Were AI's revisions appropriate?
correction_quality = Appropriate_corrections / Total_corrections

# Calibration: Is AI's uncertainty well-calibrated?
# Plot: AI's uncertainty vs Human's uncertainty for same claims
calibration_plot(ai_uncertainty, human_uncertainty)
```

---

## Phase 4: Controlled Experiments

### Experiment 1: Hallucination Detection Rate

**Hypothesis:** Proactive epistemic checking detects 70-90% of hallucinations

**Method:**
1. Create corpus of 100 claims (50 verified, 50 hallucinated)
2. Run epistemic checker
3. Measure precision, recall, F1

**Success criteria:**
- Precision > 0.8 (few false positives)
- Recall > 0.7 (catches most hallucinations)
- F1 > 0.75

---

### Experiment 2: Evidence Base Effect

**Hypothesis:** Richer evidence base improves grounding quality

**Method:**
1. Test proactive checking after Session 1 (10 findings)
2. Test proactive checking after Session 5 (60 findings)
3. Compare grounding quality:
   - Can claims reference evidence?
   - Are assessments more confident?
   - Fewer "no evidence" flags?

**Success criteria:**
- 50%+ claims in Session 5 can reference logged findings
- Average uncertainty decreases (more grounded)
- Fewer hallucinations generated (query evidence first)

---

### Experiment 3: Multi-Session Continuity

**Hypothesis:** Epistemic continuity maintains across memory compacts

**Method:**
1. Work on complex task across 3 sessions with compacts
2. Measure epistemic state preservation:
   - Are findings accessible after compact?
   - Does knowledge persist? (know vector)
   - Can resume work without reconstruction?

**Success criteria:**
- 100% finding retrieval after compact
- Knowledge vector preserved (±0.1)
- Zero manual context reconstruction needed

---

## Implementation: Testing Infrastructure

### 1. Test Corpus Creation

```bash
# Directory structure
empirica/tests/epistemic_checking/
├── corpus/
│   ├── verified_claims.json
│   ├── hallucinated_claims.json
│   └── papers/
│       ├── verified/
│       └── flawed/
├── test_proactive_checking.py
├── test_evidence_grounding.py
└── test_continuity.py
```

### 2. Automated Testing

```python
# test_proactive_checking.py

def test_hallucination_detection():
    """Test detection of known hallucinations"""
    corpus = load_test_corpus()

    results = {
        'true_positives': 0,
        'false_positives': 0,
        'true_negatives': 0,
        'false_negatives': 0
    }

    for claim in corpus:
        assessment = epistemic_checker.assess_claim(claim.text)

        # Hallucination if: uncertainty > 0.5 OR evidence is None
        flagged_as_hallucination = (
            assessment['uncertainty'] > 0.5 or
            assessment['evidence'] is None
        )

        # Compare to ground truth
        if claim.is_hallucination and flagged_as_hallucination:
            results['true_positives'] += 1
        elif claim.is_hallucination and not flagged_as_hallucination:
            results['false_negatives'] += 1
        elif not claim.is_hallucination and flagged_as_hallucination:
            results['false_positives'] += 1
        else:
            results['true_negatives'] += 1

    # Calculate metrics
    precision = results['true_positives'] / (
        results['true_positives'] + results['false_positives']
    )
    recall = results['true_positives'] / (
        results['true_positives'] + results['false_negatives']
    )
    f1 = 2 * precision * recall / (precision + recall)

    assert f1 > 0.75, f"F1 score {f1} below threshold 0.75"
```

---

## Success Criteria

### Minimum Viable Validation

**✅ Phase 1 Complete:**
- 50+ findings logged across 5 sessions
- Full CASCADE workflow followed
- Evidence base queryable

**✅ Phase 2 Complete:**
- Proactive checking tool built
- Tested on own outputs
- Can reference evidence base

**✅ Phase 3 Complete:**
- External reviewer validates epistemic assessments
- Agreement rate > 0.8
- Corrections judged appropriate

**✅ Phase 4 Complete:**
- Hallucination detection F1 > 0.75
- Evidence grounding improves with more sessions
- Continuity preserved across compacts

---

## Timeline

**Session 1 (Today):** Fix --verbose flags, establish workflow pattern
**Session 2 (Next):** Build epistemic checker tool
**Session 3:** Test on paper corpus
**Session 4:** Controlled validation experiments
**Session 5:** Write validation report with evidence

**Total time:** 5 sessions × 2-4 hours = 10-20 hours of work

**Outcome:** Empirically validated epistemic checking system with peer-reviewable audit trail

---

## Next Steps (Immediate)

1. **Start Session 1:** Fix --verbose flags with full CASCADE workflow
2. **Log all findings:** Establish evidence base systematically
3. **Test continuity:** Force memory compact, verify restoration
4. **Build momentum:** Each session adds to evidence, improves grounding

**Ready to start Session 1 with proper CASCADE workflow?**
