# System Prompt Fixes v5.2 - Multi-AI Workflows & CLI Consistency

**Date:** 2025-12-25
**Status:** Completed

## Issues Addressed

### 1. AIs Missing Critical Workflow Guidance
**Problem:** Qwen and other AIs understood CASCADE (epistemic checks) but lacked clarity on:
- Goal lifecycle management (claim/complete)
- Multi-AI coordination (discovering/resuming work)
- Session resumption patterns
- Multi-repo workspace awareness
- Project initialization
- BEADS integration details

**Impact:** AIs created goals but didn't know how to properly start or finish them in the BEADS workflow.

---

### 2. Handoff-Create Missing JSON Stdin Support
**Problem:** `handoff-create` didn't accept JSON via stdin like other commands:
```bash
# This failed:
empirica handoff-create - < /tmp/handoff.json

# Only this worked (verbose):
empirica handoff-create --session-id X --task-summary "..." --key-findings "[...]" ...
```

**Impact:** Inconsistent AI-first interface, AIs couldn't use preferred JSON stdin pattern.

---

## Solutions Implemented

### 1. Added MULTI-AI & WORKFLOW COMMANDS Section

**Files modified:**
- `/home/yogapad/.claude/CLAUDE.md` (207 → 403 lines)
- `/home/yogapad/.vibe/instructions.md` (210 → 406 lines)

**New sections added:**

#### A. Goal Lifecycle Management
```bash
# Complete workflow: create → claim → work → complete
empirica goals-create ...       # Create goal
empirica goals-claim --goal-id <ID>       # Start (creates branch + BEADS link)
empirica goals-complete --goal-id <ID>    # Finish (merges branch + closes issue)
```

#### B. Multi-AI Coordination
```bash
# Finding work
empirica goals-ready --output json        # What's ready to claim?
empirica goals-discover --output json     # What are others working on?

# Resuming work
empirica goals-resume --goal-id <ID>      # Take over incomplete work
```

#### C. Session Resumption
```bash
empirica session-snapshot --session-id <ID>   # Quick context
empirica sessions-resume --ai-id <ID>         # Resume previous session
```

#### D. Multi-Repo/Workspace Awareness
```bash
empirica workspace-map --output json          # Discover all repos
empirica workspace-overview --output json     # Cross-project health
```

#### E. Project Initialization
```bash
empirica project-init                         # First-time setup (creates config files)
```

#### F. Semantic Search (Advanced)
```bash
empirica project-search --query "..." --output json   # Qdrant-based targeted search
```

---

### 2. Fixed Handoff-Create JSON Stdin Support

**Files modified:**
- `empirica/cli/parsers/checkpoint_parsers.py`
- `empirica/cli/command_handlers/handoff_commands.py`

**Changes:**

#### Parser (checkpoint_parsers.py:127-149)
```python
# Added AI-FIRST positional config argument
handoff_create_parser.add_argument('config', nargs='?',
    help='JSON config file path or "-" for stdin (AI-first mode)')

# Updated help text with required/optional markers
handoff_create_parser.add_argument('--session-id',
    help=format_help_text('Session UUID', required=True))
```

#### Handler (handoff_commands.py:15-87)
```python
# Added config file/stdin handling
config_data = None
if hasattr(args, 'config') and args.config:
    if args.config == '-':
        config_data = parse_json_safely(sys.stdin.read())
    else:
        with open(args.config, 'r') as f:
            config_data = parse_json_safely(f.read())

# Extract from config or fall back to legacy flags
if config_data:
    session_id = config_data.get('session_id')
    task_summary = config_data.get('task_summary')
    # ... validate required fields
else:
    # Legacy mode with CLI flags
    session_id = args.session_id
    # ...
```

**Now works:**
```bash
cat > /tmp/handoff.json << 'EOF'
{
  "session_id": "abc-123",
  "task_summary": "Implemented OAuth2 flow",
  "key_findings": ["PKCE required", "Refresh token rotation prevents theft"],
  "remaining_unknowns": ["Token revocation at scale"],
  "next_session_context": "Auth complete, next: authorization layer"
}
EOF

empirica handoff-create - < /tmp/handoff.json --output json
```

