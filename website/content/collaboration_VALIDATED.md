# Cross-AI Collaboration & Workflow

**How Empirica enables seamless collaboration across AIs, platforms, and sessions**

[← Epistemics](epistemics.md) | [Back to Home](index.md) | [AI vs Agent →](ai_vs_agent.md)

---

## The Challenge: AI Collaboration at Scale

Modern AI development involves:
- **Multiple AIs** working on the same codebase
- **Different platforms** (Claude Desktop, VS Code, local models, cloud APIs)
- **Session continuity** across days, weeks, months
- **Knowledge transfer** between AI instances
- **Coordinated workflows** (design → implementation → testing)

**Traditional approaches fail because:**
- ❌ No shared epistemic state
- ❌ No session continuity
- ❌ No learning deltas
- ❌ Context lost between sessions
- ❌ No coordination mechanisms

**Empirica solves this through:**
- ✅ Centralized storage (Git + SQLite + JSON)
- ✅ Epistemic snapshots
- ✅ Handoff reports (98% token reduction)
- ✅ Learning deltas
- ✅ Sessions, goals, and subtasks
- ✅ Platform-agnostic design

---

## Storage Architecture: The Foundation

### Three Storage Systems (Simultaneous)

Empirica writes to **three formats simultaneously** for different use cases:

#### 1. **SQLite Database** (Queryable)
**Location:** `.empirica/sessions/sessions.db`

**Purpose:** Relational, queryable, persistent tracking

**Schema:**
- `sessions` - Session metadata (AI ID, timestamps, status)
- `cascades` - CASCADE executions (PREFLIGHT → POSTFLIGHT)
- `epistemic_assessments` - All 13-vector assessments
- `goals` - Goal tracking with success criteria
- `subtasks` - Subtask assignments and completion

**Use Cases:**
- Query across sessions: "Show all sessions for AI rovo-dev"
- Analytics: "What's my average epistemic growth?"
- Progress tracking: "Which goals are incomplete?"
- Cross-AI coordination: "What did the other AI learn?"

**Example Query:**
```sql
SELECT 
    session_id,
    AVG(know_after - know_before) as avg_knowledge_gain,
    AVG(uncertainty_after - uncertainty_before) as avg_uncertainty_reduction
FROM epistemic_assessments
WHERE ai_id = 'claude-dev'
GROUP BY session_id;
```

---

#### 2. **JSON Sessions** (Portable)
**Location:** `.empirica/sessions/<session_id>.json`

**Purpose:** Human-readable, exportable, shareable

**Content:**
```json
{
  "session_id": "abc123...",
  "ai_id": "claude-dev",
  "created_at": "2025-01-22T10:30:00Z",
  "cascades": [
    {
      "cascade_id": "cascade_001",
      "preflight": {
        "know": 0.35,
        "uncertainty": 0.75,
        "overall_confidence": 0.48
      },
      "investigation_rounds": 2,
      "postflight": {
        "know": 0.90,
        "uncertainty": 0.15,
        "overall_confidence": 0.88
      },
      "epistemic_delta": {
        "know": +0.55,
        "uncertainty": -0.60
      }
    }
  ],
  "goals": [...],
  "total_learning": {
    "knowledge_gain": 0.55,
    "uncertainty_reduction": 0.60
  }
}
```

**Use Cases:**
- Export sessions for backup
- Share with other AIs
- Human review and analysis
- Cross-platform transfer
- Audit trails

---

#### 3. **Reflex Logs** (Temporal Separation)
**Location:** `.empirica_reflex_logs/<ai_id>/<date>/`

**Purpose:** Prevent self-referential recursion

**Structure:**
```
.empirica_reflex_logs/
└── claude-dev/
    └── 2025-01-22/
        ├── preflight_10-30-15.json
        ├── investigate_10-32-45.json
        ├── check_10-35-20.json
        └── postflight_10-40-00.json
```

