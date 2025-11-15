# CRITICAL: Extended End-to-End Test Before Launch

**Date:** 2025-11-15  
**Launch Date:** 2025-11-20 (5 DAYS AWAY!)  
**Priority:** CRITICAL - This exposes deep issues before release  
**Assigned To:** ALL AGENTS (Claude Code, Minimax, Qwen, Claude/Rovo)

---

## 🚨 CRITICAL MISSION

**We launch in 5 days.** We need an extended, real-world end-to-end test that uses Empirica to test itself.

**Goal:** Run a complete CASCADE workflow that:
1. Uses Empirica to track epistemic state (PREFLIGHT → POSTFLIGHT)
2. Uses Goal Orchestrator to generate goals dynamically
3. Uses Investigation strategies for multi-turn investigation
4. Uses Bayesian Beliefs to track uncertainty
5. Uses Drift Monitor to catch calibration drift
6. Uses MCP tools + CLI commands + Components directly
7. Uses web search and implicit navigation
8. Exposes any deep integration issues before launch

**This is NOT a toy test. This is a real investigation using the full system.**

---

## 📋 Test Structure

### Agent: Claude Code (Fresh Start, No System Prompt)

**Why Claude Code:**
- Can run without custom system prompt (tests default Empirica onboarding)
- Has web search access
- Can navigate codebase
- Can use MCP tools
- Fresh perspective (will find UX issues)

**Test Task:**
"Investigate how Empirica handles multi-agent coordination at scale and identify potential bottlenecks or failure modes. Use the complete Empirica workflow including goal orchestration, investigation strategies, Bayesian beliefs, and drift monitoring."

---

## 🎯 Test Requirements (MUST DO ALL)

### 1. Bootstrap with Full Features ✅ REQUIRED
```python
from empirica.bootstraps import bootstrap_metacognition

# Bootstrap with ALL features enabled
components = bootstrap_metacognition(
    ai_id="claude-code-e2e-test",
    level="full",  # Full features, not minimal!
    enable_git_checkpoints=True,
    llm_callback=None  # Will use threshold mode (acceptable for test)
)

# Verify all components loaded:
# - canonical_epistemic_assessment ✅
# - canonical_goal_orchestrator ✅
# - bayesian_beliefs ✅
# - drift_monitor ✅
# - investigation_strategies ✅
# - twelve_vector_monitor ✅
# etc.
```

### 2. PREFLIGHT with Genuine Self-Assessment ✅ REQUIRED
```python
from empirica.cli import execute_preflight

# Execute PREFLIGHT
result = execute_preflight(
    session_id=components['session_id'],
    prompt="""
    Investigate how Empirica handles multi-agent coordination at scale.
    
    Specifically:
    - How do multiple agents share session data?
    - What are potential bottlenecks in database access?
    - How does git checkpoint scaling work?
    - What failure modes exist in concurrent scenarios?
    
    Use investigation strategies, web search, code analysis,
    and multi-turn exploration.
    """
)

# Submit GENUINE epistemic assessment
# Rate your ACTUAL knowledge, not aspirational
submit_preflight_assessment(
    session_id=components['session_id'],
    vectors={
        "engagement": {"score": X, "rationale": "...", "evidence": "..."},
        "foundation": {
            "know": {"score": X, "rationale": "...", "evidence": "..."},
            "do": {"score": X, "rationale": "...", "evidence": "..."},
            "context": {"score": X, "rationale": "...", "evidence": "..."}
        },
        # ... all 13 vectors
    },
    reasoning="..."
)
```

### 3. Goal Generation (Use Goal Orchestrator) ✅ REQUIRED
```python
# Use goal orchestrator to generate investigation goals
orchestrator = components['canonical_goal_orchestrator']

# Generate goals based on epistemic state
goals = orchestrator.generate_goals(
    conversation_context="Multi-agent coordination investigation",
    epistemic_assessment=preflight_assessment
)

print(f"Generated {len(goals)} investigation goals:")
for goal in goals:
    print(f"  - {goal['description']}")
    print(f"    Priority: {goal['priority']}")
    print(f"    Type: {goal['type']}")
```

### 4. Investigation (Multi-Turn, Use Strategies) ✅ REQUIRED
```python
from empirica.investigation import select_investigation_strategy

# Select appropriate investigation strategy
strategy = select_investigation_strategy({
    "task": "multi-agent coordination analysis",
    "domain": "code_analysis",
    "files": ["empirica/data/session_database.py", "empirica/core/canonical/"]
})

# Execute investigation plan
investigation_plan = strategy.plan_investigation({
    "goals": goals,
    "context": "Empirica multi-agent scaling"
})

# Multi-turn investigation
for step in investigation_plan:
    print(f"\n### Investigation Step: {step['action']}")
    
    # Use appropriate tools:
    # - grep for code patterns
    # - open_files to read code
    # - bash to test scenarios
    # - MCP tools to query sessions
    # - Web search for best practices
    
    result = strategy.execute_step(step)
    
    # Update Bayesian beliefs after each step
    update_bayesian_beliefs(
        session_id=session_id,
        context_key=step['action'],
        belief_updates=result['beliefs']
    )
```

