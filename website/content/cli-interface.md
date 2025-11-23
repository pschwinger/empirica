# CLI Interface

**The Heart of Empirica: Direct Epistemic Assessment**

[← Back to Home](index.md) | [MCP Server](mcp-integration.md) | [Skills](skills.md) | [System Prompts](system-prompts.md)

---

## Overview

The Empirica CLI is the core interface for metacognitive AI operations. It provides direct, transparent access to the epistemic assessment engine, allowing you to run cascades, investigate uncertainty, and monitor AI reasoning in real-time.

**Core Philosophy:**
- **Read-only by default:** Safe for exploration without side effects
- **Transparent:** Every operation shows reasoning and evidence
- **Epistemic-first:** Built around the 13-vector assessment system
- **Collaborative:** Designed for human-AI partnership

---

## Installation & Setup

If you haven't installed Empirica yet:

```bash
# Install from source
git clone https://github.com/Nubaeon/empirica.git
cd empirica
pip install -e .

# Verify installation
empirica --version
```

---

## Core Commands

### 1. `empirica cascade`
**Run a complete epistemic workflow.**

This is the primary command for assessing tasks. It runs the full CASCADE flow: PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT.

```bash
# Basic usage
empirica cascade "Should I refactor the authentication system?"

# With context
empirica cascade "Analyze security vulnerabilities" \
  --context ./src/auth \
  --domain security

# Enable real-time dashboard
empirica cascade "Optimize database queries" --enable-dashboard
```

### 2. `empirica assess`
**Perform a 13-vector epistemic assessment.**

Evaluates the current state of knowledge without executing actions.

```bash
# Assess current directory context
empirica assess

# Assess specific vectors
empirica assess --vectors know,uncertainty,risk
```

### 3. `empirica investigate`
**Strategic knowledge gathering.**

Targeted investigation to reduce uncertainty in specific areas.

```bash
# Investigate a specific topic
empirica investigate --topic "OAuth2 implementation details"

# Investigate with specific depth
empirica investigate --topic "Legacy code dependencies" --depth 3
```

### 4. `empirica monitor`
**Real-time session monitoring.**

Watch the epistemic state of an active session or review past sessions.

```bash
# Monitor current active session
empirica monitor --session current

# Review a specific session
empirica monitor --session <session_id>
```

### 5. `empirica bootstrap`
**Initialize metacognitive capabilities.**

Sets up the environment, loads profiles, and initializes the epistemic engine.

```bash
# Standard bootstrap
empirica bootstrap --ai-id my-agent --level 2

# Bootstrap with specific profile
empirica bootstrap --profile high_reasoning_collaborative
```

---

## Command Reference

### Global Options
All commands support these flags:
- `--json`: Output results in JSON format
- `--verbose`: Show detailed reasoning logs
- `--help`: Show command help

### Session Management
```bash
# List all sessions
empirica sessions list

# Show session details
empirica sessions show <session_id>

# Resume a previous session
empirica sessions resume --ai-id <ai_id>
```

### Goals & Subtasks
```bash
# Create a new goal
empirica goals-create --objective "Refactor API" --scope session_scoped

# Add a subtask
empirica goals-add-subtask --goal-id <id> --description "Update endpoints"

# Complete a subtask
empirica goals-complete-subtask --task-id <id> --evidence "PR #123"
```

---

## Interactive Mode

For a guided experience, use the interactive mode:

```bash
empirica interactive
```

Features:
- **Guided Workflows:** Step-by-step CASCADE execution
- **Visual Assessment:** Interactive vector adjustment
- **Session History:** Browse and resume past sessions
- **Tool Selection:** Menu-driven investigation tool selection

---

## CLI + Dashboard Integration

The CLI works seamlessly with the tmux dashboard for visualization.

**Step 1: Start the dashboard**
```bash
# In Terminal 1
empirica dashboard start --mode tmux
```

**Step 2: Run CLI commands**
```bash
# In Terminal 2
empirica cascade "Analyze system architecture" --enable-dashboard
```

**Result:**
The dashboard updates in real-time, showing:
- 13-vector radar chart
- Confidence timeline
- Current phase (PREFLIGHT/INVESTIGATE/etc.)
- Investigation findings

---

## Scripting & Automation

The CLI is designed for automation. Use JSON output for integration with other tools.

**Example: CI/CD Gate Check**

```bash
#!/bin/bash

# Run epistemic assessment on the PR
RESULT=$(empirica assess --context ./src --output json)

# Extract confidence score
CONFIDENCE=$(echo $RESULT | jq .confidence)

# Check if confidence meets threshold
if (( $(echo "$CONFIDENCE < 0.8" | bc -l) )); then
  echo "⚠️ Epistemic confidence too low ($CONFIDENCE). Manual review required."
  exit 1
else
  echo "✅ Confidence validated ($CONFIDENCE). Proceeding."
  exit 0
fi
```

---

## Troubleshooting

**Command not found?**
Ensure your virtual environment is activated:
```bash
source .venv/bin/activate
```

**Permission errors?**
Check file permissions in `.empirica/` directory:
```bash
ls -la .empirica/
```

**Session lock?**
If a session is locked, force unlock:
```bash
empirica sessions unlock <session_id> --force
```

---

**Next Steps:**
- [Connect MCP Server](mcp-integration.md) for IDE integration
- [Explore Skills](skills.md) to enhance capabilities
- [Configure System Prompts](system-prompts.md) for custom behaviors
