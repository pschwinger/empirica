# Empirica Documentation Cleanup - Epistemic Handoff Plan

**Created:** 2025-01-XX  
**For:** Acting AIs (Qwen, Gemini, Claude/Antigravity)  
**Method:** Using Empirica's own epistemic handoff system  
**Goal:** Complete Phase 1 doc consolidation (101 → ~30 files)

---

## Current State (What We've Done)

### ✅ Completed Work

**Phase 1A - Duplicate Consolidation:**
- Analyzed 9 duplicate files (installation, architecture, quick-ref)
- Created 6 canonical files with clear names
- Archived 4 duplicates to empirica-dev/docs-duplicates/
- Removed 5 old files after creating canonical versions

**Architecture Documentation:**
- Created `CANONICAL_DIRECTORY_STRUCTURE_V2.md` (matches actual codebase)
- Updated `GIT_CHECKPOINT_ARCHITECTURE.md` (git notes integration)
- Updated 5 system prompts (corrected CASCADE architecture)

**Files Moved to empirica-dev (135 total):**
- 39 from docs/archive/
- 56 from docs/wip/
- 19 from docs/system-prompts/archive/
- 15 session artifacts (SESSION_*.md, HANDOFF_*.md, etc.)
- 6 test artifacts (test_*.py, test-reflex directories)

**Canonical Docs Created:**
- `docs/installation.md` (13K)
- `docs/architecture.md` (11K)
- `docs/getting-started.md` (7.4K)
- `docs/reference/architecture-technical.md`
- `docs/reference/command-reference.md`

---

## Current State (What Remains)

**File Count:**
- Started: 101 markdown files in docs/
- After Phase 1A: ~95 files remaining
- Target: ~30 files

**Directories to Audit:**
- `docs/production/` - 23 files (comprehensive guides)
- `docs/reference/` - 11 files (technical specs)
- `docs/guides/` - Multiple subdirectories (how-tos)
- `docs/` root - ~13 numbered/named files

---

## Epistemic Self-Assessment (PREFLIGHT)

**Know (Codebase Understanding): 0.8**
- ✅ Understand git notes integration (verified working)
- ✅ Understand CASCADE architecture (BOOTSTRAP session-level)
- ✅ Understand documentation structure (3 tiers identified)
- ✅ Know which files are duplicates
- ⚠️ Don't know all content in production/ docs yet

**Clarity (Task Understanding): 0.9**
- ✅ Goal: Consolidate 101 → 30 files
- ✅ Criteria: Remove duplicates, archive outdated, verify accuracy
- ✅ Method: Read → Classify → Consolidate/Archive
- ✅ Success metrics clear

**Uncertainty (Unknowns): 0.3**
- ⚠️ Which production/ docs are still accurate?
- ⚠️ Which reference/ docs conflict with canonical prompt?
- ⚠️ Where else are there duplicates we haven't found?

**Engagement (Readiness): 0.8**
- ✅ Have clear plan and criteria
- ✅ Have tools (can read, classify, move files)
- ✅ Understand the goal

---

## Investigation Plan (Phase 1B)

### Step 1: Audit production/ (23 files)

**Goal:** Identify outdated, duplicate, or conflicting content

**Files to Check:**
```
docs/production/
├── 00_COMPLETE_SUMMARY.md          # Overview - keep?
├── 01_QUICK_START.md               # ✅ Already consolidated → getting-started.md
├── 02_INSTALLATION.md              # ✅ Already archived
├── 03_BASIC_USAGE.md               # Review: duplicate of getting-started?
├── 04_ARCHITECTURE_OVERVIEW.md     # ✅ Already archived
├── 05_EPISTEMIC_VECTORS.md         # Keep - comprehensive vector guide
├── 06_CASCADE_FLOW.md              # Verify: matches corrected CASCADE?
├── 07_INVESTIGATION_SYSTEM.md      # Review: still accurate?
├── 08_BAYESIAN_GUARDIAN.md         # Review: still exists in code?
├── 09_DRIFT_MONITOR.md             # ⚠️ Check: references old or new drift?
├── 10_PLUGIN_SYSTEM.md             # Keep - plugin docs
├── 11_DASHBOARD_MONITORING.md      # Keep - dashboard docs
├── 12_SESSION_DATABASE.md          # Keep - storage layer
├── 13_PYTHON_API.md                # Keep - API reference
├── 14_CUSTOM_PLUGINS.md            # Keep - plugin development
├── 15_CONFIGURATION.md             # Keep - config guide
├── 16_TUNING_THRESHOLDS.md         # Keep - threshold tuning
├── 17_PRODUCTION_DEPLOYMENT.md     # Keep - deployment
├── 18_MONITORING_LOGGING.md        # Keep - observability
├── 19_API_REFERENCE.md             # Review: duplicate of 13?
├── 20_TOOL_CATALOG.md              # Keep - tool reference
├── 21_TROUBLESHOOTING.md           # Keep - common issues
├── 22_FAQ.md                       # Keep - FAQs
├── 23_SESSION_CONTINUITY.md        # Keep - handoff system
├── 24_MCO_ARCHITECTURE.md          # Keep - MCO docs
├── 25_SCOPEVECTOR_GUIDE.md         # Keep - scope vectors
├── 26_CROSS_AI_COORDINATION.md     # Keep - git notes coordination
└── 27_SCHEMA_MIGRATION_GUIDE.md    # Review: still relevant?
```

