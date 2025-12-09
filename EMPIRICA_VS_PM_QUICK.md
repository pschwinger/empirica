# Empirica vs. PM Tools - Quick Reference

**TL;DR:** PM tools track WORK. Empirica tracks WHAT YOU KNOW ABOUT WORK.

---

## The 30-Second Explanation

**JIRA says:** "Task complete ✅"

**Empirica says:** "I was 65% confident, now 90%. Here's WHY my confidence changed, here's what I learned, here's what I STILL don't know, and here's whether you should trust my assessment (calibration: well-calibrated)."

**When next AI picks up the work:**
- **JIRA:** "Continue task XYZ" (starts from zero)
- **Empirica:** "You inherit 90% knowledge + 3 explicit unknowns + calibration history" (starts from AI-1's endpoint)

---

## The Five Things PM Tools Can't Do

| # | Feature | PM Tools | Empirica |
|---|---------|----------|----------|
| 1 | **Calibration Detection** | ❌ Can't measure over/underconfidence | ✅ Automatic (PREFLIGHT vs POSTFLIGHT) |
| 2 | **Epistemic Deltas** | ❌ "Task done" (binary) | ✅ "KNOW +0.25, STATE +0.55" (semantic) |
| 3 | **Explicit Unknowns** | ❌ "Blockers: X" | ✅ "Unknown: X (type: approach_uncertainty, needs investigation)" |
| 4 | **Investigation Tracking** | ❌ Can't distinguish phases | ✅ Investigation generates knowledge, execution consumes it |
| 5 | **Knowledge Inheritance** | ❌ "Reassign to Bob" | ✅ "Bob inherits 90% baseline + 3 unknowns + calibration" |

---

## The Killer Example

### Scenario: AI-1 Documents API

#### PM Tool View (Both Cases Identical)
```
Status: Done ✅
Comment: "All endpoints documented"
```

#### Empirica Case 1: Overconfident AI
```
Calibration: OVERCONFIDENT ⚠️
PREFLIGHT: uncertainty=0.20 (thought easy)
POSTFLIGHT: uncertainty=0.50 (realized complex)
Handoff: "Don't trust completeness, re-investigate"
```

#### Empirica Case 2: Well-Calibrated AI
```
Calibration: WELL_CALIBRATED ✅
PREFLIGHT: uncertainty=0.45 (knew complex)
POSTFLIGHT: uncertainty=0.15 (figured it out)
Handoff: "Trust this assessment, 17 endpoints covered"
```

**PM tools can't encode: "Task is done but don't trust it."**

**Empirica does it automatically via calibration.**

---

## Counter-Arguments

**"You could add confidence fields to JIRA"**
→ You can't automatically detect overconfidence without PREFLIGHT→POSTFLIGHT comparison

**"Developers could write detailed comments"**
→ Comments are unstructured, don't enable automatic calibration, don't support epistemic transfer

**"This is just metadata"**
→ Can your metadata answer: "Was previous AI overconfident? What did they learn? Should I trust them?"

---

## The Empirical Test

Challenge skeptics to show PM tool doing this:

```bash
# AI-1
empirica preflight "Task X"  # confidence=0.65
empirica postflight          # confidence=0.90, calibration=well_calibrated

# AI-2
empirica handoff-query       # Inherits 0.90 baseline + 3 unknowns
empirica preflight "Continue" # Starts at 0.90, not 0.00

# System
if ai2.confidence < ai1.confidence - 0.2:
    flag "CALIBRATION_DIVERGENCE - investigate discrepancy"
```

**PM tools can't do this.**

---

## The Bottom Line

| PM Tools | Empirica |
|----------|----------|
| Track tasks | Track knowledge |
| Measure velocity | Measure calibration |
| Optimize throughput | Optimize learning quality |
| Answer: "What's done?" | Answer: "What do you know?" |

**Completely different ontology.**

Not "JIRA with extra fields."

**A system for measuring what AIs know about what they're doing.**

That's functional self-awareness.
