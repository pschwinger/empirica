# Multi-Agent Teams - Coordinated AI Collaboration

**Enable seamless work handoffs between specialist AIs**

[Back to Home](index.md) | [Architecture →](architecture.md)

---

## The Problem: AI Teams Don't Coordinate

Traditional multi-agent systems struggle with handoffs:
- 🤷 **No shared context** - Each AI starts from scratch
- 📝 **Lost learnings** - Investigation findings disappear
- 🔄 **Repeated work** - No memory of what previous AI discovered
- 🎯 **Goal confusion** - No clear tracking of who does what

**Result:** Token waste, duplicate effort, lost epistemic progress.

---

## Empirica's Solution: Git-Native Coordination

**Git solves distributed collaboration for code. Empirica extends this to AI mental states.**

### Three Coordination Mechanisms

1. **🎯 Goal Discovery** - Find work created by other AIs
2. **📤 Handoff Reports** - Share session context (90%+ token reduction)
3. **🔖 Git Checkpoints** - Resume exact epistemic state

**All mechanisms use git notes** - distributed, version-controlled, human-readable.

---

## Use Case 1: Specialist Handoff

**Scenario:** Research AI investigates architecture → Implementation AI builds it

### Research AI (AI-1)

```bash
# Create session
empirica session-create --ai-id research-specialist

# PREFLIGHT assessment
empirica preflight --session-id <ID> --prompt "Investigate auth architecture"
empirica preflight-submit --session-id <ID> --vectors '{"know":0.5,...}'

# Investigate (implicit CASCADE)
# ... explore codebase, read docs, analyze patterns ...

# CHECK assessment (gate decision)
empirica check \
  --session-id <ID> \
  --findings "OAuth2 with PKCE is standard" \
            "Token refresh requires secure storage" \
            "Current system uses JWT" \
  --unknowns "Integration with existing session management" \
  --confidence 0.80

# Create investigation handoff (PREFLIGHT → CHECK)
empirica handoff-create \
  --session-id <ID> \
  --task-summary "Investigated auth architecture options" \
  --key-findings "OAuth2 with PKCE recommended for security" \
                 "Token refresh pattern: rotation prevents theft" \
                 "JWT system already in place, can extend" \
  --remaining-unknowns "Session management integration details" \
  --next-session-context "Ready for implementation phase"
```

**Handoff type:** Investigation (PREFLIGHT → CHECK)  
**Token cost:** ~400 tokens (vs ~20,000 full context)

### Implementation AI (AI-2)

```bash
# Query handoff from research specialist
empirica handoff-query --ai-id research-specialist --limit 1

# Returns:
# {
#   "task_summary": "Investigated auth architecture options",
#   "key_findings": [
#     "OAuth2 with PKCE recommended for security",
#     "Token refresh pattern: rotation prevents theft",
#     "JWT system already in place, can extend"
#   ],
#   "remaining_unknowns": [
#     "Session management integration details"
#   ],
#   "epistemic_growth": {
#     "know": 0.5 → 0.75 (gained 0.25 domain knowledge)
#   }
# }

# Create new session with context
empirica session-create --ai-id implementation-specialist

# PREFLIGHT with transferred knowledge
empirica preflight-submit \
  --session-id <NEW_ID> \
  --vectors '{"know":0.75,...}'  # Start where AI-1 left off!

# ACT phase (do the work)
# ... implement OAuth2 with PKCE ...

# POSTFLIGHT
empirica postflight --session-id <NEW_ID>
```

**Result:** AI-2 starts with AI-1's learned knowledge. No duplicate investigation!

---

## Use Case 2: Goal Discovery & Resumption

**Scenario:** AI-1 starts large project → AI-2 discovers and continues it

### AI-1 Creates Goal

