# Project-Level Tracking: Multi-Repo Epistemic Memory

**Version:** 1.0  
**Date:** 2025-12-09  
**Status:** Production Ready

---

## Overview

Project-level tracking extends Empirica's session/goal system to support **long-term, multi-repo projects** with persistent epistemic memory.

**Key Capabilities:**
- Track work across multiple repositories
- Aggregate learning across dozens of sessions
- Bootstrap instant context for any session
- Preserve findings, unknowns, dead ends, and mistakes
- Compute total epistemic growth over project lifetime

---

## Problem Statement

### Without Project-Level Tracking

**Scenario:** You're working on a project spanning multiple repos over several months.

**Pain Points:**
1. **Context Loss:** Starting a new session requires 30+ minutes to remember what you were doing
2. **Duplicate Work:** Try approaches that failed weeks ago (forgot they failed)
3. **Lost Knowledge:** Findings from Session 5 not visible in Session 15
4. **No Progress Tracking:** Can't see total epistemic growth across all sessions

**Cost:** Hours wasted per session, knowledge continuously lost

---

### With Project-Level Tracking

**Same Scenario:** You create a project once, link all sessions to it.

**Benefits:**
1. **Instant Context:** `empirica project-bootstrap` → 3 seconds, full context
2. **Prevent Repeats:** Dead ends documented, mistakes logged
3. **Growing Knowledge:** All findings preserved and queryable
4. **Progress Visible:** Total learning deltas computed automatically

**Savings:** 95% time reduction (800 tokens vs 10,000), zero knowledge loss

---

## Core Concepts

### 1. Projects

**A project** groups related work across:
- Multiple repositories (e.g., `empirica`, `empirica-dev`, `empirica-chat`)
- Multiple sessions (e.g., 50 sessions over 6 months)
- Multiple goals (e.g., 20 goals across all sessions)

**Properties:**
- `name`: Human-readable project name
- `repos`: List of repository names
- `total_sessions`: Computed count
- `total_epistemic_deltas`: Aggregated learning across all sessions

---

### 2. Epistemic Memory Components

Projects track four types of epistemic data:

#### Findings (What We Learned)
```
"MCO configuration saves 300 tokens per request"
"Session Continuity Protocol prevents 1-3h duplicate work"
```

**Purpose:** Preserve discoveries across sessions

#### Unknowns (What's Still Unclear)
```
"How to auto-generate mistake patterns with LLM?"
"Cross-repo git notes sync strategy?"
```

**Purpose:** Track open questions, mark when resolved

#### Dead Ends (What Didn't Work)
```
Approach: "Extending goals table for projects"
Why Failed: "Wrong abstraction level, too coupled"
```

**Purpose:** Prevent repeat attempts

#### Mistakes (What Went Wrong)
```
Mistake: "Created pages without checking design system"
Cost: "2 hours"
Root Cause: "KNOW"
Prevention: "Always view reference implementation first"
```

**Purpose:** Learn from failures, prevent repeats

---

### 3. Reference Docs

Track key documentation for the project:

```
docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md (system-prompt)
empirica/data/session_database.py (code)
docs/production/05_EPISTEMIC_VECTORS.md (reference)
```

**Purpose:** AI knows what docs exist, when to reference, when to update

---

### 4. Breadcrumbs

**Breadcrumbs** = Epistemic context for starting a new session

**Two Modes:**

**session_start (fast):**
- Recent 10 findings
- Unresolved unknowns only
- Recent 5 dead ends
- Recent 5 mistakes
- Token cost: ~800 (92% savings vs manual)

**live (complete):**
- All findings
- All unknowns (resolved + unresolved)
- All dead ends
- All mistakes
- Token cost: ~2,000 (80% savings vs manual)

---

## Quick Start

### 1. Create a Project

```bash
empirica project-create \
  --name "My App Backend" \
  --description "REST API, auth service, payment processing" \
  --repos '["backend", "auth-service", "payment-service"]' \
  --output json
```

**Output:**
```json
{
  "ok": true,
  "project_id": "abc123...",
  "name": "My App Backend",
  "repos": ["backend", "auth-service", "payment-service"]
}
```

---

### 2. Link Sessions to Project

**Option A: At session creation** (future)
```bash
empirica session-create --project-id abc123... --bootstrap-breadcrumbs
```

**Option B: Link existing session** (current)
```python
from empirica.data.session_database import SessionDatabase
db = SessionDatabase()
db.link_session_to_project(session_id, project_id)
db.close()
```

---

### 3. Log Epistemic Data During Work

#### Log Findings
```bash
empirica finding-log \
  --project-id abc123... \
  --session-id def456... \
  --finding "Redis caching reduced API latency from 200ms to 50ms"
```

