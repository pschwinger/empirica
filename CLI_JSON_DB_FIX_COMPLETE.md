# CLI JSON Output & Database Consolidation - Complete ✅

## Summary

Fixed two critical integration issues:
1. ✅ Added JSON output support to CLI commands
2. ✅ Deprecated global database, consolidated to project-local only

---

## Part 1: Database Consolidation

### Problem
Two databases caused confusion:
- `~/.empirica/sessions.db` (global, 954KB, 131 sessions)
- `./.empirica/sessions/sessions.db` (project-local, 733KB, 78 sessions)

### Solution
- ✅ Moved global DB to `empirica-dev/archive/old-databases/sessions.db.deprecated`
- ✅ Created README with deprecation notice and migration guide
- ✅ Now using **only** project-local database

### Result
Single source of truth: `./.empirica/sessions/sessions.db`

---

## Part 2: JSON Output Support

### Problem
CLI commands only supported text output:
```bash
$ empirica sessions-show <id> --output json
ERROR: unrecognized arguments: --output json
```

### Solution
Added `--output` flag to key commands:
- ✅ `sessions-show --output json`
- ✅ `sessions-list --output json`

### Usage
```bash
# Text output (default)
empirica sessions-show 9fc34143

# JSON output
empirica sessions-show 9fc34143 --output json
{
  "session_id": "9fc34143-7763-422c-90b8-b37a28ffab3f",
  "ai_id": "claude-code",
  "start_time": "2025-12-03 15:39:50.021873",
  "end_time": null,
  "status": "active",
  "cascades": []
}

# List in JSON
empirica sessions-list --limit 5 --output json
{
  "sessions": [...],
  "total": 5
}
```

---

## Files Modified

1. `empirica/cli/cli_core.py` - Added --output argument
2. `empirica/cli/command_handlers/utility_commands.py` - Implemented JSON output
3. `empirica-dev/archive/old-databases/` - Archived old database

---

## Testing

```bash
# Verify single database
$ ls ~/.empirica/sessions.db
ls: cannot access '~/.empirica/sessions.db': No such file or directory ✅

$ ls ./.empirica/sessions/sessions.db
./.empirica/sessions/sessions.db ✅

# Test JSON output
$ empirica sessions-show 9fc34143 --output json | jq '.session_id'
"9fc34143-7763-422c-90b8-b37a28ffab3f" ✅
```

---

## Impact

### For Statusline Integration
**Before:**
```python
# Parse text output with regex 🤮
output = subprocess.check_output(['empirica', 'sessions-show', session_id])
ai_id = re.search(r'AI: (\w+)', output).group(1)
```

**After:**
```python
# Parse structured JSON ✨
output = subprocess.check_output(['empirica', 'sessions-show', session_id, '--output', 'json'])
data = json.loads(output)
ai_id = data['ai_id']
```

### For All Users
- ✅ No more database confusion
- ✅ Clear storage location
- ✅ Programmatic CLI access

---

## Git Commit

```
4c8e9f2a Add JSON output to CLI and deprecate global database
```
