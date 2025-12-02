# Documentation Archive Plan

**Date:** 2025-01-29  
**Goal:** Keep only essential docs, archive everything superfluous  
**Rationale:** Easier maintenance, less confusion, canonical sources are clear

---

## Essential Docs (KEEP)

### Core Documentation:
```
docs/
├── production/          ✅ KEEP - User-facing production docs
├── skills/             ✅ KEEP - Skill documentation
├── system-prompts/     ✅ KEEP - Canonical system prompt
├── architecture/
│   ├── EMPIRICA_SYSTEM_OVERVIEW.md        ✅ KEEP
│   ├── EPISTEMIC_TRAJECTORY_VISUALIZATION.md  ✅ KEEP (future vision)
│   └── CANONICAL_DIRECTORY_STRUCTURE.md   ✅ KEEP (if exists)
└── guides/             ⏸️  DEFER - Review together later
```

### Root Files:
```
/
├── README.md                    ✅ KEEP (needs fix)
├── CONTRIBUTING.md              ✅ KEEP
├── LICENSE                      ✅ KEEP
└── .env.example                 ✅ KEEP
```

---

## Superfluous Docs (ARCHIVE to empirica-dev/)

### Session Summaries & Handoffs (100+ files):
```
docs/
├── *_COMPLETE.md               ❌ ARCHIVE - Session completion docs
├── *_SUMMARY.md                ❌ ARCHIVE - Session summaries
├── *_HANDOFF*.md               ❌ ARCHIVE - Handoff documents
├── *_STATUS.md                 ❌ ARCHIVE - Status updates
├── *_PROGRESS.md               ❌ ARCHIVE - Progress tracking
├── *_BRIEFING.md               ❌ ARCHIVE - AI briefings
└── *_FINDINGS.md               ❌ ARCHIVE - Investigation findings
```

**Destination:** `empirica-dev/archive/session-docs/`

### Examples (Mostly Outdated):
```
docs/examples/
├── assessment_format_example.json     ❌ ARCHIVE (old format)
├── assessment_format_NEW_schema.json  ❌ ARCHIVE (NEW schema also old!)
├── self_assessment_example.json       ❌ ARCHIVE
└── README_SCHEMA_FORMATS.md           ❌ ARCHIVE
```

**Destination:** `empirica-dev/archive/examples/`  
**Reason:** Canonical system prompt + production docs are sufficient

### Reference Docs (Mostly Wrong/Outdated):
```
docs/reference/
├── EMPIRICA_CASCADE_WORKFLOW_SPECIFICATION.md    ❌ ARCHIVED (wrong model)
├── EMPIRICA_FOUNDATION_SPECIFICATION.md          ❌ ARCHIVE (wrong model)
├── BOOTSTRAP_LEVELS_UNIFIED.md                   ❌ ARCHIVE (outdated)
├── BOOTSTRAP_QUICK_REFERENCE.md                  ❌ ARCHIVE (outdated)
├── BOOTSTRAP_UNIFICATION_SUMMARY.md              ❌ ARCHIVE (outdated)
├── CALIBRATION_SYSTEM.md                         ❌ ARCHIVE (in production docs)
├── CHANGELOG.md                                  ⚠️  KEEP? (if actively maintained)
├── command-reference.md                          ⚠️  KEEP? (or merge to production)
├── COMMON_ERRORS_AND_SOLUTIONS.md                ⚠️  KEEP? (or merge to troubleshooting)
├── INVESTIGATION_PROFILE_SYSTEM_SPEC.md          ❌ ARCHIVE (outdated)
├── NEW_SCHEMA_GUIDE.md                           ❌ ARCHIVE (which schema is "new"?)
├── STORAGE_LOCATIONS.md                          ⚠️  KEEP? (useful reference)
└── architecture-technical.md                     ❌ ARCHIVE (superseded)
```

**Destination:** `empirica-dev/archive/reference-docs/`

### Architecture Docs (Partial Archive):
```
docs/architecture/
├── ARCHITECTURE_PERSONA_SENTINEL.md              ❌ ARCHIVE (implementation details)
├── GIT_CHECKPOINT_ARCHITECTURE.md                ⚠️  KEEP? (useful reference)
├── SENTINEL_ORCHESTRATOR_DESIGN.md               ❌ ARCHIVE (implementation details)
├── SENTINEL_ORCHESTRATOR_IMPLEMENTATION_COMPLETE.md  ❌ ARCHIVE (session summary)
├── SYSTEM_ARCHITECTURE_DEEP_DIVE.md              ❌ ARCHIVE (too detailed, wrong model)
└── FUTURE_VISIONS.md                             ✅ KEEP
```

**Destination:** `empirica-dev/archive/architecture-details/`

### Integrations (Outdated/Specific):
```
docs/integrations/
└── MINIMAX_INTEGRATION.md                        ❌ ARCHIVE (specific integration)
```

**Destination:** `empirica-dev/archive/integrations/`

