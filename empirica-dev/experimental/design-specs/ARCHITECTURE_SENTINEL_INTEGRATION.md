# Architecture: Empirica + Sentinel Integration

**Date:** 2025-12-02
**Purpose:** Technical specification for integrating Sentinel orchestration into Empirica
**Phase:** Design (Phase 0)

---

## I. SYSTEM ARCHITECTURE

### Current State (Pre-Sentinel)

```
User Input
    ↓
[Choose which CLI: Claude Code / Gemini / Qwen]
    ↓
[CLI runs independently with empirica]
    ↓
Output
```

**Problem:** User chooses model, no coordination, empirica is a library not a platform.

### Target State (With Sentinel)

```
User Input (to Empirica)
    ↓
Empirica (Entry Point)
    ↓
Sentinel Router
├─ Read epistemic state
├─ Query decision history
├─ Assess which model is optimal
└─ Route with epistemic handoff
    ↓
[Model executes: Claude/Gemini/Qwen/etc]
    ↓
[Generate epistemic delta]
    ↓
[Feed back into Sentinel training]
    ↓
Output + Learning Signal
```

**Improvement:** Empirica is the OS, Sentinel is the kernel, models are execution units.

---

## II. COMPONENT INTERFACES

### A. Empirica Core → Sentinel Interface

**Sentinel Needs to Know:**

```python
sentinel_input = {
    "session_id": "uuid",
    "goal_id": "uuid",
    "phase": "INVESTIGATE" | "PLAN" | "IMPLEMENT" | "CHECK" | "POSTFLIGHT",

    "current_epistemic_state": {
        "ENGAGEMENT": 0.9,
        "KNOW": 0.3,
        "DO": 0.4,
        "CONTEXT": 0.2,
        "CLARITY": 0.6,
        "COHERENCE": 0.5,
        "SIGNAL": 0.4,
        "DENSITY": 0.7,
        "STATE": 0.2,
        "CHANGE": 0.3,
        "COMPLETION": 0.1,
        "IMPACT": 0.0,
        "UNCERTAINTY": 0.8
    },

    "goal_description": "Debug authentication system",
    "goal_type": "debugging" | "implementation" | "research" | "verification" | ...,
    "available_models": ["claude", "gemini", "qwen", "claude-code"],

    "context": {
        "recent_success_models": {"gemini": 0.85, "claude": 0.92},
        "domain": "backend",
        "complexity": 0.7,
        "time_pressure": false
    }
}
```

**Sentinel Returns:**

```python
sentinel_decision = {
    "recommended_model": "gemini",
    "confidence": 0.87,
    "alternative_model": "claude",
    "alternative_confidence": 0.78,

    "reasoning": {
        "phase_match": "INVESTIGATE phase → broad exploration needed",
        "epistemic_match": "High uncertainty (0.8) → Gemini research strength",
        "history_match": "Similar goals succeeded with Gemini 85% of time",
        "efficiency": "Cheaper than Claude-Sonnet, sufficient for exploration"
    },

    "epistemic_handoff_template": {
        "goal_id": "uuid",
        "phase": "INVESTIGATE",
        "vectors": {...},
        "narrative": "standard" | "learning" | "technical",
        "fork_recommendation": false,
        "checkpoint_before": true
    },

    "post_execution_expectation": {
        "expected_uncertainty_reduction": 0.3,
        "expected_completion": 0.4,
        "success_probability": 0.87,
        "next_phase_prediction": "PLAN or IMPLEMENT"
    }
}
```

### B. Model Execution → Delta Generation

**Model Returns (with Empirica Metadata):**

```python
execution_result = {
    "model": "gemini-2.0-flash",
    "execution_time_ms": 45000,
    "tokens_used": {
        "input": 2150,
        "output": 1820
    },

    "final_epistemic_state": {
        "ENGAGEMENT": 0.8,
        "KNOW": 0.7,
        "DO": 0.6,
        ...
        "UNCERTAINTY": 0.4
    },

    "output": {...},
    "phase_completed": "INVESTIGATE",
    "success": true
}
```

**Empirica Generates Delta:**

```python
delta_package = {
    "delta_id": "uuid",
    "timestamp": "2025-12-02T10:30:00Z",
    "session_id": "session-xyz",
    "goal_id": "goal-abc",

    "vectors_before": {...},
    "vectors_after": {...},
    "delta": {
        "KNOW": +0.4,
        "UNCERTAINTY": -0.4,
        ...
    },

    "sentinel_decision": {
        "model_recommended": "gemini",
        "confidence": 0.87
    },

    "execution_result": {
        "model_used": "gemini",
        "success": true,
        "time_ms": 45000
    },

    "quality_metrics": {
        "sentinel_match": true,  # Recommended model was used
        "success": true,         # Goal succeeded
        "confidence_change": -0.4,  # Uncertainty reduced
        "quality_score": 0.92
    }
}
```

