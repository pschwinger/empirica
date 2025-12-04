# Statusline Signals - Live Demonstration

## Overview

The Empirica statusline displays **Tier 1 metacognitive signals** - real-time indicators of an AI's epistemic state during CASCADE workflows. This document demonstrates how all 4 display modes work with real data from an actual CASCADE session.

## Real Session Data

- **Session ID**: `291e0f6d-5361-4412-ad21-bd0162881446`
- **AI ID**: `claude-code`
- **Duration**: 145.3 seconds
- **Phases**: PREFLIGHT → CHECK → POSTFLIGHT
- **Status**: Completed

### CASCADE Phases Captured

```
✓ PREFLIGHT      (1 assessment)
✓ CHECK          (1 assessment)
✓ POSTFLIGHT     (1 assessment)
```

### Learning Trajectory

| Phase      | KNOW | DO   | CONTEXT | COMPLETION |
|------------|------|------|---------|------------|
| PREFLIGHT  | 0.75 | 0.80 | 0.70    | 0.00       |
| CHECK      | 0.70 | 0.75 | 0.75    | 0.50       |
| POSTFLIGHT | 0.90 | 0.92 | 0.85    | 1.00       |

**Learning Deltas**: KNOW +0.15 | COMPLETION +1.00

---

## Display Modes

### 1. MINIMAL MODE
*Intended for: Extreme space constraints, embedded displays*

```
[empirica] [POSTFLIGHT]
```

**Components**:
- `[empirica]` - Green status indicator
- `[POSTFLIGHT]` - Current CASCADE phase in blue

**Information density**: Very low (2 items)

---

### 2. BALANCED MODE (Recommended)
*Intended for: Standard Claude Code statusline use*

```
[empirica] │ POSTFLIGHT │ → VEL:0.0/hr │ COMPLETION↑1.00
```

**Components**:
- `[empirica]` - Green status indicator
- `POSTFLIGHT` - Blue phase indicator
- `→ VEL:0.0/hr` - Progress velocity (steady trend)
- `COMPLETION↑1.00` - Top learning delta (green for positive)

**Information density**: Moderate (4 items) - the "goldilocks" setting

**Signal Priority**:
1. Drift warnings (if detected) - shown in red
2. Cognitive load (if overwhelmed) - shown in red/yellow
3. Scope stability (if creeping/runaway) - shown in red/yellow
4. Velocity (if meaningful data) - shows acceleration/slowing trends
5. Top learning delta - shows what AI learned most about

---

### 3. LEARNING MODE
*Intended for: Researchers, metacognitive analysis, learning calibration*

```
[empirica] │ POSTFLIGHT │ →0.0/hr │ C↑1.00 I↑0.25 C↑0.20
```

**Components**:
- `[empirica]` - Cyan status indicator (learning-focused)
- `POSTFLIGHT` - Phase name
- `→0.0/hr` - Velocity (no significant acceleration)
- `C↑1.00 I↑0.25 C↑0.20` - Top 3 learning deltas
  - C = COMPLETION (improved by 1.00)
  - I = IMPACT (improved by 0.25)
  - C = CLARITY (improved by 0.20)

**Information density**: High - shows learning vectors

**Shows**: Epistemic calibration, what changed from PREFLIGHT to POSTFLIGHT

---

### 4. FULL MODE
*Intended for: Debugging, comprehensive monitoring, training data collection*

```
[empirica:claude-code@291e] │ POSTFLIGHT │ U:0.10 C:0.95 K:0.90 │ →0.0/hr │ C↑1.00 I↑0.25
```

**Components**:
- `[empirica:claude-code@291e]` - AI identity and session ID
- `POSTFLIGHT` - Phase
- `U:0.10 C:0.95 K:0.90` - Key epistemic vectors
  - U = UNCERTAINTY (0.10 = very confident)
  - C = CLARITY (0.95 = very clear)
  - K = KNOW (0.90 = deep domain knowledge)
- `→0.0/hr` - Velocity trend
- `C↑1.00 I↑0.25` - Learning deltas

**Information density**: Very high - all key data

---

## Signal Explanations

### What Each Signal Means

#### 1. Phase Indicator (PREFLIGHT / CHECK / POSTFLIGHT)
- **PREFLIGHT**: AI is assessing baseline before work
- **CHECK**: AI is validating progress mid-workflow
- **POSTFLIGHT**: AI is calibrating learning after completion

#### 2. Velocity (VEL:X.X/hr)
- Shows tasks completed per hour
- `↗️ accelerating` - AI gaining momentum
- `↘️ slowing` - AI hitting obstacles
- `→ steady` - Consistent progress
- `VEL:0.0/hr` - Too few tasks or too short timespan to measure (not error)

