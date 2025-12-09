# System Prompts - Customize Empirica for Your Use Case

**When and how to customize the canonical Empirica system prompt**

[Back to Home](index.md) | [Architecture →](architecture.md)

---

## Default: Use As-Is

**99% of users should use the canonical prompt without modification.**

The canonical prompt is designed to work for:
- ✅ All AI models (Claude, Gemini, Qwen, GPT-4, etc.)
- ✅ All task types (analysis, implementation, research)
- ✅ All experience levels (beginner to expert)

**Location:** `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`

---

## When to Customize

### 1. Domain-Specific Expertise Required

**Scenario:** AI needs specialized domain knowledge  
**Examples:** Medical research, legal analysis, financial modeling

**Customization Pattern:**

```markdown
## I. ROLE
**Role:** [Domain] Specialist with epistemic grounding
**Domain:** [Specific expertise area]
**Focus:** [Domain-specific priorities]

Example:
**Role:** Clinical Research Specialist with epistemic grounding
**Domain:** Randomized controlled trials, systematic reviews, meta-analysis
**Focus:** Evidence-based medicine, statistical rigor, CONSORT compliance
```

**What to keep:** All CASCADE workflow sections unchanged

---

### 2. Restricted Tool Environment

**Scenario:** Limited MCP tool access (e.g., air-gapped environment)  
**Examples:** Secure environments, custom deployments

**Customization Pattern:**

```markdown
## IV. TOOLS & PATTERNS

### Available MCP Tools (Limited):
- **Session:** `create_session`, `get_epistemic_state`
- **CASCADE:** `execute_preflight`, `execute_postflight`
- **Note:** Git integration unavailable in this environment

### Fallback Strategy:
- Use SQLite for all persistence
- Manual session continuity via handoff reports
- No cross-AI discovery (single-agent mode)
```

**What to keep:** Epistemic principles and vector definitions unchanged

---

### 3. Custom Risk Thresholds

**Scenario:** Team has different risk tolerance  
**Examples:** High-stakes environments (medical, financial) or experimental research

**High-Stakes (Conservative Thresholds):**

```markdown
### Decision Logic (High-Stakes)
Comprehension: clarity ≥0.8 AND signal ≥0.7  # Stricter
Foundation: know ≥0.7 AND context ≥0.8

Drift Detection:
- Drops >0.15 → Investigate  # More sensitive
- Critical drift >0.3 → Stop immediately
```

**Experimental (Permissive Thresholds):**

```markdown
### Decision Logic (Experimental)
Comprehension: clarity ≥0.5 OR signal ≥0.6  # More exploratory
Foundation: know ≥0.4 OR context ≥0.5

Drift Detection:
- Drops >0.4 → Investigate  # Less sensitive
- Critical drift >0.6 → Consider stopping
```

---

## Available System Prompts

### 1. Canonical System Prompt (Recommended)

**File:** `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`

**Use For:** General-purpose AI work  
**Length:** ~800 lines (comprehensive)  
**Features:**
- Full CASCADE workflow
- 13 epistemic vectors
- Goals & subtasks
- Git integration
- Mistakes tracking
- Edit guard (metacognitive editing)

**Best For:** Production use, multi-session work, complex tasks

---

### 2. Minimalist System Prompt

**File:** `docs/system-prompts/MINIMALIST_SYSTEM_PROMPT.md`

**Use For:** Simple tasks, quick experiments  
**Length:** ~200 lines (essential only)  
**Features:**
- Core CASCADE workflow
- 13 vectors (definitions only)
- No goals/subtasks
- No git integration

**Best For:** Single-session tasks, learning Empirica, minimal overhead

---

### 3. Web Edition Prompt

**File:** `docs/system-prompts/EMPIRICA_WEB_EDITION.md`

**Use For:** Browser-based AI assistants  
**Length:** ~400 lines (web-optimized)  
**Features:**
- Browser localStorage instead of SQLite
- No git integration
- Simplified continuity
- Mobile-friendly

**Best For:** Web-based deployments, no file system access

---

### 4. Gemini-Optimized Prompt

**File:** `docs/system-prompts/GEMINI.md`

**Use For:** Google Gemini models  
**Length:** ~600 lines (Gemini-specific)  
**Features:**
- Gemini-specific tool calling patterns
- Adjusted for Gemini's strengths (multimodal, long context)
- Optimized prompt structure for Gemini

**Best For:** Using Empirica with Gemini models

---

## Customization Workflow

### Step 1: Choose Base Prompt

```bash
# Copy canonical prompt as starting point
cp docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md \
   docs/system-prompts/MY_CUSTOM_PROMPT.md
```

### Step 2: Identify What to Change

**Safe to customize:**
- ✅ Role and domain expertise (Section I)
- ✅ Tool availability (Section IV)
- ✅ Risk thresholds (Section VI)
- ✅ Examples and use cases
- ✅ Integration patterns

