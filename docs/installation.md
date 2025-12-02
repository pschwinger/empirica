# Empirica System Prompt Installation - All Platforms

**Date:** 2025-11-15
**Version:** 2.0
**Platforms:** Gemini CLI, Claude Code, GitHub Copilot CLI, Qwen Code, Atlassian Rovo Dev

---

## Quick Install (All Platforms)

```bash
cd /path/to/empirica
bash scripts/install_system_prompts_all.sh
```

This will install Empirica system prompts for all 5 supported AI CLI platforms.

---

## Platform Overview

| Platform | Method | Location | Effect | Auto-load |
|----------|--------|----------|--------|-----------|
| **Gemini CLI** | Environment variable | `~/.gemini/system_empirica.md` | Replaces system prompt | Yes (if env var set) |
| **Claude Code** | Project file | `CLAUDE.md` | Supplements system prompt | Yes (in project dir) |
| **GitHub Copilot** | Repository instructions | `.github/copilot-instructions.md` | Supplements system prompt | Yes (in repository) |
| **Qwen Code** | Context file | `QWEN.md` | Hierarchical context | Yes (auto-discovered) |
| **Rovo Dev** | Config file | `~/.rovodev/config_empirica.yml` | Additional system prompt | Manual (via --config-file) |

---

## 1. Gemini CLI

### Installation Method: Environment Variable

**What it does:** Completely replaces Gemini's default system prompt with Empirica

### Setup

```bash
# File already created at ~/.gemini/system_empirica.md

# Add to shell config
echo 'export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md' >> ~/.bashrc
source ~/.bashrc
```

### Usage

```bash
# Uses Empirica automatically
gemini

# Or one-time test
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini
```

### Verification

```bash
gemini
> "What framework are you using?"
# Expected: Should mention Empirica, CASCADE workflow, epistemic vectors
```

---

## 2. Claude Code

### Installation Method: Project File

**What it does:** Supplements Claude's default prompt with Empirica instructions

### Setup

```bash
# File already created at /path/to/empirica/CLAUDE.md

# No additional setup needed - auto-loads in project directory
```

### Usage

```bash
cd /path/to/empirica
claude
# CLAUDE.md automatically loaded
```

### Verification

```bash
cd /path/to/empirica
claude
> "What are the phases of your workflow?"
# Expected: BOOTSTRAP → PRE assessment → [implicit work] → CHECK(s) → POST assessment
```

---

## 3. GitHub Copilot CLI

### Installation Method: Repository Instructions

**What it does:** Provides repository-wide custom instructions for all Copilot requests

### Setup

```bash
# File already created at .github/copilot-instructions.md

# No additional setup needed - active immediately upon saving
```

### Usage

```bash
cd /path/to/empirica
gh copilot
# Instructions automatically included in prompts
```

### Path-Specific Instructions (Advanced)

Create `.github/instructions/NAME.instructions.md` with frontmatter:

```yaml
---
applyTo: "**/*.py"
---
[Python-specific Empirica instructions]
```

### Verification

```bash
cd /path/to/empirica
gh copilot
> "What framework are you using?"
# Expected: Should mention Empirica, CASCADE workflow
```

---

## 4. Qwen Code

### Installation Method: Context Files (QWEN.md)

**What it does:** Provides hierarchical context loaded from QWEN.md files

### Setup

```bash
# File already created at /path/to/empirica/QWEN.md

# Optional: Install global context
mkdir -p ~/.qwen
cp QWEN.md ~/.qwen/QWEN.md
```

### Hierarchical Loading

Qwen loads context files in this order:

1. **Global:** `~/.qwen/QWEN.md`
2. **Project root:** `/path/to/empirica/QWEN.md`
3. **Subdirectories:** `.qwen/QWEN.md` (up to 200 directories)

All files are concatenated into the system prompt.

### Usage

```bash
cd /path/to/empirica
qwen

# View loaded context
> /memory show

# Refresh context files
> /memory refresh
```

### Configuration (Optional)

Edit `~/.qwen/settings.json` or `./.qwen/settings.json`:

```json
{
  "context": {
    "fileName": "QWEN.md",
    "enableMultiDirectoryMemory": true
  }
}
```

### Verification

```bash
cd /path/to/empirica
qwen
> /memory show
# Expected: Should show Empirica CASCADE workflow in context
```

---

## 5. Atlassian Rovo Dev

### Installation Method: Configuration File

**What it does:** Adds custom system prompt via `additionalSystemPrompt` in config

### Setup

