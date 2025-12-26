# Vector Continuity Audit

**Purpose:** Verify all epistemic vector states are captured at the right moments across CASCADE workflow and memory compacting

**Date:** 2025-12-26
**Session:** 8ddc7f2c-72fa-45d9-8036-cf341ca6b6fd

---

## Critical Questions

1. **Are we recording all vector states correctly?**
2. **Is there consistency in when measurements are taken?**
3. **Do snapshots capture enough context for continuity?**
4. **Should past snapshots be importance-weighted (impact + completion)?**

---

## Vector Capture Points (Current State)

### 1. PREFLIGHT (Baseline)
**When:** Session start, before work begins
**Vectors captured:**
- `engagement`, `know`, `uncertainty`
- `scope_breadth`, `scope_duration`, `scope_coordination`
- Optional: task-specific vectors

**Storage:**
- ✅ SQLite reflexes table (via GitEnhancedReflexLogger)
- ✅ Git notes (empirica/reflexes ref)
- ✅ JSON logs (.empirica/logs/)

**Continuity:** ✅ WORKS - Baseline preserved

---

### 2. CHECK (Decision Gates)
**When:** Mid-work, at decision points (proceed vs investigate)
**Vectors captured:**
- Full 13-vector suite (engagement, know, do, context, clarity, coherence, signal, density, state, change, completion, impact, uncertainty)
- `decision` (proceed/investigate)
- `confidence` (calculated)

**Storage:**
- ✅ SQLite reflexes table
- ✅ Git notes
- ✅ JSON logs

**Continuity:** ✅ WORKS - Decision points tracked

---

### 3. POSTFLIGHT (Completion)
**When:** Work complete, measure learning
**Vectors captured:**
- Same 13-vector suite as CHECK
- **Learning deltas** (calculated: POSTFLIGHT - PREFLIGHT)

**Storage:**
- ✅ SQLite reflexes table
- ✅ Git notes
- ✅ JSON logs

**Continuity:** ✅ WORKS - Learning measured

---

### 4. PRE-COMPACT (Before Memory Loss)
**When:** Auto-compact or manual `/compact` trigger
**Vectors captured:**
- **Current checkpoint vectors** (most recent PREFLIGHT/CHECK/POSTFLIGHT)
- Bootstrap summary counts (findings, unknowns, goals, dead_ends)
- Investigation context (cycle, round, scope_depth) if provided

**Storage:**
- ✅ JSON snapshot (.empirica/ref-docs/pre_summary_<timestamp>.json)
- ✅ Database ref-docs table (project_reference_docs)

**Issues found:**
- ⚠️  Loads most recent checkpoint regardless of phase
- ⚠️  If last checkpoint was PREFLIGHT, pre-compact snapshot has baseline (not current state)
- ⚠️  Missing: Should capture CURRENT epistemic state, not just last checkpoint

**Continuity:** ⚠️  PARTIAL - May miss current state if no recent checkpoint

---

### 5. POST-COMPACT (After Memory Restoration)
**When:** SessionStart hook after compact
**Vectors captured:**
- **Pre-compact snapshot** loaded for comparison
- **Bootstrap evidence** loaded as anchor

**Storage:**
- ✅ Presented via check-drift output (stderr for user visibility)

**Issues found:**
- ⚠️  No fresh vector assessment captured at this point
- ⚠️  Relies on user running new PREFLIGHT/CHECK manually

**Continuity:** ⚠️  PARTIAL - Evidence presented but no fresh measurement

---

## Identified Gaps

### Gap 1: Current State Not Captured Pre-Compact
**Problem:** Pre-compact snapshot uses last checkpoint, which might be old
**Example:**
```
PREFLIGHT at 10:00 → vectors saved
Work for 2 hours (no CHECK)
Autocompact at 12:00 → snapshot has 10:00 vectors (stale!)
```

**Impact:** Drift detection compares old vectors to new, not true before/after compact

**Fix needed:** Add fresh vector assessment in pre-compact hook OR auto-run CHECK before compact

---

### Gap 2: No Post-Compact Fresh Assessment
**Problem:** After compact, we load evidence but don't capture new vector state
**Example:**
```
Pre-compact: impact=0.8, completion=0.6
[COMPACT HAPPENS]
Post-compact: Evidence loaded, but no fresh vectors captured
User continues working...
Next CHECK: Compares to PRE-compact baseline (missed the restoration point)
```

**Impact:** Can't measure drift caused by compact itself

**Fix needed:** Auto-prompt CHECK or PREFLIGHT after post-compact hook

---

### Gap 3: Snapshot Importance Weighting Missing
**Problem:** Bootstrap loads ALL ref-docs by timestamp, not importance
**Current:** `ORDER BY created_timestamp DESC`
**Needed:** `ORDER BY (impact * 0.6 + completion * 0.4) DESC LIMIT 5`

**Impact:** User gets 5 most recent snapshots, not 5 most important

**Fix needed:** Parse doc_data JSON, extract vectors, calculate importance score

---

