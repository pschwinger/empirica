# Git Parsing for Goal Tracking - Design Document

## Context

**Question from User:** What's involved in git parsing? It seems very useful - lead devs (AI-based) can see what the goals are of agents and track their progress simply via git. That seems like it would be very useful alongside the git notes in epistemic checks during git checkpoints.

**Assessment:** This is an EXCELLENT insight! Git parsing for goal tracking would create a unified audit trail that connects:
1. **Goals/Tasks** (what the AI intends to do)
2. **Git Commits** (what the AI actually did)
3. **Epistemic Checkpoints** (what the AI learned/believed at each stage)

## The Vision

### Current State
- Goals and subtasks are tracked in database
- Completion evidence is **manually recorded** as strings
- No automatic linkage between commits and task completion

### Desired State
- **Automatic commit → task mapping** using commit message patterns
- **Lead AI can query git log** to see team progress
- **Unified timeline** showing goals, commits, and epistemic state
- **Git as single source of truth** for "what actually happened"

## Implementation Design

### Phase 1: Git Commit Pattern Matching (MVP - Easy Win)

**Commit Message Convention:**
```bash
git commit -m "✅ [TASK:abc-123-def] Implement input validation

Added validation for goal objectives and success criteria.
Addresses subtask abc-123-def from goal 'Goal Architecture MVP'.
"
```

**Parser Logic:**
```python
import re
import subprocess

def parse_commit_for_task_completion(commit_hash: str) -> Optional[str]:
    """
    Extract subtask ID from commit message
    
    Pattern: ✅ [TASK:subtask-uuid] or [COMPLETE:subtask-uuid]
    Returns: subtask_id if found
    """
    msg = subprocess.check_output(
        ['git', 'log', '-1', '--format=%B', commit_hash],
        text=True
    )
    
    # Look for task completion markers
    patterns = [
        r'✅\s*\[TASK:([a-f0-9-]+)\]',
        r'\[COMPLETE:([a-f0-9-]+)\]',
        r'Addresses subtask ([a-f0-9-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, msg, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def auto_update_from_git():
    """
    Scan recent commits and auto-mark subtasks complete
    """
    # Get commits since last scan
    recent_commits = subprocess.check_output(
        ['git', 'log', '--since="1 hour ago"', '--format=%H'],
        text=True
    ).strip().split('\n')
    
    for commit_hash in recent_commits:
        subtask_id = parse_commit_for_task_completion(commit_hash)
        if subtask_id:
            # Auto-mark subtask complete with commit as evidence
            tracker.record_subtask_completion(
                subtask_id, 
                evidence=f"commit:{commit_hash[:7]}"
            )
```

**Benefits:**
- ✅ Simple to implement (~200 lines)
- ✅ Non-invasive (optional convention)
- ✅ Works today with existing git
- ✅ AI can easily include task IDs in commits

### Phase 2: Git Notes Integration (Enhanced Traceability)

**Combine with Existing Git Checkpoint System:**
```python
def create_task_completion_note(commit_hash: str, subtask: SubTask):
    """
    Add structured note to commit with task metadata
    
    Links commit to goal architecture in git notes namespace
    """
    note_data = {
        'subtask_id': subtask.id,
        'goal_id': subtask.goal_id,
        'description': subtask.description,
        'epistemic_importance': subtask.epistemic_importance.value,
        'completed_timestamp': time.time()
    }
    
    # Store in git notes (refs/notes/empirica-tasks)
    note_json = json.dumps(note_data, indent=2)
    subprocess.run([
        'git', 'notes', '--ref=empirica-tasks', 
        'add', '-m', note_json, commit_hash
    ])
```

**Query Interface for Lead AI:**
```python
def get_team_progress_from_git(goal_id: str) -> Dict[str, Any]:
    """
    Lead AI can query git to see team progress on a goal
    
    Returns timeline of commits mapped to subtasks
    """
    # Get all commits with task notes
    commits = subprocess.check_output([
        'git', 'log', '--format=%H %s', '--notes=empirica-tasks'
    ], text=True).strip().split('\n')
    
    progress = {
        'goal_id': goal_id,
        'commits': [],
        'completed_subtasks': []
    }
    
    for line in commits:
        commit_hash = line.split()[0]
        
        # Check if this commit has task note
        try:
            note = subprocess.check_output([
                'git', 'notes', '--ref=empirica-tasks', 
                'show', commit_hash
            ], text=True)
            
            task_data = json.loads(note)
            if task_data['goal_id'] == goal_id:
                progress['commits'].append({
                    'hash': commit_hash[:7],
                    'subtask': task_data['description'],
                    'timestamp': task_data['completed_timestamp']
                })
                progress['completed_subtasks'].append(task_data['subtask_id'])
        except:
            continue
    
    return progress
```

