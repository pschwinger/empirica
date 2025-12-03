# Empirica Installation & Configuration Guide

**Last Updated:** 2025-12-03
**Status:** Complete installation guide for all major AI programming interfaces

---

## Overview

This guide covers installing and configuring Empirica across 9 major AI programming platforms. Choose your platform(s) below, then follow the specific setup instructions.

**Empirica provides:**
- 39 MCP tools for epistemic tracking and session management
- System prompt integration for metacognitive reasoning
- Claude Skill for enhanced Claude on Web functionality
- Consistent epistemic framework across all interfaces

---

## Supported Platforms

| Platform | Type | Config File(s) | System Prompt | Skill Support |
|----------|------|-----------------|---------------|----|
| **Cursor IDE** | IDE | ~/.cursor/mcp.json | Yes | N/A |
| **Continue.dev** | VSCode Extension | .continue/mcpServers/ | Yes | N/A |
| **Cline** | VSCode Extension | cline_mcp_settings.json | Yes | N/A |
| **Claude Code** | CLI | ~/.claude/mcp.json | Yes | N/A |
| **Copilot CLI** | CLI | ~/.copilot/mcp-config.json | Yes | N/A |
| **Rovodev CLI** | CLI | ~/.rovodev/mcp.json | Yes | N/A |
| **Gemini CLI** | CLI | ~/.gemini/settings.json | Yes | N/A |
| **Augment Code** | IDE | Settings Panel | Yes | N/A |
| **JetBrains AI Assistant** | IDE Plugin | Settings UI | Yes | N/A |
| **Claude on Web** | Web | https://claude.ai | Yes | ✅ |

---

## Quick Start

### For Local Development (Claude Code CLI)

```bash
# 1. Copy system prompt to home directory
cp docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md ~/.claude/CLAUDE.md

# 2. Configure MCP server
mkdir -p ~/.claude
cat > ~/.claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "empirica": {
      "command": "env",
      "args": [
        "LD_LIBRARY_PATH=",
        "/path/to/empirica/.venv-mcp/bin/python3",
        "/path/to/empirica/mcp_local/empirica_mcp_server.py"
      ],
      "type": "local",
      "env": {
        "PYTHONPATH": "/path/to/empirica",
        "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
      },
      "tools": ["*"],
      "description": "Empirica metacognitive framework - all MCP tools enabled"
    }
  }
}
EOF

# 3. Verify installation
cd /any/project && claude --help
```

Done! All 39 empirica tools are now available in Claude Code.

---

## Platform-Specific Setup

### 1. Cursor IDE

**What is Cursor:** Modern code editor with Claude integration, most popular choice for developers (2025)

**Installation:**

1. **MCP Server Configuration**

   Location: `~/.cursor/mcp.json`

   ```json
   {
     "mcpServers": {
       "empirica": {
         "command": "env",
         "args": [
           "LD_LIBRARY_PATH=",
           "/path/to/empirica/.venv-mcp/bin/python3",
           "/path/to/empirica/mcp_local/empirica_mcp_server.py"
         ],
         "type": "local",
         "env": {
           "PYTHONPATH": "/path/to/empirica",
           "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
         },
         "tools": ["*"],
         "description": "Empirica metacognitive framework"
       }
     }
   }
   ```

2. **System Prompt Setup**

   Location: Cursor Settings → Features → Claude → System Prompt

   - Paste contents of `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`
   - Or use simpler version from `~/.claude/CLAUDE.md`

3. **Verification**

   ```bash
   # Open Cursor and in Claude panel, type:
   empirica --help

   # Should show all 39 MCP tools available
   ```

---

### 2. Continue.dev (VSCode Extension)

**What is Continue.dev:** VSCode extension with multi-model support, ~200k users

**Installation:**

1. **Install Extension**

   ```bash
   # In VSCode Extensions marketplace, search: "Continue"
   # Click Install on "Continue: Code Autopilot"
   ```

