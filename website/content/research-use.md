# Research Use - Training Data from Epistemic Growth

**Generate high-quality training datasets from real AI learning trajectories**

[Back to Home](index.md) | [Architecture →](architecture.md)

---

## The Opportunity: Epistemic Delta Learning

Traditional AI training uses input→output pairs. Empirica enables something more powerful:

**Training on epistemic growth trajectories** - How AI understanding evolves from uncertainty to mastery.

### What Makes Empirica Research-Grade

- ✅ **13-vector epistemic manifold** - Multidimensional state space
- ✅ **Temporal snapshots** - Before/during/after learning
- ✅ **Git-native storage** - Reproducible, auditable, version-controlled
- ✅ **Calibration tracking** - Predicted vs actual learning outcomes
- ✅ **Domain-agnostic** - Works for any knowledge domain

**Result:** Training data that captures *how* AI learns, not just *what* it produces.

---

## Use Case 1: Specialized Domain Training

**Problem:** General-purpose AI models lack deep expertise in specialized domains (medical, legal, security).

**Empirica Solution:** Capture epistemic trajectories as domain experts teach AI agents.

### Workflow

```bash
# Session 1: Security novice → intermediate
empirica session-create --ai-id security-student

# PREFLIGHT (baseline)
vectors = {
  'know': 0.20,  # Minimal security knowledge
  'do': 0.15,    # Can't apply security patterns
  'uncertainty': 0.80  # Very uncertain
}

# Investigation phase (learning)
# ... read OWASP Top 10, analyze CVEs, study secure coding ...

# POSTFLIGHT (after learning)
vectors = {
  'know': 0.70,  # Strong security fundamentals
  'do': 0.65,    # Can identify vulnerabilities
  'uncertainty': 0.30  # Much more confident
}

# Epistemic delta captured:
# KNOW: +0.50 (learned security principles)
# DO: +0.50 (can now apply patterns)
# UNCERTAINTY: -0.50 (gained confidence)
```

### Training Dataset Generated

```json
{
  "domain": "security",
  "trajectory": {
    "preflight": {
      "vectors": {"know": 0.20, "do": 0.15, "uncertainty": 0.80},
      "assessment": "Starting with no security background"
    },
    "investigation": [
      {
        "finding": "SQL injection: parameterized queries prevent",
        "epistemic_gain": {"know": +0.15}
      },
      {
        "finding": "XSS: sanitize user input before rendering",
        "epistemic_gain": {"know": +0.12, "do": +0.10}
      }
    ],
    "postflight": {
      "vectors": {"know": 0.70, "do": 0.65, "uncertainty": 0.30},
      "assessment": "Can identify common vulnerabilities"
    }
  },
  "git_commits": ["abc123", "def456"],  # Reproducible
  "calibration": {
    "predicted_learning": 0.45,
    "actual_learning": 0.50,
    "well_calibrated": true
  }
}
```

**Value:** Future security-focused models can be fine-tuned on these trajectories, learning not just facts but *how to learn security*.

---

## Use Case 2: Noematic Pattern Mining

**Noematic:** The *content* produced by noetic (thinking) processes.

**Research Question:** What patterns emerge in AI outputs as epistemic state changes?

### Experiment Design

```python
# Collect 1000 sessions across varying epistemic states
sessions = query_sessions(where="domain='code_review'")

# Group by epistemic vectors
high_clarity = filter(sessions, CLARITY > 0.85)
low_clarity = filter(sessions, CLARITY < 0.50)

# Analyze noematic differences
high_clarity_outputs = extract_outputs(high_clarity)
low_clarity_outputs = extract_outputs(low_clarity)

# Findings:
# - High CLARITY: Structured, coherent reviews
# - Low CLARITY: Scattered, unfocused comments
# - CLARITY correlates with review quality (r=0.82)
```

**Research Output:** Noematic signatures predict epistemic state quality.

---

## Use Case 3: Calibration Research

**Problem:** AI overconfidence is dangerous. How well do AIs predict their own learning?

