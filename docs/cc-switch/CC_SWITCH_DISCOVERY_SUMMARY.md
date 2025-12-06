# CC-Switch Discovery & Integration Summary

**Date:** 2025-12-06
**Status:** ✅ Research Complete - Ready for Implementation Planning

---

## What We Found

### CC-Switch Project

**GitHub:** https://github.com/farion1231/cc-switch (Desktop GUI) & https://github.com/SaladDay/cc-switch-cli (CLI)

**Status:** Mature, production-ready (v3.8.2+)
- **15.3K+ stars** on GitHub
- **Daily trending** on TypeScript repos
- **Active development** - latest release Nov 28, 2025
- **Multi-language:** English, Chinese, Japanese
- **Cross-platform:** Windows, macOS, Linux

**What It Does:**
- Unified management for Claude Code, Codex, Gemini CLI
- Provider switching with one click
- MCP server management (shared across CLIs)
- System prompt management
- Proxy configuration
- Skills repository integration

**Architecture:**
- **Frontend:** React 18 + TypeScript in Tauri 2.0
- **Backend:** Rust (Tokio async)
- **Storage:** SQLite + JSON dual-layer (v3.8.0+)
- **Size:** ~38K lines of code

---

## Perfect Match for Empirica

### Why CC-Switch is Ideal for Us

1. **Already uses SQLite + JSON storage**
   - Exactly what Empirica needs
   - Can add Empirica tables directly to their schema
   - Already has migration system in place

2. **Supports multiple CLIs with unified config**
   - Claude Code ✅
   - Codex ✅
   - Gemini ✅
   - Can easily add: Rovo Dev ✅, Qwen ✅, Copilot ✅

3. **Provider abstraction pattern**
   - Clean separation between config providers
   - Easy to add new CLI support without touching core
   - All use same data model internally

4. **Mature, tested codebase**
   - 38K+ lines means proven architecture
   - Has error handling, migration system, testing
   - Can trust it handles edge cases

5. **Active community**
   - Recent updates (Nov 2025)
   - Issues addressed promptly
   - Cross-platform support well-tested

### What We Can Build On Top

**Phase 1: Extend to Rovo Dev & Qwen**
- Add `app_type='rovo'` and `app_type='qwen'` to database
- Create RovoDevConfigProvider and QwenCliConfigProvider
- ~500-800 lines of Rust code

**Phase 2: MCO Integration**
- Add 3 new tables: mco_profiles, personas, cascade_styles
- Add provider_mco_config linking table
- Create MCO UI in React
- ~1,500-2,000 lines of code

**Phase 3: Epistemic Handoff**
- Add 3 new tables: cascade_sessions, epistemic_assessments, handoff_reports
- Create EpistemicService in backend
- Build handoff UI with charts and git notes verification
- ~2,000-3,000 lines of code

**Phase 4: Multi-AI Coordination**
- Add cross-verification commands
- Create coordination dashboard
- Build learning curve analytics
- ~1,500-2,000 lines of code

---

## Technical Integration Plan

### Database Schema Addition (SQLite)

```sql
-- Empirica MCO Tables
mco_profiles               -- Model configuration profiles
personas                   -- Agent personas (implementer, researcher, etc.)
cascade_styles             -- CASCADE workflow styles
provider_mco_config        -- Links providers to MCO settings

-- Empirica CASCADE Tables
cascade_sessions           -- Tracks SESSION across provider switches
epistemic_assessments      -- PREFLIGHT/CHECK/POSTFLIGHT vectors
handoff_reports            -- Cross-AI continuity data
```

**Total: 7 new tables** to existing 8 tables in cc-switch

### Code Organization

