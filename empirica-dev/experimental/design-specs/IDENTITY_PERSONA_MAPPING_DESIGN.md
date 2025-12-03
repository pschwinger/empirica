# Identity-Persona Mapping & Optional Signing - Design Document

**Date:** 2025-12-02  
**Status:** NEEDS IMPLEMENTATION

---

## Current Gaps

### Gap 1: Persona → AI Identity Mapping

**Current State:**
- Sessions have `ai_id` field (e.g., "copilot", "qwen", "gemini")
- Identities have `ai_id` keypairs (e.g., `.empirica/identity/copilot.key`)
- **BUT:** No automatic mapping between session `ai_id` and signing identity

**Problem:**
```bash
# Bootstrap creates session with ai_id="copilot"
empirica bootstrap --ai-id copilot --onboard

# But signing requires explicitly passing --ai-id again
empirica checkpoint-sign --session-id <uuid> --phase PREFLIGHT --round 1 --ai-id copilot
#                                                                            ^^^^^^^^^^
#                                                                            Redundant!
```

**What We Should Have:**
```bash
# Bootstrap creates session with ai_id="copilot"
empirica bootstrap --ai-id copilot --onboard

# Signing should auto-detect ai_id from session
empirica checkpoint-sign --session-id <uuid> --phase PREFLIGHT --round 1
# Auto-detects: session ai_id="copilot" → use copilot identity
```

### Gap 2: Optional Signing (Not Required)

**Current State:**
✅ Signing is **already optional** (good!)
- Checkpoints work without signing
- Signing is a separate manual step
- No performance overhead if not used

**Concern:**
⚠️ Users shouldn't feel forced to sign checkpoints

**Solution:**
Document clearly that signing is opt-in for:
- High-security environments
- Multi-agent coordination needing trust
- Audit/compliance requirements
- Public sharing of epistemic state

---

## Proposed Solutions

### Solution 1: Auto-Detect AI Identity from Session

**Implementation:**

```python
# In checkpoint_signing_commands.py
def handle_checkpoint_sign_command(args):
    session_id = args.session_id
    phase = args.phase
    round_num = args.round
    ai_id = args.ai_id  # Optional!
    
    # Auto-detect if not provided
    if not ai_id:
        from empirica.data.session_database import SessionDatabase
        db = SessionDatabase()
        session = db.get_session(session_id)
        
        if session:
            ai_id = session['ai_id']
            print(f"ℹ️  Auto-detected AI identity: {ai_id}")
        else:
            print("❌ Cannot auto-detect AI identity - session not found")
            print("   Use: --ai-id <identity>")
            sys.exit(1)
    
    # Continue with signing...
```

**Updated CLI:**
```bash
# With auto-detection
empirica checkpoint-sign --session-id abc-123 --phase PREFLIGHT --round 1
# ℹ️  Auto-detected AI identity: copilot

# Or explicit (override)
empirica checkpoint-sign --session-id abc-123 --phase PREFLIGHT --round 1 --ai-id copilot
```

### Solution 2: Make AI Identity Optional in CLI Parser

**Update parser:**

```python
# In cli_core.py
checkpoint_sign_parser.add_argument(
    '--ai-id', 
    help='AI identity to sign with (auto-detected from session if omitted)'
)
```

### Solution 3: Document Signing as Opt-In Feature

**Add to checkpoint signing docs:**

```markdown
## When to Use Signing

Signing is **completely optional**. Use it when you need:

✅ **High-Security Environments**
   - Production systems
   - Regulated industries
   - Multi-tenant systems

✅ **Multi-Agent Coordination**
   - Multiple AIs working together
   - Need to verify which AI created checkpoint
   - Trust chain required

✅ **Audit/Compliance**
   - Regulatory requirements
   - Forensic analysis
   - Chain of custody

✅ **Public Sharing**
   - Publishing epistemic state
   - Research reproducibility
   - Community verification

❌ **When NOT to Use Signing**
   - Personal projects (solo AI)
   - Development/testing
   - Local-only work
   - Performance-critical paths

**Default:** Checkpoints work perfectly without signing!
```

---

## Implementation Plan

### Phase 1: Auto-Detection (Quick Win)

