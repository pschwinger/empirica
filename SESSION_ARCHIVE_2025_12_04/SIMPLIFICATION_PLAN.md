# Cascade & Bootstrap Simplification Plan

## Issues Found (Same Pattern as Before!)

### 1. MetacognitiveCascade - Dual Logger Issue ⚡ CRITICAL
**Problem:** Uses BOTH ReflexLogger AND GitEnhancedReflexLogger
**Impact:** Parallel storage paths (same bug we just fixed!)
**Lines:** 290, 301
**Priority:** HIGH - Fix immediately

### 2. Bootstrap Files - auto_tracker Usage
**Problem:** Both bootstrap files use auto_tracker
**Impact:** If auto_tracker is unused, it's overhead
**Priority:** MEDIUM - Investigate then remove

### 3. Bootstrap Inheritance - Extended vs Optimal
**Problem:** ExtendedMetacognitiveBootstrap inherits from OptimalMetacognitiveBootstrap
**Impact:** Need to verify if inheritance is justified
**Priority:** LOW - Needs analysis

---

## Action Items:

### Task 1: Fix Dual Logger in MetacognitiveCascade ✅ DO NOW
Replace:
```python
self.reflex_logger = ReflexLogger()
if enable_git_notes:
    self.git_logger = GitEnhancedReflexLogger()
```

With:
```python
# Always use git_logger (3-layer storage)
self.git_logger = GitEnhancedReflexLogger(
    session_id=self.session_id,
    enable_git_notes=enable_git_notes  # True or False, works either way
)
# Remove reflex_logger completely
```

### Task 2: Check What Uses self.reflex_logger
Find all uses and replace with self.git_logger

### Task 3: Investigate auto_tracker
What does it actually do? Is it needed?

---

**Your call:** Should I fix the dual logger issue now?

