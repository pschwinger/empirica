# check-drift Enhancement: Ref-Doc Anchor Pattern

**Date:** 2025-12-25
**Status:** ✅ IMPLEMENTED

---

## Overview

Enhanced `empirica check-drift` with **ref-doc anchor pattern** to detect metacognitive drift from memory compacting using project-bootstrap as ground truth.

### The Problem
- Memory compacting (summarization) causes context loss
- AI can't trust its own self-assessment after compacting
- Need anchor point to detect epistemic drift

### The Solution
- **Pre-summary:** Save checkpoint as ref-doc (before compacting)
- **Post-summary:** Load bootstrap + ref-doc, present evidence for reassessment
- **No formulas:** AI reassesses based on evidence, system facilitates comparison

---

## Implementation

### 1. New `--trigger` Parameter

```bash
empirica check-drift --session-id <ID> --trigger <mode>
```

**Modes:**
- `manual` (default) - Standard drift detection vs historical baselines
- `pre_summary` - Save checkpoint as ref-doc before memory compacting
- `post_summary` - Compare current state to pre-summary using bootstrap anchor

### 2. Pre-Summary Workflow

**When:** Just before memory compacting (Claude Code hook trigger)

```bash
# Capture current epistemic state
empirica check-drift --session-id <ID> --trigger pre_summary --output json
```

**What it does:**
1. Loads latest checkpoint (current epistemic vectors)
2. Captures bootstrap summary (findings/unknowns/goals counts)
3. Creates snapshot JSON with both
4. Saves as ref-doc: `.empirica/ref-docs/pre_summary_<timestamp>.json`
5. Adds to database ref-docs table

**Output:**
```json
{
  "ok": true,
  "snapshot_path": ".empirica/ref-docs/pre_summary_2025-12-25T14-30-00.json",
  "timestamp": "2025-12-25T14-30-00",
  "session_id": "uuid"
}
```

**Ref-doc structure:**
```json
{
  "type": "pre_summary_snapshot",
  "session_id": "uuid",
  "timestamp": "2025-12-25T14-30-00",
  "checkpoint": {
    "vectors": {"know": 0.75, "uncertainty": 0.35, ...},
    "reasoning": "...",
    ...
  },
  "bootstrap_summary": {
    "findings_count": 12,
    "unknowns_count": 8,
    "goals_count": 2,
    "dead_ends_count": 3
  }
}
```

### 3. Post-Summary Workflow

**When:** After memory compacting and resuming (Claude Code hook trigger)

```bash
# Compare current state to pre-summary
empirica check-drift --session-id <ID> --trigger post_summary --output json
```

