# Empirica Documentation Pruning Plan

**Generated:** 2025-11-21  
**Based on:** Pattern matching against current system  
**Strategy:** Categorize by PURPOSE (production vs dev) not currency

---

## 📊 Analysis Summary

**Total documentation:** 168 markdown files (2.8MB)

**Breakdown by purpose:**
- ✅ **Production-ready:** 73 files → KEEP in main repo
- 📦 **Dev/internal:** 62 files → MOVE to empirica-dev
- 🔮 **Vision/research:** 10 files → MOVE to empirica-dev/vision
- 🧪 **Experimental:** 3 files → DECIDE (keep or move)
- ❓ **Uncategorized:** 20 files → REVIEW & CATEGORIZE

**Key insight:** Docs are mostly CURRENT (not outdated), but **too many dev docs mixed with user docs**.

---

## 🎯 Pruning Strategy

### Keep in Production Repo (73 files)

**Top-level guides (10 files):**
```
docs/
├── 00_START_HERE.md                    ✅ Entry point
├── 01_a_AI_AGENT_START.md              ✅ User onboarding
├── 01_b_MCP_AI_START.md                ✅ MCP setup
├── 02_INSTALLATION.md                  ✅ Install guide
├── 03_CLI_QUICKSTART.md                ✅ CLI tutorial
├── 04_MCP_QUICKSTART.md                ✅ MCP tutorial
├── 05_ARCHITECTURE.md                  ✅ System overview
├── 06_TROUBLESHOOTING.md               ✅ User troubleshooting
├── ONBOARDING_GUIDE.md                 ✅ New user guide
├── ALL_PLATFORMS_INSTALLATION.md       ✅ Cross-platform
├── ALL_PLATFORMS_QUICK_REFERENCE.md    ✅ Quick reference
└── README.md                           ✅ Docs index
```

**Production user guides (29 files):**
```
docs/production/
├── 01_QUICK_START.md                   ✅
├── 02_INSTALLATION.md                  ✅
├── 03_BASIC_WORKFLOW.md                ✅
├── 04_CASCADE_FLOW.md                  ✅
├── 05_EPISTEMIC_VECTORS.md             ✅
├── 06_CASCADE_FLOW.md                  ✅
├── 07_GOAL_ORCHESTRATOR.md             ✅
├── 08_BAYESIAN_BELIEFS.md              ✅
├── 09_DRIFT_MONITOR.md                 ✅
├── 10_PLUGIN_SYSTEM.md                 ✅
└── ... (all 29 production/*.md files)
```

**User-facing guides (34 files):**
```
docs/user-guides/               ✅ All AI agent system prompts
docs/guides/setup/              ✅ Setup guides
docs/guides/learning/           ✅ Learning resources
docs/examples/                  ✅ Code examples
```

---

### Move to empirica-dev Repo (62 files)

