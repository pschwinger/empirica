# Git Notes Expansion for Goal Tracking

**Status:** Design proposal (Phase 2 enhancement)  
**Current State:** Phase 1 implemented (commit message parsing)  
**Depends On:** Goal Architecture MVP (implemented)  
**Priority:** MEDIUM (post-Empirica release)

---

## Current Git Integration (Already Exists) ✅

### What We Have Today
Empirica already uses git notes for **epistemic checkpoint storage**:

**Namespace:**
```
refs/notes/empirica/session/<session_id>/
```

**What's Stored:**
- PREFLIGHT vectors (know, do, uncertainty, etc.)
- CHECK phase assessments
- POSTFLIGHT learning deltas
- Compressed checkpoints (~450 tokens instead of ~6,500)

**Benefits:**
- 80-90% token reduction for session continuity
- Git history tracks epistemic trajectory
- Multi-agent sessions don't collide (session-specific refs)

**Implementation:**
- `empirica/core/canonical/git_enhanced_reflex_logger.py`
- Already production-ready ✅

---

## Proposed Expansion (Phase 2) - Goal Task Tracking

### What We're Adding

**New Namespace:**
```
refs/notes/
  └── empirica/
      ├── session/<session_id>/     # EXISTING: epistemic checkpoints
      └── tasks/                     # NEW: task completion records
          ├── <goal_id_1>/
          ├── <goal_id_2>/
          └── <goal_id_3>/
```

### Why Expand?

**User's Insight:** "Lead devs (AI-based) can see what the goals are of agents and track their progress simply via git."

**This creates unified audit trail:**
1. **Goals** (what AI intends) → Database
2. **Commits** (what AI did) → Git log
3. **Task metadata** (completion evidence) → Git notes (NEW)
4. **Epistemic state** (what AI learned) → Git notes (EXISTING)

---

## What Phase 2 Adds

### 1. Task Completion Notes

**When subtask is marked complete:**
```python
# In completion/tracker.py
def record_subtask_completion(self, subtask_id: str, evidence: str):
    # ... existing database update ...
    
    # NEW: Add git note
    if self.git_available:
        self._add_task_note(subtask_id, evidence)
```

**Git note structure:**
```json
{
  "subtask_id": "abc-123-def",
  "goal_id": "goal-xyz-789",
  "description": "Implement input validation",
  "epistemic_importance": "critical",
  "completed_timestamp": 1705334400.0,
  "completion_evidence": "commit:abc1234",
  "actual_tokens": 850
}
```

**Attached to:** The commit that completed the task

### 2. Lead AI Query Interface

**New functionality:**
```python
def get_team_progress_from_git(goal_id: str) -> Dict[str, Any]:
    """
    Lead AI can query git to see team progress on a goal
    
    Returns timeline of commits mapped to subtasks
    """
    # Read git notes from refs/notes/empirica/tasks/<goal_id>
    commits = subprocess.run([
        'git', 'log', '--format=%H %s', 
        f'--notes=empirica/tasks/{goal_id}'
    ], ...)
    
    return {
        'goal_id': goal_id,
        'commits': [...],
        'completed_subtasks': [...],
        'timeline': [...]
    }
```

### 3. Unified Timeline View

**Query combining epistemic + task data:**
```python
def get_agent_journey(session_id: str, goal_id: str):
    """
    Show complete agent journey: goals → actions → learning
    """
    return {
        'goal': goal_repo.get_goal(goal_id),
        'git_timeline': [
            {
                'commit': 'abc123',
                'timestamp': '2024-01-15 10:30',
                'task_completed': 'Input validation',  # From task notes
                'epistemic_state': {                    # From session notes
                    'know': 0.85,
                    'uncertainty': 0.25
                },
                'files_changed': ['validation.py']
            },
            # ...
        ]
    }
```

---

## Comparison: Phase 1 vs Phase 2

### Phase 1 (IMPLEMENTED) ✅
**Commit Message Parsing:**
```bash
git commit -m "✅ [TASK:abc-123] Implement validation"
```

**Pros:**
- ✅ Simple (80 lines of code)
- ✅ Non-invasive (optional convention)
- ✅ Works today with no git changes
- ✅ Auto-completes tasks from commits

**Cons:**
- ❌ No structured metadata
- ❌ Can't query by goal efficiently
- ❌ No epistemic state linkage

### Phase 2 (PROPOSED) 🔄
**Git Notes Integration:**
```bash
git notes --ref=empirica/tasks/<goal_id> show abc123
# Returns structured JSON with task metadata
```

**Pros:**
- ✅ Structured metadata in git
- ✅ Efficient queries by goal
- ✅ Links tasks + commits + epistemic state
- ✅ Lead AI can see team timeline

