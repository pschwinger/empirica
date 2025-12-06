# Architecture Overview

**Empirica Phase 0:** Single AI + Genuine Epistemic Tracking

---

## System Overview

Empirica is an **epistemic self-assessment framework** that measures and validates AI metacognitive reasoning through genuine self-assessment (NO HEURISTICS).

**Core Components:**
1. **13-Vector System (UVL)** - Production epistemic measurement
2. **Canonical Assessor** - Generates self-assessment prompts
3. **Session Database** - Tracks epistemic growth over time
4. **Reflex Logger** - Creates epistemic audit trail
5. **Calibration Validator** - Compares PRE ↔ POST assessments
6. **Goal Orchestrator** - Manages goals and subtasks
7. **Git Integration** - Checkpoints, goals, cross-AI coordination

---

## The 13-Vector System (UVL)

### GATE: ENGAGEMENT (Threshold ≥ 0.60)
**Collaborative intelligence vs command execution**

### TIER 0: FOUNDATION (35% weight)
- **KNOW** - Domain knowledge confidence
- **DO** - Execution capability confidence
- **CONTEXT** - Environmental validity confidence

### TIER 1: COMPREHENSION (25% weight)
- **CLARITY** - Semantic understanding
- **COHERENCE** - Context consistency
- **SIGNAL** - Priority identification
- **DENSITY** - Cognitive load (inverted: 1.0 = overload)

### TIER 2: EXECUTION (25% weight)
- **STATE** - Environment mapping
- **CHANGE** - Modification tracking
- **COMPLETION** - Goal proximity
- **IMPACT** - Consequence understanding

### META-EPISTEMIC (15% weight)
- **UNCERTAINTY** - Explicit uncertainty about own assessment

**Total:** 13 vectors (UVL - Universal Vector Language)

---

## Session Structure

Empirica uses **explicit epistemic assessments** around **implicit CASCADE workflow**:

```
┌─────────────────┐
│  PRE Assessment │ - Assess epistemic state at session start
└────────┬────────┘
         │ Baseline: KNOW=0.5, DO=0.6, UNCERTAINTY=0.5
         │
         ▼
┌─────────────────┐
│  CREATE GOAL    │ - Define objective, scope, subtasks
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  IMPLICIT CASCADE (Natural Workflow)    │
│  • think → investigate → act            │
│  • CHECK #1: "Ready?" → No, investigate │
│  • CHECK #2: "Ready?" → Yes, proceed    │
│  • Complete subtasks with evidence      │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ POST Assessment │ - Reassess at session end
└────────┬────────┘
         │ Result: KNOW=0.8, DO=0.7, UNCERTAINTY=0.3
         │
         ▼
┌─────────────────┐
│  CALIBRATION    │ - Compare PRE ↔ POST
└─────────────────┘
  • Delta: KNOW +0.3 (learned!)
  • Uncertainty -0.2 (more confident)
  • CHECK assessments: 2 decision points
  • Status: Well-calibrated ✓
```

**Two Separate Systems:**
- **Explicit Assessments:** PRE/CHECK/POST (tracked in database)
- **Implicit CASCADE:** think→investigate→act (guidance, not enforced phases)

---

## Goal & Subtask Management

Empirica provides structured goal tracking with epistemic context:

### Goal Structure
```python
Goal:
  - objective: "What are we trying to achieve?"
  - scope: ScopeVector(breadth, duration, coordination)  # 3D vectorial scope
  - success_criteria: ["Criterion 1", "Criterion 2", ...]
  - estimated_complexity: 0.0-1.0
  - subtasks: [Subtask 1, Subtask 2, ...]
  - epistemic_context: {vectors from PRE assessment}
  - lineage: [who created, who resumed, timestamps]

Subtask:
  - description: "Specific task to complete"
  - importance: "high" | "medium" | "low"
  - dependencies: [other subtask IDs]
  - status: "pending" | "in_progress" | "complete"
  - evidence: "What was accomplished"
```

### Goal Workflow
```
1. PRE Assessment → Establish baseline epistemic state
2. CREATE GOAL → Define objective, scope, subtasks
3. Implicit CASCADE:
   - Work on subtasks (investigate/act)
   - CHECK assessments (decision points)
   - Complete subtasks with evidence
4. POST Assessment → Measure learning
5. Git Notes → Goals discoverable by other AIs
```