**Actions per file:**
1. Read content
2. Classify: KEEP / UPDATE / ARCHIVE / MERGE
3. Note: Why (outdated / duplicate / conflicts with canonical)
4. If UPDATE: What needs changing?
5. If MERGE: Merge with which file?

**Estimated complexity:** Medium (23 files, varied content)

---

### Step 2: Audit reference/ (11 files)

**Goal:** Verify technical accuracy, remove duplicates

**Files to Check:**
```
docs/reference/
├── ARCHITECTURE_OVERVIEW.md            # ✅ Already consolidated → architecture-technical.md
├── BOOTSTRAP_LEVELS_UNIFIED.md         # ⚠️ Check: BOOTSTRAP session-level?
├── BOOTSTRAP_QUICK_REFERENCE.md        # ⚠️ Check: BOOTSTRAP session-level?
├── BOOTSTRAP_UNIFICATION_SUMMARY.md    # ⚠️ Check: BOOTSTRAP session-level?
├── CALIBRATION_SYSTEM.md               # Review: references old calibration/?
├── CANONICAL_DIRECTORY_STRUCTURE.md    # ✅ Replaced by V2
├── CHANGELOG.md                        # Keep - history
├── COMMON_ERRORS_AND_SOLUTIONS.md      # Keep - troubleshooting
├── EMPIRICA_CASCADE_WORKFLOW_SPECIFICATION.md  # ⚠️ Check: CASCADE correct?
├── EMPIRICA_FOUNDATION_SPECIFICATION.md        # ⚠️ Check: foundation correct?
├── INVESTIGATION_PROFILE_SYSTEM_SPEC.md        # Keep - investigation specs
├── NEW_SCHEMA_GUIDE.md                 # Review: schema migration complete?
├── QUICK_REFERENCE.md                  # ✅ Already consolidated → command-reference.md
├── QUICK_STATUS.md                     # Review: duplicate of command-reference?
├── SESSION_TRACKING.md                 # Review: git notes vs SQLite?
└── SESSION_VS_CASCADE_ARCHITECTURE.md  # ⚠️ Check: architecture correct?
```

**Priority checks:**
- BOOTSTRAP docs (verify session-level)
- CASCADE workflow specs (verify corrected architecture)
- Calibration system (check for old drift monitor references)
- Schema migration (is it complete?)

**Estimated complexity:** Medium-High (technical content, needs verification)

---

### Step 3: Audit guides/ (multiple subdirs)

**Goal:** Keep essential how-tos, archive experimental

**Directories:**
```
docs/guides/
├── engineering/            # SEMANTIC_ENGINEERING_GUIDELINES, SEMANTIC_ONTOLOGY
├── examples/               # Check contents
├── git/                    # BRANCH_SWITCHING_GUIDE, empirica_git, git_integration
├── learning/               # Multiple files - user-facing or dev notes?
├── protocols/              # UVL_PROTOCOL
└── setup/                  # Multiple setup guides - duplicates?
```

**Actions:**
- Engineering: Review relevance (keep if current)
- Examples: Keep if demonstrates current architecture
- Git: Keep (essential for git notes)
- Learning: Classify as user docs or dev notes
- Protocols: Keep (UVL is active)
- Setup: Check for duplicates with installation.md

**Estimated complexity:** Low-Medium (smaller files, clear purposes)

---

## Decision Criteria

### KEEP if:
- ✅ Unique content (no duplicate)
- ✅ Technically accurate (matches code)
- ✅ Matches canonical architecture (corrected CASCADE)
- ✅ Essential for users or developers

### UPDATE if:
- ⚠️ Good content but outdated (fix and keep)
- ⚠️ References old architecture (update CASCADE/BOOTSTRAP)
- ⚠️ References deprecated code (update to current)

### MERGE if:
- ⚠️ Overlaps with another doc (consolidate)
- ⚠️ Partial duplicate (merge best parts)

### ARCHIVE if:
- ❌ Completely outdated (no longer relevant)
- ❌ Describes removed features
- ❌ Superseded by newer docs
- ❌ Full duplicate (no unique content)

---

## Output Format

For each file audited, create entry:

```markdown
### File: docs/production/06_CASCADE_FLOW.md

**Classification:** UPDATE  
**Reason:** References correct CASCADE but missing git checkpoints  
**Action:** Add section on automatic git checkpoint creation  
**Lines to update:** 45-60 (PREFLIGHT section)  
**Keep/Archive/Merge:** Keep after update  
```

---

## Handoff Method (Using Empirica)

### For Acting AI to Resume:

1. **Load this handoff:**
```bash
empirica goals-discover --from-ai-id rovodev
# Find: "Complete Phase 1 documentation consolidation"
empirica goals-resume <goal-id> --ai-id <your-ai-id>
```

