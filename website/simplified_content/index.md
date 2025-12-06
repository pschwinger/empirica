# We Gave AI a Mirror.

---

## When Everything Clicks Into Place

AI hallucinates because it **can't distinguish knowledge from guessing.**

Traditional approaches fail:
- ❌ Prompting "be honest" - No systematic framework
- ❌ Heuristics - Fake confidence, not real self-awareness
- ❌ Fine-tuning alone - Doesn't teach metacognition

**Empirica changes this.**

We give AI a measurement system for its own knowledge state—genuine epistemic self-awareness through systematic CASCADE assessment.

---
<!-- bento --->
## Key Differentiators

<div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-12">

<div class="glass-card p-6 rounded-xl glow-effect flex flex-col items-center text-center" markdown="1">
<img src="/assets/icons/brain-vectors.svg" alt="Genuine Self-Assessment" class="w-16 h-16 mb-4 text-indigo-400">
<!-- bento --->
### 🧠 Genuine Self-Assessment
Not heuristics. Not keyword matching. **LLM-powered honest reasoning** across 13 epistemic vectors. The AI genuinely evaluates what it knows, can do, and is uncertain about.
</div>

<div class="glass-card p-6 rounded-xl glow-effect flex flex-col items-center text-center" markdown="1">
<img src="/assets/icons/git-memory.svg" alt="Multi-Session Memory" class="w-16 h-16 mb-4 text-indigo-400">
<!-- bento -->
### 🔄 Multi-Session Memory
**Epistemic handoffs** (~400 tokens) preserve learning across sessions. 73% more efficient than manual summaries, automated, includes calibration data. **Making Git sexy again** - version-controlled epistemic state.
</div>

<div class="glass-card p-6 rounded-xl glow-effect flex flex-col items-center text-center" markdown="1">
<img src="/assets/icons/ecosystem.svg" alt="Production Ready" class="w-16 h-16 mb-4 text-indigo-400">

### 🚀 Production Ready
**23 MCP tools** for any MCP-compatible environment. **50+ CLI commands.** Python API. Git integration. SQLite + JSON + Git notes persistence. Ready to deploy today.
</div>

</div>

[Why This Matters →](use-cases.md) | [See Features →](features.md)

---

## The Framework: What, Why, How, When, Which, Who

| Component | Explanation |
|-----------|-------------|
| **What** | Epistemic state as versioned Git content (commits as CASCADE snapshots, notes as structured data, branches as reasoning paths) |
| **Why** | Automation of orchestration: branching decisions, merge logic, multi-AI sync, governance validation—all driven by epistemic vectors |
| **How** | Sentinel monitors vectors, triggers Git operations (branch/merge/fetch/push), uses hooks for governance, stores history in notes |
| **When** | Real-time monitoring via git log polls, triggered on every commit, automated decisions based on vector thresholds |
| **Which** | Multi-AI collaboration, distributed teams, container orchestration, compliance audits, self-improvement loops, knowledge distillation |
| **Who** | Engineers (context continuity), scientists (measured confidence), compliance (audit trail), DevOps (container coordination), researchers (transfer learning), enterprise (scale) |

[Read the Full Story: Making Git Sexy Again →](MAKING_GIT_SEXY_AGAIN.md)

---

## Foundation Infrastructure

---

## CASCADE Workflow
**7-phase epistemic reasoning system:**

```
PREFLIGHT → THINK → PLAN → INVESTIGATE → CHECK → ACT → POSTFLIGHT
```

**Before acting:** Assess knowledge gaps
**During work:** Track learning systematically
**After completion:** Measure epistemic growth

Each phase measures all 13 vectors. Learning deltas calculated automatically.

[Deep Dive: CASCADE →](epistemics.html)

---

## 13 Epistemic Vectors

**Gate:** ENGAGEMENT (≥0.60 required)

**Foundation (35%):** KNOW · DO · CONTEXT
**Comprehension (25%):** CLARITY · COHERENCE · SIGNAL · DENSITY
**Execution (25%):** STATE · CHANGE · COMPLETION · IMPACT
**Meta-Epistemic:** UNCERTAINTY · CALIBRATION

