# Empirica Website Wireframes - Content Structure

## Overview
This directory contains content wireframes for the Empirica website. Each wireframe defines the content structure for a specific page, separate from the visual layout.

## Visual Template
All pages use the same visual template defined in `wireframe_home.html`:
- Header with logo (clickable to home) and CTA buttons
- Navigation menu (5 items)
- Breadcrumbs
- Content area (page-specific)
- Footer

## Menu Structure

### Primary Navigation (5 items)
1. **Epistemic Awareness** (`/epistemic-awareness.html`)
   - Core concepts of epistemic humility
   - The 13 vectors explained
   - Meta-uncertainty in practice

2. **Components** (`/components.html`)
   - System architecture
   - Component catalog
   - Integration points

3. **API** (`/api.html`)
   - API reference
   - Code examples
   - Integration guides

4. **Docs** (`/docs.html`)
   - Complete documentation hub
   - Organized by role and topic
   - Search and navigation

5. **Contact Us** (`/contact.html`)
   - GitHub links
   - Community resources
   - Contributing guide

### Header CTAs (2 buttons)
- **Get Started** → `/getting-started.html` (primary)
- **Empirica MCP** → `/empirica-mcp.html` or `/docs/12_MCP_INTEGRATION.html`

### Logo/Title
- Clickable to `/index.html` (home)
- No explicit "Home" button needed

## Page Wireframes

### Home Page (`wireframe_home.html`)
- Visual template with placeholder content
- Will be populated with hero, features, getting started sections

### Content Pages (Markdown Wireframes)
1. `01_epistemic_awareness.md` - Epistemic Awareness page
2. `02_components.md` - Components page
3. `03_api.md` - API Reference page
4. `04_docs.md` - Documentation Hub page
5. `05_contact.md` - Contact Us page
6. `06_getting_started.md` - Getting Started page

## Subpages (Linked from Main Pages)

### From Getting Started
- Skills Guide (detailed MCP skills usage)
- CLI Guide (command-line interface)
- Bootstrap Guide (Python integration)
- MCP Integration (custom server setup)

### From Docs
- All 20 production docs (01-22)
- Architecture deep dive
- Skills library
- Component documentation

### From Components
- Individual component details
- Integration examples
- Configuration guides

## Content Principles

1. **No Duplication:** Each link appears once per page
2. **Clear Hierarchy:** Main menu → Content pages → Subpages
3. **Minimal Navigation:** 5 menu items, not overwhelming
4. **Progressive Disclosure:** Start simple, provide depth via links
5. **Consistent Layout:** Same header/nav/footer across all pages

## Next Steps

1. ✅ Created wireframe structure
2. ⏭️ Convert markdown wireframes to HTML pages
3. ⏭️ Populate with actual content from docs
4. ⏭️ Add visual elements (diagrams, code samples)
5. ⏭️ Review and refine

## Notes
- Based on `/empirica_web1/index.html` look and feel
- Logo: `/website/assets/empirica_logo.png`
- Documentation source: `/docs/production/`
- Skills source: `/docs/empirica_skills/`
