# Website Navigation Structure Plan

**Goal:** Organize 9 content pages into logical, user-friendly navigation with max 5-6 main items + 2 CTAs

---

## Current Content Inventory

### ✅ New Validated Pages (Created Today)
1. **`index_VALIDATED.md`** - Homepage (complete overview)
2. **`epistemics_VALIDATED.md`** - 13 vectors, calibration, epistemic types
3. **`collaboration_VALIDATED.md`** - Sessions, goals, handoffs, storage, cross-AI
4. **`ai_vs_agent_VALIDATED.md`** - High reasoning vs action-based, CASCADE patterns
5. **`architecture_VALIDATED.md`** - System design, directory structure, integration

### ✅ Existing Pages (Need Validation)
6. **`getting-started.md`** - Installation, first CASCADE, CLI/API usage
7. **`features.md`** - Core capabilities, advanced features, integrations
8. **`api-reference.md`** - Complete Python API documentation
9. **`use-cases.md`** - Real-world applications, examples

---

## Content Analysis

### Page Headers Summary

**`epistemics_VALIDATED.md`:**
- What is Epistemic Self-Assessment
- The 13 Epistemic Vectors (detailed)
- How Vectors Combine
- Critical Thresholds
- Calibrated Confidence
- Why This Matters for AI Systems
- Genuine vs Heuristic Assessment
- Reading Vector Patterns

**`collaboration_VALIDATED.md`:**
- The Challenge: AI Collaboration at Scale
- Storage Architecture (5 systems)
- Sessions: The Unit of Work
- Goals & Subtasks
- Cross-AI Collaboration Patterns
- Learning Deltas
- Epistemic Snapshots
- Platform-Agnostic Design
- MCP Tools for Collaboration

**`ai_vs_agent_VALIDATED.md`:**
- The Fundamental Distinction (AI vs Agent)
- Why the Distinction Matters
- CASCADE Usage Patterns (3 patterns)
- Agent CASCADE Guidelines
- Comparison Table
- Best Practices
- Reasoning Capability Selection
- System Prompts

**`architecture_VALIDATED.md`:**
- System Architecture Overview
- Core Design Principles
- Canonical Directory Structure
- System Prompts
- Integration Points
- Data Flow
- Performance Characteristics

**`getting-started.md`:**
- Quick Installation
- Your First CASCADE
- Using the Python API
- Setting Up the Dashboard
- Common Workflows
- Understanding Your Results
- Troubleshooting

**`features.md`:**
- Core Epistemic Features (13-vector, CASCADE)
- Advanced AI Intelligence (Bayesian Guardian, Drift Monitor)
- Investigation Strategy System
- Integration & Extensibility (MCP, Plugins, Multi-AI)
- Visualization & Monitoring
- Production & Enterprise Features

**`api-reference.md`:**
- Quick Reference
- Core Classes
- CASCADE Phases (5 phases)
- Configuration System
- Advanced Features (Bayesian, Drift)
- MCP Integration
- Plugin System
- Data Models
- Error Handling

**`use-cases.md`:**
- Software Development (Code Review, Performance)
- Research & Analysis (Literature Review, Data Science)
- Decision Support Systems
- Security Analysis
- Multi-AI Collaboration
- Quality Assurance

---

## Proposed Navigation Structure (REVISED)

### **Main Navbar (5 items + 2 CTAs)**

