# Epistemic Trajectory Visualization: The Flight Path Vision

**Status:** Future Vision / Out of Scope (Circle Back)  
**Date:** 2025-01-29  
**Priority:** HIGH (Killer Feature for Empirica)

---

## Executive Summary

Visualize AI epistemic state as a **4D flight path** through cognitive space:
- **3D Space**: Epistemic vectors (13D reduced to 3D via PCA/UMAP)
- **4th Dimension**: Time (investigation vs action phases)
- **Output**: Navigable trajectory that shows learning, drift, and hallucination prevention in real-time

**The Killer Value:** Users can **watch their AI not crash** - making Empirica's abstract metacognition tangible and demonstrable.

---

## The Problem

Empirica's value is hard to demonstrate:
- "Epistemic self-assessment" sounds fuzzy
- "Drift monitoring" is abstract
- "Hallucination prevention" is invisible

Users need to **see** the AI thinking, catching itself, and course-correcting.

---

## The Vision: Watch Your AI Think

### Without Empirica (The Crash):
```
Trajectory View:
┌─────────────────────────────────────┐
│  ●─────●─────●─────●                │  know: 0.7 → 0.7 (flat)
│              ↘                       │  confidence: 0.8 → 0.9 (rising!)
│                ●────●────💥          │  coherence: 0.6 → 0.3 (DROPPING)
│                         ↑            │  
│                    HALLUCINATION     │  
└─────────────────────────────────────┘
Pattern: Overconfidence + degrading coherence = crash
```

### With Empirica (The Save):
```
Trajectory View:
┌─────────────────────────────────────┐
│  ●─────●─────●                       │  Phase: ACT
│              ↘                       │  coherence drops 0.6→0.4
│                ●🔴                   │  🔴 CHECK triggers
│                 ↓                    │  
│                 ●────●────●          │  Phase: INVESTIGATE (blue)
│                          ↗           │  coherence: 0.4→0.7 (recovered!)
│                           ●──→       │  Phase: ACT (continues safely)
└─────────────────────────────────────┘
Annotation: "Drift detected at T+15min, investigation prevented hallucination"
```

---

## Use Cases

### 1. Real-Time Monitoring
**"See your AI think"**
- Watch epistemic state change as AI works
- Detect drift before hallucination occurs
- Visualize investigation phases (blue) vs action phases (green)
- Risk indicators: hallucination probability, drift magnitude

### 2. Trajectory Replay
**"Learn from past sessions"**
- Replay an AI's problem-solving path
- See where uncertainty spiked → investigation triggered
- Understand why one approach worked vs another
- Educational: "Here's how an expert AI navigates this problem"

### 3. Path Following
**"Navigate like a pro"**
- Find similar past trajectories for current task
- Query: "What did they do when coherence dropped here?"
- Follow proven paths through epistemic space
- Transfer learning across sessions/agents

### 4. Multi-Agent Coordination
**"See agents converging"**
- Real-time view of multiple AI agents in epistemic space
- Convergence detection: "Two agents solving similar problems"
- Divergence alerts: "Agent drifting into high-uncertainty region"
- Handoff visualization: Epistemic state transfer between agents

### 5. Debugging & Analysis
**"What went wrong?"**
- Post-mortem: replay trajectory to crash point
- Compare successful vs failed trajectories
- Identify patterns: "Always crashes when X + Y conditions"
- Calibration analysis: predicted vs actual difficulty

---

## Technical Architecture

### Data We Already Have

Empirica already captures everything needed:

1. **Git Checkpoints** (`empirica/core/canonical/empirica_git/checkpoint_manager.py`)
   ```python
   create_git_checkpoint(
       phase="INVESTIGATE",
       round_num=2,
       vectors={...},  # All 13 epistemic vectors
       metadata={"progress": "50%", "action": "read_codebase"}
   )
   ```

2. **Session Database** (`empirica/data/session_database.py`)
   - Complete session history
   - Phase transitions with timestamps
   - Vector assessments at each checkpoint

3. **Handoff Reports** (`empirica/core/handoff/report_generator.py`)
   - Epistemic snapshots at key waypoints
   - Learning deltas (know: 0.4 → 0.7)

4. **Calibration Reports** (`empirica/calibration/`)
   - Predicted vs actual difficulty
   - Confidence calibration over time

### Data Structure

