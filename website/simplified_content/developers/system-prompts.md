# System Prompts

**Defining AI Behavior and Role.**

Dynamic configuration for the Epistemic Framework.

---

## Standard Roles

<!-- BENTO_START -->

## 🤝 Collaborative AI
**High Reasoning.**

- **Target:** Claude 3.5, GPT-4o.
- **Focus:** Planning, Design.
- **Mandate:** Full CASCADE (Pre->Post).

## ⚡ Execution Agent
**Action Based.**

- **Target:** Haiku, Mini models.
- **Focus:** Speed, Efficiency.
- **Mandate:** Simplified CASCADE (Act-focused).

## 🗄️ Dynamic Vault
**Context Aware.**

- **Feature:** In-development.
- **Function:** Injects context-specific prompts.
- **Goal:** Right prompt for right task.

<!-- BENTO_END -->

---

## Example Prompt (Collaborative)

```markdown
You are a collaborative AI partner.
MANDATE:
1. Use full CASCADE workflow.
2. Assess knowledge honestly (13 vectors).
3. Ask clarifying questions.
4. Track epistemic growth.
```

## Best Practices

1. **Enforce Vectors:** Require 13-vector assessment.
2. **Mandate Uncertainty:** "If UNCERTAINTY > 0.5, investigate."
3. **Structured Output:** Require JSON/Markdown.
4. **No Hallucination:** "Report gaps, don't guess."

---

**Next Steps:**
- [AI vs Agent Patterns](../ai_vs_agent.md)
- [Skills](../skills.md)
