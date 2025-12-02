# Revised Documentation Consolidation Plan

**Date:** 2025-01-XX  
**Based on:** User clarification about Empirica Core vs Advanced Features

---

## Key Understanding

### Empirica Core (Production-Ready)
**What one AI does:**
- BOOTSTRAP → PREFLIGHT → CASCADE → CHECK → ACT → POSTFLIGHT
- 13 epistemic vectors
- Git checkpoints (automatic)
- Goal/subtask orchestration
- Session continuity (handoffs)
- SQLite + JSON + Git storage
- 23 MCP tools
- CLI interface

**Support level:** ✅ Production-ready, fully supported

---

### Advanced Features (Experimental/Optional)
**Multi-AI orchestration stack:**
- Persona orchestration (MCO)
- Dynamic routing (Sentinel)
- Bayesian Guardian
- Cognitive Vault
- Cross-AI coordination (experimental)
- Component plugins (code intelligence, workspace awareness, etc.)

**Support level:** ⚠️ Provided without promises, may be incomplete/changing

---

## Documentation Architecture

### Tier 1: User-Facing (website/simplified_content/)
**Audience:** End users, AI agents getting started  
**Content:** High-level concepts, quick start, use cases  
**Status:** Already exists, needs minor updates

---

### Tier 2: Core Docs (docs/ root) - Quick Overview
**Audience:** Users who want to understand and use Empirica Core  
**Target:** ~10-15 essential files  
**Content:**
- Installation
- Getting started (first CASCADE)
- Architecture overview (core concepts)
- Quick reference (common commands)
- Troubleshooting

**Goal:** Someone can read these in 1-2 hours and understand core Empirica

---

### Tier 3: Production Docs (docs/production/) - Deep Reference
**Audience:** Developers, advanced users, integrators  
**Target:** Keep all 30 files (00-29 are mostly correct)  
**Content:**
- Complete system reference
- All 13 vectors explained
- All 23 tools documented
- Advanced features (MCO, Sentinel, etc.)
- Configuration and tuning

**Goal:** Comprehensive reference for production deployment

---

### Tier 4: Technical Specs (docs/reference/)
**Audience:** Contributors, maintainers  
**Target:** ~10 files (remove outdated)  
**Content:**
- Canonical directory structure
- Schema specifications
- Architecture deep dives
- API reference (will be auto-generated via MkDocs Phase 2)

---

## Revised Consolidation Strategy

### Phase 1: Simplify Core User Docs (docs/ root)

**Current state:** ~13 files, some numbered, some not  
**Target:** ~10-15 essential files with clear names

**Keep & Enhance:**
1. `installation.md` ✅ (already consolidated)
2. `architecture.md` ✅ (already consolidated)
3. `getting-started.md` ✅ (already consolidated)
4. `troubleshooting.md` (06_TROUBLESHOOTING.md renamed)
5. `quick-reference.md` (command cheat sheet)

**Review & Potentially Keep:**
6. `00_START_HERE.md` - Hub page?
7. `01_a_AI_AGENT_START.md` - Quick start for AI agents?
8. `01_b_MCP_AI_START.md` - MCP-specific quick start?
9. `03_CLI_QUICKSTART.md` - CLI quick start?
10. `04_MCP_QUICKSTART.md` - MCP quick start?
11. `AI_VS_AGENT_EMPIRICA_PATTERNS.md` - Usage patterns?
12. `ONBOARDING_GUIDE.md` - Interactive onboarding?

**Questions to answer:**
- Do we need separate CLI vs MCP quick starts? Or consolidate into getting-started.md?
- Do we need separate AI agent vs MCP AI starts? Or consolidate?
- Is 00_START_HERE.md useful as a hub, or does README.md cover it?

**Estimated duplicates to consolidate:** 3-5 files

---

### Phase 2: Organize Production Docs (docs/production/)

**Current state:** 30 files (00-29), mostly correct  
**Action:** Minor fixes, NOT consolidation

**Keep all 30 files, but:**
1. Verify 00-05 match corrected CASCADE architecture
2. Update any references to old DriftMonitor → MirrorDriftMonitor
3. Mark advanced features (MCO, Sentinel, Bayesian Guardian) as experimental
4. Add "Core vs Advanced" section to 00_COMPLETE_SUMMARY.md

**Section breakdown:**
- **Core Empirica** (00-13, 20, 23): Production-ready, supported
- **Advanced Features** (14-19, 21-22, 24-29): Experimental, no guarantees

**No consolidation needed - these are comprehensive references!**

