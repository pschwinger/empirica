# Goal Orchestrator Integration - Master Implementation Plan

**Purpose:** Complete the CASCADE workflow by wiring in the goal orchestrator and tracking implicit INVESTIGATE/ACT decisions.

**Context:** This builds on completed work:
- ✅ Phase 1: Fixed database column bugs
- ✅ Phase 2.1: Separated ModalitySwitcher code
- ✅ Phase 2.2: Implemented session-end command

**Time Estimate:** 3-4 hours
**Session:** Can be done in next session using this plan
**Storage Pattern:** Git notes (optional) → SQLite (primary) → JSON (structure)

---

## 📊 CURRENT STATE vs TARGET STATE

### Current Workflow (Incomplete)
```
BOOTSTRAP → PREFLIGHT → [investigate] → CHECK → [act] → POSTFLIGHT → session-end
              ✅            ❌ implicit    ❌ no save   ❌ implicit      ✅           ✅
```

### Target Workflow (Complete)
```
BOOTSTRAP
  ↓
PREFLIGHT (assess: what do I know?)
  ↓
INVESTIGATE (find evidence, log findings)
  ├─ investigate-log --findings '[...]' --evidence '{...}'
  └─ Saves to: cascade.context_json + git notes
  ↓
CHECK (ready to proceed?)
  ├─ check --findings '[...]' --unknowns '[...]'
  ├─ check-submit --decision proceed
  ├─ Auto-generates goals from findings
  └─ Saves to: cascade.context_json + goals table + git notes
  ↓
ACT (execute tasks)
  ├─ act-log --actions '[...]' --artifacts '[...]'
  ├─ goals-complete-subtask (mark tasks done)
  └─ Saves to: cascade.final_action + cascade.context_json + git notes
  ↓
POSTFLIGHT (assess: what did I learn?)
  ↓
session-end (extract findings/goals/tasks → handoff)
```

---

## 🎯 IMPLEMENTATION TASKS

### Task 1: Fix CHECK command to save findings (30 minutes)

**Problem:** `check` command prints findings but doesn't save them to database or git notes.

**Files to modify:**
1. `empirica/cli/command_handlers/workflow_commands.py` (line 89-150)

**Changes:**
```python
def handle_check_command(args):
    """Handle check command - stores findings to CASCADE and git notes"""
    # Current: Just prints findings
    # New: Save to cascade.context_json + optional git notes
    
    # 1. Get or create active cascade
    # 2. Update context_json with check_findings, check_unknowns
    # 3. Mark check_completed = 1
    # 4. Save to SQLite
    # 5. Optional: Save to git notes refs/notes/empirica/cascades/{session}/{cascade}
```

**Database schema (already exists):**
```sql
cascades.context_json TEXT  -- Store findings here
cascades.check_completed BOOLEAN
```

**JSON structure in context_json:**
```json
{
  "check_findings": ["Finding 1", "Finding 2"],
  "check_unknowns": ["Unknown 1", "Unknown 2"],
  "check_confidence": 0.85,
  "check_timestamp": "2025-11-20T12:00:00Z"
}
```

**Git notes structure (optional):**
```
refs/notes/empirica/cascades/{session_id}/{cascade_id}
{
  "cascade_id": "abc123",
  "check_findings": [...],
  "check_unknowns": [...],
  "confidence": 0.85,
  "timestamp": "..."
}
```

**Testing:**
```bash
# Test saving findings
empirica check \
  --session-id <id> \
  --findings '["Bug found in line 217"]' \
  --unknowns '["Impact unknown"]' \
  --confidence 0.85

# Verify saved
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT context_json FROM cascades WHERE session_id = '<id>'" | jq .check_findings
```

---

### Task 2: Create investigate-log command (45 minutes)

**Problem:** No way to track investigation decisions during INVESTIGATE phase.

**New file:** `empirica/cli/command_handlers/action_commands.py`

**Function:**
```python
def handle_investigate_log_command(args):
    """
    Log investigation findings during INVESTIGATE phase
    
    Args:
        --session-id: Current session UUID
        --findings: JSON array of findings
        --evidence: JSON object with evidence (file paths, line numbers, etc.)
    
    Storage:
        SQLite: cascade.context_json["investigation_log"]
        Git notes: refs/notes/empirica/cascades/{session}/{cascade} (append)
    """
    # 1. Get active cascade
    # 2. Append to investigation_log in context_json
    # 3. Mark investigate_completed = 1
    # 4. Optional: Append to git note
```