```python
@dataclass
class EpistemicTrajectoryPoint:
    """Single point in AI's epistemic trajectory"""
    timestamp: float
    phase: str  # PREFLIGHT, INVESTIGATE, ACT, CHECK, POSTFLIGHT
    
    # 13 epistemic vectors (0-1)
    vectors: Dict[str, float]  # engagement, know, do, context, etc.
    
    # 3D position (after dimensionality reduction)
    position_3d: Tuple[float, float, float]
    
    # Context
    action: str  # "read_file", "write_code", "run_tests"
    metadata: Dict[str, Any]
    
    # Derived metrics
    hallucination_risk: float  # 0-1
    drift_magnitude: float      # 0-1
    learning_velocity: float    # Δknow/Δtime

@dataclass
class TrajectorySegment:
    """Connected segment of trajectory (one phase)"""
    start: EpistemicTrajectoryPoint
    end: EpistemicTrajectoryPoint
    phase: str
    duration: float
    risk_events: List[str]  # ["drift_detected", "check_triggered"]
    outcome: str  # "safe", "corrected", "crashed"
    color: str  # For visualization
```

### Implementation Components

#### 1. Trajectory Extraction
```python
# empirica/visualization/trajectory_extractor.py

def extract_trajectory(session_id: str) -> List[EpistemicTrajectoryPoint]:
    """Extract trajectory from git checkpoints + session DB"""
    checkpoints = load_git_checkpoints(session_id)
    session_data = load_session_data(session_id)
    
    points = []
    for cp in checkpoints:
        point = EpistemicTrajectoryPoint(
            timestamp=cp.timestamp,
            phase=cp.phase,
            vectors=cp.vectors,
            position_3d=reduce_dimensions(cp.vectors),  # PCA/UMAP
            action=cp.metadata.get('action'),
            metadata=cp.metadata,
            hallucination_risk=calculate_hallucination_risk(cp),
            drift_magnitude=calculate_drift(cp, previous_point),
            learning_velocity=calculate_learning_velocity(points, cp)
        )
        points.append(point)
    
    return points
```

#### 2. Dimensionality Reduction
```python
# empirica/visualization/dimension_reducer.py

def reduce_dimensions(vectors: Dict[str, float]) -> Tuple[float, float, float]:
    """Reduce 13D epistemic space to 3D for visualization"""
    
    # Option 1: PCA (linear, preserves global structure)
    pca = PCA(n_components=3)
    position_3d = pca.fit_transform([list(vectors.values())])
    
    # Option 2: UMAP (non-linear, preserves local structure)
    # Better for clustering similar epistemic states
    umap = UMAP(n_components=3)
    position_3d = umap.fit_transform([list(vectors.values())])
    
    # Option 3: Custom mapping (semantic axes)
    # X: knowledge (know, context, clarity)
    # Y: confidence (do, confidence, uncertainty inverse)
    # Z: coherence (coherence, signal, state)
    
    return tuple(position_3d[0])
```

#### 3. Risk Detection
```python
# empirica/visualization/risk_calculator.py

def calculate_hallucination_risk(point: EpistemicTrajectoryPoint) -> float:
    """Real-time hallucination risk (0-1)"""
    
    # Pattern 1: High confidence + low coherence
    overconfidence = max(0, point.vectors['confidence'] - 0.8) * 2
    low_coherence = max(0, 0.5 - point.vectors['coherence']) * 2
    pattern1 = overconfidence * low_coherence
    
    # Pattern 2: Flat knowledge + increasing completion (false progress)
    if has_recent_history(point):
        know_velocity = compute_velocity(point, 'know')
        completion_velocity = compute_velocity(point, 'completion')
        if know_velocity < 0.1 and completion_velocity > 0.3:
            pattern2 = 0.7
        else:
            pattern2 = 0.0
    else:
        pattern2 = 0.0
    
    # Pattern 3: Low uncertainty despite low context (false certainty)
    if point.vectors['uncertainty'] < 0.3 and point.vectors['context'] < 0.5:
        pattern3 = 0.6
    else:
        pattern3 = 0.0
    
    return min(1.0, pattern1 + pattern2 + pattern3)

def calculate_drift(current: EpistemicTrajectoryPoint, 
                   previous: EpistemicTrajectoryPoint) -> float:
    """Calculate epistemic drift magnitude"""
    
    # Vector-space distance
    vector_diff = {
        k: abs(current.vectors[k] - previous.vectors.get(k, 0))
        for k in current.vectors
    }
    
    # Weight critical vectors more
    weights = {
        'coherence': 2.0,   # Coherence drop = high drift
        'signal': 1.5,      # Signal degradation = drift
        'clarity': 1.5,
        'context': 1.0,
        # ... others default 1.0
    }
    
    weighted_drift = sum(
        vector_diff[k] * weights.get(k, 1.0)
        for k in vector_diff
    )
    
    return min(1.0, weighted_drift / len(vector_diff))
```

---

## Visualization Design

### Real-Time Dashboard

