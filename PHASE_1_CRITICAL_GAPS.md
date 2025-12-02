# Phase 1: Critical Gaps & Design Holes

**Analysis Date:** 2025-12-02
**Status:** 🔴 BLOCKING ISSUES - Must resolve before production

---

## 🚨 CRITICAL GAPS

### 1. **Persona Identity Binding (BLOCKING)**

**The Problem:**
```python
persona_id = "researcher"  # Just a string
public_key = "35f9902740ff76f3..."  # Also just a string
```

There's **no cryptographic link** between persona_id and public_key. Anyone can:
- Create a different keypair and claim to be "researcher"
- Impersonate any persona
- Register multiple "researcher" personas with different keys

**Current Code:** SigningPersona assumes the public_key in the config matches the identity, but there's no verification.

**Missing:**
- Persona_id should be a hash of (name + public_key) or similar
- Or: signed registration proof (Sentinel must approve new personas)
- Or: out-of-band key distribution (hardcoded trusted keys)

**Impact:** HIGH - Any AI could impersonate any persona

---

### 2. **Private Key Security (CRITICAL)**

**The Problem:**
```python
# .empirica/identity/researcher.key with 0600 permissions
{
  "private_key": "hex_encoded_key",  # PLAINTEXT in file
  "public_key": "...",
  "created_at": "..."
}
```

**Vulnerabilities:**
- Keys stored in plaintext on disk
- No key rotation mechanism
- No key expiration/revocation
- If filesystem compromised → entire persona compromised
- No protection against key cloning
- No audit log of key usage

**Missing:**
- Key encryption at rest (KMS or passphrase protection)
- Key rotation schedule
- Key revocation list (Qdrant or Git-based)
- Usage audit logging
- Key expiration dates

**Impact:** CRITICAL - Compromised key = persona impersonation forever

---

### 3. **Qdrant Trust (CRITICAL)**

**The Problem:**
```python
# Anyone with Qdrant access can:
registry.register_persona(fake_persona)  # No validation
```

Qdrant is treated as **trusted storage** but:
- No authentication required to write personas
- No audit trail of registrations
- No verification that registrant has authority
- Anyone can modify Qdrant and add fake personas
- No way to distinguish "official" MCO personas from attacker personas

**Missing:**
- Qdrant authentication/authorization
- Audit logging of all persona registrations
- Signed registration proofs (Sentinel approval)
- Ability to revoke/disable personas
- Out-of-band persona verification

**Impact:** HIGH - Qdrant becomes a trust boundary that's not protected

---

### 4. **Git Integrity (HIGH)**

**The Problem:**
```bash
# Signed state is in git notes, but notes can be:
git notes remove <commit>              # Delete the signature
git notes edit <commit>                # Modify the signature
git filter-branch                      # Rewrite history
git reset --hard <old-commit>         # Go back in time
```

The **signature is in the note, not protecting the note itself**.

**Scenarios:**
1. Attacker deletes git notes → signature disappears but commit remains
2. Attacker modifies notes → signature becomes invalid (detectable) but note is gone
3. Git history rewritten → signatures no longer in the "official" chain
4. Qdrant still has copies of signatures even if Git is cleaned

**Missing:**
- Signed commits (GPG/SSH signature on the commit itself)
- Notes protection mechanism
- Immutable ledger (Qdrant as source of truth?)
- Merkle chain of CASCADE phases
- Detection of history rewriting

**Impact:** HIGH - Git is mutable, signatures don't protect the Git state

---

### 5. **Public Key Distribution & Trust (CRITICAL)**

**The Problem:**
```python
# In the signed state:
"public_key": "35f9902740ff76f3..."
```

How do you KNOW this public key belongs to "researcher"?

- No certificate authority
- No key fingerprinting
- No key server
- No verification chain
- Qdrant stores it, but Qdrant itself is untrusted

**If you want to verify a signature**, you need:
1. The public key (from where?)
2. Proof that this key belongs to the persona (from where?)
3. Proof that this proof is authentic (from where?)

**Missing:**
- Key fingerprints (short identifiers)
- Web of trust or CA model
- Key verification protocol
- PIN/code for key verification
- Out-of-band key distribution

**Impact:** CRITICAL - You can't actually verify anyone

---

### 6. **CASCADE Phase Enforcement (HIGH)**

**The Problem:**
No validation that:
- Phases happen in order (PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT)
- All phases are completed
- All required personas sign off
- No phases are skipped

**Missing:**
```python
# Should enforce:
if prev_phase != "PREFLIGHT" and current_phase == "INVESTIGATE":
    raise ValueError("Must complete PREFLIGHT first")

# Should require:
required_personas = ["researcher", "reviewer", "coordinator"]
missing = set(required_personas) - set(personas_who_signed)
if missing:
    raise ValueError(f"Missing: {missing}")
```

**Impact:** MEDIUM - CASCADE can be bypassed or malformed

---

### 7. **Sentinel Not Implemented (BLOCKING)**

