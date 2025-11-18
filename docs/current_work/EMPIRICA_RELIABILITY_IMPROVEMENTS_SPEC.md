# Empirica Reliability Improvements Specification

**Date:** 2025-11-18
**Version:** 1.0
**Status:** Ready for Implementation
**Target:** AI agents using Empirica framework via MCP tools

---

## Executive Summary

This specification addresses reliability improvements for AI agents using Empirica. The goal is to achieve 95%+ reliability for the core workflow by:
1. Automating manual steps that AI agents might forget
2. Adding graceful degradation for component failures
3. Ensuring session aliases work across all MCP tools
4. Providing actionable error messages
5. Clarifying when to use Empirica

**Scope:** MCP tools and system prompts (AI agent perspective)
**Out of scope:** Human UIs, dashboards, multi-agent coordination (Cognitive Vault)

---

## Current State Assessment

### What's Working (85-90% reliability)
- ✅ Session aliases for continuity (latest:active:claude-code)
- ✅ Git checkpoints (97.5% token reduction)
- ✅ MCP tools (39 tools, bootstrap/PREFLIGHT/CHECK/POSTFLIGHT tested)
- ✅ Calibration tracking (well_calibrated results)
- ✅ CLI commands (35 consolidated commands)

### What Needs Improvement
- ⚠️ Manual drift detection (agents forget to call it)
- ⚠️ Manual goal generation (extra step after PREFLIGHT)
- ⚠️ Inconsistent session alias support (only 4/39 tools)
- ⚠️ Poor error messages (no actionable suggestions)
- ⚠️ No graceful degradation (components fail hard)
- ⚠️ Vague decision criteria (when to use Empirica?)

---

## Improvement 1: Automatic Drift Detection in CHECK Phase

### Problem
AI agents must manually call `check_drift_monitor()` during CHECK phase. The system prompt says "optional but important for long tasks" - this is easy to forget.

### Current Behavior
```python
# Agent must remember to do this:
execute_check(session_id, findings, remaining_unknowns, confidence)

# Then separately:
drift = check_drift_monitor(session_id, window_size=3)
if drift.get('drift_detected'):
    print("⚠️ Drift detected")
```

### Proposed Behavior
```python
# execute_check automatically checks drift
result = execute_check(
    session_id=session_id,
    findings=[...],
    remaining_unknowns=[...],
    confidence_to_proceed=0.75
)

# Returns includes drift analysis:
{
  "ok": true,
  "drift_analysis": {
    "detected": true,
    "type": "overconfidence",
    "pattern": "Confidence increasing faster than evidence supports",
    "severity": "moderate",
    "window_size": 3,
    "assessments_analyzed": 3
  },
  "recommendation": "recalibrate_before_acting",
  "safe_to_proceed": false  # Blocks ACT if severe drift
}
```

### Implementation Details

**File:** `mcp_local/empirica_mcp_server.py`

**Function:** `execute_check` handler (around line 1750)

**Changes:**
1. After receiving CHECK submission, automatically call drift monitor
2. Analyze drift severity (minor/moderate/severe)
3. Include drift results in response
4. Set `safe_to_proceed: false` if severe drift detected

**Drift Severity Thresholds:**
- **Minor:** Drift detected, but <0.15 delta in key vectors
- **Moderate:** 0.15-0.30 delta, recommend recalibration
- **Severe:** >0.30 delta, block ACT phase

**Integration Point:**
```python
elif name == "execute_check":
    # ... existing CHECK logic ...

    # NEW: Auto-run drift monitor
    from empirica.calibration.drift_monitor import DriftMonitor

    monitor = DriftMonitor(session_id=session_id)
    drift_result = monitor.check_drift(window_size=3)

    # Analyze severity
    severity = "none"
    safe_to_proceed = True

    if drift_result.get('drift_detected'):
        max_delta = max([abs(d) for d in drift_result.get('vector_deltas', {}).values()])
        if max_delta > 0.30:
            severity = "severe"
            safe_to_proceed = False
        elif max_delta > 0.15:
            severity = "moderate"
        else:
            severity = "minor"

    # Add to response
    response['drift_analysis'] = {
        'detected': drift_result.get('drift_detected', False),
        'type': drift_result.get('drift_type', 'none'),
        'pattern': drift_result.get('pattern', ''),
        'severity': severity,
        'window_size': 3
    }
    response['safe_to_proceed'] = safe_to_proceed

    return response
```

