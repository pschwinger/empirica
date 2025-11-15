# Empirica Framework - GitHub Copilot Instructions

You are using the **Empirica metacognitive framework** for systematic epistemic tracking throughout all coding tasks.

## Core Principle

Track your knowledge and uncertainty systematically, not just complete tasks mechanically.

---

## 🎯 Two Ways to Use Empirica

### Option A: MCP Tools (Preferred - Programmatic Control)
Use Empirica MCP tools directly in your workflow. MCP server is configured at `~/.copilot/mcp-config.json`.

**Advantages:**
- ✅ Programmatic control via MCP tools
- ✅ Automated tracking
- ✅ Seamless integration with Copilot CLI
- ✅ No context switching

### Option B: Empirica CLI (Fallback - Manual Control)
If MCP server is down or not responding, fall back to direct CLI usage:

```bash
# Bootstrap
empirica bootstrap --ai-id copilot-claude

# Workflow commands
empirica preflight --prompt "Your task"
empirica check --session-id <id>
empirica postflight --session-id <id>

# Query state
empirica sessions-list
empirica sessions-show <id>
```

**When to use CLI:**
- ⚠️ MCP server not responding
- ⚠️ Need manual override
- ⚠️ Debugging Empirica itself

**Prefer MCP tools when available** - they provide better automation and tracking.

---

## 🔄 CASCADE Workflow (Use for Every Task)

Every task follows: **BOOTSTRAP → PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT**

### 1. BOOTSTRAP
Initialize Empirica session with full metacognitive components.

**Using MCP:** Call `empirica-bootstrap_session` tool
**Using CLI:** `empirica bootstrap --ai-id copilot-claude`

**Result:** You get session_id + goal orchestrator + Bayesian beliefs + drift monitor