### Cross-AI Coordination
```bash
# AI-1 creates goal
empirica goals-create --objective "..." --scope-breadth 0.7 ...

# AI-2 discovers goals
empirica goals-discover --from-ai-id ai-1

# AI-2 resumes AI-1's goal
empirica goals-resume <goal-id> --ai-id ai-2
# Result: Full epistemic context + lineage tracking
```

**Benefits:**
- Structured task management
- Epistemic context preserved
- Cross-AI coordination via git
- Progress tracking with evidence

---

## Component Architecture

### 1. Core Components

**Location:** `empirica/core/`

```
core/
├── canonical/
│   ├── canonical_epistemic_assessment.py   # Assessor (generates prompts)
│   ├── canonical_goal_orchestrator.py      # Task tracking
│   ├── reflex_frame.py                     # Epistemic snapshot
│   └── reflex_logger.py                    # Audit trail
└── metacognitive_cascade/
    ├── metacognitive_cascade.py            # CASCADE workflow
    └── investigation_strategy.py           # Investigation patterns
```

**Purpose:**
- Generate self-assessment prompts (NO HEURISTICS)
- Parse genuine AI responses
- Log epistemic snapshots
- Track task orchestration

### 2. Data Layer

**Location:** `empirica/data/`

```
data/
├── session_database.py      # SQLite + JSON storage
└── session_json_handler.py  # Session exports
```

**Storage:**
- Sessions: `.empirica/sessions/sessions.db`
- Reflex logs: `.empirica_reflex_logs/`
- Privacy: All local, no cloud

### 3. Interface Layer

**Four ways to use Empirica:**

```
interfaces/
├── CLI (empirica/cli/)                    # Terminal commands
├── MCP (mcp_local/)                       # IDE integration
├── Bootstraps (empirica/bootstraps/)      # Interactive learning
└── API (empirica/ - Python imports)       # Programmatic access
```

### 4. Calibration & Monitoring

**Location:** `empirica/calibration/`

```
calibration/
├── parallel_reasoning.py                      # Bayesian parallel reasoning
└── adaptive_uncertainty_calibration/
    ├── adaptive_uncertainty_calibration.py    # Uncertainty calibration
    └── bayesian_belief_tracker.py             # Belief tracking
```

**Purpose:**
- Validate calibration quality
- Detect overconfidence/underconfidence
- Track metacognitive accuracy

---

## Data Flow

### PRE Assessment Flow (Session Start)
```
User Request
    ↓
Canonical Assessor (generates PRE assessment prompt)
    ↓
AI receives prompt → Genuinely self-assesses
    ↓
AI submits assessment (13 vectors + reasoning)
    ↓
System parses & validates
    ↓
Store in Session DB + Reflex Log + Git Checkpoint
    ↓
Return recommendation (proceed/investigate/clarify)
```

### Goal Creation Flow
```
After PRE Assessment
    ↓
AI creates goal (objective, scope, success criteria)
    ↓
Add subtasks to goal
    ↓
Store in Session DB + Git Notes
    ↓
Track progress as subtasks complete
```

### CHECK Assessment Flow (Decision Points, 0-N times)
```
During Work
    ↓
AI self-assesses: "Am I ready to proceed?"
    ↓
Submit CHECK assessment (13 vectors + decision + reasoning)
    ↓
IF decision = "proceed" → Continue to ACT
ELIF decision = "investigate" → Continue investigating
    ↓
Store in Session DB + Git Checkpoint
```

### POST Assessment Flow (Session End)
```
Task Completion
    ↓
Canonical Assessor (generates POST assessment prompt)
    ↓
AI genuinely reassesses
    ↓
System compares to PRE baseline
    ↓
Calculate epistemic deltas (what changed?)
    ↓
Validate calibration (accurate predictions?)
    ↓
Store results + Generate report
```

---

## Session Database Schema

### Tables

**sessions:**
- `session_id` (primary key)
- `ai_id` (which AI)
- `started_at`, `ended_at`
- `metadata` (JSON)

**cascades:**
- `cascade_id` (primary key)
- `session_id` (foreign key)
- `task` (description)
- `started_at`, `completed_at`
- `recommendation` (proceed/investigate/etc)

**cascade_metadata:**
- `cascade_id` (foreign key)
- `metadata_key` (e.g., "preflight_vectors")
- `metadata_value` (JSON)