### Gap 4: Old Snapshots Accumulate
**Problem:** Every compact creates new snapshot, no cleanup
**Current:** 5 snapshots in .empirica/ref-docs/ from recent sessions
**Needed:** Archive snapshots with completion >= 0.9 (work done)

**Impact:** Context pollution, bootstrap loads completed work as "current"

**Fix needed:** Snapshot curation based on completion vector

---

## Recommendations

### R1: Capture Fresh State Pre-Compact (HIGH PRIORITY)
```python
# In pre-compact hook, before saving snapshot:
# Option A: Auto-run CHECK to get current state
subprocess.run(['empirica', 'check', '-'], input=auto_assessment_json)

# Option B: Capture vectors from current work context (statusline?)
# Then save snapshot with CURRENT vectors, not last checkpoint
```

### R2: Capture Fresh State Post-Compact (HIGH PRIORITY)
```python
# In post-compact hook, after loading evidence:
# Prompt user (or auto-run) PREFLIGHT to establish new baseline
print("💡 Recommended: Run PREFLIGHT to assess current state after compact")
```

### R3: Importance-Weighted Snapshot Loading (MEDIUM PRIORITY)
```python
def get_project_reference_docs_by_importance(project_id: str, limit: int = 5):
    """Load top N snapshots by importance (impact * 0.6 + completion * 0.4)"""
    cursor = self._execute("""
        SELECT * FROM project_reference_docs
        WHERE project_id = ? AND doc_type = 'pre_summary_snapshot'
    """, (project_id,))

    snapshots = []
    for row in cursor.fetchall():
        doc_data = json.loads(row['doc_data'])
        vectors = doc_data.get('checkpoint', {}).get('vectors', {})

        # Calculate importance score
        impact = vectors.get('impact', 0.5)
        completion = vectors.get('completion', 0.0)
        importance = impact * 0.6 + (1 - completion) * 0.4  # Active work more important

        snapshots.append({
            **dict(row),
            'importance': importance,
            'impact': impact,
            'completion': completion
        })

    # Sort by importance, return top N
    snapshots.sort(key=lambda x: x['importance'], reverse=True)
    return snapshots[:limit]
```

### R4: Snapshot Archival/Curation (MEDIUM PRIORITY)
```python
# In SessionEnd hook or periodic cleanup:
def archive_completed_snapshots(project_id: str):
    """Move snapshots with completion >= 0.9 to archive"""
    snapshots = get_project_reference_docs(project_id)

    for snap in snapshots:
        doc_data = json.loads(snap['doc_data'])
        completion = doc_data.get('checkpoint', {}).get('vectors', {}).get('completion', 0.0)

        if completion >= 0.9:
            # Move to archive subdirectory
            old_path = Path(snap['doc_path'])
            archive_path = old_path.parent / '_archive' / old_path.name
            old_path.rename(archive_path)

            # Update database
            update_reference_doc(snap['id'], doc_path=str(archive_path))
```

---

## Test Plan

### T1: Vector Continuity Test
1. Start session with PREFLIGHT (capture baseline)
2. Work and run CHECK twice (capture decision points)
3. Trigger manual compact (verify pre-compact captures LATEST checkpoint)
4. Verify post-compact loads evidence correctly
5. Run new PREFLIGHT (establish new baseline)
6. Compare: old vectors → compact → new vectors (measure drift)

### T2: Importance Weighting Test
1. Create 5 snapshots with varying impact/completion:
   - Snapshot A: impact=0.9, completion=0.1 (high importance, active work)
   - Snapshot B: impact=0.8, completion=0.9 (completed, should archive)
   - Snapshot C: impact=0.3, completion=0.2 (low importance)
   - Snapshot D: impact=0.7, completion=0.5 (medium importance)
   - Snapshot E: impact=0.9, completion=0.8 (high impact, mostly done)
2. Load bootstrap with importance weighting
3. Verify order: A > D > E > C (B archived)

### T3: Snapshot Archival Test
1. Create completed snapshot (completion=0.95)
2. Run archival function
3. Verify moved to _archive/
4. Verify bootstrap doesn't load archived snapshots

---

## Current Status

✅ **Fixed:**
- SessionDatabase method names (generate_project_bootstrap → bootstrap_project_breadcrumbs)
- JSON output contamination in check-drift
- Pre-compact hook now saves snapshots successfully
- Post-compact hook loads evidence correctly

⚠️  **Partial:**
- Vector states captured at CASCADE gates (PREFLIGHT/CHECK/POSTFLIGHT)
- Snapshots load in bootstrap (but not importance-weighted)

❌ **Missing:**
- Fresh state capture pre-compact (uses last checkpoint, may be stale)
- Fresh state capture post-compact (no auto-assessment)
- Importance-weighted snapshot loading
- Snapshot archival/curation

---

## Next Steps

1. **Immediate:** Test hooks with real autocompact to verify they fire
2. **High Priority:** Implement fresh state capture pre/post compact
3. **Medium Priority:** Add importance-weighted snapshot loading
4. **Medium Priority:** Implement snapshot archival based on completion
5. **Document:** Update CASCADE workflow docs with vector capture points
