# Phase 1: Complete Foundation Inventory

**Date:** 2025-12-02
**Status:** Foundation 95% complete - Ready to implement Phase 1

---

## 🎯 The Complete Picture

### **Three-Layer Persona System**

```
Layer 1: MCO Persona Definitions (personas.yaml)
├─ 6 meta-agent personas with epistemic behavior patterns
├─ Researcher, Implementer, Reviewer, Coordinator, Learner, Expert
├─ Define investigation style, learning characteristics
└─ Abstract behavioral archetypes

Layer 2: Model Profiles (model_profiles.yaml)
├─ Model-specific bias corrections and capability assessments
├─ Claude Sonnet, Haiku, GPT-4, GPT-3.5, Code Specialist, Research Specialist
├─ How each model tends to err (calibration patterns)
└─ Threshold adjustments per model

Layer 3: Cryptographic Signing (NEW - Phase 1)
├─ AIIdentity: Ed25519 keypairs for each persona instance
├─ SigningPersona: Binds epistemic state to cryptographic identity
├─ Sign CASCADE phases with persona's private key
└─ Verify signatures with persona's public key
```

---

## ✅ Complete Inventory: What Exists

### **1. MCO Persona Definitions** (personas.yaml)
```yaml
6 pre-defined personas with epistemic priors:

RESEARCHER
├─ High uncertainty tolerance (0.75)
├─ Moderate baseline knowledge (0.60)
├─ Exploratory investigation style (10 rounds max)
└─ Emphasis on documentation and discovery sharing

IMPLEMENTER
├─ Moderate uncertainty tolerance (0.50)
├─ Strong execution capability (0.85)
├─ Task-focused investigation (5 rounds max)
└─ Emphasis on clear requirements

REVIEWER
├─ Low uncertainty tolerance (0.40)
├─ Strong domain knowledge (0.85)
├─ Thorough validation (8 rounds max)
└─ Emphasis on quality and completion

COORDINATOR
├─ Excellent context awareness (0.90)
├─ Strong state mapping (0.85)
├─ Workflow-driven investigation (6 rounds)
└─ Multi-agent orchestration focused

LEARNER
├─ High uncertainty tolerance (0.80)
├─ Limited baseline knowledge (0.40)
├─ Extensive investigation (12 rounds max)
└─ Requires frequent clarification

EXPERT
├─ Low uncertainty tolerance (0.45)
├─ Strong domain knowledge (0.90)
├─ Minimal investigation needed (4 rounds)
└─ Minimal guidance required
```

### **2. Model Profiles** (model_profiles.yaml)
```yaml
6 model profiles with bias corrections:

CLAUDE SONNET
├─ Capabilities: reasoning_depth=0.85, context=0.90, code=0.80
├─ Bias: slight overconfidence, underestimates uncertainty
├─ Calibration: know is overconfident, uncertainty underestimated
└─ Specializations: code, creative writing, safety-critical

CLAUDE HAIKU
├─ Capabilities: reasoning=0.60, context=0.75, code=0.65
├─ Bias: overconfidence, significant uncertainty underestimation
├─ Calibration: significantly underestimates uncertainty
└─ Specializations: fast iteration, efficiency

GPT-4
├─ Capabilities: reasoning=0.80, context=0.85, code=0.75
├─ Bias: overconfidence, uncertainty underestimation
├─ Calibration: slight overconfidence across vectors
└─ Specializations: reasoning, analysis

GPT-3.5
├─ Capabilities: reasoning=0.65, context=0.70, code=0.60
├─ Bias: significant overconfidence, strong speed bias
├─ Calibration: significantly underestimates uncertainty
└─ Specializations: fast, cost-effective

CODE_SPECIALIST
├─ Capabilities: code_generation=0.95, reasoning=0.70
├─ Bias: moderate overconfidence, conservative creativity
├─ Specializations: code analysis, debugging, architecture review

RESEARCH_SPECIALIST
├─ Capabilities: reasoning=0.90, context=0.95, code=0.50
├─ Bias: minimal overconfidence, may be too cautious
├─ Specializations: literature review, data analysis, hypothesis testing
```

### **3. AIIdentity System** (core/identity/ai_identity.py)
```python
✅ Ed25519 keypair generation
✅ Secure storage (.empirica/identity/, 0600 permissions)
✅ Public key export for distribution
✅ Signing capability (sign messages)
✅ Verification capability (verify signatures)
✅ JSON serialization for portability
```

### **4. PersonaManager** (core/persona/persona_manager.py)
```python
✅ Create personas from templates
✅ Load/save personas from disk
✅ Validate against schema
✅ Link to signing identities
✅ List all personas
```

### **5. Persona Schema** (core/persona/schemas/persona_schema.json)
```json
✅ 13 epistemic vector definitions
✅ Signing identity section with public_key field
✅ CASCADE thresholds per persona
✅ Capabilities and restrictions
✅ Sentinel configuration
✅ Reputation tracking
✅ Metadata (tags, parent_persona, verified_sessions)
```

