# Per-Project Configuration - Complete

**Date:** 2025-12-19  
**Status:** ✅ COMPLETE  
**Session:** ea61febb-4bd9-4145-96aa-0ba97a50eefb

---

## Problem Statement

**Issue:** Configuration files were treated globally instead of per-project:
- `.empirica/config.yaml` was correctly per-repo ✅
- `SEMANTIC_INDEX.yaml` was hardcoded to `docs/SEMANTIC_INDEX.yaml` ❌

**Impact:**
- empirica-web repo couldn't have its own semantic index
- All projects shared the same documentation index
- No per-project customization of semantic metadata

---

## Solution Implemented

### Architecture

**Per-Project Configuration Priority:**

1. **`.empirica/config.yaml`** - Already per-repo ✅
   - Location: `<git-root>/.empirica/config.yaml`
   - Loaded by: `empirica.config.path_resolver.load_empirica_config()`
   - Scope: Database paths, settings, environment overrides

2. **`SEMANTIC_INDEX.yaml`** - Now per-repo ✅ (NEW)
   - Priority:
     1. `<git-root>/docs/SEMANTIC_INDEX.yaml` (standard location)
     2. `<git-root>/.empirica/SEMANTIC_INDEX.yaml` (alternative)
     3. `None` (graceful degradation)
   - Loaded by: `empirica.config.semantic_index_loader.load_semantic_index()`
   - Scope: Documentation metadata, tags, concepts, use cases

---

## Implementation Details

### New Module: `empirica/config/semantic_index_loader.py`

**Purpose:** Centralized loader for SEMANTIC_INDEX.yaml with per-project support

**Functions:**
```python
def load_semantic_index(project_root: Optional[str] = None) -> Optional[Dict[str, Any]]
    """Load semantic index from project root with graceful fallback"""
    
def get_semantic_index_path(project_root: Optional[str] = None) -> Optional[Path]
    """Get path to semantic index if it exists"""
```

**Features:**
- ✅ Per-project (uses git root)
- ✅ Two location options (docs/ or .empirica/)
- ✅ Graceful degradation (returns None if missing)
- ✅ Logging for debugging
- ✅ Backwards compatible

---

### Files Updated

**1. `empirica/data/session_database.py` (line 2636)**
```python
# Before:
semantic_index_path = os.path.join(project_root, 'docs', 'SEMANTIC_INDEX.yaml')
if os.path.exists(semantic_index_path):
    semantic_index = yaml.safe_load(open(semantic_index_path, 'r', encoding='utf-8')) or {}
    index = semantic_index.get('index', {}) or {}

# After:
from empirica.config.semantic_index_loader import load_semantic_index
semantic_index = load_semantic_index(project_root)
if semantic_index:
    index = semantic_index.get('index', {}) or {}
```

**2. `empirica/cli/command_handlers/project_embed.py` (line 14)**
```python
# Before:
def _load_semantic_index(root: str) -> Dict:
    import yaml
    path = os.path.join(root, 'docs', 'SEMANTIC_INDEX.yaml')
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# After:
def _load_semantic_index(root: str) -> Dict:
    """Load semantic index (per-project, with graceful fallback)"""
    from empirica.config.semantic_index_loader import load_semantic_index
    index = load_semantic_index(root)
    return index or {}
```

**3. `empirica/core/docs/doc_planner.py` (line 20)**
```python
# Before:
def _load_semantic_index(root: str) -> Dict[str, Dict]:
    idx_path = os.path.join(root, 'docs', 'SEMANTIC_INDEX.yaml')
    if not os.path.exists(idx_path):
        return {}
    data = _load_yaml(idx_path)
    return data.get('index', {}) or {}

# After:
def _load_semantic_index(root: str) -> Dict[str, Dict]:
    """Load semantic index (per-project, with graceful fallback)"""
    from empirica.config.semantic_index_loader import load_semantic_index
    index = load_semantic_index(root)
    if not index:
        return {}
    return index.get('index', {}) or {}
```

---

## Testing

### Test 1: empirica repo (has SEMANTIC_INDEX)
```bash
cd /home/yogapad/empirical-ai/empirica
empirica project-bootstrap --output json

Result: ✅ Works
- Loads from docs/SEMANTIC_INDEX.yaml
- 16 docs indexed
- Bootstrap shows project context correctly
```

### Test 2: empirica-web repo (no SEMANTIC_INDEX)
```bash
cd /home/yogapad/empirical-ai/empirica-web
empirica project-bootstrap --output json

Result: ✅ Works with graceful degradation
- No semantic index found (expected)
- Bootstrap still works
- Shows findings, goals, unknowns from database
- No error, just skips semantic docs section
```

