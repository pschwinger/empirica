# auto_tracker Analysis

## Question: Is auto_tracker actually used or just overhead?

### Files that import/use auto_tracker:
1. empirica/auto_tracker.py (definition)
2. empirica/bootstraps/optimal_metacognitive_bootstrap.py
3. empirica/bootstraps/extended_metacognitive_bootstrap.py

### Let me check what auto_tracker does...

## Findings:

### auto_tracker.py (497 lines!)
- Uses ReflexLogger (line 109) - OLD API!
- Singleton pattern (complex)
- Context manager, decorator patterns (overhead)
- Only used by bootstraps

### Bootstrap Usage:
**optimal_metacognitive_bootstrap.py:**
- Line 112: Creates tracker
- Line 270: Calls `self.tracker.start_session()`
- **That's it!** Only 1 actual usage!

**extended_metacognitive_bootstrap.py:**
- Line 109: Creates tracker
- **Zero usages!** Just creates it and never uses it!

## Verdict: auto_tracker is BLOAT

**Evidence:**
- 497 lines of code
- Uses old ReflexLogger API
- Only 1 actual method call: `start_session()`
- Extended bootstrap creates it but NEVER USES IT
- Complex patterns (singleton, context manager, decorator) for no benefit

**start_session() probably just:**
- Creates session in SessionDatabase
- Can be done in 1 line directly!

## Recommendation: REMOVE auto_tracker

**Impact:** Remove 497 lines of unused complexity

**Replace with:**
```python
# In bootstrap, instead of:
self.tracker = EmpericaTracker.get_instance(...)
self.tracker.start_session(...)

# Just do:
from empirica.data.session_database import SessionDatabase
db = SessionDatabase()
session_id = db.create_session(ai_id=self.ai_id, bootstrap_level=self.level)
```

