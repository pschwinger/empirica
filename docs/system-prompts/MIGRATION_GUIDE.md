# Migration Guide: Moving to Canonical System Prompt

**Purpose:** Help users migrate from old/deprecated system prompts to the canonical v2.0 prompt.

---

## Why Migrate?

The canonical system prompt (v2.0) provides:
- ✅ **Correct CASCADE model** (implicit workflow + explicit assessments)
- ✅ **MCO architecture** (dynamic configuration, decision logic)
- ✅ **ScopeVector goals** (3D scope measurement)
- ✅ **Git integration** (checkpoints, handoffs)
- ✅ **Single source of truth** (one prompt for all agents)

---

## What's Deprecated

### Old System Prompts (Move to Archive)

These prompts are **outdated** and should be archived to `empirica-dev/archive/system-prompts-deprecated/`:

**Agent-Specific Prompts:**
- `ai-agents/CLAUDE.md`
- `ai-agents/QWEN.md`
- `ai-agents/MINIMAX.md`
- `ai-agents/GEMINI.md`

**Development Prompts:**
- `development/SYSTEM_PROMPT_DEV_*.md`
- `development/AGENTS.md` variants

**Old Generic Prompts:**
- `comprehensive/GENERIC_EMPIRICA_SYSTEM_PROMPT.md`
- Any prompts referencing "PREFLIGHT phase" or "POSTFLIGHT phase"

### What to Keep for Reference

**Keep these docs** (they're still useful):
- `COMPLETE_MCP_TOOL_REFERENCE.md` - Tool documentation
- `OPTIMIZATION_ANALYSIS.md` - Token optimization research
- `CUSTOMIZATION_GUIDE.md` - When/how to customize

---

## Migration Steps

### Step 1: Identify Your Current Prompt

**Where to look:**
- AI client configuration (Claude Desktop, Cursor, etc.)
- `.github/copilot-instructions.md`
- Custom agent config files
- System prompt templates

### Step 2: Replace with Canonical

1. **Open:** `docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md`
2. **Copy:** Everything between the code fences (lines 11-194)
3. **Paste:** Into your AI's system prompt configuration
4. **Done!** No customization needed for 99% of cases

### Step 3: Archive Old Prompts

```bash
# Create archive directory
mkdir -p empirica-dev/archive/system-prompts-deprecated/

# Move old prompts
mv ai-agents/CLAUDE.md empirica-dev/archive/system-prompts-deprecated/
mv ai-agents/QWEN.md empirica-dev/archive/system-prompts-deprecated/
# ... etc
```

---

## Key Changes to Understand

### 1. CASCADE is Now Implicit

**Old (Wrong):**
```
"You are in PREFLIGHT phase"
"Transition to INVESTIGATE phase"
"Now entering ACT phase"
```

**New (Correct):**
```
"I'm investigating right now" (self-assessed)
"Should I investigate more or am I ready to act?" (CHECK decision)
"Session complete, what did I learn?" (POSTFLIGHT assessment)
```

**Key insight:** CASCADE (think→investigate→act) is **implicit workflow**, not explicit phase tracking.

### 2. Assessments are Explicit Checkpoints

**Three explicit assessment points:**
- **PREFLIGHT**: Before work begins (session start)
- **CHECK**: Decision points (can happen 0-N times)
- **POSTFLIGHT**: After work completes (session end, calibration)

**Pattern:**
```
PREFLIGHT → [investigate → act → CHECK]* → POSTFLIGHT
           (implicit work with explicit checkpoints)
```

### 3. ScopeVector Goals (3D)

**Old:** Semantic strings like "project_wide", "module_scoped"  
**New:** Vectorial measurement

```python
scope = ScopeVector(
    breadth=0.7,      # 0-1: codebase span
    duration=0.3,     # 0-1: time commitment
    coordination=0.8  # 0-1: multi-agent needs
)
```

### 4. MCO Architecture

**New features in v2.0:**
- Dynamic configuration (5 YAML configs)
- Automatic decision logic
- Model-specific bias correction
- Git integration for continuity

---

## Common Migration Issues

### Issue 1: "My prompt references explicit phases"

**Problem:** Old prompts say "PREFLIGHT phase", "INVESTIGATE phase", etc.  
**Solution:** Replace with canonical prompt. It correctly shows:
- CASCADE = implicit workflow
- PREFLIGHT/CHECK/POSTFLIGHT = explicit assessments

### Issue 2: "I customized my agent prompt"

**Problem:** Agent-specific customizations  
**Solution:** See `CUSTOMIZATION_GUIDE.md` for:
- When customization is needed (rare!)
- How to customize properly
- Examples

### Issue 3: "My tools don't match the prompt"

**Problem:** Prompt references tools you don't have access to  
**Solution:** Update Section IV (TOOLS) to list only available tools

### Issue 4: "My workflow is different"

**Problem:** Team uses different workflow patterns  
**Solution:** The canonical prompt is **guidance**, not enforcement. AI naturally adapts based on task needs.

---

## Verification Checklist

After migration, verify:

- [ ] Prompt correctly shows CASCADE as implicit workflow
- [ ] PREFLIGHT/CHECK/POSTFLIGHT are assessment points, not phases
- [ ] ScopeVector format is used for goals
- [ ] Decision logic thresholds match your needs
- [ ] Tool list matches available MCP tools
- [ ] Old prompts archived (not deleted)

---

## Rollback (If Needed)

If you need to rollback temporarily:

1. Old prompts are in `empirica-dev/archive/system-prompts-deprecated/`
2. Copy back to original location
3. Update AI configuration
4. Report issues to Empirica team

**But:** The canonical prompt is tested and correct. Rollback should be rare.

---

## Getting Help

**Questions?**
- Check `CUSTOMIZATION_GUIDE.md` for customization needs
- Review `CANONICAL_SYSTEM_PROMPT.md` for correct usage
- Check `CASCADE_CONCEPTUAL_CORRECTION_SUMMARY.md` for model explanation

**Found issues?**
- Document in `empirica-dev/issues/`
- Discuss with team
- Propose improvements

---

## Timeline Recommendation

**Week 1:** Migrate personal AI agents (low risk)  
**Week 2:** Test canonical prompt with real work  
**Week 3:** Migrate team agents  
**Week 4:** Archive old prompts

Take your time. The canonical prompt is stable and tested.

---

**Version:** 2.0  
**Last Updated:** 2025-01-29  
**Status:** Migration guide for v1.x → v2.0