2. **MCP Server Configuration**

   Location: `.continue/mcpServers.yaml` in workspace root (or `~/.continue/mcpServers.yaml` for user-level)

   ```yaml
   empirica:
     command: env
     args:
       - LD_LIBRARY_PATH=
       - /path/to/empirica/.venv-mcp/bin/python3
       - /path/to/empirica/mcp_local/empirica_mcp_server.py
     env:
       PYTHONPATH: /path/to/empirica
       EMPIRICA_ENABLE_MODALITY_SWITCHER: "false"
     tools:
       - "*"
     description: Empirica metacognitive framework
   ```

3. **System Prompt Setup**

   Location: `.continue/config.json` → `systemPrompt` field

   ```json
   {
     "systemPrompt": "[Paste CANONICAL_SYSTEM_PROMPT.md content here]",
     "models": [
       {
         "title": "Claude 3.5 Sonnet",
         "provider": "openrouter",
         "model": "claude-3-5-sonnet-20241022"
       }
     ],
     "mcpServers": "mcpServers.yaml"
   }
   ```

4. **Verification**

   - In Continue chat panel, type: `@empirica --help`
   - Should show available tools

---

### 3. Cline (VSCode Extension - Open Source)

**What is Cline:** Open-source VSCode extension for AI coding, community-maintained

**Installation:**

1. **Install Extension**

   ```bash
   # In VSCode Extensions marketplace, search: "Cline"
   # Click Install on "Cline: AI Assistant" (by Saoudrizwan)
   ```

2. **MCP Server Configuration**

   Location: Project root → `cline_mcp_settings.json`

   ```json
   {
     "mcpServers": {
       "empirica": {
         "command": "env",
         "args": [
           "LD_LIBRARY_PATH=",
           "/path/to/empirica/.venv-mcp/bin/python3",
           "/path/to/empirica/mcp_local/empirica_mcp_server.py"
         ],
         "type": "local",
         "env": {
           "PYTHONPATH": "/path/to/empirica",
           "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
         },
         "tools": ["*"]
       }
     }
   }
   ```

3. **System Prompt Setup**

   Location: VSCode Settings → Cline → Custom System Prompt

   - Paste contents of `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`

4. **Verification**

   - In Cline chat, type: `/mcp list`
   - Should show empirica server and all tools

---

### 4. Claude Code CLI

**What is Claude Code:** Official Anthropic CLI, works across all projects in your terminal

**Installation:**

1. **MCP Server Configuration**

   Location: `~/.claude/mcp.json` (system-wide, all projects)

   ```json
   {
     "mcpServers": {
       "empirica": {
         "command": "env",
         "args": [
           "LD_LIBRARY_PATH=",
           "/path/to/empirica/.venv-mcp/bin/python3",
           "/path/to/empirica/mcp_local/empirica_mcp_server.py"
         ],
         "type": "local",
         "env": {
           "PYTHONPATH": "/path/to/empirica",
           "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
         },
         "tools": ["*"],
         "description": "Empirica metacognitive framework - all MCP tools enabled"
       }
     }
   }
   ```

2. **System Prompt Setup**

   Location: `~/.claude/CLAUDE.md` (system-wide, auto-loads in all sessions)

   ```bash
   # Copy system prompt
   cp docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md ~/.claude/CLAUDE.md

   # Or simpler version (already prepared)
   cp ~/.claude/CLAUDE.md.template ~/.claude/CLAUDE.md
   ```

3. **Verification**

   ```bash
   cd /any/project
   claude --help

   # Should show empirica tools available
   # Start a session: claude
   # Then type: empirica --help
   ```

**Optional: Project-Level Override**

If you want project-specific settings, create `mcp.json` in your project root:

```bash
# In your project directory
cat > mcp.json << 'EOF'
{
  "mcpServers": {
    "empirica": {
      "command": "env",
      "args": [
        "LD_LIBRARY_PATH=",
        "/path/to/empirica/.venv-mcp/bin/python3",
        "/path/to/empirica/mcp_local/empirica_mcp_server.py"
      ],
      "type": "local",
      "env": {
        "PYTHONPATH": "/path/to/empirica"
      },
      "tools": ["*"]
    }
  }
}
EOF
```

---

### 5. Copilot CLI (Microsoft)

