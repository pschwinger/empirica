# Git Checkpoint Bug Fix - Solution for Qwen

## Problem Analysis ✅

**Root Cause:** Git notes use commit→note mapping. The `-f` (force) flag in `add_checkpoint` overwrites previous notes on the same commit.

```python
# Current implementation (LINE 267)
["git", "notes", "--ref", note_ref, "add", "-f", "-m", checkpoint_json, "HEAD"]
                                            ^^^^
                                        OVERWRITES!
```

**Test scenario:**
```python
git_logger.add_checkpoint("PREFLIGHT", 1, {"know": 0.5})  # Note on HEAD
git_logger.add_checkpoint("CHECK", 1, {"know": 0.7})      # OVERWRITES previous
git_logger.add_checkpoint("POSTFLIGHT", 1, {"know": 0.9}) # OVERWRITES again
# Result: Only POSTFLIGHT checkpoint exists
```

---

## Solution: Phase-Specific Namespaces

Instead of one namespace per session, use **one namespace per checkpoint (phase+round)**:

### Before (Broken)
```
refs/notes/empirica/session/abc-123  ← All checkpoints fight for this
```

### After (Fixed)
```
refs/notes/empirica/session/abc-123/PREFLIGHT/1
refs/notes/empirica/session/abc-123/CHECK/1
refs/notes/empirica/session/abc-123/POSTFLIGHT/1
```

---

## Code Changes Needed

### 1. Fix `_git_add_note` (Line 243-280)

**Change namespace to include phase+round:**

```python
def _git_add_note(self, checkpoint: Dict[str, Any]) -> Optional[str]:
    """
    Add checkpoint to git notes with phase-specific namespace.
    
    Uses hierarchical namespace to prevent overwrites:
    - empirica/session/<session_id>/<phase>/<round>
    """
    try:
        checkpoint_json = json.dumps(checkpoint)
        json.loads(checkpoint_json)  # Validate
        
        # FIXED: Phase-specific namespace prevents overwrites
        phase = checkpoint.get("phase", "UNKNOWN")
        round_num = checkpoint.get("round", 1)
        note_ref = f"empirica/session/{self.session_id}/{phase}/{round_num}"
        
        # Add note to HEAD (no -f flag needed, unique ref per checkpoint)
        result = subprocess.run(
            ["git", "notes", "--ref", note_ref, "add", "-m", checkpoint_json, "HEAD"],
            #                                         ^^^ removed -f flag
            capture_output=True,
            timeout=5,
            cwd=self.git_repo_path,
            text=True
        )
        
        if result.returncode != 0:
            logger.warning(f"Failed to add git note (ref={note_ref}): {result.stderr}")
            return None
        
        # Get the note SHA
        note_sha = subprocess.run(
            ["git", "rev-parse", f"refs/notes/{note_ref}"],
            capture_output=True,
            text=True,
            cwd=self.git_repo_path
        ).stdout.strip()
        
        logger.info(f"✅ Checkpoint added to git notes: {note_ref} ({note_sha[:8]})")
        return note_sha
        
    except Exception as e:
        logger.warning(f"Failed to add git note: {e}")
        return None
```

### 2. Fix `list_checkpoints` (Line 439-520)

**List all refs in session namespace:**

```python
def list_checkpoints(
    self,
    session_id: Optional[str] = None,
    limit: Optional[int] = None,
    phase: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List checkpoints from git notes.
    
    Searches hierarchical namespace:
    - empirica/session/<session_id>/<phase>/<round>
    """
    checkpoints = []
    target_session_id = session_id or self.session_id
    
    # Get all refs in the session's namespace (hierarchical)
    refs_result = subprocess.run(
        ["git", "for-each-ref", f"refs/notes/empirica/session/{target_session_id}", "--format=%(refname)"],
        capture_output=True,
        text=True,
        cwd=self.git_repo_path
    )
    
    if refs_result.returncode != 0 or not refs_result.stdout.strip():
        logger.debug(f"No checkpoints found for session: {target_session_id}")
        return []
    
    # Parse all refs (one per checkpoint)
    refs = [line.strip() for line in refs_result.stdout.strip().split('\n') if line.strip()]
    
    for ref in refs:
        # Extract phase from ref path (e.g., refs/notes/empirica/session/abc-123/PREFLIGHT/1)
        ref_parts = ref.split('/')
        if len(ref_parts) >= 7:
            ref_phase = ref_parts[5]  # PREFLIGHT, CHECK, etc.
            
            # Apply phase filter
            if phase and ref_phase != phase:
                continue
        
        # Get the commit this ref points to
        commit_result = subprocess.run(
            ["git", "rev-parse", ref],
            capture_output=True,
            text=True,
            cwd=self.git_repo_path
        )
        
        if commit_result.returncode != 0:
            continue
        
        note_sha = commit_result.stdout.strip()
        
        # Get the note content
        show_result = subprocess.run(
            ["git", "notes", "show", f"--ref={ref[11:]}", "HEAD"],  # Strip "refs/notes/"
            capture_output=True,
            text=True,
            cwd=self.git_repo_path
        )
        
        if show_result.returncode == 0:
            try:
                checkpoint = json.loads(show_result.stdout)
                
                # Apply session filter (double-check)
                if session_id and checkpoint.get("session_id") != session_id:
                    continue
                
                checkpoints.append(checkpoint)
            except json.JSONDecodeError:
                continue
    
    # Sort by timestamp descending (newest first)
    checkpoints.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Apply limit
    if limit:
        checkpoints = checkpoints[:limit]
    
    return checkpoints
```