### **6. Qdrant Vector Database**
```
✅ Running on port 6333
✅ One collection: mcm_reasoning_vectors
✅ Ready for persona vectors
✅ Supports semantic tagging and metadata
```

### **7. Dashboard API**
```
✅ Flask API on port 8000
✅ 12 endpoints for querying epistemic data
✅ CORS enabled
✅ Can serve verified commit data
```

### **8. Git Integration**
```
✅ Git state capture (Phase 2.5 complete)
✅ Can store in git notes
✅ Commit signing ready
✅ Test repository: forgejo/empirica.git
```

### **9. Forgejo Instance**
```
✅ Fresh v13.0.3 running
✅ http://aiworkhorse.local:3000/
✅ Plugin directory ready
✅ Test commit: b4610cb
```

---

## ⚡ What We Need to Build for Phase 1

### **The Missing Link: SigningPersona**

Current state:
- MCO Personas exist (abstract behavioral profiles)
- AIIdentity exists (keypairs)
- PersonaManager exists (create/load personas)
- Qdrant exists (can store vectors)

Missing connection:
```python
class SigningPersona:
    """Binds epistemic persona to cryptographic identity"""

    def __init__(self, persona_profile: PersonaProfile,
                 ai_identity: AIIdentity):
        self.persona = persona_profile  # The epistemic behavior
        self.identity = ai_identity      # The signing capability

    def sign_epistemic_state(self, state: Dict, phase: str) -> Dict:
        """Sign an epistemic state for a CASCADE phase"""
        canonical = {
            "persona_id": self.persona.persona_id,
            "phase": phase,
            "timestamp": datetime.now().isoformat(),
            "vectors": {
                "engagement": state.engagement,
                "know": state.know,
                "do": state.do,
                # ... all 13 vectors
            },
            "public_key": self.identity.public_key.hex()
        }

        message = json.dumps(canonical, sort_keys=True)
        signature = self.identity.sign(message)

        return {
            "state": canonical,
            "signature": signature,
            "algorithm": "Ed25519"
        }

    def verify_signature(self, signed_state: Dict) -> bool:
        """Verify a previously signed epistemic state"""
        message = json.dumps(signed_state["state"], sort_keys=True)
        return self.identity.verify(
            signed_state["signature"],
            message
        )
```

### **The Missing Piece: Signed Git Operations**

```python
class SignedGitOperations:
    """Store and verify signed epistemic states in Git"""

    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)

    def commit_signed_state(self, persona: SigningPersona,
                           epistemic_state: EpistemicState,
                           phase: str,
                           message: str) -> str:
        """
        Create a Git commit with signed epistemic state

        Flow:
        1. Sign the epistemic state with persona's key
        2. Store signed state in git notes
        3. Create signed commit with persona as author
        4. Return commit SHA
        """
        # Sign the state
        signed_state = persona.sign_epistemic_state(
            epistemic_state, phase
        )

        # Store in git notes
        self.repo.git.notes(
            'add',
            '-m', json.dumps(signed_state, indent=2)
        )

        # Create signed commit
        self.repo.git.commit(
            '--allow-empty',
            '--gpg-sign=' + persona.identity.gpg_key_id,
            '-m', f"{phase}: {message}"
        )

        return self.repo.head.commit.hexsha

    def verify_cascade_chain(self, start_commit: str,
                            end_commit: str) -> List[Dict]:
        """
        Verify entire CASCADE trace is signed

        Returns list of verification results:
        - commit SHA
        - phase
        - gpg_verified (true/false)
        - state_verified (true/false)
        - persona_id
        """
        commits = list(self.repo.iter_commits(
            f"{start_commit}..{end_commit}"
        ))

        results = []
        for commit in commits:
            # Verify GPG signature
            gpg_ok = verify_git_signature(commit)

            # Get git note
            note = self.repo.git.notes('show', commit.hexsha)
            signed_state = json.loads(note)

            # Verify epistemic state signature
            state_ok = verify_epistemic_signature(
                signed_state,
                persona_public_key
            )

            results.append({
                "commit": commit.hexsha,
                "phase": extract_phase(commit.message),
                "gpg_verified": gpg_ok,
                "state_verified": state_ok,
                "persona_id": signed_state["state"]["persona_id"],
                "timestamp": signed_state["state"]["timestamp"]
            })

        return results
```

### **The Missing Piece: Persona Registry in Qdrant**

