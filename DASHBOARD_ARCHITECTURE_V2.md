# Empirica Unified Dashboard Architecture v2.0

**Integrated Diagnostic System**

**Date:** 2025-12-06
**Status:** Design (Ready for Implementation)
**Purpose:** Single command that validates entire Empirica system + shows performance

---

## Philosophy: The Dashboard as Self-Validation

The unified dashboard serves TWO purposes:

1. **Performance Metrics** - How are my agents doing?
2. **System Diagnostics** - Is Empirica working correctly?

These are **inseparable**. If metrics are wrong, we need to see WHERE.

---

## Complete Architecture Mapping

### LAYER 1: Git Infrastructure
```
Source: .git/ directory

Validates:
├─ refs/heads/* (branches)
├─ refs/notes/empirica/checkpoints/* (session checkpoints)
├─ refs/notes/empirica/handoff/* (handoff reports)
├─ refs/notes/empirica/session-summary/* (session summaries)
└─ Git log (commit history with markers)

Metrics:
├─ Latest commit hash + message
├─ Total commits (development velocity)
├─ Branch state (on main, clean working tree)
├─ Git notes count (distributed audit trail)
└─ Notes parsing health (can decode 100% of notes)

Diagnostics:
├─ ✓ Can read all git notes without error
├─ ✓ Session IDs in notes match sessions in DB
├─ ✓ Commit timestamps reasonable
├─ ✓ Notes refs are valid
└─ 🚩 ALERT if: Notes can't be decoded, orphaned sessions, time gaps
```

### LAYER 2: SQLite Database
```
Source: .empirica/sessions/sessions.db

Tables Validated:
├─ sessions
│  ├─ Count: TOTAL
│  ├─ With end_time: COMPLETED
│  ├─ Without end_time: IN_PROGRESS
│  ├─ total_cascades > 0: HAVE_CASCADES
│  └─ avg_confidence: TEAM_CONFIDENCE
│
├─ reflexes (CRITICAL)
│  ├─ Count total
│  ├─ Count by phase (PREFLIGHT, CHECK, POSTFLIGHT)
│  ├─ All 13 vectors present: ✓ engagement, know, do, context, clarity, coherence, signal, density, state, change, completion, impact, uncertainty
│  ├─ Ranges valid: All values 0.0-1.0
│  ├─ Linked to valid sessions (foreign key check)
│  └─ Timestamps reasonable (no future dates)
│
├─ goals
│  ├─ Count total
│  ├─ is_completed flag working (count where is_completed=1)
│  ├─ Linked to valid sessions
│  └─ scope JSON parseable
│
├─ subtasks
│  ├─ Count total
│  ├─ status='completed' count
│  ├─ Linked to valid goals
│  └─ Linked to valid sessions
│
├─ handoff_reports
│  ├─ Count by session_id
│  ├─ All required columns present
│  └─ Linked to valid sessions
│
├─ cascade_metadata (LEGACY - CHECK IF USED)
│  └─ If exists: Count, check for orphaned records
│
├─ epistemic_assessments (LEGACY - CHECK IF USED)
│  └─ If exists: Count, check schema vs reflexes
│
└─ [Other tables?]
   └─ Enumerate and validate all

Diagnostics:
├─ ✓ All foreign keys valid (no orphaned records)
├─ ✓ All required columns present
├─ ✓ No null values in critical columns
├─ ✓ Data types correct
├─ ✓ Ranges valid (0.0-1.0 for vectors)
├─ ✓ Timestamps monotonic (no time travel)
├─ ✓ No duplicate session IDs
└─ 🚩 ALERT if: FK violations, null in required cols, invalid ranges
```

