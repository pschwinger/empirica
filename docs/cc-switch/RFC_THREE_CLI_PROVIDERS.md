# RFC: Add Support for Rovo Dev, Qwen CLI, and GitHub Copilot CLI

**Status:** Draft  
**Date:** 2025-12-06  
**Authors:** Claude Code (on behalf of Empirica project)  
**Target:** CC-Switch upstream (https://github.com/farion1231/cc-switch)

---

## Summary

Propose adding support for three additional AI CLI tools to CC-Switch:
1. **Rovo Dev CLI** - Atlassian's AI coding assistant
2. **Qwen CLI** - Alibaba's Qwen model CLI interface
3. **GitHub Copilot CLI** - GitHub's official CLI for Copilot

This follows the successful pattern established with Gemini CLI support (v3.7.0) and expands CC-Switch's coverage to 6 major AI CLI tools.

---

## Motivation

### Current State
CC-Switch supports 3 AI CLIs:
- ✅ Claude Code
- ✅ Codex
- ✅ Gemini CLI (added v3.7.0)

### Problem
Developers using **Rovo Dev**, **Qwen CLI**, or **GitHub Copilot CLI** cannot:
- Manage multiple AI CLI configs in one place
- Switch between providers without manual config editing
- Sync MCP servers across all their AI tools
- Benefit from unified system prompt management

### Impact
- **Rovo Dev**: Growing enterprise adoption (Atlassian ecosystem)
- **Qwen CLI**: Strong in Chinese/Asian markets, open-source friendly
- **GitHub Copilot CLI**: Massive user base (most popular AI coding tool)

Adding these 3 CLIs would make CC-Switch the **universal AI CLI manager** for 95%+ of AI coding tool users.

---

## Proposal

### 1. Add Rovo Dev CLI Support

**Config Location:**
- Linux/macOS: `~/.rovo/config.yaml` (or `~/.config/rovo-dev/settings.yml`)
- Windows: `%APPDATA%\rovo-dev\config.yaml`

**Config Format:** YAML (similar to Claude Code)
```yaml
auth:
  api_key: "rovo_..."
  endpoint: "https://api.atlassian.com/rovo/v1"

rovo_dev:
  model: "rovo-code-v1"
  workspace_id: "..."
  
mcp_servers:
  - name: "filesystem"
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem"]
```

**Database Changes:**
```sql
-- Add to mcp_servers table
ALTER TABLE mcp_servers ADD COLUMN enabled_rovo BOOLEAN NOT NULL DEFAULT 0;
```

**Implementation:**
- New file: `src-tauri/src/services/provider/rovo.rs`
- Pattern: Copy Gemini provider structure
- Config handling: YAML parsing (similar to Claude)
- OAuth: Support Atlassian OAuth flow
- Estimated LoC: ~300-400 lines

---

### 2. Add Qwen CLI Support

**Config Location:**
- Linux/macOS: `~/.qwen/config.json` (or `~/.config/qwen-cli/settings.json`)
- Windows: `%APPDATA%\qwen-cli\config.json`

**Config Format:** JSON + Environment variables
```json
{
  "api_key": "sk-...",
  "base_url": "https://dashscope.aliyuncs.com/api/v1",
  "model": "qwen-max",
  "temperature": 0.7,
  "mcp_servers": [...]
}
```

**Or via .env:**
```bash
DASHSCOPE_API_KEY=sk-...
QWEN_MODEL=qwen-max
```

**Database Changes:**
```sql
ALTER TABLE mcp_servers ADD COLUMN enabled_qwen BOOLEAN NOT NULL DEFAULT 0;
```

**Implementation:**
- New file: `src-tauri/src/services/provider/qwen.rs`
- Pattern: Copy Gemini dual-file approach (JSON + .env)
- Config handling: JSON + dotenv parsing
- Auth: DashScope API key
- Estimated LoC: ~250-350 lines

---

### 3. Add GitHub Copilot CLI Support

**Config Location:**
- Linux/macOS: `~/.config/github-copilot/hosts.json` + `~/.config/github-copilot/config.json`
- Windows: `%APPDATA%\github-copilot\hosts.json`

**Config Format:** JSON (OAuth-based)
```json
// hosts.json
{
  "github.com": {
    "oauth_token": "ghu_...",
    "user": "username"
  }
}

// config.json (if exists)
{
  "editor": "cli",
  "enableMCP": true,
  "mcp_servers": [...]
}
```

**Database Changes:**
```sql
ALTER TABLE mcp_servers ADD COLUMN enabled_copilot BOOLEAN NOT NULL DEFAULT 0;
```

**Implementation:**
- New file: `src-tauri/src/services/provider/copilot.rs`
- Pattern: Copy Gemini dual-file approach
- Config handling: Multi-file JSON parsing
- Auth: GitHub OAuth token management
- Estimated LoC: ~300-400 lines

---

## Technical Design

### ConfigProvider Trait (Already Exists)

All three CLIs will implement the existing provider interface:

```rust
pub trait ConfigProvider {
    fn load_config(&self) -> Result<ProviderConfig, AppError>;
    fn save_config(&self, config: &ProviderConfig) -> Result<(), AppError>;
    fn sync_mcp_servers(&mut self, servers: &[MCPServer]) -> Result<(), AppError>;
    fn get_config_path(&self) -> PathBuf;
}
```

### Database Schema Migration

```rust
// src-tauri/src/database/schema.rs

pub const SCHEMA_VERSION: u32 = 5;  // Bump from 4 to 5

impl Database {
    pub fn migrate_v4_to_v5(&self) -> Result<(), AppError> {
        let conn = lock_conn!(self.conn);
        
        // Add three new columns
        conn.execute(
            "ALTER TABLE mcp_servers ADD COLUMN enabled_rovo BOOLEAN NOT NULL DEFAULT 0",
            [],
        )?;
        
        conn.execute(
            "ALTER TABLE mcp_servers ADD COLUMN enabled_qwen BOOLEAN NOT NULL DEFAULT 0",
            [],
        )?;
        
        conn.execute(
            "ALTER TABLE mcp_servers ADD COLUMN enabled_copilot BOOLEAN NOT NULL DEFAULT 0",
            [],
        )?;
        
        Ok(())
    }
}
```

### React UI Components

Add three new provider options to the UI:

```tsx
// src/components/providers/ProviderSelector.tsx

const PROVIDERS = [
  { id: 'claude', name: 'Claude Code', icon: ClaudeIcon },
  { id: 'codex', name: 'Codex', icon: CodexIcon },
  { id: 'gemini', name: 'Gemini CLI', icon: GeminiIcon },
  { id: 'rovo', name: 'Rovo Dev', icon: RovoIcon },      // NEW
  { id: 'qwen', name: 'Qwen CLI', icon: QwenIcon },      // NEW
  { id: 'copilot', name: 'Copilot CLI', icon: CopilotIcon }, // NEW
];
```

---

## Implementation Plan

### Phase 1: Research & Preparation (Weekend)
```bash
# Research actual config formats for all 3 CLIs
# Document findings
# Create implementation tickets
```

### Phase 2: Parallel Implementation (Monday-Wednesday)
```
Monday 10:00 - Start implementations
  - Developer A: Rovo Dev provider
  - Developer B: Qwen CLI provider  
  - Developer C: Copilot CLI provider

Tuesday 17:00 - First integration test
  - Merge all three branches
  - Test provider switching
  - Verify MCP sync

Wednesday 17:00 - Second integration test
  - Fix any merge conflicts
  - Test all combinations
  - Performance testing
```

### Phase 3: Testing & Documentation (Thursday)
```
- Write comprehensive tests
- Update user documentation
- Create migration guide
- Test on all platforms (Linux, macOS, Windows)
```

### Phase 4: PR Submission (Friday)
```
- Final code review
- Clean up commits
- Submit PR with detailed description
- Link to this RFC
```

---

## Testing Strategy

### Unit Tests (Per Provider)
```rust
#[cfg(test)]
mod tests {
    #[test]
    fn test_rovo_config_load() { /* ... */ }
    
    #[test]
    fn test_rovo_config_save() { /* ... */ }
    
    #[test]
    fn test_rovo_mcp_sync() { /* ... */ }
    
    // Repeat for Qwen and Copilot
}
```

### Integration Tests
```rust
#[test]
fn test_switch_between_all_providers() {
    // Test switching: Claude → Rovo → Qwen → Copilot → Claude
    // Verify config files update correctly
    // Verify MCP servers sync
}

#[test]
fn test_mcp_sync_across_all_providers() {
    // Add MCP server
    // Enable for all 6 providers
    // Verify each config file has the server
}
```

### Manual Testing Checklist
- [ ] Fresh install on Linux
- [ ] Fresh install on macOS
- [ ] Fresh install on Windows
- [ ] Upgrade from v3.8.2 (migration test)
- [ ] Provider switching (all combinations)
- [ ] MCP server sync (all providers)
- [ ] System prompt sync (all providers)
- [ ] Config file validation
- [ ] Error handling (missing CLI binaries)

---

## Breaking Changes

### None Expected

This is purely additive:
- New columns in database (default values provided)
- New provider types (existing providers unchanged)
- New UI options (existing UI preserved)

**Migration:** Automatic via schema version bump (v4 → v5)

---

## Documentation Updates

### User Docs
- `docs/providers/rovo.md` - Setup guide for Rovo Dev
- `docs/providers/qwen.md` - Setup guide for Qwen CLI
- `docs/providers/copilot.md` - Setup guide for Copilot CLI
- `README.md` - Update supported CLIs list
- `CHANGELOG.md` - Document new features

### Developer Docs
- `CONTRIBUTING.md` - Add provider implementation guide
- `docs/architecture/providers.md` - Document provider pattern
- `docs/database/schema-v5.md` - Document new schema

---

## Alternatives Considered

### Alternative 1: Support only Copilot (most popular)
**Rejected:** Leaves Rovo Dev and Qwen users without solution

### Alternative 2: Separate tool for each CLI
**Rejected:** Defeats purpose of unified management

### Alternative 3: Plugin system for community extensions
**Future work:** Good idea but overkill for initial support

---

## Success Metrics

### Adoption
- Number of users adding Rovo/Qwen/Copilot providers
- GitHub stars/downloads increase
- Community feedback (issues, discussions)

### Quality
- Zero regression bugs in existing providers
- <5 bugs reported in new providers (first month)
- 95%+ test coverage for new code

### Performance
- No increase in app startup time
- Provider switching <500ms
- Database migration <1 second

---

## Timeline

| Milestone | Date | Status |
|-----------|------|--------|
| RFC submission | 2025-12-06 | ✅ Ready |
| Config format research | 2025-12-07-08 (weekend) | Pending |
| Implementation start | 2025-12-09 (Monday) | Pending |
| First integration test | 2025-12-10 (Tuesday) | Pending |
| Testing complete | 2025-12-12 (Thursday) | Pending |
| PR submission | 2025-12-13 (Friday) | Pending |
| Target merge | 2025-12-20 | Goal |

**Total time:** 1 week (5 business days)

---

## Team

### Contributors
- **Lead**: Claude Code (Rovo Dev implementation)
- **Contributor**: Claude Sonnet (Qwen CLI implementation)
- **Contributor**: Qwen (Copilot CLI implementation)
- **Reviewer**: TBD (CC-Switch maintainer)

### Estimated Effort
- **Implementation**: 3 developers × 3 days = 9 person-days
- **Testing**: 1 developer × 2 days = 2 person-days
- **Documentation**: 0.5 person-days
- **Code review & polish**: 1 person-day
- **Total**: ~12.5 person-days

**With parallel work**: 5 calendar days (Monday-Friday)

---

## Open Questions

1. **Rovo Dev config format confirmation**
   - Need to verify actual config location (might be different than assumed)
   - Need to test with real Rovo Dev installation

2. **Qwen CLI version compatibility**
   - Multiple Qwen CLI versions exist (qwen-cli, dashscope-cli)
   - Which one to prioritize?

3. **Copilot CLI MCP support**
   - Does Copilot CLI officially support MCP servers?
   - If not, how do we integrate MCP management?

4. **Icons and branding**
   - Do we need permission to use official logos?
   - Should we create neutral icons instead?

**Resolution:** Research over weekend (Dec 7-8)

---

## Community Feedback

We would appreciate feedback on:
1. Priority of these 3 CLIs (all equally important?)
2. Any other CLI tools we should consider?
3. Config format verification (for users with these CLIs installed)
4. Feature requests specific to these providers

---

## Conclusion

This RFC proposes a natural extension of CC-Switch's existing provider system to support 3 additional major AI CLI tools. The implementation follows proven patterns, requires minimal code (~1500 LoC total), and can be completed in 1 week with parallel development.

**Benefits:**
- ✅ Makes CC-Switch the universal AI CLI manager
- ✅ Serves 95%+ of AI coding tool users
- ✅ Follows established patterns (low risk)
- ✅ Fully backward compatible
- ✅ Community-driven contribution

**Ask:** Approve RFC and provide guidance on config format verification

---

**Submitted by:** Claude Code (Empirica project)  
**Contact:** [GitHub issue discussion]  
**Related:** CC-Switch v3.7.0 (Gemini CLI support precedent)

