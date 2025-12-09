# Empirica Chat Current State Analysis

**Date:** 2025-12-08  
**Context:** Evaluating what needs updating for standalone chat experience

---

## Current Files

1. **empirica-epistemic-framework.skill** (13.7 KB)
   - Binary Claude Desktop skill file
   - Requires installation in Claude Desktop
   - Not usable in web chat interfaces

2. **empirica-demo-artifact.md** (7.5 KB)
   - Demo showing CASCADE workflow example
   - Status: Needs updating with v4.0 features (CHECK phase, etc.)

3. **EMPIRICA_SYSTEM_PROMPT_INTEGRATION.md** (9.4 KB)
   - For integrating with CLAUDE.md system prompt
   - Assumes skill file is installed
   - Not standalone

4. **README.md** (11 KB) - ✅ Just updated with v4.0
5. **EMPIRICA_SKILL_GUIDE.md** (8.3 KB) - ✅ Just updated with v4.0
6. **00_START_HERE.txt** (10.5 KB) - Quick start guide

---

## Key Findings

### MCP References
**Found:** No MCP references in demo or system prompt integration  
**Good:** Files don't assume MCP server access

### Skill File Dependency
**Issue:** Most files assume skill file is installed  
**Problem:** Not all chat interfaces support skills:
- ✅ Claude Desktop: Supports .skill files
- ❌ Claude.ai web: No skill support
- ❌ ChatGPT web: No skill support
- ❌ Gemini web: No skill support
- ❌ Other chatbots: No skill support

### Current User Experience Gaps

1. **Evaluation users** can't easily try Empirica
   - Need to install Claude Desktop
   - Need to install skill file
   - High friction

2. **Copy-paste experience** doesn't exist
   - No standalone prompt they can paste anywhere
   - README assumes skill context

3. **Demo artifact** needs v4.0 updates
   - No CHECK phase in example
   - Still uses old 4-vector simplified mode
   - Doesn't show investigation pattern

---

## What Needs Creating

### Priority 1: Standalone Copy-Paste Prompt

**Name:** `EMPIRICA_CHAT_PROMPT.md`

**Purpose:** Self-contained prompt users can paste into ANY chat interface

**Content:**
- Complete CASCADE workflow explanation
- Simple 5-vector mode (default)
- CHECK phase decision gate
- Investigation pattern
- Continuation template
- All in one copyable prompt (~800-1000 tokens)

**Target users:**
- Evaluating Empirica
- Using web chat interfaces (Claude.ai, ChatGPT, Gemini)
- Don't want to install anything

---

### Priority 2: Update Demo Artifact

**File:** `empirica-demo-artifact.md`

**Updates needed:**
- Add CHECK phase to example
- Show investigation pattern (high uncertainty → investigate)
- Update to simple 5-vector mode
- Add continuation template usage
- Make it v4.0 compliant

---

### Priority 3: Update System Prompt Integration

**File:** `EMPIRICA_SYSTEM_PROMPT_INTEGRATION.md`

**Updates needed:**
- Provide standalone version (no skill dependency)
- Add v4.0 features (CHECK, simple mode)
- Split into two versions:
  - With skill (current)
  - Without skill (new, standalone)

---

## MCP in Chat - Research Needed

**Question:** Can MCP servers be used in web chat interfaces now?

**Research findings needed:**
- Claude.ai web: MCP support status?
- ChatGPT web: MCP support status?
- Gemini web: MCP support status?

**Current assumption:** MCP only works in Claude Desktop, not web chat

**Impact:** If true, Empirica chat should NOT reference MCP tools

---

## Proposed Solution

### Create 3 Usage Tiers

**Tier 1: Copy-Paste (Universal)**
- `EMPIRICA_CHAT_PROMPT.md` - Standalone prompt
- Works in ANY chat interface
- No installation needed
- ~800-1000 tokens

**Tier 2: System Prompt (Advanced)**
- `EMPIRICA_SYSTEM_PROMPT_INTEGRATION.md` - For CLAUDE.md users
- Works in Claude Desktop, Cursor, etc.
- Requires system prompt access
- Better than copy-paste (persistent)

**Tier 3: Skill File (Claude Desktop Only)**
- `empirica-epistemic-framework.skill`
- Works only in Claude Desktop
- Requires skill installation
- Best experience but most limited

---

## Next Steps

1. **Research:** Confirm MCP only works in desktop apps, not web chat
2. **Create:** EMPIRICA_CHAT_PROMPT.md (standalone copy-paste version)
3. **Update:** empirica-demo-artifact.md (v4.0 features)
4. **Split:** EMPIRICA_SYSTEM_PROMPT_INTEGRATION.md (with/without skill)
5. **Test:** All three tiers with real users

---

**Goal:** Anyone can try Empirica in 30 seconds by pasting a prompt into their favorite chatbot.