**Testing:**
- Test with stable assessments (no drift) → safe_to_proceed: true
- Test with moderate drift → warning but proceed
- Test with severe drift → safe_to_proceed: false

---

## Improvement 2: Auto-Generate Investigation Goals from PREFLIGHT

### Problem
After PREFLIGHT, if uncertainty is high (>0.6), AI agents should investigate. But calling `generate_goals()` is a separate manual step.

### Current Behavior
```python
# Step 1: PREFLIGHT
execute_preflight(session_id, prompt)
submit_preflight_assessment(session_id, vectors, reasoning)

# Step 2: Agent must manually call this if uncertain
goals = generate_goals(session_id, conversation_context, use_epistemic_state=True)
```

### Proposed Behavior
```python
# PREFLIGHT automatically generates goals if uncertainty > threshold
result = execute_preflight(session_id, prompt)

# If uncertainty > 0.6, returns:
{
  "ok": true,
  "uncertainty_detected": true,
  "uncertainty_score": 0.65,
  "recommendation": "investigate",
  "auto_generated_goals": [
    {
      "description": "Investigate CLI command structure and dependencies",
      "priority": "high",
      "rationale": "KNOW score 0.65 indicates knowledge gaps"
    },
    {
      "description": "Map all 52 commands to handler functions",
      "priority": "high",
      "rationale": "STATE score 0.45 indicates incomplete environment mapping"
    }
  ],
  "next_step": "Follow investigation goals, then call execute_check()"
}
```

### Implementation Details

**File:** `mcp_local/empirica_mcp_server.py`

**Function:** `submit_preflight_assessment` handler (around line 1620)

**Changes:**
1. After PREFLIGHT submission, calculate overall uncertainty
2. If uncertainty > 0.6, automatically call goal orchestrator
3. Return generated goals in response
4. Provide clear next step guidance

**Integration Point:**
```python
elif name == "submit_preflight_assessment":
    # ... existing PREFLIGHT logic ...

    # Calculate overall uncertainty
    uncertainty = vectors.get('uncertainty', 0.5)
    know = vectors.get('know', 0.5)
    do_score = vectors.get('do', 0.5)
    state = vectors.get('state', 0.5)

    # NEW: Auto-generate goals if high uncertainty
    auto_goals = None
    recommendation = "proceed"

    if uncertainty > 0.6 or know < 0.7 or state < 0.6:
        recommendation = "investigate"

        # Call goal orchestrator
        try:
            from empirica.core.canonical.canonical_goal_orchestrator import CanonicalGoalOrchestrator
            orchestrator = CanonicalGoalOrchestrator()

            goals_result = orchestrator.generate_goals(
                session_id=session_id,
                conversation_context=arguments.get('prompt', ''),
                epistemic_vectors=vectors
            )

            auto_goals = goals_result.get('goals', [])[:5]  # Top 5 goals
        except Exception as e:
            logger.warning(f"Goal generation failed: {e}")
            auto_goals = None

    # Add to response
    response['uncertainty_detected'] = uncertainty > 0.6
    response['uncertainty_score'] = uncertainty
    response['recommendation'] = recommendation
    if auto_goals:
        response['auto_generated_goals'] = auto_goals
        response['next_step'] = "Follow investigation goals, then call execute_check()"
    else:
        response['next_step'] = "Proceed to ACT phase (low uncertainty)"

    return response
```

**Threshold Logic:**
- uncertainty > 0.6 → investigate
- OR know < 0.7 → investigate
- OR state < 0.6 → investigate

**Testing:**
- Low uncertainty (0.3) → no goals generated
- High uncertainty (0.7) → goals generated
- Low KNOW (0.5) → goals generated

---

## Improvement 3: Session Alias Support Across All MCP Tools

### Problem
Only 4 MCP tools support session aliases. The remaining 35 tools require full UUIDs.

### Current State
**With alias support (4 tools):**
- ✅ load_git_checkpoint
- ✅ get_epistemic_state
- ✅ get_calibration_report
- ✅ get_session_summary

