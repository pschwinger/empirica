# Phase 1.6: Epistemic Handoff Reports

**Date:** 2025-11-17
**Status:** SPECIFICATION (Ready for Implementation)
**Priority:** HIGH - Massive impact for little effort
**Estimated Effort:** 4-6 hours
**Assigned To:** Copilot Claude

---

## Executive Summary

**What:** Compressed, semantically-rich session summaries that capture what an AI learned, generated during POSTFLIGHT, enabling efficient context transfer for multi-agent coordination.

**Why:** Git checkpoints (Phase 1.5) provide 97.5% token reduction but lack semantic context about *what was learned*. Handoff reports combine checkpoint efficiency with human-readable learning summaries.

**Impact:**
- ✅ 95% faster agent rotation (10 min → 30 sec context transfer)
- ✅ ~1,250 token resume (vs 20,000 token baseline = 93.75% reduction)
- ✅ Multi-agent memory across sessions
- ✅ Queryable learning history
- ✅ Enables seamless AI-to-AI handoffs

---

## Problem Statement

### Current Limitations:

1. **Git Checkpoints (Phase 1.5)** - Efficient but not semantic:
   ```json
   {
     "phase": "POSTFLIGHT",
     "vectors": {"know": 0.95, "do": 0.95, "uncertainty": 0.20},
     "round_num": 5
   }
   ```
   - ✅ Efficient (450 tokens)
   - ❌ No context about *what* was learned
   - ❌ No guidance for next session

2. **Documentation Handoffs** - Semantic but inefficient:
   ```markdown
   # Minimax Phase 1 Test Results
   [15,000 tokens of detailed documentation]
   ```
   - ✅ Full context and learning
   - ❌ Requires 10+ minutes to read and extract key points
   - ❌ Not queryable programmatically

3. **Conversation History** - Complete but massive:
   ```
   [Full conversation: 20,000+ tokens]
   ```
   - ✅ Complete record
   - ❌ Context window bloat
   - ❌ No epistemic tracking

### The Gap:

**We need:** Compressed, semantic, queryable session summaries that capture epistemic deltas + key learnings in ~1,250 tokens.

---

## Solution Architecture

### Core Concept:

**Epistemic Handoff Report** = Structured summary generated during POSTFLIGHT that answers:

1. **What was the task?** (objective)
2. **What changed epistemically?** (vector deltas)
3. **What was learned?** (key findings)
4. **What gaps were filled?** (knowledge progression)
5. **What's still unknown?** (remaining uncertainties)
6. **What's next?** (recommended next steps)

### Report Structure:

```markdown
# Epistemic Handoff Report

**Session:** {session_id}
**AI Agent:** {ai_id}
**Date:** {timestamp}
**Task:** {task_summary}
**Duration:** {elapsed_time}

## Epistemic Trajectory

**PREFLIGHT → POSTFLIGHT Deltas:**

| Vector | Before | After | Delta | Status |
|--------|--------|-------|-------|--------|
| KNOW | 0.70 | 0.95 | +0.25 | ✅ Improved |
| DO | 0.90 | 0.95 | +0.05 | ✅ Improved |
| CONTEXT | 0.80 | 0.90 | +0.10 | ✅ Improved |
| UNCERTAINTY | 0.65 | 0.20 | -0.45 | ✅ Reduced |
| Overall Confidence | 0.683 | 0.896 | +0.213 | ✅ Calibrated |

**Calibration Status:** {well_calibrated / overconfident / underconfident}

## What I Accomplished

{2-4 bullet points of concrete deliverables}

## What I Learned

{3-5 key findings that shifted understanding}

## Knowledge Gaps Filled

{Before → After comparisons for major unknowns}

## Remaining Unknowns

{What's still uncertain or needs investigation}

## Investigation Tools Used

{Which tools/methods were effective}

## Context for Next Session

{Critical context for continuation}

## Recommended Next Steps

{Prioritized actions for next AI or next session}

## Artifacts Created

{Files, commits, documentation produced}
```

---

## Architecture Components

### 1. Report Generator

**File:** `empirica/core/handoff/report_generator.py`

**Class:** `EpistemicHandoffReportGenerator`

**Purpose:** Generate structured handoff reports during POSTFLIGHT

**Dependencies:**
- `empirica.data.session_database.SessionDatabase` (fetch assessments)
- `empirica.core.epistemic.vector_analysis` (calculate deltas)
- `empirica.calibration.calibration_validator` (check calibration)

**Key Methods:**