---

## III. DATA FLOW

### Scenario: Goal Execution with Sentinel Routing

```
┌─────────────────────────────────────────────────────┐
│ 1. Goal Created in Empirica                         │
├─────────────────────────────────────────────────────┤
│ input: {goal_id, goal_description, goal_type}       │
│ output: session_id, created goal                    │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 2. PREFLIGHT Assessment                             │
├─────────────────────────────────────────────────────┤
│ input: goal_id                                      │
│ output: epistemic_vectors (13 dimensions)           │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 3. Query Sentinel: "Which model should I use?"      │
├─────────────────────────────────────────────────────┤
│ input: {goal_type, epistemic_state, phase,         │
│         available_models}                           │
│ output: {recommended_model, confidence,             │
│          handoff_template}                          │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 4. Create Epistemic Handoff                         │
├─────────────────────────────────────────────────────┤
│ input: {goal_id, epistemic_state, phase,           │
│         narrative_type}                             │
│ output: handoff_package (goal + context + vectors) │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 5. Dispatch to Model with Handoff                   │
├─────────────────────────────────────────────────────┤
│ input: {model, handoff_package}                     │
│ output: execution_result                            │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 6. Generate Delta Package                           │
├─────────────────────────────────────────────────────┤
│ input: {before_vectors, after_vectors,             │
│         sentinel_decision, execution_result}       │
│ output: delta_package                               │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 7. Store Delta in Empirica DB + Git                │
├─────────────────────────────────────────────────────┤
│ Delta stored for:                                   │
│  - Sentinel training                                │
│  - Research analysis                                │
│  - Calibration verification                         │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 8. Weekly: Retrain Sentinel                         │
├─────────────────────────────────────────────────────┤
│ input: {all deltas from week}                       │
│ output: Sentinel v0.X (improved router)             │
└─────────────────────────────────────────────────────┘
```

---

## IV. REQUIRED NEW COMPONENTS

### A. Sentinel Router (MCP Tool)

```python
@mcp_tool
def sentinel_route_task(
    session_id: str,
    goal_id: str,
    goal_type: str,
    current_epistemic_state: Dict[str, float],
    phase: str,
    available_models: List[str]
) -> SentinelDecision:
    """
    Route a task to the optimal model based on epistemic state.

    Returns:
    - recommended_model: Best choice given state
    - confidence: 0-1 confidence in recommendation
    - reasoning: Explanation for routing decision
    - handoff_template: Template for epistemic handoff
    """

    # Phase 1: Rule-based routing (until Sentinel SLM is trained)
    if phase == "INVESTIGATE" and epistemic_state["UNCERTAINTY"] > 0.6:
        return SentinelDecision(
            model="gemini",
            confidence=0.8,
            reasoning="High-uncertainty investigation → broad research capability"
        )

    # Phase 2: SLM-based routing (after training)
    # route = sentinel_slm.predict(current_epistemic_state, goal_type, phase)
```

### B. Epistemic Handoff Engine

```python
class EpistemicHandoff:
    """Transfer epistemic context between models/sessions."""

    def create(self, goal_id, epistemic_state, phase, narrative="standard"):
        """Create handoff package for next model."""
        return HandoffPackage(
            goal_id=goal_id,
            epistemic_state=epistemic_state,
            phase=phase,
            findings=self.get_findings(goal_id),
            next_model_hint=None,  # Will be filled by Sentinel
            created_at=now()
        )

    def verify(self, handoff):
        """Verify handoff integrity before dispatch."""
        assert handoff.epistemic_state.valid()
        assert handoff.phase in CASCADE_PHASES
        assert len(handoff.findings) > 0
        return True

    def apply(self, handoff, new_session):
        """Load handoff into new session/model."""
        new_session.goal_id = handoff.goal_id
        new_session.epistemic_state = handoff.epistemic_state
        new_session.phase = handoff.phase
        new_session.findings = handoff.findings
```

### C. Delta Package Generator

