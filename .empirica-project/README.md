# Empirica Meta-Development

This directory contains configuration for using **Empirica to manage Empirica development** itself.

## Philosophy: Dogfooding

We believe the best way to build Empirica is to use it ourselves. If we wouldn't use our own framework, why should anyone else?

## Quick Start for Contributors

### 1. Start a Session

```bash
# Create a session for your work
empirica session-create --ai-id claude-code

# You'll get a session ID like: 89773382-9ffa-46c8-a644-3de6fc87e32b
```

### 2. Submit PREFLIGHT

Before starting work, assess your epistemic state:

```bash
cat > /tmp/preflight.json << 'PREFLIGHT'
{
  "session_id": "YOUR_SESSION_ID",
  "vectors": {
    "engagement": 0.85,
    "foundation": {
      "know": 0.60,
      "do": 0.75,
      "context": 0.50
    },
    "comprehension": {
      "clarity": 0.80,
      "coherence": 0.70,
      "signal": 0.75,
      "density": 0.40
    },
    "execution": {
      "state": 0.30,
      "change": 0.70,
      "completion": 0.20,
      "impact": 0.75
    },
    "uncertainty": 0.65
  },
  "reasoning": "Task: Add new CLI command. KNOW: 0.60 (familiar with CLI structure), CONTEXT: 0.50 (need to review command_handlers), UNCERTAINTY: 0.65 (unsure about arg parsing best practices)"
}
PREFLIGHT

empirica preflight-submit /tmp/preflight.json
```

### 3. Work Naturally

- Investigate codebase
- Plan implementation
- Write code
- Log findings as you discover them

### 4. CHECK Before Major Changes

```bash
cat > /tmp/check.json << 'CHECK'
{
  "session_id": "YOUR_SESSION_ID",
  "confidence": 0.80,
  "findings": ["Found existing command pattern", "Identified arg parser in cli_core.py"],
  "unknowns": ["Still unsure: error handling strategy"]
}
CHECK

DECISION=$(empirica check /tmp/check.json | jq -r '.decision')
# Returns: "proceed" or "investigate"
```

### 5. POSTFLIGHT After Completion

```bash
cat > /tmp/postflight.json << 'POSTFLIGHT'
{
  "session_id": "YOUR_SESSION_ID",
  "vectors": {
    "engagement": 0.85,
    "foundation": {"know": 0.85, "do": 0.90, "context": 0.80},
    "comprehension": {"clarity": 0.90, "coherence": 0.85, "signal": 0.85, "density": 0.50},
    "execution": {"state": 0.90, "change": 0.95, "completion": 0.95, "impact": 0.85},
    "uncertainty": 0.25
  },
  "reasoning": "Completed CLI command addition. KNOW +0.25, CONTEXT +0.30, UNCERTAINTY -0.40. Learned command_handlers structure, arg parsing patterns, error handling conventions."
}
POSTFLIGHT

empirica postflight-submit /tmp/postflight.json
```

## What We Track

When working on Empirica, we track:

- **Findings**: What we discovered during development
- **Unknowns**: What we're still uncertain about
- **Mistakes**: What didn't work (dead ends)
- **Learning**: How our understanding evolved (PREFLIGHT → POSTFLIGHT delta)

## Benefits of Meta-Development

1. **Validate the framework**: If Empirica helps us develop Empirica, it'll help others
2. **Find edge cases**: Using it ourselves reveals issues users will face
3. **Improve UX**: We experience the developer experience firsthand
4. **Generate examples**: Our own sessions become documentation
5. **Demonstrate value**: Actions speak louder than words

## Example: This Very Session

The session that created this meta-development setup:

```
Session ID: 89773382-9ffa-46c8-a644-3de6fc87e32b
Task: Update distribution configs for v1.0.0 + setup meta-empirica

PREFLIGHT vectors:
- KNOW: 0.75 (familiar with packaging)
- DO: 0.85 (confident)
- UNCERTAINTY: 0.55 (need to verify PyPI, SHA256)

Work completed:
- ✅ Rebuilt wheel with v1.0.0
- ✅ Updated Dockerfile
- ✅ Updated Homebrew formula  
- ✅ Updated Chocolatey nuspec
- ✅ Created PROJECT_CONFIG.yaml
- ✅ Created meta-development README

POSTFLIGHT vectors (to be submitted):
- KNOW: 0.90 (+0.15)
- UNCERTAINTY: 0.30 (-0.25)
```

## Questions?

See `PROJECT_CONFIG.yaml` for the full meta-development configuration.
