# Empirica Epistemic Learning System

## The Vision

Empirica is not just a workflow framework - it's a **continuous epistemic learning system** that enables AI agents to autonomously improve through:

1. **Capturing problems** without interrupting flow
2. **Storing knowledge** with semantic embeddings
3. **Learning patterns** across sessions
4. **Making better decisions** based on past experience
5. **Improving collaboratively** across multiple AI agents

## The 5-Layer Knowledge Graph

Every project accumulates knowledge across these five layers:

### Layer 1: FINDINGS
**What we discovered that works**
- "Implemented OAuth2 with JWT tokens"
- "Connection pooling reduces latency by 60%"
- Stored in: `project_findings` table
- Semantic: Success patterns, what to replicate

### Layer 2: UNKNOWNS
**What we don't know yet**
- "Token refresh mechanism unclear"
- "Performance bottleneck not identified"
- Stored in: `project_unknowns` table
- Semantic: Knowledge gaps, investigation targets

### Layer 3: ISSUES (Auto-Captured)
**Problems we encountered and how we handled them**
- "CHECK-SUBMIT doesn't support stdin JSON" → RESOLVED
- "Database timeout under load" → HANDOFF to specialist
- "CLI commands lack config file support" → WONTFIX (by design)
- Stored in: `auto_captured_issues` table
- Semantic: Anti-patterns, what NOT to do, learning history

### Layer 4: MISTAKES
**Things we tried that didn't work**
- "Tried WebSocket approach - too complex"
- "Attempted connection pooling with HikariCP - caused deadlocks"
- Stored in: `mistakes_made` table
- Semantic: Dead ends, failed approaches

### Layer 5: DEAD ENDS
**Architectural decisions and why they were rejected**
- "Investigated REST caching - incompatible with real-time requirements"
- "Considered microservices - overengineering for this scale"
- Stored in: `project_dead_ends` table
- Semantic: Design tradeoffs, architectural constraints

## How Issues Drive Learning

### Issue Lifecycle = Learning Progression

```
NEW
├─ "Problem discovered, no action yet"
├─ Semantic: "This exists and needs attention"
└─ AI thinks: "Should I work on this?"

↓

INVESTIGATING
├─ "AI actively working on it"
├─ Semantic: "Someone is handling this"
└─ Next AI thinks: "This is being addressed"

↓

RESOLVED
├─ "AI X fixed this on [date]"
├─ Semantic: "Problem solved by approach X"
├─ Includes: resolution notes with what worked
└─ Next AI thinks: "If I see this again, try X first"

OR

HANDOFF
├─ "AI X couldn't finish, marking for specialist"
├─ Semantic: "Requires expertise, context preserved"
└─ Specialist AI thinks: "Here's what was already tried"

OR

WONTFIX
├─ "Intentional decision not to fix"
├─ Semantic: "Known issue, but acceptable/out-of-scope"
└─ Next AI thinks: "This is a known constraint"
```

## The Continuous Learning Loop

### Session N: Foundation
```
AI-1 works on Feature X
├─ Discovers: "CLI stdin support missing"
├─ Auto-captures: BUG, severity=HIGH
├─ Fixes it: Adds config file parsing
├─ Marks: RESOLVED, resolution="Added parser"
└─ Result: Knowledge stored + vectorized
```

### Session N+1: Learning
```
AI-2 starts work on Related Feature Y
├─ Runs project-bootstrap
├─ Sees: "Recent issue: CLI stdin support"
├─ Semantic search: "CLI JSON issues"
├─ Finds: "Someone solved similar problem"
├─ Applies: Same fix pattern to their work
└─ Result: Leverages past learning, faster completion
```

### Session N+2: Pattern Recognition
```
AI-3 analyzes all accumulated issues
├─ Detects pattern: "stdin JSON missing in 5 commands"
├─ Semantic grouping: Related issues clustered
├─ Proposes: Systemic solution, not one-offs
└─ Result: Project-level improvement from accumulated learning
```

### Session N+3: Autonomous Improvement
```
AI-4 makes decisions informed by entire history
├─ Knows: What's been tried, what worked, what failed
├─ Semantic understanding: "These patterns lead to issues"
├─ Makes proactive decisions: "Avoid that approach"
└─ Result: Continuous autonomous improvement
```

## Technical Architecture

### Storage Layers

```
Memory Layers (Atomic Write)
├── SQLite (Queryable)
│   └── auto_captured_issues table
│       ├── id, session_id, category, severity
│       ├── status (new/investigating/resolved/wontfix)
│       └── resolution notes
│
├── Git Notes (Immutable Audit Trail)
│   └── refs/issues/... (optional)
│       └── Signed, versioned issue checkpoints
│
└── Qdrant Vectors (Semantic Search)
    └── Issue embeddings
        ├── Semantic similarity
        ├── Pattern detection
        └── Cross-session learning
```

