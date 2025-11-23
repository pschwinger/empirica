# AI vs Agent: Understanding the Distinction

**How Empirica adapts to different AI capabilities and roles**

[← Collaboration](collaboration.md) | [Back to Home](index.md) | [Architecture →](architecture.md)

---

## The Fundamental Distinction

Not all AIs are created equal. Empirica recognizes two distinct categories based on **reasoning capability** and **autonomy level**:

### AI (Collaborative Intelligence)
**Definition:** Engaged, reasoning partner working WITH the user

**Characteristics:**
- ✅ High autonomy and reasoning capability
- ✅ Engages in dialogue, asks clarifying questions
- ✅ Plans architecture, makes design decisions
- ✅ Uses full CASCADE workflow (PREFLIGHT → POSTFLIGHT)
- ✅ Creates goals, defines success criteria
- ✅ Delegates work to agents
- ✅ Learns and tracks epistemic growth

**Examples:**
- Claude Opus/Sonnet (high reasoning)
- GPT-4/GPT-4 Turbo (high reasoning)
- o1/o1-mini (high reasoning)
- Gemini Pro/Ultra (high reasoning)

**Empirica Usage:** Full CASCADE workflow with maximum autonomy

---

### Agent (Acting Intelligence)
**Definition:** Focused executor of specific, well-defined tasks

**Characteristics:**
- ✅ Lower autonomy, task-focused
- ✅ Executes predefined subtasks
- ✅ Limited dialogue (reports progress/completion)
- ✅ Uses simplified CASCADE (primarily ACT phase)
- ✅ Takes goals/subtasks as input
- ✅ Reports back with evidence
- ✅ May use lighter epistemic tracking

**Examples:**
- Mini-agent (Minimax) - Fast execution
- GPT-3.5 Turbo - Cost-effective tasks
- Claude Haiku - Quick responses
- Qwen 2.5/3 - Specialized tasks
- Grok Fast - Rapid execution
- Local models (based on modality)

**Empirica Usage:** Simplified CASCADE (ACT-focused) or skip CASCADE for simple tasks

---

## Why the Distinction Matters

### 1. **Reasoning Capability Limits**

Different models have different reasoning capabilities:

```
High Reasoning (Claude Opus, GPT-4, o1):
  - Can handle ambiguity
  - Self-directed investigation
  - Complex problem decomposition
  - Meta-reasoning about approach
  → Use full CASCADE, unlimited investigation rounds

Medium Reasoning (GPT-3.5, Claude Haiku):
  - Can execute clear tasks
  - Needs structured guidance
  - Benefits from constraints
  - Limited meta-reasoning
  → Use simplified CASCADE, max 5 investigation rounds

Low Reasoning (Specialized models):
  - Execute specific tasks well
  - Need explicit instructions
  - No meta-reasoning
  - Fast and cost-effective
  → Skip CASCADE, direct execution
```

### 2. **Cost vs Capability Trade-off**

```
Task: "Write 15 unit tests for auth validation"

Option A: Claude Opus (High reasoning)
  - Cost: $$$
  - Time: 5 minutes (includes planning)
  - Quality: Excellent (comprehensive tests)
  - Overkill: Yes (task is straightforward)

Option B: Mini-agent (Fast execution)
  - Cost: $
  - Time: 2 minutes (direct execution)
  - Quality: Good (follows patterns)
  - Appropriate: Yes (task is clear)

Savings: 80% cost, 60% time, same outcome
```

### 3. **Appropriate Tool Selection**

```
Design Task: "Architect OAuth authentication system"
→ Use AI (Claude Opus): Needs reasoning, planning, design decisions

Implementation Task: "Implement OAuth flow from spec"
→ Use AI or Agent: Depends on complexity

Testing Task: "Write tests for OAuth validation"
→ Use Agent (Mini-agent): Clear task, straightforward execution

Documentation Task: "Generate API docs from code"
→ Use Agent: Mechanical task, no reasoning needed
```

---

## CASCADE Usage Patterns

### Pattern 1: AI Solo Work (Full CASCADE)

**Use When:**
- Single AI working independently
- No delegation needed
- AI has capability to complete all work

**Workflow:**
```
AI {
  BOOTSTRAP → Initialize session, load context
  PREFLIGHT → Assess knowledge, identify uncertainty
  THINK → Analyze task, classify domain
  PLAN → Formulate strategy
  INVESTIGATE → Research, explore, prototype
  CHECK → Validate readiness (confidence ≥0.7)
  ACT → Implement, test, document
  POSTFLIGHT → Measure learning, generate handoff
}
```

