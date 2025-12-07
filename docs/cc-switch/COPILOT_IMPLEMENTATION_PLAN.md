# Copilot CLI Integration - Detailed Implementation Plan

**Date:** 2025-12-06  
**Context:** We're IN Copilot CLI, so this is our priority  
**Estimated Time:** 6-8 hours (1 focused day or 2-3 days part-time)

---

## 🎯 Goal

Implement Copilot CLI support in CC-Switch with full Empirica integration:
- MCP server management
- System prompt sync (CLAUDE.md)
- Skills sync (SKILL.md)
- Provider switching

---

## 📋 Implementation Phases

### Phase 1: Config Structure Analysis ✅ (DONE)

See: `COPILOT_CONFIG_DEEP_DIVE.md`

**Validated:**
- ✅ Config location: `~/.copilot/config.json`
- ✅ MCP config location: `~/.copilot/mcp-config.json`
- ✅ Structure: Standard JSON (easy to parse)
- ✅ Auth: GitHub OAuth (already working)

---

### Phase 2: Database Schema (1 hour)

**File:** `src-tauri/src/database/schema.rs`

**Changes needed:**

```rust
// 1. Bump schema version
pub const SCHEMA_VERSION: u32 = 5;  // From 4 to 5

// 2. Add migration function
pub fn migrate_v4_to_v5(&self) -> Result<(), AppError> {
    let conn = lock_conn!(self.conn);
    
    // Add Copilot column to mcp_servers
    conn.execute(
        "ALTER TABLE mcp_servers ADD COLUMN enabled_copilot BOOLEAN NOT NULL DEFAULT 0",
        [],
    )?;
    
    // Create system_prompts table
    conn.execute(
        "CREATE TABLE IF NOT EXISTS system_prompts (
            id TEXT PRIMARY KEY,
            provider_type TEXT NOT NULL,
            prompt_name TEXT NOT NULL,
            content TEXT NOT NULL,
            version TEXT,
            ai_id TEXT,
            enabled BOOLEAN DEFAULT 1,
            created_at INTEGER,
            updated_at INTEGER,
            UNIQUE(provider_type, prompt_name, ai_id)
        )",
        [],
    )?;
    
    // Create skills table
    conn.execute(
        "CREATE TABLE IF NOT EXISTS skills (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            category TEXT,
            version TEXT,
            enabled_claude BOOLEAN DEFAULT 0,
            enabled_gemini BOOLEAN DEFAULT 0,
            enabled_copilot BOOLEAN DEFAULT 0,
            created_at INTEGER,
            updated_at INTEGER
        )",
        [],
    )?;
    
    Ok(())
}

// 3. Update create_tables() to include new tables
```

**Testing:**
```bash
# Create test database
sqlite3 /tmp/test_schema.db < schema_v5.sql

# Verify structure
sqlite3 /tmp/test_schema.db ".schema mcp_servers"
sqlite3 /tmp/test_schema.db ".schema system_prompts"
sqlite3 /tmp/test_schema.db ".schema skills"
```

---

### Phase 3: Copilot Provider Implementation (3 hours)

**File:** `src-tauri/src/services/provider/copilot.rs` (NEW)

**Complete implementation:**

