# CC-Switch + Empirica Integration Plan

**Date:** 2025-12-06
**Status:** Analysis & Planning
**Objective:** Build multi-AI CLI switcher with Empirica MCO and epistemic handoff capabilities

---

## Executive Summary

**cc-switch** is a mature, production-ready multi-CLI management platform (Claude Code, Codex, Gemini) with:
- ✅ SQLite + JSON dual-layer storage (perfect match for Empirica)
- ✅ Cross-platform desktop app (Tauri) + CLI tool
- ✅ Provider configuration management
- ✅ MCP server management
- ✅ Skills & prompts management
- ✅ 38K+ lines of TypeScript + Rust

**Integration Vision:**
Extend cc-switch to support Rovo Dev and Qwen CLI, then add Empirica's:
- MCO (Model Configuration Object) system
- CASCADE workflow tracking
- Epistemic handoff reports
- Multi-AI coordination verification

---

## CC-Switch Architecture Analysis

### 1. Core Storage Architecture

**Current (v3.8.0+):**
```
SQLite Database (syncable data)
├── providers (configurations for each AI CLI)
├── mcp_servers (MCP server definitions)
├── prompts (system prompts per CLI)
├── skills (skills management)
├── settings (key-value pairs)
└── proxy_config (routing configuration)

JSON Files (device-level data)
├── window state
├── local paths (app-specific config dirs)
└── UI preferences
```

**Storage Location:**
- **Desktop:** Tauri app data directory (`~/.config/cc-switch/` on Linux, etc.)
- **CLI:** Default to `~/.cc-switch/` or user-specified location

### 2. Database Schema (Rust, src-tauri/src/database/)

```rust
// Providers Table (21 columns)
CREATE TABLE providers (
    id TEXT,                          // unique provider ID
    app_type TEXT,                    // 'claude'|'codex'|'gemini'|'rovo'|'qwen'
    name TEXT,                        // provider display name
    settings_config TEXT,             // JSON with API key, endpoint, etc.
    website_url TEXT,
    category TEXT,
    created_at INTEGER,
    sort_index INTEGER,
    notes TEXT,
    icon TEXT,
    icon_color TEXT,
    meta TEXT,                        // metadata JSON (can store anything)
    is_current BOOLEAN,
    is_proxy_target BOOLEAN,
    PRIMARY KEY (id, app_type)
);

// MCP Servers Table
CREATE TABLE mcp_servers (
    id TEXT PRIMARY KEY,
    name TEXT,
    server_config TEXT,               // JSON with command, args, etc.
    description TEXT,
    tags TEXT,                        // JSON array
    enabled_claude BOOLEAN,
    enabled_codex BOOLEAN,
    enabled_gemini BOOLEAN,
    // NEW: enabled_rovo, enabled_qwen
);

// Prompts Table (system prompts per CLI)
CREATE TABLE prompts (
    id TEXT,
    app_type TEXT,                    // which CLI this prompt is for
    name TEXT,
    content TEXT,                     // full prompt content
    description TEXT,
    enabled BOOLEAN,
    created_at INTEGER,
    PRIMARY KEY (id, app_type)
);

// Settings Table (key-value store)
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT                        // JSON serializable
);

// Proxy Config Table
CREATE TABLE proxy_config (
    id INTEGER PRIMARY KEY,
    enabled INTEGER,
    listen_address TEXT,
    listen_port INTEGER,
    target_app TEXT,                  // route to specific app
    ...
);
```

### 3. TypeScript Types (Frontend)

```typescript
// Provider Configuration
interface Provider {
    id: string;
    appType: AppType;                 // 'claude'|'codex'|'gemini'|'rovo'|'qwen'
    name: string;
    settingsConfig: {                 // JSON object
        apiKey?: string;
        endpoint?: string;
        model?: string;
        customHeaders?: Record<string, string>;
        // ... app-specific fields
    };
    websiteUrl?: string;
    category?: string;
    createdAt?: number;
    sortIndex?: number;
    notes?: string;
    icon?: string;
    iconColor?: string;
    isCurrent?: boolean;
    isProxyTarget?: boolean;
}

// MCP Server
interface MCPServer {
    id: string;
    name: string;
    serverConfig: {                   // JSON object
        command: string;
        args?: string[];
        env?: Record<string, string>;
    };
    description?: string;
    tags?: string[];
    enabledClaude?: boolean;
    enabledCodex?: boolean;
    enabledGemini?: boolean;
    // NEW fields for Rovo, Qwen
}

// System Prompt
interface Prompt {
    id: string;
    appType: AppType;
    name: string;
    content: string;
    description?: string;
    enabled: boolean;
    createdAt?: number;
    updatedAt?: number;
}
```