#### Log Unknowns
```bash
empirica unknown-log \
  --project-id abc123... \
  --session-id def456... \
  --unknown "How to handle rate limiting for authenticated vs unauthenticated users?"
```

#### Log Dead Ends
```bash
empirica deadend-log \
  --project-id abc123... \
  --session-id def456... \
  --approach "Using MongoDB for session storage" \
  --why-failed "High read latency (150ms), switched to Redis"
```

#### Log Mistakes
```bash
empirica mistake-log \
  --session-id def456... \
  --mistake "Deployed without updating Redis cache keys" \
  --why-wrong "Old cache keys returned stale data for 2 hours" \
  --cost-estimate "2 hours debugging + customer complaints" \
  --root-cause-vector "STATE" \
  --prevention "Add cache key update to deployment checklist"
```

---

### 4. Add Reference Docs
```bash
empirica refdoc-add \
  --project-id abc123... \
  --doc-path "docs/API.md" \
  --doc-type "api" \
  --description "REST API documentation - update when endpoints change"
```

---

### 5. Bootstrap Context (Start New Session)

```bash
empirica project-bootstrap --project-id abc123...
```

**Output:**
```
📋 Project Context: My App Backend
   REST API, auth service, payment processing
   Repos: backend, auth-service, payment-service
   Total sessions: 12

📝 Recent Findings:
   1. Redis caching reduced API latency from 200ms to 50ms
   2. JWT tokens in HTTPOnly cookies prevent XSS attacks
   ... (8 more)

❓ Unresolved Unknowns:
   1. How to handle rate limiting for auth vs unauth users?
   2. Payment retry strategy for transient failures?
   ... (5 more)

💀 Dead Ends (Don't Try Again):
   1. MongoDB for session storage → High latency
   2. Custom crypto implementation → Failed security review
   ... (3 more)

⚠️  Mistakes to Avoid:
   1. Deployed without cache key update (cost: 2h)
      → Add to deployment checklist
   ... (7 more)

📄 Reference Docs:
   1. docs/API.md (api) - Update when endpoints change
   2. auth-service/README.md (architecture)
   ... (4 more)
```

**Time:** 3 seconds  
**Tokens:** ~800  
**Context:** Complete

---

## CLI Commands

### Project Management

#### `project-create`
Create a new project for multi-repo tracking.

```bash
empirica project-create \
  --name <name> \
  --description <description> \
  --repos <json-array> \
  [--output json]
```

**Example:**
```bash
empirica project-create \
  --name "E-commerce Platform" \
  --description "Full-stack e-commerce with microservices" \
  --repos '["frontend", "api-gateway", "product-service", "order-service"]'
```

---

#### `project-list`
List all projects.

```bash
empirica project-list [--output json]
```

---

#### `project-handoff`
Create project-level handoff report (aggregates all session handoffs).

```bash
empirica project-handoff \
  --project-id <uuid> \
  --summary <summary> \
  [--key-decisions <json-array>] \
  [--patterns <json-array>] \
  [--remaining-work <json-array>] \
  [--output json]
```

**Example:**
```bash
empirica project-handoff \
  --project-id abc123... \
  --summary "Completed auth service MVP, API gateway 80% done" \
  --key-decisions '["JWT over OAuth2 for simplicity", "Redis for sessions"]' \
  --patterns '["Microservices communicate via events", "Each service has own DB"]' \
  --remaining-work '["Implement payment service", "Add rate limiting"]'
```

**Output:**
- Aggregates all session handoffs
- Computes total learning deltas
- Extracts recent mistakes (last 10)
- Builds next session bootstrap suggestions

---

#### `project-bootstrap`
Show epistemic breadcrumbs for instant context.

```bash
empirica project-bootstrap \
  --project-id <uuid> \
  [--output json]
```

---

### Epistemic Memory

#### `finding-log`
Log a project finding (what was learned/discovered).

```bash
empirica finding-log \
  --project-id <uuid> \
  --session-id <uuid> \
  --finding <text> \
  [--goal-id <uuid>] \
  [--subtask-id <uuid>] \
  [--output json]
```

---

