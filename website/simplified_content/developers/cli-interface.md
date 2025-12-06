## CLI Interface

**The Heart of Empirica: Direct Epistemic Assessment**

The Empirica CLI is the core interface for metacognitive AI operations. It provides direct, transparent access to the epistemic assessment engine, allowing you to run cascades, investigate uncertainty, and monitor AI reasoning in real-time.

---

## Overview

**Core Philosophy:**
- **Read-only by default:** Safe for exploration without side effects
- **Transparent:** Every operation shows reasoning and evidence
- **Epistemic-first:** Built around the 13-vector assessment system
- **Collaborative:** Designed for human-AI partnership
- **Automation-friendly:** JSON output for CI/CD integration

**50+ commands** organized into logical groups for session management, assessment, investigation, and monitoring.

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

# Get help
empirica --help
```

---

<!-- BENTO_START -->

## 🛫 Preflight Commands
**Start CASCADE workflow with baseline assessment.**

### `empirica preflight`
Execute epistemic preflight assessment.

```bash
# Basic usage
empirica preflight "Should I refactor the authentication system?"

# With session tracking
empirica preflight "Analyze security vulnerabilities" \
  --session-id UUID \
  --output json

# Get just the assessment prompt (for AI analysis)
empirica preflight "Complex architectural decision" \
  --prompt-only
```

### `empirica preflight-submit`
Submit preflight assessment results.

```bash
empirica preflight-submit \
  --session-id UUID \
  --vectors '{"engagement": 0.8, "know": 0.6, "do": 0.7, ...}' \
  --reasoning "Starting task - understanding requirements"
```

## 🔍 Investigation Commands
**Targeted knowledge gathering to reduce uncertainty.**

### `empirica investigate`
Strategic investigation to fill knowledge gaps.

```bash
# Investigate a specific topic
empirica investigate --topic "OAuth2 implementation details"

# Investigate with specific depth
empirica investigate --topic "Legacy code dependencies" --depth 3

# Investigate based on low vectors
empirica investigate --auto  # Automatically targets low vectors
```

### `empirica check`
Mid-workflow assessment to verify understanding.

```bash
empirica check \
  --session-id UUID \
  --findings '["CLI structure explored", "Commands tested"]' \
  --unknowns '["Website validation needed"]' \
  --confidence 0.7
```

## 🛬 Postflight Commands
**Measure learning and calculate epistemic delta.**

### `empirica postflight`
Final assessment after completing work.

```bash
# Final assessment
empirica postflight "CLI cleanup and validation complete"

# With task summary
empirica postflight \
  --session-id UUID \
  --task-summary "Completed 7 tasks, validated website"
```

### `empirica postflight-submit`
Submit final assessment with learning metrics.

```bash
empirica postflight-submit \
  --session-id UUID \
  --vectors '{"engagement": 0.9, "know": 0.8, ...}' \
  --reasoning "Task complete - knowledge increased significantly"
```

<!-- BENTO_END -->

---

<!-- BENTO_START -->

## 📊 Session Management
**Track and resume epistemic sessions.**

### `empirica session-create`
Initialize metacognitive capabilities.

```bash
# Standard bootstrap
empirica session-create --ai-id my-agent --level 2

# Bootstrap with specific profile
empirica session-create --profile high_reasoning_collaborative

# Bootstrap for specific domain
empirica session-create --ai-id security-bot --domain security
```

### `empirica sessions list`
List all sessions.

```bash
# List all sessions
empirica sessions list

# List sessions for specific AI
empirica sessions list --ai-id claude-dev

# List recent sessions
empirica sessions list --recent 10
```

### `empirica sessions resume`
Resume a previous session.

```bash
# Resume last session
empirica sessions resume --ai-id claude-dev

# Resume specific session
empirica sessions resume --session-id UUID
```

### `empirica sessions show`
Show detailed session information.

```bash
# Show session details
empirica sessions show <session_id>

# Show with epistemic trajectory
empirica sessions show <session_id> --trajectory
```

## 🎯 Goals & Subtasks
**Structure work with epistemic tracking.**

### `empirica goals-create`
Create a new goal.

```bash
# Create goal
empirica goals-create \
  --objective "Refactor API" \
  --scope session_scoped \
  --success-criteria '["All tests pass", "Performance improved"]'
```

### `empirica goals-add-subtask`
Add subtask to goal.

```bash
# Add subtask
empirica goals-add-subtask \
  --goal-id <id> \
  --description "Update endpoints" \
  --importance high
```

### `empirica goals-complete-subtask`
Mark subtask as complete.

```bash
# Complete subtask
empirica goals-complete-subtask \
  --task-id <id> \
  --evidence "PR #123 merged"
```

### `empirica goals-progress`
Check goal progress.

```bash
# Check progress
empirica goals-progress --goal-id <id>
```

<!-- BENTO_END -->

---

<!-- BENTO_START -->

## 📈 Monitoring & Analysis
**Real-time epistemic state tracking.**

### `empirica monitor`
Watch session in real-time.

```bash
# Monitor current active session
empirica monitor --session current

# Review a specific session
empirica monitor --session <session_id>

# Monitor with dashboard
empirica monitor --dashboard tmux
```

### `empirica assess`
Perform 13-vector epistemic assessment.

```bash
# Assess current directory context
empirica assess

# Assess specific vectors
empirica assess --vectors know,uncertainty,impact