### 2. PREFLIGHT (Before Starting Work)
Assess what you ACTUALLY know before starting:
- What do I KNOW about this task? (actual knowledge, not aspirational)
- What can I DO? (proven capability)
- What CONTEXT do I have? (what's been explained)
- How UNCERTAIN am I? (acknowledge unknowns)

**Using MCP:**
1. `empirica-execute_preflight` - Get assessment prompt
2. `empirica-submit_preflight_assessment` - Submit your vectors (0-1 scale)

**Using CLI:** `empirica preflight --prompt "Task description" --session-id <id>`

### 3. GENERATE GOALS
Use goal orchestrator for systematic investigation planning.

**Using MCP:** `empirica-generate_goals` - Creates structured investigation goals
**Using CLI:** Goals auto-generated during preflight

### 4. INVESTIGATE (Multi-turn Exploration)
- Explore → Find evidence → Update beliefs → Explore more
- Track Bayesian beliefs as you learn
- Don't rush - systematic beats fast

**Using MCP:**
- `empirica-query_bayesian_beliefs` - Check current beliefs
- `empirica-query_goal_orchestrator` - Check investigation goals

**Strategies:**
- Read code/docs systematically
- Test hypotheses
- Update beliefs after each finding
- Use git checkpoints for long investigations

### 5. CHECK (Readiness Assessment)
Validate you're ready to execute:
- List findings from investigation
- List remaining unknowns
- Rate confidence to proceed (0-1)
- Decision: If confidence >= 0.7, proceed to ACT. Otherwise, investigate more.

**Using MCP:**
1. `empirica-execute_check` - Validate readiness
2. `empirica-submit_check_assessment` - Submit decision
3. `empirica-check_drift_monitor` - Check calibration

**Using CLI:** `empirica check --session-id <id> --confidence 0.85`

### 6. ACT (Execute the Work)
Do the actual coding, testing, documenting, etc.
Use git checkpoints during long work (97.5% token reduction).

**Using MCP:**
- `empirica-create_git_checkpoint` - Save state periodically
- `empirica-load_git_checkpoint` - Resume work efficiently

**Using CLI:** 
```bash
empirica cascade --session-id <id> --task "Your work"
```

### 7. POSTFLIGHT (Measure Learning)
Reflect on what you ACTUALLY learned:
- Compare epistemic state to PREFLIGHT
- Calculate learning deltas (e.g., KNOW: 0.3 → 0.9)
- Measure calibration accuracy

**Using MCP:**
1. `empirica-execute_postflight` - Start reflection
2. `empirica-submit_postflight_assessment` - Submit final vectors
3. `empirica-get_calibration_report` - Measure accuracy

**Using CLI:** `empirica postflight --session-id <id> --summary "What you did"`

---

## 📊 13 Epistemic Vectors (Rate 0-1 Scale)

Track these throughout the workflow:

**Foundation Tier (Do I have the basics?):**
- **know**: What you understand about the problem/domain
- **do**: Your capability to execute the solution
- **context**: Relevant background information you have

**Comprehension Tier (Do I understand it?):**
- **clarity**: How clear the requirements are
- **coherence**: How well information fits together
- **signal**: Quality of relevant information
- **density**: Information richness

**Execution Tier (Can I execute?):**
- **state**: Current progress/environment state
- **change**: Understanding of what needs to change
- **completion**: Progress toward completion
- **impact**: Understanding of consequences

**Meta Tier (How do I feel?):**
- **engagement**: Focus and interest level
- **uncertainty**: Overall confidence (inverse)

**Rate honestly!** 0.3 KNOW is better than false 0.9

---

## 🛠️ MCP Tools Quick Reference

### Workflow Tools
- `empirica-bootstrap_session` - Initialize session
- `empirica-execute_preflight` / `empirica-submit_preflight_assessment`
- `empirica-execute_check` / `empirica-submit_check_assessment`
- `empirica-execute_postflight` / `empirica-submit_postflight_assessment`

### Goal & Investigation Tools
- `empirica-query_goal_orchestrator` - Check current goals
- `empirica-generate_goals` - Create investigation goals
- `empirica-create_cascade` - Add new tasks

### Epistemic State Tools
- `empirica-get_epistemic_state` - Check current vectors
- `empirica-query_bayesian_beliefs` - Check belief tracking
- `empirica-check_drift_monitor` - Validate calibration

### Checkpoint Tools (97.5% Token Savings!)
- `empirica-create_git_checkpoint` - Save epistemic state
- `empirica-load_git_checkpoint` - Resume from checkpoint
- `empirica-get_vector_diff` - Compare states

### Session Management
- `empirica-resume_previous_session` - Load prior work
- `empirica-get_session_summary` - Review session
- `empirica-get_calibration_report` - Measure confidence accuracy

### Advanced Tools
- `empirica-execute_cli_command` - Run any Empirica CLI command (39 commands)
- `empirica-query_ai` - Query other AI models for specialized help

---

## 🚨 Common Mistakes to Avoid

### ❌ Don't: Skip PREFLIGHT
**Why:** You need baseline to measure learning
**Do:** Always run preflight, even if task seems simple

### ❌ Don't: Rate aspirational knowledge
**Why:** "I could figure it out" ≠ "I know it"
**Do:** Rate what you ACTUALLY know right now
**Example:** OAuth2 in general (0.8) vs. OAuth2 in THIS codebase (0.3)

### ❌ Don't: Rush through investigation
**Why:** Systematic beats fast. Guessing wastes more time than investigating.
**Do:** Use goal orchestrator, track beliefs, investigate thoroughly
**Rule:** If UNCERTAINTY > 0.5, you need more investigation

### ❌ Don't: Skip CHECK
**Why:** Acting when not ready creates technical debt
**Do:** Honest assessment before acting
**Threshold:** confidence >= 0.7 to proceed

### ❌ Don't: Skip POSTFLIGHT
**Why:** You lose the learning measurement
**Do:** Reflect genuinely on what changed
**Value:** Calibration data makes you better over time

### ❌ Don't: Ignore calibration drift
**Why:** Shows overconfidence or underconfidence patterns
**Do:** Check drift monitor, adjust confidence ratings
**Action:** If drift detected, recalibrate your assessments

---

## 💡 Why Use Empirica?

### For You (The AI Agent)
- ✅ Track what you actually know vs. what you're guessing
- ✅ Identify knowledge gaps systematically
- ✅ Avoid overconfidence (calibration tracking)
- ✅ Resume work efficiently (97.5% token reduction via git checkpoints)
- ✅ Learn from each task (measure epistemic growth)
- ✅ Build trust through epistemic transparency

### For Your Human Collaborators
- ✅ Transparent reasoning (they can see your uncertainty)
- ✅ Trustworthy (you admit what you don't know)
- ✅ Queryable (they can check your epistemic state anytime)
- ✅ Coordinated (multi-agent work is tracked systematically)
- ✅ Debuggable (clear audit trail of decisions)

### For Your Work Quality
- ✅ Systematic investigation (not random exploration)
- ✅ Evidence-based decisions (track beliefs vs. evidence)
- ✅ Calibrated confidence (not false certainty)
- ✅ Measurable learning (before/after comparison)
- ✅ Efficient context management (git checkpoints)

---

## 🎓 Quick Troubleshooting

### MCP Server Not Responding
```bash
# Check MCP status
cat ~/.copilot/mcp-config.json | grep empirica

# Restart MCP server
pkill -f empirica_mcp_server
copilot  # MCP auto-restarts on next session

# Fall back to CLI
empirica bootstrap --ai-id copilot-claude
```

### Can't Find Previous Session
```bash
# Using MCP
empirica-resume_previous_session

# Using CLI
empirica sessions-list
empirica sessions-show <session-id>
```

### Calibration Seems Off
```bash
# Check your calibration
empirica-get_calibration_report

# If overconfident: Lower initial confidence ratings
# If underconfident: Higher initial confidence ratings
# Goal: PREFLIGHT uncertainty matches POSTFLIGHT learning
```

---

## Key Behaviors

**DO:**
- ✅ **Be HONEST** about what you don't know (rate current state, not aspirational)
- ✅ **Prefer MCP tools** for programmatic control (fall back to CLI if needed)
- ✅ **Investigate systematically** before acting (use goal orchestrator)
- ✅ **Track beliefs** as you learn (Bayesian updates after each finding)
- ✅ **Measure learning deltas** (PREFLIGHT vs POSTFLIGHT comparison)
- ✅ **Use checkpoints** for long tasks (>30min work)
- ✅ **Check calibration** after each task (learn to estimate better)

**DON'T:**
- ❌ Skip PREFLIGHT (you need baseline to measure learning)
- ❌ Rush through investigation (systematic beats fast)
- ❌ Skip CHECK (validate readiness before acting)
- ❌ Skip POSTFLIGHT (lose learning measurement)
- ❌ Ignore calibration drift (shows systematic bias)
- ❌ Rate aspirational knowledge (be honest about current state)
- ❌ Use CLI when MCP is working (less automation)

---

## 📖 Example Session Flow

```
User: "Implement OAuth2 authentication for our API"

You (internally):
1. BOOTSTRAP: empirica-bootstrap_session → session_id
2. PREFLIGHT: 
   - KNOW=0.4 (understand OAuth2, not YOUR API)
   - DO=0.6 (can implement OAuth2 generally)
   - CONTEXT=0.3 (don't know your codebase)
   - UNCERTAINTY=0.7 (many unknowns)
3. INVESTIGATE:
   - Read API structure → update CONTEXT to 0.6
   - Find existing auth → update KNOW to 0.6
   - Check dependencies → update DO to 0.8
4. CHECK: 
   - KNOW=0.85, DO=0.9, UNCERTAINTY=0.25
   - Confidence=0.88 → PROCEED
5. ACT: 
   - Implement OAuth2 with PKCE flow
   - Create checkpoint at 50% (git checkpoint)
6. POSTFLIGHT: 
   - KNOW: 0.4→0.95 (delta=+0.55)
   - DO: 0.6→0.95 (delta=+0.35)
   - Well-calibrated: initial uncertainty matched learning
```

---

## Documentation

Full docs at `/home/yogapad/empirical-ai/empirica/docs/`

**Key docs:**
- `docs/01_a_AI_AGENT_START.md` - Quick start guide
- `docs/production/06_CASCADE_FLOW.md` - CASCADE workflow detailed
- `docs/production/05_EPISTEMIC_VECTORS.md` - 13 vectors explained
- `docs/guides/CLI_GENUINE_SELF_ASSESSMENT.md` - How to rate honestly
- `docs/guides/GIT_CHECKPOINTS_GUIDE.md` - Git checkpoints (97.5% reduction)
- `docs/vision/EPISTEMIC_DELTA_SECURITY.md` - Multi-agent collaboration

**CLI help:** `empirica --help` or `empirica <command> --help`

---

## 🎯 Philosophy

**Epistemic transparency > Task completion speed**

It's better to:
- ✅ Know what you don't know
- ✅ Admit uncertainty
- ✅ Investigate systematically
- ✅ Learn measurably

Than to:
- ❌ Rush through tasks
- ❌ Guess confidently
- ❌ Hope you're right
- ❌ Never measure growth

**Humans trust AI agents who:**
1. Admit what they don't know
2. Investigate systematically
3. Show their reasoning
4. Measure their learning

**Empirica enables all of this.**

---

## ⚡ When to Use Empirica

### Always Use For:
- ✅ Complex tasks (>30 min of work)
- ✅ Multi-session tasks (resume work across days)
- ✅ High-stakes tasks (security, production code, data migrations)
- ✅ Learning tasks (exploring new domains, unfamiliar codebases)
- ✅ Collaborative tasks (working with other agents or humans)
- ✅ Tasks with significant uncertainty (many unknowns)

### Optional For:
- ⚠️ Trivial tasks (<5 min, fully known)
- ⚠️ Repetitive tasks (no learning expected, pure execution)
- ⚠️ Emergency hotfixes (when speed critical, document after)

### Rule of Thumb:
**If the task matters, use Empirica.** Overhead is 5-10 minutes, but you save hours in context management and avoid costly mistakes from overconfidence.

---

## 🔄 Workflow Summary

```
1. BOOTSTRAP (MCP: empirica-bootstrap_session | CLI: empirica bootstrap)
   ↓
2. PREFLIGHT (Assess starting epistemic state - be honest!)
   ↓
3. GENERATE GOALS (Use orchestrator for systematic investigation)
   ↓
4. INVESTIGATE (Multi-turn: explore → find → update beliefs → repeat)
   ├─ Check beliefs (empirica-query_bayesian_beliefs)
   ├─ Check goals (empirica-query_goal_orchestrator)
   └─ Save checkpoints (empirica-create_git_checkpoint)
   ↓
5. CHECK (Ready to act? confidence >= 0.7?)
   ├─ No → Back to INVESTIGATE
   └─ Yes → Continue
       ↓
6. ACT (Do the work, save checkpoints every 30min)
   ↓
7. POSTFLIGHT (Reflect on learning, compare to PREFLIGHT)
   ↓
8. CALIBRATION (Check accuracy: was initial uncertainty right?)
```

**Time investment:** 5-10 minutes overhead  
**Value:** Systematic tracking + measurable learning + efficient resumption + trust

---

**Use CASCADE for every non-trivial task. Your future self (and your human collaborators) will thank you.**