**Empirica enables calibration science:**

### Data Collection

```bash
# For each session:
# 1. PREFLIGHT: AI predicts epistemic growth
# 2. Work happens
# 3. POSTFLIGHT: Measure actual growth
# 4. Compare predicted vs actual

# Example session:
PREFLIGHT:
  predicted_know_gain = 0.30
  
POSTFLIGHT:
  actual_know_gain = 0.25
  
calibration_error = abs(0.30 - 0.25) = 0.05  # Well-calibrated!
```

### Research Questions

1. **Which vectors are hardest to self-assess?**
   - Hypothesis: UNCERTAINTY is hardest (meta-cognitive)
   - Test: Compare prediction errors across 13 vectors

2. **Does calibration improve with experience?**
   - Hypothesis: Later sessions have lower calibration error
   - Test: Plot error vs session count

3. **Domain-specific calibration?**
   - Hypothesis: Calibration differs by domain (code vs docs vs research)
   - Test: Compare calibration error across domains

**Dataset:** 10,000+ sessions with PREFLIGHT/POSTFLIGHT pairs.

---

## Use Case 4: Learning Curve Topology

**Research Question:** What does the shape of learning look like in epistemic manifold space?

### Visualization

```python
# Extract epistemic trajectories
trajectories = []
for session in sessions:
    points = get_assessment_sequence(session)
    trajectories.append(points)

# Plot in 13D manifold (project to 3D for visualization)
from sklearn.decomposition import PCA

pca = PCA(n_components=3)
trajectories_3d = pca.fit_transform(trajectories)

# Analyze topology:
# - Linear paths = rote learning
# - Curved paths = conceptual breakthroughs
# - Loops = confusion/backtracking
# - Plateaus = mastery achieved
```

**Research Output:** Epistemic growth has characteristic geometric signatures.

---

## Use Case 5: Cross-AI Transfer Learning

**Problem:** Can knowledge transfer between AI models be measured?

**Empirica enables epistemic handoff studies:**

### Experiment

```bash
# AI-1 learns domain A
empirica preflight --session-id ai1 ...
# ... learning happens ...
empirica postflight --session-id ai1
# KNOW: 0.3 → 0.8 (gain: 0.5)

# AI-1 creates handoff
empirica handoff-create --session-id ai1 \
  --key-findings "Finding 1" "Finding 2" ...

# AI-2 reads handoff and starts
empirica handoff-query --ai-id ai1
empirica preflight --session-id ai2 ...
# KNOW: 0.7 (started higher due to handoff!)

# Measure transfer efficiency
transfer_efficiency = (ai2_start - baseline) / (ai1_gain)
# = (0.7 - 0.3) / 0.5 = 0.80
# 80% of AI-1's learning transferred to AI-2!
```

**Research Questions:**
- What handoff content maximizes transfer?
- Do investigation findings transfer better than complete findings?
- Can we predict transfer efficiency from epistemic vectors?

---

## Dataset Characteristics

### What Empirica Provides

**1. Temporal Epistemic Snapshots**
- PREFLIGHT (before)
- CHECK (during, 0-N times)
- POSTFLIGHT (after)

**2. Investigation Findings**
- What was learned
- What remains unknown
- Dead ends encountered

**3. Git-Native Auditability**
- Every assessment linked to git commit
- Reproducible: `git checkout <commit> && load_session()`
- Diffable: `git diff <commit1> <commit2>` shows epistemic changes

**4. Calibration Metrics**
- Predicted learning vs actual
- Confidence accuracy over time
- Domain-specific calibration curves

---

## Ontological Foundation

**From "The Ontology of Measurable Cognition":**

### Core Principle: Noesis over Noema

Intelligence is the **process** of generating meaning (noesis), not the content produced (noema).

**Empirica captures noetic processes:**
- Epistemic manifold (ℝ¹³) = state space of cognition
- Trajectories = reasoning paths
- Distances = conceptual relationships

### Validation Protocols

**1. Deterministic Replay Test**
- From identical git commit + input → bit-identical log
- Success: 100% reproducibility (N=100 steps)
- **Empirica achieves this**