### Query Patterns

```python
# Current: Direct queries
issues = service.list_issues(status="resolved", category="bug")

# Future: Semantic queries (Qdrant Phase 3)
similar_issues = qdrant.search(
    query="database performance problems",
    limit=5
)
# Returns: Issues semantically related to query

# Future: Pattern detection
patterns = qdrant.analyze(
    project_id="...",
    time_window="30 days"
)
# Returns: Emerging patterns, anti-patterns
```

## Integration with CASCADE

### PREFLIGHT Phase
- Set baseline: "What we know before starting"
- Not directly related to issues

### CHECK Phase
- Display active issues as context
- "Here are problems we've encountered"
- Informs confidence decision

### POSTFLIGHT Phase
- Issues created during session are logged
- Next AI sees: "This is what was tried"

### project-bootstrap
- Shows findings + unknowns + active issues
- Next AI sees full epistemic state
- Enables informed decision-making

## Semantic Retrieval Examples

### Example 1: Avoid Duplicate Work
```
New AI encounters: Timeout in database queries
├─ Semantic search: "database performance issues"
├─ Finds: "Performance issue: Query took 2500ms (expected 500ms)"
├─ Finds resolution: "Implemented connection pooling"
└─ AI learns: "Try connection pooling first"
```

### Example 2: Learn From Anti-patterns
```
AI considers: Using WebSocket approach
├─ Semantic search: "WebSocket patterns"
├─ Finds mistake: "Tried WebSocket - too complex"
├─ Finds detail: "REST polling was better fit"
└─ AI learns: "Avoid WebSocket for this use case"
```

### Example 3: Cross-AI Knowledge Transfer
```
AI-1 session ends: "Here's what I couldn't finish"
├─ Issue marked: HANDOFF, assigned_to="ai-optimizer"
├─ Includes: Full context, stack trace, attempted fixes
│
AI-2 session starts: Gets bootstrap
├─ Sees: "Pending optimization work with full context"
├─ No re-investigation needed
└─ Can start immediately where AI-1 left off
```

## Current Implementation Status

### ✅ Phase 1: Core Capture (COMPLETE)
- Issue capture service: `empirica/core/issue_capture.py`
- 6 CLI commands: issue-list, issue-show, issue-handoff, issue-resolve, issue-export, issue-stats
- Database schema: `auto_captured_issues` table
- Handoff workflow: Export/import with full context

### 🔄 Phase 2: CASCADE Integration (IN PROGRESS)
- Add issues to project-bootstrap output
- Display active issues in CHECK gate
- Auto-capture errors during CASCADE phases

### 📋 Phase 3: Qdrant Integration (PLANNED)
- Embed all issues with semantic vectors
- Implement semantic search across issues
- Pattern detection across sessions
- Cross-AI knowledge transfer optimization

### 📋 Phase 4: Learning Analytics (PLANNED)
- Track which resolutions were actually helpful
- Measure pattern recognition effectiveness
- Generate project health metrics
- Autonomous improvement measurement

## Decision: Storage Semantics

### What Gets Stored
✅ All issues (never deleted)
✅ Status history (audit trail)
✅ Resolution notes (what worked)
✅ Who fixed it and when
✅ Full semantic embeddings

### What Gets Shown in bootstrap
✅ Active issues (new/investigating/handoff)
✅ Recently resolved (last 30 days)
✅ Critical bugs (severity=blocker)
⚠️ Old resolved (summary count only)

### What Never Gets Deleted
✅ Issues marked resolved (not deleted)
✅ Mistakes logged (not hidden)
✅ Dead ends documented (not removed)
✅ Complete audit trail preserved

**Rationale**: Learning requires history. Deleting resolved issues removes the learning value.

## Why This Matters

### Without Auto-Capture
- Each AI rediscovers the same problems
- Context lost between sessions
- No continuous improvement
- Knowledge siloed per AI

### With Auto-Capture + Semantic Learning
- **Efficiency**: Don't repeat others' work
- **Quality**: Learn from mistakes
- **Coordination**: Seamless multi-AI handoffs
- **Autonomy**: Improve without human guidance
- **Resilience**: Knowledge survives AI changes

## Next Steps

1. **Integrate issues into project-bootstrap** (next session)
2. **Auto-capture CASCADE errors** (next session)
3. **Implement Qdrant semantic search** (future)
4. **Build learning analytics** (future)
5. **Measure autonomous improvement** (future)

---

**Core Principle**: Every problem encountered is a learning opportunity. By capturing and storing it epistemically, the system enables continuous autonomous improvement across all future work.
