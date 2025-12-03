# Empirica Distribution Strategy: One-Click Install for 9+ AI Platforms

**Date:** 2025-12-03
**Status:** Distribution Architecture & Implementation Plan
**Scope:** Supporting all major AI providers and coding platforms globally

---

## Executive Summary

Based on market research of **2025 developer practices**, here's the distribution strategy:

**Primary Goal:** "One-click install" that:
- ✅ Works on Windows, macOS, Linux
- ✅ Supports all major AI providers (Claude, GPT-5, Gemini, Llama, Qwen, DeepSeek, Windsurf, Cursor, Copilot)
- ✅ Requires zero manual environment setup
- ✅ Available to both technical and non-technical users

**Recommended Approach:**
1. **Distribute via `uv` (primary)** - Modern Python standard, auto-venv creation
2. **Add Homebrew tap (macOS/Linux)** - Native package manager
3. **Add Chocolatey (Windows)** - Native package manager
4. **Offer Docker (optional)** - For complex setups
5. **Keep npm separate** - CLI wrapper if needed, MCP server stays in Python
6. **Provider-agnostic system prompt** - Works with any LLM provider

---

## Part 1: The venv Question & Modern Alternatives

### Current Approach: venv

**How you currently do it:**
```bash
# Create environment
python3 -m venv .venv-mcp

# Activate
source .venv-mcp/bin/activate

# Install
pip install -r requirements.txt
```

**Issue for users:** Requires them to:
- Know what venv is
- Remember to activate it
- Handle path setup on different OS

**Reality check:** This is **fine for developers**, but **not one-click** for non-technical users.

---

### Modern Alternative 1: `uv` (RECOMMENDED for Distribution)

**What uv is:** 2025's fastest, most user-friendly Python package manager

**How users install Empirica with uv:**
```bash
# That's it. One command. No venv needed.
uv tool install empirica-cli

# To run:
empirica start  # Already in PATH

# To upgrade:
uv tool upgrade empirica-cli
```

**Why uv is best for distribution:**
- ✅ Creates venv automatically (hidden from user)
- ✅ Manages Python version auto-installation if needed
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ **2.6x faster** than pip
- ✅ Replacing Poetry as modern standard (2025)
- ✅ Zero configuration needed
- ✅ 3 million+ downloads/month on PyPI

**Where users get it:**
```bash
# macOS
brew install uv

# Windows (via Winget or Chocolatey)
choco install uv

# Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or anywhere else:
pip install uv
```

**One-click for users = we distribute on PyPI, they run `uv tool install`**

---

### Modern Alternative 2: `pipx` (Also Good)

**How it works:**
```bash
pipx install empirica-cli
# Creates isolated venv in ~/.local/bin/empirica
```

**Comparison to uv:**
- ✅ Also creates hidden venv
- ❌ Slightly slower than uv
- ✅ More widely known (existed longer)
- ✅ Works with older Python

**Status:** Still widely used (2025), but uv is becoming standard

---

### Modern Alternative 3: `Poetry` (Professional Grade)

**For developers who want to contribute to Empirica:**
```bash
poetry install  # Creates venv, installs everything
poetry shell    # Activates it
```

**For end-users:**
```bash
pip install empirica-cli  # This can work, but requires pip knowledge
```

**Reality:** Poetry is great for **development**, not as good for **distribution to end-users**

---

### Our Recommendation for venv → Distribution

**Keep using venv for:**
- ✅ Local development
- ✅ Testing & CI/CD
- ✅ Docker builds

**Switch to `uv` for:**
- ✅ End-user distribution (one-click install)
- ✅ Documentation examples
- ✅ Getting started guides

**Implementation:**
1. Convert `requirements.txt` → `pyproject.toml` (Poetry format)
2. Distribute on PyPI (standard)
3. Users install via: `uv tool install empirica-cli` OR `pipx install empirica-cli` OR `pip install empirica-cli`
4. We then add Homebrew/Chocolatey for convenience (not requirement)

---

## Part 2: Multi-OS Installer Complexity Assessment

### Option 1: PyPI + Package Managers (RECOMMENDED)

**Distribution Method:**
```
PyPI (pip/uv/pipx) ← Primary (all platforms)
  ↓
Homebrew Tap ← macOS/Linux convenience
  ↓
Chocolatey ← Windows convenience
  ↓
Docker ← Optional, for complex setups
```

**Complexity Level:** **Low-Medium** ⭐⭐