**Why Temporal Separation Matters:**
- AI can reflect on **past** reasoning without circular loops
- Current assessment doesn't reference itself
- Historical context available for learning
- Prevents confabulation

**Example:**
```python
# WRONG - Circular reference
assessment = assess(task, context={
    'previous_assessment': current_assessment  # ❌ Self-referential!
})

# RIGHT - Temporal separation
assessment = assess(task, context={
    'reflex_logs': load_historical_logs()  # ✅ Past reasoning only
})
```

---

#### 4. **Git Notes Checkpoints** (97.5% Token Reduction) ⭐ NEW
**Location:** `git notes refs/empirica/checkpoints/<session_id>`

**Purpose:** Compressed epistemic snapshots for efficient context loading

**Token Efficiency:**
- **Baseline:** 1,821 tokens (full session history)
- **Git-enhanced:** 46 tokens (compressed checkpoint)
- **Reduction:** 97.5%

**What's Stored:**
```
Compressed checkpoint (46 tokens):
- Session ID
- Current phase
- Epistemic vector summary (13 values)
- Active goals (IDs only)
- Critical context (compressed)
```

**Use Cases:**
- Resume sessions efficiently
- Load context without token explosion
- Cross-session continuity
- Multi-day projects

**Example:**
```bash
# Create checkpoint
empirica checkpoint-create --session-id latest --phase ACT --round 1

# Load checkpoint (46 tokens vs 1,821)
empirica checkpoint-load --session-id latest
```

---

#### 5. **Handoff Reports** (98% Token Reduction) ⭐ NEW
**Location:** `git notes refs/empirica/handoff/<session_id>` + SQLite

**Purpose:** Multi-agent coordination and knowledge transfer

**Token Efficiency:**
- **Full conversation:** ~20,000 tokens
- **Handoff report:** 238-400 tokens
- **Reduction:** 98%

**What's Included:**
```markdown
# Epistemic Handoff Report

## Task Summary
Implemented OAuth authentication with token refresh

## Key Findings
1. OAuth 2.0 token bucket pattern optimal for rate limiting
2. Refresh tokens require secure storage (encrypted DB)
3. Test coverage: 95% (15 unit tests, 5 integration tests)

## Epistemic Growth
- KNOW: 0.35 → 0.90 (+0.55)
- UNCERTAINTY: 0.75 → 0.15 (-0.60)
- DO: 0.75 → 0.90 (+0.15)

## Remaining Unknowns
1. Production deployment strategy (need DevOps input)
2. Rate limit thresholds (need product decision)

## Next Session Context
OAuth implementation complete. Next: Deploy to staging, configure rate limits.

## Artifacts Created
- src/auth/oauth.py
- tests/test_oauth.py
- docs/oauth_setup.md
```

**Use Cases:**
- Hand off work to another AI
- Resume work after days/weeks
- Multi-AI coordination
- Knowledge transfer
- Efficient context restoration

---

## Sessions: The Unit of Work

### What is a Session?

A **session** is a complete work unit with:
- Unique session ID
- AI identifier
- Start/end timestamps
- One or more CASCADE executions
- Goals and subtasks
- Epistemic trajectory (learning over time)

### Session Lifecycle

```
1. BOOTSTRAP → Initialize session
   empirica session-create --ai-id=claude-dev --level=2
   
2. PREFLIGHT → Assess initial state
   empirica preflight --session-id=latest --prompt="Task"
   
3. WORK → Execute CASCADE(s)
   - INVESTIGATE
   - CHECK
   - ACT
   
4. POSTFLIGHT → Measure learning
   empirica postflight --session-id=latest
   
5. HANDOFF → Generate report
   empirica handoff-create --session-id=latest
```

### Session Continuity

**Resume Previous Session:**
```bash
# Resume last session for this AI
empirica sessions-resume --ai-id=claude-dev --count=1

# Loads:
# - Git checkpoint (46 tokens)
# - Handoff report (238 tokens)
# - Active goals
# Total: ~300 tokens vs 20,000+ for full history
```

