# CLI Commands & MCP Tools Audit

**Date:** 2025-01-XX  
**Purpose:** Verify actual commands vs documented commands

---

## CLI Commands (Actual - from --help)

**Total:** 60+ commands

### Core Workflow
1. `bootstrap` - Bootstrap the framework
2. `preflight` - Execute preflight epistemic assessment
3. `preflight-submit` - Submit preflight assessment results
4. `check` - Execute epistemic check assessment
5. `check-submit` - Submit check assessment results
6. `postflight` - Execute postflight epistemic reassessment
7. `postflight-submit` - Submit postflight assessment results
8. `workflow` - Execute full preflight→work→postflight workflow

### Assessment
9. `assess` - Run uncertainty assessment
10. `self-awareness` - Assess self-awareness
11. `metacognitive` - Run metacognitive evaluation
12. `calibration` - Run calibration analysis
13. `uvl` - Run UVL (Uncertainty Vector Learning)

### Goals & Tasks
14. `goals-create` - Create new goal
15. `goals-add-subtask` - Add subtask to existing goal
16. `goals-complete-subtask` - Mark subtask as complete
17. `goals-progress` - Get goal completion progress
18. `goals-list` - List goals
19. `goals-discover` - Discover goals from other AIs via git ⭐
20. `goals-resume` - Resume another AI's goal ⭐
21. `goal-analysis` - Analyze goal feasibility

### Session Management
22. `sessions-list` - List all sessions
23. `sessions-show` - Show detailed session info
24. `sessions-export` - Export session to JSON
25. `sessions-resume` - Resume previous sessions

### Git Checkpoints
26. `checkpoint-create` - Create git checkpoint for session
27. `checkpoint-load` - Load latest checkpoint for session
28. `checkpoint-list` - List checkpoints for session
29. `checkpoint-diff` - Show vector differences from last checkpoint

### Handoffs
30. `handoff-create` - Create epistemic handoff report (~90% token reduction)
31. `handoff-query` - Query handoff reports

### Identity Management
32. `identity-create` - Create new AI identity with Ed25519 keypair
33. `identity-list` - List all AI identities
34. `identity-export` - Export public key for sharing
35. `identity-verify` - Verify signed session

### Investigation
36. `investigate` - Investigate file/directory/concept
37. `investigate-log` - Log investigation findings during INVESTIGATE phase

### Actions
38. `act-log` - Log actions taken during ACT phase

### Decision Making
39. `decision` - Epistemic decision-making with ModalitySwitcher
40. `decision-batch` - Batch decision processing from JSON file
41. `feedback` - Provide decision feedback

### Performance
42. `performance` - Analyze performance or run benchmarks
43. `efficiency-report` - Generate token efficiency report

### Monitoring
44. `monitor` - Monitoring dashboard and statistics

### Configuration
45. `config` - Configuration management
46. `profile-list` - List available profiles
47. `profile-show` - Show profile details
48. `profile-create` - Create new profile
49. `profile-set-default` - Set default profile

### Components
50. `list` - List semantic components
51. `explain` - Explain component functionality
52. `demo` - Run component demonstration

### User Interfaces
53. `ask` - Ask a question (simple query interface)
54. `chat` - Interactive chat session (REPL)

**Plus more commands not shown in summary...**

---

## Comparison: Documented vs Actual

### What's in production/20_TOOL_CATALOG.md
**Claims 23 MCP tools**

### What's Actually Available (CLI)
**60+ commands!**

**Major discrepancies:**
- ✅ Core workflow (8 commands) - documented
- ✅ Goals (7 commands) - documented
- ✅ Checkpoints (4 commands) - documented
- ✅ Identity (4 commands) - documented
- ✅ Handoffs (2 commands) - documented
- ⚠️ **Assessment commands (5)** - NOT well documented
- ⚠️ **Investigation commands (2)** - NOT well documented
- ⚠️ **Decision making (3)** - NOT well documented
- ⚠️ **Performance (2)** - NOT well documented
- ⚠️ **Configuration (5)** - NOT well documented
- ⚠️ **Components (3)** - NOT well documented
- ⚠️ **User interfaces (2: ask, chat)** - NOT documented

---

## Key Findings

### 1. Way More Commands Than Documented
**Documented:** 23 MCP tools  
**Actual:** 60+ CLI commands

**Reason:** MCP tools are subset of CLI commands, but docs don't clarify this