**Without alias support (35 tools):**
- ❌ create_git_checkpoint
- ❌ execute_preflight
- ❌ submit_preflight_assessment
- ❌ execute_check
- ❌ submit_check_assessment
- ❌ execute_postflight
- ❌ submit_postflight_assessment
- ❌ query_bayesian_beliefs
- ❌ check_drift_monitor
- ❌ generate_goals
- ❌ create_cascade
- ❌ ... (25+ more)

### Proposed Behavior
**All 39 MCP tools accept session aliases consistently**

```python
# Any tool accepting session_id parameter:
tool_name(session_id="latest:active:claude-code")  # Works
tool_name(session_id="88dbf132")  # Works (partial UUID)
tool_name(session_id="88dbf132-cc7c-4a4b-9b59-77df3b13dbd2")  # Works (full UUID)
```

### Implementation Details

**File:** `mcp_local/empirica_mcp_server.py`

**Strategy:** Add resolver to EVERY tool handler that accepts session_id

**Pattern (already implemented for 4 tools):**
```python
elif name == "some_tool":
    try:
        session_id_or_alias = arguments.get("session_id")

        # Resolve session alias to UUID
        try:
            session_id = resolve_session_id(session_id_or_alias)
        except ValueError as e:
            return [types.TextContent(type="text", text=json.dumps({
                "ok": False,
                "error": f"Session resolution failed: {str(e)}",
                "provided": session_id_or_alias
            }, indent=2))]

        # Rest of tool logic uses session_id (UUID)
        ...
```

**Tools to Update (35 remaining):**

1. Workflow tools (7):
   - execute_preflight
   - submit_preflight_assessment
   - execute_check
   - submit_check_assessment
   - execute_postflight
   - submit_postflight_assessment
   - create_cascade

2. Checkpoint tools (5):
   - create_git_checkpoint
   - get_vector_diff
   - measure_token_efficiency
   - generate_efficiency_report
   - checkpoint_create (via CLI)

3. Goal/tracking tools (5):
   - generate_goals
   - query_goal_orchestrator
   - create_goal
   - add_subtask
   - get_goal_progress

4. Monitoring tools (3):
   - query_bayesian_beliefs
   - check_drift_monitor
   - query_handoff_reports

5. Other tools (15):
   - resume_previous_session
   - generate_handoff_report
   - bootstrap_session (uses ai_id, not session_id - skip)
   - execute_cli_command (generic wrapper - skip)
   - ... (check full list)

**Update Tool Schemas:**
For each updated tool, modify the inputSchema description:
```python
"session_id": {
    "type": "string",
    "description": "Session UUID or alias ('latest', 'latest:active', 'latest:<ai_id>', 'latest:active:<ai_id>')"
}
```

**Testing:**
- Test each tool with UUID → works
- Test each tool with partial UUID → works
- Test each tool with alias → works
- Test with invalid alias → clear error message

---

## Improvement 4: Graceful Degradation for Storage Failures

### Problem
If git checkpoints fail (git not available, permissions issue), the operation fails completely. No fallback.

### Current Behavior
```python
create_git_checkpoint(...)
# If git fails: Error, checkpoint lost
```

### Proposed Behavior
```python
result = create_git_checkpoint(...)

# If git fails, auto-fallback to SQLite:
{
  "ok": true,
  "checkpoint_id": "checkpoint_abc123",
  "storage": "sqlite_fallback",
  "warning": "Git notes unavailable, using database storage",
  "degraded_mode": true,
  "token_count": 65,
  "note": "Checkpoint saved but won't persist across git operations"
}
```

### Implementation Details

**File:** `empirica/core/canonical/git_enhanced_reflex_logger.py`

**Function:** `create_checkpoint()` method

**Changes:**
```python
def create_checkpoint(self, phase, round_num, vectors, metadata=None):
    """Create checkpoint with automatic fallback"""

    # Try git notes first
    if self.git_available:
        try:
            checkpoint_id = self._create_git_checkpoint(phase, round_num, vectors, metadata)
            return {
                "checkpoint_id": checkpoint_id,
                "storage": "git_notes",
                "degraded_mode": False
            }
        except Exception as e:
            logger.warning(f"Git checkpoint failed: {e}, falling back to SQLite")
            # Fall through to SQLite

    # Fallback to SQLite
    try:
        checkpoint_id = self._create_sqlite_checkpoint(phase, round_num, vectors, metadata)
        return {
            "checkpoint_id": checkpoint_id,
            "storage": "sqlite_fallback",
            "degraded_mode": True,
            "warning": "Git unavailable, using database storage"
        }
    except Exception as e:
        logger.error(f"SQLite checkpoint failed: {e}, falling back to JSON")
        # Final fallback to JSON file

    # Last resort: JSON file
    checkpoint_id = self._create_json_checkpoint(phase, round_num, vectors, metadata)
    return {
        "checkpoint_id": checkpoint_id,
        "storage": "json_file_fallback",
        "degraded_mode": True,
        "warning": "Both git and database unavailable, using JSON file"
    }
```

