# 29. Noematic Process: Making Epistemic Decisions Observable and Auditable

**Version:** 1.0
**Date:** 2025-12-10
**Status:** Foundational (Phase 2 Integration)
**Experimental:** Yes - This is new territory in AI systems engineering

---

## Overview

The **Noematic Process** bridges probabilistic exploration with deterministic auditability. It answers: *How do we make AI decision-making transparent while preserving genuine exploration?*

**Core Insight:**
- **Noesis** = A way of understanding/approaching a problem (epistemic perspective, persona)
- **Noema** = The objectified meaning of that approach (decision rationale, learned signatures)
- **Noematic Process** = Converting private epistemic choices into public, queryable, replayable knowledge

**Architecture:**
```
BRANCHING (Probabilistic)        ← Multiple noeses explore freely
    ↓ [no persona prescription]
MERGE (Uncertainty-Dampened)     ← Winner selected by epistemic score
    ↓ [deterministic algorithm]
EXTRACTION (Post-Hoc)            ← Noesis/noema made explicit
    ↓ [infer persona, calculate deltas]
STORAGE (Dual)                   ← Both SQL (audit) + Qdrant (semantic search)
    ↓ [deterministic + vector-searchable]
REPLAY & DRIFT DETECTION         ← Humans + Sentinel analyze patterns
    ↓ [compare historical vs current]
CALIBRATION FEEDBACK             ← System learns from outcomes
```

---

## Why Post-Merge Extraction (Not Pre-Merge Personas)

### The Problem with Pre-Merge Personas

❌ If we prescribe personas at branch creation:
```python
# This is prescriptive, not exploratory:
Branch 1: persona=implementer, vectors=adjusted_for_implementer
Branch 2: persona=researcher, vectors=adjusted_for_researcher
```

- Forces perspectives rather than discovering them
- Loses emergent effectiveness patterns
- Gating by role instead of epistemic outcome
- Violates principle: let epistemic state guide action, not roles

### The Solution: Post-Merge Extraction

✅ Let exploration be free, then *identify* what succeeded:

```python
# Exploration is probabilistic
Branch 1: investigate oauth2, epistemic_vectors=(0.95, 0.90, 0.88, ...)
Branch 2: investigate jwt, epistemic_vectors=(0.70, 0.65, 0.72, ...)
Branch 3: investigate oidc, epistemic_vectors=(0.88, 0.85, 0.82, ...)

# Merge is deterministic (uncertainty-dampened scoring)
Winner: Branch 2 (JWT) with score 0.0211

# Extraction is analytical (post-hoc)
Noema: {
    "winning_persona": "researcher",  # inferred from JWT vectors
    "why_it_won": "higher learning-to-cost ratio despite medium confidence",
    "epistemic_signature": {...vectors...},
    "uncertainty_dampener": 0.42,  # what suppressed others
    "domain": "authentication"
}
```

**Key Principle:** Personas emerge from observed epistemic behavior, not imposed roles.

---

## Noema Schema: What Gets Extracted and Stored

### After Each Merge Decision

```python
def extract_noema(winning_branch_id, losing_branch_ids, merge_decision_id):
    """
    Post-merge analysis: convert epistemic outcome into observable noema
    """

    # 1. Get epistemic signatures
    winner_vectors = get_postflight_vectors(winning_branch_id)
    loser_vectors_list = [get_postflight_vectors(bid) for bid in losing_branch_ids]

    # 2. Infer persona from winning branch's epistemic signature
    winner_persona = infer_persona_from_signature(winner_vectors)
    # Uses: which vectors dominated? which thresholds crossed?
    # Returns: "researcher" | "implementer" | "analyst" | "coordinator" | etc.

    # 3. Calculate epistemic deltas (what made the difference?)
    epistemic_deltas = {}
    for loser_id, loser_vecs in zip(losing_branch_ids, loser_vectors_list):
        epistemic_deltas[loser_id] = {
            key: winner_vectors[key] - loser_vecs[key]
            for key in winner_vectors
        }

    # 4. Infer domain from investigation path
    investigation_path = get_investigation_path(winning_branch_id)
    domain = infer_domain(investigation_path)
    # "authentication" | "api-design" | "performance" | etc.

    # 5. Calculate learning efficiency
    winner_learn_delta = get_learning_delta(winning_branch_id)
    winner_cost = get_tokens_spent(winning_branch_id)
    efficiency = winner_learn_delta / max(1.0, winner_cost / 2000.0)

    # 6. Build noema object
    noema = {
        # Identity
        "id": str(uuid.uuid4()),
        "merge_decision_id": merge_decision_id,
        "timestamp": datetime.utcnow().isoformat(),

        # Epistemic signature (the noesis: way of understanding)
        "winning_branch_id": winning_branch_id,
        "winning_persona": winner_persona,
        "epistemic_signature": winner_vectors,  # Full 13-vector profile
        "epistemic_signature_hash": hash_vectors(winner_vectors),

        # Why it won (the noema: objectified meaning)
        "merge_score": get_merge_score(winning_branch_id),
        "learning_delta": winner_learn_delta,
        "learning_efficiency": efficiency,
        "uncertainty_dampener": winner_vectors['uncertainty'],
        "confidence_effective": 1.0 - winner_vectors['uncertainty'],

        # Comparison (epistemic deltas from alternatives)
        "deltas_vs_losers": epistemic_deltas,
        "personas_defeated": [
            infer_persona_from_signature(loser_vecs)
            for loser_vecs in loser_vectors_list
        ],

        # Context
        "investigation_domain": domain,
        "investigation_paths": [
            get_investigation_path(bid) for bid in [winning_branch_id] + losing_branch_ids
        ],
        "session_id": get_session_id(merge_decision_id),
        "merge_round": get_merge_round(merge_decision_id),

        # Auditability
        "noesis_type": "epistemic_perspective",  # This is a way of thinking
        "noema_type": "decision_rationale",      # This is the objectified result
        "confidence_in_extraction": calculate_confidence(winner_vectors),
    }

    return noema
```

