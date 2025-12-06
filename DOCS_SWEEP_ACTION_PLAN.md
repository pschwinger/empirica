# Documentation Sweep - Action Plan

**Date:** 2025-12-06  
**Session:** 06e70c60-206b-4491-a6f6-e8ed74bd231b  
**Status:** ✅ Sweep Complete - Ready for Systematic Fixes  
**Files Scanned:** 139 documentation files

---

## Executive Summary

Comprehensive sweep of all Empirica documentation identified ~30-40 files needing updates. Issues are manageable and well-categorized. Most critical user-facing docs already updated in previous session.

**Key Achievement:** Goals/subtasks system successfully used to track investigation systematically with 8 subtasks logging findings and unknowns.

---

## Issues Found (Priority Order)

### 🔴 Priority 1: Production Documentation (10 files)

**Issue:** Files still reference "Empirica v2.0" instead of "v4.0"

**Files:**
1. `docs/production/07_INVESTIGATION_SYSTEM.md`
2. `docs/production/11_DASHBOARD_MONITORING.md`
3. `docs/production/14_CUSTOM_PLUGINS.md`
4. `docs/production/15_CONFIGURATION.md`
5. `docs/production/16_TUNING_THRESHOLDS.md`
6. `docs/production/18_MONITORING_LOGGING.md`
7. `docs/production/25_SCOPEVECTOR_GUIDE.md`
8. `docs/production/27_SCHEMA_MIGRATION_GUIDE.md`
9. `docs/production/DOCS_UPDATE_PLAN.md` (may be intentional planning doc)

**Already Fixed:** 03_BASIC_USAGE.md, 12_SESSION_DATABASE.md, 13_PYTHON_API.md, 17_PRODUCTION_DEPLOYMENT.md, 19_API_REFERENCE.md, 21_TROUBLESHOOTING.md, 24_MCO_ARCHITECTURE.md

**Fix:** Simple find/replace: "Empirica v2.0" → "Empirica v4.0"

**Estimated Time:** 15 minutes

---

### 🟡 Priority 2: Root Documentation (5 files)

**Issue:** Outdated references in user-facing docs

**Files:**
1. `docs/01_a_AI_AGENT_START.md` (needs verification)
2. `docs/03_CLI_QUICKSTART.md` (confirmed has bootstrap references)
3. `docs/04_MCP_QUICKSTART.md` (needs verification)
4. `docs/06_TROUBLESHOOTING.md` (needs verification)
5. `docs/ONBOARDING_GUIDE.md` (needs verification)

**Already Fixed:** README.md, docs/README.md, COMPLETE_INSTALLATION_GUIDE.md, architecture.md, getting-started.md

**Fix:** Update version references, command examples, terminology

**Estimated Time:** 20 minutes

---

### 🟡 Priority 3: Website Content (15 files)

**Issue:** Generated/validated website content has old references

**Files with issues:**
- `website/content/api-reference.md`
- `website/content/architecture_VALIDATED.md`
- `website/content/cli-interface.md`
- `website/content/collaboration_VALIDATED.md`
- `website/content/epistemics_VALIDATED.md`
- `website/content/getting-started.md`
- `website/content/index_VALIDATED.md`
- `website/content/mcp-integration.md`
- `website/content/skills.md`
- `website/content/system-prompts.md`
- `website/simplified_content/features.md`
- `website/simplified_content/getting-started.md`
- `website/simplified_content/index.md`
- `website/simplified_content/mcp-integration.md`
- `website/simplified_content/developers/cli-interface.md`

**Question:** Are these files generated or hand-written?
- If generated: Update source templates and regenerate
- If hand-written: Manual updates needed

**Estimated Time:** 30 minutes (if manual) OR 10 minutes (if regenerated)

---

### 🟢 Priority 4: Minor Fixes (3 files)

**Easy isolated fixes:**

1. **`docs/guides/PROFILE_MANAGEMENT.md`**
   - Line 3: "Empirica v2.0" → "Empirica v4.0"
   - Line 416: Add note about bootstrap_level being legacy
   - Time: 2 minutes

2. **`examples/reasoning_reconstruction/01_basic_reconstruction.sh`**
   - Replace `empirica bootstrap` → `empirica session-create`
   - Time: 1 minute

3. **`docs/architecture/STORAGE_ARCHITECTURE_COMPLETE.md`**
   - Verify no old table references remain
   - Time: 5 minutes

**Estimated Time:** 8 minutes total

---

## Already Completed ✅

