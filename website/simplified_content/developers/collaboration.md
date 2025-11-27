# Cross-AI Collaboration

**Seamless workflow across AIs and sessions.**

---

## Key Mechanisms

<!-- BENTO_START -->

## 📍 Git Checkpoints
**Mid-work Resume.**

- **Size:** ~450 tokens.
- **Stored:** Git notes.
- **Use:** Resume exact epistemic state.

## 🤝 Handoff Reports
**Knowledge Transfer.**

- **Size:** ~400 tokens.
- **Stored:** Git + SQLite.
- **Use:** Pass context to next AI.

## 📈 Learning Deltas
**Growth Measurement.**

- **Metric:** Pre vs Post flight.
- **Value:** Validates investigation.
- **Use:** Track AI capability.

<!-- BENTO_END -->

---

## Collaboration Patterns

### 1. Sequential Handoff
**AI -> AI.**
Claude designs -> GPT-4 implements -> Haiku tests.
*98% token savings vs full history.*

### 2. Parallel Collaboration
**Lead AI + Agents.**
Lead AI designs and delegates subtasks to multiple agents running in parallel.

### 3. Specialist Teams
**Domain Experts.**
Security AI + Database AI + UI AI working on shared codebase with synchronized state.

---

## Storage Architecture

1. **SQLite:** Queryable, relational tracking.
2. **JSON:** Portable, exportable sessions.
3. **Git:** Distributed, version-controlled checkpoints.

---

**Next Steps:**
- [AI vs Agent Patterns](../ai_vs_agent.md)
- [Architecture](architecture.md)
