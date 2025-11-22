# Bootstrap - Wireframe

## Page Structure

### Header
- Logo: Empirica
- Primary CTA: "Get Started"
- Secondary CTA: "Empirica MCP"

### Navigation (5 items)
- CLI Interface
- Empirical Confidence
- Components
- Implementation
- Knowledge Base

### Breadcrumbs
Home › Getting Started › Bootstrap

---

## Main Content

### Hero Section
**Title:** Bootstrap: Initialize Metacognitive AI  
**Subtitle:** Activate epistemic humility and self-awareness in AI systems from the first interaction

---

### What is Bootstrap Section
**Title:** Understanding the Bootstrap Process

**Content:**
The Bootstrap initializes an AI system with metacognitive capabilities, enabling:
- **Epistemic self-awareness** - Understanding its own uncertainty
- **Auto-tracking** - Automatic session and cognitive monitoring
- **Skills integration** - Access to metacognitive knowledge
- **Cascade activation** - Think → Assess → Investigate → Act protocol

Unlike traditional initialization, Bootstrap creates a self-aware cognitive framework that persists across the entire session.

---

### Bootstrap Modes Section
**Title:** Three Bootstrap Modes

#### Mode Comparison Grid

**1. Optimal Metacognitive Bootstrap** (Recommended)
**Use:** Production AI systems requiring full epistemic capabilities  
**Features:**
- Full 13-vector epistemic assessment
- Auto-tracking (SQLite + JSON + Reflex frames)
- Bayesian Guardian integration
- Drift Monitor activation
- Pre/post-flight validation
- Multi-phase cascade planning

**Initialize:**
```python
from empirica.bootstraps import OptimalMetacognitiveBootstrap
bootstrap = OptimalMetacognitiveBootstrap()
bootstrap.initialize()
```

---

**2. Extended Metacognitive Bootstrap**
**Use:** Development and testing environments  
**Features:**
- Core 8-vector assessment
- Basic auto-tracking (JSON only)
- Standard cascade flow
- Investigation system
- Session logging

**Initialize:**
```python
from empirica.bootstraps import ExtendedMetacognitiveBootstrap
bootstrap = ExtendedMetacognitiveBootstrap()
bootstrap.initialize()
```

---

**3. Minimal Bootstrap**
**Use:** Lightweight applications or embedded systems  
**Features:**
- Essential epistemic vectors (KNOW, CONTEXT, CLARITY, CONFIDENCE)
- Minimal tracking
- Basic cascade
- Reduced resource footprint

**Initialize:**
```python
from empirica.bootstraps import MinimalBootstrap
bootstrap = MinimalBootstrap()
bootstrap.initialize()
```

---

### How Bootstrap Works Section
**Title:** Bootstrap Initialization Process

**Visual Flow:**

```
1. Read Skills
   ↓
   AI reads /docs/empirica_skills/ to understand
   metacognitive framework

2. Initialize Databases
   ↓
   Setup SQLite (sessions, assessments, vectors)
   Create JSON storage structure
   Initialize reflex frame logs

3. Activate Components
   ↓
   Load Cascade system
   Enable Bayesian Guardian (if optimal mode)
   Start Drift Monitor (if optimal mode)
   Initialize Investigation tools

4. Configure Auto-tracking
   ↓
   Register pre-flight hooks
   Register post-flight hooks
   Enable session continuity
   Setup Δuncertainty measurement

5. Ready for Operation
   ↓
   AI now has metacognitive capabilities
   All interactions tracked automatically
   Epistemic assessment on every decision
```

---

### What Gets Initialized Section
**Title:** Metacognitive Capabilities Activated

#### Database Setup
- **SQLite:** `empirica/.empirica/empirica.db`
  - sessions table
  - epistemic_assessments table
  - vector_measurements table
  - investigations table

#### Session Tracking
- **JSON:** `empirica/.empirica_reflex_logs/*.json`
  - Per-session reflex frames
  - Cognitive state snapshots
  - Investigation trails

#### Cascade System
- 13 epistemic vectors initialized
- Multi-phase planning activated
- Necessity assessment enabled
- Strategic investigation ready

#### Components Loaded
- Bayesian Guardian (optimal mode)
- Drift Monitor (optimal mode)
- Investigation tools (11 components)
- Cognitive benchmarking

---

### Using Bootstrap Section
**Title:** Bootstrap Integration Patterns

