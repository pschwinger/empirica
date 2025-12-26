# Lean System Prompt Updates - v5.1

**Date:** 2025-12-25
**Status:** Completed

## Problem Statement

Qwen and other AIs found the lean v5.1 system prompts too sparse. While they understood epistemic checks (CASCADE workflow), they lacked clear guidance on:

1. ✗ Goal/subtask tracking (when/why/how)
2. ✗ BEADS integration (git branch/issue automation)
3. ✗ Epistemic handoffs (3 types: investigation/complete/planning)
4. ✗ Logging epistemic breadcrumbs (findings, unknowns, dead ends, mistakes)
5. ✗ CLI help output (required vs optional parameters unclear)

## Solution

### 1. Updated Lean System Prompts

**Files modified:**
- `/home/yogapad/.claude/CLAUDE.md` (Claude Code)
- `/home/yogapad/.vibe/instructions.md` (Mistral AI)

**Sections added:**

#### A. GOAL/SUBTASK TRACKING (For Complex Work)
- **When to use:** Complex investigations (>5 decisions), multi-session work, high uncertainty
- **Python API pattern:** create_goal() → create_subtask() → update_subtask_findings/unknowns/dead_ends()
- **CLI mode:** JSON stdin for goals, CLI flags for subtasks
- **Key benefit:** Goal tree auto-included in handoff

#### B. EPISTEMIC BREADCRUMBS (Required Logging)
- **Findings:** What you learned (REQUIRED)
- **Unknowns:** What's still unclear (REQUIRED)
- **Dead ends:** What didn't work (log when blocked)
- **Mistakes:** What went wrong + prevention (log errors)
- **Session-based auto-linking:** All breadcrumbs link to active goal automatically

**Why this matters:**
- CHECK decisions query unknowns (proceed vs investigate)
- Next AI loads findings (instant context)
- Dead ends prevent duplicate work
- Mistakes improve calibration

#### C. HANDOFF TYPES (Multi-Session Continuity)

**3 handoff patterns:**

1. **Investigation Handoff (PREFLIGHT → CHECK)**
   - Use: Research specialist → Implementation specialist
   - Pattern: Investigation complete, ready for execution
   - Example: "Mapped OAuth2 flow, ready to implement"

2. **Complete Handoff (PREFLIGHT → POSTFLIGHT)**
   - Use: Full task completion with learning measurement
   - Pattern: Complete CASCADE workflow
   - Example: "Implemented OAuth2, learned refresh patterns"

3. **Planning Handoff (No CASCADE)**
   - Use: Documentation/planning without epistemic assessment
   - Pattern: No PREFLIGHT/POSTFLIGHT, just findings/next steps
   - Example: "Planned OAuth2 approach, chose PKCE"

**Auto-detection:** System detects type from CASCADE phases present.

#### D. BEADS INTEGRATION (Git + Issue Tracking)

**Goals auto-create:**
- Git branch: `empirica/goal-<short-objective>`
- Git issue: If repository has issue tracking enabled

**Handoffs create:**
- Git notes: Compressed epistemic state (97.5% token reduction)
- Branch merge: When goal completes

**You don't manage this** - system handles BEADS automatically:
1. Create goal → Branch created
2. Log breadcrumbs → Git notes updated
3. Complete goal → Issue closed, branch merged
4. Create handoff → Git notes written

---

### 2. Improved CLI Help Output

**Problem:** Argparse shows all arguments under "options:" even if `required=True`, making it unclear which parameters are required vs optional.

**Solution:** Created `format_help_text()` helper function to add clear markers.

**Files modified:**
- `empirica/cli/parsers/__init__.py` - Added `format_help_text()` helper
- `empirica/cli/parsers/checkpoint_parsers.py` - Example implementation

**Helper function:**
```python
def format_help_text(text, required=False, default=None):
    """
    Format help text with clear required/optional markers.

    Args:
        text: Base help text
        required: If True, add (required) marker
        default: If provided, add default value info

    Returns:
        Formatted help text

    Examples:
        format_help_text("Session ID", required=True)
        # Returns: "Session ID (required)"

        format_help_text("Maximum items", default=10)
        # Returns: "Maximum items (optional, default: 10)"
    """
    if required:
        return f"{text} (required)"
    elif default is not None:
        return f"{text} (optional, default: {default})"
    else:
        return f"{text} (optional)"
```

**Usage in parsers:**
```python
from . import format_help_text

checkpoint_create_parser.add_argument(
    '--session-id',
    required=True,
    help=format_help_text('Session ID', required=True)
)
```

**Before:**
```
options:
  --session-id SESSION_ID    Session ID
  --metadata METADATA        JSON metadata (optional)
```

**After:**
```
options:
  --session-id SESSION_ID    Session ID (required)
  --metadata METADATA        JSON metadata (optional)
```

---

## Impact

### For AIs
- ✅ Clear guidance on goal/subtask tracking
- ✅ Explicit breadcrumb logging requirements
- ✅ Handoff patterns well-defined
- ✅ BEADS automation explained (no manual git work)
- ✅ CLI help clearly shows required vs optional

### For Users
- ✅ AIs will consistently log findings/unknowns/dead ends/mistakes
- ✅ Better multi-session continuity through handoffs
- ✅ Improved CLI usability (clear parameter requirements)

---

## Next Steps

### 1. Apply Help Text Formatting to All Parsers (Optional)

Update all parser files to use `format_help_text()`:
- `cascade_parsers.py`
- `session_parsers.py`
- `investigation_parsers.py`
- `action_parsers.py`
- `utility_parsers.py`
- `config_parsers.py`
- `monitor_parsers.py`
- `performance_parsers.py`
- `skill_parsers.py`
- `user_interface_parsers.py`
- `vision_parsers.py`
- `epistemics_parsers.py`

**Pattern:**
```python
from . import format_help_text

parser.add_argument(
    '--required-param',
    required=True,
    help=format_help_text('Description', required=True)
)

parser.add_argument(
    '--optional-param',
    default=10,
    help=format_help_text('Description', default=10)
)
```

### 2. Test with Qwen and Other AIs

Have Qwen and other AIs test the updated prompts to verify:
- ✅ Goal/subtask workflow is now clear
- ✅ Breadcrumb logging is understood
- ✅ Handoff types are clear
- ✅ BEADS integration is understood (no manual git)
- ✅ CLI help is clearer

---

## Files Changed

**System prompts:**
1. `/home/yogapad/.claude/CLAUDE.md` - Added 4 workflow sections
2. `/home/yogapad/.vibe/instructions.md` - Added 4 workflow sections

**CLI parsers:**
3. `empirica/cli/parsers/__init__.py` - Added `format_help_text()` helper
4. `empirica/cli/parsers/checkpoint_parsers.py` - Example implementation

---

## Token Counts

**CLAUDE.md:**
- Before: 207 lines
- After: 321 lines
- Change: +114 lines (55% increase)

**instructions.md:**
- Before: 210 lines
- After: 324 lines
- Change: +114 lines (54% increase)

**Trade-off:** Increased prompt size for critical workflow clarity. These sections are NOT discoverable via --help, so they must be in the system prompt.

---

**Status:** Ready for AI testing to validate improvements.