```
cc-switch-empirica-fork/
├── src-tauri/src/
│   ├── services/
│   │   ├── rovo_dev.rs              (NEW: ~200 lines)
│   │   ├── qwen_cli.rs              (NEW: ~200 lines)
│   │   ├── mco_service.rs           (NEW: ~400 lines)
│   │   └── epistemic_service.rs     (NEW: ~600 lines)
│   │
│   └── database/
│       └── schema.rs                (MODIFIED: +200 lines)
│
└── src/
    ├── components/
    │   ├── providers/
    │   │   ├── RovoDevForm.tsx      (NEW: ~150 lines)
    │   │   └── QwenCliForm.tsx      (NEW: ~150 lines)
    │   │
    │   ├── mco/                     (NEW FOLDER)
    │   │   ├── MCOProfileSelector.tsx
    │   │   ├── PersonaSettings.tsx
    │   │   └── CascadeStyleConfig.tsx
    │   │
    │   └── epistemic/               (NEW FOLDER)
    │       ├── HandoffView.tsx
    │       ├── EpistemicHistory.tsx
    │       ├── LearningCurve.tsx
    │       └── CoordinationDashboard.tsx
    │
    └── pages/
        ├── MCOPage.tsx              (NEW)
        └── EpistemicHandoffPage.tsx (NEW)
```

---

## Implementation Timeline

### Phase 1: Foundation (2-3 weeks)
- [ ] Fork cc-switch repository
- [ ] Add Rovo Dev support
- [ ] Add Qwen CLI support
- [ ] Test provider switching across all 5 CLIs
- [ ] Document config file handling

### Phase 2: MCO System (2-3 weeks)
- [ ] Add MCO tables to SQLite schema
- [ ] Create MCO profile management API
- [ ] Build MCO UI components
- [ ] Integrate MCO with provider switching
- [ ] Test bias corrections applied correctly

### Phase 3: Epistemic Tracking (2-3 weeks)
- [ ] Add CASCADE session tables
- [ ] Create epistemic_service.rs
- [ ] Build handoff report generation
- [ ] Integrate git notes verification
- [ ] Create handoff UI with charts

### Phase 4: Multi-AI Coordination (2-3 weeks)
- [ ] Build cross-verification commands
- [ ] Create coordination dashboard
- [ ] Add learning curve analytics
- [ ] Test end-to-end handoff scenarios

**Total Estimate:** 8-12 weeks for full feature parity

---

## Comparison: CC-Switch vs Building From Scratch

| Aspect | CC-Switch Fork | Build New |
|--------|---|---|
| **Base code lines** | 38K (reusable) | 0 (start from scratch) |
| **Database** | ✅ SQLite + JSON proven | Need to design |
| **Provider support** | 3 existing + easy to extend | Need to implement all |
| **UI** | Modern React + Tauri proven | Need to design |
| **Configuration** | Pattern established | Need to design |
| **MCP Integration** | Already done | Need to implement |
| **Testing** | Existing test suite | Need to write |
| **Time to MVP** | 4-6 weeks | 12-16 weeks |
| **Community** | Active (15.3K stars) | None initially |
| **Maintenance burden** | Help upstream | Full responsibility |

**Verdict:** Using cc-switch saves **8-10 weeks of development time**

---

## Key Design Decisions

### 1. Fork or Contribute Upstream?

**Recommendation:** Start with fork, propose upstream later
- Fork allows us to move quickly with Empirica-specific features
- Once stabilized, can contribute MCO system back to original project
- cc-switch community likely interested in epistemic capabilities

### 2. Keep Empirica Tables Separate?

**Recommendation:** Yes, add Empirica-specific tables but don't modify existing ones
- Keeps changes minimal and non-breaking
- Easier to sync with upstream updates
- Clear separation of concerns

### 3. Configuration Format?

**Recommendation:** Store MCO in SQLite, write prompts to config files
- SQLite for structured data (profiles, personas, settings)
- Config files for actual system prompts and model params
- JSON for UI state (device-level)

### 4. Multi-AI Coordination Security?

**Recommendation:** Use git notes for verification (already distributed)
- Git notes are cryptographically verifiable
- No central database needed
- Works across different machines/networks
- Matches Empirica's distributed philosophy

---

## What Needs to Happen Next

