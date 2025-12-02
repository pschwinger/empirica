# Empirica Canonical Directory Structure v2.0

**Last Updated:** 2025-01-XX  
**Status:** Current, matches actual codebase  
**Purpose:** Source of truth for codebase organization

---

## Overview

Empirica is organized into clear functional layers:
1. **Core** - Fundamental CASCADE, storage, orchestration
2. **CLI/MCP** - User interfaces (command-line and MCP server)
3. **Components** - Optional capabilities (tool management, validation, etc.)
4. **Plugins** - Extensible features (modality switching, etc.)
5. **Data** - Persistence layer (SQLite, JSON, Git)

---

## Top-Level Structure

```
empirica/
├── empirica/              # Main package
│   ├── core/              # Core CASCADE & orchestration
│   ├── cli/               # Command-line interface
│   ├── data/              # Persistence layer
│   ├── components/        # Optional capabilities
│   ├── plugins/           # Extensible features
│   ├── config/            # Configuration files & loaders
│   ├── calibration/       # Epistemic calibration systems
│   ├── investigation/     # Investigation strategies
│   ├── integration/       # External system hooks
│   ├── metrics/           # Performance tracking
│   ├── dashboard/         # Monitoring UI
│   ├── utils/             # Utilities
│   └── bootstraps/        # Session initialization
│
├── docs/                  # Documentation (30 files target)
├── tests/                 # Test suite
├── examples/              # Usage examples
├── mcp_local/             # MCP server implementation
├── scripts/               # Helper scripts
└── website/               # User-facing site

53 directories, 187 files
```

---

## Core Layer (`empirica/core/`)

**Purpose:** Fundamental CASCADE workflow, storage, and orchestration

```
core/
├── canonical/                          # Core workflow classes
│   ├── canonical_epistemic_assessment.py   # Epistemic vector assessment
│   ├── canonical_goal_orchestrator.py      # Goal/task management
│   ├── goal_orchestrator_bridge.py         # Legacy compatibility
│   ├── reflex_frame.py                     # Temporal state capture
│   ├── reflex_logger.py                    # Workflow logging
│   ├── git_enhanced_reflex_logger.py       # Git-integrated logging
│   └── empirica_git/                       # Git notes integration ⭐
│       ├── checkpoint_manager.py           # PREFLIGHT/CHECK/POSTFLIGHT → git notes
│       ├── goal_store.py                   # Goals → git notes (cross-AI)
│       ├── session_sync.py                 # Session metadata → git notes
│       └── sentinel_hooks.py               # Cognitive vault integration
│
├── metacognitive_cascade/              # CASCADE workflow engine
│   ├── metacognitive_cascade.py            # Main CASCADE class
│   ├── investigation_strategy.py           # Investigation patterns
│   └── investigation_plugin.py             # Pluggable investigation
│
├── drift/                              # Drift detection ⭐ NEW
│   └── mirror_drift_monitor.py             # Temporal self-validation (NO HEURISTICS)
│
├── schemas/                            # Data schemas
│   ├── epistemic_assessment.py             # 13-vector schema
│   └── assessment_converters.py            # Legacy format conversion
│
├── goals/                              # Goal orchestration
│   ├── types.py                            # Goal/task types
│   ├── repository.py                       # Goal storage & querying
│   ├── decision_logic.py                   # Goal routing logic
│   └── validation.py                       # Goal validation
│
├── tasks/                              # Task management
│   ├── types.py                            # Task types
│   └── repository.py                       # Task storage
│
├── completion/                         # Completion tracking
│   ├── tracker.py                          # Completion state
│   ├── git_query.py                        # Query git for completion
│   └── types.py                            # Completion types
│
├── handoff/                            # Session continuity
│   ├── report_generator.py                 # Epistemic handoff reports
│   ├── auto_generator.py                   # Auto-generate handoffs
│   └── storage.py                          # Handoff persistence
│
├── identity/                           # AI identity & signatures
│   ├── ai_identity.py                      # Ed25519 identity management
│   └── signature.py                        # Session signing (Phase 2)
│
├── persona/                            # Persona system
│   ├── persona_profile.py                  # Persona definitions
│   ├── persona_manager.py                  # Persona loading
│   ├── validation.py                       # Schema validation
│   ├── schemas/                            # JSON schemas
│   ├── templates/                          # Persona templates
│   ├── harness/                            # Persona execution
│   │   ├── persona_harness.py              # Orchestrator wrapper
│   │   └── communication.py                # Inter-persona comms
│   └── sentinel/                           # Cognitive routing
│       ├── sentinel_orchestrator.py        # Route based on epistemic state
│       ├── arbitration_strategies.py       # Conflict resolution
│       └── composition_strategies.py       # Persona composition
│
├── metacognition_12d_monitor/          # 12D self-awareness (experimental)
│   ├── metacognition_12d_monitor.py        # Monitor implementation
│   ├── twelve_vector_self_awareness.py     # 12-vector system
│   └── enhanced_uvl_protocol.py            # UVL protocol implementation
│
├── epistemic_bus.py                    # Event bus for epistemic updates
└── thresholds.py                       # Default threshold values
```

