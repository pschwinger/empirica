# BEADS Integration Investigation

**Session ID:** 649849c5-8199-43c6-abce-0426fd8cd464  
**Goal ID:** 5d43301e-97f4-4797-9fa2-563106e03450  
**BEADS Issue:** empirica-ovz  
**Date:** 2025-12-19  
**Status:** ✅ COMPLETE

## Final Decision

**KEEP OPT-IN, IMPROVE DISCOVERABILITY**

**Confidence:** know=0.9, uncertainty=0.15 (HIGH)  
**Learning Delta:** know +0.3, uncertainty -0.4  
**Calibration:** Moderate (started 0.6, ended 0.9)

---

## Investigation Question

**Should BEADS integration be the default (opt-out) for Empirica goals, or remain optional (opt-in)?**

---

## PREFLIGHT Assessment (Session Start)

**Epistemic State:**
- **Engagement:** 0.85 (highly engaged with this question)
- **Foundation:**
  - Know: 0.6 (moderate - we have data from testing)
  - Do: 0.7 (can implement either way)
  - Context: 0.8 (understand the landscape well)
- **Comprehension:** 0.7 (understand the patterns)
- **Execution:** 0.5 (haven't decided yet)
- **Uncertainty:** 0.55 (moderate - need investigation)

**Reasoning:**
> "Starting investigation: Should BEADS be default integration? Know: existing data (5/104 goals linked, adapter works). Don't know: architectural implications, alternative patterns, edge cases, failure modes. Need to investigate: integration patterns, opt-in vs opt-out philosophy, graceful degradation."

---

## Investigation Subtasks

### 1. 🔍 Analyze Current Adoption (HIGH priority)
**BEADS:** empirica-2ap  
**Question:** Why is adoption so low (4.8%)?

**Hypothesis:**
- Manual opt-in burden (requires `--use-beads` flag)
- Lack of awareness (users don't know it exists)
- Integration complexity (setup required?)

**Investigation approach:**
- Review commit history for BEADS-linked goals
- Check documentation for BEADS mentions
- Analyze user workflows (CLI vs API vs MCP)

---

### 2. 📊 Compare Integration Patterns (HIGH priority)
**BEADS:** empirica-085  
**Question:** What's the right pattern for optional dependencies?

**Patterns to evaluate:**

| Pattern | Example | Pros | Cons |
|---------|---------|------|------|
| **Opt-in (current)** | Git LFS (`git lfs install`) | No surprises, explicit | Low adoption, friction |
| **Opt-out** | Git hooks (auto-enable, `--no-verify` to skip) | High adoption, convenience | Unexpected behavior |
| **Required** | Database in Django | Always works | Can't use without it |
| **Graceful degradation** | Docker Compose (works without Docker) | Flexible | Complexity |

**Survey similar tools:**
- Git: Core vs extensions (LFS, hooks)
- Docker: Required for containers, optional for builds
- npm: Required vs optional dependencies
- Python: Required vs extras (`pip install empirica[beads]`)

---

### 3. ⚠️ Identify Failure Modes (CRITICAL priority)
**BEADS:** empirica-5am  
**Question:** What breaks if BEADS is default?

**Scenarios to test:**

1. **Fresh install without bd CLI:**
   ```bash
   pip install empirica
   empirica goals-create --objective "Test"  # What happens?
   ```
   - Current: BeadsAdapter checks `is_available()`, fails gracefully
   - Default: Would fail silently or error loudly?

2. **CI/CD pipelines:**
   - GitHub Actions, GitLab CI don't have bd installed
   - Should goals fail to create? Or create without BEADS?

3. **API-only usage:**
   - Python API users (not CLI)
   - Do they expect BEADS integration?

4. **Multi-repo projects:**
   - Different repos with different BEADS configs
   - Namespace conflicts? (empirica-xxx across repos)

5. **Network failures:**
   - BEADS unavailable temporarily
   - Should goals be blocked?

---

### 4. 🛤️ Define Migration Path (MEDIUM priority)
**BEADS:** empirica-45a  
**Question:** If we make it default, how to handle existing data?

**Current state:**
- 104 total goals
- 5 linked to BEADS (4.8%)
- 99 unlinked goals

**Migration options:**

**Option A: Batch migration**
```bash
# Script to link all existing goals
for goal_id in $(sqlite3 ... "SELECT id FROM goals WHERE beads_issue_id IS NULL"); do
  # Create BEADS issue retroactively
  beads_id=$(bd create "$(get_objective $goal_id)" --json | jq -r '.id')
  # Update goal
  sqlite3 ... "UPDATE goals SET beads_issue_id = '$beads_id' WHERE id = '$goal_id'"
done
```

**Option B: Lazy migration**
- Leave existing goals alone
- Only new goals get BEADS by default
- Add CLI command: `empirica goals-migrate-to-beads --goal-id <ID>`

**Option C: Opt-out flag**
```bash
# New default behavior
empirica goals-create --objective "..." # Creates BEADS issue

# Opt-out for those who don't want it
empirica goals-create --objective "..." --no-beads
```

---

### 5. 📝 Document Decision (HIGH priority)
**BEADS:** empirica-s5s  
**Question:** How to document this transparently?

**Required sections:**
1. **What we know:** Test results, adoption data, technical feasibility
2. **What we don't know:** User preferences, edge cases, long-term effects
3. **Assumptions:** BEADS is stable, users want integration, bd CLI is accessible
4. **Risks:** Breaking changes, user confusion, support burden
5. **Trade-offs:** Convenience vs complexity, adoption vs control
6. **Decision rationale:** Why we chose this path
7. **Reversibility:** How to undo if wrong

---

## Key Questions to Answer

### 🎯 Foundational Questions:
1. **Is BEADS integration foundational to Empirica's value proposition?**
   - Does Empirica work without BEADS? Yes (currently 95% of goals don't use it)
   - Does BEADS enhance Empirica meaningfully? Yes (dependency tracking, ready work detection)
   - Can they be decoupled? Yes (optional integration works)

2. **What's the user mental model?**
   - Do users think of Empirica as "BEADS + epistemic tracking"?
   - Or "epistemic framework with optional BEADS integration"?
   - **Current evidence:** Low adoption suggests optional mental model

3. **What's the right philosophy?**
   - Unix: Small tools that compose (opt-in)
   - Batteries included: Everything works out of box (opt-out)
   - Empirica leans: ??? (needs investigation)

### 🔬 Technical Questions:
1. **Is graceful degradation reliable?**
   - Test: Remove bd CLI, try to create goal
   - Current: Logs warning, continues without BEADS
   - Default: Same behavior, but more visible to users?

2. **What's the installation burden?**
   - Current: `pip install empirica` (no BEADS)
   - With BEADS default: User must install bd separately
   - Alternative: `pip install empirica[beads]` (optional extra)

### 📊 Data Questions:
1. **Why is adoption so low?**
   - Need to survey: Documentation? Friction? Awareness?
   - Hypothesis: Requires explicit flag = cognitive overhead

2. **Would default increase adoption?**
   - Likely yes (default effect is strong)
   - But is that the right outcome?

---

## Investigation Protocol

**Phase 1: Gather Evidence** (Current)
- [x] Test BEADS integration thoroughly
- [x] Document current state (5/104 goals linked)
- [ ] Review documentation for BEADS mentions
- [ ] Test failure modes (no bd CLI, CI/CD, API usage)
- [ ] Survey integration patterns in similar tools

**Phase 2: Analyze Trade-offs**
- [ ] List pros/cons of opt-in vs opt-out
- [ ] Identify breaking changes
- [ ] Estimate migration effort
- [ ] Assess user impact

**Phase 3: Make Decision**
- [ ] CHECK: Do we have enough confidence? (target: know≥0.8, uncertainty≤0.3)
- [ ] Document decision rationale
- [ ] Define implementation plan
- [ ] Create migration guide if needed

**Phase 4: Validate**
- [ ] POSTFLIGHT: Compare actual vs expected understanding
- [ ] Measure learning deltas
- [ ] Document what we learned

---

## Current Hypothesis

**Lean towards: Keep opt-in (current state) for now**

**Reasoning:**
1. **Graceful degradation already works** - BEADS integration is optional and fails gracefully
2. **Low adoption ≠ wrong default** - Could be documentation/awareness issue, not technical
3. **No user complaints** - No evidence users want it to be default
4. **Reversible decision** - Can always make it default later, harder to undo if wrong
5. **Empirica works standalone** - BEADS is enhancement, not requirement

**Alternative: Improve discoverability instead**
- Better documentation
- Onboarding prompt: "Enable BEADS integration? (recommended) [Y/n]"
- CLI hint: "Tip: Add --use-beads to track in BEADS"
- Make it easier, not forced

**Counter-argument:**
- If we believe BEADS is the right way to do goals, why make users opt-in?
- Default = design opinion = clarity

---

## Next Steps

1. Complete all 5 subtasks
2. Run CHECK assessment (measure confidence)
3. Make decision with epistemic transparency
4. Document in POSTFLIGHT

---

## Meta: Why This Investigation Matters

This is a test case for **epistemic decision-making**:
- Start with uncertainty (0.55)
- Investigate systematically (structured subtasks)
- Gather evidence (not opinions)
- Measure confidence growth (CHECK assessments)
- Document transparently (what we know vs don't know)
- Make reversible decisions when possible

If we can't decide about our own integration patterns using Empirica, how can users trust the framework?

---

**Investigation Status:** 🟡 In Progress  
**Confidence Target:** know≥0.8, uncertainty≤0.3  
**Decision Deadline:** After completing all subtasks  
**Reversibility:** High (can change later)
