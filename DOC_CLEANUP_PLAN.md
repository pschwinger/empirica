# Documentation Cleanup Plan
**Date**: 2025-12-11
**Lead**: Claude Code
**Execution**: Devstral, Qwen, Gemini (action-based AIs)
**Goal**: Fix doc-code inconsistencies - remove phantom commands, document real commands

## ✅ JSON Output Fixed
- `empirica project-bootstrap --check-integrity --output json` now works
- Returns 66 phantom commands with file locations + context
- Returns 3 undocumented commands
- Commit: f706fb1f

---

## 🎯 Core Principle
**No heuristic scripts - Human reasoning required for each phantom command.**

Many "phantom" commands are:
- ✅ **Valid examples** (shell commands like `bash`, `pwd` in instructions)
- ✅ **Valid docs** (commands that SHOULD exist but don't yet)
- ❌ **Real phantoms** (typos, deprecated, never-existed)

Each AI must **reason about context** before removing.

---

## Phase 1: Categorize Phantom Commands (Lead: Claude Code)

### Task: Audit all 66 phantom commands
**Command to get data**:
```bash
empirica project-bootstrap --project-id ea2f33a4-d808-434b-b776-b7246bd6134a \
  --check-integrity --output json | \
  python3 -c "import sys,json; data=json.load(sys.stdin); \
  print(json.dumps(data['breadcrumbs']['integrity_analysis']['cli_commands']['missing_implementations'], indent=2))"
```

### Categories:
1. **Shell commands** (NOT phantom) - `bash`, `chmod`, `pwd`, `python3`, `pip`, `tmux`
   - Action: Update integrity analyzer to exclude these

2. **Typos/garbage** - `empirica-app`, `soulentheo`, `is`, `spec`
   - Action: Remove from docs

3. **Deprecated/renamed** - Check if command exists with different name:
   - `assess` → `preflight`/`check`/`postflight`?
   - `bootstrap` → `project-bootstrap` or `session-create`?
   - `sessions` → `sessions-list`?
   - Action: Update docs with correct command name

4. **Future/planned features** - In development/design docs only
   - `dashboard`, `visualize`, `orchestrate`
   - Action: Move to `docs/future/` or mark as [PLANNED]

5. **Instructions** (NOT phantom) - Examples like "use empirica [command]"
   - Action: Keep as-is if it's teaching context

### Output: `phantom_commands_categorized.json`

---

## Phase 2: Production Docs vs Future Docs (Lead: Devstral)

### Task: Separate production from future/design docs

**Scan docs/ for keywords**:
- "Planned", "Future", "Not implemented", "TODO", "Design", "RFC"
- Any doc with >30% phantom commands = likely future doc

**Move to `docs/future/`**:
- Design documents
- RFC documents
- Feature planning docs

**Keep in `docs/production/`**:
- User-facing guides
- API reference
- Architecture (current state only)

### Output: List of moved files

---

## Phase 3: Fix Real Phantom Commands (Lead: Qwen + Gemini)

### Task: For each REAL phantom command, choose action:

#### A. Command was renamed
Example: `assess` → `preflight`/`check`/`postflight`
- Find all mentions in docs/production/
- Update to correct command name
- Verify example still works

#### B. Command never existed (typo)
Example: `empirica-app`, `soulentheo`
- Remove from docs
- Check if surrounding text needs updating

#### C. Command should exist but doesn't
Example: Some `profile-*` commands, `report`, `validate`
- Mark in docs as `[NOT IMPLEMENTED YET]`
- Or remove if not critical

### Execution:
**Qwen**: Handle categories A + B (straightforward fixes)
**Gemini**: Handle category C (requires judgment on keep vs remove)

### Output: Pull request with doc changes

---

## Phase 4: Document Undocumented Commands (Lead: Gemini)

### Task: Add docs for 3 undocumented commands:
1. `mistake-query` - Query logged mistakes
2. `skill-fetch` - Fetch skill from registry
3. `skill-suggest` - Suggest relevant skills

**For each**:
- Check CLI help: `empirica [command] --help`
- Check MCP if applicable
- Write brief section in appropriate doc file
- Add to command reference

### Output: Doc additions in `docs/reference/command-reference.md`

---

## Phase 5: Update Integrity Analyzer (Lead: Claude Code)

### Task: Make analyzer smarter

**Add exclusions**:
```python
SHELL_COMMANDS = {'bash', 'chmod', 'pwd', 'python3', 'pip', 'tmux', 'cd', 'ls', 'mkdir'}
COMMON_WORDS = {'is', 'the', 'and', 'or', 'not'}  # Ignore in command detection
```

**Add context awareness**:
- If command appears in code block with `$` prefix → shell example, not phantom
- If command has severity but mentioned once → likely false positive

### Output: Updated `empirica/utils/doc_code_integrity.py`

---

## Success Criteria

✅ Integrity score improves from 0.5% to >60%
✅ All production docs reference only real commands
✅ Future docs clearly separated
✅ 3 undocumented commands now documented
✅ Zero false positives in phantom list

---

## Coordination

**Claude Code (you)**:
- Phase 1 categorization
- Phase 5 analyzer improvements
- Review all PRs from other AIs

**Devstral** (action AI):
- Phase 2 doc reorganization
- Move files, update paths

**Qwen** (action AI):
- Phase 3.A + 3.B (straightforward fixes)
- Bulk find/replace operations

**Gemini** (reasoning AI):
- Phase 3.C (judgment calls)
- Phase 4 (documentation writing)

---

## Next Steps

1. Claude Code: Complete Phase 1 categorization → save to JSON
2. Share JSON with team
3. Devstral/Qwen/Gemini: Execute phases in parallel
4. Claude Code: Review + merge PRs
5. Verify integrity score improvement

**Timeline**: Each phase = 1-2 hours for assigned AI
**Total**: ~1 day for complete cleanup