```python
class DeltaGenerator:
    """Generate learning signals from executed goals."""

    def create(self, goal_id, before_vectors, after_vectors,
               execution_result, sentinel_decision):
        """Create delta package."""

        delta = {}
        for key in VECTOR_NAMES:
            delta[key] = after_vectors[key] - before_vectors[key]

        return DeltaPackage(
            goal_id=goal_id,
            vectors_before=before_vectors,
            vectors_after=after_vectors,
            delta=delta,

            sentinel_decision={
                "model_recommended": sentinel_decision.model,
                "confidence": sentinel_decision.confidence
            },

            execution_result={
                "model_used": execution_result.model,
                "success": execution_result.success,
                "tokens": execution_result.tokens
            },

            quality_metrics={
                "sentinel_match": (sentinel_decision.model ==
                                   execution_result.model),
                "success": execution_result.success,
                "learning_gain": sum(delta.values()),
                "confidence_change": (after_vectors["UNCERTAINTY"] -
                                      before_vectors["UNCERTAINTY"])
            }
        )

    def store(self, delta):
        """Store in database + git for analysis."""
        db.deltas.insert(delta)
        git.add_note(goal_id, delta.to_json())
```

### D. Sentinel Training Pipeline

```python
class SentinelTrainer:
    """Train routing model on collected deltas."""

    def collect_deltas(self, time_range):
        """Gather all deltas in range."""
        return db.deltas.find(
            created_at > time_range.start,
            created_at < time_range.end
        )

    def prepare_training_data(self, deltas):
        """Convert deltas to training examples."""
        examples = []
        for delta in deltas:
            example = {
                "input": {
                    "phase": delta.phase,
                    "goal_type": delta.goal_type,
                    "epistemic_state": delta.vectors_before,
                    "available_models": delta.available_models
                },
                "output": delta.sentinel_decision.model,
                "label": delta.quality_metrics.success,
                "weight": delta.quality_metrics.confidence
            }
            examples.append(example)
        return examples

    def train(self, examples, learning_rate=0.001):
        """Retrain Sentinel SLM."""
        model = DistilledLanguageModel(
            architecture="small_router",
            size_params=1_000_000_000  # 1B params
        )
        model.train(examples, epochs=5, lr=learning_rate)
        return model

    def evaluate(self, model, validation_set):
        """Test routing accuracy."""
        correct = 0
        for example in validation_set:
            prediction = model.predict(example["input"])
            if prediction == example["output"]:
                correct += 1

        accuracy = correct / len(validation_set)
        print(f"Routing accuracy: {accuracy:.2%}")
        return accuracy

    def deploy(self, model):
        """Make new version live."""
        backup_current()
        update_sentinel_weights(model)
        log_deployment(model)
```

### E. Drift Monitor Integration

```python
class DriftMonitorForSentinel:
    """Watch for model divergence in routing."""

    def compare_models_on_goal(self, goal_id):
        """Run same goal with multiple models."""

        handoff = self.get_handoff(goal_id)
        results = {}

        for model in ["claude", "gemini", "qwen"]:
            result = dispatch(model, handoff)
            results[model] = {
                "final_vectors": result.epistemic_state,
                "success": result.success,
                "tokens_used": result.tokens
            }

        divergence = self.measure_divergence(results)

        if divergence > THRESHOLD:
            alert(f"Models diverged significantly on goal {goal_id}")
            flag_for_investigation()

        return results, divergence

    def measure_divergence(self, results):
        """Quantify how much models disagreed."""
        vectors = {
            k: v["final_vectors"]
            for k, v in results.items()
        }

        # Compute variance across models per vector
        divergence = 0
        for vector_name in VECTOR_NAMES:
            values = [v[vector_name] for v in vectors.values()]
            variance = np.var(values)
            divergence += variance

        return divergence / len(VECTOR_NAMES)
```

---

## V. DATA MODELS

### Session Model (Enhanced)

```python
@dataclass
class Session:
    session_id: str
    ai_id: str
    created_at: datetime

    # Sentinel routing history
    routing_history: List[SentinelDecision]

    # Models used in this session
    models_used: List[str]

    # Epistemic trajectory
    epistemic_snapshots: List[Tuple[str, Dict]]  # (phase, vectors)

    # Deltas generated
    deltas: List[DeltaPackage]

    # Handoffs created
    handoffs: List[EpistemicHandoff]
```

### Goal Model (Enhanced)

```python
@dataclass
class Goal:
    goal_id: str
    session_id: str
    description: str
    goal_type: str  # investigation, implementation, verification, etc.

    # Routing decisions
    sentinel_decisions: List[SentinelDecision]

    # Which models were tried
    execution_history: List[{
        "model": str,
        "phase": str,
        "result": ExecutionResult,
        "delta": DeltaPackage
    }]

    # For forking
    parent_goal: Optional[str]  # If forked
    branches: List[str]  # If parent

    # Final state
    final_epistemic_state: Dict[str, float]
    success: bool
    learning_delta: DeltaPackage
```

---

## VI. INTEGRATION POINTS

### Existing Empirica → Sentinel Connection

**File:** `empirica/cli/command_handlers/routing_commands.py` (NEW)

