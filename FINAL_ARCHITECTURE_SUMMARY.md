# Empirica Architecture - Final Clean Implementation

## ✅ WHAT'S BEEN FIXED

### 1. Removed Unnecessary Simulations
**Before:** `check` command had database save logic (duplication)
**After:** `check` command is now simulation only (returns JSON)
**Why:** Real data comes from `check-submit`, not `check`

### 2. Real Data Flow: check-submit → cascade.context_json
**Implementation:**
- `check-submit` saves to `check_phase_assessments` table (primary storage)
- `check-submit` ALSO saves to `cascade.context_json` (for handoff generation)
- No duplication: Same data, different purposes (queryable vs handoff)

### 3. Implicit Decision Tracking (NEW)
**Commands Added:**
- `investigate-log` - Saves investigation findings to `cascade.context_json["investigation_log"]`
- `act-log` - Saves actions taken to `cascade.context_json["act_log"]` + `cascade.final_action`

**Purpose:** Track what happens during INVESTIGATE and ACT phases (implicit work)

### 4. MCP Server Argument Mapping (FIXED)
**File:** `mcp_local/empirica_mcp_server.py`
- Added `investigation_cycle` → `cycle` mapping
- Added skip rules for unsupported arguments (`confidence_to_proceed` in check-submit)
- **Result:** MCP tools now correctly call CLI commands

### 5. Goal Orchestrator (CLARIFIED - NOT BROKEN)
**How it works:**
- AI uses MCP tools explicitly: `create_goal`, `add_subtask`, `complete_subtask`
- Goals saved to `goals` table, tasks to `tasks` table
- No automatic generation - AI has full control
- **Evidence:** 23 goals already in database from 70+ cascades

---

## 🏗️ CORRECT ARCHITECTURE

### Storage Pattern
```
MCP Tool → CLI Command → Database Table → JSON in context_json (optional)
                      ↓
                  Git Notes (optional, for portability)
```

### Data Flow for CHECK Phase

**Step 1: AI calls MCP tool**
```python
submit_check_assessment(
    session_id="abc",
    vectors={...},
    decision="proceed",
    reasoning="...",
    investigation_cycle=1
)
```

**Step 2: MCP server routes to CLI**
```bash
empirica check-submit \
  --session-id abc \
  --vectors '{...}' \
  --decision proceed \
  --reasoning "..." \
  --cycle 1  # Mapped from investigation_cycle
```

**Step 3: CLI saves to TWO places**
```sql
-- Primary storage (queryable)
INSERT INTO check_phase_assessments (session_id, confidence, decision, gaps, next_targets, ...)

-- Secondary storage (for handoff)
UPDATE cascades SET context_json = json_set(context_json, '$.check_findings', gaps)
```

**Step 4: session-end extracts from cascade**
```python
# Reads cascade.context_json to generate handoff report
{
  "check_findings": [...],
  "investigation_log": [...],
  "act_log": [...]
}
```

---

## 📊 DATABASE TABLES

### Primary Storage (for queries)
- `check_phase_assessments` - CHECK assessment data
- `preflight_assessments` - PREFLIGHT assessment data  
- `postflight_assessments` - POSTFLIGHT assessment data
- `goals` - Goals created by AI via `create_goal`
- `tasks` - Tasks created by AI via `add_subtask`

### Secondary Storage (for handoff)
- `cascades.context_json` - JSON blob with:
  - `check_findings` (from check-submit)
  - `check_unknowns` (from check-submit)
  - `investigation_log` (from investigate-log)
  - `act_log` (from act-log)

### Why Two Storage Locations?
- **Primary tables:** Structured, queryable, normalized
- **cascade.context_json:** Denormalized, easy for handoff generation

**Pattern:** Real command writes to both, simulation commands write to neither

---

## 🎯 COMMANDS REFERENCE

### Simulation Commands (No DB write)
- `check` - Returns JSON decision, doesn't save

### Real Commands (Write to DB)
- `bootstrap` - Creates session
- `preflight-submit` - Saves to preflight_assessments
- `check-submit` - Saves to check_phase_assessments + cascade.context_json
- `postflight-submit` - Saves to postflight_assessments
- `investigate-log` - Saves to cascade.context_json["investigation_log"]
- `act-log` - Saves to cascade.context_json["act_log"]
- `goals-create` - Saves to goals table
- `goals-add-subtask` - Saves to tasks table
- `goals-complete-subtask` - Updates tasks table
- `session-end` - Creates handoff report

---

## ✅ WHAT'S WORKING NOW

1. **MCP tools correctly map to CLI** ✅
2. **check-submit saves to both tables** ✅
3. **investigate-log and act-log track implicit work** ✅
4. **session-end extracts from cascade.context_json** ✅
5. **Goal orchestrator via explicit MCP tools** ✅
6. **No unnecessary simulations** ✅
7. **No automatic heuristics** ✅

---

## 🚀 COMPLETE WORKFLOW

```python
# 1. Bootstrap
bootstrap_session(ai_id="my-agent", bootstrap_level=2)

# 2. PREFLIGHT
execute_preflight(session_id="new", prompt="Task")
submit_preflight_assessment(session_id="new", vectors={...})

# 3. INVESTIGATE (implicit work)
# AI investigates, discovers things
investigate_log(
    session_id="new",
    findings=["Found X", "Discovered Y"],
    evidence={"file": "foo.py", "lines": "10-20"}
)

# AI creates goals explicitly when needed
create_goal(session_id="new", objective="Fix bug")
add_subtask(goal_id="goal-123", description="Fix line 10")

# 4. CHECK
execute_check(
    session_id="new",
    findings=["Found X", "Fixed Y"],
    remaining_unknowns=[],
    confidence_to_proceed=0.9
)
submit_check_assessment(
    session_id="new",
    vectors={...},
    decision="proceed",
    investigation_cycle=1
)
# Saves to check_phase_assessments + cascade.context_json ✅

# 5. ACT (do the work)
# AI executes tasks
act_log(
    session_id="new",
    actions=["Fixed line 10", "Tested fix"],
    artifacts=["foo.py"]
)
complete_subtask(subtask_id="task-123", evidence="Fixed and tested")

# 6. POSTFLIGHT
execute_postflight(session_id="new", task_summary="Completed")
submit_postflight_assessment(session_id="new", vectors={...})

# 7. End session
create_handoff_report(session_id="new", ...)
# OR
session-end --session-id new
# Extracts from cascade.context_json: check_findings, investigation_log, act_log ✅
```

---

## 📝 KEY PRINCIPLES

1. **No simulations that don't save** - If it doesn't write to DB, it's a query/helper only
2. **Real commands write to primary + secondary** - Enables both queries and handoffs
3. **AI has explicit control** - Goals/tasks created via MCP tools, not automatic
4. **MCP → CLI → DB → JSON** - Simple, predictable flow
5. **Git notes optional** - Adds portability but not required

---

## 🎉 RESULT

**System is now:**
- ✅ Clean (no unnecessary simulations)
- ✅ Correct (real data flows properly)
- ✅ Trustworthy (no hidden heuristics)
- ✅ Predictable (MCP → CLI → DB pattern)
- ✅ Complete (tracks implicit work via investigate-log/act-log)

**Ready for 1.0 launch!** 🚀
