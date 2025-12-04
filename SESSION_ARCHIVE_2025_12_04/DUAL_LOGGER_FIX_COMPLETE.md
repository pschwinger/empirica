# Dual Logger Fix - MetacognitiveCascade

## Issue Fixed
MetacognitiveCascade was using BOTH ReflexLogger AND GitEnhancedReflexLogger
(same parallel storage path issue we fixed in workflow_commands)

## Changes Made

### File: empirica/core/metacognitive_cascade/metacognitive_cascade.py

**Removed:**
```python
self.reflex_logger = ReflexLogger()  # Line 290
```

**Changed:**
```python
# Before: Conditional creation of git_logger
if self.enable_git_notes:
    self.git_logger = GitEnhancedReflexLogger(enable_git_notes=True)
else:
    self.git_logger = None

# After: Always create git_logger (works with or without git notes)
self.git_logger = GitEnhancedReflexLogger(
    session_id=self.session_id,
    enable_git_notes=self.enable_git_notes  # True = 3-layer, False = JSON only
)
```

**Removed:**
```python
log_path = await self.reflex_logger.log_frame(frame_dict)  # Line 1460
```
(Redundant - git_logger.add_checkpoint() already called elsewhere)

## Result
- ✅ Single logger (git_logger) used consistently
- ✅ No more parallel storage paths
- ✅ Works with or without git notes enabled
- ✅ Cleaner, simpler code

## Next: Check auto_tracker Usage

