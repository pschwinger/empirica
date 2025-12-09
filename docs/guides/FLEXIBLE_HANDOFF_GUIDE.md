# Flexible Epistemic Handoff Guide

**Status:** Implemented ✅  
**Date:** 2025-12-08  
**Version:** 1.0

## Overview

Empirica now supports **three types of epistemic handoffs** to enable flexible multi-agent coordination and workflow patterns.

## Handoff Types

### 1. Investigation Handoff (PREFLIGHT → CHECK)

**Use case:** Specialist handoff after investigation phase

**Workflow:**
```bash
AI-1 (Investigator):
  empirica preflight → investigate → check → handoff-create

AI-2 (Executor):
  empirica handoff-query → act → postflight
```

**Epistemic deltas:** PREFLIGHT → CHECK (learning from investigation)

**Example scenarios:**
- Architecture review → Implementation
- Security audit → Remediation  
- Feasibility study → Execution
- Code exploration → Refactoring

### 2. Complete Handoff (PREFLIGHT → POSTFLIGHT)

**Use case:** Full workflow completion

**Workflow:**
```bash
AI-1:
  empirica preflight → work → postflight → handoff-create

AI-2:
  empirica handoff-query → start new work
```

**Epistemic deltas:** PREFLIGHT → POSTFLIGHT (full cycle learning)

**Example scenarios:**
- Feature implementation complete
- Bug fix verified
- Documentation updated
- Session fully complete

### 3. Planning Handoff (No assessments)

**Use case:** Documentation-only handoff

**Workflow:**
```bash
empirica handoff-create --planning-only --session-id <id> [args]
```

**Epistemic deltas:** None (documentation only)

**Example scenarios:**
- Planning documents
- Design decisions
- Meeting notes
- Context sharing without CASCADE workflow

## CLI Usage

The CLI **auto-detects** handoff type based on available assessments:

```bash
# Auto-detects type based on what exists
empirica handoff-create \
  --session-id <SESSION_ID> \
  --task-summary "What was accomplished" \
  --key-findings '["Finding 1", "Finding 2"]' \
  --remaining-unknowns '["Unknown 1"]' \
  --next-session-context "Context for next AI" \
  --output json
```

**Detection logic:**
1. If `--planning-only` flag → Planning handoff
2. If PREFLIGHT + POSTFLIGHT exist → Complete handoff
3. If PREFLIGHT + CHECK exist → Investigation handoff
4. Otherwise → Error (need at least PREFLIGHT + CHECK or --planning-only)

## Output Format

All handoff types return:

```json
{
  "ok": true,
  "session_id": "...",
  "handoff_type": "investigation|complete|planning",
  "handoff_subtype": "investigation|complete|planning",
  "epistemic_deltas": { /* PREFLIGHT→CHECK or PREFLIGHT→POSTFLIGHT */ },
  "epistemic_note": "PREFLIGHT → CHECK deltas (investigation phase)",
  "calibration_status": "well_calibrated|moderate|poor",
  "has_epistemic_deltas": true|false
}
```

## Multi-Agent Coordination Patterns

### Pattern 1: Parallel Investigation → Merge

```bash
# AI-1: Domain A investigation
AI1_SESSION=$(empirica session-create --ai-id investigator-1 --output json | jq -r .session_id)
empirica preflight --session-id $AI1_SESSION
# ... investigate domain A ...
empirica check --session-id $AI1_SESSION
empirica handoff-create --session-id $AI1_SESSION  # Investigation handoff

# AI-2: Domain B investigation  
AI2_SESSION=$(empirica session-create --ai-id investigator-2 --output json | jq -r .session_id)
empirica preflight --session-id $AI2_SESSION
# ... investigate domain B ...
empirica check --session-id $AI2_SESSION
empirica handoff-create --session-id $AI2_SESSION  # Investigation handoff

# AI-3: Merge and execute
empirica handoff-query --session-id $AI1_SESSION  # Get findings from AI-1
empirica handoff-query --session-id $AI2_SESSION  # Get findings from AI-2
# ... execute based on combined findings ...
```

### Pattern 2: Investigation → Execution Split

```bash
# Investigation specialist
INVEST_SESSION=$(empirica session-create --ai-id investigator --output json | jq -r .session_id)
empirica preflight --session-id $INVEST_SESSION
# ... thorough investigation ...
empirica check --session-id $INVEST_SESSION --confidence 0.75
empirica handoff-create --session-id $INVEST_SESSION  # Investigation handoff

# Execution specialist
EXEC_SESSION=$(empirica session-create --ai-id executor --output json | jq -r .session_id)
empirica handoff-query --session-id $INVEST_SESSION  # Get findings/unknowns
# ... implement based on investigation ...
empirica postflight --session-id $EXEC_SESSION
```

## Benefits

