# Production Docs Update Plan
**Date:** 2025-12-04
**Issue:** Docs reference deprecated bootstrap/ExtendedMetacognitiveBootstrap

## Current Reality (Post-Cleanup)

### ✅ What Works Now
- `empirica session-create --ai-id myai` - Creates session in SQLite
- MCP `bootstrap_session(ai_id="myai")` - Creates session via MCP
- No component pre-loading (all lazy-loaded on demand)
- No bootstrap command (removed)

### ❌ What's Deprecated
- `ExtendedMetacognitiveBootstrap` class - DELETED
- `OptimalMetacognitiveBootstrap` class - DELETED  
- `empirica bootstrap` command - REMOVED
- Component pre-loading concept - OBSOLETE

## Docs Needing Updates

### Critical (Heavy Bootstrap Usage)
1. **03_BASIC_USAGE.md** (33 refs) - Complete rewrite needed
2. **15_CONFIGURATION.md** (28 refs) - Update bootstrap config
3. **17_PRODUCTION_DEPLOYMENT.md** (27 refs) - Remove bootstrap steps
4. **13_PYTHON_API.md** (22 refs) - Update Python examples

### Important (Moderate Usage)
5. **23_SESSION_CONTINUITY.md** (17 refs)
6. **21_TROUBLESHOOTING.md** (17 refs)
7. **19_API_REFERENCE.md** (12 refs)

### Minor (Light Touch)
8. **24_MCO_ARCHITECTURE.md** (8 refs)
9. **12_SESSION_DATABASE.md** (7 refs)
10. **28_DECISION_LOGIC.md** (1 ref)

## Replacement Patterns

### OLD (Deprecated):
```python
from empirica.bootstraps import ExtendedMetacognitiveBootstrap

bootstrap = ExtendedMetacognitiveBootstrap(level="2", ai_id="myai")
components = bootstrap.bootstrap()
# Components: {'twelve_vector_monitor': ..., 'calibration': ...}
```

### NEW (Current):
```python
from empirica.data.session_database import SessionDatabase

# Create session
db = SessionDatabase()
session_id = db.create_session(
    ai_id="myai",
    bootstrap_level=1,  # 0-4
    components_loaded=6  # Standard count
)
db.close()

# Components lazy-load on demand - no pre-loading needed
```

### CLI OLD:
```bash
empirica bootstrap --ai-id myai --level standard
```

### CLI NEW:
```bash
empirica session-create --ai-id myai --bootstrap-level 1
# Returns session_id for use with preflight/check/postflight
```

### MCP (Still Works):
```python
# MCP tool creates session automatically
bootstrap_session(ai_id="myai", bootstrap_level=1)
# Returns: {"session_id": "...", "ok": True}
```

## Update Strategy

### Phase 1: Core Usage Docs (Priority 1)
- 03_BASIC_USAGE.md - Show session-create + direct CASCADE usage
- 13_PYTHON_API.md - Update all Python examples

### Phase 2: Configuration & Deployment
- 15_CONFIGURATION.md - Remove bootstrap config sections
- 17_PRODUCTION_DEPLOYMENT.md - Update deployment flow

### Phase 3: Reference & Troubleshooting  
- 19_API_REFERENCE.md - Update API signatures
- 21_TROUBLESHOOTING.md - Remove bootstrap troubleshooting
- 23_SESSION_CONTINUITY.md - Update session examples

### Phase 4: Architecture Docs
- 24_MCO_ARCHITECTURE.md - Update architecture diagrams
- 12_SESSION_DATABASE.md - Clarify current session creation

## Key Messages for Docs

1. **No bootstrap ceremony** - Session creation is instant, no pre-loading
2. **Lazy loading** - Components create on-demand when needed
3. **Explicit sessions** - Use session-create or MCP bootstrap_session
4. **13-vector only** - No 12-vector, no heuristics, canonical only

