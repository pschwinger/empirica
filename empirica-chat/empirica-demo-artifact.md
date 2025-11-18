# Empirica CASCADE Demo: Real Workflow Example

## Task: "Review this authentication code for security issues"

---

## 📋 PHASE 1: PREFLIGHT (Assess Before Starting)

**Time: 2 minutes**

### You assess your epistemic state:

```json
{
  "task": "Security review of authentication module",
  "vectors": {
    "know": {
      "score": 0.4,
      "rationale": "Familiar with auth concepts (OAuth, JWT), but don't know this codebase's architecture or implementation patterns",
      "evidence": "First time seeing this repo, no prior context on team conventions"
    },
    "do": {
      "score": 0.7,
      "rationale": "Can review code systematically and identify common vulnerabilities, but might miss codebase-specific issues",
      "evidence": "Done 5+ security reviews, but always on systems I understood"
    },
    "context": {
      "score": 0.2,
      "rationale": "Very little context - don't have architecture docs, deployment info, threat model",
      "evidence": "Only given the code file, no supporting documentation"
    },
    "uncertainty": {
      "score": 0.8,
      "rationale": "Pretty uncertain about my own assessment - this is a new codebase and I don't know what I don't know",
      "evidence": "Multiple knowledge gaps identified above"
    }
  },
  "summary": "Ready to start, but expect to learn a lot. Low confidence right now, but that's honest."
}
```

**Key insight:** High uncertainty here is GOOD. It means you're being realistic.

---

## 🔍 PHASE 2: INVESTIGATE (Fill Knowledge Gaps)

**Time: Variable - 30 minutes in this example**

### You investigate systematically:

```
Found: Architecture documentation (found in /docs/)
  → CONTEXT increases: 0.2 → 0.4
  → Better understanding of auth flow
  
Found: Existing security audit from 6 months ago
  → CONTEXT increases: 0.4 → 0.6
  → Know what was already checked
  → KNOW increases: 0.4 → 0.5 (understand implementation philosophy)
  
Found: Threat model document (in /docs/THREAT_MODEL.md)
  → CONTEXT increases: 0.6 → 0.8
  → Now understand what IS in scope vs. out of scope
  
Found: Code comments explaining key decisions
  → KNOW increases: 0.5 → 0.7 (understand why implemented this way)
  → UNCERTAINTY decreases: 0.8 → 0.4 (much more confident in assessment now)
```

**Evidence trail:**
- ✅ Read architecture docs (20 min)
- ✅ Reviewed previous audit findings (5 min)
- ✅ Understood threat model (10 min)
- ✅ Studied implementation patterns (15 min)
- ✅ Asked clarifying questions (5 min)

**Your updated state:**
```json
{
  "know": 0.7,
  "do": 0.8,
  "context": 0.8,
  "uncertainty": 0.4
}
```

---

## ✅ PHASE 3: CHECK (Ready to Act?)

**Time: 2 minutes**

### You assess readiness:

```
Questions to answer:
✓ Do I understand the auth flow? YES
✓ Do I know the threat model? YES
✓ Are there critical unknowns? Minor edge cases, but acceptable
✓ Can I do a thorough review now? YES

Confidence to proceed: 0.8 (80%)

Decision: PROCEED WITH REVIEW
```

**Why 0.8 and not 1.0?**
- Some edge cases still unclear (acceptable risk)
- New codebase = might miss subtle patterns (normal)
- But investigation was systematic enough (ready to act)

---

## 🎯 PHASE 4: ACT (Execute the Work)

**Time: 60 minutes - actual security review**

