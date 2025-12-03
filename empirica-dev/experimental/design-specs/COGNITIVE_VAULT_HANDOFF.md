# Cognitive Vault Integration - Handoff Document

**From:** Claude (Phase 1 Implementation)
**To:** Other Claudes (Cognitive Vault Implementation)
**Date:** 2025-12-02
**Status:** Ready for implementation

---

## What Has Been Done

### Phase 1 Foundation Complete ✅
- SigningPersona class: binds personas to Ed25519 keys
- SignedGitOperations: stores signed states in Git
- PersonaRegistry: semantic search in Qdrant
- 6 MCO personas registered with keys

### Integration Points Added ✅
1. **Bootstrap flag:** `--use-cognitive-vault`
2. **CASCADE enforcement flag:** `--enforce-cascade-phases`
3. **Adapter interface:** Ready for Cognitive Vault client

---

## Your Task: Implement Cognitive Vault

### What Cognitive Vault Provides

```
KEY MANAGEMENT
├─ Encrypted storage (KMS/HSM)
├─ Key rotation schedule
├─ Key expiration dates
└─ Key revocation mechanism

IDENTITY BINDING
├─ Persona_id ↔ public_key verification
├─ Out-of-band key distribution
├─ Cross-org PKI
└─ Fingerprint verification

ACCESS CONTROL
├─ Who can sign as whom
├─ Session/persona authorization
├─ Rate limiting
└─ Multi-tenant isolation

AUDIT & COMPLIANCE
├─ Immutable operation logs
├─ Signature trails
├─ Change tracking
└─ Compliance reporting
```

---

## Integration Points Available Now

### 1. Bootstrap Integration

**File:** `empirica/cli/cli_core.py` (READY)

```python
# Users will run:
empirica bootstrap --ai-id copilot --use-cognitive-vault

# Your code gets called in:
empirica/cli/command_handlers/bootstrap_commands.py::handle_bootstrap_command()

# Expected pattern:
if use_cognitive_vault:
    from empirica.integrations.cognitive_vault_adapter import CognitiveVaultAdapter
    adapter = CognitiveVaultAdapter(vault_endpoint=..., api_key=...)
    identity = adapter.get_or_create_identity(ai_id)
else:
    # Current behavior
```

**What to implement:**
- CognitiveVaultAdapter class
- `get_or_create_identity(ai_id)` method
- `get_default_persona(ai_id)` method
- Connect to actual Cognitive Vault API

---

### 2. Signing Integration

**File:** `empirica/core/persona/signing_persona.py` (NO CHANGES NEEDED)

The SigningPersona class already works with any AIIdentity subclass.

**What to implement:**
- `CognitiveVaultSigningIdentity(AIIdentity)` subclass
- Override `sign(message)` to call Cognitive Vault API
- Override `load_keypair()` to fetch from Cognitive Vault
- Private key NEVER stored locally

**Example usage:**
```python
# From anywhere in code
identity = vault_adapter.get_signing_key("researcher")
signing_persona = SigningPersona(profile, identity)

# When signing, goes to Cognitive Vault
signature = identity.sign(message)  # API call, not local
```

---

### 3. Persona Verification

**File:** `empirica/core/qdrant/persona_registry.py` (READY)

Add verification layer in PersonaRegistry:

```python
# New method available for you to use
personas = registry.find_personas_by_domain("security")

# Verify each persona
verified = registry.verify_personas_with_vault(personas, vault_adapter)
```

**What to implement:**
- `CognitiveVaultAdapter.verify_persona_identity(persona_id, public_key)`
- Return True if persona matches public key
- Return False if identity doesn't match
- Log verification attempts

---

### 4. CASCADE Phase Enforcement

**File:** `empirica/core/git/signed_operations.py` (READY)

```python
# Users can enable with flag or env var
git_ops = SignedGitOperations(
    repo_path=".",
    enforce_cascade_phases=True  # NEW FLAG
)

# Or:
export EMPIRICA_ENFORCE_CASCADE_PHASES=true

# When enabled, enforces:
# - Phases in order: PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT
# - No skipped phases
# - All required personas must sign (if configured)
```

