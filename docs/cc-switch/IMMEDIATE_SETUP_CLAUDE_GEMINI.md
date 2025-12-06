# Immediate Setup: Claude Code + Gemini CLI Switching with CC-Switch

**Purpose:** Validate the CC-Switch approach by immediately using it to manage Claude Code and Gemini CLI switching

**Timeline:** 30-45 minutes to get working

**Status:** Ready to implement

---

## Quick Overview

Instead of waiting for the full sprint (Monday), we can validate the approach TODAY by:
1. Cloning and building CC-Switch
2. Configuring Claude Code provider (already supported)
3. Configuring Gemini CLI provider (already supported)
4. Testing provider switching
5. Verifying MCP server sync and system prompts

This gives us **proof of concept** before committing to Rovo Dev + Qwen implementations.

---

## Prerequisites

```bash
# Check what we have installed
which node
which cargo
which sqlite3
which git

# Expected output:
# /usr/bin/node (or similar)
# /home/yogapad/.cargo/bin/cargo (or similar)
# /usr/bin/sqlite3
# /usr/bin/git
```

All should be available. If any are missing, install first.

---

## Step 1: Clone CC-Switch Repository

```bash
# Navigate to a working directory
cd /tmp

# Clone the desktop version (38K lines, all features)
git clone https://github.com/farion1231/cc-switch.git
cd cc-switch

# Check current version
cat package.json | grep '"version"'
# Should show: v3.8.2 or later
```

---

## Step 2: Review Current Claude Code Support

The cc-switch project already has Claude Code support. Let's verify:

```bash
# Look at the provider pattern
cat src-tauri/src/services/provider/claude.rs | head -50

# Look at the providers table to understand the schema
cat src-tauri/src/database/schema.rs | grep -A 20 "CREATE TABLE IF NOT EXISTS providers"
```

**Expected output:** Should show Claude Code provider with fields:
- `id` - Unique identifier
- `app_type` - Set to `'claude'` for Claude Code
- `name` - Display name (e.g., "Claude Code - Default")
- `settings_config` - JSON containing API key and endpoint
- Other metadata fields

---

## Step 3: Review Current Gemini Support

```bash
# Look at the Gemini provider implementation
cat src-tauri/src/services/provider/gemini.rs | head -50

# Check what config files Gemini uses
grep -r "\.gemini" src-tauri/src/ --include="*.rs" | head -10
```

**Expected:** Gemini support added in v3.7.0+

---

## Step 4: Build CC-Switch Desktop App

```bash
# Install dependencies
npm install

# Build the desktop app (Tauri)
# This creates a native binary using Rust backend + React frontend
npm run tauri build

# Expected output:
# Compiling tauri v2.x.x
# [... lots of compilation output ...]
# ✔ Packaged Deb bundle (.deb)
# ✔ Packaged AppImage bundle (.appimage)
```

**Time:** This takes 3-5 minutes (Rust compilation)

**Result:** Binary available at:
- Linux: `src-tauri/target/release/cc-switch` (or `.deb`/`.appimage`)
- macOS: `src-tauri/target/release/bundle/macos/CC Switch.app`

---

## Step 5: Launch CC-Switch Desktop App

```bash
# Run the built binary
./src-tauri/target/release/cc-switch

# Or if you built the .deb:
sudo dpkg -i src-tauri/target/release/bundle/deb/cc-switch_*.deb
cc-switch  # Should launch from PATH
```

**Expected:** A Tauri window opens with a React-based GUI showing:
- Provider selection dropdown
- MCP server list
- System prompt settings
- Settings/configuration options

---

## Step 6: Configure Claude Code Provider in CC-Switch

### Find Your Claude Code Config

```bash
# Your Claude Code config location
cat ~/.claude/config.yml

# Expected content (YAML format):
# auth:
#   api_key: "sk-..."
# claude_code:
#   model: "claude-opus-4-5-20251101"
#   mcp_servers: [...]
```

### Add Claude Code to CC-Switch Database

In the CC-Switch GUI:

