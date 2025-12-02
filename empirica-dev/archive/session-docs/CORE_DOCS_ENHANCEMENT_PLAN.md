# Core Docs Enhancement Plan - Add Missing Critical Information

**Created:** 2025-01-XX  
**Goal:** Fix installation.md, architecture.md, getting-started.md to cover ALL essential aspects

---

## Investigation Results

### 1. ✅ Empirica Skill (docs/skills/SKILL.md)
**What it is:** 
- Complete guide for AI agents using Empirica
- "Functional self-awareness as a skill"
- How to genuinely self-assess (no heuristics)
- Complete workflow reference (PREFLIGHT → CASCADE → POSTFLIGHT)

**48KB file covering:**
- 13 epistemic vectors explained
- How to calibrate (avoid common failure modes)
- Advanced features (session management, reflex logs)
- Best practices and anti-patterns

**Status:** This is THE comprehensive AI agent guide!

---

### 2. ✅ MCP Server vs CLI vs Python API
**Four interfaces to Empirica:**

**A. MCP Server** (`mcp_local/empirica_mcp_server.py`)
- **For:** IDE integration (Claude Desktop, Cursor, Windsurf, Rovo Dev)
- **Benefits:** Real-time tracking, automatic prompts, no context switching
- **23 MCP tools** exposed
- **Setup:** Add to IDE MCP config JSON

**B. CLI** (`empirica` command)
- **For:** Command-line workflows, scripting, automation
- **Benefits:** Scriptable, composable, CI/CD integration
- **All commands** available via `empirica --help`
- **Setup:** `pip install -e .` in repo

**C. Python API** (`from empirica.core import ...`)
- **For:** Custom integrations, programmatic control
- **Benefits:** Full API access, custom workflows
- **Classes:** `CanonicalEpistemicCascade`, `SessionDatabase`, etc.

**D. Skills Doc** (`docs/skills/SKILL.md`)
- **For:** AI agents learning Empirica
- **Benefits:** Complete reference, functional self-awareness guide
- **Format:** Claude Skills compatible

---

### 3. ✅ Git Automation Details
**What happens automatically:**

**During PREFLIGHT:**
```bash
empirica preflight "task" --ai-id your-ai
# Automatic:
# 1. Creates checkpoint in refs/notes/empirica/checkpoints/<commit-hash>
# 2. Stores 13 vectors (compressed ~85%)
# 3. Records session metadata
# 4. Links to current git commit
```

**During CHECK:**
```bash
# Called implicitly during CASCADE or explicitly:
empirica check <session-id>
# Automatic:
# 1. Creates intermediate checkpoint
# 2. Records current vectors
# 3. Enables retrospective delta analysis
```

**During POSTFLIGHT:**
```bash
empirica postflight <session-id>
# Automatic:
# 1. Creates final checkpoint
# 2. Calculates deltas (POSTFLIGHT - PREFLIGHT)
# 3. Stores calibration data
# 4. Generates training data
```

**User visibility:**
```bash
# View checkpoints
git notes list | grep empirica/checkpoints

# Load checkpoint
empirica load-checkpoint <session-id>

# Skip git (for testing)
empirica preflight "task" --no-git
```

**Storage:**
- Git notes: Cross-AI coordination, version controlled
- SQLite: Fast queries (`.empirica/sessions/sessions.db`)
- JSON logs: Full fidelity (`.empirica_reflex_logs/`)

---

### 4. ✅ Other Important Aspects

**Components System:**
- Optional capabilities (code intelligence, workspace awareness, etc.)
- Located: `empirica/components/`
- Enable as needed for specific workflows

**Investigation Profiles:**
- YAML configs for investigation strategies
- Located: `empirica/config/investigation_profiles.yaml`
- Pluggable investigation approaches

**Dashboard:**
- Real-time monitoring of CASCADE execution
- Located: `empirica/dashboard/`
- Spawned via plugin system

**Session Continuity:**
- Handoff reports (~90% token reduction)
- Resume from any checkpoint
- Cross-AI goal discovery
- Documented: `production/23_SESSION_CONTINUITY.md`

