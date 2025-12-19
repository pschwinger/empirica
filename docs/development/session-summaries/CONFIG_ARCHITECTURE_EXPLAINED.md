# Configuration Architecture Explained

**Date:** 2025-12-19  
**Status:** ✅ COMPLETE

---

## Two-Tier Configuration System

Empirica uses **two separate YAML files** for configuration, each serving a different purpose:

### 1. `.empirica/config.yaml` - Infrastructure Layer (HOW)

**Purpose:** Technical infrastructure - database paths, directories, settings

**When Created:**
- Automatically by `session-create` (first time)
- Automatically by `ensure_empirica_structure()`
- Manually by `path_resolver.create_default_config()`

**Always Required:** Yes (auto-created if missing)

**Example:**
```yaml
version: '2.0'
root: /path/to/repo/.empirica
paths:
  sessions: sessions/sessions.db
  identity: identity/
  messages: messages/
  metrics: metrics/
  personas: personas/
settings:
  auto_checkpoint: true
  git_integration: true
  log_level: info
env_overrides:
  - EMPIRICA_DATA_DIR
  - EMPIRICA_SESSION_DB
```

**Customization:** Rarely needed (standard structure)

---

### 2. `.empirica/project.yaml` - Application Layer (WHAT)

**Purpose:** Project-specific settings - metadata, BEADS config, subjects/workstreams

**When Created:**
- By `empirica project-init` command
- Not auto-created (opt-in)

**Always Required:** No (graceful degradation if missing)

**Example:**
```yaml
version: '1.0'
name: My Project
description: Project description
project_id: uuid-here
beads:
  default_enabled: true  # Goals use BEADS by default
subjects:
  cli:
    paths:
      - "empirica/cli"
    description: "CLI commands and interface"
  core:
    paths:
      - "empirica/core"
    description: "Core framework logic"
default_subject: core
auto_detect:
  enabled: true
  method: path_match
```

**Customization:** Per-project (encouraged!)

---

## Architecture Comparison

| Aspect | config.yaml | project.yaml |
|--------|-------------|--------------|
| **Purpose** | Infrastructure (HOW) | Application settings (WHAT) |
| **Scope** | Technical paths/settings | Project metadata/behavior |
| **Creation** | Auto (first session) | Manual (`project-init`) |
| **Required?** | Yes (always) | No (graceful fallback) |
| **Per-repo?** | ✅ Yes | ✅ Yes |
| **Template?** | Standard (rarely edited) | Custom (per-project) |
| **Loaded by** | `path_resolver.py` | `project_config_loader.py` |

---

## Current Status (After Today's Changes)

### empirica repo (framework)
```bash
✅ .empirica/config.yaml       # Infrastructure (auto-created)
✅ .empirica/project.yaml      # Application (just created via project-init)
   - project_id: 748a81a2-ac14-45b8-a185-994997b76828
   - BEADS default: true
```

### empirica-web repo (website)
```bash
✅ .empirica/config.yaml       # Infrastructure (auto-created)
✅ .empirica/project.yaml      # Application (just created via project-init)
   - project_id: 293091ea-38b5-4c6f-a16a-f25aeecead99
   - BEADS default: false
```

### New repos (users)
```bash
# User runs:
empirica project-init

✅ Creates both:
   - .empirica/config.yaml     # Infrastructure
   - .empirica/project.yaml    # Application
```

---

## Integration Status

### Fully Wired Components

**Reading `project.yaml`:**
- ✅ `ProjectConfig` class (loads and parses)
- ✅ `load_project_config()` (file I/O)
- ✅ `get_current_subject()` (path-based subject detection)
- ✅ `goal_commands.py` (reads `beads.default_enabled`)
- ✅ All commands using `get_current_subject()` for context filtering

**Creating `project.yaml`:**
- ✅ `empirica project-init` command
- ✅ Interactive prompts (name, description, BEADS, semantic index)
- ✅ Non-interactive mode (AI-friendly JSON)

**Graceful Degradation:**
- ✅ If `project.yaml` missing → `load_project_config()` returns `None`
- ✅ Commands continue without error
- ✅ BEADS defaults to opt-in (`False`)
- ✅ Subject detection returns `None`

---

## Use Cases

### config.yaml (Infrastructure)

**What it controls:**
- Where is the database? (`.empirica/sessions/sessions.db`)
- Where are identity keys? (`.empirica/identity/`)
- Where are metrics? (`.empirica/metrics/`)
- Auto-checkpoint enabled?
- Git integration enabled?
- Log level?

**When to edit:**
- Almost never (standard structure works)
- Custom database location? (rare)
- Disable auto-checkpoint? (debugging)
- Change log level? (debugging)

**Example use case:**
```yaml
# Point to shared database for monorepo
root: /shared/.empirica
paths:
  sessions: shared/sessions.db
```

---

### project.yaml (Application)

