# Work Distribution - Empirica Production Readiness

**Based on Rovo Dev's Deep Dive Findings**

**Date:** 2025-12-06
**Status:** Ready for parallel execution
**Confidence:** High - All tasks well-scoped with clear success criteria

---

## Overview

Rovo Dev identified 10 critical areas during real-time workflow testing. We've distributed work across the team:

| Owner | Task | Priority | Est. Time | Status |
|-------|------|----------|-----------|--------|
| **Qwen** | Schema validation script | 🔴 Critical | 4-6 hours | Pending |
| **Qwen** | Unit tests: Session continuity | 🔴 Critical | 6-8 hours | Pending |
| **Qwen** | Integration tests: Handoff reports | 🟠 High | 4-5 hours | Pending |
| **Qwen** | Integration tests: Goal tree persistence | 🟠 High | 4-5 hours | Pending |
| **Claude Code** | System prompt clarifications (CHECK logic) | 🟠 High | 2-3 hours | Pending |
| **Claude Code** | System prompt clarifications (Session workflow) | 🟠 High | 2-3 hours | Pending |
| **Claude Code** | System prompt clarifications (Goals/subtasks example) | 🟠 High | 2-3 hours | Pending |
| **Claude Code** | CLI ergonomics improvements | 🟠 High | 3-4 hours | Pending |
| **Claude Code** | CC-Switch immediate validation setup | 🟠 High | 1-2 hours | Pending |
| **Qwen** | Test remaining CLI commands | 🟠 High | 4-6 hours | Pending |

**Total Parallel Work:** ~40-50 hours of testing/documentation spread across team

---

## Priority 1: Critical Schema Issues (Qwen - 4-6 Hours)

### Task: Create Comprehensive Schema Validation Script

**Why Critical:** We found goals/subtasks schema mismatch by accident. How many others exist?

**Deliverable:** `schema_validator.py` - Automated detection of schema mismatches

**What It Does:**
```python
# For EACH table in database:
# 1. Get actual schema from DB
# 2. Get CREATE TABLE from code
# 3. Get all INSERT/SELECT statements from methods
# 4. Flag mismatches

# Output: Report of all schema inconsistencies found
```

**Files to Check:**
- `empirica/data/session_database.py` - All table definitions
- Database tables:
  - `sessions` ✅ Validate all methods use it correctly
  - `reflexes` ✅ Recently changed to unified table
  - `cascade_metadata` ❓ Deprecated?
  - `epistemic_assessments` ❓ How does it relate to reflexes?
  - `handoff_reports` ❓ All columns used?
  - `goals` ✅ Fixed schema this session, verify all methods
  - `subtasks` ✅ Fixed schema this session, verify all methods
  - Other tables?

**Success Criteria:**
- [ ] Script created that compares DB schema vs code definitions
- [ ] Script identifies all INSERT statements and their columns
- [ ] Script identifies all SELECT statements and their columns
- [ ] Script flags any column mismatches (extra, missing, type changes)
- [ ] Report generated showing all findings
- [ ] Any new mismatches documented for fixing

**Expected Output:**
```
SCHEMA VALIDATION REPORT
========================

✅ reflexes table
   - 16 columns in DB
   - 16 columns in CREATE TABLE
   - 12 methods use it
   - All INSERTs match schema ✓
   - All SELECTs match schema ✓

❌ handoff_reports table
   - 8 columns in DB
   - 10 columns in CREATE TABLE
   - Mismatch: Column 'task_summary' in CREATE but never inserted
   - Mismatch: Column 'xyz' inserted but not in schema
   - Methods affected: create_handoff_report()

✅ goals table
   - Recently fixed, all methods verified
```

---

## Priority 2: Session Continuity Tests (Qwen - 6-8 Hours)

### Task: Write Unit Tests for Multi-Session Workflows

**Why Critical:** Session switching is core to multi-day/multi-AI work. Needs verification.

**Deliverable:** `test_session_continuity.py` - Comprehensive session management tests

**Test Cases to Write:**

#### Test 1: Create Multiple Sessions and Switch Between Them
```python
def test_multiple_active_sessions():
    """
    Can I have multiple active sessions and switch between them?
    """
    # Create session 1
    session1 = db.create_session(ai_id="claude-code")

    # Start work in session 1
    db.create_reflex("PREFLIGHT", session1, vectors1)

    # Create session 2 (different task)
    session2 = db.create_session(ai_id="claude-code")

    # Start work in session 2
    db.create_reflex("PREFLIGHT", session2, vectors2)

    # Switch back to session 1, verify state
    reflex1 = db.query_reflexes(session1, "PREFLIGHT")
    assert reflex1.vectors == vectors1

    # Switch back to session 2, verify state
    reflex2 = db.query_reflexes(session2, "PREFLIGHT")
    assert reflex2.vectors == vectors2

    # List active sessions
    sessions = db.list_active_sessions(ai_id="claude-code")
    assert len(sessions) >= 2
```

#### Test 2: Session Aliases and Resume
```python
def test_session_aliases():
    """
    Are session aliases working?
    Can I reference sessions by alias like 'latest:active:claude-code'?
    """
    session_id = db.create_session(ai_id="claude-code")

    # Verify I can query using alias
    latest = db.get_session("latest:active:claude-code")
    assert latest.id == session_id

    # Can I get session summary?
    summary = db.get_session_summary(session_id)
    assert summary is not None
    assert summary.status == "active"
```

#### Test 3: Resume Previous Session
```python
def test_resume_previous_session():
    """
    Can I resume a session from a previous day?
    """
    # Session 1 - yesterday
    session1 = db.create_session(ai_id="claude-code")
    db.create_reflex("PREFLIGHT", session1, vectors1)
    db.create_goal(session1, "Test goal", 0.5, 0.5, 0.3)
    # ... do work
    db.end_session(session1)  # End yesterday's session

    # Session 2 - today (same task, resume)
    session2 = db.create_session(ai_id="claude-code")

    # Can I see goal from previous session?
    goals = db.query_goals(session2)  # Or should I query by goal_id directly?
    assert len(goals) > 0

    # Is the goal tree still there?
    goal_tree = db.get_goal_tree(goals[0].id)
    assert goal_tree is not None
```

