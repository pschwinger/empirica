# CLI Interface

**Direct Epistemic Assessment.**

The heart of Empirica operations.

---

## Essential Commands

<!-- BENTO_START -->

## 🛫 Preflight
**Start Assessment.**

`empirica preflight "Task description"`
Initiates the CASCADE workflow with a baseline assessment.

## 🔍 Investigate
**Gather Knowledge.**

`empirica investigate --topic "OAuth"`
Targeted investigation to reduce uncertainty.

## 🛬 Postflight
**Measure Learning.**

`empirica postflight "Task complete"`
Final assessment to calculate epistemic delta.

<!-- BENTO_END -->

---

## Session Management

### Bootstrap
Initialize a new session with a specific profile.
```bash
empirica bootstrap --profile high_reasoning_collaborative
```

### Resume
Continue a previous session.
```bash
empirica sessions-resume --ai-id claude-dev
```

### Monitor
Watch real-time epistemic state.
```bash
empirica monitor --session current
```

---

## Scripting & Automation

Use JSON output for CI/CD integration.

```bash
# Check confidence before deploying
CONFIDENCE=$(empirica assess --context ./src --output json | jq .confidence)
if (( $(echo "$CONFIDENCE < 0.8" | bc -l) )); then
  echo "Confidence too low."
  exit 1
fi
```

---

**Next Steps:**
- [MCP Integration](../mcp-integration.md)
- [System Prompts](system-prompts.md)