**The Problem:**
The vision requires Sentinel to:
- Approve new personas
- Verify CASCADE phases
- Collapse multiple persona outputs
- Act as governance layer

**Current State:** Sentinel is just another persona, with no special authority.

**Missing:**
- Sentinel as privileged role
- Sentinel sign-off required for CASCADE completion
- Sentinel authority over persona registration
- Sentinel final output verification
- Sentinel configuration/policies

**Impact:** BLOCKING - Whole governance model missing

---

### 8. **Timestamp & Replay Attacks (HIGH)**

**The Problem:**
```python
"timestamp": datetime.now(UTC).isoformat()  # Persona's clock
```

Issues:
- Persona controls its own timestamp (could be wrong)
- No independent timestamp verification
- Old signatures can be reused in new CASCADE chains
- No nonce to prevent replay

**Scenario:**
```
1. Researcher signs state at T1: "know=0.60"
2. Later, use same signature at T2 in different CASCADE
3. Or: Researcher's clock wrong, says T3 but actually T2
```

**Missing:**
- Git commit timestamp as authoritative time
- Nonce/unique ID per CASCADE
- Timestamp validation (can't be in future)
- Replay attack protection

**Impact:** MEDIUM-HIGH - Signatures can be replayed

---

### 9. **Model-Specific Bias Not Captured (MEDIUM)**

**The Problem:**
model_profiles.yaml defines bias corrections per model:
```yaml
claude_sonnet:
  uncertainty: "underestimated"  # Sonnet underestimates uncertainty

gpt4:
  uncertainty: "slight_overconfident"  # GPT-4 is overconfident
```

But:
- Signing doesn't capture which model/bias was applied
- Can't verify "this uncertainty vector had bias correction applied"
- Same persona_id for Claude vs GPT but different actual biases

**Missing:**
- `model_id` or `ai_implementation` in signed state
- Bias correction proof/audit trail
- Model-specific persona versions (researcher_claude vs researcher_gpt4)
- Calibration verification

**Impact:** MEDIUM - Reasoning might be biased without knowing

---

### 10. **Persona Versioning (MEDIUM)**

**The Problem:**
```python
# Version stored but not enforced
version="1.0.0"

# What if epistemic priors change?
# researcher_v1 might have: know=0.60
# researcher_v2 might have: know=0.70
# Old signatures won't validate with new definition
```

**Missing:**
- Version pinning (CASCADE uses specific persona version)
- Backward compatibility guarantees
- Version migration strategy
- Ability to look up historical persona definitions

**Impact:** MEDIUM - Personas could be inconsistent over time

---

### 11. **Reputation Scoring (MEDIUM)**

**The Problem:**
PersonaProfile includes:
```python
reputation_score: 0.75  # But who set this?
```

Current implementation:
- Reputation is static
- No mechanism to UPDATE based on outcomes
- No measurement of actual calibration
- No consequence for poor performance

**Missing:**
- Dynamic reputation updates
- Calibration measurement (how right were the vectors?)
- Reputation decay over time
- Penalty for overconfidence/underconfidence
- Reputation increase for accuracy

**Impact:** MEDIUM - Reputation is meaningless

---

### 12. **Capabilities Not Enforced (MEDIUM)**

**The Problem:**
PersonaProfile has:
```python
capabilities = {
    "can_modify_code": True,
    "can_call_external_tools": True,
    "requires_human_approval": False
}
```

But SigningPersona **never checks these**. Anyone with the private key can:
- Sign anything (ignores capability limits)
- Claim to be doing things they shouldn't
- There's no enforcement mechanism

**Missing:**
- Capability checking in sign_epistemic_state()
- Enforcement at CASCADE execution time
- Proof of which operations were performed
- Audit trail of capability usage

**Impact:** LOW - But breaks the capability design entirely

---

### 13. **Revocation Missing (CRITICAL)**

**The Problem:**
If a private key leaks:
- No way to mark persona as revoked
- Old signatures still appear valid
- No way to say "ignore all signatures from this persona after timestamp X"

**Missing:**
- Revocation list (in Qdrant or Git)
- Expiration dates on keys
- Revocation mechanism
- Detection of key compromise

**Impact:** CRITICAL - Leaked keys can't be disabled

---

### 14. **Git & Qdrant Divergence (HIGH)**

**The Problem:**
Two sources of truth:
- Git notes (signed states)
- Qdrant (persona registry + reputation)

What if they diverge?
```
Scenario:
1. Sign state in Git at T1
2. Persona deleted from Qdrant at T2
3. Now Git has signature from "deleted" persona
4. Or: Reputation updated in Qdrant but Git signature unchanged
```

**Missing:**
- Single source of truth
- Synchronization mechanism
- Conflict resolution
- Merkle proofing across systems

**Impact:** MEDIUM - Systems can become inconsistent

---

### 15. **No Audit Log (HIGH)**

**The Problem:**
Who signed what when? There's no audit trail of:
- Persona registrations (who added them to Qdrant?)
- Key generations
- Signature operations
- Qdrant writes
- Git writes

**Missing:**
- Immutable audit log
- Access logging
- Change logging
- Integration with security systems

**Impact:** HIGH - Can't answer "what happened?"

---

### 16. **Metadata Not Validated (LOW)**

**The Problem:**
```python
metadata = {
    "tags": ["mco", "researcher", "builtin"],  # Any string
    "focus_domains": [...],  # Any string
    "description": "..."  # Any text
}
```

No schema validation on metadata. Someone could:
- Add misleading tags
- Claim false specializations
- Inject malicious descriptions

**Missing:**
- Metadata schema validation
- Allowed values for tags/domains
- Metadata signing/verification

**Impact:** LOW - But enables deception

---

## 📊 Severity Summary

| Severity | Count | Examples |
|----------|-------|----------|
| 🔴 BLOCKING | 3 | Persona identity binding, Sentinel, Git integrity |
| 🔴 CRITICAL | 5 | Private keys, Qdrant trust, Key distribution, Revocation |
| 🟠 HIGH | 7 | CASCADE enforcement, Timestamps, Audit logs, Divergence |
| 🟡 MEDIUM | 8 | Bias capture, Versioning, Reputation, Capabilities |
| 🟢 LOW | 2 | Metadata validation |

---

## 🎯 Top 5 Must-Fix Issues

### #1: Persona Identity Binding
**Status:** BLOCKING
**Effort:** Medium
**Solution Options:**
- A) Persona_id = SHA256(name, public_key) - immutable identity
- B) Signed registration proof (Sentinel approves, signs persona_id+key)
- C) Hardcoded trusted personas with keys