**What it controls:**
- Project name and description
- BEADS integration (enabled by default?)
- Subjects/workstreams (CLI, core, API, docs)
- Subject path mappings (auto-detect context)
- Auto-detection settings

**When to edit:**
- Define subjects for your project
- Enable BEADS by default for team
- Add custom workstream tracking
- Configure per-project behavior

**Example use case:**
```yaml
# Frontend + Backend workstreams
name: My Full-Stack App
beads:
  default_enabled: true  # Team uses BEADS
subjects:
  frontend:
    paths: ["src/frontend", "components"]
    description: "React frontend"
  backend:
    paths: ["src/backend", "api"]
    description: "Python backend"
  docs:
    paths: ["docs"]
    description: "Documentation"
default_subject: backend
```

---

## Workflow Comparison

### Old Way (Before project-init)

**New repo setup:**
```bash
cd my-repo
git init

# Session-create auto-creates config.yaml
empirica session-create --ai-id myai

# But no project.yaml exists
# No BEADS defaults
# No subject tracking
# Manual project-create needed
```

---

### New Way (With project-init)

**New repo setup:**
```bash
cd my-repo
git init

# Initialize Empirica (creates both configs!)
empirica project-init

Project name [my-repo]: My Project
Enable BEADS by default? [y/N]: y

✅ Creates:
   - .empirica/config.yaml (infrastructure)
   - .empirica/project.yaml (application settings)
   - Project in database
   - Linked project_id

# Start working immediately
empirica session-create --ai-id myai
# Goals auto-use BEADS (default_enabled: true)
```

---

## Example Templates

### Minimal project.yaml

```yaml
version: '1.0'
name: My Project
project_id: uuid-here
beads:
  default_enabled: false
subjects: {}
auto_detect:
  enabled: true
  method: path_match
```

### Full-Featured project.yaml

```yaml
version: '1.0'
name: Empirica Framework
description: Epistemic self-awareness framework for AI agents
project_id: 748a81a2-ac14-45b8-a185-994997b76828

# BEADS integration
beads:
  default_enabled: true  # All goals use BEADS by default

# Subjects (workstreams/components)
subjects:
  cli:
    paths:
      - "empirica/cli"
    description: "CLI commands and user interface"
  
  core:
    paths:
      - "empirica/core"
    description: "Core framework logic"
  
  api:
    paths:
      - "empirica/api"
    description: "REST API endpoints"
  
  docs:
    paths:
      - "docs"
    description: "Documentation"

# Default subject if path doesn't match
default_subject: core

# Auto-detection settings
auto_detect:
  enabled: true
  method: path_match
```

---

## Answer to Original Questions

### Q1: "Is the main yaml an example config for others?"

**Answer:** 
- `config.yaml` = Standard infrastructure (not really an "example", it's the same for everyone)
- `project.yaml` = **YES, should be example/template** for users to customize per-project

**What to document:**
- Show example `project.yaml` in docs
- Explain each field (name, beads, subjects)
- Show use cases (monorepo, multi-component, BEADS teams)

---

### Q2: "Is project.yaml wired into the deeper system?"

**Answer:** ✅ **Yes, fully wired!**

**Evidence:**
1. **Reading:** `project_config_loader.py` loads it
2. **Using:** `goal_commands.py` reads `beads.default_enabled`
3. **Subject detection:** `get_current_subject()` uses path mappings
4. **Creating:** `project-init` creates it with correct format
5. **Graceful:** Missing file doesn't break anything

**What's NOT wired yet (but ready for future):**
- Other commands could use subjects for filtering
- Could add more project-level settings
- Could integrate with more BEADS features

---

## Migration Guide

### For Existing Repos (Already Using Empirica)

**Option 1: Add project.yaml (Recommended)**
```bash
cd your-repo
empirica project-init --force

# Prompts you to configure
# Creates project.yaml
# Links existing project or creates new one
```

**Option 2: Skip project.yaml (Continue Working)**
```bash
# Nothing to do!
# config.yaml already exists
# Commands work with graceful degradation
# BEADS defaults to opt-in (current behavior)
```

---

### For New Repos

**Always run project-init:**
```bash
cd new-repo
git init
empirica project-init

# Gets both configs
# Ready to work immediately
```

---

## Summary

**Two-tier configuration:**
1. **config.yaml** = Infrastructure (HOW) - auto-created, standard
2. **project.yaml** = Application (WHAT) - manual via `project-init`, customizable

**Both are per-repo:**
- Each git repo has its own `.empirica/` directory
- Separate databases, separate configs
- No global settings (except credentials in `~/.empirica/`)

**Graceful degradation:**
- `config.yaml` required (auto-created)
- `project.yaml` optional (graceful fallback)
- System works with either or both

**Best practice:**
- New repos: Always run `empirica project-init`
- Existing repos: Run `project-init --force` to add `project.yaml`
- Document `project.yaml` as customizable template

---

**Status:** Architecture complete and fully wired! ✅