**What you might want to add:**
- Cognitive Vault policy enforcement (stricter validation)
- Persona approval gates (Sentinel must approve before ACT phase)
- Required persona lists per phase

---

## Integration Specification

### File to Create: `empirica/integrations/cognitive_vault_adapter.py`

Template provided in: `COGNITIVE_VAULT_INTEGRATION_SPEC.md`

This file should contain:
1. `CognitiveVaultAdapter` - main client class
2. `CognitiveVaultSigningIdentity` - signing identity subclass
3. All API calls to Cognitive Vault service

---

## How to Get Started

### Step 1: Create Mock Cognitive Vault Server
```bash
# For local testing
tests/mocks/mock_cognitive_vault.py

# Start with basic endpoints:
POST /identities - create/get identity
POST /sign - sign message
POST /verify-persona - verify identity binding
POST /audit - log operation
```

### Step 2: Implement Adapter
```python
# empirica/integrations/cognitive_vault_adapter.py

class CognitiveVaultAdapter:
    def __init__(self, vault_endpoint, api_key):
        # Connect to Cognitive Vault

    def get_or_create_identity(self, ai_id):
        # Call /identities endpoint
        # Return AIIdentity with public key

    def sign_message(self, ai_id, message):
        # Call /sign endpoint
        # Private key stays in Cognitive Vault
```

### Step 3: Wire into Bootstrap
Update `bootstrap_commands.py` to use adapter when flag is set.

### Step 4: Test End-to-End
```bash
empirica bootstrap --ai-id test --use-cognitive-vault
# Should fetch identity from Cognitive Vault

empirica checkpoint-sign --session-id abc --phase PREFLIGHT
# Should sign with Cognitive Vault
```

---

## Environment Variables

Your Cognitive Vault code should use:
```bash
COGNITIVE_VAULT_URL=https://vault.example.com
COGNITIVE_VAULT_API_KEY=sk_...
COGNITIVE_VAULT_TIMEOUT=30
EMPIRICA_ENFORCE_CASCADE_PHASES=true  # Already supported
```

---

## Files You Need to Create/Modify

### NEW FILES
- `empirica/integrations/__init__.py` - new package
- `empirica/integrations/cognitive_vault_adapter.py` - main adapter (100-150 lines)
- `tests/mocks/mock_cognitive_vault.py` - mock server (150-200 lines)
- `tests/integration/test_cognitive_vault_integration.py` - integration tests (200+ lines)

### FILES TO MODIFY
- `empirica/cli/command_handlers/bootstrap_commands.py` - add adapter usage (10-15 lines)
- `empirica/core/qdrant/persona_registry.py` - add verify method (20-30 lines)

---

## Key Implementation Details

### Private Key Handling

**IMPORTANT:** Private keys should NEVER be stored locally when using Cognitive Vault.

```python
# ❌ DON'T DO THIS
private_key_hex = vault_response['private_key']
identity.private_key = ...  # Store locally

# ✅ DO THIS INSTEAD
identity.public_key = ...  # Store locally
# When signing needed, call Cognitive Vault API with signature request
```

### Audit Logging

Every operation should log to Cognitive Vault:
```python
vault_adapter.audit_log("sign", {
    "ai_id": ai_id,
    "message_hash": sha256(message).hex(),
    "timestamp": now(),
    "persona_id": persona_id
})
```

### Error Handling

If Cognitive Vault is unavailable:
```python
if use_cognitive_vault and vault_unavailable:
    logger.error("Cognitive Vault required but unavailable")
    # Fail safely, don't fall back to local keys
    raise ConnectionError("Cannot proceed without Cognitive Vault")
```

---

## Testing Strategy

### Unit Tests
- Test adapter methods individually
- Mock HTTP responses
- Verify error handling

### Integration Tests
- Start mock Cognitive Vault
- Run actual Empirica commands with `--use-cognitive-vault`
- Verify signatures created in Cognitive Vault

