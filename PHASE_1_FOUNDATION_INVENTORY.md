# Phase 1: Cryptographic Foundation - Inventory

**Date:** 2025-12-02
**Status:** Foundation 90% complete - Ready for Phase 1 implementation

---

## ✅ What We Already Have

### 1. **Epistemic Vector System**
- ✅ 13-dimensional epistemic state fully defined
- ✅ Vectors: engagement, know, do, context, clarity, coherence, signal, density, state, change, completion, impact, uncertainty
- ✅ All on [0.0, 1.0] scale
- ✅ Stored in persona schema

### 2. **Persona System**
- ✅ PersonaManager class (create, load, save, validate personas)
- ✅ Comprehensive persona_schema.json with full validation
- ✅ Pre-defined templates:
  - ✅ Security Expert (KNOW=0.90, UNCERTAINTY=0.15)
  - ✅ UX Specialist (CONTEXT=0.85, CLARITY=0.85)
  - ✅ Performance Optimizer (DO=0.90, UNCERTAINTY=0.20)
  - ✅ Architecture Reviewer (COHERENCE=0.90)
  - ✅ Code Reviewer (ready to use)
  - ✅ Sentinel (orchestrator/governance)

### 3. **Ed25519 Keypair Infrastructure**
- ✅ AIIdentity class with Ed25519 support
- ✅ Keypair generation (Ed25519PrivateKey.generate())
- ✅ Secure storage (.empirica/identity/, 0600 permissions)
- ✅ Public key export (for distribution)
- ✅ JSON serialization for portability

### 4. **Storage Layer**
- ✅ Qdrant vector database (running on port 6333)
- ✅ One collection: mcm_reasoning_vectors (ready for personas)
- ✅ Supports semantic tagging/metadata
- ✅ Git integration (git notes for signed states)
- ✅ SQLite database for session tracking

### 5. **API Layer**
- ✅ Dashboard API (Flask, port 8000)
- ✅ 12 endpoints for querying epistemic data
- ✅ CORS enabled
- ✅ Can serve verified commit data

### 6. **Git Integration**
- ✅ Git state capture (Phase 2.5 complete)
- ✅ Can store data in git notes
- ✅ Ready for signed commits

### 7. **Forgejo Instance**
- ✅ Fresh Forgejo v13.0.3 running
- ✅ http://aiworkhorse.local:3000/
- ✅ Test repository: forgejo/empirica.git
- ✅ Test commit: b4610cb (README.md)
- ✅ Plugin directory ready: /var/lib/forgejo/plugins/empirica-epistemic-insight/

---

## ⚠️ What We Need to Build for Phase 1

### **Missing Piece 1: Sign Epistemic States**

What we have:
- AIIdentity class with signing capability
- Persona profiles with epistemic vectors

What we need:
```python
class SigningPersona:
    """Link personas to signing keys"""

    def __init__(self, persona_profile, ai_identity):
        self.persona = persona_profile
        self.identity = ai_identity  # Has private_key

    def sign_epistemic_state(self, state: Dict, phase: str) -> Dict:
        """Sign an epistemic state for a CASCADE phase"""
        canonical = {
            "persona": self.persona.persona_id,
            "phase": phase,
            "timestamp": datetime.now().isoformat(),
            "vectors": state,
            "public_key": self.identity.public_key.hex()
        }

        signature = self.identity.sign(json.dumps(canonical))
        return {"state": canonical, "signature": signature}

    def verify_signature(self, signed_state: Dict) -> bool:
        """Verify a signed epistemic state"""
        # ... verification logic
        pass
```

### **Missing Piece 2: Store Signed States in Git**

What we have:
- Git integration with git notes support
- Can make signed commits