```
╔══════════════════════════════════════════════════════════╗
║  EMPIRICA LIVE VIEW - Session: abc123                    ║
╠══════════════════════════════════════════════════════════╣
║                                                           ║
║  [3D Trajectory Visualization - Interactive]             ║
║  • Rotate/zoom with mouse                                ║
║  • Click points for details                              ║
║  • Color: Blue=INVESTIGATE, Green=ACT, Red=CHECK         ║
║  • Width: Confidence level                               ║
║  • Glow: Risk level                                      ║
║                                                           ║
║  Current Position:     ●  [Phase: ACT]                   ║
║  ├─ Know: 0.82 ████████░░                               ║
║  ├─ Confidence: 0.76 ███████░░░                         ║
║  ├─ Coherence: 0.71 ███████░░░                          ║
║  └─ Uncertainty: 0.28 ███░░░░░░░                        ║
║                                                           ║
║  Status: ✅ SAFE ZONE                                    ║
║                                                           ║
║  Last 10 minutes:                                        ║
║  ● 15:30 - Investigation completed (+0.3 knowledge)      ║
║  ● 15:25 - 🔴 Drift detected (coherence drop)           ║
║  ● 15:20 - CHECK phase triggered                        ║
║                                                           ║
║  Risk Indicators:                                        ║
║  ⚠️  Hallucination Risk:  LOW (12%) ███░░░░░░░          ║
║  ⚠️  Drift Risk:          LOW (8%)  ██░░░░░░░░          ║
║  ✅  Learning Rate:       GOOD (0.4 Δknow/hour)         ║
║                                                           ║
║  [Timeline Slider] ════●═════════════════ [Now]          ║
║                                                           ║
╚══════════════════════════════════════════════════════════╝
```

### Visual Encoding

**Color by Phase:**
- 🔵 Blue: INVESTIGATE (learning, exploring)
- 🟢 Green: ACT (executing, building)
- 🔴 Red: CHECK (assessing, deciding)
- 🟡 Yellow: PREFLIGHT (planning)
- 🟣 Purple: POSTFLIGHT (reflecting)

**Line Width:**
- Thick: High confidence
- Thin: Low confidence

**Glow/Pulsing:**
- Red glow: High hallucination risk
- Yellow glow: Drift detected
- No glow: Safe operation

**Annotations:**
- Key events (drift detected, investigation triggered)
- Learning milestones (+0.3 knowledge)
- Risk events prevented

**3D Axes (Semantic Mapping):**
- X-axis: Knowledge (know, context, clarity)
- Y-axis: Confidence (confidence, do, certainty)
- Z-axis: Coherence (coherence, signal, state)

### Technology Stack

**Backend:**
- FastAPI endpoint: `/api/trajectory/{session_id}`
- WebSocket: Real-time updates
- Data: Extract from git notes + session DB

**Frontend:**
- Three.js: 3D rendering
- D3.js: Timeline and 2D overlays
- React: Dashboard UI

**Libraries:**
- scikit-learn: PCA/dimensionality reduction
- UMAP-learn: Non-linear projection
- NumPy: Vector calculations

---

## The Killer Demo

### Demo Script: "Watch Hallucination Get Stopped"

**Split Screen: With vs Without Empirica**

```
LEFT: AI Without Empirica          RIGHT: AI With Empirica
┌────────────────────────┬────────────────────────┐
│ 0:00 - Start task      │ 0:00 - Start task      │
│ 0:15 - Confident       │ 0:15 - Confident       │
│ 0:30 - Making changes  │ 0:30 - Coherence drops │
│ 0:45 - Adding features │ 0:45 - 🔴 Drift alert  │
│ 1:00 - Tests failing   │ 1:00 - INVESTIGATE     │
│ 1:15 - Doubling down   │ 1:15 - Learning        │
│ 1:30 - More failures   │ 1:30 - Gap identified  │
│ 2:00 - Complete mess   │ 2:00 - ACT (correct)   │
│ 💥 CRASHED             │ ✅ SOLVED              │
└────────────────────────┴────────────────────────┘

Metrics:
Without: 47min wasted, 0 learning, broken code
With: 12min investigation, +0.4 knowledge, working code
```

**Key Moments to Highlight:**

1. **T+30s**: Both confident, making progress
2. **T+45s**: LEFT continues confidently, RIGHT detects coherence drop
3. **T+1m**: LEFT tests fail (ignores), RIGHT triggers CHECK
4. **T+1m15s**: LEFT adds more broken code, RIGHT enters INVESTIGATE
5. **T+1m30s**: LEFT stuck in loop, RIGHT identifies knowledge gap
6. **T+2m**: LEFT gives up, RIGHT solves correctly

**Visual Highlight:**
- Show trajectories side-by-side
- RED path veers into "crash zone" (red cloud overlay)
- BLUE path arcs away, through investigation, back to safe zone
- Annotation: "Investigation saved 35 minutes + prevented broken code"

---

## Implementation Phases

