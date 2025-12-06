# CC-Switch + Empirica Integration Architecture

**Visual System Design**

---

## Current CC-Switch Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│ Desktop GUI (Tauri + React/TypeScript)                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Provider Manager  │  MCP Manager  │  Prompts  │  Skills  │  ...   │
│                                                                     │
└────────────────┬──────────────────────────────────────────────────┘
                 │ IPC (Tauri Commands)
                 │
┌────────────────▼──────────────────────────────────────────────────┐
│ Backend (Rust + Tauri)                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ProviderService  MCPService  PromptService  ProxyService         │
│         │              │           │              │                │
│         └──────────────┴───────────┴──────────────┘                │
│                       │                                             │
│            ┌──────────▼──────────┐                                 │
│            │  AppState + Manager │                                 │
│            └──────────┬──────────┘                                 │
│                       │                                             │
└───────────────────────┼─────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼──────┐  ┌────▼──────┐  ┌────▼──────────┐
   │  SQLite   │  │ JSON      │  │  Config Files │
   │  Database │  │  Files    │  │  (*.yml,      │
   │           │  │           │  │   *.json)     │
   │ Providers │  │ UI State  │  │               │
   │ MCP Svrs  │  │ Settings  │  │ Claude Code   │
   │ Prompts   │  │           │  │ Codex         │
   │ Skills    │  │           │  │ Gemini        │
   └───────────┘  └───────────┘  └───────────────┘
```

---

## Post-Integration Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Multi-AI CLI Switcher with Empirica Integration                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌─────────────────────────────────────────────────────────────────┐    │
│ │ Desktop GUI (Tauri + React/TypeScript)                          │    │
│ ├─────────────────────────────────────────────────────────────────┤    │
│ │                                                                 │    │
│ │  Providers  │  MCP  │  Prompts  │  Skills  │  MCO  │  Epistemic    │
│ │                                   ─────────────────────────────────  │
│ │                                   └─ Handoff  │  Sessions  │ Verify  │
│ │                                                                 │    │
│ └─────────────────────────────────────────────────────────────────┘    │
│                   │ IPC (Tauri Commands)                                │
│                   │                                                    │
│ ┌─────────────────▼─────────────────────────────────────────────┐     │
│ │ Backend (Rust + Tauri)                                        │     │
│ ├───────────────────────────────────────────────────────────────┤     │
│ │                                                               │     │
│ │ Provider  │ MCP    │ Prompt │ Proxy │ MCO   │ Epistemic │     │     │
│ │ Service   │Service │Service │Service│Service│ Service   │     │     │
│ │                                                           │     │     │
│ │ Config Providers:                                         │     │     │
│ │  ├─ Claude Code                                           │     │     │
│ │  ├─ Codex                                                 │     │     │
│ │  ├─ Gemini CLI                                            │     │     │
│ │  ├─ Rovo Dev (NEW)                                        │     │     │
│ │  └─ Qwen CLI (NEW)                                        │     │     │
│ │                                                           │     │     │
│ └────────────────┬────────────────┬──────────────┬──────────┘     │
│                  │                │              │                 │
│ ┌────────────────▼──┐  ┌──────────▼──┐  ┌──────▼──────────┐      │
│ │  SQLite Database  │  │ JSON Files  │  │  Config Files  │      │
│ ├─────────────────────┤  ├────────────────┤  ├────────────────┤      │
│ │ EXISTING TABLES:    │  │ UI State   │  │ ~/.rovodev/    │      │
│ │  • providers        │  │ Window     │  │ ~/.qwen_cli/   │      │
│ │  • mcp_servers      │  │ Paths      │  │ ~/.claude/     │      │
│ │  • prompts          │  │            │  │ ~/.codex/      │      │
│ │  • skills           │  │            │  │ ~/.gemini/     │      │
│ │  • settings         │  │            │  └────────────────┘      │
│ │  • proxy_config     │  │            │                          │
│ │  • skill_repos      │  │            │                          │
│ │                     │  │            │                          │
│ │ NEW EMPIRICA TABLES:│  │            │                          │
│ │  • mco_profiles     │  │            │                          │
│ │  • personas         │  │            │                          │
│ │  • cascade_styles   │  │            │                          │
│ │  • provider_mco_cfg │  │            │                          │
│ │  • cascade_sessions │  │            │                          │
│ │  • epistemic_assess │  │            │                          │
│ │  • handoff_reports  │  │            │                          │
│ └─────────────────────┘  └────────────────┘  └────────────────┘      │
│           │                                                       │     │
│           └─────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │  Git Repository │
                              │  & Git Notes    │
                              │                 │
                              │ refs/notes/     │
                              │ empirica/...    │
                              └─────────────────┘
                                       ▲
                                       │
                         ┌─────────────┴──────────────┐
                         │ Epistemic Service reads    │
                         │ & verifies git notes for   │
                         │ distributed audit trail    │
                         └────────────────────────────┘
```

