# 📊 Mirror Drift Monitor - Temporal Self-Validation

**Status:** ✅ Production-ready (No heuristics, no external LLMs)

---

## Overview

The **MirrorDriftMonitor** detects epistemic drift by comparing current self-assessments to historical baselines stored in Git checkpoints. It uses the **Mirror Principle**: your past epistemic state reflects back to validate your present state.

### Purpose

Detect significant changes in epistemic vectors that indicate:
- **Drops in capability** (KNOW, DO decreasing unexpectedly)
- **Context loss** (CONTEXT, CLARITY degrading)
- **Overconfidence patterns** (Uncertainty too low for complex tasks)

**Note:** Increases in epistemic vectors are EXPECTED from learning and are not flagged as drift.

---

## Architecture

### No Heuristics Design

The drift monitor is built on **pure temporal comparison**:

```
Current Assessment → Compare to → Historical Baseline → Flag Drops
                                  (from Git checkpoints)
```

**What it does NOT do:**
- ❌ Use keyword matching to classify domains
- ❌ Apply heuristic rules about what "should" happen
- ❌ Require external LLMs for validation
- ❌ Make assumptions about task types

**What it DOES do:**
- ✅ Load recent checkpoints from `checkpoint_manager`
- ✅ Calculate baseline by averaging historical vectors
- ✅ Detect statistical drops (current << baseline)
- ✅ Integrate with Git for persistence

---

## How It Works

### 1. Data Source: checkpoint_manager (PRIMARY Tier)

The drift monitor depends on the PRIMARY storage tier:

```python
from empirica.core.canonical.empirica_git.checkpoint_manager import CheckpointManager

checkpoint_manager = CheckpointManager()
recent = checkpoint_manager.load_recent_checkpoints(
    session_id=session_id,
    count=5  # Look back 5 checkpoints
)
```

**Storage:** `refs/notes/empirica/checkpoints` (~200 bytes each)

**Why PRIMARY tier?** The drift monitor requires lightweight, frequent checkpoints for temporal comparison. The compressed format is perfect for this.

---

### 2. Baseline Calculation

```python
def calculate_baseline(self, recent_checkpoints: List[dict]) -> dict:
    """
    Average recent epistemic vectors to create baseline.
    
    No heuristics - just statistical mean of past assessments.
    """
    vectors = [cp['assessment']['vectors'] for cp in recent_checkpoints]
    
    baseline = {}
    for vector_name in EPISTEMIC_VECTORS:
        values = [v[vector_name] for v in vectors]
        baseline[vector_name] = sum(values) / len(values)
    
    return baseline
```

**Simple principle:** Your average recent performance is your baseline.

---

### 3. Drift Detection

```python
def detect_drift(
    self,
    current_assessment: EpistemicAssessmentSchema,
    session_id: str
) -> DriftReport:
    """
    Compare current to baseline, flag significant drops.
    
    Increases are expected (learning), only drops indicate drift.
    """
    # Load recent history
    recent = self.checkpoint_manager.load_recent_checkpoints(
        session_id=session_id,
        count=self.lookback_window
    )
    
    if len(recent) < 3:
        return DriftReport(sufficient_history=False)
    
    # Calculate baseline
    baseline = self.calculate_baseline(recent)
    
    # Detect drops (not increases!)
    drift_detected = {}
    for vector, current_value in current_assessment.vectors.items():
        baseline_value = baseline[vector]
        delta = current_value - baseline_value
        
        # Only flag DROPS beyond threshold
        if delta < -self.drift_threshold:
            drift_detected[vector] = {
                'current': current_value,
                'baseline': baseline_value,
                'drop': abs(delta)
            }
    
    return DriftReport(
        drift_detected=bool(drift_detected),
        vectors_drifted=drift_detected,
        baseline=baseline,
        current=current_assessment.vectors
    )
```

---

## Integration with Dual-Tier Storage

The drift monitor showcases why we have two storage tiers:

### Uses PRIMARY Tier (checkpoint_manager)
- Loads 5-10 recent checkpoints efficiently
- ~200 bytes each = ~2KB total for drift detection
- Fast temporal comparison
- Automatic integration with CASCADE

### Does NOT Use SECONDARY Tier (git_enhanced_reflex_logger)
- The 2-3KB detailed logs are for debugging
- Drift detection needs lightweight, frequent data
- Shows clear separation of concerns

---

## Usage Examples

### Basic Usage

