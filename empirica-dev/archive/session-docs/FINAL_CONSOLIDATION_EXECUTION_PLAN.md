# Final Documentation Consolidation - Execution Plan

**Date:** 2025-01-XX  
**Goal:** Simplify user-facing docs, organize production reference, remove deprecated content

---

## Architecture Understanding

### Tier 1: User Docs (docs/ root) - Simple Overview
**Audience:** New users, getting started  
**Target:** 10-15 files, readable in 1-2 hours  
**Focus:** Core Empirica (what one AI does)

### Tier 2: Production Docs (docs/production/) - Comprehensive Reference  
**Audience:** Advanced users, integrators, developers  
**Target:** 27 files (keep almost all)  
**Focus:** Complete system reference (Core + Advanced features)  
**Status:** Already mostly correct, just needs organization

### Tier 3: Technical Specs (docs/reference/) - Deep Architecture
**Audience:** Contributors, maintainers  
**Target:** ~10 files  
**Focus:** Implementation specs

---

## Decision Matrix (Based on User Feedback)

### 1. Quick Starts - CONSOLIDATE ✅
**Current:** 4 separate files (CLI, MCP, AI agent, MCP AI)  
**Action:** Merge into ONE `getting-started.md` with sections  
**Rationale:** Simpler for users, less maintenance

### 2. START_HERE - MERGE ✅
**Current:** 00_START_HERE.md  
**Action:** Merge content into README.md  
**Rationale:** README.md is the natural entry point

### 3. AI Patterns - KEEP ✅
**Current:** AI_VS_AGENT_EMPIRICA_PATTERNS.md  
**Action:** Keep as separate doc (useful reference)  
**Rationale:** Distinct concept worth its own doc

### 4. Onboarding - MERGE ✅
**Current:** ONBOARDING_GUIDE.md  
**Action:** Merge into getting-started.md as interactive section  
**Rationale:** Part of getting started experience

### 5. Bootstrap Docs - ARCHIVE ✅
**Current:** 3 bootstrap docs in reference/  
**Action:** Archive to empirica-dev (historical)  
**Rationale:** SESSION-level architecture is now canonical

---

## Execution Steps

### STEP 1: Consolidate docs/ Root (Core User Docs)

**Keep as-is (already consolidated):**
- ✅ `installation.md` (13K)
- ✅ `architecture.md` (11K)  
- ✅ `getting-started.md` (7.4K)

**Create new:**
- 📝 `quick-reference.md` - Command cheat sheet (consolidate from reference/)
- 📝 `troubleshooting.md` - Common issues (06_TROUBLESHOOTING.md renamed)

**Enhance existing:**
- 📝 `getting-started.md` - Add content from:
  - 03_CLI_QUICKSTART.md (CLI section)
  - 04_MCP_QUICKSTART.md (MCP section)
  - ONBOARDING_GUIDE.md (interactive wizard section)

**Keep separate:**
- ✅ `AI_VS_AGENT_EMPIRICA_PATTERNS.md` - Usage patterns
- ✅ `README.md` - Hub (merge 00_START_HERE.md content)

**Archive/remove:**
- ❌ `00_START_HERE.md` → merge into README.md
- ❌ `01_a_AI_AGENT_START.md` → merge into getting-started.md
- ❌ `01_b_MCP_AI_START.md` → merge into getting-started.md
- ❌ `03_CLI_QUICKSTART.md` → merge into getting-started.md
- ❌ `04_MCP_QUICKSTART.md` → merge into getting-started.md
- ❌ `05_ARCHITECTURE.md` → already consolidated to architecture.md
- ❌ `06_TROUBLESHOOTING.md` → rename to troubleshooting.md
- ❌ `ONBOARDING_GUIDE.md` → merge into getting-started.md
- ❌ `ALL_PLATFORMS_INSTALLATION.md` → already consolidated to installation.md
- ❌ `ALL_PLATFORMS_QUICK_REFERENCE.md` → already archived

**Final docs/ root: ~8 files**
1. README.md (hub, links to all docs)
2. installation.md
3. getting-started.md (enhanced)
4. architecture.md
5. quick-reference.md
6. troubleshooting.md
7. AI_VS_AGENT_EMPIRICA_PATTERNS.md
8. CONTRIBUTING.md