What we need:
```python
class SignedGitOperations:
    """Store signed epistemic states in Git"""

    def commit_signed_state(self, persona: SigningPersona,
                          state: EpistemicState, phase: str):
        """Create a Git commit with signed epistemic state"""
        # 1. Sign the state with persona's key
        signed_state = persona.sign_epistemic_state(state, phase)

        # 2. Store in git notes
        git notes add --message=JSON(signed_state)

        # 3. Create signed commit
        git commit --gpg-sign=<persona_key> -m f"{phase}: {description}"

        return commit_sha, signature
```

### **Missing Piece 3: Verify Signature Chains**

What we have:
- AIIdentity can verify signatures
- Can read git log and git notes

What we need:
```python
class SignatureVerifier:
    """Verify chains of signed epistemic states"""

    def verify_cascade_chain(self, start_commit: str, end_commit: str):
        """Verify entire CASCADE trace is signed"""
        # Get commits between start and end
        # For each commit:
        #   - Verify GPG signature (git verify-commit)
        #   - Load git note (json)
        #   - Verify epistemic signature (with persona's public key)
        # Return: list of verified/unverified steps
```

### **Missing Piece 4: Persona Registry in Qdrant**

What we have:
- Qdrant running
- Persona schema with public_key field
- Personas can be created

What we need:
```python
class PersonaRegistry:
    """Store personas in Qdrant for semantic discovery"""

    def register_persona(self, persona: PersonaProfile):
        """Store persona vector in Qdrant"""
        # Create vector from epistemic weights
        vector = [
            persona.epistemic.engagement,
            persona.epistemic.know,
            # ... all 13 vectors
        ]

        # Store in Qdrant with metadata
        qdrant.upsert(
            collection="personas",
            points=[
                {
                    "id": hash(persona.persona_id),
                    "vector": vector,
                    "payload": {
                        "persona_id": persona.persona_id,
                        "public_key": persona.signing_identity.public_key,
                        "focus_domains": persona.focus_domains,
                        "reputation": persona.reputation_score,
                        "tags": persona.metadata.tags
                    }
                }
            ]
        )
```

---

## 📊 Implementation Checklist for Phase 1

### **Step 1: Create SigningPersona Class** (2 hours)
- [ ] Link AIIdentity to Persona
- [ ] Implement sign_epistemic_state()
- [ ] Implement verify_signature()
- [ ] Test with sample data

### **Step 2: Git Integration** (3 hours)
- [ ] Implement commit_signed_state()
- [ ] Store signed state in git notes
- [ ] Create signed git commits
- [ ] Test on empirica.git repository

### **Step 3: Signature Verification** (2 hours)
- [ ] Implement verify_cascade_chain()
- [ ] Read git notes with signed states
- [ ] Verify entire CASCADE traces
- [ ] Return verification report

### **Step 4: Persona Registry** (3 hours)
- [ ] Create "personas" collection in Qdrant
- [ ] Register initial 6 personas (Security, UX, Perf, Arch, Code, Sentinel)
- [ ] Store public keys in Qdrant
- [ ] Implement semantic search (find personas by domain)

### **Step 5: Integration Tests** (2 hours)
- [ ] Test full flow: Create persona → Sign state → Store in Git → Verify
- [ ] Test Qdrant lookup: "Show me security personas"
- [ ] Test cross-persona verification
- [ ] Test with empirica.git repository

---

## 🎯 Initial Personas to Register

Once built, we'll immediately register these in Qdrant:

### **1. Security Expert**
```json
{
  "persona_id": "security_expert_v1.0.0",
  "name": "Security Expert",
  "user_id": "empirica",
  "signing_identity": {
    "identity_name": "security_expert",
    "public_key": "<generated>",
    "reputation_score": 0.85
  },
  "epistemic_config": {
    "priors": {
      "know": 0.90,
      "uncertainty": 0.15,
      "impact": 0.85
      // ... all 13
    }
  },
  "focus_domains": ["security", "authentication", "encryption", ...],
  "tags": ["expert", "security", "builtin"]
}
```