**Example:**
```
Claude implements OAuth feature solo:
  PREFLIGHT (know: 0.6, uncertainty: 0.5)
  THINK: Classify as security/authentication task
  PLAN: Design token bucket pattern
  INVESTIGATE: Research OAuth flows, explore libraries
  CHECK (confidence: 0.8)
  ACT: Write auth.py, tests, docs
  POSTFLIGHT (know: 0.9, learned OAuth patterns)
```

**Time:** 15-30 minutes
**Cost:** $$$ (high reasoning model)
**Quality:** Excellent (comprehensive solution)

---

### Pattern 2: AI Delegates to Agents (Collaborative)

**Use When:**
- AI designs/plans, agents execute
- Clear task decomposition possible
- Agents have specialized capabilities
- Parallel execution beneficial

**Workflow:**
```
AI (Lead) {
  BOOTSTRAP → Initialize session
  PREFLIGHT → Assess overall knowledge
  THINK → Analyze requirements
  PLAN → Design architecture
  INVESTIGATE → Research, design architecture
    └─ CREATE GOALS & SUBTASKS
  CHECK (ready to delegate?)
  
  ┌─ DELEGATE ─────────────────────┐
  │                                 │
  ├─ Agent 1 { ACT subtasks 1-3 }  │
  ├─ Agent 2 { ACT subtasks 4-6 }  │
  └─ Agent 3 { ACT subtasks 7-9 }  │
  
  CHECK (review agent work)
  ACT (integrate, verify, refine)
  POSTFLIGHT (learned from design + agent feedback)
}

Agent (Worker) {
  Receive: subtask_id, description, context
  ACT → Execute subtask
  COMPLETE → Report evidence
  (Optional: Mini-PREFLIGHT if subtask complex)
}
```

**Example:**
```
Claude designs rate limiting, Mini-agent implements tests:

Claude (Lead AI):
  PREFLIGHT (know: 0.7, design skills high)
  THINK: Classify as performance/security task
  PLAN: Design token bucket rate limiting
  INVESTIGATE: Design rate limit strategy
  CREATE GOALS:
    - Goal 1: Implement middleware (Claude does this)
    - Goal 2: Write unit tests (delegate to mini-agent)
    - Goal 3: Write integration tests (delegate to mini-agent)
    - Goal 4: Update docs (Claude does this)
  
  DELEGATE:
    mini-agent → Goal 2 (unit tests)
    mini-agent → Goal 3 (integration tests)
  
  ACT: Implement middleware (Goal 1)
  
  WAIT: Agents complete
  
  CHECK: Review mini-agent's tests
    - Goal 2: ✅ 15 unit tests, all passing
    - Goal 3: ✅ 5 integration tests, all passing
  
  ACT: Integrate tests, verify, write docs (Goal 4)
  POSTFLIGHT: Learned token bucket implementation

Mini-agent (Goal 2 - Unit Tests):
  RECEIVE: "Write unit tests for rate_limit.py"
  ACT: Write test_rate_limit.py (15 test cases)
  COMPLETE: "Unit tests in test_rate_limit.py, 15 tests, all passing"

Mini-agent (Goal 3 - Integration Tests):
  RECEIVE: "Write integration tests for rate limiting"
  ACT: Write test_rate_limit_e2e.py (5 scenarios)
  COMPLETE: "Integration tests in test_rate_limit_e2e.py, 5 scenarios, all passing"
```

**Time:** 20 minutes (parallel execution)
**Cost:** $$ (AI for design, agents for execution)
**Quality:** Excellent (AI design + agent execution)
**Efficiency:** 60% cost savings vs AI doing everything

---

### Pattern 3: Multiple AIs Collaborating (Peer CASCADE)

**Use When:**
- Multiple reasoning AIs working together
- Each AI brings domain expertise
- Work requires multiple perspectives
- Complex problem requiring specialization

**Workflow:**
```
Lead AI {
  PREFLIGHT → Assess overall problem
  THINK → Classify domains needed
  PLAN → Decompose into specialist areas
  INVESTIGATE → Research high-level approach
  CREATE GOALS (domain-specific)
  
  ┌─ COORDINATE ───────────────────┐
  │                                 │
  ├─ AI 2 (Specialist A) {         │
  │    Mini-CASCADE on Goal 1       │
  │  }                              │
  │                                 │
  ├─ AI 3 (Specialist B) {         │
  │    Mini-CASCADE on Goal 2       │
  │  }                              │
  └─────────────────────────────────┘
  
  CHECK (synthesize specialist work)
  ACT (integrate, resolve conflicts)
  POSTFLIGHT (learned from specialists)
}

Specialist AI {
  PREFLIGHT (domain-specific assessment)
  THINK → Analyze specialist requirements
  PLAN → Design specialist solution
  INVESTIGATE (deep dive in specialty)
  ACT (specialized implementation)
  POSTFLIGHT (report findings to lead)
}
```