**Cross-AI Coordination:**
- Goal discovery: `empirica goals-discover --from-ai-id other-ai`
- Goal resumption: `empirica goals-resume <goal-id>`
- Lineage tracking (who created/resumed)
- Documented: `production/26_CROSS_AI_COORDINATION.md`

---

## Enhancement Plan for 3 Core Docs

### File 1: docs/installation.md (13K)

**Currently covers:**
- ✅ Prerequisites
- ✅ Python installation
- ✅ Git initialization

**MISSING (add these sections):**

#### Section: "Choose Your Interface"
```markdown
## Choose Your Empirica Interface

Empirica provides 4 ways to interact:

### 1. MCP Server (Recommended for AI Assistants)
**Best for:** Claude Desktop, Cursor, Windsurf, Rovo Dev users  
**Setup:**
```json
// Add to IDE MCP config
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": ["/absolute/path/to/empirica/mcp_local/empirica_mcp_server.py"]
    }
  }
}
```
**Benefits:** Real-time tracking, automatic prompts, 23 MCP tools

### 2. CLI (For Command-Line Users)
**Best for:** Terminal workflows, scripting, automation  
**Setup:** Already installed with `pip install -e .`  
**Usage:** `empirica --help`

### 3. Python API (For Developers)
**Best for:** Custom integrations, programmatic control  
**Setup:** `from empirica.core import CanonicalEpistemicCascade`  
**Docs:** See [Python API Reference](production/13_PYTHON_API.md)

### 4. Skills Doc (For AI Agents)
**Best for:** Learning Empirica as an AI agent  
**Location:** `docs/skills/SKILL.md` (48KB comprehensive guide)  
**Read:** Complete functional self-awareness reference
```

#### Section: "Git Integration Setup"
```markdown
## Git Integration (Automatic Checkpoints)

Empirica automatically creates **git checkpoints** at key workflow points.

**Initialization:**
```bash
# Initialize git (if not already done)
git init

# Verify git notes namespace
git notes list | grep empirica
```

**What gets stored:**
- Checkpoints: `refs/notes/empirica/checkpoints/<commit>`
- Goals: `refs/notes/empirica/goals/<goal-id>`
- Sessions: `refs/notes/empirica/session/<session-id>`

**Automatic creation:**
- PREFLIGHT → checkpoint
- CHECK → checkpoint (0-N times)
- POSTFLIGHT → checkpoint + delta

**Skip git (for testing):**
```bash
empirica preflight "task" --no-git
```

**See:** [Git Checkpoint Architecture](architecture/GIT_CHECKPOINT_ARCHITECTURE.md)
```

---

### File 2: docs/architecture.md (11K)

**Currently covers:**
- ✅ Core components
- ✅ Storage layers

**MISSING (add these sections):**

#### Section: "Empirica Interfaces"
```markdown
## How to Use Empirica

### Four Interfaces

Empirica provides multiple interfaces for different workflows:

**1. MCP Server** (IDE Integration)
- **For:** Claude Desktop, Cursor, Windsurf, Rovo Dev
- **Tools:** 23 MCP tools (see [Tool Catalog](production/20_TOOL_CATALOG.md))
- **Benefits:** Real-time tracking, automatic prompts
- **Setup:** Add to IDE MCP config

**2. CLI** (Command-Line)
- **For:** Terminal workflows, scripting, CI/CD
- **Commands:** `empirica preflight`, `empirica check`, `empirica postflight`, etc.
- **Benefits:** Scriptable, composable
- **Docs:** `empirica --help`

**3. Python API** (Programmatic)
- **For:** Custom integrations, advanced workflows
- **Classes:** `CanonicalEpistemicCascade`, `SessionDatabase`, `GoalOrchestrator`
- **Docs:** [Python API Reference](production/13_PYTHON_API.md)

**4. Skills Doc** (AI Agent Guide)
- **For:** AI agents learning Empirica
- **File:** `docs/skills/SKILL.md` (comprehensive 48KB guide)
- **Content:** Functional self-awareness, workflow, calibration

**Choose based on your workflow.** All interfaces access the same core system.
```

