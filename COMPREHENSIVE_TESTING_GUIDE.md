# Empirica 1.0 - Comprehensive Testing Guide

**Purpose:** Complete end-to-end test of Empirica's CASCADE workflow  
**For:** All AI agents (Claude, Gemini, Qwen, MiniMax, etc.)  
**Time:** ~30 minutes  
**Goal:** Validate all features work correctly before public launch

---

## 🎯 What This Test Validates

✅ Bootstrap session creation  
✅ PREFLIGHT assessment  
✅ INVESTIGATE phase with explicit goal creation  
✅ Goal and task management  
✅ CHECK phase decision-making  
✅ ACT phase tracking  
✅ POSTFLIGHT reflection  
✅ session-end handoff generation  
✅ Bayesian belief tracking  
✅ Drift monitor calibration  

---

## 📋 Prerequisites

1. Empirica installed and working
2. MCP server running (for IDE agents) OR CLI access
3. Database initialized (`.empirica/sessions/sessions.db`)
4. Git repository (for git notes)

**Verify installation:**
```bash
python3 -m empirica.cli --help
sqlite3 ./.empirica/sessions/sessions.db "SELECT COUNT(*) FROM sessions;"
```

---

## 🚀 PHASE 1: Bootstrap Session

### Step 1.1: Create Session

**MCP Tool (IDE agents):**
```python
result = bootstrap_session(
    ai_id="test-agent-comprehensive",
    session_type="development",
    bootstrap_level=2
)

session_id = result["session_id"]
print(f"Session created: {session_id}")
```

**CLI (terminal agents):**
```bash
empirica bootstrap --level 2 --ai-id test-agent-comprehensive
# Copy the session_id from output
```

**Expected Output:**
```json
{
  "session_id": "abc123...",
  "ai_id": "test-agent-comprehensive",
  "bootstrap_level": 2,
  "components_loaded": 6
}
```

**Verify:**
```bash
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT session_id, ai_id FROM sessions WHERE ai_id LIKE '%test-agent%';"
```

✅ **Pass Criteria:** Session record created in database

---

## 🎯 PHASE 2: PREFLIGHT Assessment

### Step 2.1: Execute PREFLIGHT

**MCP Tool:**
```python
execute_preflight(
    session_id=session_id,
    prompt="Test complete Empirica workflow: bootstrap → goals → investigation → check → act → postflight → session-end. Validate all components work correctly."
)
```

**CLI:**
```bash
empirica preflight "Test complete workflow" --prompt-only
# Returns assessment prompt
```

### Step 2.2: Self-Assess (Be Honest!)

**MCP Tool:**
```python
submit_preflight_assessment(
    session_id=session_id,
    vectors={
        "engagement": 0.85,      # Am I engaged?
        "know": 0.70,            # What do I KNOW about testing?
        "do": 0.75,              # What can I DO?
        "context": 0.80,         # Do I understand the environment?
        "clarity": 0.85,         # Is the task clear?
        "coherence": 0.80,       # Does the plan make sense?
        "signal": 0.75,          # Is information quality good?
        "density": 0.60,         # Is this complex?
        "state": 0.80,           # Do I know current state?
        "change": 0.70,          # Can I track progress?
        "completion": 0.0,       # Haven't started yet
        "impact": 0.80,          # Do I understand consequences?
        "uncertainty": 0.30      # What's uncertain?
    },
    reasoning="Starting testing workflow. Know: Basic Empirica concepts. Don't know: Specific edge cases. Uncertainty: How drift monitor behaves, whether goal creation works correctly. Ready to investigate."
)
```

**CLI:**
```bash
empirica preflight-submit \
  --session-id <session-id> \
  --vectors '{"engagement": 0.85, "know": 0.70, "do": 0.75, ...}' \
  --reasoning "Starting testing..."
```

**Verify:**
```bash
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT COUNT(*) FROM preflight_assessments WHERE session_id = '<session-id>';"
```

✅ **Pass Criteria:** Preflight assessment saved (count = 1)

---

## 🔍 PHASE 3: INVESTIGATE Phase (With Goals!)

### Step 3.1: Create Goal Explicitly

**MCP Tool:**
```python
goal_result = create_goal(
    session_id=session_id,
    objective="Test all Empirica features",
    scope="task_specific",
    success_criteria=["All commands work", "Data persists correctly", "Handoff generates"]
)

goal_id = goal_result["goal_id"]
print(f"Goal created: {goal_id}")
```

