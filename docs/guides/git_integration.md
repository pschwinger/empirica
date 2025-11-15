# Empirica Git Integration Guide

**Phase 2: Git-Native Epistemic Checkpoints**  
**Version:** 1.0  
**Date:** November 15, 2025  
**Status:** Production Ready ✅

---

## Overview

Empirica uses **git notes** to store epistemic checkpoints directly in your repository's git history. This creates a distributed, versioned, auditable record of AI reasoning that travels with your code.

**Why Git Notes?**
- ✅ **Zero additional infrastructure** - uses existing git
- ✅ **Distributed** - checkpoints sync with `git fetch`
- ✅ **Auditable** - full history in `git log --show-notes`
- ✅ **Portable** - works across providers (Claude, Qwen, local)
- ✅ **Efficient** - only stores epistemic deltas (13 vectors + metadata)

---

## Quick Start

### 1. Automatic Checkpoints in CASCADE

Empirica automatically creates checkpoints during CASCADE execution:

```python
from empirica.cascade import CASCADE

# CASCADE automatically checkpoints at each phase
cascade = CASCADE(session_id="my-task")

# Checkpoint created at PREFLIGHT
cascade.preflight(
    task="Implement feature X",
    context={"repo": "/path/to/repo"}
)

# Checkpoint created at INVESTIGATION
cascade.investigate()

# Checkpoint created at POSTFLIGHT
cascade.postflight()

# Access checkpoint history
checkpoints = cascade.list_checkpoints()
print(f"Created {len(checkpoints)} checkpoints")
```

**What gets stored:**
- 13 epistemic vectors (engagement, knowledge, uncertainty, etc.)
- Phase name (PREFLIGHT/INVESTIGATE/POSTFLIGHT)
- Round number
- Timestamp
- Compression ratio (for token efficiency tracking)

---

### 2. Manual Checkpoint Creation

Use CLI for explicit checkpoint management:

```bash
# Create checkpoint
empirica checkpoint-create \
    --session-id "feature-x-implementation" \
    --phase "PREFLIGHT" \
    --round 1

# Load latest checkpoint
empirica checkpoint-load --session-id "feature-x-implementation"

# List all checkpoints
empirica checkpoint-list --session-id "feature-x-implementation"

# Compare checkpoints
empirica checkpoint-diff \
    --session-id "feature-x-implementation" \
    --from-round 1 \
    --to-round 3

# Get efficiency report
empirica efficiency-report \
    --session-id "feature-x-implementation" \
    --format json
```

---

## Architecture

### Git Notes Structure

Empirica stores checkpoints in `refs/notes/empirica/checkpoints`:

```
refs/notes/empirica/
├── checkpoints          # Main checkpoint storage
│   ├── session-123-r1   # Round 1 checkpoint
│   ├── session-123-r2   # Round 2 checkpoint
│   └── session-123-r3   # Round 3 checkpoint
└── metadata            # Session metadata (optional)
```

**Each checkpoint contains:**

```json
{
  "session_id": "feature-x-implementation",
  "phase": "PREFLIGHT",
  "round": 1,
  "timestamp": "2025-11-15T11:00:00.000Z",
  "vectors": {
    "engagement": 0.75,
    "know": 0.65,
    "do": 0.70,
    "context": 0.60,
    "clarity": 0.70,
    "coherence": 0.75,
    "signal": 0.65,
    "density": 0.60,
    "state": 0.50,
    "change": 0.45,
    "completion": 0.40,
    "impact": 0.55,
    "uncertainty": 0.35
  },
  "compression_ratio": 0.42,
  "token_efficiency": {
    "saved_tokens": 1200,
    "checkpoint_tokens": 500
  }
}
```

---

### Fallback Strategy

Empirica uses **graceful fallback** when git is unavailable:

```
1. Try git notes (primary)
   └─ Success → use git checkpoint
   └─ Fail → fallback to SQLite

2. Try SQLite reflexes table (fallback)
   └─ Success → use latest reflex
   └─ Fail → return None (graceful)

3. Never crash on missing checkpoint
   └─ Session continues without checkpoint
```

This ensures Empirica works in:
- ✅ Git repositories
- ✅ Non-git directories
- ✅ CI/CD pipelines without git
- ✅ Docker containers
- ✅ Restricted environments

---

## CLI Commands Reference

### checkpoint-create

Create a new checkpoint.

```bash
empirica checkpoint-create \
    --session-id <SESSION_ID> \
    --phase <PHASE> \
    --round <ROUND> \
    [--force]
```