**Query Sessions:**
```bash
# List all sessions
empirica sessions-list

# Show specific session
empirica sessions-show latest:active:claude-dev

# Get session summary
empirica sessions-summary --session-id=abc123
```

---

## Goals & Subtasks: Structured Coordination

### Goal Structure

**Goals** provide structured work breakdown:

```python
goal = {
    'goal_id': 'goal-uuid',
    'session_id': 'session-uuid',
    'objective': 'Implement OAuth authentication',
    'scope': 'session_scoped',  # task_specific, session_scoped, project_wide
    'success_criteria': [
        'OAuth 2.0 flow implemented',
        'Token refresh mechanism working',
        'Test coverage ≥90%',
        'Documentation complete'
    ],
    'estimated_complexity': 0.7,  # 0.0-1.0
    'created_at': '2025-01-22T10:30:00Z',
    'status': 'in_progress'  # active, completed, blocked
}
```

**Create Goal:**
```bash
empirica goals-create \
  --session-id=latest \
  --objective="Implement OAuth authentication" \
  --scope=session_scoped \
  --success-criteria='["OAuth flow implemented", "Tests passing"]'
```

---

### Subtask Structure

**Subtasks** break goals into actionable units:

```python
subtask = {
    'task_id': 'task-uuid',
    'goal_id': 'goal-uuid',
    'description': 'Write unit tests for token validation',
    'importance': 'high',  # critical, high, medium, low
    'estimated_tokens': 500,
    'dependencies': ['task-uuid-1', 'task-uuid-2'],
    'assigned_to': 'mini-agent',  # Optional
    'status': 'pending',  # pending, in_progress, completed, blocked
    'evidence': None  # Filled on completion
}
```

**Add Subtask:**
```bash
empirica goals-add-subtask \
  --goal-id=<goal-uuid> \
  --description="Write unit tests for token validation" \
  --importance=high \
  --estimated-tokens=500
```

**Complete Subtask:**
```bash
empirica goals-complete-subtask \
  --task-id=<task-uuid> \
  --evidence="Created test_oauth_validation.py with 15 tests, all passing. Coverage 95%."
```

---

## Cross-AI Collaboration Patterns

### Pattern 1: Sequential Handoff (AI → AI)

**Use Case:** One AI completes work, hands off to another

```
Day 1: Claude (Design AI)
  PREFLIGHT: Assess requirements
  INVESTIGATE: Research OAuth patterns
  PLAN: Design architecture
  CREATE GOALS:
    - Goal 1: Implement OAuth flow (delegate to Day 2 AI)
    - Goal 2: Write tests (delegate to mini-agent)
    - Goal 3: Documentation (Claude does this)
  ACT: Write architecture docs
  POSTFLIGHT: Measure learning
  HANDOFF: Generate report (238 tokens)

Day 2: GPT-4 (Implementation AI)
  RESUME: Load handoff report (238 tokens)
  PREFLIGHT: Assess readiness
    - KNOW: 0.70 (learned from handoff)
    - CONTEXT: 0.80 (architecture clear)
  ACT: Implement OAuth flow
  POSTFLIGHT: Measure learning
  HANDOFF: Generate report

Day 3: Mini-agent (Testing AI)
  RESUME: Load handoff report
  ACT: Write tests (simple task, no full CASCADE)
  COMPLETE: Report evidence
```

**Token Efficiency:**
- Traditional: 20,000 tokens × 3 days = 60,000 tokens
- Empirica: 238 tokens × 3 handoffs = 714 tokens
- **Savings: 98.8%**

---

### Pattern 2: Parallel Collaboration (AI + Agents)

**Use Case:** Lead AI delegates to multiple agents simultaneously

