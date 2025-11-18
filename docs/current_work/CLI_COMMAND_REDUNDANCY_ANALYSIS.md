# CLI Command Redundancy Analysis
**Date:** 2025-11-17
**Analyst:** Claude (Systematic Analysis Lead)
**Objective:** Reduce CLI commands from 52 to ~37 (26% reduction target)
**Status:** Complete Analysis with Consolidation Recommendations

---

## Executive Summary

**Current State:** 52 CLI commands across 15 categories
**Recommended State:** 37 CLI commands (29% reduction)
**Commands to Remove:** 15 redundant commands
**Commands to Consolidate:** Multiple commands merged into unified interfaces

**Impact:** Simpler user experience, reduced maintenance, clearer command purpose

---

## Current Command Inventory (52 commands)

### Category Breakdown:
```
Bootstrap Commands:     3  (bootstrap, bootstrap-system, onboard)
Assessment Commands:    3  (assess, self-awareness, metacognitive)
Cascade Commands:       2  (cascade, decision)
Workflow Commands:      4  (decision-batch, preflight, postflight, workflow)
Investigation:          2  (investigate, analyze)
Performance:            2  (benchmark, performance)
Component:              3  (list, explain, demo)
Utility:                4  (feedback, goal-analysis, calibration, uvl)
Config Management:      5  (config-init, config-show, config-validate, config-get, config-set)
Profile Management:     4  (profile-list, profile-show, profile-create, profile-set-default)
Monitoring:             4  (monitor, monitor-export, monitor-reset, monitor-cost)
MCP Server:             6  (mcp-start, mcp-stop, mcp-status, mcp-test, mcp-list-tools, mcp-call)
Session Management:     3  (sessions-list, sessions-show, sessions-export)
Checkpoint Management:  5  (checkpoint-create, checkpoint-load, checkpoint-list, checkpoint-diff, efficiency-report)
User Interface:         2  (ask, chat)
```

---

## Redundancy Analysis

### 🔴 HIGH REDUNDANCY (Consolidate Immediately)

#### 1. **Bootstrap Commands (3 → 1)**
**Current:**
- `bootstrap` - Standard framework initialization
- `bootstrap-system` - Advanced system bootstrap
- `onboard` - Interactive onboarding wizard

**Analysis:**
- `bootstrap` and `bootstrap-system` differ only by default level
- `onboard` is interactive wrapper around `bootstrap`
- All three initialize the same underlying system

**Recommendation:** **CONSOLIDATE to 1 command**
```bash
# New unified command
empirica bootstrap [--level LEVEL] [--interactive] [--profile PROFILE]

# Replace:
# - bootstrap-system → bootstrap --level=extended
# - onboard → bootstrap --interactive
```

**Savings:** 2 commands removed

---

#### 2. **Assessment Commands (3 → 1)**
**Current:**
- `assess` - Uncertainty assessment
- `self-awareness` - Self-awareness assessment
- `metacognitive` - Metacognitive evaluation

**Analysis:**
- All three perform epistemic self-assessment
- Different assessment types, not different workflows
- Can be unified with `--type` flag

**Recommendation:** **CONSOLIDATE to 1 command**
```bash
# New unified command
empirica assess QUERY [--type TYPE] [--detailed]

# Types: uncertainty (default), self-awareness, metacognitive
# Replace:
# - self-awareness → assess --type=self-awareness
# - metacognitive TASK → assess TASK --type=metacognitive
```

**Savings:** 2 commands removed

---

#### 3. **Investigation Commands (2 → 1)**
**Current:**
- `investigate` - Investigate file/directory/concept
- `analyze` - Analyze subject comprehensively

**Analysis:**
- Nearly identical functionality (investigation vs analysis)
- Both take target/subject, context, and detailed flags
- Semantic difference only

**Recommendation:** **CONSOLIDATE to 1 command**
```bash
# Keep investigate (more specific semantic meaning)
empirica investigate TARGET [--type TYPE] [--context JSON]

# Types: file, directory, concept, comprehensive
# Remove: analyze (redundant)
```

**Savings:** 1 command removed

---

#### 4. **Performance Commands (2 → 1)**
**Current:**
- `benchmark` - Run performance benchmark
- `performance` - Analyze performance

**Analysis:**
- `benchmark` runs tests, `performance` analyzes results
- Can be unified with subcommand or flag

**Recommendation:** **CONSOLIDATE to 1 command**
```bash
# New unified command
empirica performance [--benchmark] [--analyze] [--target TARGET]

# Default: show current performance metrics
# --benchmark: run benchmark tests
# --analyze: detailed analysis
```

**Savings:** 1 command removed

---

