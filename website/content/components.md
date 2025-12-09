# Components - Empirica System Architecture

**Core modules that power epistemic self-awareness**

[← Back to Architecture](architecture.md) | [System Prompts →](system-prompts.md)

---

## Architecture Overview

Empirica is organized into modular components that work together to provide epistemic transparency:

```
empirica/
├── core/           # Core CASCADE & git operations
├── data/           # Storage (SQLite, git notes, JSON)
├── cli/            # Command-line interface
├── api/            # REST API (future)
├── components/     # Specialized modules
├── dashboard/      # Monitoring & visualization
├── metrics/        # Drift detection & calibration
└── plugins/        # Extensions (Forgejo, etc.)
```

---

## Core Components

### 1. Canonical (CASCADE Workflow)

**Path:** `empirica/core/canonical/`

**Purpose:** Core epistemic assessment and storage

**Key Classes:**

**`GitEnhancedReflexLogger`** - Unified storage logger
- Writes atomically to 3 layers: SQLite + git notes + JSON
- Single API call = all layers updated
- Prevents inconsistency between storage systems

```python
from empirica.core.canonical import GitEnhancedReflexLogger

logger = GitEnhancedReflexLogger(session_id=session_id)
logger.add_checkpoint(
    phase='PREFLIGHT',
    round_num=1,
    vectors={'engagement': 0.8, 'know': 0.6, ...},
    reasoning="Starting assessment"
)
# ✅ Writes to SQLite reflexes + git notes + JSON atomically
```

**Why it matters:** Single source of truth, no storage drift

---

### 2. Session Database (Storage Layer)

**Path:** `empirica/data/session_database.py`

**Purpose:** SQLite persistence and query API

**Key Methods:**

```python
from empirica.data import SessionDatabase

db = SessionDatabase()

# Create session
session_id = db.create_session(ai_id="myai", bootstrap_level=1)

# Store epistemic vectors
db.store_vectors(session_id, phase='PREFLIGHT', vectors={...})

# Query unknowns (for CHECK phase)
unknowns = db.query_unknowns_summary(session_id)

# Get current epistemic state
state = db.get_epistemic_state(session_id)

# Calibration analysis
calibration = db.get_calibration_data(session_id)
```

**Tables:**
- `sessions` - Session metadata
- `reflexes` - Epistemic assessments (13 vectors per phase)
- `goals` - Goal tracking
- `investigation_findings` - Findings/unknowns/dead ends
- `mistakes_log` - Mistake tracking for learning

---

### 3. Git Operations (Continuity Layer)

**Path:** `empirica/core/git_ops/`

**Purpose:** Git notes checkpoints and handoffs

**Key Functions:**

**Checkpoints** (75%+ token reduction)
```python
from empirica.core.git_ops import GitNotesCheckpoint

checkpoint = GitNotesCheckpoint()

# Create checkpoint
checkpoint.create_checkpoint(
    session_id=session_id,
    phase='ACT',
    round_num=1,
    vectors={...},
    metadata={'milestone': 'tests passing'}
)

# Load checkpoint (resume work)
state = checkpoint.load_checkpoint(session_id)
# Returns: phase, round, vectors, metadata, timestamp
```

**Handoffs** (75%+ token reduction)
```python
from empirica.core.handoff import EpistemicHandoffReportGenerator

generator = EpistemicHandoffReportGenerator()

# Create handoff
handoff = generator.generate_handoff_report(
    session_id=session_id,
    task_summary="OAuth2 implementation complete",
    key_findings=["PKCE prevents interception", "Refresh rotation secure"],
    remaining_unknowns=["Revocation at scale"],
    next_session_context="Auth working, next: authorization layer"
)
```

**Storage:** Git notes at `refs/notes/empirica/{checkpoints|handoff}/{session_id}`

---

### 4. Goals & Subtasks (Investigation Tracking)

**Path:** `empirica/core/goals/`

**Purpose:** Track work structure and learning

**Key Classes:**