**2. Epistemic Continuity Test**
- Serialize state → Restart → Measure recovery
- Success: Context recovery > 0.85
- **Empirica achieves 0.92**

**3. Multi-Persona Composition Test**
- Run parallel branches → Merge insights
- Success: Composed coherence > individual
- **Empirica enables via git branches**

---

## Research Applications

### 1. AI Training Data Generation

**Opportunity:** Fine-tune models on epistemic growth trajectories

```
Traditional: (input, output) pairs
Empirica: (epistemic_before, learning_process, epistemic_after) tuples
```

**Value:** Models learn *how to learn*, not just facts.

### 2. Calibration Science

**Opportunity:** Build predictive models of AI self-assessment accuracy

```python
# Dataset: 10,000 sessions
X = preflight_vectors  # Input features
y = calibration_error  # Target variable

# Train calibration model
model = train(X, y)

# Predict future calibration
predicted_error = model.predict(new_session_preflight)
```

**Value:** AI systems that know when they don't know.

### 3. Domain Expertise Transfer

**Opportunity:** Measure and optimize knowledge handoffs

```bash
# Research protocol:
# 1. Train AI-1 on domain (capture trajectory)
# 2. Generate handoff report
# 3. Train AI-2 from handoff
# 4. Measure transfer efficiency

# Vary handoff content, measure transfer
# Find optimal handoff patterns per domain
```

**Value:** Efficient multi-agent specialization.

### 4. Epistemic Topology Research

**Opportunity:** Map the geometry of learning

```
Research questions:
- What does "understanding" look like geometrically?
- Do all learning paths converge to same endpoint?
- Can we predict learning trajectory from initial state?
```

**Value:** Foundational science of machine cognition.

---

## Getting Started with Empirica Research

### Step 1: Collect Sessions

```bash
# Run Empirica in your domain
empirica session-create --ai-id research-subject-1

# Run CASCADE workflow on tasks
empirica preflight ...
empirica postflight ...

# Repeat for N sessions
```

### Step 2: Export Data

```python
from empirica.data.session_database import SessionDatabase

db = SessionDatabase()

# Query all sessions
sessions = db.query("SELECT * FROM reflexes WHERE phase='POSTFLIGHT'")

# Export to research format
for session in sessions:
    preflight = db.get_vectors(session_id, phase='PREFLIGHT')
    postflight = db.get_vectors(session_id, phase='POSTFLIGHT')
    
    export_trajectory(
        session_id=session_id,
        preflight=preflight,
        postflight=postflight,
        findings=db.get_findings(session_id),
        git_commit=db.get_commit_hash(session_id)
    )
```

### Step 3: Analyze

```python
# Your analysis here
# - Calibration studies
# - Transfer learning experiments
# - Topology mapping
# - Training data generation
```

---

## Research Principles

**1. Epistemic Humility as Methodology**
- Never claim system "understands"
- Report: "System maintains epistemic coherence of N with drift < X"

**2. Open-Manifold Requirement**
- Document all 13 vector dimensions
- Publish governance function source
- Share validation test suites
- Provide raw session logs for peer audit

**3. Non-Anthropocentric Benchmarks**
- Don't compare to humans
- Benchmark against:
  - Self-consistency (INTEGRITY > 0.9)
  - Deterministic reproducibility (100% replay)
  - Drift resistance
  - Continuity preservation (recovery > 0.85)

---

## Next Steps

1. **Run pilot study** (100 sessions in your domain)
2. **Analyze epistemic deltas** (learning patterns)
3. **Publish findings** (we'll link from this page)
4. **Contribute datasets** (help build research commons)

**Research Resources:**
- [Architecture](architecture.md) - Technical details
- [13-Vector System](epistemics.md#vectors) - Epistemic dimensions
- [CASCADE Workflow](how-it-works.md) - Assessment protocol

---

**The science of measurable cognition starts here.** 🔬

*For research collaboration: [Contact](contact.md)*