---

## Key Architectural Changes

### ⭐ NEW: Unified Drift Monitor

**Old (deprecated):**
- `empirica/calibration/parallel_reasoning.py` - `DriftMonitor` class (used heuristics)
- `empirica/calibration/adaptive_uncertainty_calibration/bayesian_belief_tracker.py` (complex)

**New (current):**
- `empirica/core/drift/mirror_drift_monitor.py` - `MirrorDriftMonitor` class
  - NO HEURISTICS
  - Temporal self-validation only
  - Compares current state to git checkpoint history
  - Principle: Increases expected (learning), decreases are drift (corruption)

**Status:** CASCADE still imports old `DriftMonitor` - needs migration

---

### ⭐ Git Notes Integration (`empirica/core/canonical/empirica_git/`)

**Architecture:**
```
Git Repository
│
├── Code (normal commits)
│   └── Your source code
│
└── Git Notes (Empirica metadata)
    ├── refs/notes/empirica/checkpoints/<commit-hash>
    │   └── {session, ai, phase, vectors, metadata}
    │
    ├── refs/notes/empirica/goals/<goal-id>
    │   └── {objective, subtasks, epistemic_state, lineage}
    │
    ├── refs/notes/empirica/session/<session-id>
    │   └── {ai_id, started, status}
    │
    └── refs/notes/empirica/tasks/<task-id>
        └── {task metadata}
```

**Benefits:**
- Cross-AI coordination (discover goals from other AIs)
- Version controlled (full audit trail)
- ~85% token compression (~3K → ~450)
- Distributed (git pull gets updates)

**Files:**
- `checkpoint_manager.py` - Creates checkpoints on PREFLIGHT/CHECK/POSTFLIGHT
- `goal_store.py` - Stores/discovers goals for cross-AI work
- `session_sync.py` - Syncs session metadata
- `sentinel_hooks.py` - Cognitive vault integration

---

## CLI Layer (`empirica/cli/`)

**Purpose:** Command-line interface for all Empirica features

```
cli/
├── cli_core.py                         # Main CLI entry point
├── cli_utils.py                        # CLI helper functions
├── mcp_client.py                       # MCP client for testing
├── simple_session_server.py            # Lightweight MCP server
├── uvl_formatter.py                    # UVL protocol formatting
│
└── command_handlers/                   # Command implementations
    ├── bootstrap_commands.py           # Session initialization
    ├── session_commands.py             # Session management
    ├── assessment_commands.py          # PREFLIGHT/CHECK/POSTFLIGHT
    ├── cascade_commands.py             # CASCADE execution
    ├── goal_commands.py                # Goal CRUD operations
    ├── goal_discovery_commands.py      # Cross-AI goal discovery ⭐
    ├── checkpoint_commands.py          # Git checkpoint management ⭐
    ├── handoff_commands.py             # Epistemic handoffs
    ├── identity_commands.py            # AI identity management
    ├── investigation_commands.py       # Investigation strategies
    ├── workflow_commands.py            # Complete workflows
    ├── monitor_commands.py             # Drift monitoring
    ├── performance_commands.py         # Performance metrics
    ├── modality_commands.py            # Modality switching
    ├── component_commands.py           # Component management
    ├── config_commands.py              # Configuration
    ├── decision_commands.py            # Decision logging
    ├── action_commands.py              # Action logging
    ├── utility_commands.py             # Utilities
    ├── mcp_commands.py                 # MCP server control
    ├── onboard_handler.py              # Interactive onboarding
    ├── ask_handler.py                  # Q&A mode
    └── chat_handler.py                 # Chat interface
```

**23 MCP Tools** exposed via these handlers (see docs/reference/mcp-tools.md)

