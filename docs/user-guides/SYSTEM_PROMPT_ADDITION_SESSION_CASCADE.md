# System Prompt Addition: Session vs Cascade Clarity

**Problem Solved:** AI agents think they should only do PREFLIGHT once per session, leading them to skip it for subsequent tasks.

**Root Cause:** System prompts don't clearly explain that sessions contain multiple cascades, and each cascade (task) needs its own PREFLIGHT-POSTFLIGHT cycle.

---

## Add This Section to System Prompts

### For ROVODEV.md, CLAUDE.md, QWEN.md, GEMINI.md, etc.

Insert this section after the "Quick Start" and before detailed workflow instructions:

---

## 🔄 Session vs Cascade - CRITICAL UNDERSTANDING

### The Architecture

```
SESSION (hours/days)
  └── CASCADE 1 (Task A): PREFLIGHT → work → POSTFLIGHT
  └── CASCADE 2 (Task B): PREFLIGHT → work → POSTFLIGHT  
  └── CASCADE 3 (Task C): PREFLIGHT → work → POSTFLIGHT
```

**Key Point:** Each task gets its own complete epistemic cycle.

### What This Means

✅ **DO:** Run PREFLIGHT for every new task  
✅ **DO:** Run POSTFLIGHT after completing each task  
✅ **DO:** Improve your PREFLIGHT scores across tasks (shows learning)  

❌ **DON'T:** Skip PREFLIGHT thinking "I already did it for this session"  
❌ **DON'T:** Use the same scores for every task  
❌ **DON'T:** Think one PREFLIGHT covers the entire session  

### Example Session with 3 Tasks

```python
# Bootstrap session ONCE
session_id = bootstrap_session(ai_id="your_id", ...)["session_id"]

# ===== TASK 1: Implement drift detection =====
execute_preflight(session_id, prompt="Add drift detection")
# Honest assessment: KNOW=0.5, UNCERTAINTY=0.7
# ... do the work ...
execute_postflight(session_id, task_summary="Drift detection complete")
# After learning: KNOW=0.85, UNCERTAINTY=0.3

# ===== TASK 2: Add error helper (NEW TASK!) =====
execute_preflight(session_id, prompt="Add error response helper")
# ⚡ Notice: KNOW=0.75 (higher!) because you learned from Task 1
# ... do the work ...
execute_postflight(session_id, task_summary="Error helper complete")
# KNOW=0.88, UNCERTAINTY=0.25

# ===== TASK 3: Fix tests (ANOTHER NEW TASK!) =====
execute_preflight(session_id, prompt="Fix test imports")
# ⚡ Notice: KNOW=0.8 (even higher!) - compounding learning
# ... do the work ...
execute_postflight(session_id, task_summary="All tests passing")
# KNOW=0.9, UNCERTAINTY=0.2
```

**What This Proves:** Genuine learning trajectory from 0.5 → 0.9 across tasks!

### Why This Matters

1. **Calibration:** Each task's PREFLIGHT-POSTFLIGHT pair measures learning for THAT task
2. **Evidence:** Multiple cycles prove you're genuinely learning, not pattern-matching
3. **Accuracy:** Task-specific assessment is more honest than session-wide guessing
4. **Trust:** Shows stakeholders that confidence improvements are real

### Quick Decision Guide

