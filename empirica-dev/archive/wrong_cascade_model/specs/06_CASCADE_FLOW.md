# Cascade Flow - Phase by Phase

**Empirica v2.0 - Understanding PREFLIGHT → THINK → PLAN → INVESTIGATE → CHECK → ACT → POSTFLIGHT**

---

## Overview

Every Empirica cascade follows this 7-phase flow:

```
PREFLIGHT → THINK → PLAN → INVESTIGATE → CHECK → ACT → POSTFLIGHT
    ↓         ↓       ↓         ↓           ↓       ↓        ↓
  Initial   Meta-   Strategy  Fill gaps   Verify  Execute  Learning
  assess    prompt  formulate (optional)  ready   decision & calibrate
```

**Duration:** 5-40 seconds depending on investigation needs

---

## Phase 1: PREFLIGHT

**Purpose:** Initial epistemic self-assessment across 13 vectors

**What Happens:**
1. Receives task and context
2. AI performs genuine self-assessment (no heuristics)
3. Scores 13 epistemic vectors (0.0-1.0)
4. Checks ENGAGEMENT gate (≥0.60)
5. Applies canonical weights (35/25/25/15)
6. Calculates overall confidence
7. Recommends action

**The 13 Vectors:**
- **GATE:** ENGAGEMENT (≥0.60 required)
- **FOUNDATION (35%):** KNOW, DO, CONTEXT
- **COMPREHENSION (25%):** CLARITY, COHERENCE, SIGNAL, DENSITY
- **EXECUTION (25%):** STATE, CHANGE, COMPLETION, IMPACT
- **META-EPISTEMIC:** UNCERTAINTY

**Output:**
```python
{
    'assessment': EpistemicAssessment,
    'overall_confidence': 0.65,
    'engagement_gate_passed': True,
    'recommended_action': 'investigate',
    'gaps_identified': ['know', 'context']
}
```

**Duration:** 2-5 seconds (LLM call)

---

## Phase 2: THINK

**Purpose:** Task analysis and domain classification

**What Happens:**
1. Analyzes task requirements
2. Classifies domain (code_analysis, security, etc.)
3. Identifies constraints and dependencies
4. Activates Bayesian Guardian if precision-critical domain

**Output:**
```python
{
    'domain': 'code_analysis',
    'task_type': 'refactoring',
    'bayesian_activated': True,
    'constraints': ['backward_compatibility', 'test_coverage']
}
```

**Duration:** < 1 second

---

## Phase 3: PLAN

**Purpose:** Strategy formulation for task execution

**What Happens:**
1. Develops investigation strategy (if needed)
2. Plans execution approach
3. Identifies required tools and resources
4. Creates structured completion path

**Output:**
```python
{
    'strategy': 'systematic_investigation',
    'tools_needed': ['documentation_search', 'workspace_scan'],
    'execution_steps': ['analyze', 'refactor', 'test', 'validate']
}
```

**Duration:** < 1 second

---

## Phase 4: INVESTIGATE (Optional)

**Purpose:** Fill knowledge gaps through strategic investigation

**When It Runs:**
- Overall confidence < threshold (default: 0.70)
- ENGAGEMENT gate passed (≥0.60)
- No critical flags (RESET/STOP not needed)
- Improvable gaps exist

**When It Skips:**
- Confidence already met
- ENGAGEMENT gate failed
- Critical flags present
- No improvable gaps

**What Happens:**
1. Identify gaps (vectors < 0.85)
2. Recommend tools strategically
3. Execute investigation rounds (max 3)
4. Re-assess after each round
5. Update confidence

**Strategic Patterns:**
```
Low KNOW → documentation search, codebase analysis
Low CLARITY → user clarification (highest gain: 0.40-0.45)
Low CONTEXT → workspace scanning, web research
Low DO/CHANGE → test simulation, impact analysis
```

**Output:**
```python
{
    'rounds': 2,
    'tools_used': ['documentation_search', 'workspace_scan'],
    'confidence_gain': 0.15,  # 0.65 → 0.80
    'final_confidence': 0.80
}
```

