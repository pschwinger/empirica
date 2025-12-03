# Learning Deltas → Code Commits: Correlation & Signing Design

**Date:** 2025-12-02  
**Problem:** How do epistemic deltas map to actual code changes and crypto signatures?

---

## 🎯 The Core Problem

### Current State

**Epistemic tracking (git notes):**
```
PREFLIGHT: KNOW=0.6, DO=0.7
CHECK:     KNOW=0.7, DO=0.8
ACT:       KNOW=0.8, DO=0.9
POSTFLIGHT: KNOW=0.9, DO=0.95
```

**Code commits (maybe):**
```
b531d53: feat: improve auth.py
f13d167: feat: add timeout handling
```

**Question:** How do we correlate KNOW: 0.6 → 0.9 with those commits?

---

## 🔍 Current Architecture Gap

### What We Track Now

**Checkpoints (in git notes):**
```json
{
  "session_id": "abc-123",
  "phase": "POSTFLIGHT",
  "vectors": {"know": 0.9, "do": 0.95},
  "timestamp": "2025-12-02T12:00:00Z",
  "meta": {"task": "improve auth module"}
}
```

**What's MISSING:**
- ❌ No link to code commits
- ❌ No file change tracking
- ❌ No learning attribution (what caused KNOW to increase?)
- ❌ Signatures don't include code commit SHAs

---

## 💡 Proposed Solution: Multi-Level Correlation

### Level 1: Timestamp Correlation (Always Available)

**Concept:** Use timestamps to correlate checkpoints with commits

```python
def get_commits_between_checkpoints(checkpoint_prev, checkpoint_curr):
    """Get all commits between two checkpoints"""
    return git_log(
        since=checkpoint_prev['timestamp'],
        until=checkpoint_curr['timestamp']
    )
```

**Advantages:**
- ✅ Always works (no code changes needed)
- ✅ Post-hoc analysis possible
- ✅ Works even if user commits manually

**Disadvantages:**
- ⚠️ Correlation is approximate (time-based only)
- ⚠️ Doesn't capture uncommitted changes

---

### Level 2: Explicit Tracking (Enhanced Checkpoints)

**Concept:** Capture git state at checkpoint time

#### Implementation: Enhanced Checkpoint Schema

```json
{
  "session_id": "abc-123",
  "phase": "POSTFLIGHT",
  "round": 1,
  "timestamp": "2025-12-02T12:00:00Z",
  "vectors": {"know": 0.9, "do": 0.95, "context": 0.85},
  "overall_confidence": 0.9,
  
  // NEW: Git state capture
  "git_state": {
    "head_commit": "b531d53",
    "commits_since_last_checkpoint": [
      {
        "sha": "f13d167",
        "message": "feat: add timeout handling",
        "author": "User Name",
        "timestamp": "2025-12-02T11:55:00Z",
        "files_changed": ["timeout.py", "config.py"],
        "insertions": 45,
        "deletions": 12
      }
    ],
    "uncommitted_changes": {
      "files_modified": ["auth.py"],
      "files_added": [],
      "files_deleted": [],
      "diff_stat": "+25 -5"
    }
  },
  
  // NEW: Learning delta calculation
  "learning_delta": {
    "know": {"prev": 0.6, "curr": 0.9, "delta": 0.3},
    "do": {"prev": 0.7, "curr": 0.95, "delta": 0.25},
    "context": {"prev": 0.8, "curr": 0.85, "delta": 0.05}
  },
  
  // NEW: Attribution (optional, Phase 2+)
  "learning_attribution": {
    "investigation": 0.1,  // 10% from reading/investigating
    "code_writing": 0.15,  // 15% from actually coding
    "testing": 0.05        // 5% from seeing tests pass
  },
  
  "meta": {"task": "improve auth module"}
}
```

#### Code Implementation