```bash
# Create goal with scope
empirica goals-create \
  --session-id <ID> \
  --objective "Migrate website from Jinja2 to Astro" \
  --scope-breadth 0.7 \
  --scope-duration 0.6 \
  --scope-coordination 0.3 \
  --success-criteria "Build passes" \
                     "All pages render" \
                     "Design preserved"

# Add subtasks
empirica goals-add-subtask \
  --goal-id <GOAL_ID> \
  --description "Setup Astro build pipeline" \
  --importance high

empirica goals-add-subtask \
  --goal-id <GOAL_ID> \
  --description "Migrate content pages" \
  --importance critical

# Complete first subtask
empirica goals-complete-subtask \
  --task-id <TASK1_ID> \
  --evidence "Astro builds successfully, 475ms build time"

# Create checkpoint
empirica checkpoint-create --session-id <ID>
```

**Goal stored in:** `refs/notes/empirica/goals/<goal_id>`

### AI-2 Discovers & Resumes

```bash
# Discover goals from all AIs
empirica goals-discover

# Returns:
# Goal f366e3be-4e6a-47fb-afe6-4e05b0c31d79
#   Objective: Migrate website from Jinja2 to Astro
#   Created by: ai-1
#   Progress: 1/2 subtasks complete (50%)
#   Status: IN_PROGRESS

# Resume goal
empirica goals-resume \
  --goal-id f366e3be-4e6a-47fb-afe6-4e05b0c31d79 \
  --ai-id ai-2

# Query subtasks to see what's done
empirica goals-get-subtasks --goal-id <GOAL_ID>

# Returns:
# Subtasks:
#   ✅ Setup Astro build pipeline (completed)
#   ⏳ Migrate content pages (pending)

# Continue work from where AI-1 left off
# ... migrate remaining pages ...

# Complete final subtask
empirica goals-complete-subtask \
  --task-id <TASK2_ID> \
  --evidence "All 19 pages migrated, design preserved"
```

**Result:** Seamless work continuation. AI-2 knows exactly what's done and what remains.

---

## Use Case 3: Parallel Exploration + Merge

**Scenario:** Multiple AIs explore different approaches → Merge best insights

### Setup: 3 AIs Explore in Parallel

```bash
# AI-1: Security-focused approach
empirica goals-create --objective "Design secure auth" --ai-id security-ai
git checkout -b approach/security

# AI-2: Performance-focused approach  
empirica goals-create --objective "Design fast auth" --ai-id perf-ai
git checkout -b approach/performance

# AI-3: UX-focused approach
empirica goals-create --objective "Design seamless auth" --ai-id ux-ai
git checkout -b approach/ux
```

### Each AI Works Independently

```bash
# Each AI runs CASCADE workflow on their branch
# Findings stored in git notes per branch
# No coordination needed during exploration
```

### Integration AI Merges Insights

```bash
# Query all handoffs
empirica handoff-query --ai-id security-ai --limit 1
empirica handoff-query --ai-id perf-ai --limit 1
empirica handoff-query --ai-id ux-ai --limit 1

# Compare findings
# Security-AI: "OAuth2 with PKCE prevents token theft"
# Perf-AI: "JWT caching reduces DB queries by 80%"
# UX-AI: "Persistent sessions reduce login friction"

# Merge branches with git
git checkout main
git merge approach/security
git merge approach/performance  
git merge approach/ux

# Create integrated implementation
# Uses best insights from all three approaches
```

**Result:** Superhuman perspective integration. Best of all approaches combined.

---

## Coordination Patterns

### Pattern 1: Investigation → Implementation

```
Research Specialist → Findings → Implementation Specialist
  (PREFLIGHT→CHECK)              (Start with CHECK knowledge)
```

**Token efficiency:** 90%+ reduction (400 vs 20,000 tokens)

### Pattern 2: Horizontal Handoff

```
AI-1 → Goal + Subtasks → AI-2 → Continue work
   (Creates structure)        (Resumes from checkpoint)
```

**No token overhead:** Goals in git notes, query on-demand

### Pattern 3: Parallel + Merge

```
       AI-1 (Branch A)
      /              \
Main                   Merge → Integrated solution
      \              /
       AI-2 (Branch B)
```