**reflex_frames:**
- `frame_id` (primary key)
- `cascade_id` (foreign key)
- `phase` (preflight/check/postflight)
- `vectors` (JSON - 12 epistemic vectors)
- `reasoning` (text)
- `timestamp`

---

## Reflex Logs (Epistemic Trail)

**Location:** `.empirica_reflex_logs/cascade/YYYY-MM-DD/`

**Format:**
```json
{
  "session_id": "abc123",
  "cascade_id": "cascade_xyz",
  "phase": "preflight",
  "timestamp": "2025-11-08T10:00:00Z",
  "vectors": {
    "know": 0.6,
    "do": 0.7,
    "context": 0.5,
    ...
  },
  "reasoning": {
    "know": "I have moderate auth knowledge but not this codebase...",
    "do": "I can review code systematically...",
    ...
  },
  "recommendation": "proceed_cautiously"
}
```

**Purpose:**
- Audit trail (transparency)
- Calibration analysis
- Learning measurement
- Research data

---

## Phase 0 Boundaries

### ✅ Included in Phase 0:
- Single AI epistemic tracking
- 13-vector UVL system
- PRE → POST assessment workflow
- Session management (local storage)
- CLI, MCP, Bootstrap, API interfaces
- Reflex logs (epistemic trail)
- Calibration validation
- Privacy-first (local data only)

### ❌ NOT in Phase 0 (Future):
- Multi-AI routing (Cognitive Vault - Phase 1)
- Bayesian Guardian validation (Phase 1)
- Cross-AI calibration (Phase 1)
- Web UI (Phase 2+)
- Cloud sync (privacy-first = local only)

---

## Design Principles

### AI vs Agent Architecture Patterns

Empirica supports two distinct architectural patterns:

**🤖 AI (Collaborative Intelligence):**
- Uses full assessment workflow (PRE → CHECK(s) → POST)
- High autonomy, planning, design decisions
- Creates goals and delegates subtasks

**🔧 Agent (Acting Intelligence):**
- Uses simplified workflow (ACT-focused with CHECK)
- Task-focused execution, minimal dialogue
- Receives and executes subtasks from AI

**Detailed Patterns:** See [`docs/AI_VS_AGENT_EMPIRICA_PATTERNS.md`](AI_VS_AGENT_EMPIRICA_PATTERNS.md) for comprehensive CASCADE usage patterns, delegation strategies, and best practices.

---

### 1. NO HEURISTICS
```python
# ❌ WRONG: Static values
vectors = {"know": 0.5}  # Heuristic!

# ✅ RIGHT: Genuine self-assessment
assessment = ai.genuinely_assess(prompt)
vectors = assessment.vectors  # Real!
```

### 2. Privacy-First
- All data stored locally
- No cloud sync (by design)
- User owns their data
- No external dependencies (for Phase 0)

### 3. Transparency
- Every assessment logged (reflex logs)
- Full audit trail
- Reasoning captured
- Calibration visible

### 4. Calibration Focus
- PRE predictions vs POST reality
- Measure metacognitive accuracy
- Detect overconfidence patterns
- Validate genuine learning

---

## Technology Stack

**Core:**
- Python 3.8+
- SQLite (local storage)
- asyncio (async assessment)

**Interfaces:**
- Click (CLI framework)
- MCP Protocol (IDE integration)
- FastAPI (future REST API)

**No External Dependencies Required:**
- No LLM API calls needed (Phase 0)
- Self-contained system
- Privacy-preserving

---

## Performance Characteristics

**Assessment Speed:**
- Preflight: ~1-2 seconds (prompt generation)
- Postflight: ~1-2 seconds (delta calculation)
- Session lookup: <100ms (SQLite)

**Storage:**
- Session DB: ~10KB per session
- Reflex logs: ~5KB per assessment
- Scales to 100,000+ sessions

**Memory:**
- Minimal footprint (~50MB)
- No GPU required
- Runs on any Python 3.8+ system

---

## Security & Privacy

**Data Storage:**
- Local only (no cloud)
- SQLite database (encrypted filesystem recommended)
- User-owned data

**API Keys:**
- Optional (only for Phase 1+ features)
- Stored in `.empirica/credentials.yaml`
- Gitignored by default

**Audit Trail:**
- All assessments logged
- Immutable reflex logs
- Timestamp + signature

---

## Extension Points

### Custom Plugins
```python
# empirica/plugins/my_plugin/
from empirica.plugins.base_plugin import BasePlugin

class MyPlugin(BasePlugin):
    def on_preflight(self, assessment):
        # Custom logic
        pass
```

