# AI vs Agent: Understanding the Distinction

**Collaborative vs Acting Intelligence.**

Empirica adapts to different capabilities and roles.

---

## Key Differences

<!-- BENTO_START -->

## 🧠 AI (Collaborative)
**High Autonomy.**

- **Role:** Reasoning partner.
- **Workflow:** Full CASCADE.
- **Examples:** Claude Opus, GPT-4.
- **Best for:** Design, Planning, Complex Tasks.

## ⚡ Agent (Acting)
**Task Focused.**

- **Role:** Executor.
- **Workflow:** Simplified (ACT-focused).
- **Examples:** Haiku, Mini-models.
- **Best for:** Tests, Docs, Simple Fixes.

## 🔄 CASCADE Usage
**Tailored workflows.**

- **AI:** Unlimited investigation, deep reasoning.
- **Agent:** Direct execution, report evidence.

<!-- BENTO_END -->

---

## Patterns

### 1. Solo Work (AI)
Single AI using full CASCADE to plan and execute complex features.

### 2. Delegation (AI + Agents)
Lead AI designs architecture and delegates specific subtasks to Agents.
- **AI:** "Design Auth System"
- **Agent:** "Write Unit Tests"

### 3. Peer Collaboration (Multi-AI)
Multiple high-reasoning AIs collaborating on complex problems with shared epistemic state.

---

## System Prompts

- **AI Prompt:** "You are a collaborative partner... use full CASCADE."
- **Agent Prompt:** "You are an execution agent... focus on completion."

[View System Prompts](developers/system-prompts.md)

---

**Next Steps:**
- [Collaboration](developers/collaboration.md)
- [Architecture](developers/architecture.md)
