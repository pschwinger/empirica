# Goal Handoff Bug - Quick Fix Summary

## Problem
Multi-AI goal handoff wasn't working - goals were stored but invisible.

## Root Causes
1. **`discover_goals()`** used wrong git command (`git notes list` vs `git for-each-ref`)
2. **`add_lineage()`** overwrote lineage when updating goals

## Solution
**File:** `empirica/core/canonical/empirica_git/goal_store.py`

### Change 1: Fix discovery (lines 189-255)
```python
# OLD: git notes list (doesn't work with custom refs)
result = subprocess.run(['git', 'notes', 'list'], ...)

# NEW: git for-each-ref (works correctly)
result = subprocess.run(['git', 'for-each-ref', 'refs/notes/empirica/goals/'], ...)
```

### Change 2: Preserve lineage (lines 72-143, 257-293)
```python
# Added parameter to store_goal()
def store_goal(..., lineage: Optional[List[Dict[str, str]]] = None):
    payload = {
        'lineage': lineage or [...]  # Use provided or create new
    }

# Updated add_lineage() to pass lineage
return self.store_goal(..., lineage=goal_data['lineage'])
```

## Verification
✅ All 7 goals discoverable  
✅ Filter by AI works  
✅ Lineage tracking works  
✅ 4 regression tests pass  

## Impact
- ✅ Multi-AI coordination now works
- ✅ Goals can be discovered and resumed
- ✅ Complete audit trail maintained

## Commands Now Working
```bash
# Discover goals from specific AI
empirica goals-discover --from-ai-id rovodev

# Resume any goal
empirica goals-resume <goal-id> --ai-id <your-ai>

# Lineage is tracked automatically
git notes --ref=empirica/goals/<goal-id> show HEAD | jq '.lineage'
```

**Status:** ✅ Fixed and tested  
**Date:** 2025-12-01