### LAYER 3: Epistemic Vectors (Core System)
```
Source: reflexes table + CASCADE workflow

13-Vector System:
├─ Tier 0 (Foundation - MUST GATE ≥0.6)
│  ├─ ENGAGEMENT (motivation/focus)
│  ├─ KNOW (actual domain knowledge)
│  ├─ DO (execution capability)
│  └─ CONTEXT (understand broader situation)
│
├─ Tier 1 (Comprehension)
│  ├─ CLARITY (understand requirements)
│  ├─ COHERENCE (things make sense together)
│  ├─ SIGNAL (extract signal from noise)
│  └─ DENSITY (handle complexity)
│
├─ Tier 2 (Execution)
│  ├─ STATE (understand current state)
│  ├─ CHANGE (manage changes)
│  ├─ COMPLETION (confidence in finishing)
│  └─ IMPACT (understand downstream effects)
│
└─ Meta
   └─ UNCERTAINTY (explicit doubt)

Validation Checks:
├─ ✓ All 13 vectors present in reflexes
├─ ✓ Values are 0.0-1.0 (no outliers)
├─ ✓ Uncertainty correlates with knowledge (high know = low uncertainty usually)
├─ ✓ Engagement > 0.0 (sessions have focus)
├─ ✓ Completion increases toward POSTFLIGHT
├─ ✓ Model profile bias corrections applied
│  └─ Claude Haiku: know -= 0.05, uncertainty += 0.10
│  └─ Claude Sonnet: know -= 0.03, uncertainty += 0.08
│  └─ Qwen: model-specific adjustments
└─ 🚩 ALERT if: Missing vectors, invalid ranges, suspect patterns

Metrics Shown:
├─ PREFLIGHT → POSTFLIGHT deltas (learning growth)
├─ CHECK confidence levels (decision quality)
├─ Uncertainty trajectory (clarity achieved)
└─ Per-AI vector trends
```

### LAYER 4: CASCADE Workflow
```
Source: reflexes table (phase column)

Workflow Validation:
├─ PREFLIGHT (baseline assessment)
│  ├─ Count of sessions with PREFLIGHT vectors
│  ├─ Avg values (should show honest self-assessment)
│  └─ 🚩 ALERT if: Missing PREFLIGHT in any session
│
├─ CHECK (decision gates, 0-N times)
│  ├─ Count of CHECK phases
│  ├─ Count per session (0-5 expected per persona)
│  ├─ Confidence trajectory (should increase)
│  └─ 🚩 ALERT if: >10 CHECKs (infinite loop?), confidence stuck flat
│
└─ POSTFLIGHT (learning measurement)
   ├─ Count of sessions with POSTFLIGHT
   ├─ Learning growth (POST_know - PRE_know)
   ├─ Uncertainty reduction (1.0 - POST_uncertainty)
   └─ 🚩 ALERT if: Missing POSTFLIGHT, negative learning, uncertainty increased

Round Number Validation:
├─ ✓ Phases in chronological order
├─ ✓ Round numbers make sense (0, 1, 2, ...)
└─ 🚩 ALERT if: Out of order, duplicates, gaps

Decision Quality:
├─ ✓ CHECK → ACT decisions happen
├─ ✓ Confidence >= 0.7 triggers PROCEED
├─ ✓ Confidence < 0.7 loops back to investigation
└─ 🚩 ALERT if: Decisions not aligned with confidence
```

### LAYER 5: Session Continuity
```
Source: sessions table + handoff_reports + git notes

Session Lifecycle:
├─ Created (start_time set)
├─ Has cascades (total_cascades > 0)
├─ Completed (end_time set)
└─ Handed off (handoff_reports entry exists)

Continuity Tracking:
├─ Per AI_ID:
│  ├─ Sessions created (total count)
│  ├─ Sessions completed (with end_time)
│  ├─ Completion rate (%)
│  └─ Handoff reports (for multi-session work)
│
├─ Session chains (A → B → C):
│  ├─ Session A ends with handoff_report
│  ├─ Session B starts, references A in resumption logic
│  └─ Data continuity maintained across sessions
│
└─ Epistemic continuity:
   ├─ Session A ends with POSTFLIGHT vectors
   ├─ Session B starts with same vectors? (resumed state)
   └─ 🚩 ALERT if: Handoff without report, resumed session has different vectors

Metrics:
├─ Total session chains (multi-session work)
├─ Avg chain length (session count per AI)
├─ Continuity success rate (handoffs that worked)
└─ Data loss incidents (0 = good)
```