**What is Copilot CLI:** Microsoft's command-line interface for GitHub Copilot, enterprise adoption

**Installation:**

1. **MCP Server Configuration**

   Location: `~/.copilot/mcp-config.json` (system-wide)

   ```json
   {
     "mcpServers": {
       "empirica": {
         "command": "env",
         "args": [
           "LD_LIBRARY_PATH=",
           "/path/to/empirica/.venv-mcp/bin/python3",
           "/path/to/empirica/mcp_local/empirica_mcp_server.py"
         ],
         "type": "local",
         "env": {
           "PYTHONPATH": "/path/to/empirica",
           "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
         },
         "tools": ["*"],
         "description": "Empirica metacognitive framework"
       }
     }
   }
   ```

2. **System Prompt Setup**

   Location: Copilot CLI settings (check `copilot config --help`)

   ```bash
   # View system prompt location
   copilot config show

   # Set system prompt (if supported)
   copilot config set system-prompt "$(cat docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md)"
   ```

3. **Verification**

   ```bash
   copilot --help
   # Should show empirica tools in available tools
   ```

---

### 6. Rovodev CLI (Atlassian)

**What is Rovodev:** Atlassian's AI CLI for development workflows

**Installation:**

1. **MCP Server Configuration**

   Location: `~/.rovodev/mcp.json` (system-wide)

   ```json
   {
     "mcpServers": {
       "empirica": {
         "command": "env",
         "args": [
           "LD_LIBRARY_PATH=",
           "/path/to/empirica/.venv-mcp/bin/python3",
           "/path/to/empirica/mcp_local/empirica_mcp_server.py"
         ],
         "type": "local",
         "env": {
           "PYTHONPATH": "/path/to/empirica",
           "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
         },
         "tools": ["*"],
         "description": "Empirica metacognitive framework"
       }
     }
   }
   ```

2. **System Prompt Setup**

   Location: Rovodev configuration (check `rovodev config --help`)

   ```bash
   # View configuration
   rovodev config show

   # Set system prompt path or content
   rovodev config set system-prompt "~/.rovodev/CLAUDE.md"
   cp docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md ~/.rovodev/CLAUDE.md
   ```

3. **Verification**

   ```bash
   rovodev --help
   # Should show empirica tools available
   ```

---

### 7. Gemini CLI (Google)

**What is Gemini CLI:** Google's command-line interface for Gemini models

**Installation:**

1. **MCP Server Configuration**

   Location: `~/.gemini/settings.json` or `.gemini/settings.json` (workspace)

   ```json
   {
     "mcpServers": {
       "empirica": {
         "command": "env",
         "args": [
           "LD_LIBRARY_PATH=",
           "/path/to/empirica/.venv-mcp/bin/python3",
           "/path/to/empirica/mcp_local/empirica_mcp_server.py"
         ],
         "type": "local",
         "env": {
           "PYTHONPATH": "/path/to/empirica",
           "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
         },
         "tools": ["*"],
         "description": "Empirica metacognitive framework"
       }
     }
   }
   ```

2. **System Prompt Setup**

   Location: `~/.gemini/system-prompt.md`

   ```bash
   cp docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md ~/.gemini/system-prompt.md

   # Then set in settings.json
   ```

3. **Verification**

   ```bash
   gemini --help
   # Should show empirica tools

   gemini chat --system-prompt ~/.gemini/system-prompt.md
   ```

---

### 8. Augment Code (IDE)

**What is Augment Code:** AI-powered IDE with deep codebase understanding

**Installation:**

1. **MCP Server Configuration**

   Location: Augment Settings → AI Settings → MCP Servers (or Settings Panel)

   - Use "Easy MCP" feature:
     ```
     Command: env
     Args: LD_LIBRARY_PATH= /path/to/empirica/.venv-mcp/bin/python3 /path/to/empirica/mcp_local/empirica_mcp_server.py
     Environment:
       PYTHONPATH=/path/to/empirica
       EMPIRICA_ENABLE_MODALITY_SWITCHER=false
     Tools: * (all)
     ```

   Or paste JSON directly:

   ```json
   {
     "empirica": {
       "command": "env",
       "args": [
         "LD_LIBRARY_PATH=",
         "/path/to/empirica/.venv-mcp/bin/python3",
         "/path/to/empirica/mcp_local/empirica_mcp_server.py"
       ],
       "env": {
         "PYTHONPATH": "/path/to/empirica",
         "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
       },
       "tools": ["*"]
     }
   }
   ```

