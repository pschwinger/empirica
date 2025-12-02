# Cognitive Vault Integration Specification

**For:** Other Claudes implementing Cognitive Vault
**Date:** 2025-12-02
**Status:** Ready for implementation

---

## Overview

Empirica Phase 1 provides epistemic signing infrastructure. Cognitive Vault provides the security layer (key management, identity binding, access control).

This document specifies how they integrate.

---

## Integration Points

### 1. Bootstrap Integration (IMMEDIATE)

**Bootstrap with Cognitive Vault:**

```bash
# Current (local keys)
empirica bootstrap --ai-id copilot --onboard

# With Cognitive Vault
empirica bootstrap --ai-id copilot --onboard --use-cognitive-vault
```

**File to modify:** `empirica/cli/command_handlers/bootstrap_commands.py`

**Changes needed:**
```python
def handle_bootstrap_command(args):
    ai_id = args.ai_id
    use_cognitive_vault = getattr(args, 'use_cognitive_vault', False)

    if use_cognitive_vault:
        # Fetch identity from Cognitive Vault instead of generating locally
        from empirica.integrations.cognitive_vault_adapter import CognitiveVaultAdapter

        adapter = CognitiveVaultAdapter(
            vault_endpoint=os.getenv("COGNITIVE_VAULT_URL"),
            api_key=os.getenv("COGNITIVE_VAULT_API_KEY")
        )

        identity = adapter.get_or_create_identity(ai_id)
        persona = adapter.get_default_persona(ai_id)
    else:
        # Current behavior: generate locally
        identity = generate_local_identity(ai_id)
        persona = create_default_persona(ai_id)

    # Rest of bootstrap...
```

**CLI Parser change:**
```python
bootstrap_parser.add_argument(
    '--use-cognitive-vault',
    action='store_true',
    help='Use Cognitive Vault for key management and personas'
)
```

---

### 2. SigningPersona Integration

**Current code:**
```python
from empirica.core.identity.ai_identity import AIIdentity
from empirica.core.persona.signing_persona import SigningPersona

identity = AIIdentity(ai_id="researcher")
identity.load_keypair()  # Loads from local .empirica/identity/

signing_persona = SigningPersona(profile, identity)
```

**With Cognitive Vault:**
```python
if use_cognitive_vault:
    identity = CognitiveVaultAdapter.get_signing_key("researcher")
else:
    identity = AIIdentity(ai_id="researcher")
    identity.load_keypair()

signing_persona = SigningPersona(profile, identity)
```

**File:** `empirica/core/persona/signing_persona.py` (no changes needed - works with any AIIdentity)

---

### 3. PersonaRegistry Integration

**Current code:**
```python
registry = PersonaRegistry()
personas = registry.find_personas_by_domain("security")
```

**With Cognitive Vault:**
```python
if use_cognitive_vault:
    registry = PersonaRegistry()
    # Add verification layer
    personas = registry.find_personas_by_domain("security")

    # Verify each persona with Cognitive Vault
    for persona in personas:
        is_verified = CognitiveVaultAdapter.verify_persona_identity(
            persona["persona_id"],
            persona["public_key"]
        )
        if not is_verified:
            logger.warning(f"Persona {persona['persona_id']} failed verification")
else:
    registry = PersonaRegistry()
    personas = registry.find_personas_by_domain("security")
```

**File:** `empirica/core/qdrant/persona_registry.py`

**Add method:**
```python
class PersonaRegistry:
    def verify_personas_with_vault(self, personas, vault_adapter):
        """Verify personas with Cognitive Vault"""
        verified = []
        for persona in personas:
            try:
                if vault_adapter.verify_persona_identity(
                    persona["persona_id"],
                    persona["public_key"]
                ):
                    verified.append(persona)
            except Exception as e:
                logger.warning(f"Verification failed: {e}")
        return verified
```

---

### 4. CASCADE Phase Enforcement

**Current:** SignedGitOperations stores signed states but doesn't enforce CASCADE phases.

**With enforcement flag:**
```python
git_ops = SignedGitOperations(
    repo_path=".",
    enforce_cascade_phases=True  # NEW
)

# This will raise error if:
# - Phases out of order
# - Phases skipped
# - Required personas missing
# - Phase already completed
```

**File:** `empirica/core/git/signed_operations.py`

