# API Reference

**Build with Empirica.**

Complete Python API documentation.

---

## Core Modules

<!-- BENTO_START -->

## 🌊 CanonicalEpistemicCascade
**Main Workflow Class.**

Orchestrates the 7-phase CASCADE workflow.
`from empirica import CanonicalEpistemicCascade`

## 💾 SessionDatabase
**Persistence.**

Manages SQLite storage for sessions and assessments.
`from empirica.data.session_database import SessionDatabase`

## 📝 ReflexLogger
**Temporal Logging.**

Handles phase-specific JSON logging to prevent loops.
`from empirica.core.canonical import ReflexLogger`

<!-- BENTO_END -->

---

## MCP Tools (Recommended)

For AI assistants, use the 23 MCP tools.

- **Session:** `bootstrap_session`, `resume_previous_session`
- **Workflow:** `execute_preflight`, `submit_check_assessment`
- **Goals:** `create_goal`, `add_subtask`
- **Continuity:** `create_git_checkpoint`, `create_handoff_report`

---

## Best Practices

### 1. Profile Configuration
Use profiles instead of manual tuning.
```python
cascade = CanonicalEpistemicCascade(profile_name="autonomous_agent")
```

### 2. Git Checkpoints
Enable version-controlled state (~450 tokens).
```python
cascade = CanonicalEpistemicCascade(enable_git_notes=True)
```

### 3. Handoff Reports
Generate reports for continuity (~400 tokens).
```python
create_handoff_report(session_id="...", task_summary="...")
```

---

**Next Steps:**
- [CLI Interface](cli-interface.md)
- [Architecture](architecture.md)