### 4. Services Architecture (Rust Backend)

**File:** `src-tauri/src/services/`

```rust
ProviderService {
    - create_provider()
    - update_provider()
    - delete_provider()
    - get_current_provider()
    - switch_provider()
    - list_providers()
    - import/export()
}

MCPService {
    - add_mcp_server()
    - remove_mcp_server()
    - enable/disable()
    - get_mcp_servers()
    - apply_to_config_files()
}

PromptService {
    - create_prompt()
    - update_prompt()
    - delete_prompt()
    - apply_prompt()
}

ProxyService {
    - setup_proxy()
    - route_requests()
    - handle_retries()
}
```

### 5. Tauri Commands (IPC Bridge)

Desktop app commands defined in Tauri:
```rust
// Provider commands
#[tauri::command]
async fn create_provider(state: State<'_, AppState>, provider: Provider) -> Result<Provider, String>

#[tauri::command]
async fn switch_provider(state: State<'_, AppState>, app_type: String, provider_id: String) -> Result<(), String>

// Config file operations
#[tauri::command]
async fn apply_provider_to_config(state: State<'_, AppState>, app_type: String, config_dir: String) -> Result<(), String>

// MCP operations
#[tauri::command]
async fn add_mcp_server(state: State<'_, AppState>, server: MCPServer) -> Result<MCPServer, String>
```

---

## Current Supported CLIs

| CLI | Support | Config File | MCP Support |
|-----|---------|------------|-------------|
| Claude Code | ✅ Full | `config.yml` | ✅ Yes |
| Codex | ✅ Full | `config.json` | ✅ Yes |
| Gemini | ✅ Full (v3.7+) | `.env` + `settings.json` | ✅ Yes |
| Rovo Dev | ❌ Not yet | `config.yml` | ✅ Yes |
| Qwen CLI | ❌ Not yet | TBD | TBD |
| Copilot CLI | ❌ Not yet | TBD | TBD |

---

## Integration Plan: Phase 1 - Extend to Rovo Dev & Qwen

### Step 1: Add Rovo Dev Support

**1.1 Extend AppType enum:**
```rust
pub enum AppType {
    Claude,
    Codex,
    Gemini,
    RovoDev,  // NEW
}
```

**1.2 Create RovoDev config provider:**
```rust
pub struct RovoDevConfigProvider {
    config_path: PathBuf,  // ~/.rovodev/config.yml
}

impl ConfigProvider for RovoDevConfigProvider {
    fn read_config() -> Result<RovoConfig>
    fn write_config(config: RovoConfig) -> Result<()>
    fn get_mcp_servers() -> Result<Vec<MCPServer>>
    fn set_mcp_servers(servers: Vec<MCPServer>) -> Result<()>
}
```

**1.3 Define RovoConfig schema:**
```typescript
interface RovoConfig {
    version: string;
    agent: {
        modelId: string;
        additionalSystemPrompt: string;  // From Empirica
        streaming: boolean;
        temperature: number;
        enableDeepPlanTool: boolean;
    };
    sessions: {
        autoRestore: boolean;
        persistenceDir: string;
    };
    mcp: {
        mcpConfigPath: string;
        allowedMcpServers: string[];
        disabledMcpServers: string[];
    };
}
```

**1.4 Mapping to cc-switch Provider:**
```
Provider {
    id: "rovo-dev-sonnet-prod",
    appType: "rovo",
    name: "Rovo Dev - Sonnet (Production)",
    settingsConfig: {
        configDir: "~/.rovodev",
        modelId: "anthropic.claude-sonnet-4-5-20250929",
        additionalSystemPrompt: "<empirica-v4.0>...",  // From Empirica
        temperature: 0.3,
        streaming: true
    },
    meta: {
        rovoVersion: "2.0",
        lastModified: "2025-12-06"
    }
}
```

### Step 2: Add Qwen CLI Support

**Similar approach for Qwen:**
```rust
pub struct QwenConfigProvider {
    config_path: PathBuf,  // ~/.qwen_cli/config.json or TBD
}
```

---

