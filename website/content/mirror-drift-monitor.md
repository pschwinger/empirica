# Mirror Drift Monitor - Real-Time Epistemic Validation

**Detect when AI capabilities degrade in real-time**

[Back to Home](index.md) | [Architecture →](architecture.md)

---

## The Problem: Silent Degradation

AI systems can lose capability without warning:
- 🧠 **Context loss** - Forgetting previous understanding
- 📉 **Capability drops** - KNOW/DO vectors decreasing unexpectedly
- 🎲 **Overconfidence** - Uncertainty too low for task complexity
- 🔄 **Confusion** - CLARITY degrading mid-session

**Traditional approach:** Hope you notice before shipping broken code.

**Empirica approach:** Continuous epistemic monitoring with automatic drift detection.

---

## How Mirror Drift Works

### The Mirror Principle

**Your past epistemic state reflects back to validate your present state.**

```
Current Assessment → Compare → Historical Baseline → Flag Drops
                              (from Git checkpoints)
```

**Core insight:** Your average recent performance is your baseline. Significant drops indicate drift.

---

## What Gets Monitored

### Tier 0 Vectors (Critical)

- **KNOW** - Domain knowledge confidence
  - Drop detection: Current << historical average
  - Example: Know=0.8 baseline, now 0.5 = **DRIFT**

- **DO** - Task execution capability
  - Drop detection: Capability regression
  - Example: Do=0.85 baseline, now 0.6 = **DRIFT**

- **CONTEXT** - Coherence with session history
  - Drop detection: Lost narrative thread
  - Example: Context=0.9 baseline, now 0.5 = **DRIFT**

### Tier 1 Vectors (Secondary)

- **CLARITY** - Internal self-consistency
- **COHERENCE** - Logical flow between steps
- **SIGNAL** - Relevance to core task

### Meta Vector

- **UNCERTAINTY** - Explicit doubt
  - Pattern detection: Too low for complex tasks = overconfidence

---

## Drift Detection Thresholds

### What Triggers Drift Warnings

```python
# Calculate baseline from last 5 checkpoints
baseline = average(last_5_checkpoints)

# Detect drops (increases are EXPECTED from learning)
for vector in [KNOW, DO, CONTEXT, CLARITY]:
    drop = baseline[vector] - current[vector]
    if drop > 0.15:  # 15% drop
        flag_drift(vector, drop)
```

**Key principle:** Only drops are flagged. Increases = learning (good!).

### Drift Severity Levels

| Drop Size | Severity | Action |
|-----------|----------|--------|
| 0.10-0.15 | ⚠️ **WARNING** | Monitor closely |
| 0.15-0.25 | 🚨 **DRIFT** | Investigate immediately |
| > 0.25 | 💥 **CRITICAL** | Stop and reset |

---

## Real-World Example

### Scenario: Context Loss During Refactoring

**Session Timeline:**

```bash
# Checkpoint 1 (Hour 1)
KNOW=0.80, DO=0.85, CONTEXT=0.90, CLARITY=0.88

# Checkpoint 2 (Hour 2) 
KNOW=0.82, DO=0.87, CONTEXT=0.92, CLARITY=0.90
# ✅ All improving (learning!)

# Checkpoint 3 (Hour 3)
KNOW=0.85, DO=0.90, CONTEXT=0.65, CLARITY=0.60
# 🚨 DRIFT DETECTED: CONTEXT drop 0.27, CLARITY drop 0.30
```

**What happened?** Large refactoring broke mental model. AI lost track of original architecture.

**Mirror Drift Alert:**
```
⚠️ EPISTEMIC DRIFT DETECTED
  
  CONTEXT: 0.92 → 0.65 (drop: 0.27) 🚨 CRITICAL
  CLARITY: 0.90 → 0.60 (drop: 0.30) 🚨 CRITICAL
  
  Recommendation: Pause and re-investigate architecture before continuing.
  Query previous session: empirica handoff-query --session-id <ID>
```

---

## Integration with Statusline

Mirror Drift Monitor feeds the **statusline** display:

```bash
# Stable state
🧠 K:0.85 D:0.90 U:0.20 [STABLE]

# Drift detected
🧠 K:0.65 D:0.70 U:0.35 [DRIFTING ⚠️]
   └─ CONTEXT dropped 0.25 from baseline

# Critical drift
🧠 K:0.45 D:0.55 U:0.50 [DRIFT CRITICAL 🚨]
   └─ Multiple vectors below safe threshold
```

**Flow:** CASCADE workflow → `reflexes` table → Mirror Drift Monitor → Statusline display

---

## No Heuristics Design

**What Mirror Drift does NOT do:**
- ❌ Use keyword matching to classify domains
- ❌ Apply heuristic rules about what "should" happen
- ❌ Require external LLMs for validation
- ❌ Make assumptions about task types

**What it DOES do:**
- ✅ Load recent checkpoints from git notes
- ✅ Calculate baseline by averaging historical vectors
- ✅ Detect statistical drops (current << baseline)
- ✅ Pure temporal comparison, no guesswork

**Design principle:** Let the data speak. Past performance predicts present capability.

---

## Architecture

### Data Flow

```
1. CASCADE Assessment (PREFLIGHT/CHECK/POSTFLIGHT)
   ↓
2. Store in reflexes table + git checkpoint
   ↓
3. Mirror Drift Monitor queries last N checkpoints
   ↓
4. Calculate baseline + detect drops
   ↓
5. Update statusline display
   ↓
6. Alert if critical drift detected
```

### Storage Queries

```python
from empirica.core.canonical.empirica_git.checkpoint_manager import CheckpointManager

# Load recent checkpoints
checkpoint_manager = CheckpointManager()
recent = checkpoint_manager.load_recent_checkpoints(
    session_id=session_id,
    count=5  # Last 5 checkpoints
)

# Calculate baseline
baseline = calculate_baseline(recent)

# Detect drift
drift_report = detect_drift(current_vectors, baseline)
```

**Storage:** Git notes at `refs/notes/empirica/checkpoints` (~200 bytes each)

---

## Use Cases

### Solo AI Development
- **Catch degradation** before shipping bugs
- **Resume confidence** after context switches
- **Track learning** vs drift patterns

### Multi-Agent Teams
- **Handoff validation** - Does AI-2 maintain AI-1's context?
- **Specialist transition** - Research → Implementation drift check
- **Parallel work merge** - Ensure no capability loss when merging branches

### Research
- **Calibration analysis** - How often do AIs drift?
- **Learning curves** - Growth vs regression patterns
- **Training data** - Epistemic stability signals

---

## Configuration

### Thresholds (Customizable)

Default thresholds in `thresholds.yaml`:

```yaml
drift_detection:
  warning_threshold: 0.10  # 10% drop
  drift_threshold: 0.15    # 15% drop
  critical_threshold: 0.25 # 25% drop
  
  lookback_count: 5        # Last 5 checkpoints
  
  monitored_vectors:
    - KNOW
    - DO
    - CONTEXT
    - CLARITY
    - COHERENCE
```

**Customize per use case:**
- Tighter thresholds for production deployments
- Looser thresholds for exploratory research
- More lookback for long-running sessions

---

## Next Steps

1. **Enable drift monitoring** in your session
2. **Create regular checkpoints** during CASCADE workflow
3. **Watch the statusline** for drift alerts
4. **Query handoffs** when drift detected to restore context

**Learn more:**
- [CASCADE Workflow](how-it-works.md) - When checkpoints happen
- [Statusline Integration](monitoring.md) - Real-time display
- [Architecture](architecture.md) - Storage details

---

**Trust but verify:** Let your past self validate your present self. 🪞
