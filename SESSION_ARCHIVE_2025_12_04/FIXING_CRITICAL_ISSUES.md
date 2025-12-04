# Fixing Critical E2E Issues

## Issues to Fix:
1. ✅ sessions-list ignores --output json
2. ✅ SessionDatabase.create_session() API mismatch
3. ✅ Remove deprecated commands (assess, calibration)
4. ✅ Remove reflex_logger.py (only used by tests)

## Doc Changes Needed (After Removing Bootstrap):
- [ ] Update README.md (remove bootstrap examples)
- [ ] Update docs/getting-started.md (no bootstrap needed)
- [ ] Update MCP quickstart (direct tool usage)
- [ ] Update CLI quickstart (commands create sessions)

---

## Starting fixes...

## Fix 1: SessionDatabase.create_session() API ✅
- Made bootstrap_level and components_loaded optional with defaults
- bootstrap_level default = 0 (minimal)
- components_loaded default = 0 (on-demand)
- Now compatible with both old and new callers


## Fix 2: sessions-list --output json ✅
- Check output format FIRST before printing header
- JSON output skips all pretty printing
- Returns {"ok": true, "sessions": [...], "count": N}

