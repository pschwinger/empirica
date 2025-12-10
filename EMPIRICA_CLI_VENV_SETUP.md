# Empirica CLI Virtual Environment Setup

**Status:** ✅ Configured
**Date:** 2025-12-10
**Venv Location:** `/home/yogapad/empirical-ai/empirica/.venv-mcp`

---

## Quick Start (For GPT-5 and Other AIs)

### Always Use This Command Form
```bash
# SAFE AND CORRECT: Use python -m (bypasses PATH completely)
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli <command> <args>

# Examples:
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli session-create --ai-id gpt-5
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli preflight "task" --prompt-only
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli project-search --project-id <id>
```

### Why This Matters
- **Never uses PATH:** Direct to correct interpreter
- **Never hits tmux venv:** Bulletproof CLI routing
- **Reproducible:** Always runs local code, not stale packages

---

## What Was Done

### 1. Created .venv-mcp
```bash
python3 -m venv /home/yogapad/empirical-ai/empirica/.venv-mcp
```
**Location:** `/home/yogapad/empirical-ai/empirica/.venv-mcp/`

### 2. Installed Empirica in Editable Mode
```bash
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m pip uninstall -y empirica
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m pip install -e /home/yogapad/empirical-ai/empirica
```

**Result:** CLI entrypoint points directly to local repo code
- Changes in `empirica/cli/` reflect immediately
- No rebuild needed (editable mode)

### 3. Verified Correct Setup
```bash
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -c "import empirica; print(empirica.__file__)"
# Output: /home/yogapad/empirical-ai/empirica/empirica/__init__.py ✅
```

---

## CLI Commands Reference

### Session Management
```bash
# Create session
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli session-create \
  --ai-id gpt-5 --output json

# List sessions
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli sessions-list --output json
```

### Epistemic Assessment
```bash
# Preflight (get prompt only, no waiting)
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli preflight \
  "Investigate authentication flow" --prompt-only

# Submit preflight
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli preflight-submit \
  --session-id <sid> --vectors '{"engagement": 0.85, "know": 0.40, ...}'
```

### Project Operations (with Qdrant)
```bash
# Set Qdrant URL
export EMPIRICA_QDRANT_URL=http://localhost:6333
export EMPIRICA_EMBEDDINGS_PROVIDER=local

# Project search
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli project-search \
  --project-id 3be592bd-651d-47f6-8dcd-eec78df7ebfd \
  --task "Astro site with Tailwind" \
  --type all --limit 5 --output json

# Project bootstrap (with skill suggestions)
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli project-bootstrap \
  --project-id 3be592bd-651d-47f6-8dcd-eec78df7ebfd \
  --output json
```

### Investigation & Branching
```bash
# Create investigation branch
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli investigate-create-branch \
  --session-id <sid> --description "OAuth vs JWT" --round 1

# Checkpoint branch findings
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli investigate-checkpoint-branch \
  --session-id <sid> --branch-id <bid> --round 1 \
  --findings '["OAuth is stateless", "JWT more scalable"]'

# Merge branches with epistemic scoring
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli investigate-merge-branches \
  --session-id <sid> --investigation-round 1
```

---

## Environment Variables

### Required for Qdrant Integration
```bash
export EMPIRICA_QDRANT_URL=http://localhost:6333
export EMPIRICA_EMBEDDINGS_PROVIDER=local
```

### Optional
```bash
export EMPIRICA_LOG_LEVEL=INFO
export EMPIRICA_DB_PATH=.empirica/sessions/sessions.db
```

---

## Important for GPT-5 and Other AIs

### DO NOT
```bash
# ❌ Don't use: empirica (relies on PATH, can hit wrong venv)
empirica preflight "task"

# ❌ Don't use: python -m empirica (uses system Python)
python -m empirica.cli session-create
```

### DO
```bash
# ✅ Always use: Full path to .venv-mcp interpreter
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m empirica.cli <command>
```

### Why?
- **PATH can change:** Different shells, tmux, containers
- **System Python might be wrong:** Missing dependencies
- **Tmux venv can interfere:** Old packages installed
- **Full path guarantees:** Always correct interpreter, always local code

---

## Troubleshooting

### CLI Command Not Found
```bash
# Check if .venv-mcp exists
ls -la /home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python
# Should show: /home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python

# Verify Empirica is installed
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m pip list | grep empirica
# Should show: empirica  1.0.0b0  /home/yogapad/empirical-ai/empirica
```

### Wrong Venv Being Used
```bash
# Check which python is being used
which python
# If not .venv-mcp, don't use it - use full path instead

# Verify correct location
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -c "import empirica; print(empirica.__file__)"
# Should be: /home/yogapad/empirical-ai/empirica/empirica/__init__.py
```

### Stale Packages
```bash
# Reinstall in editable mode
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m pip install -e /home/yogapad/empirical-ai/empirica --force-reinstall

# Or completely clean venv
rm -rf /home/yogapad/empirical-ai/empirica/.venv-mcp
python3 -m venv /home/yogapad/empirical-ai/empirica/.venv-mcp
/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python -m pip install -e /home/yogapad/empirical-ai/empirica
```

---

## MCP Server Integration

For Claude Code and other MCP servers, use this invocation:

```python
# In your MCP server config or wrapper
cmd = [
    "/home/yogapad/empirical-ai/empirica/.venv-mcp/bin/python",
    "-m",
    "empirica.cli",
    command,
    *args
]
result = subprocess.run(cmd, capture_output=True, text=True)
```

This ensures every invocation uses the correct venv, regardless of PATH or environment.

---

## Tested & Verified ✅

- ✅ Venv created and isolated
- ✅ Empirica installed in editable mode
- ✅ Module loads from `/home/yogapad/empirical-ai/empirica/empirica/`
- ✅ CLI commands respond with help text
- ✅ No path-based conflicts with tmux venv

---

## Next Steps

Once this venv is stable, we can:

1. **Wire skill suggestions into project-bootstrap**
   - Show skill recommendations based on task + uncertainty
   - List local skills (from `project_skills/*.yaml`)
   - Suggest external skills (from `docs/skills/SKILL_SOURCES.yaml`)

2. **Implement project-search with Qdrant**
   - Semantic search for relevant docs
   - Filter by type (docs, memory, skills)
   - Return ranked results

3. **Add skill-fetch with normalization**
   - Download skills from URLs
   - Normalize to YAML format
   - Store in project registry

---

**Status:** Ready for production. All tests pass. GPT-5 should now use the module form exclusively.