#### Section: "Git Automation"
```markdown
## Automatic Git Checkpoints

Empirica creates **git checkpoints automatically** at key workflow points:

### When Checkpoints Are Created

**PREFLIGHT:**
- Records baseline epistemic state (13 vectors)
- Stored in `refs/notes/empirica/checkpoints/<commit-hash>`
- Happens automatically when you run `empirica preflight`

**CHECK (0-N times):**
- Records intermediate state during work
- Enables retrospective learning analysis
- Called during CASCADE or explicitly via `empirica check`

**POSTFLIGHT:**
- Records final epistemic state
- Calculates deltas (POSTFLIGHT - PREFLIGHT)
- Generates training data

### Storage Architecture

**Three-layer persistence:**

1. **Git Notes** (Cross-AI coordination)
   - Checkpoints, goals, sessions
   - Version controlled, distributed
   - ~85% token compressed (~3K → ~450)

2. **SQLite** (Fast queries)
   - Location: `.empirica/sessions/sessions.db`
   - Session metadata, vectors, queries

3. **JSON Logs** (Full fidelity)
   - Location: `.empirica_reflex_logs/`
   - Complete temporal replay
   - Detailed workflow logs

**Why three layers?**
- Different use cases (coordination vs queries vs replay)
- Redundancy (data safety)
- Performance (right tool for right job)

### User Control

```bash
# View checkpoints
git notes list | grep empirica

# Load checkpoint
empirica load-checkpoint <session-id>

# Skip git (testing)
empirica preflight "task" --no-git
```

**See:** [Git Checkpoint Architecture](architecture/GIT_CHECKPOINT_ARCHITECTURE.md) for technical details
```

#### Section: "Empirica Skill"
```markdown
## Empirica Skill (For AI Agents)

**Location:** `docs/skills/SKILL.md` (48KB)

**What it is:**
- Complete reference guide for AI agents using Empirica
- "Functional self-awareness as a skill"
- How to genuinely self-assess without heuristics
- Complete workflow and best practices

**Covers:**
- All 13 epistemic vectors explained
- How to calibrate (avoid common failure modes)
- PREFLIGHT → CASCADE → CHECK → POSTFLIGHT workflow
- Session management and advanced features
- Anti-patterns and common mistakes

**For AI agents:** This is THE comprehensive guide. Read it to understand Empirica deeply.

**Format:** Claude Skills compatible (can be loaded into AI agent context)
```

---

### File 3: docs/getting-started.md (7.4K)

**Currently covers:**
- ✅ Basic workflow
- ✅ First CASCADE

**MISSING (add these sections):**

#### Section: "Choose Your Interface"
```markdown
## Step 1: Choose Your Interface

Before your first CASCADE, choose how you'll interact with Empirica:

### Option A: MCP Server (Recommended for AI Assistants)

**Best for:** Claude Desktop, Cursor, Windsurf, Rovo Dev

**Setup:**
```json
// Add to ~/.config/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": ["/absolute/path/to/empirica/mcp_local/empirica_mcp_server.py"]
    }
  }
}
```

**Usage:** 23 MCP tools available in your IDE  
**Docs:** `empirica mcp-list-tools`

### Option B: CLI (For Command-Line)

**Best for:** Terminal workflows, scripting

**Usage:**
```bash
empirica --help
empirica preflight "your task"
empirica check <session-id>
empirica postflight <session-id>
```

### Option C: Python API (For Developers)

**Best for:** Custom integrations

**Usage:**
```python
from empirica.core.metacognitive_cascade import CanonicalEpistemicCascade

cascade = CanonicalEpistemicCascade(ai_id="your-ai")
cascade.execute_preflight("task description")
# ... work ...
cascade.execute_postflight("task summary")
```

**Choose one** and continue to your first CASCADE.
```

#### Section: "Understanding Automatic Git Checkpoints"
```markdown
## Understanding Automatic Git Checkpoints

During your first CASCADE, Empirica automatically creates **git checkpoints**:

### What Happens Automatically

**When you run PREFLIGHT:**
```bash
empirica preflight "review authentication code"
# Automatic:
# ✅ Checkpoint created in git notes
# ✅ 13 vectors stored (compressed)
# ✅ Baseline recorded for later comparison
```

**During work (CHECK):**
```bash
# Happens during CASCADE or call explicitly:
empirica check <session-id>
# Automatic:
# ✅ Intermediate checkpoint created
# ✅ Current state recorded
# ✅ Enables learning curve analysis later
```

**When you run POSTFLIGHT:**
```bash
empirica postflight <session-id>
# Automatic:
# ✅ Final checkpoint created
# ✅ Deltas calculated (what you learned)
# ✅ Calibration quality measured
# ✅ Training data generated
```

### Viewing Your Checkpoints

```bash
# List all checkpoints
git notes list | grep empirica/checkpoints