#### 3. Learning Deltas (VECTOR↑/↓VALUE)
- `↑` = Positive learning (knowledge increased)
- `↓` = Negative learning (uncertainty increased)
- Green = Good (positive delta)
- Gray = Neutral/Negative
- Shows what changed most from PREFLIGHT to POSTFLIGHT

#### 4. Epistemic Vectors (Full Mode)
- **U (UNCERTAINTY)**: 0=confident, 1=confused
- **C (CLARITY)**: 0=unclear requirements, 1=crystal clear
- **K (KNOW)**: 0=novice, 1=expert

Colors:
- Green (good): ✓ High clarity, high know, low uncertainty
- Yellow (caution): ⚠️ Medium values
- Red (alert): 🔴 Low clarity, low know, high uncertainty

---

## Why Velocity is 0.0/hr

In this session, the 2 completed tasks were only 4.2 seconds apart:

```
Task 1 completed: 1764857388.5
Task 2 completed: 1764857392.7
Time span: 4.2 seconds
```

**Statusline logic**:
```
if time_span < 10 seconds:
    show VEL:0.0/hr (not meaningful)
else:
    calculate: (num_tasks / time_span) * 3600
```

This is **intentional** - prevents spurious metrics from instant completions.

**To see real velocity**: Tasks need to be spread over >10 seconds of actual work.

---

## Configuration

Set display mode with environment variable:

```bash
# Minimal
EMPIRICA_STATUS_MODE=minimal python3 statusline_empirica.py

# Balanced (default)
EMPIRICA_STATUS_MODE=balanced python3 statusline_empirica.py

# Learning
EMPIRICA_STATUS_MODE=learning python3 statusline_empirica.py

# Full
EMPIRICA_STATUS_MODE=full python3 statusline_empirica.py
```

Or set in Claude Code `.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "EMPIRICA_STATUS_MODE=balanced python3 /path/to/statusline_empirica.py",
    "padding": 0
  }
}
```

---

## Understanding Signal Combinations

### Example 1: Positive Learning
```
[empirica] │ POSTFLIGHT │ → VEL:2.3/hr │ KNOW↑0.25
```
**Interpretation**:
- AI completing tasks at 2.3/hour
- Learned +0.25 on KNOW vector
- ✅ Good progress

### Example 2: Drift Warning
```
[empirica] │ CHECK │ 🔴 DRIFT:0.35 [CHECK BREADCRUMBS!]
```
**Interpretation**:
- 0.35 drop in multiple vectors (likely memory loss)
- 🚨 Critical - should review decision points
- ❌ Red alert

### Example 3: High Load
```
[empirica] │ CHECK │ ⚠️ LOAD:0.8 [CHECKPOINT?]
```
**Interpretation**:
- Cognitive load very high (DENSITY 0.8)
- 🟡 Yellow caution - consider checkpointing
- ⚠️ Medium priority

---

## Data Reliability

All signals are calculated from **real CASCADE data**:

✅ **Persisted to database** (SQLite):
- Sessions table
- Cascades table (WITH epistemicassessments)
- Goals table
- Subtasks table

✅ **Also backed up** (Git Notes):
- `empirica/session/<session_id>/<phase>/<round>`
- Preserved for cross-AI discovery

✅ **JSON logs** (for analysis):
- Checkpoint JSON files
- Timestamped for correlation

---

## Next Steps for More Signals

### Tier 2 Signals (Future)
1. **Coherence Tracking** - Are decisions logically consistent?
2. **Confidence Trajectory** - Is AI getting more/less certain over time?
3. **Question Quality Evolution** - Are questions getting better/worse?
4. **Decision Quality** - Success rate of recommendations

### Tier 3 Signals (Advanced)
1. **Pattern Recognition** - Multi-vector correlation analysis
2. **Baseline Comparison** - Drift vs normal variance
3. **Cross-AI Learning** - Comparing trajectories between AIs
4. **Prediction Accuracy** - Can we predict next phase vector values?

---

## Validation Checklist

- ✅ All 3 CASCADE phases persisting to database
- ✅ Learning deltas calculated correctly (PREFLIGHT → POSTFLIGHT)
- ✅ Confidence progression tracking uncertainty properly
- ✅ Velocity algorithm excluding spurious data (<10s timespan)
- ✅ All 4 display modes rendering without errors
- ✅ Session replay mechanism working (temporal relationships preserved)
- ✅ MirrorDriftMonitor checkpoint loading fixed
- ✅ Real epistemic vectors displayed accurately

---

## Status

🎉 **Live and operational** - Statusline is displaying real Tier 1 metacognitive signals with actual CASCADE data from the database.

The system now provides genuine visibility into an AI's epistemic state during reasoning, allowing both the AI and humans to detect:
- Learning progress
- Confidence changes
- Cognitive load
- Scope creep
- Memory drift

This enables **real metacognitive awareness** - not simulated, but based on actual assessment data persisted in the CASCADE workflow.