```rust
//! GitHub Copilot CLI provider implementation
//!
//! Manages Copilot CLI configuration including:
//! - Model selection
//! - GitHub authentication
//! - MCP server synchronization
//! - System prompt management
//! - Skills/capabilities sync

use crate::error::AppError;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::PathBuf;

/// Copilot CLI main configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CopilotConfig {
    pub banner: String,
    pub model: String,
    pub last_logged_in_user: Option<CopilotUser>,
    pub logged_in_users: Vec<CopilotUser>,
    pub trusted_folders: Vec<String>,
    pub render_markdown: bool,
    pub screen_reader: bool,
    pub theme: String,
}

/// GitHub user information
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CopilotUser {
    pub host: String,
    pub login: String,
}

/// MCP server configuration structure
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CopilotMCPConfig {
    #[serde(rename = "mcpServers")]
    pub mcp_servers: HashMap<String, MCPServerEntry>,
}

/// Individual MCP server entry
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MCPServerEntry {
    #[serde(rename = "type")]
    pub type_: String,
    pub command: String,
    pub args: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub env: Option<HashMap<String, String>>,
    pub tools: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
}

impl CopilotConfig {
    /// Get Copilot CLI config directory
    pub fn config_dir() -> Result<PathBuf, AppError> {
        let home = dirs::home_dir()
            .ok_or_else(|| AppError::Config("Home directory not found".into()))?;
        Ok(home.join(".copilot"))
    }
    
    /// Get main config file path
    pub fn config_path() -> Result<PathBuf, AppError> {
        Ok(Self::config_dir()?.join("config.json"))
    }
    
    /// Get MCP config file path
    pub fn mcp_config_path() -> Result<PathBuf, AppError> {
        Ok(Self::config_dir()?.join("mcp-config.json"))
    }
    
    /// Get system prompts directory
    pub fn system_prompts_dir() -> Result<PathBuf, AppError> {
        Ok(Self::config_dir()?.join("system-prompts"))
    }
    
    /// Load main configuration
    pub fn load() -> Result<Self, AppError> {
        let path = Self::config_path()?;
        
        if !path.exists() {
            return Err(AppError::Config(
                "Copilot CLI not configured. Run 'github-copilot-cli auth' first.".into()
            ));
        }
        
        let content = std::fs::read_to_string(&path)
            .map_err(|e| AppError::Config(format!("Failed to read config: {}", e)))?;
        
        let config: CopilotConfig = serde_json::from_str(&content)
            .map_err(|e| AppError::Config(format!("Failed to parse config: {}", e)))?;
        
        Ok(config)
    }
    
    /// Save main configuration
    pub fn save(&self) -> Result<(), AppError> {
        let path = Self::config_path()?;
        
        // Ensure directory exists
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent)
                .map_err(|e| AppError::Config(format!("Failed to create config dir: {}", e)))?;
        }
        
        let content = serde_json::to_string_pretty(self)
            .map_err(|e| AppError::Config(format!("Failed to serialize config: {}", e)))?;
        
        std::fs::write(&path, content)
            .map_err(|e| AppError::Config(format!("Failed to write config: {}", e)))?;
        
        Ok(())
    }
    
    /// Load MCP configuration
    pub fn load_mcp_config() -> Result<CopilotMCPConfig, AppError> {
        let path = Self::mcp_config_path()?;
        
        if !path.exists() {
            // Return empty config if file doesn't exist
            return Ok(CopilotMCPConfig {
                mcp_servers: HashMap::new(),
            });
        }
        
        let content = std::fs::read_to_string(&path)
            .map_err(|e| AppError::Config(format!("Failed to read MCP config: {}", e)))?;
        
        let config: CopilotMCPConfig = serde_json::from_str(&content)
            .map_err(|e| AppError::Config(format!("Failed to parse MCP config: {}", e)))?;
        
        Ok(config)
    }
    
    /// Save MCP configuration
    pub fn save_mcp_config(config: &CopilotMCPConfig) -> Result<(), AppError> {
        let path = Self::mcp_config_path()?;
        
        // Ensure directory exists
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        
        let content = serde_json::to_string_pretty(config)
            .map_err(|e| AppError::Config(format!("Failed to serialize MCP config: {}", e)))?;
        
        std::fs::write(&path, content)
            .map_err(|e| AppError::Config(format!("Failed to write MCP config: {}", e)))?;
        
        Ok(())
    }
    
    /// Sync MCP servers from database
    pub fn sync_mcp_servers(&self, servers: &[MCPServer]) -> Result<(), AppError> {
        let mut mcp_config = Self::load_mcp_config()?;
        
        // Remove all servers first (clean slate)
        mcp_config.mcp_servers.clear();
        
        // Add enabled servers
        for server in servers.iter().filter(|s| s.enabled_copilot) {
            let env = if !server.env_json.is_empty() {
                match serde_json::from_str::<HashMap<String, String>>(&server.env_json) {
                    Ok(map) => Some(map),
                    Err(e) => {
                        eprintln!("Warning: Failed to parse env for {}: {}", server.name, e);
                        None
                    }
                }
            } else {
                None
            };
            
            let entry = MCPServerEntry {
                type_: "local".to_string(),
                command: server.command.clone(),
                args: serde_json::from_str(&server.args_json)
                    .unwrap_or_else(|_| vec![]),
                env,
                tools: vec!["*".to_string()],
                description: server.description.clone(),
            };
            
            mcp_config.mcp_servers.insert(server.name.clone(), entry);
        }
        
        Self::save_mcp_config(&mcp_config)?;
        Ok(())
    }
    
    /// Apply system prompt
    pub fn apply_system_prompt(
        &self,
        ai_id: &str,
        content: &str,
        prompt_name: &str
    ) -> Result<(), AppError> {
        let prompts_dir = Self::system_prompts_dir()?;
        std::fs::create_dir_all(&prompts_dir)?;
        
        let filename = format!("{}-{}.md", ai_id, prompt_name);
        let prompt_path = prompts_dir.join(filename);
        
        std::fs::write(&prompt_path, content)
            .map_err(|e| AppError::Config(format!("Failed to write system prompt: {}", e)))?;
        
        Ok(())
    }
    
    /// Remove system prompt
    pub fn remove_system_prompt(&self, ai_id: &str, prompt_name: &str) -> Result<(), AppError> {
        let prompts_dir = Self::system_prompts_dir()?;
        let filename = format!("{}-{}.md", ai_id, prompt_name);
        let prompt_path = prompts_dir.join(filename);
        
        if prompt_path.exists() {
            std::fs::remove_file(&prompt_path)
                .map_err(|e| AppError::Config(format!("Failed to remove system prompt: {}", e)))?;
        }
        
        Ok(())
    }
    
    /// List all system prompts
    pub fn list_system_prompts(&self) -> Result<Vec<(String, String)>, AppError> {
        let prompts_dir = Self::system_prompts_dir()?;
        
        if !prompts_dir.exists() {
            return Ok(Vec::new());
        }
        
        let mut prompts = Vec::new();
        
        for entry in std::fs::read_dir(&prompts_dir)? {
            let entry = entry?;
            let path = entry.path();
            
            if path.extension().and_then(|s| s.to_str()) == Some("md") {
                if let Some(stem) = path.file_stem().and_then(|s| s.to_str()) {
                    // Parse "ai-id-prompt-name.md" format
                    if let Some(pos) = stem.rfind('-') {
                        let ai_id = stem[..pos].to_string();
                        let prompt_name = stem[pos+1..].to_string();
                        prompts.push((ai_id, prompt_name));
                    }
                }
            }
        }
        
        Ok(prompts)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;
    
    #[test]
    fn test_config_serialization() {
        let config = CopilotConfig {
            banner: "never".to_string(),
            model: "claude-sonnet-4.5".to_string(),
            last_logged_in_user: Some(CopilotUser {
                host: "https://github.com".to_string(),
                login: "testuser".to_string(),
            }),
            logged_in_users: vec![],
            trusted_folders: vec!["/test/path".to_string()],
            render_markdown: true,
            screen_reader: false,
            theme: "auto".to_string(),
        };
        
        let json = serde_json::to_string_pretty(&config).unwrap();
        assert!(json.contains("claude-sonnet-4.5"));
        
        let parsed: CopilotConfig = serde_json::from_str(&json).unwrap();
        assert_eq!(parsed.model, "claude-sonnet-4.5");
    }
    
    #[test]
    fn test_mcp_config_sync() {
        // Test MCP server synchronization logic
        let mut mcp_config = CopilotMCPConfig {
            mcp_servers: HashMap::new(),
        };
        
        // Add test server
        let entry = MCPServerEntry {
            type_: "local".to_string(),
            command: "python3".to_string(),
            args: vec!["server.py".to_string()],
            env: None,
            tools: vec!["*".to_string()],
            description: Some("Test server".to_string()),
        };
        
        mcp_config.mcp_servers.insert("test".to_string(), entry);
        
        assert_eq!(mcp_config.mcp_servers.len(), 1);
        assert!(mcp_config.mcp_servers.contains_key("test"));
    }
}
```

