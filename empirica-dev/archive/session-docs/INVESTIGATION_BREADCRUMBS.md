# Investigation Breadcrumbs for Documentation Work

**Purpose:** Guide each AI through deep investigation before writing docs

---

## Core Investigation Path (ALL AIs start here)

### Step 1: Architecture Foundation (30 min)
**Read these in order:**

1. **CANONICAL_DIRECTORY_STRUCTURE_V2.md** (source of truth for codebase)
   - 150 Python files (cleaned from 187)
   - Core vs Advanced vs Experimental distinction
   - What was moved and why

2. **COMPREHENSIVE_EMPIRICA_UNDERSTANDING.md** (753 lines - complete understanding)
   - Part 1: Core Architecture (production-ready)
   - Part 2: Advanced Features (experimental)
   - Part 3-8: Documentation status, insights, technical details

3. **DEEP_EXPLORATION_FINDINGS.md** (critical issues found)
   - CASCADE migration (old DriftMonitor → MirrorDriftMonitor)
   - 12 files with deprecated code
   - Test coverage analysis

---

### Step 2: Changes & Cleanup Context (15 min)

4. **MIGRATION_PROGRESS.md** (what we fixed)
   - CASCADE core migrated to no heuristics
   - 11 files still need cleaning (Gemini/Qwen working on)

5. **CLEANUP_ROUND2_COMPLETE.md** (what we moved)
   - 37 files moved to empirica-dev
   - 4,666 lines of isolated components removed
   - Clean 150-file codebase