### LAYER 6: Goals & Subtasks
```
Source: goals + subtasks tables

Goals Validation:
├─ Count total
├─ Count by is_completed (0 or 1)
├─ Linked to valid sessions (foreign keys)
├─ scope JSON parseable (breadth, duration, coordination)
├─ Completion rate by session_id
└─ 🚩 ALERT if: Orphaned goals (no session), unparseable scope, corrupt data

Subtasks Validation:
├─ Count total
├─ Count by status ('pending', 'in_progress', 'completed')
├─ Linked to valid goals (all have goal_id in goals table)
├─ Linked to valid sessions
├─ dependencies field valid JSON
└─ 🚩 ALERT if: Orphaned subtasks, status not in enum, corrupt dependencies

Metrics:
├─ Goals per session (average)
├─ Subtasks per goal (average)
├─ Completion rates (goals, subtasks)
├─ Goal complexity distribution (scope vectors)
└─ Investigation depth (subtask dependencies)
```

### LAYER 7: Handoff Reports
```
Source: handoff_reports table + git notes (refs/notes/empirica/handoff/*)

Report Validation:
├─ Count by session_id
├─ All required fields present:
│  ├─ task_summary
│  ├─ key_findings
│  ├─ remaining_unknowns
│  ├─ next_session_context
│  ├─ artifacts_created
│  └─ epistemic_vectors (snapshot)
│
├─ Git notes parsing:
│  ├─ Can decode all handoff notes
│  ├─ JSON structure valid
│  └─ Session IDs match
│
└─ 🚩 ALERT if: Missing fields, corrupt notes, orphaned reports

Metrics:
├─ Successful handoffs (report exists, data complete)
├─ Failed handoffs (session ends without report)
├─ Context preservation (unknowns → next session findings)
└─ Artifact tracking (files created, lines added)
```

### LAYER 8: Action Hooks Integration
```
Source: .empirica/hooks/ directory + git hooks

Hook Types:
├─ Pre-hooks (before CASCADE events)
│  ├─ pre-preflight (about to start)
│  ├─ pre-check (about to decide)
│  └─ pre-postflight (about to measure)
│
├─ Post-hooks (after CASCADE events)
│  ├─ post-reflex (after vectors written)
│  ├─ post-check (after decision made)
│  ├─ post-session-create (new session)
│  ├─ post-goal-create (new goal)
│  ├─ post-goal-complete (goal finished)
│  └─ post-session-end (session closed)
│
├─ Git hooks
│  ├─ post-commit (update STATUS.json)
│  ├─ post-reflex (custom hook on reflex writes)
│  └─ post-handoff (after handoff report)
│
└─ Validation:
   ├─ ✓ All hooks executable (chmod +x)
   ├─ ✓ Hooks contain valid code
   ├─ ✓ No infinite loops
   └─ 🚩 ALERT if: Hook failures, timeouts, silent errors

Metrics:
├─ Hooks triggered (count by type)
├─ Hooks succeeded/failed
├─ Hook execution time (should be <100ms)
└─ Real-time metric capture (vectors recorded at hook time)
```

### LAYER 9: Performance Metrics (Aggregated)
```
Source: All above layers combined

Per-AI Performance:
├─ Learning growth (average ΔKNOW across sessions)
├─ Goal completion rate (%)
├─ Session completion rate (%)
├─ Uncertainty mastery (1.0 - avg uncertainty)
├─ Consistency (end_time / total_sessions)
├─ Total cascades run
└─ Achievement badges earned

Team Metrics:
├─ Total sessions, goals, subtasks
├─ Completion percentages
├─ Average epistemic vectors
├─ Learning velocity (growth per session)
├─ Mastery trends (improving/stable/declining)
└─ System health (% passing diagnostics)

Trending:
├─ Learning growth over time (this week vs last)
├─ Goal completion velocity (goals/session)
├─ Mastery improvement (vector trends)
└─ Engagement tracking (motivation trajectory)
```

