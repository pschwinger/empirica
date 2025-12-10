# Investigation System

**Empirica v4.0 - Strategic Tool Recommendations**

---

## Overview

The Investigation System provides **strategic guidance** for filling knowledge gaps within Empirica's implicit CASCADE workflow.

### Context: Investigation in CASCADE

**Two Separate Systems:**
1. **Explicit Assessments:** PRE/CHECK/POST (tracked)
2. **Implicit CASCADE:** think → **investigate** → act (natural workflow, guidance only)

Investigation is part of the implicit CASCADE - AI self-assesses "do I need to investigate?" based on uncertainty, not enforced thresholds.

**With Goals & Git:**
- Investigation work tracked via subtasks
- Progress stored in git checkpoints (automatic)
- Cross-AI: AI-2 can resume AI-1's investigation via goal discovery
- Multi-agent handoff: Use investigation handoffs (PREFLIGHT→CHECK) for specialist patterns (see [`../guides/FLEXIBLE_HANDOFF_GUIDE.md`](../guides/FLEXIBLE_HANDOFF_GUIDE.md))

**Approach:** Strategic guidance (Approach B) - suggestive, not controlling. Configurable thresholds via `thresholds.yaml`, `goal_scopes.yaml`.

**Key Principle:** Recommend tools, don't execute them. Let the AI decide.

---

## When Investigation Happens

Investigation triggers when **all 4 conditions** are met:

1. ✅ Overall confidence < threshold (default: 0.70)
2. ✅ ENGAGEMENT gate passed (≥0.60)
3. ✅ No critical flags (no RESET/STOP needed)
4. ✅ Improvable gaps exist (vectors < 0.85)

**Investigation Skips When:**
- Confidence already sufficient
- ENGAGEMENT gate failed → need clarification first
- Critical flags present → need reset/stop first
- No improvable gaps → all vectors high enough

---

## The 5 Strategic Patterns

### Pattern 1: Domain Knowledge Gap (KNOW < 0.70)

**Tools Recommended:**
- **Documentation search** (gain: 0.25-0.35)
- **Codebase semantic search** (gain: 0.20-0.30)
- **Session history analysis** (gain: 0.15-0.25)

**Example:**
```
Gap: KNOW = 0.50 (low domain knowledge)
Recommendation: "Search codebase for authentication patterns"
Expected gain: 0.30
```

### Pattern 2: Task Clarity Issue (CLARITY < 0.70)

**Tools Recommended:**
- **User clarification** (gain: 0.40-0.45) ← **HIGHEST**
- **Example analysis** (gain: 0.15-0.25)

**Example:**
```
Gap: CLARITY = 0.45 (task unclear)
Recommendation: "Ask user to clarify requirements"
Expected gain: 0.42
```

**Why highest gain?** Direct communication removes ambiguity immediately.

### Pattern 3: Environmental Context Gap (CONTEXT < 0.70, STATE < 0.70)

**Tools Recommended:**
- **Workspace scanning** (gain: 0.30-0.40)
- **Web research** (gain: 0.20-0.30)
- **File system exploration** (gain: 0.15-0.25)

**Example:**
```
Gap: CONTEXT = 0.55 (missing environmental info)
Recommendation: "Scan workspace for project structure"
Expected gain: 0.35
```

### Pattern 4: Execution Confidence Low (DO < 0.70, CHANGE < 0.70)

**Tools Recommended:**
- **Test simulation** (gain: 0.25-0.35)
- **Impact analysis** (gain: 0.20-0.30)
- **Dry run validation** (gain: 0.15-0.25)

**Example:**
```
Gap: DO = 0.60 (execution capability uncertain)
Recommendation: "Simulate test execution to verify approach"
Expected gain: 0.28
```

### Pattern 5: Multi-Gap Scenario

**Tools Recommended:**
- **Prioritized combination** of above strategies
- Highest priority gap addressed first
- Sequential recommendations

**Example:**
```
Gaps: KNOW=0.55, CLARITY=0.50, CONTEXT=0.65
Priority: CLARITY (user clarification, gain: 0.42)
Then: KNOW (documentation search, gain: 0.30)
Then: CONTEXT (workspace scan, gain: 0.35)
```

---

## Investigation Rounds

**Maximum:** 3 rounds (configurable)
**Process:**
1. Identify gaps
2. Recommend tools
3. (AI decides whether to use tools)
4. Re-assess epistemic state
5. Check if confidence met
6. Repeat or exit

**Example Flow:**
```
Round 1:
  Initial: KNOW=0.55, DO=0.60, CONTEXT=0.50 → confidence=0.55
  Recommendation: "Scan workspace" (target: CONTEXT)
  Post-investigation: CONTEXT=0.85 → confidence=0.68

Round 2:
  Current: KNOW=0.55, DO=0.60 → confidence=0.68
  Recommendation: "Search documentation" (target: KNOW)
  Post-investigation: KNOW=0.80 → confidence=0.75

confidence >= 0.70 → Exit investigation
```

