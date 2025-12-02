# Comprehensive Empirica Understanding Document

**Created:** 2025-01-XX  
**Purpose:** Complete architectural understanding for creating user-facing documentation  
**For:** Deep reasoning AIs (RovoDev + Copilot Claude) working in parallel

---

## Executive Summary

**Empirica Core** is a metacognitive framework that enables AI agents to track and calibrate their epistemic state (what they know, how confident they are, what they're uncertain about) across work sessions.

**Core Principle:** Temporal self-validation without heuristics. Increases in knowledge/confidence = learning. Decreases without investigation = drift (memory corruption).

**Production Status:**
- **Core Empirica:** Production-ready ✅ (what one AI does)
- **Advanced Features:** Experimental ⚠️ (multi-AI orchestration, personas, sentinel)

---

## Part 1: Core Architecture (Production-Ready)

### 1.1 The Fundamental Workflow

```
SESSION (one work period):
  │
  ├─ BOOTSTRAP (once per session)
  │   └─ Load: persona, model profile, thresholds
  │   └─ Restore: context from prior sessions (if continuing)
  │
  └─ GOAL/WORK (per coherent task):
      │
      ├─ PREFLIGHT (assess before work)
      │   └─ 13 epistemic vectors (honest self-assessment)
      │   └─ Decision logic: ready / need investigation / need clarification
      │   └─ Git checkpoint created automatically ✅
      │
      ├─ CASCADE (implicit AI reasoning loop)
      │   ├─ investigate (implicit - AI just does this while thinking)
      │   ├─ plan (implicit - AI naturally plans)
      │   ├─ act (explicit - actual actions/changes)
      │   └─ CHECK (explicit gate, 0-N times)
      │       └─ "Should I continue or stop?"
      │       └─ Confidence validation
      │       └─ Git checkpoint created ✅
      │   └─ [loop until goal complete or blocked]
      │
      └─ POSTFLIGHT (calibrate after work)
          └─ Re-assess 13 vectors
          └─ Calculate deltas (POSTFLIGHT - PREFLIGHT)
          └─ Measure calibration quality
          └─ Git checkpoint created ✅
          └─ Generate training data
```

**Key Points:**
- BOOTSTRAP is session-level only (not per-goal)
- CASCADE is mostly implicit (AI's natural reasoning)
- Only PREFLIGHT, CHECK, ACT, POSTFLIGHT involve explicit tool calls
- Git checkpoints automatic at PREFLIGHT/CHECK/POSTFLIGHT
- Training data = delta analysis from PREFLIGHT → [CHECKs] → POSTFLIGHT

---

### 1.2 The 13 Epistemic Vectors (UVL Protocol)

**GATE Vector:**
1. **ENGAGEMENT** (≥0.6 required) - Task engagement, motivation

**TIER 0: FOUNDATION (35% weight)**
2. **KNOW** - Domain knowledge, concepts understood
3. **DO** - Capability to execute, tools/skills available
4. **CONTEXT** - Situational awareness, environment understanding

**TIER 1: COMPREHENSION (25% weight)**
5. **CLARITY** - Requirements clarity, goal understanding
6. **COHERENCE** - Internal consistency, logical flow
7. **SIGNAL** - Information quality, signal-to-noise ratio

**TIER 2: EXECUTION (25% weight)**
8. **DENSITY** - Complexity load, cognitive burden
9. **STATE** - System/environment state awareness
10. **CHANGE** - Change tracking, what's being modified

**META-EPISTEMIC (15% weight)**
11. **COMPLETION** - Progress tracking, how close to done
12. **IMPACT** - Consequences awareness, downstream effects
13. **UNCERTAINTY** - What's unknown, confidence gaps

**All vectors:** 0.0 to 1.0 scale, assessed honestly (NO heuristics!)

**Purpose:** Track epistemic state, detect drift, measure learning, generate calibration data

---

### 1.3 Storage Architecture: Three Layers

**Why three layers?** Different use cases, redundancy, performance optimization.

**Layer 1: Git Notes (Cross-AI Coordination)**
- **Location:** `refs/notes/empirica/`
- **Structure:**
  - `checkpoints/<commit-hash>` - PREFLIGHT/CHECK/POSTFLIGHT states
  - `goals/<goal-id>` - Discoverable goals with epistemic context
  - `session/<session-id>` - Session metadata
  - `tasks/<task-id>` - Task tracking
- **Benefits:** Version controlled, distributed, ~85% token compressed (~3K → ~450)
- **Use case:** Cross-AI discovery, lineage tracking, audit trail
- **Status:** ✅ Actively working (verified: 16 goals, 5 sessions, 6 tasks stored)

**Layer 2: SQLite (Fast Queries)**
- **Location:** `.empirica/sessions/sessions.db`
- **Schema:** Sessions, vectors, assessments, queries
- **Benefits:** Fast structured queries, relational data
- **Use case:** Session lookup, vector analysis, performance metrics
- **Implementation:** `empirica/data/session_database.py`

**Layer 3: JSON Logs (Full Fidelity)**
- **Location:** `.empirica_reflex_logs/<session-id>.json`
- **Content:** Complete temporal workflow logs, reflex frames
- **Benefits:** Full fidelity, temporal replay capability
- **Use case:** Debugging, complete audit trail, retrospective analysis
- **Implementation:** `empirica/core/canonical/reflex_logger.py`

**Automatic creation:** All three layers populated automatically during PREFLIGHT/CHECK/POSTFLIGHT

---

### 1.4 Drift Detection: MirrorDriftMonitor (No Heuristics)

**Philosophy:** Temporal self-validation via mirror principle

**The Mirror Principle:**
- **Increases expected:** Learning (KNOW ↑, CLARITY ↑)
- **Decreases unexpected:** Drift/corruption (KNOW ↓ without investigation)
- **Comparison:** Current state vs recent checkpoint history (not single point)

**Implementation:**
- **Location:** `empirica/core/drift/mirror_drift_monitor.py`
- **Class:** `MirrorDriftMonitor`
- **Method:** Load recent checkpoints, compare current vectors, detect unexpected decreases

**Replaces (DEPRECATED):**
- ❌ `empirica/calibration/parallel_reasoning.py::DriftMonitor` (had heuristics)
- ❌ `empirica/calibration/adaptive_uncertainty_calibration/` (too complex, heuristics)

**Migration Status:** ⚠️ CASCADE still uses old DriftMonitor (line 76 in metacognitive_cascade.py)
- Need to update: `from empirica.calibration.parallel_reasoning import DriftMonitor`
- Change to: `from empirica.core.drift import MirrorDriftMonitor`

---

### 1.5 Four User Interfaces

**1. MCP Server (Best for AI Assistants in IDEs)**
- **Location:** `mcp_local/empirica_mcp_server.py`
- **For:** Claude Desktop, Cursor, Windsurf, Rovo Dev
- **Features:** 23 MCP tools, real-time tracking, automatic prompts
- **Setup:** Add to IDE MCP config JSON
- **Tools:** See `production/20_TOOL_CATALOG.md`

**2. CLI (Best for Terminal & Automation)**
- **Location:** `empirica/cli/`
- **Commands:** `empirica preflight`, `check`, `postflight`, `goals-create`, etc.
- **Features:** Scriptable, composable, full control
- **Usage:** `empirica --help`

**3. Python API (Best for Custom Integrations)**
- **Location:** `empirica/core/`, `empirica/data/`, etc.
- **Classes:** `CanonicalEpistemicCascade`, `SessionDatabase`, `GoalOrchestrator`
- **Usage:** `from empirica.core import ...`
- **Docs:** `production/13_PYTHON_API.md`

**4. Empirica Skill (AI Agent Learning Guide)**
- **Location:** `docs/skills/SKILL.md` (48KB)
- **For:** AI agents learning Empirica
- **Content:** Complete workflow, all 13 vectors, calibration techniques, functional self-awareness
- **Format:** Claude Skills compatible
- **Purpose:** THE comprehensive guide for AI agents

---

### 1.6 Cross-AI Coordination (Production Feature)

**Goal Discovery:**
```bash
empirica goals-discover --from-ai-id other-ai
# Returns: All goals with epistemic context and lineage
```

**Goal Resumption:**
```bash
empirica goals-resume <goal-id> --ai-id your-ai
# Loads: Other AI's epistemic state, adds lineage entry
```

**How it works:**
1. AI-1 creates goal → stored in `refs/notes/empirica/goals/<goal-id>`
2. AI-2 runs `goals-discover` → reads git notes
3. AI-2 runs `goals-resume` → loads context, adds lineage
4. AI-2 continues work with full epistemic handoff

**Benefits:**
- Distributed coordination (git pull syncs)
- Epistemic handoffs (know other AI's confidence)
- Lineage tracking (who created/resumed/completed)
- Version controlled (can branch/revert)

**Implementation:**
- `empirica/core/canonical/empirica_git/goal_store.py`
- `empirica/cli/command_handlers/goal_discovery_commands.py`

**Status:** ✅ Production-ready, actively working

---

## Part 2: Advanced Features (Experimental)

### 2.1 MCO (Meta-Cognitive Orchestrator)

**Purpose:** Persona-based orchestration, dynamic routing, multi-AI composition

**Components:**
- **Persona System:** Define AI personas with capabilities/limitations
- **Sentinel Orchestrator:** Route tasks based on epistemic state
- **Composition Strategies:** Combine multiple personas for complex tasks
- **Model Profiles:** Characteristics of different AI models

**Configuration:**
- `empirica/config/mco/personas.yaml`
- `empirica/config/mco/model_profiles.yaml`
- `empirica/config/mco/cascade_styles.yaml`
- `empirica/config/mco/goal_scopes.yaml`

**Documentation:** `production/24_MCO_ARCHITECTURE.md`

**Status:** ⚠️ Experimental, provided without production guarantees

---

### 2.2 ScopeVector System

**Purpose:** Goal scoping for orchestration decisions

**Three dimensions:**
- **Breadth** (0.0-1.0): How wide the goal spans
- **Duration** (0.0-1.0): Expected lifetime
- **Coordination** (0.0-1.0): Multi-agent coordination needed

**Usage:**
```bash
empirica goals-create \
  --scope-breadth 0.8 \
  --scope-duration 0.6 \
  --scope-coordination 0.7
```

**Documentation:** `production/25_SCOPEVECTOR_GUIDE.md`

**Status:** ⚠️ Experimental, used in MCO routing

---

### 2.3 Bayesian Guardian

**Purpose:** Confidence threshold management

**Status:** ⚠️ Experimental, may contain heuristics (review needed)

**Documentation:** `production/08_BAYESIAN_GUARDIAN.md`

---

### 2.4 Component Plugins

**Location:** `empirica/components/`

**Available components:**
- Code Intelligence Analyzer
- Context Validation
- Empirical Performance Analyzer
- Environment Stabilization
- Intelligent Navigation
- Procedural Analysis
- Runtime Validation
- Security Monitoring
- Tool Management
- Workspace Awareness

**Status:** ⚠️ Optional, experimental, enable as needed

**Documentation:** `production/10_PLUGIN_SYSTEM.md`

---

## Part 3: Documentation Status & Issues

### 3.1 Current Documentation Structure

**Tier 1: User Docs (docs/ root)**
- Currently: ~13 files with overlaps
- Target: 8-10 essential files
- Issues: Missing MCP server, git automation, Skills doc coverage

**Tier 2: Production Docs (docs/production/)**
- Currently: 27 files (00-29, some missing numbers)
- Status: Mostly correct, needs organization
- Action: Mark Core (00-13, 20, 23) vs Advanced (14-19, 21-22, 24-29)

**Tier 3: Reference Docs (docs/reference/)**
- Currently: 16 files
- Issues: Outdated bootstrap docs, superseded files
- Action: Archive 4-5 files, keep ~10

**Tier 4: Guides (docs/guides/)**
- Currently: Multiple subdirectories
- Action: Keep essential (git/, protocols/), review others

---

### 3.2 Files Needing Creation/Major Revision

**Need complete rewrite (based on deep understanding):**
1. `docs/installation.md` - Add 4 interfaces, git setup, clear choices
2. `docs/architecture.md` - Add interfaces section, git automation, Skills doc
3. `docs/getting-started.md` - Add MCP vs CLI choice, git checkpoints explanation

**Current status:**
- installation.md: 580 lines, platform-specific, missing interface overview
- architecture.md: 432 lines, missing git automation details
- getting-started.md: 338 lines → enhanced to ~450 lines ✅ (partially done)

---

### 3.3 Core vs Advanced Distinction

**Core Empirica (Production-Ready ✅):**
- Single-AI workflows
- PREFLIGHT → CASCADE → CHECK → POSTFLIGHT
- 13 epistemic vectors
- Git checkpoints (automatic)
- Goal/subtask orchestration
- Session continuity (handoffs)
- Cross-AI coordination (goal discovery)
- Storage (SQLite + JSON + Git)
- MCP tools / CLI / Python API
- Drift detection (MirrorDriftMonitor)

**Advanced Features (Experimental ⚠️):**
- MCO (persona orchestration)
- Sentinel (routing based on epistemic state)
- Bayesian Guardian
- Cognitive Vault
- Component plugins
- Multi-persona composition
- ScopeVector advanced usage

**Documentation strategy:**
- Core docs: Focus on production-ready features
- Production docs: Mark each file as Core or Advanced
- Advanced features: Clear "experimental, no guarantees" warnings

---

## Part 4: Key Insights for Documentation

### 4.1 What Users Need to Know (Priority Order)

**1. Interface Choice (Critical)**
- 4 ways to use Empirica (MCP, CLI, API, Skill)
- When to use each
- Setup instructions for each

**2. Basic Workflow (Critical)**
- PREFLIGHT → work → CHECK → POSTFLIGHT
- Git checkpoints automatic (no manual steps)
- Honest self-assessment (no heuristics)

**3. Git Automation (Important)**
- What happens automatically
- Where data is stored (3 layers)
- How to view checkpoints
- Cross-AI coordination via git notes

**4. 13 Vectors (Important)**
- What they mean
- How to assess honestly
- Avoid common failure modes (anchoring to 0.5)

**5. Goal Orchestration (Useful)**
- Creating goals
- Adding subtasks
- Completing work
- Cross-AI discovery

**6. Advanced Features (Optional)**
- MCO, personas, Sentinel
- Clearly marked as experimental

---

### 4.2 Common User Journeys

**Journey 1: AI Assistant User (MCP)**
1. Install MCP server in IDE config
2. Load empirica Skill doc for understanding
3. Use MCP tools during work (automatic tracking)
4. View sessions and checkpoints

**Journey 2: CLI User (Terminal)**
1. Install via pip
2. Run `empirica preflight "task"`
3. Work, run `empirica check` periodically
4. Run `empirica postflight`
5. View `git notes list`

**Journey 3: Developer (Python API)**
1. Import classes
2. Create CASCADE instance
3. Call methods programmatically
4. Query SessionDatabase

**Journey 4: Multi-AI Team**
1. AI-1 creates goal with `goals-create`
2. AI-2 discovers with `goals-discover`
3. AI-2 resumes with `goals-resume`
4. Lineage tracked automatically

---

### 4.3 Critical Distinctions to Clarify

**CASCADE vs Session:**
- SESSION = entire work period, may contain multiple goals
- CASCADE = work loop within a goal (investigate → plan → act → check)
- BOOTSTRAP = session-level initialization (once per session)

**Implicit vs Explicit:**
- Implicit: investigate, plan (AI just thinks)
- Explicit: PREFLIGHT, CHECK, ACT, POSTFLIGHT (tool calls)

**Core vs Advanced:**
- Core = production-ready, fully supported
- Advanced = experimental, may change

**Automatic vs Manual:**
- Automatic: Git checkpoints, vector storage, session tracking
- Manual: Assessment input, task description, goal creation

---

## Part 5: Technical Details for Reference

### 5.1 Codebase Structure (Verified)

```
empirica/
├── core/                               # Core CASCADE & orchestration
│   ├── canonical/                      # Core workflow classes
│   │   ├── canonical_epistemic_assessment.py
│   │   ├── canonical_goal_orchestrator.py
│   │   ├── reflex_frame.py
│   │   ├── reflex_logger.py
│   │   ├── git_enhanced_reflex_logger.py
│   │   └── empirica_git/               # Git notes integration ⭐
│   │       ├── checkpoint_manager.py
│   │       ├── goal_store.py
│   │       ├── session_sync.py
│   │       └── sentinel_hooks.py
│   ├── metacognitive_cascade/          # CASCADE engine
│   │   ├── metacognitive_cascade.py    # Main CASCADE class
│   │   ├── investigation_strategy.py
│   │   └── investigation_plugin.py
│   ├── drift/                          # Drift detection ⭐
│   │   └── mirror_drift_monitor.py     # NO heuristics
│   ├── schemas/                        # Data schemas
│   │   ├── epistemic_assessment.py
│   │   └── assessment_converters.py
│   ├── goals/                          # Goal orchestration
│   ├── tasks/                          # Task management
│   ├── completion/                     # Completion tracking
│   ├── handoff/                        # Session continuity
│   ├── identity/                       # AI identity & signatures
│   ├── persona/                        # Persona system (MCO)
│   └── metacognition_12d_monitor/      # 12D self-awareness (experimental)
│
├── cli/                                # Command-line interface
│   ├── cli_core.py
│   ├── mcp_client.py
│   └── command_handlers/               # 23 command handlers
│
├── data/                               # Persistence layer
│   ├── session_database.py             # SQLite
│   └── session_json_handler.py         # JSON logs
│
├── calibration/                        # ⚠️ DEPRECATED (has heuristics)
│   ├── parallel_reasoning.py           # Old DriftMonitor
│   └── adaptive_uncertainty_calibration/
│
├── components/                         # Optional capabilities
│   ├── tool_management/
│   ├── code_intelligence_analyzer/
│   ├── workspace_awareness/
│   └── ... (10+ components)
│
├── plugins/                            # Extensible features
│   └── modality_switcher/              # Route to specialized AIs
│
├── config/                             # Configuration files
│   ├── investigation_profiles.yaml
│   ├── modality_config.yaml
│   └── mco/                            # MCO configs
│
├── bootstraps/                         # Session initialization
│   ├── optimal_metacognitive_bootstrap.py
│   └── extended_metacognitive_bootstrap.py
│
├── dashboard/                          # Monitoring UI
├── metrics/                            # Performance tracking
├── investigation/                      # Investigation strategies
├── integration/                        # External system hooks
└── utils/                              # Utilities

Total: 187 Python files across 53 directories
```

**Source of truth:** `docs/reference/CANONICAL_DIRECTORY_STRUCTURE_V2.md`

---

### 5.2 Key Files & Classes

**Core CASCADE:**
- `CanonicalEpistemicCascade` - Main workflow class (in metacognitive_cascade.py)
- `CanonicalGoalOrchestrator` - Goal/task management
- `SessionDatabase` - SQLite persistence
- `ReflexLogger` - Temporal logging

**Git Integration:**
- `CheckpointManager` - Create/load checkpoints
- `GoalStore` - Store/discover goals
- `SessionSync` - Sync session metadata

**Drift Detection:**
- `MirrorDriftMonitor` - NEW (no heuristics) ✅
- `DriftMonitor` - OLD (deprecated, still in use) ⚠️

**CLI:**
- 23 command handlers in `cli/command_handlers/`
- All expose both CLI and MCP interfaces

---

### 5.3 MCP Tools (All 23)

**Session Management:**
1. `bootstrap_session` - Initialize session
2. `resume_previous_session` - Resume from git

**Workflow:**
3. `execute_preflight` - Start CASCADE
4. `submit_preflight_assessment` - Submit vectors
5. `execute_check` - Decision gate
6. `submit_check_assessment` - Submit CHECK vectors
7. `execute_postflight` - Complete CASCADE
8. `submit_postflight_assessment` - Submit final vectors

**Goals:**
9. `create_goal` - Create discoverable goal
10. `add_subtask` - Add task to goal
11. `complete_subtask` - Mark task complete
12. `get_goal_progress` - Check progress
13. `list_goals` - List all goals
14. `discover_goals` - Find other AI's goals ⭐
15. `resume_goal` - Resume another AI's goal ⭐

**State:**
16. `get_epistemic_state` - Current vectors
17. `get_session_summary` - Session overview
18. `get_calibration_report` - Calibration quality

**Git:**
19. `create_git_checkpoint` - Manual checkpoint
20. `load_git_checkpoint` - Load from git

**Handoff:**
21. `create_handoff_report` - Session continuity
22. `query_handoff_reports` - Find handoffs

**Identity:**
23. `create_identity` - AI identity management (Phase 2)

**Documentation:** `production/20_TOOL_CATALOG.md`

---

## Part 6: Documentation Work Split

### 6.1 Proposed Division of Labor

**RovoDev (Planning & Architecture):**
1. Create master documentation plan
2. Define structure for new installation.md, architecture.md, getting-started.md
3. Content templates for each section
4. Cross-reference map
5. Success criteria definition
6. Review and integration

**Copilot Claude (Execution & Detail):**
1. Execute documentation plan
2. Write detailed sections following templates
3. Verify technical accuracy against code
4. Test all code examples
5. Check all cross-references
6. Polish readability

### 6.2 Immediate Next Steps

**Step 1: Decide on documentation approach**
- Option A: Fix existing 3 files (installation, architecture, getting-started)
- Option B: Create new from scratch based on this understanding
- Recommendation: Option B (cleaner, incorporates deep understanding)

**Step 2: Create documentation structure**
- Define sections for each file
- Create templates with placeholders
- Identify insertion points for key concepts

**Step 3: Parallel execution**
- RovoDev: installation.md template
- Copilot Claude: Execute architecture.md
- Alternate or collaborate as needed

**Step 4: Integration & review**
- Cross-check consistency
- Verify technical accuracy
- Test user journeys
- Final polish

---

## Part 7: Open Questions & Decisions Needed

### 7.1 Documentation Scope

**Q1:** Should installation.md cover all 4 interfaces equally, or focus on one recommended path?
- Option A: Equal coverage (comprehensive but longer)
- Option B: Focus on MCP (recommended) with links to others
- Recommendation: Option B for simplicity

**Q2:** How much detail on git automation in user docs?
- Option A: Just "it's automatic, see technical docs for details"
- Option B: Show storage structure, viewing commands
- Recommendation: Option B (users want to understand what's happening)

**Q3:** Where to mention experimental features?
- Option A: Not at all in core docs
- Option B: Brief mention with "experimental" warning
- Recommendation: Option B (users should know they exist)

### 7.2 Technical Decisions

**Q1:** Should we migrate CASCADE to MirrorDriftMonitor now or document current state?
- Recommendation: Document current state, note migration in progress

**Q2:** Should we create separate MCP and CLI quick starts?
- Recommendation: No, unified getting-started with interface choice upfront

**Q3:** How to handle deprecated calibration/ modules in docs?
- Recommendation: Don't mention in user docs, note in technical reference only

---

## Part 8: Success Criteria

### 8.1 Documentation Quality Metrics

**Completeness:**
- ✅ All 4 interfaces documented
- ✅ Git automation explained
- ✅ 13 vectors covered
- ✅ Core vs Advanced distinction clear
- ✅ Skills doc referenced

**Accuracy:**
- ✅ All code examples work
- ✅ All commands verified
- ✅ File paths correct
- ✅ No outdated information

**Usability:**
- ✅ User can choose interface in <5 min
- ✅ First CASCADE achievable in <15 min
- ✅ Git automation understood
- ✅ Clear next steps provided

**Consistency:**
- ✅ Terminology consistent across files
- ✅ Cross-references work
- ✅ No contradictions
- ✅ Matches production/  reference docs

### 8.2 User Journey Success

**AI Assistant User:**
- Can set up MCP in <10 min
- Understands automatic tracking
- Knows about Skills doc

**CLI User:**
- Can run first PREFLIGHT in <5 min
- Understands git checkpoints
- Can view stored data

**Developer:**
- Knows Python API exists
- Can find API reference
- Understands architecture

**Multi-AI Team:**
- Knows about goal discovery
- Can use cross-AI features
- Understands lineage

---

## Conclusion

**What we have:**
- Deep architectural understanding ✅
- Verified implementation details ✅
- Clear Core vs Advanced distinction ✅
- User journey clarity ✅

**What we need:**
- User-facing docs that reflect this understanding
- Clear, accurate installation guide
- Comprehensive but approachable architecture doc
- Smooth getting-started experience

**Recommended approach:**
- Create new docs from scratch
- Split work: RovoDev (planning) + Copilot Claude (execution)
- Focus on Core features (production-ready)
- Mark Advanced clearly (experimental)

**Ready to proceed with documentation creation in parallel.** 🚀

---

**Total:** 187 Python files, 53 directories, 4 interfaces, 23 MCP tools, 13 epistemic vectors
**Status:** Comprehensive understanding complete, ready for documentation work