```python
from empirica.core.goals import GoalManager

manager = GoalManager(session_id=session_id)

# Create goal with scope
goal_id = manager.create_goal(
    objective="Implement OAuth2 authentication",
    scope={
        'breadth': 0.3,  # Single module
        'duration': 0.4,  # Days
        'coordination': 0.1  # Solo work
    },
    success_criteria=["Auth works", "Tests pass"]
)

# Add subtasks
manager.add_subtask(
    goal_id=goal_id,
    description="Research OAuth2 PKCE flow",
    importance='high'
)

# Complete subtask
manager.complete_subtask(
    task_id=task_id,
    evidence="auth/oauth.py:45-120"
)

# Get progress
progress = manager.get_goal_progress(goal_id)
# Returns: completion %, subtask status, findings, unknowns
```

---

### 5. Mirror Drift Monitor (Calibration)

**Path:** `empirica/metrics/drift_detector.py`

**Purpose:** Detect epistemic drift and overconfidence

**Key Functions:**

```python
from empirica.metrics.drift_detector import DriftDetector

detector = DriftDetector(session_id=session_id)

# Detect drift
drift_report = detector.detect_drift(
    current_vectors={'know': 0.5, 'clarity': 0.6, ...},
    previous_vectors={'know': 0.8, 'clarity': 0.85, ...}
)

# Returns:
# {
#   'drift_detected': True,
#   'magnitude': 0.35,
#   'affected_vectors': ['know', 'clarity'],
#   'recommendation': 'INVESTIGATE'
# }
```

**Thresholds:**
- **Minor drift:** 0.15-0.3 (investigate)
- **Major drift:** >0.3 (stop and recalibrate)

**Calibration tracking:** Compares predicted learning (PREFLIGHT) vs actual (POSTFLIGHT)

---

### 6. Edit Guard (Metacognitive Editing)

**Path:** `empirica/components/edit_verification/`

**Purpose:** Prevent 80% of edit failures through epistemic assessment

**How it works:**

```python
from empirica.components.edit_verification import edit_with_confidence

result = edit_with_confidence(
    file_path="myfile.py",
    old_str="def foo():\n    return 42",
    new_str="def foo():\n    return 84",
    context_source="view_output",  # Just read this file
    session_id=session_id  # Optional: calibration tracking
)

# Returns:
# {
#   'ok': True,
#   'strategy': 'atomic_edit',  # or bash_fallback, re_read_first
#   'confidence': 0.92,
#   'reasoning': 'High context freshness, unique pattern...'
# }
```

**Confidence signals:**
1. **CONTEXT** - File read freshness (view_output/fresh_read/memory)
2. **UNCERTAINTY** - Whitespace complexity (tabs/spaces/mixed)
3. **SIGNAL** - Pattern uniqueness (old_str appears exactly once?)
4. **CLARITY** - Truncation risk (old_str length vs typical)

**Strategy selection:**
- ≥0.70 → `atomic_edit` (direct file edit)
- ≥0.40 → `bash_fallback` (sed/awk/python)
- <0.40 → `re_read_first` (re-read then edit)

**Results:** 4.7x higher success rate (94% vs 20%)

---

### 7. Mistakes Tracking (Learning System)

**Path:** `empirica/core/mistakes/`

**Purpose:** Learn from past errors

**API:**

```python
from empirica.core.mistakes import MistakeLogger

logger = MistakeLogger()

# Log mistake
mistake_id = logger.log_mistake(
    session_id=session_id,
    mistake="Started new PREFLIGHT when user gave continuation instructions",
    why_wrong="Misread 'adjust X' as 'fix broken Y'",
    root_cause_vector={'CLARITY': 0.4, 'CONTEXT': 0.5},
    prevention="Check goal status, query handoff for context",
    cost_estimate="10 minutes discussion"
)

# Query mistakes (learn from past)
mistakes = logger.query_mistakes(ai_id="myai", limit=5)
# Returns: Similar mistakes to avoid repeating
```

**Use case:** Before starting work, query past mistakes to avoid known failure patterns

---

### 8. Identity & Cryptographic Signing (Phase 2)

**Path:** `empirica/core/identity/`