```python
def _create_checkpoint(
    self,
    phase: str,
    round_num: int,
    vectors: Dict[str, float],
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create checkpoint with git state tracking"""
    
    # Calculate overall confidence
    overall_confidence = self._calculate_confidence(vectors)
    
    # Capture git state
    git_state = self._capture_git_state()
    
    # Calculate learning delta (if previous checkpoint exists)
    learning_delta = self._calculate_learning_delta(vectors)
    
    checkpoint = {
        "session_id": self.session_id,
        "phase": phase,
        "round": round_num,
        "timestamp": datetime.now(UTC).isoformat(),
        "vectors": vectors,
        "overall_confidence": overall_confidence,
        "git_state": git_state,           # NEW
        "learning_delta": learning_delta,  # NEW
        "meta": metadata or {}
    }
    
    return checkpoint

def _capture_git_state(self) -> Dict[str, Any]:
    """Capture current git state"""
    try:
        # Get HEAD commit
        head_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=self.git_repo_path
        ).stdout.strip()
        
        # Get commits since last checkpoint
        commits_since_last = self._get_commits_since_last_checkpoint()
        
        # Get uncommitted changes
        uncommitted = self._get_uncommitted_changes()
        
        return {
            "head_commit": head_sha,
            "commits_since_last_checkpoint": commits_since_last,
            "uncommitted_changes": uncommitted
        }
    except Exception as e:
        logger.warning(f"Failed to capture git state: {e}")
        return {}

def _get_commits_since_last_checkpoint(self) -> List[Dict[str, Any]]:
    """Get commits made since last checkpoint"""
    
    # Get last checkpoint timestamp
    last_checkpoint = self.get_last_checkpoint()
    if not last_checkpoint:
        return []
    
    since_time = last_checkpoint['timestamp']
    
    # Get commits since then
    result = subprocess.run(
        ["git", "log", f"--since={since_time}", "--format=%H|%s|%an|%aI", "HEAD"],
        capture_output=True,
        text=True,
        cwd=self.git_repo_path
    )
    
    commits = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        sha, message, author, timestamp = line.split('|')
        
        # Get files changed in this commit
        files_result = subprocess.run(
            ["git", "show", "--stat", "--format=", sha],
            capture_output=True,
            text=True,
            cwd=self.git_repo_path
        )
        
        commits.append({
            "sha": sha,
            "message": message,
            "author": author,
            "timestamp": timestamp,
            "files_stat": files_result.stdout.strip()
        })
    
    return commits

def _get_uncommitted_changes(self) -> Dict[str, Any]:
    """Get uncommitted working directory changes"""
    
    # Get status
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=self.git_repo_path
    )
    
    modified = []
    added = []
    deleted = []
    
    for line in result.stdout.split('\n'):
        if not line:
            continue
        status = line[:2]
        file = line[3:]
        
        if 'M' in status:
            modified.append(file)
        elif 'A' in status:
            added.append(file)
        elif 'D' in status:
            deleted.append(file)
    
    # Get diff stats
    diff_result = subprocess.run(
        ["git", "diff", "--stat"],
        capture_output=True,
        text=True,
        cwd=self.git_repo_path
    )
    
    return {
        "files_modified": modified,
        "files_added": added,
        "files_deleted": deleted,
        "diff_stat": diff_result.stdout.strip()
    }

def _calculate_learning_delta(self, current_vectors: Dict[str, float]) -> Dict[str, Any]:
    """Calculate epistemic delta since last checkpoint"""
    
    last_checkpoint = self.get_last_checkpoint()
    if not last_checkpoint:
        return {}
    
    prev_vectors = last_checkpoint.get('vectors', {})
    
    deltas = {}
    for key in current_vectors:
        if key in prev_vectors:
            deltas[key] = {
                "prev": prev_vectors[key],
                "curr": current_vectors[key],
                "delta": round(current_vectors[key] - prev_vectors[key], 3)
            }
    
    return deltas
```

**Advantages:**
- ✅ Explicit correlation (precise)
- ✅ Captures uncommitted changes
- ✅ Tracks file-level changes
- ✅ Enables attribution analysis

**Disadvantages:**
- ⚠️ Larger checkpoint size (~800 tokens vs 450)
- ⚠️ Requires git commands at checkpoint time

---

### Level 3: Crypto Binding (Enhanced Signatures)

**Concept:** Sign both checkpoint AND related commits

#### Enhanced Signature Payload

```json
{
  "checkpoint_ref": "empirica/session/abc-123/POSTFLIGHT/1",
  "checkpoint_sha": "c0bac16a451bde1...",
  
  // NEW: Work commits included in signature
  "work_commits": [
    {
      "sha": "f13d167",
      "message": "feat: add timeout handling",
      "verified": true,  // If commit has GPG signature
      "files_changed": ["timeout.py", "config.py"]
    },
    {
      "sha": "b531d53",
      "message": "feat: improve auth",
      "verified": false,
      "files_changed": ["auth.py"]
    }
  ],
  
  // NEW: Uncommitted changes hash (if any)
  "uncommitted_changes_sha": "d5a7e8f...",  // SHA of diff blob
  
  // Composite signature: signs checkpoint + commits + uncommitted
  "signature": "a495d84830ab3239...",
  "ai_id": "copilot",
  "public_key": "3f978d77b7271014...",
  "signed_at": "2025-12-02T12:00:00Z",
  "version": "2.0"  // Updated version
}
```

#### Implementation

