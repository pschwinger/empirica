# Empirica - All Platforms Quick Reference

**Install all platforms in 30 seconds:**

```bash
cd /path/to/empirica
bash scripts/install_system_prompts_all.sh
```

---

## Platform Quick Reference

| Platform | File | Activation | Test Command |
|----------|------|------------|--------------|
| **Gemini CLI** | `~/.gemini/system_empirica.md` | `export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md` | `gemini` |
| **Claude Code** | `CLAUDE.md` | Auto-loads | `cd <project> && claude` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Auto-loads | `gh copilot` |
| **Qwen Code** | `QWEN.md` | Auto-discovers | `qwen` then `/memory show` |
| **Rovo Dev** | `~/.rovodev/config_empirica.yml` | `--config-file` flag | `acli rovodev run --config-file ~/.rovodev/config_empirica.yml` |

---

## One-Line Setup Per Platform

### Gemini CLI
```bash
echo 'export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md' >> ~/.bashrc && source ~/.bashrc
```

### Claude Code
```bash
# Already installed at CLAUDE.md - just use in project directory
cd /path/to/empirica && claude
```

### GitHub Copilot
```bash
# Already installed at .github/copilot-instructions.md - active immediately
gh copilot
```

### Qwen Code
```bash
# Already installed at QWEN.md - use /memory show to verify
qwen
> /memory show
```

### Rovo Dev
```bash
# Use with --config-file flag
acli rovodev run --config-file ~/.rovodev/config_empirica.yml
```

---

## Verification One-Liners

```bash
# Gemini
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini
# Ask: "What framework are you using?"

# Claude
cd /path/to/empirica && claude
# Ask: "What are the phases of your workflow?"

# Copilot
cd /path/to/empirica && gh copilot
# Ask: "What framework are you using?"

# Qwen
cd /path/to/empirica && qwen
# Use: /memory show

# Rovo
acli rovodev run --config-file ~/.rovodev/config_empirica.yml
# Ask: "What workflow do you follow?"
```

---

## What You Get (All Platforms)

**CASCADE Workflow:**
```
BOOTSTRAP → PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT → CALIBRATION
```

**13 Epistemic Vectors:**
```
engagement, know, do, context, clarity, coherence, signal, density,
state, change, completion, impact, uncertainty
```

**Key Behaviors:**
- ✅ Honest uncertainty assessment
- ✅ Systematic investigation
- ✅ Belief tracking
- ✅ Learning measurement
- ✅ Calibration awareness

---

## Platform Comparison

| Feature | Gemini | Claude | Copilot | Qwen | Rovo |
|---------|--------|--------|---------|------|------|
| **Method** | Env var | Project file | Repo file | Context file | Config file |
| **Effect** | Replace | Supplement | Supplement | Hierarchical | Supplement |
| **Auto-load** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Scope** | Global | Project | Repository | Hierarchical | Per-run |

---

## Common Commands

### Gemini CLI
```bash
# Permanent
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md

# One-time
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini
```

### Claude Code
```bash
# Just navigate to project
cd /path/to/empirica
claude
```

### GitHub Copilot
```bash
# Works in any repository with .github/copilot-instructions.md
cd /path/to/empirica
gh copilot
```

### Qwen Code
```bash
# View context
qwen
> /memory show

# Refresh context
> /memory refresh
```

### Rovo Dev
```bash
# Use custom config
acli rovodev run --config-file ~/.rovodev/config_empirica.yml

# Edit config
acli rovodev config
```

---

## File Locations

```
~/.gemini/system_empirica.md              # Gemini CLI
/project/CLAUDE.md                        # Claude Code
/project/.github/copilot-instructions.md  # GitHub Copilot
/project/QWEN.md                          # Qwen Code (project)
~/.qwen/QWEN.md                           # Qwen Code (global)
~/.rovodev/config_empirica.yml            # Rovo Dev
```

---

## Troubleshooting

### Platform Not Using Empirica?

**Gemini:**
```bash
echo $GEMINI_SYSTEM_MD  # Should show path
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
```

**Claude:**
```bash
pwd  # Should be in project directory
ls CLAUDE.md  # Should exist
```

**Copilot:**
```bash
ls .github/copilot-instructions.md  # Should exist
git status  # Must be in git repo
```

**Qwen:**
```bash
qwen
> /memory show  # Should show Empirica context
> /memory refresh  # If not showing
```

**Rovo:**
```bash
ls ~/.rovodev/config_empirica.yml  # Should exist
# Use --config-file flag
```

---

## Advanced Usage

### Per-Project Customization

**Gemini:**
```bash
export GEMINI_SYSTEM_MD=/path/to/custom.md
```

**Claude:**
```bash
# Different CLAUDE.md per project
/projectA/CLAUDE.md
/projectB/CLAUDE.md
```

**Copilot:**
```bash
# Path-specific instructions
.github/instructions/backend.instructions.md
.github/instructions/frontend.instructions.md
```

**Qwen:**
```bash
# Hierarchical
~/.qwen/QWEN.md          # Global
/project/QWEN.md         # Project
/project/module/QWEN.md  # Module
```

**Rovo:**
```bash
# Multiple configs
~/.rovodev/config_security.yml
~/.rovodev/config_research.yml
```

---

## Documentation

- **Full Installation Guide:** `docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md`
- **All Platforms Guide:** `ALL_PLATFORMS_INSTALLATION.md`
- **Platform Comparison:** `PLATFORM_COMPARISON.md`
- **AI Quick Start:** `docs/01_a_AI_AGENT_START.md`

---

## Summary

✅ **5 platforms supported:** Gemini CLI, Claude Code, GitHub Copilot, Qwen Code, Rovo Dev
✅ **Universal CASCADE workflow:** All platforms follow same methodology
✅ **30-second install:** One script installs all platforms
✅ **Platform flexibility:** Choose best tool for each task

---

**Install now:**

```bash
cd /path/to/empirica
bash scripts/install_system_prompts_all.sh
```

**Test verification:**

```bash
# Each platform - ask: "What framework are you using?"
# Expected: Empirica, CASCADE workflow, epistemic vectors
```

🚀 **Universal Empirica across the AI CLI ecosystem!**
