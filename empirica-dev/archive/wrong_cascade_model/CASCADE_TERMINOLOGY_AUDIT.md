# CASCADE Terminology Audit - Implicit vs Explicit

**Date:** 2025-01-29  
**Issue:** Conflation of implicit CASCADE workflow with explicit epistemic assessments

---

## The Correct Model

### Implicit CASCADE Workflow (Guidance)
```
THINK → PLAN → INVESTIGATE → CHECK → ACT
         ↺ (loop back based on CHECK decision)
```
- **Nature:** Implicit, self-assessed, guidance only
- **Not tracked:** AI naturally does this work
- **CHECK is decision point:** "Am I ready to act?" (can loop multiple times)
- **Goals/Subtasks:** Managed during INVESTIGATE and ACT phases

### Explicit Epistemic Assessments (Checkpoints)
```
PRE (session start) → CHECK(s) (decision points) → POST (session end)
                              ↓
                         CALIBRATION (deltas: pre→post)
```
- **Nature:** Explicit 13-vector assessments
- **Tracked:** Stored in git checkpoints, session DB
- **PRE:** "What do I know going in?" (ENGAGEMENT gate)
- **CHECK:** "Should I investigate more or proceed?" (can happen multiple times)
- **POST:** "What did I learn?" (calibration measurement)
- **CALIBRATION:** Compare predicted vs actual difficulty (pre→post deltas)

---

## The Problem

Documents and code treat CASCADE phases as **explicit state machine phases** instead of **implicit workflow guidance**.

### Wrong Patterns Found:

1. **"PREFLIGHT phase"** → Should be **"PRE assessment"**
2. **"POSTFLIGHT phase"** → Should be **"POST assessment"**
3. **"Phase transitions"** → Should be **"Assessment checkpoints"**
4. **"Enter INVESTIGATE phase"** → Should be **"AI is investigating (implicit)"**
5. **`_enter_phase(CascadePhase.INVESTIGATE)`** → Should not track phases as states

### Correct Patterns:

1. **"PRE assessment"** - Explicit 13-vector assessment at session start
2. **"CHECK assessment"** - Explicit decision point (investigate vs act)
3. **"POST assessment"** - Explicit final assessment for calibration
4. **"CASCADE workflow"** - Implicit guidance (think→plan→investigate→check→act)
5. **Goals/Subtasks** - Managed during work (investigate & act phases)

---

## Files to Archive (Wrong Information)

### Category 1: Specification Documents (HIGH PRIORITY)

1. **`docs/reference/EMPIRICA_CASCADE_WORKFLOW_SPECIFICATION.md`**
   - Treats CASCADE as explicit phases
   - Says "Phase 0: PREFLIGHT", "Phase 6: POSTFLIGHT"
   - Should say: PRE assessment, POST assessment

2. **`docs/production/06_CASCADE_FLOW.md`**
   - Title: "PREFLIGHT → THINK → PLAN → INVESTIGATE → CHECK → ACT → POSTFLIGHT"
   - Treats all as explicit phases
   - Needs complete rewrite

3. **`docs/reference/EMPIRICA_FOUNDATION_SPECIFICATION.md`**
   - Section 3.1 treats phases as explicit states
   - Needs conceptual correction

### Category 2: System Architecture Documents

4. **`docs/architecture/SYSTEM_ARCHITECTURE_DEEP_DIVE.md`**
   - References "phase transitions" as explicit state changes
   - Should clarify implicit vs explicit

5. **`docs/architecture/EMPIRICA_SYSTEM_OVERVIEW.md`**
   - Shows CASCADE as phase sequence
   - Needs clarification about implicit workflow

### Category 3: User-Facing Documentation

6. **`README.md`**
   - Shows: "PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT"
   - Should show: PRE → [implicit work: think/investigate/act] → CHECK(s) → POST

7. **`docs/installation.md`**
   - Expected output shows explicit phases
   - Needs correction

8. **`docs/ONBOARDING_GUIDE.md`**
   - Teaches CASCADE as explicit phases
   - Will confuse users

9. **`docs/production/00_COMPLETE_SUMMARY.md`**
   - References explicit phase flow
   - Needs update

### Category 4: Website Content

10. **`website/simplified_content/index.md`**
11. **`website/content/index_VALIDATED.md`**
12. **`website/simplified_content/faqs.md`**
13. **`website/content/cli-interface.md`**
14. **`website/content/docs.md`**
15. **`website/wireframes/index.md`**
16. **`website/wireframes/architecture.md`**
    - All show CASCADE as explicit phase sequence
    - All need correction

