# Empirica Simplification Action Plan

## Executive Summary

**Goal:** Reduce parameter bloat by 40%, standardize storage flow, make MCP-CLI mapping 1:1

**Current State:**
- ✅ Storage flow mapped (SQLite primary, Git Notes for cross-AI, JSON for debug)
- ✅ 12 issues found in MCP-CLI integration
- ✅ 2 critical bugs fixed
- ⚠️ Parameter bloat identified (7+ flags where 2-3 would suffice)

**Principle:** "SQLite is truth, Git is distribution, JSON is audit trail"

---

## Phase 1: Quick Wins (1-2 hours)

### Task 1.1: Add --output json to 3 commands ✅ EASY
**Files to modify:**
- `empirica/cli/command_handlers/config_commands.py` (profile-list)
- `empirica/cli/command_handlers/checkpoint_commands.py` (checkpoint-list)
- `empirica/cli/command_handlers/assessment_commands.py` (assess)

**Pattern to follow:**
```python
if args.output == 'json':
    print(json.dumps({"ok": True, "data": result}, indent=2))
else:
    # existing pretty print
```

### Task 1.2: Fix remaining MCP arg_map issues ✅ EASY
**File:** `mcp_local/empirica_mcp_server.py`

**Remaining fixes:**
1. Bootstrap level - add flexible parsing for "optimal", "extended_metacognitive"
2. Calibration command - either redesign CLI or fix MCP to not pass session-id

---

## Phase 2: Parameter Consolidation (2-4 hours)

### Task 2.1: Consolidate scope flags into single JSON ⚡ HIGH IMPACT
**Commands affected:**
- `goals-create` (--scope-breadth, --scope-duration, --scope-coordination)
- Any command using scope vectors

**Change:**
```bash
# BEFORE (3 flags):
--scope-breadth 0.7 --scope-duration 0.5 --scope-coordination 0.3

# AFTER (1 flag):
--scope '{"breadth":0.7, "duration":0.5, "coordination":0.3}'
```

**Implementation:**
1. Add `--scope` flag accepting JSON
2. Keep old flags for backwards compatibility (deprecated warning)
3. Update MCP schema to match
4. Update docs

**Files:**
- `empirica/cli/command_handlers/goal_commands.py`
- `mcp_local/empirica_mcp_server.py` (schema update)

### Task 2.2: Auto-infer phase/round from session state ⚡ HIGH IMPACT
**Commands affected:**
- `checkpoint-create` (--phase, --round currently required)

**Change:**
```bash
# BEFORE (4 flags):
empirica checkpoint-create --session-id abc --phase ACT --round 3 --metadata '{...}'

# AFTER (2 flags):
empirica checkpoint-create --session-id abc --note "Progress note"
# Phase and round auto-detected from session state in SQLite
```

**Implementation:**
1. Query SQLite reflexes table for latest phase
2. Auto-increment round based on existing checkpoints
3. Make --phase and --round optional (override if provided)

**Files:**
- `empirica/cli/command_handlers/checkpoint_commands.py`
- `empirica/data/session_database.py` (add get_current_phase method)

### Task 2.3: Consolidate goal creation parameters ⚡ MEDIUM IMPACT
**Change:**
```bash
# BEFORE (7 flags):
empirica goals-create --session-id X --objective "..." \
  --scope-breadth 0.7 --scope-duration 0.5 --scope-coordination 0.3 \
  --success-criteria '["a","b"]' --estimated-complexity 0.8

# AFTER (3 flags):
empirica goals-create --session-id X --objective "..." \
  --spec '{"scope":{"breadth":0.7,"duration":0.5,"coordination":0.3},"complexity":0.8,"success":["a","b"]}'
```

**Files:**
- `empirica/cli/command_handlers/goal_commands.py`

---

## Phase 3: MCP-CLI Alignment (1-2 hours)

### Task 3.1: Ensure 1:1 MCP-CLI mapping 🎯 CRITICAL
**Goal:** Every MCP tool should call exactly one CLI command with no parameter translation

**Current issues:**
- arg_map has 12+ mappings (too many edge cases)
- Some parameters get transformed (task_summary → summary)
- Some parameters get skipped (vectors for checkpoint-create)

**Solution:**
1. Make CLI accept exact MCP parameter names
2. Remove all arg_map entries (or reduce to <5)
3. Add CLI flags that match MCP schemas exactly

**Example fix:**
```python
# BAD (current):
arg_map = {"task_summary": "summary", ...}  # 12+ mappings

# GOOD (target):
arg_map = {}  # CLI accepts task_summary directly, no mapping needed
```

### Task 3.2: Standardize JSON output across all commands
**Rule:** Every command that outputs data MUST support `--output json`

**Audit checklist:**
- [ ] All goal commands
- [ ] All session commands
- [ ] All checkpoint commands
- [ ] All assessment commands
- [ ] All monitoring commands

---

## Phase 4: Storage Simplification (2-3 hours)

### Task 4.1: Document storage contract 📚 DOCUMENTATION
**Create:** `docs/STORAGE_CONTRACT.md`

