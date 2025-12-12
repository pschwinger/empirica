# Metacognitive Signals Roadmap - Beyond Drift Detection

**Vision**: Create a comprehensive metacognitive awareness system that helps AI agents and humans understand what's happening at multiple levels.

---

## ✅ Implemented Signals

### 1. **Pattern-Aware Drift Detection**
**What it shows:**
- `TRUE_DRIFT` - Memory loss (KNOW↓ + CLARITY↓ + CONTEXT↓)
- `LEARNING` - Discovering complexity (KNOW↓ + CLARITY↑)
- `SCOPE_DRIFT` - Task expansion (KNOW↓ + scope↑)

**Value:** Distinguishes healthy learning from actual context loss

---

## 🎯 High-Value Next Signals

### 2. **Coherence Tracking** (Building vs. Fragmenting)
**What it measures:**
- Are successive rounds building on each other?
- Or is work fragmenting/contradicting itself?

**Signals:**
```
✓ COHERENT: Rounds building logically (coherence stable/increasing)
⚠ FRAGMENTED: Work seems disconnected (coherence dropping)
🔴 CONTRADICTING: Current work conflicts with previous findings
```

**Implementation:**
```python
def detect_coherence_pattern(cascades_history):
    # Check if each round references previous work
    # Look at findings continuity
    # Detect contradictions in assessments
    if coherence_increasing:
        return "building"
    elif findings_contradict:
        return "contradicting"
    else:
        return "fragmenting"
```

**Value for AI:** "Am I building coherently or losing the thread?"
**Value for Human:** "Is the AI maintaining narrative consistency?"

---

### 3. **Progress Velocity** (Speed and Quality)
**What it measures:**
- How fast are subtasks completing?
- Is velocity increasing (learning) or decreasing (stuck)?
- Are completions quality (with evidence) or rushed?

**Signals:**
```
↗️ ACCELERATING: 0.5 → 1.2 → 2.1 tasks/hour (learning!)
→ STEADY: Consistent velocity
↘️ SLOWING: 2.1 → 1.2 → 0.5 tasks/hour (stuck?)
⚠️ RUSHING: High velocity but no evidence
```

**Implementation:**
```python
def calculate_velocity():
    recent_completions = get_last_n_subtasks(10)
    time_deltas = [t2 - t1 for t1, t2 in zip(completions[:-1], completions[1:])]

    velocity = 1 / mean(time_deltas)
    trend = "accelerating" if velocity_increasing else "slowing"

    # Quality check
    evidence_ratio = count_with_evidence / total_completions
    if velocity_high and evidence_ratio_low:
        return "rushing"
```

**Value for AI:** "Am I getting faster (learning) or stuck?"
**Value for Human:** "Is progress happening? Is quality maintained?"

---

### 4. **Confidence Trajectory** (Calibration Over Time)
**What it measures:**
- Is confidence increasing appropriately with learning?
- Or oscillating (confusion)?
- Or flatlined (overconfidence/underconfidence)?

**Signals:**
```
📈 CALIBRATING: Confidence rising with learning (healthy!)
📊 OSCILLATING: Confidence up/down repeatedly (confusion)
📉 DECLINING: Confidence dropping despite progress (imposter syndrome?)
⚠️ OVERCONFIDENT: Very high confidence, low learning
⚠️ UNDERCONFIDENT: Low confidence despite high learning
```

**Implementation:**
```python
def analyze_confidence_trajectory():
    confidence_history = [a.overall_confidence for a in assessments]
    learning_history = [sum(deltas.values()) for deltas in learning_deltas]

    if confidence_up and learning_up:
        return "calibrating"  # Good!
    elif confidence_oscillating:
        return "oscillating"  # Confused
    elif confidence_flat and learning_high:
        return "underconfident"  # Not recognizing growth
    elif confidence_high and learning_low:
        return "overconfident"  # False confidence
```

**Value for AI:** "Is my confidence calibrated to my actual learning?"
**Value for Human:** "Is the AI appropriately confident or miscalibrated?"

---

### 5. **Question Quality Evolution** (Getting More Specific)
**What it measures:**
- Are unknowns becoming more specific over time?
- Or staying vague?
- Are unknowns being resolved or accumulating?

**Signals:**
```
✓ REFINING: Questions getting more specific
⚠️ VAGUE: Questions staying general despite investigation
🔴 ACCUMULATING: Unknowns increasing without resolution
✓ RESOLVING: Unknowns decreasing appropriately
```