**Fallback Hierarchy:**
1. **Git notes** (preferred) - 97.5% token reduction, travels with repo
2. **SQLite** (fallback 1) - Still compressed, local database
3. **JSON file** (fallback 2) - Plain text, `.empirica_fallback/` directory

**Testing:**
- Git available → uses git notes
- Git unavailable → uses SQLite
- SQLite unavailable → uses JSON file
- All unavailable → clear error with recovery steps

---

## Improvement 5: Actionable Error Messages

### Problem
Current error messages don't tell agents what to do next.

### Current Examples
```python
{"ok": false, "error": "No session found"}
{"ok": false, "error": "ValueError: Invalid session_id"}
{"ok": false, "error": "Git not available"}
```

### Proposed Format
```python
{
  "ok": false,
  "error": "No session found for alias: latest:active:claude-code",
  "reason": "No active sessions in database for ai_id='claude-code'",
  "suggestion": "Call bootstrap_session(ai_id='claude-code') to start new session",
  "alternatives": [
    "Use 'latest' (any AI) instead of 'latest:active:claude-code'",
    "Check if you have ended all sessions: sessions-list"
  ],
  "recovery_commands": [
    "bootstrap_session(ai_id='claude-code', session_type='development')"
  ]
}
```

### Implementation Pattern

**File:** `mcp_local/empirica_mcp_server.py`

**Apply to all error responses:**
```python
def create_error_response(error_msg, context=None):
    """Create actionable error response"""
    response = {
        "ok": False,
        "error": error_msg
    }

    # Add context-specific suggestions
    if "No session found" in error_msg:
        response["suggestion"] = "Call bootstrap_session() to start new session"
        response["recovery_commands"] = [
            "bootstrap_session(ai_id='claude-code', session_type='development')"
        ]

    elif "Session resolution failed" in error_msg:
        response["suggestion"] = "Check session alias format or use sessions-list to find UUID"
        response["alternatives"] = [
            "Use 'latest' for most recent session",
            "Use 'latest:active' for active sessions only",
            "Use full UUID if alias doesn't work"
        ]

    elif "Git not available" in error_msg:
        response["suggestion"] = "Checkpoint saved to database fallback"
        response["note"] = "This is expected if git is not installed, checkpoint still works"

    # Add context if provided
    if context:
        response.update(context)

    return response
```

**Error Categories:**
1. **Session not found** → Suggest bootstrap_session()
2. **Invalid alias** → Show alias format examples
3. **Component unavailable** → Explain fallback used
4. **Invalid input** → Show correct format/example
5. **Permission denied** → Suggest permission fix commands

**Testing:**
- Trigger each error type
- Verify suggestion is actionable
- Verify recovery commands work

---

## Improvement 6: Clearer Decision Criteria in System Prompts

### Problem
Current guidance is vague: "Complex tasks (>1 hour)" vs "Trivial tasks (<10 min)"

### Current (CLAUDE.md, line 399)
```markdown
### Always Use For:
- ✅ Complex tasks (>1 hour of work)
- ✅ Multi-session tasks

### Optional For:
- ⚠️ Trivial tasks (<10 min, fully known)
```

