# Git Notes vs Commits - Analysis & Design

**Date:** 2025-12-02  
**Issue:** Understanding git notes behavior and auto-commit implications

---

## 🔍 Current Behavior Discovery

### What Git Notes Actually Do

When we call:
```bash
git notes --ref empirica/session/abc-123/PREFLIGHT/1 add -m "checkpoint" HEAD
```

**What happens internally:**
1. Git creates a **blob** object with the checkpoint JSON
2. Git creates a **tree** object pointing to the blob
3. Git creates a **commit** object in the `refs/notes/` namespace
4. The commit message is: "Notes added by 'git notes add'"

**Evidence:**
```bash
$ git log --all --oneline
4e86c45 Notes added by 'git notes add'  ← This is a notes commit!
c0bac16 Notes added by 'git notes add'  ← Another notes commit!
b531d53 feat: Implement schema migration...  ← This is a real work commit
```

**These notes commits are in refs/notes/ namespace:**
```
refs/notes/empirica/session/test-crypto-sign/PREFLIGHT/1
refs/notes/empirica/signatures/test-crypto-sign/PREFLIGHT/1
refs/notes/empirica/goals/92848363-f66d-4320-a0af-0f4b6ae02410
```

---

## 🤔 The Question: Are These "Auto-Commits"?

### Two Perspectives

**Perspective 1: YES - These are commits**
- Git creates commit objects
- They show up in `git log --all`
- They have SHA, author, timestamp
- They're in the git history

**Perspective 2: NO - These are NOT work commits**
- They're in refs/notes/ namespace (not refs/heads/)
- They don't modify working directory
- They don't affect code
- They're metadata, not content changes

---

## 💡 Key Insight: Git Notes ARE Commits (By Design)

**Git's note storage model:**
```
refs/
├── heads/              ← Regular branches (code commits)
│   └── main
├── remotes/            ← Remote tracking branches
│   └── origin/main
└── notes/              ← Notes storage (metadata commits)
    └── empirica/
        ├── session/    ← Checkpoints
        ├── signatures/ ← Crypto signatures
        └── goals/      ← Goal state
```