**Example:**
```
Building secure payment system:

Lead AI (Architecture - Claude Opus):
  PREFLIGHT: Understand payment requirements
  THINK: Classify as security + payment integration
  PLAN: Design system architecture
  INVESTIGATE: Research payment security patterns
  CREATE GOALS:
    - Goal 1: Security implementation (Security AI)
    - Goal 2: Payment integration (Payment AI)
    - Goal 3: Testing strategy (Lead + Test Agent)

Security AI (Specialist - o1):
  PREFLIGHT (security knowledge: 0.9)
  THINK: Analyze threat landscape
  PLAN: Design security layers
  INVESTIGATE: Threat modeling, encryption strategy
  ACT: Implement security layer, audit code
  POSTFLIGHT: Report vulnerabilities addressed

Payment AI (Specialist - GPT-4):
  PREFLIGHT (payment APIs knowledge: 0.8)
  THINK: Analyze payment requirements
  PLAN: Compare payment providers
  INVESTIGATE: Compare Stripe vs PayPal
  ACT: Implement payment integration
  POSTFLIGHT: Report integration complete + learnings

Lead AI (Integration):
  CHECK: Review security + payment implementations
  ACT: Integrate both, resolve conflicts, verify
  POSTFLIGHT: Learned security + payment patterns
```

**Time:** 45 minutes (parallel specialist work)
**Cost:** $$$$ (multiple high reasoning models)
**Quality:** Exceptional (specialist expertise)
**Use Case:** Critical/complex projects only

---

## Agent CASCADE Guidelines

### Simplified CASCADE for Agents

Agents typically use **ACT-focused workflow**:

```
Agent Workflow:
1. Receive subtask (description, context)
2. (Optional) Mini-PREFLIGHT if complex/uncertain
3. ACT → Execute work
4. COMPLETE → Report evidence
5. (Optional) Mini-POSTFLIGHT if learning occurred
```

### When Agents Use Full CASCADE

**Use full CASCADE if:**
- Subtask is complex (multi-step, >30min)
- Initial uncertainty high (>0.5)
- Learning expected (new library/pattern)
- Multiple approaches need evaluation

**Example:**
```
Agent receives: "Implement OAuth token refresh mechanism"

This is complex, so agent uses full CASCADE:
  PREFLIGHT (uncertainty: 0.6 - don't know refresh flow)
  THINK: Classify as authentication task
  PLAN: Research OAuth refresh spec
  INVESTIGATE: Research OAuth refresh token spec
  CHECK (confidence: 0.8)
  ACT: Implement refresh mechanism
  POSTFLIGHT (uncertainty: 0.2 - now understand flow)
```

### When Agents Skip CASCADE

**Skip formal CASCADE for:**
- Simple, well-defined tasks (<10min)
- Known patterns (done before)
- No uncertainty (clear instructions)

**Example:**
```
Agent receives: "Run pytest on all test files"

Simple task, just ACT:
  ACT: Run `pytest tests/ -v`
  COMPLETE: "Tests ran, 42/42 passing"
```

---

## Comparison Table

| Aspect | AI (Collaborative) | Agent (Acting) |
|--------|-------------------|----------------|
| **Autonomy** | High | Low-Medium |
| **Dialogue** | Extensive | Minimal |
| **Planning** | Creates goals/plans | Executes plans |
| **CASCADE** | Full (PREFLIGHT → POSTFLIGHT) | Simplified (ACT-focused) |
| **Investigation** | Self-directed, unlimited rounds | Structured, limited rounds |
| **Uncertainty** | Tracks and manages | Reports blockers |
| **Learning** | Measures epistemic growth | Optional, task-specific |
| **Delegation** | Delegates to agents | Rarely delegates |
| **Cost** | $$$ (high reasoning) | $ (fast execution) |
| **Speed** | Slower (includes planning) | Faster (direct execution) |
| **Quality** | Excellent (comprehensive) | Good (follows patterns) |
| **Examples** | Claude Opus, GPT-4, o1 | Mini-agent, GPT-3.5, Haiku |

---

## Best Practices

### For AIs (Collaborative Intelligence):

1. **Use full CASCADE** for significant work
2. **Create clear subtasks** when delegating
3. **Review agent work** before integrating
4. **Track learning** from both own work and agent feedback
5. **Generate handoffs** for continuity
6. **Ask clarifying questions** when uncertain
7. **Plan before acting** - don't rush to implementation