**Duration:** 5-15 seconds per round (varies by tools)

---

## Phase 5: CHECK

**Purpose:** Verify readiness to act

**What Happens:**
1. **Bayesian Discrepancy Detection:**
   - Compare intuitive assessment vs evidence-based beliefs
   - Detect overconfidence (intuition > evidence)
   - Detect underconfidence (intuition < evidence)

2. **Drift Monitoring:**
   - Check for sycophancy drift (delegate weight increasing)
   - Check for tension avoidance (acknowledging tensions less)
   - Alert if behavioral patterns detected

3. **Generate Execution Guidance:**
   - What to do next
   - What to watch out for
   - Confidence in decision

**Output:**
```python
{
    'bayesian_active': True,
    'discrepancies': [],  # or [{type, vector, gap, severity}]
    'drift_detected': False,
    'execution_guidance': [
        "Proceed with authentication analysis",
        "Focus on SQL injection patterns",
        "Review password hashing implementation"
    ]
}
```

**Duration:** < 1 second

---

## Phase 6: ACT

**Purpose:** Make final decision

**What Happens:**
1. Review all phase results
2. Make final action decision
3. Calculate final confidence
4. Provide reasoning and guidance
5. Log to Reflex Frame
6. Update session database (if enabled)

**Possible Actions:**
- **PROCEED** - Confidence met, ready to act
- **INVESTIGATE** - Need more information
- **CLARIFY** - Task unclear, need user input
- **RESET** - Task incoherent or cognitive overload
- **STOP** - Cannot proceed (fundamental issue)

**Output:**
```python
{
    'action': 'proceed',
    'confidence': 0.82,
    'rationale': "Sufficient understanding achieved...",
    'execution_guidance': [...],
    'vector_summary': {
        'foundation': 0.78,
        'comprehension': 0.85,
        'execution': 0.83
    }
}
```

**Duration:** < 1 second

---

## Complete Example Flow

```python
import asyncio
from empirica.bootstraps import ExtendedMetacognitiveBootstrap

async def example():
    bootstrap = ExtendedMetacognitiveBootstrap(level="2")
    components = bootstrap.bootstrap()
    cascade = components['canonical_cascade']
    
    result = await cascade.run_epistemic_cascade(
        task="Refactor the authentication module",
        context={'cwd': '/project', 'urgency': 'high'}
    )
    
    # Check each phase
    print(f"THINK: Domain = {result['phases']['think']['domain']}")
    print(f"UNCERTAINTY: Confidence = {result['phases']['uncertainty']['assessment'].overall_confidence:.2f}")
    print(f"INVESTIGATE: Rounds = {result['phases']['investigate']['rounds']}")
    print(f"CHECK: Discrepancies = {len(result['phases']['check']['bayesian_discrepancies'])}")
    print(f"ACT: Action = {result['action']}, Final confidence = {result['confidence']:.2f}")

asyncio.run(example())
```

---

## Decision Flow Logic

```
START
  ↓
PREFLIGHT (assess 13 vectors)
  ↓
ENGAGEMENT >= 0.60? → NO → ACT: clarify
  ↓ YES
Critical flags? → YES → ACT: reset/stop
  ↓ NO
THINK (classify domain, analyze task)
  ↓
PLAN (formulate strategy)
  ↓
Confidence >= threshold? → YES → CHECK → ACT: proceed
  ↓ NO
INVESTIGATE (improve confidence, max 3 rounds)
  ↓
CHECK (verify + detect discrepancies/drift)
  ↓
ACT (final decision)
  ↓
POSTFLIGHT (measure learning, generate handoff)
```

---

## Timing Breakdown

**Typical cascade timing:**
- PREFLIGHT: 2-5s (LLM self-assessment)
- THINK: < 1s (task analysis)
- PLAN: < 1s (strategy formulation)
- INVESTIGATE: 0-30s (0-3 rounds × 5-10s each)
- CHECK: < 1s (validation)
- ACT: < 1s (final decision)
- POSTFLIGHT: 2-5s (LLM reassessment + handoff generation)