---

## Data Flow: Provider Switch with MCO

```
User clicks "Switch Provider" in GUI
         │
         ▼
┌──────────────────────┐
│ Tauri Command:       │
│ switch_provider_with │
│ _mco(app_type, id)   │
└──────────────────┬───┘
                   │
         ┌─────────▼──────────┐
         │ 1. Query SQLite:   │
         │   Get provider     │
         │   Get MCO config   │
         │   Get profile      │
         │   Get persona      │
         │   Get cascade_style│
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────────────────────┐
         │ 2. Prepare config data:            │
         │   - API key                        │
         │   - MCO bias corrections           │
         │   - Persona settings               │
         │   - Empirica system prompt         │
         │   - CASCADE style preferences      │
         └─────────┬──────────────────────────┘
                   │
         ┌─────────▼──────────────────────────┐
         │ 3. Write to config file:           │
         │   - ~/.rovodev/config.yml          │
         │   - ~/.qwen_cli/config.json        │
         │   - ~/.claude/config.yml           │
         │   - etc.                           │
         └─────────┬──────────────────────────┘
                   │
         ┌─────────▼──────────────────────────┐
         │ 4. Update SQLite:                  │
         │   - Set is_current = true          │
         │   - Log timestamp                  │
         │   - Update last_used               │
         └─────────┬──────────────────────────┘
                   │
         ┌─────────▼──────────────────────────┐
         │ 5. Return to GUI:                  │
         │   - Provider updated               │
         │   - MCO profile applied            │
         │   - Config ready                   │
         └─────────────────────────────────────┘
```

---

## Data Flow: CASCADE Session with Handoff

```
AI Agent (Claude Code) runs PREFLIGHT
         │
         ▼
┌──────────────────────────────┐
│ Empirica Framework:          │
│ - Run PREFLIGHT assessment   │
│ - Calculate 13 vectors       │
│ - Get git notes ready        │
└──────────────┬───────────────┘
               │
         ┌─────▼──────────────────────┐
         │ 1. Store vectors in SQLite │
         │    via SessionDatabase      │
         │ 2. Write to git notes       │
         │ 3. Write to JSON logs       │
         └─────┬──────────────────────┘
               │
         ┌─────▼─────────────────────────────────┐
         │ Claude Code calls:                    │
         │ cc-switch/store_cascade_session       │
         │ (session_id, phase, vectors)          │
         └─────┬─────────────────────────────────┘
               │
         ┌─────▼─────────────────────────────────┐
         │ cc-switch Backend:                    │
         │ 1. Create cascade_sessions record     │
         │ 2. Store epistemic_assessments        │
         │ 3. Link to provider_mco_config        │
         │ 4. Verify git notes integrity        │
         └─────┬─────────────────────────────────┘
               │
         ┌─────▼─────────────────────────────────┐
         │ User switches to Sonnet (Rovo Dev)    │
         │ cc-switch switches provider           │
         │ (loads Sonnet's config + MCO)         │
         └─────┬─────────────────────────────────┘
               │
         ┌─────▼─────────────────────────────────┐
         │ Claude Code generates handoff report: │
         │ - PREFLIGHT vectors                  │
         │ - Learning trajectory                │
         │ - Key findings                       │
         │ - Unknowns to investigate            │
         │ - Recommended next steps              │
         └─────┬─────────────────────────────────┘
               │
         ┌─────▼─────────────────────────────────┐
         │ cc-switch stores handoff_reports      │
         │ - from_session_id (Code)             │
         │ - task_summary                       │
         │ - git_note_references                │
         └─────┬─────────────────────────────────┘
               │
         ┌─────▼─────────────────────────────────┐
         │ Sonnet (Rovo Dev) can:               │
         │ 1. Load previous session's vectors   │
         │ 2. Read git notes (distributed)      │
         │ 3. Access handoff report             │
         │ 4. Initialize with Code's learning  │
         │ 5. Continue from POSTFLIGHT state    │
         └─────────────────────────────────────┘
```

---

