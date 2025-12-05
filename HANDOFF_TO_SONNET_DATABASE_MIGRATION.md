# Handoff to Claude Sonnet: Database Schema Migration

**Date:** December 5, 2025
**From:** Claude Code (Implementer, Haiku)
**To:** Claude Sonnet (Architect, High-Reasoning)
**Status:** Ready for Implementation
**Urgency:** High (blocking pre-deployment)

---

## TL;DR

**Your Task:** Migrate 11 code files from deprecated epistemic tables to the canonical `reflexes` table

**Why:** Pre-deployment uniformity. Currently have 4 deprecated tables + 1 canonical table = confusion

**What's Prepared:** Complete migration spec with file-by-file changes (see below)

**Timeline:** 4-6 hours (mostly testing and verification)

**Difficulty:** Medium (straightforward refactoring, but affects many files)

---

## The Problem You're Solving

### Current State
```
Database Schema: FRAGMENTED
├── reflexes (NEW, canonical)     ← Where CASCADE phases write
├── preflight_assessments (OLD)   ← Still used by 11 code files
├── postflight_assessments (OLD)  ← Still used by 11 code files
├── check_phase_assessments (OLD) ← Still used by 11 code files
└── epistemic_assessments (OLD)   ← Unused, can delete
```

### Problem
- **Code reads/writes deprecated tables:** 11 files making direct queries
- **Two competing systems:** Old tables + new reflexes table
- **Maintenance burden:** Changes must update multiple schemas
- **Pre-deployment blocker:** Can't ship with this architecture

### Solution
Migrate all code to use `reflexes` table exclusively, delete deprecated tables

---

## What's Ready For You

### 1. Comprehensive Migration Specification
**Location:** `/docs/MIGRATION_SPEC_DATABASE_SCHEMA_UNIFORMITY.md` (400+ lines)

Contains:
- Detailed mapping of old tables → reflexes table
- File-by-file changes (code examples provided)
- Testing checklist
- Data migration script (auto-runs on existing databases)
- Rollback plan

### 2. Already Implemented (No Changes Needed)
```python
# These SessionDatabase methods ALREADY USE reflexes (no change):
db.store_vectors(session_id, phase, vectors)
db.get_latest_vectors(session_id, phase=None)
db.get_vectors_by_phase(session_id, phase)
```

### 3. Code Dependencies Documented
```
11 files need updates:
- 1 CRITICAL: session_database.py (affects all others)
- 2 HIGH: report_generator.py, sessions.py (API)
- 5 LOW: Test files
- 4 LOW: Utility/example files
```

---

## Critical Decision: Start Here

### session_database.py (Lines 1174-1206)

**Current (Deprecated):**
```python
def get_preflight_assessment(self, session_id: str):
    cursor.execute("SELECT * FROM preflight_assessments WHERE session_id = ?")
```

**After Your Changes (Canonical):**
```python
def get_preflight_vectors(self, session_id: str) -> Optional[Dict]:
    """Get latest PREFLIGHT vectors for session"""
    return self.get_latest_vectors(session_id, phase="PREFLIGHT")
```

**Why This Matters:** All other code calls `get_preflight_assessment()`. By updating SessionDatabase, you update 70% of dependent code automatically.

---

## Files to Update (Priority Order)

### PRIORITY 1: session_database.py
**Lines to Remove:**
- 72-162: Old table migrations
- 175-226: epistemic_assessments table
- 327-356: preflight_assessments table
- 358-377: check_phase_assessments table
- 379-412: postflight_assessments table
- 658-703: log_epistemic_assessment() method
- 799-859: log_preflight_assessment() method
- 861-914: log_check_phase_assessment() method
- 916-974: log_postflight_assessment() method
- 1174-1206: get_preflight/check/postflight_assessment() methods

**Lines to Add (New convenience methods):**
```python
def get_preflight_vectors(self, session_id: str) -> Optional[Dict]
def get_check_vectors(self, session_id: str, cycle: Optional[int] = None) -> List[Dict]
def get_postflight_vectors(self, session_id: str) -> Optional[Dict]
def get_vectors_by_phase(self, session_id: str, phase: str) -> List[Dict]
```

**Lines to Update:**
- 1434-1508: _get_checkpoint_from_reflexes() - Remove fallback to old tables
- 1239-1320: get_session_summary() - Use reflexes instead of cascade_metadata

### PRIORITY 2: report_generator.py (Lines 268-348)
Replace direct table queries with SessionDatabase calls:
```python
# OLD
cursor.execute("SELECT * FROM preflight_assessments WHERE session_id = ?")

# NEW
db = SessionDatabase()
vectors_data = db.get_latest_vectors(session_id, phase="PREFLIGHT")
```

**Files Affected:** 2 methods (_get_preflight_assessment, _get_postflight_assessment)

### PRIORITY 3: sessions.py (API Routes, Lines 207-245)
Update `get_session_checks()` endpoint to use reflexes:
```python
# Use db.get_vectors_by_phase() instead of direct check_phase_assessments query
```

### PRIORITY 4-11: Test Files & Utilities
- Update PRAGMA schema queries
- Replace INSERT statements with SessionDatabase.store_vectors()
- Update example code

---

## Testing Checklist (For Your Use)

