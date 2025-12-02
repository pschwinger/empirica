# Empirica Documentation Architecture Plan

**Date:** 2025-01-XX  
**Goal:** Single source of truth, minimal maintenance, clear separation of concerns

---

## Current Assets ✅

**Website (User-Facing):**
- ✅ `website/simplified_content/` - User-facing content
- ✅ `website/simplified_content/developers/` - Developer content
- ✅ `website/builder/generate_site_v2.py` - Working HTML generator
- ✅ Published at: https://nubaeon.github.io/empirica/

**Documentation (Source):**
- ✅ `docs/` - 101 markdown files (needs consolidation)
- ✅ `docs/system-prompts/` - Canonical system prompts
- ✅ Python docstrings in codebase

---

## Proposed Architecture: Two-Tier Documentation

### Tier 1: User-Facing Website (Narrative & Guides)
**Location:** `website/simplified_content/`  
**Audience:** End users, AI agents, new developers  
**Purpose:** High-level concepts, getting started, use cases  
**Technology:** Your existing `generate_site_v2.py` builder  
**Hosting:** GitHub Pages (https://nubaeon.github.io/empirica/)

**Content:**
```
website/simplified_content/
├── index.md                    # Landing page
├── getting-started.md          # Quick start
├── epistemics.md               # Core concepts
├── use-cases.md                # Real-world examples
├── examples.md                 # Code examples
├── docs.md                     # Hub linking to Tier 2 ✨
└── developers/
    ├── architecture.md         # System overview
    ├── collaboration.md        # Multi-AI patterns
    ├── system-prompts.md       # How to use system prompts
    └── api-reference.md        # Links to Tier 2 ✨
```

**Key Change:** `docs.md` and `api-reference.md` **link to MkDocs** for deep technical docs.

---

### Tier 2: Technical Reference (API & Deep Docs)
**Location:** `docs/` (source) → MkDocs (generated)  
**Audience:** Active developers, contributors, system integrators  
**Purpose:** API reference, technical specs, internal architecture  
**Technology:** MkDocs + mkdocstrings (auto-generates from code)  
**Hosting:** GitHub Pages subdirectory or separate domain

**Content:**
```
docs/
├── reference/
│   ├── api/                    # Auto-generated from docstrings
│   │   ├── cascade.md          # CanonicalEpistemicCascade
│   │   ├── database.md         # SessionDatabase
│   │   └── goals.md            # Goal orchestrator
│   ├── cli.md                  # CLI command reference
│   └── mcp-tools.md            # MCP tool catalog
├── architecture/
│   ├── cascade-flow.md         # Deep dive into CASCADE
│   ├── git-integration.md      # Git notes architecture
│   └── storage.md              # SQLite + JSON + Git
└── guides/
    ├── contributing.md         # How to contribute
    ├── testing.md              # Running tests
    └── deployment.md           # Production deployment
```

**Key Feature:** API docs **auto-generated** from Python docstrings using mkdocstrings.

---

## How They Work Together

### User Journey:

**1. New User visits website:**
```
https://nubaeon.github.io/empirica/
└─> getting-started.md → "Quick concepts, how to install"
```

**2. User wants technical details:**
```
https://nubaeon.github.io/empirica/docs.html
└─> "For deep technical reference, see: [API Docs](https://nubaeon.github.io/empirica/mkdocs/)"
```

**3. Developer needs API reference:**
```
https://nubaeon.github.io/empirica/mkdocs/reference/api/cascade/
└─> Auto-generated from docstrings, always up-to-date
```

---

## Benefits of This Architecture

### ✅ Single Source of Truth
- **Website content:** Curated narrative in `website/simplified_content/`
- **API docs:** Generated from Python docstrings (no duplication)
- **Technical specs:** Maintained in `docs/` (one place)

### ✅ Minimal Maintenance
- API reference updates automatically when code changes
- Website only needs updates for narrative/conceptual changes
- No duplicate installation/architecture/quickstart docs

### ✅ Clear Separation
- **Casual users:** Beautiful website with concepts
- **Developers:** Deep technical docs via MkDocs
- **Contributors:** Full reference in MkDocs

### ✅ Existing Infrastructure
- Keep your working `generate_site_v2.py`
- Just add MkDocs for technical docs
- Both deploy to GitHub Pages

---

## Implementation Plan

### Phase 1: Consolidate Source Docs (1-2 days)

**Actions:**
1. **Merge duplicates:**
   - Keep ONE installation guide (best of 3)
   - Keep ONE architecture doc (best of 3)
   - Keep ONE quick reference (best of 3)

2. **Reorganize `docs/`:**
   ```
   docs/
   ├── reference/           # Technical specs
   ├── architecture/        # Deep dives
   ├── guides/              # How-tos
   └── system-prompts/      # Canonical (already good)
   ```

3. **Move API details to docstrings:**
   - Add comprehensive docstrings to key classes
   - Remove redundant API markdown files

**Result:** From 101 files → ~30 essential files

---

### Phase 2: Set Up MkDocs (2-3 hours)

**Install:**
```bash
pip install mkdocs mkdocs-material mkdocstrings[python]
```

**Create `mkdocs.yml`:**
```yaml
site_name: Empirica Technical Reference
site_url: https://nubaeon.github.io/empirica/mkdocs/
theme:
  name: material
  palette:
    scheme: slate  # Dark theme
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest
    - search.highlight

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [empirica]
          options:
            show_source: true
            show_root_heading: true

nav:
  - Home: index.md
  - Reference:
      - API:
          - CASCADE: reference/api/cascade.md
          - Database: reference/api/database.md
          - Goals: reference/api/goals.md
      - CLI: reference/cli.md
      - MCP Tools: reference/mcp-tools.md
  - Architecture:
      - CASCADE Flow: architecture/cascade-flow.md
      - Git Integration: architecture/git-integration.md
  - Guides:
      - Contributing: guides/contributing.md
      - Testing: guides/testing.md
```

**Test locally:**
```bash
mkdocs serve
# Visit http://localhost:8000
```

**Deploy:**
```bash
mkdocs build --site-dir ../empirica-website/mkdocs/
# Or: mkdocs gh-deploy --dir mkdocs
```

**Result:** Beautiful technical docs at `/mkdocs/` subdirectory

---

### Phase 3: Link Website to MkDocs (1 hour)

**Update `website/simplified_content/docs.md`:**
```markdown
# Documentation Hub

## 📖 Core Concepts
- [Epistemic Awareness](epistemics.md)
- [Getting Started](getting-started.md)

## 💻 Developer Resources

### Quick Reference
- [Installation](getting-started.md#installation)
- [First CASCADE](getting-started.md#your-first-cascade)
- [System Prompts](developers/system-prompts.md)

### Technical Documentation
**For detailed API reference and technical specs:**
👉 **[Visit Technical Docs](../mkdocs/)**

Includes:
- Complete API reference (auto-generated)
- Architecture deep dives
- CLI command reference
- Contributor guides

---

**Need help?** Start with [Getting Started](getting-started.md) or [FAQs](faqs.md).
```

**Update `website/simplified_content/developers/api-reference.md`:**
```markdown
# API Reference

**Quick Overview:**

The Empirica Python API provides classes for CASCADE workflow orchestration.

## Core Classes

- **CanonicalEpistemicCascade** - Main workflow class
- **SessionDatabase** - SQLite persistence
- **ReflexLogger** - Temporal logging

## MCP Tools (Recommended for AI Agents)

For AI assistants, use the 23 MCP tools:
- Session: `bootstrap_session`, `resume_previous_session`
- Workflow: `execute_preflight`, `submit_check_assessment`
- Goals: `create_goal`, `add_subtask`

---

## 📚 Complete API Reference

**For detailed class documentation, methods, and examples:**

👉 **[View Complete API Documentation](../../mkdocs/reference/api/)**

Auto-generated from source code, always up-to-date.

---

**Quick Links:**
- [CASCADE Architecture](../../mkdocs/architecture/cascade-flow/)
- [CLI Reference](../../mkdocs/reference/cli/)
- [Contributing Guide](../../mkdocs/guides/contributing/)
```

**Result:** Website seamlessly links to technical docs

---

### Phase 4: Deploy Both (30 minutes)

**Option A: Single GitHub Pages (Recommended)**
```bash
# Build MkDocs into website output
cd website/builder
python generate_site_v2.py --output-dir ../../docs_site

cd ../..
mkdocs build --site-dir docs_site/mkdocs/

# Push docs_site/ to gh-pages branch
# Result:
# - https://nubaeon.github.io/empirica/ (main site)
# - https://nubaeon.github.io/empirica/mkdocs/ (technical docs)
```

**Option B: Separate Deployment**
```bash
# Main site to gh-pages
# MkDocs to gh-pages/mkdocs/ or separate domain
```

**Result:** Unified documentation at one domain

---

## File Structure After Implementation

```
empirica/
├── docs/                       # Source for MkDocs (30 files, down from 101)
│   ├── index.md                # MkDocs landing page
│   ├── reference/              # Technical reference
│   │   ├── api/                # Auto-generated from docstrings
│   │   ├── cli.md
│   │   └── mcp-tools.md
│   ├── architecture/           # Deep dives
│   │   ├── cascade-flow.md
│   │   ├── git-integration.md
│   │   └── storage.md
│   ├── guides/                 # How-tos
│   │   ├── contributing.md
│   │   └── testing.md
│   └── system-prompts/         # Canonical (unchanged)
│
├── website/                    # User-facing site
│   ├── simplified_content/     # Source content
│   │   ├── index.md
│   │   ├── getting-started.md
│   │   ├── docs.md             # Links to MkDocs ✨
│   │   └── developers/
│   │       └── api-reference.md # Links to MkDocs ✨
│   └── builder/
│       └── generate_site_v2.py # Your existing builder
│
├── mkdocs.yml                  # MkDocs configuration
│
└── empirica/                   # Python source
    └── **/*.py                 # With comprehensive docstrings
```

---

## Maintenance Workflow

### When Code Changes:
```bash
# 1. Update Python docstrings (in code)
# 2. Rebuild MkDocs (automatic via GitHub Action)
# Result: API docs update automatically
```

### When Narrative Changes:
```bash
# 1. Update website/simplified_content/
# 2. Run generate_site_v2.py
# 3. Deploy
# Result: User-facing site updates
```

### When Architecture Changes:
```bash
# 1. Update docs/architecture/*.md
# 2. Rebuild MkDocs
# Result: Technical docs update
```

**No more duplicate docs to maintain!**

---

## Comparison: Before vs After

### Before:
- ❌ 101+ markdown files (duplicates, outdated)
- ❌ Manual API documentation (gets stale)
- ❌ Unclear which doc is canonical
- ❌ Website separate from technical docs
- ❌ High maintenance burden

### After:
- ✅ ~30 curated source files
- ✅ Auto-generated API reference
- ✅ Clear separation (user vs developer)
- ✅ Unified at one domain
- ✅ Low maintenance (API updates automatically)

---

## Timeline

**Week 1:**
- Day 1-2: Consolidate docs (fix duplicates)
- Day 3: Set up MkDocs
- Day 4: Link website to MkDocs
- Day 5: Deploy and test

**Week 2:**
- Polish content
- Add comprehensive docstrings
- Set up GitHub Action for auto-deployment

**Total:** ~1 week to complete implementation

---

## Future: Add Code Wiki (Optional)

**After MkDocs is stable (3-6 months):**

1. **Point Code Wiki at repo**
2. **Use as exploration tool** (AI-generated understanding)
3. **Keep website + MkDocs as official docs** (curated)

**Three-tier architecture:**
- **Website** (simplified_content) - For users
- **MkDocs** (docs/) - For developers
- **Code Wiki** (AI-generated) - For exploration

---

## Recommendation

**Start with Tier 1 + Tier 2 (Website + MkDocs):**

1. ✅ Use existing website builder
2. ✅ Add MkDocs for technical docs
3. ✅ Link them together
4. ✅ Deploy to single GitHub Pages domain

**Result:** Clean, maintainable, two-tier documentation system.

**Time to implement:** ~1 week  
**Maintenance reduction:** ~80% (API docs auto-generate)  
**User experience:** Clear path from concepts to deep technical reference

---

**Ready to start? Which phase should we tackle first?**

1. Phase 1: Consolidate duplicates (immediate value)
2. Phase 2: Set up MkDocs (technical foundation)
3. Phase 3: Link them together (integration)
4. All at once (faster but riskier)
