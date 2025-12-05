# Validation Logic - What Gets Checked and Why

**Version:** 3.0 (Phase 3)  
**Status:** Production Ready  
**Purpose:** Explain validation checks and failure patterns

---

## Overview

Three validators ensure epistemic coherence across multi-AI sessions:

1. **CoherenceValidator** - Self-check before handoff
2. **HandoffValidator** - Verify incoming work
3. **EpistemicRehydration** - Calibrate from context

Each validator performs specific checks to detect common failure modes.

---

## CoherenceValidator - Self-Validation Logic

### Purpose
**"Before I hand off, did I do my work honestly?"**

Validates that current AI's work is coherent before creating checkpoint.

---

### Check 1: Scope Match

**What:** Did I do what I planned?

**How:** Compares git diff statistics against preflight plan's scope estimate.

**Thresholds:**
```python
scope_estimate = preflight_plan.get("scope_estimate", "medium")

# Line change thresholds
SCOPE_THRESHOLDS = {
    "small": (0, 100),      # 0-100 lines changed
    "medium": (50, 500),    # 50-500 lines changed
    "large": (200, 2000),   # 200-2000 lines changed
    "extra_large": (1000, 10000)  # 1000+ lines changed
}
```

**Passes If:**
- Planned "small", changed 75 lines ✓
- Planned "medium", changed 300 lines ✓
- Planned "large", changed 1200 lines ✓

**Fails If:**
- Planned "small", changed 500 lines ✗ (scope creep)
- Planned "medium", changed 10 lines ✗ (scope underdelivery)
- Planned "large", changed 50 lines ✗ (mismatch)

**Why This Matters:**
Detects unintended scope creep or scope drift. If you planned "small refactor" but changed 2000 lines, something went wrong.

---

### Check 2: Epistemic Trajectory

**What:** Is my learning trajectory coherent?

**How:** Analyzes PREFLIGHT → POSTFLIGHT vector changes to detect patterns.

**Recognized Patterns:**

#### LEARNING Pattern (✓ Coherent)
```
KNOW: ↑ (increased)
CLARITY: ↑ (increased)
UNCERTAINTY: ↓ (decreased)
```
**Interpretation:** Successfully learned through investigation.

#### COMPLEXITY Pattern (✓ Coherent)
```
KNOW: ↓ (decreased - realized don't know)
CLARITY: ↓ (decreased - found complexity)
UNCERTAINTY: ↑ (increased - honest about gaps)
```
**Interpretation:** Discovered hidden complexity, honest assessment.

#### STAGNATION Pattern (✗ Incoherent)
```
All vectors: ~same (±0.05)
```
**Interpretation:** No meaningful change - did work actually happen?

#### OVERCONFIDENCE Pattern (✗ Incoherent)
```
KNOW: ↑↑ (big increase)
UNCERTAINTY: ↑ (also increased!)
```
**Interpretation:** Contradictory - if you learned, uncertainty should decrease.

**Thresholds:**
```python
SIGNIFICANT_CHANGE = 0.10  # 0.10 or greater is meaningful
STAGNATION_THRESHOLD = 0.05  # All changes <0.05 = stagnant

# Pattern detection
if know_delta > 0.10 and clarity_delta > 0.10 and uncertainty_delta < -0.10:
    pattern = "LEARNING"
elif know_delta < -0.10 and clarity_delta < -0.10 and uncertainty_delta > 0.10:
    pattern = "COMPLEXITY"
elif all_deltas_below_threshold(0.05):
    pattern = "STAGNATION"  # Warning!
```

**Why This Matters:**
Detects epistemically incoherent assessments. If your knowledge increased but uncertainty also increased, you're contradicting yourself.

---

### Check 3: Findings Honesty

**What:** Are my findings appropriately confident given my knowledge?

**How:** Compares finding certainty against POSTFLIGHT know/clarity vectors.

**Rules:**
```python
# Rule 1: High certainty findings need high knowledge
if finding['certainty'] > 0.85 and postflight_know < 0.70:
    concern = "High certainty finding but low knowledge"

# Rule 2: Average finding certainty shouldn't exceed knowledge
avg_finding_certainty = mean([f['certainty'] for f in findings])
if avg_finding_certainty > postflight_know + 0.15:
    concern = "Findings more certain than knowledge supports"

# Rule 3: Many findings with low clarity is suspicious
if len(findings) > 5 and postflight_clarity < 0.60:
    concern = "Many findings but low clarity - overstating?"
```

