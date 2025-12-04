# Test Instructions for Qwen

## Mission:
Run integration tests to validate today's massive simplification (6,136 lines removed).

## Quick Start:

```bash
cd /home/yogapad/empirical-ai/empirica
source .venv-mcp/bin/activate

# Run storage flow compliance tests
pytest tests/integration/test_storage_flow_compliance.py -v --tb=short

# Expected: All tests should PASS
# If failures occur, document them and report back
```

## What Was Changed Today:

1. ✅ Removed dual loggers (storage flow now consistent)
2. ✅ Removed 2,459 lines of legacy metacognition code
3. ✅ Removed 1,493 lines of dead calibration code
4. ✅ Removed 497 lines of auto_tracker bloat
5. ✅ Simplified bootstrap (1,091 lines removed)
6. ✅ Fixed SessionDatabase API
7. ✅ Fixed sessions-list --output json

## Tests to Run:

### Primary: Storage Flow Compliance (7 tests)
```bash
pytest tests/integration/test_storage_flow_compliance.py -v
```

**Expected Results:**
- ✅ test_preflight_submit_creates_all_three_layers
- ✅ test_check_submit_creates_all_three_layers
- ✅ test_postflight_submit_creates_all_three_layers
- ✅ test_checkpoint_load_works
- ✅ test_handoff_create_works
- ✅ test_git_enhanced_reflex_logger_imports
- ✅ test_workflow_commands_use_correct_api

### Optional: Quick Smoke Test
```bash
# Test bootstrap
empirica bootstrap --ai-id qwen-test --level standard

# Test workflow
empirica preflight-submit --session-id <session-id> \
  --vectors '{"know":0.8,"do":0.9,"uncertainty":0.2}' \
  --reasoning "Testing simplified system"

# Test sessions list with JSON
empirica sessions-list --limit 5 --output json
```

## What to Report:

### If ALL PASS ✅
Report: "All tests passed! 6,136 line removal validated."

### If ANY FAIL ❌
Report:
1. Which test failed
2. Error message
3. Whether it's critical or can be deferred

## Context:

We removed massive amounts of bloat:
- Legacy 12-vector system (now 13-vector standard)
- Dual logger paths (now single git_logger)
- Dead calibration code
- Theater bootstrap components

Everything should still work because:
- Components created on-demand
- Storage flow properly follows 3-layer architecture
- APIs made backwards compatible

## Time Estimate:

**5-10 minutes** for full test suite + smoke test

---

**Ready to go!** Just run the pytest command above.
