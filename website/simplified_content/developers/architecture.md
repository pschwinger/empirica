# Architecture & Structure

**Understanding Empirica's system design.**

---

## System Layers

<!-- BENTO_START -->

## 🖥️ User Interaction
**The Interface Layer.**

- **CLI:** Command-line operations.
- **MCP Server:** IDE integration.
- **Dashboard:** Real-time monitoring.

## 🧠 Epistemic Framework
**The Core Logic.**

- **Canonical Assessment:** 13 vectors, genuine reasoning.
- **CASCADE Workflow:** 7 phases with investigation loop.
- **Profile System:** Context-aware constraints.

## 💾 Persistence Layer
**The Memory.**

- **SQLite:** Queryable tracking.
- **JSON:** Portable sessions.
- **Git Notes:** Version-controlled checkpoints.

<!-- BENTO_END -->

---

## Core Principles

### 1. No Heuristics
**Genuine Reasoning Only.**
We don't use keyword matching or fake confidence scores. The AI must genuinely assess its own state.

### 2. Temporal Separation
**Reflex Logs.**
Separates current reasoning from historical reasoning to prevent self-referential loops and confabulation.

### 3. Context-Aware Constraints
**Adaptive Profiles.**
- **High Reasoning:** Unlimited investigation (Claude Opus).
- **Autonomous Agent:** Structured, limited rounds (Haiku).
- **Critical Domain:** Strict compliance.

---

## Directory Structure

```
empirica/
├── empirica/                          # Core Python package
│   ├── core/canonical/                # Epistemic Framework
│   ├── core/metacognitive_cascade/    # Workflow Orchestrator
│   ├── config/                        # Profiles
│   └── data/                          # Persistence
├── mcp_local/                         # MCP Server
├── docs/                              # Documentation
└── .empirica/                         # Runtime Data
```

---

**Next Steps:**
- [CLI Interface](cli-interface.md)
- [Components](components.md)