### Immediate (This Week)
1. **Review this analysis** with team
2. **Decide:** Fork cc-switch or build new?
3. **Get approval** for Rovo Dev/Qwen support
4. **Create project board** for cc-switch-empirica fork

### Short Term (Next 2 Weeks)
1. **Fork cc-switch** repo
2. **Set up development environment**
3. **Analyze cc-switch codebase** in detail
4. **Plan Phase 1 sprints** (Rovo Dev + Qwen)
5. **Start Phase 1 development**

### Medium Term (Weeks 3-6)
1. **Complete Phase 1** (provider support)
2. **Begin Phase 2** (MCO system)
3. **Test provider switching** across all CLIs
4. **Document API** for new CLIs

---

## Risks & Mitigations

| Risk | Probability | Mitigation |
|------|------------|-----------|
| Upstream breaks API | Medium | Keep fork in sync with releases |
| SQLite schema conflicts | Low | Add prefixed tables (`empirica_*`) |
| Complex provider handling | Medium | Comprehensive testing per CLI |
| User data loss on update | Low | Implement robust migration system |
| Performance with 7 new tables | Low | Index key columns, profile queries |

---

## Success Criteria

### Phase 1: Foundation
- [ ] All 5 CLIs configurable in cc-switch
- [ ] Provider switching works without manual config editing
- [ ] MCP servers sync across all CLIs
- [ ] System prompts stored and applied per CLI

### Phase 2: MCO
- [ ] MCO profiles stored in SQLite
- [ ] Bias corrections applied on provider switch
- [ ] Persona settings loaded with provider
- [ ] CASCADE style preferences active

### Phase 3: Epistemic
- [ ] CASCADE sessions stored in database
- [ ] Handoff reports generated automatically
- [ ] Git notes verified for integrity
- [ ] Learning curves tracked per AI

### Phase 4: Multi-AI
- [ ] Cross-AI verification working
- [ ] Coordination dashboard functional
- [ ] Multiple AIs can verify each other's states
- [ ] Seamless handoff between agents

---

## Open Questions for Discussion

1. **Should we contribute this back to upstream cc-switch?**
   - Pro: Larger community benefits
   - Con: Upstream may not want Empirica-specific features

2. **How to handle competing system prompts?**
   - User's vs MCO's vs Empirica's
   - Priority order?

3. **What about other CLIs (Copilot, Continue)?**
   - Add in Phase 1 or later?

4. **Git notes storage location?**
   - Empirica repo or separate repo per AI?
   - How to sync across machines?

5. **Authentication & security?**
   - How to store API keys safely in SQLite?
   - Encryption at rest?

---

## References & Resources

### CC-Switch
- **Desktop:** https://github.com/farion1231/cc-switch
- **CLI:** https://github.com/SaladDay/cc-switch-cli
- **Latest Release:** v3.8.2 (2025-11-28)
- **Docs:** `README.md` in repo

### Empirica
- **Repo:** `/home/yogapad/empirical-ai/empirica`
- **MCO Config:** `empirica/config/mco/`
- **System Prompt:** `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`

### Technical Stack
- **Tauri:** https://tauri.app
- **Rust:** https://www.rust-lang.org
- **React:** https://react.dev
- **SQLite:** https://www.sqlite.org

---

## Conclusion

**CC-Switch is an excellent foundation for building Empirica's multi-AI coordination system.**

The project provides:
- ✅ Proven architecture (38K lines, 15.3K stars)
- ✅ Existing support for 3 CLIs
- ✅ SQLite + JSON storage we can extend
- ✅ Modern tech stack (Tauri, React, Rust)
- ✅ Active community and maintenance

By forking cc-switch and extending it with Empirica's MCO and epistemic capabilities, we can:
- Support 5+ AI CLIs from one interface
- Track epistemic states across agents
- Verify cognitive states via git notes
- Enable true multi-AI coordination
- Save 8-10 weeks vs building from scratch

**Recommendation: Proceed with cc-switch fork as foundation for Empirica Multi-AI System.**

---

**Next Step:** Schedule planning meeting to discuss implementation approach and assign tasks.

