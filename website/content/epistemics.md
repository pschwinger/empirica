# Epistemics: The Foundation of AI Self-Awareness

**Why measuring what AIs know—and don't know—is critical for reliable AI systems**

[Back to Home](index.md) | [Collaboration →](collaboration.md)

---

## What is Epistemic Self-Assessment?

**Epistemics** is the study of knowledge—what we know, how we know it, and what we're uncertain about.

Traditional AI systems either:
- ❌ **Overconfident** - Claim certainty when uncertain
- ❌ **Underconfident** - Hesitate when capable
- ❌ **Heuristic-based** - Use keyword matching to fake self-awareness
- ❌ **No uncertainty tracking** - Can't distinguish "I know" from "I guess"

**Empirica's approach:**
- ✅ **Genuine LLM-powered self-assessment** - Real reasoning, not heuristics
- ✅ **13-vector epistemic measurement** - Comprehensive knowledge state
- ✅ **Explicit uncertainty tracking** - "Know what you don't know"
- ✅ **Calibrated confidence** - Measure accuracy of self-assessment
- ✅ **Learning deltas** - Track epistemic growth over time

> **Note on Schema Migration (v2.0):** Empirica's internal schema has been updated with tier-prefixed field names (e.g., `foundation_know`, `comprehension_clarity`). This is 90% complete and backward compatible. Users interact with the same 13 vectors - the changes are internal. See [Schema Migration Guide](../docs/production/27_SCHEMA_MIGRATION_GUIDE.md) for details.

---

## The 13 Epistemic Vectors

Empirica measures AI knowledge state across **13 dimensions**, organized into 5 groups:

### Gate: ENGAGEMENT (≥0.60 required)

**Purpose:** Ensure meaningful collaboration before proceeding

- **Collaborative Intelligence** (25%) - AI-human synergy quality
- **Co-creative Amplification** (25%) - Mutual enhancement loop
- **Belief Space Management** (25%) - Shared belief coherence
- **Authentic Collaboration** (25%) - Real vs performative engagement

**Why it's a gate:**
- Low engagement (<0.60) indicates unclear task or poor fit
- Must pass before any work begins
- Prevents wasted effort on misunderstood tasks

**Example:**
```
Task: "Do the thing"
ENGAGEMENT: 0.35 ❌ → Action: CLARIFY (need user input)

Task: "Analyze authentication system for SQL injection vulnerabilities"
ENGAGEMENT: 0.85 ✅ → Continue to assessment
```

---

### Foundation Vectors (35% weight)

**Purpose:** Core knowledge and capability assessment

#### 1. KNOW - Domain Knowledge
**What it measures:** Understanding of relevant domain, concepts, technologies

**High KNOW (0.8+):**
- Deep domain understanding
- Familiar with tools and approaches
- Know context and implications

**Low KNOW (<0.5):**
- Unfamiliar domain
- Missing critical knowledge
- Need external research

**Investigation Strategy:** Web search, documentation, semantic search

---

#### 2. DO - Execution Capability
**What it measures:** Ability to execute required actions, technical capability

**High DO (0.8+):**
- Have necessary tools/access
- Technical capability present
- Know implementation approach

**Low DO (<0.5):**
- Missing required tools
- Lack technical capability
- Need user assistance

**Investigation Strategy:** Check workspace, verify access, ask user

---

#### 3. CONTEXT - Environmental Awareness
**What it measures:** Understanding of environment, current state, constraints

**High CONTEXT (0.8+):**
- Understand current environment
- Know system state
- Aware of constraints

**Low CONTEXT (<0.5):**
- Don't understand environment
- Missing system state
- Unclear on constraints

**Investigation Strategy:** Workspace scan, read files, check session history

---

### Comprehension Vectors (25% weight)

**Purpose:** Task understanding and information quality

#### 4. CLARITY - Task Understanding
**What it measures:** How clear and well-defined the request is

**High CLARITY (0.8+):**
- Specific request
- Clear goals
- Defined success criteria

**Low CLARITY (<0.5):**
- Vague request
- Unclear goals
- Ambiguous requirements

