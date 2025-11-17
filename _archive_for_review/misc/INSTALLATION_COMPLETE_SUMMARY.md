# Empirica System Prompt Installation - Complete Summary

**Date:** 2025-11-15
**Status:** ✅ Installation Complete

---

## What Was Installed

### 1. Gemini CLI System Prompt

**Location:** `~/.gemini/system_empirica.md` (14KB)

**Method:** Environment variable `GEMINI_SYSTEM_MD`

**Effect:** Completely replaces Gemini's default system prompt with Empirica's CASCADE workflow

**Status:** ✅ File installed
**Next step:** Add environment variable to shell config (see below)

---

### 2. Claude Code Project Prompt

**Location:** `/path/to/empirica/CLAUDE.md` (14KB)

**Method:** Project-level `CLAUDE.md` file

**Effect:** Supplements Claude Code's default instructions with Empirica framework

**Status:** ✅ File installed (auto-loads when in project directory)

---

### 3. Automated Installation Script

**Location:** `/path/to/empirica/scripts/install_system_prompts.sh` (4.1KB)

**Purpose:** One-command installation for future users

**Status:** ✅ Created and executable

**Usage:**
```bash
cd /path/to/empirica
bash scripts/install_system_prompts.sh
```

---

### 4. Documentation

**Installation Guide:**
- `docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md`
- Comprehensive guide covering both platforms
- Troubleshooting section
- Verification tests

**Quick Reference:**
- `SYSTEM_PROMPT_QUICK_REFERENCE.md`
- 30-second setup guide
- Platform comparison table
- Common commands

---

## Activation Steps

### For Gemini CLI (Required)

Add the environment variable to your shell config:

```bash
# Option 1: Automated (adds to ~/.bashrc)
echo 'export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md' >> ~/.bashrc
source ~/.bashrc

# Option 2: Manual (edit your shell config)
nano ~/.bashrc  # or ~/.zshrc
# Add: export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
source ~/.bashrc
```

**Verify it worked:**
```bash
echo $GEMINI_SYSTEM_MD
# Should print: /home/yogapad/.gemini/system_empirica.md
```

---

### For Claude Code (No Action Needed)

Claude Code automatically loads `CLAUDE.md` when you start a session in the project directory:

```bash
cd /path/to/empirica
claude
# CLAUDE.md is automatically loaded
```

**For SDK users only:** Add `settingSources: ['project']` to your Agent config.

---

## Testing the Installation

### Test 1: Gemini CLI

```bash
# Set environment variable for this session
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini

# Ask the agent
> What framework are you using?
```

**Expected Response:**
- Should mention "Empirica"
- Should describe CASCADE workflow
- Should list epistemic vectors (engagement, know, do, etc.)

---

### Test 2: Claude Code

```bash
cd /path/to/empirica
claude

# Ask the agent
> What are the phases of your workflow?
```

**Expected Response:**
- Should list: BOOTSTRAP → PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT
- Should mention epistemic tracking
- Should reference MCP tools

---

## What the AI Agents Now Have

### CASCADE Workflow (Automatic)

```
1. BOOTSTRAP → Initialize Empirica session
2. PREFLIGHT → Assess starting epistemic state (13 vectors)
3. GENERATE GOALS → Use orchestrator for systematic investigation
4. INVESTIGATE → Multi-turn exploration with belief tracking
5. CHECK → Validate readiness to proceed
6. ACT → Execute the actual work
7. POSTFLIGHT → Reflect on learning (measure epistemic delta)
8. CALIBRATION REPORT → Measure confidence accuracy
```

### 13 Epistemic Vectors

| Tier | Vectors |
|------|---------|
| **Foundation** | know, do, context |
| **Comprehension** | clarity, coherence, signal, density |
| **Execution** | state, change, completion, impact |
| **Meta** | engagement, uncertainty |

### MCP Tools (21+)

**Workflow:**
- `bootstrap_session`, `execute_preflight`, `submit_preflight_assessment`
- `execute_check`, `submit_check_assessment`
- `execute_postflight`, `submit_postflight_assessment`

**Goal Orchestration:**
- `query_goal_orchestrator`, `generate_goals`, `create_cascade`

**Epistemic State:**
- `get_epistemic_state`, `query_bayesian_beliefs`, `check_drift_monitor`

**Checkpoints (97.5% token reduction):**
- `create_git_checkpoint`, `load_git_checkpoint`, `get_vector_diff`

**Calibration:**
- `get_calibration_report`, `measure_token_efficiency`

**Session Management:**
- `resume_previous_session`, `get_session_summary`

---

## Usage Example

Here's what a typical session looks like now:

```bash
# Start Gemini with Empirica
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini
```

