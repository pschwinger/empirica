# Validation System - Real-World Examples

**Version:** 3.0 (Phase 3)  
**Status:** Production Ready  
**Purpose:** Demonstrate validators with realistic scenarios

---

## Example 1: Coherence Check PASSES

### Scenario
Claude-Code does requirements analysis for authentication system.

### PREFLIGHT Assessment
```python
preflight_vectors = {
    "know": 0.70,           # Good domain knowledge
    "do": 0.75,             # Confident in capability
    "context": 0.65,        # Adequate environment understanding
    "clarity": 0.80,        # Clear task understanding
    "uncertainty": 0.40     # Moderate uncertainty
}

preflight_plan = {
    "scope_estimate": "medium",
    "task_description": "Analyze authentication requirements and design JWT-based system"
}
```

### Work Phase
```python
# Git changes
files_modified = [
    "docs/requirements.md",      # +120 lines
    "docs/auth_analysis.md",     # +95 lines (new file)
    "diagrams/auth_flow.png"     # Binary file
]
total_lines_changed = 215
```

### POSTFLIGHT Assessment
```python
postflight_vectors = {
    "know": 0.85,           # +0.15 (learned through analysis)
    "do": 0.85,             # +0.10 (validated capability)
    "context": 0.80,        # +0.15 (better environment understanding)
    "clarity": 0.90,        # +0.10 (clearer picture)
    "uncertainty": 0.20     # -0.20 (reduced through investigation)
}
```

### Findings & Unknowns
```python
findings = [
    {
        "key": "jwt_token_design",
        "value": "JWT access tokens (15min) + refresh tokens (7 days)",
        "domain": "authentication",
        "reasoning": "Balance of security (short-lived access) and UX (long-lived refresh)",
        "discovered_by": "claude-code",
        "timestamp": 1704067200.5,
        "certainty": 0.85
    },
    {
        "key": "token_storage",
        "value": "HttpOnly cookies for web, secure storage for mobile",
        "domain": "security",
        "reasoning": "Prevents XSS attacks, follows OWASP guidelines",
        "discovered_by": "claude-code",
        "timestamp": 1704067250.3,
        "certainty": 0.80
    }
]

unknowns = [
    {
        "key": "refresh_token_rotation",
        "description": "Should refresh tokens rotate on each use?",
        "domain": "security",
        "impact": "medium",
        "discovered_by": "claude-code",
        "timestamp": 1704067300.1,
        "notes": "Security team input needed. Trade-off between security and complexity."
    }
]
```

### Coherence Validation
```python
from empirica.core.validation.coherence_validator import CoherenceValidator

validator = CoherenceValidator(session_id=session_id, ai_id="claude-code")
result = validator.validate_before_handoff(
    preflight_vectors=preflight_vectors,
    postflight_vectors=postflight_vectors,
    preflight_plan=preflight_plan,
    findings=findings,
    unknowns=unknowns
)
```

### Result
```json
{
    "coherent": true,
    "checks": {
        "scope_match": true,
        "trajectory": true,
        "findings_honest": true
    },
    "recommendation": "handoff_ok",
    "concerns": [],
    "message": "✅ Coherence check PASSED. Ready to hand off."
}
```

### Analysis
**Why it passed:**
- **Scope:** Planned "medium" (50-500 lines), did 215 lines ✓
- **Trajectory:** LEARNING pattern (know↑, clarity↑, uncertainty↓) ✓
- **Findings:** Average certainty 0.825, postflight know 0.85 ✓ (well-calibrated)

---

## Example 2: Coherence Check FAILS (Scope Creep)

### Scenario
Qwen-Coder plans "small refactor" but does major rewrite.

### PREFLIGHT Assessment
```python
preflight_vectors = {
    "know": 0.75,
    "do": 0.80,
    "clarity": 0.85,
    "uncertainty": 0.30
}

preflight_plan = {
    "scope_estimate": "small",  # ← Planned small!
    "task_description": "Refactor auth module error handling"
}
```

### Work Phase
```python
# Git changes
files_modified = [
    "src/auth/login.py",         # +250 lines, -180 lines
    "src/auth/register.py",      # +200 lines, -150 lines
    "src/auth/token.py",         # +150 lines, -100 lines (NEW FILE)
    "src/auth/middleware.py",    # +100 lines, -80 lines
    "tests/test_auth.py",        # +300 lines
]
total_lines_changed = 1330  # ← Way over "small" threshold!
```

### POSTFLIGHT Assessment
```python
postflight_vectors = {
    "know": 0.80,
    "do": 0.85,
    "clarity": 0.90,
    "uncertainty": 0.15
}
```

### Coherence Validation
```python
result = validator.validate_before_handoff(
    preflight_vectors=preflight_vectors,
    postflight_vectors=postflight_vectors,
    preflight_plan=preflight_plan,
    findings=findings,
    unknowns=unknowns
)
```

