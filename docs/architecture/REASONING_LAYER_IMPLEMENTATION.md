# Reasoning Layer Implementation Plan

**Product:** AI-Powered Doc-Code Intelligence Reasoning Assistant  
**Status:** Design Phase  
**Innovation:** Metacognitive noesis for code-doc relationships

---

## The Breakthrough

**Problem:** Heuristics can't understand context, meaning, or relationships  
**Solution:** Reasoning model that genuinely understands semantic connections

**Architecture:**
```
Project-Bootstrap (signals)
    ↓
Heuristic Detector (candidates) ← 129 found, many false positives
    ↓
Reasoning Layer (judgment) ← NEW! Understands context
    ↓
Structured Decisions (with explanations)
    ↓
Human Review (only uncertain cases)
```

---

## Implementation Components

### 1. Reasoning Service Interface

```python
class ReasoningService:
    """
    Abstract interface for reasoning models
    Supports: Local models, API models, custom implementations
    """
    
    def analyze_deprecation(
        self, 
        feature: str,
        context: Dict
    ) -> DeprecationJudgment:
        """
        Analyze if feature is actually deprecated
        
        Args:
            feature: Name of feature/command/function
            context: {
                'doc_mentions': [...],
                'code_implementation': str,
                'usage_history': [...],
                'git_history': {...},
                'related_features': [...]
            }
        
        Returns:
            DeprecationJudgment with confidence and reasoning
        """
        pass
    
    def analyze_relationship(
        self,
        doc_section: str,
        code_section: str
    ) -> RelationshipAnalysis:
        """
        Analyze if doc and code describe the same thing
        
        Returns semantic similarity and alignment analysis
        """
        pass
    
    def analyze_implementation_gap(
        self,
        documented_behavior: str,
        actual_implementation: str
    ) -> ImplementationGap:
        """
        Analyze if implementation matches documented behavior
        
        Returns gap analysis with severity and recommendations
        """
        pass
```

### 2. Local Model Adapter

```python
class LocalReasoningModel(ReasoningService):
    """
    Adapter for local reasoning models
    
    Supports:
    - Qwen2.5 (14B, 32B)
    - DeepSeek-R1 (7B, 14B)
    - Llama 3.3 (70B)
    - Custom fine-tuned models
    """
    
    def __init__(
        self,
        model_name: str,
        endpoint: str = "http://empirica-server:11434",
        temperature: float = 0.1  # Low for consistency
    ):
        self.model_name = model_name
        self.endpoint = endpoint
        self.temperature = temperature
    
    def _create_prompt(
        self,
        task: str,
        context: Dict
    ) -> str:
        """Create structured prompt for reasoning task"""
        pass
    
    def _parse_response(
        self,
        response: str,
        expected_format: str
    ) -> Dict:
        """Parse model response into structured format"""
        pass
```

### 3. Prompt Templates

```python
DEPRECATION_ANALYSIS_PROMPT = """
You are analyzing whether a software feature is genuinely deprecated.

Feature: {feature}

Context:
- Documentation mentions: {doc_mentions}
- Code implementation: {code_snippet}
- Usage in last 50 sessions: {usage_count} times
- Last git commit: {last_commit_date}
- Related features: {related_features}

Task: Determine if this feature is:
1. Currently deprecated (should be removed/marked)
2. Previously deprecated but now current (historical context only)
3. Still active and in use

Reasoning guidelines:
- "previously deprecated" = past tense, not current
- Check if code is actively maintained
- Check if usage patterns show active use
- Consider relationships to other features

Respond in JSON:
{{
    "status": "deprecated|historical|active",
    "confidence": 0.0-1.0,
    "reasoning": "step-by-step analysis",
    "evidence": ["key evidence points"],
    "recommendation": "specific action to take"
}}
"""

RELATIONSHIP_ANALYSIS_PROMPT = """
You are analyzing if documentation and code describe the same feature.

Documentation:
{doc_text}

Code:
{code_text}

Task: Determine the relationship:
1. Aligned: Doc accurately describes code
2. Partial: Doc describes some aspects, misses others
3. Drift: Doc describes different behavior than code
4. Unrelated: Doc and code are about different things

Consider:
- Semantic meaning (not just keywords)
- Intent vs implementation
- Evolution (doc might be outdated)

Respond in JSON:
{{
    "relationship": "aligned|partial|drift|unrelated",
    "confidence": 0.0-1.0,
    "reasoning": "detailed analysis",
    "gaps": ["what's missing or wrong"],
    "action": "what to update"
}}
"""

IMPLEMENTATION_GAP_PROMPT = """
You are analyzing if code implementation matches documented behavior.

Documented behavior:
{documented}

Actual implementation:
{implementation}

Task: Identify implementation gaps:
1. Missing features (doc says X, code doesn't do X)
2. Different behavior (doc says X, code does Y)
3. Extra features (code does X, doc doesn't mention)

Consider:
- Functional correctness
- Performance claims
- Edge cases handling

Respond in JSON:
{{
    "gap_type": "missing|different|extra|none",
    "severity": "critical|high|medium|low",
    "confidence": 0.0-1.0,
    "reasoning": "what differs and why",
    "impact": "user impact",
    "recommendation": "fix code or fix docs"
}}
"""
```