```python
class EpistemicHandoffReportGenerator:
    """
    Generate compressed epistemic handoff reports for session resumption

    Combines:
    - Vector deltas (what changed epistemically)
    - Key learnings (what was discovered)
    - Context (what next AI needs to know)
    - Recommendations (suggested next steps)
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db = SessionDatabase(db_path)
        self.vector_analyzer = VectorAnalyzer()
        self.calibration_validator = CalibrationValidator()

    def generate_handoff_report(
        self,
        session_id: str,
        task_summary: str,
        key_findings: List[str],
        remaining_unknowns: List[str],
        next_session_context: str,
        artifacts_created: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive handoff report

        Args:
            session_id: Session UUID
            task_summary: What was accomplished
            key_findings: What was learned (3-5 bullet points)
            remaining_unknowns: What's still unclear
            next_session_context: Critical context for next session
            artifacts_created: Files/commits produced

        Returns:
            {
                'session_id': str,
                'ai_id': str,
                'timestamp': str,
                'task_summary': str,
                'epistemic_deltas': Dict[str, float],
                'key_findings': List[str],
                'knowledge_gaps_filled': List[Dict],
                'remaining_unknowns': List[str],
                'investigation_tools': List[str],
                'next_session_context': str,
                'recommended_next_steps': List[str],
                'artifacts_created': List[str],
                'calibration_status': str,
                'markdown': str,  # Full markdown report
                'compressed_json': str  # Minimal JSON for storage
            }
        """
        # Fetch PREFLIGHT and POSTFLIGHT assessments
        preflight = self.db.get_preflight_assessment(session_id)
        postflight = self.db.get_postflight_assessment(session_id)

        if not preflight or not postflight:
            raise ValueError(f"Missing assessments for session {session_id}")

        # Calculate vector deltas
        deltas = self.vector_analyzer.calculate_deltas(
            preflight['vectors'],
            postflight['vectors']
        )

        # Check calibration
        calibration = self.calibration_validator.validate_calibration(
            session_id=session_id
        )

        # Identify knowledge gaps filled
        gaps_filled = self._identify_filled_gaps(
            preflight['vectors'],
            postflight['vectors'],
            key_findings
        )

        # Extract investigation tools used
        tools_used = self._extract_investigation_tools(session_id)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            postflight['vectors'],
            remaining_unknowns,
            calibration
        )

        # Get session metadata
        session_meta = self.db.get_session_metadata(session_id)

        # Build structured report
        report = {
            'session_id': session_id,
            'ai_id': session_meta.get('ai_id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'task_summary': task_summary,
            'duration_seconds': self._calculate_duration(session_id),
            'epistemic_deltas': deltas,
            'key_findings': key_findings,
            'knowledge_gaps_filled': gaps_filled,
            'remaining_unknowns': remaining_unknowns,
            'investigation_tools': tools_used,
            'next_session_context': next_session_context,
            'recommended_next_steps': recommendations,
            'artifacts_created': artifacts_created or [],
            'calibration_status': calibration['status'],
            'overall_confidence_delta': deltas.get('overall_confidence', 0.0)
        }

        # Generate markdown
        report['markdown'] = self._generate_markdown(report)

        # Generate compressed JSON (minimal, for storage)
        report['compressed_json'] = self._compress_report(report)

        return report

    def _identify_filled_gaps(
        self,
        preflight_vectors: Dict,
        postflight_vectors: Dict,
        key_findings: List[str]
    ) -> List[Dict]:
        """
        Identify which knowledge gaps were filled during session

        Returns:
            [
                {
                    'gap': 'Understanding of API patterns',
                    'before': 'Uncertain about factory methods',
                    'after': 'Fully documented Goal.create() and SubTask.create()',
                    'confidence_change': 0.25
                }
            ]
        """
        gaps = []

        # Check KNOW vector improvement
        know_delta = postflight_vectors.get('know', 0) - preflight_vectors.get('know', 0)
        if know_delta >= 0.15:  # Significant improvement
            gaps.append({
                'gap': 'Domain knowledge',
                'before': f"KNOW: {preflight_vectors.get('know', 0):.2f}",
                'after': f"KNOW: {postflight_vectors.get('know', 0):.2f}",
                'confidence_change': know_delta
            })

        # Check UNCERTAINTY reduction
        uncertainty_delta = preflight_vectors.get('uncertainty', 1) - postflight_vectors.get('uncertainty', 1)
        if uncertainty_delta >= 0.20:  # Significant reduction
            gaps.append({
                'gap': 'Task uncertainty',
                'before': f"UNCERTAINTY: {preflight_vectors.get('uncertainty', 1):.2f}",
                'after': f"UNCERTAINTY: {postflight_vectors.get('uncertainty', 1):.2f}",
                'confidence_change': uncertainty_delta
            })

        # Extract from key findings (heuristic)
        for finding in key_findings:
            if 'learned' in finding.lower() or 'discovered' in finding.lower():
                gaps.append({
                    'gap': 'Investigation finding',
                    'before': 'Unknown',
                    'after': finding,
                    'confidence_change': None
                })

        return gaps

    def _extract_investigation_tools(self, session_id: str) -> List[str]:
        """
        Extract which investigation tools were used during session

        Queries reflex logs for tool usage
        """
        tools_used = set()

        # Query reflex logs for tool mentions
        logs = self.db.query_reflex_logs(
            session_id=session_id,
            event_type='investigation'
        )

        for log in logs:
            if 'tool' in log:
                tools_used.add(log['tool'])

        return sorted(list(tools_used))

    def _generate_recommendations(
        self,
        postflight_vectors: Dict,
        remaining_unknowns: List[str],
        calibration: Dict
    ) -> List[str]:
        """
        Generate recommended next steps based on epistemic state
        """
        recommendations = []

        # Check if still high uncertainty
        if postflight_vectors.get('uncertainty', 0) > 0.40:
            recommendations.append(
                "Continue investigation - uncertainty still elevated"
            )

        # Check remaining unknowns
        if remaining_unknowns:
            recommendations.append(
                f"Address {len(remaining_unknowns)} remaining unknowns"
            )

        # Check calibration
        if calibration['status'] == 'overconfident':
            recommendations.append(
                "Validate assumptions - showing overconfidence pattern"
            )
        elif calibration['status'] == 'underconfident':
            recommendations.append(
                "Consider execution - showing underconfidence pattern"
            )

        # Check if ready for next phase
        if postflight_vectors.get('uncertainty', 1) < 0.30 and \
           postflight_vectors.get('know', 0) > 0.80:
            recommendations.append(
                "Ready for execution - strong epistemic foundation"
            )

        return recommendations

    def _generate_markdown(self, report: Dict) -> str:
        """Generate full markdown report"""
        # Implementation uses template above
        pass

    def _compress_report(self, report: Dict) -> str:
        """
        Generate minimal JSON for storage (~800 tokens)

        Strips verbose markdown, keeps critical data
        """
        compressed = {
            's': report['session_id'][:8],  # Short session ID
            'ai': report['ai_id'],
            'ts': report['timestamp'],
            'task': report['task_summary'][:200],  # Truncate
            'deltas': {
                k: round(v, 2) for k, v in report['epistemic_deltas'].items()
                if abs(v) >= 0.10  # Only significant deltas
            },
            'findings': [f[:150] for f in report['key_findings'][:5]],  # Top 5, truncate
            'unknowns': [u[:100] for u in report['remaining_unknowns'][:5]],
            'next': report['next_session_context'][:300],
            'recommend': [r[:100] for r in report['recommended_next_steps'][:3]],
            'calibrated': report['calibration_status']
        }

        return json.dumps(compressed, separators=(',', ':'))
```

