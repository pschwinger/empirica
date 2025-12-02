# Phase 1: Documentation Consolidation Plan

**Goal:** Archive outdated content, consolidate duplicates, create fresh docs matching actual codebase

**Timeline:** 2-3 days

---

## Step 1: Archive Outdated Content (Day 1 Morning)

### Criteria for "Outdated":
- References old architecture (BOOTSTRAP in CASCADE flow)
- Describes removed features
- Conflicts with canonical system prompt
- Superseded by newer docs

### Candidates for Archive:

**Check these files for outdated content:**
```bash
# Bootstrap docs - may describe old session model
docs/reference/BOOTSTRAP_LEVELS_UNIFIED.md
docs/reference/BOOTSTRAP_QUICK_REFERENCE.md
docs/reference/BOOTSTRAP_UNIFICATION_SUMMARY.md

# Schema migration docs - may be historical
docs/reference/NEW_SCHEMA_GUIDE.md

# Session tracking - may conflict with git notes
docs/reference/SESSION_TRACKING.md

# Old changelog entries
docs/reference/CHANGELOG.md (review for relevance)
```

**Action:** Read each, mark as KEEP/ARCHIVE/UPDATE

---

## Step 2: Identify Duplicates (Day 1 Afternoon)

### Known Duplicates (3 sets):

#### Set 1: Installation Guides
1. `docs/02_INSTALLATION.md`
2. `docs/production/02_INSTALLATION.md`
3. `docs/ALL_PLATFORMS_INSTALLATION.md`

**Action:** 
- Read all three
- Merge best content into ONE canonical installation.md
- Move others to empirica-dev/duplicates/

#### Set 2: Architecture Docs
1. `docs/05_ARCHITECTURE.md`
2. `docs/production/04_ARCHITECTURE_OVERVIEW.md`
3. `docs/reference/ARCHITECTURE_OVERVIEW.md`

**Action:**
- Read all three
- Verify CASCADE model is correct
- Merge into ONE canonical architecture.md
- Move others to empirica-dev/duplicates/

#### Set 3: Quick Reference
1. `docs/ALL_PLATFORMS_QUICK_REFERENCE.md`
2. `docs/production/01_QUICK_START.md`
3. `docs/reference/QUICK_REFERENCE.md`

**Action:**
- Read all three
- Merge into ONE canonical quick-reference.md
- Move others to empirica-dev/duplicates/

---

## Step 3: Consolidate Production Docs (Day 2)

### docs/production/ (27 files) - Audit for relevance

**Keep these (likely still accurate):**
- 05_EPISTEMIC_VECTORS.md ✅
- 10_PLUGIN_SYSTEM.md ✅
- 12_SESSION_DATABASE.md ✅
- 13_PYTHON_API.md ✅
- 14_CUSTOM_PLUGINS.md ✅

**Review these (may be outdated):**
- 06_CASCADE_FLOW.md (verify matches corrected architecture)
- 07_INVESTIGATION_SYSTEM.md (check if still current)
- 08_BAYESIAN_GUARDIAN.md (verify implementation)
- 09_DRIFT_MONITOR.md (verify implementation)

**Consolidate these (duplicates):**
- 01_QUICK_START.md → merge with Set 3
- 02_INSTALLATION.md → merge with Set 1
- 04_ARCHITECTURE_OVERVIEW.md → merge with Set 2

**Action:** Create audit spreadsheet, mark each file

---

## Step 4: Create Fresh Consolidated Docs (Day 2-3)

### Target Structure (30 files max):