```
Lead AI (Claude):
  PREFLIGHT: Assess overall task
  INVESTIGATE: Design system
  CREATE GOALS:
    - Goal 1: Implement middleware (Claude)
    - Goal 2: Unit tests (Agent 1)
    - Goal 3: Integration tests (Agent 2)
    - Goal 4: Documentation (Agent 3)
  
  DELEGATE:
    → Agent 1: Goal 2 (unit tests)
    → Agent 2: Goal 3 (integration tests)
    → Agent 3: Goal 4 (documentation)
  
  ACT: Implement middleware (Goal 1)
  
  WAIT: Agents complete work
  
  CHECK: Review agent work
    - Agent 1: ✅ 15 unit tests, all passing
    - Agent 2: ✅ 5 integration tests, all passing
    - Agent 3: ✅ API docs complete
  
  ACT: Integrate all work, verify
  POSTFLIGHT: Measure learning (includes agent feedback)
  HANDOFF: Generate report

Agents (Mini-agent, Qwen, GPT-3.5):
  RECEIVE: Subtask from lead AI
  ACT: Execute subtask
  COMPLETE: Report evidence
  (No full CASCADE - simple execution)
```

**Benefits:**
- Parallel execution (faster)
- Specialized agents (cheaper)
- Lead AI maintains oversight
- Coordinated through goals/subtasks

---

### Pattern 3: Multi-AI Specialist Team

**Use Case:** Complex project requiring multiple domain experts

```
Architecture AI (Claude Opus):
  PREFLIGHT: Assess overall system
  INVESTIGATE: Design architecture
  CREATE GOALS:
    - Goal 1: Security implementation (Security AI)
    - Goal 2: Payment integration (Payment AI)
    - Goal 3: Testing strategy (Lead + Test Agent)
  HANDOFF: Architecture complete

Security AI (Specialized model):
  RESUME: Load architecture handoff
  PREFLIGHT: Assess security requirements
    - KNOW: 0.90 (security expert)
    - CONTEXT: 0.80 (from handoff)
  INVESTIGATE: Threat modeling
  ACT: Implement security layer
  POSTFLIGHT: Measure learning
  HANDOFF: Security implementation complete

Payment AI (Specialized model):
  RESUME: Load architecture handoff
  PREFLIGHT: Assess payment requirements
    - KNOW: 0.85 (payment APIs expert)
  INVESTIGATE: Compare Stripe vs PayPal
  ACT: Implement payment integration
  POSTFLIGHT: Measure learning
  HANDOFF: Payment integration complete

Architecture AI (Integration):
  RESUME: Load security + payment handoffs
  CHECK: Review specialist work
  ACT: Integrate both, resolve conflicts
  POSTFLIGHT: Final learning measurement
  HANDOFF: Project complete
```

**Epistemic Coordination:**
- Each AI contributes domain expertise
- Handoffs preserve learning
- Lead AI synthesizes specialist knowledge
- Shared epistemic state via storage

---

## Learning Deltas: Measuring Growth

### What are Learning Deltas?

**Learning deltas** measure epistemic growth from PREFLIGHT to POSTFLIGHT:

```python
learning_delta = {
    'know': postflight.know - preflight.know,
    'do': postflight.do - preflight.do,
    'context': postflight.context - preflight.context,
    'uncertainty': postflight.uncertainty - preflight.uncertainty,  # Negative is good!
    'overall_confidence': postflight.overall_confidence - preflight.overall_confidence
}
```

### Example Learning Delta

```
PREFLIGHT (Baseline):
  KNOW: 0.35
  DO: 0.75
  CONTEXT: 0.60
  UNCERTAINTY: 0.75
  Overall: 0.48

... CASCADE execution ...

POSTFLIGHT (After Learning):
  KNOW: 0.90
  DO: 0.90
  CONTEXT: 0.85
  UNCERTAINTY: 0.15
  Overall: 0.88

LEARNING DELTA:
  KNOW: +0.55 🚀 (Significant knowledge gain)
  DO: +0.15 ✅ (Capability confirmed)
  CONTEXT: +0.25 ✅ (Context improved)
  UNCERTAINTY: -0.60 🎯 (Uncertainty reduced)
  Overall: +0.40 ✅ (Major confidence increase)
```