### ✅ Multi-Agent Coordination
- Investigation specialists can hand off to execution specialists
- Clear separation of concerns (research vs implementation)
- Epistemic state preserved across specialists

### ✅ Parallel Work
- Multiple AIs can investigate different domains
- Findings/unknowns tracked separately
- Merge results without duplication

### ✅ Real Workflow Patterns
- Architecture reviews that lead to implementation
- Security audits that trigger remediation
- Feasibility studies that inform execution
- Long-running investigations with handoffs

### ✅ CHECK Already Captures State
- CHECK tracks uncertainty reduction through investigation
- Findings/unknowns explicitly recorded
- Decision point for proceed vs investigate more

## Querying Handoffs

Query any handoff type the same way:

```bash
# Query by session
empirica handoff-query --session-id <SESSION_ID> --output json

# Query by AI (all handoffs from that AI)
empirica handoff-query --ai-id <AI_ID> --limit 5 --output json
```

**Returns:**
- `handoff_subtype`: "investigation" | "complete" | "planning"
- `epistemic_deltas`: Learning from investigation or full cycle
- `key_findings`: Validated knowledge
- `remaining_unknowns`: Investigation breadcrumbs
- `next_session_context`: Critical context for next AI

## Implementation Details

### Code Changes
- `empirica/cli/command_handlers/handoff_commands.py`: Added handoff type detection
- `empirica/core/handoff/report_generator.py`: Support flexible start/end assessments
- `empirica/data/session_database.py`: Uses existing `get_check_phase_assessments()`

### Storage
All handoff types stored identically:
- Git notes: `refs/notes/empirica/handoff/{session_id}`
- Database: `handoff_reports` table (if exists)
- Token efficient: ~200-600 tokens (98.8% reduction)

## Examples

See test results in commit `f61289eb`:
- Complete handoff test: Session `fe10d107-5d60-4615-8b5d-01c6dba4aa97`
- Investigation handoff test: Session `79056dbf-ede3-4c94-9fdd-70071a9e10b2`

Both tests passing ✅

---

## Using Goals & Subtasks for Epistemic Continuity

**New in v4.0:** Goals and subtasks now track `findings`, `unknowns`, and `dead_ends` for complete epistemic handoff support.

### Why Use Goals/Subtasks with Handoffs?

**Problem:** Handoffs need concrete findings/unknowns, but where do they come from?

**Solution:** Goals/subtasks are the **source of truth** for investigation discoveries.

### Complete Workflow Example

#### Step 1: Investigation Specialist Creates Goal

```bash
# PREFLIGHT assessment shows high uncertainty
empirica preflight "Investigate OAuth2 implementation patterns" --prompt-only
empirica preflight-submit --session-id <ID> --vectors '{"uncertainty": 0.7, ...}' --reasoning "..."

# High uncertainty (>0.6) triggers goal creation
empirica goals-create \
  --session-id <SESSION_ID> \
  --objective "Map OAuth2 implementation patterns in codebase" \
  --scope-breadth 0.7 \
  --scope-duration 0.4 \
  --success-criteria '["All endpoints documented", "Token flow validated", "Security audit complete"]'

# Returns: goal_id
```

#### Step 2: Create Subtasks for Investigation

```bash
# Break investigation into focused subtasks
empirica goals-add-subtask \
  --goal-id <GOAL_ID> \
  --description "Map all OAuth2 API endpoints" \
  --importance critical

empirica goals-add-subtask \
  --goal-id <GOAL_ID> \
  --description "Trace token generation and validation flow" \
  --importance high

empirica goals-add-subtask \
  --goal-id <GOAL_ID> \
  --description "Identify security vulnerabilities" \
  --importance critical
```

#### Step 3: Log Findings/Unknowns During Investigation

```python
from empirica.data.session_database import SessionDatabase

db = SessionDatabase()

# As you investigate, log discoveries incrementally
subtask_id = "..."  # From goals-add-subtask

# Log validated findings
db.update_subtask_findings(subtask_id, [
    "Authorization endpoint: /oauth/authorize",
    "Token endpoint: /oauth/token", 
    "Token TTL: 3600 seconds (1 hour)",
    "Refresh tokens enabled with 30-day expiration"
])

# Log remaining unknowns
db.update_subtask_unknowns(subtask_id, [
    "Token rotation policy unclear - need to check Redis cache",
    "Rate limiting configuration not documented",
    "PKCE flow support unknown"
])

# Log dead ends (failed approaches - saves future effort)
db.update_subtask_dead_ends(subtask_id, [
    "Tried /oauth/v1 endpoints - deprecated, use /oauth/v2",
    "OAuth 1.0a signatures not used, only OAuth 2.0 bearer tokens"
])

db.close()
```

**Why this matters:** Findings/unknowns are **persistent** and **queryable** for handoffs.