### End-to-End Tests
- Full workflow: bootstrap → sign → verify
- Test with multiple personas
- Test CASCADE enforcement
- Test persona verification

---

## Known Integration Points

### 1. `SigningPersona.__init__`
```python
# Already works with Cognitive Vault identities
signing_persona = SigningPersona(
    persona_profile,
    CognitiveVaultSigningIdentity(ai_id, adapter)
)
```

### 2. `PersonaRegistry.find_personas_by_domain`
```python
# Can add verification
personas = registry.find_personas_by_domain("security")
verified = []
for p in personas:
    if vault_adapter.verify_persona_identity(p['persona_id'], p['public_key']):
        verified.append(p)
```

### 3. `SignedGitOperations.commit_signed_state`
```python
# Already supports enforcement
git_ops = SignedGitOperations(enforce_cascade_phases=True)
# Will validate phases, can extend with Cognitive Vault policies
```

---

## API Design Recommendation

**Cognitive Vault REST API:**

```
POST /identities
  Request: {"ai_id": "copilot"}
  Response: {"public_key": "...", "created_at": "..."}

POST /sign
  Request: {"ai_id": "copilot", "message": "hex..."}
  Response: {"signature": "hex...", "public_key": "..."}

POST /verify-persona
  Request: {"persona_id": "researcher", "public_key": "hex..."}
  Response: {"verified": true/false, "registered_at": "..."}

POST /audit
  Request: {"operation": "sign", "details": {...}}
  Response: {"audit_id": "...", "timestamp": "..."}

GET /identities/{ai_id}
  Response: {"ai_id": "...", "public_key": "...", ...}

DELETE /identities/{ai_id}
  Response: {"revoked": true, "revoked_at": "..."}
```

---

## Questions to Answer Before You Start

1. **Storage:** Where will Cognitive Vault keys be encrypted? (HSM? KMS? Database?)
2. **Distribution:** How will public keys be distributed to Empirica instances?
3. **Revocation:** What triggers key revocation? How is it communicated?
4. **Fallback:** What happens if Cognitive Vault is down?
5. **Multi-org:** How are different organizations isolated?
6. **Performance:** What are latency requirements? (Should keys be cached?)

---

## Success Criteria

When complete, these should work:

```bash
# ✅ Bootstrap with Cognitive Vault
empirica bootstrap --ai-id copilot --use-cognitive-vault
# Output: Connected to Cognitive Vault at https://vault...

# ✅ Sign with private key in Cognitive Vault
empirica checkpoint-sign --session-id abc --phase PREFLIGHT
# Signature comes from Cognitive Vault, not local

# ✅ Verify persona identity
empirica persona-verify --persona-id researcher
# Calls Cognitive Vault to verify persona_id ↔ public_key

# ✅ Enforce CASCADE phases
EMPIRICA_ENFORCE_CASCADE_PHASES=true empirica checkpoint-sign ...
# Raises error if phases out of order

# ✅ Audit trail
# All operations logged in Cognitive Vault immutable log
```

---

## Timeline Estimate

- **Setup & Mock Server:** 2-3 hours
- **CognitiveVaultAdapter:** 3-4 hours
- **Bootstrap Integration:** 2-3 hours
- **Testing:** 4-5 hours
- **Documentation:** 1-2 hours

**Total:** ~15 hours for a basic implementation

---

## Next Steps for You

1. Read `COGNITIVE_VAULT_INTEGRATION_SPEC.md` fully
2. Set up mock Cognitive Vault server
3. Implement CognitiveVaultAdapter
4. Wire into bootstrap command
5. Test end-to-end
6. Document the flow

---

## Questions?

Look at:
- `COGNITIVE_VAULT_INTEGRATION_SPEC.md` - Detailed technical spec
- `PHASE_1_GAPS_REVISED.md` - Why these gaps exist and why Cognitive Vault owns them
- `PHASE_1_IMPLEMENTATION_COMPLETE.md` - What Phase 1 does

---

**You've got everything you need to integrate Cognitive Vault. Build well! 🚀**