6. **FILE_CLEANUP_PLAN.md** (what's where)
   - Components moved
   - Calibration deprecated
   - What remains in core

---

### Step 3: Documentation Current State (20 min)

7. **CLI_MCP_TOOLS_AUDIT.md** (command inventory)
   - 60+ CLI commands found
   - Only ~23 documented
   - Major gap identified

8. **CORE_DOCS_ENHANCEMENT_PLAN.md** (what needs adding)
   - Templates for git checkpoints
   - Cross-AI coordination examples
   - Skills doc references

9. **DOCUMENTATION_MASTER_PLAN.md** (this effort)
   - 4-AI coordination strategy
   - Goals and subtasks
   - Success criteria

---

## AI-Specific Investigation Paths

### For Gemini (Production Docs Audit)

**After core investigation, read:**

10. **docs/production/00_COMPLETE_SUMMARY.md**
    - Current overview of all 27 docs
    - Need to add Core vs Advanced split

11. **Scan all 27 production docs for:**
    - References to `calibration/` (DEPRECATED)
    - References to `DriftMonitor` (should be `MirrorDriftMonitor`)
    - References to `ParallelReasoningSystem` (DEPRECATED)
    - References to moved components
    - Outdated file paths

12. **For each doc, check:**
    - Code examples still work?
    - Architecture matches current state?
    - References other docs correctly?

**Breadcrumb trail:**
```
CANONICAL_DIR_STRUCTURE → COMPREHENSIVE_UNDERSTANDING → 
DEEP_EXPLORATION → production/00_COMPLETE_SUMMARY → 
Each of 27 production docs
```

---

### For Qwen (User Docs Creation)

**After core investigation, read:**

10. **docs/skills/SKILL.md** (48KB AI agent guide)
    - Understand user perspective
    - See what AI agents need to know
    - Model for writing style

11. **docs/architecture/GIT_CHECKPOINT_ARCHITECTURE.md**
    - Git automation details
    - Cross-AI coordination
    - Storage architecture

12. **Current user docs to understand gaps:**
    - docs/installation.md (current version)
    - docs/architecture.md (current version)
    - docs/getting-started.md (current version)

13. **Templates from CORE_DOCS_ENHANCEMENT_PLAN.md:**
    - Git checkpoint sections
    - Cross-AI coordination examples
    - Interface choice sections

**Breadcrumb trail:**
```
CANONICAL_DIR_STRUCTURE → COMPREHENSIVE_UNDERSTANDING → 
SKILL.md → GIT_CHECKPOINT_ARCH → Current docs → 
Enhancement templates → Write new docs
```

---

### For Copilot Claude (CLI/MCP Documentation)

**After core investigation, run:**

10. **Extract all CLI commands:**
```bash
empirica --help | tee cli_commands_list.txt
for cmd in $(empirica --help | grep "^  " | awk '{print $1}'); do
    echo "=== $cmd ===" >> cli_full_help.txt
    empirica $cmd --help >> cli_full_help.txt 2>&1
done
```

11. **Read CLI_MCP_TOOLS_AUDIT.md** (command categories)
    - Known categories
    - Expected counts
    - Gaps identified

12. **Review current tool catalog:**
    - docs/production/20_TOOL_CATALOG.md
    - See what's already documented
    - Identify missing commands

13. **Check MCP server for tool list:**
```python
from mcp_local.empirica_mcp_server import EmpricaMCPServer
server = EmpricaMCPServer()
print(list(server.tools.keys()))
```

**Breadcrumb trail:**
```
CANONICAL_DIR_STRUCTURE → COMPREHENSIVE_UNDERSTANDING → 
Extract all commands → CLI_MCP_AUDIT → Current catalog → 
MCP tool list → Document each command
```

---

### For RovoDev (Integration & Cleanup)

**After core investigation:**

10. **Scan all docs/ for deprecated references:**
```bash
grep -r "calibration/\|DriftMonitor\|ParallelReasoning" docs/ --include="*.md"
grep -r "components/tool_management\|cognitive_benchmarking" docs/ --include="*.md"
```

11. **Check cross-references:**
```bash
# Find all internal links
grep -r "\[.*\](.*\.md)" docs/ --include="*.md"
# Verify each link target exists
```

12. **Review other AIs' progress:**
```bash
empirica goals-discover --from-ai-id gemini
empirica goals-discover --from-ai-id qwen
empirica goals-discover --from-ai-id copilot-claude
```

13. **Monitor git checkpoints:**
```bash
git notes list | grep empirica
```

**Breadcrumb trail:**
```
CANONICAL_DIR_STRUCTURE → COMPREHENSIVE_UNDERSTANDING → 
Scan for deprecated → Check cross-refs → Monitor other AIs → 
Integrate changes → Final review
```

---

## Epistemic Checkpoints

### Before Starting Writing (CHECK):

**Ask yourself:**
- KNOW >0.8: Do I deeply understand Empirica architecture?
- CLARITY >0.8: Do I know exactly what to document?
- UNCERTAINTY <0.3: Are my unknowns resolved?

**If NO to any:**
- Read more breadcrumb docs
- Test more commands
- Ask user for clarification
- Coordinate with other AIs

---

## Git Checkpoint Milestones

### Each AI should create checkpoints at:

**PREFLIGHT:**
```bash
empirica preflight "Start documentation work for [your domain]" --ai-id <your-ai>
```

**After investigation:**
```bash
empirica check <session-id>
# If confidence ≥0.7, proceed to writing
# If <0.7, investigate more
```

**After each major section:**
```bash
empirica check <session-id>
# Record progress
```

**When complete:**
```bash
empirica postflight <session-id>
# Measure learning delta
```

---

## Coordination Protocol

### Discover what others are doing:

**Every 2-4 hours, check:**
```bash
empirica goals-discover --from-ai-id gemini
empirica goals-discover --from-ai-id qwen  
empirica goals-discover --from-ai-id copilot-claude
empirica goals-discover --from-ai-id rovodev
```

### If you need information from another AI:
1. Check their goal progress
2. Read their git checkpoints
3. If blocked, create handoff report

### When passing work:
```bash
empirica handoff-create <session-id> \
  --summary "Completed X, next AI should do Y" \
  --findings "Found A, B, C issues"
```

---

## Success Validation

### Before marking subtask complete:

**For documentation:**
- [ ] Code examples tested
- [ ] Links verified
- [ ] Terminology consistent
- [ ] No deprecated references
- [ ] Cross-references correct

**For investigation:**
- [ ] All breadcrumb docs read
- [ ] Architecture understood
- [ ] Gaps identified
- [ ] Ready to write

---

**Breadcrumb depth:** 13 documents minimum before writing  
**Investigation time:** 1-2 hours before creating content  
**Checkpoint frequency:** Every major milestone

This ensures high-quality, accurate documentation! ✅
