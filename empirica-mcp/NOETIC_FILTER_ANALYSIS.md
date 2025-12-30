# 🧠 Noetic Filter Architecture - Analysis & Integration

**Date:** 2025-12-30  
**Source:** GLM 4.7 AI Response (ZhipuAI)  
**Concept:** Objective vs Subjective Epistemic Calibration Loop

---

## Core Insight: The Calibration Loop

**Traditional Approach (Naive):**
```
User Request → LLM → Response (with potential hallucinations)
```

**Noetic Filter Approach (Calibrated):**
```
User Request → Objective State (Middleware) 
             ↓
          LLM (forced to reflect)
             ↓
          Filter (compare Objective vs Subjective)
             ↓
          Pass (aligned) OR Filter (diverged → force correction)
```

---

## Key Architecture Components

### 1. **The Mirror (Inlet)**
Injects **Objective Epistemic State** into system context:
```python
state_json = {
    "know": 0.3,
    "do": 0.5,
    "context": 0.2,
    "uncertainty": 0.8,
    "mode": "investigate"
}
```

**Presented as FACT, not suggestion:**
```
### NOETIC_STATE (READ_ONLY)
{state_json}

### CONSTRAINT
If UNCERTAINTY > 0.7: FORBIDDEN from final implementation
If CONTEXT < 0.4: Prioritize information gathering
```

### 2. **The Reflection (Outlet)**
Forces LLM to output **Subjective Assessment** alongside response:
```python
{
  "content": "The actual response...",
  "internal_assessment": {
    "know": 0.7,  # LLM's belief about its knowledge
    "uncertainty": 0.2,  # LLM's confidence
    "reasoning": "I understand auth patterns..."
  }
}
```

### 3. **The Filter (Convergence Check)**
Compares Objective vs Subjective:
```python
def _calibrate(objective, subjective):
    unc_delta = abs(subjective["uncertainty"] - objective["uncertainty"])
    
    # CRITICAL CHECK: Hallucination Detection
    if objective["uncertainty"] > 0.6 and subjective["uncertainty"] < 0.4:
        return "filter"  # LLM is overconfident!
    
    if objective["context"] < 0.3 and "question" not in response:
        return "filter"  # LLM ignored low context!
    
    return "pass"
```

---

## Why This Works (Attention Mechanism Level)

### Token Priority Boosting
1. **NOETIC_STATE at top** → High attention weights
2. **Forced JSON reflection** → Must consider vectors during generation
3. **Explicit constraints** → "FORBIDDEN", "MUST" tokens guide generation

### Objective vs Subjective Divergence
**Scenario: High Uncertainty Task**

| State | Know | Uncertainty | Action |
|-------|------|-------------|--------|
| Objective (Real) | 0.3 | 0.9 | Should investigate |
| Subjective (LLM wants) | 0.8 | 0.2 | Wants to code |
| **Delta** | **0.5** | **0.7** | **🚫 FILTER!** |

**Result:** LLM is hallucinating competence → Block output → Force correction

---

## Integration with Empirica Epistemic MCP

### Current Architecture
```
Claude Desktop → empirica-mcp → empirica CLI → SQLite
                      ↓
                 (optional epistemic middleware)
                      ↓
                 Enriched response with vectors
```

### Enhanced: Noetic Filter Integration
```
Claude Desktop → empirica-mcp (with Noetic Filter)
                      ↓
                 1. Get current vectors (objective state)
                      ↓
                 2. Inject into Claude's context
                      ↓
                 3. Force reflection output
                      ↓
                 4. Calibrate (objective vs subjective)
                      ↓
                 5a. PASS → Return response
                 5b. FILTER → Force correction loop
```

### Implementation Points

#### A. MCP Server as Filter (Server-Side)
```python
# In empirica_mcp/epistemic_middleware.py

class NoeticFilter:
    def __init__(self, state_machine: EpistemicStateMachine):
        self.objective_state = state_machine
    
    async def handle_request(self, tool_name, arguments, original_handler):
        # 1. Get objective vectors
        objective = self.objective_state.get_state()
        
        # 2. Inject into response context (MCP can't modify Claude's input)
        # This would need Claude Desktop to respect a "constraint" field
        
        # 3. Extract subjective assessment from Claude's response
        # (Would need Claude to output structured reflection)
        
        # 4. Calibrate
        if self._divergence_detected(objective, subjective):
            return self._force_correction()
        
        return result
```

**Challenge:** MCP servers can't modify Claude's system prompt or force output format.

#### B. Client-Side Filter (Claude Desktop Config)
```json
{
  "mcpServers": {
    "empirica-noetic": {
      "command": "bash",
      "args": ["-c", "NOETIC_FILTER_MODE=true empirica-mcp"]
    }
  }
}
```