#### `unknown-log`
Log a project unknown (what's still unclear).

```bash
empirica unknown-log \
  --project-id <uuid> \
  --session-id <uuid> \
  --unknown <text> \
  [--goal-id <uuid>] \
  [--subtask-id <uuid>] \
  [--output json]
```

---

#### `deadend-log`
Log a project dead end (what didn't work).

```bash
empirica deadend-log \
  --project-id <uuid> \
  --session-id <uuid> \
  --approach <text> \
  --why-failed <text> \
  [--goal-id <uuid>] \
  [--subtask-id <uuid>] \
  [--output json]
```

---

#### `refdoc-add`
Add a reference document to project.

```bash
empirica refdoc-add \
  --project-id <uuid> \
  --doc-path <path> \
  [--doc-type <type>] \
  [--description <text>] \
  [--output json]
```

**Doc Types:** `architecture`, `guide`, `api`, `design`, `code`, `config`, `reference`

---

## Workflow Examples

### Example 1: Long-Term Feature Development

**Scenario:** Building authentication system over 3 months

**Month 1:**
```bash
# Create project
empirica project-create --name "Auth System" --repos '["auth-service"]'

# Session 1: Research
empirica finding-log --finding "OAuth2 vs JWT: JWT simpler for our use case"
empirica unknown-log --unknown "How to handle token refresh securely?"

# Session 2: Implementation
empirica deadend-log --approach "Storing tokens in localStorage" \
  --why-failed "XSS vulnerability - security review failed"
empirica finding-log --finding "HTTPOnly cookies prevent XSS token theft"

# Session 3: Testing
empirica mistake-log --mistake "Forgot to set secure flag on cookies" \
  --cost-estimate "2 hours debugging" \
  --prevention "Add to deployment checklist"
```

**Month 3: New developer joins**
```bash
empirica project-bootstrap --project-id <auth-system>

# Instant onboarding:
# - 15 findings (what works)
# - 3 dead ends (what not to try)
# - 8 mistakes to avoid
# - 5 reference docs

# Onboarding time: 1 hour (vs 2 weeks without Empirica)
```

---

### Example 2: Cross-Repo Coordination

**Scenario:** Frontend + Backend + Mobile app

```bash
# Create project with 3 repos
empirica project-create \
  --name "Social App" \
  --repos '["frontend-web", "backend-api", "mobile-ios"]'

# Frontend session
empirica finding-log --finding "React Query simplifies API state management"

# Backend session (2 weeks later)
empirica unknown-log --unknown "Should we add GraphQL or keep REST?"

# Mobile session (1 month later)
empirica project-bootstrap --project-id <social-app>
# Sees frontend finding about React Query
# Sees backend unknown about GraphQL
# Can make informed API design decisions
```

---

### Example 3: Incident Prevention

**Scenario:** Production incident, want to prevent repeat

```bash
# Log incident as mistake
empirica mistake-log \
  --mistake "Deployed database migration without backing up first" \
  --why-wrong "Migration failed, lost 2 hours of data" \
  --cost-estimate "4 hours recovery + customer impact" \
  --root-cause-vector "STATE" \
  --prevention "Always backup before migration, add to deployment checklist"

# 3 months later, different developer
empirica project-bootstrap --project-id <production>

⚠️  Mistakes to Avoid:
   1. Deployed DB migration without backup (cost: 4h + data loss)
      → Always backup first, add to checklist

# Incident prevented
```

---

## Database Schema

### Tables

```sql
-- Projects
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    repos TEXT,  -- JSON array
    created_timestamp REAL NOT NULL,
    last_activity_timestamp REAL,
    status TEXT DEFAULT 'active',
    total_sessions INTEGER DEFAULT 0,
    total_goals INTEGER DEFAULT 0,
    total_epistemic_deltas TEXT,  -- JSON
    project_data TEXT NOT NULL
)

-- Project Findings
CREATE TABLE project_findings (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    goal_id TEXT,
    subtask_id TEXT,
    finding TEXT NOT NULL,
    created_timestamp REAL NOT NULL,
    finding_data TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
)

-- Project Unknowns
CREATE TABLE project_unknowns (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    goal_id TEXT,
    subtask_id TEXT,
    unknown TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_by TEXT,
    created_timestamp REAL NOT NULL,
    resolved_timestamp REAL,
    unknown_data TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
)

-- Project Dead Ends
CREATE TABLE project_dead_ends (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    goal_id TEXT,
    subtask_id TEXT,
    approach TEXT NOT NULL,
    why_failed TEXT NOT NULL,
    created_timestamp REAL NOT NULL,
    dead_end_data TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
)

-- Project Reference Docs
CREATE TABLE project_reference_docs (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    doc_path TEXT NOT NULL,
    doc_type TEXT,
    description TEXT,
    created_timestamp REAL NOT NULL,
    doc_data TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
)

-- Project Handoffs
CREATE TABLE project_handoffs (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    created_timestamp REAL NOT NULL,
    project_summary TEXT NOT NULL,
    sessions_included TEXT NOT NULL,  -- JSON
    total_learning_deltas TEXT,  -- JSON
    key_decisions TEXT,  -- JSON
    patterns_discovered TEXT,  -- JSON
    mistakes_summary TEXT,  -- JSON
    remaining_work TEXT,  -- JSON
    repos_touched TEXT,  -- JSON
    next_session_bootstrap TEXT,  -- JSON
    handoff_data TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
)
```

---

## Python API

```python
from empirica.data.session_database import SessionDatabase

db = SessionDatabase()

# Create project
project_id = db.create_project(
    name="My Project",
    description="Multi-repo project",
    repos=["repo1", "repo2"]
)

# Link session to project
db.link_session_to_project(session_id, project_id)

# Log epistemic data
finding_id = db.log_finding(project_id, session_id, "Found solution X")
unknown_id = db.log_unknown(project_id, session_id, "How to handle Y?")
dead_end_id = db.log_dead_end(project_id, session_id, "Approach Z", "Failed because...")

# Resolve unknown
db.resolve_unknown(unknown_id, "Finding: Solution X resolves Y")

# Add reference doc
doc_id = db.add_reference_doc(project_id, "docs/API.md", "api", "API reference")

# Bootstrap breadcrumbs
breadcrumbs = db.bootstrap_project_breadcrumbs(project_id, mode="session_start")

# Create project handoff
handoff_id = db.create_project_handoff(
    project_id,
    "Project summary",
    key_decisions=["Decision 1", "Decision 2"],
    patterns_discovered=["Pattern 1"],
    remaining_work=["Task 1", "Task 2"]
)

db.close()
```

---

## Best Practices

### 1. Log As You Go

**Don't wait until handoff to log findings.**

```bash
# Right after discovery
empirica finding-log --finding "Solution X works for problem Y"

# When you hit uncertainty
empirica unknown-log --unknown "Not sure how to handle edge case Z"

# When something fails
empirica deadend-log --approach "Tried X" --why-failed "Reason Y"
```

**Benefit:** Growing knowledge base, always current

---

### 2. Bootstrap At Session Start

**Every new session should bootstrap context.**

```bash
# First thing when starting work
empirica project-bootstrap --project-id <id>

# Review:
# - Recent findings (what we know)
# - Unresolved unknowns (what we don't know)
# - Dead ends (what not to try)
# - Mistakes (what to avoid)
```

**Benefit:** No duplicate work, instant context

---

### 3. Reference Docs for Key Files

**Add docs that AI should know about.**

```bash
empirica refdoc-add --doc-path "README.md" --doc-type "guide"
empirica refdoc-add --doc-path "src/database.py" --doc-type "code"
empirica refdoc-add --doc-path "docs/ARCHITECTURE.md" --doc-type "architecture"
```

**Benefit:** AI knows what to reference, what to update

---

### 4. Regular Project Handoffs

**Create handoff every 5-10 sessions.**

```bash
empirica project-handoff \
  --summary "Completed feature X, Y in progress" \
  --key-decisions '["Decision 1", "Decision 2"]' \
  --remaining-work '["Task 1", "Task 2"]'
```

**Benefit:** Checkpoint project state, compute total learning

---

## Token Economics

### Without Empirica

**Manual context reconstruction:**
- Read past notes: ~2000 tokens
- Query git history: ~3000 tokens
- Check documentation: ~3000 tokens
- Mental reconstruction: ~2000 tokens
- **Total: ~10,000 tokens**
- **Time: 30+ minutes**

### With Empirica (session_start mode)

**Bootstrap breadcrumbs:**
- Recent findings: ~200 tokens
- Unresolved unknowns: ~150 tokens
- Dead ends: ~100 tokens
- Mistakes: ~150 tokens
- Key decisions: ~100 tokens
- Reference docs: ~100 tokens
- **Total: ~800 tokens**
- **Time: 3 seconds**

**Savings:** 92% tokens, 99% time

---

## Troubleshooting

### Issue: Too many findings (overwhelming breadcrumbs)

**Solution:** Use live mode sparingly, rely on session_start mode for quick context

```bash
# Fast mode (default)
empirica project-bootstrap --project-id <id>
# Shows recent 10 findings

# Only use live when you need complete history
# (internally: bootstrap_project_breadcrumbs(project_id, mode="live"))
```

---

### Issue: Stale unknowns (no longer relevant)

**Solution:** Manually review and resolve

```python
# Mark as resolved even if not "solved"
db.resolve_unknown(unknown_id, "No longer relevant - architecture changed")
```

---

### Issue: Session not linked to project

**Solution:** Link manually

```python
db.link_session_to_project(session_id, project_id)
```

---

## See Also

- [CANONICAL_SYSTEM_PROMPT.md](../system-prompts/CANONICAL_SYSTEM_PROMPT.md) - Core Empirica concepts
- [05_EPISTEMIC_VECTORS.md](../production/05_EPISTEMIC_VECTORS.md) - Vector meanings
- [EPISTEMIC_CONDUCT.md](EPISTEMIC_CONDUCT.md) - Bidirectional accountability
- [PROJECT_LEVEL_TRACKING_DESIGN.md](../../PROJECT_LEVEL_TRACKING_DESIGN.md) - Architecture decisions

---

**Version History:**
- v1.0 (2025-12-09): Initial documentation for project-level tracking system