You perform thorough review:
- ✅ Check session handling (found: potential issue #1)
- ✅ Review cryptographic usage (found: best practices followed)
- ✅ Analyze access control (found: solid implementation)
- ✅ Test error handling (found: potential issue #2)
- ✅ Review external dependencies (no vulnerabilities)

**Findings documented:**
1. Session invalidation on logout could race condition (medium risk)
2. Error messages might leak user existence (low risk)
3. Solid implementation overall (positive)

---

## 🔄 PHASE 5: POSTFLIGHT (Reflect on Learning)

**Time: 3 minutes**

### You reassess and compare:

```json
{
  "preflight": {
    "know": 0.4,
    "do": 0.7,
    "context": 0.2,
    "uncertainty": 0.8
  },
  "postflight": {
    "know": 0.85,
    "do": 0.9,
    "context": 0.85,
    "uncertainty": 0.2
  },
  "learning_delta": {
    "know": "+0.45 (big - learned implementation details)",
    "do": "+0.2 (more confident in review methodology)",
    "context": "+0.65 (now understand full architecture)",
    "uncertainty": "-0.6 (much more certain now)"
  },
  "calibration_analysis": {
    "was_initial_assessment_accurate": "YES",
    "initial_confidence": 0.2,
    "actual_confidence": 0.85,
    "pattern": "Well-calibrated - initial low confidence was appropriate"
  },
  "unexpected_learnings": [
    "Architecture is more elegant than expected",
    "Team has strong security practices overall",
    "Only minor issues found despite starting uncertain"
  ],
  "reflection": "Started very uncertain, investigation validated that uncertainty. Learned quickly once I focused on the right areas. Initial CHECK assessment (0.8 confidence) was exactly right - enough knowledge to proceed, but learning happened during review."
}
```

---

## 📊 The Calibration Story

### What This Shows:

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| KNOW | 0.4 | 0.85 | +0.45 ✅ |
| DO | 0.7 | 0.9 | +0.2 ✅ |
| CONTEXT | 0.2 | 0.85 | +0.65 ✅ |
| UNCERTAINTY | 0.8 | 0.2 | -0.6 ✅ |

### Interpretation:

✅ **Well-calibrated:** Initial assessment was honest (low confidence was appropriate)
✅ **Systematic learning:** Each phase built knowledge (investigation worked)
✅ **Realistic growth:** +0.45 KNOW is substantial but not overconfident
✅ **Evidence-based:** Uncertainty dropped because you had answers

---

## Why This Matters

**Without Empirica:**
- "I reviewed the code and found 2 issues"
- No measurement of learning
- No calibration validation
- No systematic investigation trail

**With Empirica:**
- Documented epistemology: "I was uncertain, investigated, became confident"
- Measurable learning: "+0.45 KNOW, -0.6 UNCERTAINTY"
- Calibration check: "Initial assessment was accurate"
- Systematic methodology: "Here's exactly how I filled knowledge gaps"
- Future improvement: "Next security review, I can be faster because KNOW is higher"

---

## The Cascade in Action

```
START: "I don't know much about this code"
      ↓
PREFLIGHT: Honestly assess gaps (KNOW=0.4, CONTEXT=0.2)
      ↓
INVESTIGATE: Systematically fill gaps (read docs, trace code)
      ↓
CHECK: "Am I ready?" YES (confidence=0.8)
      ↓
ACT: Do thorough review (find issues, validate strengths)
      ↓
POSTFLIGHT: Measure learning (KNOW went 0.4→0.85, learned +0.45)
      ↓
RESULT: Not just "I found issues" but "Here's what I learned and how certain I am"
```

---

## Try This In Your Next Task

1. **PREFLIGHT** - Rate KNOW, DO, CONTEXT, UNCERTAINTY honestly (2 min)
2. **INVESTIGATE** - If gaps exist, fill them systematically (varies)
3. **CHECK** - Am I ready? (1 min)
4. **ACT** - Do the work (your normal time)
5. **POSTFLIGHT** - Compare to preflight, measure learning (3 min)

**Total overhead:** ~5 minutes per task
**Value:** Measurable learning + calibration improvement

---

## Key Principles

**NO HEURISTICS** - Your scores should be honest, not optimistic
**HIGH UNCERTAINTY IS VALID** - "I'm very uncertain" = 0.7-0.9 score (that's data!)
**MEASURE LEARNING** - PREFLIGHT→POSTFLIGHT comparison shows real growth
**CALIBRATION MATTERS** - Over time, your predictions get more accurate

**When in doubt, be uncertain. That's genuine metacognition.** ✨