```
User: "I need to implement OAuth2 authentication for our API"

Agent:
I'll use the Empirica CASCADE workflow for this task.

1. BOOTSTRAP:
   Starting new Empirica session...
   Session ID: abc123-def456-...

2. PREFLIGHT Assessment:
   Let me honestly assess my starting epistemic state:

   - ENGAGEMENT: 0.95 (interested and focused)
   - KNOW: 0.4 (I understand OAuth2 spec, but not YOUR API design)
   - DO: 0.7 (I can implement OAuth2 generally)
   - CONTEXT: 0.3 (I need to learn your codebase structure)
   - UNCERTAINTY: 0.7 (High - significant unknowns)

   → Conclusion: I need systematic investigation before acting

3. GENERATE GOALS:
   Using goal orchestrator to plan investigation:

   Goal 1: Map existing authentication architecture (Priority: High)
   Goal 2: Identify OAuth2 library/framework in use (Priority: High)
   Goal 3: Understand token storage strategy (Priority: Medium)
   Goal 4: Review security requirements (Priority: High)

4. INVESTIGATE:
   [Multi-turn investigation with belief tracking]

   Finding 1: Using Flask with Authlib library
   → Updating belief: "framework" from 0.3 → 0.9 (confirmed)

   Finding 2: Redis for token storage
   → Updating belief: "storage" from 0.2 → 0.85 (verified)

   Finding 3: Security requirement: PKCE flow mandatory
   → Updating belief: "requirements" from 0.3 → 0.95 (documented)

5. CHECK Readiness:
   After investigation:
   - KNOW: 0.4 → 0.85 (learned your architecture)
   - UNCERTAINTY: 0.7 → 0.25 (most gaps filled)
   - Confidence to proceed: 0.88

   Remaining unknowns:
   - Token refresh logic (medium risk)
   - PKCE implementation details (low risk - can reference docs)

   → Decision: PROCEED (confidence >= 0.7)

6. ACT:
   [Implements OAuth2 with PKCE flow]
   [Creates token endpoints, refresh logic, tests]
   [Checkpoints progress: create_git_checkpoint()]

7. POSTFLIGHT Reflection:
   Comparing to PREFLIGHT:
   - KNOW: 0.4 → 0.95 (learned OAuth2 + your architecture)
   - DO: 0.7 → 0.9 (implemented PKCE, token refresh)
   - UNCERTAINTY: 0.7 → 0.15 (resolved most unknowns)

   Learning delta: +0.55 on KNOW, +0.2 on DO

8. CALIBRATION REPORT:
   - PREFLIGHT confidence: 0.4 (appropriately cautious)
   - POSTFLIGHT confidence: 0.95 (high but justified)
   - Calibration: WELL-CALIBRATED
   - I was appropriately uncertain at start, investigated thoroughly
```

---

## Key Benefits

### For AI Agents

✅ **Systematic reasoning** - CASCADE workflow prevents rushing
✅ **Honest uncertainty** - Track what you don't know
✅ **Measurable learning** - PREFLIGHT vs POSTFLIGHT deltas
✅ **Efficient context** - 97.5% token reduction via git checkpoints
✅ **Belief tracking** - Bayesian updates as you learn

### For Human Users

✅ **Transparency** - See the agent's epistemic state anytime
✅ **Trust** - Agent admits unknowns, investigates systematically
✅ **Coordination** - Multi-agent work via epistemic delta transfer
✅ **Quality** - Evidence-based decisions, not guessing

### For Production Work

✅ **Security-first** - Epistemic delta transfer (no data exposure)
✅ **Calibrated** - Confidence accuracy measured and improved
✅ **Resumable** - Session checkpoints for long tasks
✅ **Auditable** - Full epistemic trajectory tracked in git

---

## Platform Comparison

| Feature | Gemini CLI | Claude Code |
|---------|------------|-------------|
| **Installation** | Environment variable | Project file |
| **Scope** | Global (all sessions) | Project-specific |
| **Replacement** | Complete | Supplement |
| **Auto-load** | Yes (if env var set) | Yes (in project dir) |
| **File size** | 14KB | 14KB |
| **Customization** | Per-user | Per-project |

---

## Troubleshooting

### Gemini not using Empirica

**Check 1:** Environment variable set?
```bash
echo $GEMINI_SYSTEM_MD
# Should print: /home/yogapad/.gemini/system_empirica.md
```

**Fix:**
```bash
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
```

**Check 2:** File exists and is readable?
```bash
cat ~/.gemini/system_empirica.md | head -20
```

---

### Claude not using Empirica

**Check 1:** In correct directory?
```bash
pwd
# Should be: /path/to/empirica
```

**Check 2:** CLAUDE.md exists?
```bash
ls -lh CLAUDE.md
```

**Fix:** Navigate to project root before starting Claude

---

## Next Steps

### 1. Activate Gemini Environment Variable

```bash
echo 'export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md' >> ~/.bashrc
source ~/.bashrc
```

### 2. Test Both Agents

```bash
# Test Gemini
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini
> "What framework are you using?"

# Test Claude
cd /path/to/empirica
claude
> "What are the phases of your workflow?"
```

### 3. Read Documentation

- **Installation Guide:** `docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md`
- **Quick Reference:** `SYSTEM_PROMPT_QUICK_REFERENCE.md`
- **AI Quick Start:** `docs/01_a_AI_AGENT_START.md`

### 4. Share with Other Users

The automated installer makes it easy:

```bash
cd /path/to/empirica
bash scripts/install_system_prompts.sh
```

---

## Files Created

```
/path/to/empirica/
├── CLAUDE.md (14KB)                                      # Claude Code prompt
├── SYSTEM_PROMPT_QUICK_REFERENCE.md                     # Quick reference
├── INSTALLATION_COMPLETE_SUMMARY.md                     # This file
├── scripts/
│   └── install_system_prompts.sh (4.1KB, executable)   # Automated installer
└── docs/guides/setup/
    └── EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md          # Full guide

~/.gemini/
└── system_empirica.md (14KB)                            # Gemini CLI prompt
```

---

## Summary

✅ **Gemini CLI:** File installed, needs environment variable activation
✅ **Claude Code:** File installed, auto-loads in project directory
✅ **Installer:** Automated script ready for future users
✅ **Documentation:** Comprehensive guides and quick reference

**Total installation time:** ~2 minutes
**Value:** Systematic epistemic tracking for every task

---

**Ready to test?**

```bash
# Activate Gemini
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
gemini

# Or use Claude
cd /path/to/empirica
claude
```

Both agents will now use the Empirica CASCADE workflow automatically! 🚀
