# CC-Switch One-Week Sprint - Quick Start

**Sprint:** Monday-Friday
**Goal:** Upstream-ready PR for Rovo Dev + Qwen CLI + Copilot CLI support
**Team:** Code + Sonnet + Qwen
**Success:** 6 fully-supported CLIs, comprehensive tests, zero breaking changes

---

## The 5-Day Plan at a Glance

```
MON: RFC + Codebase analysis → Setup
TUE: 3 parallel implementations → Core code done
WED: Integration testing → All tests passing
THU: Documentation + code review → Polish
FRI: Final QA + PR submission → Ready for upstream
```

---

## Your Roles

### Claude Code (You)
- **Rovo Dev** provider + UI form
- **RFC issue** creation
- **PR coordination**
- **Integration lead**

### Claude Sonnet
- **Qwen CLI** provider + UI form
- **Architecture review**
- **Code quality**
- **Documentation review**

### Qwen
- **Copilot CLI** provider + UI form
- **Test suite** (150+ tests)
- **QA verification**
- **Edge case coverage**

---

## Monday Morning Checklist

```
☐ Create RFC issue on farion1231/cc-switch
☐ Clone cc-switch repository
☐ Analyze GeminiConfigProvider as template
☐ Research Rovo Dev config format (~/.rovodev/config.yml)
☐ Research Qwen CLI config format
☐ Research Copilot CLI config format
☐ Create shared coordination doc
☐ Plan AppType enum changes
☐ Daily standup setup
```

---

## Core Deliverables

### Code (Rust)
- `src-tauri/src/services/provider/rovo_dev.rs` (350 lines)
- `src-tauri/src/services/provider/qwen_cli.rs` (350 lines)
- `src-tauri/src/services/provider/copilot_cli.rs` (350 lines)
- Shared infrastructure updates (200 lines)

### UI (React/TypeScript)
- `src/components/providers/RovoDevForm.tsx` (150 lines)
- `src/components/providers/QwenCliForm.tsx` (150 lines)
- `src/components/providers/CopilotCliForm.tsx` (150 lines)

### Tests
- 150+ new unit tests
- 50+ integration tests
- Feature parity verification
- Edge case coverage

### Documentation
- README.md updates (add 3 new CLIs)
- Config guides (3 docs)
- Screenshots (3 images)
- Troubleshooting guide
- CHANGELOG update

---

## Daily Template

### Morning Standup (09:30, 15 min)
- What's done
- What's today
- Blockers
- Dependencies

### Afternoon Sync (17:00, optional)
- Progress check
- Tomorrow planning
- Cross-AI coordination

---

## Key Files to Understand

```
cc-switch/
├── src-tauri/src/services/provider/
│   ├── gemini_auth.rs     ← Reference for auth handling
│   ├── gemini.rs          ← Reference for provider pattern
│   └── mod.rs             ← Where to register new providers
├── src/components/providers/
│   └── GeminiForm.tsx     ← Reference for UI pattern
└── tests/                 ← Reference for test patterns
```

---

## Config File Locations

**Rovo Dev:**
```
~/.rovodev/config.yml
YAML format
Key sections:
  - agent.modelId
  - agent.additionalSystemPrompt
  - agent.temperature
  - mcp.allowedMcpServers
```

**Qwen CLI:**
```
~/.qwen_cli/config.json (or configurable)
JSON format
Key fields:
  - api_key
  - endpoint
  - model
  - mcp_servers
```

**Copilot CLI:**
```
Platform-specific location
Windows: Registry or config.json
Mac: ~/.copilot/config.json
Linux: ~/.copilot/config.json
```

---

## Feature Parity Checklist

All 6 CLIs must support:
- ✅ Config read/write
- ✅ MCP server extraction
- ✅ System prompt management
- ✅ Provider switching
- ✅ Error handling
- ✅ Unit tests
- ✅ Integration tests

---

## Code Review Process

**Tuesday EOD:**
- Code's Rovo → Sonnet reviews
- Sonnet's Qwen → Qwen reviews
- Qwen's Copilot → Code reviews

