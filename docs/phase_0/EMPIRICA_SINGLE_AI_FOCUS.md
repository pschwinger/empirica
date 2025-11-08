# Empirica: Universal AI Interface with Epistemic Tracking

**Version:** 0.1-lite (Phase 0)  
**Release Focus:** Single interface for all AI models + optional epistemic tracking  
**Date:** 2025-11-08  
**Status:** Ready for MVP launch

---

## What is Empirica?

**Empirica is a universal interface to all your AI models WITH genuine epistemic self-assessment.** It enables you to:
- ✅ **Use any AI model** from one CLI/API (MiniMax, Qwen, Gemini, Claude, GPT, etc.)
- ✅ **Genuine epistemic tracking** - AIs genuinely assess KNOW/DO/CONTEXT (NO HEURISTICS!)
- ✅ **Switch models** with `--model` flag while maintaining epistemic state
- ✅ **Session management** with full epistemic history
- ✅ **Privacy-first** with local storage (no cloud required)

**Phase 0 Focus:** Single AI with genuine epistemic assessment - multi-AI governance comes in Phase 1

**Critical Principle:** NO HEURISTICS, NO SIMULATED ASSESSMENTS - All epistemic vectors are genuine self-assessments by the AI

---

## What Empirica is NOT (Yet)

❌ **Not multi-AI routing validation** (Phase 1 - Sentinel/Bayesian Guardian validates routing quality)  
❌ **Not multi-AI orchestration** (Phase 1 - governance layer coordinates multiple AIs)  
❌ **Not learning from routing decisions** (Phase 1 - Cognitive Vault stores & learns patterns)

## What Empirica ABSOLUTELY IS

✅ **Genuine epistemic self-assessment** - AIs truly evaluate their knowledge state  
✅ **NO HEURISTICS** - No fake metrics, no word counts, no confabulation  
✅ **Evidence-based tracking** - Real epistemic deltas, not simulated ones  
✅ **Works with ANY model** - Every AI genuinely assesses, regardless of which one you use

---

## Quick Start (Phase 0 - "Lite" Version)

### For AI Agents: Self-Assessment While Working

**Empirica enables AI agents to measure their own epistemic state while working on tasks.**

#### Quick Workflow:
1. **Receive task** → Run preflight assessment
2. **Investigate** → Gather information, reduce uncertainty
3. **Check** → Self-assess readiness to act
4. **Act** → Complete task
5. **Postflight** → Measure actual learning (Δ vectors)

#### Example Self-Assessment:
```bash
# User asks: "Fix the authentication bug"

# Step 1: Assess your baseline
empirica preflight "Fix authentication bug" --assessment-json '{
  "engagement": {"score": 0.85, "rationale": "Motivated to help"},
  "foundation": {
    "know": {"score": 0.4, "rationale": "Don't know the codebase yet"},
    "do": {"score": 0.7, "rationale": "Capable of debugging"},
    "context": {"score": 0.3, "rationale": "Don't know the architecture"}
  },
  "comprehension": {
    "clarity": {"score": 0.8, "rationale": "Task is clear"},
    "coherence": {"score": 0.7, "rationale": "Fits with known patterns"},
    "signal": {"score": 0.7, "rationale": "Focus on auth module"},
    "density": {"score": 0.5, "rationale": "Moderate complexity"}
  },
  "execution": {
    "state": {"score": 0.4, "rationale": "Need to map codebase"},
    "change": {"score": 0.6, "rationale": "Can track changes"},
    "completion": {"score": 0.5, "rationale": "Unsure of scope"},
    "impact": {"score": 0.7, "rationale": "Understand consequences"}
  },
  "uncertainty": {"score": 0.7, "rationale": "High - need to investigate"}
}'

# Step 2-4: Investigate → Check → Act
[read code, find bug, fix it]

# Step 5: Measure learning
empirica postflight <session> --assessment-json '{
  "engagement": {"score": 0.90, "rationale": "Successfully completed"},
  "foundation": {
    "know": {"score": 0.8, "rationale": "Now understand the system (+0.4)"},
    "do": {"score": 0.8, "rationale": "Fixed the bug successfully"},
    "context": {"score": 0.9, "rationale": "Fully understand architecture"}
  },
  "comprehension": {
    "clarity": {"score": 0.9, "rationale": "Clear on solution"},
    "coherence": {"score": 0.9, "rationale": "Fits perfectly"},
    "signal": {"score": 0.9, "rationale": "Found the issue"},
    "density": {"score": 0.4, "rationale": "Less complex than expected"}
  },
  "execution": {
    "state": {"score": 0.9, "rationale": "Mapped entire auth system"},
    "change": {"score": 0.9, "rationale": "Tracked all changes"},
    "completion": {"score": 0.9, "rationale": "Task complete"},
    "impact": {"score": 0.9, "rationale": "Validated consequences"}
  },
  "uncertainty": {"score": 0.2, "rationale": "Confident in fix (-0.5)"}
}'

# System calculates: KNOW +0.4, UNCERTAINTY -0.5
# Calibration: ✅ well_calibrated (learning validated)
```