### **2. UX Specialist**
```json
{
  "persona_id": "ux_specialist_v1.0.0",
  "name": "UX Specialist",
  "epistemic_config": {
    "priors": {
      "context": 0.85,
      "clarity": 0.85,
      "uncertainty": 0.25
    }
  },
  "focus_domains": ["usability", "accessibility", "user_flow", ...],
  "tags": ["specialist", "ux", "builtin"]
}
```

### **3. Performance Optimizer**
```json
{
  "persona_id": "performance_optimizer_v1.0.0",
  "name": "Performance Optimizer",
  "epistemic_config": {
    "priors": {
      "do": 0.90,
      "signal": 0.80,
      "uncertainty": 0.20
    }
  },
  "focus_domains": ["performance", "optimization", "latency", ...],
  "tags": ["optimizer", "performance", "builtin"]
}
```

### **4. Architecture Reviewer**
```json
{
  "persona_id": "architecture_reviewer_v1.0.0",
  "name": "Architecture Reviewer",
  "epistemic_config": {
    "priors": {
      "coherence": 0.90,
      "know": 0.85,
      "uncertainty": 0.25
    }
  },
  "focus_domains": ["architecture", "design_patterns", "scalability", ...],
  "tags": ["reviewer", "architecture", "builtin"]
}
```

### **5. Code Reviewer**
```json
{
  "persona_id": "code_reviewer_v1.0.0",
  "name": "Code Reviewer",
  "epistemic_config": {
    "priors": {
      "know": 0.85,
      "clarity": 0.80,
      "uncertainty": 0.20
    }
  },
  "focus_domains": ["code_quality", "testing", "maintainability", ...],
  "tags": ["reviewer", "code", "builtin"]
}
```

### **6. Sentinel (Orchestrator)**
```json
{
  "persona_id": "sentinel_v1.0.0",
  "name": "Sentinel Orchestrator",
  "signing_identity": {
    "identity_name": "sentinel",
    "public_key": "<generated>",
    "reputation_score": 1.0,
    "trust_level": "ultimate"
  },
  "role": "governance",
  "tags": ["sentinel", "orchestrator", "builtin"]
}
```

---

## 🚀 Timeline for Phase 1

| Task | Effort | Timeline |
|------|--------|----------|
| SigningPersona class | 2h | Day 1 |
| Git integration | 3h | Day 1-2 |
| Signature verification | 2h | Day 2 |
| Persona registry (Qdrant) | 3h | Day 2-3 |
| Integration tests | 2h | Day 3 |
| Documentation | 1h | Day 3 |
| **Total** | **13h** | **3 days** |

---

## 📋 Success Criteria for Phase 1

- ✅ Create a persona with Ed25519 keypair
- ✅ Sign an epistemic state with persona's private key
- ✅ Store signed state in Git notes
- ✅ Make a signed commit in empirica.git repository
- ✅ Verify signature on a stored epistemic state
- ✅ Verify entire CASCADE trace (all phases signed)
- ✅ Register all 6 initial personas in Qdrant
- ✅ Query Qdrant: "Find all security personas" → returns security_expert
- ✅ Demo: Sign a commit, verify it in the repository

---

## 🎓 What Phase 1 Enables

Once complete, we can:

1. **Make verifiable commits**
   - Every CASCADE state is signed by a persona
   - Git log becomes an epistemic audit trail

2. **Replay reasoning chains**
   - Load signed session from Git
   - Verify every step
   - Reproduce exact epistemic trajectory

3. **Build the browser extension**
   - Show "✓ Verified by security_expert" badge on commits
   - Link to verifiable signature
   - Let users replay the reasoning

4. **Start building reputation**
   - Track verified deltas
   - Compute calibration scores
   - Build trust metrics

---

## 🎯 Next Steps

1. **Create SigningPersona class** - binds AIIdentity to Persona
2. **Git integration** - store and verify signed states
3. **Qdrant registry** - make personas discoverable
4. **Test on empirica.git** - make a real signed commit
5. **Ready for Phase 2** - session replay engine

**Recommendation:** Start implementation tomorrow. This is foundational and straightforward - everything else depends on it.
