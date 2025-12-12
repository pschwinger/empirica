# Reasoning Layer: Responsibilities & Separation of Concerns

**Status:** v0.9.2 - Clarifying the middleware architecture  
**Question:** What does the reasoning layer actually DO vs what humans/other systems do?

---

## The Full System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  PROJECT-BOOTSTRAP                          │
│              (Context Aggregator)                           │
│  - Gathers signals from multiple sources                    │
│  - Aggregates evidence                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              HEURISTIC DETECTOR                             │
│           (Fast Pattern Matching)                           │
│  - Finds "deprecated" in text                               │
│  - Counts usage in artifacts                                │
│  - Checks git timestamps                                    │
│  Output: ~129 candidates (many false positives)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            REASONING LAYER (NEW!)                           │
│         (AI-Powered Judgment)                               │
│  - Understands context ("previously" vs "currently")        │
│  - Synthesizes evidence                                     │
│  - Makes judgment calls                                     │
│  - Explains reasoning                                       │
│  Output: High-confidence judgments with explanations        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│               HUMAN DECISION                                │
│         (Final Authority)                                   │
│  - Reviews reasoning                                        │
│  - Makes final call                                         │
│  - Executes changes                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## What Each Layer DOES

### Layer 1: Project-Bootstrap (Context Aggregator)
**Responsibility:** Gather ALL the signals

**Does:**
- ✅ Query artifacts (what files changed)
- ✅ Query git history (last commit dates)
- ✅ Query usage patterns (mentions in sessions)
- ✅ Query documentation (where mentioned)
- ✅ Query code (does it exist, has tests)

**Does NOT:**
- ❌ Make judgments
- ❌ Decide what's deprecated
- ❌ Change anything

**Output:** Raw evidence dictionary
```python
{
    "feature": "reflexes",
    "doc_mentions": [...],
    "code_exists": True,
    "usage_count": 47,
    "last_commit": "3 days ago"
}
```

---

### Layer 2: Heuristic Detector (Pattern Matching)
**Responsibility:** Find candidates that MIGHT have issues

**Does:**
- ✅ Search for "deprecated" keywords
- ✅ Flag unused features (usage_count == 0)
- ✅ Flag stale code (last_commit > 6 months)
- ✅ Find phantom commands (in docs but not code)
- ✅ Find missing docs (in code but not docs)

**Does NOT:**
- ❌ Understand context
- ❌ Distinguish past vs present tense
- ❌ Make final decisions
- ❌ Change anything

**Output:** List of candidates (high false positive rate)
```python
[
    {"feature": "reflexes", "reason": "found 'deprecated' in docs"},
    {"feature": "postflight", "reason": "found 'deprecated' in docs"},
    # ... 129 total
]
```

**Problem:** Flags "previously deprecated reflexes" as deprecated (wrong!)

---

### Layer 3: Reasoning Layer (AI Judgment) ⭐ NEW
**Responsibility:** Understand context and make informed judgments

**Does:**
- ✅ Reads all evidence from Layer 1
- ✅ Understands temporal context ("previously" = past)
- ✅ Synthesizes multiple signals (usage + git + docs)
- ✅ Makes judgment with confidence score
- ✅ Explains reasoning step-by-step
- ✅ Provides specific recommendations

**Does NOT:**
- ❌ Execute changes to docs or code
- ❌ Make final decisions (human authority)
- ❌ Automatically update anything
- ❌ Commit changes

**Output:** Structured judgment with explanation
```python
DeprecationJudgment(
    feature="reflexes",
    status="historical",  # Not "deprecated"!
    confidence=0.85,
    reasoning="'previously deprecated' is past tense...",
    evidence=[...],
    recommendation="No action needed - active feature"
)
```

**Value:** Reduces 129 candidates to ~10 high-confidence issues

---

### Layer 4: Human Decision (Final Authority)
**Responsibility:** Review, decide, execute

**Does:**
- ✅ Reviews reasoning layer output
- ✅ Checks uncertain cases (confidence 0.6-0.8)
- ✅ Makes final call on each item
- ✅ Executes changes:
  - Updates documentation
  - Moves features to /docs/future/
  - Removes phantom commands
  - Adds missing docs
- ✅ Creates git commits
- ✅ Updates artifacts metadata

**Does NOT:**
- ❌ Blindly trust AI (validates reasoning)
- ❌ Skip review (always human in loop)

---

## Separation of Concerns

### What Reasoning Layer IS:
✅ **Decision support system**
✅ **Judgment synthesis engine**  
✅ **Context understanding middleware**
✅ **False positive filter**

