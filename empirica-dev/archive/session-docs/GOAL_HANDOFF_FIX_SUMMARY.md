# Goal Handoff Bug Fix - Summary

## Problem
Goals created for multi-AI coordination were stored in git notes but could not be discovered by other AIs. The `discover_goals()` function was failing silently.

## Root Cause Analysis

### Issue 1: Wrong git command in `discover_goals()`
**File:** `empirica/core/canonical/empirica_git/goal_store.py`

**Problem:**
- Used `git notes list` which doesn't properly enumerate custom note refs
- Goals stored as `refs/notes/empirica/goals/<goal-id>` were invisible

**Evidence:**
```bash
$ git notes list
# Returns nothing or errors

$ git for-each-ref refs/notes/empirica/goals/
# Returns all goal refs correctly
```

### Issue 2: Lineage tracking broken in `add_lineage()`
**Problem:**
- `store_goal()` always created fresh lineage array
- Updated lineage was overwritten when re-storing goals
- Cross-AI coordination tracking lost

## Solution

### Fix 1: Use `git for-each-ref` for discovery
**Changed:** Lines 189-255 in `goal_store.py`

```python
# Before (broken):
result = subprocess.run(['git', 'notes', 'list'], ...)

# After (working):
result = subprocess.run(['git', 'for-each-ref', 'refs/notes/empirica/goals/'], ...)
```

**Parsing change:**
```python
# Before: Expected "hash refs/..." format
ref = parts[1] if len(parts) > 1 else parts[0]
if not ref.startswith('empirica/goals/'):  # Wrong prefix!

# After: Parse tab-separated format correctly
parts = line.split('\t')
ref = parts[1]  # refs/notes/empirica/goals/<goal-id>
if not ref.startswith('refs/notes/empirica/goals/'):  # Correct!
```

### Fix 2: Preserve lineage when updating goals
**Changed:** Lines 72-143 and 257-293 in `goal_store.py`

**Added parameter to `store_goal()`:**
```python
def store_goal(
    ...,
    lineage: Optional[List[Dict[str, str]]] = None  # NEW
) -> bool:
```

**Updated payload construction:**
```python
'lineage': lineage or [  # Use provided lineage or create new
    {
        'ai_id': ai_id,
        'timestamp': datetime.now(UTC).isoformat(),
        'action': 'created'
    }
]
```

**Fixed `add_lineage()` to pass updated lineage:**
```python
return self.store_goal(
    ...,
    lineage=goal_data['lineage']  # Pass updated lineage!
)
```

## Verification

### Test 1: Discovery works
```bash
$ empirica goals-discover
🔍 Discovered 7 goal(s)

$ empirica goals-discover --from-ai-id rovodev
🔍 Discovered 2 goal(s) from rovodev
```

### Test 2: Lineage tracking works
```bash
$ empirica goals-resume de18de49-6edf-40fc-95b5-96971fe8d5f5 --ai-id copilot-claude

$ git notes --ref=empirica/goals/de18de49... show HEAD | jq '.lineage'
[
  {
    "ai_id": "copilot-claude",
    "timestamp": "2025-12-01T16:07:55...",
    "action": "created"
  },
  {
    "ai_id": "copilot-claude",
    "timestamp": "2025-12-01T16:14:44...",
    "action": "resumed"
  }
]
```

### Test 3: All 4 documentation goals discoverable
✅ Goal 1 (Gemini): `87c8f1e3...` - Production docs audit  
✅ Goal 2 (Qwen): `9facdb1b...` - User docs creation  
✅ Goal 3 (Copilot Claude): `de18de49...` - CLI/MCP documentation  
✅ Goal 4 (RovoDev): `92848363...` - Integration & cleanup  

## Impact

### Before Fix
- ❌ Goals invisible to other AIs
- ❌ No cross-AI coordination possible
- ❌ Multi-AI workflows broken
- ❌ Lineage tracking lost on resume

### After Fix
- ✅ All goals discoverable via `goals-discover`
- ✅ Filter by AI creator works correctly
- ✅ Goals can be resumed by any AI
- ✅ Complete lineage tracking maintained
- ✅ Multi-AI documentation workflow unblocked

## Files Changed
1. `empirica/core/canonical/empirica_git/goal_store.py` (2 functions fixed)
   - `discover_goals()` - Fixed git command and parsing
   - `store_goal()` - Added lineage parameter
   - `add_lineage()` - Pass lineage to store_goal

## Next Steps for Multi-AI Coordination

Each AI can now:

1. **Discover available goals:**
   ```bash
   empirica goals-discover --from-ai-id rovodev
   ```

2. **Resume their assigned goal:**
   ```bash
   empirica goals-resume <goal-id> --ai-id <their-ai>
   ```

3. **Start work with PREFLIGHT:**
   ```bash
   empirica preflight "Documentation work" --ai-id <their-ai>
   ```

4. **Track progress via lineage:**
   - Every resume/complete action is recorded
   - Full audit trail of which AI worked on what
   - Enables true cross-AI collaboration

## Technical Notes

- Git notes refs use full path: `refs/notes/empirica/goals/<uuid>`
- `git notes list` only works with default refs
- `git for-each-ref` required for custom ref namespaces
- Lineage must be preserved across updates (immutable append-only log)

---

**Fixed:** 2025-12-01  
**Verified:** All 7 goals discoverable, lineage tracking confirmed  
**Status:** ✅ Ready for multi-AI coordination