**Testing plan:**
```bash
# Unit tests
cd /tmp/cc-switch
cargo test --package cc-switch --lib services::provider::copilot

# Integration test
python3 << 'PYTHON'
import json
import tempfile
import os

# Create test config
test_config = {
    "banner": "never",
    "model": "claude-sonnet-4.5",
    "logged_in_users": [],
    "trusted_folders": [],
    "render_markdown": True,
    "theme": "auto"
}

with tempfile.TemporaryDirectory() as tmpdir:
    config_path = os.path.join(tmpdir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(test_config, f)
    
    # Verify round-trip
    with open(config_path) as f:
        loaded = json.load(f)
    
    assert loaded["model"] == "claude-sonnet-4.5"
    print("✅ Config serialization works!")
PYTHON
```

---

### Phase 4: React UI Components (2 hours)

**Files to create/modify:**

**1. `src/components/providers/CopilotProvider.tsx`** (NEW)

```tsx
import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

interface CopilotConfig {
  model: string;
  github_login?: string;
  trusted_folders: string[];
  render_markdown: boolean;
  theme: string;
}

export function CopilotProviderConfig() {
  const [config, setConfig] = useState<CopilotConfig | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadConfig();
  }, []);
  
  const loadConfig = async () => {
    try {
      const cfg = await invoke<CopilotConfig>('copilot_load_config');
      setConfig(cfg);
    } catch (e) {
      console.error('Failed to load Copilot config:', e);
    } finally {
      setLoading(false);
    }
  };
  
  const saveConfig = async () => {
    if (!config) return;
    
    try {
      await invoke('copilot_save_config', { config });
      // Show success message
    } catch (e) {
      console.error('Failed to save config:', e);
      // Show error message
    }
  };
  
  if (loading) return <div>Loading...</div>;
  if (!config) return <div>Copilot CLI not configured</div>;
  
  return (
    <div className="copilot-provider-config">
      <h3>Copilot CLI Configuration</h3>
      
      <div className="form-group">
        <label>Model</label>
        <select 
          value={config.model}
          onChange={(e) => setConfig({...config, model: e.target.value})}
        >
          <option value="claude-sonnet-4.5">Claude Sonnet 4.5</option>
          <option value="gpt-4">GPT-4</option>
          <option value="gpt-4-turbo">GPT-4 Turbo</option>
        </select>
      </div>
      
      <div className="form-group">
        <label>Trusted Folders</label>
        <textarea
          value={config.trusted_folders.join('\n')}
          onChange={(e) => setConfig({
            ...config,
            trusted_folders: e.target.value.split('\n').filter(l => l.trim())
          })}
          rows={5}
          placeholder="/path/to/project1\n/path/to/project2"
        />
      </div>
      
      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={config.render_markdown}
            onChange={(e) => setConfig({...config, render_markdown: e.target.checked})}
          />
          Render Markdown
        </label>
      </div>
      
      <div className="form-group">
        <label>Theme</label>
        <select
          value={config.theme}
          onChange={(e) => setConfig({...config, theme: e.target.value})}
        >
          <option value="auto">Auto</option>
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>
      </div>
      
      <button onClick={saveConfig}>Save Configuration</button>
    </div>
  );
}
```