2. **Check git context:**
```bash
# See what we've changed
git log --oneline -20
git diff HEAD~10 docs/

# Check git notes
git notes list | grep empirica
```

3. **Start with PREFLIGHT:**
```bash
empirica preflight "Audit production/ docs for consolidation" --ai-id <your-ai-id>
```

4. **Execute investigation:**
- Read each file in production/
- Classify using criteria above
- Document findings

5. **Run CHECK periodically:**
```bash
empirica check <session-id>
# Assess: confidence, progress, blockers
```

6. **Complete with POSTFLIGHT:**
```bash
empirica postflight <session-id>
# Report: files audited, classifications, recommendations
```

---

## Expected Outcomes

### Phase 1B Complete:
- All production/ files classified (23 files)
- All reference/ files classified (11 files)
- All guides/ files classified (~20 files)
- Clear list: KEEP (30) / ARCHIVE (20+) / UPDATE (10+)

### Phase 1C: Execution
- Archive outdated files to empirica-dev
- Update files needing corrections
- Merge duplicate content
- Final count: ~30 canonical files

---

## Success Metrics

**Quantitative:**
- ✅ From 95 files → 30 files
- ✅ All duplicates removed
- ✅ All conflicts resolved
- ✅ All outdated content archived

**Qualitative:**
- ✅ Clear navigation (easy to find what you need)
- ✅ Consistent architecture (matches canonical prompt & code)
- ✅ Accurate content (matches current implementation)
- ✅ No confusion (one source of truth per topic)

---

## Technical Debt to Note

### CASCADE Still Uses Old DriftMonitor ⚠️

**Current:**
```python
# Line 76 in empirica/core/metacognitive_cascade/metacognitive_cascade.py
from empirica.calibration.parallel_reasoning import ParallelReasoningSystem, DriftMonitor
```

**Should be:**
```python
from empirica.core.drift import MirrorDriftMonitor
```

**Impact on docs:**
- Any docs referencing drift detection should note this transition
- docs/production/09_DRIFT_MONITOR.md may need update
- Some references to "parallel reasoning" may be outdated

**Recommendation:** Note this in docs, plan separate migration task

---

## Resources for Acting AI

**Key documents to reference:**
- `docs/reference/CANONICAL_DIRECTORY_STRUCTURE_V2.md` - Codebase truth
- `docs/architecture/GIT_CHECKPOINT_ARCHITECTURE.md` - Git notes architecture
- `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md` - Corrected CASCADE
- `docs/DUPLICATE_ANALYSIS.md` - What we've already consolidated
- `docs/PHASE1_COMPLETE.md` - Phase 1A summary

**Git context:**
- Check recent commits for documentation changes
- Check git notes for any session continuity data
- Review diffs to see what's been updated

**CLI commands:**
```bash
# Discovery
empirica goals-discover --from-ai-id rovodev

# Resume
empirica goals-resume <goal-id> --ai-id <your-ai-id>

# Workflow
empirica preflight "task" --ai-id <your-ai-id>
empirica check <session-id>
empirica postflight <session-id>

# Create handoff when done
empirica handoff-create <session-id> \
  --summary "Audited N files, classified as KEEP/ARCHIVE/UPDATE" \
  --findings "Found X duplicates, Y outdated, Z conflicts"
```

---

## Questions for Acting AI to Answer

1. **Which production/ docs are still accurate?**
   - Check against current code implementation
   - Verify CASCADE architecture matches canonical

2. **Which reference/ docs conflict with corrected architecture?**
   - BOOTSTRAP session-level (not per-cascade)
   - CASCADE implicit work (not explicit phases)
   - Drift monitor unified (not parallel reasoning)

3. **Where are hidden duplicates?**
   - Content overlap between production/ and reference/
   - Similar guides in different locations
   - Redundant troubleshooting sections

4. **What needs updating vs archiving?**
   - Good content but outdated → UPDATE
   - Superseded or obsolete → ARCHIVE
   - Completely wrong → DELETE (rare)

---

## Timeline Estimate

**Per Acting AI:**
- Phase 1B (Audit): 1-2 days (reading and classifying)
- Phase 1C (Execute): 1 day (archive/update/merge)

**Total Phase 1 completion:** ~3 days with one focused AI

**Parallel work possible:**
- AI-1: Audit production/ (23 files)
- AI-2: Audit reference/ (11 files)
- AI-3: Audit guides/ (~20 files)
- Consolidate findings, execute together

---

## Epistemic State for Handoff

**What I know well (0.8-0.9):**
- Git notes integration architecture
- CASCADE corrected architecture (BOOTSTRAP session-level)
- Which duplicates we've already consolidated
- Documentation structure and goals

**What needs investigation (0.3-0.5):**
- Content accuracy of production/ docs
- Whether reference/ docs conflict with canonical
- Hidden duplicates we haven't found yet

**Confidence to proceed:** 0.7
- Clear plan and criteria
- Good context and resources
- Well-defined success metrics
- Just need execution time

---

**Handoff complete. Ready for acting AI to resume with full context.** ✅