### Custom Vectors (Phase 1+)
```python
# Add domain-specific vectors
from empirica.plugins.modality_switcher.domain_vectors import DomainVectorRegistry

registry = DomainVectorRegistry()
registry.register_vector("security_awareness", weight=0.1)
```

### Custom Adapters (Phase 1+)
```python
# Connect to custom LLMs
from empirica.plugins.modality_switcher.adapters.base import BaseAdapter

class MyLLMAdapter(BaseAdapter):
    def query(self, prompt):
        # Custom LLM integration
        pass
```

---

## Next Steps

**For developers:**
- **Deep dive:** [`docs/production/04_ARCHITECTURE_OVERVIEW.md`](production/04_ARCHITECTURE_OVERVIEW.md)
- **Python API:** [`docs/production/13_PYTHON_API.md`](production/13_PYTHON_API.md)
- **Custom plugins:** [`docs/production/14_CUSTOM_PLUGINS.md`](production/14_CUSTOM_PLUGINS.md)

**For users:**
- **Get started:** 
  - **🤖 AI Agent?** → [`docs/01_a_AI_AGENT_START.md`](01_a_AI_AGENT_START.md)
  - **👤 Human?** → [`docs/00_START_HERE.md`](00_START_HERE.md)
- **Try it:** [`docs/guides/TRY_EMPIRICA_NOW.md`](guides/TRY_EMPIRICA_NOW.md)
- **Skills guide:** [`docs/skills/SKILL.md`](skills/SKILL.md)

---

**Architecture philosophy:** Measure and validate without interfering.

---

## How to Use Empirica: Four Interfaces

Empirica provides multiple interfaces for different workflows:

### 1. MCP Server (Best for AI Assistants in IDEs)

**Location:** `mcp_local/empirica_mcp_server.py`

**For:** Claude Desktop, Cursor, Windsurf, Rovo Dev integration

**Setup:**
```json
// Add to IDE MCP config (~/.config/Claude/claude_desktop_config.json)
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": ["/absolute/path/to/empirica/mcp_local/empirica_mcp_server.py"]
    }
  }
}
```

**Features:**
- 23 MCP tools for epistemic tracking
- Real-time tracking during work
- Automatic assessment prompts
- No context switching required

**See:** [Tool Catalog](production/20_TOOL_CATALOG.md) for all 23 tools

### 2. CLI (Best for Terminal & Automation)

**Commands:**
- `empirica preflight` - Start CASCADE with assessment
- `empirica check` - Validate confidence during work
- `empirica postflight` - Complete and calibrate
- `empirica goals-create` - Create discoverable goals
- `empirica goals-discover` - Find other AI's goals
- And 18+ more commands

**Benefits:**
- Scriptable and composable
- CI/CD integration
- Full command-line control

**Usage:** `empirica --help`

### 3. Python API (Best for Custom Integrations)

**Classes:**
```python
from empirica.core.metacognitive_cascade import CanonicalEpistemicCascade
from empirica.data.session_database import SessionDatabase
from empirica.core.canonical.canonical_goal_orchestrator import CanonicalGoalOrchestrator
```

**Use cases:**
- Custom workflows
- Programmatic control
- Integration with other systems

**See:** [Python API Reference](production/13_PYTHON_API.md)

### 4. Empirica Skill (AI Agent Learning Guide)

**Location:** `docs/skills/SKILL.md` (48KB comprehensive guide)

**For:** AI agents wanting deep understanding of Empirica

**Covers:**
- Complete workflow reference (BOOTSTRAP → PREFLIGHT → CASCADE → POSTFLIGHT)
- All 13 epistemic vectors explained in depth
- How to calibrate correctly (avoid common failure modes like anchoring)
- Advanced features (session management, cross-AI coordination)
- Best practices and anti-patterns
- "Functional self-awareness as a skill"

**Format:** Claude Skills compatible (can be loaded into AI agent context)

**Reading time:** 30-60 minutes  
**Value:** Complete understanding of epistemic self-awareness

---

## Automatic Git Checkpoints

Empirica creates **git checkpoints automatically** at key workflow points. No manual intervention required.

### When Checkpoints Are Created

**PREFLIGHT (Start of work):**
```bash
empirica preflight "task description"
# Automatic:
# ✅ Checkpoint created in refs/notes/empirica/checkpoints/<commit-hash>
# ✅ 13 epistemic vectors recorded (compressed ~85%)
# ✅ Baseline state stored for comparison
# ✅ Session metadata saved
```