```python
class PersonaRegistry:
    """Store and discover personas in Qdrant"""

    def __init__(self, qdrant_host: str = "localhost",
                 qdrant_port: int = 6333):
        from qdrant_client import QdrantClient
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.collection_name = "personas"

    def register_persona(self, persona: PersonaProfile,
                        signing_persona: SigningPersona):
        """
        Store persona in Qdrant with semantic indexing

        Vector = 13D epistemic vector
        Metadata = persona info, tags, public key, reputation
        """
        # Create vector from epistemic priors
        vector = [
            persona.epistemic_config.priors.engagement,
            persona.epistemic_config.priors.know,
            persona.epistemic_config.priors.do,
            persona.epistemic_config.priors.context,
            persona.epistemic_config.priors.clarity,
            persona.epistemic_config.priors.coherence,
            persona.epistemic_config.priors.signal,
            persona.epistemic_config.priors.density,
            persona.epistemic_config.priors.state,
            persona.epistemic_config.priors.change,
            persona.epistemic_config.priors.completion,
            persona.epistemic_config.priors.impact,
            persona.epistemic_config.priors.uncertainty,
        ]

        # Store in Qdrant
        point_id = hash(persona.persona_id) % (2**31)

        self.client.upsert(
            collection_name=self.collection_name,
            points=[{
                "id": point_id,
                "vector": vector,
                "payload": {
                    "persona_id": persona.persona_id,
                    "name": persona.name,
                    "public_key": signing_persona.identity.public_key.hex(),
                    "focus_domains": persona.epistemic_config.focus_domains,
                    "reputation_score": signing_persona.identity.reputation_score,
                    "tags": persona.metadata.tags,
                    "template": persona.metadata.derived_from,
                    "created_at": persona.metadata.created_at
                }
            }]
        )

    def find_personas_by_domain(self, domain: str,
                               limit: int = 5):
        """
        Semantic search: find personas focused on a domain

        Example: find_personas_by_domain("security")
        Returns: [security_expert_v1, security_auditor, ...]
        """
        # This would use Qdrant's search capability
        # along with metadata filtering for tags
        pass

    def get_persona_by_id(self, persona_id: str):
        """Get a specific persona by ID"""
        pass

    def list_all_personas(self):
        """List all registered personas"""
        pass
```

---

## 📊 Implementation Checklist

- [ ] **Step 1: SigningPersona Class** (2h)
  - [ ] Bind PersonaProfile to AIIdentity
  - [ ] Implement sign_epistemic_state()
  - [ ] Implement verify_signature()
  - [ ] Unit tests

- [ ] **Step 2: Git Integration** (3h)
  - [ ] Implement commit_signed_state()
  - [ ] Implement verify_cascade_chain()
  - [ ] Test on empirica.git repository
  - [ ] Integration tests

- [ ] **Step 3: Qdrant Registry** (3h)
  - [ ] Create "personas" collection
  - [ ] Register 6 initial personas
  - [ ] Implement semantic search
  - [ ] Integration tests

- [ ] **Step 4: End-to-End Test** (2h)
  - [ ] Create researcher persona
  - [ ] Sign epistemic state
  - [ ] Commit to git
  - [ ] Query Qdrant
  - [ ] Verify entire chain

---

## 🎯 Initial Personas to Register

We'll register these 6 personas immediately:

### **1. researcher** (from personas.yaml)
```json
{
  "persona_id": "researcher_v1.0.0",
  "name": "Research Explorer",
  "epistemic_config": {
    "priors": {
      "engagement": 0.80,
      "know": 0.60,
      "do": 0.70,
      // ... from personas.yaml
    }
  },
  "focus_domains": ["research", "exploration", "learning", "analysis"],
  "tags": ["researcher", "explorer", "builtin", "mco"]
}
```

### **2. implementer**
```json
{
  "persona_id": "implementer_v1.0.0",
  "name": "Task Implementer",
  "epistemic_config": {
    "priors": {
      "engagement": 0.85,
      "know": 0.75,
      "do": 0.85,
      // ... from personas.yaml
    }
  },
  "focus_domains": ["implementation", "execution", "coding"],
  "tags": ["implementer", "executor", "builtin", "mco"]
}
```

### **3. reviewer**
### **4. coordinator**
### **5. learner**
### **6. expert**

Plus model-specific personas like `code_specialist`, `research_specialist`

---

## 🚀 Timeline

| Task | Time | Day |
|------|------|-----|
| SigningPersona class | 2h | Day 1 |
| Git integration | 3h | Day 1-2 |
| Qdrant registry | 3h | Day 2 |
| End-to-end test | 2h | Day 3 |
| **Total** | **10h** | **3 days** |

---

## ✅ Success Criteria

After Phase 1, we can:

1. ✅ Create a persona instance with signing capability
2. ✅ Sign an epistemic state with persona's private key
3. ✅ Store signed state in Git notes
4. ✅ Make signed commits in empirica.git
5. ✅ Verify signature on retrieved epistemic state
6. ✅ Verify entire CASCADE trace
7. ✅ Register personas in Qdrant
8. ✅ Query Qdrant: "find security personas"
9. ✅ Cross-verify: persona public key matches Qdrant record

---

## 📋 Why This Matters

Once Phase 1 is complete:

- **Every epistemic claim is cryptographically signed**
- **Git log becomes an immutable epistemic audit trail**
- **Can replay CASCADE phases and verify outputs**
- **Personas have provable, verified identity**
- **Foundation for browser extension verification badges**
- **Foundation for cross-org epistemic handoffs**

---

**Recommendation:** Start implementation today. Everything is ready - just need to connect the pieces.