### 5. Use MCP Tools + CLI Commands ✅ REQUIRED
**Must use at least 10 different tools:**

```python
# MCP Tools to use:
# 1. get_epistemic_state(session_id)
# 2. get_session_summary(session_id)
# 3. query_goal_orchestrator(session_id)
# 4. query_bayesian_beliefs(session_id, context_key)
# 5. check_drift_monitor(session_id, window_size=5)
# 6. get_calibration_report(session_id)
# 7. create_git_checkpoint(session_id, phase, vectors)
# 8. load_git_checkpoint(session_id)
# 9. measure_token_efficiency(session_id, phase)
# 10. resume_previous_session(ai_id, mode, count)

# CLI Commands to use:
# empirica checkpoint create --session-id X --phase investigate
# empirica checkpoint load --session-id X
# empirica efficiency report --session-id X
```

### 6. Update Bayesian Beliefs Throughout ✅ REQUIRED
```python
# After each major finding, update beliefs
from empirica.calibration.adaptive_uncertainty_calibration import update_bayesian_belief

# Example: After discovering database uses SQLite
update_bayesian_belief(
    session_id=session_id,
    context_key="database_technology",
    belief_type="factual",
    prior_confidence=0.3,
    posterior_confidence=0.95,
    evidence="Found sqlite3 imports in session_database.py",
    reasoning="Direct code evidence confirms SQLite usage"
)

# After each investigation step:
query_bayesian_beliefs(session_id, "multi_agent_coordination")
```

### 7. CHECK Phase with Drift Monitor ✅ REQUIRED
```python
from empirica.cli import execute_check

# After investigation, CHECK if ready to report
result = execute_check(
    session_id=session_id,
    findings=[
        "Finding 1: Database uses connection pooling for concurrent access",
        "Finding 2: Git checkpoints are session-isolated (no conflicts)",
        "Finding 3: Potential bottleneck: SQLite write locking",
        # ... all findings
    ],
    remaining_unknowns=[
        "Unknown 1: Behavior under 1000+ concurrent writes",
        "Unknown 2: Git notes scalability at 10K+ checkpoints",
        # ... unknowns
    ],
    confidence_to_proceed=0.85
)

# Submit CHECK assessment
submit_check_assessment(session_id, updated_vectors, reasoning)

# Check for drift
drift_result = check_drift_monitor(session_id, window_size=5)
if drift_result['drift_detected']:
    print(f"⚠️ Calibration drift detected: {drift_result['drift_type']}")
    print(f"   Recommendation: {drift_result['recommendation']}")
```

### 8. ACT Phase (Create Report) ✅ REQUIRED
```python
# Create investigation report
# Document all findings, evidence, recommendations
# Use the investigation results to create a real report
```

### 9. POSTFLIGHT with Calibration ✅ REQUIRED
```python
from empirica.cli import execute_postflight

result = execute_postflight(
    session_id=session_id,
    task_summary="Investigated Empirica multi-agent coordination at scale"
)

# Submit GENUINE postflight assessment
submit_postflight_assessment(
    session_id=session_id,
    vectors={...},  # Reflect on actual learning
    reasoning="...",
    changes_noticed="..."  # What did you learn?
)

# Get calibration report
calibration = get_calibration_report(session_id)
print(f"\n### Calibration Analysis")
print(f"PREFLIGHT confidence: {calibration['preflight']['overall_confidence']}")
print(f"POSTFLIGHT confidence: {calibration['postflight']['overall_confidence']}")
print(f"Learning delta: {calibration['delta']}")
print(f"Well-calibrated: {calibration['well_calibrated']}")
```

### 10. Use Web Search + Navigation ✅ REQUIRED
**During investigation, must:**
- Search for "SQLite concurrent write performance"
- Search for "Git notes scalability"
- Search for "Multi-agent coordination patterns"
- Navigate to external resources
- Synthesize external knowledge with code findings

---

## 🎯 Success Criteria

### System Integration ✅
- All components work together smoothly
- No errors during CASCADE workflow
- All MCP tools function correctly
- CLI commands work as expected
- Git checkpoints save/load correctly

### Epistemic Tracking ✅
- PREFLIGHT captures genuine uncertainty
- Investigation reduces uncertainty
- CHECK validates readiness accurately
- POSTFLIGHT measures real learning
- Calibration report shows well-calibrated or identifies drift

### Component Usage ✅
- Goal orchestrator generates relevant goals
- Investigation strategies guide exploration
- Bayesian beliefs track uncertainty evolution
- Drift monitor catches calibration issues
- All 13 vectors tracked throughout