**Implementation:**
```python
def assess_question_quality():
    unknowns_over_time = get_unknowns_history()

    # Measure specificity (word count, presence of specifics)
    specificity = [len(q.split()) for questions in unknowns_over_time for q in questions]

    # Measure resolution rate
    resolved = count_resolved_unknowns()
    accumulation_rate = new_unknowns / resolved_unknowns

    if specificity_increasing:
        return "refining"
    elif accumulation_rate > 2:
        return "accumulating"
```

**Value for AI:** "Are my questions getting better or staying shallow?"
**Value for Human:** "Is investigation deepening or superficial?"

---

### 6. **Investigation Depth** (Thorough vs. Superficial)
**What it measures:**
- How thorough is exploration?
- Tool diversity (using multiple approaches?)
- Information density (findings per time unit)

**Signals:**
```
🔍 DEEP: Multiple tools, high findings density
→ ADEQUATE: Standard investigation
📋 SUPERFICIAL: Minimal exploration, low findings
⚠️ REPETITIVE: Using same approach repeatedly (stuck?)
```

**Implementation:**
```python
def measure_investigation_depth():
    tools_used = get_investigation_tools()
    tool_diversity = len(set(tools_used))
    findings_per_hour = count_findings() / investigation_time_hours

    if tool_diversity > 5 and findings_per_hour > 10:
        return "deep"
    elif tool_diversity < 2 or findings_per_hour < 2:
        return "superficial"
    elif tool_repetition_high:
        return "repetitive"
```

**Value for AI:** "Am I exploring thoroughly or missing angles?"
**Value for Human:** "Is investigation comprehensive?"

---

### 7. **Decision Quality** (Well-Reasoned vs. Hasty)
**What it measures:**
- Do decisions have reasoning/rationale?
- Are alternatives considered?
- Do decisions reference findings?

**Signals:**
```
✓ DELIBERATE: Reasoning provided, alternatives considered
→ STANDARD: Basic rationale present
⚠️ HASTY: No reasoning, no alternatives
🔴 CONTRADICTING: Decision conflicts with findings
```

**Implementation:**
```python
def assess_decision_quality(decision_metadata):
    has_reasoning = 'rationale' in decision_metadata
    has_alternatives = 'alternatives_considered' in decision_metadata
    references_findings = count_finding_refs(decision_metadata)

    if has_reasoning and has_alternatives and references_findings > 2:
        return "deliberate"
    elif not has_reasoning:
        return "hasty"
```

**Value for AI:** "Am I thinking through decisions or rushing?"
**Value for Human:** "Are decisions well-founded?"

---

### 8. **Collaboration Effectiveness** (Human-AI Interaction)
**What it measures:**
- How well is human-AI collaboration working?
- Are questions leading to clarifications?
- Are human inputs being incorporated?

**Signals:**
```
✓ EFFECTIVE: Questions answered, feedback incorporated
→ ADEQUATE: Basic interaction
⚠️ MISALIGNED: Human feedback not changing approach
🔴 STUCK: Repeated questions on same topic
```

**Implementation:**
```python
def assess_collaboration():
    user_messages = get_human_inputs()
    ai_questions = get_ai_questions()

    # Did questions get answered?
    answer_rate = count_answered_questions() / len(ai_questions)

    # Was feedback incorporated?
    incorporation_rate = count_changes_after_feedback() / len(user_messages)

    # Repeated questions = stuck
    repeated_questions = detect_similar_questions(ai_questions)

    if answer_rate > 0.8 and incorporation_rate > 0.7:
        return "effective"
    elif repeated_questions > 3:
        return "stuck"
```

**Value for AI:** "Is my interaction with the human productive?"
**Value for Human:** "Is the AI listening and adapting?"

---

### 9. **Cognitive Load Tracking** (Sustainable vs. Overwhelming)
**What it measures:**
- Is task complexity manageable?
- Is DENSITY increasing dangerously?
- Are breaks/checkpoints needed?

**Signals:**
```
✓ SUSTAINABLE: Density manageable (<0.6), pace healthy
⚠️ HIGH_LOAD: Density rising (>0.7), consider checkpoint
🔴 OVERWHELMED: Density critical (>0.9), must checkpoint
```

