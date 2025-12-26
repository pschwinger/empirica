# Auto Issue Capture: Continuous Epistemic Learning System

## Overview

Auto Issue Capture is not just error tracking - it's a **continuous epistemic learning system** that enables AI agents to:
- Capture problems discovered during work without interrupting flow
- Learn patterns from previous work (bugs, performance issues, incomplete work)
- Make better decisions across sessions by understanding what's been tried
- Improve autonomously through semantic retrieval of similar issues

## Architecture: 5-Layer Knowledge System

Empirica's epistemic memory consists of five complementary layers, all storable in Qdrant for semantic retrieval:

```
PROJECT KNOWLEDGE GRAPH
├── 1. FINDINGS (positive discoveries)
│   └── "Implemented OAuth2 with JWT tokens"
│   └── Semantic: "auth implementation patterns"
│
├── 2. UNKNOWNS (gaps identified)
│   └── "Token refresh mechanism unclear"
│   └── Semantic: "gaps in current knowledge"
│
├── 3. AUTO-CAPTURED ISSUES (problems encountered)
│   └── "CHECK-SUBMIT doesn't support stdin JSON"
│   └── Semantic: "CLI compatibility issues"
│   └── Status: resolved → next AI knows it was fixed
│
├── 4. MISTAKES (things tried and failed)
│   └── "Tried connection pooling with HikariCP - caused deadlocks"
│   └── Semantic: "anti-patterns, what NOT to do"
│
├── 5. DEAD ENDS (paths explored and abandoned)
│   └── "Investigated WebSocket approach - too complex for use case"
│   └── Semantic: "architectural decisions, why NOT taken"
│
└── 6. EPISTEMIC ARTIFACTS (sources & validation)
    └── Papers, docs, validated facts
    └── Semantic: "ground truth for this domain"
```

## How Issues Fit Into Epistemic Learning

### Issue Lifecycle and Meaning

Each issue passes through phases with semantic significance:

```
NEW → INVESTIGATING → RESOLVED/WONTFIX/HANDOFF
                ↓
         Each state tells next AI something
```

**NEW**: "Problem discovered, no action taken yet"
- Next AI: "Should I work on this?"

**INVESTIGATING**: "AI actively working on it"
- Next AI: "This is being handled, don't duplicate"

**RESOLVED**: "AI X fixed this on [date]"
- Next AI: "This problem is solved. If you see it again, here's what worked"

**HANDOFF**: "AI X couldn't finish, marking for specialist"
- Next AI: "I'm the specialist - here's context from who started it"

**WONTFIX**: "Intentional decision not to fix"
- Next AI: "This is a known issue but we're accepting it - here's why"

### Semantic Retrieval Use Cases

Once all issues are stored in Qdrant with vectors:

**Case 1: Avoid Duplicate Work**
```
New AI encounters timeout in database queries
→ Semantic search: "database performance issues"
→ Finds: "Performance issue: Query user_profiles took 2500ms (expected 500ms)"
→ Finds resolution: "Implemented connection pooling"
→ AI: "I should implement connection pooling first"
```

**Case 2: Learn From Mistakes**
```
AI considers using approach X
→ Semantic search: "approach X patterns"
→ Finds mistake: "Tried WebSocket approach - too complex for this use case"
→ AI: "Someone already tried that and abandoned it. Why? Let me check..."
```

**Case 3: Pattern Recognition**
```
AI notices 3 similar CLI compatibility issues
→ Semantic search groups them
→ AI discovers pattern: "stdin JSON support missing across commands"
→ AI proposes systemic fix: "Add config file support to all commands"
```

**Case 4: Cross-AI Knowledge Transfer**
```
AI-1 encounters bug, creates issue, marks RESOLVED
AI-2 starts on related task
→ Project-bootstrap includes issue with status=resolved
→ AI-2 semantic search: "related CLI issues"
→ Finds: "Previous AI fixed CHECK-SUBMIT stdin support"
→ AI-2: "I should check if my work benefits from that fix"
```

## Issue Categories and Semantic Meaning

| Category | Meaning | Cross-Session | Semantic Value |
|----------|---------|----------------|-----------------|
| **BUG** | Code defect | ✅ YES | Anti-pattern, what to avoid |
| **ERROR** | Runtime failure | ⚠️ CONTEXT | Was it transient or systemic? |
| **TODO** | Incomplete work | ✅ YES | Work queue, continuous improvement |
| **PERFORMANCE** | Degradation | ✅ YES | Optimization opportunities |
| **DEPRECATION** | Old patterns | ✅ YES | Migration path, what's superseded |
| **COMPATIBILITY** | Version/platform issues | ✅ YES | Environmental constraints |
| **DESIGN** | Architecture question | ✅ YES | Design decisions, tradeoffs |
| **WARNING** | Potential problem | ⚠️ CONTEXT | Risk assessment |

## Integration Points

### 1. CASCADE Workflow

```
PREFLIGHT → THINK → PLAN → INVESTIGATE → CHECK → ACT → POSTFLIGHT
                                  ↓
                         Auto-capture issues
                         during investigation
                         
                          ↓
                         
                    Display in project-bootstrap
                    as epistemic context
```