#### Test 4: Session Data Isolation
```python
def test_session_isolation():
    """
    Are different sessions properly isolated?
    """
    session1 = db.create_session(ai_id="claude-code")
    session2 = db.create_session(ai_id="claude-sonnet")

    # Add data to session1
    db.create_reflex("PREFLIGHT", session1, {"know": 0.7})

    # Query reflexes from session2 should not see session1 data
    reflexes2 = db.query_reflexes(session2)
    assert len(reflexes2) == 0

    # Only session1 should have the reflex
    reflexes1 = db.query_reflexes(session1)
    assert len(reflexes1) == 1
```

**Success Criteria:**
- [ ] All 4 test cases pass
- [ ] Tests cover create, switch, resume, isolate scenarios
- [ ] Any failures documented with root cause
- [ ] Schema issues (if found) reported for Qwen to fix with validator

---

## Priority 2: Handoff Report Tests (Qwen - 4-5 Hours)

### Task: Write Integration Tests for Handoff Creation/Querying

**Why Important:** ~90% token reduction is huge, but needs verification that it works end-to-end

**Deliverable:** `test_handoff_reports.py` - Comprehensive handoff report tests

**Test Cases to Write:**

#### Test 1: Create Handoff Report After POSTFLIGHT
```python
def test_create_handoff_basic():
    """
    Can I create a handoff report with all fields?
    """
    session_id = db.create_session(ai_id="claude-code")

    # Complete a full workflow
    db.create_reflex("PREFLIGHT", session_id, preflight_vectors)
    db.create_reflex("CHECK/1", session_id, check_vectors)
    db.create_reflex("POSTFLIGHT", session_id, postflight_vectors)

    # Create handoff report
    handoff_id = db.create_handoff_report(
        session_id=session_id,
        task_summary="Investigated OAuth2 flow",
        key_findings=["Endpoint: /oauth/authorize", "Token endpoint: /oauth/token"],
        remaining_unknowns=["Token rotation strategy"],
        next_session_context="Ready to implement OAuth2",
        artifacts_created=["oauth.py", "jwt_handler.py"]
    )

    assert handoff_id is not None
    assert handoff_id != ""

    # Verify handoff was stored
    handoff = db.query_handoff_reports(ai_id="claude-code")[0]
    assert handoff.task_summary == "Investigated OAuth2 flow"
    assert len(handoff.key_findings) == 2
    assert len(handoff.artifacts_created) == 2
```

#### Test 2: Query Handoff Reports
```python
def test_query_handoff_reports():
    """
    Can I query handoff reports for a specific AI?
    """
    session1 = db.create_session(ai_id="claude-code")
    session2 = db.create_session(ai_id="claude-sonnet")

    # Create handoffs for both
    db.create_handoff_report(session1, "Code handoff", [...], [...], "...", [])
    db.create_handoff_report(session2, "Sonnet handoff", [...], [...], "...", [])

    # Query handoffs for claude-code only
    code_handoffs = db.query_handoff_reports(ai_id="claude-code")
    assert len(code_handoffs) >= 1
    assert code_handoffs[0].task_summary == "Code handoff"

    # Query handoffs for claude-sonnet only
    sonnet_handoffs = db.query_handoff_reports(ai_id="claude-sonnet")
    assert len(sonnet_handoffs) >= 1
    assert sonnet_handoffs[0].task_summary == "Sonnet handoff"

    # Verify isolation
    assert len(code_handoffs) != len(sonnet_handoffs)
```

#### Test 3: Handoff Report Includes Goal Tree
```python
def test_handoff_includes_goal_tree():
    """
    Does handoff report automatically include goal tree from session?
    """
    session_id = db.create_session(ai_id="claude-code")

    # Create goals
    goal_id = db.create_goal(session_id, "Understand OAuth", 0.6, 0.5, 0.3)
    subtask_id = db.create_subtask(goal_id, "Map endpoints", "high")
    db.update_subtask_findings(subtask_id, ["Endpoint: /authorize"])
    db.update_subtask_unknowns(subtask_id, ["Token rotation?"])

    # Create handoff
    handoff_id = db.create_handoff_report(
        session_id=session_id,
        task_summary="...",
        key_findings=[...],
        remaining_unknowns=[...],
        next_session_context="...",
        artifacts_created=[...]
    )

    # Verify handoff includes goal information
    handoff = db.query_handoff_reports(ai_id="claude-code")[0]

    # Question: Does handoff include goal_tree JSON?
    # Or must I separately query goal tree?
    if hasattr(handoff, 'goal_tree_json'):
        goal_tree = json.loads(handoff.goal_tree_json)
        assert goal_tree[0].id == goal_id
    else:
        # If not automatic, verify I can get it separately
        goal_tree = db.get_goal_tree(session_id)
        assert goal_tree[0].id == goal_id
```

#### Test 4: Next Session Loads Handoff Context
```python
def test_next_session_loads_handoff():
    """
    How does next session access previous handoff?
    """
    # SESSION 1
    session1 = db.create_session(ai_id="claude-code")
    goal1 = db.create_goal(session1, "Understand OAuth", 0.6, 0.5, 0.3)
    # ... work ...
    handoff1 = db.create_handoff_report(
        session1,
        "OAuth investigation complete",
        ["endpoints", "flow"],
        ["token rotation"],
        "Ready to implement",
        ["oauth.py"]
    )

    # SESSION 2 (next day, same AI)
    session2 = db.create_session(ai_id="claude-code")

    # How do I load the previous context?
    # Option A: Query handoff directly
    previous_handoffs = db.query_handoff_reports(ai_id="claude-code")
    assert len(previous_handoffs) >= 1

    # Option B: Load goal tree from previous session
    if hasattr(previous_handoffs[0], 'session_id'):
        prev_goals = db.get_goal_tree(previous_handoffs[0].session_id)
        # Continue from previous investigation

    # Option C: Something else?
    # This test should clarify the actual workflow
```

**Success Criteria:**
- [ ] All 4 test cases pass
- [ ] Handoff report creation verified
- [ ] Handoff querying verified
- [ ] Goal tree inclusion verified (or documented as separate)
- [ ] Next session loading workflow clarified
- [ ] Token reduction claim verified (if possible)

