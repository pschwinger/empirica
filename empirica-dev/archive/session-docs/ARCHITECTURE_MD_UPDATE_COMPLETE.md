# architecture.md Update Complete

**Date:** 2025-01-29  
**Task:** Update architecture.md to reflect current reality and correct CASCADE model

---

## What Was Updated

### 1. Terminology Fix
**Changed:**
- "PREFLIGHT" → "PRE assessment"
- "POSTFLIGHT" → "POST assessment"
- "Preflight → Postflight" → "PRE → POST assessment"

**Throughout the document**

### 2. Core Components Updated
**Added:**
- Goal Orchestrator - Manages goals and subtasks
- Git Integration - Checkpoints, goals, cross-AI coordination

### 3. Session Structure Rewritten
**Before:** Simple PREFLIGHT → WORK → POSTFLIGHT
**After:** Complete flow showing:
- PRE assessment (session start)
- CREATE GOAL (with subtasks)
- Implicit CASCADE (think→investigate→act)
- CHECK assessments (0-N decision points)
- POST assessment (session end)
- CALIBRATION (PRE→POST deltas)

### 4. Added Comprehensive Goal & Subtask Section
**New Section:** 40+ lines covering:
- Goal structure (objective, scope, subtasks, epistemic context, lineage)
- Subtask structure (description, importance, status, evidence)
- Goal workflow (PRE → CREATE → CASCADE → POST → Git)
- Cross-AI coordination examples
- Benefits

### 5. Data Flow Sections Enhanced
**Added:**
- Goal Creation Flow
- CHECK Assessment Flow (decision points, 0-N times)
- Updated PRE/POST flows with git checkpoints
- Clarified that CHECK can happen multiple times

### 6. AI vs Agent Pattern Updated
**Before:** Referenced "PREFLIGHT → POSTFLIGHT"
**After:** "PRE → CHECK(s) → POST assessment"

### 7. Git Integration Clarified
**Enhanced:**
- When checkpoints are created
- Goal discovery and resumption
- Cross-AI coordination via git
- Lineage tracking

---

## Sections Now Include

✅ System Overview (7 core components including goals & git)
✅ 13-Vector System (UVL)
✅ Session Structure (correct model with diagram)
✅ **Goal & Subtask Management** (NEW comprehensive section)
✅ Data Flow (PRE/Goal/CHECK/POST flows)
✅ Calibration System
✅ Design Principles (NO HEURISTICS, Privacy, etc.)
✅ Technology Stack
✅ CLI/MCP/Python API interfaces
✅ **Git Integration** (checkpoints, goals, cross-AI coordination)
✅ Deep Dive References

---

## Alignment with Current Reality

The document now reflects:

1. **CANONICAL_DIRECTORY_STRUCTURE_V2.md:**
   - Correct docs structure
   - Clean organization after archiving

2. **STORAGE_LOCATIONS.md:**
   - Session database locations
   - Git notes locations
   - Reflex logs

3. **Canonical System Prompt:**
   - Two separate systems (explicit assessments + implicit workflow)
   - CHECK can happen 0-N times
   - Goals and subtasks mentioned

4. **Actual Implementation:**
   - Git checkpoints automatic
   - Goal orchestrator exists
   - Cross-AI coordination via git

---

## Files Modified

1. `docs/architecture.md` - Complete update
2. `ARCHITECTURE_MD_UPDATE_COMPLETE.md` - This summary

---

## Remaining Work

### Minor:
- `docs/skills/SKILL.md` - May still reference old workflow (48KB file)
- Some production docs still use "PREFLIGHT/POSTFLIGHT" (acceptable as "assessment")

### Future:
- Remove reference to `AI_VS_AGENT_EMPIRICA_PATTERNS.md` (archived)
- Update Phase 0 boundaries if goals/git are part of Phase 0

---

**Status:** architecture.md now accurately reflects current system ✅  
**Goal/Subtask:** Comprehensively documented  
**Git Integration:** Clearly explained  
**Terminology:** Consistent with canonical system prompt
