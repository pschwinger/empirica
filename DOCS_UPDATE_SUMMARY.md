# Documentation Update Required ⚠️

## Issue
Production docs reference deleted bootstrap classes and removed commands.

## Scope
**10 docs need updates** (198 total bootstrap references)

### Critical Priority (4 docs)
1. `03_BASIC_USAGE.md` - 33 refs - Needs complete rewrite
2. `15_CONFIGURATION.md` - 28 refs - Remove bootstrap config
3. `17_PRODUCTION_DEPLOYMENT.md` - 27 refs - Update deployment flow
4. `13_PYTHON_API.md` - 22 refs - Update Python examples

### Lower Priority (6 docs)
5-10. Various architecture/reference docs with 1-17 refs each

## What Changed

### Removed ❌
- `ExtendedMetacognitiveBootstrap` class (deleted)
- `OptimalMetacognitiveBootstrap` class (deleted)
- `empirica bootstrap` command (removed)
- Component pre-loading concept (obsolete)

### Added ✅
- `empirica session-create` command
- Direct SessionDatabase.create_session() API
- Lazy-loading components (no ceremony)

## Next Steps

See `docs/production/DOCS_UPDATE_PLAN.md` for:
- Detailed file-by-file breakdown
- OLD → NEW code examples
- Replacement patterns
- Update strategy

**Recommendation:** Update 03_BASIC_USAGE.md first (most visible to users).