### Test 3: Loader debug
```bash
python3 empirica/config/semantic_index_loader.py

Result: ✅ 
- Loads semantic index from correct location
- Shows version, docs count, path
```

---

## Benefits

### For Projects

**Each repo can now:**
- ✅ Have its own SEMANTIC_INDEX.yaml
- ✅ Define project-specific documentation metadata
- ✅ Customize tags, concepts, use cases per project
- ✅ Work without semantic index (graceful degradation)

**Example:**
```
empirica/
  docs/SEMANTIC_INDEX.yaml         # Framework documentation index
  
empirica-web/
  docs/SEMANTIC_INDEX.yaml         # Website documentation index
  (or no index at all - works either way)
```

### For Developers

**Flexibility:**
- Two location options: `docs/` (standard) or `.empirica/` (alternative)
- Graceful degradation: missing index doesn't break anything
- Centralized loader: one place to update logic

**Debugging:**
- Loader logs which file it loaded
- Debug function shows path resolution
- Clear error messages if parsing fails

---

## Migration Guide

### For Existing Projects

**No migration needed!** ✅ Backwards compatible.

**Current projects:**
- If you have `docs/SEMANTIC_INDEX.yaml` → Continues to work
- If you don't have it → Continues to work (graceful degradation)

### For New Projects

**Option 1: Use standard location (recommended)**
```bash
mkdir -p docs
cp empirica/docs/SEMANTIC_INDEX.yaml docs/SEMANTIC_INDEX.yaml
# Edit to match your project's documentation
```

**Option 2: Use alternative location**
```bash
mkdir -p .empirica
cp empirica/docs/SEMANTIC_INDEX.yaml .empirica/SEMANTIC_INDEX.yaml
# Edit to match your project's documentation
```

**Option 3: Skip semantic index**
```bash
# Do nothing - graceful degradation
# Bootstrap will work without semantic docs
```

---

## Semantic Index Format

**Example:**
```yaml
version: "2.0"
project: "my-project"
index:
  "01_GETTING_STARTED.md":
    tags:
      - quickstart
      - setup
      - beginner-friendly
    concepts:
      - Installation
      - First steps
    questions:
      - How do I install?
      - Where do I start?
    use_cases:
      - new_user_onboarding
      - quick_setup
  
  "architecture/SYSTEM_OVERVIEW.md":
    tags:
      - architecture
      - system-design
      - advanced
    concepts:
      - Architecture patterns
      - Component design
    questions:
      - How does it work internally?
      - What are the main components?
    use_cases:
      - understanding_internals
      - contributing

total_docs_indexed: 2
last_updated: "2025-12-19"
```

---

## Per-Project Configuration Summary

| Config File | Scope | Location | Per-Project? | Fallback |
|-------------|-------|----------|--------------|----------|
| `.empirica/config.yaml` | Paths, settings | `<git-root>/.empirica/` | ✅ Yes | CWD/.empirica |
| `SEMANTIC_INDEX.yaml` | Doc metadata | `<git-root>/docs/` or `<git-root>/.empirica/` | ✅ Yes | None (graceful) |
| `project.yaml` | Project settings | `<git-root>/.empirica/` | ✅ Yes | None |
| `credentials.yaml` | API keys | `~/.empirica/` | ❌ Global | Required |

---

## Future Enhancements

### 1. Auto-generate semantic index
```bash
empirica doc-index-generate
# Analyzes docs/ directory
# Generates SEMANTIC_INDEX.yaml with basic metadata
```

### 2. Validate semantic index
```bash
empirica doc-index-validate
# Checks SEMANTIC_INDEX.yaml format
# Verifies referenced files exist
# Reports missing metadata
```

### 3. Merge semantic indices
```bash
empirica doc-index-merge --from ../other-project
# Useful for monorepos or related projects
```

---

## Related Changes

- **Session:** ea61febb-4bd9-4145-96aa-0ba97a50eefb
- **Investigation:** 649849c5-8199-43c6-abce-0426fd8cd464 (BEADS integration)
- **Documentation:** All previous fixes (database fragmentation, etc.)

---

## Summary

✅ **Per-project configuration now complete:**
- `.empirica/config.yaml` ← Already per-project
- `SEMANTIC_INDEX.yaml` ← Now per-project (NEW)

✅ **Each git repo can have its own:**
- Database configuration
- Documentation index
- Project settings
- BEADS integration defaults

✅ **Graceful degradation:**
- Missing configs don't break functionality
- Sensible defaults for everything
- Clear logging and error messages

✅ **100% backwards compatible:**
- Existing projects continue to work
- No migration required
- Opt-in for new features

---

**Status:** Ready for production
