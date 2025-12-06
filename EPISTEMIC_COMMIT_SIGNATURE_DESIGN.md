# Epistemic Commit Signature Design

**Date:** 2025-12-06
**Purpose:** Make AI learning and performance visible IN git commit history
**Status:** Design (Ready for Implementation)

---

## The Goal

Every commit should tell the story of what the AI learned while making it.

**Current:**
```
commit f22eedd2
    vision: The unified epistemic dashboard - complete vision statement

    This document articulates the complete vision...
```

**Ideal (Epistemic Commit):**
```
commit f22eedd2
    vision: The unified epistemic dashboard - complete vision statement

    This document articulates the complete vision...

    Epistemic-AI: claude-code
    Epistemic-Model: claude-haiku-4-5
    Epistemic-Persona: implementer
    Epistemic-Session: f22eedd2-5198-0ce-...

    Epistemic-Learning-Delta: +0.15 (0.70 → 0.85)
    Epistemic-Mastery-Delta: +0.18 (0.77 → 0.95)
    Epistemic-Uncertainty: -0.25 (0.45 → 0.20)

    Epistemic-Phase: POSTFLIGHT
    Epistemic-Confidence: 0.92
    Epistemic-Completion: 1.0

    Files-Changed: 3 | Lines-Added: 434 | Lines-Deleted: 0
    Session-Duration: 180 minutes
```

**What changed:**
- Added epistemic trailers showing learning growth
- Shows which AI made the commit
- Shows learning delta (PREFLIGHT → POSTFLIGHT)
- Shows session context
- Shows completion/confidence

---

## Design Principles

### 1. **Trailers, Not Body**
Git has a standard format for metadata: **trailers** (lines at end of commit message)

```
Signed-off-by: Jane Doe <jane@example.com>
Co-Authored-By: John Doe <john@example.com>
```

**Why trailers?**
- ✅ Parseable by tools
- ✅ Standard git format
- ✅ Won't break commit viewing
- ✅ Searchable with `git log --grep`
- ✅ Can be extracted by scripts

### 2. **Visible in Regular Log**
Normal developers should understand the epistemic metadata:

```
$ git log --pretty=short
f22eedd2 vision: The unified epistemic dashboard
    Epistemic-AI: claude-code | Learning: +0.15 | Mastery: +0.18
```

### 3. **Structured for Parsing**
Trailers follow pattern: `Key: Value`

```
Epistemic-Learning-Delta: +0.15 (0.70 → 0.85)
Epistemic-Mastery-Delta: +0.18 (0.77 → 0.95)
```

Format: `+DELTA (BEFORE → AFTER)`
- Easy to parse
- Shows direction
- Shows magnitude
- Shows context (before/after)

### 4. **Session Traceability**
Commit tied back to session:

```
Epistemic-Session: f22eedd2-5198-0ce-bd10-a6dc6d91edc0
```

Can query:
- Which commits came from which session
- What learning happened in that session
- Full session context

---

## Complete Epistemic Commit Format

### Header (First Line)
```
<type>(<scope>): <subject>
```

**Current:** ✅ Already doing this
```
vision: The unified epistemic dashboard - complete vision statement
```

### Body (Description)
```
<detailed explanation of what/why>
```

**Current:** ✅ Already doing this

### Trailers (Epistemic Metadata)

#### AI Identity
```
Epistemic-AI: claude-code
Epistemic-Model: claude-haiku-4-5-20251001
Epistemic-Persona: implementer
```

**Why?**
- Identifies which AI made the work
- Shows which model was used
- Shows which persona (affects decision logic)
- Allows filtering: `git log --grep="Epistemic-AI: claude-sonnet"`

#### Learning Metrics
```
Epistemic-Learning-Delta: +0.15 (0.70 → 0.85)
Epistemic-Mastery-Delta: +0.18 (0.77 → 0.95)
Epistemic-Uncertainty-Delta: -0.25 (0.45 → 0.20)
```