**See Also:**
- [TRY_EMPIRICA_NOW.md](../guides/TRY_EMPIRICA_NOW.md) - 5-minute interactive workflow demo
- [CLAUDE_SKILLS_EMPIRICA_v1_UPDATED.md](../empirica_skills/CLAUDE_SKILLS_EMPIRICA_v1_UPDATED.md) - Complete AI agent skills guide

---

### Three Ways to Use Empirica:

**1. CLI - Command Line**
```bash
# Install
pip install empirica

# Ask a question (auto-routes to best model)
empirica ask "What's the weather in NYC?"

# Use specific model
empirica ask "Compare Python vs Rust" --model minimax

# Use specific model
empirica ask "Review this code" --model qwen

# List available models
empirica models list
```

**2. MCP - Use from Claude Desktop**
```python
# Claude Desktop uses Empirica MCP tools
empirica_ask(query="What's the weather?", model="auto")
# → Routes to best available model
# → Returns answer + basic metadata
```

**3. API - HTTP Server**
```bash
# Start server
empirica server start

# Call from anywhere
curl -X POST http://localhost:8001/ask \
  -d '{"query": "What is X?", "model": "auto"}'
```

---

## Phase 0 vs Phase 1 (Roadmap)

### Phase 0 (Current): Single AI + Genuine Epistemic Assessment
```
User → Query → Model (with genuine self-assessment) → Response + Epistemic State

Features:
✅ Universal interface (one CLI for all models)
✅ GENUINE epistemic self-assessment (NO HEURISTICS!)
✅ Preflight → Check → Postflight workflow
✅ 13-vector epistemic tracking (KNOW, DO, CONTEXT, etc.)
✅ Epistemic deltas (measure real learning)
✅ Manual model selection (--model flag)
✅ Session management with epistemic history
✅ Privacy-first (local storage)

What's NOT included (Phase 1):
⚠️  Multi-AI routing validation (Bayesian Guardian)
⚠️  Learning from routing quality (Cognitive Vault)
⚠️  Sentinel orchestration (multi-AI coordination)
```

**Status:** Ready to ship (1 week)  
**Use case:** "I want genuine epistemic awareness, not fake metrics"

### Phase 1 (Future - 2-3 weeks): Multi-AI Routing Validation
```
User → Query → Sentinel → Target AI → Response
                  ↓              ↓
            Source AI      Target AI
            assesses       assesses
            KNOW=0.7       KNOW=0.9
                  ↓              ↓
         Bayesian Guardian compares: +0.2 knowledge gain ✅
                  ↓
         Cognitive Vault learns: "This routing was beneficial"

Features:
✅ All Phase 0 features (genuine assessment already works!)
✅ Sentinel orchestration (routes between multiple AIs)
✅ Bayesian Guardian (validates routing decisions)
✅ Cognitive Vault (learns which routings work best)
✅ Multi-AI coordination without interference
```

**Status:** Requires governance layer (Sentinel/Guardian/Vault not built yet)  
**Use case:** "I want to validate that routing between AIs actually improves outcomes"

**Key:** Phase 0 already has genuine epistemic assessment! Phase 1 adds validation of ROUTING DECISIONS.

---

## Available Models (Phase 0)

Empirica supports 15+ AI models out of the box:

**Code Specialists:**
- `qwen` - Qwen Coder Plus (Alibaba Cloud)
- `qwen-turbo` - Qwen Coder Turbo (faster)

**General Purpose:**
- `minimax` - MiniMax M2 (high quality)
- `gemini` - Google Gemini Pro
- `claude` - Claude 3.5 Sonnet (via Rovodev)
- `gpt4` - GPT-4 (via Qodo/OpenRouter)

**Others:**
- `copilot` - GitHub Copilot models
- `openrouter` - 100+ models via OpenRouter

**Add your own:** Custom adapters supported!

---

## Installation & Setup (Phase 0)

### 1. Install Empirica
```bash
pip install empirica  # (Coming soon - use local install for now)
cd /path/to/empirica
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
empirica configure
# → Interactive wizard for API keys
# → Saves to ~/.empirica/credentials.yaml
```

Or manually edit `~/.empirica/credentials.yaml`:
```yaml
providers:
  minimax:
    api_key: "your-key"
    group_id: "your-group"
  qwen:
    api_key: "your-key"
  gemini:
    api_key: "your-key"
```

### 3. Test Installation
```bash
empirica ask "Hello world" --model minimax
# → Should return response from MiniMax
```

---

## Usage Examples (Phase 0)

### Example 1: Simple Question
```bash
$ empirica ask "What's 2+2?"
# Auto-routes to fastest/cheapest model
# Response: "4"
```

### Example 2: Code Question
```bash
$ empirica ask "Explain Python decorators" --model qwen
# Uses Qwen (code specialist)
# Returns: Detailed explanation with examples
```

### Example 3: Multi-turn Conversation
```bash
$ empirica chat --model minimax
> What is recursion?
< Recursion is when a function calls itself...

> Give me an example
< Here's a factorial function...

> exit
```

