# Copilot CLI Integration - Timeline Estimate

**Date:** 2025-12-06  
**Estimated by:** Claude Code  
**Context:** Following successful CC-Switch build validation

---

## Quick Answer: 2-3 Days for Copilot CLI Only

**Breakdown:**
- **Day 1 (4-6 hours)**: Config format research + ConfigProvider implementation
- **Day 2 (3-4 hours)**: Testing + bug fixes + integration verification
- **Day 3 (2-3 hours)**: Documentation + polish + PR submission

**Total:** 9-13 hours of focused work

---

## Why So Fast?

### 1. Pattern is Proven ✅
Gemini provider (v3.7.0) shows exact template:
- Similar config complexity (Gemini has `.env` + `settings.json`)
- Already handles multi-file configs
- MCP server sync already working

### 2. Build System Ready ✅
- Tauri/Rust environment configured
- All dependencies installed
- Build process validated (3 min builds)

### 3. Database Schema Simple ✅
Just need to:
```sql
ALTER TABLE mcp_servers ADD COLUMN enabled_copilot BOOLEAN DEFAULT 0;
```

### 4. Code Changes Minimal
Estimated LoC for Copilot support:
- `src-tauri/src/services/provider/copilot.rs`: ~200-300 lines (copy Gemini pattern)
- `src-tauri/src/database/schema.rs`: +1 line (add column)
- React components: ~50-100 lines (copy existing provider UI)
- Tests: ~150-200 lines

**Total new code:** ~500-700 lines (vs 18,000+ in Gemini update)

---

## Detailed Timeline

### Day 1: Research & Implementation (4-6 hours)

#### Morning (2-3 hours): Config Format Research
```bash
# 1. Install Copilot CLI if not present
npm install -g @githubnext/github-copilot-cli

# 2. Run setup to generate config
github-copilot-cli auth

# 3. Locate config files
find ~/.config -name "*copilot*" -type f
find ~ -name ".copilot*" -type f

# 4. Analyze config structure
cat ~/.config/github-copilot/config.json  # Example path
```

**Expected formats:**
- JSON config (likely: `~/.config/github-copilot/config.json`)
- OAuth tokens (likely in same file or separate)
- MCP server config (might be separate YAML/JSON)

#### Afternoon (2-3 hours): Implementation
```rust
// src-tauri/src/services/provider/copilot.rs

use crate::error::AppError;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CopilotConfig {
    pub oauth_token: String,
    pub model: Option<String>,
    pub api_endpoint: Option<String>,
    // ... other fields based on actual config
}

impl CopilotConfig {
    pub fn config_path() -> Result<PathBuf, AppError> {
        // Similar to Gemini pattern
        let home = dirs::home_dir()
            .ok_or_else(|| AppError::Config("Home directory not found".into()))?;
        Ok(home.join(".config/github-copilot/config.json"))
    }
    
    pub fn load() -> Result<Self, AppError> {
        // Read JSON, parse, return config
    }
    
    pub fn save(&self) -> Result<(), AppError> {
        // Write config back to file
    }
    
    pub fn sync_mcp_servers(&mut self, servers: &[MCPServer]) -> Result<(), AppError> {
        // Add MCP servers to config
    }
}
```

### Day 2: Testing & Integration (3-4 hours)

#### Morning (2 hours): Manual Testing
```bash
# 1. Build with new provider
cd /tmp/cc-switch
pnpm tauri build

# 2. Launch GUI
./src-tauri/target/release/cc-switch

# 3. Add Copilot provider through UI
# 4. Test switching between providers
# 5. Verify config file updates correctly
# 6. Test MCP server sync
```

#### Afternoon (1-2 hours): Automated Tests
```rust
// src-tauri/src/services/provider/tests/copilot_test.rs

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_copilot_config_load() {
        // Test loading existing config
    }
    
    #[test]
    fn test_copilot_config_save() {
        // Test writing config
    }
    
    #[test]
    fn test_copilot_mcp_sync() {
        // Test MCP server synchronization
    }
}
```