- [ ] Unit tests: SessionDatabase methods work with reflexes only
- [ ] Integration tests: Handoff reports generate correctly
- [ ] API tests: Session endpoints return correct data
- [ ] Dashboard tests: Statusline displays cognitive load correctly
- [ ] Data integrity: Migration script preserves all data (row count check)
- [ ] Backward compat: Existing databases auto-migrate on first run
- [ ] Grep verification: No stray queries to old tables remain

---

## Implementation Approach (Recommended)

### Phase 1: Setup (30 min)
1. Create `test_reflexes_migration.py` test file
2. Write tests for new convenience methods before implementing them
3. Verify tests fail (TDD approach)

### Phase 2: Core Migration (2-3 hours)
1. Update session_database.py (methods + schema)
2. Update report_generator.py
3. Update sessions.py API
4. Run integration tests after each file

### Phase 3: Cleanup (1 hour)
1. Update test files (5 files)
2. Update utilities and examples
3. Run full test suite

### Phase 4: Verification (1 hour)
1. Grep for stray old-table queries: `grep -r "FROM preflight_assessments" .`
2. Verify no queries remain
3. Migration data loss check
4. Review code for any missed dependencies

---

## Data Backward Compatibility

**Important:** You don't need to handle this in code. The spec includes an automatic migration function in `_create_tables()`:

```python
def _migrate_if_needed(self):
    """Auto-migrates old tables → reflexes on first init"""
    # Migrates preflight_assessments → reflexes WHERE phase='PREFLIGHT'
    # Migrates check_phase_assessments → reflexes WHERE phase='CHECK'
    # Migrates postflight_assessments → reflexes WHERE phase='POSTFLIGHT'
    # Then drops old tables
```

This runs automatically when SessionDatabase initializes, so:
- ✅ Existing databases auto-upgrade
- ✅ No data loss
- ✅ Zero manual migration needed

---

## Key Code Patterns You'll Use

### Pattern 1: Get Latest Assessment
**OLD:**
```python
cursor.execute("SELECT * FROM preflight_assessments WHERE session_id = ? ORDER BY assessed_at DESC LIMIT 1")
```

**NEW:**
```python
vectors_data = db.get_latest_vectors(session_id, phase="PREFLIGHT")
# Returns: {'vectors': {...}, 'timestamp': ..., 'phase': ...}
```

### Pattern 2: Get All Checks
**OLD:**
```python
cursor.execute("SELECT * FROM check_phase_assessments WHERE session_id = ?")
```

**NEW:**
```python
checks = db.get_vectors_by_phase(session_id, phase="CHECK")
# Returns: List of dicts with all vectors, timestamps, rounds
```

### Pattern 3: Access Vector Values
**OLD:**
```python
row['know']  # Direct column access
row['density']
```

**NEW:**
```python
vectors_data['vectors']['know']  # Access through nested dict
vectors_data['vectors']['density']
```

---

## Gotchas to Avoid

1. **Don't forget the migration function** - Add `_migrate_if_needed()` to `_create_tables()`
2. **Verify round numbers** - CHECK phases use `round` column (auto-incremented), old tables used `investigation_cycle`
3. **JSON parsing** - reflex_data is JSON string, needs `json.loads()` to access metadata
4. **Timestamp handling** - reflexes uses UNIX timestamp (float), old tables used DATETIME string
5. **Phase naming** - Must use uppercase: 'PREFLIGHT', 'CHECK', 'POSTFLIGHT'

---

## References

### Full Specification
👉 `/docs/MIGRATION_SPEC_DATABASE_SCHEMA_UNIFORMITY.md` (read section IV for file-by-file details)

### Related Code
- `empirica/data/session_database.py` - SessionDatabase class
- `empirica/core/canonical/git_enhanced_reflex_logger.py` - How reflexes table is used elsewhere
- `empirica/core/handoff/report_generator.py` - Example of old queries that need updating

### Tests to Reference
- `tests/integration/test_reflex_logging_integration.py` - How reflexes is tested
- `tests/test_phase1.6_handoff_reports.py` - Handoff report tests (update these)

---

## Success Metrics

✅ All 11 files updated to use reflexes only
✅ All tests pass (unit + integration + API)
✅ No queries to deprecated tables remain (grep clean)
✅ Data migration works on test database
✅ Code review approval
✅ Documentation updated

---

## Questions to Clarify (Before You Start)

1. **Timing:** Can you start immediately or need context window prep?
2. **Testing:** Should I set up a test database for you to validate against?
3. **Review:** Do you want intermediate PRs (1 per file group) or 1 final PR?
4. **Scope:** Should you also update documentation references to deprecated tables?

---

## Handoff Summary

| Item | Status |
|------|--------|
| Migration spec written | ✅ Complete |
| Code examples provided | ✅ Complete |
| SessionDatabase API ready | ✅ Already implemented |
| Test approach documented | ✅ Complete |
| Backward compat script ready | ✅ Included in spec |
| Rollback plan documented | ✅ Complete |
| Ready for implementation | ✅ YES |

---

## Next Steps

1. **You (Sonnet):** Review migration spec and code examples
2. **You:** Start with session_database.py (critical path)
3. **You:** Test each file update before moving to next
4. **Codebase:** Full integration testing after all files updated
5. **Deployment:** Database schema cleanup (old tables deleted)

Good luck! This is high-value work for deployment readiness. 🚀
