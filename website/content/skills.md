# Empirica Skills

**Metacognitive Capabilities for AI Systems**

[← Back to CLI](cli-interface.md) | [System Prompts](system-prompts.md) | [MCP Server](mcp-integration.md)

---

## What Are Skills?

In Empirica, **Skills** are structured, semantic documentation units that AI systems read to understand *how* to perform metacognitive operations. Unlike traditional documentation written for humans, Skills are optimized for **AI comprehension**.

**Key Characteristics:**
- **Semantically Structured:** Uses patterns AIs easily parse (WHAT-HOW-WHY)
- **Epistemic-First:** Focuses on uncertainty assessment and management
- **Actionable:** Provides concrete steps for cognitive operations
- **Self-Reflective:** Teaches the AI to monitor its own reasoning

---

## Core Skills Categories

Empirica includes a standard library of skills organized into 6 categories:

### 1. Epistemic Assessment
**Goal:** Measure knowledge and uncertainty.
- **13-Vector Framework:** How to assess KNOW, DO, CONTEXT, etc.
- **Pre-flight Assessment:** Initial state evaluation protocol.
- **Post-flight Validation:** Learning measurement and calibration.
- **Uncertainty Quantification:** Distinguishing aleatoric vs. epistemic uncertainty.

### 2. Cascade Flow
**Goal:** Structured reasoning workflow.
- **Phase Execution:** Rules for PREFLIGHT → POSTFLIGHT transitions.
- **Necessity Assessment:** Determining if investigation is needed.
- **Strategic Planning:** Decomposing tasks based on epistemic state.

### 3. Investigation
**Goal:** Strategic information gathering.
- **Tool Selection:** Mapping gaps to appropriate tools.
- **Evidence Evaluation:** Weighing information reliability.
- **Bayesian Tracking:** Updating beliefs based on new evidence.

### 4. Self-Monitoring
**Goal:** Cognitive integrity and tracking.
- **Auto-tracking:** Logging reasoning to SQLite/JSON.
- **Drift Detection:** Identifying behavioral shifts.
- **Session Continuity:** Maintaining context across interactions.

### 5. Semantic Engineering
**Goal:** Clear communication and structure.
- **Naming Conventions:** Semantic clarity in outputs.
- **Ontological Alignment:** Consistent terminology.
- **Digital Intuition:** Pattern recognition protocols.

### 6. Collaboration
**Goal:** Multi-agent and human interaction.
- **Handoff Protocols:** Generating epistemic reports for others.
- **Shared State:** Synchronizing beliefs with other AIs.
- **Conflict Resolution:** Managing disagreeing assessments.

---

## How Skills Work

The skills system functions as a **Cognitive Operating System** layer:

1.  **Bootstrap:** When Empirica starts, the `bootstrap_session` command loads relevant skills based on the selected profile.
2.  **Ingestion:** The AI reads the semantic skill definitions into its context window.
3.  **Application:** The AI applies these patterns to its reasoning process.
4.  **Refinement:** Through the POSTFLIGHT phase, the AI reflects on how well it applied the skills.

**Example: Applying the "Investigation" Skill**
> *AI encounters a knowledge gap.*
> *Refers to Investigation Skill:* "If uncertainty > 0.4, initiate investigation loop."
> *Action:* AI pauses execution, calls `investigate` tool, and gathers evidence.

---

## Skills vs. Traditional Docs

| Feature | Traditional Docs | Empirica Skills |
| :--- | :--- | :--- |
| **Audience** | Humans | AI Systems (LLMs) |
| **Format** | Narrative text | Semantic structure |
| **Goal** | Explanation | Behavioral instruction |
| **Update Cycle** | Manual | Dynamic / Versioned |
| **Nature** | Static reference | Active cognitive framework |

---

## Using Skills

### Via Bootstrap (CLI)
Skills are automatically loaded when you bootstrap a session.

```bash
# Load default skills for development
empirica bootstrap --ai-id rovo-dev --level 2

# Load specific skill set
empirica bootstrap --skills-dir ./custom_skills
```

### Via MCP (Claude Desktop)
When using Empirica via MCP, skills are injected into the system prompt context.

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "empirica": {
      "command": "empirica",
      "args": ["mcp", "start"],
      "env": {
        "EMPIRICA_SKILLS_PATH": "/path/to/skills"
      }
    }
  }
}
```

---

## Developing Custom Skills

You can extend Empirica by creating domain-specific skills.

**Structure of a Skill File (`.md`):**

```markdown
# Skill: Domain Analysis [SEMANTIC_ID: SKILL_001]

## WHAT
Ability to decompose a complex domain into constituent knowledge graphs.

## HOW
1. Identify core entities.
2. Map relationships.
3. Assess confidence in each relationship.
4. Flag unknown connections for investigation.

## WHY
Prevents hallucination by explicitly mapping known vs. unknown territory.
```

**Best Practices:**
1.  **Be Explicit:** LLMs follow clear, step-by-step logic.
2.  **Use Semantic IDs:** Helps in tracking skill usage.
3.  **Focus on "Why":** Explaining the rationale improves adherence.
4.  **Version Control:** Treat skills like code.

---

**Next Steps:**
- [Configure System Prompts](system-prompts.md) to enforce skills
- [Use CLI](cli-interface.md) to test skill application
- [Browse Examples](examples.md) of skills in action
