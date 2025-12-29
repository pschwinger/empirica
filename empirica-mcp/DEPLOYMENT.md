# 🚀 Epistemic MCP Server - Deployment Guide

## Prerequisites

The epistemic MCP server requires the full Empirica package to be installed.

### Why?

1. **CLI dependency**: Server routes all stateful operations through `empirica` CLI
2. **Import dependencies**: Imports from `empirica.data`, `empirica.config`, etc.
3. **Epistemic modes**: `load_context` mode calls `empirica project-bootstrap`

## Installation

### 1. Install Empirica (includes empirica-mcp)

```bash
# From PyPI (recommended)
pip install empirica

# Or from source
git clone https://github.com/Nubaeon/empirica.git
cd empirica
pip install -e .
```

This installs both:
- ✅ `empirica` CLI
- ✅ `empirica-mcp` server

### 2. Verify Installation

```bash
# Check CLI
empirica --version

# Check MCP server
empirica-mcp --help
```

## Claude Desktop Configuration

### Option 1: Standard Mode (No Epistemic)

```json
{
  "mcpServers": {
    "empirica": {
      "command": "empirica-mcp"
    }
  }
}
```

### Option 2: Epistemic Mode (NEW)

```json
{
  "mcpServers": {
    "empirica-epistemic": {
      "command": "bash",
      "args": [
        "-c",
        "EMPIRICA_EPISTEMIC_MODE=true EMPIRICA_PERSONALITY=balanced_architect empirica-mcp"
      ]
    }
  }
}
```

### Option 3: Both (Standard + Epistemic)

```json
{
  "mcpServers": {
    "empirica": {
      "command": "empirica-mcp"
    },
    "empirica-epistemic": {
      "command": "bash",
      "args": [
        "-c",
        "EMPIRICA_EPISTEMIC_MODE=true empirica-mcp"
      ]
    }
  }
}
```

## Restart Claude Desktop

After editing config:
1. Quit Claude Desktop completely
2. Restart Claude Desktop
3. Server should auto-connect

## Verify It's Working

In Claude Desktop:

```
"Can you list available Empirica tools?"
```

You should see all 40+ Empirica MCP tools listed.

If epistemic mode enabled, tool responses will include:
```json
{
  "epistemic_state": {
    "vectors": {...},
    "routing": {...}
  }
}
```

## Troubleshooting

### "empirica CLI not found"

```bash
# Check if empirica is in PATH
which empirica

# If not, install
pip install empirica

# Verify
empirica --version
```

### "Module not found: empirica"

```bash
# Install full package
pip install empirica

# Not just MCP server
pip install empirica-mcp  # ❌ Won't work standalone
```

### "Permission denied"

```bash
# Make executable
chmod +x $(which empirica-mcp)
```

### Claude Desktop config syntax

Make sure JSON is valid:
- No trailing commas
- Proper quotes
- Valid escape sequences

## Package Structure

```
empirica/                    # Main package
├── empirica/               # Core library
│   ├── cli/               # CLI implementation
│   ├── data/              # Session database
│   └── ...
└── empirica-mcp/          # MCP server (depends on empirica)
    ├── empirica_mcp/
    │   ├── server.py      # MCP server
    │   ├── epistemic/     # Epistemic components
    │   └── ...
    └── pyproject.toml     # Declares empirica>=1.1.0
```

## Development Setup

```bash
# Clone repo
git clone https://github.com/Nubaeon/empirica.git
cd empirica

# Install in editable mode
pip install -e .

# Test
empirica --version
empirica-mcp --help

# Run epistemic tests
cd empirica-mcp
python test_epistemic.py
```

## Production Deployment

```bash
# Install from PyPI
pip install empirica

# Configure Claude Desktop
# (see configs above)

# Restart Claude Desktop
```

**That's it!** 🚀

---

## Next Steps

1. ✅ Install `empirica` package
2. ✅ Configure Claude Desktop
3. ✅ Restart Claude Desktop
4. 🎉 Test epistemic MCP server

See `QUICK_START.md` for usage examples.
