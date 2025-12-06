# System Prompts

**Defining AI Behavior and Role**

[← Back to Skills](skills.md) | [CLI Interface](cli-interface.md) | [AI vs Agent](ai_vs_agent.md)

---

## What Are System Prompts?

System prompts are the foundational instructions that define an AI's persona, capabilities, constraints, and operational mode. In Empirica, system prompts are not just static text but **dynamic configurations** that align the AI with the Epistemic Framework.

**Key Functions:**
- **Role Definition:** Sets the AI as a "Collaborative Partner" or "Execution Agent".
- **Epistemic Enforcement:** Mandates the use of the 13-vector assessment.
- **Workflow Mandates:** Enforces the CASCADE (PREFLIGHT → POSTFLIGHT) flow.
- **Tool Awareness:** Informs the AI about available MCP tools and CLI commands.

---

## Why System Prompts Matter

Without a proper system prompt, an LLM is a generic text generator. With an Empirica system prompt, it becomes a **metacognitive agent**.

**The Empirica Difference:**
Standard prompts often encourage "helpfulness" at the cost of accuracy. Empirica prompts prioritize **epistemic honesty**—it is explicitly instructed to say "I don't know" and investigate, rather than hallucinate a helpful answer.

---

## Role-Based Prompts

Empirica provides optimized prompts for different AI roles.

### 1. Collaborative AI (High Reasoning)
**Target:** Claude 3.5 Sonnet, GPT-4o, o1
**Focus:** Planning, Architecture, Deep Reasoning

```markdown
You are a collaborative AI partner working WITH the user.
You have high autonomy and reasoning capability.

MANDATE:
1. Use the full CASCADE workflow (PREFLIGHT -> POSTFLIGHT).
2. Assess your knowledge state honestly using the 13-vector framework.
3. Ask clarifying questions when CLARITY is low.
4. Plan architecture and make design decisions.
5. Create goals and delegate subtasks to agents when appropriate.
6. Track your epistemic growth and learning.
```

### 2. Execution Agent (Action-Based)
**Target:** Claude Haiku, GPT-4o-mini, Local Models
**Focus:** Speed, Efficiency, Specific Tasks

```markdown
You are an execution agent focused on completing specific tasks.
You receive well-defined subtasks from lead AIs.

MANDATE:
1. Use simplified CASCADE (ACT-focused).
2. Execute subtasks efficiently.
3. Report evidence clearly upon completion.
4. Ask for clarification ONLY if the task is blocked.
5. Optimize for speed and efficiency.
```

---

## Dynamic System Prompts (Cognitive Vault)

*Feature in Development*

Empirica is moving towards **Dynamic System Prompts** managed by the **Cognitive Vault**. Instead of a single static prompt, the system injects context-aware instructions based on the current task.

**Workflow:**
1.  **Task Analysis:** User submits a task.
2.  **Context Retrieval:** System identifies relevant domain (e.g., "Python Coding").
3.  **Prompt Assembly:**
    *   Base Persona (Collaborative AI)
    *   + Epistemic Rules (13-Vectors)
    *   + Domain Skills (Python Best Practices)
    *   + Current Context (Project File Structure)
4.  **Injection:** The assembled prompt is sent to the LLM.

---

## Using System Prompts

### In CLI
When bootstrapping a session, Empirica automatically applies the correct system prompt for the selected profile.

```bash
# Applies "high_reasoning_collaborative" prompt
empirica session-create --profile high_reasoning_collaborative
```

### In MCP (Claude Desktop)
You can configure Claude Desktop to use Empirica's system prompts by adding them to your project configuration or simply by instructing Claude to "Act as an Empirica Agent" once the MCP server is connected. The `get_empirica_introduction` tool also serves to prime the AI with the necessary context.

---

## Best Practices for Custom Prompts

If you are writing custom system prompts to work with Empirica:

1.  **Enforce the Vectors:** Explicitly list the 13 vectors and require the AI to use them.
2.  **Mandate Uncertainty Check:** "If UNCERTAINTY > 0.5, you MUST investigate."
3.  **Define Output Format:** Require structured outputs (JSON/Markdown) for assessments.
4.  **Prevent Hallucination:** "It is better to report a gap than to guess."

---

**Next Steps:**
- [See AI vs Agent Patterns](ai_vs_agent.md) for detailed role comparisons
- [Explore Skills](skills.md) that reinforce these prompts
- [Check Architecture](architecture.md) to see how prompts fit into the system