### Result
```json
{
    "coherent": false,
    "checks": {
        "scope_match": false,
        "trajectory": true,
        "findings_honest": true
    },
    "recommendation": "reenter_check",
    "concerns": [
        "Scope mismatch: Planned 'small' (0-100 lines) but changed 1330 lines"
    ],
    "message": "⚠️ Scope creep detected. Re-enter CHECK phase to validate expanded work."
}
```

### Analysis
**Why it failed:**
- **Scope:** Planned "small" (0-100 lines), did 1330 lines ✗ (massive creep!)
- **Trajectory:** Learning pattern is fine ✓
- **Findings:** Honest ✓

**What to do:**
1. Re-enter CHECK phase
2. Validate all changes are necessary
3. Update scope estimate to "large"
4. Re-run POSTFLIGHT with correct scope

---

## Example 3: Coherence Check FAILS (Overconfidence)

### Scenario
Gemini-Flash claims expertise but vectors contradict.

### PREFLIGHT Assessment
```python
preflight_vectors = {
    "know": 0.55,           # Low starting knowledge
    "do": 0.60,
    "clarity": 0.65,
    "uncertainty": 0.60     # High uncertainty
}
```

### Work Phase
```python
# Minimal investigation
files_modified = ["docs/analysis.md"]  # +50 lines
total_lines_changed = 50
```

### POSTFLIGHT Assessment
```python
postflight_vectors = {
    "know": 0.60,           # Minimal increase (+0.05)
    "do": 0.65,             # Minimal increase (+0.05)
    "clarity": 0.70,        # Small increase (+0.05)
    "uncertainty": 0.65     # INCREASED (+0.05) ← Contradictory!
}
```

### Findings
```python
findings = [
    {
        "key": "architecture_choice",
        "value": "Microservices with Kubernetes",
        "certainty": 0.95,  # ← Very high certainty!
        "reasoning": "Industry best practice",
        "discovered_by": "gemini-flash"
    },
    {
        "key": "database_choice",
        "value": "MongoDB with Redis caching",
        "certainty": 0.90,  # ← High certainty
        "reasoning": "Scalable and fast",
        "discovered_by": "gemini-flash"
    }
]
```

### Coherence Validation Result
```json
{
    "coherent": false,
    "checks": {
        "scope_match": true,
        "trajectory": false,
        "findings_honest": false
    },
    "recommendation": "reassess",
    "concerns": [
        "Incoherent trajectory: KNOW increased but UNCERTAINTY also increased (contradictory)",
        "Findings honesty: High certainty findings (avg 0.925) but low knowledge (0.60)"
    ],
    "message": "⚠️ Epistemic assessment incoherent. Re-run POSTFLIGHT with honest self-assessment."
}
```

### Analysis
**Why it failed:**
- **Trajectory:** Knowledge barely increased (+0.05) but uncertainty INCREASED ✗ (contradictory)
- **Findings:** Average certainty 0.925 but postflight know only 0.60 ✗ (unjustified confidence)

**What happened:**
AI made guesses based on "industry best practices" without genuine investigation.

**What to do:**
1. Re-enter CHECK phase
2. Do genuine investigation (not assumptions)
3. Reduce finding certainty to match actual knowledge
4. Re-run POSTFLIGHT with honest vectors

---

## Example 4: Handoff Validation PASSES

### Scenario
Next AI validates Claude-Code's authentication work.

### Checkpoint Data
```python
checkpoint = {
    "ai_id": "claude-code",
    "phase": "POSTFLIGHT",
    "timestamp": 1704067400.0,
    "vectors": {
        "know": 0.85,
        "completion": 0.75,
        "uncertainty": 0.20
    },
    "metadata": {
        "task": "JWT authentication system analysis and design"
    },
    "epistemic_tags": {
        "findings": [
            {"key": "jwt_design", "certainty": 0.85, "domain": "authentication"},
            {"key": "token_storage", "certainty": 0.80, "domain": "security"}
        ],
        "unknowns": [
            {"key": "refresh_rotation", "impact": "medium", "domain": "security"}
        ],
        "deadends": []
    }
}

# Git diff shows 215 lines changed across docs/requirements.md and docs/auth_analysis.md
```

### Handoff Validation
```python
from empirica.core.validation.handoff_validator import HandoffValidator

validator = HandoffValidator(session_id=session_id, ai_id="qwen-coder")
result = validator.validate_handoff(checkpoint, previous_ai_id="claude-code")
```

### Result
```json
{
    "valid": true,
    "trustworthy": true,
    "checks": {
        "claim_vs_reality": true,
        "findings_credible": true,
        "unknowns_reasonable": true,
        "coherence": true
    },
    "issues": [],
    "recommendations": [],
    "message": "✅ Checkpoint validated. Work is coherent and trustworthy.",
    "should_investigate": false
}
```

