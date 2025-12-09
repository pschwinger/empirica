# Epistemic Continuity Issues Found

**Date:** 2025-12-08  
**Context:** Review of recent goals/subtasks and CHECK phase handoff changes  
**Status:** Issues identified, fixes recommended

---

## Summary

Recent commits (f61289eb, 496e304c) added:
1. ✅ Flexible handoff system (PREFLIGHT→CHECK or PREFLIGHT→POSTFLIGHT)
2. ✅ `goals-get-subtasks` command to retrieve subtask details
3. ✅ `update_subtask_findings/unknowns/dead_ends` methods in SessionDatabase

**However:** Critical fields are missing from the SubTask dataclass, breaking epistemic continuity.

---

## Issue 1: SubTask Missing Epistemic Fields (CRITICAL)

### Problem

The `SubTask` dataclass in `empirica/core/tasks/types.py` does NOT include:
- `findings: List[str]` - Validated discoveries during investigation
- `unknowns: List[str]` - Remaining questions/unknowns
- `dead_ends: List[str]` - Attempted approaches that didn't work

### Evidence

**Current SubTask definition:**
```python
@dataclass
class SubTask:
    id: str
    goal_id: str
    description: str
    status: TaskStatus
    epistemic_importance: EpistemicImportance
    dependencies: List[str] = field(default_factory=list)
    estimated_tokens: Optional[int] = None
    actual_tokens: Optional[int] = None
    completion_evidence: Optional[str] = None
    notes: str = ""
    created_timestamp: float = field(default_factory=time.time)
    completed_timestamp: Optional[float] = None
    # ❌ Missing: findings, unknowns, dead_ends
```

**But SessionDatabase stores them:**
```python
def update_subtask_findings(self, subtask_id: str, findings: List[str]):
    subtask_data['findings'] = findings  # ✅ Stored in DB
    
def update_subtask_unknowns(self, subtask_id: str, unknowns: List[str]):
    subtask_data['unknowns'] = unknowns  # ✅ Stored in DB
    
def update_subtask_dead_ends(self, subtask_id: str, dead_ends: List[str]):
    subtask_data['dead_ends'] = dead_ends  # ✅ Stored in DB
```

**And goals-get-subtasks doesn't retrieve them:**
```python
def handle_goals_get_subtasks_command(args):
    subtasks_dict.append({
        "task_id": task.id,
        "description": task.description,
        "status": task.status.value,
        # ... other fields ...
        "metadata": task.metadata  # ❌ But findings/unknowns not in metadata
    })
```

### Impact

**Broken epistemic continuity:**
1. AI investigates, logs findings via `update_subtask_findings()`
2. Findings stored in database JSON: `subtask_data['findings'] = [...]`
3. AI resumes session, runs `goals-get-subtasks`
4. **Findings are lost** - not loaded into SubTask object
5. AI has no context of prior discoveries

**Real-world scenario:**
```bash
# Session 1: Investigation
empirica goals-add-subtask --goal-id <ID> --description "Map OAuth2 endpoints"
# AI investigates...
db.update_subtask_findings(subtask_id, ["Found /oauth/authorize", "Token TTL is 3600s"])
db.update_subtask_unknowns(subtask_id, ["Refresh token rotation unclear"])

# Session 2: Resume work
empirica goals-get-subtasks --goal-id <ID>
# Returns:
{
  "subtasks": [{
    "task_id": "...",
    "description": "Map OAuth2 endpoints",
    "status": "in_progress"
    # ❌ NO FINDINGS
    # ❌ NO UNKNOWNS
  }]
}
```

AI cannot see what was already discovered!

---

## Issue 2: goals-get-subtasks Doesn't Expose Findings/Unknowns

### Problem

Even if we fix the SubTask dataclass, `goals-get-subtasks` command doesn't include findings/unknowns in output.

### Current Implementation

```python
subtasks_dict.append({
    "task_id": task.id,
    "description": task.description,
    "status": task.status.value,
    "created_at": task.created_timestamp,
    "completed_at": task.completed_timestamp,
    "dependencies": task.dependencies,
    "metadata": task.metadata  # Generic metadata, not findings/unknowns
})
```

### Needed Implementation

```python
subtasks_dict.append({
    "task_id": task.id,
    "description": task.description,
    "status": task.status.value,
    "created_at": task.created_timestamp,
    "completed_at": task.completed_timestamp,
    "dependencies": task.dependencies,
    "findings": task.findings,  # ✅ Explicit
    "unknowns": task.unknowns,  # ✅ Explicit
    "dead_ends": task.dead_ends,  # ✅ Explicit
    "completion_evidence": task.completion_evidence,
    "notes": task.notes
})
```

---

## Issue 3: SubTask.from_dict Doesn't Load Findings/Unknowns

### Problem