**2. Update `src/components/providers/ProviderSelector.tsx`**

```tsx
// Add Copilot to provider list
const PROVIDERS = [
  { id: 'claude', name: 'Claude Code', icon: ClaudeIcon },
  { id: 'codex', name: 'Codex', icon: CodexIcon },
  { id: 'gemini', name: 'Gemini CLI', icon: GeminiIcon },
  { id: 'copilot', name: 'Copilot CLI', icon: CopilotIcon }, // NEW
];
```

**3. Create Copilot icon component**

---

### Phase 5: Tauri Commands (1 hour)

**File:** `src-tauri/src/main.rs`

```rust
#[tauri::command]
fn copilot_load_config() -> Result<CopilotConfig, String> {
    CopilotConfig::load()
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn copilot_save_config(config: CopilotConfig) -> Result<(), String> {
    config.save()
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn copilot_sync_mcp_servers(servers: Vec<MCPServer>) -> Result<(), String> {
    let config = CopilotConfig::load()
        .map_err(|e| e.to_string())?;
    
    config.sync_mcp_servers(&servers)
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn copilot_apply_system_prompt(
    ai_id: String,
    content: String,
    prompt_name: String
) -> Result<(), String> {
    let config = CopilotConfig::load()
        .map_err(|e| e.to_string())?;
    
    config.apply_system_prompt(&ai_id, &content, &prompt_name)
        .map_err(|e| e.to_string())
}

// Add to main function
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            // ... existing handlers
            copilot_load_config,
            copilot_save_config,
            copilot_sync_mcp_servers,
            copilot_apply_system_prompt,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

### Phase 6: Empirica Migration (1 hour)

**Goal:** Migrate Empirica SKILL.md and CLAUDE.md into CC-Switch

**Implementation:**

```rust
// Migration script: empirica_import.rs

pub fn import_empirica_skill() -> Result<(), AppError> {
    let db = Database::connect()?;
    
    // Read SKILL.md
    let skill_path = PathBuf::from("/path/to/empirica/docs/skills/SKILL.md");
    let skill_content = std::fs::read_to_string(skill_path)?;
    
    // Extract metadata (lines 1-4)
    let lines: Vec<&str> = skill_content.lines().collect();
    let name = lines.get(1)
        .and_then(|l| l.strip_prefix("name: "))
        .ok_or_else(|| AppError::Config("Invalid SKILL.md format".into()))?;
    
    let description = lines.get(2)
        .and_then(|l| l.strip_prefix("description: "))
        .ok_or_else(|| AppError::Config("Invalid SKILL.md format".into()))?;
    
    // Insert into skills table
    db.conn.execute(
        "INSERT OR REPLACE INTO skills (
            id, name, description, category, version,
            enabled_claude, enabled_gemini, enabled_copilot
        ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8)",
        params![
            "empirica-epistemic-framework",
            name,
            description,
            "metacognition",
            "4.0",
            true,   // enabled_claude
            true,   // enabled_gemini
            true,   // enabled_copilot
        ]
    )?;
    
    Ok(())
}

