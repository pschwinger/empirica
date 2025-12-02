# Deep Documentation Audit - Structural Issues

**Date:** 2025-01-29  
**Focus:** Wide-area structural gaps, not cosmetic fixes

---

## Priority 1: Heuristic Threshold References (48 instances)

### The Issue:
Docs say things like "IF UNCERTAINTY > 0.5 THEN investigate" - this is **heuristic decision logic** that Empirica explicitly avoids.

### The Caveat (from user):
**Thresholds ARE configurable externally:**
- Advanced users can set thresholds
- AIs can adjust based on self-assessment
- **Sentinel** sets thresholds based on domain/expertise/capability
- Configured via: `thresholds.yaml`, `goal_scopes.yaml`, `model_profiles.yaml`

### How to Fix:
**Wrong:**
```
IF UNCERTAINTY > 0.5 THEN investigate
Required: KNOW ≥ 0.6 to proceed
```

**Right:**
```
Guidance: High uncertainty suggests investigation
Configurable threshold (default 0.5, adjust via thresholds.yaml)
AI self-assesses readiness, Sentinel can override based on capability
```

**Pattern to find:**
- `IF.*>.*THEN`
- `threshold.*0\.[0-9]`
- `UNCERTAINTY > 0\.[0-9]`
- `required.*≥.*0\.[0-9]`
- Hard requirements without mentioning configurability

**Action:** Scan and fix to clarify thresholds are:
1. Guidance (not enforcement)
2. Configurable (externally controlled)
3. Context-dependent (Sentinel, domain, capability)

---

## Priority 2: Goal/Subtask Structural Gap (18 production docs)

### The Issue:
Production docs missing goal/subtask mentions - but these are **core features**:
- Goals organize work with epistemic context
- Vectorial scope (breadth, duration, coordination)
- Subtasks with evidence tracking
- Git integration for cross-AI coordination

### What's Missing:
Many production docs explain workflow without mentioning:
- How to create goals
- ScopeVector (3D scope measurement)
- Subtask management
- Goal lineage (who created/resumed)
- Cross-AI goal discovery

### Files Without Goal Mentions:
```
docs/production/*.md (18 files need at least a reference)
```

### How to Fix:
Add to each relevant production doc:

**Minimum:** 
"Empirica organizes work into goals with vectorial scope, subtasks, and epistemic context. Goals stored in git notes enable cross-AI coordination."

**Better (where workflow is explained):**
- Section on goal creation
- ScopeVector explanation (breadth/duration/coordination)
- Subtask tracking with evidence
- Git storage and cross-AI discovery

**Reference:**
- docs/architecture.md (has comprehensive goal section now)
- docs/production/25_SCOPEVECTOR_GUIDE.md (dedicated guide)

---

## Priority 3: Git Integration Gap (21 core docs)

### The Issue:
Git integration is **automatic and core** but many docs don't mention it:
- Checkpoints stored in git notes
- Goals discoverable by other AIs
- Handoff reports (98% compression)
- Cross-session continuity

### What Needs Adding:
**Checkpoints:**
- Where: `.git/notes/empirica/checkpoints/<session_id>`
- Compression: 85% (500 vs 6,500 tokens)
- Format: Compressed epistemic vectors + metadata

**Goals:**
- Where: `.git/notes/empirica/goals/<goal_id>`
- Discovery: Other AIs can `goals-discover` and `goals-resume`
- Lineage: Track who created, who resumed, when

**Handoffs:**
- Where: `.git/notes/empirica/handoffs/<session_id>`
- Compression: 98% (300 vs 20,000 tokens)
- Purpose: Session continuity without full context

### Files Missing Git Context:
```
docs/*.md (many core docs)
docs/production/*.md (many production docs)
```

### How to Fix:
Add git integration notes where continuity/coordination is discussed:

**Minimum:**
"Empirica stores checkpoints and goals in git notes for continuity and cross-AI coordination."

**Better:**
- Checkpoint storage and compression
- Goal discovery workflow
- Handoff reports for session continuity
- Cross-AI coordination via git

**Reference:**
- docs/architecture/STORAGE_ARCHITECTURE_COMPLETE.md (comprehensive)
- docs/guides/git/ (git integration guides)

---

## Priority 4: "Two Systems" Conceptual Clarity (12 mentions)

### The Issue:
The KEY conceptual distinction is only explained in ~12 docs:
- **Explicit Assessments:** PRE/CHECK/POST (tracked)
- **Implicit CASCADE:** think→investigate→act (guidance)

This should be reinforced more widely, especially in:
- Getting started guides
- Production workflow docs
- Troubleshooting (when users ask "where are my phases?")

### How to Fix:
Add to workflow explanations:

```markdown
## Two Separate Systems

**Explicit Assessments (Tracked):**
- PRE: Session start baseline
- CHECK: Decision points (0-N times)
- POST: Session end calibration

**Implicit CASCADE (Guidance):**
- think → investigate → act
- Natural workflow, not enforced phases
- AI self-assesses current activity
```

**Files to update:**
- docs/getting-started.md
- docs/production/03_BASIC_USAGE.md
- docs/production/07_INVESTIGATION_SYSTEM.md
- Key workflow docs

---

## Priority 5: MCO/Persona Unexplained References (41 mentions)

### The Issue:
"MCO", "persona", "Sentinel" mentioned without explanation
- Users might be confused
- Only explained in docs/production/24_MCO_ARCHITECTURE.md

### How to Fix:
First mention should have a brief explanation + link:

```markdown
**MCO (Metacognitive Orchestrator)** - Dynamic configuration system (personas, cascade styles, model profiles). See [MCO Architecture](../production/24_MCO_ARCHITECTURE.md).

**Sentinel** - Advanced orchestration system that can adjust thresholds based on domain/capability.
```

---

## Summary: Structural Gaps

| Issue | Count | Priority | Effort |
|-------|-------|----------|--------|
| Heuristic thresholds | 48 | HIGH | Medium (clarify configurability) |
| Missing goal mentions | 18 | HIGH | Low (add minimum reference) |
| Missing git context | 21 | MEDIUM | Low (add minimum reference) |
| "Two systems" unclear | ~30 | MEDIUM | Low (add explanation) |
| MCO unexplained | 41 | LOW | Low (add brief note + link) |

---

## Recommended Approach

### Phase 1: Fix Heuristic Thresholds
- Scan 48 instances
- Add context: "Configurable via thresholds.yaml, Sentinel can adjust"
- Change "required" to "guidance"

### Phase 2: Add Goal References
- 18 production docs need minimum: "Goals with vectorial scope..."
- Link to comprehensive docs

### Phase 3: Add Git Integration Notes
- 21 docs need minimum: "Stored in git notes for continuity..."
- Link to STORAGE_ARCHITECTURE_COMPLETE.md

### Phase 4: Reinforce Two Systems
- Add to key workflow docs
- Clarify in troubleshooting

### Phase 5: Explain MCO/Sentinel
- First mention gets definition + link
- Especially in production docs

---

## Next Steps

1. **Review with user** - Confirm priorities and approach
2. **Start with Phase 1** - Heuristic threshold audit
3. **Add goal/git references** - Phases 2 & 3
4. **Reinforce concepts** - Phases 4 & 5

---

**Note:** These are STRUCTURAL issues, not cosmetic. They affect user understanding of how Empirica actually works.
