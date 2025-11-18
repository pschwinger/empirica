# Session Aliases and Graceful Degradation - Implementation Spec

**Created:** November 18, 2025  
**Status:** Ready to start (new session recommended)  
**Estimated:** 120-165 min | 23,000 tokens  
**Priority:** High - improves UX and reliability

---

## Objective

Implement session aliases and graceful degradation improvements across all MCP tools to improve user experience and system reliability.

---

## Background

### Current State
- Some tools support session aliases (`latest:active:rovodev`)
- Some tools only accept explicit UUIDs
- Inconsistent behavior across 35+ tools
- No graceful degradation when git unavailable

### Desired State
- **All tools** support session aliases consistently
- Clear documentation in tool schemas
- Graceful fallback: git → SQLite → JSON
- Comprehensive test coverage

---

## Subtasks (5)

### 1. Add resolve_session_id to all 35 remaining MCP tools
**Estimated:** 60-90 min | 12,000 tokens

**Current Status:**
- Some tools already use `resolve_session_id()`
- 35 tools still need this added

**Implementation Pattern:**
```python
# Before (old pattern)
session_id = arguments.get("session_id")

# After (new pattern)
session_id_or_alias = arguments.get("session_id")
try:
    session_id = resolve_session_id(session_id_or_alias)
except ValueError as e:
    error_response = create_error_response(
        "invalid_alias",
        f"Session resolution failed: {str(e)}",
        {"provided": session_id_or_alias}
    )
    return [types.TextContent(type="text", text=json.dumps(error_response, indent=2))]
```

**Tools Needing Update:**
- All 35 tools that accept `session_id` parameter
- Check each tool's current implementation
- Apply resolve_session_id consistently
- Use structured error responses (already implemented!)

**Verification:**
- Test with explicit UUID
- Test with `latest` alias
- Test with `latest:active` alias
- Test with `latest:active:ai_id` alias

---

### 2. Update all 35 tool schemas to document session alias support
**Estimated:** 20-30 min | 4,000 tokens

**Current Issue:**
Tool schemas don't mention alias support, causing confusion.

**Solution:**
Update each tool's schema/docstring to document:
```python
session_id: Union[str, SessionAlias]
    Either explicit UUID or session alias.
    
    Supported aliases:
    - 'latest' - Most recent session
    - 'latest:active' - Most recent active session
    - 'latest:rovodev' - Most recent for specific AI
    - 'latest:active:rovodev' - Most recent active for AI (recommended)
    
    Examples:
    - "1493402f-792b-487c-b98b-51e31ebf00a1" (explicit UUID)
    - "latest:active:rovodev" (alias)
```

**Files to Update:**
- `mcp_local/empirica_mcp_server.py` - inline docstrings
- Any schema definition files
- User-facing documentation

---

### 3. Create integration tests for session alias support
**Estimated:** 20-30 min | 4,000 tokens

**Test File:** `tests/integration/test_session_aliases.py`

**Test Coverage:**
```python
class TestSessionAliases:
    def test_explicit_uuid_works(self):
        """Test tools work with explicit session UUID"""
        
    def test_latest_alias(self):
        """Test 'latest' alias resolves correctly"""
        
    def test_latest_active_alias(self):
        """Test 'latest:active' alias resolves correctly"""
        
    def test_latest_ai_id_alias(self):
        """Test 'latest:active:ai_id' alias resolves correctly"""
        
    def test_invalid_alias_returns_error(self):
        """Test invalid alias returns structured error"""
        
    def test_nonexistent_session_returns_error(self):
        """Test non-existent session returns structured error"""
        
    def test_alias_consistency_across_tools(self):
        """Test same alias resolves to same session across different tools"""
```

**Approach:**
1. Create test session with known ID
2. Test resolution with each alias type
3. Verify consistency across multiple tools
4. Test error cases

---

### 4. Implement graceful degradation fallback hierarchy
**Estimated:** 15-25 min | 2,000 tokens

**Current Issue:**
If git unavailable, some operations fail completely.

**Solution:**
Implement fallback hierarchy:
1. **Git (preferred)** - Full functionality with git notes
2. **SQLite (fallback 1)** - Core functionality from database
3. **JSON (fallback 2)** - Minimal functionality from reflex logs

**Implementation Areas:**

#### Checkpoint Operations
```python
# Try git first
try:
    from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
    git_logger = GitEnhancedReflexLogger(session_id=session_id)
    checkpoint = git_logger.get_last_checkpoint()
except (ImportError, GitNotAvailableError):
    # Fallback to SQLite
    checkpoint = db.get_last_checkpoint_from_db(session_id)
    if not checkpoint:
        # Fallback to JSON
        checkpoint = json_handler.get_last_checkpoint_from_reflex(session_id)
```

#### Session State
```python
# Graceful degradation for get_epistemic_state
try:
    # Full state from git
    state = git_logger.get_full_state()
except:
    # Partial state from database
    state = db.get_session_state(session_id)
    state["warning"] = "Limited state - git unavailable"
```

**Operations Needing Fallback:**
- `load_git_checkpoint`
- `create_git_checkpoint`
- `get_vector_diff`
- Any git-dependent operations

---

### 5. Test all fallback modes
**Estimated:** 5-10 min | 1,000 tokens

**Test File:** `tests/integration/test_graceful_degradation.py`

