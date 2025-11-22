# CLI Interface - Wireframe

## Page Structure

### Header
- Logo: Empirica
- Primary CTA: "Get Started"
- Secondary CTA: "Empirica MCP"

### Navigation (5 items)
- CLI Interface (active)
- Empirical Confidence
- Components
- Implementation
- Knowledge Base

### Breadcrumbs
Home › Getting Started › CLI Interface

---

## Main Content

### Hero Section
**Title:** Empirica CLI: Direct Epistemic Assessment  
**Subtitle:** Command-line interface for metacognitive AI operations with safety and transparency

---

### CLI Philosophy Section
**Title:** Built for Safety & Collaboration

**Core Principles:**
- **Read-only by default** - Safe for AI exploration
- **Clear feedback** - Every operation shows reasoning
- **Resource protection** - Built-in timeouts and limits
- **Graceful degradation** - Continues working if components fail
- **Human-AI collaboration** - Designed for transparency

---

### Installation Section
**Title:** Quick Setup

```bash
# Install Empirica
cd empirica
pip install -e .

# Verify CLI available
which empirica
# or
python -m empirica.cli --help
```

---

### Core Commands Section
**Title:** Essential CLI Commands

#### Command Grid (6 cards)

**1. cascade**
```bash
empirica cascade "Should I proceed with deployment?"
```
Run full epistemic cascade with 13-vector assessment

**2. assess**
```bash
empirica assess --context ./project
```
Evaluate current epistemic state across all vectors

**3. investigate**
```bash
empirica investigate --topic "authentication flow"
```
Strategic investigation with tool recommendations

**4. monitor**
```bash
empirica monitor --session current
```
Real-time session monitoring and tracking

**5. bootstrap**
```bash
empirica bootstrap --mode optimal
```
Initialize metacognitive capabilities

**6. status**
```bash
empirica status
```
Check system status and configuration

---

### Command Details Section
**Title:** Command Reference

#### `empirica cascade`
**Purpose:** Run complete epistemic cascade flow  
**Options:**
- `--enable-dashboard` - Show real-time tmux visualization
- `--confidence-threshold` - Set minimum confidence level (default: 0.7)
- `--enable-bayesian` - Activate Bayesian Guardian
- `--context` - Provide additional context

**Example:**
```bash
empirica cascade "Refactor auth system?" \
  --enable-dashboard \
  --confidence-threshold 0.75 \
  --context project_dir=./src
```

---

#### `empirica assess`
**Purpose:** 13-vector epistemic assessment  
**Options:**
- `--vectors` - Specific vectors to assess (default: all 13)
- `--output` - Format: json, text, or dashboard (default: text)
- `--context` - Working directory or context

**Example:**
```bash
empirica assess --vectors know,context,clarity --output json
```

---

#### `empirica investigate`
**Purpose:** Strategic investigation with tool mapping  
**Options:**
- `--topic` - Investigation focus
- `--tools` - Specific tools to use
- `--depth` - Investigation depth (1-3, default: 2)

**Example:**
```bash
empirica investigate \
  --topic "database schema" \
  --depth 2
```

---

#### `empirica monitor`
**Purpose:** Session and reflex frame monitoring  
**Options:**
- `--session` - Session ID or "current"
- `--format` - Output format (live, json, summary)
- `--vectors` - Show vector changes

**Example:**
```bash
empirica monitor --session current --format live
```

---

#### `empirica bootstrap`
**Purpose:** Initialize metacognitive system  
**Options:**
- `--mode` - Bootstrap mode: optimal, extended, minimal
- `--skills-dir` - Custom skills directory
- `--auto-track` - Enable automatic tracking

**Example:**
```bash
empirica bootstrap --mode optimal --auto-track
```

---

### CLI Output Examples Section
**Title:** Understanding CLI Output