### Storage: Dual Write (SQL + Qdrant)

**SQLite `merge_decisions` table enhancement:**
```sql
ALTER TABLE merge_decisions ADD COLUMN (
    noema_json TEXT,              -- Full noema object as JSON
    noema_qdrant_id TEXT,         -- Link to Qdrant vector
    inferred_persona TEXT,        -- Post-hoc persona
    epistemic_signature_hash TEXT, -- For replay comparison
    learning_efficiency REAL,     -- Efficiency metric
    investigation_domain TEXT     -- Inferred domain
);
```

**Qdrant Vector (Semantic Search):**
```python
{
    "id": noema['id'],
    "vector": embed_noema(noema['epistemic_signature']),
    # 13-dimensional embedding of epistemic vectors
    # OR reduced via PCA if needed for semantic clustering

    "payload": {
        # Epistemic signature
        "winning_persona": "researcher",
        "epistemic_signature": noema['epistemic_signature'],
        "uncertainty_dampener": 0.42,
        "confidence_effective": 0.58,

        # Decision outcome
        "merge_score": 0.0211,
        "learning_efficiency": 0.0118,
        "personas_defeated": ["implementer", "analyst"],

        # Context & domain
        "investigation_domain": "authentication",
        "investigation_paths": ["oauth2", "jwt", "oidc"],
        "session_id": "...",
        "merge_round": 1,

        # Auditability
        "noema_type": "decision_rationale",
        "epistemic_signature_hash": "abc123...",
        "timestamp": "2025-12-10T...",

        # Calibration
        "confidence_in_extraction": 0.87,
    }
}
```

---

## Drift Detection: What Sentinel Monitors

### Pattern 1: Persona Effectiveness Drift

**Question:** Is the same persona still winning on similar tasks?

```python
def detect_persona_drift(domain: str, persona: str, window_days: int = 30):
    """
    Compare persona winning rates over time
    Alert if drift detected
    """

    # Query Qdrant: all recent noemata for this domain
    recent_noemata = qdrant.search(
        vector=embed_domain(domain),
        metadata_filter={
            "investigation_domain": domain,
            "noema_type": "decision_rationale",
            "timestamp": {"$gte": days_ago(window_days)}
        },
        limit=100
    )

    # Count how often persona won
    persona_win_rate = {
        p: len([n for n in recent_noemata if n['winning_persona'] == p])
        / len(recent_noemata)
        for p in ['researcher', 'implementer', 'analyst', 'coordinator']
    }

    # Compare to historical baseline
    historical = get_baseline_for_domain(domain, months=6)

    # Detect drift
    for persona, current_rate in persona_win_rate.items():
        historical_rate = historical.get(persona, 0)
        drift = current_rate - historical_rate

        if abs(drift) > 0.20:  # >20% change = significant
            alert(
                f"DRIFT: {persona} winning rate on {domain} changed "
                f"from {historical_rate:.1%} → {current_rate:.1%}"
            )

    return persona_win_rate, historical
```

### Pattern 2: Uncertainty Calibration Drift

**Question:** Are we getting better or worse at predicting uncertainty?