```
┌─────────────────────────────────────────────────────────────────┐
│  Logo    [Learn] [CLI] [Platform] [Developers] [Community]      │
│                                          [Get Started] [Docs] →  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Changes:**
- ✅ **CLI elevated to main navbar** (heart of everything)
- ✅ **MCP + Skills + System Prompts grouped** under CLI (context injection)
- ✅ **Docs moved to CTA** (reference material)
- ✅ **5 main items maintained**

---

### **1. Learn** (Dropdown - Conceptual Understanding)

**Purpose:** Understand what Empirica is and why it matters

```
Learn ▼
├── What is Empirica (index.md)
├── Epistemics & Calibration (epistemics.md)
├── Why It Matters (use-cases.md)
└── Features Overview (features.md)
```

**Rationale:**
- **What is Empirica** - Homepage, overview, quick intro
- **Epistemics & Calibration** - Deep dive into the core differentiator
- **Why It Matters** - Real-world use cases, benefits
- **Features Overview** - Comprehensive capabilities

**No changes from original plan**

---

### **2. CLI** (Dropdown - The Heart of Empirica) ⭐ NEW

**Purpose:** Command-line interface and context injection mechanisms

```
CLI ▼
├── CLI Interface (NEW - cli-interface.md)
├── MCP Server (mcp-integration.md)
├── Skills (NEW - skills.md)
└── System Prompts (NEW - system-prompts.md)
```

**Rationale:**
- **CLI Interface** - Core commands, workflows, scripting (heart of everything)
- **MCP Server** - 23 tools, IDE integration, setup
- **Skills** - Metacognitive capabilities, semantic documentation
- **System Prompts** - AI behavior configuration, role-based prompts

**Why grouped together:**
All four are about **injecting context** into AI systems:
- CLI: Direct command execution
- MCP: IDE-level integration
- Skills: Semantic knowledge injection
- System Prompts: Behavioral context injection

---

### **3. Platform** (Dropdown - System & Architecture)

**Purpose:** Understand how Empirica works under the hood

```
Platform ▼
├── Architecture (architecture.md)
├── Cross-AI Collaboration (collaboration.md)
├── AI vs Agent Patterns (ai_vs_agent.md)
└── Components (NEW - components.md)
```

**Rationale:**
- **Architecture** - System design, directory structure
- **Cross-AI Collaboration** - Sessions, goals, handoffs, storage
- **AI vs Agent Patterns** - High reasoning vs action-based
- **Components** - 11 enterprise components

**No changes from original plan**

---

### **4. Developers** (Dropdown - Implementation)

**Purpose:** Build with Empirica

```
Developers ▼
├── Getting Started (getting-started.md)
├── API Reference (api-reference.md)
└── Examples & Tutorials (NEW - examples.md)
```

**Rationale:**
- **Getting Started** - Installation, first CASCADE, quick start
- **API Reference** - Complete Python API docs
- **Examples & Tutorials** - Code examples, patterns, workflows

**Changes:**
- ❌ Removed MCP Integration (moved to CLI section)
- ✅ Streamlined to 3 core developer resources

---

### **5. Community** (Dropdown - Engagement)

**Purpose:** Connect and contribute

```
Community ▼
├── GitHub (external link)
├── Discussions (external link)
├── Contributing (NEW - to be created)
└── Contact Us (contact.md)
```

**Rationale:**
- **GitHub** - Source code, issues
- **Discussions** - Community forum
- **Contributing** - How to contribute
- **Contact Us** - Support, inquiries

**No changes from original plan**

---

### **CTAs (Top Right)**

```
[Get Started] → /getting-started
[Docs] → /docs/production/ (dropdown to production/reference/guides)
```

**Rationale:**
- **Get Started** - Primary CTA for new users
- **Docs** - Reference documentation (was main navbar item, now CTA)

**Changes:**
- ❌ Removed MCP Server CTA (now in CLI dropdown)
- ✅ Added Docs CTA (cleaner access to reference materials)

---


## Content Reorganization Required (REVISED)

### **New Pages to Create:**

#### 1. **`cli-interface.md`** ⭐ NEW (Build from scratch)

**Content to include:**
- CLI Philosophy (read-only by default, safety)
- Installation & Setup
- Core Commands (cascade, assess, investigate, monitor, bootstrap, status)
- Command Reference (detailed options)
- CLI Output Examples
- Interactive Mode
- CLI + Dashboard Integration
- Configuration
- Scripting & Automation
- Troubleshooting

**Sources:**
- `website/wireframes/03_cli_interface.md` (reference only, rebuild)
- `docs/production/03_CLI_QUICKSTART.md`
- `docs/guides/CLI_WORKFLOW_COMMANDS_COMPLETE.md`
- Actual CLI code: `empirica/cli/cli_core.py`

---

#### 2. **`skills.md`** ⭐ NEW (Build from scratch)

**Content to include:**
- What Are Empirica Skills
- Core Skills Categories (6 categories)
- How Skills Work
- Skills vs Traditional Docs
- Available Skills Documentation
- Using Skills (Bootstrap + MCP)
- Skills Development (Custom Skills)

**Sources:**
- `website/wireframes/02_skills.md` (reference only, rebuild)
- `docs/skills/SKILL.md`
- Skills directory structure

---

#### 3. **`system-prompts.md`** ⭐ NEW (Create from scratch)

**Content to include:**
- What Are System Prompts
- Why System Prompts Matter
- AI vs Agent System Prompts
- Role-Based Prompts
- Dynamic System Prompts (Future: Cognitive Vault)
- Using System Prompts
- Best Practices

**Sources:**
- `docs/AI_VS_AGENT_EMPIRICA_PATTERNS.md` (system prompts section)
- `architecture_VALIDATED.md` (system prompts section)
- Actual system prompt files (if they exist)

---

#### 4. **`components.md`** - Extract from `features.md`

**Content to extract:**
- 11 Enterprise Components
- Component architecture
- Component integration
- Component usage examples

**Keep in `features.md`:**
- Core Epistemic Features (13-vector, CASCADE)
- Advanced AI Intelligence (Bayesian Guardian, Drift Monitor)
- Investigation Strategy System
- Visualization & Monitoring
- Production & Enterprise Features

---

#### 5. **`mcp-integration.md`** - Extract from `features.md`

**Content to extract:**
- MCP Server Integration
- 23 MCP tools (list and descriptions)
- Setup and configuration
- IDE integration (Claude Desktop, VS Code, etc.)
- MCP tool usage examples

**Already in features.md MCP section**

---

#### 6. **`examples.md`** - Extract from `use-cases.md`

**Content to extract:**
- Code examples from each use case
- Implementation patterns
- Integration patterns
- Common workflows
- Scripting examples

**Keep in `use-cases.md`:**
- Overview table
- Use case descriptions (without code)
- Benefits and metrics
- Success factors
- Performance metrics

---

### **Pages to Update:**

#### 7. **Update `features.md`**
- ❌ Remove: MCP Integration section → move to `mcp-integration.md`
- ❌ Remove: Components section → move to `components.md`
- ✅ Keep: Core features, Bayesian, Drift, Investigation, Visualization

#### 8. **Update `use-cases.md`**
- ❌ Remove: Code examples → move to `examples.md`
- ✅ Keep: Use case descriptions, benefits, metrics, success factors

---

## Final Page Count (REVISED)

### **After Reorganization: 15 pages**

**Learn Section (4):**
1. index.md (What is Empirica)
2. epistemics.md (Epistemics & Calibration)
3. use-cases.md (Why It Matters)
4. features.md (Features Overview)

**CLI Section (4):** ⭐ NEW
5. cli-interface.md (CLI Interface) - **NEW**
6. mcp-integration.md (MCP Server) - **NEW** (extracted from features.md)
7. skills.md (Skills) - **NEW**
8. system-prompts.md (System Prompts) - **NEW**

**Platform Section (4):**
9. architecture.md (Architecture)
10. collaboration.md (Cross-AI Collaboration)
11. ai_vs_agent.md (AI vs Agent Patterns)
12. components.md (Components) - **NEW** (extracted from features.md)

**Developers Section (3):**
13. getting-started.md (Getting Started)
14. api-reference.md (API Reference)
15. examples.md (Examples & Tutorials) - **NEW** (extracted from use-cases.md)

**Docs Section:**
- Links to existing /docs/ structure (via CTA)

**Community Section:**
- External links + contact page

---


## Navigation Best Practices Applied

✅ **Max 5-6 main items** - We have 5 (Learn, Platform, Developers, Docs, Community)
✅ **2 CTAs** - Get Started + MCP Server
✅ **Logical grouping** - Conceptual → Technical → Implementation → Reference → Community
✅ **No repeated buttons** - Each page appears once in navigation
✅ **Clear hierarchy** - Dropdown menus organize related content
✅ **User journey** - Learn → Understand → Build → Reference → Engage

---

## Implementation Steps (REVISED)

### **Phase 1: Create New CLI Pages** ⭐ PRIORITY
1. ✅ Create `cli-interface.md` (build from scratch using wireframe as reference)
2. ✅ Create `skills.md` (build from scratch using wireframe as reference)
3. ✅ Create `system-prompts.md` (create from scratch using docs)
4. ✅ Create `mcp-integration.md` (extract from `features.md`)

### **Phase 2: Extract Other New Pages**
5. ✅ Create `components.md` (extract from `features.md`)
6. ✅ Create `examples.md` (extract from `use-cases.md`)

### **Phase 3: Update Existing Pages**
7. ✅ Update `features.md` (remove MCP and Components sections)
8. ✅ Update `use-cases.md` (remove code examples)
9. ✅ Add cross-links between related pages

### **Phase 4: Implement Navigation**
10. ✅ Implement navbar with 5 main items (Learn, CLI, Platform, Developers, Community)
11. ✅ Implement dropdown menus for each section
12. ✅ Add 2 CTAs (Get Started, Docs)
13. ✅ Add breadcrumbs to pages
14. ✅ Add "Next Steps" links at bottom of pages

### **Phase 5: Validate**
15. ✅ Test all navigation paths
16. ✅ Verify no broken links
17. ✅ Ensure mobile responsiveness
18. ✅ Validate all content accuracy

---

## User Journey Examples

### **Journey 1: New User**
```
Home (index.md)
  → Learn > Epistemics (epistemics.md)
  → Learn > Why It Matters (use-cases.md)
  → [Get Started CTA] (getting-started.md)
  → Developers > API Reference (api-reference.md)
```

### **Journey 2: Developer**
```
Home (index.md)
  → [Get Started CTA] (getting-started.md)
  → Developers > API Reference (api-reference.md)
  → Developers > Examples (examples.md)
  → Platform > Architecture (architecture.md)
```

### **Journey 3: Researcher**
```
Home (index.md)
  → Learn > Epistemics (epistemics.md)
  → Platform > Architecture (architecture.md)
  → Learn > Features (features.md)
  → Docs > Production Docs
```

### **Journey 4: IDE User**
```
Home (index.md)
  → [MCP Server CTA] (mcp-integration.md)
  → Developers > Getting Started (getting-started.md)
  → Platform > Collaboration (collaboration.md)
```

---

## Next Steps

**User Decision Required:**

1. **Approve navigation structure?**
   - 5 main items (Learn, Platform, Developers, Docs, Community)
   - 2 CTAs (Get Started, MCP Server)
   - Dropdown menus as proposed

2. **Approve content splits?**
   - Extract `components.md` from `features.md`
   - Extract `mcp-integration.md` from `features.md`
   - Extract `examples.md` from `use-cases.md`

3. **Proceed with implementation?**
   - Create 3 new pages
   - Update 2 existing pages
   - Implement navigation

---

**Status:** Ready for user review and approval