### Proposed Replacement
```markdown
### Use Empirica When:

**Rule of thumb: If UNCERTAINTY > 0.6, use Empirica**

#### Definite YES (Always use):
- ✅ Task requires investigation (you don't know the architecture/domain)
  - Example: "Refactor authentication system" (unknown codebase structure)
  - Example: "Debug intermittent test failure" (unknown root cause)

- ✅ Task will span multiple conversation sessions
  - Example: Multi-day feature implementation
  - Example: Large refactoring broken into phases

- ✅ Task has high stakes (consequences of errors are severe)
  - Example: Production deployment scripts
  - Example: Security-critical code
  - Example: Data migration scripts

- ✅ Task requires collaboration with other AIs
  - Example: Minimax does testing, you do implementation
  - Example: Handoff to Rovo Dev for specialized task

#### Definite NO (Skip Empirica):
- ❌ Simple information retrieval with high confidence
  - Example: "What's the syntax for Python list comprehension?"
  - Example: "Show me the git command to undo last commit"

- ❌ Single file edit with known, straightforward solution
  - Example: "Fix typo in README.md line 42"
  - Example: "Add import statement to file.py"

- ❌ Running a single command with no uncertainty
  - Example: "Run npm install"
  - Example: "Show git status"

#### Decision Matrix:

| Your State | Task Complexity | Use Empirica? |
|------------|----------------|---------------|
| UNCERTAINTY > 0.6 | Any | ✅ YES |
| KNOW < 0.7 | Any | ✅ YES |
| High stakes | Any | ✅ YES |
| Multi-session | Any | ✅ YES |
| UNCERTAINTY < 0.3 AND KNOW > 0.8 | <30 min | ❌ NO (optional) |
| UNCERTAINTY < 0.3 AND KNOW > 0.8 | >30 min | ⚠️ OPTIONAL |

#### Quick Self-Check:
1. **Do I know how to do this?** (KNOW score)
   - <0.7 → Use Empirica

2. **Am I uncertain about the approach?** (UNCERTAINTY score)
   - >0.6 → Use Empirica

3. **What happens if I'm wrong?**
   - Bad consequences → Use Empirica

4. **Will this take multiple sessions?**
   - Yes → Use Empirica

When in doubt, use Empirica. The 10-minute overhead prevents hours of debugging.
```

### Implementation

**Files to Update:**
1. `CLAUDE.md` (lines 399-414)
2. `MINIMAX.md` (same section)
3. `QWEN.md` (same section)
4. `GEMINI.md` (same section)
5. `ROVODEV.md` (same section)
6. `COPILOT_CLAUDE.md` (same section)
7. `.github/copilot-instructions.md` (same section)

**Changes:**
- Replace "WHEN TO USE EMPIRICA" section
- Add decision matrix
- Add concrete examples
- Add quick self-check questions

---

## Success Metrics

### Reliability Target: 95%+

**Measure by task type:**

| Task Type | Current | Target | How to Measure |
|-----------|---------|--------|----------------|
| Complex tasks (>1 hour) | 85% | 95% | AI completes without errors, user validates |
| Multi-session tasks | 90% | 98% | Session resumption works via aliases |
| High-stakes tasks | 80% | 95% | No production incidents from Empirica usage |
| First-time use | 50% | 80% | AI follows workflow without confusion |
| Error recovery | 40% | 90% | AI recovers from failures using suggestions |

### Definition of "Works"
1. AI agent follows PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT
2. No manual intervention needed (automatic drift detection, goal generation)
3. Session aliases work across all tools
4. Errors have actionable recovery steps
5. Calibration report shows "well_calibrated"

### Testing Plan

**Phase 1: Unit Tests (each improvement)**
- Drift detection with various patterns
- Goal generation with different uncertainty levels
- Session alias resolution for all tools
- Fallback storage (git → SQLite → JSON)
- Error message format validation

**Phase 2: Integration Tests (full workflow)**
- PREFLIGHT with high uncertainty → auto-generates goals
- CHECK with drift → blocks ACT phase
- Session resumption via aliases → loads correctly
- Git unavailable → falls back gracefully

**Phase 3: Real-World Dogfooding**
- Use Empirica for implementing these improvements
- Track calibration across sessions
- Measure time overhead vs. value gained
- Document failure modes encountered

---

## Implementation Plan

### Phase 1: Core Reliability (High Priority)
**Target: 2-3 hours of work**

1. **Auto-drift detection in CHECK** (45 min)
   - Modify execute_check handler
   - Add severity analysis
   - Block ACT if severe drift
   - Test with sample data

2. **Session aliases everywhere** (60 min)
   - Add resolver to remaining 35 tools
   - Update tool schemas
   - Test representative sample (10 tools)
   - Document pattern for remaining tools