### Session f5ca01e1 (Previous)
- ✅ README.md (root)
- ✅ docs/README.md
- ✅ docs/production/00_DOCUMENTATION_MAP.md (created new)
- ✅ docs/production/03_BASIC_USAGE.md
- ✅ docs/production/12_SESSION_DATABASE.md
- ✅ docs/production/13_PYTHON_API.md
- ✅ docs/production/17_PRODUCTION_DEPLOYMENT.md
- ✅ docs/production/19_API_REFERENCE.md
- ✅ docs/production/21_TROUBLESHOOTING.md
- ✅ docs/production/24_MCO_ARCHITECTURE.md
- ✅ 5 cross-reference files
- ✅ 6 historical docs archived to empirica-dev

### Session 06e70c60 (Current)
- ✅ Schema fix: goals/subtasks tables matched to actual DB
- ✅ Updated 12_SESSION_DATABASE.md with correct goals/subtasks schema
- ✅ Comprehensive sweep: 139 files scanned, 8 subtasks completed
- ✅ All findings and unknowns logged systematically

---

## Unknowns to Resolve (23 total)

### Category: Scope Decisions

1. **Planning Docs:** Should DOCS_UPDATE_PLAN.md, MIGRATION_SPEC_DATABASE_SCHEMA_UNIFORMITY.md be updated or archived?
   - Recommendation: Archive to empirica-dev if they're historical planning docs

2. **Website Generation:** Are website files generated or hand-written?
   - Action: Check for website generation scripts
   - If generated: Update source and regenerate
   - If manual: Bulk find/replace

3. **Schema Migration Guide:** Should 27_SCHEMA_MIGRATION_GUIDE.md keep v2.0 reference?
   - Recommendation: Yes, if it documents "migrating FROM v2.0 TO v4.0"

### Category: Verification Needed

4. **Examples:** Do example scripts actually work with v4.0?
   - Action: Run examples to verify functionality

5. **Links:** Full extent of broken links unknown
   - Action: Automated link checker or manual spot checks

6. **Architecture Docs:** Verify consistency with ground truth SVGs
   - Action: Compare architecture docs against storage_architecture_flow.svg

### Category: Prioritization

7. **Fix Order:** Which files are most important for users?
   - Recommendation: Priority 1 → Priority 2 → Priority 4 → Priority 3
   - Rationale: Production docs > User-facing > Easy wins > Website

---

## Recommended Approach

### Option A: Batch Fix (Recommended)

**Phase 1: Critical Production Docs (30 minutes)**
- Fix all Priority 1 files (10 production docs)
- Fix all Priority 2 files (5 root docs)
- Fix Priority 4 easy wins (3 files)
- Total: 18 files

**Phase 2: Website Content (30 minutes)**
- Determine if website is generated
- If generated: Update templates and regenerate
- If manual: Bulk updates to 15 files

**Phase 3: Verification (30 minutes)**
- Test example scripts
- Spot-check links
- Verify architecture doc consistency

**Total Time:** ~90 minutes for complete update

### Option B: User-Facing First

**Phase 1: User Impact (20 minutes)**
- Priority 2 files (docs/ root - 5 files)
- Priority 4 easy wins (3 files)

**Phase 2: Reference Docs (30 minutes)**
- Priority 1 files (production/ - 10 files)

**Phase 3: Website Later**
- Defer website updates or regenerate in bulk

---

## Files Not Needing Updates ✅

### docs/guides/ (Mostly Clean)
- ✅ GOAL_TREE_USAGE_GUIDE.md
- ✅ MCP_CONFIGURATION_EXAMPLES.md
- ✅ SESSION_ALIASES.md
- ✅ TRY_EMPIRICA_NOW.md
- ⚠️ PROFILE_MANAGEMENT.md (minor fix needed)

### docs/architecture/ (Clean)
- ✅ EMPIRICA_SYSTEM_OVERVIEW.md (needs verification)
- ✅ EPISTEMIC_TRAJECTORY_VISUALIZATION.md
- ✅ FUTURE_VISIONS.md
- ✅ README.md
- ✅ STORAGE_ARCHITECTURE_VISUAL_GUIDE.md
- ⚠️ STORAGE_ARCHITECTURE_COMPLETE.md (verify no old table refs)

### examples/ (Mostly Clean)
- ✅ custom_investigation_strategy_example.py
- ✅ phase3_harness_demo.py
- ✅ phase3_persona_demo.py
- ✅ reasoning_reconstruction/02_knowledge_transfer.py
- ⚠️ reasoning_reconstruction/01_basic_reconstruction.sh (minor fix)

---

## Detailed Fix Instructions

### Priority 1: Production Docs v2.0 → v4.0