**Add:**
```python
class SignedGitOperations:
    def __init__(self, repo_path: str = ".", enforce_cascade_phases: bool = False):
        self.repo = git.Repo(repo_path)
        self.enforce_cascade_phases = enforce_cascade_phases

    def commit_signed_state(self, signing_persona, epistemic_state,
                           phase, message, required_personas=None):
        """Store signed state with optional phase enforcement"""

        if self.enforce_cascade_phases:
            self._validate_phase_sequence(phase, required_personas)

        # Continue with normal flow...

    def _validate_phase_sequence(self, phase, required_personas=None):
        """Enforce CASCADE phase order"""
        CASCADE_ORDER = ["PREFLIGHT", "INVESTIGATE", "CHECK", "ACT", "POSTFLIGHT"]

        # Get last phase from git log
        last_phase = self._get_last_phase()

        if last_phase:
            if CASCADE_ORDER.index(phase) <= CASCADE_ORDER.index(last_phase):
                raise ValueError(f"Phase {phase} cannot follow {last_phase}")

        if required_personas:
            # Check all required personas have signed
            pass
```

**Environment variable option:**
```bash
export EMPIRICA_ENFORCE_CASCADE_PHASES=true
empirica checkpoint-sign --session-id abc --phase PREFLIGHT --round 1
```

---

### 5. Cognitive Vault Adapter Interface

**Create new file:** `empirica/integrations/cognitive_vault_adapter.py`

```python
"""
Adapter for integrating with Cognitive Vault

Cognitive Vault provides:
- Key management (encrypted storage, HSM integration)
- Identity binding (persona_id ↔ public_key verification)
- Access control (who can sign as whom)
- Audit logging (immutable trail of all operations)
- Revocation mechanism (disable compromised personas)
"""

class CognitiveVaultAdapter:
    """Client for Cognitive Vault service"""

    def __init__(self, vault_endpoint: str, api_key: str):
        self.endpoint = vault_endpoint
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {api_key}"

    def get_or_create_identity(self, ai_id: str) -> AIIdentity:
        """Get or create Ed25519 identity from Cognitive Vault

        Returns:
            AIIdentity with public key, but private key stored in Cognitive Vault
        """
        response = self.session.post(
            f"{self.endpoint}/identities",
            json={"ai_id": ai_id}
        )
        response.raise_for_status()

        data = response.json()

        # Create local AIIdentity wrapper (no private key locally)
        identity = AIIdentity(ai_id)
        identity.public_key = Ed25519PublicKey.from_public_bytes(
            bytes.fromhex(data["public_key"])
        )

        return identity

    def get_signing_key(self, ai_id: str) -> AIIdentity:
        """Get identity for signing (private key stays in Cognitive Vault)"""
        # Returns AIIdentity that delegates signing to Cognitive Vault
        return CognitiveVaultSigningIdentity(ai_id, self)

    def sign_message(self, ai_id: str, message: bytes) -> bytes:
        """Sign message with Cognitive Vault (private key never leaves Cognitive Vault)"""
        response = self.session.post(
            f"{self.endpoint}/sign",
            json={
                "ai_id": ai_id,
                "message": message.hex()
            }
        )
        response.raise_for_status()
        return bytes.fromhex(response.json()["signature"])

    def verify_persona_identity(self, persona_id: str, public_key_hex: str) -> bool:
        """Verify persona_id matches public_key"""
        response = self.session.post(
            f"{self.endpoint}/verify-persona",
            json={
                "persona_id": persona_id,
                "public_key": public_key_hex
            }
        )
        response.raise_for_status()
        return response.json()["verified"]

    def get_default_persona(self, ai_id: str):
        """Get default persona for AI"""
        response = self.session.get(
            f"{self.endpoint}/personas/{ai_id}"
        )
        response.raise_for_status()
        return response.json()

    def audit_log(self, operation: str, details: dict):
        """Log operation to immutable audit trail"""
        response = self.session.post(
            f"{self.endpoint}/audit",
            json={
                "operation": operation,
                "details": details,
                "timestamp": datetime.now(UTC).isoformat()
            }
        )
        response.raise_for_status()


class CognitiveVaultSigningIdentity(AIIdentity):
    """AIIdentity that delegates signing to Cognitive Vault"""

    def __init__(self, ai_id: str, adapter: CognitiveVaultAdapter):
        super().__init__(ai_id)
        self.adapter = adapter

    def sign(self, message: bytes) -> bytes:
        """Sign with Cognitive Vault (private key never leaves Cognitive Vault)"""
        signature = self.adapter.sign_message(self.ai_id, message)
        self.adapter.audit_log("sign", {
            "ai_id": self.ai_id,
            "message_hash": hashlib.sha256(message).hexdigest()
        })
        return signature

    def load_keypair(self):
        """Load public key from Cognitive Vault"""
        response = self.adapter.session.get(
            f"{self.adapter.endpoint}/identities/{self.ai_id}"
        )
        response.raise_for_status()
        data = response.json()

        self.public_key = Ed25519PublicKey.from_public_bytes(
            bytes.fromhex(data["public_key"])
        )
```