3. **Auto-goal generation from PREFLIGHT** (45 min)
   - Modify submit_preflight_assessment handler
   - Call goal orchestrator if uncertainty > 0.6
   - Return goals in response
   - Test with low/high uncertainty

### Phase 2: Resilience (Medium Priority)
**Target: 1-2 hours of work**

4. **Graceful degradation** (60 min)
   - Implement git → SQLite → JSON fallback
   - Add to create_git_checkpoint
   - Test failure modes
   - Document degraded mode behavior

5. **Actionable error messages** (30 min)
   - Create error response helper
   - Apply to common error points
   - Test each error category
   - Verify suggestions are accurate

### Phase 3: Documentation (Low Priority)
**Target: 30-45 minutes**

6. **Update system prompts** (30 min)
   - Replace decision criteria section
   - Add decision matrix
   - Add concrete examples
   - Update all 7 AI prompt files

---

## Task Breakdown for Multi-Agent Work

### Task 1: Auto-Drift Detection (Rovo Dev)
**Estimated:** 45-60 minutes
**Files:** `mcp_local/empirica_mcp_server.py`
**Description:** Integrate drift monitor into execute_check handler

**Subtasks:**
1. Modify execute_check handler to auto-call drift monitor
2. Add severity analysis (minor/moderate/severe)
3. Return drift results in CHECK response
4. Set safe_to_proceed flag based on severity
5. Test with stable/moderate/severe drift scenarios

**Success Criteria:**
- CHECK returns drift_analysis in response
- Severe drift sets safe_to_proceed: false
- Tests pass for all severity levels

---

### Task 2: Session Aliases Everywhere (Claude Code)
**Estimated:** 60-90 minutes
**Files:** `mcp_local/empirica_mcp_server.py`
**Description:** Add session alias support to remaining 35 MCP tools

**Subtasks:**
1. Audit all 39 tools, identify which lack alias support (35 remaining)
2. Add resolve_session_id() pattern to each tool handler
3. Update tool schemas to document alias support
4. Test representative sample (10 tools minimum)
5. Document pattern for any remaining tools

**Success Criteria:**
- All MCP tools accept "latest:active:<ai_id>" format
- Tool schemas document alias support
- Tests pass for UUID, partial UUID, and alias inputs

---

### Task 3: Auto-Goal Generation (Mini-agent)
**Estimated:** 45-60 minutes
**Files:** `mcp_local/empirica_mcp_server.py`
**Description:** Modify PREFLIGHT to auto-generate investigation goals

**Subtasks:**
1. Modify submit_preflight_assessment handler
2. Calculate uncertainty threshold (>0.6 or KNOW <0.7)
3. Call goal orchestrator if threshold met
4. Return generated goals in PREFLIGHT response
5. Test with low/high uncertainty vectors

**Success Criteria:**
- PREFLIGHT returns auto_generated_goals when uncertainty > 0.6
- Goals are relevant to epistemic gaps (KNOW, STATE, etc.)
- Low uncertainty doesn't trigger goal generation

---

### Task 4: Graceful Degradation (Claude Code)
**Estimated:** 60-75 minutes
**Files:** `empirica/core/canonical/git_enhanced_reflex_logger.py`
**Description:** Implement fallback hierarchy for checkpoint storage

**Subtasks:**
1. Create _create_sqlite_checkpoint() method
2. Create _create_json_checkpoint() method
3. Modify create_checkpoint() to try git → SQLite → JSON
4. Test git unavailable scenario
5. Test SQLite unavailable scenario
6. Document degraded mode behavior

**Success Criteria:**
- Git failure → SQLite fallback (with warning)
- SQLite failure → JSON fallback (with warning)
- All modes save checkpoint successfully

---

### Task 5: Actionable Error Messages (Rovo Dev)
**Estimated:** 30-45 minutes
**Files:** `mcp_local/empirica_mcp_server.py`
**Description:** Add actionable suggestions to all error responses

**Subtasks:**
1. Create create_error_response() helper function
2. Define suggestion templates for common errors
3. Apply to 5 most common error points
4. Test each error category
5. Verify recovery commands are accurate

**Success Criteria:**
- Errors include "suggestion" field
- Errors include "recovery_commands" where applicable
- Suggestions are actionable and accurate

---