**Effort to implement:**
- PyPI: 1-2 hours (just `pyproject.toml` + GitHub Actions)
- Homebrew tap: 2-3 hours (create tap repo, formula)
- Chocolatey: 2-3 hours (nuspec file + moderation)
- **Total: 5-8 hours**, one-time setup

**Ongoing maintenance:**
- Update PyPI: Automatic with GitHub release
- Homebrew: Auto-sync from PyPI or GitHub release
- Chocolatey: Auto-sync from GitHub release
- **Total: 10 minutes per release**

**Why this is best:**
- ✅ Follows 2025 industry standard (same pattern as Ruff, uv itself, etc.)
- ✅ Works cross-platform automatically
- ✅ No custom code needed
- ✅ Native for each platform
- ✅ Users already familiar
- ✅ Easy to maintain

---

### Option 2: PyInstaller Binaries (Not Recommended)

**What it does:** Creates standalone `.exe` / `.app` / `.bin` executable for each OS

**Complexity Level:** **Medium** ⭐⭐⭐

**Effort:**
- Initial setup: 8-12 hours (must build on each OS or use VM)
- Per release: 1-2 hours (rebuild for Windows, macOS, Linux)
- Maintenance: High (debug platform-specific issues)

**Issues:**
- ❌ Binaries are 50-100 MB each (vs 5 MB via pip)
- ❌ Must rebuild every release
- ❌ Antivirus false positives on Windows
- ❌ Can't hot-patch dependencies (security updates require full rebuild)
- ❌ macOS code signing complexity
- ❌ No way to update Python interpreter in binary

