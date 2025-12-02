# Dashboard API Specification (Phase 3.3)

**Status**: Specification Document
**Date**: 2025-12-02
**Purpose**: Foundation for Forgejo plugin and standalone dashboards
**Audience**: Backend implementers, plugin developers, dashboard designers

---

## Overview

The Dashboard API exposes Empirica's three-layer storage architecture through queryable REST endpoints, enabling:

- **Live dashboards** (current epistemic state, learning curves)
- **Commit-bound analytics** (which files changed when learning increased?)
- **Crypto verification** (verify AI reasoning wasn't tampered)
- **Uncertainty heatmaps** (confidence by module/file)
- **Multi-AI coordination** (see multiple AIs' learning trajectories)

### Design Principles

1. **Prefer git notes for current state** (fast, 450 tokens)
2. **Use SQLite for historical queries** (indexed, relational)
3. **Sign with git note SHAs** (not JSON files, not database rows)
4. **Expose learning deltas explicitly** (epistemic_deltas field)
5. **Include git binding data** (commit SHAs, file changes)

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│           Dashboard API (FastAPI/Flask)         │
├─────────────────────────────────────────────────┤
│ Sessions │ Deltas │ Verification │ Heatmaps    │
├─────────────────────────────────────────────────┤
│   Query Layer (Aggregation & Filtering)         │
├─────────────────────────────────────────────────┤
│  SQLite (history)  │  Git Notes (current state) │
│  sessions table    │  refs/notes/empirica/*    │
└─────────────────────────────────────────────────┘
```

---

## Core Endpoints

### 1. Session Management

#### GET `/api/v1/sessions`
List all sessions with filtering and pagination.

**Query Parameters:**
```
- ai_id: Filter by AI agent
- since: ISO timestamp (e.g., "2025-11-01")
- limit: Max results (default: 20)
- offset: Pagination offset (default: 0)
```

**Response:**
```json
{
  "ok": true,
  "total": 42,
  "sessions": [
    {
      "session_id": "d8e62559-3f7e-4806-b78e-f82968162594",
      "ai_id": "copilot",
      "start_time": "2025-12-02T13:00:00Z",
      "end_time": "2025-12-02T14:30:00Z",
      "duration_seconds": 5400,
      "task_summary": "Mapped complete Empirica architecture...",
      "phase": "POSTFLIGHT",
      "overall_confidence": 0.85,
      "uncertainty": 0.15,
      "git_head": "f13d167",
      "checkpoints_count": 3
    }
  ]
}
```

---

#### GET `/api/v1/sessions/{session_id}`
Retrieve detailed session information.

**Response:**
```json
{
  "ok": true,
  "session": {
    "session_id": "d8e62559-3f7e-4806-b78e-f82968162594",
    "ai_id": "copilot",
    "start_time": "2025-12-02T13:00:00Z",
    "end_time": "2025-12-02T14:30:00Z",
    "duration_seconds": 5400,
    "task_summary": "Mapped architecture and designed crypto signing strategy",
    "overall_confidence": 0.85,
    "git_state": {
      "head_commit": "f13d167",
      "commits_since_session_start": 2,
      "files_changed": ["auth.py", "tests.py"],
      "lines_added": 170,
      "lines_removed": 20
    },
    "epistemic_timeline": [
      {
        "phase": "PREFLIGHT",
        "round": 1,
        "timestamp": "2025-12-02T13:00:00Z",
        "vectors": {
          "know": 0.60,
          "do": 0.70,
          "context": 0.80,
          "clarity": 0.65,
          "coherence": 0.75,
          "signal": 0.80,
          "density": 0.45,
          "state": 0.70,
          "change": 0.60,
          "completion": 0.40,
          "impact": 0.50,
          "engagement": 0.85,
          "uncertainty": 0.50
        }
      },
      {
        "phase": "POSTFLIGHT",
        "round": 1,
        "timestamp": "2025-12-02T14:30:00Z",
        "vectors": {
          "know": 0.85,
          "do": 0.95,
          "context": 0.90,
          "clarity": 0.90,
          "coherence": 0.95,
          "signal": 0.90,
          "density": 0.35,
          "state": 0.90,
          "change": 0.90,
          "completion": 0.95,
          "impact": 0.90,
          "engagement": 0.95,
          "uncertainty": 0.15
        }
      }
    ],
    "checkpoints": [
      {
        "phase": "PREFLIGHT",
        "round": 1,
        "timestamp": "2025-12-02T13:00:00Z",
        "git_state_sha": "abc123def456...",
        "signature_verified": true,
        "signature_by": "copilot"
      },
      {
        "phase": "POSTFLIGHT",
        "round": 1,
        "timestamp": "2025-12-02T14:30:00Z",
        "git_state_sha": "xyz789uvw...",
        "signature_verified": true,
        "signature_by": "copilot"
      }
    ]
  }
}
```

---

### 2. Learning Deltas

#### GET `/api/v1/sessions/{session_id}/deltas`
Get epistemic changes from PREFLIGHT to POSTFLIGHT.

**Response:**
```json
{
  "ok": true,
  "session_id": "d8e62559-3f7e-4806-b78e-f82968162594",
  "deltas": {
    "know": {"preflight": 0.60, "postflight": 0.85, "delta": 0.25},
    "do": {"preflight": 0.70, "postflight": 0.95, "delta": 0.25},
    "context": {"preflight": 0.80, "postflight": 0.90, "delta": 0.10},
    "clarity": {"preflight": 0.65, "postflight": 0.90, "delta": 0.25},
    "uncertainty": {"preflight": 0.50, "postflight": 0.15, "delta": -0.35},
    "overall_confidence": {"preflight": 0.70, "postflight": 0.85, "delta": 0.15},
    "learning_velocity": {
      "know_per_minute": 0.0093,  // 0.25 delta / 5400 seconds * 60
      "overall_per_minute": 0.0056
    }
  },
  "git_correlation": {
    "commit_sha": "f13d167",
    "files_changed": ["auth.py", "tests.py"],
    "lines_added": 170,
    "lines_removed": 20,
    "correlation_strength": "high"  // Based on delta magnitude
  }
}
```

---

#### GET `/api/v1/commits/{commit_sha}/epistemic`
Get epistemic state associated with a specific git commit.

**Response:**
```json
{
  "ok": true,
  "commit_sha": "f13d167",
  "commit_message": "feat: implement auth improvements",
  "files_changed": ["auth.py", "tests.py"],
  "lines_added": 170,
  "lines_removed": 20,
  "epistemic_context": {
    "session_id": "d8e62559-3f7e-4806-b78e-f82968162594",
    "ai_id": "copilot",
    "know": 0.85,
    "uncertainty": 0.15,
    "investigated": ["jwt_refresh", "session_hijack"],
    "not_investigated": ["distributed_consensus"],
    "confidence_basis": "tested_in_staging_30_days",
    "risk_assessment": "low_for_single_node"
  },
  "learning_delta": {
    "know": 0.25,
    "do": 0.25,
    "overall": 0.15
  }
}
```

---

### 3. Crypto Verification

#### GET `/api/v1/checkpoints/{session_id}/{phase}/{round}/verify`
Verify cryptographic signature of a checkpoint.

**Query Parameters:**
```
- public_key: Optional public key hex (uses stored identity if omitted)
```

**Response:**
```json
{
  "ok": true,
  "checkpoint_id": "d8e62559-3f7e-4806-b78e-f82968162594/POSTFLIGHT/1",
  "git_note_sha": "abc123def456...",
  "signature_verified": true,
  "signed_by": "copilot",
  "signature_date": "2025-12-02T14:30:00Z",
  "public_key": "ed25519:abcdef...",
  "content_hash": "sha256:xyz789...",
  "verification_method": "ed25519_signature"
}
```

---

#### GET `/api/v1/sessions/{session_id}/signatures`
List all verified signatures for a session.

**Response:**
```json
{
  "ok": true,
  "session_id": "d8e62559-3f7e-4806-b78e-f82968162594",
  "signatures": [
    {
      "phase": "PREFLIGHT",
      "round": 1,
      "timestamp": "2025-12-02T13:00:00Z",
      "git_note_sha": "abc123...",
      "verified": true,
      "signed_by": "copilot",
      "public_key": "ed25519:abcdef..."
    },
    {
      "phase": "POSTFLIGHT",
      "round": 1,
      "timestamp": "2025-12-02T14:30:00Z",
      "git_note_sha": "xyz789...",
      "verified": true,
      "signed_by": "copilot",
      "public_key": "ed25519:abcdef..."
    }
  ],
  "all_verified": true,
  "verification_status": "fully_signed_and_verified"
}
```

---

### 4. Uncertainty Heatmaps

#### GET `/api/v1/files/{filepath}/uncertainty`
Get confidence/uncertainty metrics by file.

**Example**: `/api/v1/files/auth.py/uncertainty`

**Response:**
```json
{
  "ok": true,
  "filepath": "auth.py",
  "uncertainty_metrics": {
    "overall_uncertainty": 0.15,
    "know": 0.85,
    "do": 0.95,
    "investigated_areas": ["jwt_refresh", "session_hijack"],
    "not_investigated": ["distributed_consensus"],
    "risk_level": "low_for_single_node"
  },
  "changes_made": [
    {
      "session_id": "d8e62559-3f7e-4806-b78e-f82968162594",
      "commit_sha": "f13d167",
      "lines_added": 50,
      "lines_removed": 10,
      "confidence": 0.85,
      "timestamp": "2025-12-02T14:00:00Z"
    }
  ],
  "aggregate_confidence": 0.85
}
```

---

#### GET `/api/v1/modules/{module_name}/epistemic`
Get epistemic knowledge map for a module/directory.

**Example**: `/api/v1/modules/auth/epistemic`

**Response:**
```json
{
  "ok": true,
  "module": "auth",
  "epistemic_map": {
    "submodules": {
      "jwt": {
        "know": 0.85,
        "uncertainty": 0.15,
        "status": "well_understood"
      },
      "session_management": {
        "know": 0.80,
        "uncertainty": 0.20,
        "status": "mostly_understood"
      },
      "distributed_auth": {
        "know": 0.40,
        "uncertainty": 0.60,
        "status": "not_investigated"
      }
    },
    "overall_know": 0.80,
    "overall_uncertainty": 0.20,
    "coverage": "75%",
    "risk_areas": ["distributed_consensus"],
    "tested": ["staging_30_days"]
  },
  "recent_sessions": 3,
  "last_modified": "2025-12-02T14:00:00Z"
}
```

---

### 5. Multi-AI Coordination

#### GET `/api/v1/ai/{ai_id}/learning-curve`
Get learning trajectory for a specific AI.

**Query Parameters:**
```
- since: Start date (default: 30 days ago)
- limit: Max data points (default: 100)
```

**Response:**
```json
{
  "ok": true,
  "ai_id": "copilot",
  "total_sessions": 42,
  "time_period": "2025-11-02 to 2025-12-02",
  "learning_trajectory": [
    {
      "session_id": "session1",
      "timestamp": "2025-11-02T10:00:00Z",
      "know": 0.65,
      "do": 0.70,
      "uncertainty": 0.35,
      "overall_confidence": 0.67
    },
    {
      "session_id": "session2",
      "timestamp": "2025-11-03T14:00:00Z",
      "know": 0.72,
      "do": 0.78,
      "uncertainty": 0.28,
      "overall_confidence": 0.75
    }
  ],
  "statistics": {
    "average_know": 0.75,
    "average_uncertainty": 0.25,
    "learning_velocity": 0.0045,
    "trend": "improving"
  }
}
```

---

#### GET `/api/v1/compare-ais`
Compare learning curves across multiple AIs.

**Query Parameters:**
```
- ai_ids: Comma-separated AI identifiers (e.g., "copilot,gemini,claude")
- since: Start date
- metric: Which metric to compare (default: "know")
```

**Response:**
```json
{
  "ok": true,
  "comparison": [
    {
      "ai_id": "copilot",
      "average_know": 0.75,
      "average_uncertainty": 0.25,
      "sessions": 42,
      "trend": "improving"
    },
    {
      "ai_id": "gemini",
      "average_know": 0.78,
      "average_uncertainty": 0.22,
      "sessions": 38,
      "trend": "stable"
    }
  ],
  "best_performer": "gemini",
  "most_improving": "copilot"
}
```

---

## Authentication & Security

### Default (Development)
- No authentication required for localhost (`127.0.0.1`)
- Use `X-API-Key` header for remote access

### Production
- OAuth2 with client credentials
- JWT tokens with 1-hour expiration
- Rate limiting: 100 requests/minute per API key

```bash
curl -H "X-API-Key: your-key" https://api.example.com/api/v1/sessions
```

---

## Error Responses

All errors follow this format:

```json
{
  "ok": false,
  "error": "session_not_found",
  "message": "Session d8e62559-... does not exist",
  "status_code": 404
}
```

**Common errors:**
- `400`: Invalid query parameters
- `404`: Resource not found
- `500`: Server error
- `422`: Invalid data format

---

## Implementation Notes

### Caching Strategy
- **Current state** (git notes): Cache 5 minutes
- **Historical data** (SQLite): Cache 1 hour
- **Verification results**: Cache 24 hours (crypto stable)

### Query Performance
- Session list: `O(log n)` with index on `ai_id`, `start_time`
- Commit lookup: `O(1)` with git object store
- File uncertainty: `O(m)` where m = number of changes to file

### Pagination
- Default limit: 20
- Maximum limit: 1000
- Use `offset` for pagination (no cursor needed for v1)

---

## Usage Examples

### Example 1: Dashboard showing learning over time
```python
# Get all sessions for an AI
sessions = await api.get("/api/v1/sessions?ai_id=copilot&limit=50")

# For each session, get learning deltas
for session in sessions['sessions']:
    deltas = await api.get(f"/api/v1/sessions/{session['session_id']}/deltas")
    # Plot deltas over time
```

### Example 2: Verify commit was made with high confidence
```python
# Get epistemic context for commit
epistemic = await api.get("/api/v1/commits/f13d167/epistemic")

# Check if AI was confident
if epistemic['epistemic_context']['know'] > 0.85:
    print("✅ Commit made with high confidence")
else:
    print("⚠️ Commit made with low confidence - might need review")
```

### Example 3: Find risky files
```python
# Get module epistemic map
module = await api.get("/api/v1/modules/auth/epistemic")

# Identify areas not investigated
risk_areas = module['epistemic_map']['risk_areas']
if risk_areas:
    print(f"⚠️ Not investigated: {risk_areas}")
```

---

## Integration with Forgejo Plugin

The Forgejo plugin uses these endpoints to:

1. **Show confidence heatmaps** on file diffs
   - Calls `/api/v1/files/{filepath}/uncertainty`
   - Colors lines based on `know` score

2. **Link commits to epistemic state**
   - Calls `/api/v1/commits/{sha}/epistemic`
   - Shows "AI confidence" badge on commits

3. **Verify signatures in PRs**
   - Calls `/api/v1/sessions/{id}/signatures`
   - Shows "✅ Verified by Claude" badge

4. **Show learning curves in dashboards**
   - Calls `/api/v1/ai/{ai_id}/learning-curve`
   - Plots knowledge over time

---

## Future Enhancements (Not in Phase 3.3)

- **WebSocket streaming** for real-time updates
- **GraphQL API** as alternative to REST
- **Database sharding** for large deployments
- **Federated queries** across multiple repos
- **Custom metric endpoints** (user-defined analysis)

---

## Related Documentation

- `/docs/production/25_SCOPEVECTOR_GUIDE.md` - Epistemic vector semantics
- `/docs/architecture/STORAGE_ARCHITECTURE_VISUAL_GUIDE.md` - Storage layers
- `/docs/production/09_DRIFT_MONITOR.md` - Calibration and drift
- `/empirica/core/checkpoint_signer.py` - Crypto verification

---

**Specification Version**: 1.0
**Last Updated**: 2025-12-02
**Status**: Ready for Implementation
**Next Step**: Implement endpoints in Flask/FastAPI