# Load a specific checkpoint
empirica load-checkpoint <session-id>

# View checkpoint data
git notes show refs/notes/empirica/checkpoints/<commit-hash>
```

### Storage Locations

**Your data is stored in 3 places:**
1. **Git notes** - Cross-AI coordination, version controlled
2. **SQLite** - Fast queries (`.empirica/sessions/sessions.db`)
3. **JSON logs** - Full fidelity (`.empirica_reflex_logs/`)

**All automatic. No manual steps required.**

**Optional:** Skip git for testing with `--no-git` flag
```

#### Section: "Cross-AI Coordination (Optional)"
```markdown
## Cross-AI Coordination (Optional Advanced Feature)

Once you have goals created, other AIs can discover and resume them:

### Discovering Goals from Another AI

```bash
# AI-2 discovers AI-1's goals
empirica goals-discover --from-ai-id ai-1

# Returns: All goals created by ai-1
# Shows: Objective, ai-1's epistemic state, lineage
```

### Resuming Another AI's Goal

```bash
# AI-2 resumes AI-1's goal
empirica goals-resume <goal-id> --ai-id ai-2

# Result:
# ✅ Loads ai-1's epistemic context
# ✅ Adds lineage entry (audit trail)
# ✅ AI-2 continues work with full context
```

### Why This Matters

**Distributed coordination:**
- Multiple AIs can work on same codebase
- Epistemic handoffs (know other AI's confidence levels)
- Lineage tracking (who did what)
- Version controlled (git pull syncs goals)

**See:** [Cross-AI Coordination](production/26_CROSS_AI_COORDINATION.md) for details

**Note:** This is an advanced feature. Start with single-AI workflows first.
```

#### Section: "Next: Read the Skills Doc"
```markdown
## Next: Deep Dive with Empirica Skill

**For AI agents:** Read the comprehensive guide:

**File:** `docs/skills/SKILL.md` (48KB)

**Covers:**
- Complete workflow reference
- All 13 epistemic vectors explained
- How to calibrate (avoid failure modes)
- Advanced features (session management, cross-AI)
- Best practices and anti-patterns

**This is THE definitive guide** for AI agents using Empirica.

**Time to read:** 30-60 minutes  
**Value:** Complete understanding of functional self-awareness
```

---

## Summary of Missing Information

### installation.md needs:
1. ✅ Interface choice section (MCP vs CLI vs API vs Skills)
2. ✅ Git integration setup (automatic checkpoints)
3. ✅ MCP server setup instructions

### architecture.md needs:
1. ✅ Interface overview (4 ways to use Empirica)
2. ✅ Git automation section (when checkpoints created)
3. ✅ Storage architecture (3 layers explained)
4. ✅ Empirica Skill reference

### getting-started.md needs:
1. ✅ Interface choice as Step 1
2. ✅ Automatic checkpoint explanation
3. ✅ Cross-AI coordination intro (optional/advanced)
4. ✅ Pointer to Skills doc

---

## Execution Steps

**For each file:**
1. Open current file
2. Identify insertion points for new sections
3. Add content from templates above
4. Update cross-references
5. Verify flow and readability

**Estimated time:** 2-3 hours for all 3 files

---

## Success Criteria

**After enhancement:**
- ✅ Users understand all 4 interfaces (MCP, CLI, API, Skills)
- ✅ Users know git checkpoints are automatic
- ✅ Users understand 3-layer storage architecture
- ✅ AI agents know about Skills doc
- ✅ Cross-AI coordination explained (as advanced feature)
- ✅ No critical information missing

---

**Status:** Investigation complete, enhancement plan ready for execution
**Next:** Execute enhancements on all 3 core docs