**Options:**
- `--session-id`: Session identifier (required)
- `--phase`: CASCADE phase (PREFLIGHT/INVESTIGATE/POSTFLIGHT) (required)
- `--round`: Round number (required)
- `--force`: Overwrite existing checkpoint

**Example:**
```bash
empirica checkpoint-create \
    --session-id "auth-system-refactor" \
    --phase "INVESTIGATE" \
    --round 2
```

---

### checkpoint-load

Load the latest checkpoint for a session.

```bash
empirica checkpoint-load \
    --session-id <SESSION_ID> \
    [--round <ROUND>] \
    [--format json|yaml]
```

**Options:**
- `--session-id`: Session identifier (required)
- `--round`: Specific round to load (optional, defaults to latest)
- `--format`: Output format (default: json)

**Example:**
```bash
# Load latest
empirica checkpoint-load --session-id "auth-system-refactor"

# Load specific round
empirica checkpoint-load --session-id "auth-system-refactor" --round 2
```

**Output:**
```json
{
  "phase": "INVESTIGATE",
  "round": 2,
  "vectors": { ... },
  "timestamp": "2025-11-15T11:00:00.000Z"
}
```

---

### checkpoint-list

List all checkpoints for a session.

```bash
empirica checkpoint-list \
    --session-id <SESSION_ID> \
    [--format table|json|yaml]
```

**Options:**
- `--session-id`: Session identifier (required)
- `--format`: Output format (default: table)

**Example:**
```bash
empirica checkpoint-list --session-id "auth-system-refactor"
```

**Output (table format):**
```
Round | Phase        | Timestamp           | Know | Uncertainty
------|--------------|---------------------|------|------------
1     | PREFLIGHT    | 2025-11-15 10:00:00 | 0.65 | 0.40
2     | INVESTIGATE  | 2025-11-15 10:30:00 | 0.82 | 0.25
3     | POSTFLIGHT   | 2025-11-15 11:00:00 | 0.89 | 0.12
```

---

### checkpoint-diff

Compare two checkpoints.

```bash
empirica checkpoint-diff \
    --session-id <SESSION_ID> \
    [--from-round <ROUND>] \
    [--to-round <ROUND>] \
    [--format json|yaml|table]
```

**Options:**
- `--session-id`: Session identifier (required)
- `--from-round`: Starting round (default: first)
- `--to-round`: Ending round (default: latest)
- `--format`: Output format (default: json)

**Example:**
```bash
empirica checkpoint-diff \
    --session-id "auth-system-refactor" \
    --from-round 1 \
    --to-round 3
```

**Output:**
```json
{
  "session_id": "auth-system-refactor",
  "from_round": 1,
  "to_round": 3,
  "deltas": {
    "know": 0.24,
    "uncertainty": -0.28,
    "completion": 0.50
  },
  "trajectory": "positive"
}
```

---

### efficiency-report

Generate token efficiency report.

```bash
empirica efficiency-report \
    --session-id <SESSION_ID> \
    [--format json|markdown] \
    [--output <FILE>]
```

**Options:**
- `--session-id`: Session identifier (required)
- `--format`: Output format (default: json)
- `--output`: Save to file (optional)

**Example:**
```bash
empirica efficiency-report \
    --session-id "auth-system-refactor" \
    --format markdown \
    --output report.md
```

**Output:**
```markdown
# Token Efficiency Report

**Session:** auth-system-refactor  
**Rounds:** 3  
**Total Tokens Saved:** 3,600

## Checkpoint Efficiency

| Round | Phase       | Saved | Checkpoint | Ratio |
|-------|-------------|-------|-----------|--------|
| 1     | PREFLIGHT   | 1,200 | 500       | 0.42   |
| 2     | INVESTIGATE | 1,500 | 600       | 0.40   |
| 3     | POSTFLIGHT  | 900   | 400       | 0.44   |

**Average Compression:** 42% token reduction
```

---

## Python API

### CASCADE Integration

```python
from empirica.cascade import CASCADE

# CASCADE handles checkpoints automatically
cascade = CASCADE(session_id="my-task")

# Access checkpoint data
checkpoint = cascade.get_current_checkpoint()
print(f"Current phase: {checkpoint['phase']}")
print(f"Knowledge: {checkpoint['vectors']['know']}")

# List all checkpoints
history = cascade.list_checkpoints()
for cp in history:
    print(f"Round {cp['round']}: {cp['phase']} - Know={cp['vectors']['know']}")
```

