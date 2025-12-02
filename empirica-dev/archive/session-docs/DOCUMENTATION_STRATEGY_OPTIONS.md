# Documentation Strategy Options for Empirica

## Current Problem
- 101+ markdown files across multiple directories
- Duplicate content (3x installation, 3x architecture, 3x quick-ref)
- Constantly changing codebase
- Confusion for both humans and AIs

## Goal
- Single source of truth
- Always up-to-date with code
- Easy to maintain
- Clear navigation

---

## Option 1: Traditional Static Site Generators

### MkDocs + Material Theme (Most Popular for Python)

**Pros:**
- ✅ Markdown-based (keep existing docs)
- ✅ Beautiful Material theme
- ✅ Fast and simple
- ✅ Plugin ecosystem (mkdocstrings pulls from Python docstrings)
- ✅ Free hosting on GitHub Pages
- ✅ Search built-in

**Cons:**
- ⚠️ Manual maintenance (docs still separate from code)
- ⚠️ Can get outdated if not updated with code changes

**Setup:**
```bash
pip install mkdocs mkdocs-material mkdocstrings[python]
mkdocs new .
# Edit mkdocs.yml configuration
mkdocs serve  # Local preview
mkdocs build  # Generate static site
```

**Best for:** Teams who want full control, beautiful docs, but can commit to maintenance.

---

### Sphinx + ReadTheDocs (Traditional Python Standard)

**Pros:**
- ✅ Industry standard for Python
- ✅ Auto-generates API docs from docstrings
- ✅ Extensive plugin ecosystem
- ✅ Free hosting on ReadTheDocs

**Cons:**
- ⚠️ ReStructuredText (more complex than Markdown)
- ⚠️ Steeper learning curve
- ⚠️ Can be overkill for smaller projects

**Best for:** Large projects needing extensive cross-referencing and API documentation.

---

### Docusaurus (Meta/Facebook)

**Pros:**
- ✅ Modern, React-based
- ✅ Markdown support
- ✅ Versioned docs
- ✅ Beautiful UI

**Cons:**
- ⚠️ Requires Node.js (not Python-native)
- ⚠️ More complex setup

**Best for:** Projects with JavaScript frontend needs or requiring versioned docs.

---

## Option 2: AI-Powered Living Documentation

### Google Code Wiki (NEW - Nov 2024) 🔥

**What it does:**
- Scans entire codebase automatically
- Generates structured wiki using Gemini AI
- Updates automatically on every code change
- Creates architecture diagrams, API references, guides
- AI can answer questions about the codebase

**Pros:**
- ✅ **Always up-to-date** (regenerates on every commit)
- ✅ **Zero maintenance** (AI does it all)
- ✅ **Living documentation** (evolves with code)
- ✅ AI can answer "how does X work?" questions
- ✅ Understands context and relationships

**Cons:**
- ⚠️ New (launched Nov 2024, may have bugs)
- ⚠️ Requires Google Cloud/Gemini API access
- ⚠️ Less control over output format
- ⚠️ May need manual curation for narrative docs

**How it works:**
1. Point it at GitHub repository
2. Gemini scans full codebase
3. Generates wiki automatically
4. Re-scans after every change
5. AI answers questions about the code

**Setup:**
```bash
# (Details pending - Code Wiki is very new)
# Likely requires: GitHub app installation + Google Cloud API
```

**Best for:** Teams wanting zero-maintenance docs that stay current automatically.

---

### Mintlify (AI-Powered Docs Platform)

**What it does:**
- AI generates documentation from code
- Beautiful interactive docs
- API reference auto-generation
- Code snippets and examples

**Pros:**
- ✅ AI-assisted writing
- ✅ Beautiful modern UI
- ✅ Auto-generates API docs
- ✅ Fast setup

**Cons:**
- ⚠️ Commercial service (paid plans)
- ⚠️ Less customization than open-source
- ⚠️ Vendor lock-in

