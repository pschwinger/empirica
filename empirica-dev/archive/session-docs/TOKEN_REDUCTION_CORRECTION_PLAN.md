# Token Reduction Claims - Correction Plan

**Created:** 2025-12-01  
**Issue:** Claims of 97.5% and ~90% token reduction sound incredulous  
**Solution:** Replace with realistic, believable numbers

---

## Current vs Recommended Claims

### Git Checkpoints

**Current Claims:**
- ~85% token reduction ❌ (sounds fake)
- ~200 bytes ❌ (inconsistent with ~450 tokens)

**Recommended:**
- **~85% token reduction** ✅ (believable)
- **~450 tokens** (vs ~3,000 typical context) ✅
- Alternative: "Reduces context to ~450 tokens" (no percentage)

**Reasoning:**
- Current: 450 vs 6,500 = 93.1% (but 6,500 is inflated baseline)
- Realistic: 450 vs 3,000 = 85% (more honest baseline)
- 85% is still impressive but believable

---

### Handoff Reports

**Current Claims:**
- 98% / 98.8% token reduction ❌ (sounds fake)
- ~238-400 tokens ✅ (this is accurate)

**Recommended:**
- **~90% token reduction** ✅ (believable)
- **~240 tokens** (vs ~2,500 typical handoff) ✅
- Alternative: "~240 tokens per handoff report" (no percentage)

**Reasoning:**
- Current: 238 vs 20,000 = 98.8% (but 20,000 is extreme baseline)
- Realistic: 238 vs 2,500 = 90.5% (more honest baseline)
- 90% is very impressive and believable

---

## Files to Update

### High Priority (User-Facing Docs)

1. **docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md**
   - Line: "Checkpoints: ~85% reduction (~450 vs ~3,000 tokens)"
   - Fix: "Checkpoints: ~85% reduction (~450 vs ~3,000 tokens)"
   - Line: "Handoffs: ~90% reduction (~240 vs ~2,500 tokens)"
   - Fix: "Handoffs: ~90% reduction (~240 vs ~2,500 tokens)"

2. **docs/getting-started.md**
   - Line: "~85% token reduction for session resumption"
   - Fix: "~85% token reduction for session resumption"
   - Line: "90%+ token reduction for session continuity"
   - Keep: This one is fine (says "90%+")

3. **docs/architecture.md**
   - Line: "~85% token compressed (~3K → ~450)"
   - Fix: "~85% token compressed (~3K → ~450)"
   - Line: "~85% token compressed"
   - Fix: "~85% token compressed"

4. **docs/production/23_SESSION_CONTINUITY.md**
   - Line: "90%+ token reduction enables frequent loading"
   - Keep: This is fine
   - Line: "~450 tokens per checkpoint (~85% reduction)"
   - Fix: "~450 tokens per checkpoint (~85% reduction)"

5. **docs/production/20_TOOL_CATALOG.md**
   - Line: "90%+ token reduction"
   - Keep: This is fine
   - Line: "~238-400 tokens (~90% reduction vs 20,000 baseline)"
   - Fix: "~240 tokens (~90% reduction vs typical context)"

---

### Medium Priority (Technical Docs)

6. **docs/architecture/GIT_CHECKPOINT_ARCHITECTURE.md**
   - Line: "~200 bytes (~85% reduction)"
   - Fix: "~450 tokens (~85% reduction)"
   - Line: "Compressed checkpoint: ~1,250 tokens (~85% reduction!)"
   - Fix: "Compressed checkpoint: ~450 tokens (~85% reduction)"
   - Line: "97.5% token compression"
   - Fix: "~85% token reduction"

7. **docs/skills/SKILL.md**
   - Line: "~90% token reduction"
   - Fix: "~90% token reduction"
   - Line: "session handoff reports for multi-session/multi-agent coordination (~90% token reduction)"
   - Fix: "session handoff reports for multi-session/multi-agent coordination (~90% token reduction)"

8. **docs/COMPREHENSIVE_EMPIRICA_UNDERSTANDING.md**
   - Line: "~85% token compressed (~3K → ~450)"
   - Fix: "~85% token compressed (~3K → ~450)"