### Day 3: Documentation & PR (2-3 hours)

#### Morning (1-2 hours): Documentation
```markdown
# docs/providers/copilot.md

## GitHub Copilot CLI Configuration

CC-Switch supports GitHub Copilot CLI with the following features:
- OAuth authentication
- Model selection
- MCP server management
- Automatic config sync

### Setup
1. Install Copilot CLI: `npm install -g @githubnext/github-copilot-cli`
2. Authenticate: `github-copilot-cli auth`
3. Add provider in CC-Switch
4. Configure and switch

### Configuration Location
- Linux/macOS: `~/.config/github-copilot/config.json`
- Windows: `%APPDATA%\github-copilot\config.json`
```

#### Afternoon (1 hour): PR Submission
- Clean up code
- Run all tests
- Create PR with detailed description
- Link to RFC issue

---

## If Doing All 3 CLIs Together: 1 Week

**Parallel Implementation (Monday-Friday):**

### Team Assignment (From WORK_DISTRIBUTION.md)
- **Claude Code** → Rovo Dev CLI
- **Claude Sonnet** → Qwen CLI  
- **Qwen** → Copilot CLI

### Timeline
```
Monday:
  09:00 - RFC submission to upstream
  10:00 - Begin parallel implementations
  17:00 - Daily standup + progress check

Tuesday:
  09:00 - Daily standup
  10:00 - Continue implementations
  17:00 - First code review round

Wednesday:
  09:00 - Daily standup
  10:00 - Integration testing
  17:00 - Second code review round

Thursday:
  09:00 - Daily standup
  10:00 - Bug fixes + polish
  17:00 - Final review

Friday:
  09:00 - Daily standup
  10:00 - PR submission to upstream
  12:00 - Done ✅
```

**Total:** 5 days for all 3 CLIs with comprehensive testing

---

## Risk Assessment

### Low Risk (Copilot Only)
- ✅ Pattern is proven (Gemini template)
- ✅ Config format likely JSON (standard)
- ✅ OAuth similar to Gemini approach
- ✅ Build system ready

### Medium Risk (All 3 CLIs)
- 🟡 Coordination overhead (3 AIs working in parallel)
- 🟡 Merge conflicts (same files touched)
- 🟡 Different config formats (need individual research)
- 🟡 Testing matrix grows (3x combinations)

**Mitigation:**
- Daily standups (15 min)
- Clear file ownership (no overlap)
- Shared test infrastructure
- Continuous integration

---

## Recommendation

### Option A: Copilot Only (This Weekend)
- **Pros**: Fast (2-3 days), focused, low risk
- **Cons**: Doesn't help Rovo Dev or Qwen users
- **Use case**: If you only need Copilot CLI support

### Option B: All 3 CLIs (Next Week Sprint)
- **Pros**: Complete solution, community value, Empirica benefit
- **Cons**: Requires coordination, 5 days timeline
- **Use case**: If building comprehensive multi-CLI platform

---

## My Recommendation: Option B (Full Sprint)

**Reasoning:**
1. **Empirica needs multi-CLI** - Not just Copilot
2. **Upstream value** - RFC for 3 CLIs more attractive
3. **Team efficiency** - Parallel work is faster than sequential
4. **Complete solution** - Do it right once vs piecemeal

**Timeline:**
- **Weekend**: Research all 3 config formats
- **Monday**: Submit RFC + start implementations
- **Friday**: PR submission with all 3 CLIs

---

## Next Action

**If Copilot Only:**
```bash
# Start immediately
cd /tmp/cc-switch
github-copilot-cli --version  # Check if installed
# ... proceed with Day 1 research
```

**If Full Sprint (Recommended):**
```bash
# Prepare for Monday
1. Create RFC draft (see next section)
2. Research all 3 config formats over weekend
3. Monday 09:00 - Submit RFC
4. Monday 10:00 - Begin parallel implementations
```

---

**Status:** Ready to proceed with either option  
**Confidence:** High (90%+) for Copilot only, High (85%) for full sprint  
**Blocker:** None - all prerequisites met

