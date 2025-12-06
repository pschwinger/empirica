# Unified Epistemic Dashboard - Implementation Roadmap

**Date:** 2025-12-06
**Vision:** One command that shows performance AND validates entire Empirica system
**Implementation:** 4 phases over 2-3 weeks

---

## Executive Summary

### Current State
- ✅ `status.sh` - Shows system metrics
- ✅ `leaderboard.sh` - Shows agent rankings
- ❌ No diagnostics (are metrics correct?)
- ❌ No action hooks (real-time capture)
- ❌ Separate commands (context switching)

### Desired State
- ✅ `empirica.sh` - Unified dashboard + diagnostics
- ✅ Action hooks - Real-time metric capture
- ✅ Architecture validation - Self-checking system
- ✅ Anomaly detection - Automatic alerts
- ✅ Traceability - Every number traceable to source

---

## Phase 1: Unified Dashboard (Week 1 - 2 Days)

### Goal: Merge status.sh + leaderboard.sh into empirica.sh

**Implementation:**
```bash
# New unified command
./empirica.sh              # Full output
./empirica.sh --summary    # Executive summary
./empirica.sh --leaderboard  # Performance only
./empirica.sh --diagnostics  # System health only
./empirica.sh --json       # Machine-readable
./empirica.sh --csv        # Spreadsheet-friendly
```

**Work:**
1. **Code consolidation** (4-6 hours)
   - Merge status.sh + leaderboard.sh into empirica.sh
   - Keep both individual commands as aliases (backward compatibility)
   - Add shared utility functions

2. **Output restructuring** (3-4 hours)
   - Section 1: System Diagnostics (new)
   - Section 2: CASCADE Workflow Health
   - Section 3: Performance Metrics
   - Section 4: System Metrics
   - Section 5: Anomalies & Alerts

3. **Testing** (2 hours)
   - Verify all modes work
   - Check output formatting
   - Validate performance (<3 seconds)

**Files:**
- `empirica.sh` (new unified script, ~600 lines)
- Deprecate: Keep `status.sh` and `leaderboard.sh` as aliases

**Success Criteria:**
- ✅ Single command shows everything
- ✅ All previous metrics still visible
- ✅ System diagnostics section added
- ✅ Execution time <3 seconds
- ✅ Backward compatible (old commands still work)

---

## Phase 2: Architecture Validation Layer (Week 1 - 3 Days)

### Goal: Validate all 9 architectural layers

**Implementation:**

```python
# New module: empirica/diagnostics/architecture_validator.py

class ArchitectureValidator:
    def validate_git_infrastructure(self):
        """Check git refs, notes, commits"""

    def validate_database_integrity(self):
        """Check FK constraints, orphaned records, types"""

    def validate_epistemic_vectors(self):
        """Check all 13 vectors, ranges, patterns"""

    def validate_cascade_workflow(self):
        """Check PREFLIGHT→CHECK→POSTFLIGHT completeness"""

    def validate_session_continuity(self):
        """Check handoffs, session chains, data preservation"""

    def validate_goals_subtasks(self):
        """Check completeness, dependencies, links"""

    def validate_handoff_reports(self):
        """Check required fields, git notes, parsing"""

    def validate_action_hooks(self):
        """Check all hooks executable, no failures"""

    def generate_report(self):
        """Return structured validation results"""
```

**Validation Checks (Examples):**

```python
# Git Infrastructure
✓ Can read all git notes without error
✓ Session IDs in notes match sessions in DB
✓ Commit timestamps reasonable
✗ ALERT: Notes corrupted on session XYZ

# Database
✓ All foreign keys valid (no orphans)
✓ All required columns present
✓ No null in critical fields
✗ ALERT: Goals without session_id found (5 records)

# Epistemic Vectors
✓ All 13 vectors present in reflexes
✓ Values 0.0-1.0 (no outliers)
✓ Uncertainty correlates with knowledge
✗ ALERT: Agent ABC has declining learning trend

# CASCADE Workflow
✓ All sessions have PREFLIGHT
✓ CHECK count reasonable (max 5 per session)
✓ All sessions have POSTFLIGHT
✗ ALERT: Agent XYZ has 12 CHECKs (infinite loop?)
```