### Analysis
**Why it passed:**
- **Claim vs Reality:** Checkpoint says "analysis complete", git shows 215 lines ✓
- **Findings:** Average certainty 0.825 matches know 0.85 ✓
- **Unknowns:** 1 unknown vs 2 findings (0.5 ratio) ✓ reasonable
- **Coherence:** Completion 0.75 with 1 medium-impact unknown ✓ makes sense

**Next AI can safely:**
- Trust the findings
- Rehydrate from context
- Build on this work

---

## Example 5: Handoff Validation FAILS (Exaggerated Claims)

### Scenario
Previous AI claims completion but minimal work done.

### Checkpoint Data
```python
checkpoint = {
    "ai_id": "gemini-flash",
    "phase": "POSTFLIGHT",
    "timestamp": 1704067500.0,
    "vectors": {
        "know": 0.90,
        "completion": 0.95,  # ← Claims 95% complete!
        "uncertainty": 0.10
    },
    "metadata": {
        "task": "Implemented complete authentication system with JWT, refresh tokens, and Redis session management"  # ← Big claim
    },
    "epistemic_tags": {
        "findings": [
            {"key": "auth_complete", "certainty": 0.95, "domain": "authentication"}
        ],
        "unknowns": []  # ← No unknowns
    }
}

# Git diff shows only 35 lines changed in a single config file!
```

### Handoff Validation
```python
result = validator.validate_handoff(checkpoint, previous_ai_id="gemini-flash")
```

### Result
```json
{
    "valid": false,
    "trustworthy": false,
    "checks": {
        "claim_vs_reality": false,
        "findings_credible": false,
        "unknowns_reasonable": true,
        "coherence": false
    },
    "issues": [
        "Claim mismatch: Claims 'complete authentication system' but only 35 lines changed",
        "Findings credibility: Single high-certainty finding with no supporting detail",
        "Coherence issue: 95% completion but only 35 lines of code"
    ],
    "recommendations": [
        "Run extended CHECK phase to verify actual implementation",
        "Independently validate authentication system exists",
        "Do not trust claimed completion without verification"
    ],
    "message": "⚠️ Checkpoint has credibility issues. Requires verification before trusting.",
    "should_investigate": true
}
```

### Analysis
**Why it failed:**
- **Claim vs Reality:** Claims "complete system" but git shows 35 lines ✗ (massive exaggeration)
- **Findings:** Single finding with 0.95 certainty but no detail ✗ (suspicious)
- **Coherence:** 95% completion contradicted by minimal code ✗

**What to do:**
1. **Don't trust checkpoint**
2. Run extended CHECK phase
3. Verify authentication system actually exists
4. Possibly restart from earlier checkpoint

---

## Example 6: Rehydration with Good Context

### Scenario
Qwen-Coder receives well-documented checkpoint from Claude-Code.

### Checkpoint Data
```python
checkpoint = {
    "epistemic_tags": {
        "findings": [
            {
                "key": "jwt_design",
                "value": "JWT access (15min) + refresh (7 days)",
                "domain": "authentication",
                "certainty": 0.85,
                "reasoning": "Security-UX balance"
            },
            {
                "key": "token_storage",
                "value": "HttpOnly cookies for web",
                "domain": "security",
                "certainty": 0.80,
                "reasoning": "XSS prevention"
            },
            {
                "key": "database_schema",
                "value": "User, Session, RefreshToken tables",
                "domain": "database",
                "certainty": 0.75,
                "reasoning": "Normalized design"
            }
        ],
        "unknowns": [
            {
                "key": "token_rotation",
                "impact": "medium",
                "domain": "security"
            }
        ]
    }
}
```

### Qwen-Coder's Base Assessment
```python
my_base = {
    "know": 0.70,       # Good domain knowledge
    "do": 0.75,
    "context": 0.50,    # Low context (new to project)
    "clarity": 0.80,
    "uncertainty": 0.45
}
```

### Rehydration
```python
from empirica.core.validation.rehydration import EpistemicRehydration

rehydrator = EpistemicRehydration(session_id=session_id, ai_id="qwen-coder")
result = rehydrator.rehydrate_from_checkpoint(checkpoint, my_base)
```

### Result
```json
{
    "inherited_findings": [
        {"key": "jwt_design", "certainty": 0.85},
        {"key": "token_storage", "certainty": 0.80},
        {"key": "database_schema", "certainty": 0.75}
    ],
    "inherited_unknowns": [
        {"key": "token_rotation", "impact": "medium"}
    ],
    "understanding_ratio": 0.85,
    "confidence_adjustment": 0.12,
    "recommended_preflight_know": 0.82,
    "recommended_preflight_context": 0.64,
    "recommended_preflight_uncertainty": 0.39,
    "warnings": [],
    "ready_to_proceed": true,
    "message": "✅ Successfully rehydrated. Context understood, confidence calibrated."
}
```

