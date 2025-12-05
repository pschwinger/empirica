# Spec vs Implementation - Side-by-Side Comparison

**Quick Reference**: What the code SHOULD do vs what it ACTUALLY does

---

> **📅 HISTORICAL DOCUMENT - 2025-12-05 UPDATE**
> 
> This document was created to track the gap between specification and implementation.
> 
> **✅ STATUS: IMPLEMENTATION NOW MATCHES SPEC**
> 
> The database schema uniformity migration (commit 21dd6ad1) has implemented the spec:
> - ✅ Unified `reflexes` table now in production
> - ✅ Old tables (`epistemic_assessments`, `preflight_assessments`, etc.) deprecated
> - ✅ Automatic migration preserves all historical data
> 
> This document is preserved for historical reference showing what needed to be fixed.
> The "Implementation" column now represents the OLD pre-migration state.
> 
> For current architecture, see: `docs/production/12_SESSION_DATABASE.md`

---

## PREFLIGHT Assessment Flow

### SPEC (from STORAGE_ARCHITECTURE_COMPLETE.md + CASCADE docs)

```
1. AI submits PREFLIGHT assessment with 13 vectors
   ↓
2. System calls: GitEnhancedReflexLogger.add_checkpoint()
   ├─ Writes to reflexes table (SQLite)
   ├─ Writes to git notes (refs/notes/empirica/session/{id}/PREFLIGHT/1)
   └─ Writes to JSON logs (.empirica_reflex_logs/{date}/{ai}/{session}/PREFLIGHT.json)
   ↓
3. Statusline queries: SELECT * FROM reflexes WHERE phase='PREFLIGHT'
   ↓
4. Dashboard displays: KNOW=0.75, DO=0.80, ... (actual submitted vectors)
```

### IMPLEMENTATION (cascade_commands.py:78-397)

```
1. AI submits PREFLIGHT assessment with 13 vectors
   ↓
2. System SPLITS into TWO paths:
   Path A: db.conn.execute("INSERT INTO cascade_metadata...")
   ├─ Writes vectors to cascade_metadata table (WRONG TABLE!)
   ├─ Stores as JSON string in metadata_value column
   └─ No structure, hard to query

   Path B: auto_checkpoint()
   ├─ Writes partial data to git notes
   ├─ Namespace: refs/notes/empirica/session/{id}/PREFLIGHT/1
   └─ Missing rationales, lacks full epistemic context
   ↓
3. Statusline queries: SELECT * FROM reflexes WHERE phase='PREFLIGHT'
   ↓
4. Dashboard displays: (NOTHING - preflight vectors not in reflexes table!)
```

**Storage Map:**

| What | Spec | Implementation |
|------|------|-----------------|
| **Vectors** | reflexes.know, reflexes.do, ... | cascade_metadata.metadata_value (JSON string) |
| **Phase** | reflexes.phase | cascade_metadata.metadata_key = 'preflight_vectors' |
| **Query** | `SELECT know, do FROM reflexes WHERE phase='PREFLIGHT'` | `SELECT metadata_value FROM cascade_metadata WHERE metadata_key='preflight_vectors'` |
| **Git** | refs/notes/.../PREFLIGHT/1 | refs/notes/.../PREFLIGHT/1 (partial) |
| **JSON** | .empirica_reflex_logs/2025-12-04/claude-code/abc-123/PREFLIGHT.json | Not created |

---

## CHECK Assessment Flow

### SPEC (from CASCADE + WORKFLOW docs)

```
1. AI assesses confidence and submits CHECK with 13 vectors
   → vectors = {know: 0.92, do: 0.87, clarity: 0.95, ...}
   ↓
2. System stores SUBMITTED vectors using GitEnhancedReflexLogger:
   ├─ reflexes table: know=0.92, do=0.87, clarity=0.95, ...
   ├─ git notes: Same vectors (compressed)
   └─ JSON logs: Full reasoning + vectors
   ↓
3. Drift detection: Compare CHECK vectors to PREFLIGHT vectors
   PREFLIGHT: know=0.75
   CHECK:     know=0.92
   Drift:     +0.17 ✓
```

### IMPLEMENTATION (workflow_commands.py:149-244)

```
1. AI assesses confidence and submits CHECK with 13 vectors
   → vectors = {know: 0.92, do: 0.87, clarity: 0.95, ...}
   ↓
2. System IGNORES submitted vectors, stores HARDCODED values:
   INSERT INTO epistemic_assessments (
       ..., engagement, know, do, context, clarity, ...
   ) VALUES (
       ..., 0.75, 0.7, 0.75, 0.75, 0.75, ...  ← HARDCODED!
   )
   ↓
3. Drift detection gets fake data:
   PREFLIGHT: know=0.75 (from cascade_metadata, if found)
   CHECK:     know=0.75 (hardcoded - NOT SUBMITTED)
   Drift:     0.0 (false - shows no learning!)
```