---

### SessionDatabase API

```python
from empirica.data.session_database import SessionDatabase

db = SessionDatabase()

# Get latest checkpoint (tries git, falls back to SQLite)
checkpoint = db.get_git_checkpoint(session_id="my-task")

if checkpoint:
    print(f"Source: {checkpoint['source']}")  # 'git' or 'sqlite_fallback'
    print(f"Vectors: {checkpoint['vectors']}")

# List all checkpoints
checkpoints = db.list_git_checkpoints(session_id="my-task")

# Get checkpoint diff
diff = db.get_checkpoint_diff(
    session_id="my-task",
    from_round=1,
    to_round=3
)
print(f"Knowledge delta: {diff['deltas']['know']}")
```

---

### Low-Level Git Notes API

```python
from empirica.utils.git_notes_manager import GitNotesManager

manager = GitNotesManager()

# Check if git is available
if manager.is_git_available():
    # Create checkpoint
    success = manager.create_checkpoint(
        session_id="my-task",
        phase="PREFLIGHT",
        round_num=1,
        vectors={...},
        compression_ratio=0.42
    )
    
    # Load checkpoint
    checkpoint = manager.load_checkpoint(
        session_id="my-task",
        round_num=1
    )
    
    # List all checkpoints
    checkpoints = manager.list_checkpoints(session_id="my-task")
```

---

## Advanced Usage

### Cross-Provider Handoff

Checkpoints enable seamless handoff between AI providers:

```python
# Claude session creates checkpoint
claude_cascade = CASCADE(
    session_id="shared-task",
    ai_id="claude-3.5-sonnet"
)
claude_cascade.preflight(task="Start feature X")
# Checkpoint stored in git notes

# Qwen session loads checkpoint
qwen_cascade = CASCADE(
    session_id="shared-task",
    ai_id="qwen-2.5-coder"
)
checkpoint = qwen_cascade.get_current_checkpoint()
# Qwen reconstructs Claude's reasoning from vectors
qwen_cascade.investigate()  # Continues from where Claude left off
```

**Token savings:** ~40% vs. passing full context

---

### Distributed Teams

Git notes sync across remotes:

```bash
# Team member A creates checkpoint
empirica checkpoint-create --session-id "project-x" --phase "PREFLIGHT" --round 1

# Commit and push
git commit -m "Feature X initial work"
git push origin main

# Push git notes
git push origin refs/notes/empirica/checkpoints

# Team member B pulls
git pull origin main
git fetch origin refs/notes/empirica/checkpoints:refs/notes/empirica/checkpoints

# Load checkpoint
empirica checkpoint-load --session-id "project-x"
```

**Result:** Team member B's AI reconstructs member A's AI reasoning state.

---

### Audit Trail

View complete reasoning history:

```bash
# View checkpoint history
git log --show-notes=empirica/checkpoints

# Export checkpoint trajectory
empirica checkpoint-list --session-id "project-x" --format json > trajectory.json

# Analyze epistemic deltas
empirica checkpoint-diff \
    --session-id "project-x" \
    --from-round 1 \
    --to-round 10 \
    --format json > deltas.json
```

Use this for:
- ✅ Debugging AI reasoning
- ✅ Training local models (epistemic deltas as training data)
- ✅ Performance optimization
- ✅ Compliance audits

---

## Configuration

### Git Notes Setup

Git notes are created automatically by Empirica. To manually configure:

```bash
# View git notes configuration
git config --list | grep notes

# Set default notes ref (optional, Empirica does this)
git config notes.rewriteRef refs/notes/empirica/checkpoints

# Push notes to remote
git push origin refs/notes/empirica/checkpoints
```

---

### Environment Variables

```bash
# Disable git integration (force SQLite fallback)
export EMPIRICA_DISABLE_GIT=1

# Change git notes namespace
export EMPIRICA_GIT_NOTES_REF=refs/notes/empirica/custom

# Verbose git logging
export EMPIRICA_GIT_VERBOSE=1
```

---

## Testing

Run integration tests:

```bash
# Test CASCADE git integration
pytest tests/integration/test_cascade_git_integration.py

# Test CLI commands
pytest tests/integration/test_cli_checkpoint_commands.py

# Test SessionDatabase git methods
pytest tests/integration/test_session_database_git.py

# Run all git integration tests
pytest tests/integration/test_*git*.py -v
```

---

## Troubleshooting