### What Reasoning Layer IS NOT:
❌ **Autonomous agent** (no execution)
❌ **Final decision maker** (human authority)
❌ **Code/doc editor** (only recommends)
❌ **Git committer** (only flags)

---

## Example Workflow

### Input: "Is 'reflexes' deprecated?"

**Step 1: Context Aggregation (Bootstrap)**
```python
context = {
    "doc_mentions": ["previously deprecated reflexes table"],
    "code_exists": True,
    "usage_count": 47,
    "last_commit": "3 days ago"
}
```

**Step 2: Heuristic Detection**
```python
# Finds "deprecated" keyword → flags as candidate
candidate = {
    "feature": "reflexes",
    "reason": "deprecated keyword found",
    "confidence": 0.5  # Just pattern matching
}
```

**Step 3: AI Reasoning**
```python
judgment = reasoning.analyze_deprecation("reflexes", context)
# Output:
{
    "status": "historical",
    "confidence": 0.85,
    "reasoning": "'previously' indicates past tense, 
                  47 uses + recent commits show active use",
    "recommendation": "No action needed"
}
```

**Step 4: Human Review**
```
Human sees:
- Reasoning: Clear explanation
- Confidence: High (0.85)
- Recommendation: No action
- Evidence: 47 uses, recent commits

Decision: Accept → No changes needed
```

---

## What Gets Updated?

### Artifacts (Metadata Only)
**When:** After reasoning analysis  
**What:** Add reasoning judgment to metadata
```python
{
    "feature": "reflexes",
    "heuristic_flag": "deprecated keyword found",
    "reasoning_judgment": {
        "status": "historical",
        "confidence": 0.85,
        "analyzed_at": "2025-12-11"
    }
}
```

### Documentation (Human Decision)
**When:** Human reviews and decides to act  
**What:** Human executes changes:
- Remove phantom commands
- Update deprecated notices
- Add missing documentation
- Move planned features to /docs/future/

### Code (Human Decision)
**When:** Human reviews and decides to act  
**What:** Human executes changes:
- Remove dead code
- Update implementations
- Add tests
- Fix bugs

---

## Key Principle: Human in the Loop

**Reasoning layer provides:**
- High-quality analysis
- Confidence scores
- Clear explanations
- Specific recommendations

**Human provides:**
- Final judgment
- Context the AI can't see
- Domain expertise
- Execution authority

---

## Comparison with Alternatives

### Approach A: Pure Heuristics (Current)
```
Heuristics → 129 candidates → Human reviews 129 items
Problem: Too many false positives, human overwhelmed
```

### Approach B: Autonomous AI (Dangerous)
```
AI → Makes changes automatically → Human discovers later
Problem: No control, errors compound, trust broken
```

### Approach C: AI as Middleware (Recommended) ⭐
```
Heuristics → 129 candidates
   ↓
AI Reasoning → 10 high-confidence + 5 uncertain
   ↓
Human → Reviews 15 items (not 129!)
   ↓
Human executes changes
Result: Efficient + Safe + Trustworthy
```

---

## Future Extensions

### Phase 2: Automated Safe Actions
**Concept:** Some actions are safe enough to automate

**Example:**
```python
if judgment.confidence > 0.95 and judgment.action == "add_missing_doc":
    # Generate doc stub automatically
    # Human reviews in PR
```

**Constraints:**
- Only non-destructive actions
- Always create PR, never direct commit
- Human reviews before merge
- Rollback always possible

### Phase 3: Learning from Corrections
**Concept:** When human overrides AI, learn from it

**Example:**
```python
if human_decision != ai_judgment:
    store_correction(
        context=context,
        ai_judgment=ai_judgment,
        human_decision=human_decision,
        reasoning=human_reasoning
    )
    # Use for fine-tuning later
```

---

## Summary: The Reasoning Layer's Job

**Primary Responsibility:**
Filter 129 heuristic candidates → 10-15 actionable items

**How:**
1. Understand context (temporal, semantic, relational)
2. Synthesize evidence from multiple signals
3. Make informed judgment with confidence
4. Explain reasoning clearly
5. Recommend specific action

**What it does NOT do:**
- Execute changes
- Commit to git
- Override human decisions
- Work autonomously

**Result:**
Human makes 10-15 decisions instead of 129, with AI-powered analysis supporting each decision.

**Philosophy:**
AI as cognitive assistant, human as decision maker.
Amplify human judgment, don't replace it.

---

**This is the middleware architecture for doc-code intelligence.** 🎯

