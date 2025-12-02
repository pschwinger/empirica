# Test Suite for Checkpoint & Goals System Bugs

**Created:** 2025-12-01  
**Purpose:** Regression tests for bugs found during audit  
**For:** Qwen (bug fixing AI)

---

## Overview

Two new comprehensive test files created to catch bugs that existing tests missed:

1. **`tests/integrity/test_checkpoint_bugs_regression.py`**
   - Unit + integration tests for specific bugs
   - 350+ lines of test code
   - 4 test classes, 20+ test methods

2. **`tests/integration/test_e2e_workflows.py`**
   - End-to-end workflow tests
   - 300+ lines of test code
   - 4 test classes covering full user journeys

---

## Why Existing Tests Didn't Catch These Bugs

### Problem 1: Database Mocking
```python
# Existing test (tests/unit/test_git_enhanced_reflex_logger.py)
@patch('subprocess.run')
def test_add_checkpoint_creates_sqlite_fallback(self, mock_run):
    # This mocks subprocess, so doesn't test ACTUAL database
    # Missing reflexes table not caught!
```

**Our fix:**
```python
# New test (tests/integrity/test_checkpoint_bugs_regression.py)
def test_reflexes_table_exists(self, db_path):
    # Tests REAL database, catches missing table
    conn = sqlite3.connect(db_path)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reflexes'")
```

### Problem 2: Missing Method Not Tested
```python
# Existing test only tested add_checkpoint and get_last_checkpoint
# Never tested list_checkpoints (didn't exist!)
```

**Our fix:**
```python
# New test explicitly tests list_checkpoints
def test_list_checkpoints_method_exists(self, git_logger):
    assert hasattr(git_logger, 'list_checkpoints')
    assert callable(git_logger.list_checkpoints)
```

### Problem 3: No Vector Validation
```python
# Existing tests created checkpoints but never verified vectors were populated
```

**Our fix:**
```python
# New test verifies vectors are NOT empty
def test_checkpoint_create_includes_vectors(self):
    checkpoint = git_logger.get_last_checkpoint()
    assert checkpoint["vectors"] != {}
    assert len(checkpoint["vectors"]) == 13
```

---

## How to Run Tests

### Quick Test (Run After Each Fix)

```bash
# Test list_checkpoints method
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointListMethod -v

# Test reflexes table
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestReflexesTableSchema -v

# Test vector storage
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointVectorStorage -v
```

### Full Regression Suite

```bash
# All regression tests
pytest tests/integrity/test_checkpoint_bugs_regression.py -v

# All integration tests
pytest tests/integration/test_e2e_workflows.py -v
```

### Complete Test Run (Before Commit)

```bash
# All checkpoint-related tests (existing + new)
pytest -k "checkpoint" -v

# All goals-related tests
pytest -k "goal" -v

# Everything
pytest tests/ -v
```

---

## Test File Structure

### `test_checkpoint_bugs_regression.py`

**Class 1: TestCheckpointListMethod** (7 tests)
- ✅ Method exists
- ✅ Returns empty list when no checkpoints
- ✅ Returns created checkpoints
- ✅ Filters by session_id
- ✅ Filters by phase
- ✅ Respects limit parameter
- ✅ Sorts by timestamp (newest first)

**Class 2: TestReflexesTableSchema** (3 tests)
- ✅ Table exists in database
- ✅ Has correct columns (13 vectors + metadata)
- ✅ Can store vector data

**Class 3: TestCheckpointVectorStorage** (3 tests)
- ✅ Loads vectors from database
- ✅ Created checkpoints include vectors
- ✅ Vectors are not empty

**Class 4: TestCLICheckpointCommands** (3 tests)
- ✅ CLI command exists
- ✅ Executes without AttributeError
- ✅ Stores vectors (no "empty vectors" warning)

### `test_e2e_workflows.py`

**Class 1: TestCheckpointWorkflowE2E** (1 test)
- ✅ Full workflow: bootstrap → preflight → checkpoint → list → load
- ✅ Verifies vectors preserved throughout

**Class 2: TestGoalsWorkflowE2E** (1 test)
- ✅ Full workflow: create → add subtasks → complete → progress

