# API Page Wireframe

## Page: /api.html

### Purpose
Provide complete API reference for developers integrating Empirica.

---

## Content Structure

### Hero Section
**Headline:** Empirica API Reference  
**Subheadline:** Complete documentation for integrating epistemic awareness into your AI systems.

---

### Section 1: Quick Start API Usage

**Python API:**
```python
from empirica import bootstrap_empirica, assess_epistemic_state

# Initialize
session = bootstrap_empirica(
    session_name="my_task",
    enable_cascade=True
)

# Assess uncertainty before starting
vectors = assess_epistemic_state("Create a complex website")

# Check if investigation is needed
if vectors['explicit_uncertainty'] > 0.7:
    # Trigger cascade for systematic investigation
    results = session.cascade_investigate()
```

**MCP Integration:**
```json
{
  "mcpServers": {
    "empirica": {
      "command": "python",
      "args": ["-m", "empirica.empirica_mcp_server"]
    }
  }
}
```

---

### Section 2: Core APIs

#### Bootstrap API
**Function:** `bootstrap_empirica(session_name, enable_cascade=True, db_path=None)`
- Initializes Empirica session with full tracking
- Returns: Session object with epistemic monitoring

#### Session Management API  
**Functions:**
- `create_session(name)` - Start new session
- `get_session(session_id)` - Retrieve session
- `end_session(session_id)` - Close with final assessment
- `export_session_json(session_id)` - Export for analysis

#### Epistemic Assessment API
**Functions:**
- `assess_epistemic_state(context)` - Get 13-vector assessment
- `get_vector_value(vector_name)` - Single vector query
- `track_vector_change(vector_name, old, new)` - Monitor drift

---

### Section 3: Component APIs

#### Cascade Controller API
**Functions:**
- `initiate_cascade(context)` - Start multi-phase investigation
- `get_cascade_status()` - Check progress
- `get_cascade_results()` - Retrieve findings

**Cascade Phases:**
- Phase 1: Epistemic assessment
- Phase 2: Knowledge gap identification
- Phase 3: Investigation planning
- Phase 4: Evidence gathering

#### Bayesian Guardian API
**Functions:**
- `update_belief(evidence, prior)` - Bayesian update
- `calculate_confidence(data)` - Statistical confidence
- `get_uncertainty_bounds()` - Confidence intervals

#### Drift Monitor API
**Functions:**
- `start_monitoring(vectors)` - Begin drift detection
- `get_drift_events()` - Retrieve detected changes
- `set_drift_threshold(vector, threshold)` - Configure sensitivity

---

### Section 4: MCP Server API

#### Available Tools/Skills
- `empirica.assess` - Epistemic vector assessment
- `empirica.investigate` - Trigger cascade investigation
- `empirica.track` - Log epistemic state change
- `empirica.validate` - Post-flight validation

#### Skill Parameters
Each skill accepts context and configuration parameters documented in `/docs/empirica_skills/`

---

### Section 5: Database Schema

**Tables:**
- `sessions` - Session metadata and state
- `reflex_frames` - Epistemic snapshots over time
- `investigations` - Cascade investigation records
- `drift_events` - Detected state changes
- `vector_history` - Longitudinal vector tracking

**Schema Details:** Link to full schema documentation

---

### Section 6: Configuration API

**Config Options:**
```python
config = {
    'cascade_enabled': True,
    'drift_monitoring': True,
    'auto_investigate_threshold': 0.7,
    'vector_tracking': 'all',  # or specific vectors
    'export_format': 'json',
    'db_path': '.empirica/sessions.db'
}
```

---

### Section 7: Events & Callbacks

**Event Hooks:**
- `on_high_uncertainty` - Triggered when threshold exceeded
- `on_cascade_complete` - Investigation finished
- `on_drift_detected` - Vector changed significantly
- `on_session_end` - Session closing

**Usage:**
```python
session.on_high_uncertainty(lambda vectors: print(f"High uncertainty: {vectors}"))
```

---

### Call-to-Action
- Link to full API documentation in /docs
- Link to code examples on GitHub
- Link to MCP integration guide