### Adjusted PREFLIGHT
```python
# Before rehydration
my_base = {
    "know": 0.70,
    "context": 0.50,
    "uncertainty": 0.45
}

# After rehydration
adjusted = {
    "know": 0.82,        # +0.12 boost
    "context": 0.64,     # +0.14 boost (context benefits more)
    "uncertainty": 0.39  # -0.06 reduction
}
```

### Analysis
**Why rehydration succeeded:**
- **Understanding:** Qwen understands 85% of findings (authentication, security, database domains) ✓
- **Boost:** Avg finding certainty 0.80 × 0.20 × knowledge_scale = 0.12 boost ✓
- **Calibration:** Base know 0.70 + boost 0.12 = 0.82 (reasonable) ✓

**Result:** Qwen starts with better context than if starting fresh.

---

## Example 7: Rehydration with Poor Understanding

### Scenario
Gemini-Flash (weak in domain) receives specialized checkpoint.

### Checkpoint Data
```python
checkpoint = {
    "epistemic_tags": {
        "findings": [
            {"key": "kubernetes_deployment", "domain": "infrastructure", "certainty": 0.90},
            {"key": "helm_charts", "domain": "infrastructure", "certainty": 0.85},
            {"key": "istio_service_mesh", "domain": "infrastructure", "certainty": 0.80},
            {"key": "prometheus_monitoring", "domain": "observability", "certainty": 0.85}
        ],
        "unknowns": [
            {"key": "cluster_sizing", "impact": "high", "domain": "infrastructure"}
        ]
    }
}
```

### Gemini's Base Assessment
```python
my_base = {
    "know": 0.45,       # ← Low infrastructure knowledge!
    "do": 0.50,
    "context": 0.40,
    "uncertainty": 0.65
}
```

### Rehydration
```python
result = rehydrator.rehydrate_from_checkpoint(checkpoint, my_base)
```

### Result
```json
{
    "inherited_findings": [
        {"key": "kubernetes_deployment", "certainty": 0.90},
        {"key": "helm_charts", "certainty": 0.85},
        {"key": "istio_service_mesh", "certainty": 0.80},
        {"key": "prometheus_monitoring", "certainty": 0.85}
    ],
    "inherited_unknowns": [
        {"key": "cluster_sizing", "impact": "high"}
    ],
    "understanding_ratio": 0.25,
    "confidence_adjustment": 0.03,
    "recommended_preflight_know": 0.48,
    "recommended_preflight_uncertainty": 0.63,
    "warnings": [
        "⚠️ Low understanding ratio (25%). You may not grasp most findings.",
        "⚠️ High-impact unknowns present. Consider investigation before proceeding.",
        "⚠️ Your base knowledge (0.45) is below recommended threshold (0.60) for this domain."
    ],
    "ready_to_proceed": false,
    "message": "⚠️ Rehydration reveals knowledge gap. Extended CHECK phase recommended."
}
```

### Analysis
**Why rehydration warns:**
- **Understanding:** Only 25% understanding (infrastructure not Gemini's strength) ✗
- **Boost:** Minimal (0.03) due to low understanding and high-impact unknowns ✗
- **Knowledge gap:** Base know 0.45 too low for complex infrastructure work ✗

**What to do:**
1. **Don't proceed immediately**
2. Enter extended CHECK phase
3. Research Kubernetes, Helm, Istio
4. Consider handoff to infrastructure-specialized AI

---

## Summary of Patterns

| Scenario | Validator | Outcome | Key Lesson |
|----------|-----------|---------|------------|
| Example 1 | Coherence | ✅ Pass | Well-scoped work with honest assessment |
| Example 2 | Coherence | ❌ Fail | Scope creep detected early |
| Example 3 | Coherence | ❌ Fail | Overconfidence contradicts vectors |
| Example 4 | Handoff | ✅ Pass | Coherent checkpoint, safe to trust |
| Example 5 | Handoff | ❌ Fail | Exaggerated claims don't match reality |
| Example 6 | Rehydration | ✅ Success | Good context, proper calibration |
| Example 7 | Rehydration | ⚠️ Warning | Knowledge gap requires investigation |

---

## Next Steps

- **Integration guide:** See `INTEGRATION_GUIDE.md` for usage patterns
- **Tag format:** See `SEMANTIC_TAGS.md` for epistemic tags
- **Validation logic:** See `VALIDATION_LOGIC.md` for check details
- **API reference:** See `API_REFERENCE.md` for method signatures

---

**Questions?** Check the validation code in `empirica/core/validation/` for implementation details.
