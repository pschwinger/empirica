# Collaboration - Multi-Agent Coordination with Empirica

**How AIs work together with epistemic transparency**

[← Back to Home](index.md) | [Teams →](teams.md)

---

## Overview

Empirica enables multiple AI agents to collaborate on complex tasks while maintaining:
- ✅ Shared epistemic context (what each agent knows)
- ✅ Work continuity (no duplicate effort)
- ✅ Cryptographic accountability (who did what)
- ✅ Learning transfer (agents learn from each other)

---

## Collaboration Patterns

### 1. Sequential Handoff (Investigation → Implementation)

**Scenario:** AI 1 investigates, AI 2 implements

**Workflow:**

```python
# AI 1: Investigation
session_1 = session_create("researcher-ai")
goal_1 = create_goal(
    session_1,
    objective="Research OAuth2 best practices",
    scope={'breadth': 0.2, 'duration': 0.3, 'coordination': 0.0}
)
# ... investigate, gather findings ...
handoff_1 = create_handoff_report(
    session_1,
    task_summary="OAuth2 research complete",
    key_findings=[
        "PKCE prevents auth code interception",
        "Refresh token rotation mitigates theft",
        "Secure storage required for tokens"
    ],
    remaining_unknowns=["Token revocation at scale"],
    next_session_context="Ready for implementation"
)

# AI 2: Implementation (queries AI 1's handoff)
session_2 = session_create("implementer-ai")
reports = query_handoff_reports(ai_id="researcher-ai", limit=1)
# AI 2 now has full context from AI 1
# Implements based on AI 1's findings
```

**Benefits:**
- **75%+ token reduction** vs re-explaining context
- **No knowledge loss** between handoffs
- **Clear accountability** (AI 1 = research, AI 2 = code)

---

### 2. Parallel Exploration (Multiple Perspectives)

**Scenario:** Multiple AIs explore different approaches

**Workflow:**

```python
# Create shared goal
goal = create_goal(
    session_id=coordinator_session,
    objective="Evaluate authentication strategies",
    scope={'breadth': 0.4, 'duration': 0.5, 'coordination': 0.7}
)

# AI 1: Explores OAuth2
ai_1_session = session_create("oauth-specialist")
subtask_1 = add_subtask(goal, "Evaluate OAuth2 approach", "high")

# AI 2: Explores JWT
ai_2_session = session_create("jwt-specialist")
subtask_2 = add_subtask(goal, "Evaluate JWT approach", "high")

# AI 3: Explores SAML
ai_3_session = session_create("saml-specialist")
subtask_3 = add_subtask(goal, "Evaluate SAML approach", "high")

# Each AI completes their subtask
complete_subtask(subtask_1, evidence="OAuth2 analysis complete")
complete_subtask(subtask_2, evidence="JWT analysis complete")
complete_subtask(subtask_3, evidence="SAML analysis complete")

# Coordinator queries all findings
goal_progress = get_goal_progress(goal)
# Returns: 100% complete, all findings aggregated
```

**Benefits:**
- **Parallel work** (no blocking)
- **Diverse perspectives** (each AI specializes)
- **Aggregated knowledge** (all findings in one place)

---

### 3. Goal Discovery & Resume (Avoid Duplication)

**Scenario:** AI 2 discovers AI 1's incomplete work and resumes

**Workflow:**

```python
# AI 1: Starts work but doesn't complete
ai_1_session = session_create("ai-1")
goal_1 = create_goal(
    ai_1_session,
    objective="Implement rate limiting",
    scope={'breadth': 0.3, 'duration': 0.4, 'coordination': 0.0}
)
add_subtask(goal_1, "Research algorithms", "high")
complete_subtask(task_1, evidence="Research complete")
add_subtask(goal_1, "Implement token bucket", "critical")
# ... AI 1 stops (incomplete) ...

# AI 2: Discovers AI 1's work
ai_2_session = session_create("ai-2")
goals = discover_goals(from_ai_id="ai-1")
# Finds: "Implement rate limiting" goal (50% complete)

# AI 2: Resumes goal
resumed_goal = resume_goal(
    goal_id=goal_1,
    ai_id="ai-2"
)
# AI 2 continues from subtask 2 (token bucket implementation)
# No duplicate research work!
```