---

## Priority 2: Goal Tree Persistence Tests (Qwen - 4-5 Hours)

### Task: Write Integration Tests for Goal Continuity Across Sessions

**Why Important:** Goals are core to complex investigations spanning multiple sessions

**Deliverable:** `test_goal_persistence.py` - Goal tree continuity tests

**Test Cases to Write:**

#### Test 1: Create Goal, Log Findings, Resume in New Session
```python
def test_goal_continuation_across_sessions():
    """
    Can I work on a goal across multiple sessions?
    """
    # SESSION 1
    session1 = db.create_session(ai_id="claude-code")
    goal_id = db.create_goal(session1, "Understand OAuth2", 0.6, 0.5, 0.3)

    subtask1 = db.create_subtask(goal_id, "Map endpoints", "high")
    db.update_subtask_findings(subtask1, ["Auth: /authorize", "Token: /token"])
    db.update_subtask_unknowns(subtask1, ["Token expiration?"])

    subtask2 = db.create_subtask(goal_id, "Understand flow", "high")
    db.update_subtask_findings(subtask2, ["3-leg flow", "Authorization code"])
    db.update_subtask_unknowns(subtask2, ["Refresh token rotation?"])

    # End session 1
    # db.end_session(session1)  # optional

    # SESSION 2 (next day)
    session2 = db.create_session(ai_id="claude-code")

    # Can I query the same goal?
    goals = db.query_goals(session2, goal_id=goal_id)  # By goal ID?
    assert len(goals) == 1
    assert goals[0].objective == "Understand OAuth2"

    # Can I see all subtasks and previous findings?
    goal_tree = db.get_goal_tree(goal_id)
    assert len(goal_tree.subtasks) == 2
    assert "Auth: /authorize" in goal_tree.subtasks[0].findings
    assert "Token expiration?" in goal_tree.subtasks[0].unknowns

    # Can I add more findings?
    db.update_subtask_findings(subtask1,
        ["Auth: /authorize", "Token: /token", "Refresh: /refresh"])

    # Can I complete a subtask?
    db.complete_subtask(subtask1, evidence="Documented in design doc")

    # Verify in session 2
    subtask1_updated = db.get_subtask(subtask1)
    assert subtask1_updated.status == "completed"
```

#### Test 2: Complete_Subtask Method - Does It Update Status?
```python
def test_complete_subtask_updates_status():
    """
    Does complete_subtask() actually change the status field?
    """
    goal_id = db.create_goal(db.create_session(ai_id="test"), "Test", 0.5, 0.5, 0.3)
    subtask_id = db.create_subtask(goal_id, "Test subtask", "high")

    # Check initial status
    cursor = db.conn.cursor()
    cursor.execute("SELECT status FROM subtasks WHERE id = ?", (subtask_id,))
    initial_status = cursor.fetchone()[0]
    assert initial_status == "pending"

    # Complete it
    db.complete_subtask(subtask_id, evidence="Test evidence")

    # Check status changed
    cursor.execute("SELECT status, completion_evidence FROM subtasks WHERE id = ?", (subtask_id,))
    row = cursor.fetchone()
    assert row[0] == "completed", f"Status should be 'completed' but got '{row[0]}'"
    assert row[1] == "Test evidence", f"Evidence not stored: {row[1]}"
```

#### Test 3: Goal Status Progression
```python
def test_goal_status_progression():
    """
    How does a goal's status change?
    - Created: pending
    - All subtasks completed: completed?
    - Handoff created: archived?
    """
    session_id = db.create_session(ai_id="test")
    goal_id = db.create_goal(session_id, "Test", 0.5, 0.5, 0.3)

    # Create subtasks
    subtask1 = db.create_subtask(goal_id, "Task 1", "high")
    subtask2 = db.create_subtask(goal_id, "Task 2", "high")

    # Check initial goal status
    goal = db.get_goal(goal_id)
    assert goal.status == "pending"  # or "in_progress"?

    # Complete first subtask
    db.complete_subtask(subtask1, evidence="Done")

    # Check goal status - should it change?
    goal = db.get_goal(goal_id)
    # Is it still "pending"? "in_progress"?

    # Complete second subtask
    db.complete_subtask(subtask2, evidence="Done")

    # Check goal status - should be "completed" now?
    goal = db.get_goal(goal_id)
    # Expected: status == "completed"

    # Verify all subtasks are completed
    cursor = db.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM subtasks WHERE goal_id = ? AND status != 'completed'",
                   (goal_id,))
    incomplete_count = cursor.fetchone()[0]
    assert incomplete_count == 0
```

#### Test 4: Query Unknowns Summary (Critical for CHECK Gate)
```python
def test_query_unknowns_summary():
    """
    Does query_unknowns_summary() work?
    This is used in CHECK phase to decide proceed vs investigate
    """
    session_id = db.create_session(ai_id="test")
    goal_id = db.create_goal(session_id, "Test", 0.6, 0.5, 0.3)

    subtask1 = db.create_subtask(goal_id, "Task 1", "high")
    subtask2 = db.create_subtask(goal_id, "Task 2", "medium")

    # Add unknowns
    db.update_subtask_unknowns(subtask1, ["Unknown 1", "Unknown 2"])
    db.update_subtask_unknowns(subtask2, ["Unknown 3"])

    # Query unknowns summary
    summary = db.query_unknowns_summary(session_id)

    # What format is this in?
    # Expected structure:
    assert hasattr(summary, 'total_unknowns') or 'total_unknowns' in summary
    # assert summary.total_unknowns == 3

    # Or is it a list?
    # assert len(summary) == 3

    # Or nested by goal?
    # assert summary['goals'][goal_id]['unknowns_count'] == 3

    # Clarify actual return format and verify it works
```

**Success Criteria:**
- [ ] All 5 test cases pass
- [ ] Goal continuation verified across sessions
- [ ] Status progression clarified and tested
- [ ] complete_subtask() actually updates status
- [ ] query_unknowns_summary() works as documented
- [ ] Any schema issues identified for fixing

---

## Priority 3: System Prompt Clarifications (Claude Code - 2-3 Hours Each)