---

### 6. Configuration

**Environment variables for Cognitive Vault:**
```bash
COGNITIVE_VAULT_URL=https://vault.example.com
COGNITIVE_VAULT_API_KEY=sk_test_...
COGNITIVE_VAULT_TIMEOUT=30
EMPIRICA_ENFORCE_CASCADE_PHASES=true
```

**Config file: `.empirica/config.yaml`**
```yaml
cognitive_vault:
  enabled: true
  endpoint: https://vault.example.com
  api_key: ${COGNITIVE_VAULT_API_KEY}
  timeout: 30

cascade:
  enforce_phases: true
  required_personas:
    - researcher
    - reviewer
    - coordinator
```

---

## Implementation Checklist for Other Claudes

### Step 1: Create Cognitive Vault Adapter (2-3 hours)
- [ ] Create `empirica/integrations/cognitive_vault_adapter.py`
- [ ] Implement `CognitiveVaultAdapter` class
- [ ] Implement `CognitiveVaultSigningIdentity` class
- [ ] Add tests in `tests/unit/integrations/test_cognitive_vault_adapter.py`

### Step 2: Bootstrap Integration (1-2 hours)
- [ ] Add `--use-cognitive-vault` flag to bootstrap parser
- [ ] Update `bootstrap_commands.py` to use adapter
- [ ] Test with mock Cognitive Vault server
- [ ] Update bootstrap tests

### Step 3: SigningPersona Integration (30 minutes)
- [ ] Update SigningPersona to work with Cognitive Vault identities
- [ ] Test signing with vault-based keys
- [ ] Verify signatures still work

### Step 4: CASCADE Enforcement (1-2 hours)
- [ ] Add `enforce_cascade_phases` parameter to SignedGitOperations
- [ ] Implement phase validation logic
- [ ] Add environment variable support
- [ ] Add tests

### Step 5: PersonaRegistry Verification (1 hour)
- [ ] Add `verify_personas_with_vault()` method
- [ ] Update search to include verification
- [ ] Test cross-org persona verification

### Step 6: Documentation & Testing (1-2 hours)
- [ ] Write integration guide
- [ ] Create example .env file
- [ ] Add end-to-end tests with mock Cognitive Vault

---

## Testing Strategy

### Mock Cognitive Vault Server

For testing without actual Cognitive Vault:

```python
# tests/mocks/mock_cognitive_vault.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/identities', methods=['POST'])
def create_identity():
    ai_id = request.json['ai_id']
    # Generate test keypair
    test_key = Ed25519PrivateKey.generate()

    return jsonify({
        "ai_id": ai_id,
        "public_key": test_key.public_key().public_bytes(...).hex()
    })

@app.route('/sign', methods=['POST'])
def sign():
    message = bytes.fromhex(request.json['message'])
    signature = test_key.sign(message)
    return jsonify({"signature": signature.hex()})

# ... more endpoints
```

**Test with mock:**
```python
def test_bootstrap_with_mock_vault(mock_vault_server):
    with mock_vault_server:
        result = run_command("bootstrap --ai-id test --use-cognitive-vault")
        assert "✓ Connected to Cognitive Vault" in result
```

---

## Handoff Checklist

- [ ] This spec is clear
- [ ] Integration points are obvious
- [ ] Tests show expected behavior
- [ ] Mock server enables development
- [ ] Example .env provided
- [ ] CLI flags added
- [ ] Documentation complete

---

## Questions to Resolve with Cognitive Vault Team

1. **Key Format:** How should private keys be returned? (signed JWTs? Hardware tokens?)
2. **Revocation:** How are revoked personas signaled? (List? Timestamp? Event stream?)
3. **Audit Trail:** How do we access audit logs? (API? File export? Dashboard?)
4. **Multi-tenancy:** How do we isolate organizations' personas?
5. **Fallback:** What happens if Cognitive Vault is down? (Offline mode? Local signing?)
6. **Latency:** What are performance expectations? (Should we cache keys locally?)

---

## Success Criteria

When complete, these commands should work:

```bash
# Bootstrap with Cognitive Vault
empirica bootstrap --ai-id copilot --use-cognitive-vault

# Sign with Cognitive Vault (private key never leaves Cognitive Vault)
empirica checkpoint-sign --session-id abc --phase PREFLIGHT

# Verify Cognitive Vault persona
empirica persona-verify --persona-id researcher

# Enforce CASCADE phases
EMPIRICA_ENFORCE_CASCADE_PHASES=true empirica checkpoint-sign ...
```

---

**Ready for implementation. Good luck!** 🚀