**Content:**
```markdown
# Empirica Storage Contract

## Primary Source of Truth: SQLite

ALL operational data lives in SQLite:
- Sessions, cascades, reflexes (vectors), goals, tasks

## Distribution Layer: Git Notes

ONLY used for cross-AI coordination:
- goals/{goal_id} - Goal discovery across AIs
- handoffs/{session_id} - Session continuity reports
- checkpoints/{session_id} - Optional compressed snapshots

Git Notes are READ-ONLY from other repos, WRITE from owning repo.

## Audit Trail: JSON Files

Debug/development only:
- ~/.empirica_reflex_logs/ - Detailed reflex frames
- Can be disabled in production with --no-reflex-logs flag

## Command Storage Rules

| Command | SQLite Write | Git Notes | JSON Files |
|---------|-------------|-----------|------------|
| preflight-submit | ✅ reflexes | ❌ | ✅ optional |
| checkpoint-create | ❌ read only | ✅ write | ❌ |
| goals-create | ✅ goals | ✅ discovery | ❌ |
| handoff-create | ❌ read only | ✅ write | ❌ |
| sessions-list | ✅ read only | ❌ | ❌ |
```

### Task 4.2: Make Git Notes optional 🔧 REFACTORING
**Goal:** System works 100% without git, git is purely for cross-AI features

**Implementation:**
1. Add `--enable-git-notes` flag (default: true)
2. Wrap all git operations in try/except with graceful degradation
3. Log warning if git operations fail, but continue

**Files:**
- `empirica/core/canonical/empirica_git/checkpoint_manager.py`
- `empirica/core/canonical/empirica_git/goal_store.py`

---

## Phase 5: Testing & Validation (1 hour)

### Task 5.1: Add integration tests for MCP-CLI mapping
**File:** `tests/integration/test_mcp_cli_parity.py`

```python
def test_mcp_parameters_match_cli():
    """Ensure MCP tool parameters exactly match CLI flags"""
    from mcp_local.empirica_mcp_server import list_tools
    
    tools = list_tools()
    for tool in tools:
        # Extract MCP parameters
        mcp_params = tool.inputSchema.get('properties', {}).keys()
        
        # Get corresponding CLI command
        cli_cmd = get_cli_command(tool.name)
        
        # Parse CLI --help to get accepted flags
        cli_flags = parse_cli_flags(cli_cmd)
        
        # Assert 1:1 mapping
        assert mcp_params == cli_flags, f"Mismatch in {tool.name}"
```

### Task 5.2: Test all commands with --output json
**File:** `tests/integration/test_json_output_consistency.py`

```python
def test_all_commands_support_json_output():
    """Ensure every command supports --output json"""
    commands = get_all_cli_commands()
    
    for cmd in commands:
        result = run_cli(f"empirica {cmd} --output json")
        assert result.returncode == 0 or "--output" in result.stderr
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            assert 'ok' in data  # Standard response format
```

---

## Assignment Matrix

### For AI Agent 1: Quick Wins (Easy) ⭐
- [ ] Add --output json to 3 commands
- [ ] Fix remaining MCP arg_map issues
- [ ] Test and validate

**Estimated time:** 1-2 hours  
**Difficulty:** ⭐ Easy

### For AI Agent 2: Parameter Consolidation (Medium) ⭐⭐
- [ ] Consolidate scope flags
- [ ] Auto-infer phase/round
- [ ] Update MCP schemas

**Estimated time:** 2-4 hours  
**Difficulty:** ⭐⭐ Medium

### For AI Agent 3: Storage & Documentation (Medium) ⭐⭐
- [ ] Document storage contract
- [ ] Make Git Notes optional
- [ ] Add integration tests

**Estimated time:** 2-3 hours  
**Difficulty:** ⭐⭐ Medium

### For AI Agent 4: MCP-CLI Alignment (Hard) ⭐⭐⭐
- [ ] Achieve 1:1 MCP-CLI mapping
- [ ] Reduce arg_map to <5 entries
- [ ] Update all schemas

**Estimated time:** 2-3 hours  
**Difficulty:** ⭐⭐⭐ Hard

---

## Success Criteria

✅ **Parameter reduction:** CLI commands use 40% fewer flags
✅ **Storage clarity:** Everyone knows SQLite=primary, Git=distribution
✅ **MCP simplicity:** arg_map has <5 entries, 1:1 mapping
✅ **Consistency:** All commands support --output json
✅ **Testing:** Integration tests prevent future mismatches

---

## Files to Review

### High Priority:
1. `mcp_local/empirica_mcp_server.py` - arg_map consolidation
2. `empirica/cli/command_handlers/goal_commands.py` - scope consolidation
3. `empirica/cli/command_handlers/checkpoint_commands.py` - auto-infer phase/round
4. `empirica/data/session_database.py` - add helper methods

### Medium Priority:
5. All command handlers - add --output json
6. `docs/STORAGE_CONTRACT.md` - new documentation
7. `tests/integration/` - new tests

### Low Priority:
8. Git Notes modules - make optional
9. MCP schemas - update after CLI changes

---

## Next Steps

1. **Review this plan** - Any questions or concerns?
2. **Assign AI agents** - Who takes which phase?
3. **Create handoff docs** - Each AI documents their changes
4. **Sequential execution** - Phase 1 → 2 → 3 → 4 → 5
5. **Test thoroughly** - Run full test suite after each phase

**Estimated total time:** 8-12 hours across 4 AI agents (2-3 hours each)

---

**Status:** 📋 Plan ready for review and assignment