**Purpose:** Ed25519 keypairs for AI identity and session signing

**Key Operations:**

```python
from empirica.core.identity import IdentityManager

manager = IdentityManager()

# Create AI identity
manager.create_identity(ai_id="myai", overwrite=False)
# Generates: Ed25519 keypair at ~/.empirica/identities/myai/

# Export public key (for sharing)
public_key = manager.export_public_key(ai_id="myai")

# Sign session (automatic during CASCADE)
# Signature stored in git notes

# Verify session authenticity
verification = manager.verify_signature(session_id=session_id)
# Returns: is_valid, ai_id, timestamp, public_key
```

**Use case:** Multi-AI collaboration with cryptographic proof of authorship

---

## CLI Components

**Path:** `empirica/cli/`

**Purpose:** Command-line interface

**Structure:**
```
cli/
├── main.py                 # Entry point
├── command_handlers/       # Command implementations
│   ├── session_commands.py
│   ├── cascade_commands.py
│   ├── goal_commands.py
│   └── handoff_commands.py
└── mcp_client.py          # MCP server implementation
```

**Key features:**
- Argument parsing and validation
- JSON/default output formats
- Session aliases (latest:active:ai-id)
- Progress indicators

---

## Dashboard Components

**Path:** `empirica/dashboard/`

**Purpose:** Web-based monitoring and visualization

**Features:**
- Real-time epistemic state
- Drift detection alerts
- Goal progress tracking
- Calibration graphs
- Multi-AI comparison

**Status:** Beta (v0.9.0), see `docs/production/11_DASHBOARD_MONITORING.md`

---

## Plugin System

**Path:** `empirica/plugins/`

**Purpose:** Extend Empirica with custom functionality

**Available Plugins:**

**Forgejo Plugin** (`forgejo-plugin-empirica/`)
- Shows epistemic state in git UI
- Git commit annotations
- Repository-level calibration tracking
- Installation: `docs/production/32_FORGEJO_PLUGIN_ARCHITECTURE.md`

**Custom Plugins:**
- Extend base plugin class
- Hook into CASCADE phases
- Access session database
- Guide: `docs/production/14_CUSTOM_PLUGINS.md`

---

## Integration Components

**Path:** `empirica/integration/`

**Purpose:** External system integrations

**Planned:**
- Jupyter notebook integration
- VSCode extension
- GitHub Actions
- CI/CD hooks

---

## Component Dependencies

```
┌──────────────────────────────────────────────┐
│           CLI / MCP / API                     │
└──────────────┬───────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│   Core      │  │ Components  │
│ (CASCADE)   │  │ (Specialized)│
└──────┬──────┘  └──────┬──────┘
       │                │
       └────────┬───────┘
                │
                ▼
       ┌────────────────┐
       │  Data Layer    │
       │ (SQLite + Git) │
       └────────────────┘
```

**Design principles:**
- Loose coupling
- Component independence
- Shared data layer
- No circular dependencies

---

## Testing Components

**Path:** `tests/`

**Structure:**
```
tests/
├── unit/           # Component unit tests
├── integration/    # Cross-component tests
├── e2e/            # End-to-end workflows
└── fixtures/       # Test data
```

**Run tests:**
```bash
# All tests
pytest

# Specific component
pytest tests/unit/test_git_ops.py

# Coverage
pytest --cov=empirica --cov-report=html
```

---

## Next Steps

1. **Explore:** Browse component source code
2. **Extend:** Build custom plugins
3. **Contribute:** Submit improvements
4. **Integrate:** Connect to your tools

**Learn More:**
- [Architecture Overview](architecture.md) - System design
- [Storage Architecture](https://github.com/Nubaeon/empirica/blob/main/docs/architecture/STORAGE_ARCHITECTURE_COMPLETE.md) - Data flow
- [Python API](api-reference.md) - Programmatic access
- [Custom Plugins](https://github.com/Nubaeon/empirica/blob/main/docs/production/14_CUSTOM_PLUGINS.md) - Extend Empirica

---

**Modular design enables customization without compromising core epistemic principles.** 🔧
