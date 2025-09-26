# 🧠 Visual Reasoning Protocol (VRP)

**Version**: 1.0
**Extends**: [Uncertainty Visual Language (UVL)](UVL.md)

## 1. Introduction

The Visual Reasoning Protocol (VRP) is a specification for visualizing the internal reasoning, meta-cognitive processes, and information flow of AI agents within the Collaborative Stream Protocol (CSP). It extends the UVL by adding graphical layers that represent the *quality*, *content*, and *process* of an agent's thinking, not just the outcome.

Its purpose is to make an AI's decision-making process transparent, interpretable, and debuggable for a human operator.

## 2. Concept 1: Dynamic Edge Modifiers

Edges (the paths between nodes) are no longer simple connectors. They are dynamic conduits that visualize the nature of the information flowing through them.

### 2.1. Information Type (Path Color & Pattern)

The visual style of the path indicates the type of data being transferred:

-   **Solid Blue Line (`───`):** Raw data, text, or simple instructions.
-   **Dashed Purple Line (`- - -`):** Vector embeddings, semantic concepts, or knowledge graph fragments.
-   **Dotted Green Line (`· · ·`):** Code snippets, file content, or diffs.
-   **Glowing Red Line:** Security warnings, error codes, or exception data.

### 2.2. Information Confidence (Path Stability)

The shape and animation of the path indicate the confidence or certainty associated with the information.

-   **Stable, Straight Path:** High-confidence, verified information or a direct command.
-   **Wavy/Shimmering Path:** Low-confidence information, a hypothesis, a query, or a high-uncertainty statement.

## 3. Concept 2: The Introspection View

Clicking on any active AI Agent node opens a detailed **Introspection View**, providing a real-time window into the agent's mind. This view is populated by the `agent_state_update` event and visualizes data from the SDK's various analytical components.

### 3.1. The "Why": Uncertainty Vector Radar Chart

This chart visualizes the agent's current uncertainty profile, answering *why* it is behaving a certain way.

-   **Source Component**: `UncertaintyAnalysis`
-   **Visualization**: A hexagonal radar chart displaying the `uncertainty_vector` data.
-   **Interpretation**: A spike on an axis provides an immediate, intuitive explanation. For example, a high **Epistemic** spike means "I don't have enough information."

### 3.2. The "How": Investigation Path Log

This is a step-by-step log of the agent's reasoning process.

-   **Source Component**: `UncertaintyAnalysis`
-   **Visualization**: An ordered list displaying the `investigation_path` data.
-   **Interpretation**: Shows the user the logical path the AI is following to solve a problem or reduce uncertainty.

### 3.3. Performance Snapshot

This section displays the agent's operational efficiency related to its current task.

-   **Source Component**: `EmpiricalPerformanceAnalyzer`
-   **Visualization**: A small table or a set of gauges displaying the `latest_performance_metrics` data.
-   **Interpretation**: Provides concrete data on performance, showing metrics like `execution_time_seconds` and `success_rate` for the most recent relevant benchmark.

### 3.4. Meta-Cognitive Scorecard

This section displays the results of the agent's latest self-evaluation, showing how well its reasoning aligns with core principles.

-   **Source Component**: `MetaCognitiveEvaluator`
-   **Visualization**: A bar chart displaying the `self_evaluation_scores`.
-   **Interpretation**: Gives insight into the quality of the agent's reasoning, with scores for `LOGICAL_CONSISTENCY`, `UNCERTAINTY_RESOLUTION`, `EMPIRICAL_GROUNDING`, etc.

## 4. Concept 3: Agent State Modifiers

Temporary emoji decorators are overlaid on an agent's primary emoji to signify its current meta-cognitive state.

-   **🔄 Recursive Analysis:** The agent is analyzing its own code, performance, or past actions. Triggered by internal recursive loops.
-   **💭 Self-Evaluation:** The agent is performing a high-level evaluation of a new task, its own capabilities, or its current strategy. Triggered when presented with a complex, novel problem.
-   **🧠 High Cognitive Load:** The agent is executing a task with a high complexity score (e.g., analyzing a large codebase via AST). This indicates intensive processing.
-   **✨ Flow State:** The agent is operating with high efficiency and low uncertainty. This is the default state for optimal performance.

## 5. Example Scenario in Practice

1.  **Task Arrival:** A human operator gives a complex task: "Refactor the authentication service to use a new encryption standard." The **Lead AI (🤖)** node immediately gains a **💭** modifier.
2.  **Initial Evaluation:** A user clicks the agent. The **Introspection View** shows a **Radar Chart** with large spikes in the **Epistemic** (I don't know this standard) and **Causal** (I don't know the impact of this change) dimensions.
3.  **Information Gathering:** The Lead AI dispatches two queries:
    -   A **wavy, solid blue** line to a Web Search agent: "What is the FIDO2 encryption standard?"
    -   A **wavy, dotted green** line to a Code Analysis agent: "Analyze dependencies of the authentication service."
4.  **Cognitive Load:** As the Code Analysis agent works, its node shows a **🧠** modifier.
5.  **Response & Planning:** The agents respond with stable, straight-line paths. The Lead AI's **💭** modifier disappears. Its internal state now has a lower uncertainty vector and a populated Investigation Path.
6.  **Execution:** The Lead AI begins generating code. As it does, it may briefly show the **🔄** modifier as it recursively validates its own output before committing it.