### Why Learning Deltas Matter

**1. Validate Investigation Effectiveness**
```
If UNCERTAINTY doesn't decrease → Investigation failed
If KNOW doesn't increase → No learning occurred
If Overall confidence doesn't improve → Wasted effort
```

**2. Track AI Capability Growth**
```
Session 1: KNOW delta = +0.20
Session 2: KNOW delta = +0.35
Session 3: KNOW delta = +0.50
→ AI is getting better at learning in this domain
```

**3. Optimize Investigation Strategy**
```
Investigation A: 3 rounds, KNOW delta = +0.15
Investigation B: 2 rounds, KNOW delta = +0.40
→ Investigation B more efficient
```

**4. Calibrate Confidence**
```
Predicted confidence after investigation: 0.80
Actual confidence (POSTFLIGHT): 0.75
Delta: -0.05 (slightly overconfident)
→ Adjust future predictions
```

---

## Epistemic Snapshots: Point-in-Time State

### What are Epistemic Snapshots?

**Snapshots** capture complete epistemic state at a specific moment:

```python
snapshot = {
    'timestamp': '2025-01-22T10:35:00Z',
    'phase': 'CHECK',
    'round': 2,
    'vectors': {
        'engagement': 0.85,
        'know': 0.70,
        'do': 0.80,
        'context': 0.75,
        'clarity': 0.90,
        'coherence': 0.85,
        'signal': 0.80,
        'density': 0.40,
        'state': 0.75,
        'change': 0.70,
        'completion': 0.65,
        'impact': 0.75,
        'uncertainty': 0.35
    },
    'overall_confidence': 0.75,
    'active_goals': ['goal-uuid-1', 'goal-uuid-2'],
    'investigation_rounds_completed': 2
}
```

### Use Cases

**1. Resume Work Efficiently**
```bash
# Load snapshot (46 tokens)
empirica checkpoint-load --session-id=latest

# vs loading full history (1,821 tokens)
# 97.5% token savings
```

**2. Track Epistemic Trajectory**
```
Snapshot 1 (PREFLIGHT): Overall 0.48
Snapshot 2 (CHECK Round 1): Overall 0.65 (+0.17)
Snapshot 3 (CHECK Round 2): Overall 0.75 (+0.10)
Snapshot 4 (POSTFLIGHT): Overall 0.88 (+0.13)
→ Steady epistemic growth
```

**3. Cross-AI Coordination**
```
AI 1 creates snapshot at end of session
AI 2 loads snapshot at start of next session
→ Perfect continuity, minimal tokens
```

---

## Platform-Agnostic Design

### Why Platform Independence Matters

AIs work across:
- **IDEs:** VS Code, Cursor, Windsurf, Zed
- **Platforms:** Claude Desktop, ChatGPT, local models
- **Environments:** Cloud, local, hybrid

**Empirica's solution:**
- **Git** - Universal version control
- **SQLite** - Portable database (single file)
- **JSON** - Universal format
- **File-based** - No server required

### Cross-Platform Workflow

```
Claude Desktop (Mac):
  - Creates session
  - Stores in Git + SQLite + JSON
  - Generates handoff report

VS Code + Copilot (Windows):
  - Loads handoff from Git
  - Continues work
  - Updates SQLite + JSON

Local Qwen Model (Linux):
  - Loads checkpoint from Git
  - Executes subtasks
  - Reports completion

All synchronized via:
  - Git (distributed)
  - SQLite (portable file)
  - JSON (universal format)
```

---

## MCP Tools for Collaboration

Empirica provides **23 MCP tools** for collaboration:

### Session Management
```python
# Bootstrap new session
bootstrap_session(ai_id="claude-dev", session_type="development", bootstrap_level=2)

# Resume previous session
resume_previous_session(ai_id="claude-dev", count=1)

# Get session summary
get_session_summary(session_id="latest:active:claude-dev")

# Get current epistemic state
get_epistemic_state(session_id="latest")
```

