# docs/guides/ Cleanup Complete

**Date:** 2025-01-29  
**Result:** Reduced from 29 files to ~14 essential guides

---

## What Was Done

### 1. Archived (10 files)
**To:** `empirica-dev/archive/guides/`
- EMPIRICA_METHODOLOGY_PROMPTS.md
- EMPIRICA_QUICK_PROMPTS.md
- CLI_GENUINE_SELF_ASSESSMENT.md
- DECISION_LOGGING_GUIDE.md
- CLI_WORKFLOW_COMMANDS_COMPLETE.md
- FINAL_TEST_AND_WEBSITE_PLAN.md
- NEW_SESSION_EMPIRICA_TEST_INSTRUCTIONS.md
- MAKING_EMPIRICA_REPEATABLE.md
- ADAPTIVE_SESSION_LOADING_ANALYSIS.md
- QWEN_GEMINI_TESTING_GUIDE.md
- EMPIRICA_MCP_INTEGRATION_SPEC.md
- learning/ (2 files: AI self awareness, complete learning)

### 2. Moved to Experimental (2 files)
**To:** `empirica-dev/experimental/`
- investigation-strategies/EXTENSIBLE_INVESTIGATION_STRATEGIES.md
- git-workflows/BRANCH_SWITCHING_GUIDE.md

### 3. Reorganized (2 items)
- mcp_config_rovodev.json → moved to docs/guides/setup/
- EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md → docs/system-prompts/INSTALLATION.md

### 4. Kept for Developers (2 files)
- engineering/SEMANTIC_ENGINEERING_GUIDELINES.md
- engineering/SEMANTIC_ONTOLOGY.md

---

## Final docs/guides/ Structure

```
docs/guides/
├── CRITICAL_NO_HEURISTICS_PRINCIPLE.md       ✅ Core principle
├── REASONING_ACTING_SPLIT_GUIDE.md           ✅ Important pattern
├── TRY_EMPIRICA_NOW.md                       ✅ User quickstart
├── MCP_CONFIGURATION_EXAMPLES.md             ✅ Practical examples
├── PROFILE_MANAGEMENT.md                     ✅ User feature
├── SESSION_ALIASES.md                        ✅ User feature
├── engineering/
│   ├── SEMANTIC_ENGINEERING_GUIDELINES.md    ✅ For developers
│   └── SEMANTIC_ONTOLOGY.md                  ✅ For developers
├── git/
│   ├── empirica_git.md                       ✅ Core feature
│   └── git_integration.md                    ✅ Core feature
├── protocols/
│   └── UVL_PROTOCOL.md                       ✅ Format spec
└── setup/
    ├── CLAUDE_CODE_MCP_SETUP.md              ✅ Platform setup
    ├── MCP_SERVERS_SETUP.md                  ✅ General setup
    └── mcp_config_rovodev.json               ✅ Example config

Total: 14 files (was 29)
```

---

## New Locations

### System Prompts
```
docs/system-prompts/
├── CANONICAL_SYSTEM_PROMPT.md                ✅ Main prompt
├── CUSTOMIZATION_GUIDE.md                    ✅ Customization
├── MIGRATION_GUIDE.md                        ✅ Migration
├── INSTALLATION.md                           ✅ Installation (moved from guides/)
└── ...
```

### Experimental
```
empirica-dev/experimental/
├── investigation-strategies/
│   └── EXTENSIBLE_INVESTIGATION_STRATEGIES.md
└── git-workflows/
    └── BRANCH_SWITCHING_GUIDE.md
```

---

## Benefits

1. **Focused:** Only essential guides remain
2. **Clear purpose:** Each guide serves users/developers
3. **Less confusion:** No session/analysis docs
4. **Better organization:** System prompt docs together
5. **Experimental clear:** Advanced features separate

---

## Next Steps

1. ✅ Guides cleanup complete
2. 📋 Next: Update CANONICAL_DIRECTORY_STRUCTURE_V2.md
3. 📋 Future: Review CLI guides in archive (update or delete?)

---

**Status:** Cleanup complete ✅  
**Guides:** 14 essential files (vs. 29 before)