### 4. Batch Analysis Pipeline

```python
class ReasoningPipeline:
    """
    Batch processing pipeline for analyzing candidates
    
    Optimizations:
    - Batch similar queries
    - Cache results
    - Parallel processing
    - Progress tracking
    """
    
    def analyze_deprecation_candidates(
        self,
        candidates: List[Dict],
        reasoning_service: ReasoningService
    ) -> List[DeprecationJudgment]:
        """
        Process all deprecation candidates
        
        Returns judgments sorted by confidence
        """
        results = []
        
        for candidate in candidates:
            context = self._gather_context(candidate)
            judgment = reasoning_service.analyze_deprecation(
                candidate['feature'],
                context
            )
            results.append(judgment)
        
        return sorted(results, key=lambda x: x.confidence, reverse=True)
    
    def _gather_context(self, candidate: Dict) -> Dict:
        """
        Gather all relevant context for reasoning
        
        Sources:
        - Doc mentions with surrounding text
        - Code implementation
        - Artifacts usage history
        - Git commit history
        - Related features analysis
        """
        pass
```

### 5. Integration with Project-Bootstrap

```python
# Extended project-bootstrap with reasoning
def bootstrap_project_breadcrumbs(
    project_id: str,
    check_integrity: bool = False,
    use_reasoning: bool = False,  # NEW!
    reasoning_model: str = "qwen2.5-14b"  # NEW!
) -> Dict:
    """
    Bootstrap with optional AI reasoning layer
    
    When use_reasoning=True:
    - Runs heuristic detection
    - Sends candidates to reasoning model
    - Returns high-confidence judgments
    - Flags uncertain cases for human review
    """
    
    breadcrumbs = {...}
    
    if use_reasoning:
        # Initialize reasoning service
        reasoning = LocalReasoningModel(reasoning_model)
        
        # Analyze candidates
        pipeline = ReasoningPipeline()
        judgments = pipeline.analyze_deprecation_candidates(
            integrity_candidates,
            reasoning
        )
        
        # Add to breadcrumbs
        breadcrumbs["reasoning_analysis"] = {
            "model": reasoning_model,
            "high_confidence": [j for j in judgments if j.confidence > 0.8],
            "needs_review": [j for j in judgments if 0.6 <= j.confidence <= 0.8],
            "total_analyzed": len(judgments)
        }
    
    return breadcrumbs
```

---

## Data Structures

```python
@dataclass
class DeprecationJudgment:
    feature: str
    status: Literal["deprecated", "historical", "active"]
    confidence: float  # 0.0-1.0
    reasoning: str
    evidence: List[str]
    recommendation: str
    metadata: Dict

@dataclass
class RelationshipAnalysis:
    relationship: Literal["aligned", "partial", "drift", "unrelated"]
    confidence: float
    reasoning: str
    gaps: List[str]
    action: str

@dataclass
class ImplementationGap:
    gap_type: Literal["missing", "different", "extra", "none"]
    severity: Literal["critical", "high", "medium", "low"]
    confidence: float
    reasoning: str
    impact: str
    recommendation: str
```

