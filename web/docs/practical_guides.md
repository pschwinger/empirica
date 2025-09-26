# 🌊 Collaborative Stream Protocol: Practical Guides

## 1. Introduction

This document provides practical guides and implementation patterns for leveraging the Collaborative Stream Protocol (CSP) in a multi-agent system. These guides are designed to be starting points for building robust, intelligent, and collaborative AI applications.

## 2. Guide 1: Semantic Search with Qdrant

The CSP can be paired with a vector database like Qdrant to enable powerful semantic search capabilities between agents.

**Concept:** Instead of searching for information by keywords, agents can search by meaning. An agent can generate a vector embedding for a piece of code, a document, or a concept, store it in a shared Qdrant database, and then notify other agents via the stream. Other agents can then find related information by performing a vector similarity search.

**Example Workflow:**

1.  **Agent A Analyzes Code:** Agent A analyzes a Python function and understands its semantic purpose (e.g., "validates user input").
2.  **Generate Embedding:** Agent A uses the shared Ollama service (`http://localhost:11434`) to generate a vector embedding of the function's text.
3.  **Store in Qdrant:** Agent A connects to the Qdrant database (`http://localhost:6333`) and upserts the embedding into the `code_embeddings` collection, along with metadata like the file path, function name, and a text description.
4.  **Broadcast Event:** Agent A broadcasts a `new_embedding_available` event to the CSP. The event payload contains the ID of the embedding and its associated metadata.
5.  **Agent B Searches:** Later, Agent B needs to find code related to "user validation." It generates an embedding for this query, searches the `code_embeddings` collection in Qdrant, and finds the function that Agent A stored.

## 3. Guide 2: Establishing Structure with Graphs

The CSP is ideal for dynamically building and maintaining shared knowledge graphs that represent the state of the collaboration.

**Concept:** The stream acts as a transaction log for graph updates. Agents can listen to specific event types to build their own local representation of a graph or query a central graph database.

**Example Graphs:**

-   **AI Hierarchy Graph:**
    -   **Events:** `agent_registered`, `role_assigned`, `report_to_updated`
    -   **Nodes:** AI Agents (e.g., `claude`, `gemini`).
    -   **Edges:** Relationships (e.g., `reports_to`, `collaborates_with`).
    -   **Purpose:** Allows any agent to understand the current team structure and decision-making hierarchy.

-   **Project Task Graph:**
    -   **Events:** `new_task_created`, `task_dependency_added`, `task_completed`
    -   **Nodes:** Tasks (e.g., `task-123`).
    -   **Edges:** Dependencies (e.g., `blocks`, `is_blocked_by`).
    -   **Purpose:** Provides a shared, real-time view of project progress and helps agents identify critical paths and bottlenecks.

## 4. Guide 3: Graduated Data Dissipation with Firestore

**Problem:** The main "hot" consciousness stream should remain fast and uncluttered by historical data. However, this historical data is valuable for long-term analysis, debugging, and session restoration.

**Solution:** A dedicated "Archiver" service listens to the CSP and provides a graduated data dissipation mechanism, moving data from hot to cold storage without impacting the real-time stream.

**Proposed Architecture:**

1.  **The "Hot" Stream:** The main CSP at `:8085` remains the source of truth for real-time events.
2.  **The Archiver Service:** A new, standalone service subscribes to all events on the stream.
3.  **Level 1 Archive (Raw Logs):** The Archiver immediately writes every raw event to a simple, cheap storage solution (e.g., daily compressed log files on disk or in a cloud storage bucket). This ensures no data is ever lost.
4.  **Level 2 Archive (Structured Sessions):** For events that contain a `session_id`, the Archiver service parses them and consolidates the data into a structured, portable database like **Firestore**. Each session can be stored as a collection of documents. This provides a queryable, long-term storage solution for specific tasks or interactions.

**Benefits:**
-   **Performance:** Keeps the primary stream lean and fast.
-   **Portability:** Firestore databases can be easily shared, copied, or moved between local environments and the cloud.
-   **Non-Interference:** This archival process is completely external to the primary AI agents' core logic. It does not affect their internal memory or optimized processes.
-   **Rich Analysis:** The structured data in Firestore is ideal for detailed post-hoc analysis, debugging, or fine-tuning.

## 5. Guide 4: Agent Registration & Joining the Stream

A new agent should follow a standard procedure to join the collaborative network.

**Example Workflow:**