```python
from empirica.core.drift.mirror_drift_monitor import MirrorDriftMonitor
from empirica.core.schemas.epistemic_assessment import EpistemicAssessmentSchema

# Initialize
monitor = MirrorDriftMonitor(
    drift_threshold=0.2,  # Flag 20% drops
    lookback_window=5     # Compare to last 5 checkpoints
)

# Current assessment from PREFLIGHT/CHECK/POSTFLIGHT
current = EpistemicAssessmentSchema(
    vectors={
        'engagement': 0.8,
        'know': 0.4,  # ⚠️ Potential drop
        'do': 0.9,
        'context': 0.7,
        # ... etc
    }
)

# Detect drift
report = monitor.detect_drift(
    current_assessment=current,
    session_id='abc-123'
)

if report.drift_detected:
    print(f"Drift detected in: {list(report.vectors_drifted.keys())}")
    for vector, data in report.vectors_drifted.items():
        print(f"{vector}: {data['current']:.2f} (was {data['baseline']:.2f})")
```

### Integration with CASCADE

The CASCADE workflow automatically creates checkpoints, feeding the drift monitor:

```python
# CASCADE creates checkpoint after each round
checkpoint_manager.save(
    session_id=session_id,
    assessment=current_assessment,
    phase='INVESTIGATE',
    round_num=2
)

# Drift monitor automatically has data for next CHECK
report = monitor.detect_drift(current_assessment, session_id)
```

---

## Configuration

### Thresholds

```python
MirrorDriftMonitor(
    drift_threshold=0.2,     # 20% drop triggers alert
    lookback_window=5,       # Compare to last 5 checkpoints
    min_history=3            # Need 3+ checkpoints to start
)
```

**Tuning guidance:**
- **drift_threshold=0.1**: Sensitive (10% drop triggers)
- **drift_threshold=0.2**: Balanced (20% drop triggers) ← Default
- **drift_threshold=0.3**: Conservative (30% drop triggers)

### Session-Specific Tuning

```python
# Load from config
from empirica.config.threshold_loader import ThresholdLoader

thresholds = ThresholdLoader.load()
monitor = MirrorDriftMonitor(
    drift_threshold=thresholds['drift_threshold'],
    lookback_window=thresholds['lookback_window']
)
```

---

## Drift Reports

### Report Structure

```python
@dataclass
class DriftReport:
    drift_detected: bool
    sufficient_history: bool
    vectors_drifted: dict  # {vector: {current, baseline, drop}}
    baseline: dict         # Baseline values
    current: dict          # Current values
    timestamp: float
```

### Example Report

```json
{
  "drift_detected": true,
  "sufficient_history": true,
  "vectors_drifted": {
    "know": {
      "current": 0.4,
      "baseline": 0.7,
      "drop": 0.3
    },
    "context": {
      "current": 0.5,
      "baseline": 0.8,
      "drop": 0.3
    }
  },
  "baseline": {
    "engagement": 0.85,
    "know": 0.7,
    "do": 0.9,
    "context": 0.8,
    ...
  },
  "current": {
    "engagement": 0.8,
    "know": 0.4,
    "do": 0.9,
    "context": 0.5,
    ...
  },
  "timestamp": 1234567890.5
}
```

---

## Why This Design Works

### 1. Pure Temporal Comparison
No heuristics means no assumptions about what tasks "should" look like. The AI's own history is the truth.

### 2. Git Integration
Leverages existing checkpoint infrastructure - no separate storage needed.

### 3. Learning-Aware
Only flags DROPS, not increases. Learning should increase epistemic vectors over time.

### 4. Lightweight
Uses PRIMARY tier (checkpoint_manager) for efficiency - ~450 tokens per checkpoint.

### 5. Self-Contained
No external LLMs, no keyword matching, no complex rules. Just: current vs baseline.

---

## Common Scenarios

### Scenario 1: Normal Learning Pattern

```
Round 1: know=0.5, do=0.6
Round 2: know=0.6, do=0.7  ← Learning (increase)
Round 3: know=0.7, do=0.8  ← More learning

Drift? NO - increases are expected
```

### Scenario 2: Context Loss

```
Round 1: context=0.8, clarity=0.9
Round 2: context=0.7, clarity=0.8  ← Slight drop
Round 3: context=0.4, clarity=0.5  ← Significant drop!

Drift? YES - context dropped 40%, clarity dropped 40%
Likely cause: Scope creep, task switched without PREFLIGHT
```

### Scenario 3: Overconfidence Pattern