**JSON structure:**
```json
{
  "investigation_log": [
    {
      "timestamp": "2025-11-20T10:30:00Z",
      "findings": ["Column mismatch in utility_commands.py"],
      "evidence": {"file": "utility_commands.py", "lines": "217-222"}
    },
    {
      "timestamp": "2025-11-20T10:45:00Z",
      "findings": ["12 total occurrences found"],
      "evidence": {"files": ["utility_commands.py"], "count": 12}
    }
  ]
}
```

**CLI registration:**
Add to `empirica/cli/cli_core.py`:
```python
def _add_action_parsers(subparsers):
    investigate_log_parser = subparsers.add_parser('investigate-log', 
        help='Log investigation findings')
    investigate_log_parser.add_argument('--session-id', required=True)
    investigate_log_parser.add_argument('--findings', required=True, 
        help='JSON array of findings')
    investigate_log_parser.add_argument('--evidence', 
        help='JSON object with evidence')
```

**Testing:**
```bash
# Log investigation
empirica investigate-log \
  --session-id <id> \
  --findings '["Found bug in line 217"]' \
  --evidence '{"file": "utility_commands.py", "lines": "217-222"}'

# Verify
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT context_json FROM cascades" | jq .investigation_log
```

---

### Task 3: Create act-log command (45 minutes)

**Problem:** No way to track actions taken during ACT phase.

**File:** `empirica/cli/command_handlers/action_commands.py` (same file as Task 2)

**Function:**
```python
def handle_act_log_command(args):
    """
    Log actions taken during ACT phase
    
    Args:
        --session-id: Current session UUID
        --actions: JSON array of actions taken
        --artifacts: JSON array of files modified/created
        --goal-id: Optional goal UUID being worked on
    
    Storage:
        SQLite: cascade.final_action + cascade.context_json["act_log"]
        Git notes: refs/notes/empirica/cascades/{session}/{cascade} (append)
    """
    # 1. Get active cascade
    # 2. Append to act_log in context_json
    # 3. Set final_action field (summary)
    # 4. Mark act_completed = 1
    # 5. Optional: Append to git note
```

**JSON structure:**
```json
{
  "act_log": [
    {
      "timestamp": "2025-11-20T11:00:00Z",
      "actions": ["Fixed line 217", "Fixed line 295"],
      "artifacts": ["utility_commands.py"],
      "goal_id": "goal-uuid-123"
    }
  ]
}
```

**Database:**
```sql
cascades.final_action TEXT  -- Summary: "Fixed 12 column name occurrences"
cascades.act_completed BOOLEAN
```

**CLI registration:**
```python
act_log_parser = subparsers.add_parser('act-log', 
    help='Log actions taken')
act_log_parser.add_argument('--session-id', required=True)
act_log_parser.add_argument('--actions', required=True, 
    help='JSON array of actions')
act_log_parser.add_argument('--artifacts', 
    help='JSON array of files modified')
act_log_parser.add_argument('--goal-id', 
    help='Goal UUID being worked on')
```

**Testing:**
```bash
# Log actions
empirica act-log \
  --session-id <id> \
  --actions '["Fixed line 217", "Tested fix"]' \
  --artifacts '["utility_commands.py"]'

# Verify
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT final_action FROM cascades WHERE session_id = '<id>'"
```

---

### Task 4: Wire goal orchestrator into check-submit (1 hour)

**Problem:** Goals exist but aren't auto-generated from CHECK findings.

**File:** `empirica/cli/command_handlers/workflow_commands.py` (line 153-240)

