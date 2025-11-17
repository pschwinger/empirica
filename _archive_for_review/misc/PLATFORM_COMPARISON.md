# Empirica System Prompt: Platform Comparison

**Date:** 2025-11-15

---

## Installation Methods Comparison

| Platform | Method | Location | Effect | Scope |
|----------|--------|----------|--------|-------|
| **Gemini CLI** | `GEMINI_SYSTEM_MD` environment variable | `~/.gemini/system_empirica.md` | **Replaces** entire system prompt | Global (all sessions) |
| **Claude Code** | `CLAUDE.md` project file | Project root directory | **Supplements** default prompt | Project-specific |

---

## Detailed Feature Comparison

### Gemini CLI

| Feature | Details |
|---------|---------|
| **Installation Method** | Environment variable `GEMINI_SYSTEM_MD` |
| **File Location** | `~/.gemini/system_empirica.md` |
| **Effect on System Prompt** | Complete replacement of default |
| **Configuration Scope** | Per-user (global across all sessions) |
| **Auto-load** | Yes (when environment variable is set) |
| **Activation** | Add to `~/.bashrc` or `~/.zshrc` |
| **Customization** | Single file, applies to all Gemini sessions |
| **Override** | Can be overridden with different env var value |
| **Testing** | Can test without permanent install using inline env var |
| **Best For** | Users who want Empirica for ALL Gemini work |

**Setup Command:**
```bash
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
```

**One-time Test:**
```bash
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini
```

---

### Claude Code

| Feature | Details |
|---------|---------|
| **Installation Method** | Project-level `CLAUDE.md` file |
| **File Location** | `CLAUDE.md` in project root |
| **Effect on System Prompt** | Supplements (adds to) default instructions |
| **Configuration Scope** | Per-project |
| **Auto-load** | Yes (when in project directory) |
| **Activation** | Automatic when Claude starts in project dir |
| **Customization** | Different `CLAUDE.md` per project |
| **Override** | Can have project-specific versions |
| **Testing** | Place file in test project directory |
| **Best For** | Users who want Empirica for SPECIFIC projects |

**Setup Command:**
```bash
cp GENERIC_EMPIRICA_SYSTEM_PROMPT.md /path/to/project/CLAUDE.md
```

**SDK Configuration (if needed):**
```python
# Python
agent = Agent(setting_sources=["project"])
```

---

## Behavior Differences

### Gemini CLI: Complete Replacement

**What happens:**
- Gemini's default system prompt is **completely replaced**
- Only Empirica instructions are active
- No Gemini default behaviors remain

**Advantages:**
- ✅ Clean slate - no conflicting instructions
- ✅ Consistent behavior across all sessions
- ✅ Empirica framework is the only framework

**Considerations:**
- ⚠️ Loses any Gemini-specific default behaviors
- ⚠️ Applies to ALL Gemini sessions (not selective)

---

### Claude Code: Supplemental Addition

**What happens:**
- Claude's default system prompt **remains active**
- Empirica instructions are **added on top**
- Both Claude Code tools and Empirica framework available

**Advantages:**
- ✅ Keeps Claude Code's built-in tool usage
- ✅ Per-project customization
- ✅ Can mix Empirica with other project instructions

**Considerations:**
- ⚠️ Potential for instruction conflicts (if contradictory)
- ⚠️ Claude must balance both instruction sets
- ⚠️ Empirica is supplemental, not primary

---

## Use Case Recommendations

### Use Gemini CLI When:

✅ You want **all** your Gemini sessions to use Empirica
✅ You prefer **complete control** over the system prompt
✅ You work on **diverse technical tasks** needing systematic tracking
✅ You want **consistent epistemic tracking** across all work
✅ You're comfortable with **environment variable** management

**Example users:**
- AI researchers tracking learning across experiments
- Security analysts needing systematic investigation
- DevOps engineers managing complex systems
- Technical leads coordinating multiple projects

---

### Use Claude Code When:

✅ You want Empirica for **specific projects** only
✅ You prefer **project-specific** customization
✅ You want to **preserve** Claude Code's default behaviors
✅ You work in **teams** where different projects have different needs
✅ You're comfortable with **per-project** configuration files

**Example users:**
- Development teams with varying project methodologies
- Consultants working on client-specific projects
- Researchers with different epistemic requirements per study
- Organizations with project-specific compliance needs

---

## Multi-Project Scenarios

### Scenario 1: Multiple Projects, All Use Empirica

**Gemini CLI Approach:**
```bash
# One environment variable, applies everywhere
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md
```

**Claude Code Approach:**
```bash
# CLAUDE.md in each project
/project-A/CLAUDE.md
/project-B/CLAUDE.md
/project-C/CLAUDE.md
```

**Winner:** Gemini CLI (simpler for universal use)

---

### Scenario 2: Some Projects Use Empirica, Others Don't

**Gemini CLI Approach:**
```bash
# Requires manually unsetting/changing env var
unset GEMINI_SYSTEM_MD  # For non-Empirica work
export GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md  # For Empirica work
```

**Claude Code Approach:**
```bash
# Just add CLAUDE.md to Empirica projects
/empirica-project/CLAUDE.md  # Uses Empirica
/standard-project/           # No CLAUDE.md, uses defaults
```

**Winner:** Claude Code (automatic per-project selection)

---

### Scenario 3: Different Empirica Customizations Per Project