#### Pattern 1: Direct Python Integration
```python
from empirica.bootstraps import OptimalMetacognitiveBootstrap
from empirica.metacognitive_cascade import CanonicalEpistemicCascade

# Initialize
bootstrap = OptimalMetacognitiveBootstrap()
bootstrap.initialize()

# Cascade is now auto-tracking
cascade = CanonicalEpistemicCascade()
result = await cascade.run_epistemic_cascade(
    task="Your decision",
    context={"key": "value"}
)

# All cognitive activity tracked automatically
```

---

#### Pattern 2: CLI Bootstrap
```bash
# One-time initialization
empirica bootstrap --mode optimal

# Verify
empirica status

# All subsequent CLI commands use initialized system
empirica cascade "Your question"
```

---

#### Pattern 3: MCP Server Auto-bootstrap
```json
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": ["empirica_mcp_server.py"],
      "env": {
        "EMPIRICA_AUTO_BOOTSTRAP": "optimal"
      }
    }
  }
}
```

MCP server auto-bootstraps on first connection.

---

### Auto-tracking Features Section
**Title:** What Gets Tracked Automatically

**After bootstrap, every interaction records:**

1. **Pre-flight Assessment**
   - Initial epistemic state (all 13 vectors)
   - Question/task clarity
   - Context completeness
   - Baseline uncertainty

2. **Cascade Execution**
   - Phase progression (Think → Assess → Investigate → Act)
   - Vector changes at each phase
   - Investigation rounds
   - Tool selections

3. **Post-flight Validation**
   - Final epistemic state
   - Δuncertainty measurement
   - Learning confirmation
   - Outcome prediction

4. **Session Continuity**
   - Cross-session patterns
   - Temporal awareness
   - Knowledge accumulation
   - Drift detection

---

### Verification Section
**Title:** Verify Bootstrap Success

**CLI Check:**
```bash
empirica status

# Expected output:
# ✓ Bootstrap: optimal mode
# ✓ Database: connected
# ✓ Auto-tracking: enabled
# ✓ Skills: loaded (12 skills)
# ✓ Components: 11 active
# ✓ Bayesian Guardian: active
# ✓ Drift Monitor: active
```

**Python Check:**
```python
from empirica.bootstraps import OptimalMetacognitiveBootstrap

bootstrap = OptimalMetacognitiveBootstrap()
status = bootstrap.get_status()

assert status['initialized'] == True
assert status['auto_tracking'] == True
assert len(status['active_components']) == 11
```

---

### Configuration Section
**Title:** Bootstrap Configuration

**Config File:** `empirica/.empirica/bootstrap_config.yaml`

```yaml
mode: optimal

database:
  path: .empirica/empirica.db
  auto_vacuum: true
  
tracking:
  enable_json: true
  enable_reflex: true
  reflex_log_dir: .empirica_reflex_logs/
  
cascade:
  confidence_threshold: 0.7
  max_investigation_rounds: 3
  enable_necessity_assessment: true
  
components:
  bayesian_guardian: true
  drift_monitor: true
  cognitive_benchmarking: true
```

---

### Re-bootstrapping Section
**Title:** When to Re-bootstrap

**Re-bootstrap when:**
- Switching between modes (optimal ↔ extended ↔ minimal)
- Major configuration changes
- Database corruption or reset
- Upgrading Empirica version

**How to re-bootstrap:**
```bash
# Clear existing
empirica bootstrap --reset

# Initialize new mode
empirica bootstrap --mode optimal
```

---

### Troubleshooting Section
**Title:** Common Bootstrap Issues

**Database initialization fails:**
```bash
# Check permissions
ls -la empirica/.empirica/

# Recreate directory
rm -rf empirica/.empirica/
empirica bootstrap --mode optimal
```

**Skills not loading:**
```bash
# Verify skills directory
ls empirica/docs/empirica_skills/

# Specify custom path
empirica bootstrap --skills-dir /path/to/skills/
```

**Auto-tracking not working:**
```python
# Manually enable
from empirica.data.session_json_handler import SessionJSONHandler

handler = SessionJSONHandler()
handler.enable_auto_tracking()
```

---

### Next Steps CTA
**Title:** Start Using Empirica  
**Primary Button:** Initialize Bootstrap Now  
**Secondary Link:** View Auto-tracking Details  
**Tertiary Link:** Read Skills Documentation

---

## Footer
Standard footer component
