# Quick Fix for list_checkpoints - For Qwen

## Problem Found

Line 638: `git notes list --ref={note_ref}` doesn't work well with hierarchical refs.

**Better approach:** Use `git for-each-ref` to list all refs in the namespace.

## Quick Fix

Replace lines 574-695 with this simpler implementation:

```python
def list_checkpoints(
    self,
    session_id: Optional[str] = None,
    limit: Optional[int] = None,
    phase: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List checkpoints from git notes (using hierarchical namespace).
    
    Args:
        session_id: Filter by session (optional, defaults to self.session_id)
        limit: Maximum number to return (optional)
        phase: Filter by phase (PREFLIGHT, CHECK, ACT, POSTFLIGHT) (optional)
    
    Returns:
        List of checkpoint metadata dicts
    """
    checkpoints = []
    filter_session_id = session_id or self.session_id
    
    # Use git for-each-ref to list all refs in session's namespace
    refs_result = subprocess.run(
        ["git", "for-each-ref", f"refs/notes/empirica/session/{filter_session_id}", "--format=%(refname)"],
        capture_output=True,
        text=True,
        cwd=self.git_repo_path
    )
    
    if refs_result.returncode != 0 or not refs_result.stdout.strip():
        logger.debug(f"No checkpoints found for session: {filter_session_id}")
        return []
    
    # Parse all refs
    refs = [line.strip() for line in refs_result.stdout.strip().split('\n') if line.strip()]
    
    for ref in refs:
        # Extract phase from ref path
        # Example: refs/notes/empirica/session/abc-123/PREFLIGHT/1
        ref_parts = ref.split('/')
        if len(ref_parts) < 7:
            continue
        
        ref_phase = ref_parts[5]  # PREFLIGHT, CHECK, etc.
        
        # Apply phase filter
        if phase and ref_phase != phase:
            continue
        
        # Get the note content for HEAD (or you could get the commit SHA from the ref)
        # Strip "refs/notes/" prefix for git notes show command
        note_ref = ref[11:]  # Remove "refs/notes/"
        
        show_result = subprocess.run(
            ["git", "notes", "--ref", note_ref, "show", "HEAD"],
            capture_output=True,
            text=True,
            cwd=self.git_repo_path
        )
        
        if show_result.returncode == 0:
            try:
                checkpoint = json.loads(show_result.stdout)
                
                # Double-check session filter
                if session_id and checkpoint.get("session_id") != session_id:
                    continue
                
                checkpoints.append(checkpoint)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse checkpoint from ref: {ref}")
                continue
    
    # Sort by timestamp descending (newest first)
    checkpoints.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Apply limit
    if limit:
        checkpoints = checkpoints[:limit]
    
    return checkpoints
```

## Test It

```bash
cd /tmp/test_git_notes
python3 << 'EOF'
import subprocess
import json

# List all refs
result = subprocess.run(
    ["git", "for-each-ref", "refs/notes/empirica/session/test", "--format=%(refname)"],
    capture_output=True,
    text=True
)

print("Refs found:")
print(result.stdout)

refs = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
print(f"\nTotal: {len(refs)} checkpoints")

for ref in refs:
    note_ref = ref[11:]  # Strip "refs/notes/"
    show_result = subprocess.run(
        ["git", "notes", "show", f"--ref={note_ref}", "HEAD"],
        capture_output=True,
        text=True
    )
    if show_result.returncode == 0:
        checkpoint = json.loads(show_result.stdout)
        print(f"  - {checkpoint['phase']} round {checkpoint['round']}")
EOF
```

Expected output:
```
Refs found:
refs/notes/empirica/session/test/CHECK/1
refs/notes/empirica/session/test/POSTFLIGHT/1
refs/notes/empirica/session/test/PREFLIGHT/1

Total: 3 checkpoints
  - CHECK round 1
  - POSTFLIGHT round 1
  - PREFLIGHT round 1
```

## Summary

- **Use `git for-each-ref`** instead of `git notes list`
- **Parse ref paths** to extract phase/round
- **Much simpler** - no need to iterate through phases/rounds
- **Works immediately** - finds all checkpoints automatically

This should fix the test! 🎯