---

### 2. Storage Layer

**Options:** Three storage backends for different use cases

#### Option A: Git Notes (Recommended - most efficient)

**Namespace:** `refs/notes/empirica/handoff/{session_id}`

**Advantages:**
- ✅ Distributed (travels with repo)
- ✅ Version controlled
- ✅ No database dependency
- ✅ Integrates with existing git checkpoint system

**Implementation:**

```python
class GitHandoffStorage:
    """Store handoff reports in git notes"""

    def store_handoff(self, session_id: str, report: Dict) -> str:
        """
        Store handoff report in git notes

        Returns:
            Note SHA
        """
        note_ref = f"empirica/handoff/{session_id}"
        compressed = report['compressed_json']

        result = subprocess.run(
            ['git', 'notes', '--ref', note_ref, 'add', '-f', '-m', compressed, 'HEAD'],
            capture_output=True, timeout=5, cwd='.', text=True
        )

        if result.returncode != 0:
            raise GitError(f"Failed to store handoff: {result.stderr}")

        # Also store full markdown as separate note
        markdown_ref = f"empirica/handoff/{session_id}/markdown"
        subprocess.run(
            ['git', 'notes', '--ref', markdown_ref, 'add', '-f', '-m', report['markdown'], 'HEAD'],
            capture_output=True, timeout=5, cwd='.', text=True
        )

        return self._get_note_sha(note_ref)

    def load_handoff(self, session_id: str, format: str = 'json') -> Dict:
        """
        Load handoff report from git notes

        Args:
            session_id: Session UUID
            format: 'json' or 'markdown'
        """
        note_ref = f"empirica/handoff/{session_id}"
        if format == 'markdown':
            note_ref += '/markdown'

        result = subprocess.run(
            ['git', 'notes', '--ref', note_ref, 'show', 'HEAD'],
            capture_output=True, timeout=2, cwd='.', text=True
        )

        if result.returncode != 0:
            return None

        if format == 'json':
            return json.loads(result.stdout)
        else:
            return {'markdown': result.stdout}
```

#### Option B: Session Database (Queryable)

**Table:** `handoff_reports`

**Schema:**

```sql
CREATE TABLE handoff_reports (
    session_id TEXT PRIMARY KEY,
    ai_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    task_summary TEXT,
    epistemic_deltas TEXT,  -- JSON
    key_findings TEXT,  -- JSON array
    remaining_unknowns TEXT,  -- JSON array
    next_session_context TEXT,
    recommended_next_steps TEXT,  -- JSON array
    calibration_status TEXT,
    compressed_json TEXT,  -- Full compressed report
    markdown_report TEXT,  -- Full markdown
    created_at REAL NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE INDEX idx_handoff_ai ON handoff_reports(ai_id);
CREATE INDEX idx_handoff_timestamp ON handoff_reports(timestamp);
```

**Advantages:**
- ✅ Fast queries (by AI, by date, by task type)
- ✅ No git dependency
- ✅ Integrates with existing session database

**Implementation:**

```python
class DatabaseHandoffStorage:
    """Store handoff reports in session database"""

    def store_handoff(self, session_id: str, report: Dict):
        """Store handoff report in database"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO handoff_reports
            (session_id, ai_id, timestamp, task_summary, epistemic_deltas,
             key_findings, remaining_unknowns, next_session_context,
             recommended_next_steps, calibration_status, compressed_json,
             markdown_report, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            report['ai_id'],
            report['timestamp'],
            report['task_summary'],
            json.dumps(report['epistemic_deltas']),
            json.dumps(report['key_findings']),
            json.dumps(report['remaining_unknowns']),
            report['next_session_context'],
            json.dumps(report['recommended_next_steps']),
            report['calibration_status'],
            report['compressed_json'],
            report['markdown'],
            time.time()
        ))
        self.conn.commit()

    def load_handoff(self, session_id: str) -> Optional[Dict]:
        """Load handoff report from database"""
        self.cursor.execute('''
            SELECT * FROM handoff_reports WHERE session_id = ?
        ''', (session_id,))

        row = self.cursor.fetchone()
        if not row:
            return None

        return self._row_to_dict(row)

    def query_handoffs(
        self,
        ai_id: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Query handoff reports by AI or date"""
        query = "SELECT * FROM handoff_reports WHERE 1=1"
        params = []

        if ai_id:
            query += " AND ai_id = ?"
            params.append(ai_id)

        if since:
            query += " AND timestamp >= ?"
            params.append(since)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        self.cursor.execute(query, params)
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]
```

#### Option C: Markdown Files (Human-readable)

**Location:** `docs/sessions/handoffs/{ai_id}/{session_id}.md`

**Advantages:**
- ✅ Human-readable in file system
- ✅ Version controlled (if committed)
- ✅ Easy to browse

**Implementation:**

```python
class MarkdownHandoffStorage:
    """Store handoff reports as markdown files"""

    def __init__(self, base_path: str = "docs/sessions/handoffs"):
        self.base_path = Path(base_path)

    def store_handoff(self, session_id: str, report: Dict):
        """Store handoff as markdown file"""
        ai_dir = self.base_path / report['ai_id']
        ai_dir.mkdir(parents=True, exist_ok=True)

        filepath = ai_dir / f"{session_id}.md"
        filepath.write_text(report['markdown'])

        # Also store compressed JSON sidecar
        json_path = ai_dir / f"{session_id}.json"
        json_path.write_text(report['compressed_json'])

    def load_handoff(self, session_id: str, ai_id: str) -> Optional[Dict]:
        """Load handoff report from markdown file"""
        filepath = self.base_path / ai_id / f"{session_id}.md"
        json_path = self.base_path / ai_id / f"{session_id}.json"

        if not filepath.exists():
            return None

        markdown = filepath.read_text()
        compressed = json.loads(json_path.read_text()) if json_path.exists() else {}

        return {
            'markdown': markdown,
            'compressed': compressed
        }
```