**CLI:**
```bash
empirica goals-create \
  --session-id <session-id> \
  --objective "Test all Empirica features" \
  --scope task_specific \
  --success-criteria '["All commands work", "Data persists", "Handoff generates"]'
```

**Verify:**
```bash
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT id, objective FROM goals WHERE session_id = '<session-id>';"
```

✅ **Pass Criteria:** Goal record created

### Step 3.2: Break Down into Subtasks

**MCP Tool:**
```python
# Subtask 1: Test bootstrap
add_subtask(
    goal_id=goal_id,
    description="Verify bootstrap creates session correctly",
    epistemic_importance=0.9
)

# Subtask 2: Test goal system
add_subtask(
    goal_id=goal_id,
    description="Verify goal and task creation works",
    epistemic_importance=0.8
)

# Subtask 3: Test investigation tracking
add_subtask(
    goal_id=goal_id,
    description="Test investigate-log command",
    epistemic_importance=0.7
)

# Subtask 4: Test session-end
add_subtask(
    goal_id=goal_id,
    description="Verify handoff report generation",
    epistemic_importance=0.9
)
```

**CLI:**
```bash
empirica goals-add-subtask --goal-id <goal-id> --description "Verify bootstrap"
empirica goals-add-subtask --goal-id <goal-id> --description "Verify goals"
empirica goals-add-subtask --goal-id <goal-id> --description "Test investigate-log"
empirica goals-add-subtask --goal-id <goal-id> --description "Test session-end"
```

**Verify:**
```bash
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT COUNT(*) FROM tasks WHERE goal_id = '<goal-id>';"
```

✅ **Pass Criteria:** 4 tasks created

### Step 3.3: Log Investigation Findings

**MCP Tool:**
```python
# Log what you discover during investigation
investigate_log(
    session_id=session_id,
    findings=[
        "Bootstrap created session successfully",
        "Goal creation command works",
        "Subtasks added correctly",
        "Database schema is correct"
    ],
    evidence={
        "database_verified": True,
        "tables_checked": ["sessions", "goals", "tasks"],
        "record_count": 4
    }
)
```

**CLI:**
```bash
empirica investigate-log \
  --session-id <session-id> \
  --findings '["Bootstrap works", "Goals work", "Tasks work", "Schema correct"]' \
  --evidence '{"database_verified": true, "tables_checked": ["sessions", "goals", "tasks"]}'
```

**Verify:**
```bash
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT json_extract(context_json, '$.investigation_log') FROM cascades WHERE session_id = '<session-id>';" | jq .
```

✅ **Pass Criteria:** Investigation log contains 4 findings

### Step 3.4: Update Bayesian Beliefs

**MCP Tool:**
```python
# Query current beliefs
beliefs = query_bayesian_beliefs(
    session_id=session_id,
    context_key="empirica_testing"
)

print(f"Current beliefs: {beliefs}")

# Update beliefs based on evidence
# (Note: Bayesian beliefs update automatically based on cascade assessments)
```

**CLI:**
```bash
# Bayesian beliefs are tracked automatically through PREFLIGHT/CHECK/POSTFLIGHT
# No manual command needed - validates through drift monitor
```

---

## ✅ PHASE 4: CHECK Phase

### Step 4.1: Assess Readiness

**MCP Tool:**
```python
execute_check(
    session_id=session_id,
    findings=[
        "All bootstrap tests passed",
        "Goal system working correctly",
        "Investigation tracking functional",
        "Database persistence verified"
    ],
    remaining_unknowns=[
        "Drift monitor behavior not yet tested",
        "Handoff generation not yet validated"
    ],
    confidence_to_proceed=0.85
)
```

**CLI:**
```bash
empirica check \
  --session-id <session-id> \
  --findings '["Bootstrap passed", "Goals work", "Investigation works", "DB verified"]' \
  --unknowns '["Drift monitor untested", "Handoff not validated"]' \
  --confidence 0.85
```

### Step 4.2: Submit CHECK Assessment