---

### 3. Improved CLI Help Text Clarity

**Files modified:**
- `empirica/cli/parsers/__init__.py`
- `empirica/cli/parsers/checkpoint_parsers.py` (examples)

**Added helper function:**
```python
def format_help_text(text, required=False, default=None):
    """
    Format help text with clear required/optional markers.

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

## Token Counts

**Lean prompts growth:**
- CLAUDE.md: 207 → 403 lines (+196 lines, 96% increase)
- instructions.md: 210 → 406 lines (+196 lines, 93% increase)

**Trade-off justified:** Multi-AI workflow commands are NOT discoverable via `--help` alone - they require understanding of the full workflow pattern. These must be in the system prompt.

---

## Testing Checklist

### Handoff-Create JSON Stdin
- [ ] Test: `echo '{"session_id":"..."}' | empirica handoff-create -`
- [ ] Test: Legacy mode still works with CLI flags
- [ ] Test: Error messages clear for missing fields
- [ ] Test: Both epistemic and planning handoffs work

### Help Text Improvements
- [ ] Test: `empirica checkpoint-create --help` shows (required) markers
- [ ] Test: All commands using `format_help_text()` have clear labels
- [ ] Test: Apply to remaining parsers (optional, can be done incrementally)

### AI Understanding
- [ ] Test with Qwen: Does it understand goal lifecycle?
- [ ] Test with Qwen: Does it know about goals-ready/goals-discover?
- [ ] Test with Mistral: Does it understand multi-AI coordination?
- [ ] Test: Do AIs properly claim and complete goals (not just create)?

---

## Files Changed

**System prompts:**
1. `/home/yogapad/.claude/CLAUDE.md` - Added MULTI-AI & WORKFLOW COMMANDS
2. `/home/yogapad/.vibe/instructions.md` - Added MULTI-AI & WORKFLOW COMMANDS

**CLI parsers:**
3. `empirica/cli/parsers/__init__.py` - Added `format_help_text()` helper
4. `empirica/cli/parsers/checkpoint_parsers.py` - Added JSON stdin to handoff-create, improved help text

**CLI handlers:**
5. `empirica/cli/command_handlers/handoff_commands.py` - Added config/stdin handling

---

## Next Steps (Optional)

### 1. Apply Help Text Formatting to All Parsers
Pattern to follow:
```python
from . import format_help_text

parser.add_argument(
    '--required-param',
    required=True,
    help=format_help_text('Description', required=True)
)
```

**Parsers to update:**
- cascade_parsers.py
- session_parsers.py
- investigation_parsers.py
- action_parsers.py
- utility_parsers.py
- config_parsers.py
- monitor_parsers.py
- performance_parsers.py
- skill_parsers.py
- user_interface_parsers.py
- vision_parsers.py
- epistemics_parsers.py

### 2. Add JSON Stdin Support to More Commands
Commands that might benefit (currently legacy-only):
- `mistake-log` (already has --session-id, could use JSON for full context)
- `finding-log`, `unknown-log`, `deadend-log` (batch operations)
- `goals-complete` (complex with multiple flags)

---

## Key Improvements Summary

✅ **Goal lifecycle now clear** - AIs know to claim (start) and complete (finish), not just create
✅ **Multi-AI coordination documented** - Finding work (goals-ready), resuming work (goals-resume)
✅ **Session resumption patterns clear** - session-snapshot vs sessions-resume vs checkpoint-load
✅ **Multi-repo workflows documented** - workspace-map, workspace-overview
✅ **Handoff-create AI-first** - JSON stdin support like other commands
✅ **Help text clearer** - (required) and (optional) markers explicit

**Impact:** AIs can now:
- Properly execute BEADS workflows (claim/complete)
- Coordinate in multi-AI teams (discover/resume work)
- Work across multiple repositories
- Use consistent JSON stdin interface for complex commands

---

**Status:** Ready for AI testing (Qwen, Mistral, others)
