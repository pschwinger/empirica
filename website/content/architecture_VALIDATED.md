# Architecture & Structure

**Understanding Empirica's system design and canonical organization**

[← AI vs Agent](ai_vs_agent.md) | [Back to Home](index.md)

---

## System Architecture Overview

Empirica is built on a **three-layer architecture** designed for modularity, extensibility, and genuine epistemic reasoning:

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERACTION LAYER                      │
│  - CLI (command-line interface)                                  │
│  - MCP Server (IDE integration)                                  │
│  - Dashboard (real-time monitoring)                              │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    EPISTEMIC FRAMEWORK LAYER                     │
│  - Canonical Assessment (13 vectors, genuine LLM reasoning)      │
│  - CASCADE Workflow (7 phases with investigation loop)           │
│  - Profile System (context-aware constraints)                    │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                     INVESTIGATION SYSTEM LAYER                   │
│  - Domain strategies (code, research, creative, etc.)            │
│  - Plugin system (user-provided investigation tools)             │
│  - Tool recommendations (profile-driven suggestions)             │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                       PERSISTENCE LAYER                          │
│  - SQLite database (queryable, relational)                       │
│  - JSON sessions (portable, exportable)                          │
│  - Reflex logs (temporal separation)                             │
│  - Git notes (97.5% token reduction)                             │
└─────────────────────────────────────────────────────────────────┘
```

**Source:** `docs/reference/ARCHITECTURE_OVERVIEW.md`

---

## Core Design Principles

### 1. No Heuristics Principle

**Empirica does not use heuristics to simulate AI self-awareness.**

❌ **What Empirica Avoids:**
```python
# WRONG - Keyword matching
if 'refactor' in task:
    domain = 'code_analysis'
    know = 0.7  # Fake confidence

# WRONG - Hardcoded confidence boosts
confidence += 0.15 * tools_used  # Not genuine learning

# WRONG - Simulated learning
know_after = know_before + (rounds * 0.05)  # Fake growth
```

✅ **What Empirica Does:**
```python
# Genuine LLM self-assessment
assessment = await assessor.assess(
    task="Refactor authentication system",
    context={"cwd": "/project", "domain": "security"}
)

# LLM genuinely reasons:
# "I understand authentication patterns (know: 0.7)
#  but I'm uncertain about this specific codebase (uncertainty: 0.6)
#  and I don't know the current implementation (context: 0.4).
#  I need to investigate before proceeding."
```

**Why This Matters:**
- Real reasoning about knowledge state
- Handles novel situations
- Honest uncertainty acknowledgment
- Genuine learning measurement

---

### 2. Temporal Separation

**Reflex logs separate current reasoning from historical reasoning.**

**Problem:** Self-referential recursion
```python
# WRONG - Circular reference
assessment = assess(task, context={
    'previous_assessment': current_assessment  # ❌ Self-referential!
})
```

**Solution:** Temporal separation
```python
# RIGHT - Past reasoning only
assessment = assess(task, context={
    'reflex_logs': load_historical_logs()  # ✅ Historical context
})
```

**Benefits:**
- Prevents confabulation
- AI can reflect on past without loops
- Clear separation of current vs historical
- Enables genuine meta-reasoning

---

### 3. Context-Aware Constraints

**Investigation constraints adapt to AI capability and domain.**

```
High Reasoning Models (Claude Opus, GPT-4, o1):
  → high_reasoning_collaborative profile
  → Unlimited investigation rounds
  → Maximum autonomy

Autonomous Agents (GPT-3.5, Claude Haiku):
  → autonomous_agent profile
  → Max 5 investigation rounds
  → Structured guidance

Critical Domains (Medical, Legal, Financial):
  → critical_domain profile
  → Max 3 investigation rounds
  → Strict compliance rules
```

**Why Adaptive:**
- Right constraints for right context
- No artificial limitations
- Appropriate guidance per capability
- Domain-specific safety

---

### 4. Genuine Calibration

**Track how well AI predictions match reality.**

```
PREFLIGHT: Initial assessment (baseline)
    ↓
Investigation: Gather information
    ↓
CHECK: Reassess after investigation
    ↓
ACT: Execute task
    ↓
POSTFLIGHT: Final assessment (compare with baseline)
    ↓