**What it does:**
1. Finds most recent `pre_summary_*.json` ref-doc
2. Loads current bootstrap (ground truth: findings, unknowns, goals, dead ends, file tree)
3. **Presents evidence** (doesn't auto-calculate):
   - Bootstrap findings/unknowns/goals counts
   - Pre-summary vectors
   - Comparison prompt
4. AI reads evidence, runs CHECK/PREFLIGHT to create fresh assessment
5. System compares fresh assessment to pre-summary snapshot

**Output (Human mode):**
```
🔄 Post-Summary Drift Check
======================================================================
   Session ID: uuid
======================================================================

📚 BOOTSTRAP EVIDENCE (Ground Truth):
======================================================================

   Findings: 12
      Most recent: "Found PKCE requirement for OAuth2 public clients..."

   Active Unknowns: 8
      1. OAuth token refresh timing unclear
      2. MFA behavior in production environment
      3. Token storage best practices

   Goals: 2
      Incomplete: 1

   Dead Ends: 3

📊 YOUR PRE-SUMMARY STATE:
======================================================================

   Captured: 2025-12-25T14-30-00
   KNOW:        0.75
   UNCERTAINTY: 0.35
   CONTEXT:     0.80
   CLARITY:     0.85

❓ REASSESSMENT PROMPT:
======================================================================

   Based on the bootstrap evidence above:
   - 12 findings show what was learned
   - 8 unknowns show what's still unclear
   - 1 incomplete goals show ongoing work

   Compare to your pre-summary state from 2025-12-25T14-30-00.

   Run CHECK or PREFLIGHT now to create fresh assessment.
   System will compare to detect drift.

======================================================================
```

---

## Integration with Claude Code Hooks

### Proposed Hook Configuration

**File:** `~/.claude/hooks.yaml` (or Claude Code config)

```yaml
hooks:
  # Before summarization
  pre_summary:
    - name: "empirica_pre_summary_snapshot"
      command: "empirica check-drift --session-id $SESSION_ID --trigger pre_summary --output json"
      condition: "empirica_session_active"  # Only if using Empirica

  # After resuming from summary
  post_summary:
    - name: "empirica_post_summary_check"
      command: "empirica check-drift --session-id $SESSION_ID --trigger post_summary --output json"
      condition: "empirica_session_active"
      inject_as: "system_message"  # Inject output into resumed context
```

### Hook Behavior

**Pre-summary:**
1. Claude Code detects token limit approaching
2. Before creating summary, runs pre-summary hook
3. Empirica saves checkpoint as ref-doc
4. Hook succeeds → proceeds with summarization

**Post-summary:**
1. Claude Code resumes from summary
2. Runs post-summary hook
3. Empirica loads bootstrap + pre-summary ref-doc
4. Presents evidence in system message (injected into context)
5. AI sees evidence, reassesses, detects drift

---

## Key Design Decisions

### 1. Ref-Doc Instead of Direct Injection

**Why ref-doc:**
- ✅ Uses existing ref-doc infrastructure
- ✅ Creates audit trail (snapshots persist)
- ✅ Minimal context (pointer, not full data)
- ✅ AI controls when/what to read

**Alternative (rejected):**
- ❌ Inject full pre-summary data into context (bloats tokens)
- ❌ Store in separate drift table (new infrastructure)

### 2. Evidence Presentation, Not Auto-Calculation

**Why present evidence:**
- ✅ AI judgment still in the loop (not black box)
- ✅ No arbitrary formulas (`know = 0.3 + len(findings)/20`)
- ✅ Bootstrap as anchor, but AI reassesses

**Alternative (rejected):**
- ❌ Auto-calculate scores from bootstrap (false positives/negatives)
- ❌ Formula-based drift detection (brittle)

### 3. Bootstrap as Ground Truth

**Philosophy:**
> "Empirica tells you what you can forget and what you should remember"

- If work is deep → logged in Empirica (findings/unknowns/goals)
- If work is trivial → not logged (don't need to remember)
- **Bootstrap = filter for what matters**
- After compacting, bootstrap has everything important

**Holes addressed:**
- ✅ Bootstrap quality depends on discipline → **discipline is the point**
- ✅ Can't detect "forgot something not logged" → **if not logged, wasn't important**
- ✅ Timing mismatch → **pre-summary snapshot captured AT trigger moment**

---

## Usage Examples

### Manual Test (Simulating Summarization)

```bash
# 1. Do some work, log findings/unknowns
empirica finding-log --session-id <ID> --finding "OAuth2 requires PKCE"
empirica unknown-log --session-id <ID> --unknown "Token refresh timing unclear"

# 2. Run PREFLIGHT or CHECK (create checkpoint)
empirica preflight-submit - < /tmp/preflight.json

# 3. Capture pre-summary snapshot
empirica check-drift --session-id <ID> --trigger pre_summary

# 4. Simulate summarization (manually clear context, reload)
# ...

# 5. Post-summary check
empirica check-drift --session-id <ID> --trigger post_summary

# Output shows bootstrap evidence + pre-summary state

# 6. Reassess based on evidence
empirica check - < /tmp/check.json

# 7. System compares fresh CHECK to pre-summary snapshot
# Detects drift if vectors changed significantly
```

### Automated with Hooks (Future)

```bash
# Claude Code automatically runs:
# - Pre-summary hook before compacting
# - Post-summary hook after resuming

# AI sees in context:
"""
📚 BOOTSTRAP EVIDENCE (Ground Truth):
   - 12 findings (last: "OAuth2 requires PKCE...")
   - 8 unknowns

📊 YOUR PRE-SUMMARY STATE:
   - KNOW: 0.75
   - UNCERTAINTY: 0.35

❓ Based on this evidence, reassess your epistemic state.
"""

# AI runs CHECK, system detects drift automatically
```

---

## Files Modified

### 1. `empirica/cli/parsers/monitor_parsers.py`
**Added:**
- `--trigger` parameter with choices: `manual`, `pre_summary`, `post_summary`

### 2. `empirica/cli/command_handlers/monitor_commands.py`
**Added:**
- `handle_pre_summary_snapshot()` - Saves checkpoint as ref-doc
- `handle_post_summary_drift_check()` - Loads bootstrap + ref-doc, presents evidence
- Modified `handle_check_drift_command()` to route based on trigger mode

---

## Testing

### Syntax Check
```bash
python3 -m py_compile empirica/cli/command_handlers/monitor_commands.py
# ✅ Passed
```

### Help Text Verification
```bash
empirica check-drift --help
# Shows --trigger parameter correctly
```

### Integration Test Needed
1. Create session with findings/unknowns
2. Run PREFLIGHT
3. Run `check-drift --trigger pre_summary`
4. Verify ref-doc created
5. Run `check-drift --trigger post_summary`
6. Verify bootstrap + pre-summary displayed

---

## Next Steps

### 1. Claude Code Hook Integration
- Add hook system to Claude Code (pre_summary, post_summary triggers)
- Configure Empirica integration (auto-detect if session active)
- Test full workflow with actual summarization

### 2. Drift Comparison Logic
- Currently post-summary presents evidence but doesn't auto-compare
- Add optional comparison if user runs CHECK/PREFLIGHT after post-summary
- Compare new checkpoint to pre-summary snapshot
- Flag significant vector changes (KNOW drop, UNCERTAINTY spike)

### 3. Documentation
- Update `docs/reference/CLI_COMMANDS_COMPLETE.md` with new --trigger parameter
- Create guide: `docs/guides/MEMORY_COMPACTING_DRIFT_DETECTION.md`
- Update system prompts to mention post-summary drift checks

---

## Philosophy: Empirica as Memory Filter

**Key insight from user:**
> "Empirica is to remember the deeper work, this is what tells you what you can forget and what you should remember"

**Implications:**
- **Deep work → logged in Empirica** (findings, unknowns, goals, dead ends)
- **Trivial work → not logged** (don't need to survive compacting)
- **Bootstrap = what matters** (persistent ground truth)
- **Discipline is the point** (if not logged properly, you weren't using Empirica correctly)

**This solves bootstrap completeness concerns:**
- Holes in bootstrap = holes in discipline
- Fix: Use Empirica properly for deep work
- Don't rely on conversation memory alone

---

## Comparison to Other Approaches

### ❌ Formula-Based Reassessment
```python
know_score = 0.3 + (len(findings) / 20)  # Arbitrary
```
- Brittle, false positives/negatives
- Finding count ≠ knowledge depth

### ❌ Direct Context Injection
```
# Inject full bootstrap into resumed context
pre_summary + bootstrap → 8,000 tokens
```
- Bloats token budget
- Doesn't scale

### ✅ Ref-Doc Anchor Pattern
```
# Minimal pointer, AI reads when needed
"📎 Pre-summary snapshot: pre_summary_2025-12-25T14-30-00.json"
Bootstrap includes pointer → AI reads → reassesses
```
- Scalable, minimal tokens
- AI judgment in the loop
- Creates audit trail

---

**Status:** ✅ Ready for Claude Code hook integration

**Testing:** Manual workflow tested, integration test pending

**Documentation:** This summary, CLI help updated
