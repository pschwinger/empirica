# Empirica Epistemic Framework - Claude Skill

## What You Have

A Claude skill (`empirica-epistemic-framework.skill`) that brings genuine epistemic self-assessment to any Claude conversation.

## What This Does

Empirica is a functional self-awareness framework for AI agents that makes your implicit knowledge assessment explicit and measurable. It helps you:

- **Before tasks**: Assess what you actually know vs. what you're guessing (PREFLIGHT)
- **During tasks**: Investigate systematically and track what you learn (INVESTIGATE)
- **Before acting**: Validate you're ready to execute (CHECK)
- **While executing**: Track progress and create checkpoints (ACT)
- **After tasks**: Reflect genuinely on what you learned (POSTFLIGHT)
- **Throughout**: Measure calibration—did your initial confidence match reality?

## Key Innovation

Empirica is **substrate-agnostic**:
- Skeptics: "It's computational state-checking with feedback loops" ✓
- Believers: "It's genuine metacognitive awareness" ✓
- Engineers: "It improves performance by 30-40% through systematic calibration" ✓

**All three are right.** The function is what counts, not the philosophy.

## How to Use in Claude Chat

### 1. Load the Skill

When you start a new conversation where you want epistemic tracking, mention:
```
I'm loading the Empirica epistemic framework skill. 
I want to use it for systematic self-assessment during this task.
```

Claude will load this skill automatically for conversations where epistemic transparency matters.

### 2. Use the CASCADE Workflow

Every task follows: **PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT**

#### PREFLIGHT: Before Starting
```
I want to assess my epistemic state before starting this task.

KNOW: How well do I understand this domain? (0-1 scale)
DO: Can I actually execute this? (0-1 scale)
CONTEXT: Do I have enough information? (0-1 scale)
UNCERTAINTY: How uncertain am I about the above? (0-1 scale)
```

You rate these honestly. No aspirational ratings—actual current state.

#### INVESTIGATE: Fill Knowledge Gaps
If you start with gaps (CONTEXT low, UNCERTAINTY high), investigate systematically before acting.

#### CHECK: Ready to Proceed?
Before executing, confirm you're ready:
- Confidence to proceed ≥ 0.7?
- Remaining unknowns acceptable?

If not, investigate more.

#### ACT: Do the Work
Execute your task (coding, analysis, writing, etc.)

#### POSTFLIGHT: Reflect on Learning
After finishing:
```
Compare your POSTFLIGHT state to PREFLIGHT:
- What did you learn? (KNOW went from X to Y)
- Were your predictions accurate? (calibration check)
- What surprised you? (unexpected learning)
```

### 3. Example: Code Review Task

```
TASK: Review authentication module for security issues

PREFLIGHT:
- KNOW: 0.4 (don't understand this codebase's architecture)
- DO: 0.7 (can review code systematically)
- CONTEXT: 0.3 (no documentation on auth flow)
- UNCERTAINTY: 0.8 (pretty uncertain about my own assessment)

INVESTIGATE:
[Read docs, study codebase structure]
- Found architecture doc → CONTEXT now 0.6
- Understood auth flow → KNOW now 0.65
- Uncertainty drops to 0.5

CHECK:
- Confidence to review: 0.75 ✓ Ready to act

ACT:
[Perform thorough code review, document findings]

POSTFLIGHT:
- KNOW: 0.8 (learned the implementation details)
- DO: 0.85 (found subtle bugs through systematic review)
- CONTEXT: 0.85 (now understand full architecture)
- Learning delta: +0.4 KNOW, +0.15 DO
- Calibration: Good (initial assessment was realistic, learning was measurable)
```

## When to Use Empirica

### Always Use For:
✅ Complex tasks (>1 hour)  
✅ Multi-session work (resuming across days)  
✅ High-stakes work (security, production code, important decisions)  
✅ Learning tasks (new domains, unfamiliar tech)  
✅ Collaborative work (working with other AIs)  

