# Empirica Phase 1 Testing Report

**Date:** 2025-12-02  
**Objective:** Test Phase 1 end-to-end to find what breaks when empirica is actually used

---

## Key Finding

**Empirica does NOT work magically.** It requires:
1. **Deliberate invocation** - You must explicitly call empirica APIs
2. **Proper configuration** - Complex setup of personas, identities, configs
3. **Dependency management** - All required packages must be installed
4. **Understanding of internals** - API signatures, file formats, naming conventions
5. **Integration awareness** - How components work together

---

## Issues Found and Fixed

### Issue #1: Circular Import in core/git/__init__.py
**Status:** ✅ FIXED  
**Cause:** __init__.py was importing SignedGitOperations which then imported git (GitPython), creating circular dependency  
**Fix:** Removed eager import from __init__.py

### Issue #2: PersonaProfile Constructor Signature
**Status:** ✅ FIXED  
**Cause:** Constructor requires SigningIdentityConfig + EpistemicConfig, not domain/expertise/tags  
**Fix:** Updated test to use proper dataclass constructors

### Issue #3: SigningIdentityConfig Requires 64-Char Hex Key
**Status:** ✅ FIXED  
**Cause:** Validation in PersonaProfile.__post_init__ checks public_key is exactly 64 hex chars  
**Fix:** Generated proper Ed25519 public key and converted to hex

### Issue #4: AIIdentity Keypair Location Convention
**Status:** ✅ FIXED  
**Cause:** AIIdentity looks for keys in `.empirica/identity/{ai_id}.key`  
**Fix:** Created keypair files in correct location

### Issue #5: AIIdentity Keypair Format (JSON, not PEM)
**Status:** ✅ FIXED  
**Cause:** AIIdentity.load_keypair() expects JSON format with specific fields  
**Fix:** Created JSON files with ai_id, private_key (hex), public_key (hex), created_at, metadata

### Issue #6: SigningPersona Parameter Name
**Status:** ✅ FIXED  
**Cause:** Method signature is `epistemic_vectors` not `epistemic_state`  
**Fix:** Updated call to use correct parameter name

### Issue #7: AIIdentity.public_key_hex is a Method
**Status:** ✅ FIXED  
**Cause:** Not a property, must be called as `public_key_hex()`  
**Fix:** Updated code to call method

### Issue #8: GitPython Not Installed
**Status:** ✅ FIXED  
**Cause:** Dependency not in environment  
**Fix:** `pip install GitPython`

### Issue #9: Package Naming Conflict (git vs empirica.core.git)
**Status:** ✅ FIXED  
**Cause:** `import git` inside empirica.core.git package resolves to itself, not GitPython  
**Fix:** Renamed empirica/core/git → empirica/core/git_ops

### Issue #10: Git Reference Conflict
**Status:** ✅ RESOLVED (never actually occurred in production code)  
**Original Claim:** `fatal: update_ref failed for ref 'refs/notes/empirica'`  
**Investigation:** All refs properly namespaced; no bare `refs/notes/empirica` exists  
**Verification:** Runtime tests confirm no conflict (53 refs, all correct)  
**Note:** Either transient test artifact or misdiagnosis; codebase is correct  
**Details:** See `GIT_REF_CONFLICT_RESOLUTION.md`

---

## What This Demonstrates

### Positive (Empirica DOES Work)
✅ Ed25519 signing works  
✅ PersonaProfile validation works  
✅ SigningPersona creates valid cryptographic bindings  
✅ Git operations are being called correctly  
✅ Epistemic state JSON is properly formatted  

### Requires Deliberate Use
❌ No automatic setup - must configure everything manually  
❌ No sensible defaults - all parameters must be explicit  
❌ API is complex - multiple interdependent components  
❌ Internal format knowledge required - keypair formats, file locations  
❌ Dependency management matters - GitPython not installed by default  

---

## System Prompt Requirements

The canonical system prompt MUST clarify:

### 1. Empirica is Not Magic
```markdown
**Critical:** Empirica does not work automatically.
You must EXPLICITLY invoke empirica mechanisms:
- create_goal()
- bootstrap_session()  
- execute_preflight()
- execute_postflight()
- create_goal_checkpoint()
etc.

Empirica will NOT capture epistemic data unless you call these functions.
```

### 2. Required Setup
```markdown
Before using Empirica, ensure:
1. Session is bootstrapped with appropriate configuration
2. Personas are properly defined with epistemic priors
3. AI identity is created and keypair loaded
4. All 13 epistemic vectors are initialized
5. Appropriate dependencies are installed (qdrant-client, git, cryptography, etc.)
```

### 3. Common Pitfalls
```markdown
❌ DON'T: Write code and hope empirica tracks it
✅ DO: Call empirica.execute_preflight() BEFORE work
  
❌ DON'T: Use raw git commits for formal work
✅ DO: Use empirica.create_git_checkpoint() to create verifiable records

❌ DON'T: Trust that systems will "just work"
✅ DO: Test empirica usage end-to-end early in your session
```

### 4. API Contract
```markdown
Empirica provides:
- SigningPersona: Bind personas to Ed25519 keys
- PersonaRegistry: Semantic search of personas
- SignedGitOperations: Store signed states in git
- CanonicalEpistemicAssessor: Validate epistemic states

These are tools. They don't work unless you use them.
```

---

## Recommendations

### For Users (AI and Human)

1. **Start with explicit empirica usage**
   - Run `empirica bootstrap` before major work
   - Call `execute_preflight()` at session start
   - Call `execute_postflight()` at completion

2. **Test empirica integration early**
   - Don't assume it works
   - Create test goal and checkpoint
   - Verify git notes contain signed state

3. **Understand the dependencies**
   - Empirica requires: cryptography, GitPython, qdrant-client, etc.
   - Check environment has all packages
   - Install with: `pip install empirica[full]`

4. **Use proper configuration**
   - Don't rely on defaults
   - Define personas explicitly
   - Set epistemic priors based on domain knowledge
   - Create proper keypairs in `.empirica/identity/`

### For Empirica Developers

1. **Document API signatures clearly**
   - Parameter names matter (epistemic_vectors vs epistemic_state)
   - Type hints should be strict
   - Examples should be complete and tested

2. **Consider sensible defaults**
   - Pre-built personas for common use cases
   - Default bootstrap configuration
   - Template keypair generation

3. **Improve error messages**
   - Don't just say "file not found"
   - Suggest how to create missing files
   - Validate user input early and clearly

4. **Test integration thoroughly**
   - Package naming conflicts (git vs empirica.core.git)
   - Dependency installation
   - End-to-end workflows

---

## Conclusion

Empirica Phase 1 **DOES WORK** when used properly. But it requires:
- Understanding the architecture
- Explicit invocation
- Proper configuration
- Awareness of dependencies

**This is not a flaw - it's correct design.**

Empirica is not meant to be invisible middleware. It's meant to be deliberately used for formal, verified reasoning work. Users should know they're using it.

The system prompt should make this crystal clear.

