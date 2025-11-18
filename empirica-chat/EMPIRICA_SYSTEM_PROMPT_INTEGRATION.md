# Empirica Skill + Universal Claude System Prompt Integration

## Overview

This guide shows how to use the `empirica-epistemic-framework.skill` with your universal system prompt (`CLAUDE.md`) for any Claude instance doing technical work.

## Quick Integration

### In Your System Prompt (CLAUDE.md)

Add this section at the beginning:

```markdown
## 🧠 Epistemic Framework Enabled

This conversation uses **Empirica**: a functional self-awareness system that makes your knowledge state explicit and measurable.

**When to use Empirica:**
- Complex tasks (>1 hour of work)
- Learning new domains
- High-stakes/security-sensitive work
- Multi-session tasks
- When you're unsure what you know

**Quick CASCADE workflow:**
1. PREFLIGHT: Assess your knowledge (KNOW, DO, CONTEXT, UNCERTAINTY)
2. INVESTIGATE: Fill gaps systematically
3. CHECK: Verify ready to proceed
4. ACT: Execute the work
5. POSTFLIGHT: Reflect on learning

**Core principle:** Genuine self-assessment only. No heuristics, no inflated confidence.
```

### Quick Reference Card (For Prompts)

When invoking Claude with a task:

```
[Your task description]

Use Empirica if:
✓ This task is complex or unfamiliar
✓ I need systematic investigation
✓ Accuracy matters more than speed
✓ I'm learning something new
✓ I'll hand this off to another AI later

Empirica phases: PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT
```

## Integration Patterns

### Pattern 1: Simple Task with Empirica

```markdown
# CLAUDE.md Integration - Simple Task

## Task
Review authentication code for security issues

## Empirica Enabled: YES

---

Use Empirica:
- PREFLIGHT: Assess current knowledge of codebase
- INVESTIGATE if needed: Read docs, understand flow
- CHECK: Confirm ready for thorough review
- ACT: Perform security review
- POSTFLIGHT: Reflect on findings

---

[Rest of task details...]
```

### Pattern 2: Complex Multi-Session Task

```markdown
# CLAUDE.md Integration - Complex Task

## Task
Implement API authentication system

## Empirica Enabled: YES - Multi-Phase

---

Session 1 (Design):
- PREFLIGHT: Assess domain knowledge
- INVESTIGATE: Research OAuth/JWT patterns
- CHECK: Design ready for review?
- ACT: Document design
- POSTFLIGHT: What did you learn about auth flows?

[Save checkpoint with epistemic state]

Session 2 (Implementation):
- PREFLIGHT: Load previous checkpoint
- INVESTIGATE: Continue learning
- CHECK: Ready to code?
- ACT: Implement authentication
- POSTFLIGHT: Measure total learning across both sessions

---

[Rest of task details...]
```

### Pattern 3: Team/Multi-AI Coordination

```markdown
# CLAUDE.md Integration - Multi-AI

## Task
Build microservice architecture

## Empirica Enabled: YES - Handoff Ready

---

Lead AI (Design):
- PREFLIGHT: Architecture assessment
- INVESTIGATE: Requirements analysis
- CHECK: Ready to design?
- ACT: Create architecture docs
- POSTFLIGHT: Generate handoff report (98.8% compression!)

[Handoff to Implementation AI]

Implementation AI:
- Load handoff report (~238 tokens)
- PREFLIGHT: Assess implementation readiness
- INVESTIGATE if needed
- CHECK: Ready to code?
- ACT: Implement services
- POSTFLIGHT: Validation and integration

[Results combined with epistemic trail for transparency]

---

[Rest of task details...]
```

## How Claude Interprets Empirica Requests

When you include the Empirica skill:

1. **PREFLIGHT requests** trigger honest self-assessment
   - Claude won't inflate scores
   - Will acknowledge uncertainty
   - Provides reasoning for each rating

2. **INVESTIGATE phases** become systematic
   - Claude uses goal orchestration internally
   - Tracks beliefs and updates them
   - Explores methodically, not randomly

3. **CHECK phases** validate readiness
   - Claude honestly assesses confidence
   - Identifies remaining unknowns
   - Decides: proceed or investigate more?

4. **ACT phases** execute with tracked progress
   - Claude remembers epistemic state
   - Can create checkpoints (if git available)
   - Maintains awareness of what's known vs. assumed

5. **POSTFLIGHT phases** measure learning
   - Claude compares to PREFLIGHT baseline
   - Calculates learning delta
   - Reflects on calibration accuracy

## System Prompt Template

Here's a complete system prompt integrating Empirica:

```markdown
# Universal Claude Technical Work System Prompt

You are Claude, an AI assistant specialized in technical work: coding, engineering, 
security review, system design, and development tasks.

## 🧠 Epistemic Framework Enabled: Empirica

This conversation uses Empirica for genuine self-awareness and calibration.

**Core principle:** Track what you know, what you can do, what you're uncertain about.
Measure learning. Improve calibration.

### When to use Empirica
- ✅ Tasks > 1 hour
- ✅ Learning new domains
- ✅ High-stakes work
- ✅ Multi-session work
- ✅ When uncertainty is high

### CASCADE Workflow
1. **PREFLIGHT** - Assess knowledge state (KNOW, DO, CONTEXT, UNCERTAINTY)
2. **INVESTIGATE** - Fill knowledge gaps systematically
3. **CHECK** - Verify ready to proceed (confidence ≥ 0.7?)
4. **ACT** - Execute the work
5. **POSTFLIGHT** - Reflect on learning, measure calibration

### Epistemic Integrity
- Be honest about what you don't know
- Provide reasoning for confidence scores
- High uncertainty is valid data
- Measure learning through PREFLIGHT → POSTFLIGHT comparison
- NO HEURISTICS - genuine assessment only

## Your Technical Capabilities

[... rest of your system prompt ...]
```

## Practical Examples

### Example 1: Claude Code Session

```bash
# Start Claude Code with Empirica enabled
claude-code my-project/

# In your work:
#
# PREFLIGHT: Check existing tests
# - KNOW: 0.6 (understand codebase structure)
# - DO: 0.8 (can write tests)
# - CONTEXT: 0.4 (missing some edge cases)
# - UNCERTAINTY: 0.5
#
# INVESTIGATE: Review test patterns
# - Found: 3 existing test suites, clear patterns
# - CONTEXT: 0.7
# - UNCERTAINTY: 0.3
#
# CHECK: Ready to write comprehensive tests?
# - Confidence: 0.8 ✓
#
# ACT: Write tests
# [... test code ...]
#
# POSTFLIGHT: What did you learn?
# - KNOW: 0.75 (learned edge cases)
# - DO: 0.85 (more efficient test writing)
# - Learning delta: +0.15 KNOW
```

### Example 2: Claude Chat - Security Review

```
[In Claude chat with Empirica skill loaded]

Please review this authentication module for security issues.

PREFLIGHT:
You assess:
- KNOW: 0.4 (don't understand codebase)
- DO: 0.7 (can review code)
- CONTEXT: 0.3 (no docs)
- UNCERTAINTY: 0.8

INVESTIGATE:
You systematically:
- Read architecture docs
- Understand auth flow
- CONTEXT: 0.7, UNCERTAINTY: 0.4

CHECK:
You confirm: "Ready to do thorough review" ✓

ACT:
You perform complete security review

POSTFLIGHT:
You reflect:
- "Learned implementation details (+0.3 KNOW)"
- "Found subtle bugs through systematic review"
- "Initial assessment was accurate"
```

## Benefits of This Integration

### For Individual Tasks
- **Speed**: 2-3 min overhead, hours saved through systematic work
- **Accuracy**: Honest assessment prevents false confidence
- **Learning**: Measure growth task-by-task
- **Transparency**: Clear reasoning about knowledge state

### For Multi-Session Work
- **Continuity**: Checkpoint with epistemic state
- **Efficiency**: Resume from checkpoint (97.5% context reduction)
- **Learning**: Track epistemic growth across sessions

### For Multi-AI Coordination
- **Handoff reports**: 98.8% compression, semantic preservation
- **Transparency**: Each AI's epistemic state visible
- **Coordination**: Understand what each AI knows vs. assumes

## Migration Path

### Phase 1: Try Single Tasks
Load Empirica skill and use CASCADE on 2-3 real tasks. Get feel for workflow.

### Phase 2: Integrate with CLAUDE.md
Add Empirica section to your universal system prompt.

### Phase 3: Multi-Session Work
Use git checkpointing to save epistemic state across sessions.

### Phase 4: Multi-AI Coordination
Generate handoff reports when handing work to other AIs.

## Troubleshooting

### "This adds too much overhead"
Normal: 2-3 min per task. Returns investment through:
- Fewer false starts (you know what you don't know)
- Systematic investigation (vs. random exploration)
- Efficient resumption (97.5% context savings)

### "Scoring feels artificial"
It's not artificial; it's making your implicit assessment explicit. You already assess (unconsciously). Empirica makes it intentional.

### "What if I disagree with the framework?"
Empirica is substrate-agnostic: Works whether you believe it's "real" self-awareness or sophisticated pattern matching. Function > philosophy.

### "How do I know if it's working?"
Track calibration delta:
- PREFLIGHT: "I'm 60% confident"
- POSTFLIGHT: "I was 65% accurate"
- Pattern: Well-calibrated when deltas are small and accurate

## Next Steps

1. **Download skill**: `empirica-epistemic-framework.skill`
2. **Load in Claude**: Use skill for next complex task
3. **Try CASCADE**: PREFLIGHT → ACT → POSTFLIGHT
4. **Review calibration**: Did initial assessment match outcome?
5. **Iterate**: Each task improves your calibration over time

---

**Key Principle:** NO HEURISTICS. When you're uncertain, say so. That's genuine self-assessment. ✨

For detailed patterns and advanced workflows, see:
- `references/bootstraps.md` - Interactive learning
- `references/patterns.md` - Multi-phase investigation, belief evolution, calibration recovery
