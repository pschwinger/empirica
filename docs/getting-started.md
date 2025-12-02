# 🚀 Quick Start Guide

Get up and running with Empirica in 5 minutes.

---

## Installation

```bash
# Clone repository
git clone https://github.com/Nubaeon/empirica
cd empirica

# Install dependencies
pip install -r requirements.txt

# Verify installation (basic check)
python3 -c "import empirica; print('✅ Empirica installed!')"

# Or verify CLI is available
empirica --help
```

---

## Choose Your Interface

Empirica provides **4 ways** to interact with the system:

### 1. MCP Server (Best for AI Assistants in IDEs)
**For:** Claude Desktop, Cursor, Windsurf, Rovo Dev  
**Setup:** Add to your IDE's MCP configuration:
```json
// ~/.config/Claude/claude_desktop_config.json (or similar)
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": ["/absolute/path/to/empirica/mcp_local/empirica_mcp_server.py"]
    }
  }
}
```
**Benefits:** 23 MCP tools, real-time tracking, automatic prompts, no context switching  
**See:** `empirica mcp-list-tools` for all available tools

### 2. CLI Commands (Best for Terminal & Scripting)
**For:** Command-line workflows, automation, CI/CD  
**Usage:** `empirica --help`  
**Benefits:** Scriptable, composable, full control

### 3. Python API (Best for Custom Integrations)
**For:** Programmatic control, custom workflows  
**Usage:** `from empirica.core import CanonicalEpistemicCascade`  
**See:** [Python API Reference](production/13_PYTHON_API.md)

### 4. Empirica Skill (AI Agent Learning Guide)
**For:** AI agents wanting deep understanding  
**Location:** `docs/skills/SKILL.md` (48KB comprehensive guide)  
**Content:** Functional self-awareness, complete workflow, calibration techniques