2. **System Prompt Setup**

   Location: Settings → AI Settings → System Prompt (or Settings Panel)

   - Paste contents of `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`
   - Or use shorter version for IDE context

3. **Verification**

   - Check MCP Servers panel
   - Should show empirica server connected
   - In AI chat, type: `/empirica --help`

---

### 9. JetBrains AI Assistant

**What is JetBrains AI Assistant:** IDE plugin for IntelliJ IDEA, PyCharm, WebStorm, etc.

**Installation:**

1. **Enable AI Assistant Plugin**

   - Open IDE → Settings/Preferences → Plugins
   - Search "AI Assistant"
   - Click Install (usually pre-installed in 2024+)

2. **MCP Server Configuration**

   Location: Settings/Preferences → Tools → AI Assistant → MCP

   - Click "Add MCP Server"
   - Name: `empirica`
   - Command: `env`
   - Arguments:
     ```
     LD_LIBRARY_PATH=
     /path/to/empirica/.venv-mcp/bin/python3
     /path/to/empirica/mcp_local/empirica_mcp_server.py
     ```
   - Environment:
     ```
     PYTHONPATH=/path/to/empirica
     EMPIRICA_ENABLE_MODALITY_SWITCHER=false
     ```
   - Tools: `*` (all)

   Or use JSON configuration file at:
   ```
   ~/.config/JetBrains/[IDE]/ai.xml
   ```

3. **System Prompt Setup**

   Location: Settings/Preferences → Tools → AI Assistant → System Prompt

   - Paste contents of `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`
   - Or use shorter version optimized for IDE context

4. **Verification**

   - Open AI Assistant panel (bottom right or View → AI Assistant)
   - Type: `empirica --help`
   - Should show all tools available

---

## System Prompt Integration

### CANONICAL_SYSTEM_PROMPT.md

This is the complete Empirica agent prompt with all details about:
- 13 epistemic vectors
- CASCADE workflow (PREFLIGHT → INVESTIGATE → ACT → POSTFLIGHT)
- MCO Architecture v2.0
- Work principles and tool usage

**Location:** `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`

**How to use:**

1. **Copy to system-wide location** (for all projects):
   ```bash
   cp docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md ~/.claude/CLAUDE.md
   ```

2. **Add to IDE settings:**
   - Cursor: Settings → Features → Claude → System Prompt
   - Continue.dev: `.continue/config.json` → `systemPrompt`
   - Cline: VSCode Settings → Cline → Custom System Prompt
   - JetBrains: Settings → Tools → AI Assistant → System Prompt

3. **For CLI tools:**
   - Copy to home directory or project root
   - Or set as environment variable: `EMPIRICA_SYSTEM_PROMPT=~/.claude/CLAUDE.md`

### Shorter Version (CLAUDE.md)

For more compact IDE contexts, there's a shorter version:

**Location:** See `~/.claude/CLAUDE.md` (if using Claude Code)

This version includes:
- Essential role definition
- Epistemic vector reference (compact)
- Key methodology
- Tool usage patterns

Use this for:
- IDE integrations (less context)
- Web interfaces
- Mobile-constrained environments

---

## Claude Skill Integration

### What is a Claude Skill?

A Claude Skill is a structured set of instructions that extends Claude's capabilities with custom functionality. For Empirica, the Skill provides:
- Epistemic assessment framework
- CASCADE workflow templates
- Goal creation and tracking
- Session management helpers

### Create an Empirica Skill