**Git handles complexity:** Standard merge tools work

---

## Multi-Agent Scope Vector

Goals track coordination complexity:

```bash
empirica goals-create \
  --scope-coordination 0.8  # 0.0-1.0 scale
```

**Scope.coordination:**
- `0.0-0.2` - Solo work, minimal coordination
- `0.3-0.5` - Occasional handoffs
- `0.6-0.8` - Frequent multi-agent collaboration
- `0.9-1.0` - Complex orchestration, many AIs

**Used for:** Resource planning, complexity estimation, handoff tracking

---

## Git Notes Structure

All coordination data stored in git notes:

```
refs/notes/empirica/
├── goals/<goal_id>           # Goal definitions
├── checkpoints/<session_id>   # Epistemic state snapshots
└── handoff/<session_id>       # Handoff reports
```

**Benefits:**
- 🌐 **Distributed** - Works across repos, forks, remotes
- 🔍 **Human-readable** - `git notes show` reveals content
- 🔄 **Merge-able** - Conflict resolution built-in
- 📊 **Queryable** - Standard git tools work

---

## Architecture

### Handoff Types (Flexible)

**1. Investigation Handoff** (PREFLIGHT → CHECK)
- **Use:** Specialist transitions
- **Contains:** Findings, unknowns, epistemic deltas
- **Example:** Research → Implementation

**2. Complete Handoff** (PREFLIGHT → POSTFLIGHT)
- **Use:** Full session completion
- **Contains:** Full learning deltas, artifacts created
- **Example:** Feature complete, ready for review

**3. Planning Handoff** (No assessments)
- **Use:** Documentation only
- **Contains:** Context, decisions, no epistemic data
- **Example:** Meeting notes, design docs

**Auto-detection:** CLI automatically picks correct type based on available assessments.

---

## Real-World Scenarios

### Scenario 1: 24/7 Development

**Problem:** Project needs continuous progress across timezones.

**Solution:**
```bash
# AI-1 (US timezone) works 8 hours
empirica preflight → work → checkpoint → handoff

# AI-2 (EU timezone) resumes
empirica checkpoint-load latest:active:ai-1
empirica handoff-query --ai-id ai-1
# Continues work seamlessly

# AI-3 (Asia timezone) continues
empirica checkpoint-load latest:active:ai-2
# 24/7 progress maintained
```

### Scenario 2: Security Review Pipeline

**Problem:** Every feature needs security validation.

**Solution:**
```bash
# Dev AI implements feature
empirica goals-create --objective "Add file upload"
empirica postflight --session-id <ID>

# Security AI discovers goal
empirica goals-discover
# Reviews implementation, adds subtask: "Security audit"

# If issues found, creates investigation handoff
empirica handoff-create \
  --findings "Path traversal vulnerability in filename handling" \
  --unknowns "Input validation coverage"

# Dev AI queries handoff, fixes issues
empirica handoff-query --ai-id security-ai
# Implements fixes based on findings
```

### Scenario 3: Research Team

**Problem:** Multiple researchers exploring same problem space.

**Solution:**
```bash
# 5 AIs each explore different approach
empirica goals-create --objective "Optimize algorithm X"
git checkout -b explore/<approach-name>

# Each documents findings in handoff
empirica handoff-create --key-findings "..."

# Meta-researcher synthesizes insights
empirica handoff-query --limit 10
# Analyzes all findings, creates unified solution
```

---

## Next Steps

1. **Create your first goal** with coordination scope
2. **Generate handoff report** after completing work
3. **Query handoffs** from other AIs
4. **Resume goals** created by other AIs

**Learn more:**
- [How It Works](how-it-works.md) - CASCADE workflow
- [Making Git Sexy Again](git-integration.md) - Git notes details
- [Architecture](architecture.md) - Storage architecture

---

**Multi-agent coordination that actually works:** Git-native, token-efficient, epistemically continuous. 🤝