```bash
# File already created at ~/.rovodev/config_empirica.yml

# Edit default config to use Empirica
acli rovodev config
# Or use custom config file directly
```

### Usage

```bash
# Use custom Empirica config
acli rovodev run --config-file ~/.rovodev/config_empirica.yml
```

### Configuration Details

The `config_empirica.yml` includes:

```yaml
agent:
  additionalSystemPrompt: |
    [Empirica CASCADE workflow instructions...]
  streaming: true
  temperature: 0.3
  modelId: "auto"
  enableDeepPlanTool: true
```

### Verification

```bash
acli rovodev run --config-file ~/.rovodev/config_empirica.yml
> "What workflow do you follow?"
# Expected: Should mention Empirica CASCADE workflow
```

---

## Platform Comparison

### Complete Replacement vs Supplemental

| Platform | Type | Notes |
|----------|------|-------|
| **Gemini CLI** | Complete Replacement | Only Empirica instructions active |
| **Claude Code** | Supplemental | Empirica + Claude Code defaults |
| **GitHub Copilot** | Supplemental | Empirica + Copilot defaults |
| **Qwen Code** | Hierarchical Context | Multiple QWEN.md files concatenated |
| **Rovo Dev** | Supplemental | Empirica appended to default prompt |

### Activation Method

| Platform | Activation | Ease of Use |
|----------|------------|-------------|
| **Gemini CLI** | Environment variable | One-time setup |
| **Claude Code** | Project file | Automatic |
| **GitHub Copilot** | Repository file | Automatic |
| **Qwen Code** | Context discovery | Automatic |
| **Rovo Dev** | Config flag | Manual per-run |

### Best Use Cases

| Platform | Best For |
|----------|----------|
| **Gemini CLI** | Universal Empirica usage (all work) |
| **Claude Code** | Project-specific Empirica |
| **GitHub Copilot** | Repository-wide team standards |
| **Qwen Code** | Hierarchical context (global + project + local) |
| **Rovo Dev** | Atlassian-integrated workflows |

---

## What AI Agents Get

### CASCADE Workflow (All Platforms)

```
1. BOOTSTRAP → Initialize Empirica session
2. PREFLIGHT → Assess starting state (13 epistemic vectors)
3. GENERATE GOALS → Systematic investigation planning
4. INVESTIGATE → Multi-turn exploration with belief tracking
5. CHECK → Readiness validation (confidence >= 0.7 to proceed)
6. ACT → Execute the work
7. POSTFLIGHT → Measure learning deltas
8. CALIBRATION REPORT → Confidence accuracy
```

### 13 Epistemic Vectors

| Tier | Vectors |
|------|---------|
| **Foundation** | engagement, know, do, context |
| **Comprehension** | clarity, coherence, signal, density |
| **Execution** | state, change, completion, impact |
| **Meta** | uncertainty |

### Key Behaviors

**All platforms encourage:**
- ✅ Honest uncertainty assessment
- ✅ Systematic investigation
- ✅ Belief tracking as learning progresses
- ✅ Learning measurement (PREFLIGHT vs POSTFLIGHT)
- ✅ Calibration awareness

---

## Verification Tests (All Platforms)

### Test 1: Framework Recognition

**Ask:** "What framework are you using?"

**Expected:** Should mention Empirica, CASCADE workflow, epistemic tracking

**Test on:**
- Gemini CLI
- Claude Code
- GitHub Copilot CLI
- Qwen Code (via `/memory show`)
- Rovo Dev

---

### Test 2: Workflow Understanding

**Ask:** "What are the phases of your workflow?"

**Expected:** Should list PRE assessment → implicit CASCADE workflow → CHECK assessments → POST assessment

**Test on:** All platforms

---

### Test 3: Epistemic Vectors

**Ask:** "What epistemic vectors do you track?"

**Expected:** Should list 13 vectors (engagement, know, do, context, clarity, coherence, signal, density, state, change, completion, impact, uncertainty)

**Test on:** All platforms

---

### Test 4: MCP Tools Awareness (Empirica-specific)

**Ask:** "What MCP tools do you have access to?"

**Expected:** Should mention execute_preflight, submit_preflight_assessment, query_goal_orchestrator, etc.

**Test on:** Platforms with Empirica MCP server access (Gemini, Claude, Qwen)

---

## File Locations Summary

```
# Gemini CLI
~/.gemini/system_empirica.md (14KB)

# Claude Code
/path/to/empirica/CLAUDE.md (14KB)

# GitHub Copilot CLI
/path/to/empirica/.github/copilot-instructions.md (5KB)

# Qwen Code
/path/to/empirica/QWEN.md (8KB)
~/.qwen/QWEN.md (optional, 8KB)

# Rovo Dev
~/.rovodev/config_empirica.yml (3KB)
```