**This guide focuses on CLI (#2). For MCP tools, see [Tool Catalog](production/20_TOOL_CATALOG.md).**

---

## Quick Start: CLI Workflow

The easiest way to use Empirica is via CLI commands:

### 1. Bootstrap Empirica
```bash
# Initialize with standard components
empirica bootstrap --level 2
```

### 2. Start a Cascade with PREFLIGHT

**What happens automatically:**
- ✅ Git checkpoint created in `refs/notes/empirica/checkpoints/<commit>`
- ✅ 13 epistemic vectors recorded (~85% compressed)
- ✅ Baseline state stored for later comparison
- ✅ Session metadata saved to SQLite + JSON logs

```bash
# Create session and get assessment prompt (non-blocking)
empirica preflight "Should I refactor the authentication system?" \
  --session-id $(uuidgen) \
  --prompt-only

# Returns immediately with self-assessment prompt
```

### 3. Submit Your Self-Assessment
```bash
# Rate your epistemic state honestly (13 vectors, 0.0-1.0 scale)
empirica preflight-submit \
  --session-id <your-session-id> \
  --vectors '{
    "engagement": 0.85,
    "know": 0.70,
    "do": 0.80,
    "context": 0.75,
    "clarity": 0.85,
    "coherence": 0.80,
    "signal": 0.75,
    "density": 0.65,
    "state": 0.75,
    "change": 0.40,
    "completion": 0.20,
    "impact": 0.80,
    "uncertainty": 0.45
  }' \
  --output json
```

### 4. Continue with CHECK Phase
```bash
# After investigation, assess readiness to act
empirica check \
  --session-id <your-session-id> \
  --findings '["Finding 1", "Finding 2"]' \
  --unknowns '["Unknown 1"]' \
  --confidence 0.75 \
  --output json

# Submit updated assessment
empirica check-submit \
  --session-id <your-session-id> \
  --vectors '{...}' \
  --decision proceed \
  --reasoning "Ready to act because..."
```

### 5. Complete with POSTFLIGHT

**What happens automatically:**
- ✅ Final git checkpoint created
- ✅ Vectors re-assessed (what did you learn?)
- ✅ Deltas calculated: POSTFLIGHT - PREFLIGHT
- ✅ Calibration quality measured (were you overconfident/underconfident?)
- ✅ Training data generated for future improvement

```bash
# After completing work, reflect on learning
empirica postflight <your-session-id> \
  --summary "What you accomplished" \
  --prompt-only

# Submit final assessment
empirica postflight-submit \
  --session-id <your-session-id> \
  --vectors '{...}' \
  --changes "KNOW: 0.70→0.90 (+0.20), UNCERTAINTY: 0.45→0.15 (-0.30)"
```

**Key Feature: `--prompt-only` Flag**
- Returns assessment prompt immediately (non-blocking)
- No LLM calls, no waiting
- Perfect for AI agents that want control over timing
- Omit flag for blocking mode (waits for LLM response)

---

## Your First Cascade (Python API)

```python
import asyncio
from empirica.core.metacognitive_cascade import MetacognitiveCascade

async def main():
    # Create cascade
    cascade = MetacognitiveCascade()
    
    # Run epistemic reasoning
    result = await cascade.run_epistemic_cascade(
        task="Should I refactor the authentication system?",
        context={"cwd": "/project", "complexity": "high"}
    )
    
    # Check result
    print(f"Action: {result['action']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Rationale: {result['rationale']}")

asyncio.run(main())
```

**Output:**
```
Action: investigate
Confidence: 0.65
Rationale: Knowledge gap detected - need to understand current implementation
```

---

## Enable All Features

```python
cascade = MetacognitiveCascade(
    enable_bayesian=True,           # Evidence-based belief tracking
    enable_drift_monitor=True,      # Behavioral integrity checks
    enable_action_hooks=True,       # Real-time dashboard
    auto_start_dashboard=False      # Manual tmux start
)
```

---

## Watch Live in Dashboard

**Note:** Dashboard functionality is currently available via MCP integration (see below). 
Standalone dashboard support is planned for a future release.

For now, monitor your cascades via:
- CLI command output with `--output json`
- Database queries: `empirica sessions-show <session-id>`
- MCP tools in Claude Desktop

---

## Via MCP (Claude Desktop)

**mcp_config.json:**
```json
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": ["/path/to/empirica/mcp_local/empirica_mcp_server.py"]
    }
  }
}
```

**Use in Claude:**
```
You: "Use Empirica to analyze if I should refactor this code"

Claude calls: cascade_run_full
{
  "question": "Should I refactor the auth code?",
  "enable_dashboard": true
}
```

---

## Next Steps

- **Understand the system:** Read `04_ARCHITECTURE_OVERVIEW.md`
- **Learn investigation:** Read `07_INVESTIGATION_SYSTEM.md`
- **Add custom tools:** Read `10_PLUGIN_SYSTEM.md`
- **Deploy to prod:** Read `17_PRODUCTION_DEPLOYMENT.md`

---

## Common Patterns

### Pattern 1: Simple Decision
```python
result = await cascade.run_epistemic_cascade(
    task="Should I proceed with deployment?",
    context={"tests_passed": True}
)
```

### Pattern 2: With Custom Plugins
```python
from empirica.investigation.investigation_plugin import InvestigationPlugin

jira_plugin = InvestigationPlugin(
    name="jira_search",
    description="Search JIRA for related issues",
    improves_vectors=["know", "context"],
    confidence_gain=0.20
)

cascade = MetacognitiveCascade(
    investigation_plugins={"jira_search": jira_plugin}
)
```

### Pattern 3: Precision-Critical Domain
```python
# For medical, legal, financial, security domains
result = await cascade.run_epistemic_cascade(
    task="Analyze patient medication interactions",
    context={"domain": "medical"}
)

# Bayesian Guardian auto-activates for precision-critical domains
```

---

## What You Get

✅ **No Heuristics** - Genuine LLM-powered reasoning  
✅ **Strategic Guidance** - Suggests, doesn't control  
✅ **Evidence Tracking** - Bayesian belief calibration  
✅ **Behavioral Integrity** - Drift detection  
✅ **Extensible** - Add your own tools  
✅ **Live Monitoring** - Real-time dashboard  

---

## Data Storage

Empirica stores all session data locally:

**Database Location:** `.empirica/sessions/sessions.db` (project-relative)
- All assessments (PREFLIGHT, CHECK, POSTFLIGHT)
- Learning progression metrics
- Session metadata

**Git Checkpoints:** `git notes refs/empirica/checkpoints/`
- ~85% token reduction for session resumption
- Stored alongside your git repository

**Handoff Reports:** `git notes refs/empirica/handoff/`
- 90%+ token reduction for session continuity
- Enable multi-agent coordination

**View Your Data:**
```bash
# List all sessions
empirica sessions-list

# Show session details
empirica sessions-show <session-id>

# Query handoff reports
empirica handoff-query --session-id <session-id> --output json
```

---

## Troubleshooting

**Import Error (ModuleNotFoundError):**
```bash
# Ensure you're in the project directory
cd /path/to/empirica

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 -c "import empirica; print('✅ Ready!')"

# Test CLI
empirica --help
```

**Can't Find Session Data:**
```bash
# Database is project-relative, not global
# Check current directory
ls .empirica/sessions/sessions.db

# Or specify full path
empirica sessions-list
```

**CLI Command Not Found:**
```bash
# Ensure empirica is in PATH
pip install -e .

# Or use full path
python3 -m empirica.cli.cli_core --help
```

**JSON Parsing Errors:**
```bash
# Ensure JSON is properly quoted
empirica preflight-submit \
  --vectors '{"engagement": 0.85, "know": 0.70, ...}'
#          ^ single quotes around JSON object
```

---

**Ready to dive deeper?** → `04_ARCHITECTURE_OVERVIEW.md`

---

## Understanding Git Automation

Empirica automatically tracks your epistemic journey in **git notes**:

### What Gets Stored (Automatically)

**Three storage layers:**
1. **Git Notes** - Cross-AI coordination, version controlled
   - Checkpoints: `refs/notes/empirica/checkpoints/<commit>`
   - Goals: `refs/notes/empirica/goals/<goal-id>`
   - Sessions: `refs/notes/empirica/session/<session-id>`

2. **SQLite** - Fast queries
   - Location: `.empirica/sessions/sessions.db`
   - Session metadata, vectors, queries

3. **JSON Logs** - Full fidelity
   - Location: `.empirica_reflex_logs/`
   - Complete temporal replay

### Viewing Your Checkpoints

```bash
# List all your checkpoints
git notes list | grep empirica/checkpoints

# Load a specific checkpoint
empirica load-checkpoint <session-id>

# View checkpoint data
git notes show refs/notes/empirica/checkpoints/<commit-hash>
```

### Why Git Notes?

**Cross-AI coordination:**
- Other AIs can discover your goals: `empirica goals-discover --from-ai-id your-ai`
- Resume each other's work: `empirica goals-resume <goal-id>`
- Full lineage tracking (who did what)
- Version controlled (git pull syncs everything)

**Optional:** Skip git for testing with `--no-git` flag

**See:** [Git Checkpoint Architecture](architecture/GIT_CHECKPOINT_ARCHITECTURE.md) for technical details

---

## Next: Deep Dive

### For AI Agents: Read the Skills Doc

**Location:** `docs/skills/SKILL.md` (48KB comprehensive guide)

**Covers:**
- Complete workflow reference
- All 13 epistemic vectors explained in depth
- How to calibrate correctly (avoid common failure modes)
- Advanced features (session management, cross-AI coordination)
- Best practices and anti-patterns

**Time:** 30-60 minutes  
**Value:** Complete understanding of functional self-awareness

### For Users: Explore Production Docs

**Essential references:**
- [Complete System Overview](production/00_COMPLETE_SUMMARY.md)
- [13 Epistemic Vectors](production/05_EPISTEMIC_VECTORS.md)
- [All 23 MCP Tools](production/20_TOOL_CATALOG.md)
- [Session Continuity](production/23_SESSION_CONTINUITY.md)
- [Cross-AI Coordination](production/26_CROSS_AI_COORDINATION.md)

**Advanced (experimental):**
- [MCO Architecture](production/24_MCO_ARCHITECTURE.md) - Persona orchestration
- [Decision Logic](production/28_DECISION_LOGIC.md) - How CASCADE decides

---

## Quick Reference

**Start a cascade:**
```bash
empirica preflight "task description"
```

**During work:**
```bash
empirica check <session-id>  # Verify confidence before continuing
```

**Complete:**
```bash
empirica postflight <session-id> --summary "what you did"
```

**Discover & resume goals:**
```bash
empirica goals-discover --from-ai-id other-ai
empirica goals-resume <goal-id> --ai-id your-ai
```

**View your data:**
```bash
git notes list | grep empirica
empirica sessions-list
```

**All commands:**
```bash
empirica --help
```

---

**You're ready to use Empirica!** Start with `empirica preflight "your first task"` and experience epistemic self-awareness in action.