Calibration delta reveals over/under-confidence patterns
```

**Calibration Metrics:**
- Prediction accuracy
- Overconfidence detection
- Underconfidence detection
- Learning effectiveness
- Continuous improvement

---

## Canonical Directory Structure

Empirica follows a **canonical** (authoritative) directory structure for consistency and clarity:

### Root Structure

```
empirica/
├── empirica/                          # Core Python package
├── mcp_local/                         # MCP server implementations
├── docs/                              # Documentation
├── tests/                             # Test suite
├── examples/                          # Working examples
├── .empirica/                         # Runtime data (auto-created)
├── .empirica_reflex_logs/             # Reflex logs (auto-created)
└── pyproject.toml                     # Package configuration
```

---

### Core Package: `empirica/`

#### 1. **Canonical Epistemic Framework** (`empirica/core/canonical/`)

**Purpose:** Genuine epistemic self-assessment (no heuristics)

```
empirica/core/canonical/
├── canonical_epistemic_assessment.py  # LLM-powered self-assessment
├── reflex_frame.py                    # Data structures (13 vectors)
├── reflex_logger.py                   # Phase-specific JSON logging
└── git_enhanced_reflex_logger.py      # Git checkpoints (97.5% reduction)
```

**Key Files:**
- `canonical_epistemic_assessment.py` - Generates LLM prompts, parses responses
- `reflex_frame.py` - Defines `EpistemicAssessment`, `VectorState`, `Action` enum
- `git_enhanced_reflex_logger.py` - Compressed checkpoints in git notes

**Import Paths:**
```python
from empirica.core.canonical import (
    CanonicalEpistemicAssessor,
    EpistemicAssessment,
    VectorState,
    Action,
    CANONICAL_WEIGHTS,
    ENGAGEMENT_THRESHOLD
)
```

---

#### 2. **CASCADE Workflow** (`empirica/core/metacognitive_cascade/`)

**Purpose:** 7-phase metacognitive workflow

```
empirica/core/metacognitive_cascade/
├── metacognitive_cascade.py           # Main CASCADE orchestrator
├── investigation_plugin.py            # Plugin interface
├── investigation_strategy.py          # Domain-aware investigation
└── mcp_aware_investigation.py         # MCP tool execution
```

**Key Files:**
- `metacognitive_cascade.py` - Orchestrates PREFLIGHT → POSTFLIGHT
- `investigation_plugin.py` - User-provided investigation tools
- `investigation_strategy.py` - Domain-specific tool recommendations

**Import Paths:**
```python
from empirica.core.metacognitive_cascade import CanonicalEpistemicCascade
```

---

#### 3. **Configuration System** (`empirica/config/`)

**Purpose:** Profile-based investigation configuration

```
empirica/config/
├── investigation_profiles.yaml        # 5 profiles (high_reasoning, autonomous, etc.)
├── profile_loader.py                  # Profile loading and selection
└── modality_config.yaml               # Modality switcher (optional)
```

**5 Built-in Profiles:**
1. `high_reasoning_collaborative` - Max autonomy (Claude, GPT-4, o1)
2. `autonomous_agent` - Structured (GPT-3.5, Haiku)
3. `critical_domain` - Strict compliance (medical, legal)
4. `exploratory` - Max freedom (research, learning)
5. `balanced` - Default middle-ground

**Import Paths:**
```python
from empirica.config.profile_loader import select_profile, load_profile
```

**Note:** v2.0 introduces **MCO Architecture** (Meta-Agent Configuration Object) which replaces Investigation Profiles with dynamic YAML-based configuration. See MCO section below.

---

#### 3a. **MCO Architecture (v2.0)** (`empirica/config/mco/`)

**Purpose:** Dynamic configuration via YAML files

```
empirica/config/mco/
├── personas.yaml                      # 6 AI personas (researcher, implementer, etc.)
├── cascade_styles.yaml                # CASCADE workflow styles
├── goal_scopes.yaml                   # Goal scope recommendations
├── model_profiles.yaml                # Model-specific bias corrections
├── protocols.yaml                     # Communication protocols
├── goal_scope_loader.py               # Scope recommendation logic
└── mco_loader.py                      # MCO loading logic
```

**6 MCO Personas** (in `personas.yaml`):
1. `researcher` - High uncertainty tolerance, deep investigation
2. `implementer` - Balanced, action-oriented
3. `reviewer` - High precision, quality focus
4. `coordinator` - Multi-agent orchestration
5. `learner` - Maximum exploration
6. `expert` - Minimal investigation, high confidence

**Key Features:**
- **Dynamic Thresholds**: Persona-specific confidence gates
- **Scope Recommendations**: AI-driven goal scoping based on epistemic state
- **Model Profiles**: Bias correction for different AI models (GPT-4, Claude, etc.)
- **CASCADE Styles**: Different workflow patterns per persona
- **Backward Compatible**: Falls back to Investigation Profiles if MCO not available

**Import Paths:**
```python
from empirica.config.mco.mco_loader import load_mco_persona
from empirica.config.goal_scope_loader import get_scope_recommendations
```

---

#### 4. **Data Management** (`empirica/data/`)

**Purpose:** Persistence, export/import, tracking

```
empirica/data/
├── session_database.py                # SQLite database
└── session_json_handler.py            # JSON session export/import
```

**Storage Locations:**
- SQLite: `.empirica/sessions/sessions.db`
- JSON: `.empirica/sessions/<session_id>.json`
- Reflex logs: `.empirica_reflex_logs/<ai_id>/<date>/`
- Git notes: `git notes refs/empirica/checkpoints/<session_id>`

**Import Paths:**
```python
from empirica.data.session_database import SessionDatabase
from empirica.data.session_json_handler import SessionJSONHandler
```

---

#### 5. **CLI** (`empirica/cli/`)

**Purpose:** Command-line interface

```
empirica/cli/
├── cli_core.py                        # Main CLI logic
├── command_handlers/                  # Command implementations
│   ├── bootstrap_commands.py
│   ├── assessment_commands.py
│   ├── cascade_commands.py
│   ├── session_commands.py
│   └── ... (15+ handlers)
└── uvl_formatter.py                   # UVL formatting
```

**Entry Point:**
```bash
python -m empirica.cli
# or
empirica <command>
```

---

#### 6. **Components** (`empirica/components/`)

**Purpose:** Optional advanced components (11 enterprise components)

```
empirica/components/
├── code_intelligence_analyzer/        # Code analysis
├── context_validation/                # Context verification
├── goal_management/                   # Goal orchestration
├── security_monitoring/               # Security scanning
├── tool_management/                   # Enhanced tool handling
└── ... (6 more components)
```

**Note:** Most components are optional. Core functionality doesn't depend on them.

---

### MCP Server: `mcp_local/`

**Purpose:** IDE integration via Model Context Protocol

```
mcp_local/
├── empirica_mcp_server.py             # Main MCP server (23 tools)
├── start_empirica_mcp.sh              # Startup script
└── archive/                           # Archived documentation
```

**23 MCP Tools:**
- Session Management (4 tools)
- Assessment Workflow (6 tools)
- Goals & Subtasks (5 tools)
- Continuity (5 tools)
- Help (3 tools)

---

### Documentation: `docs/`

**Purpose:** Comprehensive documentation

```
docs/
├── 00_START_HERE.md                   # Entry point for humans
├── 01_a_AI_AGENT_START.md             # Entry point for AI agents (CLI)
├── 01_b_MCP_AI_START.md               # Entry point for AI agents (MCP)
├── production/                        # 25 production docs
│   ├── 00_COMPLETE_SUMMARY.md
│   ├── 05_EPISTEMIC_VECTORS.md
│   ├── 06_CASCADE_FLOW.md
│   └── ... (22 more docs)
├── reference/                         # Reference documentation
│   ├── CANONICAL_DIRECTORY_STRUCTURE.md
│   ├── ARCHITECTURE_OVERVIEW.md
│   └── ...
└── guides/                            # User guides
```

---

### Runtime Data: `.empirica/` (auto-created)

**Purpose:** Runtime data storage

```
.empirica/
├── sessions/                          # Session storage
│   ├── sessions.db                    # SQLite database
│   └── <session_id>.json              # JSON session exports
└── config/                            # Runtime configuration
    └── user_preferences.json          # User preferences
