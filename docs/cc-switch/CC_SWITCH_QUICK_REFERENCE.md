# CC-Switch + Empirica Quick Reference

---

## What is CC-Switch?

**Multi-CLI manager** for switching between Claude Code, Codex, Gemini (and soon: Rovo Dev, Qwen)

- **GUI App:** Desktop interface (Tauri)
- **CLI Tool:** Command-line management
- **Database:** SQLite + JSON storage
- **Latest:** v3.8.2 (Nov 2025)
- **Size:** 38K lines of code
- **Stars:** 15.3K on GitHub

---

## How It Works Currently

```
User selects provider in GUI
    ↓
Backend queries SQLite database
    ↓
Reads provider config + MCP servers + prompts
    ↓
Writes to Claude Code config (~/.claude/config.yml)
    ↓
Writes to Gemini config (~/.gemini/settings.json)
    ↓
Switches active CLI instantly
```

---

## Database Tables (Current)

| Table | Purpose | Rows |
|-------|---------|------|
| `providers` | AI CLI configs | Many |
| `mcp_servers` | MCP server definitions | Many |
| `prompts` | System prompts | Many |
| `skills` | Installed skills | Many |
| `skill_repos` | Skill repositories | Few |
| `settings` | Key-value config | Few |
| `proxy_config` | Proxy server setup | 1 |
| `provider_endpoints` | Alternative endpoints | Few |

---

## Proposed Empirica Tables (New)

| Table | Purpose | Rows |
|-------|---------|------|
| `mco_profiles` | Model profiles (Haiku, Sonnet, etc.) | Few |
| `personas` | Agent personas (implementer, researcher) | Few |
| `cascade_styles` | CASCADE workflow styles | Few |
| `provider_mco_config` | Links providers → MCO settings | Many |
| `cascade_sessions` | CASCADE workflow sessions | Many |
| `epistemic_assessments` | PREFLIGHT/CHECK/POSTFLIGHT vectors | Many |
| `handoff_reports` | Cross-AI handoff data | Many |

**Total New Tables:** 7
**Total Existing Tables:** 8
**Grand Total:** 15 tables

---

## Four-Phase Implementation

### Phase 1: Foundation (2-3 weeks)
**Goal:** Support 5+ CLIs with unified management

**Tasks:**
- Add Rovo Dev config provider
- Add Qwen CLI config provider
- Test switching across all 5
- Document config file handling

**Result:** `app_type` field supports: claude, codex, gemini, rovo, qwen

---

### Phase 2: MCO System (2-3 weeks)
**Goal:** Store and apply model configurations

**Tasks:**
- Add MCO tables to schema
- Create MCO profile UI
- Load bias corrections on switch
- Apply persona settings

**Result:** When switching to Sonnet, automatically load Sonnet's MCO profile

---

### Phase 3: Epistemic Handoff (2-3 weeks)
**Goal:** Track CASCADE sessions and generate handoffs

**Tasks:**
- Add CASCADE tables
- Create epistemic_service.rs
- Build handoff report generator
- Integrate git notes verification

**Result:** Code completes POSTFLIGHT → report generated → Sonnet loads handoff

---

### Phase 4: Multi-AI Coordination (2-3 weeks)
**Goal:** Enable agents to verify each other's states

**Tasks:**
- Build cross-verification commands
- Create coordination dashboard
- Add learning curve analytics
- Test handoff scenarios

**Result:** Sonnet can query Code's vectors, Qwen can verify both

---

## Key Integration Points

```
┌─────────────────────────────┐
│  cc-switch GUI (React)      │
├─────────────────────────────┤
│  New Pages/Tabs:            │
│  • MCO Configuration        │
│  • Epistemic Handoff        │
│  • Coordination Dashboard   │
└──────────┬──────────────────┘
           │ Tauri IPC
┌──────────▼──────────────────┐
│  Backend (Rust)             │
├─────────────────────────────┤
│  New Services:              │
│  • MCO Service              │
│  • Epistemic Service        │
│  • RovoDev Provider         │
│  • Qwen Provider            │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│  SQLite Database            │
├─────────────────────────────┤
│  New Tables:                │
│  • mco_profiles             │
│  • personas                 │
│  • cascade_styles           │
│  • provider_mco_config      │
│  • cascade_sessions         │
│  • epistemic_assessments    │
│  • handoff_reports          │
└─────────────────────────────┘
```

---

## Empirica Integration Points

### 1. System Prompts
```
MCO Profile → Empirica System Prompt v4.0
    ↓
Stored in SQLite prompts table
    ↓
Applied when writing config files
    ↓
Each CLI gets tailored prompt + MCO settings
```

### 2. CASCADE Sessions
```
Empirica CASCADE workflow
    ↓
Stores vectors in cc-switch database
    ↓
Creates handoff_reports
    ↓
Git notes contains checkpoint JSON
```

### 3. Multi-AI Coordination
```
Agent A completes work
    ↓
cc-switch stores CASCADE session
    ↓
Generates handoff report
    ↓
Agent B switches provider
    ↓
cc-switch loads previous session
    ↓
Agent B resumes with full context
```

---

## Code Structure

### Rust Backend (src-tauri/src/)

**New files:**
- `services/rovo_dev.rs` (200 lines)
- `services/qwen_cli.rs` (200 lines)
- `services/mco_service.rs` (400 lines)
- `services/epistemic_service.rs` (600 lines)

**Modified files:**
- `database/schema.rs` (+200 lines for new tables)

