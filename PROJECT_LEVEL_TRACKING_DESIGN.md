# Project-Level Tracking Design Document

**Session ID:** 49f4486e-c475-401b-bb09-f6a7c83e034c  
**Goal ID:** 8b7962bc-a138-4b81-97ec-9ae3a8ae5402  
**Date:** 2025-12-09  
**Status:** Investigation Phase

---

## Problem Statement

**Current Gap:** No way to track work across multiple repositories or link sessions to long-term projects.

**Real-World Example:**
- User has: `empirica` (main), `empirica-chat` (skill package), `empirica-dev` (dev fork)
- Sessions in empirica-dev don't link back to main project
- empirica-chat work isn't tracked at all (not even a git repo)
- No project-level handoffs or learning delta aggregation
- Starting new session requires manual context reconstruction

**Impact:**
- Lost context across repos
- Duplicate work
- No project completion tracking
- Can't compute total epistemic growth for a project

---

## Investigation Findings

### Subtask 1: Multi-Repo Workflow ✅

**Repos Discovered:**
1. **empirica** (main)
   - Git repo: https://github.com/Nubaeon/empirica.git
   - Full Empirica framework
   - Sessions tracked in `.empirica/sessions/sessions.db`

2. **empirica-chat**
   - NOT a git repo - just a directory
   - Contains: Claude skill package (.skill files, guides)
   - Purpose: Simplified 4-vector Empirica for Claude chat
   - No session tracking currently

3. **empirica-dev**
   - Git repo: https://github.com/Nubaeon/empirica-dev.git
   - Development fork of main empirica
   - Separate `.empirica/` directory
   - Sessions don't link to main project

**Current Pain Points:**
- Work in empirica-dev is isolated from main
- empirica-chat changes aren't tracked
- No way to see "all sessions related to Empirica project"
- Starting new session = manual "what did I work on last time?" reconstruction

---

## Design: Projects Table Schema

### Approach: New Table (Not Extending Goals)

**Rationale:**
- Goals are session-scoped (hours to days)
- Projects are multi-session, multi-repo (weeks to months)
- Different lifecycle and queries
- Cleaner separation of concerns

### Schema Design

```sql
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,                    -- UUID
    name TEXT NOT NULL,                     -- "Empirica Core"
    description TEXT,                       -- "Main framework development"
    repos TEXT,                             -- JSON array: ["empirica", "empirica-dev", "empirica-chat"]
    created_timestamp REAL NOT NULL,
    last_activity_timestamp REAL,
    status TEXT DEFAULT 'active',           -- 'active' | 'paused' | 'complete'
    metadata TEXT,                          -- JSON: tags, priority, etc.
    
    -- Computed fields (updated on checkpoint/handoff)
    total_sessions INTEGER DEFAULT 0,
    total_goals INTEGER DEFAULT 0,
    total_epistemic_deltas TEXT,            -- JSON: aggregated learning across all sessions
    
    project_data TEXT NOT NULL              -- Full JSON blob for extensibility
)
```

### Session-Project Linking

**Option A: Foreign Key in Sessions Table** (RECOMMENDED)
```sql
ALTER TABLE sessions ADD COLUMN project_id TEXT;
ALTER TABLE sessions ADD FOREIGN KEY (project_id) REFERENCES projects(id);
```

**Pros:**
- Simple 1:many relationship
- Easy queries: "SELECT * FROM sessions WHERE project_id = ?"
- No junction table overhead

**Cons:**
- Session can only belong to one project

**Option B: Junction Table**
```sql
CREATE TABLE project_sessions (
    project_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    PRIMARY KEY (project_id, session_id),
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
)
```

**Pros:**
- Session can belong to multiple projects
- More flexible

**Cons:**
- More complex queries
- Extra table to maintain
- Unclear when one session relates to multiple projects

**Decision: Option A (Foreign Key)**
- Most common case: 1 session = 1 project
- Simpler implementation
- Can extend later if multi-project sessions needed

---

## Project-Level Handoff Structure

### Design: Aggregate All Session Handoffs

