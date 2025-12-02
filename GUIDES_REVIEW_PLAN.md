# docs/guides/ Review Plan

**Total:** 29 files  
**Task:** Decide what to keep vs archive

---

## Category Analysis

### 📚 KEEP (Essential Guides)

**Core Principles:**
- ✅ `CRITICAL_NO_HEURISTICS_PRINCIPLE.md` - Core philosophy
- ✅ `REASONING_ACTING_SPLIT_GUIDE.md` - Important pattern

**User Guides:**
- ✅ `TRY_EMPIRICA_NOW.md` - Quick start for users
- ✅ `MCP_CONFIGURATION_EXAMPLES.md` - Practical examples
- ✅ `PROFILE_MANAGEMENT.md` - User feature
- ✅ `SESSION_ALIASES.md` - User feature

**Setup Guides:**
- ✅ `setup/CLAUDE_CODE_MCP_SETUP.md` - Platform-specific setup
- ✅ `setup/MCP_SERVERS_SETUP.md` - General MCP setup
- ✅ `setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md` - Important setup (but maybe merge to docs/installation.md?)

**Git Integration:**
- ✅ `git/empirica_git.md` - Core feature
- ✅ `git/git_integration.md` - Core feature
- ⚠️ `git/BRANCH_SWITCHING_GUIDE.md` - Keep or archive?

**Protocols:**
- ✅ `protocols/UVL_PROTOCOL.md` - Structured format

---

## ❌ ARCHIVE (Outdated/Session Docs)

**Session/Task Docs:**
- ❌ `FINAL_TEST_AND_WEBSITE_PLAN.md` - Session planning doc
- ❌ `NEW_SESSION_EMPIRICA_TEST_INSTRUCTIONS.md` - Session doc
- ❌ `CLI_WORKFLOW_COMMANDS_COMPLETE.md` - Session completion doc
- ❌ `MAKING_EMPIRICA_REPEATABLE.md` - Session doc

**Analysis/Investigation Docs:**
- ❌ `setup/ADAPTIVE_SESSION_LOADING_ANALYSIS.md` - Analysis doc
- ❌ `setup/QWEN_GEMINI_TESTING_GUIDE.md` - Specific testing guide
- ❌ `setup/EMPIRICA_MCP_INTEGRATION_SPEC.md` - Spec doc (covered in production)

**Learning/Reference Docs:**
- ❌ `learning/AI Self awareness - full reference.md` - Covered in system prompt
- ❌ `learning/COMPLETE_LEARNING_DOCUMENTATION.md` - Superseded

---

## ⚠️ UNCERTAIN (Need Discussion)

**Methodology Prompts:**
- ⚠️ `EMPIRICA_METHODOLOGY_PROMPTS.md` - Useful or redundant with system prompt?
- ⚠️ `EMPIRICA_QUICK_PROMPTS.md` - Quick reference or in system prompt already?

**CLI Guides:**
- ⚠️ `CLI_GENUINE_SELF_ASSESSMENT.md` - Covered in production docs?
- ⚠️ `DECISION_LOGGING_GUIDE.md` - Covered elsewhere?

**Advanced Features:**
- ⚠️ `EXTENSIBLE_INVESTIGATION_STRATEGIES.md` - Advanced feature guide
- ⚠️ `engineering/SEMANTIC_ENGINEERING_GUIDELINES.md` - For developers?
- ⚠️ `engineering/SEMANTIC_ONTOLOGY.md` - For developers?

**Examples:**
- ⚠️ `examples/mcp_configs/mcp_config_rovodev.json` - Example config

---

## Recommendation Summary

### KEEP (~12-14 files):
```
docs/guides/
├── CRITICAL_NO_HEURISTICS_PRINCIPLE.md       ✅ Core principle
├── REASONING_ACTING_SPLIT_GUIDE.md           ✅ Important pattern
├── TRY_EMPIRICA_NOW.md                       ✅ User quickstart
├── MCP_CONFIGURATION_EXAMPLES.md             ✅ Practical examples
├── PROFILE_MANAGEMENT.md                     ✅ User feature
├── SESSION_ALIASES.md                        ✅ User feature
├── git/
│   ├── empirica_git.md                       ✅ Core feature
│   └── git_integration.md                    ✅ Core feature
├── protocols/
│   └── UVL_PROTOCOL.md                       ✅ Format spec
└── setup/
    ├── CLAUDE_CODE_MCP_SETUP.md              ✅ Platform setup
    └── MCP_SERVERS_SETUP.md                  ✅ General setup
```

### ARCHIVE (~10-12 files):
```
empirica-dev/archive/guides/
├── FINAL_TEST_AND_WEBSITE_PLAN.md
├── NEW_SESSION_EMPIRICA_TEST_INSTRUCTIONS.md
├── CLI_WORKFLOW_COMMANDS_COMPLETE.md
├── MAKING_EMPIRICA_REPEATABLE.md
├── learning/ (both files)
└── setup/
    ├── ADAPTIVE_SESSION_LOADING_ANALYSIS.md
    ├── QWEN_GEMINI_TESTING_GUIDE.md
    └── EMPIRICA_MCP_INTEGRATION_SPEC.md
```

### DISCUSS (~7 files):
- Methodology prompts (2)
- CLI guides (2)
- Engineering guides (2)
- Examples (1)

---

## Questions for You:

1. **EMPIRICA_METHODOLOGY_PROMPTS.md** - Keep (useful quick reference) or archive (redundant with system prompt)?

2. **EMPIRICA_QUICK_PROMPTS.md** - Keep or archive?

3. **CLI_GENUINE_SELF_ASSESSMENT.md** - Keep or archive (covered in production docs)?

4. **DECISION_LOGGING_GUIDE.md** - Keep or archive?

5. **EXTENSIBLE_INVESTIGATION_STRATEGIES.md** - Keep (advanced feature) or archive?

6. **engineering/** subdirectory - Keep (for developers) or archive (internal docs)?

7. **examples/mcp_configs/** - Keep (useful example) or move to setup/?

8. **BRANCH_SWITCHING_GUIDE.md** - Keep or archive (git workflow detail)?

9. **EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md** - Keep in guides/ or merge into docs/installation.md?

---

## After Review:

**Estimated final guides/ structure:** ~12-15 essential files (vs. 29 currently)

**Benefits:**
- Clear purpose for each guide
- No session/analysis docs cluttering
- Essential user guides remain accessible
- Advanced features documented
