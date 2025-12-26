# Recent Additions Audit - Documentation Needs

**Date:** 2025-12-25
**Scope:** Last 7-10 days of work

## Summary

Audit of recent additions to identify what needs proper documentation vs what's already covered.

---

## 1. Workflow Automation Features ✅ DOCUMENTED

**Added:**
- TUI Dashboard Design (`docs/architecture/TUI_DASHBOARD_DESIGN.md`)
- AI Workflow Automation - 8 strategies (`docs/architecture/AI_WORKFLOW_AUTOMATION.md`)
- Interactive Checklist TUI (`docs/architecture/INTERACTIVE_CHECKLIST_TUI.md`)
- Semantic Workflow Index (`docs/architecture/SEMANTIC_WORKFLOW_INDEX.md`)
- Workflow suggestions - completeness scoring (`empirica/cli/utils/workflow_suggestions.py`)

**Documentation status:**
- ✅ Architecture docs exist
- ✅ Added to SEMANTIC_INDEX.yaml
- ✅ Mentioned in lean system prompts
- ⚠️ **TODO:** Update CANONICAL_SYSTEM_PROMPT.md with workflow automation sections

**Action needed:**
- [ ] Add workflow automation sections to `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`
- [ ] Add to CHANGELOG.md under "Workflow Automation" section

---

## 2. CLI Improvements ✅ MOSTLY DOCUMENTED

**Added (commits from last week):**
- `--verbose` flag standardization (f76fb05c)
- `--version` flag with detailed info (44a49eb9)
- Grouped help output (16242e09)
- Parser modularization into `empirica/cli/parsers/` (42144883)
- `--format` → `--output` standardization (0577400a)
- `format_help_text()` helper (today)
- JSON stdin support for `handoff-create` (today)

**Documentation status:**
- ✅ CLI commands auto-generated in `docs/reference/CLI_COMMANDS_GENERATED.md`
- ✅ Grouped help visible in `empirica --help`
- ⚠️ **Missing:** Parser modularization architecture doc
- ⚠️ **Missing:** JSON stdin pattern documentation

**Action needed:**
- [ ] Add "CLI Architecture" section to existing doc (which one?)
- [ ] Document AI-first JSON stdin pattern (add to CLI_REFERENCE.md)
- [ ] Update CHANGELOG.md with CLI improvements

---

## 3. System Prompt Updates ⚠️ NEEDS CONSOLIDATION

**Added (today):**
- Lean prompts v5.1 (CLAUDE.md, instructions.md) - pruned to 207 lines
- Lean prompts v5.2 - added multi-AI workflows (now 403-406 lines)
- Strengthened documentation policy
- Multi-AI workflow commands section
- Epistemic breadcrumbs section
- Handoff types section
- BEADS integration section

**Documentation status:**
- ✅ Lean prompts updated: `/home/yogapad/.claude/CLAUDE.md`, `/home/yogapad/.vibe/instructions.md`
- ✅ Summary docs created: `LEAN_PROMPT_UPDATES.md`, `SYSTEM_PROMPT_FIXES_v5.2.md`
- ⚠️ **TODO:** Update CANONICAL_SYSTEM_PROMPT.md with v5.2 additions
- ⚠️ **Issue:** Summary docs in project root (should be in `docs/development/session-summaries/`)

**Action needed:**
- [ ] Update `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md` with workflow automation + multi-AI sections
- [ ] Move `LEAN_PROMPT_UPDATES.md` → `docs/development/session-summaries/LEAN_PROMPT_UPDATES_2025-12-25.md`
- [ ] Move `SYSTEM_PROMPT_FIXES_v5.2.md` → `docs/development/session-summaries/SYSTEM_PROMPT_v5.2_2025-12-25.md`
- [ ] Update CHANGELOG.md under "System Prompts" section

---

## 4. File Tree in Bootstrap ✅ ALREADY IMPLEMENTED

**Feature:**
- `project-bootstrap` includes `tree` output (respects .gitignore)
- Implemented at `empirica/data/session_database.py:3117`
- Uses `generate_file_tree()` method with 60s cache

**Documentation status:**
- ✅ Code implemented and working
- ✅ Mentioned in updated documentation policy (lean prompts)
- ❓ **Check:** Is this mentioned in CASCADE_WORKFLOW.md or PROJECT_LEVEL_TRACKING.md?

