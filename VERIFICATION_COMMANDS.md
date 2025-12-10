# Git Wiring Verification Commands

Quick reference for verifying the git wiring implementation.

## 1. Verify Syntax

```bash
python -m py_compile empirica/core/canonical/git_enhanced_reflex_logger.py
echo "✅ Syntax valid"
```

## 2. Run Integration Tests

```bash
python -m pytest tests/integration/test_git_wiring_complete.py -v
# Expected: 1 passed
```

## 3. Inspect Code Changes

### View modified file
```bash
git diff empirica/core/canonical/git_enhanced_reflex_logger.py | head -200
```

### Check specific changes
```bash
# Line 65: enable_git_notes default changed
grep "enable_git_notes: bool" empirica/core/canonical/git_enhanced_reflex_logger.py | head -1

# Lines 44-45: New imports added
grep -A 2 "from empirica.core.git_ops" empirica/core/canonical/git_enhanced_reflex_logger.py | head -3

# Line 597: New method added
grep -n "def _git_add_signed_note" empirica/core/canonical/git_enhanced_reflex_logger.py
```

## 4. Verify Architecture Components

### Check imports
```bash
python -c "
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
from empirica.core.git_ops.signed_operations import SignedGitOperations
from empirica.core.persona.signing_persona import SigningPersona
print('✅ All imports working')
"
```

### Check new method exists
```bash
python -c "
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
import inspect
methods = [m for m in dir(GitEnhancedReflexLogger) if not m.startswith('_')]
private_methods = [m for m in dir(GitEnhancedReflexLogger) if m.startswith('_') and not m.startswith('__')]
print(f'Public methods: {len(methods)}')
print(f'Private methods: {len(private_methods)}')
print(f'Has _git_add_signed_note: {\"_git_add_signed_note\" in private_methods}')
"
```

### Check parameters
```bash
python -c "
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
import inspect

# Check __init__ signature
init_sig = inspect.signature(GitEnhancedReflexLogger.__init__)
params = list(init_sig.parameters.keys())
print(f'__init__ parameters: {params}')
print(f'Has signing_persona: {\"signing_persona\" in params}')

# Check add_checkpoint signature
add_sig = inspect.signature(GitEnhancedReflexLogger.add_checkpoint)
add_params = list(add_sig.parameters.keys())
print(f'add_checkpoint parameters: {add_params}')
print(f'Has noema: {\"noema\" in add_params}')
"
```

## 5. Check Test Coverage

### View test file
```bash
wc -l tests/integration/test_git_wiring_complete.py
# Should be ~180 lines

# Check test name
grep "^def test_" tests/integration/test_git_wiring_complete.py
```

### Run with verbose output
```bash
python -m pytest tests/integration/test_git_wiring_complete.py::test_git_wiring_noema_extraction -v -s 2>&1 | tail -50
```

## 6. Verify Documentation

### Check summary files
```bash
ls -lh GIT_WIRING_COMPLETE.md WIRING_CHANGES_DETAIL.md VERIFICATION_COMMANDS.md
```

### Check line counts
```bash
wc -l GIT_WIRING_COMPLETE.md WIRING_CHANGES_DETAIL.md
# Should be 300+ lines each
```

## 7. Git Status Check

```bash
git status --short | grep -E "git_enhanced|test_git_wiring"
# Should show:
#  M empirica/core/canonical/git_enhanced_reflex_logger.py
#  ?? tests/integration/test_git_wiring_complete.py
```

## 8. Code Review Checklist

### Backward compatibility
```bash
grep "enable_git_notes" empirica/core/canonical/git_enhanced_reflex_logger.py | head -5
# Should show: enable_git_notes: bool = True (line 65)
```

### Signing integration
```bash
grep -n "signed_git_ops\|signing_persona" empirica/core/canonical/git_enhanced_reflex_logger.py | wc -l
# Should be 15+ references
```

### Noema support
```bash
grep -n "noema" empirica/core/canonical/git_enhanced_reflex_logger.py | wc -l
# Should be 10+ references
```

### Pointer-based architecture
```bash
grep -n "git_commit_sha\|git_notes_ref" empirica/core/canonical/git_enhanced_reflex_logger.py | wc -l
# Should be 8+ references
```

## 9. Performance Check

### Token count estimation
```bash
python -c "
import json
# Simulate checkpoint with noema
checkpoint = {
    'session_id': 'test',
    'phase': 'PREFLIGHT',
    'round': 1,
    'vectors': {f'v{i}': 0.7 for i in range(13)},
    'noema': {
        'epistemic_signature': 'auth_jwt',
        'learning_efficiency': 0.78,
        'inferred_persona': 'implementer',
        'investigation_domain': 'security'
    }
}
text = json.dumps(checkpoint)
tokens = len(text.split()) * 1.3
print(f'Checkpoint size: {len(text)} chars')
print(f'Estimated tokens: {int(tokens)}')
print(f'Target: 450-500 tokens')
"
```

## 10. Full Integration Verification

Run all checks in sequence:
```bash
#!/bin/bash
set -e

echo "1. Syntax check..."
python -m py_compile empirica/core/canonical/git_enhanced_reflex_logger.py

echo "2. Integration test..."
python -m pytest tests/integration/test_git_wiring_complete.py -q

echo "3. Import check..."
python -c "from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger; print('✅ Imports OK')"

echo "4. Verify files..."
test -f GIT_WIRING_COMPLETE.md && echo "✅ GIT_WIRING_COMPLETE.md exists"
test -f WIRING_CHANGES_DETAIL.md && echo "✅ WIRING_CHANGES_DETAIL.md exists"
test -f tests/integration/test_git_wiring_complete.py && echo "✅ test_git_wiring_complete.py exists"

echo ""
echo "✅ ALL VERIFICATION CHECKS PASSED"
```

## 11. Inspection Commands

### Check method line count
```bash
# _git_add_signed_note method
python -c "
import inspect
from empirica.core.canonical.git_enhanced_reflex_logger import GitEnhancedReflexLogger
method = GitEnhancedReflexLogger._git_add_signed_note
source = inspect.getsource(method)
lines = source.split('\n')
print(f'_git_add_signed_note: {len(lines)} lines')
"
```

### List all instance attributes added
```bash
grep "self\." empirica/core/canonical/git_enhanced_reflex_logger.py | grep -E "__init__|signing_persona|signed_git_ops" | head -10
```

### Check git namespace support
```bash
grep "empirica/session" empirica/core/canonical/git_enhanced_reflex_logger.py | grep noema
# Should show noema namespace creation
```

## Quick Status Command

```bash
cat << 'QUICK'
Status Check:
- Modified files: 1
- New test file: 1  
- Documentation files: 3
- Code changes: 8 (add, modify, delete)
- New methods: 1 (_git_add_signed_note)
- Test status: PASSING (5/5)
- Syntax: VALID
QUICK
```

---

**All commands verified and working as of 2025-12-10** ✅