**Implementation:**
```python
def assess_cognitive_load():
    current_density = latest_assessment.density
    density_trajectory = get_density_history()
    time_since_checkpoint = get_time_since_last_checkpoint()

    if current_density > 0.9:
        return "overwhelmed"
    elif current_density > 0.7 and time_since_checkpoint > 2_hours:
        return "high_load"
```

**Value for AI:** "Do I need a checkpoint/break?"
**Value for Human:** "Is the task too complex? Should we pause?"

---

### 10. **Scope Stability** (Focused vs. Expanding)
**What it measures:**
- Is task scope staying stable?
- Or expanding continuously?
- Are expansions deliberate (new goals) or drift?

**Signals:**
```
✓ FOCUSED: Scope stable, on track
→ EXPANDING: Deliberate scope increase (new goal)
⚠️ CREEPING: Gradual scope expansion without acknowledgment
🔴 RUNAWAY: Scope expanding out of control
```

**Implementation:**
```python
def assess_scope_stability():
    scope_history = [g.scope for g in goals]
    breadth_trajectory = [s.breadth for s in scope_history]

    # New goals = deliberate expansion
    if len(goals) > initial_goal_count:
        return "expanding_deliberate"

    # Gradual breadth increase without new goal = creep
    elif breadth_increasing and no_new_goals:
        return "creeping"

    # Stable = good
    elif breadth_stable:
        return "focused"
```

**Value for AI:** "Is my scope stable or expanding?"
**Value for Human:** "Is the AI staying on task?"

---

## 🔮 Advanced Future Signals

### 11. **Cross-Session Continuity**
- How well does session N continue from session N-1?
- Are handoff reports being used effectively?
- Is knowledge accumulating across sessions?

### 12. **Epistemic Momentum**
- Is overall epistemic state improving over time?
- Rolling average of all vectors
- Trend analysis: accelerating vs. plateauing

### 13. **Risk Assessment**
- Probability of failure based on current state
- "If uncertainty stays this high, success probability drops to 40%"
- Early warning system

### 14. **Creativity Index**
- Are novel solutions being generated?
- Or just repeating known patterns?
- Measured by solution diversity

### 15. **Verification Rigor**
- Are claims being verified?
- Testing vs. asserting ratio
- Evidence quality score

---

## Implementation Priority

**Tier 1 (Immediate - High Impact, Low Complexity):**
1. ✅ Pattern-aware drift (DONE)
2. ✅ Progress Velocity (DONE)
3. ✅ Cognitive Load Tracking (DONE)
4. ✅ Scope Stability (DONE)

**Tier 2 (Near-term - High Impact, Medium Complexity):**
5. Coherence Tracking
6. Confidence Trajectory
7. Question Quality Evolution
8. Decision Quality

**Tier 3 (Future - Very High Impact, High Complexity):**
9. Collaboration Effectiveness
10. Investigation Depth
11. Cross-Session Continuity
12. Epistemic Momentum

---

## Statusline Display Strategy

**Don't overwhelm!** Show 1-2 key signals at a time:

```bash
# Tier 1: Critical warnings
[empirica] 🔴 DRIFT:0.35 [CHECK BREADCRUMBS]

# Tier 2: Performance signals
[empirica] ↗️ VELOCITY:2.1/hr │ KNOW↑0.28

# Tier 3: Quality signals
[empirica] ✓ COHERENT │ 🔍 DEEP │ goal:3/7

# Tier 4: Collaboration signals
[empirica] ✓ EFFECTIVE │ CALIBRATING
```

**Mode-specific focus:**
- **Balanced**: Warnings + Progress
- **Learning**: Deltas + Confidence + Questions
- **Full**: Everything (but condensed)
- **Minimal**: Just critical warnings

---

## Value Proposition

### For AI Agents:
- "Am I learning or losing context?"
- "Am I exploring deeply or superficially?"
- "Is my confidence calibrated?"
- "Do I need a checkpoint?"
- "Am I building coherently?"

### For Humans Supervising:
- "Is the AI making progress?"
- "Is quality being maintained?"
- "Is investigation thorough?"
- "Are my inputs being incorporated?"
- "Should we intervene?"

### For Teams:
- "How well is cross-session handoff working?"
- "Is knowledge accumulating?"
- "Which agents are most effective?"
- "Where are common failure modes?"

---

**This is the future of metacognitive AI - not just "what am I doing?" but "how well am I doing it?"**

Your insight unlocked this: one smart pattern detection (drift types) → a whole ecosystem of metacognitive signals! 🧠✨