**Passes If:**
```python
# Coherent: Knowledge supports certainty
postflight_know = 0.85
finding_certainty = 0.80  # ✓ Supported

postflight_know = 0.70
avg_finding_certainty = 0.65  # ✓ Conservative
```

**Fails If:**
```python
# Overconfident: Findings too certain
postflight_know = 0.55
finding_certainty = 0.95  # ✗ Unjustified

# Too many findings for low clarity
postflight_clarity = 0.50
num_findings = 12  # ✗ Suspicious volume
```

**Why This Matters:**
Prevents AI from overstating findings. If you have low knowledge but claim high-certainty findings, you're likely guessing.

---

### Recommendation Logic

Based on check results, validator recommends action:

```python
if all_checks_pass:
    recommendation = "handoff_ok"
    message = "✅ Coherence check PASSED. Ready to hand off."

elif trajectory_failed:
    recommendation = "reassess"
    message = "⚠️ Epistemic trajectory incoherent. Re-run POSTFLIGHT assessment."

elif scope_failed or findings_dishonest:
    recommendation = "reenter_check"
    message = "⚠️ Scope/findings concerns. Re-enter CHECK phase for validation."
```

---

## HandoffValidator - Incoming Work Validation

### Purpose
**"Before I trust their work, does it make sense?"**

Validates checkpoint quality before trusting previous AI's work.

---

### Check 1: Claim vs Reality

**What:** Did they do what they claimed?

**How:** Compares checkpoint description against git diff statistics.

**Rules:**
```python
# Rule 1: If they claim work but no git changes
if checkpoint_describes_work and git_lines_changed < 10:
    issue = "Claims work completed but minimal/no code changes"

# Rule 2: If major changes but minimal checkpoint description
if git_lines_changed > 500 and len(checkpoint_description) < 50:
    issue = "Major changes but minimal checkpoint documentation"

# Rule 3: Checkpoint phase mismatch
if checkpoint_phase == "POSTFLIGHT" and completion_vector < 0.50:
    issue = "POSTFLIGHT but low completion - work unfinished?"
```

**Passes If:**
```python
# Coherent claims
checkpoint = "Refactored auth module (300 lines)"
git_diff = 287 lines changed  # ✓ Matches

checkpoint = "Investigated database options, no code changes"
git_diff = 0 lines changed  # ✓ Matches
```

**Fails If:**
```python
# Mismatch: Claims vs reality
checkpoint = "Completed full authentication system"
git_diff = 15 lines changed  # ✗ Exaggerated claim

checkpoint = "Minor fix"
git_diff = 2500 lines changed  # ✗ Understated work
```

**Why This Matters:**
Detects when AI overstates or understates work. If checkpoint claims "completed" but git shows 10 lines changed, something's wrong.

---

### Check 2: Findings Credibility

**What:** Do findings make sense given their assessment?

**How:** Validates findings against POSTFLIGHT vectors.

**Rules:**
```python
# Rule 1: High certainty needs high knowledge
for finding in findings:
    if finding['certainty'] > 0.85 and postflight_know < 0.70:
        issue = f"Finding '{finding['key']}' has high certainty but AI had low knowledge"

# Rule 2: Uniform certainty is suspicious
certainties = [f['certainty'] for f in findings]
if len(set(certainties)) == 1 and len(findings) > 3:
    issue = "All findings have identical certainty - templated?"

# Rule 3: Too many high-certainty findings
high_certainty_count = sum(1 for f in findings if f['certainty'] > 0.90)
if high_certainty_count > len(findings) * 0.7:
    issue = "Most findings have >0.90 certainty - overconfident?"
```

**Credible Findings:**
```python
# Varied certainty, matches knowledge
postflight_know = 0.80
findings = [
    {"certainty": 0.85},  # High but justified
    {"certainty": 0.70},  # Medium
    {"certainty": 0.60}   # Lower for less certain
]  # ✓ Credible distribution
```

**Suspicious Findings:**
```python
# All same certainty
findings = [
    {"certainty": 0.85},
    {"certainty": 0.85},
    {"certainty": 0.85},
    {"certainty": 0.85}
]  # ✗ Templated?

# Overconfident across board
postflight_know = 0.55
findings = [
    {"certainty": 0.95},
    {"certainty": 0.92},
    {"certainty": 0.90}
]  # ✗ Too confident given knowledge
```