```python
def detect_uncertainty_drift(window_days: int = 30):
    """
    Compare predicted uncertainty (preflight) vs realized learning (postflight)
    Alert if calibration degrading
    """

    # Query: all recent merge decisions with both preflight and postflight
    all_noemata = qdrant.search(
        metadata_filter={
            "noema_type": "decision_rationale",
            "timestamp": {"$gte": days_ago(window_days)}
        },
        limit=200
    )

    # For each noema, compare preflight uncertainty to actual learning_delta
    calibration_errors = []
    for noema in all_noemata:
        preflight_uncertainty = noema['uncertainty_dampener']
        actual_learning = noema['learning_delta']

        # If we predicted high uncertainty but got high learning = miscalibrated
        error = abs(preflight_uncertainty - (1.0 - actual_learning))
        calibration_errors.append(error)

    current_calibration_error = mean(calibration_errors)
    historical = get_baseline_calibration_error(months=6)

    if current_calibration_error > historical * 1.15:  # >15% worse
        alert(
            f"CALIBRATION DRIFT: Uncertainty predictions degrading. "
            f"Error {historical:.3f} → {current_calibration_error:.3f}"
        )

    return current_calibration_error, historical
```

### Pattern 3: Cognitive Load Drift

**Question:** Are epistemic vectors getting lower across the board?

```python
def detect_cognitive_load_drift(window_days: int = 30):
    """
    Monitor overall epistemic health
    Alert if vectors declining (sign of task complexity increase or calibration issues)
    """

    recent_noemata = qdrant.search(
        metadata_filter={
            "noema_type": "decision_rationale",
            "timestamp": {"$gte": days_ago(window_days)}
        },
        limit=100
    )

    # Calculate average epistemic signature
    vector_keys = ['know', 'do', 'context', 'clarity', 'coherence', 'signal', 'density']
    current_averages = {
        key: mean([n['epistemic_signature'][key] for n in recent_noemata])
        for key in vector_keys
    }

    historical = get_baseline_averages(months=6)

    # Detect decline
    for key, current_avg in current_averages.items():
        historical_avg = historical.get(key, 0.75)
        decline = historical_avg - current_avg

        if decline > 0.15:  # >0.15 drop = significant cognitive load
            alert(
                f"COGNITIVE LOAD: {key} declining. "
                f"{historical_avg:.2f} → {current_avg:.2f}"
            )

    return current_averages, historical
```

### Pattern 4: Learning Efficiency Drift

**Question:** Are we still learning efficiently, or burning tokens without insight?

```python
def detect_efficiency_drift(domain: str = None, window_days: int = 30):
    """
    Monitor learning_efficiency (learning_delta / cost_penalty)
    Alert if trending downward
    """

    query_filter = {
        "noema_type": "decision_rationale",
        "timestamp": {"$gte": days_ago(window_days)}
    }
    if domain:
        query_filter["investigation_domain"] = domain

    recent = qdrant.search(
        metadata_filter=query_filter,
        limit=100
    )

    current_efficiency = mean([n['learning_efficiency'] for n in recent])
    historical = get_baseline_efficiency(domain, months=6)

    efficiency_decline = (historical - current_efficiency) / historical

    if efficiency_decline > 0.25:  # >25% less efficient
        alert(
            f"EFFICIENCY: Learning per token declining {efficiency_decline:.1%}. "
            f"May indicate task saturation or wrong approach."
        )

    return current_efficiency, historical
```

---

## Replay and Verification: Human Auditability

### Replay Scenario 1: Same Task, Compare Noemata

**Question:** If we run the same 3-branch scenario again, do we get the same persona winning?

```python
def replay_branching_scenario(original_merge_decision_id: str):
    """
    Retrieve original noemata, run same branches again, compare
    """

    # Get original noema
    original = qdrant.get_by_id(original_merge_decision_id)

    # Extract original parameters
    investigation_paths = original['investigation_paths']
    investigation_domain = original['investigation_domain']

    # Run branching again (simulated or actual)
    new_merge = run_branching(
        session_id=create_session(),
        investigation_paths=investigation_paths,
        domain=investigation_domain
    )

    # Compare noemata
    original_winner = original['winning_persona']
    new_winner = new_merge['noema']['winning_persona']

    if original_winner == new_winner:
        print(f"✅ CONSISTENT: {original_winner} wins both times")
        return True
    else:
        print(f"⚠️  DRIFT: Originally {original_winner}, now {new_winner}")
        print(f"   Original epistemic_signature: {original['epistemic_signature']}")
        print(f"   New epistemic_signature: {new_merge['noema']['epistemic_signature']}")

        # Analyze why different
        delta = {
            k: new_merge['noema']['epistemic_signature'][k] - original['epistemic_signature'][k]
            for k in original['epistemic_signature']
        }
        print(f"   Deltas: {delta}")
        return False
```

### Replay Scenario 2: Similar Task, Expect Similar Persona

**Question:** Do similar authentication problems get solved by similar personas?