When loading SubTask from database, `from_dict()` doesn't extract findings/unknowns from JSON.

### Current Implementation

```python
@staticmethod
def from_dict(data: Dict[str, Any]) -> 'SubTask':
    return SubTask(
        id=data['id'],
        goal_id=data['goal_id'],
        description=data['description'],
        status=TaskStatus(data['status']),
        epistemic_importance=EpistemicImportance(data['epistemic_importance']),
        dependencies=data.get('dependencies', []),
        # ... other fields ...
        # ❌ Missing: findings, unknowns, dead_ends
    )
```

### Needed Implementation

```python
@staticmethod
def from_dict(data: Dict[str, Any]) -> 'SubTask':
    return SubTask(
        # ... existing fields ...
        findings=data.get('findings', []),  # ✅ Load from JSON
        unknowns=data.get('unknowns', []),  # ✅ Load from JSON
        dead_ends=data.get('dead_ends', [])  # ✅ Load from JSON
    )
```

---

## Issue 4: SubTask.to_dict Doesn't Save Findings/Unknowns

### Problem

When serializing SubTask to JSON, `to_dict()` doesn't include findings/unknowns.

### Current Implementation

```python
def to_dict(self) -> Dict[str, Any]:
    return {
        'id': self.id,
        'goal_id': self.goal_id,
        'description': self.description,
        # ... other fields ...
        # ❌ Missing: findings, unknowns, dead_ends
    }
```

### Needed Implementation

```python
def to_dict(self) -> Dict[str, Any]:
    return {
        # ... existing fields ...
        'findings': self.findings,  # ✅ Serialize
        'unknowns': self.unknowns,  # ✅ Serialize
        'dead_ends': self.dead_ends  # ✅ Serialize
    }
```

---

## Issue 5: Documentation Gap - FLEXIBLE_HANDOFF_GUIDE.md

### Problem

The guide shows examples but doesn't explain:
1. How to retrieve findings/unknowns for CHECK handoffs
2. That findings/unknowns are **critical** for investigation handoffs
3. How to use `goals-get-subtasks` for session resumption

### What's Missing

**Example showing epistemic continuity:**
```python
# Investigation specialist (Session 1)
db.update_subtask_findings(subtask_id, ["Found X", "Validated Y"])
db.update_subtask_unknowns(subtask_id, ["Z still unclear"])

# Create investigation handoff
empirica handoff-create --session-id <ID> \
  --key-findings "$(empirica goals-get-subtasks --goal-id <GOAL_ID> --output json | jq -r '.subtasks[].findings[]')" \
  --remaining-unknowns "$(empirica goals-get-subtasks --goal-id <GOAL_ID> --output json | jq -r '.subtasks[].unknowns[]')"

# Execution specialist (Session 2)
empirica handoff-query --session-id <ID>
# Gets findings/unknowns from handoff
```

**Current guide is good but needs this practical workflow.**

---

## Recommended Fixes

### Fix 1: Add Fields to SubTask Dataclass (CRITICAL)

**File:** `empirica/core/tasks/types.py`

```python
@dataclass
class SubTask:
    # ... existing fields ...
    
    # Epistemic investigation tracking
    findings: List[str] = field(default_factory=list)  # Validated discoveries
    unknowns: List[str] = field(default_factory=list)  # Remaining questions
    dead_ends: List[str] = field(default_factory=list)  # Failed approaches
```

### Fix 2: Update from_dict() Method

```python
@staticmethod
def from_dict(data: Dict[str, Any]) -> 'SubTask':
    return SubTask(
        # ... existing fields ...
        findings=data.get('findings', []),
        unknowns=data.get('unknowns', []),
        dead_ends=data.get('dead_ends', [])
    )
```

### Fix 3: Update to_dict() Method

```python
def to_dict(self) -> Dict[str, Any]:
    return {
        # ... existing fields ...
        'findings': self.findings,
        'unknowns': self.unknowns,
        'dead_ends': self.dead_ends
    }
```

### Fix 4: Update goals-get-subtasks Command

**File:** `empirica/cli/command_handlers/goal_commands.py`

```python
def handle_goals_get_subtasks_command(args):
    # ... existing code ...
    
    subtasks_dict.append({
        "task_id": task.id,
        "description": task.description,
        "status": task.status.value,
        "created_at": task.created_timestamp,
        "completed_at": task.completed_timestamp,
        "dependencies": task.dependencies,
        "findings": task.findings if hasattr(task, 'findings') else [],  # ✅ Add
        "unknowns": task.unknowns if hasattr(task, 'unknowns') else [],  # ✅ Add
        "dead_ends": task.dead_ends if hasattr(task, 'dead_ends') else [],  # ✅ Add
        "completion_evidence": task.completion_evidence,
        "notes": task.notes
    })
```