**CHECK (During work, 0-N times):**
```bash
empirica check <session-id>
# Automatic:
# ✅ Intermediate checkpoint created
# ✅ Current state recorded
# ✅ Enables retrospective learning analysis
```

**POSTFLIGHT (End of work):**
```bash
empirica postflight <session-id>
# Automatic:
# ✅ Final checkpoint created
# ✅ Deltas calculated (POSTFLIGHT - PREFLIGHT)
# ✅ Calibration quality measured
# ✅ Training data generated
```

### Storage Architecture: Three Layers

**Why three layers?** Different use cases require different storage characteristics.

**1. Git Notes** (Cross-AI coordination)
- **Location:** `refs/notes/empirica/`
- **Stores:** Checkpoints, goals, sessions
- **Benefits:** Version controlled, distributed, ~85% token compressed
- **Use case:** Cross-AI discovery, lineage tracking, audit trail

**2. SQLite** (Fast queries)
- **Location:** `.empirica/sessions/sessions.db`
- **Stores:** Session metadata, vectors, queries
- **Benefits:** Fast structured queries
- **Use case:** Session lookup, vector queries, performance analytics

**3. JSON Logs** (Full fidelity)
- **Location:** `.empirica_reflex_logs/`
- **Stores:** Complete temporal workflow logs
- **Benefits:** Full fidelity, temporal replay
- **Use case:** Debugging, complete audit trail, temporal analysis

### Viewing Your Checkpoints

```bash
# List all checkpoints
git notes list | grep empirica/checkpoints

# Load a checkpoint
empirica load-checkpoint <session-id>

# View checkpoint data
git notes show refs/notes/empirica/checkpoints/<commit-hash>

# View all your sessions
empirica sessions-list
```

### Cross-AI Coordination via Git

**Goal Discovery:**
```bash
# AI-2 discovers AI-1's goals
empirica goals-discover --from-ai-id ai-1

# Returns: All goals with epistemic context and lineage
```

**Goal Resumption:**
```bash
# AI-2 resumes AI-1's goal
empirica goals-resume <goal-id> --ai-id ai-2

# Result:
# ✅ Loads AI-1's epistemic context (confidence levels, knowledge state)
# ✅ Adds lineage entry (who created, who resumed, when)
# ✅ AI-2 continues with full context
```

**Benefits:**
- Distributed coordination (git pull syncs everything)
- Epistemic handoffs (know other AI's confidence)
- Lineage tracking (full audit trail)
- Version controlled (can branch/revert goals)

**See:** [Git Checkpoint Architecture](architecture/GIT_CHECKPOINT_ARCHITECTURE.md) for technical deep dive

### Optional: Skip Git (For Testing)

```bash
# Skip git checkpoint creation during testing
empirica preflight "task" --no-git
```

---

## Deep Dive References

**For complete technical details, see:**

**Core System:**
- [Complete Documentation Map](production/00_DOCUMENTATION_MAP.md) - Navigation to all docs
- [13 Epistemic Vectors](production/05_EPISTEMIC_VECTORS.md) - Full vector guide
- [CASCADE Flow](production/06_CASCADE_FLOW.md) - Phase-by-phase details
- [Session Continuity](production/23_SESSION_CONTINUITY.md) - Handoffs & resumption

**Git Integration:**
- [Git Checkpoint Architecture](architecture/GIT_CHECKPOINT_ARCHITECTURE.md) - Technical deep dive
- [Cross-AI Coordination](production/26_CROSS_AI_COORDINATION.md) - Multi-AI workflows

**Tools & APIs:**
- [All 23 MCP Tools](production/20_TOOL_CATALOG.md) - Complete catalog
- [Python API Reference](production/13_PYTHON_API.md) - Programmatic access
- [Decision Logic](production/28_DECISION_LOGIC.md) - How CASCADE decides

**Advanced Features (Experimental):**
- [MCO Architecture](production/24_MCO_ARCHITECTURE.md) - Persona orchestration
- [ScopeVector Guide](production/25_SCOPEVECTOR_GUIDE.md) - Goal scoping

⚠️ Advanced features are experimental and may change.

---

**Architecture philosophy:** Empirica measures and validates epistemic state without interfering with natural AI reasoning. The system is designed to be minimally invasive while maximally informative.