## Phase 2: Empirica MCO Integration

### Goal: Add epistemic configuration management to cc-switch

### 2.1 New Database Tables

```sql
-- MCO Profiles (model profiles from empirica/config/mco/model_profiles.yaml)
CREATE TABLE mco_profiles (
    id TEXT PRIMARY KEY,
    model_name TEXT,                   // 'claude_haiku', 'claude_sonnet', etc.
    reasoning_depth REAL,
    code_generation REAL,
    safety_awareness REAL,
    speed_vs_accuracy_bias REAL,
    uncertainty_underestimation REAL,
    notes TEXT,
    created_at INTEGER
);

-- Personas (implementer, researcher, reviewer)
CREATE TABLE personas (
    id TEXT PRIMARY KEY,
    name TEXT,
    engagement_threshold REAL,
    investigation_max_rounds INTEGER,
    preferred_tools TEXT,              // JSON array
    learning_style TEXT,
    created_at INTEGER
);

-- CASCADE Styles
CREATE TABLE cascade_styles (
    id TEXT PRIMARY KEY,
    style_name TEXT,                   // 'implementation', 'research', etc.
    pattern TEXT,                      // "PREFLIGHT → CHECK → ACT → POSTFLIGHT"
    investigation_budget INTEGER,
    validation_gates_confidence REAL,
    created_at INTEGER
);

-- Provider MCO Config (maps provider to MCO settings)
CREATE TABLE provider_mco_config (
    provider_id TEXT NOT NULL,
    app_type TEXT NOT NULL,
    mco_profile_id TEXT,               // Link to mco_profiles
    persona_id TEXT,                   // Link to personas
    cascade_style_id TEXT,             // Link to cascade_styles
    bias_corrections TEXT,             // JSON with vector adjustments
    PRIMARY KEY (provider_id, app_type),
    FOREIGN KEY (provider_id, app_type) REFERENCES providers(id, app_type)
);
```

### 2.2 Empirica Prompt Integration

Add new Prompt type for Empirica system prompts:

```typescript
interface EmpericaPrompt extends Prompt {
    appType: AppType;
    promptType: 'empirica_canonical' | 'empirica_mco' | 'custom';
    mcoprofileId?: string;
    personaId?: string;
    cascadeStyleId?: string;
    systemPromptContent: string;
    aiId?: string;                     // 'claude-code', 'claude-sonnet', 'qwen'
}
```

### 2.3 Provider Switching with MCO

When switching providers, also load:
1. MCO profile (bias corrections)
2. Persona configuration
3. CASCADE style preferences
4. Empirica system prompt for that AI

```rust
#[tauri::command]
async fn switch_provider_with_mco(
    state: State<'_, AppState>,
    app_type: String,
    provider_id: String
) -> Result<ProviderWithMCO, String> {
    // 1. Get provider
    let provider = state.db.get_provider(&provider_id, &app_type)?;

    // 2. Get MCO config for this provider
    let mco = state.db.get_provider_mco_config(&provider_id, &app_type)?;

    // 3. Get MCO profile details
    let profile = state.db.get_mco_profile(&mco.mco_profile_id)?;
    let persona = state.db.get_persona(&mco.persona_id)?;
    let style = state.db.get_cascade_style(&mco.cascade_style_id)?;

    // 4. Write config with updated system prompt + MCO settings
    write_config_with_mco(&provider, &profile, &persona, &style)?;

    Ok(ProviderWithMCO {
        provider,
        mco_profile: profile,
        persona,
        cascade_style: style
    })
}
```

---

## Phase 3: Epistemic Handoff Integration

### Goal: Store and verify CASCADE checkpoints in cc-switch database

### 3.1 New Tables for Handoff Data