---

## Tool Capability Map

**16+ tools available:**

### Standard Tools:
- `read` - Read file contents
- `write` - Write to files
- `edit` - Edit files
- `list_dir` - List directory contents
- `grep_file_content` - Search in files

### Empirica Tools:
- `web_search` - Search web for information
- `semantic_search_qdrant` - Semantic code search
- `session_manager_search` - Search past sessions

### User Interaction:
- `user_clarification` - Ask user for input (HIGHEST GAIN)

### Plugin-Defined:
- Custom domain-specific tools via plugin system

---

## Domain Awareness

Different domains get different tool recommendations:

### CODE_ANALYSIS Domain:
```python
Tools: filesystem_search, semantic_search_qdrant, code_pattern_detection
Focus: Understanding codebase structure
```

### SECURITY_REVIEW Domain:
```python
Tools: vulnerability_scan, code_review_tools, security_pattern_matching
Focus: Finding security issues
```

### ARCHITECTURE_DESIGN Domain:
```python
Tools: component_mapping, dependency_analysis, system_visualization
Focus: Understanding system design
```

### GENERAL Domain:
```python
Tools: Standard tools + web_search
Focus: Broad information gathering
```

---

## Tool Recommendation Example

```python
from empirica.investigation import recommend_investigation_tools
from empirica.core.canonical import CanonicalEpistemicAssessor

# After assessment
assessment = await assessor.assess(task, context)

# Get tool recommendations
recommendations = recommend_investigation_tools(
    assessment=assessment,
    context=context,
    domain='code_analysis'
)

# Check recommendations
for rec in recommendations:
    print(f"Tool: {rec.tool_name}")
    print(f"Reason: {rec.reasoning}")
    print(f"Gap addressed: {rec.gap_addressed}")
    print(f"Expected confidence gain: {rec.confidence:.2f}")
    print()
```

**Output:**
```
Tool: workspace_scan
Reason: Map project structure to improve CONTEXT understanding
Gap addressed: context
Expected confidence gain: 0.35

Tool: documentation_search
Reason: Find authentication patterns to improve KNOW
Gap addressed: know
Expected confidence gain: 0.30
```

---

## Investigation Necessity Logic

**4 Skip Conditions:**

### 1. Confidence Already Met
```python
if overall_confidence >= threshold:
    skip_investigation()
    proceed_to_check()
```

### 2. Critical Flags Present
```python
if coherence < 0.50:  # Task incoherent
    skip_investigation()
    recommend_action('reset')

if density > 0.90:  # Cognitive overload
    skip_investigation()
    recommend_action('reset')

if change < 0.50:  # Cannot progress
    skip_investigation()
    recommend_action('stop')
```

### 3. ENGAGEMENT Gate Failed
```python
if engagement < 0.60:
    skip_investigation()
    recommend_action('clarify')  # Need user clarification first
```

### 4. No Improvable Gaps
```python
all_vectors_high = all(v >= 0.85 for v in vectors)
if all_vectors_high:
    skip_investigation()
    # Confidence issue is intrinsic, not fixable by investigation
```

---

## Custom Plugins

Extend investigation with custom tools:

```python
from empirica.investigation import InvestigationPlugin

# Define custom tool
jira_plugin = InvestigationPlugin(
    name='jira_search',
    description='Search JIRA for related issues',
    execute_fn=lambda ctx: search_jira(ctx['query']),
    improves_vectors=['know', 'context'],
    confidence_gain=0.25,
    domain_specific='code_analysis'
)

# Register plugin
from empirica.investigation import PluginRegistry
registry = PluginRegistry()
registry.register(jira_plugin)

# Use in cascade
cascade = CanonicalEpistemicCascade(
    investigation_plugins={'jira_search': jira_plugin}
)
```

**See:** [14_CUSTOM_PLUGINS.md](14_CUSTOM_PLUGINS.md) for details

---

## Bayesian Evidence Tracking

When Bayesian Guardian is active, tool results update beliefs:

```python
# Tool executed: documentation_search
evidence = Evidence(
    outcome=True,  # Success
    strength=0.8,  # Strong evidence
    vector_addressed='know'
)

# Update Bayesian belief
belief = bayesian_tracker.update_belief('task:know', evidence)
# belief.mean increases, belief.variance decreases

# Discrepancy detection in CHECK phase
if intuitive_know > belief.mean + 2σ:
    alert_overconfidence()
```

---

## Documentation Integration

To prevent knowledge loss and doc sprawl, Empirica provides doc-check suggestions at CHECK/POSTFLIGHT:

```bash
empirica doc-check --project-id <UUID> --output json
```