#### Step 4: CHECK Phase Decision Using Goals Data

```bash
# Query all unknowns across all subtasks for this session
empirica goals-get-subtasks --goal-id <GOAL_ID> --output json > subtasks.json

# Extract findings and unknowns
FINDINGS=$(jq -r '.subtasks[].findings[]' subtasks.json | jq -R . | jq -s .)
UNKNOWNS=$(jq -r '.subtasks[].unknowns[]' subtasks.json | jq -R . | jq -s .)

# Run CHECK assessment
empirica check \
  --session-id <SESSION_ID> \
  --findings "$FINDINGS" \
  --unknowns "$UNKNOWNS" \
  --confidence 0.82

# Submit CHECK assessment
empirica check-submit \
  --session-id <SESSION_ID> \
  --vectors '{"know": 0.85, "uncertainty": 0.20, ...}' \
  --decision proceed \
  --reasoning "Sufficient findings to proceed, minor unknowns acceptable"
```

**Key insight:** `goals-get-subtasks` aggregates all findings/unknowns from investigation.

#### Step 5: Create Investigation Handoff

```bash
# Handoff automatically uses findings/unknowns from CHECK assessment
empirica handoff-create \
  --session-id <SESSION_ID> \
  --task-summary "Mapped OAuth2 implementation - 15 endpoints documented, token flow validated" \
  --key-findings "$FINDINGS" \
  --remaining-unknowns "$UNKNOWNS" \
  --next-session-context "Ready for security remediation. Focus on unknowns: rate limiting config, PKCE support" \
  --output json
```

**Result:** Investigation handoff with complete epistemic context.

#### Step 6: Execution Specialist Resumes Work

```bash
# New AI queries handoff
empirica handoff-query --session-id <SESSION_ID> --output json

# Returns:
{
  "handoff_subtype": "investigation",
  "key_findings": [
    "Authorization endpoint: /oauth/authorize",
    "Token endpoint: /oauth/token",
    "Token TTL: 3600 seconds",
    "Refresh tokens enabled with 30-day expiration"
  ],
  "remaining_unknowns": [
    "Token rotation policy unclear - need to check Redis cache",
    "Rate limiting configuration not documented", 
    "PKCE flow support unknown"
  ],
  "epistemic_deltas": {
    "know": 0.25,
    "uncertainty": -0.50
  },
  "next_session_context": "Ready for security remediation. Focus on unknowns..."
}

# Execution specialist also gets subtask details
empirica goals-get-subtasks --goal-id <GOAL_ID> --output json

# Returns full context:
{
  "subtasks": [{
    "task_id": "...",
    "description": "Map all OAuth2 API endpoints",
    "status": "completed",
    "findings": ["Authorization endpoint: /oauth/authorize", ...],
    "unknowns": ["Token rotation policy unclear", ...],
    "dead_ends": ["Tried /oauth/v1 endpoints - deprecated", ...]
  }]
}
```

**Execution specialist now has:**
- ✅ Complete findings from investigation
- ✅ Specific unknowns to address
- ✅ Dead ends to avoid
- ✅ Epistemic deltas showing learning
- ✅ Context for decision-making

### Programmatic Access (Python)

```python
from empirica.data.session_database import SessionDatabase

db = SessionDatabase()

# Get all unknowns for session (for CHECK decisions)
unknowns = db.query_unknowns_summary(session_id)
# Returns: ["Token rotation unclear", "Rate limiting unknown", ...]

# Use in CHECK phase
db.log_check_phase_assessment(
    session_id=session_id,
    vectors={...},
    decision='proceed',
    findings=all_findings,
    unknowns=unknowns,  # From query_unknowns_summary
    confidence_to_proceed=0.85
)

# Create handoff programmatically
from empirica.core.handoff.report_generator import EpistemicHandoffReportGenerator

generator = EpistemicHandoffReportGenerator()
report = generator.generate_handoff_report(
    session_id=session_id,
    task_summary="...",
    key_findings=all_findings,
    remaining_unknowns=unknowns,
    next_session_context="..."
)

db.close()
```

### Benefits of Goals/Subtasks + Handoffs

| Without Goals/Subtasks | With Goals/Subtasks |
|------------------------|---------------------|
| ❌ Findings lost between sessions | ✅ Findings persistent in database |
| ❌ Unknowns forgotten | ✅ Unknowns tracked per subtask |
| ❌ Dead ends repeated | ✅ Dead ends documented |
| ❌ Manual tracking in notes | ✅ Structured queryable data |
| ❌ Context reconstruction required | ✅ Context preserved automatically |
| ❌ Handoffs are vague | ✅ Handoffs have concrete data |

### Multi-AI Workflow Pattern