**Work:**
1. **Design validation functions** (4-5 hours)
   - One validator per layer
   - Reusable check patterns

2. **Implement validators** (6-8 hours)
   - Write all validation logic
   - Create alerts/warnings
   - Collect results

3. **Integration** (2-3 hours)
   - Hook into empirica.sh
   - Format diagnostic output
   - Add performance metrics

**Files:**
- `empirica/diagnostics/architecture_validator.py` (new, ~400 lines)
- `empirica/diagnostics/__init__.py` (new)
- `empirica.sh` (updated to call validators)

**Success Criteria:**
- ✅ All 9 layers validated
- ✅ Issues detected and reported
- ✅ Validation <1 second
- ✅ Clear alert messages
- ✅ Diagnostics section populated

---

## Phase 3: Action Hooks Integration (Week 2 - 3 Days)

### Goal: Real-time metric capture at source

**Implementation:**

Define 8 core action hooks:

```bash
# CASCADE Workflow Hooks
.empirica/hooks/post-preflight          # After PREFLIGHT vectors written
.empirica/hooks/post-check              # After CHECK decision made
.empirica/hooks/post-postflight         # After POSTFLIGHT assessment

# Session Lifecycle Hooks
.empirica/hooks/post-session-create     # New session created
.empirica/hooks/post-session-end        # Session closing
.empirica/hooks/post-goal-create        # New goal created
.empirica/hooks/post-goal-complete      # Goal finished
.empirica/hooks/post-handoff            # Handoff report written
```

**Hook Template:**

```bash
#!/bin/bash
# Example: post-preflight hook

set -e

SESSION_ID=$1
PHASE=$2
VECTORS=$3  # JSON: {engagement: 0.85, know: 0.7, ...}

# 1. Write to primary: SQLite reflexes table
python3 << 'PYTHON'
import json, sys
from empirica.data.session_database import SessionDatabase

db = SessionDatabase()
vectors = json.loads("""$VECTORS""")
db.write_reflex(
    session_id="$SESSION_ID",
    phase="$PHASE",
    vectors=vectors,
    timestamp=time.time()
)
db.close()
PYTHON

# 2. Backup to git notes
git notes --ref=refs/notes/empirica/checkpoints \
  add -f -m "Phase: $PHASE, Session: $SESSION_ID, Vectors: $VECTORS"

# 3. Log to audit trail
echo "{\"event\": \"$PHASE\", \"session\": \"$SESSION_ID\", \"timestamp\": \"$(date -u +%s)\"}" \
  >> .empirica_reflex_logs/events.jsonl

# 4. Trigger dashboard update (if needed)
python3 scripts/update-metrics.py "$SESSION_ID"

echo "✓ Metrics captured: $SESSION_ID/$PHASE"
```

**Work:**
1. **Design hook system** (2-3 hours)
   - Identify all trigger points
   - Define hook interface
   - Create hook discovery

2. **Implement hooks** (4-6 hours)
   - Write 8 hook templates
   - Test each hook
   - Add error handling

3. **Integration with CASCADE** (3-4 hours)
   - Wire hooks into workflow
   - Call hooks at right points
   - Handle hook failures gracefully

**Files:**
- `.empirica/hooks/post-preflight` (new, ~40 lines)
- `.empirica/hooks/post-check` (new, ~40 lines)
- `.empirica/hooks/post-postflight` (new, ~40 lines)
- `.empirica/hooks/post-session-*` (3 new, ~40 lines each)
- `.empirica/hooks/post-goal-*` (2 new, ~40 lines each)
- `.empirica/hooks/post-handoff` (new, ~40 lines)
- `empirica/core/hook_manager.py` (new, ~100 lines)

**Success Criteria:**
- ✅ All 8 hooks implemented
- ✅ Hooks fire at correct times
- ✅ Metrics captured in real-time
- ✅ No performance impact (<100ms per hook)
- ✅ Failed hooks don't crash workflow
- ✅ Audit trail complete in JSON logs

---

## Phase 4: Anomaly Detection & Self-Validation (Week 2-3 - 3 Days)

### Goal: Automatic detection of problems

**Implementation:**