**Changes to handle_check_submit_command:**
```python
def handle_check_submit_command(args):
    # ... existing code ...
    
    # NEW: Auto-generate goals if confidence high enough
    if decision == "proceed" and confidence >= 0.7:
        try:
            from empirica.core.canonical.goal_orchestrator_bridge import CanonicalGoalOrchestrator
            from empirica.core.goals.repository import GoalRepository
            import subprocess
            
            # Get findings from CHECK (stored in context_json)
            cursor.execute("""
                SELECT cascade_id, context_json FROM cascades 
                WHERE session_id = ? AND completed_at IS NULL
                ORDER BY started_at DESC LIMIT 1
            """, (session_id,))
            
            result = cursor.fetchone()
            if result:
                cascade_id, context_json_str = result
                context = json.loads(context_json_str) if context_json_str else {}
                findings = context.get('check_findings', [])
                
                if findings:
                    # Generate goals using orchestrator
                    orchestrator = CanonicalGoalOrchestrator(session_id)
                    goals = orchestrator.generate_goals_from_context(
                        context={"findings": findings},
                        conversation=""
                    )
                    
                    # Save goals to database
                    goal_repo = GoalRepository()
                    goal_ids = []
                    
                    for goal in goals:
                        goal_repo.save(goal)
                        goal_ids.append(goal.id)
                        
                        # Optional: Save to git notes
                        try:
                            note_ref = f"refs/notes/empirica/goals/{session_id}/{goal.id}"
                            goal_data = {
                                "id": goal.id,
                                "objective": goal.objective,
                                "scope": goal.scope.value,
                                "created_from_findings": True,
                                "findings": findings
                            }
                            subprocess.run(
                                ['git', 'notes', '--ref', note_ref, 'add', '-f', '-m',
                                 json.dumps(goal_data), 'HEAD'],
                                capture_output=True,
                                timeout=5
                            )
                        except Exception as e:
                            logger.debug(f"Git notes optional: {e}")
                    
                    # Link goals to cascade
                    context['generated_goals'] = goal_ids
                    cursor.execute("""
                        UPDATE cascades 
                        SET context_json = ?, goal_id = ?
                        WHERE cascade_id = ?
                    """, (json.dumps(context), goal_ids[0] if goal_ids else None, cascade_id))
                    
                    db.conn.commit()
                    
                    print(f"✨ Auto-generated {len(goals)} goals from findings")
                    for goal in goals:
                        print(f"   • {goal.objective}")
                    
        except Exception as e:
            logger.warning(f"Could not auto-generate goals: {e}")
            # Don't fail check-submit if goal generation fails
```

**Database updates:**
```sql
-- Link goal to cascade
UPDATE cascades SET goal_id = '<goal-uuid>' WHERE cascade_id = '<cascade-id>';

-- Store goal IDs in context
UPDATE cascades SET context_json = json_set(context_json, '$.generated_goals', '["uuid1", "uuid2"]');
```

**Testing:**
```bash
# Run check-submit with findings
empirica check --session-id <id> --findings '["Bug found"]' --confidence 0.85
empirica check-submit --session-id <id> --vectors '{...}' --decision proceed

# Verify goals created
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT objective FROM goals WHERE session_id = '<id>'"

# Verify linked to cascade
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT goal_id FROM cascades WHERE session_id = '<id>'"
```

---

### Task 5: Update session-end to extract goals (30 minutes)

**Problem:** session-end doesn't extract goals/tasks from cascades.

**File:** `empirica/core/handoff/auto_generator.py` (line 150+)

**Changes to auto_generate_handoff:**
```python
def auto_generate_handoff(session_id: str, db_path: str = "./.empirica/sessions/sessions.db") -> Dict:
    # ... existing code ...
    
    # NEW: Extract goals from cascades
    goals_completed = []
    tasks_completed = []
    
    cursor.execute("""
        SELECT DISTINCT goal_id, goal_json FROM cascades 
        WHERE session_id = ? AND goal_id IS NOT NULL
    """, (session_id,))
    
    for goal_id, goal_json in cursor.fetchall():
        # Try git notes first (most semantic)
        try:
            note_ref = f"refs/notes/empirica/goals/{session_id}/{goal_id}"
            result = subprocess.run(
                ['git', 'notes', '--ref', note_ref, 'show', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                goal_data = json.loads(result.stdout)
                goals_completed.append(goal_data['objective'])
        except:
            # Fallback to SQLite
            cursor.execute("SELECT objective FROM goals WHERE id = ?", (goal_id,))
            obj = cursor.fetchone()
            if obj:
                goals_completed.append(obj[0])
        
        # Get tasks for this goal (if tasks table exists)
        try:
            cursor.execute("""
                SELECT description FROM tasks 
                WHERE goal_id = ? AND is_completed = 1
            """, (goal_id,))
            for (desc,) in cursor.fetchall():
                tasks_completed.append(desc)
        except:
            pass  # Tasks table optional
    
    # Add to handoff data
    handoff_data['goals_achieved'] = goals_completed[:5]  # Top 5
    handoff_data['tasks_completed'] = tasks_completed[:10]  # Top 10
    handoff_data['productivity_metrics'] = {
        'goals_created': len(goals_completed),
        'tasks_completed': len(tasks_completed),
        'cascades_run': len(cascades)
    }
    
    return handoff_data
```

