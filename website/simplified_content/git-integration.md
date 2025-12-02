# Git Integration: Epistemic Infrastructure

**Git as cognitive infrastructure for distributed AI reasoning.**

Empirica uses **git notes** to store compressed epistemic state directly in your repository, enabling seamless handoffs and 80-97.5% token reduction.

---

## Why Git Notes?

<!-- BENTO_START -->

## 🌍 Distributed by Design
**No central server required.**

- Works offline
- Container-native coordination
- Syncs with `git fetch/push`

## 📊 Token Efficient
**Massive reduction in context size.**

- Checkpoints: 97.5% reduction
- Handoffs: 98% reduction  
- Goals: Compressed epistemic state

## 🔗 Cross-AI Coordination
**Seamless collaboration.**

- Discover goals from other AIs
- Resume work with epistemic transfer
- Track lineage (who worked on what)

<!-- BENTO_END -->

---

## Three Core Use Cases

### 1. Checkpoints (97.5% Token Reduction)

**Automatic epistemic snapshots** during CASCADE phases.

```bash
# Automatic during CASCADE
empirica preflight "Implement feature X"
# → Checkpoint created in git notes

# Manual checkpoint
empirica checkpoint-create --session-id latest --phase PREFLIGHT
```

**Stored in:** `refs/notes/empirica/checkpoints`

**What's saved:**
- 13 epistemic vectors (engagement, know, uncertainty, etc.)
- Phase (PREFLIGHT/CHECK/POSTFLIGHT)
- Timestamp
- Metadata

**Result:** ~500 tokens instead of ~6,500 (full session history)

---

### 2. Goal Discovery (Cross-AI)

**Share goals across AIs** via git notes.

```bash
# AI-1 creates goal
empirica goals-create --objective "Implement rate limiting"

# AI-2 discovers goals from AI-1
empirica goals-discover --from-ai-id "claude-code"

# AI-2 resumes AI-1's goal
empirica goals-resume --goal-id <uuid>
```

**Stored in:** `refs/notes/empirica/goals/{goal-id}`

**Enables:**
- Multi-AI projects
- Specialist handoffs (Security AI → Payment AI)
- Load balancing across AIs

---

### 3. Handoff Reports (98% Token Reduction)

**Compress session summaries** for continuity.

```bash
# Create handoff at session end
empirica handoff-create \
  --session-id latest \
  --task-summary "OAuth implementation complete" \
  --key-findings "Token bucket pattern optimal"

# Next session loads handoff
empirica sessions-resume --ai-id your-id
```

**Stored in:** `refs/notes/empirica/handoff/{session-id}`

**Result:** 238-400 tokens instead of ~20,000 (full conversation)

---

## Safe Degradation

**Works everywhere:**

```
✅ Git repository → Uses git notes (optimal)
✅ Non-git directory → Falls back to SQLite
✅ CI/CD pipeline → Graceful degradation
✅ Docker container → No git required
```

All git operations fail gracefully. Empirica never crashes due to missing git.

---

## Unified Architecture

```
refs/notes/empirica/
├── checkpoints          # Epistemic snapshots (97.5% reduction)
├── goals/{goal-id}      # Cross-AI goal sharing
└── handoff/{session-id} # Session continuity (98% reduction)

Infrastructure:
└── session_sync.py      # Git sync layer (pull/push)
```

**Clean, unified, distributed.**

---

## Sync Across Remotes

```bash
# Push git notes to remote
git push origin refs/notes/empirica/checkpoints
git push origin refs/notes/empirica/goals/*
git push origin refs/notes/empirica/handoff/*

# Fetch git notes from remote
git fetch origin refs/notes/empirica/checkpoints:refs/notes/empirica/checkpoints
```

**Result:** Team member B's AI reconstructs member A's AI reasoning state.

---

## Key Takeaway

**Git is cognitive infrastructure.**

- **Checkpoints** = Compressed epistemic snapshots
- **Goals** = Cross-AI coordination
- **Handoffs** = Session continuity
- **Notes** = Distributed, versioned, auditable

**Token savings:** 80-98% reduction vs. traditional context loading.

---

**Next Steps:**
- [Architecture](developers/architecture.md)
- [Collaboration](developers/collaboration.md)
- [Full Git Integration Guide](../docs/guides/git_integration.md)