**Gemini CLI Approach:**
```bash
# Requires multiple prompt files and env var switching
export GEMINI_SYSTEM_MD=~/.gemini/system_security.md  # Security project
export GEMINI_SYSTEM_MD=~/.gemini/system_research.md  # Research project
```

**Claude Code Approach:**
```bash
# Different CLAUDE.md per project
/security-project/CLAUDE.md     # Security-focused Empirica
/research-project/CLAUDE.md     # Research-focused Empirica
```

**Winner:** Claude Code (automatic context switching)

---

## Technical Comparison

### Prompt Precedence

| Platform | Precedence Order |
|----------|------------------|
| **Gemini CLI** | `GEMINI_SYSTEM_MD` > default system prompt |
| **Claude Code** | Built-in tools + `CLAUDE.md` (merged) |

### File Size Impact

| Platform | File Size | Impact on Context |
|----------|-----------|-------------------|
| **Gemini CLI** | 14KB | Replaces default (neutral) |
| **Claude Code** | 14KB | Adds to default (+14KB) |

### Update Process

| Platform | Update Method |
|----------|---------------|
| **Gemini CLI** | Edit `~/.gemini/system_empirica.md` → restart Gemini |
| **Claude Code** | Edit `CLAUDE.md` → restart Claude (per project) |

---

## Installation Comparison

### Setup Time

| Platform | Initial Setup | Per-Project Setup |
|----------|---------------|-------------------|
| **Gemini CLI** | 2 minutes (one-time) | 0 minutes (automatic) |
| **Claude Code** | 1 minute (first project) | 30 seconds (copy file) |

### Automated Installation

Both platforms supported by `scripts/install_system_prompts.sh`:

```bash
cd /path/to/empirica
bash scripts/install_system_prompts.sh
```

**What it installs:**
- Gemini CLI: `~/.gemini/system_empirica.md` + env var setup
- Claude Code: `CLAUDE.md` in Empirica project root

---

## Testing Comparison

### Gemini CLI Testing

**Without permanent install:**
```bash
GEMINI_SYSTEM_MD=~/.gemini/system_empirica.md gemini
```

**With permanent install:**
```bash
gemini  # Uses Empirica automatically
```

### Claude Code Testing

**Test project:**
```bash
cd /test/project
cp /empirica/GENERIC_EMPIRICA_SYSTEM_PROMPT.md ./CLAUDE.md
claude  # Uses Empirica in this project
```

**Production project:**
```bash
cd /production/project
# No CLAUDE.md → uses default Claude behavior
claude
```

---

## Customization Examples

### Gemini CLI: Security-Focused Empirica

```bash
# Create custom security prompt
cp ~/.gemini/system_empirica.md ~/.gemini/system_security.md
nano ~/.gemini/system_security.md
# Add: Security audit phases, threat modeling, etc.

# Use for security work
export GEMINI_SYSTEM_MD=~/.gemini/system_security.md
```

### Claude Code: Research vs Production

```bash
# Research project (thorough investigation)
/research/project/CLAUDE.md
# Contents: Full CASCADE, extended INVESTIGATE phase

# Production project (faster iteration)
/production/project/CLAUDE.md
# Contents: Simplified CASCADE, focus on ACT phase
```

---

## Troubleshooting Comparison

### Gemini CLI Issues

| Issue | Check | Fix |
|-------|-------|-----|
| Not using Empirica | `echo $GEMINI_SYSTEM_MD` | `export GEMINI_SYSTEM_MD=...` |
| File not found | `ls ~/.gemini/system_empirica.md` | Re-run installer |
| Wrong prompt | `cat $GEMINI_SYSTEM_MD \| head` | Verify file contents |

### Claude Code Issues

| Issue | Check | Fix |
|-------|-------|-----|
| Not using Empirica | `ls CLAUDE.md` | Copy file to project root |
| Wrong directory | `pwd` | `cd /path/to/project` |
| SDK not loading | Check `settingSources` | Add `"project"` to config |

---

## Platform-Specific Features

### Gemini CLI Only

- ✅ Complete system prompt replacement
- ✅ Single configuration for all sessions
- ✅ Environment variable control
- ✅ Easy global enable/disable

### Claude Code Only

- ✅ Per-project customization
- ✅ Preserves built-in tool usage
- ✅ Version control friendly (project-specific)
- ✅ Automatic context switching

---

## Recommendation Matrix

| User Type | Recommended Platform | Reason |
|-----------|---------------------|--------|
| **AI Researcher** | Gemini CLI | Consistent epistemic tracking across all experiments |
| **Security Analyst** | Gemini CLI | Systematic investigation for all security work |
| **Development Team** | Claude Code | Per-project flexibility |
| **Consultant** | Claude Code | Client-specific customization |
| **Solo Developer** | Either | Personal preference |
| **DevOps Engineer** | Gemini CLI | Consistent tracking across diverse systems |
| **Technical Lead** | Both | Gemini for personal, Claude for team projects |

---

## Summary

### Gemini CLI

**Best for:** Universal Empirica usage across all work
**Key feature:** Complete system prompt replacement
**Setup:** One-time environment variable
**Use case:** Consistent epistemic tracking everywhere

### Claude Code

**Best for:** Project-specific Empirica usage
**Key feature:** Per-project customization
**Setup:** Copy `CLAUDE.md` to project root
**Use case:** Flexible, context-aware epistemic tracking

---

**Both platforms fully supported by Empirica's automated installer:**

```bash
cd /path/to/empirica
bash scripts/install_system_prompts.sh
```

**Choose based on your workflow needs!** 🚀