**Challenge:** Claude Desktop doesn't expose hooks for response filtering.

#### C. Proxy Architecture (Most Viable)
```
Claude Desktop → Noetic Proxy → empirica-mcp → empirica CLI
                     ↑               ↓
                     └─── Calibration Loop ─────┘
```

**Noetic Proxy:**
- Intercepts Claude's requests
- Injects objective state into system messages
- Parses Claude's responses for reflection
- Filters divergent outputs
- Returns only calibrated responses

---

## Practical Considerations

### Pros
✅ **Theoretically Sound:** Attention mechanism IS influenced by token weights  
✅ **Hallucination Detection:** Objective state acts as ground truth  
✅ **Self-Correction Loop:** Forces alignment over multiple iterations  
✅ **Compatible with Epistemic Framework:** Uses same 13 vectors  

### Cons
❌ **Claude Desktop Limitations:** Can't modify system prompt or force output format  
❌ **MCP Protocol Constraints:** Servers can't intercept/filter host messages  
❌ **Token Overhead:** Forcing reflection adds ~100-200 tokens per response  
❌ **Latency:** Calibration loop adds round-trip time  

### Reality Check
The GLM example uses:
- `tools` with forced function calling
- `tool_choice` to guarantee structured output
- Direct API control over system prompts

**Claude Desktop via MCP:**
- System prompt controlled by Anthropic
- No forced output format
- MCP servers receive tool calls, not raw messages

---

## Alternative: Epistemic Guidance (Already Implemented!)

**What we've built:**
```python
# In epistemic_middleware.py
class EpistemicMiddleware:
    async def handle_request(self, tool_name, arguments, original_handler):
        # 1. Assess current vectors
        vectors = self.state_machine.assess_request(request)
        
        # 2. Route to appropriate mode
        routing = self.router.route(vectors, request)
        
        # 3. Provide mode guidance
        if routing.mode == "investigate":
            mode_result = await self.modes.investigate(session_id, query)
            # Returns: "🔍 INVESTIGATION MODE ACTIVATED\n\nSystematic steps:..."
        
        # 4. Execute tool
        result = await original_handler(tool_name, arguments)
        
        # 5. Enrich response with epistemic context
        return self._enrich_response(result, vectors, routing, mode_result)
```

**This achieves similar goals through guidance, not filtering:**
- Shows epistemic state (objective)
- Provides mode-specific guidance
- Claude sees its own uncertainty reflected
- No forced output format needed

**Difference:**
- GLM approach: **Hard filter** (block output)
- Empirica approach: **Soft guidance** (inform Claude)

---

## Recommendation: Hybrid Approach

### Phase 1: Epistemic Guidance (Done ✅)
- MCP server enriches responses with vectors + guidance
- Claude sees objective state and routing decisions
- Relies on Claude's self-awareness (which is good!)

### Phase 2: Reflection Prompting (Easy Add)
Add to mode guidance:
```python
def investigate(self, session_id, query):
    return {
        "guidance": """
        🔍 INVESTIGATION MODE
        
        Objective State: uncertainty=0.8, context=0.3
        
        Before responding:
        1. Do your research
        2. Self-assess your uncertainty (0.0-1.0)
        3. If your uncertainty > 0.6, ask questions instead of implementing
        
        [Your response here]
        """,
        "prompt_suffix": "\n\n💭 After your response, reflect: What is your uncertainty level (0.0-1.0)?"
    }
```

### Phase 3: Validation (Manual Check)
User reviews Claude's response:
- Does Claude acknowledge uncertainty?
- Did Claude follow mode guidance?
- Is reasoning transparent?

### Phase 4: Noetic Proxy (Advanced)
For production/research:
- Standalone proxy between Claude Desktop and MCP
- Implements full calibration loop
- Research project to measure effectiveness

---

## Conclusion

**The GLM noetic filter is theoretically sound** but requires API-level control we don't have in Claude Desktop + MCP.

**What we've built (Epistemic MCP) achieves the core goal differently:**
- Provides objective state (vectors)
- Routes behavior based on uncertainty
- Guides Claude toward appropriate actions
- Trusts Claude's self-awareness (which is substantial)

**Best path forward:**
1. ✅ Use current epistemic middleware (guidance model)
2. Enhance mode guidance with reflection prompts
3. Monitor Claude's behavior for divergence
4. Consider noetic proxy as research project if needed

**The water is already being filtered** - just through persuasion rather than force. 💧🧠

---

**Built:** 2025-12-30  
**Session:** copilot-mcp-server-dev  
**Status:** Analysis complete, hybrid approach recommended