1. **Create Skill Structure**

   ```bash
   mkdir -p empirica-skill
   cd empirica-skill

   # Create SKILL.md (primary instructions)
   cat > SKILL.md << 'EOF'
   # Empirica Metacognitive Skill

   This skill enables epistemic reasoning using the Empirica framework.

   ## Key Capabilities

   - Assess epistemic state using 13 vectors (KNOW, UNCERTAINTY, CLARITY, etc.)
   - Execute CASCADE phases (PREFLIGHT, INVESTIGATE, ACT, POSTFLIGHT)
   - Create and manage goals with success criteria
   - Generate epistemic handoffs between sessions
   - Track learning across task execution

   ## Usage

   1. Start with PREFLIGHT phase: assess epistemic state
   2. Execute INVESTIGATE or ACT phases as needed
   3. Capture results and generate POSTFLIGHT assessment
   4. Create handoff package for next session

   See full documentation in Empirica framework.
   EOF

   # Create templates directory
   mkdir -p templates

   # Create goal template
   cat > templates/goal_template.md << 'EOF'
   # Goal Template

   ## Objective
   [What are we trying to accomplish?]

   ## Success Criteria
   - [ ] Criterion 1
   - [ ] Criterion 2
   - [ ] Criterion 3

   ## Epistemic Scope
   - **BREADTH:** 0.0-1.0 (how wide: single function → entire system)
   - **DURATION:** 0.0-1.0 (how long: minutes/hours → weeks/months)
   - **COORDINATION:** 0.0-1.0 (solo work → heavy multi-agent coordination)

   ## Initial Assessment
   - KNOW: 0.0-1.0
   - UNCERTAINTY: 0.0-1.0
   - CLARITY: 0.0-1.0
   - COMPLETION: 0.0-1.0
   EOF
   ```

2. **Deploy to Claude on Web**

   - Go to https://claude.ai
   - In the chat interface, look for "Customize Claude" or "Add Skills"
   - Click "Import Skill" or "Create Custom Skill"
   - Upload the skill folder or paste SKILL.md content
   - Test with: "Create a goal using the Empirica framework"

3. **Share the Skill**

   - Export the skill from Claude interface
   - Share skill URL or package with teammates
   - Others can import same skill

### Example Skill Interactions

```
User: Use Empirica to plan a project

Claude (with Skill):
I'll help you plan this using the Empirica metacognitive framework.

PREFLIGHT Phase - Initial Assessment:

Current Epistemic State:
- KNOW: 0.4 (partially familiar with requirements)
- UNCERTAINTY: 0.7 (many unknowns remain)
- CLARITY: 0.5 (need to clarify scope)
- COMPLETION: 0.0 (not started)

Recommendation: Execute INVESTIGATE phase to reduce uncertainty...
```

---

## Verification & Testing

### For Each Platform

**Step 1: Test MCP Server Connection**

```bash
# CLI tools (Claude Code, Copilot, etc.)
claude --help  # Should show empirica tools

# Check specific tool
claude empirica bootstrap --ai-id test-ai

# Continue.dev or Cline
@empirica --help  # In chat interface
/mcp list  # Should show empirica server
```

**Step 2: Test System Prompt Loading**

```bash
# Start session
claude

# Check if system prompt loaded
# (Look for role definition and epistemic vectors in context)

# Test epistemic reasoning
empirica preflight --prompt "What should I do?"
```

**Step 3: Verify All 39 Tools Available**

```bash
# Get tool list
empirica --list-tools

# Should output all tools including:
# - Session management (bootstrap, resume, etc.)
# - Epistemic assessment (preflight, check, postflight)
# - Goal orchestration (create, discover, etc.)
# - Git integration (checkpoint, handoff)
# - And 29 more...
```

### Integration Testing Checklist

- [ ] MCP server starts without errors
- [ ] All 39 tools appear in help/list
- [ ] System prompt loads in session
- [ ] Epistemic vectors accessible
- [ ] Goal creation works
- [ ] Session checkpoints persist to git
- [ ] Handoffs generate correctly
- [ ] Cross-model routing functions (if multi-model setup)

---

## Troubleshooting

### MCP Server Won't Start

**Error:** `ModuleNotFoundError: No module named 'empirica'`