**Recommendation:** Use **Git Notes (Option A)** as primary, with **Database (Option B)** for querying. This gives best of both: distributed storage + fast queries.

---

### 3. MCP Tools for Handoff Reports

**File:** `mcp_local/empirica_mcp_server.py` (add new tools)

**New Tools:**

```python
@mcp.tool()
def generate_handoff_report(
    session_id: str,
    task_summary: str,
    key_findings: list[str],
    remaining_unknowns: list[str],
    next_session_context: str,
    artifacts_created: list[str] = None
) -> dict:
    """
    Generate epistemic handoff report for session

    Use during POSTFLIGHT to create compressed session summary for next AI.

    Args:
        session_id: Session UUID
        task_summary: What was accomplished (2-3 sentences)
        key_findings: What was learned (3-5 bullet points)
        remaining_unknowns: What's still unclear
        next_session_context: Critical context for next session
        artifacts_created: Files/commits produced

    Returns:
        {
            'session_id': str,
            'report_id': str,
            'markdown': str,
            'storage_location': str,
            'token_count': int
        }
    """
    generator = EpistemicHandoffReportGenerator()

    report = generator.generate_handoff_report(
        session_id=session_id,
        task_summary=task_summary,
        key_findings=key_findings,
        remaining_unknowns=remaining_unknowns,
        next_session_context=next_session_context,
        artifacts_created=artifacts_created
    )

    # Store in git notes + database
    git_storage = GitHandoffStorage()
    db_storage = DatabaseHandoffStorage()

    note_sha = git_storage.store_handoff(session_id, report)
    db_storage.store_handoff(session_id, report)

    # Estimate token count
    token_count = len(report['compressed_json']) // 4  # Rough estimate

    return {
        'session_id': session_id,
        'report_id': note_sha,
        'markdown': report['markdown'],
        'storage_location': f"git:refs/notes/empirica/handoff/{session_id}",
        'token_count': token_count,
        'status': 'success'
    }


@mcp.tool()
def resume_previous_session(
    ai_id: str = "claude",
    resume_mode: str = "last",
    session_id: str = None,
    count: int = 1,
    detail_level: str = "summary"
) -> dict:
    """
    Load summary of previous Empirica session(s) to resume work.

    Returns structured summary with:
    - Session metadata (when, duration, status)
    - Epistemic trajectory (PREFLIGHT → POSTFLIGHT delta)
    - Key accomplishments and learnings
    - Knowledge gaps that were filled
    - Investigation tools used
    - Next steps (if any)

    Use when starting a new session to catch up on previous work.

    Args:
        ai_id: AI agent identifier (defaults to 'claude')
        resume_mode: How to select session(s)
            - 'last': Most recent session only
            - 'last_n': N most recent sessions
            - 'session_id': Specific session by ID
        session_id: For 'session_id' mode: specific session to load
        count: For 'last_n' mode: how many recent sessions (1-5)
        detail_level: Amount of detail to return
            - 'summary': Key points only (~400 tokens)
            - 'detailed': + tools used, artifacts created (~800 tokens)
            - 'full': + all assessments, full markdown (~1,250 tokens)

    Returns:
        {
            'sessions': [
                {
                    'session_id': str,
                    'timestamp': str,
                    'duration': str,
                    'task': str,
                    'epistemic_deltas': dict,
                    'key_findings': list,
                    'knowledge_gaps_filled': list,
                    'remaining_unknowns': list,
                    'next_steps': list,
                    'investigation_tools': list,  # detailed/full only
                    'artifacts_created': list,  # detailed/full only
                    'full_markdown': str  # full only
                }
            ],
            'total_sessions': int,
            'token_estimate': int
        }
    """
    db = SessionDatabase()
    git_storage = GitHandoffStorage()

    # Determine which session(s) to load
    if resume_mode == "last":
        sessions = db.get_recent_sessions(ai_id=ai_id, limit=1)
    elif resume_mode == "last_n":
        sessions = db.get_recent_sessions(ai_id=ai_id, limit=min(count, 5))
    elif resume_mode == "session_id":
        if not session_id:
            raise ValueError("session_id required for 'session_id' mode")
        session = db.get_session(session_id)
        sessions = [session] if session else []
    else:
        raise ValueError(f"Invalid resume_mode: {resume_mode}")

    if not sessions:
        return {
            'sessions': [],
            'total_sessions': 0,
            'token_estimate': 0,
            'message': f"No sessions found for ai_id={ai_id}"
        }

    # Load handoff reports
    results = []
    total_tokens = 0

    for session in sessions:
        # Try git first, fallback to database
        handoff = git_storage.load_handoff(session['session_id'], format='json')
        if not handoff:
            db_storage = DatabaseHandoffStorage()
            handoff = db_storage.load_handoff(session['session_id'])

        if not handoff:
            # No handoff report - skip or generate minimal summary
            continue

        # Build response based on detail level
        result = {
            'session_id': handoff['s'],
            'ai_id': handoff['ai'],
            'timestamp': handoff['ts'],
            'task': handoff['task'],
            'epistemic_deltas': handoff['deltas'],
            'key_findings': handoff['findings'],
            'remaining_unknowns': handoff['unknowns'],
            'next_steps': handoff['recommend'],
            'calibration_status': handoff['calibrated']
        }

        if detail_level in ['detailed', 'full']:
            # Load full report for additional details
            full_report = git_storage.load_handoff(session['session_id'], format='markdown')
            # Extract tools/artifacts from markdown (or store separately)
            result['investigation_tools'] = []  # Parse from markdown
            result['artifacts_created'] = []  # Parse from markdown

        if detail_level == 'full':
            full_report = git_storage.load_handoff(session['session_id'], format='markdown')
            result['full_markdown'] = full_report['markdown']

        # Estimate tokens
        token_estimate = len(json.dumps(result)) // 4
        total_tokens += token_estimate

        results.append(result)

    return {
        'sessions': results,
        'total_sessions': len(results),
        'token_estimate': total_tokens,
        'detail_level': detail_level
    }


@mcp.tool()
def query_handoff_reports(
    ai_id: str = None,
    since: str = None,
    task_pattern: str = None,
    limit: int = 10
) -> dict:
    """
    Query handoff reports by AI, date, or task pattern

    Use for:
    - "What did Minimax work on last week?"
    - "Show recent testing sessions"
    - "What have all agents learned about git integration?"

    Args:
        ai_id: Filter by AI agent (e.g., 'minimax', 'claude-code')
        since: ISO timestamp or relative (e.g., '2025-11-01', '7 days ago')
        task_pattern: Regex pattern to match task summaries
        limit: Max results (default: 10)

    Returns:
        {
            'reports': [
                {
                    'session_id': str,
                    'ai_id': str,
                    'timestamp': str,
                    'task': str,
                    'key_findings': list,
                    'epistemic_growth': float  # Overall confidence delta
                }
            ],
            'total_found': int
        }
    """
    db_storage = DatabaseHandoffStorage()

    # Query database
    reports = db_storage.query_handoffs(
        ai_id=ai_id,
        since=since,
        limit=limit
    )

    # Filter by task pattern if provided
    if task_pattern:
        import re
        pattern = re.compile(task_pattern, re.IGNORECASE)
        reports = [r for r in reports if pattern.search(r['task_summary'])]

    # Format results
    results = []
    for report in reports:
        results.append({
            'session_id': report['session_id'],
            'ai_id': report['ai_id'],
            'timestamp': report['timestamp'],
            'task': report['task_summary'],
            'key_findings': json.loads(report['key_findings']),
            'epistemic_growth': report['epistemic_deltas'].get('overall_confidence', 0.0)
        })

    return {
        'reports': results,
        'total_found': len(results)
    }
```