# Output as JSON for scripting
empirica assess --output json
```

### `empirica calibration-report`
View calibration accuracy.

```bash
# Get calibration report for session
empirica calibration-report --session-id <id>

# Get calibration trends
empirica calibration-report --ai-id claude-dev --trend
```

## 💾 Continuity & Handoffs
**Preserve context across sessions.**

### `empirica handoff-create`
Generate handoff report.

```bash
# Create handoff report
empirica handoff-create \
  --session-id <id> \
  --task-summary "Completed authentication refactor" \
  --key-findings '["OAuth2 implemented", "Tests passing"]' \
  --next-context "Need to deploy to staging"
```

### `empirica handoff-query`
Search handoff reports.

```bash
# Query handoffs for AI
empirica handoff-query --ai-id claude-dev --limit 5

# Query specific session
empirica handoff-query --session-id <id>
```

### `empirica checkpoint-create`
Save epistemic state to git.

```bash
# Create git checkpoint
empirica checkpoint-create \
  --session-id <id> \
  --phase ACT \
  --round-num 3
```

<!-- BENTO_END -->

---

## Command Reference

### Global Options

All commands support these flags:
- `--json`: Output results in JSON format
- `--verbose`: Show detailed reasoning logs
- `--help`: Show command help
- `--quiet`: Suppress non-essential output

### Output Formats

```bash
# Human-readable (default)
empirica assess

# JSON for scripting
empirica assess --output json

# Compact JSON
empirica assess --output json --compact
```

---

## Scripting & Automation

### CI/CD Integration

Use JSON output for automated decision-making:

```bash
# Check confidence before deploying
CONFIDENCE=$(empirica assess --context ./src --output json | jq .confidence)
if (( $(echo "$CONFIDENCE < 0.8" | bc -l) )); then
  echo "Confidence too low for deployment"
  exit 1
fi
```

### Automated Workflows

```bash
#!/bin/bash
# Automated epistemic workflow

# 1. Bootstrap session
SESSION_ID=$(empirica session-create --ai-id ci-bot --level 2 --output json | jq -r .session_id)

# 2. Run preflight
empirica preflight "Run security audit" --session-id $SESSION_ID

# 3. Submit assessment (would be done by AI in practice)
empirica preflight-submit \
  --session-id $SESSION_ID \
  --vectors '{"engagement": 0.9, ...}' \
  --reasoning "Security audit task"

# 4. Execute work
./run_security_audit.sh

# 5. Run postflight
empirica postflight "Security audit complete" --session-id $SESSION_ID

# 6. Get calibration
empirica calibration-report --session-id $SESSION_ID
```

---

## Interactive Mode

For a guided experience, use the interactive mode:

```bash
# Start interactive mode
empirica interactive

# Interactive with specific profile
empirica interactive --profile autonomous_agent
```

The interactive mode provides:
- Step-by-step CASCADE guidance
- Automatic vector assessment prompts
- Real-time epistemic state display
- Investigation recommendations

---

## Dashboard Integration

Launch the tmux dashboard for real-time visualization:

```bash
# Start dashboard
empirica dashboard start --mode tmux

# Dashboard with specific session
empirica dashboard start --session-id <id>

# Stop dashboard
empirica dashboard stop
```

The dashboard shows:
- **13D vector visualization** with live updates
- **CASCADE phase tracking** (PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT)
- **Confidence timeline** showing epistemic trajectory
- **Investigation recommendations** as they're generated

---

## Advanced Usage

### Custom Profiles

```bash
# Use custom profile
empirica session-create --profile-file ./my_profile.json

# Override profile thresholds
empirica session-create \
  --profile high_reasoning \
  --threshold-uncertainty-high 0.75 \
  --threshold-engagement-min 0.65
```

### Domain-Specific Configuration

```bash
# Security domain (stricter thresholds)
empirica session-create --domain security

# Research domain (higher uncertainty tolerance)
empirica session-create --domain research

# Code analysis domain
empirica session-create --domain code_analysis
```

---

## Troubleshooting

### Common Issues

**Command not found:**
```bash
# Ensure empirica is in PATH
which empirica

# Or use python module syntax
python3 -m empirica.cli <command>
```

**Session not found:**
```bash
# List available sessions
empirica sessions list

# Use latest session
empirica monitor --session latest
```

**Database errors:**
```bash
# Check database
ls .empirica/sessions/sessions.db

# Reset database (caution: deletes all sessions)
empirica db-reset --confirm
```

---

## Best Practices

### For Automation

1. **Always use `--output json`** for scripting
2. **Check exit codes** for error handling
3. **Use session IDs** for continuity
4. **Enable verbose logging** for debugging

### For Development

1. **Start with interactive mode** to learn the workflow
2. **Use the dashboard** for real-time feedback
3. **Review calibration reports** to improve self-assessment
4. **Create handoffs** for multi-session work

### For Production

1. **Use profiles** appropriate for your AI model
2. **Set domain-specific thresholds** for your use case
3. **Monitor calibration** to track accuracy over time
4. **Preserve git checkpoints** for auditability

---

**Next Steps:**
- [MCP Integration](../mcp-integration.md) - Integrate with AI assistants
- [API Reference](api-reference.md) - Python API documentation
- [System Prompts](system-prompts.md) - Configure AI behavior
- [Architecture](architecture.md) - Understand the system design