**Solution:**
```bash
# Verify PYTHONPATH is correct
echo $PYTHONPATH

# Should point to empirica root directory containing:
# - empirica/
# - mcp_local/
# - docs/

# If wrong, fix in config file (mcp.json, etc.)
```

**Error:** `FileNotFoundError: /path/to/empirica_mcp_server.py`

**Solution:**
```bash
# Verify file exists and path is correct
ls -la /path/to/empirica/mcp_local/empirica_mcp_server.py

# If using relative paths, convert to absolute:
realpath /path/to/empirica
# Then use absolute path in config
```

### Tools Not Appearing

**Error:** Some or all empirica tools missing

**Solution:**
1. Check `"tools": ["*"]` is set in config (enables ALL tools)
2. Restart the CLI/IDE completely (not just reload)
3. Verify Python environment:
   ```bash
   /path/to/empirica/.venv-mcp/bin/python3 -c "import empirica; print(empirica.__file__)"
   ```

### System Prompt Not Loading

**Error:** System prompt ignored, not applied to session

**Solution:**
- Check file exists at configured path
- Verify file is readable: `ls -la ~/.claude/CLAUDE.md`
- Check file is valid markdown (no binary characters)
- Restart IDE/CLI to reload configuration
- For IDEs, check settings persist after restart

### Python Environment Issues

**Error:** `LD_LIBRARY_PATH` or library conflicts

**Solution:**
```bash
# LD_LIBRARY_PATH="" clears conflicting libraries
# This is intentional in the config

# If you need specific libraries, replace with:
"LD_LIBRARY_PATH=/usr/local/lib:/opt/lib"

# Verify Python sees correct dependencies:
/path/to/empirica/.venv-mcp/bin/python3 -c "import git; print(git.__file__)"
```

### Configuration File Syntax

**Error:** JSON/YAML parsing error

**Solution:**
- Use JSON validator: `jq < ~/.claude/mcp.json`
- For YAML (Continue.dev): `yamllint .continue/mcpServers.yaml`
- Check for trailing commas (JSON doesn't allow)
- Ensure all quotes are matched

---

## Common Configuration Paths

Quick reference for all config file locations:

```bash
# IDEs
~/.cursor/mcp.json                           # Cursor
~/.config/cursor/settings.json               # Cursor (alternate)
~/.vscode/extensions/                        # VSCode (if local)
~/.jetbrains/idea/options/                   # JetBrains

# CLIs
~/.claude/mcp.json                           # Claude Code
~/.claude/settings.json                      # Claude Code (alternate)
~/.copilot/mcp-config.json                   # Copilot
~/.rovodev/mcp.json                          # Rovodev
~/.gemini/settings.json                      # Gemini CLI

# VSCode Extensions
.continue/mcpServers.yaml                    # Continue.dev (workspace)
~/.continue/mcpServers.yaml                  # Continue.dev (user)
cline_mcp_settings.json                      # Cline (workspace)

# System Prompts
~/.claude/CLAUDE.md                          # Claude Code
~/.copilot/system-prompt.md                  # Copilot
~/.rovodev/CLAUDE.md                         # Rovodev
~/.gemini/system-prompt.md                   # Gemini CLI
.continue/config.json                        # Continue.dev
```

---

## Environment Variables

Set these in your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) for all sessions:

```bash
# Point to empirica installation
export EMPIRICA_HOME="/path/to/empirica"

# Enable detailed logging (optional)
export EMPIRICA_LOG_LEVEL="DEBUG"

# System prompt location (optional)
export EMPIRICA_SYSTEM_PROMPT="~/.claude/CLAUDE.md"

# Disable modality switching (standard setup)
export EMPIRICA_ENABLE_MODALITY_SWITCHER="false"

# Enable Sentinel routing (when ready for Phase 2)
export EMPIRICA_ENABLE_SENTINEL="false"  # Set to true after Phase 1
```

---

## Next Steps

### After Installation

1. **Test the Setup**
   ```bash
   cd /any/project
   claude
   # In session:
   empirica preflight --prompt "Debug a simple function"
   ```

