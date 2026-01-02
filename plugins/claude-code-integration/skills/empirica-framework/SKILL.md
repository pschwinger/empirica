---
name: empirica-framework
description: "This skill should be used when the user asks to 'assess my knowledge state', 'run preflight', 'do a postflight', 'use CASCADE workflow', 'track what I know', 'measure learning', 'check epistemic drift', or mentions epistemic vectors, calibration, functional self-awareness, or structured investigation before coding tasks."
version: 1.0.0
---

# Empirica: Epistemic Framework for Claude Code

Measure what you know. Track what you learn. Prevent overconfidence.

## Quick Start: CASCADE Workflow

Every significant task follows **PREFLIGHT -> CHECK -> POSTFLIGHT**:

```bash
# 1. Create session
empirica session-create --ai-id claude-code --output json

# 2. Load project context
empirica project-bootstrap --session-id <ID> --output json

# 3. PREFLIGHT - Assess BEFORE starting
empirica preflight-submit - << 'EOF'
{
  "session_id": "<ID>",
  "task_context": "What you're about to do",
  "vectors": {
    "know": 0.6,        # Domain understanding (0-1)
    "uncertainty": 0.4,  # How uncertain you are (0-1)
    "context": 0.7,      # Information sufficiency (0-1)
    "clarity": 0.8       # Understanding of the ask (0-1)
  },
  "reasoning": "Honest assessment of current state"
}
EOF

# 4. Do the work, logging breadcrumbs
empirica finding-log --finding "Key discovery" --impact 0.7
empirica unknown-log --unknown "Question that emerged"

# 5. CHECK - Gate before major action (if uncertainty > 0.5)
empirica check-submit - << 'EOF'
{
  "session_id": "<ID>",
  "task_context": "Ready to implement?",
  "vectors": {"know": 0.75, "uncertainty": 0.3, "context": 0.8, "clarity": 0.85},
  "findings": ["What you learned"],
  "unknowns": ["What's still unclear"],
  "reasoning": "Why you're ready (or not)"
}
EOF

# 6. POSTFLIGHT - Measure learning AFTER completion
empirica postflight-submit - << 'EOF'
{
  "session_id": "<ID>",
  "task_context": "What you completed",
  "vectors": {"know": 0.85, "uncertainty": 0.2, "context": 0.9, "clarity": 0.9},
  "reasoning": "Compare to PREFLIGHT - this is your learning delta"
}
EOF
```

## The 4 Core Vectors

Rate each 0.0 to 1.0 with honest reasoning:

| Vector | Question | Low (0.3) | High (0.8) |
|--------|----------|-----------|------------|
| **KNOW** | What do I understand? | New domain, no experience | Deep familiarity |
| **UNCERTAINTY** | How unsure am I? | Very uncertain, many unknowns | Confident, few gaps |
| **CONTEXT** | Do I have enough info? | Missing key details | Full picture |
| **CLARITY** | Do I understand the ask? | Vague requirements | Crystal clear |

**Key principle:** Be ACCURATE, not optimistic. High uncertainty is valid data.

## Breadcrumb Commands

Log as you work - these link to your active goal automatically:

```bash
# Discoveries
empirica finding-log --finding "Auth uses JWT not sessions" --impact 0.7

# Questions that emerge
empirica unknown-log --unknown "How does rate limiting work here?"

# Dead ends (prevents repeating mistakes)
empirica deadend-log --approach "Tried monkey-patching" --why-failed "Breaks in prod"

# Resolve unknowns
empirica unknown-resolve --unknown-id <UUID> --resolved-by "Found in docs"
```

**Impact scale:** 0.1-0.3 trivial | 0.4-0.6 important | 0.7-0.9 critical

## Goals and Subtasks

For complex work, create goals to track progress:

```bash
# Create goal
empirica goals-create --session-id <ID> --objective "Implement OAuth flow" \
  --scope-breadth 0.6 --scope-duration 0.5 --output json

# Add subtasks
empirica goals-add-subtask --goal-id <GOAL_ID> --description "Research OAuth providers"
empirica goals-add-subtask --goal-id <GOAL_ID> --description "Implement token storage"

# Complete subtasks with evidence
empirica goals-complete-subtask --subtask-id <TASK_ID> --evidence "commit abc123"

# Check progress
empirica goals-progress --goal-id <GOAL_ID>
```

## When to Use CHECK

Run CHECK gate when:
- Uncertainty > 0.5 (too uncertain to proceed safely)
- Scope > 0.6 (high-impact changes)
- Post-compact (context was just reduced)
- Before irreversible actions

CHECK returns `proceed` or `investigate` based on your vectors.

## Calibration: The Learning Loop

The power of Empirica is in the **delta**:

```
PREFLIGHT: know=0.5, uncertainty=0.6
   ... do work ...
POSTFLIGHT: know=0.8, uncertainty=0.2

Learning delta: +0.3 know, -0.4 uncertainty
```

Over time, calibration reports show if you're:
- **Overconfident:** Predicted high, actual lower
- **Underconfident:** Predicted low, actual higher
- **Well-calibrated:** Predictions match outcomes

## Common Patterns

### Pattern 1: Quick Task
```
PREFLIGHT -> Work -> POSTFLIGHT
```

### Pattern 2: Investigation
```
PREFLIGHT -> Investigate -> CHECK -> Work -> POSTFLIGHT
```

### Pattern 3: Complex Feature
```
PREFLIGHT -> Goal + Subtasks -> [CHECK at each gate] -> POSTFLIGHT
```

## Integration with Hooks

This plugin includes automatic hooks for epistemic continuity:

- **PreCompact:** Saves epistemic snapshot before context reduction
- **SessionStart:** Loads bootstrap + snapshot after compact
- **SessionEnd:** Cleans up old snapshots

These run automatically - no manual intervention needed.

## Key Commands Reference

```bash
empirica --help                          # All commands
empirica session-create --ai-id <name>   # Start session
empirica project-bootstrap --session-id <ID>  # Load context
empirica preflight-submit -              # PREFLIGHT (stdin JSON)
empirica check-submit -                  # CHECK gate (stdin JSON)
empirica postflight-submit -             # POSTFLIGHT (stdin JSON)
empirica finding-log --finding "..."     # Log discovery
empirica unknown-log --unknown "..."     # Log question
empirica goals-list                      # Show active goals
empirica check-drift --session-id <ID>   # Detect drift
```

## Best Practices

**DO:**
- Be honest about uncertainty (it's data, not failure)
- Log findings as you discover them
- Use CHECK before major actions
- Compare POSTFLIGHT to PREFLIGHT

**DON'T:**
- Inflate scores to "look good"
- Skip PREFLIGHT (you lose calibration baseline)
- Ignore high uncertainty signals
- Forget to log what you learned

## More Information

See [references/cascade-workflow.md](references/cascade-workflow.md) for detailed CASCADE phases.
See [references/vector-guide.md](references/vector-guide.md) for the full 13-vector system.
See [references/calibration-patterns.md](references/calibration-patterns.md) for calibration examples.

---

**Remember:** When uncertain, say so. That's genuine metacognition.