**Total new Rust:** ~1,600 lines

### React Frontend (src/)

**New components:**
- `components/providers/RovoDevForm.tsx` (150 lines)
- `components/providers/QwenCliForm.tsx` (150 lines)
- `components/mco/*` (300-400 lines)
- `components/epistemic/*` (500-600 lines)

**New pages:**
- `pages/MCOPage.tsx` (200 lines)
- `pages/EpistemicHandoffPage.tsx` (300 lines)

**Total new React:** ~1,600-1,800 lines

---

## CLI Support Timeline

| CLI | Current | Phase 1 | Phase 2+ |
|-----|---------|---------|----------|
| Claude Code | ✅ Full | ✅ Improved | ✅ With MCO |
| Codex | ✅ Full | ✅ Improved | ✅ With MCO |
| Gemini | ✅ Full (v3.7+) | ✅ Improved | ✅ With MCO |
| Rovo Dev | ❌ Not yet | ✅ Added | ✅ Full support |
| Qwen CLI | ❌ Not yet | ✅ Added | ✅ Full support |
| Copilot | ❌ Not yet | 🔄 Planned | ✅ Possible |

---

## Database Schema Summary

### Before Integration
```
8 tables:
- providers, mcp_servers, prompts, skills
- skill_repos, settings, proxy_config, provider_endpoints
```

### After Integration
```
15 tables:
- 8 existing (untouched)
- 7 new Empirica tables
```

### Key Linking
```
provider → provider_mco_config → mco_profiles
                               → personas
                               → cascade_styles

cascade_sessions → epistemic_assessments
                → handoff_reports
```

---

## Performance Considerations

| Query | Complexity | Index Strategy |
|-------|-----------|-----------------|
| Get current provider | O(1) | `PRIMARY KEY (id, app_type)` |
| Get MCO for provider | O(1) | Foreign key efficient |
| List sessions by AI | O(n) | Index on `ai_id` |
| Get assessments by session | O(n) | Index on `session_id` |
| Find handoff reports | O(n) | Index on `from_ai_id` + `created_at` |

**Expected:** <100ms queries even with thousands of records

---

## Migration Strategy

### Data Preservation
- Existing provider, MCP, prompt data: **untouched**
- New tables: **created empty** on first run
- Backward compatible: Old cc-switch works without new tables

### Upgrade Path
```
v3.8.2 cc-switch
    ↓
cc-switch-empirica fork (v0.1)
    ↓
Run migration (adds 7 tables)
    ↓
All existing data preserved
    ↓
New features available
```

---

## Success Checklist

### Phase 1
- [ ] Rovo Dev config reads/writes work
- [ ] Qwen CLI config reads/writes work
- [ ] All 5 CLIs appear in provider list
- [ ] Switching works without manual editing
- [ ] Config files updated correctly

### Phase 2
- [ ] MCO profiles stored in SQLite
- [ ] Bias corrections applied on switch
- [ ] Persona settings load with provider
- [ ] System prompts vary by MCO

### Phase 3
- [ ] CASCADE sessions stored automatically
- [ ] Handoff reports generated
- [ ] Git notes verified correctly
- [ ] Learning curves tracked

### Phase 4
- [ ] Cross-AI verification working
- [ ] Coordination dashboard functional
- [ ] Multiple AIs can verify each other
- [ ] Seamless handoff between agents

---

## Key Decisions

| Decision | Recommendation | Rationale |
|----------|---|---|
| **Fork or contribute?** | Start with fork | Move fast, sync upstream later |
| **Table location?** | New `empirica_*` tables | Keep changes minimal |
| **Config format?** | SQLite + files | Structured + human-readable |
| **Security?** | Git notes + SQL params | No injection, distributed |
| **Versioning?** | Same as cc-switch | Keep in sync with upstream |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| **Upstream API changes** | Keep fork in sync with releases |
| **Data loss on update** | Comprehensive migration testing |
| **Performance issues** | Index all foreign keys + test at scale |
| **CLI config format changes** | Abstract in ConfigProvider pattern |
| **Git notes unavailable** | Fall back to SQLite (already works) |

---

## Time Estimates

| Task | Estimate |
|------|----------|
| Rovo Dev support | 1 week |
| Qwen CLI support | 1 week |
| MCO system | 2 weeks |
| Epistemic handoff | 2 weeks |
| Multi-AI coordination | 2 weeks |
| Testing & docs | 2 weeks |
| **Total** | **10 weeks** |

**vs. Building from Scratch:** 18-22 weeks

**Savings:** 8-12 weeks

---

## Next Immediate Actions

1. **Review:** Discuss this plan with team
2. **Approve:** Get sign-off on fork vs upstream approach
3. **Setup:** Create project repository and board
4. **Planning:** Detailed sprint planning for Phase 1
5. **Start:** Begin Rovo Dev support implementation

---

## Resources

### Repositories
- **cc-switch (Desktop):** https://github.com/farion1231/cc-switch
- **cc-switch-cli:** https://github.com/SaladDay/cc-switch-cli
- **Empirica:** `/home/yogapad/empirical-ai/empirica`

### Documentation
- `/tmp/CC_SWITCH_EMPIRICA_INTEGRATION_PLAN.md` — Full technical plan
- `/tmp/CC_SWITCH_EMPIRICA_ARCHITECTURE.md` — System design
- `/tmp/CC_SWITCH_DISCOVERY_SUMMARY.md` — Complete analysis

---

**Status:** Ready for team discussion and implementation planning.