**Best for:** Teams wanting beautiful docs quickly with AI assistance but okay with paid service.

---

## Option 3: Hybrid Approach (Recommended for Empirica)

### Strategy: Docstrings + MkDocs + Code Wiki

**Phase 1: Clean up existing docs (now)**
- Consolidate duplicates
- Keep only essential narrative docs in `docs/`
- Move detailed API docs to Python docstrings

**Phase 2: Generate from code (short-term)**
- Use `mkdocstrings` to auto-generate API reference from docstrings
- Keep narrative guides in markdown
- MkDocs combines both into beautiful site

**Phase 3: Add Code Wiki (future)**
- Use Code Wiki as AI-powered architecture explorer
- Keep MkDocs for official documentation
- Code Wiki for internal team understanding

**Benefits:**
- ✅ Reduces manual maintenance (API docs from code)
- ✅ Narrative docs still under your control
- ✅ Beautiful presentation (MkDocs Material)
- ✅ AI-powered exploration available (Code Wiki)
- ✅ Always up-to-date API reference

---

## Comparison Matrix

| Tool | Maintenance | Control | AI-Powered | Cost | Python-Native |
|------|-------------|---------|------------|------|---------------|
| **MkDocs** | Medium | High | No | Free | Yes |
| **Sphinx** | Medium | High | No | Free | Yes |
| **Docusaurus** | Medium | High | No | Free | No |
| **Code Wiki** | **Zero** | Low | **Yes** | Free* | N/A |
| **Mintlify** | Low | Medium | Yes | Paid | N/A |

*Code Wiki: Free tier TBD, requires Google Cloud API access

---

## Recommendation for Empirica

### Immediate (This Week):
1. **Consolidate existing docs** (fix duplicates)
2. **Move API docs to docstrings** in code
3. **Keep ~20 essential narrative docs**

### Short-term (Next Month):
1. **Set up MkDocs + Material theme**
2. **Add mkdocstrings plugin** (auto-generate API docs)
3. **Deploy to GitHub Pages** (free hosting)

**Result:**
- Clean, maintainable documentation
- API reference auto-generated from code
- Beautiful searchable site
- Minimal manual maintenance

### Future (When Stable):
1. **Evaluate Code Wiki** (when more mature)
2. **Use as internal tool** for team understanding
3. **Keep MkDocs as official docs**

**Result:**
- Two-tier documentation:
  - **Official docs** (MkDocs, curated)
  - **Living wiki** (Code Wiki, AI-generated)

---

## Action Plan

### Option A: Quick Win (Conservative)
```bash
# 1. Install MkDocs
pip install mkdocs mkdocs-material mkdocstrings[python]

# 2. Create config
mkdocs new .
# Edit mkdocs.yml to point at docs/

# 3. Preview
mkdocs serve

# 4. Deploy
mkdocs gh-deploy
```

**Time:** 1-2 hours  
**Benefit:** Beautiful docs site immediately

### Option B: AI-Powered (Experimental)
```bash
# 1. Set up Code Wiki (once available)
# Connect GitHub repo to Code Wiki

# 2. Let AI generate initial docs
# Review and curate

# 3. Set up auto-regeneration on commits
```

**Time:** Unknown (Code Wiki is new)  
**Benefit:** Zero maintenance, always current

### Option C: Hybrid (Recommended)
```bash
# 1. Do Option A (MkDocs)
# 2. Add Code Wiki as experimental layer
# 3. Best of both worlds
```

**Time:** 2-4 hours initially  
**Benefit:** Controlled + AI-powered

---

## Decision Needed

**Questions:**
1. **Control vs Automation**: Manual curation (MkDocs) or AI generation (Code Wiki)?
2. **Timeline**: Quick setup or experiment with new tools?
3. **Audience**: External users (polished docs) or internal team (living wiki)?
4. **Resources**: Time to maintain or let AI handle it?

**My Recommendation:** Start with MkDocs + mkdocstrings (proven, fast), then add Code Wiki when it matures.