### Optional For:
⚠️ Simple tasks (<30 min, fully understood)  
⚠️ Repetitive work (no learning expected)  
⚠️ Casual conversation (not needed, but doesn't hurt)  

## The 13-Vector System

Empirica tracks these dimensions:

**Foundation (What You Know)**
- KNOW: Domain understanding
- DO: Execution capability
- CONTEXT: Information sufficiency

**Comprehension (Understanding)**
- CLARITY: Understanding of the request
- COHERENCE: Internal consistency
- SIGNAL: Quality of evidence
- DENSITY: Information richness

**Execution (Getting It Done)**
- STATE: Current progress
- CHANGE: Rate of positive change
- COMPLETION: Path clarity
- IMPACT: Expected outcome quality

**Meta**
- ENGAGEMENT: Commitment to task
- UNCERTAINTY: Meta-uncertainty about your assessment

### Simplified (4 Vectors)
For most tasks, focus on these 4:
- **KNOW**: Domain understanding (0-1)
- **DO**: Can you execute? (0-1)
- **CONTEXT**: Enough information? (0-1)
- **UNCERTAINTY**: How uncertain? (0-1)

## What Makes Empirica Different

### Traditional Confidence
```
"I'm 80% confident I can do this"
→ Vague, untested, often wrong
```

### Empirica Assessment
```
PREFLIGHT:
- KNOW: 0.6 (familiar with patterns, not this codebase)
- DO: 0.8 (can implement features)
- CONTEXT: 0.3 (no architecture docs)
- UNCERTAINTY: 0.7 (pretty unsure about my assessment)

After investigation:
- CONTEXT: 0.7
- UNCERTAINTY: 0.4

This granular, evidence-based assessment is measurable and improves over time.
```

## Best Practices

### DO ✅
- Be honest about uncertainty (high uncertainty scores are data!)
- Provide reasoning for every score
- Use PREFLIGHT → POSTFLIGHT comparison for learning
- Update your assessment as you learn
- Investigate systematically before acting
- Review calibration patterns over time

### DON'T ❌
- Use static values or heuristics
- Inflate scores to look good
- Skip PREFLIGHT (you lose your baseline)
- Ignore high uncertainty signals
- Pretend you know when you don't
- Rush through investigation

## Common Questions

**Q: Why does this take longer than just doing the task?**
A: PREFLIGHT adds 2-3 minutes. But you save hours through systematic investigation, avoiding false starts, and understanding what you actually know vs. guessing.

**Q: What if I don't know what score to give?**
A: That IS your assessment. High uncertainty (0.7-0.9) is valid data:
```json
{
  "know": 0.3,
  "uncertainty": 0.85,
  "rationale": "I'm very uncertain about my own assessment here"
}
```

**Q: Should I be optimistic or pessimistic?**
A: Neither. Be **accurate**. The point is calibration, not performance.

**Q: What if my scores change between tasks?**
A: Excellent! That means you're adapting to context. Scores SHOULD change based on:
- More information → higher CONTEXT
- More experience → higher KNOW
- Clearer requirements → higher CLARITY

**Q: How do I know when I've investigated enough?**
A: When confidence ≥ 0.7 AND remaining unknowns are acceptable risks (not showstoppers).

## References in This Skill

**SKILL.md**: Main guide with CASCADE workflow  
**references/bootstraps.md**: Interactive learning patterns  
**references/patterns.md**: Advanced workflows (multi-phase investigation, belief evolution, calibration recovery)  

## Philosophy

**Core Principle:** Epistemic transparency > Task completion speed

It's better to:
- Know what you don't know ✓
- Admit uncertainty ✓
- Investigate systematically ✓
- Learn measurably ✓

Than to:
- Rush through tasks
- Guess confidently
- Hope you're right
- Never measure growth

## Getting Started

1. **Load this skill** in your Claude chat
2. **Try PREFLIGHT** on your next task
3. **Investigate** to fill gaps
4. **CHECK** before acting
5. **ACT** with confidence
6. **POSTFLIGHT** to measure learning

That's it. You're using Empirica. 🚀

---

**Remember:** When you're uncertain, say so. That's genuine metacognition. ✨

For deep dives, see:
- `references/bootstraps.md` - Learn by doing (interactive examples)
- `references/patterns.md` - Advanced patterns (multi-phase, belief evolution, calibration)