```bash
# Files to update (9-10 files)
files=(
  "docs/production/07_INVESTIGATION_SYSTEM.md"
  "docs/production/11_DASHBOARD_MONITORING.md"
  "docs/production/14_CUSTOM_PLUGINS.md"
  "docs/production/15_CONFIGURATION.md"
  "docs/production/16_TUNING_THRESHOLDS.md"
  "docs/production/18_MONITORING_LOGGING.md"
  "docs/production/25_SCOPEVECTOR_GUIDE.md"
  "docs/production/27_SCHEMA_MIGRATION_GUIDE.md"
)

# For each file:
# Find: "Empirica v2.0"
# Replace: "Empirica v4.0"

# Also check for:
# - "**Empirica v2.0 -"
# - "Empirica Version 2.0"
# - "v2.0"
```

### Priority 2: Root Docs

**Check each file for:**
1. Version references (v2.0 → v4.0)
2. Command examples (`empirica bootstrap` → `empirica session-create`)
3. Old table references
4. Links to 00_COMPLETE_SUMMARY (→ 00_DOCUMENTATION_MAP)

### Priority 3: Website

**Determine generation method:**
```bash
# Check for generation scripts
ls website/builder/*.py
cat website/builder/generate_site_v2.py

# If generated:
# 1. Update source templates
# 2. Run generation script
# 3. Verify output

# If manual:
# 1. Use find/replace for bulk updates
# 2. Spot-check critical pages
```

### Priority 4: Quick Wins

**File 1: PROFILE_MANAGEMENT.md**
```
Line 3: Empirica v2.0 → Empirica v4.0
Line 416: Add note "# Note: bootstrap_level is legacy (no effect in v4.0)"
```

**File 2: 01_basic_reconstruction.sh**
```bash
# Find: empirica bootstrap
# Replace: empirica session-create
```

**File 3: STORAGE_ARCHITECTURE_COMPLETE.md**
```
# Verify: No references to epistemic_assessments, preflight_assessments, goal_id, subtask_id
# Should reference: reflexes table, id columns, JSON fields
```

---

## Testing Plan

### After Updates

1. **Spot Check Links:**
   - README.md → docs/production/00_DOCUMENTATION_MAP.md
   - DOCUMENTATION_MAP.md → All referenced docs
   - Production docs → Architecture docs

2. **Verify Examples:**
   ```bash
   cd examples/
   python custom_investigation_strategy_example.py
   bash reasoning_reconstruction/01_basic_reconstruction.sh
   ```

3. **Check Consistency:**
   - All production docs reference v4.0
   - No references to old table names (except migration guide context)
   - bootstrap_level examples have deprecation notes

---

## Metrics

### Sweep Statistics
- **Files Scanned:** 139
- **Files Needing Updates:** ~35-40
- **Files Already Updated:** 15+ (previous session)
- **Files Remaining:** ~25-30
- **Subtasks Completed:** 8/8
- **Findings Logged:** 34
- **Unknowns Logged:** 23

### Estimated Fix Time
- **Priority 1:** 15 minutes
- **Priority 2:** 20 minutes
- **Priority 3:** 30 minutes (manual) or 10 minutes (regenerate)
- **Priority 4:** 8 minutes
- **Testing:** 30 minutes
- **Total:** 73-103 minutes (1.2-1.7 hours)

---

## Next Steps

**Immediate:**
1. ✅ Document sweep complete (this file)
2. ⏭️ Decide: Fix now or defer to separate session?
3. ⏭️ If fix now: Start with Priority 1 (production docs)
4. ⏭️ If defer: Run POSTFLIGHT and create handoff report

**For Fixes:**
1. Start with Priority 1 (production v2.0 → v4.0)
2. Continue with Priority 2 (root docs)
3. Handle Priority 4 quick wins
4. Resolve website generation question
5. Update Priority 3 (website) accordingly
6. Run testing verification
7. Document completion

---

## Summary for Handoff

**What Was Found:**
- 35-40 files need updates (out of 139 scanned)
- Main issues: v2.0 references, bootstrap_level examples, website content
- Issues are well-categorized and prioritized
- Most critical docs already updated in previous session

**What's Ready:**
- Complete file list of issues
- Prioritized action plan
- Detailed fix instructions
- Testing checklist
- Goals/subtasks system tracking all findings

**Decision Needed:**
- Fix all now (1-2 hours) OR defer to separate session?
- Website: regenerate from templates OR manual updates?
- Planning docs: archive to empirica-dev OR update?

---

**Session:** 06e70c60-206b-4491-a6f6-e8ed74bd231b  
**Date:** 2025-12-06  
**Status:** ✅ Sweep Complete, Ready for Systematic Fixes