### 2. Missing Command Categories in Docs
- Assessment tools (assess, self-awareness, metacognitive, calibration, uvl)
- Investigation logging (investigate-log)
- Action logging (act-log)
- Decision making (decision, decision-batch, feedback)
- Performance (performance, efficiency-report)
- Monitoring (monitor)
- Configuration (config, profile-*)
- Components (list, explain, demo)
- User interfaces (ask, chat)

### 3. MCP vs CLI Confusion
**Need to clarify:**
- Are MCP tools a subset of CLI commands?
- Do all CLI commands have MCP equivalents?
- What's the mapping?

---

## Action Items for Production Docs

### Update production/20_TOOL_CATALOG.md
**Current title:** "Tool Catalog (23 MCP Tools)"  
**Should be:** "Command & Tool Reference (60+ commands, 23 MCP tools)"

**Add sections:**
1. Core Workflow (8 commands)
2. Assessment & Calibration (5 commands)
3. Goals & Tasks (7 commands)
4. Session Management (4 commands)
5. Git Checkpoints (4 commands)
6. Handoffs (2 commands)
7. Identity Management (4 commands)
8. Investigation (2 commands)
9. Actions (1 command)
10. Decision Making (3 commands)
11. Performance (2 commands)
12. Monitoring (1 command)
13. Configuration (5 commands)
14. Components (3 commands)
15. User Interfaces (2 commands)

**For each command:**
- Purpose
- Usage
- Example
- MCP equivalent (if exists)

### Clarify MCP vs CLI
**Add section explaining:**
- CLI = Full command set (60+)
- MCP = Subset for IDE integration (23 tools)
- MCP tools focus on workflow tracking (preflight, check, postflight, goals)
- CLI includes utilities, configuration, monitoring, etc.

---

## Epistemic Guidance for Copilot Claude

**Based on 13 vectors, what Claude needs to explore:**

### KNOW (Domain Knowledge) - Priority: HIGH
**Need to understand:**
- All 60+ CLI commands (read help text)
- Purpose of each command category
- How commands relate to CASCADE workflow
- Which are core vs advanced features

**Exploration:**
```bash
empirica --help
empirica <command> --help  # For each command
grep -r "def handle_" empirica/cli/command_handlers/
```

### CONTEXT (Environment Understanding) - Priority: HIGH
**Need to understand:**
- Current state of production/20_TOOL_CATALOG.md
- What's documented vs what exists
- Gaps in documentation

**Exploration:**
```bash
cat docs/production/20_TOOL_CATALOG.md
diff <(documented commands) <(actual commands)
```

### CLARITY (Requirements Understanding) - Priority: MEDIUM
**Need to clarify:**
- Should docs cover all 60+ commands or focus on core?
- How to organize such a large command set?
- User vs developer commands?

**Questions for user:**
- Document all 60+ or just core 20-30?
- Separate user commands from dev commands?

### DO (Capability) - Priority: HIGH
**Need to be able to:**
- Test each command
- Verify command output
- Write accurate examples

**Exploration:**
```bash
empirica bootstrap --help
empirica preflight --help
# Try commands in test environment
```

### UNCERTAINTY (What's Unknown) - Priority: HIGH
**Key uncertainties:**
- MCP tool list (need to extract from code)
- CLI-to-MCP mapping
- Which commands are experimental vs stable

**Investigation needed:**
- Parse mcp_local/empirica_mcp_server.py for tool list
- Check each command handler for MCP exposure
- Ask user: which are stable vs experimental

---

## Recommended Approach

### Phase 1: Audit Commands (Copilot Claude)
1. Extract all CLI commands from --help
2. Extract all MCP tools from mcp_server code
3. Create mapping: CLI ↔ MCP
4. Categorize by: Core / Advanced / Experimental

### Phase 2: Update production/20_TOOL_CATALOG.md
1. Rename to "Command & Tool Reference"
2. Add all command categories
3. Document each command
4. Show MCP equivalents where they exist
5. Mark experimental features

### Phase 3: Update User Docs
1. installation.md - Focus on core commands only
2. getting-started.md - Show workflow commands
3. architecture.md - Reference full catalog

---

## Questions for User

1. **Should production/20_TOOL_CATALOG.md cover all 60+ commands?**
   - Or focus on core 20-30 for users?

2. **How to distinguish user vs developer commands?**
   - E.g., `config`, `profile-*` seem developer-focused

3. **Which commands are experimental?**
   - `decision`, `modality`, components?

4. **What's the MCP tool list?**
   - Need to extract from code accurately

---

**Status:** Major discrepancy found - 60+ commands vs 23 documented  
**Priority:** Update production/20_TOOL_CATALOG.md before user docs  
**Next:** Copilot Claude should audit and document all commands