**Critical thresholds trigger automated decisions:**
- High uncertainty → INVESTIGATE phase
- Low coherence → RESET task
- Cognitive overload → SIMPLIFY approach

[Complete Vector Guide →](epistemics.html)

---

## Delta Learning Measurement

**PREFLIGHT vs POSTFLIGHT comparison** automatically tracks:

```
Session Start (PREFLIGHT):  KNOW: 0.4, UNCERTAINTY: 0.6
↓
[INVESTIGATE + ACT phases]
↓
Session End (POSTFLIGHT):   KNOW: 0.85, UNCERTAINTY: 0.2

Epistemic Delta: +0.45 knowledge, -0.40 uncertainty
```

Learning growth measured, not guessed. Calibration validated against actual outcomes.

[See Examples →](examples.html)

---

## Goal & Subtask Management

**Structured task tracking integrated with CASCADE:**

- Create goals with success criteria
- Break down into epistemic subtasks
- Track completion with evidence
- Query progress across sessions
- Multi-AI coordination support

**MCP + CLI tools** make this seamless.

[Goal Management Guide →](features.html)

---

## Architectural Overview

### Storage Layer (Triple Redundancy)
- **SQLite** - Queryable, relational tracking
- **JSON** - Human-readable, portable exports
- **Git Notes** - Version-controlled checkpoints (~450 tokens)

### Continuity System
- **Epistemic Handoffs** - Session-to-session continuity (~400 tokens)
- **Calibration Reports** - Knowledge distillation for training
- **Git Integration** - Distributed, portable, version-controlled

### Integration Interfaces
- **MCP Server** - 23 tools for any MCP-compatible environment
- **CLI** - 50+ commands for automation
- **Python API** - Embed in any application

**Everything talks to everything.** Session data in SQLite. Checkpoints in Git. Handoffs queryable. Goals tracked. Learning measured.

[Architecture Details →](developers/architecture.html)

---

## MCP ↔ CLI Mapping

Every MCP tool has a CLI equivalent:

| MCP Tool | CLI Command | Purpose |
|----------|-------------|---------|
| `bootstrap_session` | `empirica session-create` | Initialize session |
| `execute_preflight` | `empirica preflight` | Baseline assessment |
| `create_goal` | `empirica goals-create` | Structure work |
| `create_handoff_report` | `empirica handoff-create` | Session continuity |
| `create_git_checkpoint` | `empirica checkpoint-create` | Version control |

**Use MCP for AI assistants. Use CLI for automation.**

[Full MCP Guide →](mcp-integration.md) | [CLI Reference →](developers/cli-interface.md)

---

## 🔮 Cognitive Vault (Coming Soon)

**Enterprise-grade intelligence infrastructure** for teams:

### Advanced Components

**Bayesian Guardian**
Evidence-based belief tracking with automated discrepancy detection

**Sentinel**
Behavioral drift monitoring and integrity validation

**AUGIE** (Adaptive Uncertainty Grounded Intelligence Engine)
Cross-AI collaboration with shared epistemic state

**Meta-MCP**
Epistemic state-based routing and role assignment across AI agents

**Available for teams and enterprise users.** Early access program opening Q1 2026.

[Join Waitlist →](contact.md)

---

## Quick Start

### Option 1: MCP Integration (30 seconds)
**Works with any MCP-compatible environment: IDEs (Cursor, Windsurf, Antigravity) or CLIs (Claude Code, Qwen Code, Gemini CLI)**

Add to MCP config:
```json
{
  "mcpServers": {
    "empirica": {
      "command": "/path/to/empirica/.venv-mcp/bin/python3",
      "args": ["-m", "empirica.mcp_local.empirica_mcp_server"]
    }
  }
}
```

Restart client. Use 23 MCP tools immediately.

[Full MCP Setup →](mcp-integration.md)