#### 5. **Config Commands (5 → 2)**
**Current:**
- `config-init` - Initialize configuration
- `config-show` - Show current configuration
- `config-validate` - Validate configuration
- `config-get` - Get configuration value
- `config-set` - Set configuration value

**Analysis:**
- `config-get` and `config-set` are CRUD operations
- `config-show` overlaps with `config-get` (no args = show all)
- `config-validate` can be flag on `config` command

**Recommendation:** **CONSOLIDATE to 2 commands**
```bash
# New structure
empirica config [KEY] [VALUE] [--validate] [--init] [--section SECTION]

# Usage:
# - config                      → show all config
# - config --init               → initialize config
# - config --validate           → validate config
# - config routing.strategy     → get value (replaces config-get)
# - config routing.strategy epistemic → set value (replaces config-set)
# - config --section routing    → show section (replaces config-show --section)

# Alternative: Keep as 2 commands
empirica config show [--section SECTION] [--validate]
empirica config set KEY VALUE
```

**Savings:** 3 commands removed

---

#### 6. **Monitor Commands (4 → 1)**
**Current:**
- `monitor` - Display monitoring dashboard
- `monitor-export` - Export monitoring data
- `monitor-reset` - Reset statistics
- `monitor-cost` - Display cost analysis

**Analysis:**
- All are monitoring operations
- Can be unified with subcommands/flags

**Recommendation:** **CONSOLIDATE to 1 command**
```bash
# New unified command
empirica monitor [--export FILE] [--reset] [--cost] [--history]

# Default: show dashboard
# --export: export to file
# --reset: reset statistics
# --cost: show cost analysis
# --history: show request history
```

**Savings:** 3 commands removed

---

#### 7. **MCP Commands (6 → 3)**
**Current:**
- `mcp-start` - Start MCP server
- `mcp-stop` - Stop MCP server
- `mcp-status` - Check server status
- `mcp-test` - Test server connection
- `mcp-list-tools` - List available tools
- `mcp-call` - Call tool directly

**Analysis:**
- Server lifecycle commands can be unified (start/stop/status)
- Tool operations separate (list/call)

**Recommendation:** **CONSOLIDATE to 3 commands**
```bash
# Server management
empirica mcp server [--start] [--stop] [--status] [--test]

# Tool operations
empirica mcp tools [--list] [--show-all]
empirica mcp call TOOL_NAME [--arguments JSON]

# Replaces:
# - mcp-start → mcp server --start
# - mcp-stop → mcp server --stop
# - mcp-status → mcp server --status (or just mcp server)
# - mcp-test → mcp server --test
# - mcp-list-tools → mcp tools --list
```

**Savings:** 3 commands removed

---

### 🟡 MEDIUM REDUNDANCY (Consider Consolidation)

#### 8. **Cascade Commands (2 → Keep 2)**
**Current:**
- `cascade` - Epistemic cascade with ModalitySwitcher
- `decision` - Epistemic decision-making with ModalitySwitcher

**Analysis:**
- Both use same ModalitySwitcher routing
- Different semantic purposes (general cascade vs decision-specific)
- Different default behaviors expected by users

**Recommendation:** **KEEP BOTH** (semantic clarity valuable)
- Users expect `decision` for decision-making contexts
- `cascade` for general epistemic analysis

**Savings:** 0 commands removed

---

#### 9. **Workflow Commands (4 → Keep 4)**
**Current:**
- `decision-batch` - Batch decision processing
- `preflight` - Execute preflight assessment
- `postflight` - Execute postflight reassessment
- `workflow` - Full preflight→work→postflight

**Analysis:**
- Each serves distinct workflow phase
- MCP tools likely depend on these specific commands
- Part of documented CASCADE workflow

**Recommendation:** **KEEP ALL 4**
- Critical workflow commands for CASCADE pattern
- Used by MCP server and documented processes

**Savings:** 0 commands removed

---

### 🟢 LOW REDUNDANCY (Keep As-Is)

#### 10. **Component Commands (3 → Keep 3)**
- `list`, `explain`, `demo` - All serve different purposes

#### 11. **Utility Commands (4 → Keep 4)**
- `feedback`, `goal-analysis`, `calibration`, `uvl` - Distinct utilities

#### 12. **Profile Commands (4 → Keep 4)**
- Profile management is core feature, all commands needed

#### 13. **Session Commands (3 → Keep 3)**
- Essential CRUD operations for sessions

#### 14. **Checkpoint Commands (5 → Keep 5)**
- Phase 1.5 feature, all commands serve distinct purposes

#### 15. **User Interface (2 → Keep 2)**
- `ask` and `chat` serve different interaction patterns

---

## Consolidation Summary

### Commands to Remove (15 total):