### Fix 5: Update FLEXIBLE_HANDOFF_GUIDE.md

Add section showing:
1. How to use `goals-get-subtasks` to gather findings/unknowns
2. How to pass them to `handoff-create`
3. Complete workflow example with investigation → execution handoff

---

## Testing Recommendations

### Test 1: Round-trip Findings/Unknowns

```python
# Create subtask
subtask_id = db.create_subtask(goal_id, "Test task", 'high')

# Add findings/unknowns
db.update_subtask_findings(subtask_id, ["Finding 1", "Finding 2"])
db.update_subtask_unknowns(subtask_id, ["Unknown 1"])

# Retrieve via goals-get-subtasks
result = handle_goals_get_subtasks_command(args)

# Verify findings/unknowns present
assert "Finding 1" in result['subtasks'][0]['findings']
assert "Unknown 1" in result['subtasks'][0]['unknowns']
```

### Test 2: CHECK Phase Handoff with Findings

```python
# Create goal + subtasks with findings
goal_id = db.create_goal(session_id, "Investigate X", 0.6, 0.4)
subtask_id = db.create_subtask(goal_id, "Map API", 'high')
db.update_subtask_findings(subtask_id, ["Found endpoint /api/v1"])
db.update_subtask_unknowns(subtask_id, ["Rate limiting unclear"])

# Run CHECK assessment
empirica check --session-id <ID> \
  --findings '[...]' \
  --unknowns '[...]' \
  --confidence 0.75

# Create investigation handoff
empirica handoff-create --session-id <ID> \
  --task-summary "Mapped API endpoints" \
  --key-findings '[...]' \
  --remaining-unknowns '[...]'

# Verify handoff includes findings/unknowns
handoff = empirica handoff-query --session-id <ID>
assert "Found endpoint" in handoff['key_findings']
assert "Rate limiting unclear" in handoff['remaining_unknowns']
```

### Test 3: Session Resumption

```python
# Session 1: Investigation
session1_id = create_session()
goal_id = db.create_goal(session1_id, "Investigate OAuth2", 0.7, 0.5)
subtask_id = db.create_subtask(goal_id, "Map endpoints", 'critical')
db.update_subtask_findings(subtask_id, ["Endpoint: /oauth/authorize"])
db.update_subtask_unknowns(subtask_id, ["Token expiry unclear"])

# Session 2: Resume
empirica handoff-query --session-id session1_id
empirica goals-get-subtasks --goal-id goal_id

# Verify findings/unknowns available for new AI
subtasks = handle_goals_get_subtasks_command(args)
assert "Endpoint: /oauth/authorize" in subtasks['subtasks'][0]['findings']
```

---

## Priority Assessment

| Issue | Severity | Impact | Priority |
|-------|----------|--------|----------|
| SubTask missing fields | **CRITICAL** | Breaks epistemic continuity | **P0** |
| from_dict not loading | **HIGH** | Data loss on retrieval | **P0** |
| to_dict not saving | **HIGH** | Data loss on serialization | **P0** |
| goals-get-subtasks output | **HIGH** | CLI users can't access data | **P1** |
| Documentation gap | **MEDIUM** | Users don't know how to use feature | **P2** |

---

## Benefits After Fixes

**For Single AI:**
- Resume work with full context of prior discoveries
- See findings/unknowns when reviewing goals
- Make informed CHECK decisions based on accumulated knowledge

**For Multi-AI Workflows:**
- Investigation specialist logs findings
- Investigation handoff (PREFLIGHT→CHECK) preserves findings
- Execution specialist receives findings via handoff
- No context loss between specialists

**For Epistemic Continuity:**
- Complete audit trail of discoveries
- Clear separation: findings (validated) vs unknowns (breadcrumbs)
- Dead ends tracked to avoid repeated mistakes

---

## Next Steps

1. **Implement Fix 1-3** (SubTask dataclass changes) - 15 minutes
2. **Implement Fix 4** (goals-get-subtasks output) - 10 minutes
3. **Test round-trip** - 10 minutes
4. **Update FLEXIBLE_HANDOFF_GUIDE.md** - 30 minutes
5. **Test multi-AI handoff workflow** - 20 minutes

**Total estimated time:** 1.5 hours

---

## Related Files

- `empirica/core/tasks/types.py` - SubTask dataclass
- `empirica/cli/command_handlers/goal_commands.py` - goals-get-subtasks command
- `empirica/data/session_database.py` - update_subtask_findings/unknowns/dead_ends
- `docs/guides/FLEXIBLE_HANDOFF_GUIDE.md` - Usage documentation
- `docs/guides/GOAL_TREE_USAGE_GUIDE.md` - May need update too

---

**Status:** Analysis complete, ready for implementation  
**Confidence:** High (0.9) - Clear cause and clear solution  
**Impact:** Critical for epistemic continuity
