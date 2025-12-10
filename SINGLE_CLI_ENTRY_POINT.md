# Single Empirica CLI Entry Point

**Date:** 2025-12-10
**Status:** ✅ Complete
**Objective:** One and only one empirica command (no confusion)

---

## What Was Done

### 1. Removed Empirica from Tmux Venv
```bash
/home/yogapad/.venv/tmux/bin/python -m pip uninstall -y empirica
# Successfully uninstalled empirica-1.0.0b0
```

### 2. Kept Only .venv-mcp
```bash
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m pip list | grep empirica
# empirica  1.0.0b0  /home/yogapad/empirical-ai/empirica
```

### 3. Verified No PATH Collision
```bash
which -a empirica
# Exit code 1 (not found) ✅
```

### 4. Confirmed .venv-mcp Works
```bash
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli --help
# ✅ CLI responds with all commands
```

---

## Result

| Location | Status |
|----------|--------|
| tmux venv | ❌ REMOVED (no confusion) |
| .venv-mcp | ✅ ONLY VERSION (source of truth) |
| PATH | ✅ CLEAN (no stray commands) |

---

## How to Use

### For Everyone (Claude Code, GPT-5, Humans)
Use the full path form (bulletproof, no PATH issues):

```bash
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli <COMMAND>
```

### Examples
```bash
# Session management
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli session-create --ai-id gpt-5

# Epistemic assessment
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli preflight "task" --prompt-only

# Investigation branching
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli investigate-create-branch --session-id <sid> --description "Option A" --round 1
```

---

## Benefits

✅ **No confusion:** Only one empirica command exists
✅ **No PATH issues:** Full path bypasses any ambiguity
✅ **No version conflicts:** Only .venv-mcp has empirica installed
✅ **Easy to update:** Changes to local code immediately take effect (editable mode)
✅ **Self-service:** Everyone can run CLI commands independently

---

## Verification

```bash
# Confirm only one instance
ls /home/yogapad/empirical-ai/empirica/.venv-mcp/bin/empirica
# /home/yogapad/empirical-ai/empirica/.venv-mcp/bin/empirica ✅

# Confirm it works
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli --help | head -5
# usage: empirica [-h] [--verbose] [--config CONFIG] ... ✅

# Confirm module location
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -c "import empirica; print(empirica.__file__)"
# /home/yogapad/empirical-ai/empirica/empirica/__init__.py ✅
```

---

## Recommendation

Create a shell alias in your `~/.bashrc` or `~/.zshrc` if you use the command often (optional):

```bash
alias empirica='/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli'

# Then you can use:
empirica session-create --ai-id gpt-5
```

But the full path form is always safe and recommended for scripts/automation.

---

**Status:** One command, zero confusion. Ready for production.
