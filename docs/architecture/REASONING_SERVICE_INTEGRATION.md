# Reasoning Service Integration Architecture

**Goal:** Connect Empirica to local reasoning models on empirica-server  
**Challenge:** How should services communicate?  
**Decision:** Multiple integration patterns for flexibility

---

## Communication Options

### Option 1: Direct HTTP API (Ollama)
**Pattern:** Direct API calls to Ollama endpoint

```python
import requests

response = requests.post(
    "http://empirica-server:11434/api/generate",
    json={
        "model": "phi4",
        "prompt": "...",
        "stream": False,
        "format": "json"
    }
)
```

**Pros:**
- ✅ Simple, direct
- ✅ Low latency
- ✅ No intermediate services

**Cons:**
- ⚠️ Tight coupling to Ollama
- ⚠️ No abstraction for other model types

---

### Option 2: Action Hook (Event-Driven)
**Pattern:** Triggered by project-bootstrap events

```python
# In project-bootstrap
def bootstrap_project_breadcrumbs(..., use_reasoning=False):
    breadcrumbs = {...}
    
    if use_reasoning:
        # Trigger reasoning action hook
        from empirica.integration.empirica_action_hooks import trigger_reasoning_analysis
        
        reasoning_results = trigger_reasoning_analysis(
            event="integrity_check",
            payload={
                "candidates": integrity_candidates,
                "model": "phi4"
            }
        )
        
        breadcrumbs["reasoning_analysis"] = reasoning_results
    
    return breadcrumbs
```

**Pros:**
- ✅ Loosely coupled
- ✅ Extensible (other events can trigger reasoning)
- ✅ Fits existing Empirica patterns

**Cons:**
- ⚠️ More complex
- ⚠️ Adds indirection

---

### Option 3: MCP Tool Integration
**Pattern:** Reasoning as MCP tool

```python
# MCP tool: analyze_with_reasoning
def handle_analyze_with_reasoning(args):
    """
    MCP tool for AI-powered analysis
    
    Args:
        task: "deprecation" | "alignment" | "gap"
        feature: Feature name
        context: Dict of evidence
        model: Model name (default: phi4)
    
    Returns:
        Structured judgment with reasoning
    """
    reasoning_service = LocalReasoningModel(args.model)
    return reasoning_service.analyze(args.task, args.feature, args.context)
```

**Pros:**
- ✅ AI-to-AI communication
- ✅ Works in MCP workflows
- ✅ Discoverable via MCP

**Cons:**
- ⚠️ Only accessible via MCP
- ⚠️ Not available in direct Python usage

---

### Option 4: Hybrid (Recommended)
**Pattern:** Reasoning service with multiple interfaces

```
┌─────────────────────────────────────────────────┐
│         Reasoning Service (Core)                │
│  - LocalReasoningModel (Ollama client)          │
│  - Prompt templates                             │
│  - Result parsing                               │
└─────────────────────────────────────────────────┘
         ↑          ↑            ↑
         │          │            │
    ┌────┴───┐  ┌───┴────┐  ┌───┴────┐
    │ Python │  │  MCP   │  │ Action │
    │  API   │  │  Tool  │  │  Hook  │
    └────────┘  └────────┘  └────────┘
```

**Usage patterns:**

```python
# 1. Direct Python API
from empirica.reasoning import LocalReasoningModel

reasoning = LocalReasoningModel("phi4", endpoint="http://empirica-server:11434")
judgment = reasoning.analyze_deprecation(feature, context)

# 2. Via project-bootstrap (action hook)
breadcrumbs = db.bootstrap_project_breadcrumbs(
    project_id,
    check_integrity=True,
    use_reasoning=True,
    reasoning_model="phi4"
)

# 3. Via MCP tool (for AI agents)
result = mcp_client.call_tool(
    "analyze_with_reasoning",
    task="deprecation",
    feature="reflexes",
    context={...}
)
```

---

## Recommended Architecture

### Layer 1: Core Service (Model Agnostic)

```python
# empirica/reasoning/service.py
class ReasoningService(ABC):
    """Abstract interface for reasoning services"""
    
    @abstractmethod
    def analyze_deprecation(self, feature: str, context: Dict) -> DeprecationJudgment:
        pass
    
    @abstractmethod
    def analyze_relationship(self, doc: str, code: str) -> RelationshipAnalysis:
        pass
```

### Layer 2: Ollama Adapter