1. **Click "Add Provider"**
2. **Select Provider Type:** `Claude Code`
3. **Fill in:**
   - **Name:** "Claude Code - Default"
   - **API Key:** (paste from `~/.claude/config.yml` auth.api_key)
   - **Model:** "claude-opus-4-5-20251101" (or latest)
   - **MCP Servers:** (leave empty for now, we'll sync later)
4. **Click "Save"**

**Result:** Claude Code provider now in CC-Switch database

---

## Step 7: Configure Gemini CLI Provider in CC-Switch

### Find Your Gemini Config

```bash
# Your Gemini CLI config location
cat ~/.gemini/settings.json

# Or if using env vars:
echo $GEMINI_API_KEY
```

### Add Gemini to CC-Switch Database

In the CC-Switch GUI:

1. **Click "Add Provider"**
2. **Select Provider Type:** `Gemini`
3. **Fill in:**
   - **Name:** "Gemini CLI - Default"
   - **API Key:** (from environment or settings.json)
   - **Model:** "gemini-2.0-flash" (or latest available)
   - **MCP Servers:** (optional)
4. **Click "Save"**

**Result:** Gemini provider now in CC-Switch database

---

## Step 8: Test Provider Switching

### In CC-Switch GUI

1. **Select "Claude Code - Default"** from dropdown
2. **Click "Switch Provider"**
3. **Verify:**
   - CC-Switch writes config to `~/.claude/config.yml`
   - Check file was updated: `cat ~/.claude/config.yml | grep api_key`

### Switch to Gemini

1. **Select "Gemini CLI - Default"** from dropdown
2. **Click "Switch Provider"**
3. **Verify:**
   - CC-Switch writes config to `~/.gemini/settings.json`
   - Check file was updated: `cat ~/.gemini/settings.json | grep api_key`

### Switch Back to Claude Code

1. **Select "Claude Code - Default"** from dropdown
2. **Click "Switch Provider"**
3. **Verify:** Config restored to Claude Code settings

**Expected:** Switching works without manual config file editing ✅

---

## Step 9: Verify MCP Server Sync

### Add MCP Server in CC-Switch

In the CC-Switch GUI:

1. **Go to "MCP Servers" tab**
2. **Click "Add Server"**
3. **Fill in:**
   - **Name:** "test-mcp"
   - **Command:** "python -m http.server"
   - **Environment:** (optional)
4. **Click "Save"**

### Switch Between Providers

1. **Switch to Claude Code** → Check `~/.claude/config.yml` has MCP server entry
2. **Switch to Gemini** → Check `~/.gemini/settings.json` has MCP server entry

**Expected:** MCP servers sync across providers when switching ✅

---

## Step 10: Verify System Prompts

### Add System Prompt in CC-Switch

In the CC-Switch GUI:

1. **Go to "Prompts" tab**
2. **Click "Add Prompt"**
3. **Fill in:**
   - **Name:** "empirica-baseline"
   - **Content:** (paste first 100 lines of Empirica system prompt)
4. **Click "Save"**

### Assign Prompt to Providers

1. **Select Claude Code provider**
2. **Assign prompt:** "empirica-baseline"
3. **Click "Save"**

### Test Prompt Application

When switching to Claude Code:
- Check that system prompt is written to `~/.claude/config.yml` under the appropriate field
- Verify the prompt content is correct (no truncation or encoding issues)

**Expected:** Prompts apply correctly when switching providers ✅

---

## Step 11: Database Verification

### Inspect CC-Switch SQLite Database

```bash
# CC-Switch stores database at (varies by OS):
# Linux: ~/.config/cc-switch/sqlite.db
# macOS: ~/Library/Application Support/cc-switch/sqlite.db

# Check if database exists
ls -lh ~/.config/cc-switch/sqlite.db

# Query providers table
sqlite3 ~/.config/cc-switch/sqlite.db
> SELECT id, app_type, name, created_at FROM providers;
# Expected: Should show Claude Code and Gemini entries with timestamps

# Query MCP servers
> SELECT id, name, command FROM mcp_servers;
# Expected: Should show test-mcp entry

# Query prompts
> SELECT id, name, LENGTH(content) as content_length FROM prompts;
# Expected: Should show empirica-baseline with proper content length

> .quit
```

**Expected:** Database shows all configured providers, MCP servers, and prompts ✅

---

## Step 12: Troubleshooting

### Issue: "Permission denied" when running binary

**Solution:**
```bash
chmod +x src-tauri/target/release/cc-switch
./src-tauri/target/release/cc-switch
```

### Issue: Database file not found

**Solution:**
```bash
# CC-Switch creates database on first launch
# If not found, launch the GUI and configure a provider
# This triggers database creation automatically
```

### Issue: Config file not updated after switching

**Solution:**
```bash
# Verify CC-Switch is writing to correct path
cat ~/.claude/config.yml | grep -i "api_key"

# Check file permissions
ls -l ~/.claude/config.yml  # Should be writable (644 or 664)

# If file is read-only, make writable:
chmod 644 ~/.claude/config.yml
```

### Issue: MCP servers not syncing

**Solution:**
1. Verify MCP server added to CC-Switch database: `sqlite3 ~/.config/cc-switch/sqlite.db "SELECT * FROM mcp_servers;"`
2. Manually check if provider config includes MCP reference
3. Try re-saving the provider to trigger sync

### Issue: App crashes on launch

**Solution:**
```bash
# Check logs
# Linux: ~/.config/cc-switch/logs/
tail -f ~/.config/cc-switch/logs/*.log

# Rebuild with verbose output
npm run tauri dev  # Development mode with hot reload
```

---

## Success Criteria

### ✅ Phase 1: Basic Setup
- [ ] CC-Switch cloned and built successfully
- [ ] Claude Code provider configured in CC-Switch
- [ ] Gemini provider configured in CC-Switch
- [ ] Database file created at expected location

### ✅ Phase 2: Provider Switching
- [ ] Switching to Claude Code updates `~/.claude/config.yml`
- [ ] Switching to Gemini updates `~/.gemini/settings.json`
- [ ] Switching back to Claude Code restores correct config
- [ ] No manual config file editing required

### ✅ Phase 3: MCP Server Management
- [ ] MCP servers added in CC-Switch persist in database
- [ ] MCP servers sync to both Claude Code and Gemini configs
- [ ] Switching providers maintains correct MCP configuration

### ✅ Phase 4: System Prompts
- [ ] System prompts added in CC-Switch persist in database
- [ ] Prompts assigned to providers apply on switch
- [ ] No truncation or encoding issues with prompt content

### ✅ Phase 5: Data Persistence
- [ ] SQLite database readable with sqlite3 CLI
- [ ] All providers, MCP servers, prompts visible in database
- [ ] Configuration survives app restart

---

## What This Validates

By completing this immediate setup, we validate:

1. **CC-Switch Architecture Works** - Tauri + Rust + React + SQLite proven functional
2. **Provider Pattern Extensible** - Claude Code + Gemini use same pattern → Rovo Dev + Qwen will too
3. **Config Switching Works** - Files update correctly on provider switch
4. **MCP Sync Works** - Shared MCP servers across different CLIs
5. **System Prompt Integration Works** - Prompts apply correctly per CLI

This gives us **HIGH CONFIDENCE** that extending to Rovo Dev and Qwen will work similarly.

---

## Next Steps After Validation

Once this immediate setup is complete and verified:

1. **Document What We Learned**
   - Note any differences between expected and actual behavior
   - Document any workarounds needed
   - Update integration plan if needed

2. **Copilot CLI Team Parallel Work**
   - Analyze Copilot CLI config format
   - Plan ConfigProvider implementation
   - Begin first-round integration

3. **Create RFC Issue**
   - Use findings from immediate setup to inform RFC
   - Include working example of provider pattern
   - Propose Rovo Dev + Qwen support based on validation

4. **Start One-Week Sprint (Monday)**
   - With validation complete, begin parallel implementations
   - Code: Rovo Dev (using Gemini pattern as template)
   - Sonnet: Qwen CLI (using Gemini pattern as template)
   - Qwen: Copilot CLI (using learned patterns from Copilot team)

---

## Resources

- **CC-Switch Desktop:** https://github.com/farion1231/cc-switch
- **Tauri Docs:** https://tauri.app/docs
- **SQLite Docs:** https://www.sqlite.org/cli.html
- **Our Sprint Plan:** `/home/yogapad/empirical-ai/empirica/docs/cc-switch/ONE_WEEK_EXECUTION_PLAN.md`

---

**Time Estimate:** 30-45 minutes to complete all 12 steps

**Difficulty:** Low - mostly GUI interaction + file verification

**Risk:** Very low - just testing existing features, no code changes

**Value:** Extremely high - validates entire approach before sprint commitment

---

**Status:** Ready to execute immediately. Start with Step 1 (clone repo) and work through sequentially.