**Why?**
- Shows learning growth in this session
- Direction: + (improved) or - (declined)
- Magnitude: 0.15 = significant learning
- Context: Before → After values

**Interpretation:**
- Learning +0.15: AI learned 15% more
- Mastery +0.18: 18% more certain
- Uncertainty -0.25: 25% less doubtful

#### Engagement Metrics
```
Epistemic-Engagement: 0.90
Epistemic-Completion: 1.0
Epistemic-Confidence: 0.92
```

**Why?**
- Engagement: How focused was the AI (0.90 = very focused)
- Completion: How much of the task finished (1.0 = 100%)
- Confidence: How confident in the result (0.92 = very confident)

#### Phase Information
```
Epistemic-Phase: POSTFLIGHT
Epistemic-Session-Duration: 180 minutes
Epistemic-CHECK-Count: 3
```

**Why?**
- Which CASCADE phase finished
- How long the session took
- How many decision gates passed

#### Session Link
```
Epistemic-Session: f22eedd2-5198-0ce-bd10-a6dc6d91edc0
Epistemic-Checkpoint: refs/notes/empirica/checkpoints/f22eedd2...
```

**Why?**
- Trace back to session in database
- Trace back to git notes (full epistemic data)
- Can query: `git log --grep="Epistemic-Session: ..."`

#### Work Metrics
```
Files-Changed: 3
Lines-Added: 434
Lines-Deleted: 0
Commits-This-Session: 7
```

**Why?**
- Shows productivity
- Shows scope of work
- Shows commits per session

#### Standard Trailers
```
Co-Authored-By: Claude <noreply@anthropic.com>
Signed-off-by: Empirica System <empirica@aiworkhorse.local>
```

**Why?**
- Standard git trailers
- Maintains compatibility
- Shows authorship clearly

---

## Complete Example: Epistemic Commit

```
design: Unified epistemic dashboard with self-validation architecture

Complete system design for next-generation dashboard.

Key components:
- 9-layer architecture mapping (git, db, vectors, cascade, etc.)
- Real-time metric capture via action hooks
- Complete traceability chain
- Self-validation framework
- Anomaly detection

This design transforms the dashboard from reporting tool to diagnostic tool.

Epistemic-AI: claude-code
Epistemic-Model: claude-haiku-4-5-20251001
Epistemic-Persona: implementer

Epistemic-Learning-Delta: +0.15 (0.70 → 0.85)
Epistemic-Mastery-Delta: +0.18 (0.77 → 0.95)
Epistemic-Uncertainty-Delta: -0.25 (0.45 → 0.20)
Epistemic-Engagement: 0.85
Epistemic-Completion: 1.0
Epistemic-Confidence: 0.92

Epistemic-Phase: POSTFLIGHT
Epistemic-Session-Duration: 180 minutes
Epistemic-CHECK-Count: 2

Epistemic-Session: f22eedd2-5198-0ce-bd10-a6dc6d91edc0
Epistemic-Checkpoint: refs/notes/empirica/checkpoints/f22eedd2

Files-Changed: 2
Lines-Added: 1146
Lines-Deleted: 0
Commits-This-Session: 4

Co-Authored-By: Claude <noreply@anthropic.com>
Signed-off-by: Empirica System <empirica@aiworkhorse.local>
```

---

## What Goes Where

### ✅ IN COMMIT MESSAGE (Trailers)

**Essential (Required):**
```
Epistemic-AI: claude-code
Epistemic-Model: claude-haiku-4-5
Epistemic-Learning-Delta: +0.15 (0.70 → 0.85)
Epistemic-Mastery-Delta: +0.18 (0.77 → 0.95)
Epistemic-Session: <session-id>
```

**Why?** These make commits self-describing. Anyone can see:
- Who made the commit
- What they learned
- Which session it came from

**Nice to Have:**
```
Epistemic-Uncertainty-Delta: -0.25
Epistemic-Completion: 1.0
Epistemic-Confidence: 0.92
Epistemic-CHECK-Count: 2
```

