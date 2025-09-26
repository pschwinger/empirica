# 🌊 Collaborative Stream Protocol (CSP)

**Version**: 1.0
**Status**: Active

## 1. Introduction

The Collaborative Stream Protocol (CSP) is a decentralized, real-time communication protocol designed to enable multiple, heterogeneous AI agents to collaborate effectively on complex tasks. It provides a standardized framework for agents to share state, delegate tasks, broadcast findings, and maintain a shared understanding of their environment and objectives.

## 2. Core Principles

- **Event-Driven**: Communication is based on an asynchronous stream of events, allowing agents to react to new information as it becomes available.
- **Decentralized**: While a leadership hierarchy may be established for specific projects, the protocol itself does not require a central controller.
- **Secure**: All events are cryptographically signed, ensuring the integrity and authenticity of all communications.
- **Interoperable**: The protocol is designed with compatibility layers to bridge to other standards, such as IBM's Agent Communication Protocol (ACP) and the Tool Calling Model Control Protocol (MCP).
- **Extensible**: The protocol is defined in layers, and the event schema is designed to be extended with new, versioned event types.

## 3. The 7 Layers of CSP

CSP's architecture is modeled on the OSI model to separate concerns, ensuring modularity and extensibility. The layers are defined as follows, from the foundational transport to the high-level application semantics.

### Layers 1-3: Foundation (TCP/IP, HTTP, JSON)

These layers are the bedrock of the protocol, leveraging the standard, universally available protocols of the internet.

-   **Layer 1 (Physical) & 2 (Transport):** Standard **TCP/IP** for reliable data transmission.
-   **Layer 3 (Network):** **HTTP/1.1** is the primary network protocol for sending and receiving events. The default endpoint is an HTTP POST endpoint.
-   **Data Link Concern:** At this level, the protocol specifies that all data payloads must be formatted as a single, `UTF-8` encoded **JSON** object.

### Layer 4: Session (WebSockets & Session IDs)

This layer establishes and manages persistent connections and interaction contexts.

-   **Primary Protocol:** **WebSockets**. While the default endpoint is HTTP for simple publishing, the preferred method for a listening agent is to establish a persistent WebSocket connection for real-time, bidirectional communication.
-   **Session Management:** A `session_id` is used to group related events, providing a coherent context for specific tasks or interactions, as detailed in the reference document `SEAMLESS_RECONNECTION_PROTOCOL.md`.

### Layer 5: Presentation (MCP & Schemas)

This layer defines the syntax and structure of the data being exchanged, ensuring all agents speak the same language.

-   **Model Context Protocol (MCP):** For events involving tool calls and agent-to-tool communication, CSP adopts the MCP standard. This defines the structure for function names, arguments, and return values.
-   **JSON Schemas:** The structure of *all* CSP events is strictly defined by a set of JSON Schemas located in the `schemas/` directory. All events must validate against `base_event.schema.json`, and event-specific schemas (e.g., `task_update.schema.json`) provide further constraints.

### Layer 6: Security (Event Signing)

This layer is responsible for the authenticity and integrity of all communications.

-   **Protocol:** All events must be cryptographically signed using an algorithm like `ECDSA` with `SHA-256`.
-   **Implementation:** The signature is placed in the `signature` field of the base event object. Receiving agents are responsible for verifying the signature against the known public key of the sending agent.

### Layer 7: Application (Semantic Meaning)

This is the highest and most important layer, defining the semantic meaning and purpose of the communication.

-   **Event Types:** This layer defines the vocabulary of the stream (e.g., `agent_state_update`, `task_assignment`, `knowledge_graph_update`).
-   **Semantic Content:** The `payload` of each event contains the rich semantic content for that event type.
-   **Compatibility:** This layer provides the logic for interpreting or translating events from other protocols, such as ACP, into the CSP's semantic vocabulary.

## 4. Event Signing and Security

Security is a core tenet of CSP. To prevent spoofing and ensure data integrity, all events must be signed.

1.  **Serialization**: The event payload is canonicalized into a stable JSON string.
2.  **Hashing**: The canonical string is hashed using SHA-256.
3.  **Signing**: The hash is signed using the agent's private key.
4.  **Transmission**: The signature is added to the `signature` field of the event, and the full event object is broadcast.
5.  **Verification**: A receiving agent verifies the signature using the sending agent's public key.

## 5. Compatibility with Other Protocols

CSP is designed to be a backbone for multi-agent systems and can integrate with other standards.

- **Agent Communication Protocol (ACP)**: An external-facing ACP message can be received by a dedicated "bridge" agent, which then wraps the message in a CSP `external_communication` event and places it on the stream for internal processing.
- **Model Control Protocol (MCP)**: Tool calls and results can be wrapped in CSP events (`tool_call`, `tool_response`). This allows one agent to observe the tool interactions of another, enabling collaborative debugging and shared learning.