2. **Create Your First Goal**
   ```bash
   empirica goals-create \
     --session-id session-001 \
     --objective "Debug authentication system" \
     --success-criteria "Login works" "Password reset works"
   ```

3. **Run Through CASCADE Workflow**
   - PREFLIGHT: Assess epistemic state
   - INVESTIGATE: Gather information
   - ACT: Make changes
   - POSTFLIGHT: Capture learning

4. **Integrate with Your Development**
   - Use empirica for complex tasks
   - Let it track epistemic state
   - Review deltas and learning patterns
   - Iterate on methodology

---

## Support & Documentation

### Key Documentation Files

- **CANONICAL_SYSTEM_PROMPT.md** - Complete agent prompt
- **ARCHITECTURE_SENTINEL_INTEGRATION.md** - Technical architecture (Phase 1 vision)
- **VISION_EMPIRICA_SENTINEL_SYSTEM.md** - Long-term product vision
- **SESSION_ALIASES.md** - Session management helpers
- **TRY_EMPIRICA_NOW.md** - Quick tutorial

### Getting Help

- **Check logs:** `echo $EMPIRICA_LOG_LEVEL` and review output
- **Verify installation:** `empirica --version`
- **List tools:** `empirica --list-tools`
- **Check session:** `empirica session-status --session-id [id]`
- **Read error messages carefully** - they often point to the exact issue

---

## Configuration Template Generator

Save this as `setup-empirica.sh` to automate setup for your platform:

```bash
#!/bin/bash

# Empirica Setup Script
# Usage: ./setup-empirica.sh [cursor|continue|cline|claude-code|copilot|rovodev|gemini|augment|jetbrains]

PLATFORM=${1:-claude-code}
EMPIRICA_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

echo "Setting up Empirica for: $PLATFORM"
echo "Empirica path: $EMPIRICA_PATH"

case $PLATFORM in
  claude-code)
    mkdir -p ~/.claude
    cp docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md ~/.claude/CLAUDE.md
    cat > ~/.claude/mcp.json << EOF
{
  "mcpServers": {
    "empirica": {
      "command": "env",
      "args": ["LD_LIBRARY_PATH=", "$EMPIRICA_PATH/.venv-mcp/bin/python3", "$EMPIRICA_PATH/mcp_local/empirica_mcp_server.py"],
      "type": "local",
      "env": {
        "PYTHONPATH": "$EMPIRICA_PATH",
        "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
      },
      "tools": ["*"]
    }
  }
}
EOF
    echo "✅ Claude Code configured"
    ;;

  cursor)
    mkdir -p ~/.cursor
    cp docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md ~/.cursor/CLAUDE.md
    cat > ~/.cursor/mcp.json << EOF
{
  "mcpServers": {
    "empirica": {
      "command": "env",
      "args": ["LD_LIBRARY_PATH=", "$EMPIRICA_PATH/.venv-mcp/bin/python3", "$EMPIRICA_PATH/mcp_local/empirica_mcp_server.py"],
      "type": "local",
      "env": {
        "PYTHONPATH": "$EMPIRICA_PATH",
        "EMPIRICA_ENABLE_MODALITY_SWITCHER": "false"
      },
      "tools": ["*"]
    }
  }
}
EOF
    echo "✅ Cursor configured"
    ;;

  *)
    echo "Platform not recognized. Supported: claude-code, cursor, continue, cline, copilot, rovodev, gemini, augment, jetbrains"
    exit 1
    ;;
esac

echo ""
echo "Setup complete! Verify with: empirica --help"
```

Usage:
```bash
chmod +x setup-empirica.sh
./setup-empirica.sh claude-code
./setup-empirica.sh cursor
```

---

## Feedback & Issues

If you encounter problems:

1. **Check this guide** for your specific platform
2. **Verify paths** are absolute and correct
3. **Test Python:** `/path/to/venv/bin/python3 -c "import empirica"`
4. **Check git:** `git status` in empirica root
5. **Review logs:** Enable DEBUG logging if available
6. **Consult docs:** See files linked in "Support & Documentation" section

**Last Updated:** 2025-12-03
**Version:** 1.0
**Status:** Production Ready