### Task 1: ADD CHECK Phase Decision Logic Section

**Current Problem:** "CHECK is a gate" is vague. Users don't know the actual decision rules.

**Document to Update:** `/home/yogapad/.claude/CLAUDE.md` (Empirica System Prompt v4.0)

**Section to Add (After "### CHECK (0-N Times - Gate Decision)"):**

```markdown
### CHECK Phase Decision Thresholds (v4.0)

**Decision Gate Logic:**

Before CHECK, query unknowns:
```python
summary = db.query_unknowns_summary(session_id)
# Returns: total_unknowns, breakdown by goal/subtask
```

**Proceed vs Investigate Decision:**

| Condition | Action | Reasoning |
|-----------|--------|-----------|
| unknowns ≤2 AND confidence ≥0.75 | **PROCEED** | High confidence, minimal open questions |
| unknowns >2 OR confidence <0.75 | **INVESTIGATE MORE** | Still too many unknowns or low confidence |
| First CHECK shows >5 unknowns | **Expect 2-3 more rounds** | Complex investigation needs time |

**CHECK Can Run Multiple Times:**

- Round 1: unknowns=5, confidence=0.65 → INVESTIGATE
- Round 2: unknowns=3, confidence=0.70 → INVESTIGATE
- Round 3: unknowns=1, confidence=0.80 → PROCEED

**No Penalty for Multiple Rounds:**
Each CHECK round collects findings, refines understanding. Going from "high uncertainty" to "high confidence" is the point.

**Example Workflow:**

```bash
# PREFLIGHT shows uncertainty=0.7 (high)
empirica preflight-submit --session-id xyz \
  --vectors '{"uncertainty": 0.7, "know": 0.6, ...}'

# Create goal + subtasks immediately
goal_id=$(empirica goal-create --session-id xyz \
  --objective "Understand payment processing" \
  --scope-breadth 0.6 --scope-duration 0.4)

# Investigate 1 hour
empirica investigate-log --session-id xyz \
  --finding "Webhook endpoint: /payments/webhook" \
  --unknown "Webhook signature validation method?"

# CHECK Round 1
unknown_count=$(empirica query-unknowns --session-id xyz | jq '.total')
# → 8 unknowns

empirica check --session-id xyz \
  --unknowns '["Webhook validation?", "Retry logic?", ...]' \
  --confidence 0.65

empirica check-submit --session-id xyz \
  --vectors '{"know": 0.65, ...}' \
  --decision "investigate"  # Too many unknowns, continue

# Investigate 30 more minutes
# ... log more findings ...

# CHECK Round 2
unknown_count=$(empirica query-unknowns --session-id xyz | jq '.total')
# → 2 unknowns (reduced from 8)

empirica check --session-id xyz \
  --unknowns '["Retry exponential backoff?", "Max retries?"]' \
  --confidence 0.78

empirica check-submit --session-id xyz \
  --vectors '{"know": 0.78, ...}' \
  --decision "proceed"  # Ready to implement

# ACT: Write the payment processor
# ...

# POSTFLIGHT
empirica postflight-submit --session-id xyz \
  --vectors '{"know": 0.88, ...}'  # +0.10 learning
```

**Your Role in Implementer Persona:**

Your persona allows 1-3 CHECK cycles (vs researcher who might do 5+). This is because:
- You prefer clarity before execution
- You learn faster through implementation
- You don't need exhaustive understanding
- 2-3 rounds usually get you to 0.75+ confidence

**Key Principle:**
The goal is INFORMATION QUALITY, not speed. If CHECK reveals you need 3 rounds, that's fine. Executing with low confidence is worse.
```

---

### Task 2: ADD Session Continuity Workflow Section

**Current Problem:** System prompt doesn't show the complete multi-session workflow. Users unclear on how to resume work.

**Section to Add (New section in "## VI. CASCADE WORKFLOW"):**

```markdown
### Multi-Session Continuity (v4.0)

**Scenario:** Work on complex task over 2+ sessions (same AI, different days OR handoff to another AI)

**SESSION 1: Initial Investigation**

```bash
# 1. Create session
session_id=$(empirica session-create --ai-id claude-code)

# 2. PREFLIGHT
empirica preflight --session-id $session_id \
  --prompt "Your task description here"

empirica preflight-submit --session-id $session_id \
  --vectors '{"engagement":0.85,"know":0.6,...}'

# 3. Create goal (if uncertainty >0.6)
goal_id=$(empirica goal-create --session-id $session_id \
  --objective "Understand payment processing" \
  --scope-breadth 0.6 --scope-duration 0.4)

# 4. Create subtasks for investigation areas
subtask1=$(empirica subtask-add --goal-id $goal_id \
  --description "Map payment endpoints" --importance high)

subtask2=$(empirica subtask-add --goal-id $goal_id \
  --description "Understand webhook flow" --importance high)

# 5. Investigate - log findings incrementally
empirica investigate-log --session-id $session_id \
  --finding "Found: Payment endpoint /api/payments/process" \
  --unknown "Webhook signature validation?"

# Update subtask with findings
empirica subtask-update --task-id $subtask1 \
  --findings '["Endpoint: /api/payments/process", "GET /status"]' \
  --unknowns '["Async processing?", "Webhook timeout?"]'

# 6. CHECK gates (0-3 rounds)
#    First CHECK
summary=$(empirica query-unknowns --session-id $session_id)
# If too many unknowns: investigate more

#    Second CHECK (after more investigation)
empirica check --session-id $session_id \
  --findings '["Async processing confirmed", "3-second timeout"]' \
  --unknowns '["Retry exponential backoff?"]' \
  --confidence 0.75

empirica check-submit --session-id $session_id \
  --vectors '{"know":0.75,"do":0.8,...}' \
  --decision "proceed"

# 7. POSTFLIGHT
empirica postflight --session-id $session_id \
  --task-summary "Completed payment flow investigation"

empirica postflight-submit --session-id $session_id \
  --vectors '{"engagement":0.9,"know":0.82,...}'