pub fn import_empirica_system_prompt() -> Result<(), AppError> {
    let db = Database::connect()?;
    
    // Read CLAUDE.md
    let prompt_path = PathBuf::from("~/.claude/CLAUDE.md");
    let prompt_content = std::fs::read_to_string(prompt_path)?;
    
    // Insert for each provider
    for provider in &["claude", "gemini", "copilot"] {
        db.conn.execute(
            "INSERT OR REPLACE INTO system_prompts (
                id, provider_type, prompt_name, content, version, ai_id, enabled
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            params![
                format!("empirica-core-{}-claude-code", provider),
                provider,
                "empirica-core",
                prompt_content,
                "5.0",
                "claude-code",
                true
            ]
        )?;
    }
    
    Ok(())
}
```

---

### Phase 7: Testing & Validation (1 hour)

**Test Plan:**

```bash
# 1. Unit tests
cd /tmp/cc-switch
cargo test

# 2. Integration test - Config round-trip
./test_copilot_config_roundtrip.sh

# 3. Manual testing
./src-tauri/target/release/cc-switch

# Test checklist:
# [ ] Load Copilot config
# [ ] Modify model selection
# [ ] Save config
# [ ] Verify ~/.copilot/config.json updated
# [ ] Add MCP server
# [ ] Sync to Copilot
# [ ] Verify ~/.copilot/mcp-config.json updated
# [ ] Apply system prompt
# [ ] Verify ~/.copilot/system-prompts/<ai>.md created
# [ ] Switch to different provider
# [ ] Switch back to Copilot
# [ ] Verify all settings restored
```

---

## 📊 Timeline Summary

| Phase | Task | Time | Dependencies |
|-------|------|------|--------------|
| 1 | Config analysis | - | ✅ Done |
| 2 | Database schema | 1h | - |
| 3 | Provider implementation | 3h | Phase 2 |
| 4 | UI components | 2h | Phase 3 |
| 5 | Tauri commands | 1h | Phase 3 |
| 6 | Empirica migration | 1h | Phase 2,3 |
| 7 | Testing | 1h | All |
| **Total** | **9 hours** | - | - |

**Realistic schedule:**
- **Weekend (Saturday)**: Phases 2-3 (4 hours)
- **Weekend (Sunday)**: Phases 4-6 (4 hours)
- **Monday morning**: Phase 7 (1 hour)

---

## 🎯 Success Criteria

### Must Have
- [ ] CC-Switch can read Copilot config
- [ ] CC-Switch can write Copilot config
- [ ] MCP servers sync to ~/.copilot/mcp-config.json
- [ ] System prompts write to ~/.copilot/system-prompts/
- [ ] Provider switching works (<500ms)

### Should Have
- [ ] SKILL.md imported to database
- [ ] CLAUDE.md imported to database
- [ ] Skills enable/disable per provider
- [ ] Visual config diff before save

### Nice to Have
- [ ] Auto-detect Empirica installation
- [ ] Suggest optimal MCP server config
- [ ] Validate system prompt syntax

---

## 🚀 Next Actions

### Tonight (If you have time)
```bash
# Verify config locations
ls -la ~/.copilot/config.json
ls -la ~/.copilot/mcp-config.json

# Test manual edit (backup first!)
cp ~/.copilot/config.json ~/.copilot/config.json.bak
# Edit, test, restore
```

### Weekend Saturday
```bash
# Phase 2: Database schema
cd /tmp/cc-switch
# Edit src-tauri/src/database/schema.rs
# Implement migration
# Test schema

# Phase 3: Provider implementation
# Create src-tauri/src/services/provider/copilot.rs
# Implement all methods
# Write unit tests
```

### Weekend Sunday
```bash
# Phase 4-6: UI + Migration
# Create React components
# Add Tauri commands
# Import Empirica content
# Build and test
```

### Monday Morning
```bash
# Phase 7: Final testing
# Manual test all features
# Fix any bugs
# Update documentation
# Ready for PR!
```

---

**Status:** Ready to implement  
**Confidence:** Very High (95%)  
**Estimated completion:** Monday morning