---

### Phase 3: Clean Reference Docs (docs/reference/)

**Current state:** ~16 files  
**Target:** ~10 files (remove outdated)

**Review for removal/archive:**
1. `CANONICAL_DIRECTORY_STRUCTURE.md` - ✅ Replaced by V2
2. `NEW_SCHEMA_GUIDE.md` - Schema migration complete? Archive if yes
3. `BOOTSTRAP_LEVELS_UNIFIED.md` - Still relevant?
4. `BOOTSTRAP_QUICK_REFERENCE.md` - Duplicate of production/02?
5. `BOOTSTRAP_UNIFICATION_SUMMARY.md` - Historical? Archive?

**Keep:**
6. `CANONICAL_DIRECTORY_STRUCTURE_V2.md` ✅
7. `ARCHITECTURE_OVERVIEW.md` (renamed to architecture-technical.md) ✅
8. `QUICK_REFERENCE.md` (renamed to command-reference.md) ✅
9. `EMPIRICA_CASCADE_WORKFLOW_SPECIFICATION.md` - Technical spec
10. `EMPIRICA_FOUNDATION_SPECIFICATION.md` - Foundation spec
11. `SESSION_VS_CASCADE_ARCHITECTURE.md` - Core concept
12. `CALIBRATION_SYSTEM.md` - If still accurate
13. `CHANGELOG.md` - History
14. `COMMON_ERRORS_AND_SOLUTIONS.md` - Troubleshooting

**Estimated to archive:** 3-5 files

---

### Phase 4: Simplify Guides (docs/guides/)

**Current subdirectories:**
- engineering/ (2 files)
- examples/ (?)
- git/ (3 files)
- learning/ (multiple files)
- protocols/ (1 file)
- setup/ (multiple files)