# 8. Create handoff report (before ending session)
handoff_id=$(empirica handoff-create --session-id $session_id \
  --task-summary "Payment flow documented" \
  --key-findings '["Async processing", "Webhook required"]' \
  --remaining-unknowns '["Retry strategy needs testing"]' \
  --next-session-context "Ready to implement payment processor" \
  --artifacts '["payment_design.md", "endpoint_spec.txt"]')
```

**SESSION 2: Resumption (Same AI, Different Day)**

```bash
# 1. Query previous handoff reports
handoffs=$(empirica handoff-query --ai-id claude-code --limit 3)
# Returns: List of recent handoff reports

# 2. Review previous context
# From handoff:
#   - task_summary: "Payment flow documented"
#   - key_findings: ["Async processing", "Webhook required"]
#   - remaining_unknowns: ["Retry strategy needs testing"]
#   - next_session_context: "Ready to implement..."

# 3. Load goal tree from previous session
previous_session=$(echo $handoffs | jq -r '.[0].session_id')
goals=$(empirica goal-tree --session-id $previous_session)
# Returns: Complete goal tree with all subtasks and findings

# 4. Create NEW session for this work
new_session=$(empirica session-create --ai-id claude-code)

# 5. Quick PREFLIGHT (you have context now)
empirica preflight --session-id $new_session \
  --prompt "Continue from previous: Implement payment processor based on design"

empirica preflight-submit --session-id $new_session \
  --vectors '{"engagement":0.85,"know":0.85,...}'
  # Note: know starts higher because you loaded context

# 6. Continue investigation/implementation
# You have full context from previous session:
# - What you learned
# - What you still don't know
# - What artifacts you created

# 7. Complete previous subtasks
empirica subtask-complete --task-id $subtask1 \
  --evidence "Documented in payment_implementation.py"

# 8. New investigation if needed
new_unknown=$(empirica investigate-log --session-id $new_session \
  --finding "Implemented async retry with exponential backoff" \
  --unknown "Should we cache webhook responses?")

# 9. CHECK based on remaining unknowns
empirica check --session-id $new_session \
  --confidence 0.8

# 10. POSTFLIGHT
empirica postflight-submit --session-id $new_session \
  --vectors '{"engagement":0.9,"know":0.9,...}'

# 11. Create handoff for next AI (if continuing)
empirica handoff-create --session-id $new_session \
  --task-summary "Payment processor fully implemented" \
  --key-findings '["Retry strategy: exponential backoff", "Cache strategy: no"]' \
  --remaining-unknowns '["Need to test under load"]' \
  --next-session-context "Ready for testing phase" \
  --artifacts '["payment_processor.py", "test_endpoints.py"]'
```

**SESSION 3: Handoff to Different AI**

```bash
# Claude Code finished, now Sonnet continues testing

# 1. Query handoff from Claude Code
handoffs=$(empirica handoff-query --from-ai-id claude-code)

# 2. Claude Sonnet creates new session
sonnet_session=$(empirica session-create --ai-id claude-sonnet)

# 3. Load Claude Code's goal tree + findings
prev_session=$(echo $handoffs | jq -r '.[0].session_id')
context=$(empirica session-context --session-id $prev_session)
# Returns: Full epistemic state + goal tree + unknowns

# 4. PREFLIGHT with high knowledge (from handoff)
empirica preflight --session-id $sonnet_session \
  --prompt "Test payment processor (already implemented by Claude Code)"

empirica preflight-submit --session-id $sonnet_session \
  --vectors '{"engagement":0.8,"know":0.8,...}'
  # Sonnet has context from Code's handoff

# 5. Sonnet's testing work continues
# ...

# Pattern: Each session builds on previous context via handoff reports
```

**Key Principles:**

1. **One Session = One Coherent Task**
   - Don't try to do 5 things in one session
   - Split into goal subtasks, not new sessions

2. **Handoff = Context Bridge**
   - Always create handoff if stopping
   - Includes goal tree + findings + unknowns
   - Saves ~90% of context tokens for next session

3. **New Session = Fresh PREFLIGHT**
   - Even if continuing same task
   - You have context now, so rating is higher
   - Measures what you learned since last session

4. **Goal Tree is Persistent**
   - Once created, accessible across all sessions
   - Subtasks stay until explicitly completed
   - Findings accumulate across sessions
   - Unknowns refine as you investigate

5. **Confidence Progression**
   - SESSION 1: Low (0.6), high uncertainty (0.7)
   - SESSION 2: Higher (0.8), investigation resolved
   - SESSION 3: Complete (0.9), ready for next phase

**Typical Multi-Day Task:**

```
Day 1 (Claude Code):
  PREFLIGHT: uncertainty=0.7, know=0.5
  Investigate + CREATE GOAL + 2 CHECKs
  POSTFLIGHT: uncertainty=0.2, know=0.8 (+0.30 learning)
  Create handoff

Day 2 (Claude Code):
  Load previous context
  PREFLIGHT: uncertainty=0.2, know=0.8 (starts where left off)
  Continue investigation or implementation
  POSTFLIGHT: uncertainty=0.05, know=0.9 (+0.10 more learning)
  Create handoff