### Phase 3: Integration with Epistemic Checkpoints (The Power Move)

**Unified Git Timeline:**
```
commit abc123  [Task: ✅ Input validation]  [Epistemic: KNOW:0.85, UNCERTAINTY:0.25]
commit def456  [Task: ✅ Database schema]   [Epistemic: KNOW:0.75, UNCERTAINTY:0.35]
commit ghi789  [Task: ❌ Failed test fix]  [Epistemic: KNOW:0.60, UNCERTAINTY:0.50]
```

**Combined Query:**
```python
def get_agent_journey(session_id: str, goal_id: str):
    """
    Show complete agent journey: goals → actions → learning
    
    For lead AI to understand what happened and why
    """
    return {
        'goal': goal_repo.get_goal(goal_id),
        'planned_tasks': task_repo.get_goal_subtasks(goal_id),
        'git_timeline': [
            {
                'commit': 'abc123',
                'timestamp': '2024-01-15 10:30',
                'task_completed': 'Input validation',
                'epistemic_state': {
                    'know': 0.85,
                    'uncertainty': 0.25
                },
                'files_changed': ['validation.py', 'test_validation.py']
            },
            # ... more commits
        ],
        'epistemic_deltas': {
            'know': 0.40 → 0.85,  # Learning trajectory
            'uncertainty': 0.65 → 0.25  # Confidence growth
        }
    }
```

## Use Cases

### Use Case 1: Multi-Agent Team Coordination

**Scenario:** Lead AI managing 3 junior AIs on a complex task

```python
# Lead AI queries team progress
team_status = {
    'agent_1': get_team_progress_from_git('goal-abc-123'),
    'agent_2': get_team_progress_from_git('goal-def-456'),
    'agent_3': get_team_progress_from_git('goal-ghi-789')
}

# Lead AI sees:
# - Agent 1: 80% complete, 8/10 commits
# - Agent 2: 20% complete, 2/10 commits, last commit 3 hours ago (blocked?)
# - Agent 3: 100% complete, all tests passing

# Lead AI can intervene: "Agent 2 seems stuck, let me check their epistemic state"
epistemic_check = load_git_checkpoint(agent_2_session_id)
# Sees: UNCERTAINTY=0.85, KNOW=0.35 → Agent 2 needs help!
```

### Use Case 2: Post-Mortem Analysis

**Scenario:** Understanding why a task failed

```bash
# Git log shows the story
git log --notes=empirica-tasks --notes=empirica-checkpoints

commit xyz  [TASK: Attempted performance optimization]
            [EPISTEMIC: KNOW:0.55, UNCERTAINTY:0.65, CLARITY:0.40]
            "I thought caching would help but wasn't sure..."
            
commit abc  [TASK: Reverted optimization]  
            [EPISTEMIC: KNOW:0.70, UNCERTAINTY:0.35, CLARITY:0.85]
            "Realized the issue was database N+1, not caching"
```

**Insight:** The epistemic state shows the AI was uncertain (0.65) when it made the wrong choice. After investigation (INVESTIGATE phase), uncertainty dropped and it corrected course.

### Use Case 3: Onboarding New AI Agent

**Scenario:** New AI needs to understand existing codebase

```python
# New AI: "What were the goals of the previous work?"
history = get_agent_journey(previous_session_id, previous_goal_id)

# New AI sees:
# 1. Original goal: "Implement authentication system"
# 2. Subtasks completed (from git): 12/15
# 3. Incomplete tasks: OAuth integration, token refresh, rate limiting
# 4. Epistemic trajectory: KNOW grew from 0.35 → 0.80 over 3 days
# 5. Blockers noted: "OAuth provider documentation unclear" (UNCERTAINTY spike)

# New AI can continue from exactly where previous AI left off
```

