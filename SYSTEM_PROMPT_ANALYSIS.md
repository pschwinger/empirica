# System Prompt Analysis - Flexible Handoff Updates

**Date:** 2025-12-08  
**Context:** Check if system prompts need updates for flexible handoffs and epistemic continuity  
**Status:** Analysis complete

---

## Summary

Analyzed 4 system prompts:
1. CANONICAL_SYSTEM_PROMPT.md (full version)
2. MINIMALIST_SYSTEM_PROMPT.md (condensed)
3. GEMINI.md (Google Gemini specific)
4. Rovo Dev config.yml (your system prompt)

---

## Analysis Results

### 1. CANONICAL_SYSTEM_PROMPT.md ✅ Already Good

**Handoff mentions:** 16 instances

**Already includes:**
- Goals/subtasks with findings/unknowns tracking
- CHECK phase with query_unknowns_summary()
- Handoff creation workflow
- Investigation findings storage

**Example (lines 279-291):**
```python
# Log investigation findings as you discover them
db.update_subtask_findings(
    subtask_id,
    findings=["Found X", "Validated Y"]
)

# Log unknowns that remain (for CHECK phase decisions)
db.update_subtask_unknowns(
    subtask_id,
    unknowns=["Still unclear: Z"]
)
```

**Missing:** Explicit mention of 3 handoff types (investigation/complete/planning)

**Recommendation:** Add brief section on flexible handoff types.

---

### 2. MINIMALIST_SYSTEM_PROMPT.md ⚠️ Needs Update

**Handoff mentions:** 0 (only mentions `create_handoff_report` in tools list)

**Missing:**
- No explanation of handoff concept
- No mention of 3 handoff types
- No mention of findings/unknowns for CHECK handoffs
- No handoff workflow examples

**Impact:** Users won't know handoffs exist or how to use them

**Recommendation:** Add minimal handoff section (2-3 lines) since this is minimalist prompt.

---

### 3. GEMINI.md ⚠️ Needs Update

**Handoff mentions:** 0 (only mentions `create_handoff_report` in tools list)

**Status:** Identical to MINIMALIST_SYSTEM_PROMPT.md

**Recommendation:** Same as MINIMALIST - add minimal handoff section.

---

### 4. Rovo Dev config.yml ⚠️ Needs Update

**Handoff mentions:** 0

**Current content:**
- ✅ Has goals/subtasks with findings/unknowns
- ✅ Has query_unknowns_summary()
- ❌ No handoff explanation
- ❌ No mention of 3 handoff types

**Recommendation:** Add 2-3 lines about flexible handoffs after goals/subtasks section.

---

## Recommended Updates

### Priority 1: CANONICAL_SYSTEM_PROMPT.md (Minor)

Add section after goals/subtasks:

```markdown
### Flexible Handoffs (v4.0 - Session Continuity)

**3 Types:**
1. **Investigation** (PREFLIGHT→CHECK): Decision gate, pass findings/unknowns to execution specialist
2. **Complete** (PREFLIGHT→POSTFLIGHT): Full learning cycle, measure calibration
3. **Planning** (No CASCADE): Documentation-only, no epistemic deltas

**When to use:**
- Investigation: High uncertainty investigation → execution handoff
- Complete: Full task completion with learning measurement
- Planning: Multi-session planning without CASCADE workflow

**Create:**
```bash
empirica handoff-create --session-id <ID> \
  --task-summary "..." \
  --key-findings '[...]' \
  --remaining-unknowns '[...]' \
  --next-session-context "..."
```

**Query:**
```bash
empirica handoff-query --session-id <ID> --output json
```

**Details:** `docs/guides/FLEXIBLE_HANDOFF_GUIDE.md`
```

---

### Priority 2: MINIMALIST_SYSTEM_PROMPT.md (Minimal Addition)

Add after goals/subtasks section:

```markdown
## HANDOFFS (Session Continuity)

**3 types:** Investigation (PREFLIGHT→CHECK), Complete (PREFLIGHT→POSTFLIGHT), Planning (no CASCADE)

**Investigation handoff:**
```bash
# After CHECK: Pass findings/unknowns to execution specialist
empirica handoff-create --session-id <ID> --key-findings '[...]' --remaining-unknowns '[...]'
empirica handoff-query --session-id <ID>  # Resume work
```

**Details:** `docs/guides/FLEXIBLE_HANDOFF_GUIDE.md`
```

**Token cost:** ~50 tokens (within 500 token budget)

---

### Priority 3: GEMINI.md (Same as MINIMALIST)

Same update as MINIMALIST_SYSTEM_PROMPT.md (they're identical files).

---

### Priority 4: Rovo Dev config.yml (Minimal Addition)

Add after goals/subtasks section (line 75):

```yaml
  additionalSystemPrompt: |
    # ... existing content ...
    
    ## HANDOFFS (Session Continuity)
    **3 types:** Investigation (PREFLIGHT→CHECK), Complete (PREFLIGHT→POSTFLIGHT), Planning (no CASCADE)
    
    Investigation handoff: After CHECK, pass findings/unknowns to execution specialist
    ```bash
    empirica handoff-create --session-id <ID> --key-findings '[...]' --remaining-unknowns '[...]'
    empirica handoff-query --session-id <ID>
    ```
    
    ## ANTI-PATTERNS
    # ... rest of content ...
```

**Token cost:** ~40 tokens

---

## Key Concepts to Include

### Must Have (All Prompts):
1. **3 handoff types exist** (investigation/complete/planning)
2. **Investigation handoffs use findings/unknowns** from goals/subtasks
3. **handoff-create and handoff-query commands**

### Nice to Have (CANONICAL only):
4. Auto-detection logic (PREFLIGHT+CHECK vs PREFLIGHT+POSTFLIGHT)
5. Use cases for each type
6. Link to FLEXIBLE_HANDOFF_GUIDE.md

---

## Why This Matters

**Without handoff explanation in system prompts:**
- AIs won't know handoffs exist
- Multi-AI workflows won't be discoverable
- Investigation → execution pattern won't be used
- Users might not realize session continuity is available

**With handoff explanation:**
- ✅ AIs know to create handoffs after investigation
- ✅ Multi-AI workflows become natural pattern
- ✅ Session continuity promoted
- ✅ Flexible types (investigation/complete/planning) understood

---

## Token Budget Impact

| Prompt | Current Tokens | Added Tokens | New Total | Status |
|--------|----------------|--------------|-----------|--------|
| CANONICAL | ~2,100 | ~100 | ~2,200 | ✅ Acceptable |
| MINIMALIST | ~450 | ~50 | ~500 | ✅ Within budget |
| GEMINI | ~450 | ~50 | ~500 | ✅ Within budget |
| Rovo Dev | ~450 | ~40 | ~490 | ✅ Within budget |

**All updates fit within token budgets.**

---

## Implementation Order

1. **CANONICAL_SYSTEM_PROMPT.md** - Most comprehensive, sets pattern
2. **MINIMALIST_SYSTEM_PROMPT.md** - Reference for condensed version
3. **GEMINI.md** - Copy from MINIMALIST
4. **Rovo Dev config.yml** - Your personal prompt

---

## Validation

After updates, validate that:
- [ ] All prompts mention handoffs
- [ ] 3 types (investigation/complete/planning) explained
- [ ] handoff-create and handoff-query commands shown
- [ ] Findings/unknowns connection to CHECK handoffs mentioned
- [ ] Link to FLEXIBLE_HANDOFF_GUIDE.md included
- [ ] Token budgets not exceeded

---

**Recommendation:** Update all 4 prompts to include flexible handoff awareness.

**Estimated time:** 20 minutes for all updates

**Priority:** Medium-High (users need to know handoffs exist)