```

**Auto-Initialization:** Created automatically on first use.

---

### Reflex Logs: `.empirica_reflex_logs/` (auto-created)

**Purpose:** Temporal separation logs

```
.empirica_reflex_logs/
└── <ai_id>/                           # Per-AI logs
    └── <date>/                        # Per-date logs
        ├── preflight_<timestamp>.json
        ├── investigate_<timestamp>.json
        ├── check_<timestamp>.json
        └── postflight_<timestamp>.json
```

**Purpose:** Prevents self-referential recursion.

---

## System Prompts: The Foundation

### Why System Prompts Matter

**System prompts** define AI behavior, role, and capabilities:

**AI System Prompt (High Reasoning):**
```
You are a collaborative AI partner working WITH the user.
You have high autonomy and reasoning capability.

Use full CASCADE workflow:
- PREFLIGHT: Assess your knowledge state honestly
- THINK: Analyze task requirements
- PLAN: Formulate strategy
- INVESTIGATE: Research when uncertain
- CHECK: Validate readiness
- ACT: Execute with confidence
- POSTFLIGHT: Measure learning

Ask clarifying questions when uncertain.
Plan architecture and make design decisions.
Create goals and delegate to agents when appropriate.
Track your epistemic growth and learning.
```

**Agent System Prompt (Action-Based):**
```
You are an execution agent focused on completing specific tasks.
You receive well-defined subtasks from lead AIs.