#### Example 1: Cascade Result
```
🐙 13-Vector Epistemic Cascade
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pre-flight Assessment:
  KNOW:        0.45 ⚠️  - Limited knowledge of current state
  CONTEXT:     0.62 ⚠️  - Partial context available
  CLARITY:     0.78 ✓  - Question well-defined
  CONFIDENCE:  0.52 ⚠️  - Below threshold
  
Recommendation: INVESTIGATE
Rationale: Knowledge gap detected - need to understand current
          authentication implementation before refactoring

Suggested Tools:
  1. code_structure_analyzer
  2. dependency_mapper
  3. test_coverage_assessor

Would you like to proceed with investigation? [y/N]
```

---

#### Example 2: Assessment Output
```
📊 Epistemic State Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Core Epistemic Vectors (8):
  🟢 KNOW:           0.82  High - Strong knowledge base
  🟢 CONTEXT:        0.76  Good - Sufficient context
  🟡 CLARITY:        0.68  Medium - Some ambiguity
  🟢 CONFIDENCE:     0.74  Good - Above threshold
  🟡 PREDICT:        0.65  Medium - Outcome uncertain
  🟢 EXECUTE:        0.79  High - Clear execution path
  🟢 MONITOR:        0.71  Good - Tracking available
  🟡 EXPLAIN:        0.63  Medium - Can explain partially

Advanced Vectors (5):
  🟢 ENGAGE:         0.88  High - Strong engagement
  🟡 JUSTIFY:        0.69  Medium - Evidence building
  🟡 COLLABORATE:    0.66  Medium - Multi-agent capable
  🟢 TEMPORAL:       0.77  Good - Session continuity
  🟢 UNCERTAINTY:    0.73  Good - Explicit awareness

Overall Confidence: 0.73 ✓
Recommendation: PROCEED with monitoring
```

---

### Interactive Mode Section
**Title:** Interactive CLI Session

**Content:**
Launch interactive mode for guided workflows:

```bash
empirica interactive
```

**Interactive Features:**
- Guided cascade execution
- Step-by-step assessment
- Investigation tool selection
- Real-time feedback
- Session history navigation

---

### CLI + Dashboard Section
**Title:** Visual Monitoring with Tmux

**Combined Usage:**
```bash
# Terminal 1: Start dashboard
tmux new -s empirica-dashboard
empirica dashboard start

# Terminal 2: Run cascade with visualization
empirica cascade "Your question" --enable-dashboard

# Dashboard shows:
# - Live vector changes
# - Investigation rounds
# - Bayesian updates
# - Drift detection
# - Phase progression
```

---

### Configuration Section
**Title:** CLI Configuration

**Config File:** `~/.empirica/config.yaml`

```yaml
default_confidence_threshold: 0.7
enable_bayesian: true
enable_drift_monitor: true
auto_start_dashboard: false
session_storage: ~/.empirica/sessions/
log_level: INFO
```

---

### Scripting & Automation Section
**Title:** Using CLI in Scripts

**Example Script:**
```bash
#!/bin/bash
# deployment_check.sh

# Run cascade for deployment decision
RESULT=$(empirica cascade \
  "Deploy to production?" \
  --context environment=staging \
  --confidence-threshold 0.8 \
  --output json)

# Parse JSON result
ACTION=$(echo "$RESULT" | jq -r '.action')

if [ "$ACTION" == "proceed" ]; then
  echo "✓ Cascade approved deployment"
  ./deploy.sh
else
  echo "⚠ Cascade recommends: $ACTION"
  exit 1
fi
```

---

### Troubleshooting Section
**Title:** Common CLI Issues

**Command not found:**
```bash
# Add to PATH or use full path
python -m empirica.cli cascade "question"
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Dashboard not starting:**
```bash
# Check tmux installed
tmux -V

# Start manually
empirica dashboard start --force
```

---

### Next Steps CTA
**Title:** Master the CLI  
**Primary Button:** Try Interactive Mode  
**Secondary Link:** View All Commands  
**Tertiary Link:** Read Python API Documentation

---

## Footer
Standard footer component
