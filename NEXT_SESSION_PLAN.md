# Next Session Plan - Post Clean Install Success

**Date:** November 19, 2025  
**Session Completed:** 274757a9-1610-40ce-8919-d03193b15f70 (15 cascades!)  
**Status:** Clean install SUCCESSFUL ✅

---

## 🎉 Clean Install Test Results

**Tested on:** Fresh machine instance  
**Result:** ✅ **Worked perfectly, no issues!**

### System Requirements Discovered
- **git** - Required for git clone (obviously, but document it!)
- **pip** - Required for package installation
- **Python 3.10+** - Already documented

**Action:** Add system requirements section to README/docs

---

## 🚀 New Development: Antigravity Integration

### What is Antigravity?
- **Source:** Google's new UI-based AI system
- **Unique:** Runs Claude + Gemini under the hood
- **Value Prop:** Creates artifacts (interactive demos, installers, etc.)

### Demo Created
**On fresh machine, you created:**
1. Complete Empirica installer walkthrough
2. Empirica backend web plugin
   - Connects to existing SQLite database
   - Reads JSON reflex logs
   - Full web interface for Empirica data

**This proves:** Empirica's architecture is plugin-friendly!

---

## 📦 Global Installer Need

### Current State
- antigravity has global installer script (already done)
- Empirica should also be globally installable

### Requirements
- System-wide installation option
- Not just `pip install -e .` (local)
- Potentially: `curl | bash` installer or `pipx install empirica`

**Decision Point:** 
- Use `pipx` for isolated global install?
- Create custom installer script?
- Both?

---

## 📁 Repository Split Decision: empirica vs empirica-dev

### The Problem
- Current repo has TOO MUCH documentation
- Many docs are superfluous for production users
- Dev docs (session notes, validation reports, etc.) clutter production

### Option 1: Separate Repositories ⭐ **Recommended**
```
empirica/              (Public, production-ready)
├── README.md          (User-facing)
├── docs/production/   (User guides only)
├── docs/guides/       (How-to guides)
├── docs/reference/    (API reference)
├── empirica/          (Core code)
├── tests/             (Essential tests)
└── examples/          (User examples)

empirica-dev/          (Private/dev, all the context)
├── README.md          (Dev-facing)
├── docs/current_work/ (Session reports)
├── docs/archive/      (Historical context)
├── docs/vision/       (Future plans)
├── validation/        (Test reports)
└── research/          (Investigations)
```

**Pros:**
- Clean separation of concerns
- Users see only what they need
- Devs have full history
- Easy to manage permissions

**Cons:**
- Need to sync code changes
- Two repos to maintain

### Option 2: Monorepo with .gitignore
```
empirica/
├── docs/              (Production only)
├── docs-dev/          (Dev docs - gitignored for releases)
├── .gitignore         (Exclude docs-dev/ from releases)
```

**Pros:**
- Single repo, easier sync
- Git submodules could work

**Cons:**
- Dev docs still in repo (just hidden)
- Harder to manage clean releases

### Option 3: Branches (Not Recommended)
```
main branch    - Production code + minimal docs
develop branch - All dev docs + work in progress
```

**Pros:**
- Single repo

**Cons:**
- Messy, branches diverge
- Hard to keep in sync

### Recommendation
**Use Option 1: Separate Repositories**

Reasoning:
- Cleaner for users (no clutter)
- Empirica is production tool, should feel production-ready
- Dev context stays accessible but separate
- Can make empirica-dev private if needed
- Matches industry pattern (many projects do this)

---

## 📚 Docs Pruning Strategy

### Keep in Production (empirica repo)
```
docs/
├── production/        ✅ Keep (01-23 user guides)
├── guides/            ✅ Keep (setup, development, learning)
├── reference/         ✅ Keep (architecture, API reference)
├── examples/          ✅ Keep (code examples)
└── README.md          ✅ Keep (already good)
```

### Move to Dev (empirica-dev repo)
```
docs/
├── current_work/      ❌ Move (session reports from THIS session!)
├── archive/           ❌ Move (all historical work)
├── vision/            ❌ Move (future plans)
├── metrics/           ❌ Move (performance analysis)
└── integrations/      ? Maybe keep?
```

### Delete Entirely
```
- Old validation reports (archived, not needed)
- Duplicate documentation
- Obsolete guides (already updated)
```

---

## 🎯 Next Session Tasks

### Priority 1: System Requirements
1. Add git/pip to README system requirements
2. Update installation docs with prerequisites
3. Add troubleshooting for missing git/pip

### Priority 2: Repository Split
1. Decide: Separate repos or monorepo approach?
2. Create empirica-dev repo (if separate)
3. Move dev docs to empirica-dev
4. Prune empirica to production-ready state
5. Update both READMEs

### Priority 3: Global Installer
1. Research best approach (pipx vs custom script)
2. Create global install script
3. Test on multiple systems
4. Document global install option

### Priority 4: Docs Pruning
1. Audit all docs/ folders
2. Identify keep vs move vs delete
3. Execute pruning
4. Verify all doc references still work

### Priority 5: Antigravity Integration
1. Document antigravity demo
2. Consider: Official antigravity integration guide?
3. Showcase: "Build Empirica plugins with Antigravity"

---

## 💡 Strategic Questions for Next Session

1. **Repo split timing:** Do before or after 1.0.0-beta release?
2. **empirica-dev visibility:** Private repo or public?
3. **Global installer:** Essential for 1.0 or can be v1.1?
4. **Docs pruning depth:** How minimal should production docs be?
5. **Antigravity showcase:** Make it a headline feature?

---

## 📊 Current State Summary

**System:** 99.9% release ready  
**Clean Install:** ✅ Verified working  
**Missing:** System requirements doc, global installer, docs pruning  
**Blocker:** Too many dev docs in production repo  
**Solution:** Repository split + docs pruning

---

**Next session: Focus on production readiness and repository cleanup!**