### Phase 1: Data Extraction (2-3 days)
- Extract trajectories from git checkpoints
- Parse session database for phase transitions
- Build TrajectoryPoint data structure
- Basic dimensionality reduction (PCA)

### Phase 2: Risk Calculation (2-3 days)
- Implement hallucination risk detector
- Drift magnitude calculation
- Learning velocity metrics
- Test on historical sessions

### Phase 3: Basic 2D Visualization (3-5 days)
- Simple 2D plot (matplotlib or plotly)
- Timeline view with risk indicators
- Proof of concept: Show one session trajectory
- Validate visual encoding makes sense

### Phase 4: 3D Interactive Dashboard (1-2 weeks)
- Three.js 3D rendering
- Interactive controls (rotate, zoom, click)
- Real-time WebSocket updates
- Timeline slider and playback

### Phase 5: Multi-Agent View (1 week)
- Show multiple agents simultaneously
- Convergence detection UI
- Handoff visualization
- Coordination features

### Phase 6: Path Following API (1 week)
- Trajectory search: Find similar paths
- Context retrieval: What did they do here?
- Recommendation engine: Suggest next steps
- Learning transfer features

---

## Success Metrics

**User Understanding:**
- "I can see why Empirica helps" (qualitative feedback)
- Reduced "what is this doing?" support questions
- Increased adoption after seeing demo

**Technical Validation:**
- Hallucination risk correlates with actual errors (>0.8 correlation)
- Drift detection predicts CHECK triggers (>0.9 accuracy)
- Trajectory similarity predicts problem similarity (>0.7)

**Business Impact:**
- Demo conversion rate increases
- "Aha moment" happens in first 2 minutes
- Users share visualizations (social proof)

---

## Open Questions

1. **Dimensionality Reduction:**
   - PCA (linear) vs UMAP (non-linear) vs custom semantic axes?
   - How to make 3D projection interpretable?
   - Can we label the axes meaningfully?

2. **Real-Time Performance:**
   - How often to sample trajectory points?
   - Can we do dimensionality reduction in real-time?
   - WebSocket update frequency?

3. **Multi-Agent Scale:**
   - How many agents can we show simultaneously?
   - Clustering vs individual trajectories?
   - How to handle 100+ active agents?

4. **Path Matching:**
   - Distance metric in epistemic space?
   - How to weight different vectors?
   - Time-series similarity (DTW, Frechet distance)?

5. **Privacy:**
   - What if trajectory reveals proprietary problem-solving?
   - Anonymization for shared trajectories?
   - Public vs private trajectory database?

---

## Related Work

**Similar Concepts:**
- DeepMind's AlphaGo move visualization
- Tesla's Autopilot visualization
- GitHub Copilot's confidence indicators
- Debugging visualizations (time-travel debugging)

**Unique to Empirica:**
- Multi-dimensional epistemic state (not just "confidence")
- Phase-based color coding (investigate vs act)
- Drift detection and correction visualization
- Multi-agent coordination view

---

## Future Extensions

### Comparative Analysis
- Overlay multiple trajectories
- "Expert path" vs "my path"
- Success pattern identification

### Predictive Guidance
- "You're entering a risk zone"
- "Similar trajectories investigated here"
- Real-time suggestions based on past paths

### Collaborative Features
- Share trajectories with team
- "Follow this AI's approach"
- Trajectory diff: What did they do differently?

### Educational Use Cases
- Teaching AI how to think metacognitively
- Case studies: "How to handle uncertainty"
- Pattern library: Common trajectories for common problems

---

## Marketing Value

**Tagline:** "See your AI think. Watch it not crash."

**Key Messages:**
1. **Visibility**: Metacognition is no longer a black box
2. **Prevention**: Watch hallucination get stopped in real-time
3. **Learning**: See knowledge accumulate over time
4. **Trust**: Transparent AI reasoning builds confidence

**Demo Moments:**
- "Here's where most AIs crash" (red zone)
- "Watch Empirica catch it" (drift alert)
- "Investigation saves the day" (blue arc to safety)
- "Problem solved, knowledge gained" (green completion)

This is THE feature that makes Empirica's value immediately tangible.

---

## Next Steps (When We Circle Back)

1. **Prototype trajectory extraction** from existing git checkpoints
2. **Build simple 2D visualization** to validate concept
3. **Test risk calculations** on historical sessions
4. **Get user feedback** on visual encoding
5. **Plan full 3D implementation** with Three.js

**Estimated Total Effort:** 4-6 weeks for full implementation

**Priority:** HIGH - This is a killer feature that makes abstract metacognition concrete and demonstrable.

---

**Status:** VISION DOCUMENTED - Ready for future implementation  
**Location:** `docs/architecture/EPISTEMIC_TRAJECTORY_VISUALIZATION.md`  
**Tags:** #visualization #killer-feature #hallucination-prevention #drift-monitoring #future-work