Day 3 (Claude Sonnet):
  Load Claude Code's context
  PREFLIGHT: uncertainty=0.1, know=0.85 (trusts Code's investigation)
  Testing phase
  POSTFLIGHT: uncertainty=0.05, know=0.88
  Create handoff

Day 4 (Qwen):
  Load Sonnet's context
  PREFLIGHT: uncertainty=0.05, know=0.85
  Final QA phase
  POSTFLIGHT: completed with full confidence
```

**Summary:**

Multi-session work isn't about creating many sessions. It's about:
1. One goal per deep investigation
2. Multiple CHECK rounds within same session as needed
3. Handoff report when stopping
4. New session only when picking up again
5. Goal tree provides continuity
6. Each session shows learning delta

This structure enables true multi-day, multi-AI coordination.
```

---

### Task 3: ADD Goals/Subtasks Complete Example Section

**Current Problem:** System prompt mentions goals/subtasks but no complete end-to-end example.

**Section to Add (New section in "## VI. CASCADE WORKFLOW"):**

```markdown
### Goals/Subtasks: Complete End-to-End Example (v4.0)

**Scenario:** Complex investigation with high uncertainty

**WHEN TO USE GOALS:**
- Uncertainty >0.6 (too much to hold in head)
- Task has >3 distinct investigation areas
- Multiple days of work expected
- Other AIs might need to continue the work

**WHEN NOT TO USE:**
- Simple question that can resolve in 1-2 hours
- Already high confidence (0.8+)
- Straightforward implementation task

**EXAMPLE: Investigating OAuth2 Implementation Strategy**

```bash
# STEP 1: Session created, PREFLIGHT shows high uncertainty
session_id=$(empirica session-create --ai-id claude-code)

empirica preflight --session-id $session_id \
  --prompt "Investigate best OAuth2 flow for user-agent SPA application"

empirica preflight-submit --session-id $session_id \
  --vectors '{
    "engagement": 0.85,
    "know": 0.50,           # Low - OAuth2 has many flows
    "do": 0.60,             # Could learn
    "context": 0.55,
    "clarity": 0.50,        # Problem is clear but solution unclear
    "coherence": 0.60,
    "signal": 0.65,
    "density": 0.55,
    "state": 0.60,
    "change": 0.50,
    "completion": 0.05,     # Haven't started
    "impact": 0.70,
    "uncertainty": 0.65     # HIGH - multiple unknowns
  }'
# Key: uncertainty=0.65 (high) → CREATE GOAL

# STEP 2: Create goal immediately after PREFLIGHT
goal_id=$(empirica goal-create --session-id $session_id \
  --objective "Determine optimal OAuth2 flow for user-agent SPA" \
  --scope-breadth 0.7 \
  --scope-duration 0.4 \
  --scope-coordination 0.3)

echo "Created goal: $goal_id"
# → goal_id: 123e4567-e89b-12d3-a456-426614174000

# STEP 3: Break investigation into subtasks
subtask_endpoints=$(empirica subtask-add --goal-id $goal_id \
  --description "Map OAuth2 provider endpoints" \
  --importance high)

subtask_flows=$(empirica subtask-add --goal-id $goal_id \
  --description "Document OAuth2 flows (auth code, implicit, PKCE)" \
  --importance high)

subtask_security=$(empirica subtask-add --goal-id $goal_id \
  --description "Analyze security implications per flow" \
  --importance high)

subtask_implementation=$(empirica subtask-add --goal-id $goal_id \
  --description "Prototype selected flow" \
  --importance medium)

echo "Created 4 subtasks for investigation"

# STEP 4: Investigate - log findings incrementally
# Finding 1: Endpoints
empirica subtask-update --task-id $subtask_endpoints \
  --findings '[
    "Google OAuth2 endpoints: /authorize, /token, /userinfo",
    "Authorization code required (security best practice)",
    "PKCE support: recommended for SPAs (RFC 7636)"
  ]' \
  --unknowns '["Do all providers support PKCE?", "Revocation endpoint?"]'

# Finding 2: Flows
empirica subtask-update --task-id $subtask_flows \
  --findings '[
    "Authorization Code Flow: most secure, server required",
    "Implicit Flow: deprecated due to security issues",
    "Authorization Code + PKCE: perfect for SPA (no server backend)"
  ]' \
  --unknowns '["Refresh token rotation strategy?", "Token lifetime?"]'

# Finding 3: Security
empirica subtask-update --task-id $subtask_security \
  --findings '[
    "Authorization Code + PKCE is most secure for SPA",
    "Implicit Flow should not be used (token in URL fragment)",
    "Must validate state parameter to prevent CSRF"
  ]' \
  --unknowns '["SameSite cookie requirements?", "Token storage security?"]'

# STEP 5: Before CHECK, query unknowns summary
unknowns_summary=$(empirica query-unknowns --session-id $session_id)
echo "Current unknowns:"
echo $unknowns_summary | jq '.'
# Output example:
# {
#   "total_unknowns": 6,
#   "by_goal": {
#     "123e4567...": {
#       "unknowns": ["Do all providers support PKCE?", ...],
#       "count": 6
#     }
#   }
# }

# STEP 6: First CHECK
empirica check --session-id $session_id \
  --findings '[
    "Authorization Code + PKCE is the right choice",
    "All major providers support PKCE",
    "Must handle state, CSRF, token storage"
  ]' \
  --unknowns '[
    "Exact token lifetime recommendations?",
    "Refresh token rotation schedule?"
  ]' \
  --confidence 0.70

empirica check-submit --session-id $session_id \
  --vectors '{
    "know": 0.70,           # Improved from 0.50
    "uncertainty": 0.40,    # Reduced from 0.65
    "clarity": 0.75,        # Clear on which flow to use
    "completion": 0.40,
    ...
  }' \
  --decision "investigate"  # Still 2 unknowns, investigate more
# Note: confidence 0.70 < 0.75 threshold → INVESTIGATE

# STEP 7: Continue investigation
# Research token lifetime recommendations
empirica subtask-update --task-id $subtask_endpoints \
  --findings '[
    "...previous findings...",
    "Recommended token lifetime: 1 hour",
    "Refresh token lifetime: 1 week (max)"
  ]' \
  --unknowns '["Token rotation on refresh?"]'

# STEP 8: Second CHECK (round 2)
empirica check --session-id $session_id \
  --findings '[
    "Token lifetime: 1 hour (industry standard)",
    "Refresh token: rotates on each use (security best practice)"
  ]' \
  --unknowns '[]'  # All unknowns resolved!
  --confidence 0.82

empirica check-submit --session-id $session_id \
  --vectors '{
    "know": 0.82,           # Improved from 0.70
    "uncertainty": 0.15,    # Resolved unknowns
    "completion": 0.85,     # Almost done
    ...
  }' \
  --decision "proceed"  # confidence 0.82 >= 0.75 AND unknowns=0
# Decision: PROCEED to implementation

# STEP 9: Complete investigation subtasks
empirica subtask-complete --task-id $subtask_endpoints \
  --evidence "All endpoints documented in ENDPOINT_SPEC.md"

empirica subtask-complete --task-id $subtask_flows \
  --evidence "Flow comparison in OAUTH_FLOWS.md (rows 15-30)"