---

## Real-Time Metric Capture via Action Hooks

**Key insight:** Metrics should be captured AT the source (action hooks), not calculated retroactively.

### Hook → Metric Flow

```
CASCADE Workflow Event
    ↓
Action Hook Triggers
    ↓
Hook captures:
├─ Event type (preflight, check, postflight, etc.)
├─ Session ID
├─ AI ID
├─ Timestamp
├─ Current vectors (if available)
├─ Phase + round_num
└─ Context (what triggered it)
    ↓
Hook writes to:
├─ SQLite reflexes table (PRIMARY)
├─ Git notes (BACKUP)
└─ JSON log (AUDIT TRAIL)
    ↓
Dashboard queries from PRIMARY source
└─ Falls back to GIT NOTES if DB unavailable
```

### Example: PREFLIGHT Hook

```bash
# .empirica/hooks/post-preflight

#!/bin/bash
SESSION_ID=$1
VECTORS=$2  # JSON: {engagement, know, do, ...}

# 1. Write to database
empirica reflexes-write \
  --session-id "$SESSION_ID" \
  --phase "PREFLIGHT" \
  --vectors "$VECTORS"

# 2. Trigger git note write
empirica git-note-write \
  --session-id "$SESSION_ID" \
  --type "checkpoint" \
  --data "PREFLIGHT"

# 3. Update STATUS.json
python3 scripts/update-metrics.py "$SESSION_ID"

# 4. Log to JSON audit trail
echo "{\"event\": \"preflight\", \"session\": \"$SESSION_ID\", \"time\": \"$(date -u +%s)\"}" >> .empirica_reflex_logs/events.jsonl
```

---

## Unified Dashboard Output

### Command
```bash
./empirica.sh [--full] [--diagnostics] [--leaderboard] [--json] [--csv]
```

### Default Output (Combined)
```
╔════════════════════════════════════════════════════════════════════╗
║             EMPIRICA UNIFIED DASHBOARD & DIAGNOSTIC                ║
║                 Status: FULLY OPERATIONAL ✓                        ║
╚════════════════════════════════════════════════════════════════════╝

1. SYSTEM DIAGNOSTICS
   Git Infrastructure:        ✅ All 4 git notes refs readable
   Database Integrity:        ✅ No orphaned records, all FKs valid
   Reflexes Table:            ✅ All 13 vectors present, ranges valid
   Session Continuity:        ✅ 90% handoff success rate
   ACTION HOOKS:              ✅ All 8 hooks executable, 0 failures

2. CASCADE WORKFLOW HEALTH
   PREFLIGHT → CHECK → POSTFLIGHT:  ✅ All 199 sessions have full workflow
   Decision Quality:          ✅ Confidence tracking accurate
   Learning Measurement:      ✅ 199 POSTFLIGHT assessments complete

3. PERFORMANCE METRICS
   🥇 empirica_tester         🚀🧠🔬🌟    (Learning: 0.5, Mastery: 0.7)
   🥈 test_agent              🚀⚡🧠🔬    (Learning: 0.225, Mastery: 0.625)
   🥉 claude-docs-overhaul    🧠🔬🎓      (Learning: 0.157, Mastery: 0.9)

4. SYSTEM METRICS
   Sessions:                  199 (90 complete, 109 in progress)
   Goals:                     147 (85 complete, 62 in progress)
   Subtasks:                  312 (205 complete)
   Cascades:                  ??? (need to implement)
   Handoffs:                  ??? (need to implement)

5. ANOMALIES & ALERTS
   🚩 Claude Sonnet: 5 sessions, 0 completed (check for hangs?)
   🚩 storage-flow-test: 20 sessions, 0 completed (pattern issue?)
   ⚠️  Qwen agents: Low learning growth (expected? check algorithms)

═══════════════════════════════════════════════════════════════════════

Database: .empirica/sessions/sessions.db
Git Notes: 4 refs (checkpoints, handoff, sessions, etc.)
Action Hooks: 8 hooks, 0 failures
Last Updated: 2025-12-06 20:15:32
Uptime: All systems nominal
```

