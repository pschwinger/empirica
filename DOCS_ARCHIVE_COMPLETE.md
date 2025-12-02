# Documentation Archive Complete

**Date:** 2025-01-29  
**Result:** Reduced from ~200+ files to ~70 essential files

---

## What Was Archived

### Total: ~87 files moved to empirica-dev/archive/

**session-docs/** (~62 files)
- Session summaries, handoffs, progress reports
- Cleanup logs, investigation breadcrumbs
- Task-specific docs (QWEN cleanup, bootstrap tasks)
- Strategy documents, audit reports

**examples/** (4 files)
- Outdated schema examples

**reference-docs/** (9 files)
- EMPIRICA_FOUNDATION_SPECIFICATION.md (wrong CASCADE model)
- Bootstrap unification docs (outdated)
- CALIBRATION_SYSTEM.md (in production now)
- Investigation specs (outdated)
- NEW_SCHEMA_GUIDE.md (which is "new"?)
- architecture-technical.md (too detailed)

**architecture-details/** (5 files)
- SENTINEL_ORCHESTRATOR_* (implementation details)
- SYSTEM_ARCHITECTURE_DEEP_DIVE.md (wrong model)
- GIT_CHECKPOINT_ARCHITECTURE.md (implementation details)

**integrations/** (1 file)
- MINIMAX_INTEGRATION.md

**wrong_cascade_model/** (6 files - archived earlier)
- CASCADE specifications with wrong model
- Session summaries from today

---

## What's Left (Essential)

### docs/ Structure:
```
docs/
├── 00_START_HERE.md                   ✅ Entry point
├── 01_a_AI_AGENT_START.md            ✅ AI quickstart
├── 01_b_MCP_AI_START.md              ✅ MCP quickstart
├── 03_CLI_QUICKSTART.md              ✅ CLI guide
├── 04_MCP_QUICKSTART.md              ✅ MCP guide
├── 06_TROUBLESHOOTING.md             ✅ Troubleshooting
├── ONBOARDING_GUIDE.md               ✅ Onboarding (needs fix)
├── README.md                          ✅ Docs index
├── architecture.md                    ✅ High-level arch
├── getting-started.md                 ✅ Getting started
├── installation.md                    ✅ Installation
├── production/                        ✅ 26 files (user-facing)
├── skills/                            ✅ Skill docs
├── system-prompts/                    ✅ 5 files (canonical + guides)
├── architecture/                      ✅ 8 files (overview + visuals)
├── reference/                         ✅ 5 files (structure, storage, changelog)
└── guides/                            ⏸️  29 files (to review together)
```

### Root Files:
```
/
├── README.md                          ✅ Main readme (needs fix)
├── THE_MIRROR_PRINCIPLE.md            ✅ Foundational concept
├── CONTRIBUTING.md                    ✅ Contributing guide
├── LICENSE                            ✅ License
└── Config files (.env.example, etc.)  ✅
```

**Total: ~70 essential files** (vs. 200+ before)

---

## Benefits

1. **Clarity:** Only maintained docs in main tree
2. **Less confusion:** No contradictory session docs
3. **Easier maintenance:** 70 files vs. 200+
4. **Clear canonical sources:** System prompt + production docs
5. **Nothing lost:** Everything archived, not deleted

---

## Next Steps

### Immediate (Step 1):
1. Fix docs using canonical system prompt as reference
2. Update README.md (root) - correct CASCADE model
3. Update ONBOARDING_GUIDE.md - correct model
4. Review docs/ root files (quickstarts, etc.) for wrong model

### Short-term:
5. Review guides/ together (29 files) - keep essentials
6. Update production docs with correct model
7. Create migration notes for users

### Long-term (Step 3):
8. Refactor code to match canonical system prompt
9. Remove explicit phase tracking
10. Make CASCADE guidance-only

---

## Archive Locations

All archived files in `empirica-dev/archive/`:
- `session-docs/` - Session summaries, progress, handoffs
- `examples/` - Outdated examples
- `reference-docs/` - Wrong specs, outdated references
- `architecture-details/` - Implementation details
- `integrations/` - Specific integrations
- `wrong_cascade_model/` - Wrong conceptual model docs

Each directory has a README explaining what was archived and why.

---

**Status:** Archiving complete ✅  
**Next:** Fix remaining docs using canonical system prompt as reference
