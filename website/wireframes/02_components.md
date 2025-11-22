# Components Page Wireframe

## Page: /components.html

### Purpose
Showcase the modular architecture and component ecosystem of Empirica.

---

## Content Structure

### Hero Section
**Headline:** Build with Thoughtful Components  
**Subheadline:** Empirica provides a complete toolkit for building epistemically-aware AI systems.

---

### Section 1: Component Overview
**Content:**
Empirica's architecture is built from modular, composable components organized into six categories:

---

### Section 2: Core System Components

**Bootstrap System**
- `optimal_metacognitive_bootstrap.py` - Primary initialization with full epistemic tracking
- `extended_metacognitive_bootstrap.py` - Extended configuration options
- **Purpose:** Initialize Empirica with proper database, session tracking, and vector monitoring

**Session Management**
- `session_manager.py` - Handle session lifecycle
- `session_json_handler.py` - Export sessions to JSON for analysis
- **Purpose:** Track AI work sessions with full epistemic state

**Database Layer**
- `empirica_db.py` - SQLite storage for epistemic data
- Schema: sessions, reflex_frames, investigations, drift_events
- **Purpose:** Persistent storage of all epistemic tracking data

---

### Section 3: Epistemic Assessment Components

**Cascade System** 
- `cascade_controller.py` - Orchestrate multi-phase epistemic analysis
- `cascade_phases/` - Phase 1-4 implementations
- **Purpose:** Progressive uncertainty reduction through investigation

**Bayesian Guardian**
- `bayesian_guardian.py` - Probabilistic belief updating
- Bayesian inference for uncertainty quantification
- **Purpose:** Rigorous statistical foundation for confidence levels

**Drift Monitor**
- `drift_monitor.py` - Detect epistemic state changes
- Track vector evolution over time
- **Purpose:** Alert when assumptions become invalid

**13th Vector Detector**
- `explicit_uncertainty_detector.py` - Recognize meta-uncertainty
- Trigger investigation when needed
- **Purpose:** Catch "I don't know enough to proceed" moments

---

### Section 4: Analysis & Monitoring

**Cognitive Benchmarking**
- `cognitive_benchmarking/` - Performance assessment
- `llm_assessment.py` - Evaluate reasoning quality
- **Purpose:** Measure epistemic awareness effectiveness

**Dashboard**
- Real-time epistemic vector visualization
- Session timeline and investigation tracking
- **Purpose:** Monitor AI reasoning as it happens

---

### Section 5: Integration Components

**MCP Server**
- `empirica_mcp_server.py` - Model Context Protocol integration
- Skills-based interface for Claude, Copilot, etc.
- **Purpose:** Seamless integration with modern AI toolchains

**CLI Interface**
- `empirica_cli.py` - Command-line tooling
- Session replay, investigation analysis
- **Purpose:** Developer workflow integration

**Plugin System**
- `plugin_manager.py` - Extensible architecture
- Custom epistemic assessors
- **Purpose:** Customize Empirica for domain-specific needs

---

### Section 6: Skills & Utilities

**Skills Library**
- `docs/empirica_skills/` - Reusable epistemic patterns
- `advanced_investigation.md` - Deep analysis strategies
- `cascade_orchestration.md` - Multi-phase workflows
- **Purpose:** Best practices and proven patterns

**Utilities**
- `utils/` - Helper functions
- `semantic_toolkit.py` - Language processing
- **Purpose:** Common functionality across components

---

### Call-to-Action
- Link to API Reference for technical details
- Link to Getting Started for integration guide
- Link to Docs for component documentation