### Task 6: Update System Prompts (Mini-agent)
**Estimated:** 30-40 minutes
**Files:** All 7 AI prompt files
**Description:** Replace decision criteria with clearer guidance

**Subtasks:**
1. Update CLAUDE.md "WHEN TO USE EMPIRICA" section
2. Copy to MINIMAX.md, QWEN.md, GEMINI.md
3. Copy to ROVODEV.md, COPILOT_CLAUDE.md
4. Update .github/copilot-instructions.md
5. Verify formatting and examples

**Success Criteria:**
- All 7 files have updated decision criteria
- Decision matrix included
- Concrete examples provided

---

## Notes for Multi-Agent Coordination

### Using Empirica to Dogfood Itself

**Session Setup:**
1. Each agent bootstraps with their ai_id (claude-code, rovodev, mini-agent)
2. Use session aliases for coordination: `latest:active:rovodev`
3. Create checkpoints at task boundaries
4. Generate handoff reports when passing work

**Coordination Pattern:**
```python
# Claude Code completes Task 2
create_git_checkpoint(
    session_id=session_id,
    phase="ACT",
    round_num=1,
    vectors={...},
    metadata={"task": "session_aliases", "status": "complete", "next_agent": "rovodev"}
)

generate_handoff_report(
    session_id=session_id,
    task_summary="Added session alias support to 35 MCP tools",
    key_findings=["All tools now support latest:active:ai_id format"],
    remaining_unknowns=[],
    next_session_context="Rovo Dev: proceed with Task 1 (drift detection)",
    artifacts_created=["mcp_local/empirica_mcp_server.py"]
)
```

**Expected Outcome:**
- Measure our own calibration while implementing
- Validate that the improvements actually help
- Document any friction points discovered
- Prove Empirica works at scale

---

## Appendix A: Complete Tool Audit

**Tools WITH session alias support (4):**
1. load_git_checkpoint ✅
2. get_epistemic_state ✅
3. get_calibration_report ✅
4. get_session_summary ✅

**Tools NEEDING session alias support (35):**

*Workflow (7):*
5. execute_preflight
6. submit_preflight_assessment
7. execute_check
8. submit_check_assessment
9. execute_postflight
10. submit_postflight_assessment
11. create_cascade

*Checkpoints (4):*
12. create_git_checkpoint
13. get_vector_diff
14. measure_token_efficiency
15. generate_efficiency_report

*Goals (6):*
16. generate_goals
17. query_goal_orchestrator
18. create_goal
19. add_subtask
20. complete_subtask
21. get_goal_progress

*Monitoring (4):*
22. query_bayesian_beliefs
23. check_drift_monitor
24. query_handoff_reports
25. generate_handoff_report

*Session queries (1):*
26. resume_previous_session

*Other (13):*
27-39. (Various specialized tools)

---

## Appendix B: Testing Checklist

### Drift Detection
- [ ] Stable assessments (no drift) → proceed
- [ ] Minor drift (<0.15 delta) → warning
- [ ] Moderate drift (0.15-0.30) → recommend recalibrate
- [ ] Severe drift (>0.30) → block ACT

### Goal Generation
- [ ] Low uncertainty (0.3) → no goals
- [ ] High uncertainty (0.7) → goals generated
- [ ] Low KNOW (0.5) → goals generated
- [ ] Goals relevant to epistemic gaps

### Session Aliases
- [ ] Full UUID works
- [ ] Partial UUID (8 chars) works
- [ ] "latest" works
- [ ] "latest:active" works
- [ ] "latest:ai_id" works
- [ ] "latest:active:ai_id" works
- [ ] Invalid alias → clear error

### Graceful Degradation
- [ ] Git available → git notes
- [ ] Git unavailable → SQLite
- [ ] SQLite unavailable → JSON
- [ ] Each fallback includes warning

### Error Messages
- [ ] "No session found" → suggests bootstrap
- [ ] "Invalid alias" → shows format
- [ ] "Git unavailable" → explains fallback
- [ ] All errors have suggestions

### System Prompts
- [ ] All 7 files updated
- [ ] Decision matrix included
- [ ] Examples are concrete
- [ ] Formatting correct

---

## Version History

**v1.0 (2025-11-18)**
- Initial specification
- 6 improvements defined
- Task breakdown for multi-agent work
- Ready for implementation