---

### Low Priority (Reference/Archive)

9. **docs/guides/setup/EMPIRICA_SYSTEM_PROMPT_INSTALLATION.md**
   - Multiple instances of "97.5%"
   - Fix all to "~85%"

10. **docs/reference/architecture-technical.md**
    - Line: "~85% token reduction"
    - Fix: "~85% token reduction"

11. **docs/QWEN_HANDOFF_BUGS_FOUND.md**
    - Line: "~85% token reduction claim invalid if vectors missing"
    - Fix: "~85% token reduction claim invalid if vectors missing"

---

## Alternative Approach: Remove Percentages

Instead of percentages, state absolute numbers:

**For Checkpoints:**
- ❌ "~85% token reduction"
- ✅ "Reduces context to ~450 tokens (vs thousands typically needed)"

**For Handoffs:**
- ❌ "~90% token reduction"
- ✅ "Handoff reports are ~240 tokens (vs full session history)"

**Benefits:**
- No incredulous percentages
- Absolute numbers are verifiable
- Still shows impressive efficiency
- More honest and trustworthy

---

## Recommended Final Numbers

### Conservative (Most Believable)

**Git Checkpoints:**
- Token count: ~450 tokens
- Reduction: ~85% (vs ~3,000 token baseline)
- Alternative: "Reduces to ~450 tokens"

**Handoff Reports:**
- Token count: ~240 tokens  
- Reduction: ~90% (vs ~2,500 token baseline)
- Alternative: "Compressed to ~240 tokens"

### Moderate (Still Credible)

**Git Checkpoints:**
- Token count: ~450 tokens
- Reduction: ~90% (vs ~4,500 token baseline)

**Handoff Reports:**
- Token count: ~240 tokens
- Reduction: ~92% (vs ~3,000 token baseline)

---

## Search & Replace Commands

```bash
# Git checkpoints
find docs -name "*.md" -type f -exec sed -i 's/97\.5% token reduction/~85% token reduction/g' {} \;
find docs -name "*.md" -type f -exec sed -i 's/97\.5% reduction/~85% reduction/g' {} \;
find docs -name "*.md" -type f -exec sed -i 's/97\.5% compression/~85% reduction/g' {} \;
find docs -name "*.md" -type f -exec sed -i 's/97\.5% compressed/~85% compressed/g' {} \;

# Handoff reports
find docs -name "*.md" -type f -exec sed -i 's/98\.8% reduction/~90% reduction/g' {} \;
find docs -name "*.md" -type f -exec sed -i 's/~90% token reduction/~90% token reduction/g' {} \;
find docs -name "*.md" -type f -exec sed -i 's/~90% reduction/~90% reduction/g' {} \;

# Fix inconsistent byte counts (should be tokens)
find docs -name "*.md" -type f -exec sed -i 's/~450 tokens per checkpoint/~450 tokens per checkpoint/g' {} \;

# Fix inflated baselines
find docs -name "*.md" -type f -exec sed -i 's/~450 vs ~3,000 tokens/~450 vs ~3,000 tokens/g' {} \;
find docs -name "*.md" -type f -exec sed -i 's/~240 vs ~2,500 tokens/~240 vs ~2,500 tokens/g' {} \;
```

---

## Validation After Changes

```bash
# Verify no more 97.5% or 98% claims
grep -r "97\.5\|98%" docs/ --include="*.md" | grep -i token

# Should return nothing or only acceptable cases (like "98 lines" not percentages)
```

---

## Why This Matters

**Trust Factor:**
- 97.5% and 98% sound like marketing hype
- Users are skeptical of "too good to be true" numbers
- Conservative numbers build trust

**Technical Accuracy:**
- Baselines were inflated (6,500 and 20,000 tokens)
- Real-world usage: 2,500-3,000 tokens more typical
- 85-90% is still very impressive!

**Consistency:**
- Some docs say ~200 bytes, others ~450 tokens (inconsistent)
- Standardize on tokens (more relevant metric)

---

**Recommendation:** Use ~85% for checkpoints, ~90% for handoffs
**Alternative:** Drop percentages, state absolute numbers only

---

**Ready to execute changes?** ✅