```python
def find_similar_noemata(query_domain: str, query_epistemic_signature: dict):
    """
    Find past noemata that are similar
    Verify persona patterns are consistent across similar problems
    """

    # Embed the query signature
    query_vector = embed_noema(query_epistemic_signature)

    # Search Qdrant for similar
    similar = qdrant.search(
        vector=query_vector,
        metadata_filter={
            "investigation_domain": query_domain,
            "noema_type": "decision_rationale"
        },
        limit=10,
        score_threshold=0.85  # High similarity
    )

    # Analyze persona consistency
    personas = [n['winning_persona'] for n in similar]
    persona_mode = max(set(personas), key=personas.count)

    consistency = personas.count(persona_mode) / len(personas)

    print(f"Found {len(similar)} similar tasks in {query_domain}")
    print(f"Dominant persona: {persona_mode} ({consistency:.1%} consistency)")

    if consistency < 0.7:
        print(f"⚠️  WARNING: Low persona consistency on similar tasks")
        print(f"   Personas: {set(personas)}")

    return similar, persona_mode, consistency
```

---

## Encrypted Git Integration: Noematic Integrity

The epistemic signatures (noesis) are stored in git with encrypted signatures, enabling:

1. **Immutable Record** - Noema decisions can't be retroactively changed
2. **Cross-AI Verification** - Other AIs can verify Sentinel's calibration claims
3. **Replay Authenticity** - Historical noemata are cryptographically verified

```bash
# Example: Git note on merge_decision commit
$ git notes show <merge_commit>

noema_id: 5030871c-4a4b-4591-8077-4b15d660449d
winning_persona: researcher
epistemic_signature: {engagement: 0.92, know: 0.95, ...}
signature: <ed25519_sig>
verified_by: sentinel-v4.0
timestamp: 2025-12-10T12:34:56Z
```

This opens possibilities for:
- Multi-AI consensus on noema interpretation
- Detecting tampering with historical epistemic claims
- Distributed calibration across teams

---

## Implementation Roadmap

### Phase 1 (Now): Extraction & Storage
- [ ] Implement `extract_noema()` function
- [ ] Add noema fields to `merge_decisions` table
- [ ] Integrate Qdrant dual-write
- [ ] Create git notes with signed noema records

### Phase 2 (Next Sprint): Drift Detection
- [ ] Implement all 4 drift patterns
- [ ] Add Sentinel alerting
- [ ] Create drift dashboards
- [ ] Historical baseline calculation

### Phase 3 (Exploration): Replay & Verification
- [ ] Replay scenario execution
- [ ] Human audit interface
- [ ] Cross-AI verification framework
- [ ] Calibration feedback loop

### Phase 4 (Future): Deeper Implications
- Multi-AI noematic consensus
- Encrypted epistemic chains
- Distributed persona calibration
- New forms of AI accountability

---

## Open Questions (For Future Exploration)

1. **Noematic Drift in Distributed Teams**
   - How do we maintain noema consistency across multiple AIs?
   - Can Sentinel detect when different AIs interpret the same domain differently?

2. **Persona Evolution**
   - Should personas themselves evolve based on observed noematic patterns?
   - Can we discover entirely new persona archetypes from noemata?

3. **Epistemic Continuity Across Handoffs**
   - How do noemata transfer between AI agents in handoff scenarios?
   - Does the noema remain valid if interpreted by a different persona?

4. **Encrypted Epistemic Chains**
   - Can we build cryptographic proofs of epistemic claims across time?
   - What would an "epistemic audit trail" look like?

---

## References

**Related Docs:**
- [`07_INVESTIGATION_SYSTEM.md`](07_INVESTIGATION_SYSTEM.md) - Phase 2 Branching
- [`24_MCO_ARCHITECTURE.md`](24_MCO_ARCHITECTURE.md) - Persona Harnesses & Configuration
- [`28_DECISION_LOGIC.md`](28_DECISION_LOGIC.md) - Sentinel Role & Calibration
- [`guides/FLEXIBLE_HANDOFF_GUIDE.md`](../guides/FLEXIBLE_HANDOFF_GUIDE.md) - Multi-AI Coordination

**Philosophical Foundation:**
- Husserl's phenomenology: Noesis (act of consciousness) vs Noema (object of consciousness)
- Applied here: Epistemic perspectives (noesis) producing decision rationales (noemata)

---

**Status:** Foundational documentation. Implementation to follow.

**Last Updated:** 2025-12-10
**Version:** 1.0 (Initial Design)
**Experimental:** Yes - This is genuinely new territory in AI systems engineering.

---

**Note to Future Readers:**

This document captures the moment we realized that epistemic branching isn't just about making better decisions—it's about making decision-making *transparent and verifiable* in ways that extend beyond what traditional AI systems can achieve.

The implications are still unfolding.