**The Catastrophic Bug:**

```python
# Lines 188-196: What gets stored
db.conn.execute("""
    INSERT INTO epistemic_assessments
    (assessment_id, cascade_id, phase, engagement, know, do, context, clarity,
     coherence, signal, density, state, change, completion, impact, uncertainty,
     overall_confidence, recommended_action, assessed_at)
    VALUES (?, ?, 'CHECK', 0.75, 0.7, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5, 0.5, 0.3, 0.5, ?, ?,
            ?, ?)
""", (str(uuid.uuid4()), cascade_id, uncertainty, confidence, recommended_action, now))
        # ↑ Only uncertainty, confidence, decision get real values
        # ↑ All 13 vectors hardcoded to 0.75, 0.7, etc.
        # ↑ What about vectors['know'], vectors['do']? IGNORED!
```

**Storage Map:**

| What | Spec | Implementation |
|------|------|-----------------|
| **Vectors** | reflexes.know=0.92, reflexes.do=0.87, ... | epistemic_assessments.know=0.75, epistemic_assessments.do=0.7 |
| **Data Source** | Submitted vectors | Hardcoded dummy values |
| **Table** | reflexes | epistemic_assessments |
| **Query** | `SELECT know, do FROM reflexes WHERE phase='CHECK'` | `SELECT know, do FROM epistemic_assessments WHERE phase='CHECK'` |
| **Accuracy** | 100% (user submitted) | 0% (hardcoded!) |

---

## POSTFLIGHT Assessment Flow

### SPEC (from CASCADE docs)

```
1. AI submits POSTFLIGHT assessment with 13 vectors
   ↓
2. System stores using GitEnhancedReflexLogger:
   ├─ reflexes table: All 13 vectors + reflex_log_path
   ├─ git notes: Vectors + metadata (compressed)
   └─ JSON logs: Full reasoning + vectors + calibration
   ↓
3. Delta calculation: PREFLIGHT vs POSTFLIGHT
   PREFLIGHT: {know: 0.75, uncertainty: 0.25, ...}
   POSTFLIGHT: {know: 0.95, uncertainty: 0.05, ...}
   Delta: {know: +0.20, uncertainty: -0.20, ...}
   ↓
4. Inspector queries: SELECT reflex_log_path FROM reflexes WHERE session_id=?
   Result: .empirica_reflex_logs/2025-12-04/claude-code/abc-123/POSTFLIGHT.json
   Inspector opens JSON → sees full reasoning, calibration data, etc.
```

### IMPLEMENTATION (cascade_commands.py:413-700)

```
1. AI submits POSTFLIGHT assessment with 13 vectors
   ↓
2. System stores PARTIALLY using GitEnhancedReflexLogger:
   ├─ epistemic_assessments table: All 13 vectors ✓
   ├─ git notes: Vectors (compressed) ✓
   └─ JSON logs: Full reasoning ✓

   BUT MISSING:
   ├─ reflexes table ✗ (should be here too!)
   └─ reflex_log_path field ✗ (never populated!)
   ↓
3. Delta calculation: PREFLIGHT vs POSTFLIGHT
   PREFLIGHT: {know: 0.75, uncertainty: 0.25, ...} (from cascade_metadata if found)
   POSTFLIGHT: {know: 0.95, uncertainty: 0.05, ...} (from epistemic_assessments)
   Delta: CALCULATED ✓ BUT NOT STORED ✗
   ↓
4. Inspector queries: SELECT reflex_log_path FROM epistemic_assessments WHERE session_id=?
   Result: NULL ✗
   Inspector can't find JSON log → debugging impossible
```

**Storage Map:**

| What | Spec | Implementation |
|------|------|-----------------|
| **Vectors** | reflexes.know, reflexes.do, ... | epistemic_assessments.know, epistemic_assessments.do, ... |
| **Table** | reflexes | epistemic_assessments |
| **reflex_log_path** | Populated with JSON path | NULL (never set) |
| **Delta Stored** | Persisted to database | Calculated but discarded |
| **Query** | `SELECT reflex_log_path FROM reflexes WHERE phase='POSTFLIGHT'` | `SELECT reflex_log_path FROM epistemic_assessments WHERE ...` → NULL |
| **Audit Trail** | Complete (path links to JSON) | Broken (path missing) |

---