**Why This Matters:**
Prevents blind trust in findings. If previous AI had low knowledge but claims high-certainty findings, validate independently.

---

### Check 3: Unknowns Reasonableness

**What:** Do remaining unknowns make sense?

**How:** Validates unknown tags for clarity and impact.

**Rules:**
```python
# Rule 1: Too many unknowns vs findings
unknown_to_finding_ratio = len(unknowns) / max(len(findings), 1)
if unknown_to_finding_ratio > 2.0:
    issue = "More unknowns than findings - unclear progress?"

# Rule 2: High impact unknowns should block completion
high_impact_unknowns = [u for u in unknowns if u['impact'] == 'high']
if len(high_impact_unknowns) > 0 and completion_vector > 0.80:
    issue = "High completion but high-impact unknowns remain"

# Rule 3: Unknown descriptions should be clear
for unknown in unknowns:
    if len(unknown['description']) < 20:
        issue = f"Unknown '{unknown['key']}' has vague description"
```

**Reasonable Unknowns:**
```python
# Good balance
findings = 5
unknowns = 2  # Ratio: 0.4 ✓

# High impact blocks completion
unknowns = [{"impact": "high", "key": "database_schema"}]
completion_vector = 0.45  # ✓ Not claiming completion
```

**Unreasonable Unknowns:**
```python
# Too many unknowns
findings = 2
unknowns = 8  # Ratio: 4.0 ✗ Unclear progress

# High completion despite unknowns
unknowns = [{"impact": "high", "key": "critical_blocker"}]
completion_vector = 0.90  # ✗ Contradictory
```

**Why This Matters:**
If unknowns outnumber findings 4:1, previous AI didn't make clear progress. If high-impact unknowns remain but they claim completion, checkpoint is incoherent.

---

### Check 4: Overall Coherence

**What:** Does checkpoint hang together as a whole?

**How:** Context-specific consistency checks.

**Rules:**
```python
# Rule 1: POSTFLIGHT with low completion but no unknowns
if phase == "POSTFLIGHT" and completion < 0.50 and len(unknowns) == 0:
    issue = "Low completion but no unknowns - where's the work?"

# Rule 2: High uncertainty but confident findings
if uncertainty_vector > 0.70 and avg_finding_certainty > 0.85:
    issue = "High uncertainty but confident findings - contradictory"

# Rule 3: Many findings but low knowledge gain
if len(findings) > 10 and know_delta < 0.10:
    issue = "Many findings but minimal knowledge increase"
```

**Why This Matters:**
Catches internally inconsistent checkpoints. If they're highly uncertain but have confident findings, something's wrong.

---

### Recommendation Logic

```python
if all_checks_pass:
    should_investigate = False
    message = "✅ Checkpoint validated. Safe to proceed."

elif claim_vs_reality_failed:
    should_investigate = True
    message = "⚠️ Claims don't match git reality. Run extended CHECK before trusting."

elif findings_not_credible:
    should_investigate = True
    message = "⚠️ Findings questionable. Independently validate before trusting."

elif unknowns_unreasonable or not_coherent:
    should_investigate = True
    message = "⚠️ Checkpoint has inconsistencies. Investigate before proceeding."
```

---

## EpistemicRehydration - Calibration Logic

### Purpose
**"What should I inherit from their context?"**

Calculates how much to adjust starting confidence based on previous AI's work.

---

### Calculation 1: Understanding Ratio

**What:** What % of their findings do I understand?

**How:** For each finding, check if my base knowledge covers that domain.

**Algorithm:**
```python
def calculate_understanding_ratio(findings, my_knowledge):
    understood_count = 0
    
    for finding in findings:
        domain = finding['domain']
        
        # Domain-specific knowledge check
        if domain in ['authentication', 'security'] and my_knowledge['know'] > 0.60:
            understood_count += 1
        elif domain in ['database', 'api_design'] and my_knowledge['know'] > 0.65:
            understood_count += 1
        elif my_knowledge['know'] > 0.70:  # General knowledge
            understood_count += 1
    
    return understood_count / len(findings) if findings else 0.0
```

**Interpretation:**
- `ratio >= 0.70` → I understand most findings ✓
- `0.50 <= ratio < 0.70` → Partial understanding ⚠️
- `ratio < 0.50` → Don't understand most findings ✗

**Why This Matters:**
If you don't understand 70% of findings, you can't effectively build on their work. Rehydration warns you to investigate first.