**Files to modify:**
1. `empirica/cli/command_handlers/checkpoint_signing_commands.py`
   - Make `ai_id` optional in `handle_checkpoint_sign_command`
   - Auto-detect from session database
   - Fall back to explicit `--ai-id` if needed

2. `empirica/cli/cli_core.py`
   - Update help text for `--ai-id` parameter
   - Show it's optional with auto-detection

**Estimated time:** 30 minutes

### Phase 2: Documentation (Critical)

**Files to create/update:**
1. `docs/guides/CHECKPOINT_SIGNING_GUIDE.md`
   - Clear "opt-in" messaging
   - When to use / when not to use
   - Performance impact (none if not used)
   - Example workflows

2. Update `CHECKPOINT_CRYPTO_SIGNING_COMPLETE.md`
   - Add section on optional nature
   - Clarify no overhead if not signing

**Estimated time:** 1 hour

### Phase 3: Persona Integration (Future)

**If we want deeper integration:**

Add `persona_id` field to sessions table:
```sql
ALTER TABLE sessions ADD COLUMN persona_id TEXT;
```

Update bootstrap to store persona:
```python
db.create_session(
    ai_id=ai_id,
    persona_id=persona_name,  # e.g., "security_expert", "code_reviewer"
    ...
)
```

Allow signing with persona:
```bash
empirica checkpoint-sign --session-id abc-123 --persona security_expert
# Resolves: security_expert → security_expert identity
```

**Estimated time:** 2 hours

---

## Recommended Approach

**Immediate (Do Now):**
1. ✅ Make `--ai-id` optional in checkpoint-sign
2. ✅ Auto-detect from session database
3. ✅ Document signing as opt-in feature

**Near-term (Next Session):**
1. Add comprehensive signing guide
2. Update all checkpoint docs with "optional" messaging
3. Add FAQ about performance/overhead

**Future (Phase 2.1):**
1. Consider persona integration if needed
2. Auto-signing flag for automatic workflow
3. Dashboard visualization of signed vs unsigned

---

## Code Snippet: Auto-Detection Implementation

```python
def handle_checkpoint_sign_command(args):
    """Sign a checkpoint with AI identity (auto-detected or explicit)"""
    try:
        from empirica.core.checkpoint_signer import CheckpointSigner
        from empirica.data.session_database import SessionDatabase
        
        session_id = args.session_id
        phase = args.phase
        round_num = args.round
        ai_id = getattr(args, 'ai_id', None)  # May be None
        output_format = getattr(args, 'output', 'default')
        
        # Auto-detect AI identity if not provided
        if not ai_id:
            db = SessionDatabase()
            session = db.get_session(session_id)
            
            if session:
                ai_id = session['ai_id']
                if output_format != 'json':
                    print(f"ℹ️  Auto-detected AI identity from session: {ai_id}")
            else:
                error_result = {
                    "ok": False,
                    "error": "session_not_found",
                    "message": f"Session not found: {session_id}",
                    "hint": "Use --ai-id to specify identity explicitly"
                }
                
                if output_format == 'json':
                    print(json.dumps(error_result, indent=2))
                else:
                    print(f"❌ Session not found: {session_id}")
                    print(f"\n💡 Either:")
                    print(f"   1. Provide valid session ID")
                    print(f"   2. Use --ai-id to specify identity explicitly")
                
                sys.exit(1)
        
        # Rest of signing logic...
```

---

## Testing Plan

**Test cases:**
1. ✅ Sign with explicit `--ai-id` (existing behavior)
2. ✅ Sign without `--ai-id` (auto-detect from session)
3. ✅ Sign with non-existent session (error handling)
4. ✅ Sign with session but no identity file (error handling)
5. ✅ Sign with override `--ai-id` (different from session)

---

## Session Aliases Integration

**Current aliases work for:**
- `sessions-show`
- `checkpoint-load`
- `checkpoint-list`

**Should also work for signing:**
```bash
# Use alias instead of full UUID
empirica checkpoint-sign --session-id latest:active --phase PREFLIGHT --round 1
# Auto-detects: latest:active → resolves to UUID → gets ai_id → signs
```

**Implementation:** Already supported via `resolve_session_id()` in session_resolver!

---

**Summary:**
1. Signing is already optional (no changes needed there)
2. We should add AI identity auto-detection (30 min fix)
3. We should document clearly that signing is opt-in
4. Session aliases already work with signing commands