**Do NOT change:**
- ❌ 13 vector definitions (Section II)
- ❌ CASCADE phase sequence (PREFLIGHT → CHECK → POSTFLIGHT)
- ❌ Storage architecture (reflexes table, git notes, JSON)
- ❌ Core epistemic principles

### Step 3: Test Thoroughly

```bash
# Create test session
empirica session-create --ai-id test-custom-prompt

# Run PREFLIGHT with custom prompt
# Verify vectors are stored correctly
empirica sessions-show --session-id <ID>

# Check storage layers
sqlite3 ~/.empirica/sessions/sessions.db \
  "SELECT * FROM reflexes WHERE session_id='<ID>'"
```

### Step 4: Validate Calibration

Run 5-10 sessions and check:
- ✅ Vectors stored correctly
- ✅ CASCADE phases complete
- ✅ Checkpoints/handoffs work
- ✅ Calibration tracking functional

---

## Common Customization Patterns

### Pattern 1: Add Domain Expertise

```markdown
## I. ROLE & DOMAIN

**Base Role:** AI assistant with epistemic self-awareness (Empirica)

**Domain Specialization:** [Your Domain]
- [Expertise 1]
- [Expertise 2]
- [Expertise 3]

**Domain-Specific Epistemic Concerns:**
- [What counts as "knowing" in your domain?]
- [What uncertainties matter most?]
- [What evidence is required for claims?]

## II. DOMAIN VECTORS (Extended)

In addition to the 13 core vectors, track:
- **domain_expertise:** [0.0-1.0] - Domain-specific knowledge depth
- **domain_validation:** [0.0-1.0] - Evidence quality by domain standards

**Store these in reflex_data JSON, not as separate SQLite columns**
```

---

### Pattern 2: Adjust Workflow for Speed

```markdown
## III. SIMPLIFIED CASCADE (Fast Mode)

**For tasks <30 minutes:**

1. **Quick PREFLIGHT** (2-3 vectors only)
   - know, do, uncertainty (skip others)
   
2. **Skip CHECK** (only for short tasks)

3. **Quick POSTFLIGHT** (same 3 vectors)
   - Measure learning delta

**Note:** Still writes to reflexes table for calibration tracking
```

---

### Pattern 3: Multi-Agent Coordination

```markdown
## IV. MULTI-AGENT COORDINATION

**Your Role in Team:** [Lead/Support/Specialist]

**Coordination Protocol:**
1. Query handoffs from other AIs: `query_handoff_reports(ai_id="<ID>")`
2. Discover goals: `discover_goals(from_ai_id="<ID>")`
3. Resume goals if needed: `resume_goal(goal_id="<ID>")`
4. Create handoff for next AI: `create_handoff_report(...)`

**Critical:** Always query before starting to avoid duplicate work
```

---

## Testing Your Custom Prompt

### Test Suite

```bash
# 1. Session creation
empirica session-create --ai-id test

# 2. PREFLIGHT (should work unchanged)
empirica preflight --session-id <ID> --prompt "Test task"

# 3. Submit vectors (verify all 13 stored)
empirica preflight-submit --session-id <ID> \
  --vectors '{"engagement":0.8,"know":0.6,...}' \
  --reasoning "Test"

# 4. Check storage
empirica sessions-show --session-id <ID> --output json | jq '.epistemic_state'

# 5. Verify git notes (if using git integration)
git notes --ref=empirica/checkpoints/<SESSION_ID> show HEAD
```

---

## Getting Help

### Resources

- **Customization Guide:** `docs/system-prompts/CUSTOMIZATION_GUIDE.md`
- **Examples:** `docs/system-prompts/` (see different variants)
- **Architecture:** `docs/architecture/STORAGE_ARCHITECTURE_COMPLETE.md`

### Community

- **Discord:** [Join Community](https://discord.gg/collaborative-ai)
- **GitHub Discussions:** [Ask Questions](https://github.com/Nubaeon/empirica/discussions)
- **Issues:** [Report Problems](https://github.com/Nubaeon/empirica/issues)

---

## Best Practices

### ✅ Do

- Start with canonical prompt
- Test extensively before deploying
- Document your changes
- Share successful customizations with community
- Keep epistemic principles intact

### ❌ Don't

- Change vector definitions
- Skip CASCADE phases
- Modify storage architecture
- Remove epistemic transparency
- Guess at thresholds (test empirically)

---

## Next Steps

1. **Choose:** Select appropriate base prompt
2. **Customize:** Make minimal changes for your use case
3. **Test:** Run test sessions and validate
4. **Deploy:** Use in production with monitoring
5. **Share:** Contribute back to community

**Learn More:**
- [Getting Started](getting-started.md) - Basics
- [CASCADE Workflow](how-it-works.md) - Core concepts
- [Architecture](architecture.md) - Technical details
- [Examples](examples.md) - Real-world use cases

---

**Customize when needed, but remember: epistemic transparency is the core principle. Don't compromise it.** 🧠
