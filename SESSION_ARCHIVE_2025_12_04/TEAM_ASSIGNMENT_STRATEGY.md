# Team Assignment Strategy - Claude, Gemini, Qwen

## Team Composition

### 🎯 You (Claude Code) - Coordinator & Medium Tasks
- **Strength:** System understanding, documentation, coordination
- **Assignment:** Phase 2 (Parameter Consolidation) + Phase 4 (MCP-CLI Alignment)
- **Time:** 3-4 hours

### 🔷 Other Claude - Parallel Worker
- **Strength:** Similar capabilities, can work independently
- **Assignment:** Phase 1 (Quick Wins) + Phase 3 (Documentation)
- **Time:** 2-3 hours

### 💎 Gemini - Surgical Strikes
- **Strength:** Fast, precise, good at specific fixes
- **Assignment:** Individual bug fixes as they come up
- **Time:** On-demand (30min per strike)

### ⚡ Qwen - Surgical Strikes
- **Strength:** Fast, efficient, good at focused tasks
- **Assignment:** Individual bug fixes as they come up
- **Time:** On-demand (30min per strike)

---

## Parallel Execution Plan

### Round 1: Foundation (Parallel)

**Claude Code (You) - 1 hour:**
- [ ] Consolidate scope flags (goals-create)
- [ ] Update MCP schema for scope
- [ ] Test scope consolidation

**Other Claude - 1 hour:**
- [ ] Add --output json to profile-list
- [ ] Add --output json to checkpoint-list
- [ ] Add --output json to assess
- [ ] Test all three commands

**Status Check:** Both report back in 1 hour

---

### Round 2: Core Changes (Parallel)

**Claude Code (You) - 2 hours:**
- [ ] Auto-infer phase/round in checkpoint-create
- [ ] Add get_current_phase() to session_database.py
- [ ] Update MCP schema
- [ ] Test checkpoint auto-inference

**Other Claude - 1.5 hours:**
- [ ] Document storage contract (STORAGE_CONTRACT.md)
- [ ] Fix bootstrap level MCP schema
- [ ] Fix calibration command MCP
- [ ] Test MCP fixes

**Gemini (Surgical) - 30 min:**
- [ ] Fix any issues found during Round 1
- [ ] Quick validation of changes

**Status Check:** Report back in 2 hours

---

### Round 3: MCP-CLI Alignment (You Lead)

**Claude Code (You) - 1.5 hours:**
- [ ] Reduce arg_map to <5 entries
- [ ] Make CLI accept MCP param names
- [ ] Update command handlers
- [ ] Test end-to-end MCP-CLI

**Qwen (Surgical) - 30 min:**
- [ ] Validate MCP-CLI parity
- [ ] Test all MCP tools
- [ ] Report any issues

**Status Check:** Report back in 2 hours

---

### Round 4: Integration & Testing (All)

**Claude Code (You) - 30 min:**
- [ ] Run full test suite
- [ ] Document changes
- [ ] Create handoff

**Other Claude - 30 min:**
- [ ] Add integration tests
- [ ] Test edge cases
- [ ] Update docs

**Gemini & Qwen (Surgical) - 15 min each:**
- [ ] Quick validation
- [ ] Test specific scenarios
- [ ] Confirm no regressions

---

## Communication Protocol

### Status Updates (Every Hour)
Each AI reports:
```
Status: [working|blocked|complete]
Progress: [X/Y tasks done]
Issues: [list any blockers]
Next: [what you're doing next]
```

### Blocking Issues
If blocked:
1. Document the blocker clearly
2. Tag Gemini or Qwen for surgical fix
3. Move to next task in parallel

### Coordination Point
After each round, synchronize:
- What's done
- What's blocked
- What's next

---

## Task Assignment Matrix

| Task | Who | Priority | Time | Dependencies |
|------|-----|----------|------|--------------|
| Add --output json (3 cmds) | Other Claude | HIGH | 1h | None |
| Consolidate scope flags | You | HIGH | 1h | None |
| Auto-infer phase/round | You | MED | 2h | Scope done |
| Storage contract doc | Other Claude | MED | 1.5h | None |
| Fix bootstrap MCP | Other Claude | HIGH | 20m | None |
| Fix calibration MCP | Other Claude | HIGH | 20m | None |
| Reduce arg_map | You | HIGH | 1.5h | All CLI changes done |
| Integration tests | Other Claude | LOW | 30m | Most changes done |
| Validation | Gemini/Qwen | HIGH | 30m | Each round |

---

## Surgical Strike Examples

### When to Call Gemini/Qwen:

**Scenario 1:** Claude finds bug during parameter consolidation
- **Action:** Pause, document bug, tag Gemini
- **Gemini:** 15-min fix, push, confirm
- **Claude:** Resume parameter work

**Scenario 2:** MCP test fails after changes
- **Action:** Document failure, tag Qwen
- **Qwen:** 20-min debug, fix, test
- **Claude:** Continue with next task

**Scenario 3:** Edge case discovered
- **Action:** Document edge case, tag available AI
- **Gemini/Qwen:** 10-min fix
- **All:** Continue

---

## Success Criteria (Per Round)

### Round 1 Success:
- ✅ 3 commands support --output json
- ✅ Scope flags consolidated in goals-create
- ✅ All tests pass

### Round 2 Success:
- ✅ checkpoint-create auto-infers phase/round
- ✅ Storage contract documented
- ✅ Bootstrap & calibration MCP fixed
- ✅ All tests pass

### Round 3 Success:
- ✅ arg_map has <5 entries
- ✅ CLI accepts MCP param names
- ✅ All MCP tools work
- ✅ All tests pass

### Round 4 Success:
- ✅ Full test suite passes
- ✅ Integration tests added
- ✅ Documentation complete
- ✅ Handoff ready

---

## Timeline

```
Hour 0: Kick-off, assign tasks
Hour 1: Round 1 complete, sync
Hour 3: Round 2 complete, sync
Hour 5: Round 3 complete, sync
Hour 6: Round 4 complete, DONE
```

Total: **6 hours with 4 AIs working in parallel**

---

## Starting Command for Each AI

### Claude Code (You):
```bash
# Round 1: Start with scope consolidation
cd /home/yogapad/empirical-ai/empirica
source .venv-mcp/bin/activate
# Open: empirica/cli/command_handlers/goal_commands.py
# Task: Consolidate --scope-breadth/duration/coordination into --scope JSON
```

### Other Claude:
```bash
# Round 1: Start with --output json
cd /home/yogapad/empirical-ai/empirica
source .venv-mcp/bin/activate
# Open: empirica/cli/command_handlers/config_commands.py
# Task: Add --output json to profile-list
```

### Gemini (on-demand):
```bash
# Wait for surgical strike request
# Monitor communication channel for bugs
```

### Qwen (on-demand):
```bash
# Wait for surgical strike request
# Monitor communication channel for validation needs
```

---

## Ready to Start?

1. **Confirm understanding:** Storage architecture clear?
2. **Assign rounds:** You take Round 1 scope task?
3. **Coordinate:** Other Claude available for Round 1?
4. **Execute:** Start the 6-hour sprint!