```json
{
  "project_handoff_id": "uuid",
  "project_id": "uuid",
  "timestamp": "2025-12-09T...",
  
  "project_summary": "Completed mistakes tracking system, epistemic conduct framework, MCO protocols",
  
  "sessions_included": [
    {
      "session_id": "uuid1",
      "date": "2025-12-09",
      "summary": "Implemented mistakes tracking",
      "epistemic_deltas": {"know": 0.35, "do": 0.35, ...}
    },
    {
      "session_id": "uuid2",
      "date": "2025-12-08",
      "summary": "Designed MCO protocols",
      "epistemic_deltas": {"know": 0.25, ...}
    }
  ],
  
  "total_learning_deltas": {
    "know": 0.60,        // Sum across all sessions
    "do": 0.55,
    "uncertainty": -0.85  // Total uncertainty reduction
  },
  
  "key_decisions": [
    "Used MCO configuration instead of system prompt bloat (~300 tokens saved)",
    "Bidirectional accountability framework for epistemic conduct",
    "Projects table for multi-repo tracking"
  ],
  
  "patterns_discovered": [
    "Session Continuity Protocol prevents 1-3 hours duplicate work",
    "Web Project Protocol prevents 2-4 hours design system mistakes"
  ],
  
  "mistakes_made": [
    {
      "mistake": "Created pages without checking design system",
      "cost": "2 hours",
      "root_cause": "KNOW",
      "prevention": "Always view reference implementation first"
    }
  ],
  
  "remaining_work": [
    "Project-level tracking implementation",
    "Epistemic breadcrumbs bootstrap"
  ],
  
  "repos_touched": ["empirica", "empirica-dev"],
  
  "next_session_bootstrap": {
    "context_breadcrumbs": [
      "Last worked on: Project-level tracking design",
      "Key decision: Use foreign key in sessions table",
      "Discovered: empirica-chat is not a git repo"
    ],
    "suggested_focus": "Implement projects table and CLI commands"
  }
}
```

### Storage

**Option 1: Git Notes** (RECOMMENDED)
- Namespace: `refs/notes/empirica/project-handoff/<project_id>`
- Benefit: Versioned, survives repo clones
- Format: JSON

**Option 2: Database Table**
```sql
CREATE TABLE project_handoffs (
    handoff_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    created_timestamp REAL NOT NULL,
    handoff_data TEXT NOT NULL,  -- Full JSON
    FOREIGN KEY (project_id) REFERENCES projects(id)
)
```

**Decision: Both** (3-layer like reflexes)
- Git notes (primary, versioned)
- Database (queryable)
- JSON files (human-readable backup)

---

## Epistemic Breadcrumbs Bootstrap

### What are "Epistemic Breadcrumbs"?

Quick context for starting a new session on an existing project:

1. **Last session summary** (what was worked on)
2. **Recent mistakes** (what NOT to do)
3. **Key decisions** (design choices made)
4. **Remaining unknowns** (what needs investigation)
5. **Patterns discovered** (reusable knowledge)

### Bootstrap Mechanism

```python
def bootstrap_session_with_project_context(project_id: str, session_id: str):
    """
    Load epistemic breadcrumbs from project history
    """
    # 1. Get project metadata
    project = db.get_project(project_id)
    
    # 2. Get latest project handoff
    latest_handoff = db.get_latest_project_handoff(project_id)
    
    # 3. Get recent mistakes (last 10)
    recent_mistakes = db.get_mistakes(project_id=project_id, limit=10)
    
    # 4. Get incomplete goals
    incomplete_goals = db.get_goals(project_id=project_id, status='in_progress')
    
    # 5. Get recent session handoffs (last 3)
    recent_handoffs = db.get_session_handoffs(project_id=project_id, limit=3)
    
    # 6. Aggregate into breadcrumbs
    breadcrumbs = {
        "project": {
            "name": project['name'],
            "description": project['description'],
            "total_sessions": project['total_sessions'],
            "learning_deltas": project['total_epistemic_deltas']
        },
        "last_activity": {
            "summary": latest_handoff['project_summary'],
            "date": latest_handoff['timestamp'],
            "next_focus": latest_handoff['next_session_bootstrap']['suggested_focus']
        },
        "mistakes_to_avoid": [
            {
                "mistake": m['mistake'],
                "prevention": m['prevention'],
                "cost": m['cost_estimate']
            }
            for m in recent_mistakes[:5]  # Top 5
        ],
        "key_decisions": latest_handoff['key_decisions'],
        "incomplete_work": [
            {
                "goal": g['objective'],
                "progress": f"{g['completed_subtasks']}/{g['total_subtasks']}"
            }
            for g in incomplete_goals
        ]
    }
    
    return breadcrumbs
```

### CLI Usage

```bash
# Create session with project context
empirica session-create --project-id <ID> --bootstrap-breadcrumbs

# Output:
# 📋 Loading project context...
# Project: Empirica Core (3 sessions, 15 hours)
# Last activity: 2025-12-09 - "Implemented mistakes tracking"
# 
# ⚠️  Recent mistakes to avoid:
#   1. Created pages without design system check (cost: 2 hours)
#      → Always view reference implementation first
# 
# 🎯 Incomplete work:
#   1. Project-level tracking (2/6 subtasks complete)
# 
# 💡 Suggested focus: Implement projects table and CLI commands
# 
# Session created: 49f4486e-c475-401b-bb09-f6a7c83e034c
```

### Token Efficiency