---

## Data Layer (`empirica/data/`)

**Purpose:** Multi-layer persistence (SQLite + JSON + Git)

```
data/
├── session_database.py                 # SQLite database (sessions, vectors)
└── session_json_handler.py             # JSON logs (detailed workflow)
```

**Storage Layers:**
1. **SQLite** (`.empirica/sessions/sessions.db`) - Session metadata, vectors, queries
2. **JSON Logs** (`.empirica_reflex_logs/`) - Detailed temporal logs
3. **Git Notes** (`refs/notes/empirica/`) - Compressed checkpoints, cross-AI coordination

**Why three layers?**
- SQLite: Fast queries, structured data
- JSON: Full fidelity, temporal replay
- Git: Cross-AI, version controlled, compressed

---

## Components Layer (`empirica/components/`)

**Purpose:** Optional capabilities (enable as needed)

```
components/
├── tool_management/                    # Tool selection & management
│   ├── tool_management.py              # Base tool manager
│   ├── epistemic_tool_selector_minimal.py  # Tool routing
│   ├── meta_mcp_registry.py            # MCP tool registry
│   ├── enhanced_bash_tools.py          # Bash execution
│   └── enhanced_file_tools.py          # File operations
│
├── code_intelligence_analyzer/         # Code analysis
├── context_validation/                 # Context checking
├── empirical_performance_analyzer/     # Performance tracking
├── environment_stabilization/          # Environment monitoring
├── intelligent_navigation/             # Workspace navigation
├── procedural_analysis/                # Process analysis
├── runtime_validation/                 # Runtime checks
├── security_monitoring/                # Security audits
└── workspace_awareness/                # Workspace understanding
```

**Status:** Most components are optional/experimental. Core workflow doesn't require them.

---

## Plugins Layer (`empirica/plugins/`)

**Purpose:** Extensible features (completely optional)

```
plugins/
├── base_plugin.py                      # Plugin base class
├── dashboard_spawner.py                # Dashboard launcher
│
└── modality_switcher/                  # Route tasks to specialized AIs
    ├── modality_switcher.py            # Main plugin
    ├── epistemic_router.py             # Route based on vectors
    ├── epistemic_snapshot.py           # Capture epistemic state
    ├── epistemic_extractor.py          # Extract from thinking
    ├── genuine_self_assessment.py      # Self-assessment without heuristics
    ├── domain_vectors.py               # Domain-specific vectors
    ├── thinking_analyzer.py            # Parse AI thinking
    ├── snapshot_provider.py            # Snapshot API
    ├── usage_monitor.py                # Track routing decisions
    ├── plugin_registry.py              # Plugin discovery
    ├── register_adapters.py            # Adapter registration
    ├── config_loader.py                # Configuration
    ├── auth_manager.py                 # API authentication
    │
    ├── adapters/                       # AI platform adapters
    │   ├── copilot_adapter.py          # GitHub Copilot
    │   ├── gemini_adapter.py           # Google Gemini
    │   ├── minimax_adapter.py          # Minimax
    │   ├── openrouter_adapter.py       # OpenRouter
    │   ├── qodo_adapter.py             # Qodo
    │   ├── qwen_adapter.py             # Qwen
    │   └── rovodev_adapter.py          # RovoDev
    │
    └── domain_vectors_custom/          # Custom domain vectors
        └── example_chemistry.py        # Example custom domain
```

---

## Calibration Layer (`empirica/calibration/`)

**Purpose:** Epistemic calibration systems (being refactored)

```
calibration/
├── parallel_reasoning.py               # OLD: ParallelReasoningSystem (deprecated)
│   └── DriftMonitor class              # ⚠️ DEPRECATED - use MirrorDriftMonitor
│
└── adaptive_uncertainty_calibration/   # OLD: Bayesian tracking (deprecated)
    ├── adaptive_uncertainty_calibration.py
    └── bayesian_belief_tracker.py      # ⚠️ DEPRECATED - contained heuristics
```

**Status:** Being replaced by `core/drift/mirror_drift_monitor.py` (no heuristics)

**Migration needed:** Update CASCADE to use `MirrorDriftMonitor` instead of `DriftMonitor`

---

## Configuration Layer (`empirica/config/`)

**Purpose:** YAML configuration files and loaders