It computes a doc_completeness_score and suggests updates:
- Update investigation guides when many unresolved unknowns exist
- Update project-level tracking when many findings are logged
- Update CLI reference when new commands are added in this session

Heuristic target: score ≥ 0.8 before marking a goal complete.

## Investigation Best Practices

### Do:
✅ Trust the recommendations (they're strategic)
✅ Prioritize user clarification (highest gain)
✅ Limit rounds to 2-3 (diminishing returns)
✅ Re-assess after investigation
✅ Track evidence with Bayesian Guardian

### Don't:
❌ Investigate when ENGAGEMENT gate failed
❌ Skip re-assessment after tools
❌ Ignore recommended tools without reason
❌ Investigate beyond 3 rounds (plateau effect)

---

## Configuration

```python
cascade = CanonicalEpistemicCascade(
    action_confidence_threshold=0.70,  # When to stop investigating
    max_investigation_rounds=3,        # Maximum rounds
    enable_bayesian=True,             # Track evidence
    investigation_plugins={}          # Custom tools
)
```

---

## Phase 2: Epistemic Branching (Parallel Investigation)

**New in v4.0:** Support for parallel investigation branches with epistemic auto-merge.

### When to Use Branching

Branching helps when there are **multiple valid investigation approaches** and you want to:
1. Explore each path systematically
2. Measure which path yields best learning
3. Auto-merge the highest-value path

**Example Scenario:**
```
Task: Implement authentication
Approach 1: OAuth2 (complex, secure, industry standard)
Approach 2: JWT (simple, stateless, suitable for APIs)
Approach 3: OIDC (enterprise, federated identity)

Result: Create 3 branches, checkpoint each, merge highest scorer
```

### Branching Workflow

```bash
# 1. Create parallel investigation branches
empirica investigate-create-branch \
  --session-id <sid> \
  --investigation-path oauth2 \
  --preflight-vectors '{"engagement":0.95,"know":0.90,...}'

empirica investigate-create-branch \
  --session-id <sid> \
  --investigation-path jwt \
  --preflight-vectors '{"engagement":0.70,"know":0.65,...}'

empirica investigate-create-branch \
  --session-id <sid> \
  --investigation-path oidc \
  --preflight-vectors '{"engagement":0.88,"know":0.85,...}'

# 2. Perform investigation work in each branch (implicit, natural work)

# 3. Checkpoint each branch with postflight vectors
empirica investigate-checkpoint-branch \
  --branch-id <bid1> \
  --postflight-vectors '{"engagement":0.96,"know":0.93,...}' \
  --tokens-spent 2500 \
  --time-spent 45

# ... repeat for other branches

# 4. Trigger epistemic auto-merge
empirica investigate-merge-branches \
  --session-id <sid> \
  --round 1
```

### Epistemic Merge Score Formula

```
merge_score = (learning_delta × quality × confidence) / cost_penalty

Where:
- learning_delta = average gain in [know, do, context, clarity, signal]
- quality = (coherence + clarity + (1 - density)) / 3
- confidence = 1 - uncertainty (DAMPENER: uncertainty suppresses scores)
- cost_penalty = max(1.0, tokens_spent / 2000.0)
```

**Key Insight:** Uncertainty acts as a **dampener**, not just a measurement. High-uncertainty branches get lower merge scores even with good learning, preventing ambiguous approaches from winning.

### Branching Decision Gate

After checkpointing all branches, `investigate-merge-branches`:
1. Calculates `merge_score` for each branch
2. Selects **highest scorer as winner**
3. Records decision with full rationale
4. Updates branch status to `merged`

**Winner Selection Criteria:**
- Highest `merge_score` (explicit calculation)
- Learning-to-cost optimization (natural outcome of formula)
- Uncertainty-aware (high uncertainty = lower score)

### Multi-Round Branching

For complex tasks, run multiple branching rounds:

```bash
# Round 1: OAuth2 vs JWT vs OIDC → Winner: JWT
empirica investigate-merge-branches --session-id <sid> --round 1

# Round 2: JWT implementation approaches → Winner: JWT-RS256
empirica investigate-merge-branches --session-id <sid> --round 2

# Each round is recorded in merge_decisions table
```

---

## Next Steps

- **Custom Plugins:** [14_CUSTOM_PLUGINS.md](14_CUSTOM_PLUGINS.md)
- **API Reference:** [13_PYTHON_API.md](13_PYTHON_API.md)
- **Cascade Flow:** [06_CASCADE_FLOW.md](06_CASCADE_FLOW.md)
- **Flexible Handoffs:** [../guides/FLEXIBLE_HANDOFF_GUIDE.md](../guides/FLEXIBLE_HANDOFF_GUIDE.md)

---

**Investigation is guidance, not control. AI decides, Empirica suggests.** 🎯