**Bootstrap (2 removed):**
- ❌ `bootstrap-system` → `bootstrap --level=extended`
- ❌ `onboard` → `bootstrap --interactive`

**Assessment (2 removed):**
- ❌ `self-awareness` → `assess --type=self-awareness`
- ❌ `metacognitive` → `assess QUERY --type=metacognitive`

**Investigation (1 removed):**
- ❌ `analyze` → `investigate TARGET --type=comprehensive`

**Performance (1 removed):**
- ❌ `benchmark` → `performance --benchmark`

**Config (3 removed):**
- ❌ `config-show` → `config [--section SECTION]`
- ❌ `config-get` → `config KEY`
- ❌ `config-set` → `config KEY VALUE`

**Monitor (3 removed):**
- ❌ `monitor-export` → `monitor --export FILE`
- ❌ `monitor-reset` → `monitor --reset`
- ❌ `monitor-cost` → `monitor --cost`

**MCP (3 removed):**
- ❌ `mcp-start` → `mcp server --start`
- ❌ `mcp-stop` → `mcp server --stop`
- ❌ `mcp-status` → `mcp server --status`

---

## New Command Structure (37 commands)

### Consolidated Commands:
```
Bootstrap:          1  (bootstrap)
Assessment:         1  (assess)
Cascade:            2  (cascade, decision)
Workflow:           4  (decision-batch, preflight, postflight, workflow)
Investigation:      1  (investigate)
Performance:        1  (performance)
Component:          3  (list, explain, demo)
Utility:            4  (feedback, goal-analysis, calibration, uvl)
Config:             2  (config, config-set OR unified config)
Profile:            4  (profile-list, profile-show, profile-create, profile-set-default)
Monitor:            1  (monitor)
MCP:                3  (mcp-server, mcp-tools, mcp-call)
Sessions:           3  (sessions-list, sessions-show, sessions-export)
Checkpoints:        5  (checkpoint-create, checkpoint-load, checkpoint-list, checkpoint-diff, efficiency-report)
User Interface:     2  (ask, chat)

TOTAL: 37 commands (29% reduction from 52)
```

---

## Implementation Recommendations

### Phase 1: Create Alias/Wrapper Support (No Breaking Changes)
1. Keep all 52 existing commands functional
2. Add new consolidated commands as alternatives
3. Mark old commands as deprecated in help text
4. Update documentation to show new syntax

### Phase 2: Migration Period (Deprecation Warnings)
1. Add deprecation warnings to old commands
2. Redirect to new consolidated commands
3. Track usage to identify migration status

### Phase 3: Removal (After Migration)
1. Remove deprecated commands from codebase
2. Update all tests and documentation
3. Final validation

---

## Benefits of Consolidation

### User Experience:
✅ **Simpler mental model** - Fewer commands to remember
✅ **Consistent patterns** - Similar operations use same command structure
✅ **Reduced documentation** - Less content to read and maintain
✅ **Better discoverability** - Flags make functionality explicit

### Developer Experience:
✅ **Less code duplication** - Shared implementation logic
✅ **Easier testing** - Fewer command entry points
✅ **Clearer architecture** - Logical grouping of functionality
✅ **Faster feature development** - Add flags vs new commands

### Maintenance:
✅ **Reduced surface area** - 29% fewer command handlers
✅ **Easier deprecation** - Centralized command logic
✅ **Better versioning** - Flags are easier to add/remove than commands

---

## Risk Assessment

### Low Risk Changes:
- Bootstrap consolidation (semantic overlap clear)
- Assessment consolidation (type-based dispatch straightforward)
- Investigation/Performance consolidation (minimal user impact)

### Medium Risk Changes:
- Config consolidation (verify no scripts depend on old commands)
- Monitor consolidation (ensure flag combinations work correctly)

### High Risk Changes:
- MCP consolidation (verify MCP server doesn't call CLI directly)
- Ensure no internal tooling depends on specific command names

---

## Next Steps

1. **Review with team** - Validate consolidation strategy
2. **Check dependencies** - Grep codebase for subprocess calls to CLI
3. **Create implementation plan** - Phased rollout with backward compatibility
4. **Update documentation** - New command reference guide
5. **Write migration guide** - Help users transition

---

## Validation Checklist

- [ ] No MCP tools call CLI commands directly (or update if they do)
- [ ] No scripts in `/scripts/` depend on removed commands
- [ ] Test suite updated for new command structure
- [ ] Documentation reflects consolidated commands
- [ ] Help text updated with examples
- [ ] Deprecation warnings added for old commands
- [ ] Migration guide created for users

---

**Recommendation:** Proceed with consolidation in phased approach to minimize user disruption while achieving 29% command reduction target.

**Achievement:** 15 commands removed, 37 commands remaining (exceeds 26% reduction goal)
