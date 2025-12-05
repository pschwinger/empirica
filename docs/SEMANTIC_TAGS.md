# Semantic Epistemic Tags - Format Documentation

**Version:** 3.0 (Phase 3)  
**Status:** Production Ready  
**Purpose:** Structured knowledge transfer between AIs

---

## Overview

Epistemic tags are structured metadata attached to git checkpoints that enable **semantic knowledge transfer** between AIs:

- **Findings:** What was learned during the work phase
- **Unknowns:** What remains unclear or requires investigation
- **Deadends:** What approaches were tried but don't work

Tags are stored in git notes alongside checkpoints and enable the next AI to:
1. Understand what was learned
2. Avoid repeating failed approaches
3. Calibrate confidence based on inherited context

---

## Tag Type 1: Findings

### Purpose

A **finding** represents a key discovery, decision, or learning from the work phase.

### Format

```json
{
  "key": "string (identifier)",
  "value": "string (what was learned)",
  "domain": "string (knowledge area)",
  "reasoning": "string (why this matters)",
  "discovered_by": "string (AI identifier)",
  "timestamp": "float (unix timestamp)",
  "certainty": "float (0.0-1.0 confidence)"
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | Yes | Short, unique identifier (e.g., `"auth_pattern"`) |
| `value` | string | Yes | What was learned (e.g., `"JWT with refresh tokens"`) |
| `domain` | string | Yes | Knowledge area (e.g., `"authentication"`, `"database"`, `"architecture"`) |
| `reasoning` | string | Yes | Why this finding matters |
| `discovered_by` | string | Yes | AI identifier who made discovery |
| `timestamp` | float | Yes | When discovered (unix timestamp) |
| `certainty` | float | Yes | Confidence in finding (0.0-1.0 scale) |

### Examples

#### High Certainty Finding

```json
{
  "key": "database_choice",
  "value": "PostgreSQL 15 with TimescaleDB extension",
  "domain": "database",
  "reasoning": "Requirement for time-series data + relational integrity",
  "discovered_by": "claude-code",
  "timestamp": 1704067200.5,
  "certainty": 0.95
}
```

**Interpretation:** High certainty (0.95) - well-justified decision with clear requirements.

#### Medium Certainty Finding

```json
{
  "key": "api_design_pattern",
  "value": "RESTful with GraphQL for complex queries",
  "domain": "api_design",
  "reasoning": "REST for simple CRUD, GraphQL for flexible frontend needs",
  "discovered_by": "qwen-coder",
  "timestamp": 1704067300.2,
  "certainty": 0.75
}
```

**Interpretation:** Medium certainty (0.75) - reasonable approach but alternatives exist.

#### Low Certainty Finding

```json
{
  "key": "caching_strategy",
  "value": "Redis with 5-minute TTL",
  "domain": "performance",
  "reasoning": "Estimated load based on similar projects",
  "discovered_by": "gemini-flash",
  "timestamp": 1704067400.8,
  "certainty": 0.55
}
```

**Interpretation:** Low certainty (0.55) - educated guess, needs validation with real metrics.

---

## Tag Type 2: Unknowns

### Purpose

An **unknown** represents something that remains unclear, needs investigation, or has unresolved options.

### Format

```json
{
  "key": "string (identifier)",
  "description": "string (what's unclear)",
  "domain": "string (knowledge area)",
  "impact": "string (high/medium/low)",
  "discovered_by": "string (AI identifier)",
  "timestamp": "float (unix timestamp)",
  "notes": "string (additional context)"
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | Yes | Short identifier (e.g., `"orm_choice"`) |
| `description` | string | Yes | What's unclear (e.g., `"SQLAlchemy vs Tortoise vs Django ORM"`) |
| `domain` | string | Yes | Knowledge area affected |
| `impact` | string | Yes | Impact level: `"high"`, `"medium"`, or `"low"` |
| `discovered_by` | string | Yes | AI identifier who identified unknown |
| `timestamp` | float | Yes | When identified (unix timestamp) |
| `notes` | string | No | Additional context or options |

### Examples

#### High Impact Unknown

```json
{
  "key": "deployment_platform",
  "description": "AWS ECS vs Kubernetes vs GCP Cloud Run",
  "domain": "infrastructure",
  "impact": "high",
  "discovered_by": "claude-code",
  "timestamp": 1704067200.5,
  "notes": "Need to understand budget constraints and team expertise. All three viable technically."
}
```

**Interpretation:** Critical decision blocking deployment planning.

#### Medium Impact Unknown

```json
{
  "key": "test_framework",
  "description": "pytest vs unittest - which to standardize on?",
  "domain": "testing",
  "impact": "medium",
  "discovered_by": "qwen-coder",
  "timestamp": 1704067300.2,
  "notes": "Both work, affects test structure. Team has pytest experience."
}
```

**Interpretation:** Important for consistency but not blocking progress.

#### Low Impact Unknown

```json
{
  "key": "logging_format",
  "description": "JSON logs vs plain text",
  "domain": "observability",
  "impact": "low",
  "discovered_by": "gemini-flash",
  "timestamp": 1704067400.8,
  "notes": "JSON better for parsing, plain text more readable. Easy to change later."
}
```

**Interpretation:** Minor decision, can be deferred or changed easily.

---

## Tag Type 3: Deadends

### Purpose

A **deadend** represents an approach that was tried but doesn't work, preventing future AIs from repeating the same mistake.

### Format

```json
{
  "approach": "string (what was tried)",
  "blocker": "string (why it doesn't work)",
  "domain": "string (knowledge area)",
  "tried_by": "string (AI identifier)",
  "timestamp": "float (unix timestamp)",
  "why_eliminated": "string (technical reason)",
  "alternative_tried": "string (what worked instead)"
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `approach` | string | Yes | What was attempted |
| `blocker` | string | Yes | Why it failed or doesn't work |
| `domain` | string | Yes | Knowledge area affected |
| `tried_by` | string | Yes | AI identifier who tried it |
| `timestamp` | float | Yes | When tried (unix timestamp) |
| `why_eliminated` | string | Yes | Detailed technical reason for failure |
| `alternative_tried` | string | No | What approach worked instead (if found) |

### Examples

#### Technical Blocker Deadend

```json
{
  "approach": "Monolithic authentication service",
  "blocker": "Incompatible with microservices architecture requirement",
  "domain": "architecture",
  "tried_by": "claude-code",
  "timestamp": 1704067200.5,
  "why_eliminated": "Service isolation requirement mandates separate auth service. Monolith creates tight coupling.",
  "alternative_tried": "Standalone auth microservice with event bus integration"
}
```

#### Dependency Blocker Deadend

```json
{
  "approach": "Using library XYZ for PDF generation",
  "blocker": "Library requires Python 3.11, project locked to 3.9",
  "domain": "dependencies",
  "tried_by": "qwen-coder",
  "timestamp": 1704067300.2,
  "why_eliminated": "Project constraint: Python 3.9 for production stability. Library XYZ has no 3.9 backport.",
  "alternative_tried": "ReportLab library (Python 3.9 compatible)"
}
```

#### Performance Blocker Deadend

```json
{
  "approach": "In-memory session storage",
  "blocker": "Doesn't survive server restarts, loses sessions",
  "domain": "session_management",
  "tried_by": "gemini-flash",
  "timestamp": 1704067400.8,
  "why_eliminated": "Production requirement: sessions must persist across deployments. In-memory violates this.",
  "alternative_tried": "Redis-backed sessions with persistence"
}
```

---

## When to Create Each Tag Type

### Create a Finding When:

- ✅ You make a key technical decision
- ✅ You discover important architectural constraint
- ✅ You learn something that changes approach
- ✅ You validate an assumption with evidence
- ✅ You identify a pattern or best practice

### Create an Unknown When:

- ✅ Multiple viable options exist (need decision)
- ✅ Missing information blocks next steps
- ✅ External dependency not yet determined
- ✅ Performance characteristics unknown (need metrics)
- ✅ Stakeholder decision required

### Create a Deadend When:

- ✅ You try an approach that fails technically
- ✅ Dependency doesn't work as expected
- ✅ Performance is unacceptable
- ✅ Conflicts with project constraints
- ✅ Implementation revealed fundamental flaw

---

## Tag Organization

### Store Tags in Checkpoint

Tags are passed to `add_checkpoint()` via `epistemic_tags` parameter:

```python
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger

logger = GitEnhancedReflexLogger(session_id=session_id)

logger.add_checkpoint(
    phase="POSTFLIGHT",
    vectors=postflight_vectors,
    metadata={"task": "Authentication module completed"},
    epistemic_tags={
        "findings": [
            {
                "key": "auth_pattern",
                "value": "JWT with refresh tokens",
                "domain": "authentication",
                "reasoning": "Security + UX balance",
                "discovered_by": "claude-code",
                "timestamp": 1704067200.5,
                "certainty": 0.85
            }
        ],
        "unknowns": [
            {
                "key": "token_rotation_policy",
                "description": "7-day vs 30-day refresh token lifetime",
                "domain": "security",
                "impact": "medium",
                "discovered_by": "claude-code",
                "timestamp": 1704067200.5,
                "notes": "Needs security team input"
            }
        ],
        "deadends": [
            {
                "approach": "OAuth 2.0 implicit flow",
                "blocker": "Security recommendation deprecated this flow",
                "domain": "authentication",
                "tried_by": "claude-code",
                "timestamp": 1704067200.5,
                "why_eliminated": "IETF OAuth 2.0 Security BCP deprecates implicit flow. Use authorization code + PKCE.",
                "alternative_tried": "Authorization code flow with PKCE"
            }
        ]
    }
)
```

### Retrieve Tags from Checkpoint

```python
checkpoint = logger.get_latest_checkpoint()
epistemic_tags = checkpoint.get("epistemic_tags", {})

findings = epistemic_tags.get("findings", [])
unknowns = epistemic_tags.get("unknowns", [])
deadends = epistemic_tags.get("deadends", [])
```

---

## Tag Validation Rules

### Certainty Calibration

Validators check that finding certainty matches your epistemic state:

```python
# ❌ SUSPICIOUS: Low knowledge but high certainty finding
preflight_know = 0.4
finding_certainty = 0.95  # Overconfident!

# ✅ COHERENT: Knowledge supports certainty
preflight_know = 0.85
finding_certainty = 0.85  # Matches
```

### Unknown Impact Justification

High-impact unknowns should block progress:

```python
# ✅ Good: High impact unknown with clear blocker
{
    "key": "database_schema",
    "description": "User table structure unclear",
    "impact": "high",
    "notes": "Blocks user authentication implementation"
}

# ⚠️ Suspicious: High impact but seems minor
{
    "key": "button_color",
    "description": "Blue vs green submit button",
    "impact": "high"  # Really? High impact?
}
```

### Deadend Blocker Clarity

Deadends must have clear technical reason:

```python
# ✅ Good: Clear technical blocker
{
    "approach": "SQLite for production",
    "blocker": "No multi-writer support",
    "why_eliminated": "Production has 3 app servers. SQLite doesn't support concurrent writes from multiple processes."
}

# ❌ Bad: Vague reason
{
    "approach": "Library X",
    "blocker": "Didn't work",
    "why_eliminated": "Had issues"  # Not specific enough!
}
```

---

## Advanced: Domain Taxonomy

Suggested domain categories for consistency:

| Domain | Use For |
|--------|---------|
| `authentication` | Auth, login, tokens, sessions |
| `authorization` | Permissions, roles, access control |
| `database` | Schema, queries, migrations, ORM |
| `api_design` | REST, GraphQL, endpoints, contracts |
| `architecture` | System structure, services, patterns |
| `performance` | Caching, optimization, scaling |
| `security` | Vulnerabilities, encryption, compliance |
| `testing` | Unit tests, integration tests, coverage |
| `deployment` | Infrastructure, CI/CD, containers |
| `observability` | Logging, metrics, tracing |
| `dependencies` | Libraries, frameworks, versions |
| `frontend` | UI, UX, components, styling |

Use these for consistency across AIs.

---

## Best Practices

### 1. Be Specific in Values

```python
# ❌ Vague
{"key": "database", "value": "We'll use PostgreSQL"}

# ✅ Specific
{"key": "database_choice", "value": "PostgreSQL 15 with TimescaleDB extension for time-series data"}
```

### 2. Justify Certainty

```python
# ❌ Unjustified high certainty
{"certainty": 0.95, "reasoning": "Seems good"}

# ✅ Justified
{"certainty": 0.85, "reasoning": "Validated against 3 similar projects. Meets all requirements. Team has expertise."}
```

### 3. Quantify Impact

```python
# ❌ Unclear impact
{"impact": "high", "notes": "Important decision"}

# ✅ Clear impact
{"impact": "high", "notes": "Blocks deployment until resolved. Affects 5 dependent services."}
```

### 4. Document Alternatives in Deadends

```python
# ✅ Good: Shows what worked
{
    "approach": "Approach A",
    "blocker": "Reason X",
    "why_eliminated": "Technical details",
    "alternative_tried": "Approach B (successful)"
}
```

---

## Next Steps

- **Integration guide:** See `INTEGRATION_GUIDE.md` for usage
- **Validation logic:** See `VALIDATION_LOGIC.md` for how tags are validated
- **Examples:** See `VALIDATION_EXAMPLES.md` for real scenarios

---

**Questions?** Check validation code in `empirica/core/validation/`