### #2: Private Key Security
**Status:** CRITICAL
**Effort:** Medium
**Solution Options:**
- A) Encrypt keys with passphrase (KMS integration)
- B) Hardware security module (HSM)
- C) Key rotation mechanism + expiration dates

### #3: Public Key Trust Chain
**Status:** CRITICAL
**Effort:** High
**Solution Options:**
- A) Certificate authority (CA) model
- B) Web of trust (personas signing each other's keys)
- C) Hardcoded key distribution (boring but secure)

### #4: Sentinel Implementation
**Status:** BLOCKING
**Effort:** High
**Solution Options:**
- A) Sentinel as privileged persona (must approve all operations)
- B) Sentinel as separate system (external validator)
- C) Multi-sig model (majority of senior personas approval)

### #5: Git & Qdrant Consistency
**Status:** HIGH
**Effort:** Medium
**Solution Options:**
- A) Qdrant as source of truth, Git as implementation detail
- B) Git as source of truth, Qdrant as cache
- C) Merkle tree linking them together

---

## 🔧 What Works Today

✅ Basic signing/verification (cryptography is sound)
✅ Persona creation and storage
✅ Epistemic state capture
✅ Semantic search by domain
✅ Individual signature verification

---

## ❌ What Doesn't Work

❌ Persona identity verification (who is "researcher"?)
❌ Key management (lost key = lost persona)
❌ Distributed trust (no way to verify from external system)
❌ Enforcement of CASCADE structure
❌ Governance (Sentinel missing)
❌ Audit trails (no logging)
❌ Revocation (can't disable personas)
❌ Consistency (Git and Qdrant can diverge)

---

## 🛠️ Recommended Fix Priority

```
Phase 1.5: SECURITY HARDENING
├─ [BLOCKING] Persona identity binding
├─ [CRITICAL] Private key encryption + management
├─ [CRITICAL] Public key trust mechanism
├─ [BLOCKING] Sentinel implementation
├─ [HIGH] Audit logging
└─ [HIGH] CASCADE phase enforcement

Phase 2: Session Replay (unchanged - uses Phase 1.5)

Phase 3: Browser Extension (unchanged)
```

---

## Questions to Answer

1. **Trust Model:** Who do we trust? (Qdrant admin? Git repo owner? Sentinel? External PKI?)
2. **Threat Model:** What attacks are we protecting against? (Insider? Attacker with key access? Attacker with Qdrant access?)
3. **Revocation:** If a persona is compromised, how do we kill it?
4. **Consistency:** If Git and Qdrant disagree, which is truth?
5. **Key Distribution:** How do external systems verify a persona's public key?
6. **Governance:** Who approves new personas? Who can modify personas?

---

## Conclusion

**Phase 1 is cryptographically sound but structurally incomplete.**

The signing/verification math works, but without solving the identity binding, key management, and governance layers, the system is:
- ✅ Technically correct
- ❌ Practically unusable
- ❌ Not production-ready
- ❌ Vulnerable to impersonation

**Recommendation:** Before moving to Phase 2, invest in Phase 1.5 security hardening focusing on identity binding and Sentinel implementation.

---

**Risk Level:** 🔴 DO NOT DEPLOY TO PRODUCTION without addressing BLOCKING issues