### With `--diagnostics` Flag
```
Detailed validation of each layer:
✓ Git: All notes decoded successfully
✓ Database: No orphaned records, all timestamps reasonable
✓ Reflexes: All 13 vectors present, ranges valid
  - Engagement avg: 0.73 (good)
  - Know avg: 0.68 (acceptable)
  - Uncertainty avg: 0.32 (good - low is good)
✓ Sessions: 45% closure rate (good for ongoing work)
✓ Goals: 57% completion rate
✓ Subtasks: 65% completion rate
✓ Handoffs: 90% success (10% missing reports - check)
✓ Hooks: All 8 operational, <100ms execution
✓ Continuity: Session chains working, data preserved

No critical issues found.
```

---

## Self-Validation Framework

The dashboard is also **self-validating**:

### If Numbers Don't Show Up

```
./empirica.sh --diagnostics

Shows where the break is:
├─ Git notes can't be read? → Git problem
├─ Database returns 0 records? → Write path broken
├─ Vectors missing? → ACTION HOOKS not firing
├─ Goals orphaned? → FK constraint issue
├─ Handoff reports incomplete? → Handoff logic broken
└─ Metrics wrong? → Calculation algorithm issue
```

### If Numbers Look Wrong

```
Examples:
├─ Uncertainty INCREASES after POSTFLIGHT?
│  → CHECK: Model not learning (understand why)
│
├─ Engagement drops suddenly?
│  → CHECK: Session termination logic
│
├─ 50% sessions have no POSTFLIGHT?
│  → CHECK: Action hook not firing
│
├─ Goals orphaned (no session)?
│  → CHECK: Foreign key constraint
│
└─ Handoff reports show 0%?
│  → CHECK: Handoff write logic
```

---

## Traceability Chain

This is the **killer feature**: complete traceability

```
Action Hook fires
    ↓
Writes to reflexes table
    ↓
Also writes to git notes (backup)
    ↓
Also writes to JSON log (audit trail)
    ↓
Dashboard queries reflexes
    ↓
If numbers don't match:
├─ Check git notes (should match)
├─ Check JSON log (full record)
├─ Check action hook logs (did it fire?)
└─ Trace exact issue
```

Every number in the dashboard is **traceable to its source**.

---

## Integration Checklist

### Phase 1: Unify Dashboard
- [ ] Combine status.sh + leaderboard.sh into empirica.sh
- [ ] Add diagnostics layer
- [ ] Add system validation
- [ ] Add anomaly alerts

### Phase 2: Action Hooks
- [ ] Define all hook types (8 minimum)
- [ ] Create hook templates
- [ ] Integrate with CASCADE workflow
- [ ] Real-time metric capture

### Phase 3: Full Architecture Mapping
- [ ] Map all 9 layers
- [ ] Validation rules per layer
- [ ] Diagnostic output for each
- [ ] Alert thresholds

### Phase 4: Self-Validation
- [ ] Layer-by-layer integrity checks
- [ ] Cross-layer consistency validation
- [ ] Anomaly detection
- [ ] Alert generation

---

## Why This Is Powerful

**The dashboard becomes Empirica's health monitor.**

Instead of:
- "Something's wrong but I don't know what"

You get:
- "Learning vectors aren't increasing because action hooks aren't firing because git notes decode is failing"

**Complete transparency. Complete traceability. Complete confidence.**

This turns the dashboard from a **reporting tool** into a **diagnostic tool**.

When Rovo Dev or Qwen or Claude find a bug, they can look at the dashboard and see EXACTLY where it is.

---

**Status:** Designed, ready for implementation
**Effort:** Medium (3-5 days)
**Impact:** High (diagnostic system for all Empirica)