**MCP Tool:**
```python
submit_check_assessment(
    session_id=session_id,
    vectors={
        "engagement": 0.90,      # Increased: engaged in testing
        "know": 0.85,            # Increased: learned system works
        "do": 0.85,              # Increased: demonstrated capability
        "context": 0.90,         # Increased: understand environment better
        "clarity": 0.90,         # Task remains clear
        "coherence": 0.85,       # Plan validated
        "signal": 0.85,          # Good evidence collected
        "density": 0.55,         # Less complex than expected
        "state": 0.90,           # Clear current state
        "change": 0.80,          # Tracking progress well
        "completion": 0.50,      # Halfway through
        "impact": 0.85,          # Understand impact
        "uncertainty": 0.15      # Reduced: most unknowns resolved
    },
    decision="proceed",
    reasoning="Investigation complete. Bootstrap, goals, tasks, investigate-log all working. Remaining: test act-log, postflight, session-end, drift monitor. Confidence high to proceed.",
    investigation_cycle=1
)
```

**CLI:**
```bash
empirica check-submit \
  --session-id <session-id> \
  --vectors '{"engagement": 0.90, "know": 0.85, ...}' \
  --decision proceed \
  --reasoning "Investigation complete, ready to act" \
  --cycle 1
```

**Verify:**
```bash
# Check that check-submit saved to BOTH tables
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT COUNT(*) FROM check_phase_assessments WHERE session_id = '<session-id>';"

sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT json_extract(context_json, '$.check_findings') FROM cascades WHERE session_id = '<session-id>';" | jq .
```

✅ **Pass Criteria:** Saved to both check_phase_assessments AND cascade.context_json

---

## 🎬 PHASE 5: ACT Phase

### Step 5.1: Execute Work (Complete Subtasks)

**MCP Tool:**
```python
# Get subtasks for goal
# (Manually track which ones you've completed)

# Complete subtask 1
complete_subtask(
    subtask_id="<task-1-id>",
    evidence="Verified bootstrap creates session with all required fields"
)

# Complete subtask 2
complete_subtask(
    subtask_id="<task-2-id>",
    evidence="Goals and tasks created successfully, linked to session"
)

# Complete subtask 3
complete_subtask(
    subtask_id="<task-3-id>",
    evidence="investigate-log saved findings to cascade.context_json"
)
```

**CLI:**
```bash
# List tasks to get IDs
empirica goals-list --session-id <session-id>

# Complete each task
empirica goals-complete-subtask --subtask-id <task-1-id> --evidence "Bootstrap verified"
empirica goals-complete-subtask --subtask-id <task-2-id> --evidence "Goals verified"
empirica goals-complete-subtask --subtask-id <task-3-id> --evidence "investigate-log verified"
```

### Step 5.2: Log Actions Taken

**MCP Tool:**
```python
act_log(
    session_id=session_id,
    actions=[
        "Completed bootstrap verification",
        "Completed goal system verification",
        "Completed investigation tracking verification",
        "Marked 3 subtasks as complete"
    ],
    artifacts=[
        "database queries executed",
        "verification tests passed"
    ],
    goal_id=goal_id
)
```

**CLI:**
```bash
empirica act-log \
  --session-id <session-id> \
  --actions '["Bootstrap verified", "Goals verified", "Investigation verified", "3 tasks complete"]' \
  --artifacts '["database queries", "tests passed"]' \
  --goal-id <goal-id>
```

**Verify:**
```bash
# Check act_log saved
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT json_extract(context_json, '$.act_log') FROM cascades WHERE session_id = '<session-id>';" | jq .

# Check final_action set
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT final_action FROM cascades WHERE session_id = '<session-id>';"
```

✅ **Pass Criteria:** act_log contains 4 actions, final_action is set

---

## 🔍 PHASE 6: Check Drift Monitor

**MCP Tool:**
```python
# Check for calibration drift
drift_result = check_drift_monitor(
    session_id=session_id,
    window_size=2  # Check last 2 assessments (PREFLIGHT and CHECK)
)

print(f"Drift detected: {drift_result.get('drift_detected')}")
print(f"Drift type: {drift_result.get('drift_type')}")
print(f"Pattern: {drift_result.get('pattern')}")
```

**CLI:**
```bash
# Drift monitor checks automatically through assessments
# Verify it's tracking:
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT drift_detected FROM sessions WHERE session_id = '<session-id>';"
```

✅ **Pass Criteria:** Drift monitor active (returns result, no errors)

---

## 🎓 PHASE 7: POSTFLIGHT Assessment

### Step 7.1: Execute POSTFLIGHT

**MCP Tool:**
```python
execute_postflight(
    session_id=session_id,
    task_summary="Completed comprehensive testing of Empirica 1.0. Verified: bootstrap, goal creation, task management, investigation tracking, CHECK phase, ACT phase, drift monitor. All features working correctly."
)
```

