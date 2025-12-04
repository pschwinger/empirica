# Empirica Architecture - CORRECTED UNDERSTANDING

## Storage Architecture (Corrected)

### 1. **Git** - PRIMARY for epistemic/learning data ✅
- Checkpoints (compressed epistemic state snapshots)
- Goals (cross-AI discovery via git notes)
- Handoffs (session continuity reports)
- **This is where the epistemic knowledge lives**

### 2. **SQLite** - Session metadata & operational data
- Session tracking (ai_id, start_time, end_time)
- Basic metadata (bootstrap_level, cascades count)
- **NOT for epistemic vectors - those are in Git**

### 3. **JSON** - Output format & interchange
- Command outputs (--output json)
- Import/export
- API responses

## Data Flow (Corrected)

```
User Action → CLI Command → Process
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              Git (epistemic)    SQLite (session)
              - Vectors          - Metadata
              - Checkpoints      - Tracking
              - Goals            - Status
              - Handoffs         
                    ↓                   ↓
                    └─────────┬─────────┘
                              ↓
                        JSON output
```

## What "Consolidate" Means

**NOT:** Changing storage backends
**YES:** Consolidating CLI parameters

### Example 1: Scope Parameters
```bash
# BEFORE (3 separate flags):
empirica goals-create \
  --scope-breadth 0.7 \
  --scope-duration 0.5 \
  --scope-coordination 0.3

# AFTER (1 JSON flag):
empirica goals-create \
  --scope '{"breadth":0.7, "duration":0.5, "coordination":0.3}'

# Storage: STILL goes to Git (goals note) - unchanged!
# Just easier to specify
```

### Example 2: Auto-infer from Git
```bash
# BEFORE (must specify phase/round):
empirica checkpoint-create \
  --session-id abc \
  --phase ACT \
  --round 3

# AFTER (read from git to auto-detect):
empirica checkpoint-create --session-id abc

# How: Read latest checkpoint from git notes to determine phase/round
# Storage: STILL writes to Git - just smarter about parameters
```

## Corrected Architecture Principle

**"Git is epistemic truth, SQLite is session tracking, JSON is interchange"**

Git:
- ✅ Epistemic vectors (KNOW, DO, UNCERTAINTY, etc.)
- ✅ Checkpoints (compressed state)
- ✅ Goals (cross-AI discovery)
- ✅ Handoffs (learning deltas)
- ✅ ALL learning/epistemic data

SQLite:
- ✅ Session metadata (who, when, status)
- ✅ Basic tracking (cascades count, timestamps)
- ✅ Quick queries (list sessions, check status)
- ❌ NOT epistemic vectors (those are in Git)

JSON:
- ✅ CLI output format (--output json)
- ✅ Import/export
- ✅ API responses
- ❌ NOT storage (it's an output format)

## What Actually Needs Simplifying

### 1. Parameter Consolidation (CLI interface)
**Problem:** Too many flags
**Solution:** Group related params into JSON objects
**Storage impact:** NONE - just easier to use

### 2. Smart Defaults (infer from Git)
**Problem:** Must specify phase/round manually
**Solution:** Read from git notes to auto-detect
**Storage impact:** NONE - just smarter parameter handling

### 3. Consistent --output json
**Problem:** Some commands don't support it
**Solution:** Add --output json everywhere
**Storage impact:** NONE - just output formatting

### 4. MCP-CLI 1:1 Mapping
**Problem:** Parameter names differ between MCP and CLI
**Solution:** Make CLI accept MCP param names directly
**Storage impact:** NONE - just reduces translation bugs

## Git-Centric Operations (Keep These!)

All these commands read/write Git - **DO NOT CHANGE STORAGE:**

```bash
checkpoint-create    → writes git notes (epistemic state)
checkpoint-load      → reads git notes (restore state)
goals-create         → writes git notes (cross-AI discovery)
goals-discover       → reads git notes (from other repos)
handoff-create       → writes git notes (session continuity)
preflight-submit     → writes git notes (initial epistemic state)
postflight-submit    → writes git notes (final epistemic state + delta)
```

SQLite is just for quick lookups like "list my sessions" or "when did I start?"

## What We're Actually Fixing

### ✅ Easy Fixes (CLI interface only):
1. Add --output json to 3 commands
2. Consolidate scope flags (3 flags → 1 JSON)
3. Fix MCP parameter name mismatches

### ✅ Medium Fixes (smarter parameter handling):
4. Auto-infer phase/round by reading from git
5. Accept partial vectors with defaults
6. Reduce arg_map in MCP server

### ❌ NOT Changing:
- Git as primary epistemic storage
- SQLite as session metadata
- JSON as output format
- Any storage backends or data flow

## Corrected Simplification Goals

**Goal:** Reduce CLI complexity by 40% WITHOUT changing storage architecture

How:
1. Fewer flags (group into JSON objects)
2. Smarter defaults (infer from git state)
3. Consistent output (--output json everywhere)
4. Better MCP-CLI alignment (no parameter translation)

Storage architecture remains: **Git for epistemic, SQLite for metadata, JSON for output**

---

**Bottom Line:**

We're simplifying the **USER INTERFACE** (CLI flags), not the **STORAGE ARCHITECTURE** (Git/SQLite/JSON).

Git remains the epistemic brain, SQLite remains the session tracker, JSON remains the output format.