**This is actually CORRECT behavior:**
- Git notes must be stored as commits (that's how git works)
- The commits are in a separate namespace
- They don't interfere with regular git workflow
- They're pushed/pulled like any ref

---

## 🎯 The Real Question: Do We Auto-Commit WORK Changes?

**Answer:** NO - Empirica NEVER auto-commits work changes.

### What Empirica Does

✅ **Creates git notes** (metadata commits in refs/notes/)
- Checkpoints: `refs/notes/empirica/session/{id}/{phase}/{round}`
- Signatures: `refs/notes/empirica/signatures/{id}/{phase}/{round}`
- Goals: `refs/notes/empirica/goals/{goal_id}`

❌ **Does NOT create work commits** (no refs/heads/ changes)
- Never runs `git commit` on user's code
- Never stages files with `git add`
- Never modifies working directory
- Never touches user's branches

### Code Evidence

**GitEnhancedReflexLogger only uses git notes:**
```python
# Line 269 in git_enhanced_reflex_logger.py
result = subprocess.run(
    ["git", "notes", "--ref", note_ref, "add", "-m", checkpoint_json, "HEAD"],
    #        ^^^^^ Git notes command, NOT git commit!
    ...
)
```

**CheckpointSigner only uses git notes:**
```python
# Line 161 in checkpoint_signer.py
result = subprocess.run(
    ["git", "notes", "--ref", signature_ref, "add", "-f", "-m", 
     json.dumps(signature_payload), "HEAD"],
    #        ^^^^^ Git notes, NOT git commit!
    ...
)
```

**Goal orchestrator only uses git notes:**
```python
# Goals stored as notes, not commits
note_ref = f"empirica/goals/{goal_id}"
```

---

## 🚦 Decision: No Auto-Commit Flag Needed

### Why NOT Needed

1. **No work commits are made**
   - Empirica only creates notes commits (metadata)
   - User's code commits are never touched
   - Git workflow is unaffected

2. **Git notes are essential**
   - 97% token reduction depends on git notes
   - Checkpoint resumption requires git notes
   - Crypto signing requires git notes
   - Multi-agent coordination requires git notes

3. **Notes commits are harmless**
   - They're in refs/notes/ namespace
   - They don't clutter branch history
   - They don't affect working directory
   - They're invisible in normal git workflow

4. **Disabling would break Empirica**
   - No checkpoints → no resumption
   - No signatures → no verification
   - No goals → no coordination
   - Defeats the entire purpose

### What Users Control

Users already control git notes via existing flags:

**At bootstrap/session level:**
```python
GitEnhancedReflexLogger(
    session_id=session_id,
    enable_git_notes=True  # ← User choice!
)
```

**Default:** `enable_git_notes=False` for backward compatibility

**Enable:** Only when user explicitly enables git features

---

## 📋 Current Behavior Summary

### When enable_git_notes=True

**What DOES happen:**
- ✅ Notes commits created in refs/notes/empirica/
- ✅ Checkpoints stored as git notes
- ✅ Signatures stored as git notes
- ✅ Goals stored as git notes

**What DOES NOT happen:**
- ❌ No `git commit` on user's code
- ❌ No `git add` on user's files
- ❌ No working directory changes
- ❌ No branch modifications

### When enable_git_notes=False

**What DOES happen:**
- ✅ Checkpoints saved to SQLite fallback
- ✅ Checkpoints saved to JSON files

**What DOES NOT happen:**
- ❌ No git notes created
- ❌ No compression benefits (6,500 tokens vs 450)
- ❌ No resumption efficiency gains
- ❌ No crypto signing possible

---

## 🔧 What About User Work Commits?

**Scenario:** User wants Empirica to commit their code changes

**Example:**
```bash
# User makes code change
vim auth.py

# User wants: Auto-commit after checkpoint
empirica checkpoint-create --session-id abc-123 --phase PREFLIGHT --round 1 --auto-commit
#                                                                              ^^^^^^^^^^^
#                                                                              Should this exist?
```

### Design Options

#### Option 1: No Auto-Commit (Current, Recommended)

**Rationale:**
- Git workflow is personal (some use squash, rebase, etc.)
- Empirica shouldn't dictate git strategy
- Users can commit manually when they want
- Separation of concerns: Empirica = epistemic tracking, Git = code versioning

**User workflow:**
```bash
# User makes changes
vim auth.py

# User commits (their way)
git add auth.py
git commit -m "feat: improve auth timeout"

# Empirica adds note to this commit
empirica checkpoint-create --session-id abc-123 --phase PREFLIGHT --round 1
# Note attached to HEAD (user's commit)
```

#### Option 2: Optional Auto-Commit Flag

**Implementation:**
```python
def handle_checkpoint_create_command(args):
    # ... checkpoint creation ...
    
    if args.auto_commit:
        # Check if working directory is clean
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            # Uncommitted changes exist
            subprocess.run(["git", "add", "-A"])
            subprocess.run([
                "git", "commit", "-m", 
                f"empirica: checkpoint {phase} round {round_num}"
            ])
```

**CLI:**
```bash
empirica checkpoint-create --session-id abc-123 --phase PREFLIGHT --round 1 --auto-commit
```

**Concerns:**
- ⚠️ Opinionated (forces git workflow)
- ⚠️ Could conflict with user's git strategy
- ⚠️ Hard to get right (what about .gitignore, unstaged files, etc.)
- ⚠️ Violates principle of least surprise

#### Option 3: Git Integration Hook (Future)

**Concept:** Let users configure git hooks

**Example `.empirica/config.toml`:**
```toml
[git]
auto_commit = true
commit_message_template = "empirica: {phase} round {round}"
auto_push = false
```

**Implementation:** User opts-in explicitly via config

---

## 🎯 Recommendation

### Keep Current Behavior (No Auto-Commit Flag)

**Reasons:**
1. ✅ Git notes are NOT user code commits (they're metadata)
2. ✅ Users control git notes via `enable_git_notes` flag
3. ✅ Adding auto-commit flag would be opinionated and risky
4. ✅ Separation of concerns: Empirica tracks epistemic state, users control code commits

### If Users Want Auto-Commit

**Option 1: Use git hooks** (user configures)
```bash
# .git/hooks/post-commit
#!/bin/bash
empirica checkpoint-create --session-id latest:active --phase ACT --round 1
```

**Option 2: Wrapper script** (user creates)
```bash
#!/bin/bash
# commit_and_checkpoint.sh
git commit "$@"
empirica checkpoint-create --session-id latest:active --phase ACT --round 1
```

**Option 3: Git aliases** (user configures)
```bash
git config alias.ccp '!git commit "$@" && empirica checkpoint-create --session-id latest:active --phase ACT --round 1'
```

---

## 📊 Comparison: Git Notes vs Work Commits

| Aspect | Git Notes (Current) | Work Commits (Proposed) |
|--------|-------------------|------------------------|
| **Namespace** | refs/notes/ | refs/heads/ |
| **Modifies code** | No | Yes |
| **Affects working dir** | No | Yes |
| **Shows in git log** | Only with --all | Yes, always |
| **Shows in git status** | No | Yes |
| **User controls** | enable_git_notes flag | Would need auto_commit flag |
| **Breaking change** | No | Potentially yes |
| **Opinionated** | No | Yes |

---

## 🔑 Key Takeaways

1. **Git notes ARE commits** - That's how git stores notes internally
2. **These are metadata commits** - Not user code commits
3. **They're in refs/notes/** - Separate namespace from branches
4. **No auto-commit flag needed** - Empirica doesn't commit user code
5. **Users control via enable_git_notes** - Already configurable
6. **Separation of concerns** - Empirica = epistemic tracking, Git = code versioning

---

## 📝 Documentation Needed

**Add to checkpoint docs:**

```markdown
## Git Notes vs Code Commits

Empirica uses git notes to store checkpoints efficiently. This creates commits in
the `refs/notes/empirica/` namespace, which are METADATA commits, not code commits.

**What Empirica does:**
- ✅ Creates git notes (metadata commits in refs/notes/)
- ✅ Stores checkpoints, signatures, goals as notes

**What Empirica does NOT do:**
- ❌ Never commits your code changes
- ❌ Never modifies your working directory
- ❌ Never runs `git commit` on your files

**To see notes commits:**
```bash
git log --all  # Shows both code and notes commits
```

**To hide notes commits:**
```bash
git log --no-notes  # Shows only code commits
```

**Your code commits are completely under your control.**
```

---

**Recommendation:** No changes needed to current behavior. Document clearly that git notes are metadata commits, not code commits.