empirica subtask-complete --task-id $subtask_security \
  --evidence "Security analysis in SECURITY_REVIEW.md"

# STEP 10: Create prototype (subtask 4)
# ... write code ...
# After implementation complete:
empirica subtask-complete --task-id $subtask_implementation \
  --evidence "Prototype: src/auth/oauth-handler.ts + test coverage"

# STEP 11: All subtasks complete, mark goal complete
# (This might be automatic, or manual - clarify)

# STEP 12: POSTFLIGHT
empirica postflight --session-id $session_id \
  --task-summary "OAuth2 strategy determined and prototyped: Authorization Code + PKCE with 1-hour tokens"

empirica postflight-submit --session-id $session_id \
  --vectors '{
    "engagement": 0.90,
    "know": 0.88,           # +0.38 learning (from 0.50)
    "do": 0.85,
    "context": 0.87,
    "clarity": 0.92,        # Very clear now
    "uncertainty": 0.08,    # Almost no uncertainty
    "completion": 0.95,
    ...
  }'

# STEP 13: Create handoff report
# Goal tree is automatically included
handoff=$(empirica handoff-create --session-id $session_id \
  --task-summary "OAuth2 strategy: Authorization Code + PKCE selected and prototyped" \
  --key-findings '[
    "PKCE is standard for modern SPAs",
    "Refresh token rotation improves security",
    "1-hour token lifetime matches industry practice"
  ]' \
  --remaining-unknowns '[
    "Need to test with multiple providers",
    "Performance impact of token refresh?"
  ]' \
  --next-session-context "Implementation ready for testing phase" \
  --artifacts '[
    "ENDPOINT_SPEC.md",
    "OAUTH_FLOWS.md",
    "SECURITY_REVIEW.md",
    "src/auth/oauth-handler.ts"
  ]')

echo "Handoff created: $handoff"
```

**Learning Progression This Example:**

| Phase | Uncertainty | Know | Clarity | Completion |
|-------|-------------|------|---------|------------|
| PREFLIGHT | 0.65 | 0.50 | 0.50 | 0.05 |
| CHECK 1 | 0.40 | 0.70 | 0.75 | 0.40 |
| CHECK 2 | 0.15 | 0.82 | 0.92 | 0.85 |
| POSTFLIGHT | 0.08 | 0.88 | 0.92 | 0.95 |
| **Delta** | **-0.57** | **+0.38** | **+0.42** | **+0.90** |

**Key Observations:**

1. **Uncertainty drives goal creation**
   - PREFLIGHT: 0.65 uncertainty → CREATE GOAL
   - POSTFLIGHT: 0.08 uncertainty (resolved)

2. **Multiple CHECK rounds are normal**
   - Round 1: 0.70 confidence < 0.75 threshold → INVESTIGATE
   - Round 2: 0.82 confidence >= 0.75 → PROCEED
   - Two rounds was sufficient here

3. **Subtasks organize investigation**
   - 4 subtasks covered key areas
   - Each subtask tracked findings + unknowns
   - Reduced cognitive load vs mental tracking

4. **Goal tree enables continuity**
   - If Sonnet picked this up: goal tree shows all findings
   - No need to re-investigate
   - Unknowns are explicit

5. **Handoff report bridges sessions**
   - Next session gets: key findings + remaining unknowns + artifacts
   - ~90% context in ~3KB of data
   - Instead of entire session transcript

**This is the power of the goal/subtask system:**
- Reduces uncertainty systematically
- Enables collaboration (other AIs see your reasoning)
- Creates audit trail of investigation
- Accelerates multi-session work
```

---

### Task 4: CLI Ergonomics Improvements (Claude Code - 3-4 Hours)

**Current Problem:** CLI requires JSON format for parameters, no forgiving error messages

**Files to Update:**
- `empirica/cli/command_handlers/*.py` - All command handlers
- `empirica/cli/utils.py` - Parameter parsing helpers

**Changes Needed:**

#### 1. Add Parameter Validation Helper
```python
# empirica/cli/utils.py

def parse_json_array_or_string(value: str) -> list:
    """Parse JSON array or convert string to array."""
    if not value:
        return []

    # Try JSON first
    try:
        result = json.loads(value)
        if isinstance(result, list):
            return result
        else:
            raise ValueError(f"Expected JSON array, got {type(result).__name__}")
    except json.JSONDecodeError:
        # If not valid JSON, treat as single string
        # Could accept: --unknowns "Unknown 1" --unknowns "Unknown 2"
        # Or: --unknowns "Unknown 1, Unknown 2"
        return [value]

def parse_json_object_or_dict(value: str) -> dict:
    """Parse JSON object with helpful error message."""
    if not value:
        return {}

    try:
        result = json.loads(value)
        if isinstance(result, dict):
            return result
        else:
            raise ValueError(f"Expected JSON object, got {type(result).__name__}")
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Parameter must be valid JSON object.\n"
            f"Error: {e}\n"
            f"Example: --vectors '{{\"know\": 0.75, \"do\": 0.8, ...}}'\n"
            f"Got: {value}"
        )
```

#### 2. Improve Error Messages
```python
# Before (unhelpful)
json.loads(user_input)  # → JSONDecodeError: Expecting value...

# After (helpful)
try:
    result = json.loads(user_input)
except json.JSONDecodeError:
    raise click.UsageError(
        f"--unknowns must be a JSON array of strings.\n"
        f"✅ Correct:   --unknowns '[\"Unknown 1\", \"Unknown 2\"]'\n"
        f"❌ Incorrect: --unknowns 'Unknown 1'\n"
        f"Got: {user_input}"
    )
```

#### 3. Support Multiple --finding Flags
```bash
# Instead of requiring: --findings '["Finding 1", "Finding 2"]'
# Also accept: --finding "Finding 1" --finding "Finding 2"

# Example:
empirica investigate-log --session-id xyz \
  --finding "Endpoint: /authorize" \
  --finding "Token endpoint: /token" \
  --unknown "Webhook signature?"
```

**Success Criteria:**
- [ ] Helpful error messages for all JSON parameters
- [ ] Support both JSON and convenience formats where possible
- [ ] All error messages show examples of correct format
- [ ] No crashes, always give clear guidance
- [ ] Documentation updated with new syntax options