**Investigation Strategy:** **HIGHEST PRIORITY** - Ask user for clarification (0.40 gain)

---

#### 5. COHERENCE - Logical Consistency
**What it measures:** Internal logical consistency of request and approach

**High COHERENCE (0.8+):**
- Request makes logical sense
- No contradictions
- Approach is sound

**Low COHERENCE (<0.5):**
- Contradictory requirements
- Logical issues
- Approach unclear

**Critical Threshold:** <0.50 → RESET (task incoherent)

**Investigation Strategy:** Ask user to resolve contradictions

---

#### 6. SIGNAL - Information Quality
**What it measures:** Ratio of useful information to noise

**High SIGNAL (0.8+):**
- Clear signal
- Relevant information
- Focused request

**Low SIGNAL (<0.5):**
- Lost in noise
- Too much irrelevant info
- Hard to extract signal

**Investigation Strategy:** Extract structured objectives

---

#### 7. DENSITY - Complexity Management
**What it measures:** Information load (inverted - HIGH is bad)

**Low DENSITY (0.3-0.5) - GOOD:**
- Manageable information load
- Right amount of detail

**High DENSITY (0.8+) - BAD:**
- Information overload
- Overwhelming complexity
- Cognitive saturation

**Critical Threshold:** >0.90 → RESET (cognitive overload)

**Investigation Strategy:** Break down into manageable pieces

---

### Execution Vectors (25% weight)

**Purpose:** Readiness and progress tracking

#### 8. STATE - Current Readiness
**What it measures:** Understanding of current state

**High STATE (0.8+):**
- Clear picture of current state
- Know what exists
- See starting point

**Low STATE (<0.5):**
- Unclear current state
- Don't know what exists
- Can't see starting point

**Investigation Strategy:** Workspace scan, read files, bash commands

---

#### 9. CHANGE - Progress Tracking
**What it measures:** Ability to track and manage changes

**High CHANGE (0.8+):**
- Can track progress
- Monitor evolution
- Detect regressions

**Low CHANGE (<0.5):**
- Can't track changes
- No change visibility
- Can't detect issues

**Critical Threshold:** <0.50 → STOP (cannot progress)

**Investigation Strategy:** Ask about version control, testing, validation

---

#### 10. COMPLETION - Goal Proximity
**What it measures:** Visibility of path to completion

**High COMPLETION (0.8+):**
- Clear path to done
- Know the steps
- Success criteria clear

**Low COMPLETION (<0.5):**
- Unclear path forward
- Don't know steps
- Success criteria vague

**Investigation Strategy:** Create structured completion path

---

#### 11. IMPACT - Consequence Awareness
**What it measures:** Ability to predict consequences

**High IMPACT (0.8+):**
- Understand consequences
- Can predict effects
- Know risks

**Low IMPACT (<0.5):**
- Can't predict consequences
- Unknown effects
- Risks unclear

**Investigation Strategy:** Ask user about constraints and acceptable impacts

---

### Meta-Epistemic: UNCERTAINTY

#### 12. UNCERTAINTY - Explicit Uncertainty Measurement
**What it measures:** "What you don't know about what you don't know"

**Type:** Meta-epistemic (not included in overall confidence calculation)

**Low UNCERTAINTY (<0.3) - GOOD:**
- Confident in assessment
- Domain well-understood
- Few unknowns

**High UNCERTAINTY (0.7+) - INVESTIGATE:**
- Significant epistemic gaps
- Domain beyond training data
- Many unknowns present

**Why it's different:**
- Tracks uncertainty ABOUT the 13-vector assessment itself
- Enables PREFLIGHT vs POSTFLIGHT comparison
- Validates investigation effectiveness

**Example:**
```
PREFLIGHT:
  KNOW: 0.35 (low knowledge)
  UNCERTAINTY: 0.75 (high uncertainty)
  → Action: INVESTIGATE

... investigation happens ...

POSTFLIGHT:
  KNOW: 0.80 (knowledge increased +0.45)
  UNCERTAINTY: 0.25 (uncertainty reduced -0.50)
  → Investigation was effective! ✅
```

---

#### 13. CALIBRATION - Confidence Accuracy (POSTFLIGHT only)
**What it measures:** How well predictions matched reality