**Cons:**
- ❌ More complex (~500 lines of code)
- ❌ Requires git notes support
- ❌ Need to handle concurrent writes

---

## Implementation Plan (Phase 2)

### Step 1: Extend CompletionTracker
**File:** `empirica/core/completion/tracker.py`

```python
def _add_task_note(self, subtask_id: str, commit_hash: str):
    """Add task completion note to git"""
    subtask = self.task_repo.get_subtask(subtask_id)
    
    note_data = {
        'subtask_id': subtask.id,
        'goal_id': subtask.goal_id,
        'description': subtask.description,
        'epistemic_importance': subtask.epistemic_importance.value,
        'completed_timestamp': time.time(),
        'completion_evidence': commit_hash,
        'actual_tokens': subtask.actual_tokens
    }
    
    # Use goal-specific namespace
    note_ref = f"empirica/tasks/{subtask.goal_id}"
    subprocess.run([
        'git', 'notes', '--ref', note_ref, 
        'add', '-m', json.dumps(note_data), commit_hash
    ])
```

### Step 2: Add Query Interface
**File:** `empirica/core/completion/git_query.py` (NEW)

```python
class GitProgressQuery:
    """Query git notes for team progress tracking"""
    
    def get_goal_timeline(self, goal_id: str):
        """Get commit timeline for goal with task metadata"""
        pass
    
    def get_team_progress(self, goal_ids: List[str]):
        """Multi-goal progress for team coordination"""
        pass
    
    def get_unified_timeline(self, session_id: str, goal_id: str):
        """Combine epistemic + task data"""
        pass
```

### Step 3: Add MCP Tool
**Tool:** `query_git_progress`

```python
elif name == "query_git_progress":
    from empirica.core.completion.git_query import GitProgressQuery
    
    goal_id = arguments.get("goal_id")
    
    query = GitProgressQuery()
    timeline = query.get_goal_timeline(goal_id)
    
    return [types.TextContent(type="text", text=json.dumps(timeline))]
```

---

## Why This Matters for Multi-Agent Teams

### Use Case: Lead AI Coordinating 3 Junior AIs

**Without Phase 2:**
```python
# Lead AI has to query database for each agent
agent1_progress = db.query_progress(agent1_session)
agent2_progress = db.query_progress(agent2_session)
agent3_progress = db.query_progress(agent3_session)
# Can't see git history, just database state
```

**With Phase 2:**
```python
# Lead AI queries git (single source of truth)
team_status = git_query.get_team_progress([goal1, goal2, goal3])
# Sees: commits, tasks, epistemic state, all in one timeline
# Can identify stuck agents, blockers, dependencies
```

**Lead AI can see:**
- Agent 2 hasn't committed in 3 hours → Might be stuck
- Agent 2's last epistemic state: UNCERTAINTY=0.85 → Needs help
- Agent 1 completed dependency → Agent 3 can now proceed

---

## Compatibility with Existing System

### No Breaking Changes
- Phase 1 (commit parsing) continues to work
- Existing epistemic git notes unchanged
- Database remains source of truth (git is enhancement)

### Graceful Degradation
- If git notes fail → Falls back to database
- If not in git repo → Uses database only
- Multi-repo projects → Each repo has own notes

---

## Recommendation

### For Empirica Release (Now)
✅ **Phase 1 is sufficient** - Commit message parsing works well

### For Post-Release (1-2 weeks)
🔄 **Implement Phase 2** if multi-agent coordination becomes priority

### For Future (1-3 months)
🚀 **Phase 3** - Dashboard visualization, anomaly detection, epistemic trajectory analysis

---

## Timeline

**Phase 1:** ✅ DONE (implemented in goal architecture MVP)  
**Phase 2:** 1 week effort (~500 lines of code)  
**Phase 3:** 1 month effort (full feature with dashboard)

---

## Questions for Decision

1. **Is multi-agent coordination a priority post-release?**
   - If yes → Implement Phase 2 soon
   - If no → Phase 1 is sufficient

2. **Do we want lead AIs to query git directly?**
   - If yes → Phase 2 essential
   - If no → Database queries are fine

3. **Should we standardize on git as "single source of truth"?**
   - If yes → Phase 2 aligns with vision
   - If no → Keep database primary

---

## Summary

**Current State:**
- ✅ Git notes for epistemic checkpoints (EXISTING)
- ✅ Commit message parsing for tasks (Phase 1 - NEW)

**Proposed Expansion:**
- 🔄 Git notes for task metadata (Phase 2)
- 🔄 Lead AI query interface (Phase 2)
- 🔄 Unified timeline view (Phase 2)

**Recommendation:** Phase 1 is sufficient for Empirica release. Consider Phase 2 post-release if multi-agent coordination becomes priority.