### Category 5: System Prompts & Agent Instructions

17. **`docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`**
18. **`.github/copilot-instructions.md`**
    - Instruct agents to use explicit phases
    - Should teach implicit workflow + explicit assessments

### Category 6: Test Documentation

19. **`tests/coordination/archive/COMPREHENSIVE_TEST_ARCHITECTURE.md`**
20. **`tests/coordination/archive/GEMINI_STATUS_REVIEW.md`**
21. **`tests/coordination/archive/EMPIRICA_VALIDATION_TEST_PLAN.md`**
    - Test against explicit phase sequences
    - Should test assessments, not phases

### Category 7: Session Summaries (Recent - Created by Me!)

22. **`SESSION_COMPLETE_E2E_TESTING.md`**
23. **`E2E_MCP_TEST_RESULTS.md`**
24. **`SESSION_SUMMARY_VALIDATION_FIX.md`**
    - I perpetuated the wrong model!
    - Shows CASCADE as: "BOOTSTRAP → PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT"

### Category 8: MCP Server Documentation

25. **`mcp_local/empirica_mcp_server.py`** (inline docs)
    - Tool descriptions show explicit phases
    - Needs correction

---

## Code Files Needing Refactor

### Primary Issue:

**`empirica/core/metacognitive_cascade/metacognitive_cascade.py`**
- Line 90: `class CascadePhase(Enum)` treats phases as explicit states
- Lines 420, 523, 809, 861, 904, 973: `_enter_phase()` calls
- Should track: `current_work_type` (investigating vs acting) - IMPLICIT
- Should track: `assessment_type` (PRE vs CHECK vs POST) - EXPLICIT

### Secondary Issues:

**`empirica/core/schemas/epistemic_assessment.py`**
- Line 21: `class CascadePhase(Enum)` - same issue
- Should be: `AssessmentType(Enum)` with values: PRE, CHECK, POST

**`empirica/config/mco/protocols.yaml`**
- Line 399: `enum: ["PREFLIGHT", "INVESTIGATE", "CHECK", "ACT", "POSTFLIGHT"]`
- Should be: `enum: ["PRE", "CHECK", "POST"]` for assessments
- Separate: `work_type: ["thinking", "investigating", "acting"]` for implicit

**Test Files:**
- `tests/unit/cascade/test_preflight.py` → `test_pre_assessment.py`
- `tests/unit/cascade/test_postflight.py` → `test_post_assessment.py`
- `tests/unit/cascade/test_investigate.py` → Should test implicit work, not phase
- `tests/unit/cascade/test_act.py` → Should test implicit work, not phase

---

## Recommendation

### Archive Location:
```
empirica-dev/archive/wrong_cascade_model/
├── specs/
│   ├── EMPIRICA_CASCADE_WORKFLOW_SPECIFICATION.md
│   ├── CASCADE_FLOW.md
│   └── EMPIRICA_FOUNDATION_SPECIFICATION.md
├── docs/
│   ├── README.md
│   ├── ONBOARDING_GUIDE.md
│   └── installation.md
├── website/
│   ├── index.md
│   ├── faqs.md
│   └── ...
└── session_summaries/
    ├── SESSION_COMPLETE_E2E_TESTING.md
    ├── E2E_MCP_TEST_RESULTS.md
    └── ...
```

### Create New Documents:
1. **`EMPIRICA_EPISTEMIC_ASSESSMENT_SPEC.md`** - PRE, CHECK, POST assessments
2. **`CASCADE_IMPLICIT_WORKFLOW_GUIDE.md`** - Think/investigate/act guidance
3. **`CORRECT_CASCADE_MODEL.md`** - Clarify the two systems

---

## Next Steps

1. **Create archive directory** in empirica-dev
2. **Move wrong docs** to archive
3. **Create correction document** explaining the right model
4. **Update key specs** (Foundation, Architecture)
5. **Refactor code** (metacognitive_cascade.py, schemas)
6. **Update MCP tools** (preflight → pre_assessment, etc.)
7. **Rewrite user docs** with correct model

---

## Key Insight from User

> "CASCADE = implicit workflow with guidance (think→investigate→act)
> Assessments = explicit checkpoints (PRE→CHECK(s)→POST→CALIBRATION)
> Goals/subtasks = managed during work phases
> Don't conflate workflow guidance with explicit state tracking"

This is a **fundamental conceptual correction** that affects the entire system.