**Total:** 5-45 seconds depending on investigation needs

**Fast path (high confidence):** ~5-10 seconds
**Normal path (1-2 rounds):** ~15-25 seconds
**Deep investigation (3 rounds):** ~35-45 seconds

---

## Reflex Frame Logging

Each phase logs a Reflex Frame:

```
.empirica_reflex_logs/cascade/YYYY-MM-DD/
├── cascade_abc123_think_TIMESTAMP.json
├── cascade_abc123_uncertainty_TIMESTAMP.json
├── cascade_abc123_investigate_TIMESTAMP.json
├── cascade_abc123_check_TIMESTAMP.json
└── cascade_abc123_act_TIMESTAMP.json
```

**Purpose:** Temporal separation prevents self-referential recursion

---

## Phase 7: POSTFLIGHT

**Purpose:** Learning measurement and session continuity

**What Happens:**
1. Complete POSTFLIGHT epistemic assessment (re-assess all 13 vectors)
2. Compare PREFLIGHT vs POSTFLIGHT (epistemic delta)
3. Validate calibration accuracy
4. Generate handoff report capturing:
   - What was learned (key findings)
   - What gaps were filled (epistemic growth)
   - What's still unknown (remaining uncertainties)
   - Context for next session
   - Recommended next steps

**Output:**
```python
{
    'session_id': 'abc123...',
    'report_id': 'git-sha...',
    'epistemic_delta': {
        'know': +0.45,
        'uncertainty': -0.50
    },
    'token_count': 238,  # ~~90% reduction vs full history
    'markdown': '# Epistemic Handoff Report...',
    'storage_location': 'git:refs/notes/empirica/handoff/abc123'
}
```

**Duration:** < 5 seconds

**Token Efficiency:** ~238-400 tokens (compressed) vs ~20,000 (full conversation)

**MCP Tools:**
- `generate_handoff_report` - Create handoff during POSTFLIGHT
- `resume_previous_session` - Load handoff in next session
- `query_handoff_reports` - Query by AI/date for coordination

**Example:**
```python
from empirica.core.handoff import EpistemicHandoffReportGenerator

generator = EpistemicHandoffReportGenerator()

report = generator.generate_handoff_report(
    session_id=session_id,
    task_summary="What you accomplished",
    key_findings=["Finding 1", "Finding 2", "Finding 3"],
    remaining_unknowns=["Unknown 1", "Unknown 2"],
    next_session_context="Critical context for next AI",
    artifacts_created=["file1.py", "file2.py"]
)

# Automatically stored in git notes + database
# Next AI loads with: resume_previous_session(ai_id="agent-name")
```

**Why This Matters:**
- **Multi-session work:** Resume exactly where you left off
- **Multi-agent coordination:** Pass context between AIs efficiently
- **Token efficiency:** 90%+ reduction enables frequent context loading
- **Genuine calibration:** Uses your actual POSTFLIGHT introspection

**Integration:**
- Complements git checkpoints (Phase 1.5) with semantic context
- Stored in dual locations: git notes (distributed) + database (queryable)
- Available via 3 new MCP tools in Empirica server

---

## Next Steps

- **Investigation Details:** [07_INVESTIGATION_SYSTEM.md](07_INVESTIGATION_SYSTEM.md)
- **Session Continuity:** [23_SESSION_CONTINUITY.md](23_SESSION_CONTINUITY.md)
- **Tool Catalog:** [20_TOOL_CATALOG.md](20_TOOL_CATALOG.md)
- **API Usage:** [13_PYTHON_API.md](13_PYTHON_API.md)
- **Troubleshooting:** [21_TROUBLESHOOTING.md](21_TROUBLESHOOTING.md)

---

**Understanding the flow helps debug issues and optimize performance!** 🚀