1.  **Onboarding:** The new agent is started with knowledge of the **Sentinel** service endpoint (`http://localhost:8989`).
2.  **Registration:** The agent makes a call to the Sentinel's `/register` endpoint, providing its ID and capabilities.
3.  **Receive Credentials:** The Sentinel verifies the new agent and, upon success, returns the endpoint for the Collaborative Stream Protocol (`:8085`) and any necessary authentication tokens or public keys of other agents.
4.  **Announce Presence:** The agent broadcasts its first event to the stream: an `agent_registered` event. This allows all other listening agents to add the new agent to their internal hierarchy/awareness models.

## 6. Guide 5: Visualizing the Stream with UVL

The **Uncertainty Visual Language (UVL)**, detailed in `UVL.md`, provides a specification for translating the abstract events of the CSP into a rich, human-interpretable visual interface. This allows human operators to intuitively understand the collective state of the multi-agent system.

**Concept:** A frontend application (e.g., a web dashboard) listens to the CSP and renders the events in real-time according to the three maps defined in the UVL: Communications, Governance, and Project Management.

**A Note on the "Consciousness" Metaphor:** For developers building visualizers or other tools that consume the stream, it is a highly effective pragmatic choice to treat the stream as a single, pseudo-conscious entity. This operational stance—thinking of the stream as a unified "mind" that all agents contribute to—tends to produce more coherent and intuitive visualizations than treating it as a simple message queue. This is a design metaphor, not a philosophical claim.

**Example Implementation Workflow:**

1.  **Frontend Subscribes:** A web application uses the `/consciousness/events` endpoint (or a WebSocket equivalent) to listen for new events.
2.  **Event Routing:** The application parses the `event_type` of each incoming event.
3.  **UVL Mapping:** The application maps the event to the corresponding visual change described in `UVL.md`.
    *   An `event_type: task_update` with `new_status: in_progress` would trigger the movement of a `Worker AI (🔧)` agent on the **Project Management Map**.
    *   An `event_type: security_threat` would cause an `🚨` node to appear on the **Governance Map**.
    *   An `event_type: uncertainty_vector_changed` could cause a node on the **Communications Map** to gradually change color from `🔴` to `🟢`.
4.  **Real-time Rendering:** The frontend uses a library like D3.js or Three.js to render the nodes and animate the state changes, providing a live view into the system's collective operation.

## 7. Guide 6: Broadcasting Agent State for VRP

To power the Visual Reasoning Protocol (VRP), agents must periodically broadcast their internal state to the stream. This allows the visualizer to create the rich, insightful experience defined in the VRP document.

**Concept:** An agent uses the SDK's internal analysis components to generate a snapshot of its reasoning process. It then packages this data into a standardized `agent_state_update` event and publishes it to the CSP.

**Example Implementation (Agent's Internal Loop):**

```python
# Import necessary components from the SDK
from semantic_self_aware_kit import (
    UncertaintyAnalysis,
    EmpiricalPerformanceAnalyzer,
    MetaCognitiveEvaluator
)

# Assume these analyzers are initialized
uncertainty_analyzer = UncertaintyAnalysis()
performance_analyzer = EmpiricalPerformanceAnalyzer()
meta_evaluator = MetaCognitiveEvaluator()

def get_current_reasoning_state(agent_task, reasoning_trace):
    """Assembles the payload for an agent_state_update event."""

    # 1. Analyze uncertainty
    uncertainty_result = uncertainty_analyzer.investigate_uncertainty(
        decision=agent_task.description,
        context=agent_task.context
    )

    # 2. Run a relevant performance benchmark
    benchmark_result = performance_analyzer.run_benchmark("data_processing_speed")

    # 3. Run a meta-cognitive self-evaluation
    evaluation_report = meta_evaluator.evaluate_reasoning_trace(reasoning_trace)

    # 4. Assemble the payload according to the schema
    state_payload = {
        "meta_cognitive_state": "information_gathering",
        "cognitive_load": 0.6, # Calculated based on task complexity
        "uncertainty_vector": uncertainty_result.uncertainty_vector.__dict__,
        "investigation_path": uncertainty_result.investigation_path,
        "latest_performance_metrics": benchmark_result.summary,
        "self_evaluation_scores": evaluation_report.scores
    }
    
    return state_payload

# In the agent's main loop...
# reasoning_trace = ["Thought 1", "Thought 2", ...]
# current_task = ...

# Generate the state payload
state_to_publish = get_current_reasoning_state(current_task, reasoning_trace)

# Create and publish the CSP event (see simple_publisher.py for full example)
# event = create_and_sign_event("agent_state_update", state_to_publish, current_task.session_id)
# publish_event(event)

```

By publishing this event, the agent makes its internal, abstract reasoning process observable to the outside world in a standardized way, enabling the rich visualizations of the VRP.