**Without breadcrumbs:**
- Manual context reconstruction: ~5000 tokens
- Reading multiple handoff reports: ~3000 tokens
- Checking goals/mistakes manually: ~2000 tokens
- **Total: ~10,000 tokens**

**With breadcrumbs:**
- Automated aggregation: ~500 tokens
- **Savings: 95%**

---

## CLI Commands Design

### `empirica project-create`

```bash
empirica project-create \
  --name "Empirica Core" \
  --description "Main framework development" \
  --repos '["empirica", "empirica-dev", "empirica-chat"]' \
  --output json

# Output:
{
  "ok": true,
  "project_id": "uuid",
  "name": "Empirica Core",
  "repos": ["empirica", "empirica-dev", "empirica-chat"]
}
```

### `empirica project-checkpoint`

```bash
empirica project-checkpoint \
  --project-id <ID> \
  --summary "Implemented mistakes tracking and epistemic conduct framework" \
  --key-decisions '["MCO config instead of prompt bloat", "Bidirectional accountability"]' \
  --output json

# Creates checkpoint in git notes + database
```

### `empirica project-handoff`

```bash
empirica project-handoff \
  --project-id <ID> \
  --output json

# Aggregates all session handoffs since last project checkpoint
# Computes total learning deltas
# Extracts patterns, mistakes, decisions
# Stores in git notes + database
```

### `empirica session-create --project-id`

```bash
empirica session-create \
  --ai-id claude-rovo-dev \
  --project-id <ID> \
  --bootstrap-breadcrumbs \
  --output json

# Links session to project
# Loads epistemic breadcrumbs
# Displays context summary
```

---

## Implementation Plan

### Phase 1: Database Schema (High Priority)
1. Add `projects` table
2. Add `project_id` column to `sessions` table
3. Add `project_handoffs` table (optional - can use git notes only)
4. Create indexes

### Phase 2: Database Methods (High Priority)
1. `create_project(name, description, repos) -> project_id`
2. `get_project(project_id) -> project_dict`
3. `link_session_to_project(session_id, project_id)`
4. `get_project_sessions(project_id) -> [sessions]`
5. `aggregate_project_learning_deltas(project_id) -> deltas_dict`
6. `create_project_handoff(project_id, ...) -> handoff_id`
7. `get_latest_project_handoff(project_id) -> handoff_dict`
8. `bootstrap_project_breadcrumbs(project_id) -> breadcrumbs_dict`

### Phase 3: CLI Commands (High Priority)
1. `project-create` command handler
2. `project-checkpoint` command handler
3. `project-handoff` command handler
4. Update `session-create` to accept `--project-id` and `--bootstrap-breadcrumbs`
5. Register commands in CLI core

### Phase 4: Git Integration (Medium Priority)
1. Store project handoffs in git notes: `refs/notes/empirica/project-handoff/<project_id>`
2. 3-layer atomic write (git + database + JSON)
3. Query from git notes for cross-repo access

### Phase 5: MCP Integration (Medium Priority)
1. Add MCP tools: `create_project`, `project_handoff`, `bootstrap_breadcrumbs`
2. Route to CLI like other commands

### Phase 6: Testing (High Priority)
1. Create test project: "Empirica Ecosystem"
2. Link 3 sessions across empirica/empirica-dev
3. Create project checkpoint
4. Generate project handoff
5. Start new session with breadcrumbs bootstrap
6. Verify context loaded correctly

---

## Remaining Unknowns

1. **Mistake pattern generation:** How to analyze project-level mistakes and auto-generate prevention strategies?
   - Could use LLM to analyze mistake patterns
   - "You've made 3 KNOW-related mistakes, all design system related → Pattern: Always check design system first"

2. **Cross-repo git notes:** If empirica and empirica-dev are separate repos, how do project handoffs sync?
   - Option A: Store in main repo only
   - Option B: Mirror to all repos
   - Option C: Use shared .empirica/ directory

3. **Project completion criteria:** How to mark a project as "complete"?
   - Manual: `empirica project-complete --project-id <ID>`
   - Auto: All goals complete + explicit confirmation

4. **Breadcrumbs staleness:** How old is too old for breadcrumbs?
   - Option: Only include sessions from last 30 days
   - Option: Include all sessions but weight recent ones higher

---

## Next Steps

1. Complete subtask 2: Finalize projects table schema
2. Complete subtask 3: Design session-project linking (foreign key decided)
3. Complete subtask 4: Design project handoff structure (defined above)
4. Complete subtask 5: Design breadcrumbs bootstrap (defined above)
5. Move to implementation phase (subtask 6)

---

**Session Status:** Investigation phase ongoing, 2/6 subtasks complete
**UNCERTAINTY:** Dropped from 0.65 → 0.35 after investigation
**Ready for:** CHECK phase to decide if we should proceed to prototype