**Thursday EOD:**
- All AIs review all implementations
- Cross-check for patterns/consistency
- Verify feature parity

---

## Testing Strategy

### Tuesday (as you code)
- Unit tests for each component
- Basic functionality verification

### Wednesday (full integration)
- Integration tests (switching between all 6)
- MCP server sync tests
- Config file generation tests
- Regression tests (existing functionality)

### Thursday (edge cases)
- Missing config files
- Malformed JSON/YAML
- Partial configs
- Concurrent operations
- Performance tests

### Friday (final verification)
- All tests pass
- No regressions
- Feature parity confirmed
- Documentation matches code

---

## PR Submission Checklist (Friday)

Before submitting to upstream:
- [ ] All tests passing
- [ ] All code documented
- [ ] Screenshots included
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] No breaking changes
- [ ] Feature parity verified (6 CLIs)
- [ ] Backward compatibility confirmed
- [ ] Code follows upstream style
- [ ] Documentation complete

---

## Backup Plans (If Delays)

**If 50% done by EOD Tuesday:**
- Push some tests to Wednesday
- Reduce documentation polish
- Focus on core functionality

**If blockers Wednesday:**
- Extend integration to Thursday AM
- Skip non-critical features
- Get to "working" state

**If Thursday docs lag:**
- Minimal docs for PR
- Expand post-merge
- Community can help polish

**If Friday issues:**
- Submit PR with known issues
- Address feedback in Week 2
- Don't block on perfection

---

## Success Metrics

### End of Tuesday
- 3 provider implementations complete
- 3 UI components complete
- All code compiles

### End of Wednesday
- All tests passing (150+)
- Integration verified
- No regressions
- Feature parity confirmed

### End of Thursday
- Documentation complete
- Code polished
- Screenshots ready
- PR-ready

### End of Friday
- PR submitted to upstream
- RFC issue responded to
- Community engagement started
- All deliverables complete

---

## Communication

### Standup Template
```
STANDUP: [Name] - [Day]

Completed:
- Item 1
- Item 2

Today:
- Item 1
- Item 2

Blockers:
- Issue (if any)

Dependencies:
- Need X from Y
```

### Issue/PR Comments
- Professional and clear
- Link to related work
- Provide context
- Ask for feedback

---

## Important Notes

1. **Parallel work** - All 3 AIs work simultaneously
2. **One branch** - All in same feature branch
3. **Daily integration** - Merge every evening
4. **Test continuously** - Don't leave testing for end
5. **Document as you go** - Don't leave docs for Thursday
6. **Communicate daily** - Standups are critical
7. **Quality first** - Upstream expects excellence
8. **Community focus** - This is for everyone

---

## Post-Sprint Timeline

```
WEEK 2: Address PR feedback (if any)
WEEK 3: Merge to upstream + new release
WEEK 4: Fork for Empirica MCO layer
WEEK 5+: Add epistemic tracking to forked version
```

---

## Resources

- **cc-switch repo:** https://github.com/farion1231/cc-switch
- **Rovo Dev docs:** Check ~/.rovodev/config.yml structure
- **Qwen CLI docs:** Research qwen-cli config format
- **Copilot docs:** Microsoft Copilot CLI documentation
- **Sprint plan:** /tmp/ONE_WEEK_EXECUTION_PLAN.md
- **Upstream strategy:** /tmp/UPSTREAM_FIRST_STRATEGY.md

---

## Motivation

> This one-week sprint:
> 1. Makes CC-Switch the universal AI CLI switcher (6 platforms)
> 2. Benefits the entire open-source community
> 3. Establishes your credibility upstream
> 4. Creates perfect foundation for Empirica MCO layer
> 5. Demonstrates multi-AI orchestration power
> 6. Positions you as ecosystem leaders

**This is exactly the kind of work that changes industries.**

---

## Go Time 🚀

**Monday morning: RFC issue**
**Friday afternoon: PR submitted**
**In between: Build something awesome**

**Status:** Ready to execute
**Confidence:** HIGH (with 3 experienced AIs collaborating)
**Expected Outcome:** Upstream merge within 2 weeks

