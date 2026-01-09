# Empirica Python API Reference

**Framework Version:** 1.3.0
**Status:** Production Ready

---

## API Categories

### [Core Session Management](core_session_management.md)
- **SessionDatabase** - Central database for all session data
- **Session creation, retrieval, and management**
- **Epistemic vector storage and retrieval**

### [Goals & Tasks](goals_tasks.md)
- **GoalRepository** - Goal creation, tracking, and completion
- **Subtask management** - Task breakdown and progress tracking
- **Goal-tree operations** - Hierarchical goal management

### [CASCADE Workflow](cascade_workflow.md)
- **Cascade execution** - Reasoning cascade management
- **Epistemic assessment** - Preflight, Check, Postflight phases
- **Reflex logging** - Epistemic state capture

### [Project Management](project_management.md)
- **ProjectRepository** - Project lifecycle management
- **Handoff reports** - AI-to-AI handoff documentation
- **Project tracking** - Cross-session project management

### [Investigation Tools](investigation_tools.md)
- **Branch management** - Investigation branch operations
- **Tool execution tracking** - Investigation tool usage
- **Merge decisions** - Branch comparison and selection

### [Epistemic Tracking](epistemic_tracking.md)
- **Epistemic snapshots** - Point-in-time state capture
- **Bayesian beliefs** - Belief evolution tracking
- **Divergence monitoring** - Delegate-trustee alignment

### [Knowledge Management](knowledge_management.md)
- **BreadcrumbRepository** - Findings, unknowns, dead-ends
- **Epistemic sources** - Source attribution and confidence
- **Reference documents** - Project documentation links

### [Memory & Search](memory_search.md)
- **QdrantMemory** - Vector search for semantic retrieval
- **EmbeddingProvider** - Multi-provider embeddings (Jina, Voyage, Ollama, OpenAI)
- **Lessons System** - Cold storage procedural knowledge

### [System Utilities](system_utilities.md)
- **BranchMapping** - Git branch to goal mapping
- **DocCodeIntegrity** - Documentation-code integrity checking
- **Migration tools** - Schema evolution utilities

---

## API Philosophy

**AI-First Design:** All APIs designed for autonomous AI agent usage with structured return values and comprehensive error handling.

**Epistemic Self-Awareness:** APIs capture and track epistemic state throughout all operations.

**Modular Architecture:** APIs organized in logical modules that can be used independently while maintaining consistency.

**Four-Layer Storage:** Data flows through SQLite (hot), Git Notes (warm), JSON Logs (audit), and Qdrant (search).

---

## Getting Started

For new users, start with:
1. [Core Session Management](core_session_management.md) - Essential session operations
2. [CASCADE Workflow](cascade_workflow.md) - Core reasoning workflow
3. [Goals & Tasks](goals_tasks.md) - Task management operations

---

**Total Modules:** 9 categories
**API Stability:** Production ready