---

## Priority 3: System Prompt Updates (Claude Code - 2-3 Hours)

**Task:** Update `/home/yogapad/.claude/CLAUDE.md` with the 3 clarifications above

**File:** `/home/yogapad/.claude/CLAUDE.md`

**Sections to Add/Update:**

1. ✅ Section: "CHECK Phase Decision Thresholds (v4.0)" - Added above
2. ✅ Section: "Multi-Session Continuity (v4.0)" - Added above
3. ✅ Section: "Goals/Subtasks: Complete End-to-End Example (v4.0)" - Added above

**After Updates:**
- [ ] System prompt is 8-10 pages longer (comprehensive)
- [ ] All examples are runnable (matching actual CLI)
- [ ] Clear decision thresholds documented
- [ ] Multi-session workflow explicit
- [ ] Goals/subtasks usage obvious

---

## Priority 2: CC-Switch Validation Setup (Claude Code - 1-2 Hours)

**Current Status:** IMMEDIATE_SETUP_CLAUDE_GEMINI.md created and ready to use

**Task:** Follow validation guide (already created)

**Deliverable:** Validation report with findings

**Success Criteria:**
- [ ] CC-Switch cloned and built
- [ ] Claude Code provider configured
- [ ] Gemini provider configured
- [ ] Provider switching works (no manual editing)
- [ ] MCP server sync verified
- [ ] System prompts apply correctly
- [ ] Database persistence verified
- [ ] Report documenting any issues

---

## Priority 3: Test All Remaining CLI Commands (Qwen - 4-6 Hours)

**Current Status:** Basic commands tested, many missing

**Commands to Test:**

```bash
# Handoff operations
empirica handoff-create --session-id xyz ...
empirica handoff-query --ai-id claude-code
empirica handoff-query --from-ai-id claude-code

# Session management
empirica session-create
empirica session-show --session-id xyz
empirica session-summary --session-id xyz
empirica sessions-list
empirica sessions-show

# Goal operations
empirica goal-create --session-id xyz ...
empirica goal-tree --session-id xyz
empirica goals-list --session-id xyz

# Subtask operations
empirica subtask-add --goal-id xyz ...
empirica subtask-complete --task-id xyz ...
empirica subtask-update --task-id xyz ...

# Query operations
empirica query-unknowns --session-id xyz
empirica query-goals --session-id xyz

# Performance monitoring
empirica performance-metrics
```

**Test Template:**
```bash
# For each command, verify:
1. ✅ Command exists (no "command not found")
2. ✅ Help text works: empirica COMMAND --help
3. ✅ Parameter validation (gives clear error for invalid input)
4. ✅ Success case works
5. ✅ Return value matches documentation
6. ✅ Data persists (can query it back)
```

**Success Criteria:**
- [ ] All commands tested and verified working
- [ ] Any inconsistencies documented for fixing
- [ ] Schema issues (if found) reported to validator
- [ ] Parameter name consistency verified (MCP vs CLI)

---

## Timeline & Work Distribution

### This Week

| Day | Claude Code | Qwen | Copilot |
|-----|-------------|------|---------|
| **Today** | Start CC-Switch validation | Start schema validator | Start Copilot setup |
| **Tomorrow** | Finish CC-Switch validation | Run schema validator | Analyze Copilot config |
| **Weekend** | System prompt clarifications | Test session continuity | Finalize integration plan |
| **Mon** | Finish prompt updates + test them | Finish all unit tests | RFC ready |

### Expected Completion

- ✅ Schema validation: Friday (Qwen)
- ✅ All unit tests: Friday (Qwen)
- ✅ All integration tests: Friday (Qwen)
- ✅ System prompt clarity: Friday (Claude Code)
- ✅ CLI ergonomics: Friday (Claude Code)
- ✅ CC-Switch validation: Friday (Claude Code)
- ✅ Command testing: Friday (Qwen)

**By Monday Morning:**
- All schema issues identified and root causes documented
- All ambiguities in system prompt clarified with examples
- CC-Switch proven to work with existing CLIs
- All CLI commands verified to work as documented

---

## Success Metrics

### For Qwen (Testing & Schema)
- All 3 test suites pass (session continuity, handoff, goals)
- Zero schema mismatches remaining (or clearly documented)
- All CLI commands verified working
- No regressions from fixes

### For Claude Code (Prompts & CC-Switch)
- System prompt updated with 3 new sections + examples
- CHECK phase decision logic explicit with thresholds
- Session continuity workflow complete with examples
- Goals/subtasks end-to-end example runnable
- CLI ergonomics improved with helpful error messages
- CC-Switch validation complete with findings

### For Copilot CLI Team
- Copilot config format analyzed
- Integration plan updated
- RFC ready for Monday submission

---

## Questions for Clarification

During execution, capture answers to:

1. **Session Resume:** Can I resume exact same session UUID, or always create new?
2. **Complete Subtask:** Does method auto-update status, or separate step?
3. **Goal Status:** Does goal status auto-update as subtasks complete?
4. **Handoff Automatic:** Does handoff auto-include goal tree or manual?
5. **Query Unknowns:** What's exact return format of query_unknowns_summary()?
6. **Session Aliases:** Do aliases like "latest:active:claude-code" actually work?
7. **Handoff Querying:** When I query handoff reports, what's included vs separate query?

---

## Notes for Distribution

**For Qwen:**
- Focus on finding and documenting issues, not just passing tests
- Schema validation script is priority 1 (could uncover many issues)
- Unit tests verify the fixes
- Integration tests verify the full workflows

**For Claude Code:**
- System prompt needs to be very clear - these are examples for all AIs
- Include runnable bash commands (match actual CLI)
- Check all examples work before finalizing
- CC-Switch validation might raise new questions for Qwen to test

**For Copilot CLI Team:**
- Parallel stream: you should be autonomous
- Share findings with team in daily standup
- Coordinate with RFC timing (need Rovo Dev + Qwen ready by Friday for RFC)

---

**Status:** Ready for immediate parallel execution

**Confidence:** High - All work is well-scoped with clear success criteria

**Next:** Distribute tasks and begin parallel work streams