**Strategy:**
- **git/**: Keep (essential for git notes)
- **protocols/**: Keep (UVL protocol)
- **setup/**: Review for duplicates with installation.md
- **engineering/**: Keep if relevant to contributors
- **learning/**: Archive if dev notes, keep if user guides
- **examples/**: Keep if demonstrates core features

**Estimated to archive:** 5-10 files

---

## Final Target Structure

```
docs/
├── (root) - 10-15 core user docs
│   ├── installation.md          # Cross-platform setup
│   ├── getting-started.md       # First CASCADE
│   ├── architecture.md          # Core concepts
│   ├── troubleshooting.md       # Common issues
│   ├── quick-reference.md       # Command cheat sheet
│   ├── mcp-quickstart.md        # MCP-specific (if needed)
│   ├── cli-quickstart.md        # CLI-specific (if needed)
│   └── ...
│
├── production/ - 30 comprehensive references
│   ├── 00-13: Core Empirica (production-ready)
│   ├── 14-29: Advanced features (experimental)
│   └── Clear labeling of core vs advanced
│
├── reference/ - ~10 technical specs
│   ├── CANONICAL_DIRECTORY_STRUCTURE_V2.md
│   ├── architecture-technical.md
│   ├── CASCADE workflow spec
│   ├── Foundation spec
│   └── ...
│
├── guides/ - ~10-15 practical how-tos
│   ├── git/ (git notes integration)
│   ├── protocols/ (UVL)
│   └── ...
│
├── architecture/ - Deep dives
│   ├── GIT_CHECKPOINT_ARCHITECTURE.md
│   └── ...
│
└── system-prompts/ - Canonical (already good)
    ├── CANONICAL_SYSTEM_PROMPT.md
    └── ...
```

**Total target:** ~65-75 files (down from ~95)

---

## Specific Actions

### A. Consolidate docs/ root quick starts

**Current:**
- 03_CLI_QUICKSTART.md
- 04_MCP_QUICKSTART.md
- 01_a_AI_AGENT_START.md
- 01_b_MCP_AI_START.md

**Options:**

**Option 1:** Consolidate into getting-started.md with sections
```markdown
# Getting Started

## Using Empirica (Choose Your Interface)
- CLI (command-line)
- MCP (AI assistants)
- Python API

## Your First CASCADE
- PREFLIGHT → investigate → CHECK → ACT → POSTFLIGHT
```

**Option 2:** Keep separate quick starts for different audiences
- getting-started.md (general)
- mcp-quickstart.md (AI assistants)
- cli-quickstart.md (command-line users)

**Recommendation:** Option 1 (consolidate) for simplicity

---

### B. Mark Advanced Features in Production Docs

**Add to docs/production/00_COMPLETE_SUMMARY.md:**

```markdown
## Documentation Structure

### Core Empirica (Production-Ready ✅)
These features are fully supported and production-ready:
- 00-05: Overview, Quick Start, Installation, Usage, Architecture, Vectors
- 06: CASCADE Flow
- 07: Investigation System
- 09: Drift Monitor (MirrorDriftMonitor)
- 10-13: Plugins, Dashboard, Session Database, Python API
- 20: Tool Catalog (23 MCP tools)
- 23: Session Continuity

### Advanced Features (Experimental ⚠️)
These features are provided without guarantees and may change:
- 08: Bayesian Guardian
- 14-19: Configuration, Tuning, Deployment (advanced)
- 21-22: FAQ, Troubleshooting (advanced)
- 24-29: MCO, Personas, Cross-AI, Sentinel, Cognitive Vault

**Use Core Empirica for production. Advanced features for experimentation.**
```

---

### C. Archive Outdated Reference Docs

**To empirica-dev/docs-reference-deprecated/:**
1. CANONICAL_DIRECTORY_STRUCTURE.md (replaced by V2)
2. BOOTSTRAP_UNIFICATION_SUMMARY.md (if historical)
3. NEW_SCHEMA_GUIDE.md (if migration complete)

**Criteria:** 
- Superseded by newer docs
- Historical/one-time migration guides
- No longer accurate

---

### D. Enhance Core Docs with Links

**Update docs/architecture.md:**
```markdown
# Empirica Architecture

## Core Concepts
- [Epistemic vectors explained](quick-reference.md#vectors)
- [CASCADE workflow](getting-started.md#your-first-cascade)
- [Git checkpoints](getting-started.md#automatic-checkpoints)

## Deep Dives
For comprehensive technical details, see:
- [Complete Architecture Reference](production/04_ARCHITECTURE_OVERVIEW.md)
- [All 23 Tools](production/20_TOOL_CATALOG.md)
- [Git Checkpoint Architecture](architecture/GIT_CHECKPOINT_ARCHITECTURE.md)

## Advanced Features (Experimental)
For multi-AI orchestration and advanced features:
- [MCO Architecture](production/24_MCO_ARCHITECTURE.md)
- [Cross-AI Coordination](production/26_CROSS_AI_COORDINATION.md)
- [Sentinel & Cognitive Vault](production/24_MCO_ARCHITECTURE.md#sentinel)

⚠️ Advanced features are experimental and may change.
```

---

## Execution Plan

### Day 1: Core Docs Consolidation
1. Review docs/ root files (00-06, 01_a, 01_b, 03, 04, AI_VS_AGENT, ONBOARDING)
2. Decide: Consolidate quick starts or keep separate?
3. Merge or archive duplicates
4. Enhance architecture.md with links to production/

**Result:** ~10-15 essential core docs

---

### Day 2: Production Docs Organization
1. Add "Core vs Advanced" section to 00_COMPLETE_SUMMARY.md
2. Review 00-05 for CASCADE architecture accuracy
3. Update any DriftMonitor references
4. Mark experimental features clearly

**Result:** 30 organized production docs (no consolidation)

---

### Day 3: Reference & Guides Cleanup
1. Archive outdated reference docs (3-5 files)
2. Review guides/ for duplicates (5-10 files)
3. Update cross-references

**Result:** ~10 reference docs, ~10-15 guides

---

## Success Metrics

**Quantitative:**
- From ~95 files → ~65-75 files
- Core docs: 10-15 (simple overview)
- Production docs: 30 (comprehensive, organized)
- Reference: 10 (technical specs)
- Guides: 10-15 (practical how-tos)

**Qualitative:**
- ✅ Clear "Core vs Advanced" distinction
- ✅ Core docs readable in 1-2 hours
- ✅ Production docs comprehensive but organized
- ✅ No duplicate content
- ✅ All docs link to deeper references

---

## Questions for User

1. **Quick starts:** Consolidate into one getting-started.md, or keep separate CLI/MCP versions?
2. **Start files:** Keep 00_START_HERE.md as hub, or merge into README.md?
3. **AI patterns:** Keep AI_VS_AGENT_EMPIRICA_PATTERNS.md or merge into architecture.md?
4. **Onboarding:** Keep ONBOARDING_GUIDE.md or merge into getting-started.md?
5. **Reference bootstrap docs:** Archive old bootstrap docs or keep for reference?

---

**Status:** Plan ready for execution  
**Next:** Answer 5 questions above, then execute consolidation
