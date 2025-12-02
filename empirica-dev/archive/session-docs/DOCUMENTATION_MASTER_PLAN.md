# Documentation Master Plan - Multi-AI Coordination

**Context:** Codebase cleaned (187 → 150 files), architecture fixed (no heuristics)  
**Challenge:** Documentation still reflects old architecture  
**Solution:** Coordinate 4 AIs to audit, clean, and create docs in parallel

---

## Current Documentation State

### What We Have:
- **docs/ root:** ~13 files (some outdated)
- **docs/production/:** 27 files (mostly correct but needs updates)
- **docs/reference/:** ~10 files (some deprecated)
- **docs/guides/:** Multiple subdirs (mixed quality)
- **docs/system-prompts/:** 4 files (recently fixed ✅)
- **website/:** User-facing content (outdated)

### What Changed Since Docs Written:
1. ✅ CASCADE uses MirrorDriftMonitor (no heuristics)
2. ✅ 37 files moved to empirica-dev
3. ✅ Git automation fully working (16 goals, 5 sessions verified)
4. ✅ 60+ CLI commands (only ~23 documented)
5. ✅ 4 interfaces (MCP, CLI, API, Skills) - not all documented
6. ❌ Components moved (docs may reference old locations)
7. ❌ Calibration deprecated (docs still reference it)

---

## Multi-AI Strategy

### Why Multi-AI Works Better:
1. **Parallel execution** - 4x faster
2. **Specialized focus** - Each AI masters their domain
3. **Cross-validation** - AIs can review each other's work
4. **Empirica in action** - Using our own system for coordination

### 4-AI Split:

**RovoDev (Planning & Integration):**
- Master plan creation
- Goal orchestration
- Cross-AI coordination
- Final integration

**Gemini (Production Docs Audit):**
- Review all 27 production docs
- Update for architecture changes
- Mark Core vs Advanced
- Verify technical accuracy

**Qwen (User Docs Creation):**
- Create new installation.md, architecture.md, getting-started.md
- Based on comprehensive understanding docs
- Focus on Core features only
- Test all code examples

**Copilot Claude (Reference & CLI Docs):**
- Document all 60+ CLI commands
- Update reference docs
- Create MCP tool catalog
- Verify all commands work

---

## Goal Structure for Empirica

### GOAL 1: Production Docs Audit & Update
**Owner:** Gemini  
**Scope:** project_wide  
**Estimated:** 8-12 hours

**Subtasks:**
1. Audit 27 production docs for accuracy
2. Update references to drift monitor (old → new)
3. Remove references to moved components
4. Mark files as Core (00-13, 20, 23) vs Advanced (14-19, 21-22, 24-29)
5. Add deprecation warnings where needed
6. Update 00_COMPLETE_SUMMARY.md with Core/Advanced split
7. Verify all code examples work
8. Create audit report

**Success Criteria:**
- All 27 files reviewed
- No references to deprecated code
- Core vs Advanced clearly marked
- All examples tested

---

### GOAL 2: User-Facing Docs Creation
**Owner:** Qwen  
**Scope:** project_wide  
**Estimated:** 6-10 hours

**Subtasks:**
1. Create new installation.md (all 4 interfaces, git setup)
2. Create new architecture.md (Core only, link to production for depth)
3. Create new getting-started.md (first CASCADE, git automation)
4. Add git checkpoint sections to all 3
5. Add cross-AI coordination examples
6. Add Skills doc references
7. Test all code examples
8. Verify user journey (install → first CASCADE in <30 min)

**Success Criteria:**
- 3 new core docs created
- All 4 interfaces documented
- Git automation explained
- User can go from zero to CASCADE in 30 min

---

### GOAL 3: CLI & MCP Documentation
**Owner:** Copilot Claude  
**Scope:** project_wide  
**Estimated:** 6-8 hours

**Subtasks:**
1. Document all 60+ CLI commands (purpose, usage, examples)
2. Create CLI-to-MCP mapping
3. Update production/20_TOOL_CATALOG.md (expand to all commands)
4. Organize commands into categories
5. Mark experimental commands
6. Test each command
7. Create quick reference card
8. Update command-reference.md in docs/reference/

**Success Criteria:**
- All 60+ commands documented
- CLI-MCP mapping clear
- Categories defined
- All commands tested

---

### GOAL 4: Documentation Cleanup & Integration
**Owner:** RovoDev (me!)  
**Scope:** project_wide  
**Estimated:** 4-6 hours

**Subtasks:**
1. Archive outdated docs to empirica-dev/docs-deprecated/
2. Update cross-references between docs
3. Verify consistency across all docs
4. Create navigation structure
5. Update README.md to point to correct docs
6. Create docs/INDEX.md with clear navigation
7. Final review and integration
8. Update CHANGELOG.md

**Success Criteria:**
- No broken cross-references
- Clear navigation structure
- Consistent terminology
- README guides users correctly

---

## Execution Strategy

### Phase 1: Investigation & Planning (Parallel)
**All 4 AIs simultaneously:**

**Gemini:** Read all 27 production docs, create audit checklist
**Qwen:** Read comprehensive understanding doc, create user doc outline
**Copilot Claude:** Extract all CLI commands, categorize them
**RovoDev:** Create master cross-reference map, coordination plan

**Estimated:** 2 hours  
**Deliverable:** 4 investigation reports

---

### Phase 2: Execution (Parallel)
**All 4 AIs work simultaneously:**