**Benefits:**
- **No work duplication** (AI 2 doesn't re-research)
- **Continuity** (picks up where AI 1 left off)
- **Accountability** (both AIs credited in git trail)

---

## Epistemic Handoff Mechanics

### What Gets Transferred

**Handoff report includes:**

1. **Task Summary** - What was accomplished
2. **Key Findings** - Validated knowledge (what's TRUE)
3. **Remaining Unknowns** - What's still unclear (breadcrumbs)
4. **Artifacts Created** - Files, commits, tests
5. **Next Session Context** - What to do next
6. **Epistemic State** - Final 13D vector (KNOW, DO, UNCERTAINTY, etc.)

**Example:**

```json
{
  "session_id": "abc123...",
  "ai_id": "researcher-ai",
  "task_summary": "OAuth2 research complete",
  "key_findings": [
    "PKCE prevents authorization code interception",
    "Refresh token rotation mitigates theft risk",
    "Secure storage required for refresh tokens"
  ],
  "remaining_unknowns": [
    "Token revocation strategy at scale",
    "Multi-device token management"
  ],
  "artifacts_created": [
    "docs/oauth2_analysis.md",
    "research/oauth2_threat_model.md"
  ],
  "next_session_context": "Ready for implementation. Use PKCE with refresh rotation.",
  "epistemic_state": {
    "know": 0.85,
    "do": 0.6,
    "uncertainty": 0.15
  }
}
```

---

### Query Patterns

**Query by AI ID:**
```python
# Get latest handoff from specific AI
reports = query_handoff_reports(ai_id="researcher-ai", limit=1)
```

**Query by Session ID:**
```python
# Get handoff for specific session
report = query_handoff_reports(session_id=session_id, limit=1)
```

**Query multiple handoffs:**
```python
# Get last 5 handoffs from any AI
reports = query_handoff_reports(ai_id="researcher-ai", limit=5)
```

---

## Git-Native Collaboration

### Cryptographic Signatures (Phase 2)

**Every session is cryptographically signed:**

```python
# AI 1 creates identity
create_identity(ai_id="ai-1")
# Generates Ed25519 keypair

# Session automatically signed
session_1 = session_create("ai-1")
# Signature stored in git notes

# AI 2 verifies authenticity
verification = verify_signature(session_id=session_1)
# Returns: {
#   "is_valid": true,
#   "ai_id": "ai-1",
#   "timestamp": "2025-12-09T18:00:00Z",
#   "public_key": "ed25519:abc123..."
# }
```

**Benefits:**
- **Proof of authorship** (can't forge AI identity)
- **Audit trail** (who did what, when)
- **Trust** (verify handoff authenticity)

---

### Git Notes for Discovery

**How goal discovery works:**

```bash
# AI 1 creates goal → stored in git notes
git notes --ref=empirica/goals/<GOAL_ID> add HEAD

# AI 2 discovers goals via git
git notes --ref=empirica/goals/* list

# AI 2 reads goal details
git notes --ref=empirica/goals/<GOAL_ID> show HEAD
```

**Benefits:**
- **Git-native** (no external coordination server)
- **Distributed** (works in any git repo)
- **Auditable** (full history in git)

---

## Coordination Strategies

### Strategy 1: Lead + Specialists

**Pattern:** One lead AI coordinates multiple specialist AIs

**Roles:**
- **Lead:** Creates goals, assigns subtasks, reviews findings
- **Specialists:** Complete specific subtasks, report findings

**Example:**

```python
# Lead AI
lead_session = session_create("lead-ai")
goal = create_goal(lead_session, objective="Build auth system", ...)

# Assign to specialists
add_subtask(goal, "Research OAuth2", importance="high")
add_subtask(goal, "Implement token service", importance="critical")
add_subtask(goal, "Write tests", importance="high")

# Specialists work in parallel
# (each queries goal, completes their subtask)

# Lead AI monitors progress
progress = get_goal_progress(goal)
# Sees: 66% complete (2/3 subtasks done)
```

---

### Strategy 2: Peer-to-Peer

**Pattern:** AIs collaborate as equals, no hierarchy

**Workflow:**
1. **Discover:** Each AI queries for existing goals
2. **Claim:** AI claims unclaimed subtask
3. **Complete:** AI completes subtask, creates handoff
4. **Repeat:** Next AI picks up next subtask

**Benefits:**
- **No bottleneck** (no single coordinator)
- **Resilient** (any AI can continue work)
- **Scalable** (add more AIs as needed)

---

### Strategy 3: Pipeline

**Pattern:** Linear pipeline of specialized AIs

**Example:** Research → Design → Implement → Test → Deploy

```
AI 1 (Research) → handoff → AI 2 (Design) → handoff → AI 3 (Implement)
```

**Each handoff includes:**
- Findings from previous stage
- Unknowns to address in next stage
- Artifacts created
- Next step guidance

---

## Anti-Patterns (What to Avoid)

### ❌ Duplicate Work

**Problem:** AI 2 doesn't query AI 1's handoff, duplicates research

**Solution:** **Always** `query_handoff_reports()` before starting

---

### ❌ Lost Context

**Problem:** AI 2 starts fresh, ignores AI 1's findings

**Solution:** Use `query_handoff_reports()` + `get_goal_subtasks()`

---

### ❌ Conflicting Work

**Problem:** AI 1 and AI 2 modify same file simultaneously

**Solution:** Use goal scope + subtask assignment to partition work

---

### ❌ No Accountability

**Problem:** Can't tell which AI did what

**Solution:** Git-signed sessions + git trail per AI

---

## Best Practices

### ✅ Do

1. **Query before starting:** Check for existing handoffs/goals
2. **Create handoffs:** Always handoff when stopping work
3. **Track findings:** Use subtasks to record discoveries
4. **Sign sessions:** Enable cryptographic signatures (Phase 2)
5. **Monitor progress:** Check `get_goal_progress()` regularly

### ⚠️ Consider

- Use lead AI for complex coordination
- Partition work by scope (breadth/duration)
- Set clear success criteria per subtask
- Review calibration across AIs (who learns fastest?)

---

## Real-World Example

### Multi-AI Website Redesign

**Goal:** Redesign website with 5 pages

**AI Team:**
1. **Designer AI** - Creates mockups, design system
2. **Content AI** - Writes copy, validates accuracy
3. **Developer AI** - Implements Astro pages
4. **QA AI** - Tests, identifies issues
5. **Coordinator AI** - Manages progress

**Workflow:**

```python
# Coordinator creates goal
goal = create_goal(
    session_id=coord_session,
    objective="Redesign website with 5 pages",
    scope={'breadth': 0.6, 'duration': 0.5, 'coordination': 0.8},
    success_criteria=["Design approved", "Content accurate", "All pages functional"]
)

# Designer completes design
add_subtask(goal, "Create design system", "critical")
complete_subtask(task_1, evidence="Figma mockups + color palette")
handoff_design = create_handoff_report(..., findings=["Glassmorphic design", "Indigo/cyan palette"])

# Content queries design handoff
reports = query_handoff_reports(ai_id="designer-ai", limit=1)
# Content writes copy matching design
add_subtask(goal, "Write page copy", "high")
complete_subtask(task_2, evidence="5 MD files created")

# Developer queries both handoffs
reports = query_handoff_reports(ai_id="content-ai", limit=1)
# Developer implements pages
add_subtask(goal, "Implement Astro pages", "critical")
# ... and so on
```

**Result:** 5 AIs collaborate efficiently, no duplicate work, full audit trail

---

## Next Steps

1. **Learn:** [Multi-Agent Teams](teams.md)
2. **Implement:** [Getting Started](getting-started.md)
3. **Coordinate:** Create goals, assign subtasks
4. **Handoff:** Query previous work, create handoffs

**Learn More:**
- [Goals & Subtasks](how-it-works.md#goals)
- [Cryptographic Identity](https://github.com/Nubaeon/empirica/blob/main/docs/production/26_CROSS_AI_COORDINATION.md)
- [Git Integration](MAKING_GIT_SEXY_AGAIN.md)

---

**Epistemic transparency enables genuine AI collaboration, not just parallel monologues.** 🤝