**Class 3: TestDatabaseIntegrity** (1 test)
- ✅ Reflexes table exists and has correct structure

**Class 4: TestMCPToolsIntegration** (2 tests - skipped)
- ⏭️ MCP checkpoint tools (requires server)
- ⏭️ MCP goals tools (requires server)

---

## Expected Test Results

### Before Fixes (SHOULD FAIL)

```bash
$ pytest tests/integrity/test_checkpoint_bugs_regression.py -v

FAILED test_list_checkpoints_method_exists - AttributeError: 'GitEnhancedReflexLogger' object has no attribute 'list_checkpoints'
FAILED test_reflexes_table_exists - AssertionError: reflexes table must exist in database schema
FAILED test_checkpoint_create_includes_vectors - AssertionError: Checkpoint vectors must not be empty
```

### After Fixes (SHOULD PASS)

```bash
$ pytest tests/integrity/test_checkpoint_bugs_regression.py -v

PASSED test_list_checkpoints_method_exists
PASSED test_list_checkpoints_empty
PASSED test_list_checkpoints_after_create
PASSED test_reflexes_table_exists
PASSED test_reflexes_table_schema
PASSED test_checkpoint_create_includes_vectors
... (all tests pass)

========================= 20 passed in 5.23s =========================
```

---

## Test-Driven Development Workflow for Qwen

### Step 1: Run Tests (Should Fail)

```bash
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointListMethod::test_list_checkpoints_method_exists -v
```

**Expected:** FAIL (method doesn't exist)

### Step 2: Implement Fix

```python
# In empirica/core/reflex/git_reflex_logger.py
class GitEnhancedReflexLogger:
    def list_checkpoints(self, session_id=None, limit=None, phase=None):
        # Implementation here
        pass
```

### Step 3: Run Test Again (Should Pass)

```bash
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointListMethod::test_list_checkpoints_method_exists -v
```

**Expected:** PASS (method exists now)

### Step 4: Run All Related Tests

```bash
pytest tests/integrity/test_checkpoint_bugs_regression.py::TestCheckpointListMethod -v
```

**Expected:** All tests in class pass

### Step 5: Repeat for Each Bug

- Fix Bug #1 → Tests pass
- Fix Bug #2 → Tests pass
- Run full suite → All pass

### Step 6: Run E2E Tests

```bash
pytest tests/integration/test_e2e_workflows.py -v
```

**Expected:** End-to-end workflows pass

---

## CI/CD Integration

Add to GitHub Actions / GitLab CI:

```yaml
# .github/workflows/test.yml
name: Test Checkpoint & Goals Systems

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run regression tests
        run: pytest tests/integrity/test_checkpoint_bugs_regression.py -v
      
      - name: Run integration tests
        run: pytest tests/integration/test_e2e_workflows.py -v
```

---

## Coverage Report

Generate coverage to verify all code paths tested:

```bash
pytest --cov=empirica.core.reflex \
       --cov=empirica.cli.command_handlers.checkpoint_commands \
       tests/integrity/test_checkpoint_bugs_regression.py \
       --cov-report=html

# Open htmlcov/index.html to see coverage
```

**Target coverage:**
- `git_reflex_logger.py`: >80% (especially list_checkpoints)
- `checkpoint_commands.py`: >70% (CLI handlers)
- `session_db.py`: >60% (database operations)

---

## Troubleshooting Test Failures

### "Database file doesn't exist"

```bash
# Create test database first
empirica bootstrap --ai-id "test"
```

### "Git repository not found"

```bash
# Tests need to run in git repo
cd /path/to/empirica
git init  # if not already initialized
```

### "Module not found"

```bash
# Install in development mode
pip install -e .
```

### "Permission denied" on .empirica directory

```bash
# Fix permissions
chmod -R 755 ~/.empirica
```

---

## Next Steps After Tests Pass

1. ✅ All regression tests pass
2. ✅ All integration tests pass
3. ✅ Update documentation with correct behavior
4. ✅ Create git checkpoint to mark milestone
5. ✅ Create handoff report for documentation team
6. ✅ Merge fixes to main branch

---

**Test suite complete. Ready for Qwen to implement fixes!** 🚀