---

### 4. CLI Integration

**File:** `empirica/cli.py` (add new functions)

```python
def generate_handoff_report(
    session_id: str,
    task_summary: str,
    key_findings: List[str],
    remaining_unknowns: List[str],
    next_session_context: str,
    artifacts_created: List[str] = None
) -> Dict:
    """
    Generate epistemic handoff report (wrapper for MCP tool)

    Usage:
        from empirica.cli import generate_handoff_report

        report = generate_handoff_report(
            session_id=session_id,
            task_summary="Validated Goal Architecture Phase 1",
            key_findings=[
                "All 4 test categories passed",
                "Performance <15ms for tracking",
                "API uses factory pattern with auto-ID"
            ],
            remaining_unknowns=[
                "Pytest environment issue (non-blocking)",
                "Long-term performance with 100+ goals"
            ],
            next_session_context="Phase 1 production-ready. Phase 2 (Git Notes) ready for validation.",
            artifacts_created=[
                "docs/current_work/GOAL_ARCHITECTURE_TEST_RESULTS.md",
                "docs/current_work/GOAL_ARCHITECTURE_BUGS.md"
            ]
        )

        print(f"✅ Handoff report: {report['report_id']}")
        print(f"📊 Token count: {report['token_count']}")
    """
    generator = EpistemicHandoffReportGenerator()

    report = generator.generate_handoff_report(
        session_id=session_id,
        task_summary=task_summary,
        key_findings=key_findings,
        remaining_unknowns=remaining_unknowns,
        next_session_context=next_session_context,
        artifacts_created=artifacts_created
    )

    # Store
    git_storage = GitHandoffStorage()
    db_storage = DatabaseHandoffStorage()

    note_sha = git_storage.store_handoff(session_id, report)
    db_storage.store_handoff(session_id, report)

    return {
        'session_id': session_id,
        'report_id': note_sha,
        'markdown': report['markdown'],
        'token_count': len(report['compressed_json']) // 4,
        'status': 'success'
    }


def resume_previous_session(
    ai_id: str = "claude",
    resume_mode: str = "last",
    session_id: str = None,
    count: int = 1,
    detail_level: str = "summary"
) -> Dict:
    """
    Load previous session handoff report(s)

    Usage:
        from empirica.cli import resume_previous_session

        # Load last session
        handoff = resume_previous_session(ai_id="minimax", resume_mode="last")

        print(f"Previous task: {handoff['sessions'][0]['task']}")
        print(f"Key findings: {handoff['sessions'][0]['key_findings']}")
        print(f"Next steps: {handoff['sessions'][0]['next_steps']}")

        # Load last 3 sessions with full detail
        recent = resume_previous_session(
            ai_id="claude-code",
            resume_mode="last_n",
            count=3,
            detail_level="full"
        )
    """
    # Implementation calls MCP tool or direct class method
    # (See MCP tool implementation above)
    pass
```

---

### 5. Workflow Integration

**Integration Point:** POSTFLIGHT phase

**File:** `empirica/workflows/postflight.py` (modify)

```python
def execute_postflight(
    session_id: str,
    task_summary: str,
    generate_handoff: bool = True  # NEW: Auto-generate handoff
) -> Dict:
    """
    Execute POSTFLIGHT assessment

    Args:
        session_id: Session UUID
        task_summary: What was accomplished
        generate_handoff: Auto-generate handoff report (default: True)
    """
    # Existing POSTFLIGHT logic
    # ...

    # NEW: Auto-generate handoff report
    if generate_handoff:
        try:
            # Prompt AI for handoff inputs
            print("\n📋 Generating handoff report...")
            print("Please provide:")
            print("1. Key findings (what you learned):")
            key_findings = []  # Collect from AI

            print("2. Remaining unknowns:")
            remaining_unknowns = []  # Collect from AI

            print("3. Context for next session:")
            next_context = ""  # Collect from AI

            print("4. Artifacts created (files/commits):")
            artifacts = []  # Collect from AI

            # Generate report
            from empirica.cli import generate_handoff_report

            handoff = generate_handoff_report(
                session_id=session_id,
                task_summary=task_summary,
                key_findings=key_findings,
                remaining_unknowns=remaining_unknowns,
                next_session_context=next_context,
                artifacts_created=artifacts
            )

            print(f"\n✅ Handoff report generated: {handoff['report_id']}")
            print(f"📊 Token count: {handoff['token_count']}")
            print(f"📍 Location: git:refs/notes/empirica/handoff/{session_id}")

            return {
                **result,  # Existing POSTFLIGHT result
                'handoff_report': handoff
            }

        except Exception as e:
            logger.warning(f"Failed to generate handoff report: {e}")
            # Don't fail POSTFLIGHT if handoff generation fails
            return result

    return result
```