---

## Advanced Customization

### Per-Project Customization

Each platform supports project-specific customization:

**Gemini CLI:**
```bash
# Use different prompt per project
export GEMINI_SYSTEM_MD=/path/to/project/custom_prompt.md
```

**Claude Code:**
```bash
# Different CLAUDE.md per project
/project-A/CLAUDE.md  # Security-focused Empirica
/project-B/CLAUDE.md  # Research-focused Empirica
```

**GitHub Copilot:**
```bash
# Path-specific instructions
.github/instructions/backend.instructions.md  # Backend standards
.github/instructions/frontend.instructions.md  # Frontend standards
```

**Qwen Code:**
```bash
# Hierarchical context
~/.qwen/QWEN.md              # Global standards
/project/.qwen/QWEN.md       # Project standards
/project/module/.qwen/QWEN.md  # Module standards
```

**Rovo Dev:**
```bash
# Multiple config files
~/.rovodev/config_security.yml   # Security workflows
~/.rovodev/config_research.yml   # Research workflows
```

---

## Troubleshooting

### Gemini CLI not using Empirica

**Check:**
```bash
echo $GEMINI_SYSTEM_MD
# Should print: ~/.gemini/system_empirica.md
```

**Fix:**
```bash
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
```

---

### Claude Code not using Empirica

**Check:**
```bash
ls -lh /path/to/empirica/CLAUDE.md
pwd  # Should be in empirica directory
```

**Fix:** Start Claude in the correct directory

---

### GitHub Copilot not using instructions

**Check:**
```bash
ls -lh .github/copilot-instructions.md
git rev-parse --is-inside-work-tree  # Must be in git repo
```

**Fix:** Ensure file exists and you're in repository root

---

### Qwen Code not loading context

**Check:**
```bash
# In Qwen session
> /memory show
```

**Fix:**
```bash
# Refresh context
> /memory refresh
```

---

### Rovo Dev not using Empirica config

**Check:**
```bash
ls -lh ~/.rovodev/config_empirica.yml
```

**Fix:** Use correct flag:
```bash
acli rovodev run --config-file ~/.rovodev/config_empirica.yml
```

---

## Next Steps

### 1. Install (if not done)

```bash
cd /path/to/empirica
bash scripts/install_system_prompts_all.sh
```

### 2. Activate

- **Gemini:** Add environment variable to shell config
- **Claude:** No action needed (auto-loads)
- **Copilot:** No action needed (auto-loads)
- **Qwen:** No action needed (auto-discovers)
- **Rovo:** Use `--config-file` flag

### 3. Verify

Test each platform with the verification questions above.

### 4. Read Documentation

- **Installation Guide:** `docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md`
- **Platform Comparison:** `PLATFORM_COMPARISON.md`
- **Quick Reference:** `SYSTEM_PROMPT_QUICK_REFERENCE.md`
- **AI Quick Start:** `docs/01_a_AI_AGENT_START.md`

---

## Benefits of Multi-Platform Support

### For Individual Users

✅ Use Empirica across different AI tools
✅ Consistent methodology regardless of platform
✅ Choose best tool for each task while maintaining systematic approach

### For Teams

✅ Standardize epistemic tracking across team members
✅ Support different tool preferences while maintaining consistency
✅ Repository-wide standards (GitHub Copilot) + personal config (Gemini/Claude/Qwen)

### For Organizations

✅ Empirica becomes platform-agnostic
✅ AI tool decisions independent of methodology
✅ Systematic knowledge tracking across all AI-assisted work

---

## Summary

| Platform | Install Time | Complexity | Auto-load | Best For |
|----------|--------------|------------|-----------|----------|
| **Gemini CLI** | 2 min | Low | Yes | Universal usage |
| **Claude Code** | 1 min | Very Low | Yes | Project-specific |
| **GitHub Copilot** | 1 min | Very Low | Yes | Repository-wide |
| **Qwen Code** | 1 min | Low | Yes | Hierarchical context |
| **Rovo Dev** | 2 min | Medium | Manual | Atlassian workflows |

**All platforms installed?** You now have **universal Empirica support** across the AI CLI ecosystem! 🚀

---

**Install now:**

```bash
cd /path/to/empirica
bash scripts/install_system_prompts_all.sh
```

**Questions?** Read the detailed docs in `docs/guides/setup/`