Use simplified CASCADE:
- ACT: Execute subtask efficiently
- COMPLETE: Report evidence clearly

Use full CASCADE for complex/uncertain tasks.
Ask for clarification if task is unclear.
Optimize for speed and efficiency.
```

### Future: Dynamic System Prompts

**Vision:** Cognitive Vault + Sentinel provides role-based prompts

```python
# AI requests prompt
prompt = get_system_prompt(
    ai_id="claude-dev",
    role="collaborative_ai",
    modality="coding",
    task_type="feature_design"
)
→ Returns: AI_COLLABORATIVE_PROMPT

# Agent requests prompt
prompt = get_system_prompt(
    ai_id="mini-agent",
    role="acting_agent",
    modality="testing",
    task_type="test_implementation"
)
→ Returns: AGENT_EXECUTION_PROMPT
```

**Benefits:**
- Right prompt for right role
- Consistent terminology
- Token-efficient
- Centrally managed
- Version controlled

---

## Integration Points

### 1. CLI Integration

**Entry Point:** `python -m empirica.cli`

**Key Commands:**
```bash
# Bootstrap with profile
empirica bootstrap --profile high_reasoning_collaborative

# Auto-select profile
empirica bootstrap --ai-model claude-sonnet --domain research

# Workflow commands
empirica preflight "task description"
empirica investigate
empirica check
empirica postflight

# Session management
empirica sessions-list
empirica sessions-resume --ai-id=your-id

# Goals & subtasks
empirica goals-create --objective="Your goal"
empirica goals-add-subtask --goal-id=<id> --description="..."
empirica goals-complete-subtask --task-id=<id>
```

---

### 2. MCP Server Integration

**23 MCP Tools Available:**

**Session Management:**
- `bootstrap_session(ai_id, session_type, profile)`
- `resume_previous_session(ai_id, count)`
- `get_session_summary(session_id)`
- `get_epistemic_state(session_id)`

**Assessment Workflow:**
- `execute_preflight(session_id, prompt)`
- `submit_preflight_assessment(session_id, vectors)`
- `execute_check(session_id, findings, unknowns, confidence)`
- `submit_check_assessment(session_id, vectors, decision)`
- `execute_postflight(session_id, task_summary)`
- `submit_postflight_assessment(session_id, vectors)`

**Goals & Subtasks:**
- `create_goal(session_id, objective, scope, success_criteria)`
- `add_subtask(goal_id, description, importance)`
- `complete_subtask(task_id, evidence)`
- `get_goal_progress(goal_id)`
- `list_goals(session_id)`

**Continuity:**
- `create_git_checkpoint(session_id, phase, round_num)`
- `load_git_checkpoint(session_id)`
- `create_handoff_report(session_id, task_summary, key_findings, ...)`
- `query_handoff_reports(ai_id, limit)`

**Help:**
- `get_empirica_introduction()`
- `get_workflow_guidance(phase)`
- `cli_help()`

---

### 3. Plugin Integration

**Investigation Plugins:**

```python
# User creates plugin
my_plugin = InvestigationPlugin(
    name='database_search',
    description='Search internal database',
    improves_vectors=['know', 'context'],
    confidence_gain=0.20,
    executor=my_db_search_function
)