---

## Model Requirements

**Ideal characteristics:**
- Fast inference (< 1s per judgment)
- Good reasoning capabilities
- JSON output reliability
- Context window: 4K-8K tokens
- Local deployment capable

**Candidate models:**
- **Qwen2.5-14B:** Strong reasoning, good JSON
- **DeepSeek-R1-7B:** Specialized for reasoning
- **Llama 3.3-70B:** Powerful but slower
- **Custom fine-tuned:** Trained on code-doc examples

---

## Performance Optimization

### Caching Strategy
```python
# Cache reasoning results
cache_key = hash(feature + context_summary)
if cache_key in reasoning_cache:
    return cached_result

# Batch processing
batch_size = 10
for batch in chunks(candidates, batch_size):
    results = reasoning_service.batch_analyze(batch)
```

### Parallel Processing
```python
# Use ThreadPoolExecutor for I/O-bound reasoning calls
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(reasoning_service.analyze, candidate)
        for candidate in candidates
    ]
    results = [future.result() for future in futures]
```

---

## Cost Analysis

**Per-analysis cost (local model):**
- Inference: Free (local)
- Time: 0.5-2s per analysis
- Total for 129 candidates: ~2-4 minutes

**Benefits:**
- 95%+ accuracy (vs 50% heuristic)
- Explanations for every decision
- No API costs
- Privacy (local processing)

---

## Testing Strategy

### Phase 1: Ground Truth Dataset
```python
# Create labeled examples
ground_truth = [
    {
        "feature": "reflexes",
        "context": {...},
        "expected_status": "active",
        "reason": "Core feature, actively used"
    },
    # ... 20-30 examples
]

# Measure accuracy
accuracy = evaluate_reasoning_service(
    reasoning_service,
    ground_truth
)
```

### Phase 2: Human Validation
```python
# Have human expert review 10% of judgments
# Calculate inter-rater agreement
# Refine prompts based on disagreements
```

---

## Rollout Plan

**Week 1: Implementation**
- Day 1-2: Reasoning service interface + local adapter
- Day 3-4: Prompt engineering + testing
- Day 5: Integration with project-bootstrap

**Week 2: Validation**
- Day 1-2: Create ground truth dataset
- Day 3-4: Run on 129 candidates
- Day 5: Human validation of results

**Week 3: Production**
- Day 1: Documentation
- Day 2: CLI commands
- Day 3-5: Apply recommendations, verify integrity

---

## Success Metrics

**Technical:**
- Accuracy > 95% (vs ground truth)
- Speed < 2s per analysis
- False positive rate < 5%

**Product:**
- Integrity score: 46% → 80%+
- Phantom commands: 66 → < 10
- User confidence in doc-code alignment

---

## Future Extensions

### Phase 2: Active Monitoring
```python
# Run reasoning analysis on every commit
# Detect doc-code drift in real-time
# Auto-generate PRs with recommendations
```

### Phase 3: Learning from Corrections
```python
# When human overrides judgment
# Store as training example
# Fine-tune model on corrections
# Continuous improvement
```

### Phase 4: Multi-Language Support
```python
# Extend to TypeScript, Go, Rust
# Cross-language doc-code analysis
# API documentation validation
```

---

## Product Positioning

**Name:** Empirica Reasoning Layer  
**Tagline:** "Any local AI becomes a doc-code intelligence expert"

**Value Prop:**
- Turn local LLMs into specialized reasoning assistants
- Understand context, not just patterns
- Explain every decision
- Privacy-preserving (local inference)

**Pricing (future):**
- Open source core
- Enterprise plugin for custom models
- SaaS option with hosted reasoning

---

**Status:** Ready for model selection and implementation  
**Next Step:** Choose reasoning model and implement adapter  
**ETA:** 1-2 weeks for full implementation

---

This is metacognitive infrastructure for AI systems. 🚀