```python
def sign_checkpoint_with_commits(
    self,
    session_id: str,
    phase: str,
    round_num: int
) -> Dict[str, Any]:
    """Sign checkpoint including related work commits"""
    
    # Load checkpoint
    checkpoint = self.get_checkpoint(session_id, phase, round_num)
    checkpoint_sha = self._get_checkpoint_note_sha(session_id, phase, round_num)
    
    # Get git state from checkpoint
    git_state = checkpoint.get('git_state', {})
    work_commits = git_state.get('commits_since_last_checkpoint', [])
    uncommitted = git_state.get('uncommitted_changes', {})
    
    # Create composite payload
    composite_payload = {
        "checkpoint_sha": checkpoint_sha,
        "work_commits": [
            {
                "sha": c['sha'],
                "message": c['message'],
                "timestamp": c['timestamp']
            }
            for c in work_commits
        ],
        "uncommitted_changes": uncommitted,
        "signed_at": datetime.now(UTC).isoformat()
    }
    
    # Sign composite payload
    payload_json = json.dumps(composite_payload, sort_keys=True)
    signature = self.identity.sign(payload_json.encode())
    
    # Store signature
    signature_payload = {
        "checkpoint_ref": f"empirica/session/{session_id}/{phase}/{round_num}",
        "checkpoint_sha": checkpoint_sha,
        "work_commits": composite_payload['work_commits'],
        "uncommitted_changes": composite_payload['uncommitted_changes'],
        "signature": signature.hex(),
        "ai_id": self.ai_id,
        "public_key": self.identity.public_key_hex(),
        "signed_at": composite_payload['signed_at'],
        "version": "2.0"
    }
    
    # Store in git notes
    self._store_signature(session_id, phase, round_num, signature_payload)
    
    return signature_payload
```

**Advantages:**
- ✅ Cryptographic proof of epistemic state → code correlation
- ✅ Verifiable chain of custody
- ✅ Proves both "what learned" and "what changed"
- ✅ Tamper-proof

**Disadvantages:**
- ⚠️ More complex verification
- ⚠️ Larger signature payload
- ⚠️ Requires git state capture

---

## 🎯 Recommended Phased Approach

### Phase 2.5: Basic Correlation (Quick Win)

**Implement:** Timestamp-based correlation + git state capture

**Changes:**
1. Add `git_state` field to checkpoints (captures HEAD, commits, diffs)
2. Add `learning_delta` calculation
3. Update checkpoint creation to call `_capture_git_state()`

**Estimated effort:** 4 hours

**Benefits:**
- ✅ Enables dashboard queries: "What code changed during KNOW increase?"
- ✅ Provides attribution data
- ✅ Works with or without user commits

---

### Phase 2.6: Enhanced Signatures (Next)

**Implement:** Composite signatures (checkpoint + commits)

**Changes:**
1. Update `CheckpointSigner.sign_checkpoint()` to include work commits
2. Sign composite payload: checkpoint SHA + commit SHAs
3. Update verification to check both checkpoint and commits
4. Add `checkpoint-sign --include-commits` flag

**Estimated effort:** 6 hours

**Benefits:**
- ✅ Cryptographic binding of epistemic state to code
- ✅ Verifiable learning → code correlation
- ✅ Audit trail for compliance

---

### Phase 3.0: Attribution Analysis (Future)

**Implement:** ML-based attribution of learning to activities

**Concept:**
```python
# Train model to predict: What activity caused KNOW to increase?
attribution = predict_learning_source(
    delta=0.3,  # KNOW increased 0.3
    activities=[
        "read 5 files",
        "wrote 50 lines",
        "ran 3 tests",
        "debugged 2 issues"
    ]
)
# → "code_writing": 60%, "testing": 30%, "reading": 10%
```

**Estimated effort:** 2-3 weeks (research + implementation)

---

## 📊 Dashboard Implications

### With Enhanced Checkpoints

**Query 1: What code changed during learning?**
```sql
SELECT 
    c.phase,
    c.learning_delta->>'know' as know_delta,
    json_array_length(c.git_state->'commits_since_last_checkpoint') as commits,
    c.git_state->'uncommitted_changes'->>'diff_stat' as changes
FROM checkpoints c
WHERE session_id = 'abc-123'
ORDER BY c.timestamp;
```

**Query 2: Learning efficiency (delta per commit)**
```python
def calculate_learning_efficiency(session_id):
    checkpoints = get_checkpoints(session_id)
    
    for checkpoint in checkpoints:
        delta = checkpoint['learning_delta']['know']['delta']
        commits = len(checkpoint['git_state']['commits_since_last_checkpoint'])
        
        if commits > 0:
            efficiency = delta / commits
            print(f"{checkpoint['phase']}: {efficiency:.2f} KNOW per commit")
```