```python
# empirica/diagnostics/anomaly_detector.py

class AnomalyDetector:
    def detect_learning_anomalies(self):
        """
        Learning should increase → POSTFLIGHT know > PREFLIGHT know
        Flag: decreasing learning (knowledge regression)
        """

    def detect_cascade_anomalies(self):
        """
        CHECK count should be 1-5 per session
        Flag: >10 CHECKs (infinite loop?)
        Flag: 0 CHECKs (skipped decision gate?)
        """

    def detect_uncertainty_anomalies(self):
        """
        Uncertainty should decrease over session
        Flag: increasing uncertainty (getting more confused)
        """

    def detect_engagement_anomalies(self):
        """
        Engagement should stay positive
        Flag: engagement drops (motivation lost)
        """

    def detect_completion_anomalies(self):
        """
        Goals should complete within reasonable time
        Flag: goal stuck (>10 days incomplete)
        """

    def detect_continuity_anomalies(self):
        """
        Handoffs should succeed
        Flag: missing handoff reports
        Flag: session chains broken
        """

    def detect_hook_anomalies(self):
        """
        Hooks should fire consistently
        Flag: missing PREFLIGHT vectors
        Flag: missing POSTFLIGHT assessments
        """
```

**Anomaly Examples:**

```
🚩 Claude Sonnet: 5 sessions, 0 completed
   → Possible: Sessions not ending properly
   → Check: session.end_time being set

🚩 Qwen agents: Learning growth near 0
   → Possible: Model not learning from experience
   → Check: PREFLIGHT vs POSTFLIGHT vectors

🚩 storage-flow-test: 20 sessions, all in progress
   → Possible: Sessions stuck, not terminating
   → Check: Action hook for session-end firing?

🚩 Uncertainty INCREASES in POSTFLIGHT
   → Possible: Getting more confused
   → Check: Agent struggling with topic
```

**Work:**
1. **Design anomalies** (3-4 hours)
   - Define 7-10 key anomalies
   - Set alert thresholds
   - Create detection logic

2. **Implement detectors** (4-6 hours)
   - Write anomaly functions
   - Generate alert messages
   - Calculate severity

3. **Integration** (2-3 hours)
   - Hook into empirica.sh
   - Display anomalies section
   - Make actionable

**Files:**
- `empirica/diagnostics/anomaly_detector.py` (new, ~300 lines)
- `empirica/diagnostics/alerts.py` (new, ~50 lines)
- `empirica.sh` (updated to show anomalies)

**Success Criteria:**
- ✅ 7-10 anomalies detected
- ✅ Clear alert messages
- ✅ Actionable recommendations
- ✅ False positives <5%
- ✅ Performance <500ms

---

## Integration Into CASCADE Workflow

**Where action hooks live in CASCADE:**

```
Session Creation
    ↓
post-session-create hook fires
    ↓
PREFLIGHT Assessment
    ↓
post-preflight hook fires (vectors captured)
    ↓
Investigation (0-N rounds)
    ↓
CHECK Assessment
    ↓
post-check hook fires (decision captured)
    ↓
Decision: Proceed or Investigate More?
    ├─ If Investigate: → loop back
    └─ If Proceed: → ACT
    ↓
Work Done
    ↓
POSTFLIGHT Assessment
    ↓
post-postflight hook fires (learning measured)
    ↓
Handoff (optional)
    ↓
post-handoff hook fires (continuity captured)
    ↓
Session End
    ↓
post-session-end hook fires (closure confirmed)
```

---

## Unified Dashboard Output Example

