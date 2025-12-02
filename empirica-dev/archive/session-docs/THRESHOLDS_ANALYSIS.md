# Thresholds Files Analysis

## File Relationship: CORRECT DESIGN ✅

### File 1: empirica/config/threshold_loader.py
**Purpose:** Dynamic threshold loader from YAML  
**Loads from:** `config/mco/cascade_styles.yaml`  
**Features:**
- Profile switching (default, exploratory, rigorous, etc.)
- Runtime overrides
- Custom profile creation
- Part of MCO architecture

### File 2: empirica/core/thresholds.py
**Purpose:** Backwards compatibility wrapper  
**Uses:** threshold_loader.py internally  
**Features:**
- Provides legacy constant access (ENGAGEMENT_THRESHOLD, etc.)
- Lazy loads from threshold_loader
- Falls back to hardcoded defaults if YAML unavailable

## Architecture: NOT DUPLICATE ✅

```
Code using legacy constants:
  from empirica.core.thresholds import ENGAGEMENT_THRESHOLD
            ↓
  empirica/core/thresholds.py (wrapper)
            ↓
  empirica/config/threshold_loader.py (loads YAML)
            ↓
  empirica/config/mco/cascade_styles.yaml (actual values)
```

**Result:** Two files serve different purposes
- threshold_loader.py = actual loader (MCO system)
- thresholds.py = backwards compatibility layer

**Decision:** KEEP BOTH ✅

---

## Verification: Check imports


## Usage Check:


## Conclusion:

**Both files needed:**
- threshold_loader.py = Core loader (MCO system, YAML-based)
- thresholds.py = Compatibility wrapper (legacy code support)

**Status:** ✅ CORRECT ARCHITECTURE, NO DUPLICATION

**Action:** Keep both files as-is