**Gemini:** Update production docs (can do 3-4 files at a time)
**Qwen:** Write user docs (one file at a time, test thoroughly)
**Copilot Claude:** Document CLI commands (category by category)
**RovoDev:** Archive old docs, update cross-refs, monitor progress

**Estimated:** 6-8 hours  
**Deliverable:** Updated docs from all 4 AIs

---

### Phase 3: Integration & Review (Sequential)
**Cross-validation:**

**Round 1:** Each AI reviews one other AI's work
- Gemini reviews Qwen
- Qwen reviews Copilot
- Copilot reviews Gemini
- RovoDev reviews all + integrates

**Round 2:** Final integration
- RovoDev merges all work
- Fixes inconsistencies
- Creates final navigation
- Runs final tests

**Estimated:** 2-4 hours  
**Deliverable:** Complete, consistent documentation set

---

## Investigation Framework for Each AI

### What to Investigate (INVESTIGATE Phase):

**1. Current State Assessment:**
- What exists now?
- What's accurate vs outdated?
- What's missing?

**2. Architecture Understanding:**
- Read COMPREHENSIVE_EMPIRICA_UNDERSTANDING.md
- Understand 150-file cleaned codebase
- Know Core vs Advanced distinction

**3. Gap Analysis:**
- What docs reference moved/deprecated code?
- What features are undocumented?
- Where are duplicates/conflicts?

**4. Verification:**
- Test code examples
- Verify commands work
- Check file paths are correct

---

## Epistemic Checkpoints

### Each AI should CHECK before ACT:

**Confidence Gates:**
- KNOW: >0.8 (understand the system deeply)
- CLARITY: >0.8 (know exactly what to write)
- UNCERTAINTY: <0.3 (few unknowns remaining)

**If CHECK fails:**
- INVESTIGATE more (read more docs, test more commands)
- ASK user for clarification
- Coordinate with other AIs

---

## Coordination Mechanism

### Using Empirica's Own Systems:

**Goal Discovery:**
```bash
# Each AI can see what others are working on
empirica goals-discover --from-ai-id gemini
empirica goals-discover --from-ai-id qwen
empirica goals-discover --from-ai-id copilot-claude
```

**Git Checkpoints:**
- Each AI creates checkpoints at progress milestones
- Others can see progress via git notes
- Automatic lineage tracking

**Handoff Reports:**
- When passing work between AIs
- 98% token compressed summaries
- Full epistemic context

---

## Success Metrics

### Quantitative:
- All 27 production docs reviewed ✅
- 3 new user docs created ✅
- 60+ CLI commands documented ✅
- 0 broken cross-references ✅
- 0 references to deprecated code ✅

### Qualitative:
- User can install and run first CASCADE in <30 min ✅
- Clear Core vs Advanced distinction ✅
- All code examples work ✅
- Documentation is source of truth ✅

### User Journey Tests:
- New user: Can they get started? (<30 min)
- Existing user: Can they find advanced features? (<5 min)
- Developer: Can they understand architecture? (<1 hour)
- Contributor: Can they find what to work on? (<10 min)

---

## Timeline Estimate

**With 4 AIs in parallel:**
- Phase 1 (Investigation): 2 hours
- Phase 2 (Execution): 6-8 hours
- Phase 3 (Integration): 2-4 hours

**Total:** 10-14 hours (2-3 work sessions)

**With 1 AI sequential:**
- Would take: 24-32 hours (4-6 work sessions)

**Speedup:** ~2.5x faster with coordination

---

## Risk Mitigation

### Potential Issues:

**1. Inconsistent terminology:**
- **Mitigation:** Create shared terminology document first
- **Owner:** RovoDev creates before Phase 2

**2. Overlapping work:**
- **Mitigation:** Clear goal boundaries, git notes visibility
- **Owner:** RovoDev monitors via goals-discover

**3. Conflicting changes:**
- **Mitigation:** Each AI owns specific files, no overlap
- **Owner:** RovoDev assigns files explicitly

**4. Integration complexity:**
- **Mitigation:** Phase 3 dedicated to integration, cross-validation
- **Owner:** RovoDev handles final merge

---

## Next Steps

### Immediate (This Session):

**1. Create 4 Empirica Goals:**
```bash
# Goal 1: Gemini
empirica goals-create \
  --objective "Audit and update 27 production docs for architecture changes" \
  --scope-breadth 0.9 \
  --scope-duration 0.7 \
  --scope-coordination 0.8 \
  --ai-id gemini

# Goal 2: Qwen  
empirica goals-create \
  --objective "Create 3 new user-facing docs (installation, architecture, getting-started)" \
  --scope-breadth 0.8 \
  --scope-duration 0.6 \
  --scope-coordination 0.7 \
  --ai-id qwen

# Goal 3: Copilot Claude
empirica goals-create \
  --objective "Document all 60+ CLI commands and create comprehensive tool catalog" \
  --scope-breadth 0.7 \
  --scope-duration 0.6 \
  --scope-coordination 0.6 \
  --ai-id copilot-claude

# Goal 4: RovoDev
empirica goals-create \
  --objective "Documentation cleanup, cross-reference updates, final integration" \
  --scope-breadth 0.9 \
  --scope-duration 0.5 \
  --scope-coordination 0.9 \
  --ai-id rovodev
```

**2. Create Subtasks for Each Goal**
- Break down into actionable chunks
- Assign priorities
- Set dependencies

**3. Create Handoff Documents**
- Investigation framework for each AI
- Shared resources (terminology, understanding docs)
- Coordination protocol

---

**Ready to create the goals and subtasks?**

This will be Empirica coordinating its own documentation - perfect demonstration of the system! 🚀