---

### 6. Integration with Existing Systems

**Phase 1.5 Git Checkpoints:**
- Handoff reports complement checkpoints (semantic vs structural)
- Store in same git notes namespace (`empirica/...`)
- Use together for optimal context loading

**Session Database:**
- Store handoff reports alongside assessments
- Enable queries across sessions
- Track epistemic progression over time

**Goal Orchestrator:**
- Can query previous handoffs to inform goal generation
- Learn from past investigation strategies
- Avoid repeating failed approaches

**Calibration System:**
- Handoff reports include calibration status
- Enable tracking calibration improvement over time
- Identify systematic biases

---

## Implementation Plan

### Phase 1: Core Generator (2 hours)

**Tasks:**
1. Create `empirica/core/handoff/` directory
2. Implement `EpistemicHandoffReportGenerator` class
3. Add vector delta calculation
4. Add knowledge gap identification
5. Add recommendation generation
6. Add markdown template rendering
7. Add JSON compression

**Deliverable:** Working report generator with unit tests

---

### Phase 2: Storage Layer (1 hour)

**Tasks:**
1. Implement `GitHandoffStorage` (git notes)
2. Implement `DatabaseHandoffStorage` (session DB)
3. Add database migration for `handoff_reports` table
4. Add storage integration tests

**Deliverable:** Dual storage working (git + database)

---

### Phase 3: MCP Tools (1 hour)

**Tasks:**
1. Add `generate_handoff_report` MCP tool
2. Add `resume_previous_session` MCP tool
3. Add `query_handoff_reports` MCP tool
4. Add CLI wrappers in `empirica/cli.py`
5. Add MCP tool tests

**Deliverable:** 3 new MCP tools registered and tested

---

### Phase 4: Workflow Integration (30 min)

**Tasks:**
1. Modify `execute_postflight()` to prompt for handoff inputs
2. Add auto-generation option
3. Update POSTFLIGHT docs
4. Test end-to-end workflow

**Deliverable:** POSTFLIGHT auto-generates handoff reports

---

### Phase 5: Documentation & Testing (30 min)

**Tasks:**
1. Update CASCADE workflow docs
2. Add handoff report examples
3. Update CLAUDE.md system prompt
4. Create usage guide
5. End-to-end integration test

**Deliverable:** Complete documentation and examples

---

## Testing Strategy

### Unit Tests:

```python
# tests/unit/test_handoff_generator.py

def test_generate_handoff_report():
    """Test basic handoff report generation"""
    generator = EpistemicHandoffReportGenerator()

    report = generator.generate_handoff_report(
        session_id="test-session",
        task_summary="Test task",
        key_findings=["Finding 1", "Finding 2"],
        remaining_unknowns=["Unknown 1"],
        next_session_context="Continue testing"
    )

    assert 'session_id' in report
    assert 'epistemic_deltas' in report
    assert 'markdown' in report
    assert 'compressed_json' in report
    assert len(report['key_findings']) == 2

def test_identify_filled_gaps():
    """Test knowledge gap identification"""
    generator = EpistemicHandoffReportGenerator()

    preflight = {'know': 0.70, 'uncertainty': 0.65}
    postflight = {'know': 0.95, 'uncertainty': 0.20}

    gaps = generator._identify_filled_gaps(
        preflight, postflight, ["Learned API patterns"]
    )

    assert len(gaps) >= 2  # KNOW improvement + UNCERTAINTY reduction

def test_generate_recommendations():
    """Test recommendation generation"""
    generator = EpistemicHandoffReportGenerator()

    # High uncertainty case
    vectors = {'uncertainty': 0.60, 'know': 0.70}
    recommendations = generator._generate_recommendations(
        vectors, ["Unknown 1", "Unknown 2"], {'status': 'well_calibrated'}
    )

    assert any('investigation' in r.lower() for r in recommendations)

    # Ready for execution case
    vectors = {'uncertainty': 0.20, 'know': 0.90}
    recommendations = generator._generate_recommendations(
        vectors, [], {'status': 'well_calibrated'}
    )

    assert any('execution' in r.lower() or 'ready' in r.lower() for r in recommendations)

def test_compress_report():
    """Test JSON compression"""
    generator = EpistemicHandoffReportGenerator()

    full_report = {
        'session_id': 'a' * 36,
        'task_summary': 'x' * 500,
        'epistemic_deltas': {'know': 0.25, 'do': 0.05, 'context': 0.02},
        'key_findings': ['f' * 200] * 10
    }

    compressed = json.loads(generator._compress_report(full_report))

    # Should be significantly smaller
    assert len(compressed['s']) == 8  # Short session ID
    assert len(compressed['task']) <= 200  # Truncated
    assert len(compressed['deltas']) == 1  # Only significant deltas (>=0.10)
    assert len(compressed['findings']) <= 5  # Top 5 only
```

### Integration Tests:

```python
# tests/integration/test_handoff_workflow.py

def test_end_to_end_handoff():
    """Test complete handoff workflow"""
    # 1. Bootstrap session
    session_id = bootstrap_session()

    # 2. Execute PREFLIGHT
    execute_preflight(session_id, "Test task")
    submit_preflight_assessment(session_id, test_vectors)

    # 3. Execute POSTFLIGHT
    execute_postflight(session_id, "Task complete")
    submit_postflight_assessment(session_id, test_vectors_after)

    # 4. Generate handoff
    report = generate_handoff_report(
        session_id=session_id,
        task_summary="Test complete",
        key_findings=["Finding 1"],
        remaining_unknowns=["Unknown 1"],
        next_session_context="Continue"
    )

    assert report['status'] == 'success'
    assert report['token_count'] > 0

    # 5. Resume in new session
    handoff = resume_previous_session(ai_id="test", resume_mode="last")

    assert len(handoff['sessions']) == 1
    assert handoff['sessions'][0]['task'] == "Test complete"
    assert handoff['token_estimate'] < 2000  # Should be compressed

def test_git_storage():
    """Test git notes storage"""
    storage = GitHandoffStorage()

    test_report = {
        'session_id': 'test-123',
        'compressed_json': '{"test": "data"}',
        'markdown': '# Test Report'
    }

    # Store
    note_sha = storage.store_handoff('test-123', test_report)
    assert note_sha

    # Load JSON
    loaded = storage.load_handoff('test-123', format='json')
    assert loaded['test'] == 'data'

    # Load markdown
    loaded_md = storage.load_handoff('test-123', format='markdown')
    assert '# Test Report' in loaded_md['markdown']

def test_database_storage():
    """Test database storage and queries"""
    storage = DatabaseHandoffStorage()

    test_report = {
        'session_id': 'test-456',
        'ai_id': 'claude',
        'timestamp': datetime.now().isoformat(),
        'task_summary': 'Test task',
        'epistemic_deltas': {'know': 0.25},
        'key_findings': ['Finding 1'],
        'remaining_unknowns': [],
        'next_session_context': 'Continue',
        'recommended_next_steps': ['Step 1'],
        'calibration_status': 'well_calibrated',
        'compressed_json': '{}',
        'markdown': '# Test'
    }

    # Store
    storage.store_handoff('test-456', test_report)

    # Load
    loaded = storage.load_handoff('test-456')
    assert loaded['task_summary'] == 'Test task'

    # Query
    results = storage.query_handoffs(ai_id='claude', limit=1)
    assert len(results) >= 1
    assert results[0]['ai_id'] == 'claude'
```

---

## Usage Examples

### Example 1: Generate Handoff During POSTFLIGHT

```python
from empirica.bootstraps import bootstrap_metacognition
from empirica.cli import execute_postflight, submit_postflight_assessment, generate_handoff_report

# After completing work...
session_id = "your-session-id"

# Execute POSTFLIGHT
execute_postflight(session_id, "Validated Goal Architecture Phase 1")

# Submit assessment
submit_postflight_assessment(
    session_id=session_id,
    vectors={...},
    reasoning="Successfully validated all functionality"
)

# Generate handoff
handoff = generate_handoff_report(
    session_id=session_id,
    task_summary="Validated Goal Architecture Phase 1 - all tests passing",
    key_findings=[
        "All 4 test categories passed (pytest, MCP tools, input validation, git parsing)",
        "Performance excellent: <15ms for progress tracking",
        "API uses factory pattern: Goal.create() and SubTask.create() with auto-ID",
        "Only 1 minor environmental issue (pytest config, non-blocking)",
        "Production readiness confirmed"
    ],
    remaining_unknowns=[
        "Pytest environment configuration issue (causes silent failure)",
        "Long-term performance with 100+ goals not tested",
        "Production MCP tool response times need monitoring"
    ],
    next_session_context=(
        "Phase 1 complete and production-ready. "
        "Phase 2 (Git Notes Integration) implemented by RovoDev, needs validation. "
        "Focus areas: GitProgressQuery class, MCP tool naming, Phase 1+2 integration."
    ),
    artifacts_created=[
        "docs/current_work/GOAL_ARCHITECTURE_TEST_RESULTS.md",
        "docs/current_work/GOAL_ARCHITECTURE_BUGS.md",
        "manual_test_goals.py"
    ]
)

print(f"✅ Handoff report: {handoff['report_id']}")
print(f"📊 Token count: {handoff['token_count']}")
print(f"📍 Stored in: git:refs/notes/empirica/handoff/{session_id}")
```

### Example 2: Resume Previous Session

```python
from empirica.cli import resume_previous_session

# Start new session, load previous context
handoff = resume_previous_session(
    ai_id="minimax",
    resume_mode="last",
    detail_level="detailed"
)

if handoff['sessions']:
    prev = handoff['sessions'][0]

    print(f"""
📋 Previous Session Context:

   Task: {prev['task']}

   Epistemic Growth:
   {format_deltas(prev['epistemic_deltas'])}

   Key Findings:
   {format_list(prev['key_findings'])}

   Remaining Unknowns:
   {format_list(prev['remaining_unknowns'])}

   Recommended Next Steps:
   {format_list(prev['next_steps'])}

   Tools Used: {', '.join(prev['investigation_tools'])}

   Artifacts: {', '.join(prev['artifacts_created'])}
""")

    print(f"\n✅ Context loaded ({handoff['token_estimate']} tokens)")
    print("Ready to continue work...")
```

### Example 3: Query Team History

```python
from empirica.cli import query_handoff_reports

# What did all agents work on this week?
reports = query_handoff_reports(
    since="7 days ago",
    limit=20
)

print(f"\n📊 Team Activity (Last 7 Days):\n")

for report in reports['reports']:
    print(f"""
{'='*60}
Agent: {report['ai_id']}
Date: {report['timestamp']}
Task: {report['task']}

Key Findings:
{format_list(report['key_findings'])}

Epistemic Growth: {report['epistemic_growth']:+.2f}
{'='*60}
""")

# What did Minimax learn about testing?
minimax_testing = query_handoff_reports(
    ai_id="minimax",
    task_pattern="test|validation",
    limit=10
)

print(f"\n🔍 Minimax Testing Sessions: {minimax_testing['total_found']}")
```

### Example 4: Multi-Agent Coordination

