# Validation Fix Summary

## Problem Identified

You encountered these validation errors when calling MCP tools:
- `'optimal' is not of type 'integer'` (for bootstrap_level)
- `'project_wide' is not of type 'object'` (for scope)

## Root Cause Analysis

The validation was happening at the **local MCP server level** (not cloud):
- Location: `mcp.server.lowlevel.server.py:496` in the MCP Python SDK
- Mechanism: `jsonschema.validate(instance=arguments, schema=tool.inputSchema)`
- Trigger: `@app.call_tool()` defaults to `validate_input=True`

This was **heuristic-based validation** disguised as "schema enforcement" - exactly what CASCADE aims to avoid.

## Solution Applied

### 1. Disabled Rigid Schema Validation
```python
@app.call_tool(validate_input=False)  # CASCADE = guidance, not enforcement
```

### 2. Added Flexible bootstrap_level Parsing
Now accepts both strings and integers:
```python
bootstrap_level = "optimal"  # ✅ Maps to 2
bootstrap_level = 2          # ✅ Also works
bootstrap_level = "minimal"  # ✅ Maps to 0
```

### 3. Kept Scope Vectorial (No Semantic Presets)
Scope remains **self-assessed vectors only** (no heuristic shortcuts):
```python
# ✅ Correct: AI self-assesses based on epistemic state
scope = {
    "breadth": 0.7,      # 0-1: codebase span
    "duration": 0.6,     # 0-1: time commitment
    "coordination": 0.4  # 0-1: multi-agent coordination
}

# ❌ Rejected: Semantic names would be heuristics
scope = "project_wide"  # Falls back to defaults + warning
```

## Key Insight: Scope is Vectorial, Not Semantic

Initially, I tried to add semantic presets like:
- `"project_wide"` → `{breadth: 0.9, duration: 0.8, coordination: 0.7}`
- `"session_scoped"` → `{breadth: 0.5, duration: 0.4, coordination: 0.3}`

**You correctly stopped me** - this would be adding heuristics back in! 

Scope MUST be self-assessed by the AI based on:
1. Current epistemic state (know, clarity, confidence, etc.)
2. Guidance from `empirica/config/mco/goal_scopes.yaml`
3. Actual task requirements

## CASCADE Philosophy Reinforced

> **CASCADE is a cockpit, not a straitjacket.**

**Before:**
- Rigid schemas block AI with validation errors
- Parameters must match exact formats
- Investigation phase triggered by keywords

**After:**
- Schemas provide guidance, not enforcement
- AI self-assesses what makes sense
- Investigation phase is implicit based on epistemic state
- Trust AI reasoning over rigid rules

## Files Modified

1. **mcp_local/empirica_mcp_server.py**
   - Added `validate_input=False` to `@app.call_tool()` decorator
   - Added flexible bootstrap_level parsing (strings → integers)
   - Added scope validation warning (rejects semantic strings)
   - Added logging setup
   - Updated header documentation

2. **MCP_FLEXIBLE_VALIDATION_FIX.md**
   - Comprehensive documentation of the fix
   - Scope self-assessment guidance
   - Examples of correct usage

## Testing

```bash
# Bootstrap: flexible
bootstrap_session(ai_id="agent", bootstrap_level="optimal")  # ✅
bootstrap_session(ai_id="agent", bootstrap_level=2)          # ✅

# Scope: vectorial only
create_goal(..., scope={"breadth": 0.7, "duration": 0.6, "coordination": 0.4})  # ✅
create_goal(..., scope="project_wide")  # ❌ Warning + defaults
```

## Impact

✅ No more validation errors for intuitive parameters  
✅ Backward compatible with structured formats  
✅ Aligns with CASCADE philosophy (guidance > enforcement)  
✅ AI agents self-assess scope based on epistemic state  
✅ Removed temptation to add semantic heuristics  

## Next Steps

The MCP server now trusts AI self-assessment. AI agents should:

1. **Assess epistemic state** (13 vectors via PREFLIGHT)
2. **Consult guidance** (`goal_scopes.yaml` for scope mapping)
3. **Self-assess parameters** (bootstrap_level, scope vectors, complexity)
4. **Proceed with confidence** (no rigid validation blocking them)

---

**Date:** 2025-01-XX  
**Participants:** Rovo Dev + User  
**Outcome:** Validation is now guidance, not enforcement ✅