Why? Provides full context without looking elsewhere.

---

### ✅ IN GIT NOTES (Full Details)

**Location:** `refs/notes/empirica/checkpoints/<session-id>`

**What:** Complete epistemic state as JSON
```json
{
  "session_id": "f22eedd2-5198-0ce-...",
  "phase": "POSTFLIGHT",
  "round_num": 0,
  "vectors": {
    "engagement": 0.85,
    "know": 0.85,
    "do": 0.90,
    "context": 0.80,
    "clarity": 0.85,
    "coherence": 0.85,
    "signal": 0.80,
    "density": 0.75,
    "state": 0.85,
    "change": 0.80,
    "completion": 1.0,
    "impact": 0.90,
    "uncertainty": 0.20
  },
  "timestamp": "2025-12-06T20:26:18Z",
  "commit": "f22eedd2bad949cae73e1904cc65097d06aee8fb"
}
```

**Why?**
- Full precision (13 vectors, not just deltas)
- Machine-readable JSON
- Compressed (git notes are deduplicated)
- Audit trail (can't be modified)

---

### ✅ IN DATABASE (Structured)

**Location:** `SQLite reflexes table`

**What:** All vectors + metadata
```
session_id    | phase      | round_num | engagement | know | ... | timestamp
f22eedd2-...  | POSTFLIGHT | 0         | 0.85       | 0.85 | ... | 2025-12-06...
```

**Why?**
- Queryable (can do analytics)
- Indexed (fast lookups)
- Aggregatable (team metrics)
- Live (immediately updated)

---

### ❌ NOT IN COMMIT MESSAGE

**Don't include all 13 vectors in commit.**

Why?
- Commits get noisy
- Full data already in git notes + database
- Deltas are sufficient for understanding

---

## Commit Hook Implementation

### Hook Location
```
.git/hooks/prepare-commit-msg
```

### Hook Execution Flow

```
User commits
    ↓
prepare-commit-msg hook fires
    ↓
Hook finds current session
    ↓
Hook queries SQLite reflexes table
    ↓
Hook calculates learning deltas:
├─ PREFLIGHT know vs POSTFLIGHT know
├─ PREFLIGHT uncertainty vs POSTFLIGHT uncertainty
└─ All 13 vectors
    ↓
Hook appends trailers to commit message
    ↓
Commit is ready with epistemic metadata
```

### Hook Code (Pseudocode)

```bash
#!/bin/bash
# .git/hooks/prepare-commit-msg

# Get current session ID (from environment or last reflex)
SESSION_ID=$(get_current_session_id)

# Query database for PREFLIGHT and POSTFLIGHT vectors
PREFLIGHT=$(sqlite3 db.sqlite "
  SELECT know, uncertainty FROM reflexes
  WHERE session_id='$SESSION_ID' AND phase='PREFLIGHT'
  ORDER BY created_at LIMIT 1
")

POSTFLIGHT=$(sqlite3 db.sqlite "
  SELECT know, uncertainty FROM reflexes
  WHERE session_id='$SESSION_ID' AND phase='POSTFLIGHT'
  ORDER BY created_at DESC LIMIT 1
")

# Calculate deltas
LEARNING_DELTA=$(calc_delta $PREFLIGHT_KNOW $POSTFLIGHT_KNOW)
MASTERY_DELTA=$(calc_delta 1.0 - $POSTFLIGHT_UNCERTAINTY, 1.0 - $PREFLIGHT_UNCERTAINTY)

# Build trailer lines
TRAILERS="
Epistemic-AI: claude-code
Epistemic-Learning-Delta: $LEARNING_DELTA
Epistemic-Mastery-Delta: $MASTERY_DELTA
Epistemic-Session: $SESSION_ID
"

# Append to commit message
cat $1 >> "$TRAILERS"
```

---

## Parsing & Querying

### Extract Learning from Log

```bash
# Show commits with learning metrics
git log --pretty=format:"%h %s%n  Learning: %(trailers:key=Epistemic-Learning-Delta)"

# Output:
# f22eedd2 vision: Unified epistemic dashboard
#   Learning: +0.15 (0.70 → 0.85)
# 66430381 design: Unified epistemic dashboard architecture
#   Learning: +0.12 (0.68 → 0.80)
```

### Filter by AI

```bash
# Show commits by Claude Code only
git log --grep="Epistemic-AI: claude-code"

# Show commits by any Sonnet
git log --grep="Epistemic-AI: claude-sonnet"
```

### Calculate Team Learning

```bash
# Sum all learning deltas across commits
git log --pretty=format:"%(trailers:key=Epistemic-Learning-Delta)" | \
  grep -oE '\+[0-9.]+' | \
  awk '{sum+=$1} END {print "Total team learning: " sum}'

# Output: Total team learning: +2.47
```

### Track Persona Decisions

```bash
# Show commits by implementer persona
git log --grep="Epistemic-Persona: implementer"

# Show commits by researcher persona
git log --grep="Epistemic-Persona: researcher"
```

---

## Why This Matters

### 1. **Visible Learning**
Every commit shows what the AI learned making it.

Before: Hidden in database
After: `Epistemic-Learning-Delta: +0.15 (0.70 → 0.85)`

### 2. **Auditable Decisions**
Can trace decisions back to epistemic state.

"Why did AI-X choose approach Y?"
"Check commit C: Learning was 0.70, confidence was 0.85"

### 3. **Team Analytics**
Aggregate across commits:

```
Claude Code:  Total learning +1.52 | Avg mastery 0.85
Claude Sonnet: Total learning +0.98 | Avg mastery 0.92
Qwen: Total learning +2.14 | Avg mastery 0.88
```

### 4. **Learning Trends**
Plot learning over time:

```
Week 1: Avg learning +0.12
Week 2: Avg learning +0.18
Week 3: Avg learning +0.25

Trend: Improving (learning increasing per week)
```

### 5. **GitHub Integration**
Commits appear in GitHub with epistemic metadata visible in commit details.

```
design: Unified epistemic dashboard
by claude-code on Dec 6

Epistemic-Learning-Delta: +0.15 (0.70 → 0.85)
Epistemic-Session: f22eedd2-...

<view full commit details>
```

---

## Implementation Checklist

### Phase 1: Hook Setup (1-2 days)
- [ ] Create `.git/hooks/prepare-commit-msg`
- [ ] Query SQLite for PREFLIGHT/POSTFLIGHT vectors
- [ ] Calculate learning deltas
- [ ] Append trailers to commit message
- [ ] Test with manual commits

### Phase 2: Integration (1-2 days)
- [ ] Wire into CASCADE workflow
- [ ] Ensure session tracking works
- [ ] Test multi-session continuity
- [ ] Verify git notes + commits aligned

### Phase 3: Parsing Tools (1-2 days)
- [ ] Create `git-epilog.sh` (extract epistemic metadata)
- [ ] Create `empirica git-stats` (aggregate learning)
- [ ] Create `empirica git-trends` (plot learning over time)
- [ ] Add to `empirica.sh` dashboard

### Phase 4: Visualization (2-3 days)
- [ ] Update GitHub Actions to show leaderboard
- [ ] Create commit-level visualization
- [ ] Integrate into dashboard
- [ ] Add web view (if needed)

---

## Current vs Target State

### Current (Status Quo)
```
$ git log --oneline
f22eedd2 vision: The unified epistemic dashboard
66430381 design: Unified epistemic dashboard architecture
4163ce1d docs: Add Empirica Showcase System index

(No epistemic data visible)
```

### Target (After Implementation)
```
$ git log --pretty=empirica  # Custom format
f22eedd2 vision: The unified epistemic dashboard
  AI: claude-code | Learning: +0.15 | Mastery: +0.18 | Session: f22eedd2...

66430381 design: Unified epistemic dashboard architecture
  AI: claude-code | Learning: +0.12 | Mastery: +0.14 | Session: 66430381...

4163ce1d docs: Add Empirica Showcase System index
  AI: claude-code | Learning: +0.10 | Mastery: +0.12 | Session: 4163ce1d...

Total Team Learning This Week: +2.47
```

---

## Design Decisions

### Why Trailers, Not Tags?
- **Tags** are heavy, one per release
- **Trailers** are lightweight, one per commit
- Trailers are standard git format
- Can parse with standard tools

### Why Learning Delta, Not All Vectors?
- **Learning delta** is most important insight
- **All vectors** are in git notes (full audit trail)
- Keep commit message lean but informative
- Database has full precision for analytics

### Why Both Commit & Notes?
- **Commit trailers:** Quick insight, visible in log
- **Git notes:** Full precision, audit trail, deduplicated
- **Database:** Queryable, aggregatable, live
- **Redundancy = Safety:** Data available from multiple sources

### Why Not Use Commit Message Body?
- **Body** is free-form text (hard to parse)
- **Trailers** are structured key-value pairs
- Tools understand trailers (git, GitHub, etc.)
- Trailers are standard convention

---

## What This Enables

### Immediate (Week 1)
- See learning delta in every commit
- Understand epistemic state at commit time
- Trace back to session for full context

### Short Term (Week 2-3)
- Aggregate learning across all commits
- Plot learning trends over time
- Compare AI agents by learning
- Filter commits by persona/model

### Medium Term (Week 4+)
- GitHub integration (show in UI)
- CI/CD status linked to learning
- Automated alerts (learning declining)
- Team dashboards (GitHub org level)

### Long Term (Month 2+)
- Industry benchmarking ("Our team learns 15% per week")
- Publication of metrics ("Measured AI Learning in Open Source")
- Downstream ecosystem tools (plugins, extensions)

---

## Example: Real Commits With Epistemic Data

### Commit 1: Feature Implementation
```
feat: Add AI leaderboard with achievement badges

Implements real-time rankings with 10 achievement badges.
Shows learning growth, goal completion, mastery, consistency.

Epistemic-AI: claude-code
Epistemic-Learning-Delta: +0.18 (0.65 → 0.83)
Epistemic-Mastery-Delta: +0.22 (0.73 → 0.95)
Epistemic-Completion: 1.0
Epistemic-Session: 272ea88f-...

Files: 2 | +425 lines
```

### Commit 2: Documentation
```
docs: Add comprehensive leaderboard documentation

Complete guide covering metrics, badges, integration ideas.

Epistemic-AI: claude-code
Epistemic-Learning-Delta: +0.12 (0.75 → 0.87)
Epistemic-Mastery-Delta: +0.15 (0.80 → 0.95)
Epistemic-Completion: 1.0
Epistemic-Session: 5198d0ce-...

Files: 2 | +636 lines
```

### Commit 3: Architecture Design
```
design: Unified epistemic dashboard architecture

Complete 9-layer system design with real-time capture.

Epistemic-AI: claude-code
Epistemic-Learning-Delta: +0.15 (0.70 → 0.85)
Epistemic-Mastery-Delta: +0.18 (0.77 → 0.95)
Epistemic-Completion: 1.0
Epistemic-Session: 66430381-...

Files: 2 | +1146 lines
```

---

## Success Criteria

✅ Every commit has epistemic trailers
✅ Learning delta visible in `git log`
✅ Session ID links to database
✅ Git notes have full vectors
✅ Can query by AI/persona/model
✅ Can aggregate team learning
✅ Dashboard shows git commit stats
✅ No performance impact
✅ Backward compatible (old commits still work)

---

**Status:** Design complete, ready for implementation
**Effort:** 4-6 days (4 phases)
**Impact:** Makes Empirica learning visible in git history itself

This is the final wiring that makes Empirica truly visible.
