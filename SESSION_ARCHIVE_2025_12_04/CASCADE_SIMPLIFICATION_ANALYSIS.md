# Cascade Simplification Analysis

## Current Structure

### Files Found:
1. **empirica/bootstraps/extended_metacognitive_bootstrap.py** (714 lines)
2. **empirica/bootstraps/optimal_metacognitive_bootstrap.py** (521 lines)
3. **empirica/bootstraps/onboarding_wizard.py** (797 lines)
4. **empirica/core/metacognitive_cascade/metacognitive_cascade.py** (2290 lines!)
5. **empirica/core/metacognition_12d_monitor/metacognition_12d_monitor.py**

### Questions:
1. Do we need TWO bootstrap files (extended vs optimal)?
2. Does metacognitive_cascade.py have inheritance/bloat?
3. Is it using BOTH ReflexLogger AND GitEnhancedReflexLogger?

## Let me investigate...

## Findings:

### 1. Bootstrap Inheritance Chain:
```python
ExtendedMetacognitiveBootstrap(OptimalMetacognitiveBootstrap):  # 714 lines
    ↓ inherits from
OptimalMetacognitiveBootstrap:  # 521 lines (standalone)
```

**Issue:** Another inheritance! ExtendedMetacognitiveBootstrap extends OptimalMetacognitiveBootstrap

### 2. MetacognitiveCascade Issues:
```python
Line 290: self.reflex_logger = ReflexLogger()              # OLD API (JSON only)
Line 301: self.git_logger = GitEnhancedReflexLogger(...)   # NEW API (3-layer)
```

**Issue:** Uses BOTH loggers! Same parallel storage path problem we just fixed!

### 3. auto_tracker imported in optimal_metacognitive_bootstrap.py
```python
from empirica.auto_tracker import EmpericaTracker
```

**Issue:** Uses auto_tracker which we said could be deprecated

## Questions to Answer:

1. **What's the difference between Extended and Optimal bootstrap?**
   - Is Extended actually used?
   - Can we merge them?

2. **Why does MetacognitiveCascade use TWO loggers?**
   - reflex_logger (ReflexLogger - JSON only)
   - git_logger (GitEnhancedReflexLogger - 3-layer)
   - Should just use git_logger everywhere!

3. **Is auto_tracker actually used?**
   - You said it's not used
   - Can we remove it from bootstrap?


## Usage Analysis:

### ExtendedMetacognitiveBootstrap IS Used:
- bootstrap_commands.py (main CLI)
- component_commands.py (3 places)
- __init__.py (exported)

**Current pattern:**
```python
bootstrap = ExtendedMetacognitiveBootstrap(ai_id, level)
```

### auto_tracker IS Used:
- optimal_metacognitive_bootstrap.py creates tracker
- extended_metacognitive_bootstrap.py creates tracker
- But you said it's not actually used for anything

### MetacognitiveCascade Dual Logger Pattern:
```python
Line 290: self.reflex_logger = ReflexLogger()  # ALWAYS created
Line 296: if self.enable_git_notes:
Line 301:     self.git_logger = GitEnhancedReflexLogger()  # CONDITIONALLY created
```

**Problem:** 
- Creates ReflexLogger ALWAYS (even when git_logger exists)
- Same parallel storage issue!
- Should only use git_logger

---

## Recommended Simplifications:

### 1. Remove Dual Loggers from MetacognitiveCascade ⚡ PRIORITY
**Impact:** HIGH - Same issue we just fixed in workflow_commands!

**Fix:**
```python
# Line 290: REMOVE
# self.reflex_logger = ReflexLogger()

# Line 296-304: CHANGE
if self.enable_git_notes:
    self.git_logger = GitEnhancedReflexLogger(...)
else:
    # Just use git_logger with enable_git_notes=False
    self.git_logger = GitEnhancedReflexLogger(
        session_id=self.session_id,
        enable_git_notes=False  # Will only do JSON logging
    )
```

**Benefit:** Single logger, consistent behavior

### 2. Remove auto_tracker if Not Actually Used 🔧
**Impact:** MEDIUM - Simplifies bootstrap

**Questions:**
- What does auto_tracker actually DO?
- Is it just creating overhead?
- Can we remove it from both bootstrap files?

### 3. Merge Bootstrap Files? 🤔
**Impact:** LOW - More investigation needed

**Questions:**
- What does ExtendedMetacognitiveBootstrap add over Optimal?
- Can we merge them into one?
- Or is the inheritance justified here?

---

## Immediate Action: Fix Dual Logger Issue

**File:** empirica/core/metacognitive_cascade/metacognitive_cascade.py
**Line:** 290

Same issue as workflow_commands - using two storage paths!