**Query 3: Files touched during high-learning periods**
```python
def find_high_impact_files(session_id, threshold=0.2):
    """Find files changed during high learning (delta > threshold)"""
    
    checkpoints = get_checkpoints(session_id)
    high_impact_files = {}
    
    for checkpoint in checkpoints:
        delta = checkpoint['learning_delta']['know']['delta']
        if delta > threshold:
            commits = checkpoint['git_state']['commits_since_last_checkpoint']
            for commit in commits:
                for file in commit.get('files_changed', []):
                    high_impact_files[file] = high_impact_files.get(file, 0) + delta
    
    return sorted(high_impact_files.items(), key=lambda x: x[1], reverse=True)
```

---

## 🔐 Signature Verification Flow

### With Composite Signatures

```python
def verify_composite_signature(session_id, phase, round_num):
    """Verify checkpoint + commits signature"""
    
    # Load signature
    signature_data = load_signature(session_id, phase, round_num)
    
    # Verify checkpoint SHA
    checkpoint_sha = get_checkpoint_note_sha(session_id, phase, round_num)
    assert checkpoint_sha == signature_data['checkpoint_sha'], "Checkpoint SHA mismatch"
    
    # Verify work commit SHAs (if present)
    for commit_data in signature_data.get('work_commits', []):
        commit_sha = commit_data['sha']
        
        # Verify commit exists in repo
        result = subprocess.run(
            ["git", "cat-file", "-e", commit_sha],
            capture_output=True
        )
        
        if result.returncode != 0:
            raise ValueError(f"Commit {commit_sha} not found in repository")
        
        # Optionally verify commit GPG signature
        if commit_data.get('verified'):
            verify_gpg_signature(commit_sha)
    
    # Reconstruct composite payload
    composite_payload = {
        "checkpoint_sha": signature_data['checkpoint_sha'],
        "work_commits": signature_data['work_commits'],
        "uncommitted_changes": signature_data.get('uncommitted_changes', {}),
        "signed_at": signature_data['signed_at']
    }
    
    # Verify Ed25519 signature
    payload_json = json.dumps(composite_payload, sort_keys=True)
    public_key = bytes.fromhex(signature_data['public_key'])
    signature_bytes = bytes.fromhex(signature_data['signature'])
    
    try:
        public_key_obj = ed25519.Ed25519PublicKey.from_public_bytes(public_key)
        public_key_obj.verify(signature_bytes, payload_json.encode())
        return True
    except:
        return False
```

---

## 📝 Documentation Example

### User-Facing Documentation

```markdown
## Correlating Learning to Code Changes

Empirica tracks both your epistemic state (what you know) and the code changes you make.
Each checkpoint captures the current git state, allowing you to see:

**What changed during learning:**
```bash
empirica checkpoint-show abc-123 --phase POSTFLIGHT --round 1

Output:
📊 Checkpoint: POSTFLIGHT Round 1
   Learning: KNOW: 0.6 → 0.9 (+0.3)
   
   Code commits during learning:
   - f13d167: feat: add timeout handling (timeout.py, config.py)
   - b531d53: feat: improve auth (auth.py)
   
   Uncommitted changes:
   - auth.py: +25 -5 lines
```

**Query learning efficiency:**
```bash
empirica analyze learning-efficiency --session-id abc-123

Output:
Phase         Learning  Commits  Efficiency
PREFLIGHT     +0.1      0        N/A
CHECK         +0.1      0        N/A  
ACT           +0.3      2        0.15/commit
POSTFLIGHT    +0.0      0        N/A
```

**Find high-impact files:**
```bash
empirica analyze high-impact-files --session-id abc-123

Output:
Files changed during high learning periods (delta > 0.2):

1. auth.py: 0.3 total learning delta
2. timeout.py: 0.3 total learning delta
3. config.py: 0.3 total learning delta
```
```

---

## 🎯 Implementation Priority

### Must Have (Phase 2.5)
1. ✅ Git state capture in checkpoints
2. ✅ Learning delta calculation
3. ✅ Timestamp-based correlation

### Should Have (Phase 2.6)
1. ✅ Composite signatures (checkpoint + commits)
2. ✅ Enhanced verification
3. ✅ Dashboard queries

### Nice to Have (Phase 3.0)
1. ⭐ Attribution analysis (ML-based)
2. ⭐ Learning efficiency metrics
3. ⭐ High-impact file detection

---

**Next Step:** Implement Phase 2.5 (git state capture) - 4 hour effort, enables all dashboard queries and provides foundation for Phase 2.6 signatures.