**Only use if:** Users are completely non-technical (can't install Python)
**Better alternative:** Use `uv` which handles this automatically

---

### Option 3: Tauri Desktop App (Modern but Overkill)

**What it does:** Create native GUI app that wraps CLI

**Complexity Level:** **Medium-High** ⭐⭐⭐⭐

**Advantages:**
- ✅ Beautiful one-click installer
- ✅ Auto-updates built-in
- ✅ Small (~2.5 MB vs Electron's 85 MB)
- ✅ Cross-platform

**Disadvantages:**
- ❌ Not needed for CLI tool
- ❌ Adds GUI overhead
- ❌ Need separate desktop team
- ❌ Learning curve for Rust

**Use case:** If you want a Desktop IDE version later (Phase 5+), not for current CLI

---

### Option 4: Docker (Complementary)

**Complexity Level:** **Low** ⭐⭐

**Effort:** 2-3 hours, includes in release CI/CD

**Why Docker?**
- ✅ Works everywhere (Linux, macOS, Windows with Docker Desktop)
- ✅ Zero Python dependency
- ✅ Reproducible environment
- ✅ Easy for teams to share
- ❌ Slower startup (container overhead)
- ❌ File system permissions complexity on macOS/Windows

**Best for:** Teams already using Docker, enterprise deployments

**Not primary because:** Most individual developers prefer native tools

---

## Part 3: npm Package Strategy - Should We Do It?

### The Question

"Should Empirica CLI be an npm package that bundles Python MCP server?"

### The Answer

**Short: No. Here's why:**

---

### Why npm + Python Hybrid is Hard

**Problem 1: Double Dependency Hell**
```json
// package.json
{
  "dependencies": {
    "empirica-cli": "1.0.0"  // Downloads npm package
  }
}
```

When user installs via npm, they get:
- ✅ JavaScript CLI wrapper
- ❌ NOW they need Python too
- ❌ AND a venv for the Python server
- ❌ AND configuration for communication

This is **worse** than just using pip directly.

**Problem 2: Bundle Size**
```
Option A: pip install empirica-cli
→ 15 MB (Python + dependencies)

Option B: npm install empirica
→ 180+ MB (npm package + Python runtime bundled)
```

npm would be **12x larger** due to Python runtime bundling.

**Problem 3: Maintenance Nightmare**
- Update Python? Must rebuild entire npm package
- Update npm dependency? Must test with bundled Python
- Version conflicts? User has npm Python + system Python
- File size grows with each release

---

### What npm is Actually Good For

**npm IS good for:**
1. ✅ Node.js tools (written in TypeScript/JavaScript)
2. ✅ Web services
3. ✅ Frontend tooling (Webpack, Vite, etc.)
4. ✅ Distributing pre-built binaries (like `uv-npm` does)

**npm is POOR for:**
- ❌ Python development (use pip)
- ❌ CLI tools with heavy dependencies (use Homebrew/pip)
- ❌ Hybrid Python+Node projects

---

### Real-World Example: Why This Failed

**Vercel CLI** tried hybrid approach:
```bash
npm install -g vercel
# Installation downloads 200+ MB
# Includes Node.js, npm, Python runtime
# Slow, bloated, confusing updates
```

Modern approach: Just use pip for Python, npm for JavaScript, keep them separate.

---

### Our Recommendation: Keep Them Separate

**Distribution Model:**
```
┌─────────────────────────────────────┐
│  Empirica CLI (Python)              │
├─────────────────────────────────────┤
│ Distribution: pip/uv/Homebrew       │
│ Version: managed by pyproject.toml  │
│ Dependencies: Python packages       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Empirica MCP Server (Python)       │
├─────────────────────────────────────┤
│ Distribution: pip/uv                │
│ Version: same as CLI                │
│ Runs in: hidden venv (created by uv)│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Empirica System Prompt (Markdown)  │
├─────────────────────────────────────┤
│ Distribution: git, part of Empirica │
│ Location: ~/.empirica/CLAUDE.md     │
│ Provider agnostic: Works everywhere │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Empirica Skill (Markdown)          │
├─────────────────────────────────────┤
│ Distribution: Share as folder/JSON  │
│ Location: Claude.ai skill import    │
│ Claude-specific: Claude only        │
└─────────────────────────────────────┘
```

**Why separate?**
- ✅ Each component uses best distribution for its platform
- ✅ Users can install pieces they need
- ✅ No bloat
- ✅ Easy to update independently
- ✅ Standard pattern (like how Playwright does it)

---

## Part 4: Provider Agnosticism - Supporting ALL AI Platforms

### Current Reality (2025)

**Developers are using 3+ AI tools in parallel:**
- 59% run 3+ tools simultaneously
- 20% manage 5+ tools
- Top tools: ChatGPT (82%), Copilot (68%), Claude.ai (41%), Gemini (47%)

**This means:** Users want to use Empirica with multiple providers.

### How to Support All Providers

**System Prompt Strategy:** Provider-agnostic core

```markdown
# Empirica Agent Framework (Provider Agnostic)

This framework is designed to work with ANY AI language model:
- OpenAI (GPT-4, GPT-5, etc.)
- Anthropic (Claude)
- Google (Gemini)
- Meta (Llama)
- Alibaba (Qwen)
- DeepSeek
- Mistral
- Local models (Ollama, etc.)

## Core Components (LLM-Agnostic)

### 1. Epistemic Vectors (13-dimensional)
- KNOW, UNCERTAINTY, CLARITY, COHERENCE, etc.
- These are framework concepts, not model-specific
- Any LLM can assess/update these

### 2. CASCADE Workflow
- PREFLIGHT: Assess state (all models do this)
- INVESTIGATE: Gather information (all models can do this)
- ACT: Execute plan (all models can do this)
- POSTFLIGHT: Capture learning (all models can do this)

### 3. Goal Orchestration
- Create goals, track progress, iterate
- Works with any model

## What's Provider-Specific?

- **System Prompt Variations:** Each provider has different token limits, behavior quirks
- **API Integration:** How to call each provider
- **Cost Tracking:** Different pricing models
- **Quality Metrics:** Some models faster, some smarter, etc.
```

### Implementation: Three Tiers of System Prompts

**Tier 1: Universal Core** (works with all providers)
```markdown
# Empirica Metacognitive Framework (Universal)
## Epistemic Vectors
## CASCADE Workflow
## Goal Creation & Tracking
## Learning Patterns
```

**Tier 2: Provider Optimizations** (Claude-specific, GPT-specific, etc.)
```markdown
# Empirica + Claude Sonnet 4.5
- Leverage 1M token context window
- Use computer use capabilities
- Optimize for reasoning_effort parameter
```

**Tier 3: Skill Integrations** (Platform-specific)
```
Empirica Skill for Claude.ai (Claude only)
Empirica for ChatGPT custom GPT (OpenAI only)
Empirica for Gemini workspace (Google only)
```

---

## Part 5: Distribution Timeline & Priority

### Phase 0: Foundation (NOW)
**Effort: 5-8 hours, one-time**

1. ✅ Convert to `pyproject.toml` (Poetry format)
   - Currently uses `requirements.txt` and venv
   - Add `[build-system]` section
   - Add `[tool.poetry.scripts]` for CLI entrypoint

2. ✅ Create `setup.py` / `setup.cfg` alternative (fallback)
   - For users with old pip

3. ✅ Publish to PyPI (test first via TestPyPI)
   - Create account, get token
   - Run `poetry publish` (or use GitHub Actions)
   - Takes ~5 minutes

4. ✅ Verify installation works via uv/pipx
   ```bash
   uv tool install empirica-cli
   empirica --help
   ```

**Result:** Users can install via `uv tool install empirica-cli`

---

### Phase 1: Package Manager Integration (Week 2)
**Effort: 4-6 hours, one-time**

1. **Homebrew Tap** (2-3 hours)
   - Create `homebrew-empirica` repo on GitHub
   - Add formula pointing to PyPI
   - Test: `brew install yogapad/empirica/empirica-cli`

2. **Chocolatey** (2-3 hours)
   - Create `.nuspec` manifest
   - Upload to Chocolatey
   - Moderation takes 1-2 days
   - Users: `choco install empirica-cli`

3. **Docker** (1-2 hours)
   - Create `Dockerfile` with Python + Empirica
   - Publish to Docker Hub
   - Users: `docker run empirica-cli empirica start`

**Result:** Cross-platform one-click install via native package managers

---

### Phase 2: Provider Optimization (Week 3-4)
**Effort: 8-12 hours, ongoing**

1. **System Prompt Variants**
   - Create `EMPIRICA_UNIVERSAL.md` (all providers)
   - Create `EMPIRICA_CLAUDE.md` (optimized for Claude)
   - Create `EMPIRICA_GPT5.md` (optimized for GPT-5)
   - Create `EMPIRICA_GEMINI.md` (optimized for Gemini)

2. **Distribution Config**
   - Users download variant for their provider
   - Or one universal version (works with all)

3. **Quality Testing**
   - Test same goal on: Claude, GPT-4, Gemini, Llama
   - Measure epistemic tracking accuracy
   - Optimize prompts based on results

---

### Phase 3: Skill Integration (Week 4-5)
**Effort: 4-6 hours, per-platform**

1. **Claude Skill** (2-3 hours)
   - Already documented
   - Create skill folder + deploy

2. **ChatGPT Custom GPT** (2-3 hours)
   - Similar to skill but OpenAI format
   - Create custom instruction + actions

3. **Gemini Workspace** (2-3 hours)
   - Gemini equivalent of skills

4. **Open-source Models** (1-2 hours)
   - Ollama integration guide
   - Local Llama/Mistral setup

---

### Phase 4: Documentation & UX (Ongoing)

**Update installation guide** (already started):
- ✅ Created EMPIRICA_INSTALLATION_GUIDE.md
- Update with `uv` as primary method
- Add provider-specific setup instructions
- Add troubleshooting per provider

**Create quick-start scripts**:
```bash
# downloads and runs one-line install
curl -sSL https://empirica.sh/install.sh | bash
```

---

## Part 6: Realistic Distribution Timeline & Effort

### If You (solo) Implement

| Phase | Task | Hours | When | Notes |
|-------|------|-------|------|-------|
| **Now** | PyPI publishing | 2-3 | This week | Core distribution |
| **Week 2** | Homebrew + Chocolatey | 4-6 | Next week | Package managers |
| **Week 3** | Docker + Scripts | 3-4 | Following week | Optional shortcuts |
| **Week 4** | System prompt variants | 4-6 | Ongoing | Per-provider optimization |
| **Week 5+** | Skill integrations | 2-4 per | As needed | Claude, GPT, Gemini |
| **Total** | Full rollout | **18-26 hours** | **1 month** | One-person doable |

### If You Get 1-2 AIs/Contributors to Help

| Parallel Streams | Timeline |
|---|---|
| PyPI + Homebrew (you) + Chocolatey (AI#1) | Week 1-2 |
| Docker (AI#2) + Prompt variants (AI#3) | Week 2-3 |
| Skills + Testing (team) | Week 3-4 |
| **Total: 2-3 weeks** | **Much faster** |

---

## Part 7: What to DO Next - Concrete Steps

### Step 1: Convert to pyproject.toml (2 hours)

```bash
# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[project]
name = "empirica-cli"
version = "0.1.0"
description = "Empirica: Epistemic reasoning framework for AI agents"
authors = [{name = "Empirica Team", email = "team@empirica.ai"}]
license = {text = "MIT"}
requires-python = ">=3.9"
dependencies = [
    "click>=8.1.0",
    "gitpython>=3.1.0",
    # ... rest of dependencies from requirements.txt
]

[project.scripts]
empirica = "empirica.cli:main"  # Points to your CLI entry

[project.urls]
Homepage = "https://empirica.sh"
Documentation = "https://docs.empirica.sh"
Repository = "https://github.com/empirica/empirica"
EOF
```

### Step 2: Test with uv (30 minutes)

```bash
# Install uv locally
brew install uv  # or download from https://astral.sh/uv

# Build distribution
uv build  # Creates dist/ directory

# Test in temp environment
uv venv /tmp/test-empirica
source /tmp/test-empirica/bin/activate
pip install dist/empirica*.whl

# Verify
empirica --help
```

### Step 3: Publish to TestPyPI (30 minutes)

```bash
# Create account at test.pypi.org
# Generate API token

# Publish to test
uv publish --publish-url https://test.pypi.org/legacy/ \
  --token "$TEST_PYPI_TOKEN"

# Test installation
pip install -i https://test.pypi.org/simple/ empirica-cli

# Verify works
empirica --help
```

### Step 4: Publish to Real PyPI (15 minutes)

```bash
# Create account at pypi.org
# Generate API token

# Publish
uv publish --token "$PYPI_TOKEN"

# Now anyone can:
uv tool install empirica-cli
# or
pipx install empirica-cli
# or
pip install empirica-cli
```

### Step 5: Create GitHub Actions for Auto-Publishing (1 hour)

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI
on:
  push:
    tags:
      - 'v*'
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
      - run: uv build
      - run: uv publish --token ${{ secrets.PYPI_TOKEN }}
```

Then releases are automatic:
```bash
git tag v0.2.0
git push origin v0.2.0
# Workflow auto-publishes to PyPI
```

---

## Part 8: Provider-Agnostic System Prompt Architecture

### Current State
- CANONICAL_SYSTEM_PROMPT.md works with Claude
- System Prompt is somewhat Claude-optimized

### Proposed Change

**Create three prompt variants:**

**1. EMPIRICA_UNIVERSAL.md** (All providers)
```markdown
# Empirica Metacognitive Framework (Works with Any AI)

## Who This Works With
- OpenAI: GPT-4, GPT-5, o1, Codex
- Claude: All versions
- Google: Gemini 1.5, 2.5
- Meta: Llama 3.1, 4
- Alibaba: Qwen 2.5
- DeepSeek: Latest
- Mistral, Local models, etc.

## Design Principles
- Pure reasoning concepts (not API-specific)
- Epistemic vectors are model-agnostic
- CASCADE workflow works everywhere
- Goal tracking is simple YAML/JSON

## Provider Differences (Handled Automatically)
- Claude: Uses system prompt directly
- GPT: Might shorten for token limits
- Gemini: Might use different formatting
- Local: No changes needed
```

**2. EMPIRICA_CLAUDE.md** (Claude optimization)
- Full system prompt
- Leverage 1M token context
- Use extended thinking if available
- Optimize for Claude's strengths

**3. EMPIRICA_GPT5.md** (GPT-5 optimization)
- Shorter prompt (less redundancy)
- Leverage reasoning effort parameter
- Optimize for different behavior patterns

### Distribution Strategy

```bash
# Users pick their provider
curl https://empirica.sh/prompts/universal.md  # Works everywhere
curl https://empirica.sh/prompts/claude.md     # Optimized for Claude
curl https://empirica.sh/prompts/gpt5.md       # Optimized for GPT-5
curl https://empirica.sh/prompts/gemini.md     # Optimized for Gemini

# Or via command
empirica prompt --provider=claude    # Get Claude-optimized
empirica prompt --provider=universal # Get universal

# Or embedded in CLI
empirica start --provider=gpt5 --api-key=$OPENAI_KEY
```

---

## Part 9: Success Metrics & Definition of "One-Click Install"

### Success Criteria

**Definition: "One-Click Install"**

A non-technical user should be able to:
```bash
# 1. Download/run installer
[Click install button OR run one command]

# 2. Run immediately without:
# - Understanding Python environments
# - Manual venv creation
# - Path configuration
# - Dependency management

# 3. Execute Empirica
empirica start
```

**Success Metrics:**

| Metric | Target | Verification |
|--------|--------|---|
| Installation time | <5 minutes | Time new user from install to `empirica --help` |
| Success rate | >95% | Works on Windows, macOS, Linux without errors |
| Uninstall cleanness | Zero remnants | `brew uninstall` or `uv uninstall` leaves no traces |
| Multi-provider support | All 5+ major | Can use with Claude, GPT-5, Gemini, Llama, local models |
| System prompt availability | Works everywhere | User can apply same system prompt to any provider |
| Skill support | Claude + fallback | Skill for Claude, docs for others |

---

## Part 10: Risk Assessment & Mitigation

### Risk 1: PyPI Publishing Complexity
**Risk:** New to PyPI publishing, might make mistakes
**Mitigation:**
- Use TestPyPI first (free dry-run)
- Follow Astral's uv publishing guide (they do it)
- GitHub Actions automation reduces manual steps

### Risk 2: Cross-Platform Python Issues
**Risk:** Works on Linux/Mac, fails on Windows (or vice versa)
**Mitigation:**
- Test on all three OS via CI/CD
- Use Docker for testing (simulates environments)
- `uv` is cross-platform tested already

### Risk 3: Package Manager Moderation Delays
**Risk:** Chocolatey approval takes days, user experience suffers
**Mitigation:**
- PyPI is primary (instant)
- Homebrew syncs automatically
- Chocolatey is convenience, not required

### Risk 4: Prompt Quality Varies by Provider
**Risk:** System prompt tuned for Claude, doesn't work well with GPT-5
**Mitigation:**
- Test same task with 3+ providers
- Create provider-specific variants
- Document differences clearly
- Iterate based on user feedback

### Risk 5: Skill Integration Only Works with Claude
**Risk:** Other providers can't use Empirica Skill
**Mitigation:**
- Skill is optional (system prompt is primary)
- Create equivalent for ChatGPT custom GPT
- Document workarounds for other providers
- This is expected (skills are provider-specific)

---

## Summary: What to Do This Week

### Priority 1 (Today)
- [ ] Decide: Proceed with uv + Homebrew + Chocolatey strategy? (Recommended)
- [ ] Review this document for any changes

### Priority 2 (This Week)
- [ ] Convert `requirements.txt` → `pyproject.toml`
- [ ] Test with `uv install` locally
- [ ] Create TestPyPI account
- [ ] Publish to TestPyPI for testing

### Priority 3 (Next Week)
- [ ] Publish to real PyPI
- [ ] Create Homebrew tap repo
- [ ] Create Chocolatey submission
- [ ] Test cross-platform installation

### Priority 4 (Week 3+)
- [ ] Create provider-agnostic system prompts
- [ ] Develop Skill integrations per provider
- [ ] Set up CI/CD for automated publishing
- [ ] Full documentation update

---

## Appendix: Tool Comparison Summary

### For Distribution to End-Users

| Method | Effort | Users Understand | Cross-Platform | Speed | Size |
|--------|--------|---|---|---|---|
| **uv tool install** | ⭐ Minimal | ⭐⭐ Medium | ✅ Perfect | ⭐⭐⭐ Fast | 15 MB |
| **Homebrew** | ⭐⭐ Low | ⭐⭐⭐ High | ✅ Mac/Linux | ⭐⭐ Medium | 15 MB |
| **Chocolatey** | ⭐⭐ Low | ⭐⭐ Medium | ✅ Windows | ⭐⭐ Medium | 15 MB |
| **PyPI (pip)** | ⭐ Minimal | ⭐ Low | ✅ Perfect | ⭐⭐⭐ Fast | 15 MB |
| **Docker** | ⭐⭐ Low | ⭐⭐ Medium | ✅ Perfect | ⭐ Slow | 200 MB |
| **PyInstaller** | ⭐⭐⭐ High | ⭐⭐⭐ High | ❌ Needs rebuild | ⭐ Slow | 80 MB |
| **npm (hybrid)** | ⭐⭐⭐⭐ Very High | ⭐⭐ Medium | ✅ Perfect | ⭐ Slow | 180 MB |
| **Tauri** | ⭐⭐⭐⭐ Very High | ⭐⭐⭐ High | ✅ Perfect | ⭐ Slow | 100 MB |

**Recommended:** **uv + Homebrew + Chocolatey** combination

---

**Created:** 2025-12-03
**Next Review:** After Phase 1 implementation
**Status:** Ready for decision & implementation