### For Agents (Acting Intelligence):

1. **Use simplified CASCADE** (ACT-focused) for simple tasks
2. **Use full CASCADE** for complex/uncertain tasks
3. **Report evidence** clearly when completing
4. **Ask for clarification** if subtask unclear
5. **Don't overthink** - execute efficiently
6. **Follow patterns** - don't reinvent
7. **Complete quickly** - optimize for speed

### For Users (Human Coordinators):

1. **Choose right tool** - AI for reasoning, agent for execution
2. **Delegate appropriately** - match task complexity to tool
3. **Provide context** when assigning to agents
4. **Review handoffs** between AIs/agents
5. **Track costs** - agents cheaper, AIs more capable
6. **Use parallel execution** - agents can work simultaneously
7. **Trust but verify** - review agent work

---

## Reasoning Capability Selection

### How Empirica Measures Reasoning

Empirica uses **epistemic reasoning benchmarks** to assess AI capability:

**High Reasoning Indicators:**
- Can self-assess accurately (calibration >0.85)
- Handles ambiguity well (clarity <0.5 → investigates)
- Meta-reasons about approach (plans before acting)
- Learns effectively (epistemic deltas >0.30)
- Asks clarifying questions when uncertain

**Medium Reasoning Indicators:**
- Self-assesses with guidance (calibration 0.70-0.85)
- Needs structured tasks (clarity >0.60)
- Follows patterns (limited meta-reasoning)
- Learns moderately (epistemic deltas 0.15-0.30)
- Reports blockers when stuck

**Low Reasoning Indicators:**
- Limited self-assessment (calibration <0.70)
- Needs explicit instructions (clarity >0.80)
- Executes without planning
- Limited learning (epistemic deltas <0.15)
- Doesn't ask questions

### Profile Assignment

Based on reasoning capability, Empirica assigns profiles:

```
High Reasoning → high_reasoning_collaborative profile
  - Unlimited investigation rounds
  - Dynamic confidence thresholds
  - Light tool suggestions
  - Maximum autonomy

Medium Reasoning → autonomous_agent profile
  - Max 5 investigation rounds
  - Confidence threshold: 0.70
  - Guided tool suggestions
  - Structured guidance

Low Reasoning → No CASCADE (direct execution)
  - Skip epistemic assessment
  - Execute tasks directly
  - Report completion
  - Cost-effective
```

---

## System Prompts: The Foundation

### Why System Prompts Matter

**System prompts** define AI behavior and role:

```
AI System Prompt (High Reasoning):
"You are a collaborative AI partner working WITH the user.
You have high autonomy and reasoning capability.
Use full CASCADE workflow (PREFLIGHT → POSTFLIGHT).
Ask clarifying questions when uncertain.
Plan architecture and make design decisions.
Create goals and delegate to agents when appropriate.
Track your epistemic growth and learning."

Agent System Prompt (Action-Based):
"You are an execution agent focused on completing specific tasks.
You receive well-defined subtasks from lead AIs.
Use simplified CASCADE (ACT-focused) for simple tasks.
Use full CASCADE for complex/uncertain tasks.
Report evidence clearly when completing.
Ask for clarification if task is unclear.
Optimize for speed and efficiency."
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
→ Returns: AI_COLLABORATIVE_PROMPT (full CASCADE guidance)

# Agent requests prompt
prompt = get_system_prompt(
    ai_id="mini-agent",
    role="acting_agent",
    modality="testing",
    task_type="test_implementation"
)
→ Returns: AGENT_EXECUTION_PROMPT (ACT-focused guidance)
```

**Benefits:**
- Right prompt for right role
- Consistent terminology (AI vs Agent)
- Token-efficient (load only needed guidance)
- Centrally managed, version controlled

---

## Next Steps

**Learn More:**
- [Architecture](architecture.md) - System design and canonical structure
- [Collaboration](collaboration.md) - Sessions, goals, handoffs
- [Epistemics](epistemics.md) - 13-vector system deep dive
- [Production Docs](../docs/AI_VS_AGENT_EMPIRICA_PATTERNS.md) - Complete patterns reference

**Try It:**
```python
# High reasoning AI (full CASCADE)
from empirica.core.metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade

cascade = CanonicalEpistemicCascade(
    profile_name='high_reasoning_collaborative'
)
result = await cascade.run_epistemic_cascade(task="Design OAuth system")

# Agent (simplified CASCADE)
cascade_agent = CanonicalEpistemicCascade(
    profile_name='autonomous_agent'
)
result = await cascade_agent.run_epistemic_cascade(task="Write unit tests")
```

---

**Built for all AI capabilities. Right tool, right task.** 🤖
