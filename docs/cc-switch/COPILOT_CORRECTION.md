# Copilot Instructions Location - Correction

**Date:** 2025-12-06  
**Issue:** Documentation incorrectly stated Copilot prompt is in `~/.claude/CLAUDE.md`

---

## ✅ CORRECT Location

**Copilot CLI reads system prompts from:**
```
.github/copilot-instructions.md
```

**In Empirica project:**
```
/home/yogapad/empirical-ai/empirica/.github/copilot-instructions.md
```

**Format:** Markdown (624 lines)  
**Version:** Rovo Dev Edition v4.0 (but works for all Copilot CLIs)

---

## 📝 Key Differences from Claude Code

| Aspect | Claude Code | Copilot CLI |
|--------|-------------|-------------|
| **Location** | `~/.claude/CLAUDE.md` (global) | `.github/copilot-instructions.md` (per-repo) |
| **Scope** | System-wide | Repository-specific |
| **Format** | Markdown | Markdown |
| **Size** | 5,000+ lines | 624 lines (trimmed) |
| **Loading** | Always loaded | Loaded when in repo with `.github/` |

---

## 🎯 CC-Switch Integration Impact

### What Changes

**System Prompt Management:**

```rust
// OLD (incorrect assumption)
pub fn apply_system_prompt(&self, ai_id: &str, content: &str) -> Result<(), AppError> {
    // Write to ~/.copilot/system-prompts/<ai>.md
    let home = dirs::home_dir()?;
    let path = home.join(".copilot/system-prompts").join(format!("{}.md", ai_id));
    std::fs::write(path, content)?;
    Ok(())
}

// NEW (correct implementation)
pub fn apply_system_prompt(
    &self,
    workspace_root: &Path,
    ai_id: &str,
    content: &str
) -> Result<(), AppError> {
    // Write to <workspace>/.github/copilot-instructions.md
    let github_dir = workspace_root.join(".github");
    std::fs::create_dir_all(&github_dir)?;
    
    let path = github_dir.join("copilot-instructions.md");
    std::fs::write(path, content)?;
    
    Ok(())
}
```

### Implications

**✅ Pros:**
- Per-repository customization (better for multi-project workflows)
- Git-versioned (changes tracked, can review history)
- Team-shareable (all devs get same prompts)
- More flexible (different prompts per project)

**⚠️ Cons:**
- Need to specify workspace root
- Must create prompt for each repo
- Not global (can't set once for all projects)

---

## 🔄 Updated Implementation Plan

### Phase 6 Changes: Empirica Migration

```rust
// Updated import function
pub fn import_empirica_system_prompt(workspace_root: &Path) -> Result<(), AppError> {
    let db = Database::connect()?;
    
    // Read from .github/copilot-instructions.md (NOT ~/.claude/CLAUDE.md)
    let prompt_path = workspace_root.join(".github/copilot-instructions.md");
    
    if !prompt_path.exists() {
        return Err(AppError::Config(
            "copilot-instructions.md not found in workspace".into()
        ));
    }
    
    let prompt_content = std::fs::read_to_string(prompt_path)?;
    
    // Store in database
    db.conn.execute(
        "INSERT OR REPLACE INTO system_prompts (
            id, provider_type, prompt_name, content, version, ai_id, enabled, workspace_root
        ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)",
        params![
            format!("empirica-core-copilot-{}", workspace_root.display()),
            "copilot",
            "empirica-core",
            prompt_content,
            "4.0",
            "copilot-cli",
            true,
            workspace_root.to_str().unwrap()
        ]
    )?;
    
    Ok(())
}
```

### Updated Schema

```sql
-- Add workspace_root column to system_prompts
ALTER TABLE system_prompts ADD COLUMN workspace_root TEXT;

-- Index for fast workspace queries
CREATE INDEX idx_system_prompts_workspace ON system_prompts(workspace_root, provider_type);
```

---

## 🚀 Updated User Workflow

### Before (Incorrect Assumption)

```bash
# Switch to Copilot CLI
# System writes to ~/.copilot/system-prompts/claude-code.md
# Copilot CLI loads it (WRONG - doesn't work!)
```

### After (Correct Implementation)

```bash
# In CC-Switch GUI:
1. Select provider: "Copilot CLI"
2. Select workspace: "/home/yogapad/empirical-ai/empirica"
3. Apply system prompt: "empirica-core"
4. System writes to: /home/yogapad/empirical-ai/empirica/.github/copilot-instructions.md
5. Copilot CLI auto-loads when in that workspace ✅
```

---

## 📊 File Locations (CORRECTED)

```
Copilot CLI System Prompts:
  <workspace>/.github/copilot-instructions.md   # ✅ CORRECT
  
  NOT:
  ~/.copilot/system-prompts/<ai>.md            # ❌ WRONG (doesn't exist)

Copilot CLI Config:
  ~/.copilot/config.json                       # ✅ Correct (main config)
  ~/.copilot/mcp-config.json                   # ✅ Correct (MCP servers)

Empirica System Prompts:
  ~/.claude/CLAUDE.md                          # Claude Code (global)
  <workspace>/.github/copilot-instructions.md  # Copilot CLI (per-repo)
  ~/.gemini/system-prompt.txt                  # Gemini CLI (if supported)
```

---

## ✅ What This Means for Implementation

### No Impact on Timeline

**Still 9 hours total:**
- Database schema: +10 min (add workspace_root column)
- Provider implementation: Same (just different path)
- UI: +5 min (add workspace selector)
- Testing: Same

### Better User Experience

**Per-workspace prompts are BETTER:**
- Different projects = different prompts
- Git-versioned (can review changes)
- Team-sharable (commit to repo)
- More flexible than global prompt

### Updated Success Criteria

- [ ] CC-Switch writes to `.github/copilot-instructions.md`
- [ ] Supports multiple workspaces
- [ ] Shows which workspace is active
- [ ] Can sync same prompt to multiple workspaces
- [ ] Git-aware (detects .git directory)

---

## 📝 Action Items

### Update These Documents

1. **COPILOT_CONFIG_DEEP_DIVE.md**
   - ✅ Correct system prompt location
   - ✅ Add workspace_root concept
   - ✅ Update file locations summary

2. **COPILOT_IMPLEMENTATION_PLAN.md**
   - ✅ Update Phase 6 (Empirica migration)
   - ✅ Add workspace selector to UI
   - ✅ Update database schema

3. **RFC_THREE_CLI_PROVIDERS.md**
   - ✅ Note per-repo vs global prompt differences
   - ✅ Update Copilot CLI section

### Test Plan Addition

```bash
# Test workspace-specific prompts
mkdir -p /tmp/test-workspace-1/.github
mkdir -p /tmp/test-workspace-2/.github

# Write different prompts
echo "Prompt for workspace 1" > /tmp/test-workspace-1/.github/copilot-instructions.md
echo "Prompt for workspace 2" > /tmp/test-workspace-2/.github/copilot-instructions.md

# Verify Copilot CLI loads correct one
cd /tmp/test-workspace-1
github-copilot-cli --help  # Should use workspace 1 prompt

cd /tmp/test-workspace-2
github-copilot-cli --help  # Should use workspace 2 prompt
```

---

## 🎉 Summary

**Original error:** Assumed global prompt like Claude Code  
**Actual behavior:** Per-repository prompt in `.github/`  
**Impact:** Minor (10-15 min additional work)  
**Benefit:** Better UX (per-workspace customization)  

**Timeline still 9 hours total** ✅

---

**Status:** Corrected and ready to implement  
**Next:** Update main docs with correct paths