```
Investigation Specialist (AI-1):
  1. PREFLIGHT → High uncertainty (0.7)
  2. Create goal with subtasks
  3. Investigate → Log findings/unknowns per subtask
  4. CHECK → Aggregate findings/unknowns from goals-get-subtasks
  5. Create investigation handoff

↓ Epistemic Handoff (via git notes)

Execution Specialist (AI-2):
  1. Query handoff → Get findings/unknowns
  2. Query goals-get-subtasks → Get detailed context
  3. Create execution goal based on unknowns
  4. Work → Log new findings
  5. POSTFLIGHT → Measure completion
```

### Key Commands Summary

```bash
# Investigation phase
goals-create                     # Create investigation goal
goals-add-subtask                # Break down investigation
goals-get-subtasks               # Query findings/unknowns (NEW: includes epistemic data!)
check                            # Decision gate using unknowns
handoff-create                   # Preserve context

# Execution phase  
handoff-query                    # Retrieve investigation context
goals-get-subtasks               # Get detailed findings/unknowns/dead_ends
goals-create                     # Create execution goal
goals-complete-subtask           # Mark work complete
```

### Technical Details

**SubTask Schema (v4.0):**
```python
@dataclass
class SubTask:
    # ... existing fields ...
    findings: List[str]    # Validated discoveries
    unknowns: List[str]    # Remaining questions
    dead_ends: List[str]   # Failed approaches
```

**Storage:** All three fields stored in `subtask_data` JSON column in database.

**Serialization:** Fully supported in `to_dict()`, `from_dict()`, and `goals-get-subtasks` output.

**Query optimization:** `query_unknowns_summary(session_id)` aggregates unknowns across all subtasks efficiently.

---

## Best Practices

### 1. Log Findings Incrementally

**❌ Don't wait until end:**
```python
# Bad - all context lost if interrupted
# ... investigate for 2 hours ...
db.update_subtask_findings(task_id, ["Finding 1", "Finding 2", ...])
```

**✅ Log as you discover:**
```python
# Good - preserves progress
db.update_subtask_findings(task_id, ["Found /oauth/authorize"])
# ... continue investigation ...
db.update_subtask_findings(task_id, ["Token TTL: 3600s"])
# ... continue investigation ...
db.update_subtask_findings(task_id, ["Refresh tokens: 30 days"])
```

### 2. Be Specific with Unknowns

**❌ Vague:**
```python
unknowns = ["Need more research", "Unclear how it works"]
```

**✅ Actionable:**
```python
unknowns = [
    "Token rotation policy - check Redis cache implementation",
    "Rate limiting - need to find nginx config or middleware",
    "PKCE flow support - verify client library version"
]
```

### 3. Document Dead Ends

**Why:** Saves future AI from repeating failed approaches.

```python
dead_ends = [
    "Tried /api/v1/oauth endpoints - all return 404, use /oauth/v2",
    "Attempted to find config in .env - not there, check database",
    "OAuth 1.0a docs misleading - system only uses OAuth 2.0"
]
```

### 4. Use CHECK for Decision Quality

**Pattern:** CHECK phase aggregates unknowns to decide if ready to proceed.

```bash
# Get current unknowns
unknowns=$(empirica goals-get-subtasks --goal-id <ID> --output json | jq -r '.subtasks[].unknowns[]')

# If unknowns are critical → investigate more
# If unknowns are minor → proceed

empirica check --session-id <ID> \
  --unknowns "$unknowns" \
  --confidence 0.85  # High confidence = ready to proceed
```

---

## Troubleshooting

### Issue: goals-get-subtasks returns empty findings

**Cause:** Using older SubTask objects without new fields.

**Solution:** Update `empirica/core/tasks/types.py` to v4.0 schema (includes findings/unknowns/dead_ends).

### Issue: Handoff missing findings/unknowns

**Cause:** CHECK assessment not run, or didn't include findings/unknowns.

**Solution:** Always run CHECK before investigation handoff:
```bash
empirica check --session-id <ID> --findings '[...]' --unknowns '[...]' --confidence 0.8
```

### Issue: query_unknowns_summary returns empty

**Cause:** Unknowns not logged via `update_subtask_unknowns()`.

**Solution:** Log unknowns incrementally during investigation:
```python
db.update_subtask_unknowns(subtask_id, ["Unknown 1", "Unknown 2"])
```

---

## Related Documentation

- `docs/guides/GOAL_TREE_USAGE_GUIDE.md` - Goals/subtasks system overview
- `docs/production/06_CASCADE_FLOW.md` - CHECK phase details
- `docs/production/23_SESSION_CONTINUITY.md` - Session resumption patterns
- `docs/reference/CLI_COMMANDS_COMPLETE.md` - All CLI commands

---

**Last Updated:** 2025-12-08  
**Version:** 1.0 (Goals/subtasks epistemic continuity)