```sql
-- CASCADE Sessions (tracked across provider switches)
CREATE TABLE cascade_sessions (
    id TEXT PRIMARY KEY,               // UUID from Empirica
    ai_id TEXT NOT NULL,               // 'claude-code', 'sonnet', 'qwen'
    provider_id TEXT NOT NULL,
    app_type TEXT NOT NULL,
    session_type TEXT,                 // 'development', 'production', 'testing'
    created_at INTEGER,
    completed_at INTEGER,
    phase TEXT,                        // 'PREFLIGHT', 'CHECK', 'POSTFLIGHT'
    current_round INTEGER,
    FOREIGN KEY (provider_id, app_type) REFERENCES providers(id, app_type)
);

-- Epistemic Assessments (PREFLIGHT, CHECK, POSTFLIGHT vectors)
CREATE TABLE epistemic_assessments (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    phase TEXT,                        // 'PREFLIGHT', 'CHECK', 'POSTFLIGHT'
    round_num INTEGER,
    vectors TEXT,                      // JSON with all 13 vectors
    overall_confidence REAL,
    timestamp INTEGER,
    git_note_sha TEXT,                 // Reference to git notes storage
    FOREIGN KEY (session_id) REFERENCES cascade_sessions(id)
);

-- Handoff Reports (for cross-AI continuity)
CREATE TABLE handoff_reports (
    id TEXT PRIMARY KEY,
    from_session_id TEXT NOT NULL,
    to_session_id TEXT,                // Next session (can be NULL initially)
    from_ai_id TEXT,
    to_ai_id TEXT,
    task_summary TEXT,
    key_findings TEXT,                 // JSON array
    remaining_unknowns TEXT,           // JSON array
    next_session_context TEXT,
    artifacts_created TEXT,            // JSON array
    created_at INTEGER,
    FOREIGN KEY (from_session_id) REFERENCES cascade_sessions(id)
);
```

### 3.2 Handoff UI in Desktop App

**New tab: "Epistemic Handoff"**
- View CASCADE sessions for each AI
- See latest assessment vectors
- Compare learning trajectories (PREFLIGHT → POSTFLIGHT)
- Load git notes (distributed audit trail)
- Generate handoff reports for next session

```typescript
interface HandoffView {
    fromSession: CascadeSession;
    toSession?: CascadeSession;

    fromAssessments: EpistemicAssessment[];      // PREFLIGHT, CHECK, POSTFLIGHT
    toAssessments?: EpistemicAssessment[];

    learningDelta: {
        [vectorName: string]: {
            from: number,
            to: number,
            delta: number
        }
    };

    gitNotes: {
        checkpoints: GitNoteCheckpoint[];
        verified: boolean;
    };

    handoffReport?: HandoffReport;
}
```

---

## Phase 4: Multi-AI Coordination

### Goal: Enable verification across agents (Claude Code, Sonnet, Qwen)

### 4.1 Coordination View

New dashboard showing:
1. **Current Active Sessions:** Each AI's current CASCADE phase
2. **Epistemic States:** Side-by-side vector comparison
3. **Cross-verification:** Can each AI verify others' git notes?
4. **Handoff Chain:** Visual flow of work passing between AIs
5. **Learning Curves:** Track each AI's knowledge improvement

### 4.2 Verification Commands

```rust
#[tauri::command]
async fn verify_git_notes(
    session_id: String,
    phase: String,
    round: u32
) -> Result<VerificationResult, String> {
    // 1. Query git notes
    let checkpoint = git_notes::get_checkpoint(&session_id, &phase, round)?;

    // 2. Verify JSON structure and vectors
    let is_valid = verify_checkpoint_structure(&checkpoint)?;

    // 3. Cross-check with SQLite reflexes table
    let db_record = state.db.get_assessment(&session_id, &phase, round)?;
    let vectors_match = checkpoint.vectors == db_record.vectors;

    Ok(VerificationResult {
        git_note_accessible: true,
        structure_valid: is_valid,
        vectors_in_sqlite: vectors_match,
        timestamp_verified: checkpoint.timestamp == db_record.timestamp,
        can_resume: vectors_match && is_valid
    })
}

#[tauri::command]
async fn cross_verify_agents(
    ai_id_1: String,
    ai_id_2: String
) -> Result<CrossVerificationResult, String> {
    let sessions_1 = state.db.get_sessions_for_ai(&ai_id_1)?;
    let sessions_2 = state.db.get_sessions_for_ai(&ai_id_2)?;

    // For each pair of sessions, verify:
    // - Can AI 2 read AI 1's git notes?
    // - Are vectors consistent?
    // - Can handoff happen safely?

    Ok(CrossVerificationResult {
        ai_1_reachable: true,
        ai_2_reachable: true,
        git_notes_accessible: true,
        safe_to_handoff: true,
        recommendations: vec![]
    })
}
```

---

## Technical Integration Steps

### Short Term (Phase 1-2: 2-4 weeks)

1. **Add Rovo Dev support to cc-switch**
   - Create RovoConfigProvider
   - Update database schema (add app_type='rovo')
   - Write config file handler
   - Test provider switching