---

### Calculation 2: Confidence Adjustment

**What:** How much should I boost my starting confidence?

**How:** Estimate boost based on understanding ratio, unknowns, and my base knowledge.

**Algorithm:**
```python
def estimate_rehydration_boost(findings, unknowns, my_base_know):
    # Base boost from findings
    if len(findings) > 0:
        avg_finding_certainty = mean([f['certainty'] for f in findings])
        base_boost = avg_finding_certainty * 0.20  # Max 0.20 from findings
    else:
        base_boost = 0.0
    
    # Penalty from unknowns
    high_impact_unknowns = [u for u in unknowns if u['impact'] == 'high']
    unknown_penalty = len(high_impact_unknowns) * 0.05  # -0.05 per high-impact unknown
    
    # Scale by my base knowledge (low knowledge = conservative boost)
    knowledge_scale = min(my_base_know, 0.80) / 0.80
    
    # Final boost (capped at 0.15)
    boost = (base_boost - unknown_penalty) * knowledge_scale
    return max(0.0, min(boost, 0.15))
```

**Example Results:**
```python
# Strong context, high understanding
findings = [{"certainty": 0.85}, {"certainty": 0.80}]
unknowns = []
my_base_know = 0.75
boost = 0.13  # Significant boost ✓

# Weak context, many unknowns
findings = [{"certainty": 0.60}]
unknowns = [{"impact": "high"}, {"impact": "high"}]
my_base_know = 0.55
boost = 0.02  # Minimal boost ⚠️

# No findings
findings = []
unknowns = []
my_base_know = 0.70
boost = 0.00  # No boost ✓
```

**Why This Matters:**
Prevents over-calibration. Even with good findings, boost is capped at +0.15 (15%) to avoid false confidence.

---

### Calculation 3: Adjusted PREFLIGHT Vectors

**What:** What should my starting vectors be?

**How:** Apply boost to relevant vectors based on inherited context.

**Algorithm:**
```python
def calculate_adjusted_preflight(checkpoint, my_base):
    boost = estimate_rehydration_boost(
        checkpoint['findings'],
        checkpoint['unknowns'],
        my_base['know']
    )
    
    return {
        "know": min(my_base['know'] + boost, 0.95),
        "context": min(my_base['context'] + boost * 1.2, 0.95),  # Context benefits more
        "clarity": my_base['clarity'],  # Not affected by inheritance
        "uncertainty": max(my_base['uncertainty'] - boost * 0.5, 0.05),  # Decrease uncertainty
        # ... other vectors
    }
```

**Example:**
```python
# Before rehydration
my_base = {
    "know": 0.60,
    "context": 0.50,
    "uncertainty": 0.50
}

# After rehydration (boost = 0.12)
adjusted = {
    "know": 0.72,        # +0.12
    "context": 0.64,     # +0.14 (context benefits more)
    "uncertainty": 0.44  # -0.06 (reduced uncertainty)
}
```

**Why This Matters:**
Properly calibrates your starting point. You start more informed than you would from scratch, but not overconfident.

---

## Common Failure Modes Detected

| Failure Mode | Validator | Check | Detection |
|--------------|-----------|-------|-----------|
| **Scope Creep** | Coherence | Scope Match | Planned small, did large |
| **Overconfidence** | Coherence | Trajectory | KNOW↑ but UNCERTAINTY↑ |
| **Stagnation** | Coherence | Trajectory | All vectors unchanged |
| **Dishonest Findings** | Coherence | Findings Honesty | High certainty, low knowledge |
| **Exaggerated Claims** | Handoff | Claim vs Reality | Claims work, minimal git diff |
| **Templated Findings** | Handoff | Findings Credibility | All same certainty |
| **Unclear Progress** | Handoff | Unknowns Reasonable | Unknowns > Findings by 4x |
| **Contradictory State** | Handoff | Overall Coherence | High completion, high-impact unknowns |
| **Poor Inheritance** | Rehydration | Understanding Ratio | <50% understanding |

---

## Next Steps

- **Integration guide:** See `INTEGRATION_GUIDE.md` for usage
- **Tag format:** See `SEMANTIC_TAGS.md` for epistemic tags
- **Examples:** See `VALIDATION_EXAMPLES.md` for real scenarios

---

**Questions?** Check code in `empirica/core/validation/validation_utils.py` for implementation details.