# Register with CASCADE
cascade = CanonicalEpistemicCascade(
    investigation_plugins={'db': my_plugin}
)

# Plugin suggestions filtered by profile
# - light mode: AI can ignore
# - guided mode: AI should consider
# - prescribed mode: Must use if relevant
```

---

## Data Flow: Complete CASCADE

```
1. User Prompt
    ↓
2. [PREFLIGHT] Canonical Epistemic Assessment
    │ - LLM genuinely reasons about 13 vectors
    │ - Baseline established
    │ - Auto-tracked: SQLite + JSON + Reflex log
    ↓
3. [THINK] Initial Reasoning
    │ - LLM thinks about approach
    │ - Domain classification
    ↓
4. [PLAN] Task Decomposition
    │ - Break down into subtasks
    │ - Goal orchestrator manages goals
    ↓
5. [INVESTIGATE] Investigation Loop
    │ ┌─────────────────────────────┐
    │ │ A. Identify epistemic gaps  │
    │ │ B. Load investigation profile│
    │ │ C. Strategy recommends tools│
    │ │ D. Plugins add custom tools │
    │ │ E. AI selects tools         │
    │ │ F. MCP executes tools       │
    │ │ G. Results integrated       │
    │ │ [CHECK] Self-assess         │
    │ │ H. Continue OR exit?        │
    │ └─────────────────────────────┘
    ↓
6. [ACT] Execute Task
    │ - Perform actual work
    │ - Generate output
    ↓
7. [POSTFLIGHT] Final Assessment
    │ - Genuine reassessment
    │ - Compare with PREFLIGHT
    │ - Epistemic delta calculated
    │ - Auto-tracked: SQLite + JSON + Reflex log
    ↓
8. Results + Session Data
```

---

## Performance Characteristics

### Time Complexity
- Epistemic assessment: O(1) LLM call
- CASCADE execution: O(n) where n = investigation rounds
- Profile loading: O(1) YAML parse (cached)
- Database queries: O(log n) with indexes

### Space Complexity
- Session storage: ~10KB per session (JSON)
- Database growth: ~50KB per 100 assessments
- Reflex logs: ~5KB per phase per session
- Memory usage: <100MB typical

### Token Efficiency
- **Baseline session loading:** 1,821 tokens
- **Git-enhanced loading:** 46 tokens
- **Reduction:** 97.5%
- **Handoff reports:** 238-400 tokens vs 20,000
- **Reduction:** 98%

---

## Best Practices

### For Developers

1. **Follow canonical structure** - Don't deviate from directory layout
2. **Use import paths correctly** - Full paths required
3. **Extend via plugins** - Don't modify core
4. **Test against profiles** - Verify behavior across profiles
5. **Document integration points** - Clear extension mechanisms

### For Users

1. **Choose right profile** - Match AI capability and domain
2. **Use MCP tools** - Leverage IDE integration
3. **Track sessions** - Use session management
4. **Generate handoffs** - Enable continuity
5. **Review calibration** - Improve over time

### For AIs

1. **Understand architecture** - Know where files are
2. **Use correct imports** - Follow canonical paths
3. **Respect profiles** - Honor constraints
4. **Track learning** - Measure epistemic growth
5. **Generate handoffs** - Enable collaboration

---

## Next Steps

**Learn More:**
- [Epistemics](epistemics.md) - 13-vector system deep dive
- [Collaboration](collaboration.md) - Sessions, goals, handoffs
- [AI vs Agent](ai_vs_agent.md) - High reasoning vs action-based
- [Production Docs](../docs/reference/ARCHITECTURE_OVERVIEW.md) - Complete architecture reference
- [Directory Structure](../docs/reference/CANONICAL_DIRECTORY_STRUCTURE.md) - Complete file reference

**Try It:**
```python
from empirica.core.metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade
from empirica.config.profile_loader import select_profile

# Auto-select profile
profile = select_profile(ai_model='claude-sonnet', domain='research')

# Create CASCADE with profile
cascade = CanonicalEpistemicCascade(profile_name=profile.name)

# Run CASCADE
result = await cascade.run_epistemic_cascade(
    task="Your task here",
    context={"domain": "your_domain"}
)
```

---

**Built with architectural clarity. Understand the system, extend the system.** 🏗️