**CLI:**
```bash
empirica postflight <session-id> --prompt-only
# Returns prompt for assessment
```

### Step 7.2: Submit POSTFLIGHT (Honest Reflection!)

**MCP Tool:**
```python
submit_postflight_assessment(
    session_id=session_id,
    vectors={
        "engagement": 0.95,      # High engagement throughout
        "know": 0.95,            # Learned comprehensive system knowledge
        "do": 0.95,              # Demonstrated full capability
        "context": 0.95,         # Complete understanding
        "clarity": 0.95,         # Task fully clear
        "coherence": 0.95,       # Everything coheres
        "signal": 0.95,          # Excellent data quality
        "density": 0.45,         # Simpler than initially thought
        "state": 0.95,           # Perfect state awareness
        "change": 0.95,          # Tracked all progress
        "completion": 1.0,       # Task complete!
        "impact": 0.95,          # Understand full impact
        "uncertainty": 0.05      # Almost no uncertainty remaining
    },
    reasoning="Testing complete. Learned: All core features work correctly. Goals created explicitly, investigation tracked, actions logged, drift monitor functioning. Epistemic growth: know 0.70→0.95 (+0.25), do 0.75→0.95 (+0.20), uncertainty 0.30→0.05 (-0.25).",
    changes="All features validated working"
)
```

**CLI:**
```bash
empirica postflight-submit \
  --session-id <session-id> \
  --vectors '{"engagement": 0.95, "know": 0.95, "do": 0.95, ...}' \
  --changes "All features validated"
```

**Verify:**
```bash
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT COUNT(*) FROM postflight_assessments WHERE session_id = '<session-id>';"
```

✅ **Pass Criteria:** Postflight assessment saved

---

## 📊 PHASE 8: Session End & Handoff

### Step 8.1: Complete Remaining Subtask

**MCP Tool:**
```python
# Complete the last subtask (handoff generation)
complete_subtask(
    subtask_id="<task-4-id>",
    evidence="About to test session-end handoff generation"
)
```

### Step 8.2: End Session & Generate Handoff

**MCP Tool:**
```python
# Option A: Use session-end CLI command
# (MCP doesn't have session-end tool yet)
```

**CLI:**
```bash
empirica session-end --session-id <session-id>
```

**Expected Output:**
```
============================================================
SESSION END SUMMARY
============================================================
Session ID: abc123...
Cascades: 1
Duration: 25.5 minutes

Task: Test complete Empirica workflow

Key Findings (4):
  1. Bootstrap works correctly
  2. Goal system functional
  3. Investigation tracking working
  4. All features validated

Remaining Unknowns (0):

Next Session Context:
  High confidence gained (+0.25). Work validated and ready for next phase.

Epistemic Trajectory:
  Knowledge: 0.70 → 0.85 → 0.95
  Overall: +0.25

Productivity Metrics:
  Cascades run: 1
  Findings discovered: 8
  Actions taken: 4

============================================================
✅ Session ended successfully
📋 Query handoff: empirica handoff-query --session-id abc123...
============================================================
```

### Step 8.3: Verify Handoff Stored

**Query handoff:**
```bash
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT task_summary, key_findings_json FROM handoff_reports WHERE session_id = '<session-id>';"
```

**Check git notes:**
```bash
git notes list | grep empirica
git notes --ref=empirica/handoff/<session-id> show HEAD
```

✅ **Pass Criteria:** 
- Handoff report in database ✅
- Git notes created (optional) ✅
- Includes findings, actions, trajectory ✅

---

## 🎯 PHASE 9: Calibration Report

**MCP Tool:**
```python
calibration = get_calibration_report(session_id=session_id)

print("Calibration Report:")
print(f"  PREFLIGHT confidence: {calibration['preflight_confidence']}")
print(f"  POSTFLIGHT confidence: {calibration['postflight_confidence']}")
print(f"  Epistemic delta: {calibration['epistemic_delta']}")
print(f"  Status: {calibration['calibration']}")
```

**CLI:**
```bash
# Get full session summary
empirica sessions-show <session-id>
```

✅ **Pass Criteria:** Calibration status = "well_calibrated" (ideally)

---

## ✅ FINAL VERIFICATION CHECKLIST

Run these queries to verify everything:

