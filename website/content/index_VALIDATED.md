# Empirica: Metacognitive AI Framework

**Production-grade epistemic reasoning system for AI self-awareness**

Measure and validate AI knowledge state through genuine LLM-powered self-assessment across 13 epistemic dimensions.

[Get Started](getting-started.md) | [View on GitHub](https://github.com/Nubaeon/empirica) | [Documentation](api-reference.md)

---

## What is Empirica?

Empirica is a **metacognitive AI framework** that helps AI systems measure and validate their knowledge state without interfering with their internal reasoning processes.

### Core Philosophy

> "Eliminating heuristics and getting AIs to measure and validate without interfering with their internal systems."

### Key Differentiators

- **Genuine Self-Assessment** - LLM-powered reasoning, not keyword matching or heuristics
- **13-Vector Epistemic System** - Comprehensive knowledge state measurement
- **CASCADE Workflow** - Systematic 7-phase epistemic reasoning process
- **Explicit Uncertainty Tracking** - "Know what you don't know" measurement
- **Production-Ready** - SQLite + JSON + Git notes persistence

---

## The 13 Epistemic Vectors

Empirica's core innovation: comprehensive self-assessment across 13 dimensions.

[Read full Epistemics Guide →](epistemics.md)

### Gate: ENGAGEMENT (≥0.60 required)
- Collaborative intelligence quality
- Prerequisite for all assessments

### Foundation (35% weight)
1. **KNOW** - Domain knowledge confidence
2. **DO** - Execution capability assessment
3. **CONTEXT** - Environmental awareness

### Comprehension (25% weight)
4. **CLARITY** - Task understanding
5. **COHERENCE** - Logical consistency
6. **SIGNAL** - Information quality
7. **DENSITY** - Complexity management

### Execution (25% weight)
8. **STATE** - Current readiness
9. **CHANGE** - Progress tracking
10. **COMPLETION** - Goal proximity
11. **IMPACT** - Consequence awareness

### Meta-Epistemic
12. **UNCERTAINTY** - Explicit uncertainty measurement
13. **CALIBRATION** - Confidence vs accuracy tracking (POSTFLIGHT)

### Critical Thresholds

```python
ENGAGEMENT_THRESHOLD = 0.60  # Gate - must pass to proceed
COHERENCE_CRITICAL = 0.50    # < 0.50 → RESET (task incoherent)
DENSITY_CRITICAL = 0.90      # > 0.90 → RESET (cognitive overload)
CHANGE_CRITICAL = 0.50       # < 0.50 → STOP (cannot progress)
UNCERTAINTY_HIGH = 0.80      # > 0.80 → INVESTIGATE (high uncertainty)
```

**Source:** `empirica/core/canonical/reflex_frame.py`

---

## CASCADE Workflow

Empirica implements a canonical 7-phase epistemic cascade:

```
PREFLIGHT → THINK → PLAN → INVESTIGATE → CHECK → ACT → POSTFLIGHT
```

[See Architecture Details →](architecture.md)

### Phase Descriptions

**1. PREFLIGHT** - Initial epistemic assessment
- Assess all 13 vectors before starting
- Identify knowledge gaps and uncertainties
- Check ENGAGEMENT gate (≥0.60)
- Decision: proceed, investigate, or clarify

**2. THINK** - Task analysis
- Understand task requirements
- Classify domain (code_analysis, security, etc.)
- Identify constraints and dependencies
- Activate Bayesian Guardian if precision-critical

**3. PLAN** - Strategy formulation
- Develop investigation strategy
- Plan execution approach
- Identify required tools and resources
- Create structured completion path

**4. INVESTIGATE** - Knowledge gathering (Optional)
- Systematic information collection
- Fill identified knowledge gaps
- Update epistemic state
- Max 3 investigation rounds

**5. CHECK** - Validation
- Reassess epistemic state
- Detect Bayesian discrepancies
- Monitor for behavioral drift
- Decision: proceed or loop to INVESTIGATE

**6. ACT** - Confident execution
- Execute task with learned knowledge
- Track actions and decisions
- Log to Reflex Frame

**7. POSTFLIGHT** - Learning & calibration
- Reassess all 13 vectors
- Measure epistemic delta (PREFLIGHT vs POSTFLIGHT)
- Validate calibration accuracy
- Generate handoff report for session continuity

### Code Example

```python
from empirica.core.metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade

# Initialize CASCADE
cascade = CanonicalEpistemicCascade(
    enable_bayesian=True,        # Evidence-based belief tracking
    enable_drift_monitor=True,   # Behavioral integrity monitoring
    enable_action_hooks=True     # tmux dashboard integration
)

# Run epistemic cascade
result = await cascade.run_epistemic_cascade(
    task="Analyze codebase for security vulnerabilities",
    context={"cwd": "/project", "domain": "security"}
)

# Results
print(f"Action: {result['action']}")              # proceed, investigate, clarify, reset, stop
print(f"Confidence: {result['confidence']:.2f}")  # 0.0-1.0
print(f"Knowledge Gaps: {result['knowledge_gaps']}")
print(f"Epistemic Delta: {result.get('epistemic_delta', {})}")  # PREFLIGHT vs POSTFLIGHT
```

**Timing:** 5-45 seconds depending on investigation needs
- Fast path (high confidence): ~5-10 seconds
- Normal path (1-2 investigation rounds): ~15-25 seconds
- Deep investigation (3 rounds): ~35-45 seconds

---

## MCP Server Integration

Empirica provides **23 MCP tools** for Claude Desktop integration.

[View MCP Integration Guide →](mcp-integration.md)

### Architecture
- **Thin CLI wrapper** - Routes to Empirica CLI for reliability
- **3 stateless tools** - Handled directly (introduction, guidance, help)
- **20 stateful tools** - Routed through CLI subprocess

### MCP Tools (Complete List)

**Workflow (10 tools):**
1. `bootstrap_session` - Initialize session
2. `execute_preflight` - PREFLIGHT assessment
3. `submit_preflight_assessment` - Submit vectors
4. `execute_check` - CHECK phase
5. `submit_check_assessment` - Submit check vectors
6. `execute_postflight` - POSTFLIGHT assessment
7. `submit_postflight_assessment` - Submit postflight vectors
8. `create_goal` - Create structured goal
9. `add_subtask` - Add subtask to goal
10. `complete_subtask` - Mark subtask complete

**Session Management (5 tools):**
11. `get_epistemic_state` - Current state
12. `get_session_summary` - Session summary
13. `get_calibration_report` - Calibration analysis
14. `resume_previous_session` - Resume sessions
15. `list_goals` - List session goals

**Continuity (5 tools):**
16. `create_git_checkpoint` - Git notes checkpoint (97.5% token reduction)
17. `load_git_checkpoint` - Load checkpoint
18. `create_handoff_report` - 98% token reduction
19. `query_handoff_reports` - Query reports
20. `get_goal_progress` - Goal progress

**Help (3 tools):**
21. `get_empirica_introduction` - Framework intro
22. `get_workflow_guidance` - Phase guidance
23. `cli_help` - CLI command help

### CLI Commands

50+ commands available via `empirica` CLI. [View CLI Reference →](cli-interface.md)

```bash
# Bootstrap
empirica session-create --ai-id=your-id --level=2

# Workflow
empirica preflight --session-id=latest:active:your-id --prompt="Task"
empirica preflight-submit --session-id=latest --vectors='{...}'
empirica check --session-id=latest --findings='[...]' --unknowns='[...]' --confidence=0.8
empirica postflight --session-id=latest
empirica postflight-submit --session-id=latest --vectors='{...}'

# Goals
empirica goals-create --session-id=latest --objective="..." --scope=session_scoped
empirica goals-add-subtask --goal-id=<id> --description="..."
empirica goals-complete-subtask --task-id=<id>

# Session Management
empirica sessions-list
empirica sessions-show latest:active:your-id
empirica sessions-resume --ai-id=your-id --count=1

# Checkpoints
empirica checkpoint-create --session-id=latest --phase=ACT --round=1
empirica checkpoint-load --session-id=latest

# Handoff Reports
empirica handoff-create --session-id=latest --task-summary="..." --key-findings='[...]'
empirica handoff-query --ai-id=your-id --limit=5
```

---

## Enterprise Components

**11 production-ready enterprise components** with **27 Python implementation modules**.

[Explore Components →](components.md)

### Component Catalog

1. **Code Intelligence Analyzer** - Code analysis & comprehension
2. **Context Validation** - Context verification & validation
3. **Empirical Performance Analyzer** - Performance tracking
4. **Environment Stabilization** - Environment health & stability
5. **Goal Management** - Goal tracking & prioritization
6. **Intelligent Navigation** - Workspace navigation
7. **Procedural Analysis** - Procedure validation
8. **Runtime Validation** - Runtime checks & validation
9. **Security Monitoring** - Security scanning
10. **Tool Management** - Tool registry & recommendation
11. **Workspace Awareness** - Workspace state tracking

### Usage Example

```python
from empirica.components.code_intelligence_analyzer import CodeIntelligenceAnalyzer
from empirica.components.security_monitoring import SecurityMonitor

# Code analysis
analyzer = CodeIntelligenceAnalyzer()
analysis = analyzer.analyze_file("src/module.py")

print(f"Complexity: {analysis.complexity_score}")
print(f"Quality: {analysis.quality_score}")

# Security scan
monitor = SecurityMonitor()
scan = monitor.scan_vulnerabilities(path="./src")

print(f"Critical: {len(scan.critical)}")
print(f"High: {len(scan.high)}")
```

**Source:** `empirica/components/` + `docs/production/20_TOOL_CATALOG.md`

---

## Data Persistence & Session Continuity

[View Collaboration Features →](collaboration.md)

### Storage Systems

**1. Session Database (SQLite)**
- Complete session tracking
- Cascade history
- Epistemic state snapshots

**2. JSON Export**
- Human-readable session data
- Cross-tool compatibility

**3. Reflex Frame Logging**
- Temporal separation (prevents recursion)
- Epistemic assessment history

**4. Git Notes Checkpoints**
- **97.5% token reduction**
- Compressed session state
- Git-native storage

**5. Handoff Reports**
- **98% token reduction** (238-400 tokens vs 20,000)
- Multi-agent coordination
- Epistemic delta tracking

### Advanced Capabilities

**Git Integration**
- Checkpoint compression
- Session resumption
- 97.5% token savings

**Multi-AI Collaboration**
- Shared belief spaces
- Epistemic state synchronization
- Handoff reports for context transfer

**Learning Deltas**
- PREFLIGHT vs POSTFLIGHT comparison
- Epistemic growth measurement
- Calibration validation

**Cross-Session Continuity**
- Resume previous sessions
- Query handoff history
- Efficient context restoration

---

## Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/Nubaeon/empirica
cd empirica

# Install dependencies
pip install -e .

# Verify installation
empirica session-create --ai-id=test-agent --level=2
```

### Your First CASCADE

```python
from empirica.core.metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade

# 1. Initialize CASCADE
cascade = CanonicalEpistemicCascade(
    enable_bayesian=True,
    enable_drift_monitor=True
)

# 2. Run epistemic cascade
result = await cascade.run_epistemic_cascade(
    task="Review Python code for improvements",
    context={"cwd": "/project", "language": "python"}
)

# 3. View results
print(f"Confidence: {result['confidence']:.2f}")
print(f"Action: {result['action']}")
print(f"Knowledge Gaps: {result['knowledge_gaps']}")
```

### MCP Integration (Claude Desktop)

The MCP server runs automatically when Claude Desktop starts. All 23 tools are available:

- `bootstrap_session`
- `execute_preflight` / `submit_preflight_assessment`
- `execute_check` / `submit_check_assessment`
- `execute_postflight` / `submit_postflight_assessment`
- `create_goal`, `add_subtask`, `complete_subtask`
- And 14 more tools...

### Next Steps

1. **[13-Vector System](epistemics.md)** - Deep dive into vectors
2. **[Use Cases](use-cases.md)** - Real-world applications
3. **[MCP Integration](mcp-integration.md)** - Claude Desktop setup
4. **[API Reference](api-reference.md)** - Comprehensive API docs

---

## Why Empirica?

### Traditional AI Approach
- ❌ Heuristics and keyword matching
- ❌ No genuine self-awareness
- ❌ Overconfidence or underconfidence
- ❌ No uncertainty tracking

### Empirica Approach
- ✅ Genuine LLM-powered self-assessment
- ✅ 13-vector epistemic measurement
- ✅ Explicit uncertainty tracking
- ✅ Calibrated confidence
- ✅ Production-ready persistence

---

## Learn More

- **GitHub:** [https://github.com/Nubaeon/empirica](https://github.com/Nubaeon/empirica)
- **Documentation:** [api-reference.md](api-reference.md)
- **Quick Start:** [getting-started.md](getting-started.md)
- **Features:** [features.md](features.md)

---

**Built with epistemic transparency. Know what you don't know.** 🧠