**Action needed:**
- [ ] Verify file_tree is documented in `docs/guides/PROJECT_LEVEL_TRACKING.md`
- [ ] If not, add section: "File Structure Context" with tree command details

---

## 5. Help Text Improvements ⚠️ PARTIAL

**Added (today):**
- `format_help_text()` helper in `empirica/cli/parsers/__init__.py`
- Applied to `checkpoint-create` and `handoff-create` parsers
- Shows "(required)" and "(optional, default: X)" in help output

**Documentation status:**
- ✅ Function documented in code
- ⚠️ **Missing:** Not applied to all parsers yet (12 parser files remaining)
- ⚠️ **Missing:** Pattern not documented for future parser additions

**Action needed:**
- [ ] Add "CLI Development Guide" section to `docs/development/` explaining `format_help_text()` pattern
- [ ] OR add to existing `docs/development/REPOSITORY_ORGANIZATION.md`
- [ ] Create issue/TODO for applying to remaining parsers

---

## Summary of Documentation Gaps

### HIGH PRIORITY (User-Facing)
1. **Update CANONICAL_SYSTEM_PROMPT.md** with:
   - Workflow automation sections
   - Multi-AI workflow commands
   - Strengthened documentation policy
   - File tree in bootstrap

2. **Document AI-First JSON Stdin Pattern** in `docs/reference/CLI_REFERENCE.md`:
   - Pattern: positional `config` argument with `nargs='?'`
   - Handler: check `args.config`, read stdin if `-`, parse JSON
   - Example: `handoff-create`, `session-create`, `goals-create`

3. **Verify/Add File Tree Documentation** in `docs/guides/PROJECT_LEVEL_TRACKING.md`

### MEDIUM PRIORITY (Developer-Facing)
4. **CLI Development Guide** - `format_help_text()` pattern for future parsers

5. **Parser Modularization Architecture** - How CLI is organized into `empirica/cli/parsers/`

### LOW PRIORITY (Cleanup)
6. **Move session summary docs** from project root to `docs/development/session-summaries/`

7. **Update CHANGELOG.md** with all recent additions

---

## Recommended Actions (In Order)

### 1. Update CANONICAL_SYSTEM_PROMPT.md (15 min)
```bash
# Read current canonical prompt
# Add workflow automation sections from lean prompts
# Add multi-AI workflow commands section
# Add strengthened documentation policy
# Commit: "docs: Update canonical prompt with workflow automation and v5.2 additions"
```

### 2. Document JSON Stdin Pattern (10 min)
```bash
# Edit docs/reference/CLI_REFERENCE.md
# Add "AI-First JSON Stdin Pattern" section
# Show parser pattern + handler pattern + examples
# Commit: "docs: Document AI-first JSON stdin pattern for CLI commands"
```

### 3. Verify File Tree Documentation (5 min)
```bash
# Check docs/guides/PROJECT_LEVEL_TRACKING.md for file_tree mention
# If missing, add "File Structure Context" section
# Commit: "docs: Add file tree context to project bootstrap guide"
```

### 4. Move Session Summaries (5 min)
```bash
mv LEAN_PROMPT_UPDATES.md docs/development/session-summaries/LEAN_PROMPT_UPDATES_2025-12-25.md
mv SYSTEM_PROMPT_FIXES_v5.2.md docs/development/session-summaries/SYSTEM_PROMPT_v5.2_2025-12-25.md
git add docs/development/session-summaries/
git commit -m "docs: Move session summaries to proper location"
```

### 5. Update CHANGELOG.md (10 min)
```bash
# Add sections:
# - Workflow Automation (TUI, checklist, semantic index)
# - CLI Improvements (--verbose, --version, grouped help, JSON stdin)
# - System Prompts (v5.1 lean, v5.2 multi-AI, doc policy)
# Commit: "docs: Update CHANGELOG with recent additions"
```

---

## What Does NOT Need Documentation

✅ **Workflow suggestions implementation** - Internal code, output visible in bootstrap
✅ **Parser modularization details** - Developer refactor, doesn't change behavior
✅ **Help text helper** - Internal utility, pattern can be inferred from code
✅ **Lean prompt iterations** - Session summaries are sufficient

---

## Total Effort: ~45 minutes to close all documentation gaps

**Status:** Ready for execution