### Option 2: CLI (5 minutes)
```bash
# NPM package (coming soon)
npm install -g empirica

# Or from source
git clone https://github.com/Nubaeon/empirica
cd empirica
pip install -e .

empirica session-create --ai-id=your-id --level=2
empirica preflight --session-id=latest --prompt="Your task"
```

[Getting Started →](getting-started.md)

### Option 3: Python API
```python
from empirica import CanonicalEpistemicCascade

cascade = CanonicalEpistemicCascade(
    agent_id="your-agent",
    enable_bayesian=True
)

result = await cascade.run_epistemic_cascade(
    task="Your task",
    context={"domain": "your_domain"}
)
```

[API Docs →](developers/api-reference.md)

---

## Provider Agnostic by Design

**Works everywhere. Excels with smaller models.**

### High-Reasoning Models
Claude, GPT-4, Gemini benefit from **structured decision-making** and **explicit uncertainty tracking**.

### Fast-Acting Models
Qwen-3-32B, Phi-4, Mistral, Ollama models gain **guidance and structure** that dramatically improves output quality.

### Modern IDEs
Cursor, Windsurf, Antigravity get **native epistemic awareness** through MCP integration.

### CLI Interfaces
Claude Code, Qwen Code, Gemini CLI, Copilot CLI enable **automation workflows** with 50+ commands.

**Tested across the entire ecosystem.** November 2025.

---

## Why Empirica Wins

| Traditional AI | Empirica |
|---------------|----------|
| Simulated confidence | **Measured epistemic state** |
| Hidden uncertainty | **13th vector tracks unknowns** |
| No learning metrics | **PREFLIGHT ↔ POSTFLIGHT deltas** |
| Manual session summaries | **Automated handoffs (~400 tokens)** |
| No calibration | **Tracked and validated** |
| Vendor lock-in | **Provider agnostic (tested: Claude, GPT-4, Gemini, Qwen, Phi-4, Mistral, Ollama)** |

---

## Real-World Impact

**Multi-day development** - Build across sessions without context loss
**Security analysis** - Explicit uncertainty prevents overconfidence
**Multi-agent teams** - Shared epistemic state coordination
**Knowledge distillation** - Calibration reports for model training

[Use Cases →](use-cases.md) | [Examples →](examples.md)

---

## Learn More

**Core Concepts:**
- [13 Epistemic Vectors](epistemics.html) - Complete measurement system
- [CASCADE Workflow](developers/architecture.html) - 7-phase process
- [AI vs Agent Patterns](ai-vs-agent.html) - When to use what

**Get Building:**
- [Getting Started](getting-started.md) - Installation & first steps
- [MCP Integration](mcp-integration.md) - AI assistant setup
- [API Reference](developers/api-reference.md) - Complete Python API
- [CLI Commands](developers/cli-interface.md) - 50+ command reference

**More:**
- [Features](features.md) - Complete feature list
- [FAQs](faqs.md) - Common questions
- [Contact](contact.md) - Get in touch

---

## What, Why, How, When, Which, Who?

**Complete framework for understanding Empirica's positioning:**

### WHAT: Epistemic State as Versioned Infrastructure

Empirica measures and tracks AI's knowledge state across 13 epistemic vectors:
- **KNOW** (domain knowledge), **DO** (execution capability), **CONTEXT** (environmental awareness)
- **CLARITY** (task understanding), **COHERENCE** (logical consistency), **SIGNAL** (information quality), **DENSITY** (complexity management)
- **STATE** (readiness), **CHANGE** (progress), **COMPLETION** (goal proximity), **IMPACT** (consequence awareness)
- **UNCERTAINTY** (explicit unknowns), **CALIBRATION** (confidence accuracy)

Stored in Git as versioned content: commits (CASCADE snapshots) + notes (structured data) + branches (reasoning paths).

**[Deep dive: MAKING_GIT_SEXY_AGAIN.md](../../MAKING_GIT_SEXY_AGAIN.md)**

---

### WHY: Automation of Orchestration Hard Stuff

Traditional AI orchestration requires custom infrastructure. Empirica uses Git primitives:

