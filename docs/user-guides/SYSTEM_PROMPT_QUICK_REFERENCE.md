# Empirica System Prompt Quick Reference

**Install in 30 seconds:**

```bash
cd /path/to/empirica
bash scripts/install_system_prompts.sh
```

---

## What Gets Installed

| AI Agent | File Location | Effect |
|----------|---------------|--------|
| **Gemini CLI** | `~/.gemini/system_empirica.md` | Replaces entire system prompt |
| **Claude Code** | `CLAUDE.md` (project root) | Supplements system prompt |

---

## Environment Variable (Gemini Only)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
```

Then reload:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

---

## Verification Tests

### Test Gemini CLI

```bash
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini
```

Ask: `"What framework are you using?"`

**Expected:** Should mention Empirica, CASCADE workflow, epistemic vectors

---

### Test Claude Code

```bash
cd /path/to/empirica
claude
```

Ask: `"What workflow phases do you follow?"`

**Expected:** Should list BOOTSTRAP → PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT

---

## What You Get

**CASCADE Workflow:**
1. BOOTSTRAP - Initialize session
2. PREFLIGHT - Assess starting epistemic state
3. GENERATE GOALS - Systematic investigation planning
4. INVESTIGATE - Multi-turn exploration with belief tracking
5. CHECK - Readiness assessment
6. ACT - Execute the work
7. POSTFLIGHT - Measure learning
8. CALIBRATION REPORT - Confidence accuracy

**13 Epistemic Vectors:**
- engagement, know, do, context
- clarity, coherence, signal, density
- state, change, completion, impact
- uncertainty

**MCP Tools (21 total via v2 CLI wrapper):**
- `execute_preflight`, `submit_preflight_assessment`
- `goals-list`, `create_goal`
- `query_bayesian_beliefs`, `check_drift_monitor`
- `create_git_checkpoint`, `load_git_checkpoint`
- And 15 more (routes to Empirica CLI for reliability)

---

## Usage Example

```bash
# Start Gemini with Empirica
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini

# Agent will follow CASCADE workflow automatically
You: "Help me debug our authentication system"

Agent:
> I'll use the Empirica CASCADE workflow:
>
> 1. BOOTSTRAP: Starting session...
> 2. PREFLIGHT: My starting epistemic state:
>    - KNOW: 0.3 (don't know your auth system)
>    - UNCERTAINTY: 0.8 (need investigation)
>
> 3. INVESTIGATE: Exploring codebase...
>    [Uses goal management, tracks beliefs]
>
> 4. CHECK: Confidence to proceed: 0.85
>
> 5. ACT: [Debugs the issue]
>
> 6. POSTFLIGHT: Learning delta:
>    - KNOW: 0.3 → 0.9
>    - Calibration: Well-calibrated
```

---

## Troubleshooting

**Gemini not using Empirica:**
```bash
# Check environment variable
echo $GEMINI_SYSTEM_MD

# Should print: ~/.gemini/system_empirica.md
# If not, run:
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
```

**Claude not using Empirica:**
```bash
# Check CLAUDE.md exists in project root
ls -lh /path/to/empirica/CLAUDE.md

# Make sure you're in the right directory
cd /path/to/empirica
```

---

## Full Documentation

- **Installation Guide:** `docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md`
- **AI Quick Start:** `docs/01_a_AI_AGENT_START.md`
- **MCP Tools:** `docs/04_MCP_QUICKSTART.md`
- **Epistemic Vectors:** `docs/guides/CLI_GENUINE_SELF_ASSESSMENT.md`

---

## Platform Comparison

| Feature | Gemini CLI | Claude Code |
|---------|------------|-------------|
| **Method** | Environment variable | Project file |
| **Scope** | Global (all sessions) | Project-specific |
| **Replacement** | Complete | Supplement |
| **Auto-load** | Yes (if env var set) | Yes (if in project) |
| **Customization** | Per-user | Per-project |

---

**Install now:**

```bash
cd /path/to/empirica
bash scripts/install_system_prompts.sh
```

**Questions?** Read: `docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md`