```python
def route_task_with_sentinel(goal_id, phase, epistemic_state):
    """Query Sentinel for model recommendation."""

    sentinel = get_sentinel_model()  # Load trained router

    decision = sentinel.route(
        goal_id=goal_id,
        phase=phase,
        epistemic_state=epistemic_state,
        available_models=CONFIG.available_models
    )

    return decision
```

### Model Dispatch → Delta Generation

**File:** `empirica/core/execution/model_dispatcher.py` (NEW)

```python
def dispatch_with_delta_tracking(model, handoff, goal_id):
    """Execute goal and generate delta."""

    # Get vectors before
    before_vectors = get_epistemic_state(goal_id)

    # Execute with the model
    result = execute_model(model, handoff)

    # Get vectors after
    after_vectors = get_epistemic_state(goal_id)

    # Generate delta
    delta = delta_generator.create(
        goal_id=goal_id,
        before_vectors=before_vectors,
        after_vectors=after_vectors,
        execution_result=result,
        sentinel_decision=handoff.sentinel_decision
    )

    # Store for training
    delta_generator.store(delta)

    return result, delta
```

---

## VII. DEPLOYMENT STRATEGY

### Local Development (Phase 1)

```
empirica-local/
├── empirica/          (core framework)
├── sentinel-router/   (rule-based routing initially)
├── deltas-db/        (local SQLite)
├── models/           (local model instances)
│   ├── claude-code/
│   ├── gemini-cli/
│   └── qwen-cli/
└── training-pipeline/ (retrain weekly from deltas)
```

### Production (Phase 2+)

```
empirica-cloud/
├── empirica-api/      (REST endpoint)
├── sentinel-service/  (inference server)
├── deltas-db/        (distributed DB)
├── model-pool/       (managed model instances)
├── training-service/ (weekly retraining)
└── cognitive-vault/  (key management)
```

---

## VIII. TESTING STRATEGY

### Unit Tests (Per Component)

```python
# test_sentinel_router.py
def test_high_uncertainty_routing():
    """Verify Sentinel chooses research model for high uncertainty."""
    decision = sentinel.route(
        epistemic_state={"UNCERTAINTY": 0.8, "KNOW": 0.2},
        phase="INVESTIGATE"
    )
    assert decision.model == "gemini"
    assert decision.confidence > 0.75

# test_delta_generator.py
def test_delta_calculation():
    """Verify learning delta is computed correctly."""
    delta = generator.create(
        before_vectors={"KNOW": 0.3, "UNCERTAINTY": 0.8},
        after_vectors={"KNOW": 0.7, "UNCERTAINTY": 0.4}
    )
    assert delta.delta["KNOW"] == 0.4
    assert delta.delta["UNCERTAINTY"] == -0.4
```

### Integration Tests (Full Flow)

```python
# test_e2e_routing.py
def test_goal_with_sentinel_routing():
    """End-to-end: Goal → Sentinel → Model → Delta."""

    # 1. Create goal
    goal = create_goal("Debug auth system")

    # 2. Route with Sentinel
    decision = sentinel.route(goal.id)
    assert decision.model in available_models

    # 3. Execute
    result = execute(decision.model, goal.id)
    assert result.success == True

    # 4. Verify delta created
    delta = get_delta(goal.id)
    assert delta is not None
    assert delta.quality_metrics.success == True
    assert delta.quality_metrics.learning_gain > 0
```

### Sentinel Training Tests

```python
# test_sentinel_training.py
def test_sentinel_learns_from_deltas():
    """Verify Sentinel improves with more deltas."""

    # Train on batch 1 (100 deltas)
    model_v1 = train_sentinel(deltas_batch_1)
    acc_v1 = evaluate(model_v1, validation_set)

    # Train on batch 1 + 2 (200 deltas)
    model_v2 = train_sentinel(deltas_batch_1 + deltas_batch_2)
    acc_v2 = evaluate(model_v2, validation_set)

    # Verify improvement
    assert acc_v2 > acc_v1, "Sentinel should improve with more data"
```

---

## IX. MIGRATION PATH

### Week 1-2: Setup
- Create new components
- Write base implementations
- Setup test infrastructure

### Week 3-4: Integration
- Connect Empirica → Sentinel routing
- Implement delta generation
- Test end-to-end

### Week 5-6: Data Collection
- Run goals through new system
- Collect deltas
- Verify quality

### Week 7-8: Training
- Train first Sentinel SLM
- Evaluate accuracy
- Deploy if good

### Week 9+: Iteration
- More goals → more deltas
- Retrain weekly
- Measure improvement

---

**Status:** Ready for Phase 0 detailed design
**Next:** Architecture review with team
