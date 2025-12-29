# 🚀 Epistemic MCP Server - Quick Start

## 5-Minute Setup

### 1. Standard MCP Server (No Changes)

```bash
empirica-mcp
```

Works exactly as before. No epistemic layer.

### 2. Epistemic MCP Server (NEW)

```bash
export EMPIRICA_EPISTEMIC_MODE=true
empirica-mcp
```

Now every tool call includes epistemic self-awareness!

### 3. Try Different Personalities

```bash
# Cautious (investigates early)
export EMPIRICA_PERSONALITY=cautious_researcher

# Pragmatic (action-oriented)
export EMPIRICA_PERSONALITY=pragmatic_implementer

# Balanced (default)
export EMPIRICA_PERSONALITY=balanced_architect

# Adaptive (learns over time)
export EMPIRICA_PERSONALITY=adaptive_learner

empirica-mcp
```

---

## What You'll See

### Normal Tool Response
```json
{
  "ok": true,
  "session_id": "abc123",
  "message": "Session created"
}
```

### Epistemic Tool Response
```json
{
  "ok": true,
  "session_id": "abc123",
  "message": "Session created",
  
  "epistemic_state": {
    "vectors": {
      "know": 0.60,
      "uncertainty": 0.40,
      "context": 0.70,
      "clarity": 0.85
    },
    "routing": {
      "mode": "confident_implementation",
      "confidence": 0.85,
      "reasoning": "Know=0.60 ≥ 0.6, Uncertainty=0.40 < 0.5, confident execution"
    }
  }
}
```

Plus optional mode guidance!

---

## Claude Desktop Config

```json
{
  "mcpServers": {
    "empirica-epistemic": {
      "command": "bash",
      "args": [
        "-c",
        "EMPIRICA_EPISTEMIC_MODE=true EMPIRICA_PERSONALITY=balanced_architect empirica-mcp"
      ]
    }
  }
}
```

Restart Claude Desktop, and epistemic mode is active!

---

## Testing Locally

```bash
# Test components
cd empirica-mcp
python test_epistemic.py

# Should output:
# ✅ All components working!
```

---

## What Happens Behind the Scenes

```
1. Tool call arrives (e.g., "session_create")
   ↓
2. EpistemicStateMachine assesses request
   → Updates vectors (clarity, uncertainty, etc.)
   ↓
3. VectorRouter routes based on vectors
   → Selects mode (load_context, investigate, implement, etc.)
   ↓
4. EpistemicModes executes mode behavior
   → Provides guidance if needed
   ↓
5. Original tool handler executes
   → Normal MCP response
   ↓
6. StateMachine learns from result
   → Updates vectors (know↑, uncertainty↓, etc.)
   ↓
7. Middleware enriches response
   → Adds epistemic context to response
```

---

## 5 Behavioral Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **clarify** | clarity < 0.6 | Ask questions before proceeding |
| **load_context** | context < 0.5 | Load project data first |
| **investigate** | uncertainty > 0.6 | Systematic research |
| **confident_implementation** | know ≥ 0.7, uncertainty < 0.4 | Direct action |
| **cautious_implementation** | Moderate vectors | Careful, incremental steps |

---

## Observe Routing Changes

```bash
# Low context request → load_context mode
tool: session_create (first time)

# High uncertainty request → investigate mode  
tool: create_goal with complex objective

# High confidence request → confident_implementation
tool: list_sessions (simple query)
```

---

## Customization

Want custom personality thresholds?

Edit: `empirica_mcp/epistemic/personality.py`

```python
CUSTOM_PROFILE = PersonalityProfile(
    name="custom",
    thresholds={
        "uncertainty_tolerance": 0.5,
        "context_threshold": 0.6,
        "know_threshold": 0.8,
        "clarity_threshold": 0.7
    },
    description="Your custom behavior"
)
```

---

## What's Next?

1. **Try it** - Enable epistemic mode and observe
2. **Compare** - Toggle between standard and epistemic
3. **Tune** - Adjust personality thresholds
4. **Extend** - Add custom modes for your domain

**Welcome to vector-programmed AI agents.** 🧠
