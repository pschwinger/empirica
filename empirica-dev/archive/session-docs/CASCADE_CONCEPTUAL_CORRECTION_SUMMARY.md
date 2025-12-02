# CASCADE Conceptual Correction Summary

**Date:** 2025-01-29  
**Status:** Critical conceptual clarification identified  
**Impact:** Affects documentation, code, and user understanding

---

## The Key Insight

User clarified that we've been conflating two separate systems:

### 1. CASCADE Workflow (Implicit Guidance)
```
THINK → PLAN → INVESTIGATE → CHECK → ACT
         ↺ (loop back if CHECK says "not ready")
```
- **Nature:** Implicit, self-assessed workflow
- **Not enforced:** AI naturally moves through these mental phases
- **CHECK is decision point:** "Am I ready to act?" (can loop multiple times)
- **Goals/Subtasks:** General flow of work during investigate & act phases

### 2. Epistemic Assessments (Explicit Checkpoints)
```
PRE (session start) → CHECK(s) (decision points) → POST (session end)
                              ↓
                         CALIBRATION (deltas)
```
- **Nature:** Explicit 13-vector epistemic assessments
- **Tracked:** Stored in git checkpoints, session DB
- **PRE:** "What do I know going in?" (ENGAGEMENT gate at session start)
- **CHECK:** "Should I investigate more or proceed?" (can happen multiple times)
- **POST:** "What did I learn?" (calibration measurement at session end)
- **CALIBRATION:** Compare pre→post deltas to measure learning

---

## What Was Wrong

### The Conflation:
We were treating CASCADE phases as **explicit trackable states** instead of **implicit workflow guidance**.

**Wrong thinking:**
- "You are in PREFLIGHT phase" ← rigid state tracking
- "Now transition to INVESTIGATE phase" ← enforced state machine
- "POSTFLIGHT is the final phase" ← wrong!

**Correct thinking:**
- "I'm thinking about the task" ← AI self-assesses (implicit)
- "Should I investigate more or am I ready to act?" ← CHECK decision
- "Session complete, what did I learn?" ← POST assessment

### The Pattern We Got Wrong:
```
❌ WRONG: PREFLIGHT → THINK → INVESTIGATE → CHECK → ACT → POSTFLIGHT
           (treating all as explicit phases)

✅ RIGHT: PRE assessment → [implicit work: think/investigate/act] → CHECK(s) → POST assessment
           (explicit checkpoints around implicit work)
```

---

## What We Did Today

### 1. Fixed MCP Validation (Completed ✅)
- Disabled rigid schema validation
- Added flexible parameter parsing
- Reinforced "guidance, not enforcement" philosophy

### 2. Documented Future Vision (Completed ✅)
- Created trajectory visualization vision doc
- "See your AI think. Watch it not crash."

### 3. End-to-End Testing (Completed ✅)
- 15/15 tests passing
- Found only documentation gaps, not code bugs

### 4. Discovered Conceptual Issue (In Progress)
- User clarified: CASCADE = implicit, assessments = explicit
- Audited documentation
- Began archiving wrong documents

---

## What Got Archived

### Moved to `empirica-dev/archive/wrong_cascade_model/`:

**Specifications:**
- `EMPIRICA_CASCADE_WORKFLOW_SPECIFICATION.md`
- `06_CASCADE_FLOW.md`

**Session Summaries (created by me today!):**
- `SESSION_COMPLETE_E2E_TESTING.md`
- `E2E_MCP_TEST_RESULTS.md`
- `SESSION_SUMMARY_VALIDATION_FIX.md`

**Audit:**
- `CASCADE_TERMINOLOGY_AUDIT.md` (full list of what needs fixing)

---

## What Still Needs Archiving/Fixing

### High Priority Documentation:
- `README.md` - Shows wrong CASCADE flow
- `docs/ONBOARDING_GUIDE.md` - Teaches wrong model
- `docs/installation.md` - Shows wrong expectations
- `docs/production/00_COMPLETE_SUMMARY.md` - References wrong model
- `docs/reference/EMPIRICA_FOUNDATION_SPECIFICATION.md` - Wrong conceptual model

### System Prompts:
- `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md` - Instructs agents wrongly
- `.github/copilot-instructions.md` - Wrong instructions

### Website Content:
- All website files showing CASCADE as explicit phases

### Code That Needs Refactoring:
- `empirica/core/metacognitive_cascade/metacognitive_cascade.py`
  - `class CascadePhase(Enum)` treats phases as states
  - `_enter_phase()` calls throughout
  - Should track: assessment type (PRE/CHECK/POST) not workflow phases