```
╔════════════════════════════════════════════════════════════════════╗
║       EMPIRICA UNIFIED DASHBOARD v2.0 - FULL DIAGNOSTICS           ║
║            Status: FULLY OPERATIONAL ✓ | All Systems Green         ║
╚════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. SYSTEM DIAGNOSTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Git Infrastructure:        ✅ OK | 4 notes refs readable | 48 notes total
Database Integrity:        ✅ OK | 0 orphaned records | All FKs valid
Reflexes Table:            ✅ OK | 13 vectors present | Ranges valid
Session Continuity:        ✅ OK | 90% handoff success | 0 data loss
Action Hooks:              ✅ OK | 8/8 executable | 0 failures

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. CASCADE WORKFLOW HEALTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sessions with PREFLIGHT:   199/199 (100%) ✅
Sessions with CHECK:       187/199 (94%)  ⚠️ (12 missing CHECK)
Sessions with POSTFLIGHT:  199/199 (100%) ✅
Decision Quality:          ✅ Confidence tracking accurate

CASCADE Pattern: PREFLIGHT → [CHECK]* → POSTFLIGHT
  Avg CHECKs per session:  0.9 (good, no infinite loops)
  Max CHECKs:              5 (within expected range)
  Learning measurement:    ✅ Complete for 199 sessions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥇  1. empirica_tester        🚀🧠🔬🌟   Learning: 0.5    Mastery: 0.7
🥈  2. test_agent             🚀⚡🧠🔬   Learning: 0.225  Mastery: 0.625
🥉  3. claude-docs-overhaul   🧠🔬🎓    Learning: 0.157  Mastery: 0.9

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. SYSTEM METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sessions:       199 total (90 complete 45%) (109 in progress 55%)
Goals:          147 total (85 complete 57%) (62 in progress 43%)
Subtasks:       312 total (205 complete 65%) (107 in progress 35%)
Cascades:       Tracked via hooks (real-time)
Handoffs:       90% success (9/10 complete)

Team Learning:  Avg 0.068 | Max 0.5 | Min -0.5
Team Mastery:   Avg 0.452 | Max 0.95 | Min 0.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. ANOMALIES & ALERTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  ATTENTION NEEDED:

1. Claude Sonnet: 5 sessions, 0% complete
   → Possible: Sessions not terminating properly
   → Action: Check post-session-end hook logs

2. storage-flow-test: 20 sessions, 0% complete
   → Possible: Systematic issue with session closure
   → Action: Review session termination logic

3. Qwen agents: Learning growth near 0 (avg -0.1)
   → Possible: Model not learning from experience
   → Action: Check PREFLIGHT vs POSTFLIGHT vectors
   → Note: May be expected (test agents?)

4. 12 sessions missing CHECK phase
   → Possible: Decision gate skipped
   → Action: Verify CHECK capture hook firing

═══════════════════════════════════════════════════════════════════════
Database: .empirica/sessions/sessions.db (500KB)
Git Notes: refs/notes/empirica/{checkpoints,handoff,sessions} (48 total)
Action Hooks: 8 hooks, last fired 2025-12-06 20:15:31
Audit Trail: 3,247 events logged
Last Updated: 2025-12-06 20:15:45
System Uptime: 12.3 days, 0 critical errors
═══════════════════════════════════════════════════════════════════════
```

---

## Implementation Timeline

| Phase | Duration | Effort | Owner | Deliverable |
|-------|----------|--------|-------|-------------|
| 1: Unified Dashboard | 2 days | 10-15 hrs | Claude Code | empirica.sh |
| 2: Architecture Validation | 3 days | 15-20 hrs | Claude Sonnet | Validators |
| 3: Action Hooks | 3 days | 12-18 hrs | Qwen | Hooks + integration |
| 4: Anomaly Detection | 3 days | 10-15 hrs | Copilot CLI | Detectors |

**Total:** ~2-3 weeks, ~50-70 hours

---

## Expected Outcome

After all phases:

✅ **One command** shows everything
✅ **Real-time metrics** via action hooks
✅ **System diagnostics** built-in
✅ **Anomaly detection** automatic
✅ **Traceability** complete (everything traceable to source)
✅ **Self-validating** (can detect its own bugs)

**This becomes Empirica's health monitor and bug detector combined.**

---

## Success Criteria

### Phase 1
- ✅ empirica.sh combines status + leaderboard
- ✅ All metrics still visible
- ✅ <3 second execution
- ✅ Backward compatible

### Phase 2
- ✅ All 9 layers validated
- ✅ Issues detected
- ✅ Clear reporting
- ✅ No false positives

### Phase 3
- ✅ All 8 hooks working
- ✅ Real-time capture
- ✅ Audit trail complete
- ✅ No performance impact

### Phase 4
- ✅ 7-10 anomalies detected
- ✅ Clear alerts
- ✅ Actionable recommendations
- ✅ <1 second detection

---

**Status:** Designed and ready for implementation
**Next Step:** Start Phase 1 (merge scripts into unified dashboard)