```
config/
├── investigation_profiles.yaml         # Investigation strategy profiles
├── modality_config.yaml                # Modality switching config
├── threshold_loader.py                 # Load threshold values
├── profile_loader.py                   # Load investigation profiles
├── goal_scope_loader.py                # Load goal scopes
├── credentials_loader.py               # Load API credentials
│
└── mco/                                # Meta-Cognitive Orchestrator configs
    ├── personas.yaml                   # Persona definitions
    ├── model_profiles.yaml             # Model characteristics
    ├── cascade_styles.yaml             # CASCADE style definitions
    ├── goal_scopes.yaml                # Goal scope definitions
    └── protocols.yaml                  # Protocol definitions
```

---

## Investigation Layer (`empirica/investigation/`)

**Purpose:** Pluggable investigation strategies

```
investigation/
├── investigation_plugin.py             # Base investigation plugin
└── advanced_investigation/             # Advanced strategies
    └── advanced_investigation.py       # Multi-strategy investigation
```

---

## Bootstrap Layer (`empirica/bootstraps/`)

**Purpose:** Session initialization strategies

```
bootstraps/
├── optimal_metacognitive_bootstrap.py  # Default bootstrap
├── extended_metacognitive_bootstrap.py # Extended bootstrap
└── onboarding_wizard.py                # Interactive onboarding
```

---

## Dashboard Layer (`empirica/dashboard/`)

**Purpose:** Real-time monitoring (optional)

```
dashboard/
├── cascade_monitor.py                  # Live CASCADE monitoring
└── snapshot_monitor.py                 # Epistemic snapshot viewer
```

---

## Supporting Layers

### Metrics (`empirica/metrics/`)
```
metrics/
└── token_efficiency.py                 # Token usage tracking
```

### Integration (`empirica/integration/`)
```
integration/
└── empirica_action_hooks.py            # External system hooks
```

### Utils (`empirica/utils/`)
```
utils/
└── session_resolver.py                 # Session ID resolution
```

### Cognitive Benchmarking (`empirica/cognitive_benchmarking/`)
```
cognitive_benchmarking/
├── erb/                                # Epistemic Reasoning Benchmark
│   ├── epistemic_reasoning_benchmark.py
│   ├── cascade_workflow_orchestrator.py
│   └── comprehensive_epistemic_test_suite.py
├── analysis/
│   └── cross_benchmark_correlation.py
└── cloud_adapters/
    └── unified_cloud_adapter.py
```

---

## External Interfaces

### MCP Server (`mcp_local/`)
```
mcp_local/
├── empirica_mcp_server.py              # Standard MCP server
├── empirica_tmux_mcp_server.py         # Tmux-aware MCP server
└── start_empirica_mcp.sh               # Startup script
```

### Scripts (`scripts/`)
```
scripts/
├── safe_delete.py                      # Safe file deletion
├── cleanup_helper.sh                   # Cleanup automation
├── safe-branch-switch.sh               # Git branch switching
├── install_system_prompts.sh           # Install prompts
└── test_checkpoint_helper.sh           # Checkpoint testing
```

---

## Documentation Structure (`docs/`)

**Status:** Cleaned up from 200+ to ~70 essential files (2025-01-29)