2. **Add Qwen CLI support**
   - Similar to Rovo Dev
   - Determine Qwen config file format
   - Create QwenConfigProvider

3. **Integrate Empirica MCO**
   - Add MCO tables to cc-switch database
   - Create MCO profile UI in desktop app
   - Update provider switching to load MCO settings
   - Write MCO profile settings to config files

### Medium Term (Phase 3: 2-3 weeks)

4. **Add epistemic assessment storage**
   - Create CASCADE session tables
   - Add endpoints to store PREFLIGHT/CHECK/POSTFLIGHT vectors
   - Integrate with git notes (read/verify)
   - Build handoff report generation

5. **Create handoff UI**
   - Epistemic history viewer
   - Learning trajectory charts
   - Handoff report generator
   - Git notes verification panel

### Long Term (Phase 4+: Ongoing)

6. **Multi-AI coordination dashboard**
   - Real-time CASCADE phase tracking
   - Cross-verification tools
   - Handoff recommendations
   - Learning curve analytics

---

## File Structure (Proposed)

### New cc-switch directories:

```
cc-switch/
├── src-tauri/src/
│   ├── models/                         // Data types
│   │   ├── empirica.rs                // MCO, persona, cascade style
│   │   └── handoff.rs                 // Handoff reports
│   ├── services/
│   │   ├── rovo_dev.rs                // RovoDev config provider
│   │   ├── qwen_cli.rs                // Qwen config provider
│   │   ├── mco_service.rs             // MCO profile management
│   │   └── epistemic_service.rs       // CASCADE session + handoff
│   └── database/
│       └── schema.rs                  // NEW: MCO tables + CASCADE tables
│
├── src/
│   ├── components/
│   │   ├── providers/
│   │   │   └── RovoDevForm.tsx        // NEW
│   │   │   └── QwenCliForm.tsx        // NEW
│   │   ├── mco/                       // NEW
│   │   │   ├── MCOProfileSelector.tsx
│   │   │   ├── PersonaSettings.tsx
│   │   │   └── CascadeStyleConfig.tsx
│   │   └── epistemic/                 // NEW
│   │       ├── HandoffView.tsx
│   │       ├── EpistemicHistory.tsx
│   │       ├── LearningCurve.tsx
│   │       └── CoordinationDashboard.tsx
│   └── pages/
│       ├── MCOPage.tsx                // NEW
│       └── EpistemicHandoffPage.tsx   // NEW
```

---

## Integration Benefits

| Aspect | Benefit |
|--------|---------|
| **Configuration** | Single place to manage all AI CLI configs (Claude Code, Codex, Gemini, Rovo Dev, Qwen, Copilot) |
| **MCO System** | Automatically apply model-specific bias corrections and personas when switching providers |
| **Epistemic Tracking** | Store and verify CASCADE assessments in standardized database |
| **Handoff Reports** | Generate 98.8% token-efficient handoffs between agents |
| **Cross-verification** | Any AI can verify any other AI's cognitive state via git notes |
| **Learning Analytics** | Track knowledge improvement curves across all agents |
| **Distributed Coordination** | No central database dependency—git-backed epistemic states |

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Desktop** | Tauri 2.0 (Rust + TypeScript/React) |
| **CLI** | Node.js (if cc-switch-cli fork) |
| **Storage** | SQLite 3.x + JSON files |
| **Config Format** | YAML (Claude Code, Rovo Dev), JSON (Codex, Gemini, Qwen) |
| **VCS** | Git + git notes for distributed audit trail |
| **Authentication** | Provider-specific (API keys, OAuth) |

---

## References

- **cc-switch (Desktop):** https://github.com/farion1231/cc-switch
- **cc-switch-cli (CLI):** https://github.com/SaladDay/cc-switch-cli
- **Empirica:** `/home/yogapad/empirical-ai/empirica`
- **Rovo Dev Config:** `~/.rovodev/config.yml`
- **Empirica MCO:** `empirica/config/mco/`

---

## Next Steps

1. **Review this plan** with all stakeholders
2. **Create cc-switch fork** for Empirica-extended version
3. **Start Phase 1:** Rovo Dev + Qwen CLI support
4. **Parallel development:** MCO + epistemic table schema
5. **Test end-to-end:** Provider switching → MCO loading → config file updates

---

**Status:** Ready for implementation planning and design review.