```python
# Lead AI querying team progress

from empirica.cli import resume_previous_session

# Load all recent sessions from team
claude_work = resume_previous_session(ai_id="claude-code", resume_mode="last")
minimax_work = resume_previous_session(ai_id="minimax", resume_mode="last")
rovodev_work = resume_previous_session(ai_id="rovodev", resume_mode="last")

# Synthesize team status
print(f"""
🚀 Team Status Summary:

Claude (Co-Lead):
  Task: {claude_work['sessions'][0]['task']}
  Status: {claude_work['sessions'][0]['calibration_status']}
  Next: {claude_work['sessions'][0]['next_steps'][0]}

Minimax (Testing):
  Task: {minimax_work['sessions'][0]['task']}
  Status: {minimax_work['sessions'][0]['calibration_status']}
  Next: {minimax_work['sessions'][0]['next_steps'][0]}

RovoDev (Implementation):
  Task: {rovodev_work['sessions'][0]['task']}
  Status: {rovodev_work['sessions'][0]['calibration_status']}
  Next: {rovodev_work['sessions'][0]['next_steps'][0]}

📋 Coordination Notes:
- All agents well-calibrated
- No blocking unknowns
- Ready for Phase 2 validation handoff to Minimax
""")
```

---

## Success Metrics

### Token Efficiency:
- **Target:** 93.75% reduction vs baseline (20,000 → 1,250 tokens)
- **Measurement:** Track actual token usage in `resume_previous_session()`
- **Validation:** Compare compressed JSON size vs full conversation history

### Context Transfer Speed:
- **Target:** 95% faster handoffs (10 min → 30 sec)
- **Measurement:** Time from session end to next AI ready to work
- **Validation:** Benchmark with/without handoff reports

### Semantic Completeness:
- **Target:** Next AI can resume work without asking clarifying questions
- **Measurement:** Track "context gap" questions in resumed sessions
- **Validation:** Compare question count with/without handoff reports

### Multi-Agent Coordination:
- **Target:** Zero duplicate work across agents
- **Measurement:** Track overlap in investigation areas
- **Validation:** Query handoff reports for redundant work

---

## Documentation Updates

### Files to Update:

1. **docs/production/01_QUICK_START.md**
   - Add handoff report generation to POSTFLIGHT section
   - Add session resumption example

2. **docs/production/06_CASCADE_FLOW.md**
   - Update POSTFLIGHT phase to include handoff generation
   - Add "Resuming Work" section with examples

3. **docs/guides/GIT_CHECKPOINTS_GUIDE.md**
   - Add handoff reports as complementary to checkpoints
   - Show combined usage for optimal efficiency

4. **CLAUDE.md** (system prompt)
   - Add handoff report generation to POSTFLIGHT instructions
   - Add `resume_previous_session()` to quick reference

5. **README.md**
   - Add Phase 1.6 to feature list
   - Update token efficiency claims (93.75% reduction)

6. **docs/architecture/** (new file)
   - This spec document as architectural reference

---

## Risks & Mitigations

### Risk 1: AI Forgets to Generate Handoff

**Impact:** Next session lacks context

**Mitigation:**
- Auto-prompt during POSTFLIGHT
- Make generation optional but default-on
- Add reminder to system prompt

### Risk 2: Handoff Reports Incomplete

**Impact:** Insufficient context for resumption

**Mitigation:**
- Clear prompts for required fields
- Validation before storage
- Fallback to conversation history if needed

### Risk 3: Storage Failures

**Impact:** Handoff report not saved

**Mitigation:**
- Dual storage (git + database)
- Graceful degradation (don't fail POSTFLIGHT)
- Retry logic for git operations

### Risk 4: Token Estimates Inaccurate

**Impact:** Unexpectedly high token usage

**Mitigation:**
- Actual token counting (not estimation)
- Truncation limits in compression
- Monitoring and adjustment

---

## Future Enhancements (Post-Launch)

### Phase 1.7: Semantic Search
- Vector embeddings for handoff reports
- "Find sessions similar to current task"
- Cross-agent learning transfer

### Phase 1.8: Automated Handoff Chains
- Lead AI automatically routes work based on handoffs
- "Minimax finished testing → Claude validates → Gemini optimizes"

### Phase 1.9: Handoff Visualization
- Web UI showing epistemic trajectories
- Timeline view of multi-agent coordination
- Knowledge graph of learnings

---

## Acceptance Criteria

**Definition of Done:**

- [x] Spec document complete (this document)
- [ ] `EpistemicHandoffReportGenerator` class implemented
- [ ] Git notes storage working
- [ ] Database storage working
- [ ] 3 MCP tools registered (`generate_handoff_report`, `resume_previous_session`, `query_handoff_reports`)
- [ ] CLI wrappers in `empirica/cli.py`
- [ ] POSTFLIGHT auto-generation integrated
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing (end-to-end workflow)
- [ ] Documentation updated (5 files)
- [ ] Token efficiency validated (<1,500 tokens for detailed resume)
- [ ] Example usage scripts working
- [ ] Handoff to Copilot Claude complete

---

## Handoff to Copilot Claude

**Implementation Owner:** Copilot Claude

**Estimated Effort:** 4-6 hours

**Priority:** HIGH - Enables seamless multi-agent coordination

**Prerequisites:**
- ✅ Phase 1.5 (Git Checkpoints) complete
- ✅ Session database operational
- ✅ MCP server running
- ✅ PREFLIGHT/POSTFLIGHT workflow stable

**Deliverables:**
1. Working handoff report generator
2. Dual storage (git + database)
3. 3 new MCP tools
4. Updated CASCADE workflow
5. Complete documentation
6. Passing tests

**Testing Validation:**
1. Generate handoff for test session
2. Resume session in fresh context
3. Verify <1,500 tokens loaded
4. Query team history
5. End-to-end multi-agent scenario

**Success Criteria:**
- Token efficiency: 93.75% reduction vs baseline
- Context transfer: <30 seconds (vs 10 minutes)
- Zero context gaps (no clarifying questions needed)
- All tests passing

---

**Questions for Copilot Claude?** See "Architecture Components" section for detailed implementation guidance.

**Ready to implement!** 🚀

---

**Document Version:** 1.0
**Author:** Claude (Co-Lead)
**Date:** 2025-11-17
**Status:** Ready for Handoff