---

### STEP 2: Organize docs/production/ (Reference Docs)

**Add section header to 00_COMPLETE_SUMMARY.md:**

```markdown
# Empirica Complete Documentation

## Using This Documentation

### Core Empirica (Production-Ready ✅)
**Start here if you're new or deploying to production.**

Essential guides:
- 00-05: Overview, Installation, Usage, Architecture, Vectors, CASCADE
- 09: Drift Monitor (temporal self-validation)
- 12-13: Session Database, Python API
- 20: Tool Catalog (all 23 MCP tools)
- 23: Session Continuity (handoffs, resumption)

### Advanced Features (Experimental ⚠️)
**Explore these for multi-AI orchestration and advanced capabilities.**

Experimental:
- 08: Bayesian Guardian
- 14-19: Custom Plugins, Configuration, Tuning, Deployment, Monitoring, API
- 21-22: Advanced Troubleshooting, FAQ
- 24-29: MCO, Personas, ScopeVector, Cross-AI, Schema, Decision Logic

**Note:** Advanced features are provided without production guarantees and may evolve.
```

**Minor updates:**
- ✅ Verify 00-09 match corrected CASCADE architecture
- ✅ Add note about MirrorDriftMonitor in 09_DRIFT_MONITOR.md
- ✅ Mark experimental features clearly

**No consolidation - these are comprehensive references!**

**Final production/: 27 files (organized, not consolidated)**

---

### STEP 3: Clean docs/reference/ (Technical Specs)

**Archive to empirica-dev/docs-reference-deprecated/:**
1. ❌ `CANONICAL_DIRECTORY_STRUCTURE.md` (replaced by V2)
2. ❌ `BOOTSTRAP_LEVELS_UNIFIED.md` (session-level architecture now canonical)
3. ❌ `BOOTSTRAP_QUICK_REFERENCE.md` (superseded)
4. ❌ `BOOTSTRAP_UNIFICATION_SUMMARY.md` (historical)
5. ❌ `NEW_SCHEMA_GUIDE.md` (if schema migration complete)

**Keep:**
1. ✅ `CANONICAL_DIRECTORY_STRUCTURE_V2.md` (source of truth)
2. ✅ `architecture-technical.md` (deep dive)
3. ✅ `command-reference.md` (command cheat sheet)
4. ✅ `EMPIRICA_CASCADE_WORKFLOW_SPECIFICATION.md` (spec)
5. ✅ `EMPIRICA_FOUNDATION_SPECIFICATION.md` (spec)
6. ✅ `SESSION_VS_CASCADE_ARCHITECTURE.md` (core concept)
7. ✅ `CALIBRATION_SYSTEM.md` (if accurate)
8. ✅ `INVESTIGATION_PROFILE_SYSTEM_SPEC.md` (spec)
9. ✅ `CHANGELOG.md` (history)
10. ✅ `COMMON_ERRORS_AND_SOLUTIONS.md` (troubleshooting)

**Final reference/: ~10 files**

---

### STEP 4: Simplify docs/guides/

**Review each subdirectory:**

**git/ (3 files):**
- ✅ Keep all (essential for git notes integration)

**protocols/ (1 file):**
- ✅ Keep UVL_PROTOCOL.md

**setup/ (multiple files):**
- Review for duplicates with installation.md
- Archive duplicates

**engineering/ (2 files):**
- ✅ Keep (contributor docs)

**learning/ (multiple files):**
- Review: User guides? Keep
- Review: Dev notes? Archive to empirica-dev

**examples/ (unknown):**
- ✅ Keep if demonstrates core features
- ❌ Archive if outdated

**Estimated final guides/: ~10-15 files**

---

### STEP 5: Enhance Core Docs with Links

**Update architecture.md to link to production/:**