- **Branching Logic:** Sentinel automatically creates investigation branches when UNCERTAINTY > 0.70 or KNOW < 0.50
- **Merging for Calibration:** Measures which reasoning paths are more efficient, learns from success patterns
- **Multi-AI Coordination:** Uses git remotes (no central database needed), AIs coordinate via git push/pull
- **Zero-Trust Governance:** Signed commits, required approvals, immutable audit trail
- **No Custom Code:** Git already handles versioning, distribution, signing, merging — repurpose it for AI

**Result:** Orchestration that's simpler, more reliable, and built on proven infrastructure.

---

### HOW: Sentinel Orchestrator Controls Everything via Git

Sentinel is the "git master" managing AI reasoning:

```
Monitor (git log)     → Detect epistemic state
  ↓
Decide (thresholds)   → Branch or merge?
  ↓
Execute (git ops)     → Create branch, merge, rebase
  ↓
Measure (calibration) → Which path was more efficient?
  ↓
Learn (git notes)     → Store for future decisions
```

**Single AI Session:** CASCADE phases → git commits → epistemic snapshots

**Multi-AI Coordination:** AI-1 pushes main → AI-2 fetches + rebases → AI-3 continues work from known state

**Calibration:** Post-merge, Sentinel calculates δ_KNOW, δ_UNCERTAINTY, stores in git notes for learning

---

### WHEN: Continuous Real-Time Orchestration

- **Every CASCADE commit** triggers Sentinel decisions
- **Every git log poll** checks if investigation branches should be created or merged
- **Every phase completion** updates epistemic vectors and evaluates thresholds
- **Post-merge** automatically calculates calibration deltas
- **Across sessions** handoffs preserve learning in structured ~400 token summaries

**Timeline:** No delays, no bottlenecks, pure Git ops (microseconds)

---

### WHICH: Use Cases Across Every Domain

| Domain | How Empirica Helps |
|--------|-------------------|
| **Multi-AI Teams** | Coordinate 5+ AIs without central server, pure Git remotes |
| **Distributed Development** | Compliance audit trail (git log shows all reasoning) |
| **Security Analysis** | Explicit uncertainty prevents overconfidence, measured risk |
| **Container Orchestration** | Zero-trust: AIs sync via signed git commits, no shared DB |
| **Self-Improvement Loops** | Calibration data proves which strategies work best |
| **Knowledge Distillation** | Use calibration reports to train smaller models |
| **Multi-Session Projects** | 3-day development with continuous epistemic context |
| **Quality Assurance** | Epistemic coverage reveals unknown unknowns before production |

---

### WHO: Benefits by Role

| Role | Current Pain | Empirica Solves | Immediate Win |
|------|--------------|-----------------|---------------|
| **Software Engineer** | Context loss across sessions | Epistemic handoffs preserve learning | Multi-day projects with continuity |
| **Data Scientist** | Can't trust AI confidence | 13 vectors measured, not guessed | Make confident decisions about model outputs |
| **Security Officer** | No audit trail of AI reasoning | Complete git log + signatures | Instant compliance validation |
| **DevOps Engineer** | Complex container coordination | Git remotes handle everything | Coordinate 10+ AIs without infrastructure |
| **AI Researcher** | Can't measure learning transfer | Calibration data tracks it | Evidence that guidance helps small models |
| **Enterprise Manager** | High cost of AI orchestration | Pure Git infrastructure | Scale team from 1 AI to 50 AIs |

---

## The Bottom Line

**Empirica makes AI genuinely self-aware through epistemic measurement, then automates coordination by treating Git as cognitive infrastructure.**

Not a vendor-specific platform. Not proprietary inference. Not monthly subscriptions.

**Just Git + systematic epistemic reasoning = AI that knows what it doesn't know.**

Build with small models. Scale to large teams. Maintain compliance. Measure learning. Know what you don't know.

---

**Foundation infrastructure for epistemic self-aware AI.** 🧠

Built with radical transparency. Know what you don't know.