```
Round 1: uncertainty=0.3 (appropriate for exploration)
Round 2: uncertainty=0.2 (gaining confidence)
Round 3: uncertainty=0.05 (very confident)
Round 4: uncertainty=0.02 (extremely confident)

Drift? Possibly - if baseline uncertainty=0.25, current=0.02 is a 92% drop
Warning: May indicate overconfidence, not true confidence
```

---

## Testing

### Unit Tests

See `tests/unit/drift/test_mirror_drift_monitor.py`:

```python
def test_drift_detection_drops():
    """Verify drops are detected"""
    monitor = MirrorDriftMonitor(drift_threshold=0.2)
    
    # Create history with know=0.7
    history = [create_checkpoint(know=0.7) for _ in range(5)]
    
    # Current has know=0.4 (drop of 0.3)
    current = create_assessment(know=0.4)
    
    report = monitor.detect_drift(current, 'test-session')
    
    assert report.drift_detected
    assert 'know' in report.vectors_drifted
    assert report.vectors_drifted['know']['drop'] == 0.3
```

### Integration Tests

See `tests/integration/test_check_drift_integration.py`:

```python
def test_cascade_drift_detection():
    """Verify CASCADE → checkpoint → drift detection flow"""
    # Run CASCADE, create checkpoints
    # Simulate context loss
    # Verify drift detected at CHECK phase
```

---

## Troubleshooting

### "Insufficient history" Error

**Cause:** Less than 3 checkpoints available
**Solution:** Run a few CASCADE rounds first to build history

```python
if report.sufficient_history is False:
    print("Need more checkpoints for drift detection")
    # Continue working, drift detection will activate later
```

### False Positives

**Cause:** Drift threshold too low
**Solution:** Increase threshold or lookback window

```python
# More conservative
monitor = MirrorDriftMonitor(
    drift_threshold=0.3,  # 30% drop required
    lookback_window=10    # More history context
)
```

### Missing Checkpoints

**Cause:** CASCADE not creating checkpoints
**Solution:** Verify checkpoint_manager is enabled

```python
from empirica.core.canonical.empirica_git.checkpoint_manager import auto_checkpoint

# Ensure auto_checkpoint decorator is used in CASCADE
@auto_checkpoint
def investigate_phase(self):
    # ... CASCADE work
```

---

## Implementation Details

### File Structure

```
empirica/core/drift/
├── __init__.py
└── mirror_drift_monitor.py  # Main implementation
```

### Dependencies

```python
# Core dependencies
from empirica.core.canonical.empirica_git.checkpoint_manager import CheckpointManager
from empirica.core.schemas.epistemic_assessment import EpistemicAssessmentSchema

# No external LLM dependencies
# No heuristic libraries
# Pure Python + Git
```

### Git Notes Namespace

```
refs/notes/empirica/checkpoints/
  └── <commit-sha>
      └── {
            "vectors": {...},      # 13 epistemic vectors
            "phase": "CHECK",       # CASCADE phase
            "round_num": 2,         # CASCADE round
            "timestamp": 1234567890
          }
```

---

## Related Documentation

- [GIT_NOTES_CONSOLIDATION_PLAN.md](../../GIT_NOTES_CONSOLIDATION_PLAN.md) - Dual-tier storage architecture
- [GIT_CHECKPOINT_ARCHITECTURE.md](../architecture/GIT_CHECKPOINT_ARCHITECTURE.md) - Checkpoint system
- [UNIFIED_DRIFT_MONITOR_DESIGN.md](../../UNIFIED_DRIFT_MONITOR_DESIGN.md) - Design rationale
- [MIRROR_DRIFT_MONITOR_COMPLETE.md](../../MIRROR_DRIFT_MONITOR_COMPLETE.md) - Implementation summary
- [06_CASCADE_FLOW.md](./06_CASCADE_FLOW.md) - CASCADE workflow
- [05_EPISTEMIC_VECTORS.md](./05_EPISTEMIC_VECTORS.md) - Vector definitions

---

## Future Enhancements

### Phase 2: Cross-Session Drift
```python
# Compare to baseline across multiple sessions
monitor.detect_drift_cross_session(
    current_session='session-2',
    baseline_session='session-1'
)
```

### Phase 3: Inter-Agent Coordination
```python
# Detect drift when resuming another AI's work
monitor.detect_handoff_drift(
    current_ai='ai-2',
    previous_ai='ai-1',
    goal_id='goal-123'
)
```

---

**Status:** ✅ Production-ready
**Heuristics:** None
**External Dependencies:** None
**Storage:** PRIMARY tier (checkpoint_manager)