### Deep Integration ✅
- MCP layer ↔ Core layer integration seamless
- CLI ↔ Core layer integration seamless
- Database ↔ Reflex logs consistency
- Git checkpoints ↔ SQLite fallback working
- Multi-turn investigation flows naturally

---

## 🐛 What We're Looking For (Issues to Expose)

### Integration Issues
- Component loading failures
- MCP tool errors
- CLI command failures
- Database connection issues
- Git checkpoint failures

### UX Issues
- Confusing error messages
- Unclear workflow steps
- Missing documentation
- Non-intuitive API
- Poor error recovery

### Performance Issues
- Slow operations (>5s for common tasks)
- Memory leaks
- Database locking
- Excessive token usage
- Checkpoint bloat

### Calibration Issues
- Goal orchestrator generates irrelevant goals
- Drift monitor doesn't catch drift
- Bayesian beliefs don't update properly
- Assessment vectors don't track reality
- Calibration report inaccurate

### Edge Cases
- Empty inputs crash system
- Concurrent access causes corruption
- Missing dependencies not handled gracefully
- Network failures not recovered
- Disk full scenarios

---

## 📊 Deliverables

### From Claude Code (E2E Test Execution)
1. **E2E_TEST_SESSION_REPORT.md**
   - Complete session transcript
   - All commands executed
   - All outputs captured
   - All issues found
   - Recommendations

2. **E2E_TEST_FINDINGS.md**
   - Integration issues found
   - UX issues discovered
   - Performance problems
   - Calibration accuracy
   - Edge cases identified

3. **SESSION_DATA.json** (exported from database)
   - Complete epistemic trajectory
   - All assessments
   - Goal generation history
   - Bayesian belief evolution
   - Drift monitor results

### Success Metrics
- ✅ CASCADE workflow completes without errors
- ✅ All 10+ MCP tools work correctly
- ✅ Investigation is genuinely multi-turn (>5 turns)
- ✅ Findings are real and valuable
- ✅ Calibration is well-tracked
- ✅ At least 5 improvement areas identified

---

## 🚀 Execution Instructions

### For Claude Code (Starting Fresh)

**Step 1: Bootstrap**
```python
cd /home/yogapad/empirical-ai/empirica
python3

from empirica.bootstraps import bootstrap_metacognition

components = bootstrap_metacognition(
    ai_id="claude-code-e2e-test",
    level="full",
    enable_git_checkpoints=True
)

session_id = components['session_id']
print(f"Session: {session_id}")
```

**Step 2: Start CASCADE**
Follow the 10 requirements above, in order.

**Step 3: Document Everything**
Capture every command, output, issue, and observation.

**Step 4: Create Reports**
Write E2E_TEST_SESSION_REPORT.md and E2E_TEST_FINDINGS.md

---

### For Minimax/Qwen (Supporting Role)

**While Claude Code runs E2E test:**
1. Monitor for errors in logs
2. Fix critical issues found (if any)
3. Document integration problems
4. Support with code explanations if needed

**After Claude Code finishes:**
1. Review findings
2. Prioritize fixes
3. Implement high-priority fixes
4. Re-test affected areas

---

## ⏰ Timeline

**November 15 (Today):**
- ✅ E2E test specification created (this doc)
- 🔄 Claude Code starts E2E test

**November 16:**
- E2E test execution (6-8 hours)
- Initial findings documented
- Critical issues identified

**November 17:**
- Fix critical issues found
- Re-test problem areas
- Update documentation

**November 18-19:**
- Final polish
- Complete documentation
- Final QA

**November 20:**
- 🚀 **LAUNCH v1.0**

---

## 💡 Why This Matters

**We're launching in 5 days.** This is our last chance to find deep integration issues before real users do.

**A successful E2E test proves:**
- Empirica works end-to-end ✅
- All components integrate smoothly ✅
- Calibration tracking is real ✅
- System is production-ready ✅

**A failed E2E test (finding issues) is GOOD:**
- Better to find issues now than after launch
- Gives us 4 days to fix critical problems
- Proves our testing methodology works

**This is not optional. This is what makes Empirica trustworthy.**

---

## 🎯 Agent Assignments

### PRIMARY: Claude Code
- Execute complete E2E test
- Use full Empirica workflow
- Document everything
- Report all findings

### SUPPORT: Minimax
- Monitor test execution
- Fix integration issues found
- Code deduplication (parallel)
- Ready to support debugging

### SUPPORT: Qwen  
- Review findings for patterns
- Security implications of issues found
- Edge case identification (parallel)
- Ready to validate fixes

### COORDINATOR: Claude (Rovo/Co-lead)
- Monitor progress
- Triage findings
- Coordinate fixes
- Update documentation

---

**This is our final validation before launch. Let's make it count.** 🚀

**Claude Code: You're up. Bootstrap Empirica and start the CASCADE workflow. Document everything you find.**