### Checkpoints not appearing

**Problem:** `checkpoint-list` returns empty

**Solution:**
1. Check if git is available: `git --version`
2. Check if you're in a git repo: `git rev-parse --git-dir`
3. Check if notes exist: `git notes --ref=empirica/checkpoints list`
4. Enable verbose logging: `export EMPIRICA_GIT_VERBOSE=1`

---

### Git notes not syncing

**Problem:** Checkpoints don't appear on remote

**Solution:**
```bash
# Explicitly push notes
git push origin refs/notes/empirica/checkpoints

# Configure automatic note syncing
git config notes.rewriteRef refs/notes/empirica/checkpoints
git config remote.origin.push '+refs/notes/empirica/checkpoints:refs/notes/empirica/checkpoints'
```

---

### SQLite fallback always used

**Problem:** Even in git repo, using SQLite

**Solution:**
1. Check `EMPIRICA_DISABLE_GIT` env var
2. Verify git repo: `git status`
3. Check permissions: `ls -la .git/`
4. Try manual checkpoint: `empirica checkpoint-create --session-id test --phase PREFLIGHT --round 1`

---

## Best Practices

### 1. Session IDs

Use descriptive, consistent session IDs:

```python
# ✅ Good
session_id = "auth-system-refactor-2025-11-15"

# ❌ Bad
session_id = "session-123"
```

---

### 2. Checkpoint Frequency

- ✅ **PREFLIGHT:** Always checkpoint before investigation
- ✅ **INVESTIGATE:** Checkpoint after major discoveries
- ✅ **POSTFLIGHT:** Always checkpoint after completion

**Avoid:** Checkpointing every minor step (creates noise)

---

### 3. Git Notes Syncing

```bash
# Add to .git/config for automatic sync
[remote "origin"]
    push = +refs/heads/*:refs/heads/*
    push = +refs/notes/empirica/checkpoints:refs/notes/empirica/checkpoints
    fetch = +refs/notes/empirica/checkpoints:refs/notes/empirica/checkpoints
```

---

### 4. Checkpoint Cleanup

Old checkpoints are kept for audit trail. To clean up:

```bash
# List all checkpoint notes
git notes --ref=empirica/checkpoints list

# Remove specific checkpoint (careful!)
git notes --ref=empirica/checkpoints remove <commit-sha>
```

---

## Performance

### Token Efficiency

Checkpoints reduce token usage by ~40%:

```
Traditional handoff:
├─ Full context: 3,000 tokens
├─ Reasoning history: 2,000 tokens
└─ Total: 5,000 tokens

With checkpoint:
├─ Checkpoint: 500 tokens (13 vectors + metadata)
├─ Minimal context: 2,000 tokens
└─ Total: 2,500 tokens

Savings: 50% reduction
```

---

### Storage Overhead

Checkpoints are compact:

```
Per checkpoint:
├─ Vectors: ~200 bytes (13 floats)
├─ Metadata: ~150 bytes
└─ Total: ~350 bytes

100 checkpoints = 35 KB
1000 checkpoints = 350 KB
```

**Negligible** compared to code repository size.

---

## Future Roadmap

### Phase 3: Delta-Based Training (Q1 2026)

Use checkpoints as training data for local models:

```python
# Collect epistemic deltas
deltas = []
for session in all_sessions:
    checkpoints = db.list_git_checkpoints(session)
    delta = compute_delta(checkpoints[0], checkpoints[-1])
    deltas.append(delta)

# Train local model on reasoning trajectories
train_local_model(deltas, model="ouro-looplm")

# Use trained model for new sessions
cascade = CASCADE(ai_id="local-trained-model")
```

**Result:** Self-improving system that learns from its own reasoning history.

---

## Summary

Empirica's git integration provides:

✅ **Distributed** - Epistemic state travels with code  
✅ **Efficient** - 40% token reduction via compression  
✅ **Auditable** - Full reasoning history in git  
✅ **Portable** - Works across AI providers  
✅ **Resilient** - Graceful fallback to SQLite  

**Next steps:**
1. Run `pytest tests/integration/test_*git*.py` to verify setup
2. Try `empirica checkpoint-create` in your repo
3. Explore checkpoint history with `git log --show-notes`
4. Read `/home/yogapad/empirical-ai/empirica/COPILOT_CLAUDE_NEXT_TASKS.md` for Phase 3 roadmap

---

**Version:** 1.0  
**Last Updated:** November 15, 2025  
**License:** See LICENSE file