```
docs/
├── index.md                    # Quick overview + navigation
├── getting-started.md          # Installation + first steps (consolidated Set 1)
├── architecture.md             # System overview (consolidated Set 2)
├── quick-reference.md          # Command cheat sheet (consolidated Set 3)
│
├── reference/                  # Technical specifications
│   ├── epistemic-vectors.md    # 13 vectors explained
│   ├── cascade-workflow.md     # Phase-by-phase details
│   ├── cli-commands.md         # All CLI commands
│   ├── mcp-tools.md            # All 23 MCP tools
│   ├── python-api.md           # API class reference
│   └── git-integration.md      # Git notes architecture
│
├── guides/                     # How-to guides
│   ├── first-cascade.md        # Tutorial: Your first workflow
│   ├── goal-orchestration.md   # Using goals and subtasks
│   ├── multi-ai-coordination.md # Cross-AI collaboration
│   ├── contributing.md         # How to contribute
│   ├── testing.md              # Running tests
│   └── troubleshooting.md      # Common issues
│
├── architecture/               # Deep dives
│   ├── session-structure.md    # SESSION → BOOTSTRAP → GOAL flow
│   ├── storage-layers.md       # SQLite + JSON + Git notes
│   ├── calibration-system.md   # PREFLIGHT → CHECK → POSTFLIGHT
│   ├── drift-monitor.md        # Confidence drift detection
│   └── plugin-system.md        # Plugin architecture
│
└── system-prompts/             # Already good! ✅
    ├── CANONICAL_SYSTEM_PROMPT.md
    ├── CUSTOMIZATION_GUIDE.md
    └── README.md
```

**Total:** ~25-30 files (down from 101)

---

## Step 5: Grab Resources from Live Site

### Assets to Save:
- ✅ `preflight_postflight_comparison.svg` (already saved from scrape)
- Diagrams from live site
- Any other visual resources
- Link structures

**Action:**
```bash
# Download assets from live site
wget -r -np -nH --cut-dirs=1 -A svg,png,jpg https://nubaeon.github.io/empirica/assets/

# Save in docs/assets/ or website/assets/
```

---

## Step 6: Validate Against Codebase (Day 3)

### Verification Checklist:

For each consolidated doc, verify:
- [ ] Code examples actually work
- [ ] CLI commands match `empirica --help`
- [ ] MCP tools match actual implementation
- [ ] Architecture matches canonical system prompt
- [ ] API references match actual classes/methods
- [ ] No references to removed features

**Method:**
```bash
# Test all code examples
# Run all CLI commands
# Check Python imports
# Verify MCP tool names
```

---

## Execution Plan

### Day 1 Morning: Archive Sweep
```bash
# Create archive tracking
mkdir -p ../empirica-dev/docs-outdated/

# Review and move outdated files
# Document what was archived and why
```

### Day 1 Afternoon: Duplicate Analysis
```bash
# Read all three sets of duplicates
# Create comparison notes
# Identify best content from each
```

### Day 2 Morning: Merge Duplicates
```bash
# Create consolidated installation.md
# Create consolidated architecture.md
# Create consolidated quick-reference.md
# Move originals to empirica-dev/duplicates/
```

### Day 2 Afternoon: Production Audit
```bash
# Review all 27 production docs
# Mark KEEP/ARCHIVE/UPDATE
# Update files that need corrections
```

### Day 3: Final Structure
```bash
# Reorganize into target structure
# Write any missing essential docs
# Validate all code examples
# Update cross-references
```

---

## Success Criteria

**Quantitative:**
- ✅ From 101 files → ~30 files
- ✅ Zero duplicate content
- ✅ All code examples tested
- ✅ All CLI commands verified

**Qualitative:**
- ✅ Clear navigation (easy to find what you need)
- ✅ Consistent architecture (matches canonical prompt)
- ✅ Up-to-date content (matches current codebase)
- ✅ No confusion (one source of truth for each topic)

---

## Tracking Progress

### Create audit spreadsheet:
```csv
File,Status,Action,Notes,Done
docs/02_INSTALLATION.md,Duplicate,Merge,Keep best parts,[ ]
docs/production/02_INSTALLATION.md,Duplicate,Archive,Less detail,[ ]
docs/ALL_PLATFORMS_INSTALLATION.md,Duplicate,Archive,Outdated,[ ]
...
```

---

## Questions to Answer During Audit

1. **Bootstrap docs**: Do they match session-level architecture?
2. **CASCADE docs**: Do they show BOOTSTRAP correctly?
3. **API docs**: Do they match actual Python classes?
4. **CLI docs**: Do they match `empirica --help` output?
5. **Examples**: Do code snippets actually work?

---

**Ready to start Phase 1?**

Next: Begin with duplicate analysis (2-3 hours) to identify quick wins.