- `empirica/core/schemas/epistemic_assessment.py`
  - `class CascadePhase` should be `AssessmentType`
- `empirica/config/mco/protocols.yaml`
  - Enums need correction

---

## What Needs to Be Created

### New Core Documents:

1. **`CORRECT_CASCADE_MODEL.md`**
   - Clear explanation of implicit vs explicit
   - Visual diagrams
   - Examples

2. **`EMPIRICA_EPISTEMIC_ASSESSMENT_SPEC.md`**
   - PRE assessment (session start, ENGAGEMENT gate)
   - CHECK assessment (decision points, can repeat)
   - POST assessment (session end, calibration)
   - CALIBRATION (measure learning deltas)

3. **`CASCADE_IMPLICIT_WORKFLOW_GUIDE.md`**
   - THINK → PLAN → INVESTIGATE → CHECK → ACT
   - Guidance, not enforcement
   - How to self-assess current phase
   - When to loop back

4. **Updated `README.md`**
   - Correct CASCADE description
   - Clear about implicit vs explicit

5. **Updated System Prompts**
   - Teach correct model
   - Emphasize implicit workflow + explicit checkpoints

---

## Key Terminology Changes

### Old (Wrong) → New (Correct):

| Old Term | New Term | Reason |
|----------|----------|--------|
| PREFLIGHT phase | PRE assessment | It's an assessment, not a phase |
| POSTFLIGHT phase | POST assessment | It's an assessment, not a phase |
| Phase transition | Assessment checkpoint | Not transitioning phases |
| Enter INVESTIGATE phase | Currently investigating (implicit) | Not a trackable state |
| CASCADE phases | CASCADE workflow (implicit) | Guidance, not states |
| execute_preflight | submit_pre_assessment | Clearer purpose |
| execute_postflight | submit_post_assessment | Clearer purpose |

---

## Impact Assessment

### Documentation:
- **~25+ files** need correction or archiving
- **3 major specs** need rewrite
- **Website content** needs update

### Code:
- **Core cascade engine** needs refactor (metacognitive_cascade.py)
- **Schemas** need renaming (CascadePhase → AssessmentType)
- **MCP tools** could use clearer names (preflight → pre_assessment)
- **Tests** need to reflect correct model

### User Impact:
- **Low immediate impact** - system works correctly
- **High long-term impact** - wrong mental model leads to misuse
- **Documentation gap** - users may be confused

---

## Recommendations

### Immediate (Next Session):
1. Create `CORRECT_CASCADE_MODEL.md` with clear explanation
2. Update `README.md` with correct description
3. Create new assessment specification document
4. Update key system prompts

### Short-term (Next Few Sessions):
5. Archive remaining wrong documentation
6. Rewrite core specifications
7. Update website content
8. Create migration guide for users

### Long-term (Future):
9. Refactor `metacognitive_cascade.py` to remove explicit phase tracking
10. Rename schemas (CascadePhase → AssessmentType)
11. Consider renaming MCP tools for clarity
12. Update all tests to reflect correct model

---

## Key Quotes from User

> "CASCADE I mean the think - plan - investigate - check - act (implicit with guidance)"

> "where pre- check (multiple times if necessary) - post - calibration of deltas are explicit for the whole session"

> "We should not conflate the workflow cascade from the explicit self assessments"

> "The decisions themselves for both investigate and act phases are captured but that's just the general flow of work"

> "Its where the goals and subtasks are taken care of"

---

## Files Created This Session

✅ `CASCADE_CONCEPTUAL_CORRECTION_SUMMARY.md` (this file)  
✅ `empirica-dev/archive/wrong_cascade_model/README.md`  
✅ Archived 5 key documents to empirica-dev  
✅ `VALIDATION_FIX_SUMMARY.md` (earlier work)  
✅ `MCP_FLEXIBLE_VALIDATION_FIX.md` (earlier work)  
✅ `docs/architecture/EPISTEMIC_TRAJECTORY_VISUALIZATION.md` (future vision)

---

## Next Steps

**Priority 1:** Create correct conceptual documentation
- Write `CORRECT_CASCADE_MODEL.md`
- Update `README.md`
- Fix system prompts

**Priority 2:** Archive remaining wrong docs
- Move user-facing docs to archive
- Move website content to archive
- Document what was moved and why

**Priority 3:** Refactor code (future)
- This is a larger effort
- Can be done incrementally
- Existing code works, just uses wrong conceptual model

---

**Status:** Conceptual clarification complete. Documentation cleanup in progress.  
**Impact:** This is a fundamental correction that improves long-term maintainability and user understanding.