```
docs/
├── 00_START_HERE.md                    # Entry point
├── 01_a_AI_AGENT_START.md             # AI agent quick start
├── 01_b_MCP_AI_START.md               # MCP-enabled AI start
├── 03_CLI_QUICKSTART.md               # CLI basics
├── 04_MCP_QUICKSTART.md               # MCP basics
├── 06_TROUBLESHOOTING.md              # Common issues
├── ONBOARDING_GUIDE.md                # Comprehensive onboarding
├── getting-started.md                  # Getting started
├── installation.md                     # Installation guide
├── architecture.md                     # High-level architecture
├── README.md                           # Documentation index
│
├── production/                         # Production documentation (26 files)
│   ├── 00_COMPLETE_SUMMARY.md         # Overview
│   ├── 03_BASIC_USAGE.md              # Getting started
│   ├── 05_EPISTEMIC_VECTORS.md        # 13 vectors explained
│   ├── 07_INVESTIGATION_SYSTEM.md     # Investigation
│   ├── 08_BAYESIAN_GUARDIAN.md        # Drift detection
│   ├── 13_PYTHON_API.md               # Python API reference
│   ├── 19_API_REFERENCE.md            # Complete API reference
│   ├── 20_TOOL_CATALOG.md             # MCP tools catalog
│   ├── 24_MCO_ARCHITECTURE.md         # MCO v2.0 architecture
│   └── ... (and 17 more)
│
├── skills/                             # Skill documentation
│   └── SKILL.md                       # Skill system
│
├── system-prompts/                     # System prompts (6 files)
│   ├── CANONICAL_SYSTEM_PROMPT.md     # Single source of truth ⭐
│   ├── CUSTOMIZATION_GUIDE.md         # When/how to customize
│   ├── MIGRATION_GUIDE.md             # Migrating from old prompts
│   ├── INSTALLATION.md                # System prompt installation
│   ├── OPTIMIZATION_ANALYSIS.md       # Token optimization
│   └── README.md                      # System prompts index
│
├── architecture/                       # Architecture docs (8 files)
│   ├── EMPIRICA_SYSTEM_OVERVIEW.md    # High-level overview
│   ├── EPISTEMIC_TRAJECTORY_VISUALIZATION.md  # Future vision
│   ├── FUTURE_VISIONS.md              # Vision index
│   ├── STORAGE_ARCHITECTURE_*.md      # Storage architecture
│   ├── *.svg                          # Visual diagrams
│   └── README.md                      # Architecture index
│
├── reference/                          # Reference docs (5 files)
│   ├── CANONICAL_DIRECTORY_STRUCTURE_V2.md  # This file
│   ├── STORAGE_LOCATIONS.md           # Storage locations
│   ├── CHANGELOG.md                   # Changelog
│   ├── command-reference.md           # Command reference
│   └── CANONICAL_DIRECTORY_STRUCTURE.md  # V1 (deprecated)
│
└── guides/                             # User/dev guides (14 files)
    ├── CRITICAL_NO_HEURISTICS_PRINCIPLE.md  # Core principle
    ├── REASONING_ACTING_SPLIT_GUIDE.md      # Important pattern
    ├── TRY_EMPIRICA_NOW.md                  # Quick start
    ├── MCP_CONFIGURATION_EXAMPLES.md        # MCP examples
    ├── PROFILE_MANAGEMENT.md                # Profile system
    ├── SESSION_ALIASES.md                   # Session aliases
    ├── engineering/                         # For developers
    │   ├── SEMANTIC_ENGINEERING_GUIDELINES.md
    │   └── SEMANTIC_ONTOLOGY.md
    ├── git/                                 # Git integration
    │   ├── empirica_git.md
    │   └── git_integration.md
    ├── protocols/                           # Protocols
    │   └── UVL_PROTOCOL.md
    └── setup/                               # Setup guides
        ├── CLAUDE_CODE_MCP_SETUP.md
        ├── MCP_SERVERS_SETUP.md
        └── mcp_config_rovodev.json
```

**Note:** Session docs, outdated specs, and examples archived to `empirica-dev/archive/`

---

## Key Dependencies

**Minimal Core:**
- Python 3.8+
- SQLite (built-in)
- Git (for checkpoint persistence)

**Optional:**
- MCP SDK (for MCP server)
- Various AI platform SDKs (for modality switching)
- Dashboard dependencies (for monitoring)

---

## Migration Notes

### Deprecated Components

**Being replaced:**
1. `empirica/calibration/parallel_reasoning.py::DriftMonitor` 
   → `empirica/core/drift/mirror_drift_monitor.py::MirrorDriftMonitor`

2. `empirica/calibration/adaptive_uncertainty_calibration/` 
   → Removed (contained heuristics)

**Status:** CASCADE still imports old `DriftMonitor`. Migration pending.

**Migration task:**
```python
# OLD (in metacognitive_cascade.py)
from empirica.calibration.parallel_reasoning import DriftMonitor

# NEW (should be)
from empirica.core.drift import MirrorDriftMonitor
```

---

## Version History

**v2.0 (2025-01-XX):**
- Added `core/drift/mirror_drift_monitor.py` (unified drift detection)
- Added `core/canonical/empirica_git/` (git notes integration)
- Marked `calibration/` as deprecated
- Updated CASCADE architecture (BOOTSTRAP session-level)

**v1.0 (2024):**
- Initial structure

---

## Questions?

For codebase structure questions, consult:
1. This file (source of truth)
2. `docs/architecture/` (deep dives)
3. Individual `__init__.py` files (package documentation)

---

**Last Verified:** 2025-01-XX  
**Total Files:** 187 Python files across 53 directories  
**Status:** ✅ Current