**Session reports (45 files) → empirica-dev/sessions/**
```
docs/current_work/
├── CLAUDE_HANDOFF_SYSTEMATIC_ANALYSIS.md
├── CLI_COMMAND_REDUNDANCY_ANALYSIS.md
├── CROSS_PROFILE_BEHAVIOR_VALIDATION_REPORT.md
├── FINAL_SESSION_SUMMARY.md
├── GOAL_ARCHITECTURE_BUGS.md
├── MINIMAX_VALIDATION_RESULTS.md
├── P1.5_CLI_AUDIT_REPORT.md
├── SESSION_COMPLETE_2025_11_19.md
└── ... (all 45 current_work/*.md files)

WHY: These are internal session logs, not user documentation
```

**Architecture deep-dives (4 files) → empirica-dev/architecture/**
```
docs/architecture/
├── PHASE_1.6_DOCUMENTATION_UPDATE_PLAN.md
├── PHASE_1.6_EPISTEMIC_HANDOFF_REPORTS.md
├── PHASE_1.6_IMPLEMENTATION_COMPLETE.md
└── PHASE_1.6_VALIDATION_REPORT.md

WHY: Implementation details, not user-facing architecture
```

**Dev guides (4 files) → empirica-dev/guides/**
```
docs/guides/development/
├── AI_COMPONENT_GUIDE.md
├── AI_DEVELOPMENT_GUIDE.md
├── AI_VALIDATION_INSTRUCTIONS.md
└── MULTI_AI_COLLABORATION_GUIDE.md

WHY: For Empirica developers, not Empirica users
```

**Internal reference (7 files) → empirica-dev/reference/**
```
docs/reference/
├── CODE_DEDUPLICATION_ANALYSIS.md
├── DOCUMENTATION_CLEANUP_PLAN.md
├── LAUNCH_CHECKLIST_NOV_20_2025.md
├── MCP_CLI_ARCHITECTURE_ANALYSIS.md
├── META_MCP_ARCHITECTURE_ANALYSIS.md
├── SECURITY_SANITIZATION_PLAN.md
└── BOOTSTRAP_QUICK_REFERENCE.md (maybe - internal reference)

WHY: Internal analysis, not user reference
```

**Metrics (2 files) → empirica-dev/metrics/**
```
docs/metrics/
└── session_9_token_efficiency.md

docs/integrations/
└── MINIMAX_INTEGRATION.md

WHY: Internal performance tracking
```

---

### Move to empirica-dev/vision (10 files)

```
docs/vision/                            → empirica-dev/vision/
├── EMPIRICA_ACTION_REPLAY_VISION.md
├── EMPIRICA_VISION.md
├── EPISTEMIC_DELTA_SECURITY.md
├── META_ANALYSIS_GIT_EPISTEMIC_PATTERNS.md
├── REASONING_MEMORY_ARCHITECTURE.md
├── SENTINEL_GIT_MASTER_VISION.md
├── SENTINEL_SWARM_ORCHESTRATION.md
├── VISION_GIT_AS_EPISTEMIC_MEMORY.md
└── VISION_RECURSIVE_LEARNING_DELTAS.md

docs/research/                          → empirica-dev/research/
└── RECURSIVE_EPISTEMIC_REFINEMENT.md

WHY: Future plans, not current features
```

---

### Experimental (3 files) - DECISION NEEDED

```
docs/guides/experimental/
├── modality_switcher/MODALITY_SWITCHING_USAGE_GUIDE.md
└── README.md

docs/skills/
└── SKILL.md

OPTIONS:
1. Keep in production as "Advanced Features" (if stable)
2. Move to empirica-dev as "WIP Features" (if not ready)
3. Document as "deprecated" if no longer maintained

RECOMMENDATION: Review each file's stability before deciding
```

---

### Uncategorized (20 files) - REVIEW NEEDED

**Architecture docs (2 files):**
```
docs/architecture/
├── EMPIRICA_SYSTEM_OVERVIEW.md         → Keep? (user-facing overview)
└── SYSTEM_ARCHITECTURE_DEEP_DIVE.md    → Move? (too detailed for users)
```

**Guides (18 files):**
```
docs/guides/
├── CLI_GENUINE_SELF_ASSESSMENT.md      → Keep? (user guide)
├── CLI_WORKFLOW_COMMANDS_COMPLETE.md   → Keep? (CLI reference)
├── CRITICAL_NO_HEURISTICS_PRINCIPLE.md → Keep? (important concept)
├── DECISION_LOGGING_GUIDE.md           → Keep? (user feature)
├── EMPIRICA_QUICK_PROMPTS.md           → Keep? (user reference)
├── EXTENSIBLE_INVESTIGATION_STRATEGIES.md → Move? (advanced dev)
├── FINAL_TEST_AND_WEBSITE_PLAN.md      → Move! (internal planning)
├── MAKING_EMPIRICA_REPEATABLE.md       → Move? (dev guide)
├── MCP_CONFIGURATION_EXAMPLES.md       → Keep! (user examples)
├── PROFILE_MANAGEMENT.md               → Keep! (user feature)
├── REASONING_ACTING_SPLIT_GUIDE.md     → Keep? (important concept)
├── SESSION_ALIASES.md                  → Keep! (user feature)
├── TRY_EMPIRICA_NOW.md                 → Keep! (user onboarding)
├── empirica_git.md                     → Keep? (user git integration)
├── git_integration.md                  → Keep? (user git integration)
├── engineering/                        → Move? (dev guidelines)
└── protocols/UVL_PROTOCOL.md           → Keep? (user protocol)
```

**Action:** Review each file, apply categorization logic

---

## 🛠️ Implementation Plan

### Phase 1: Prepare empirica-dev Repo
```bash
# Create new repo
gh repo create empirica-dev --private --description "Empirica development workspace"

# Clone and setup structure
git clone git@github.com:USER/empirica-dev.git
cd empirica-dev

mkdir -p {sessions,architecture,guides,reference,metrics,vision,research}

# Create README
cat > README.md << 'END'
# Empirica Development Workspace

Internal development documentation and session reports for Empirica.

**For production documentation, see:** [empirica](https://github.com/USER/empirica)

## Structure
- `sessions/` - Session reports and validation results
- `architecture/` - Implementation details and analysis
- `guides/` - Developer-only guides
- `reference/` - Internal reference documentation
- `metrics/` - Performance and token efficiency tracking
- `vision/` - Future roadmap and research proposals
- `research/` - Experimental investigations
END

git add . && git commit -m "Initial structure"
git push
```

### Phase 2: Move Files (Script-Based)
```bash
cd /path/to/empirica

# Create move script
cat > /tmp/move_docs.sh << 'SCRIPT'
#!/bin/bash
DEV_REPO="/path/to/empirica-dev"

# Move session reports
mv docs/current_work/*.md "$DEV_REPO/sessions/"

# Move architecture deep-dives
mv docs/architecture/PHASE_*.md "$DEV_REPO/architecture/"

# Move dev guides
mv docs/guides/development/*.md "$DEV_REPO/guides/"

# Move internal reference
mv docs/reference/{CODE_DEDUPLICATION,DOCUMENTATION_CLEANUP,LAUNCH_CHECKLIST,*_ARCHITECTURE,SECURITY_SANITIZATION}*.md "$DEV_REPO/reference/"

# Move metrics
mv docs/metrics/*.md "$DEV_REPO/metrics/"

# Move vision
mv docs/vision/*.md "$DEV_REPO/vision/"
mv docs/research/*.md "$DEV_REPO/research/"

echo "✅ Files moved to empirica-dev"
SCRIPT

chmod +x /tmp/move_docs.sh
bash /tmp/move_docs.sh
```

### Phase 3: Clean Up Directories
```bash
cd /path/to/empirica/docs

# Remove empty directories
rmdir current_work 2>/dev/null
rmdir guides/development 2>/dev/null
rmdir architecture 2>/dev/null  # Keep if has user-facing docs
rmdir metrics 2>/dev/null
rmdir vision 2>/dev/null
rmdir research 2>/dev/null

# Verify structure
tree -L 2
```

### Phase 4: Update References
```bash
# Find broken links in production docs
cd /path/to/empirica
grep -r "docs/current_work" docs/
grep -r "docs/vision" docs/
grep -r "PHASE_1.6" docs/

# Update links to point to empirica-dev repo
# Example: [Session Report](../current_work/SESSION.md)
# Becomes: [Session Report](https://github.com/USER/empirica-dev/blob/main/sessions/SESSION.md)
```

### Phase 5: Verify Production Docs
```bash
# Check production docs are complete
cd /path/to/empirica/docs
ls -1 *.md                           # Top-level guides
ls -1 production/*.md                # User guides
ls -1 user-guides/*.md               # AI prompts
ls -1 guides/setup/*.md              # Setup guides
ls -1 guides/learning/*.md           # Learning resources
ls -1 reference/*.md                 # API reference
ls -1 examples/*.md                  # Examples

# Should see clean, user-focused structure
```

---

## ✅ Success Criteria

**Production repo should have:**
- ✅ Only user-facing documentation
- ✅ Clear learning path (00 → 06)
- ✅ Complete reference documentation
- ✅ Working examples
- ✅ No session reports or internal analysis
- ✅ < 1MB total documentation

**empirica-dev repo should have:**
- ✅ All session reports archived
- ✅ Implementation details preserved
- ✅ Dev guides accessible
- ✅ Vision/roadmap documented
- ✅ Searchable and organized

---

## 🎯 Next Actions

1. **Review uncategorized files** (20 files) - Decide keep vs move
2. **Create empirica-dev repo** - Setup structure
3. **Run move script** - Transfer 72+ files
4. **Update cross-references** - Fix broken links
5. **Verify production docs** - Ensure completeness
6. **Test documentation** - User walkthrough
7. **Commit changes** - Separate commits for traceability

---

## 📝 Notes

- **Pattern matching worked!** - Most docs are current, just misplaced
- **No deletion needed** - Move, don't delete (preserve history)
- **Repository split is correct strategy** - Separation of concerns
- **User experience will improve** - Cleaner, focused documentation

