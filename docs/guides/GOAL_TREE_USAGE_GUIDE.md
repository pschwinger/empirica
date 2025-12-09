# Goal Tree Usage Guide - Complete Reference

**Version:** 4.0  
**Audience:** Developers using Empirica for complex investigations  
**Status:** Comprehensive Guide  

---

## Table of Contents

1. [What is Goal Tracking?](#what-is-goal-tracking)
2. [When to Use Goals](#when-to-use-goals)
3. [Core Concepts](#core-concepts)
4. [Complete Workflow](#complete-workflow)
5. [Integration with CHECK](#integration-with-check)
6. [Multi-Session Handoff](#multi-session-handoff)
7. [Best Practices](#best-practices)
8. [Common Patterns](#common-patterns)
9. [Troubleshooting](#troubleshooting)

---

## What is Goal Tracking?

**Goal tracking** is Empirica's system for structured investigation management, enabling:

1. **Decision Quality** - CHECK phase uses unknowns to inform readiness
2. **Continuity** - Next AI sees complete investigation record
3. **Audit Trail** - Findings, unknowns, and dead_ends all tracked

### The Three Benefits

#### 1. Decision Quality
```python
# Without goals: "I think I understand enough?" (no evidence)
# With goals: query_unknowns_summary() → "2 unknowns, both non-blocking → PROCEED"
```

#### 2. Continuity
```python
# Without goals: Next AI starts from scratch
# With goals: get_goal_tree() → sees findings, unknowns, dead_ends
```

#### 3. Audit Trail
```python
# Without goals: Investigation process invisible
# With goals: Complete path from question → answer recorded
```

---

## When to Use Goals

### Complexity Levels

#### ⚠️ Simple Tasks - SKIP Goals
- **Characteristics:**
  - Single file changes
  - Low uncertainty (< 0.3)
  - < 30 minutes work
  - Clear path forward

- **Example:** "Fix typo in config file"
- **Approach:** Just do it, no goals needed

#### ✅ Medium Complexity - CONSIDER Goals
- **Characteristics:**
  - Multiple files involved
  - Moderate uncertainty (0.3-0.6)
  - Few hours work
  - Some unknowns to resolve

- **Example:** "Add rate limiting to API"
- **Approach:** Create goal if investigation needed

#### ✅ High Complexity - USE Goals
- **Characteristics:**
  - Multiple modules/systems
  - High uncertainty (> 0.6)
  - Multi-session work
  - Many unknowns

- **Example:** "Implement OAuth2 authentication"
- **Approach:** Always use goals

### Decision Flowchart

```
Start task
    ↓
Assess uncertainty (PREFLIGHT)
    ↓
uncertainty < 0.3? → Skip goals, proceed
    ↓
uncertainty 0.3-0.6? → Consider goals if multi-session
    ↓
uncertainty > 0.6? → Use goals
```

---

## Core Concepts

### Goals

**Purpose:** Track high-level investigation objectives with scope assessment

**Structure:**
```python
goal = {
    'goal_id': 'uuid',
    'objective': 'What are you trying to understand?',
    'scope_breadth': 0.0-1.0,      # How wide
    'scope_duration': 0.0-1.0,     # How long
    'scope_coordination': 0.0-1.0, # Multi-agent?
    'status': 'in_progress|complete|blocked'
}
```

### Subtasks

**Purpose:** Break down investigation into trackable units

**Structure:**
```python
subtask = {
    'subtask_id': 'uuid',
    'description': 'Specific investigation task',
    'importance': 'critical|high|medium|low',
    'findings': ['Discovery 1', 'Discovery 2', ...],
    'unknowns': ['Question 1', 'Question 2', ...],
    'dead_ends': ['Attempted X - blocked by Y', ...],
    'status': 'not_started|in_progress|complete'
}
```

### Investigation Tracking Fields

#### findings
**What you discovered**
- Log as you discover things
- Concrete observations
- Used for: Documentation, implementation reference, handoff

**Examples:**
```python
findings = [
    "Auth endpoint: /oauth/authorize",
    "PKCE required for public clients",
    "Refresh token format: JWT with 30-day expiry"
]
```

#### unknowns
**What remains unclear**
- Log questions that emerge
- **Critical for CHECK phase decisions**
- Used for: Readiness assessment, investigation planning

**Examples:**
```python
unknowns = [
    "How does MFA affect refresh flow?",
    "Best practice for token storage in mobile?",
    "Rate limiting on token endpoint?"
]
```

#### dead_ends
**Paths explored but blocked**
- Log attempts that failed
- Prevents duplicate investigation
- Used for: Audit trail, avoiding rework

**Examples:**
```python
dead_ends = [
    "JWT extension - security policy blocks custom claims",
    "Redis for session storage - infrastructure not available"
]
```

### Scope Vectors

**Purpose:** Assess investigation complexity

#### scope_breadth (How Wide)
| Value | Meaning | Example |
|-------|---------|---------|
| 0.0-0.2 | Single file | Fix one function |
| 0.3-0.5 | Few modules | Update auth system |
| 0.6-0.8 | Multiple systems | Implement OAuth2 |
| 0.9-1.0 | Entire codebase | Architecture refactor |

#### scope_duration (How Long)
| Value | Meaning | Example |
|-------|---------|---------|
| 0.0-0.2 | Minutes | Quick fix |
| 0.3-0.5 | Hours | Feature implementation |
| 0.6-0.8 | Days | Major feature |
| 0.9-1.0 | Weeks/Months | Large project |

#### scope_coordination (Multi-Agent)
| Value | Meaning | Example |
|-------|---------|---------|
| 0.0-0.2 | Solo | Individual task |
| 0.3-0.5 | Some coordination | Review required |
| 0.6-0.8 | Multi-agent | Collaborative work |
| 0.9-1.0 | Heavy coordination | Team project |

---

## Complete Workflow

### Step-by-Step: OAuth2 Implementation

```python
from empirica.data.session_database import SessionDatabase

db = SessionDatabase()
session_id = db.create_session(ai_id="oauth_project")

# === STEP 1: PREFLIGHT Assessment ===
# Assess initial state
preflight_vectors = {
    'engagement': 0.8,
    'know': 0.4,        # Don't fully understand OAuth2
    'do': 0.6,
    'uncertainty': 0.6  # High uncertainty
}
db.store_vectors(session_id, 'PREFLIGHT', preflight_vectors)

# Decision: High uncertainty → need structured investigation
# Create goal to track

# === STEP 2: Create Goal ===
goal_id = db.create_goal(
    session_id=session_id,
    objective="Understand OAuth2 authentication flow for secure API access",
    scope_breadth=0.6,      # Touches auth/, api/, config/
    scope_duration=0.4,     # Few hours of investigation
    scope_coordination=0.3  # Mostly solo, some docs review
)

# === STEP 3: Break Down Investigation ===
# Create subtasks for different aspects

endpoint_task = db.create_subtask(
    goal_id=goal_id,
    description="Map OAuth2 endpoints and request/response formats",
    importance='critical'
)

flow_task = db.create_subtask(
    goal_id=goal_id,
    description="Understand authorization code flow with PKCE",
    importance='critical'
)

security_task = db.create_subtask(
    goal_id=goal_id,
    description="Review security requirements and token management",
    importance='high'
)

# === STEP 4: Investigate & Log Incrementally ===

# Start with endpoint mapping
# [Read docs, examine code, test endpoints...]

db.update_subtask_findings(endpoint_task, [
    "Authorization endpoint: /oauth/authorize",
    "Requires: client_id, redirect_uri, state, code_challenge",
    "Returns: authorization code via redirect"
])

db.update_subtask_findings(endpoint_task, [
    "Token endpoint: /oauth/token (POST only)",
    "Requires: code, code_verifier, client_id",
    "Returns: access_token, refresh_token, expires_in"
])

db.update_subtask_unknowns(endpoint_task, [
    "Token expiration times not documented",
    "Refresh token rotation policy unclear"
])

# Continue with flow investigation
db.update_subtask_findings(flow_task, [
    "Authorization code flow: redirect → authorize → exchange code → tokens",
    "PKCE required for public clients (code_challenge)",
    "State parameter prevents CSRF attacks"
])

db.update_subtask_unknowns(flow_task, [
    "How does MFA integration affect the flow?"
])

# Security investigation
db.update_subtask_findings(security_task, [
    "Refresh tokens enabled with 30-day expiry",
    "Access tokens short-lived (1 hour)",
    "HTTPS required for all endpoints"
])

db.update_subtask_dead_ends(security_task, [
    "JWT custom claims extension - blocked by security policy",
    "Must use opaque tokens"
])

# === STEP 5: CHECK Phase Decision ===

# Query unknowns for readiness assessment
unknowns_summary = db.query_unknowns_summary(session_id)
print(f"Total unknowns: {unknowns_summary['total_unknowns']}")
# Output: Total unknowns: 3

# Evaluate each unknown:
# 1. "Token expiration" → Can check in implementation, non-blocker
# 2. "Refresh rotation" → Can implement basic flow first
# 3. "MFA integration" → Edge case, out of scope for MVP

# CHECK assessment with evidence
check_vectors = {
    'know': 0.8,         # Much better understanding
    'do': 0.8,           # Ready to implement
    'uncertainty': 0.25  # Low - 3 unknowns but all non-blocking
}

db.store_vectors(
    session_id=session_id,
    phase='CHECK',
    vectors=check_vectors,
    round_num=1,
    metadata={
        'decision': 'PROCEED',
        'confidence': 0.8,
        'unknowns_evaluated': [
            "Token expiration - can discover during implementation",
            "Refresh rotation - implement basic flow first",
            "MFA integration - edge case, out of MVP scope"
        ]
    },
    reasoning="3 unknowns remain but none block core implementation"
)

# === STEP 6: Implementation ===
# [Implement OAuth2 using findings from investigation...]

# === STEP 7: POSTFLIGHT Reflection ===
postflight_vectors = {
    'engagement': 0.9,
    'know': 0.85,        # Learned significantly
    'do': 0.9,           # Implementation successful
    'uncertainty': 0.15  # Low - clear understanding
}

db.store_vectors(
    session_id=session_id,
    phase='POSTFLIGHT',
    vectors=postflight_vectors,
    metadata={
        'task_summary': 'Implemented OAuth2 authorization code flow with PKCE',
        'calibration_accuracy': 'well-calibrated'
    },
    reasoning="Successfully implemented, learned OAuth2 patterns and security requirements"
)

# === STEP 8: Handoff Preparation ===
# Get complete goal tree for next session
goal_tree = db.get_goal_tree(session_id)

# goal_tree contains:
# - Goal objective and scope
# - All subtasks with descriptions
# - All findings (what was discovered)
# - All unknowns (what remains unclear)
# - All dead_ends (what was attempted but blocked)

db.close()
```

---

## Integration with CHECK

### The CHECK-Goals Connection

**Goals inform CHECK decisions but are separate from CASCADE phases.**

### Pattern: Evidence-Based CHECK

```python
# Step 1: Investigation phase - update subtasks
db.update_subtask_findings(task_id, ["Found X", "Discovered Y"])
db.update_subtask_unknowns(task_id, ["Question A?", "Question B?"])

# Step 2: CHECK decision point - query evidence
unknowns = db.query_unknowns_summary(session_id)

# Step 3: Evaluate unknowns
for goal_unknowns in unknowns['unknowns_by_goal']:
    print(f"Goal: {goal_unknowns['objective']}")
    print(f"Unknowns: {goal_unknowns['unknown_count']}")
    # Evaluate: Are these blockers?

# Step 4: Make evidence-based decision
if all_unknowns_are_non_blocking:
    decision = "PROCEED"
else:
    decision = "INVESTIGATE_MORE"

# Step 5: Store CHECK with evidence
db.store_vectors(
    session_id=session_id,
    phase='CHECK',
    vectors={'confidence': 0.75, 'uncertainty': 0.25},
    metadata={
        'decision': decision,
        'unknowns_summary': unknowns
    },
    reasoning="Evidence shows readiness to proceed"
)
```

### CHECK Decision Matrix

| Unknowns | Confidence | Decision | Reasoning |
|----------|------------|----------|-----------|
| 0 | ≥0.75 | PROCEED | High confidence, no unknowns |
| 1-2 | ≥0.70 | PROCEED | Few unknowns, evaluate if blockers |
| 1-2 | <0.70 | INVESTIGATE | Low confidence, need more clarity |
| 3+ | ≥0.70 | EVALUATE | Many unknowns, assess each one |
| 3+ | <0.70 | INVESTIGATE | Many unknowns + low confidence |

---

## Multi-Session Handoff

### Scenario: Session Ends Mid-Investigation

**Session 1 (You):**
```python
# Create goal and investigate
goal_id = db.create_goal(session_id, "Understand OAuth2 flow", ...)
subtask_id = db.create_subtask(goal_id, "Map endpoints", 'high')

# Log some discoveries
db.update_subtask_findings(subtask_id, [
    "Auth endpoint found",
    "PKCE required"
])

# Log remaining questions
db.update_subtask_unknowns(subtask_id, [
    "Token expiration unclear",
    "Refresh mechanism unknown"
])

# Session ends before completion
# Store goal tree in handoff
goal_tree = db.get_goal_tree(session_id)
```

**Session 2 (Next AI):**
```python
# Resume work - load previous investigation
goal_tree = db.get_goal_tree(previous_session_id)

# See exactly where you left off:
for goal in goal_tree:
    print(f"Goal: {goal['objective']}")
    for subtask in goal['subtasks']:
        print(f"  Findings: {len(subtask['findings'])} discoveries")
        print(f"  Unknowns: {len(subtask['unknowns'])} questions")
        # Continue where previous session stopped

# Continue investigation without duplication
```

### Handoff Pattern

Goal trees are automatically included in handoff reports for multi-agent coordination. See [`FLEXIBLE_HANDOFF_GUIDE.md`](FLEXIBLE_HANDOFF_GUIDE.md) for investigation handoff patterns (PREFLIGHT→CHECK) and complete handoff patterns (PREFLIGHT→POSTFLIGHT).

```python
# End of Session 1
from empirica.core.handoff import EpistemicHandoffReportGenerator

generator = EpistemicHandoffReportGenerator(db)
handoff_report = generator.generate_handoff_report(
    session_id=session_id,
    task_summary="OAuth2 investigation in progress",
    key_findings=[...],
    remaining_unknowns=[...],
    next_session_context="Continue with token management investigation"
)

# Goal tree automatically included in handoff report

# Start of Session 2
# Query handoff reports
handoffs = db.query_handoff_reports(ai_id="oauth_project", limit=1)
latest_handoff = handoffs[0]

# Load goal tree from handoff
goal_tree = latest_handoff['goal_tree']

# Resume work with complete context
```

---

## Best Practices

### 1. Create Goals During Work, Not Before

❌ **Anti-pattern:**
```python
# Don't pre-plan everything
goal = create_goal("Research OAuth2")
subtask1 = create_subtask("Step 1")
subtask2 = create_subtask("Step 2")
subtask3 = create_subtask("Step 3")
# Then do investigation
```

✅ **Correct:**
```python
# Start with goal, add subtasks as needed
goal = create_goal("Understand OAuth2 flow")

# Do some investigation
# [Discover endpoints are complex]

# Create subtask for this aspect
subtask1 = create_subtask("Map endpoints")

# Continue investigating
# [Discover PKCE is required]

# Create another subtask
subtask2 = create_subtask("Understand PKCE")
```

### 2. Update Incrementally

❌ **Anti-pattern:**
```python
# Don't wait until end
# [Do all investigation]
# [Then log everything at once]
update_findings([...50 findings...])
```

✅ **Correct:**
```python
# Log as you discover
# [Find endpoint]
update_findings(["Auth endpoint: /oauth/authorize"])

# [Find parameter requirement]
update_findings(["Requires: state param for CSRF"])

# [Encounter unknown]
update_unknowns(["Token expiration unclear"])
```

### 3. Be Specific in Descriptions

❌ **Anti-pattern:**
```python
findings = [
    "Found some stuff",
    "Figured out the thing",
    "It works"
]
```

✅ **Correct:**
```python
findings = [
    "Authorization endpoint: /oauth/authorize with state param",
    "PKCE code_challenge must use SHA256 hash",
    "Refresh tokens enabled with 30-day expiration"
]
```

### 4. Distinguish Findings vs Unknowns

**findings** = Concrete discoveries (what you learned)
**unknowns** = Open questions (what remains unclear)

```python
# Clear distinction
findings = [
    "Token endpoint returns JSON with access_token field"  # ✅ Concrete
]

unknowns = [
    "What happens if refresh token expires?"  # ✅ Question
]
```

### 5. Use Unknowns for CHECK

**Unknowns directly inform CHECK decisions:**

```python
# Good: Actionable unknowns that inform readiness
unknowns = [
    "Rate limiting on token endpoint?",  # Can affect implementation
    "MFA flow integration unclear"        # Might block implementation
]

# Query before CHECK
summary = query_unknowns_summary(session_id)
# Evaluate each unknown: Blocker? Non-blocker?
```

### 6. Don't Over-Structure Simple Tasks

If uncertainty < 0.3 and task < 30 min → Skip goals

```python
# Simple task: Fix typo
# ❌ Don't: Create goal, subtasks, log findings
# ✅ Do: Just fix it, log in POSTFLIGHT if desired
```

---

## Common Patterns

### Pattern 1: Single Goal, Multiple Subtasks

**Use when:** Investigation has clear aspects to explore

```python
goal = create_goal("Understand authentication system")

# Break down by aspect
subtask1 = create_subtask("Current implementation audit")
subtask2 = create_subtask("OAuth2 specification review")
subtask3 = create_subtask("Security requirements analysis")
```

### Pattern 2: Multiple Goals for Complex Work

**Use when:** Work has multiple independent objectives

```python
# Goal 1: Understanding
goal1 = create_goal("Understand OAuth2 specification")

# Goal 2: Implementation
goal2 = create_goal("Design OAuth2 integration architecture")

# Goal 3: Testing
goal3 = create_goal("Develop OAuth2 test strategy")
```

### Pattern 3: Iterative Investigation

**Use when:** Investigation reveals new areas to explore

```python
# Start with one goal
goal = create_goal("Understand API authentication")
subtask1 = create_subtask("Review current auth")

# During investigation, discover OAuth2 is complex
# Add subtasks as needed
subtask2 = create_subtask("Research OAuth2 flows")
subtask3 = create_subtask("Evaluate PKCE requirement")

# Multiple CHECK rounds
# CHECK round 1: Need more investigation
# CHECK round 2: Ready to proceed
```

---

## Troubleshooting

### Problem: Too Many Unknowns

**Symptom:** `query_unknowns_summary()` returns 10+ unknowns

**Solutions:**
1. **Break down investigation** - Create more focused subtasks
2. **Prioritize** - Which unknowns are blockers?
3. **Additional CHECK** - Run CHECK, then investigate more
4. **Scope reduction** - Can you implement a subset?

```python
# If overwhelmed with unknowns
unknowns = query_unknowns_summary(session_id)
if unknowns['total_unknowns'] > 10:
    # Evaluate: Which are blockers?
    blockers = identify_blocking_unknowns(unknowns)
    # Focus investigation on blockers only
```

### Problem: Goal Tree Too Deep

**Symptom:** Many goals, many subtasks, hard to navigate

**Solutions:**
1. **Consolidate** - Merge related goals
2. **Complete** - Mark finished subtasks complete
3. **Focus** - One goal at a time

```python
# Keep it manageable
# ❌ Bad: 5 goals x 10 subtasks = 50 items
# ✅ Good: 1-2 active goals, 3-5 subtasks each
```

### Problem: Findings Too Vague

**Symptom:** Findings like "figured it out", "it works"

**Solutions:**
1. **Be specific** - What exactly did you find?
2. **Include evidence** - Reference code, docs, endpoints
3. **Actionable** - Could someone implement from your findings?

```python
# ❌ Vague
findings = ["Auth works", "Need to use tokens"]

# ✅ Specific
findings = [
    "Auth endpoint: /oauth/authorize returns 302 redirect",
    "Access tokens must be included in Authorization header: Bearer <token>"
]
```

### Problem: Not Using CHECK

**Symptom:** Going straight from investigation to implementation

**Solutions:**
1. **Explicit CHECK** - Always query unknowns before major action
2. **Evidence-based** - Use `query_unknowns_summary()` for decision
3. **Document decision** - Store reasoning in CHECK

```python
# Always CHECK before implementing
# Step 1: Investigate
# Step 2: Query unknowns
unknowns = query_unknowns_summary(session_id)

# Step 3: Explicit CHECK
# Evaluate: Ready to proceed?

# Step 4: Store decision
store_vectors(phase='CHECK', metadata={'decision': ...})
```

---

## Summary

**Goals/subtasks enable:**
- ✅ Evidence-based CHECK decisions
- ✅ Efficient multi-session handoff
- ✅ Complete audit trail

**Use when:**
- Uncertainty > 0.3
- Multi-session work
- Complex investigations

**Update:**
- Incrementally during work
- Be specific in findings/unknowns
- Query unknowns before CHECK

**Result:** Systematic investigation, clear decisions, efficient continuity.

---

**See Also:**
- `06_CASCADE_FLOW.md` - How goals integrate with CASCADE
- `13_PYTHON_API.md` - Complete API reference
- `03_BASIC_USAGE.md` - Quick start examples