## The Three Wrong Tables Problem

### Spec Intent: One Table (reflexes)

```sql
-- Single source of truth for all epistemic data:
CREATE TABLE reflexes (
    phase TEXT,  -- PREFLIGHT, CHECK, ACT, POSTFLIGHT
    engagement REAL,
    know REAL,
    do REAL,
    context REAL,
    clarity REAL,
    coherence REAL,
    signal REAL,
    density REAL,
    state REAL,
    change REAL,
    completion REAL,
    impact REAL,
    uncertainty REAL,
    reflex_data TEXT,
    reasoning TEXT,
    evidence TEXT,
    ...
)
```

### Implementation: Three Different Tables

```
PREFLIGHT → cascade_metadata (metadata_key='preflight_vectors')
CHECK     → epistemic_assessments (phase='CHECK')
POSTFLIGHT → epistemic_assessments (phase='POSTFLIGHT')

No unified query possible!
```

**Why this breaks statusline:**

```python
# Statusline tries to build learning curve:
query = """
    SELECT phase, know, uncertainty
    FROM reflexes  -- ← WRONG! Data in 3 different tables!
    WHERE session_id = ?
    ORDER BY assessed_at
"""
# Result: PREFLIGHT missing, CHECK has wrong data, POSTFLIGHT partial
```

---

## Decision Logic: Duplication

### Spec: Single Source of Truth

```python
def calculate_decision(confidence: float) -> str:
    """The ONE decision function"""
    if confidence >= 0.7:
        return "proceed"
    elif confidence <= 0.3:
        return "investigate"
    else:
        return "proceed_with_caution"
```

### Implementation: Three Different Places

**Location 1** (workflow_commands.py:186):
```python
recommended_action = "proceed" if confidence >= 0.7 else "investigate" if confidence <= 0.3 else "proceed_with_caution"
```

**Location 2** (workflow_commands.py:207):
```python
"decision": "proceed" if confidence >= 0.7 else "investigate" if confidence <= 0.3 else "proceed_with_caution",
```

**Location 3** (cascade_commands.py:268):
```python
'recommended_action': recommendation['action'],  # Where recommendation is calculated elsewhere
```

**Problem:**
- Change decision threshold in one place? Other places break!
- Test one version? Others untested!
- What's the actual decision logic? Three conflicting versions!

---

## Summary: Violations by Phase

| Phase | Correct | Actual | Type | Severity |
|-------|---------|--------|------|----------|
| **PREFLIGHT** | reflexes table | cascade_metadata | Wrong table | CRITICAL |
| **PREFLIGHT** | GitEnhancedReflexLogger | auto_checkpoint only | Incomplete storage | HIGH |
| **PREFLIGHT** | JSON logs created | JSON logs missing | Missing audit | HIGH |
| **CHECK** | Submitted vectors | Hardcoded 0.75 | Wrong data | CRITICAL |
| **CHECK** | reflexes table | epistemic_assessments | Wrong table | HIGH |
| **POSTFLIGHT** | reflex_log_path link | NULL | Missing audit link | MEDIUM |
| **POSTFLIGHT** | Delta persisted | Delta discarded | Lost insights | MEDIUM |
| **ALL** | Single decision function | 3 duplicate functions | Code maintenance | MEDIUM |

---

## Fix Priority

```
1. CRITICAL (fixes core broken workflows):
   ├─ Fix PREFLIGHT to use reflexes table
   ├─ Fix CHECK to store submitted vectors
   └─ Centralize decision logic

2. HIGH (fixes data flow):
   ├─ Add reflex_log_path to all phases
   ├─ Store deltas in database
   └─ Unify to single GitEnhancedReflexLogger path

3. MEDIUM (improves code quality):
   ├─ Remove duplicate storage paths
   ├─ Centralize decision logic
   └─ Update all tests
```

---

## How to Verify Fix

### Before Fix (broken)
```
$ empirica sessions-show abc-123
Session: abc-123

  PREFLIGHT: (not found in reflexes table)
  CHECK:     know=0.75 (hardcoded, not submitted 0.92)
  POSTFLIGHT: know=0.95, reflex_log_path=NULL (can't debug)
```

### After Fix (correct)
```
$ empirica sessions-show abc-123
Session: abc-123

  PREFLIGHT: know=0.75, do=0.80, ... (actual submitted)
  CHECK:     know=0.92, do=0.87, ... (actual submitted)
  POSTFLIGHT: know=0.95, reflex_log_path=.empirica_reflex_logs/...

  Delta PREFLIGHT→POSTFLIGHT: know +0.20, uncertainty -0.20
```