**Calculated during POSTFLIGHT:**
- Compare PREFLIGHT predictions with actual outcomes
- Measure overconfidence (predicted > actual)
- Measure underconfidence (predicted < actual)
- Track calibration patterns over time

**Purpose:** Continuous improvement of self-assessment accuracy

---

## How Vectors Combine

### Canonical Weights

```python
overall_confidence = (
    foundation_confidence × 0.35 +      # KNOW, DO, CONTEXT
    comprehension_confidence × 0.25 +   # CLARITY, COHERENCE, SIGNAL, DENSITY
    execution_confidence × 0.25 +       # STATE, CHANGE, COMPLETION, IMPACT
    engagement × 0.15                   # ENGAGEMENT
)
```

### Group Calculations

```python
foundation_confidence = (know + do + context) / 3
comprehension_confidence = (clarity + coherence + signal + (1 - density)) / 4  # density inverted
execution_confidence = (state + change + completion + impact) / 4
```

**Source:** `empirica/core/canonical/reflex_frame.py`

---

## Critical Thresholds

Empirica enforces critical thresholds to prevent unsafe operation:

```python
ENGAGEMENT_THRESHOLD = 0.60  # Must pass to proceed
COHERENCE_CRITICAL = 0.50    # < 0.50 → RESET (task incoherent)
DENSITY_CRITICAL = 0.90      # > 0.90 → RESET (cognitive overload)
CHANGE_CRITICAL = 0.50       # < 0.50 → STOP (cannot progress)
UNCERTAINTY_HIGH = 0.80      # > 0.80 → INVESTIGATE (high uncertainty)
```

**Why thresholds matter:**
- **Safety** - Prevent AI from proceeding when confused
- **Quality** - Ensure minimum understanding before action
- **Honesty** - Force acknowledgment of uncertainty

---

## Calibrated Confidence: The Differentiator

### Traditional AI Confidence
```
AI: "I'm 95% confident this will work"
Reality: *Doesn't work*
AI: "I'm 95% confident this fix will work"
Reality: *Still doesn't work*
```

**Problem:** No learning, no calibration, no improvement

---

### Empirica's Calibrated Confidence

**Phase 1: PREFLIGHT (Baseline)**
```python
assessment_preflight = {
    'know': 0.35,           # Low domain knowledge
    'do': 0.75,             # Can execute
    'context': 0.60,        # Some context
    'uncertainty': 0.75,    # High uncertainty
    'overall_confidence': 0.48
}
# Recommendation: INVESTIGATE
```

**Phase 2: INVESTIGATE**
- Research OAuth flows
- Explore authentication libraries
- Read security best practices
- Prototype token validation

**Phase 3: CHECK (Reassessment)**
```python
assessment_check = {
    'know': 0.80,           # Knowledge increased +0.45
    'do': 0.85,             # Capability confirmed +0.10
    'context': 0.75,        # Context improved +0.15
    'uncertainty': 0.30,    # Uncertainty reduced -0.45
    'overall_confidence': 0.82
}
# Recommendation: PROCEED
```

**Phase 4: ACT**
- Implement OAuth authentication
- Write tests
- Document approach

**Phase 5: POSTFLIGHT (Calibration)**
```python
assessment_postflight = {
    'know': 0.90,           # Final knowledge +0.55 from PREFLIGHT
    'do': 0.90,             # Execution validated +0.15
    'context': 0.85,        # Full context +0.25
    'uncertainty': 0.15,    # Minimal uncertainty -0.60
    'overall_confidence': 0.88,
    
    # Calibration metrics
    'calibration_accuracy': 0.92,  # Predictions matched reality
    'overconfidence_delta': -0.04,  # Slightly underconfident (good!)
    'epistemic_growth': 0.40        # Significant learning occurred
}
```

**Learning Delta:**
```
KNOW: 0.35 → 0.90 (+0.55) 🚀
UNCERTAINTY: 0.75 → 0.15 (-0.60) 🎯
Overall: 0.48 → 0.88 (+0.40) ✅
```