**New task from user?** → Run PREFLIGHT  
**Finished a task?** → Run POSTFLIGHT  
**Same task, investigating?** → Continue cascade (don't restart)  
**Taking a break/ending work?** → Session naturally pauses (resume later)

### Red Flags

🚩 "I already did PREFLIGHT for this session" → NO! Each task needs PREFLIGHT  
🚩 Same KNOW score across 3 tasks → Not honest assessment  
🚩 PREFLIGHT score decreases across tasks → Probably copy-paste error  
🚩 No POSTFLIGHT after completing task → Missing calibration data

---

## Integration Points

### Update Existing Sections

#### In "Workflow Overview" Section
Add callout:
```
⚠️ IMPORTANT: Each task gets its own PREFLIGHT → work → POSTFLIGHT cycle.
Don't skip PREFLIGHT thinking you "already did it" for the session!
```

#### In "PREFLIGHT" Section
Add:
```
**Frequency:** Run PREFLIGHT for EVERY new task, even within the same session.

Why? Each task is a separate cascade with its own epistemic cycle.
Your PREFLIGHT scores should IMPROVE across tasks as you learn!

Example:
- Task 1 PREFLIGHT: KNOW=0.5 (baseline)
- Task 2 PREFLIGHT: KNOW=0.75 (learned from Task 1!)
- Task 3 PREFLIGHT: KNOW=0.85 (compound learning!)
```

#### In "POSTFLIGHT" Section
Add:
```
**Frequency:** Run POSTFLIGHT after EVERY completed task.

This creates the calibration data (PREFLIGHT vs POSTFLIGHT) that proves
your confidence assessments are accurate.

Don't skip it thinking "I'll do one POSTFLIGHT at the end of the session."
Each task needs its own completion assessment!
```

#### In "Available Tools" Section
Clarify:
```
**Session-Level Tools (use once per session):**
- bootstrap_session
- get_session_summary
- resume_previous_session

**Cascade-Level Tools (use once per TASK):**
- execute_preflight  ← Run for EVERY task!
- submit_preflight_assessment
- execute_check
- submit_check_assessment
- execute_postflight  ← Run after EVERY task!
- submit_postflight_assessment
```

---

## Example: Annotated Session

```python
# ========================================
# SESSION START (Do this ONCE)
# ========================================
session_id = bootstrap_session(
    ai_id="rovodev",
    session_type="development",
    bootstrap_level=2
)["session_id"]

# ========================================
# CASCADE 1: Task "Implement drift detection"
# ========================================

# PREFLIGHT for THIS task (baseline assessment)
execute_preflight(
    session_id=session_id,
    prompt="Implement automatic drift detection in CHECK phase"
)

# Honest self-assessment for drift detection task
submit_preflight_assessment(
    session_id=session_id,
    vectors={
        "foundation": {
            "know": {"score": 0.6},  # I know what drift is
            "do": {"score": 0.7},     # I can write the code
            "context": {"score": 0.5}  # Need to understand CHECK phase
        },
        "uncertainty": {"score": 0.7}  # Several unknowns
    },
    reasoning="I understand drift concepts but need to investigate CHECK phase integration"
)

# ... DO THE WORK (INVESTIGATE, CHECK, ACT) ...

# POSTFLIGHT for THIS task (measure learning)
execute_postflight(
    session_id=session_id,
    task_summary="Implemented 3-tier drift detection with ACT blocking"
)

submit_postflight_assessment(
    session_id=session_id,
    vectors={
        "foundation": {
            "know": {"score": 0.85},  # Learned CHECK phase structure
            "do": {"score": 0.9},      # Implemented successfully
            "context": {"score": 0.8}   # Understand integration now
        },
        "uncertainty": {"score": 0.25}  # Most unknowns resolved
    },
    changes_noticed="Learned CHECK phase structure, drift monitor API, severity classification"
)

# ========================================
# CASCADE 2: Task "Add error response helper"
# THIS IS A NEW TASK - RUN PREFLIGHT AGAIN!
# ========================================

# PREFLIGHT for THIS new task
execute_preflight(
    session_id=session_id,  # SAME session, NEW cascade
    prompt="Create structured error response helper function"
)

# Assessment for error helper task
submit_preflight_assessment(
    session_id=session_id,
    vectors={
        "foundation": {
            "know": {"score": 0.75},  # Higher! Learned from Task 1
            "do": {"score": 0.8},      # More confident in codebase
            "context": {"score": 0.7}   # Better codebase understanding
        },
        "uncertainty": {"score": 0.5}  # Lower uncertainty
    },
    reasoning="More familiar with codebase structure from Task 1, confident I can add helper"
)

# ... DO THE WORK ...

execute_postflight(
    session_id=session_id,
    task_summary="Created error helper with 5 error types, applied to 6 locations"
)

submit_postflight_assessment(
    session_id=session_id,
    vectors={
        "foundation": {
            "know": {"score": 0.88},
            "do": {"score": 0.9},
            "context": {"score": 0.85}
        },
        "uncertainty": {"score": 0.2}
    },
    changes_noticed="Learned error pattern throughout codebase, helper pattern design"
)

# ========================================
# CASCADE 3: Task "Fix test mocks"
# ANOTHER NEW TASK - PREFLIGHT AGAIN!
# ========================================

execute_preflight(
    session_id=session_id,  # SAME session, ANOTHER new cascade
    prompt="Fix test mock import issues"
)

submit_preflight_assessment(
    session_id=session_id,
    vectors={
        "foundation": {
            "know": {"score": 0.8},   # Even higher!
            "do": {"score": 0.85},     # Strong confidence
            "context": {"score": 0.8}   # Solid understanding
        },
        "uncertainty": {"score": 0.4}  # Manageable unknowns
    },
    reasoning="Familiar with test structure and mock patterns from previous work"
)

# ... DO THE WORK ...

execute_postflight(
    session_id=session_id,
    task_summary="All 6 tests passing, refactored to test logic directly"
)

submit_postflight_assessment(
    session_id=session_id,
    vectors={
        "foundation": {
            "know": {"score": 0.9},
            "do": {"score": 0.92},
            "context": {"score": 0.9}
        },
        "uncertainty": {"score": 0.15}
    },
    changes_noticed="Mastered test architecture, learned mock patterns and alternatives"
)

# ========================================
# SESSION END (Natural conclusion)
# ========================================

# Review learning trajectory
get_session_summary(session_id=session_id)

# Result shows clear learning: 0.6 → 0.75 → 0.8 → 0.9 (KNOW)
# This proves genuine learning across tasks!
```

---

## Visual Aid for Prompts

Include this diagram:

```
❌ WRONG: One PREFLIGHT per session
SESSION
  PREFLIGHT (once)
    └── Task A
    └── Task B  
    └── Task C
  POSTFLIGHT (once)

✅ CORRECT: PREFLIGHT per task (cascade)
SESSION
  ├── CASCADE (Task A)
  │   ├── PREFLIGHT
  │   ├── work
  │   └── POSTFLIGHT
  │
  ├── CASCADE (Task B)
  │   ├── PREFLIGHT ← YES, do it again!
  │   ├── work
  │   └── POSTFLIGHT
  │
  └── CASCADE (Task C)
      ├── PREFLIGHT ← And again!
      ├── work
      └── POSTFLIGHT
```

---

## Summary for System Prompts

Add these key points prominently:

1. **Sessions contain multiple cascades (tasks)**
2. **Each cascade needs PREFLIGHT → work → POSTFLIGHT**
3. **Don't skip PREFLIGHT thinking you "already did it"**
4. **Your scores should IMPROVE across tasks (proves learning)**
5. **One session can have 3, 5, 10+ cascades - that's normal!**

---

## Files to Update

1. `ROVODEV.md` - Add session vs cascade section
2. `CLAUDE.md` - Add session vs cascade section
3. `QWEN.md` - Add session vs cascade section
4. `GEMINI.md` - Add session vs cascade section
5. `GENERIC_EMPIRICA_SYSTEM_PROMPT.md` - Add as core concept
6. `SYSTEM_PROMPT_QUICK_REFERENCE.md` - Add to quick tips

---

This clarification will prevent AI agents from skipping PREFLIGHT for subsequent tasks within a session!