### Root-Level Session Docs:
```
/
├── DATABASE_LOCATION_FIX_SUMMARY.md              ❌ ARCHIVE
├── EMPIRICA_HANDOFF_DOC_CLEANUP_PLAN.md          ❌ ARCHIVE
├── GIT_CHECKPOINT_BUG_FIX_FOR_QWEN.md            ❌ ARCHIVE
├── GOAL_HANDOFF_FIX_SUMMARY.md                   ❌ ARCHIVE
├── HANDOFF_GEMINI_BOOTSTRAP_MIGRATION.md         ❌ ARCHIVE
├── HANDOFF_QWEN_CLI_CLEANUP.md                   ❌ ARCHIVE
├── QUICK_FIX_SUMMARY.md                          ❌ ARCHIVE
├── SESSION_COMPLETE_*.md                         ❌ ARCHIVE (all of them)
├── THE_MIRROR_PRINCIPLE.md                       ⚠️  KEEP? (interesting concept)
├── CASCADE_CONCEPTUAL_CORRECTION_SUMMARY.md      ❌ ARCHIVE (session doc)
├── SYSTEM_PROMPT_CLEANUP_SUMMARY.md              ❌ ARCHIVE (session doc)
└── VALIDATION_FIX_SUMMARY.md                     ❌ ARCHIVE (session doc)
```

**Destination:** `empirica-dev/archive/session-docs/`

### Guides Subdirectories (Defer for Now):
```
docs/guides/
├── engineering/         ⏸️  DEFER - Review together
├── examples/            ⏸️  DEFER - Review together
├── git/                 ⏸️  DEFER - Review together
├── learning/            ⏸️  DEFER - Review together
├── protocols/           ⏸️  DEFER - Review together
└── setup/               ⏸️  DEFER - Review together
```

---

## Archive Organization in empirica-dev/

```
empirica-dev/
└── archive/
    ├── wrong_cascade_model/          (already exists)
    ├── session-docs/                 (NEW - all session summaries/handoffs)
    ├── examples/                     (NEW - old examples)
    ├── reference-docs/               (NEW - outdated reference docs)
    ├── architecture-details/         (NEW - implementation details)
    ├── integrations/                 (NEW - specific integrations)
    └── system-prompts-deprecated/    (NEW - old agent prompts, if any)
```

---

## Execution Plan

### Phase 1: Root-Level Session Docs (Easy Wins)
**Action:** Move all `*_SUMMARY.md`, `*_COMPLETE.md`, `*_HANDOFF*.md` from root to `empirica-dev/archive/session-docs/`

**Count:** ~15-20 files

### Phase 2: docs/ Session Docs (Bulk Archive)
**Action:** Move all session-related docs from `docs/` to `empirica-dev/archive/session-docs/`

**Patterns:**
- `*_COMPLETE.md`
- `*_SUMMARY.md`
- `*_HANDOFF*.md`
- `*_STATUS.md`
- `*_PROGRESS.md`
- `*_BRIEFING.md`
- `*_FINDINGS.md`
- `*_PLAN.md`
- `*_AUDIT*.md`

**Count:** ~50-100 files

### Phase 3: docs/examples/ (Complete Archive)
**Action:** Move entire `docs/examples/` to `empirica-dev/archive/examples/`

**Count:** 3-4 files

### Phase 4: docs/reference/ (Selective Archive)
**Action:** Archive most reference docs, keep only:
- `CHANGELOG.md` (if actively maintained)
- `command-reference.md` (if still accurate)
- `STORAGE_LOCATIONS.md` (useful reference)

**Archive:** ~10-12 files

### Phase 5: docs/architecture/ (Selective Archive)
**Action:** Keep only:
- `EMPIRICA_SYSTEM_OVERVIEW.md`
- `EPISTEMIC_TRAJECTORY_VISUALIZATION.md`
- `FUTURE_VISIONS.md`
- `GIT_CHECKPOINT_ARCHITECTURE.md` (maybe)

**Archive:** ~5-6 files

### Phase 6: docs/integrations/ (Complete Archive)
**Action:** Move to `empirica-dev/archive/integrations/`

**Count:** 1 file

---

## What We'll Have After

### Essential Documentation (Maintained):
```
docs/
├── production/          📚 User-facing docs (maintained)
├── skills/             📚 Skill documentation (maintained)
├── system-prompts/     📚 Canonical prompt (maintained)
├── architecture/       📚 System overview + future visions (minimal)
└── guides/             ⏸️  To be reviewed together

Total: ~30-40 files (vs. 200+ currently)
```

### Archive (Reference Only):
```
empirica-dev/archive/
├── wrong_cascade_model/      (wrong conceptual model)
├── session-docs/            (~100+ session summaries/handoffs)
├── examples/                (outdated examples)
├── reference-docs/          (outdated specs)
├── architecture-details/    (implementation details)
└── integrations/            (specific integrations)

Total: ~150+ files archived
```

---

## Benefits

1. **Clarity:** Only maintained docs in `docs/`
2. **Maintenance:** Easy to keep ~40 files accurate vs. 200+
3. **No Loss:** Everything archived in `empirica-dev/`, not deleted
4. **Focus:** Clear canonical sources (system prompt + production docs)
5. **Onboarding:** New users see only essential docs

---

## Questions Before Execution

1. **CHANGELOG.md** - Keep or archive? (is it actively maintained?)
2. **command-reference.md** - Keep or merge into production docs?
3. **STORAGE_LOCATIONS.md** - Keep as reference or archive?
4. **GIT_CHECKPOINT_ARCHITECTURE.md** - Keep or archive?
5. **THE_MIRROR_PRINCIPLE.md** - Keep (interesting concept) or archive?

---

## Next Steps

1. **Get approval** on what to keep/archive
2. **Create archive directories** in empirica-dev/
3. **Execute phases 1-6** systematically
4. **Create archive READMEs** explaining what was archived and why
5. **Update root README.md** to reflect clean structure
6. **Fix production docs** using canonical prompt as reference

---

**Ready to execute?** Let's start with Phase 1 (easy wins) if approved.