**Calibration Insight:**
- AI predicted 0.82 confidence after investigation
- Actual outcome confidence: 0.88
- Delta: -0.06 (slightly underconfident)
- **Pattern:** This AI tends to underestimate slightly → can be more confident

---

## Why This Matters for AI Systems

### 1. **Reliability**
- AIs that know their limits are more reliable
- Explicit uncertainty prevents overconfident failures
- Calibration improves over time

### 2. **Safety**
- Critical thresholds prevent unsafe operation
- ENGAGEMENT gate ensures task understanding
- COHERENCE check catches contradictory requirements

### 3. **Efficiency**
- Don't waste time on tasks AI can't do
- Investigation focuses on actual gaps
- Learning deltas show what was gained

### 4. **Collaboration**
- Humans know when to trust AI vs verify
- AIs know when to ask for help
- Shared epistemic state enables coordination

### 5. **Continuous Improvement**
- Calibration metrics reveal patterns
- Over/underconfidence detected
- Self-assessment accuracy improves

---

## Genuine vs Heuristic Assessment

### ❌ Heuristic Approach (What Empirica Avoids)

```python
# WRONG - Keyword matching
if 'refactor' in task:
    domain = 'code_analysis'
    know = 0.7  # Fake confidence

# WRONG - Hardcoded confidence boosts
confidence += 0.15 * tools_used  # Not genuine learning

# WRONG - Simulated learning
know_after = know_before + (rounds * 0.05)  # Fake growth
```

**Problems:**
- Not genuine reasoning
- Can't handle novel situations
- No real uncertainty awareness
- Fake learning deltas

---

### ✅ Empirica's Genuine Approach

```python
# Genuine LLM self-assessment
assessment = await assessor.assess(
    task="Refactor authentication system",
    context={"cwd": "/project", "domain": "security"}
)

# LLM genuinely reasons:
# "I understand authentication patterns (know: 0.7)
#  but I'm uncertain about this specific codebase (uncertainty: 0.6)
#  and I don't know the current implementation (context: 0.4).
#  I need to investigate before proceeding."

# Result: EpistemicAssessment with genuine reasoning
```

**Benefits:**
- Real reasoning about knowledge state
- Handles novel situations
- Honest uncertainty acknowledgment
- Genuine learning measurement

---

## Reading Vector Patterns

### Pattern 1: Knowledge Gap
```
KNOW: 0.35 (low)
DO: 0.80 (high)
CONTEXT: 0.70 (good)
→ Strategy: External search (web, documentation)
```

### Pattern 2: Unclear Request
```
CLARITY: 0.40 (low)
KNOW: 0.75 (good)
DO: 0.80 (good)
→ Strategy: User clarification (HIGHEST PRIORITY)
```

### Pattern 3: Missing Environment Context
```
CONTEXT: 0.35 (low)
STATE: 0.40 (low)
KNOW: 0.70 (good)
→ Strategy: Environmental scanning (workspace, files)
```

### Pattern 4: High Uncertainty
```
KNOW: 0.30 (low)
UNCERTAINTY: 0.85 (very high)
CLARITY: 0.45 (low)
→ Strategy: Comprehensive investigation required
```

### Pattern 5: Ready to Proceed
```
All vectors > 0.70
ENGAGEMENT: 0.80
UNCERTAINTY: 0.25
Overall: 0.78
→ Action: PROCEED with confidence
```

---

## Next Steps

**Learn More:**
- [Cross-AI Collaboration](collaboration.md) - Sessions, goals, handoffs
- [AI vs Agent Patterns](ai_vs_agent.md) - High reasoning vs action-based AIs
- [Architecture](architecture.md) - System design and structure
- [Production Docs](../docs/production/05_EPISTEMIC_VECTORS.md) - Complete vector reference

**Try It:**
```python
from empirica.core.metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade

cascade = CanonicalEpistemicCascade()
result = await cascade.run_epistemic_cascade(
    task="Your task here",
    context={"domain": "your_domain"}
)

print(f"Confidence: {result['confidence']:.2f}")
print(f"Epistemic Delta: {result.get('epistemic_delta', {})}")
```

---

**Built with epistemic transparency. Know what you don't know.** 🧠