**Test Coverage:**
```python
class TestGracefulDegradation:
    def test_git_mode_preferred(self):
        """Test git operations work when available"""
        
    def test_sqlite_fallback_when_git_unavailable(self):
        """Test SQLite fallback activates when git unavailable"""
        
    def test_json_fallback_as_last_resort(self):
        """Test JSON fallback works when git and SQLite fail"""
        
    def test_fallback_warning_messages(self):
        """Test users are informed about degraded mode"""
        
    def test_operations_still_work_in_degraded_mode(self):
        """Test core operations continue to function"""
```

**Testing Approach:**
1. Mock git unavailability
2. Verify SQLite fallback activates
3. Mock SQLite failure
4. Verify JSON fallback activates
5. Ensure warnings are clear

---

## Implementation Order

**Recommended sequence:**
1. Subtask 1: Add resolve_session_id (bulk of work)
2. Subtask 2: Update schemas (documentation)
3. Subtask 3: Create alias tests (validation)
4. Subtask 4: Implement fallback hierarchy (reliability)
5. Subtask 5: Test fallbacks (verification)

**Rationale:** Complete alias support first (most impactful), then add resilience.

---

## Success Criteria

### Functionality
- ✅ All 35+ tools support session aliases
- ✅ Consistent resolution across all tools
- ✅ Graceful degradation when git unavailable
- ✅ Clear warnings in degraded mode

### Documentation
- ✅ All tool schemas document alias support
- ✅ Examples provided for each alias type
- ✅ User guide updated

### Testing
- ✅ Integration tests for alias resolution
- ✅ Tests for all fallback modes
- ✅ Error case coverage

### User Experience
- ✅ Users can use aliases anywhere
- ✅ Operations continue in degraded mode
- ✅ Clear error messages for invalid aliases

---

## Files to Modify

### Primary
- `mcp_local/empirica_mcp_server.py` - Add resolve_session_id to 35 tools

### Tests (New)
- `tests/integration/test_session_aliases.py`
- `tests/integration/test_graceful_degradation.py`

### Documentation
- Tool schemas/docstrings in MCP server
- User guides (if needed)

---

## Dependencies

### Existing Infrastructure
- ✅ `resolve_session_id()` function already exists
- ✅ `create_error_response()` already exists (81% coverage!)
- ✅ Session database schema supports aliases
- ✅ Pattern established in some tools

### New Requirements
- None! All infrastructure exists, just needs consistent application

---

## Estimated Effort

**Total:** 120-165 minutes | 23,000 tokens

**Breakdown:**
- Subtask 1: 60-90 min (bulk work)
- Subtask 2: 20-30 min (documentation)
- Subtask 3: 20-30 min (testing)
- Subtask 4: 15-25 min (fallback implementation)
- Subtask 5: 5-10 min (fallback testing)

**Risk Factors:**
- Finding all 35 tools that need updates
- Edge cases in alias resolution
- Testing degraded modes without actual git failure

---

## Bootstrap Information for Next Session

### Context to Provide
1. This spec document
2. Previous session achievements:
   - 81% error helper coverage
   - Session vs cascade clarification
   - Structured error response pattern established
3. `resolve_session_id()` function location
4. `create_error_response()` function location

### Quick Start Commands
```python
# Bootstrap new session
bootstrap_session(ai_id='your_id', session_type='development', bootstrap_level=2)

# Execute PREFLIGHT
execute_preflight(
    session_id='your_session',
    prompt='Implement session aliases and graceful degradation across 35 MCP tools'
)

# Search for tools needing updates
grep -n 'arguments.get("session_id")' mcp_local/empirica_mcp_server.py
```

---

## Notes from Previous Session

### Patterns Established
- ✅ Structured error responses (use `create_error_response()`)
- ✅ Exception handlers with tracebacks + structure
- ✅ Consistent error types (6 types defined)
- ✅ Test-driven approach

### Best Practices
- Systematic batching (group similar changes)
- Commit frequently with clear messages
- Test after each batch
- Document patterns for future work

### Tools Already Updated
Some tools already use `resolve_session_id()` - check before modifying:
- `get_session_summary`
- `get_epistemic_state`
- `load_git_checkpoint`
- `resume_previous_session`
- `get_calibration_report`

**Strategy:** Find tools that DON'T use it yet, apply pattern consistently.

---

## Success Metrics

### Coverage
- **Session alias support:** 35/35 tools (100%)
- **Schema documentation:** 35/35 tools (100%)
- **Test coverage:** All alias types + all fallback modes

### Quality
- **Consistency:** Same alias behavior across all tools
- **Reliability:** Operations work in degraded mode
- **User Experience:** Clear, helpful error messages

### Performance
- **No regressions:** Existing functionality intact
- **All tests passing:** Including new alias tests
- **Production ready:** Documented and validated

---

## Handoff Checklist for Next Session

- [ ] Read this spec document
- [ ] Bootstrap new session
- [ ] Execute PREFLIGHT for this task
- [ ] Search for tools needing `resolve_session_id()`
- [ ] Apply pattern systematically (batch by operation type)
- [ ] Update schemas as you go
- [ ] Create tests after bulk implementation
- [ ] Implement fallback hierarchy
- [ ] Test degraded modes
- [ ] Commit frequently with clear messages
- [ ] Execute POSTFLIGHT when complete

---

## Questions for Next Session

1. Should we add new alias patterns beyond the existing 4?
2. Should fallback warnings be logged or returned in response?
3. Should we add metrics for degraded mode usage?
4. Any edge cases in alias resolution we should handle?

---

**Status:** Ready for implementation in fresh session  
**Prepared by:** Rovo Dev (Session 1493402f-792b-487c-b98b-51e31ebf00a1)  
**Date:** November 18, 2025