## Implementation Roadmap

### Now (Phase 1 - Can implement today)
- ✅ Add `parse_commit_for_task_completion()` to `CompletionTracker`
- ✅ Add commit message pattern matching
- ✅ Auto-scan recent commits on `track_progress()` call
- ✅ Document commit conventions for AIs

**Effort:** 2-3 hours, ~200 lines of code

### Next (Phase 2 - 1 week)
- Add git notes for task completion metadata
- Build query interface for lead AIs
- Integrate with existing `create_git_checkpoint()`
- Add CLI command: `empirica git-progress <goal-id>`

**Effort:** 1 day, ~500 lines of code

### Future (Phase 3 - 1 month)
- Unified timeline visualization
- Epistemic trajectory analysis
- Multi-agent coordination dashboard
- Automatic anomaly detection (stuck agents)

**Effort:** 1 week, full feature

## Recommendation

**Start with Phase 1 NOW** because:
1. ✅ Minimal effort (~200 lines)
2. ✅ Immediate value (automatic task completion)
3. ✅ Non-invasive (optional convention)
4. ✅ Foundation for Phases 2 & 3
5. ✅ Aligns with "git as epistemic memory" vision

**The killer feature:** Lead AIs can run `git log --notes=empirica-tasks` and see **exactly** what happened, when, and why. This is HUGE for multi-agent teams.

## Code to Add Today

Add to `empirica/core/completion/tracker.py`:

```python
def auto_update_from_recent_commits(self, goal_id: str, since: str = "1 hour ago") -> int:
    """
    Scan recent git commits and auto-mark subtasks complete
    
    Args:
        goal_id: Goal to update
        since: Time period to scan (git log --since format)
        
    Returns:
        Number of subtasks auto-completed
    """
    import subprocess
    import re
    
    try:
        # Get recent commits
        result = subprocess.run(
            ['git', 'log', f'--since={since}', '--format=%H'],
            capture_output=True, text=True, check=True
        )
        
        commit_hashes = result.stdout.strip().split('\n')
        auto_completed = 0
        
        for commit_hash in commit_hashes:
            if not commit_hash:
                continue
            
            # Get commit message
            msg_result = subprocess.run(
                ['git', 'log', '-1', '--format=%B', commit_hash],
                capture_output=True, text=True, check=True
            )
            
            # Look for task completion markers
            patterns = [
                r'✅\s*\[TASK:([a-f0-9-]+)\]',
                r'\[COMPLETE:([a-f0-9-]+)\]',
                r'Addresses subtask ([a-f0-9-]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, msg_result.stdout, re.IGNORECASE)
                if match:
                    subtask_id = match.group(1)
                    
                    # Verify this subtask belongs to the goal
                    subtask = self.task_repo.get_subtask(subtask_id)
                    if subtask and subtask.goal_id == goal_id:
                        # Auto-mark complete
                        if self.record_subtask_completion(
                            subtask_id, 
                            evidence=f"commit:{commit_hash[:7]}"
                        ):
                            auto_completed += 1
                            logger.info(
                                f"Auto-completed subtask {subtask_id} from commit {commit_hash[:7]}"
                            )
        
        return auto_completed
        
    except subprocess.CalledProcessError:
        logger.warning("Failed to scan git commits (not a git repo?)")
        return 0
```

**Usage:**
```python
# AI can call this after making commits
tracker = CompletionTracker()
count = tracker.auto_update_from_recent_commits(goal_id)
print(f"Auto-completed {count} tasks from recent commits")
```

## Questions for Discussion

1. **Should git parsing be always-on or opt-in?**
   - Recommendation: Opt-in via flag (`auto_track_from_git=True`)
   
2. **What commit message format should be standard?**
   - Recommendation: `✅ [TASK:uuid]` for clarity and searchability
   
3. **Should we backfill existing commits?**
   - Recommendation: No, only scan forward from now
   
4. **How does this interact with non-git workflows?**
   - Recommendation: Falls back gracefully if not in git repo

## Related Work

- **Existing:** Git checkpoints for epistemic state (97.5% token reduction)
- **Existing:** Reflex logger tracks decisions in database
- **New:** This bridges goals → commits → epistemic state

**This creates a unified audit trail in git that lead AIs can query!**