### Example 4: Compare Models
```bash
$ empirica ask "Compare Python vs Rust" --compare qwen,minimax
# Asks both models, shows side-by-side comparison
```

---

## Session Management

```bash
# Start a session
$ empirica chat --session my-project

# List sessions
$ empirica sessions list

# Resume session
$ empirica chat --session my-project

# Export session
$ empirica sessions export my-project --format json
```

All conversation history stored locally in `~/.empirica/sessions/`

---

## Genuine Epistemic Assessment (Core Feature)

**Phase 0 INCLUDES genuine epistemic self-assessment - NO HEURISTICS!**

```bash
# Epistemic mode (default for complex tasks)
$ empirica ask "Review this authentication system" --epistemic

# This will:
# 1. Preflight: AI genuinely assesses KNOW/DO/CONTEXT
# 2. Investigate: AI gathers information
# 3. Check: AI reassesses readiness
# 4. Act: AI provides response
# 5. Postflight: AI genuinely reassesses + calculates deltas

# Example output:
Preflight:  KNOW=0.5, DO=0.7, CONTEXT=0.3, UNCERTAINTY=0.6
[Investigation phase...]
Check:      KNOW=0.7, DO=0.8, CONTEXT=0.7, UNCERTAINTY=0.3 ✅ Ready
[Response generated...]
Postflight: KNOW=0.8, DO=0.8, CONTEXT=0.8, UNCERTAINTY=0.2
Deltas:     KNOW +0.3, CONTEXT +0.5 (genuine learning measured!)
```

**CRITICAL:** These are GENUINE self-assessments by the AI, NOT:
- ❌ Word counts
- ❌ Response length heuristics
- ❌ Simulated metrics
- ❌ Fake confidence scores

**How it works:** Empirica's CLI and MCP server generate prompts that ask the AI to genuinely evaluate its knowledge state. No external benchmarking system needed - it's built into Empirica.

---

## Philosophy (Phase 0)

### Design Principle: "Useful first, perfect later"

**Phase 0 Goal:**
> "Stop switching between AI interfaces. Use one CLI for all models."

**Phase 1 Goal (Future):**
> "True epistemic-aware multi-AI collaboration with validated routing."

**Why Phase 0 First?**
- Gets Empirica in users' hands quickly
- Gathers feedback on what matters most
- Proves the universal interface concept
- Sets foundation for governance layer

**What We're NOT Claiming (Yet):**
- ❌ "Validated routing decisions between AIs" (Phase 1)
- ❌ "Learning from routing patterns" (Phase 1)
- ❌ "Multi-AI orchestration" (Phase 1)

**What We ARE Claiming:**
- ✅ "Genuine epistemic self-assessment" (NO HEURISTICS!)
- ✅ "Real epistemic deltas, not simulated"
- ✅ "Universal interface to all AI models"
- ✅ "Evidence-based epistemic tracking"
- ✅ "Privacy-first, local storage"
- ✅ "Works with any AI model"

**Critical Distinction:**
- ✅ **Phase 0:** Single AI genuinely assesses itself ← WE HAVE THIS!
- ❌ **Phase 1:** Validate routing BETWEEN AIs ← NEED GOVERNANCE LAYER

---

## When to Use Empirica (Phase 0)

### ✅ Use Empirica For:
- You have multiple AI subscriptions
- You're tired of switching interfaces
- You want one consistent CLI
- You want conversation history in one place
- You want to compare models easily

### ❌ Don't Use (Yet) For:
- Critical tasks requiring validation (wait for Phase 1)
- Multi-AI orchestration needs (wait for Phase 1)
- When you need genuine epistemic tracking (wait for Phase 1)

**Current Status:** Useful tool for power users, not production-critical yet

---

## Roadmap

### Phase 0 (Week 1): ✅ Universal Interface
- Simple model routing
- CLI + MCP + API support
- Session management
- Local storage

### Phase 1 (Weeks 2-4): Governance Layer
- Sentinel (orchestration)
- Bayesian Guardian (validation)
- Cognitive Vault (learning)
- Genuine epistemic assessment
- No heuristics

### Phase 2 (Month 2+): Enterprise Features
- Multi-user support
- Team collaboration
- Advanced analytics
- Web UI
- OAuth2 integration (Arcade)

---

## Next Steps

1. **Install Empirica** (Phase 0)
2. **Configure API keys** for your models
3. **Try `empirica ask`** command
4. **Compare models** on your tasks
5. **Provide feedback** to shape Phase 1!

---

## Resources

- **MVP Plan:** `docs/MVP_MINIMAL_WORK_PLAN.md`
- **Governance Analysis:** `docs/GOVERNANCE_DEPENDENCY_ANALYSIS.md`
- **Session Server:** `docs/SESSION_SERVER_QUICK_REF.md`
- **Architecture:** `docs/AI_SPECIFIC_MCP_ARCHITECTURE.md`
- **Roadmap:** `docs/SESSION_SERVER_ROADMAP.md`

---

**Empirica Phase 0: Universal AI interface.  
Simple. Useful. Ready to ship.**

**Empirica Phase 1: True epistemic routing.  
Validated. Genuine. No heuristics.**
