# Storage Flow Compliance Tests

## Purpose

These tests verify the fix for the critical storage flow violation where
preflight-submit, check-submit, and postflight-submit were bypassing the
3-layer storage architecture.

## What's Tested

### 1. Three Storage Layers
All workflow commands must write to:
- **SQLite** - Queryable, structured data
- **Git Notes** - Compressed, distributed, signable
- **JSON Logs** - Full audit trail

### 2. Cross-AI Features
Tests that features dependent on git notes work:
- `checkpoint-load` - Loads from git notes
- `handoff-create` - Reads epistemic data from git notes
- `goals-discover` - Cross-AI goal discovery (if available)

### 3. No Regressions
- GitEnhancedReflexLogger is standalone (no inheritance)
- Workflow commands use new API (not old SessionDatabase)

## Running Tests

```bash
# Run all storage flow tests
pytest tests/integration/test_storage_flow_compliance.py -v

# Run specific test
pytest tests/integration/test_storage_flow_compliance.py::TestStorageFlowCompliance::test_preflight_submit_creates_all_three_layers -v

# Run with detailed output
pytest tests/integration/test_storage_flow_compliance.py -v --tb=short
```

## Expected Results

All tests should **PASS** if the storage flow fix is working correctly.

If tests fail:
- Check git is available (`git --version`)
- Check empirica CLI is in PATH
- Check .empirica_reflex_logs directory permissions
- Review test output for specific failures

## Test Coverage

- ✅ preflight-submit → 3-layer storage
- ✅ check-submit → 3-layer storage
- ✅ postflight-submit → 3-layer storage
- ✅ checkpoint-load works (reads git notes)
- ✅ handoff-create works (reads git notes)
- ✅ No inheritance bloat
- ✅ Correct API usage

## Notes

- Tests create a temporary session with `--ai-id storage-flow-test`
- Tests verify git notes exist via `git for-each-ref`
- JSON logs are checked in `.empirica_reflex_logs/` directory
- Tests are safe to run multiple times (creates new sessions)

## Maintenance

If storage architecture changes:
1. Update tests to match new architecture
2. Ensure 3-layer principle is maintained
3. Add tests for new storage layers if added