```markdown
# Empirica Architecture

## Core Concepts

[Brief overview of SESSION → BOOTSTRAP → CASCADE...]

## Deep Dive References

For comprehensive technical details:
- **[Complete System Overview](production/00_COMPLETE_SUMMARY.md)** - Start here
- **[13 Epistemic Vectors](production/05_EPISTEMIC_VECTORS.md)** - Full vector guide
- **[CASCADE Flow Details](production/06_CASCADE_FLOW.md)** - Phase-by-phase
- **[All 23 MCP Tools](production/20_TOOL_CATALOG.md)** - Complete catalog
- **[Session Continuity](production/23_SESSION_CONTINUITY.md)** - Handoffs & resumption
- **[Git Checkpoints](architecture/GIT_CHECKPOINT_ARCHITECTURE.md)** - Technical deep dive

## Advanced Features (Experimental)

⚠️ These features are experimental and may change:
- **[MCO Architecture](production/24_MCO_ARCHITECTURE.md)** - Persona orchestration
- **[Cross-AI Coordination](production/26_CROSS_AI_COORDINATION.md)** - Multi-AI workflows
- **[ScopeVector Guide](production/25_SCOPEVECTOR_GUIDE.md)** - Goal scoping
- **[Decision Logic](production/28_DECISION_LOGIC.md)** - How CASCADE decides

Use Core Empirica for production deployment.
```

---

## File Cleanup Summary

### Files to Archive (empirica-dev):
**From docs/ root:** (9 files)
- 00_START_HERE.md
- 01_a_AI_AGENT_START.md
- 01_b_MCP_AI_START.md
- 03_CLI_QUICKSTART.md
- 04_MCP_QUICKSTART.md
- 05_ARCHITECTURE.md (old version)
- 06_TROUBLESHOOTING.md (will be renamed)
- ONBOARDING_GUIDE.md
- ALL_PLATFORMS_INSTALLATION.md (old version)

**From docs/reference/:** (4-5 files)
- CANONICAL_DIRECTORY_STRUCTURE.md
- BOOTSTRAP_LEVELS_UNIFIED.md
- BOOTSTRAP_QUICK_REFERENCE.md
- BOOTSTRAP_UNIFICATION_SUMMARY.md
- NEW_SCHEMA_GUIDE.md (if complete)

**From docs/guides/:** (5-10 files estimated)
- Duplicates of installation.md
- Outdated examples
- Dev notes (not user guides)

**Total to archive:** ~20-25 files

---

## Final File Count

**Before:** ~95 files  
**After:** ~60-70 files

**Breakdown:**
- docs/ root: 8 files (simple overview)
- production/: 27 files (comprehensive reference)
- reference/: 10 files (technical specs)
- guides/: 10-15 files (practical how-tos)
- architecture/: 2-3 files (deep dives)
- system-prompts/: 4 files (canonical)

**Plus:** website/, tests/, examples/ (unchanged)

---

## Success Criteria

### Quantitative
- ✅ docs/ root: 8 essential files (down from ~13)
- ✅ production/: 27 organized files (marked Core vs Advanced)
- ✅ reference/: 10 files (down from ~16)
- ✅ guides/: 10-15 files (down from ~20+)
- ✅ ~20-25 files archived to empirica-dev

### Qualitative
- ✅ Clear "Core vs Advanced" distinction
- ✅ Core docs readable in 1-2 hours
- ✅ No duplicate quick starts
- ✅ Production docs organized by support level
- ✅ All docs link to deeper references
- ✅ Deprecated content archived

---

## Timeline

**With one acting AI:**
- Step 1 (Core docs): 0.5 day
- Step 2 (Production organization): 0.5 day
- Step 3 (Reference cleanup): 0.5 day
- Step 4 (Guides review): 0.5 day
- Step 5 (Enhancement): 0.5 day

**Total:** 2-3 days

**With parallel AIs:**
- AI-1: Steps 1 + 5 (1 day)
- AI-2: Steps 2 + 3 (1 day)
- AI-3: Step 4 (0.5 day)

**Total:** 1 day

---

## Next Action

**Execute Step 1 now?** Or hand off to acting AIs?

**Commands for acting AI:**
```bash
# Discover goal
empirica goals-discover --from-ai-id rovodev

# Resume
empirica goals-resume 661ed26e-ae7c-4606-8b85-c99d6ff8db3a --ai-id <your-ai-id>

# Start
empirica preflight "Execute Step 1: Consolidate core user docs" --ai-id <your-ai-id>
```

---

**Status:** Ready for execution ✅  
**Plan:** Consolidate core docs, organize production reference, clean deprecated