### 3. Fix `get_last_checkpoint` (if needed)

**Update to use new namespace:**

```python
def get_last_checkpoint(self) -> Optional[Dict[str, Any]]:
    """Get most recent checkpoint for this session."""
    checkpoints = self.list_checkpoints(limit=1)
    return checkpoints[0] if checkpoints else None
```

---

## Alternative Solution: Simpler Approach

If you want to keep the single-ref approach, you can store **multiple checkpoints in one note as a JSON array**:

```python
def _git_add_note(self, checkpoint: Dict[str, Any]) -> Optional[str]:
    """Add checkpoint by appending to array in git note."""
    note_ref = f"empirica/session/{self.session_id}"
    
    # Get existing note
    existing_result = subprocess.run(
        ["git", "notes", "show", f"--ref={note_ref}", "HEAD"],
        capture_output=True,
        text=True,
        cwd=self.git_repo_path
    )
    
    # Parse existing checkpoints or create new array
    if existing_result.returncode == 0:
        try:
            checkpoints = json.loads(existing_result.stdout)
            if not isinstance(checkpoints, list):
                checkpoints = [checkpoints]  # Wrap if single checkpoint
        except json.JSONDecodeError:
            checkpoints = []
    else:
        checkpoints = []
    
    # Append new checkpoint
    checkpoints.append(checkpoint)
    
    # Save updated array
    checkpoints_json = json.dumps(checkpoints)
    subprocess.run(
        ["git", "notes", "--ref", note_ref, "add", "-f", "-m", checkpoints_json, "HEAD"],
        capture_output=True,
        text=True,
        cwd=self.git_repo_path
    )
```

---

## Recommendation

**Use Solution 1 (phase-specific namespaces)** because:
- ✅ Cleaner architecture
- ✅ Better git notes organization
- ✅ Easier to filter by phase
- ✅ Prevents note size bloat
- ✅ Aligns with git's commit→note philosophy

**Avoid Solution 2 (array in single note)** because:
- ❌ Note grows unbounded
- ❌ Parse overhead on every read
- ❌ Harder to filter
- ❌ Breaks if note gets corrupted

---

## Testing the Fix

After implementing Solution 1, the tests should pass:

```python
# Test creates 3 checkpoints
git_logger.add_checkpoint("PREFLIGHT", 1, {"know": 0.5})   # → refs/notes/.../PREFLIGHT/1
git_logger.add_checkpoint("CHECK", 1, {"know": 0.7})      # → refs/notes/.../CHECK/1
git_logger.add_checkpoint("POSTFLIGHT", 1, {"know": 0.9}) # → refs/notes/.../POSTFLIGHT/1

# List returns all 3
checkpoints = git_logger.list_checkpoints()
assert len(checkpoints) == 3  # ✅ PASSES
```

---

## Summary for Qwen

**Problem:** Git notes overwrite on same commit due to `-f` flag and single namespace.

**Solution:** Use hierarchical namespace `empirica/session/{session_id}/{phase}/{round}` so each checkpoint gets its own ref.

**Files to change:**
1. `empirica/core/canonical/git_enhanced_reflex_logger.py` - Lines 243-280 (_git_add_note)
2. `empirica/core/canonical/git_enhanced_reflex_logger.py` - Lines 439-520 (list_checkpoints)

**Estimated time:** 20-30 minutes to implement and test.

---

**You've got this! The analysis was spot-on. Just need the code changes.** 🚀