```bash
# 1. Session exists
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT session_id, ai_id, start_time, end_time FROM sessions WHERE session_id = '<session-id>';"

# 2. Cascades completed
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT cascade_id, preflight_completed, check_completed, postflight_completed FROM cascades WHERE session_id = '<session-id>';"

# 3. Goals created
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT id, objective FROM goals WHERE session_id = '<session-id>';"

# 4. Tasks created and completed
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT id, description, is_completed FROM tasks WHERE goal_id IN (SELECT id FROM goals WHERE session_id = '<session-id>');"

# 5. Investigation log exists
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT json_extract(context_json, '$.investigation_log') FROM cascades WHERE session_id = '<session-id>';" | jq .

# 6. Act log exists
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT json_extract(context_json, '$.act_log') FROM cascades WHERE session_id = '<session-id>';" | jq .

# 7. Handoff report created
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT session_id, task_summary, json_array_length(key_findings_json) as findings_count FROM handoff_reports WHERE session_id = '<session-id>';"

# 8. Assessments saved (3 total: PREFLIGHT, CHECK, POSTFLIGHT)
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT 
    (SELECT COUNT(*) FROM preflight_assessments WHERE session_id = '<session-id>') as preflight,
    (SELECT COUNT(*) FROM check_phase_assessments WHERE session_id = '<session-id>') as check,
    (SELECT COUNT(*) FROM postflight_assessments WHERE session_id = '<session-id>') as postflight;"
```

**Expected Results:**
- Session: 1 row ✅
- Cascade: 1 row, all phases complete ✅
- Goals: 1 row ✅
- Tasks: 4 rows, all completed ✅
- Investigation log: Not empty ✅
- Act log: Not empty ✅
- Handoff: 1 row with 4+ findings ✅
- Assessments: 1 preflight, 1 check, 1 postflight ✅

---

## 📊 SUCCESS CRITERIA

### Core Features (Must Pass)
- [x] Bootstrap creates session
- [x] PREFLIGHT saves assessment
- [x] Goals created explicitly (not automatic)
- [x] Tasks added and completed
- [x] Investigation tracked via investigate-log
- [x] CHECK saves to both tables
- [x] Actions tracked via act-log
- [x] POSTFLIGHT saves assessment
- [x] session-end generates handoff
- [x] Handoff includes findings, actions, trajectory

### Advanced Features (Should Pass)
- [x] Bayesian beliefs tracked
- [x] Drift monitor functional
- [x] Git notes created (optional)
- [x] Epistemic deltas calculated
- [x] Calibration report accurate

### Data Quality (Must Verify)
- [x] All data persists to database
- [x] Context_json includes investigation_log and act_log
- [x] Handoff is semantic (not raw dumps)
- [x] Token count < 600 for handoff

---

## 🎉 TEST RESULTS REPORTING

**Report Format:**
```
Empirica 1.0 Testing Report
AI Agent: [Your Name/Model]
Date: [Date]
Duration: [Minutes]

✅ PASSED TESTS: [X/25]
❌ FAILED TESTS: [X/25]

Core Features: [X/10] passed
Advanced Features: [X/5] passed
Data Quality: [X/4] passed
Overall: [X/19] minimum required to pass

Issues Encountered:
- [Issue 1]
- [Issue 2]

Recommendations:
- [Recommendation 1]
- [Recommendation 2]

Conclusion: [PASS / FAIL / NEEDS WORK]
```

---

## 🚀 POST-TEST CLEANUP

```bash
# Optional: Clean up test session
empirica sessions-export <session-id> --output test-results.json
# Archive for reference, then delete if desired
```

---

## 📝 NOTES FOR DIFFERENT AI AGENTS

### Claude (MCP via Rovo/Cline)
- Has direct MCP tool access ✅
- Use MCP tools throughout ✅
- session-end must use CLI ⚠️

### Gemini (MCP)
- Has MCP tool access ✅
- May need to verify MCP server running
- Follow same pattern as Claude

### Qwen (MCP)
- Has MCP tool access ✅
- May have different MCP integration
- Verify MCP tools work before starting

### MiniMax (MCP)
- Has MCP tool access ✅
- May need configuration
- Test MCP server first

### CLI-Only Agents
- Use CLI commands throughout ✅
- All features accessible via CLI ✅
- Slightly more verbose but complete

---

## ✅ LAUNCH READINESS

If this test passes completely:
- ✅ System ready for 1.0 launch
- ✅ All features working as documented
- ✅ User trust model validated
- ✅ Documentation accurate

**Good luck testing!** 🚀