### 2. Project-Bootstrap Output

```json
{
  "findings": [...],
  "unknowns": [...],
  "issues": {
    "active": [
      {"id": "...", "category": "bug", "message": "..."}
    ],
    "resolved": [
      {"id": "...", "message": "...", "resolution": "..."}
    ]
  }
}
```

### 3. Qdrant Semantic Index

All issues stored as vectors:
```
Issue → Embedding → Qdrant Vector Store
          ↓
    Semantic search for related issues
    Pattern detection across sessions
    Continuous learning
```

## Decision: What Gets Stored vs What Gets Shown

### Stored (All Sessions, All Projects)
- ✅ All issues with status
- ✅ Resolution notes
- ✅ Who fixed it and when
- ✅ Full semantic embedding

### Shown in project-bootstrap
- ✅ Active issues (new, investigating, handoff)
- ✅ Recently resolved (last 30 days)
- ✅ Critical bugs (severity=blocker)
- ⚠️ Old resolved issues (summary count only)

### Removed (Never)
- ❌ Issues never deleted
- ✅ Status marks completion, not deletion
- ✅ Audit trail preserved
- ✅ Semantic learning maintained

## Continuous Learning Loop

```
Session N: AI-1 encounters issue → captures it → resolves it
                                    ↓
                            Stored in project DB
                            Vectorized in Qdrant
                                    ↓
Session N+1: AI-2 starts work
                ↓
        project-bootstrap shows issues
        AI-2 semantic search finds related issues
                ↓
        AI-2 learns: "Someone tried X before"
                ↓
        AI-2 makes better decision
                ↓
        Project knowledge improves
                ↓
Session N+2: AI-3 benefits from N+1's learning
                ↓
        Continuous improvement cycle
```

## Implementation Status

### Phase 1: Core Capture ✅ COMPLETE
- Issue capture service fully functional
- CLI commands (6 total) operational
- Database schema in place
- Manual testing verified

### Phase 2: CASCADE Integration 🔄 IN PROGRESS
- [ ] Add issues to project-bootstrap output
- [ ] Display active issues in CHECK gate
- [ ] Filter resolved issues appropriately

### Phase 3: Qdrant Integration 📋 PENDING
- [ ] Embed all issues with vectors
- [ ] Semantic search for similar issues
- [ ] Pattern detection across sessions
- [ ] Cross-AI knowledge transfer

### Phase 4: Learning Analytics 📋 PENDING
- [ ] Track which resolved issues were actually helpful
- [ ] Measure pattern recognition effectiveness
- [ ] Improve AI decision quality over time
- [ ] Generate insights about project trends

## Example: Real-World Scenario

```
PROJECT: Empirica Core CLI

Session 1 (AI-1 - rovo-dev):
├─ Discovers: "CHECK-SUBMIT doesn't support stdin JSON"
├─ Auto-captures: BUG, severity=HIGH, status=NEW
├─ Fixes it: Adds config file support
├─ Marks: status=RESOLVED, resolution="Added stdin/config parsing"
└─ Result: Issue stored + vectorized

Session 2 (AI-2 - qwen-optimizer):
├─ Runs project-bootstrap
├─ Sees: "Recently resolved: CHECK-SUBMIT stdin support"
├─ Semantic search: "CLI JSON input issues"
├─ Finds: "CHECK also lacked stdin support"
├─ Applies same fix: "Config file support pattern"
└─ Result: Systemic improvement, not one-off fix

Session 3 (AI-3 - analysis-bot):
├─ Semantic analysis across all issues
├─ Detects pattern: "stdin JSON missing in many commands"
├─ Creates epic: "Standardize JSON input across CLI"
├─ Proposes systemic solution
└─ Result: Project-level improvement from accumulated learning
```

## Epistemic Value Proposition

Without auto-capture:
- Each AI rediscovers the same problems
- Context lost between sessions
- No continuous improvement
- Knowledge silos

With auto-capture + semantic retrieval:
- **Pattern Recognition**: Similar issues grouped by semantics
- **Decision Support**: "Here's what was tried before"
- **Continuous Learning**: Each session improves project knowledge
- **Audit Trail**: Full history of what was tried and why
- **Multi-AI Coordination**: Handoff without context loss

## Configuration

### To Enable/Disable Issue Capture
```bash
# In session initialization
empirica session-create --ai-id myai --auto-capture=true
```

### To Include in project-bootstrap
```bash
empirica project-bootstrap --project-id proj-uuid --include-issues=active
```

### To Perform Semantic Search
```bash
# Phase 3 implementation (pending)
empirica issues-search --project-id proj-uuid \
  --semantic-query "database performance problems"
```

## Next Steps

1. **Add issues to project-bootstrap** (next session)
2. **Implement Qdrant integration** (Phase 3)
3. **Build semantic search UI** (Phase 4)
4. **Measure learning effectiveness** (Phase 4)

---

**Key Insight**: Auto Issue Capture is the foundation for continuous epistemic learning across AI agents. By storing not just what was discovered, but also what was tried and the results, the system enables autonomous improvement over time.