```python
# empirica/reasoning/ollama_adapter.py
class OllamaReasoningModel(ReasoningService):
    """Adapter for Ollama-hosted models"""
    
    def __init__(
        self,
        model_name: str = "phi4",
        endpoint: str = "http://empirica-server:11434",
        timeout: int = 30
    ):
        self.model_name = model_name
        self.endpoint = endpoint
        self.timeout = timeout
    
    def _call_ollama(self, prompt: str, format: str = "json") -> Dict:
        """Low-level Ollama API call"""
        response = requests.post(
            f"{self.endpoint}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "format": format,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 2048
                }
            },
            timeout=self.timeout
        )
        return response.json()
    
    def analyze_deprecation(self, feature: str, context: Dict) -> DeprecationJudgment:
        """Analyze if feature is deprecated"""
        prompt = self._build_deprecation_prompt(feature, context)
        response = self._call_ollama(prompt, format="json")
        return self._parse_deprecation_response(response)
```

### Layer 3: Integration Points

**A. Direct Python Usage**
```python
# From any Python code
from empirica.reasoning import OllamaReasoningModel

reasoning = OllamaReasoningModel("phi4")
judgment = reasoning.analyze_deprecation("reflexes", context)
```

**B. Project-Bootstrap Hook**
```python
# In session_database.py
def bootstrap_project_breadcrumbs(..., use_reasoning=False, reasoning_model="phi4"):
    if use_reasoning:
        from empirica.reasoning import OllamaReasoningModel
        
        reasoning = OllamaReasoningModel(reasoning_model)
        # ... analyze candidates
```

**C. MCP Tool**
```python
# In empirica_mcp_server.py
async def handle_analyze_with_reasoning(args):
    from empirica.reasoning import OllamaReasoningModel
    
    reasoning = OllamaReasoningModel(args.model)
    return reasoning.analyze_deprecation(args.feature, args.context)
```

---

## Server Configuration

### Ollama Endpoint
- **URL:** `http://empirica-server:11434`
- **Protocol:** HTTP REST API
- **Format:** JSON
- **Timeout:** 30s (adjustable)

### Available Models
- `phi4` (14B) - Strong reasoning
- `qwen2.5:7b` - Fast, good JSON
- `qwen2.5:14b` - More powerful
- Others as deployed

### Network Requirements
- Empirica → empirica-server:11434 (HTTP)
- No authentication (internal network)
- Latency: < 100ms typically

---

## Implementation Priority

**Phase 1: Core + Ollama Adapter** (Now)
- ReasoningService interface
- OllamaReasoningModel implementation
- Prompt templates
- Test with phi4

**Phase 2: Project-Bootstrap Integration** (Next)
- Add use_reasoning flag
- Integrate with integrity analysis
- CLI support

**Phase 3: MCP Tool** (Later)
- Expose as MCP tool
- AI-to-AI reasoning
- Workflow integration

---

## Error Handling

```python
class ReasoningError(Exception):
    """Base class for reasoning errors"""
    pass

class ModelNotAvailableError(ReasoningError):
    """Model not found on server"""
    pass

class ReasoningTimeoutError(ReasoningError):
    """Model took too long to respond"""
    pass

class InvalidResponseError(ReasoningError):
    """Model returned invalid/unparseable response"""
    pass

# Graceful degradation
try:
    judgment = reasoning.analyze_deprecation(feature, context)
except ReasoningError as e:
    logger.warning(f"Reasoning failed: {e}, falling back to heuristic")
    judgment = heuristic_analysis(feature, context)
```

---

## Configuration

```python
# empirica/config/reasoning_config.yaml
reasoning:
  default_model: "phi4"
  endpoint: "http://empirica-server:11434"
  timeout: 30
  retry_attempts: 2
  fallback_to_heuristic: true
  
  models:
    phi4:
      temperature: 0.1
      top_p: 0.9
      max_tokens: 2048
    
    qwen2.5:
      temperature: 0.2
      top_p: 0.95
      max_tokens: 1024
```

---

## Testing Strategy

```python
# Test with mock server
def test_reasoning_service():
    # Mock Ollama response
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            "response": '{"status": "active", "confidence": 0.95}'
        }
        
        reasoning = OllamaReasoningModel("phi4")
        judgment = reasoning.analyze_deprecation("test", {})
        
        assert judgment.status == "active"
        assert judgment.confidence == 0.95
```

---

## Recommendation

**Start with Option 4 (Hybrid):**
1. Build core OllamaReasoningModel (generic, reusable)
2. Integrate with project-bootstrap (primary use case)
3. Add MCP tool later (bonus for AI workflows)

**This gives:**
- ✅ Direct Python access (for testing, scripts)
- ✅ Bootstrap integration (main product feature)
- ✅ Future extensibility (MCP, other models)

Ready to implement! 🚀