## Database Schema Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ EXISTING cc-switch TABLES                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  providers ◄────┐                                              │
│  ├─id           │                                              │
│  ├─app_type ────┼──────► provider_endpoints                   │
│  ├─name         │        ├─provider_id                        │
│  ├─settings_cfg │        ├─app_type                           │
│  ├─is_current   │        └─url                                │
│  └─meta ────────┼──────► provider_mco_config (NEW)            │
│                 │        ├─provider_id                        │
│  mcp_servers    │        ├─app_type                           │
│  ├─id           │        ├─mco_profile_id ─┐                 │
│  ├─name         │        ├─persona_id ────┐│                 │
│  ├─server_cfg   │        └─cascade_style  ││                 │
│  ├─tags         │                         │└─────┐           │
│  └─enabled_*    │                         │      │           │
│                 │                         │      │           │
│  prompts        │        mco_profiles (NEW) personas (NEW)   │
│  ├─id           │        ├─id              ├─id              │
│  ├─app_type ────┴──┐     ├─model_name      ├─name            │
│  ├─content         │     ├─reasoning       ├─threshold       │
│  └─enabled         │     └─bias_fields     └─settings        │
│                    │                                          │
│  settings          │     cascade_styles (NEW)                │
│  ├─key             │     ├─id                                │
│  └─value ◄─────────┘     ├─style_name                        │
│                          └─pattern                            │
│  proxy_config                                                 │
│  ├─enabled                                                    │
│  └─settings                 ┌─────────────────────────────┐  │
│                             │  CASCADE/Epistemic Tables  │  │
│  skill_repos               │  (NEW - Empirica)           │  │
│  ├─owner                   │                             │  │
│  └─name                    │  cascade_sessions ◄─────┐  │  │
│                            │  ├─id (UUID)           │  │  │
│  skills                    │  ├─ai_id ──────┐      │  │  │
│  ├─key                     │  ├─provider_id ┼─────┐│  │  │
│  └─installed_at            │  ├─phase       │     ││  │  │
│                            │  └─round       │     ││  │  │
└────────────────────────────┤                │     ││──┼──┘
                             │  epistemic     │     │└──┼─ mco config
                             │  _assessments  │     │   │
                             │  ├─id          │     │   │
                             │  ├─session_id ─┴─────┘   │
                             │  ├─vectors (JSON)        │
                             │  └─git_note_sha         │
                             │                         │
                             │  handoff_reports        │
                             │  ├─id                   │
                             │  ├─from_session_id ─────┘
                             │  ├─to_session_id
                             │  ├─task_summary
                             │  └─findings (JSON)
                             │
                             └─────────────────────────────┘
```

---

## Config File Integration Points

```
┌─ Provider selected in cc-switch
│
├─→ ~/.rovodev/config.yml
│   ├─ agent.modelId = <from provider>
│   ├─ agent.additionalSystemPrompt = <Empirica prompt from MCO>
│   ├─ agent.temperature = <from MCO profile>
│   └─ mcp.allowedMcpServers = <synced from SQLite>
│
├─→ ~/.qwen_cli/config.json
│   ├─ model = <from provider>
│   ├─ system_prompt = <Empirica prompt>
│   └─ mcp_config = <synced>
│
├─→ ~/.claude/config.yml
│   ├─ agent.modelId
│   └─ agent.additionalSystemPrompt
│
├─→ ~/.codex/config.json
│   └─ (similar structure)
│
└─→ ~/.gemini/settings.json
    └─ (similar structure)

All driven by:
┌──────────────────────────────┐
│ cc-switch SQLite Database    │
├──────────────────────────────┤
│ providers table              │
│ mco_profiles table           │
│ personas table               │
│ provider_mco_config table    │
└──────────────────────────────┘
```

---

## Technology Stack Summary

```
┌──────────────────────────────┐
│ Frontend Layer               │
├──────────────────────────────┤
│ React 18 + TypeScript        │
│ Tauri 2.0 Frontend           │
│ TailwindCSS UI               │
└──────────────────────────────┘
          │
          │ IPC (Tauri Commands)
          │
┌──────────────────────────────┐
│ Backend Layer (Rust)         │
├──────────────────────────────┤
│ Tauri 2.0 Backend            │
│ Tokio Async Runtime          │
│ rusqlite (SQLite driver)     │
└──────────────────────────────┘
          │
          ├─→ SQLite Database
          ├─→ JSON Config Files
          ├─→ Git Operations
          ├─→ File System
          └─→ Network (API calls)
```

---

## Synchronization Strategy

```
SQLite (Source of Truth)
    │
    ├─→ Write to config files (when provider switches)
    ├─→ Backup to JSON (periodic)
    ├─→ Store to git notes (Empirica integration)
    └─→ Sync to cloud (future feature)

Git Notes (Distributed Verification)
    │
    └─→ Queryable by any AI agent
        ├─ Verify epistemic states
        ├─ Access handoff reports
        └─ Track CASCADE phases
```

---

## Key Integration Points

| Component | Integration | Purpose |
|-----------|-----------|---------|
| **cc-switch SQLite** | Empirica SessionDatabase | Store MCO configs + CASCADE sessions |
| **cc-switch Config Providers** | Rovo Dev, Qwen CLI | Auto-write system prompts to config files |
| **cc-switch Prompt Manager** | Empirica System Prompts | Store Empirica v4.0 prompt per AI |
| **cc-switch MCP Manager** | Empirica MCP Tools | Sync MCP server configs across CLIs |
| **Git Notes** | Handoff Reports | Distributed cognitive audit trail |
| **Provider Switching** | MCO Loading | Apply bias corrections on switch |

---

This architecture enables **unified management of all AI CLIs with Empirica's epistemic tracking and multi-agent coordination**.