### Goals & Subtasks
```python
# Create goal
create_goal(
    session_id="latest",
    objective="Implement OAuth authentication",
    scope="session_scoped",
    success_criteria=["OAuth flow working", "Tests passing"]
)

# Add subtask
add_subtask(
    goal_id="goal-uuid",
    description="Write unit tests",
    importance="high"
)

# Complete subtask
complete_subtask(
    task_id="task-uuid",
    evidence="Tests created, all passing"
)

# Get goal progress
get_goal_progress(goal_id="goal-uuid")
```

### Continuity
```python
# Create git checkpoint (97.5% token reduction)
create_git_checkpoint(
    session_id="latest",
    phase="ACT",
    round_num=1
)

# Load checkpoint
load_git_checkpoint(session_id="latest")

# Create handoff report (98% token reduction)
create_handoff_report(
    session_id="latest",
    task_summary="OAuth implementation complete",
    key_findings=["Token bucket pattern optimal", "95% test coverage"],
    remaining_unknowns=["Deployment strategy TBD"],
    next_session_context="Ready for staging deployment"
)

# Query handoff reports
query_handoff_reports(ai_id="claude-dev", limit=5)
```

---

## Cross-AI Coordination (v2.0) 🆕

### Discover Goals Across AIs

**New Feature**: AIs can discover and resume goals created by other AIs via git notes.

```python
# Discover goals from another AI
discover_goals(from_ai_id="claude-code")

# Returns:
# [
#   {
#     "goal_id": "goal-uuid-1",
#     "objective": "Implement rate limiting",
#     "created_by": "claude-code",
#     "epistemic_state": {"know": 0.7, "uncertainty": 0.3},
#     "status": "in_progress"
#   }
# ]

# Resume another AI's goal
resume_goal(
    goal_id="goal-uuid-1",
    ai_id="current-ai",
    handoff_context="Continuing rate limiting implementation"
)
```

**Use Cases:**
- **Multi-AI Projects**: Different AIs work on different goals
- **Specialist Handoff**: Security AI → Payment AI → Integration AI
- **Load Balancing**: Distribute goals across available AIs
- **Continuity**: Resume work when original AI unavailable

**Lineage Tracking:**
- Every goal tracks which AIs worked on it
- Epistemic handoffs preserve learning
- Git notes enable distributed coordination

---

## Best Practices

### For Lead AIs (High Reasoning)
1. **Create clear goals** with success criteria
2. **Break down into subtasks** for delegation
3. **Generate handoffs** for continuity
4. **Track learning deltas** to validate growth
5. **Review agent work** before integrating

### For Agent AIs (Action-Based)
1. **Execute subtasks** efficiently
2. **Report evidence** clearly
3. **Complete subtasks** with details
4. **Ask for clarification** if unclear
5. **Don't overthink** - execute and report

### For All AIs
1. **Use checkpoints** for long tasks
2. **Generate handoffs** at session end
3. **Load handoffs** at session start
4. **Track epistemic growth** via deltas
5. **Coordinate via goals/subtasks**

---

## Next Steps

**Learn More:**
- [AI vs Agent Patterns](ai_vs_agent.md) - High reasoning vs action-based AIs
- [Architecture](architecture.md) - System design and structure
- [Epistemics](epistemics.md) - 13-vector system deep dive
- [Production Docs](../docs/production/23_SESSION_CONTINUITY.md) - Complete continuity guide

**Try It:**
```bash
# Create session
empirica session-create --ai-id=your-id --level=2

# Create goal
empirica goals-create --session-id=latest --objective="Your goal"

# Create handoff
empirica handoff-create --session-id=latest --task-summary="What you did"

# Resume later
empirica sessions-resume --ai-id=your-id --count=1
```

---

**Built for collaboration. Work together, learn together.** 🤝