**Updated handoff JSON structure:**
```json
{
  "session_id": "...",
  "task_summary": "Fixed database bugs",
  "key_findings": ["Column mismatch found", ...],
  "goals_achieved": ["Fix database column names", "Separate ModalitySwitcher"],
  "tasks_completed": ["Update line 217", "Update line 295", ...],
  "productivity_metrics": {
    "goals_created": 4,
    "tasks_completed": 12,
    "cascades_run": 4
  },
  "epistemic_deltas": {...}
}
```

**Testing:**
```bash
# End session with goals
empirica session-end --session-id <id>

# Verify handoff includes goals
empirica handoff-query --session-id <id> | jq .goals_achieved
```

---

## 📋 COMPLETE IMPLEMENTATION CHECKLIST

### Phase 1: Fix CHECK to save findings (30 min)
- [ ] Modify `handle_check_command` in `workflow_commands.py`
- [ ] Save findings to `cascade.context_json`
- [ ] Mark `check_completed = 1`
- [ ] Optional: Save to git notes
- [ ] Test with real CHECK command

### Phase 2: Add investigate-log command (45 min)
- [ ] Create `action_commands.py`
- [ ] Implement `handle_investigate_log_command`
- [ ] Add CLI parser to `cli_core.py`
- [ ] Register in `command_handlers/__init__.py`
- [ ] Test logging investigation findings

### Phase 3: Add act-log command (45 min)
- [ ] Add `handle_act_log_command` to `action_commands.py`
- [ ] Set `cascade.final_action` and `act_completed`
- [ ] Add CLI parser to `cli_core.py`
- [ ] Register in `command_handlers/__init__.py`
- [ ] Test logging actions

### Phase 4: Wire goal orchestrator (1 hour)
- [ ] Modify `handle_check_submit_command` in `workflow_commands.py`
- [ ] Call `CanonicalGoalOrchestrator.generate_goals_from_context()`
- [ ] Save goals to database via `GoalRepository`
- [ ] Link goals to cascade via `goal_id` column
- [ ] Optional: Save to git notes
- [ ] Test goal auto-generation

### Phase 5: Update session-end (30 min)
- [ ] Modify `auto_generate_handoff` in `auto_generator.py`
- [ ] Extract goals from cascades
- [ ] Try git notes first, fallback to SQLite
- [ ] Add `goals_achieved` and `productivity_metrics` to handoff
- [ ] Test full workflow end-to-end

---

## 🧪 END-TO-END TESTING SCRIPT

```bash
#!/bin/bash
# Test complete goal orchestrator integration

SESSION_ID=$(empirica bootstrap --level 2 --ai-id test-goal-integration | jq -r .session_id)

echo "Session: $SESSION_ID"

# CASCADE 1: PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT

# PREFLIGHT
empirica preflight "Fix database bugs" --prompt-only
empirica preflight-submit --session-id $SESSION_ID --vectors '{"know": 0.60, "do": 0.70, "uncertainty": 0.40}' --reasoning "Starting investigation"

# INVESTIGATE (NEW!)
empirica investigate-log \
  --session-id $SESSION_ID \
  --findings '["Found column mismatch in utility_commands.py"]' \
  --evidence '{"file": "utility_commands.py", "lines": "217-222"}'

# CHECK (NOW SAVES FINDINGS!)
empirica check \
  --session-id $SESSION_ID \
  --findings '["12 occurrences of started_at/ended_at found"]' \
  --unknowns '["Impact on running queries unknown"]' \
  --confidence 0.85

empirica check-submit \
  --session-id $SESSION_ID \
  --vectors '{"know": 0.85, "do": 0.85, "uncertainty": 0.15}' \
  --decision proceed

# Should see: "✨ Auto-generated 1 goals from findings"

# ACT (NEW!)
empirica act-log \
  --session-id $SESSION_ID \
  --actions '["Fixed line 217", "Fixed line 295", "Tested sessions-list"]' \
  --artifacts '["utility_commands.py"]'

# POSTFLIGHT
empirica postflight $SESSION_ID --prompt-only
empirica postflight-submit --session-id $SESSION_ID --vectors '{"know": 0.90, "do": 0.90, "uncertainty": 0.10}' --changes "Fixed database bugs"

# SESSION-END (NOW INCLUDES GOALS!)
empirica session-end --session-id $SESSION_ID

# VERIFY
echo ""
echo "Verifying results:"
echo "1. Check findings saved:"
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT json_extract(context_json, '$.check_findings') FROM cascades WHERE session_id = '$SESSION_ID'"

echo ""
echo "2. Goals created:"
sqlite3 ./.empirica/sessions/sessions.db \
  "SELECT objective FROM goals WHERE session_id = '$SESSION_ID'"

echo ""
echo "3. Goals in handoff:"
empirica handoff-query --session-id $SESSION_ID | jq .goals_achieved

echo ""
echo "✅ Test complete!"
```

---

## 🎯 DECISION POINTS

### Q1: Should investigate-log be mandatory or optional?
**Recommendation:** **Optional**
- Allows fast iteration when AI is confident
- Can be added incrementally for complex investigations
- Doesn't slow down simple cascades

### Q2: Should goals auto-generate or require explicit creation?
**Recommendation:** **Auto-generate**
- Less manual work for AI
- Ensures goals are created consistently
- Can still manually create with `goals-create` if needed

### Q3: How granular should act-log be?
**Recommendation:** **Per-task granularity**
- Not per-line (too verbose)
- Not per-cascade (loses detail)
- Per-task: Good balance for handoff generation

### Q4: Should we enforce goal completion before postflight?
**Recommendation:** **Warn but allow**
- Don't block postflight if goals incomplete
- Show warning: "⚠️ 2 goals still in progress"
- Allows flexibility for partial completion

---

## 📊 EXPECTED OUTCOMES

After implementation, the workflow will:

1. ✅ Track ALL decisions (not just assessments)
2. ✅ Auto-generate goals from findings
3. ✅ Link goals → cascades → tasks
4. ✅ Generate semantic handoffs with productivity metrics
5. ✅ Store in git notes (portable) + SQLite (queryable)
6. ✅ Enable true session continuity across AIs

**Token efficiency:**
- Handoff reports stay ~500-600 tokens
- Includes goals/tasks but semantic summaries only
- Full detail queryable from database/git notes if needed

---

## 🚀 NEXT SESSION INSTRUCTIONS

To implement this plan in the next session:

1. **Bootstrap Empirica:**
```bash
empirica bootstrap --level 2 --ai-id goal-integration-work
```

2. **Follow checklist phases 1-5 sequentially**
3. **Test after each phase**
4. **Run end-to-end test script**
5. **Create handoff at session end**

**Estimated completion:** 3-4 hours

---

## 📝 FILES TO CREATE/MODIFY

### New Files:
1. `empirica/cli/command_handlers/action_commands.py` - investigate-log & act-log

### Modified Files:
1. `empirica/cli/command_handlers/workflow_commands.py` - CHECK save + goal generation
2. `empirica/core/handoff/auto_generator.py` - Extract goals
3. `empirica/cli/cli_core.py` - Register new commands
4. `empirica/cli/command_handlers/__init__.py` - Export new handlers

**Total changes:** ~500 lines across 5 files

---

## ✅ SUCCESS CRITERIA

The implementation is complete when:

1. ✅ CHECK command saves findings to cascade
2. ✅ investigate-log and act-log commands work
3. ✅ Goals auto-generate from CHECK findings
4. ✅ session-end includes goals/tasks in handoff
5. ✅ End-to-end test script passes
6. ✅ Git notes populated (optional but nice to have)
7. ✅ SQLite queries return expected data

---

**This plan is ready to execute. All details needed are included.**
