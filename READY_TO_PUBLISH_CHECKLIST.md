# ✅ Ready to Publish - Final Checklist

**Date:** 2025-12-03  
**Status:** All systems ready for PyPI publication

---

## ✅ Completed Pre-Publishing Tasks

### Package Quality
- [x] Package builds without errors
- [x] Package size optimized (556KB)
- [x] Critical bug fixed (modality_switcher included)
- [x] Twine validation passes: `PASSED`
- [x] Clean install tested in fresh venv
- [x] CLI commands work (`empirica bootstrap --help`)
- [x] All imports succeed (including modality_switcher)
- [x] Docker image builds and runs successfully

### Documentation
- [x] README.md cleaned and professional (162 lines)
- [x] WHY_EMPIRICA.md created (public philosophy)
- [x] docs/COMPLETE_INSTALLATION_GUIDE.md created (371 lines)
- [x] All WIP/schema migration warnings removed
- [x] Root directory cleaned (23 → 7 files)
- [x] docs/ cleaned (75+ → 63 files)
- [x] Session docs archived to empirica-dev/

### GitHub URLs Updated
- [x] README.md → `github.com/nubaeon/empirica`
- [x] docs/COMPLETE_INSTALLATION_GUIDE.md → `github.com/nubaeon/empirica`
- [x] packaging/homebrew/empirica.rb → `github.com/nubaeon/empirica`
- [x] packaging/chocolatey/empirica.nuspec → `github.com/nubaeon/empirica`
- [x] packaging/chocolatey/tools/chocolateyinstall.ps1 → `github.com/nubaeon/empirica`

### Docker Hub URLs Updated
- [x] README.md → `soulentheo/empirica`
- [x] docs/COMPLETE_INSTALLATION_GUIDE.md → `soulentheo/empirica`
- [x] scripts/distribute_all.sh → `soulentheo/empirica`
- [x] DISTRIBUTION_README.md → `soulentheo/empirica`

### PyPI Credentials
- [x] PyPI account created (username: `soulentheo`)
- [x] API token generated
- [x] `.pypirc` configured at `/home/yogapad/.pypirc`
- [x] Secure permissions set (600)
- [x] Twine installed and tested (v6.2.0)

### Distribution Automation
- [x] scripts/publish_to_pypi.sh ready
- [x] scripts/distribute_all.sh ready (one-click distribution)
- [x] Homebrew formula ready (packaging/homebrew/empirica.rb)
- [x] Chocolatey package ready (packaging/chocolatey/)
- [x] Docker image ready (empirica:1.0.0-beta)

---

## 🚀 Publishing Commands

### Option 1: Test First (Recommended)

```bash
cd /home/yogapad/empirical-ai/empirica

# Publish to TestPyPI first
./scripts/publish_to_pypi.sh test

# Verify installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ empirica

# Test it works
empirica bootstrap --help
```

### Option 2: Direct to Production

```bash
cd /home/yogapad/empirical-ai/empirica

# Publish to production PyPI
./scripts/publish_to_pypi.sh prod

# Verify installation from PyPI
pip install empirica

# Test it works
empirica bootstrap --help
```

### Option 3: Full Distribution Pipeline

```bash
cd /home/yogapad/empirical-ai/empirica

# Run complete distribution pipeline
./scripts/distribute_all.sh prod
```

This will:
1. Clean old builds
2. Build package
3. Validate with twine
4. Test installation
5. Publish to PyPI
6. Update Homebrew formula SHA256
7. Update Chocolatey package SHA256
8. Rebuild Docker image
9. Test Docker image

---

## 📦 Package Details

**Version:** 1.0.0-beta  
**Size:** 556KB (wheel and tarball)  
**SHA256:** `bf9f9ee2f65277959121ddfa7069a71343ef25c592afe6142e9143eed2572e50`

**Files in package:**
- ✅ empirica/ (all modules including modality_switcher)
- ✅ mcp_local/ (MCP server)
- ✅ docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md
- ✅ docs/skills/SKILL.md
- ✅ empirica/config/*.yaml (all config files)

**Excluded (correctly):**
- ✅ forgejo-plugin-empirica/ (33MB node_modules)
- ✅ empirica-dev/ (development notes)
- ✅ website/ (website builder)
- ✅ tests/ (test suite)
- ✅ scripts/ (build scripts)

---

## 🔍 Post-Publishing Verification

After publishing, verify:

```bash
# 1. Search on PyPI
open https://pypi.org/project/empirica/

# 2. Install in clean environment
python3 -m venv /tmp/verify_empirica
/tmp/verify_empirica/bin/pip install empirica

# 3. Test CLI
/tmp/verify_empirica/bin/empirica --version
/tmp/verify_empirica/bin/empirica bootstrap --help

# 4. Test imports
/tmp/verify_empirica/bin/python -c "
from empirica.cli.cli_core import main
from empirica.core.schemas.epistemic_assessment import EpistemicAssessment
from empirica.plugins.modality_switcher import ModalitySwitcher
print('✅ All imports successful')
"

# 5. Cleanup
rm -rf /tmp/verify_empirica
```

---

## 🐳 Docker Hub Publishing (Optional)

After PyPI publishing, you can publish the Docker image:

```bash
cd /home/yogapad/empirical-ai/empirica

# Tag for Docker Hub
docker tag empirica:1.0.0-beta soulentheo/empirica:1.0.0-beta
docker tag empirica:1.0.0-beta soulentheo/empirica:latest

# Login to Docker Hub
docker login

# Push images
docker push soulentheo/empirica:1.0.0-beta
docker push soulentheo/empirica:latest

# Verify
docker pull soulentheo/empirica:latest
docker run --rm soulentheo/empirica:latest --version
```

---

## 🍺 Homebrew Publishing (Optional)

After PyPI publishing:

1. **Create Homebrew tap:**
   ```bash
   brew tap-new nubaeon/tap
   ```

2. **Copy formula:**
   ```bash
   cp packaging/homebrew/empirica.rb $(brew --repo nubaeon/tap)/Formula/
   ```

3. **Push to GitHub:**
   ```bash
   cd $(brew --repo nubaeon/tap)
   git add Formula/empirica.rb
   git commit -m "Add Empirica formula"
   git push
   ```

4. **Users install:**
   ```bash
   brew tap nubaeon/tap
   brew install empirica
   ```

---

## 🍫 Chocolatey Publishing (Optional)

After PyPI publishing (requires Windows):

1. **Build package:**
   ```powershell
   cd packaging/chocolatey
   choco pack
   ```

2. **Test locally:**
   ```powershell
   choco install empirica -s . -y
   empirica bootstrap --help
   ```

3. **Publish to Chocolatey Community:**
   ```powershell
   choco apikey --key YOUR_API_KEY --source https://push.chocolatey.org/
   choco push empirica.1.0.0-beta.nupkg --source https://push.chocolatey.org/
   ```

---

## ⚠️ Important Notes

### API Token Security
- **Never commit** `/home/yogapad/.pypirc` to git
- Token is in `.gitignore` (verify: `cat .gitignore | grep pypirc`)
- Token has limited scope (only `empirica` package)

### Version Bumping
When releasing new versions:

1. Update version in `pyproject.toml`
2. Update version in `packaging/chocolatey/empirica.nuspec`
3. Rebuild: `python -m build`
4. New SHA256 will be calculated automatically
5. Run `./scripts/distribute_all.sh prod`

### Package Name Ownership
- Package name `empirica` is claimed on PyPI by user `soulentheo`
- Only this account can upload to `empirica` package
- TestPyPI and production PyPI are separate accounts (may need separate tokens)

---

## ✅ Final Status

**Everything is ready!** 🎉

You can now publish Empirica to PyPI with:

```bash
./scripts/publish_to_pypi.sh test   # Recommended: test first
# OR
./scripts/publish_to_pypi.sh prod   # Direct to production
```

---

## 📊 What Happens When You Publish

1. **Cleaning** - Removes old build artifacts
2. **Building** - Creates wheel and source distribution
3. **Validation** - Runs `twine check`
4. **Testing** - Tests installation in clean venv
5. **Uploading** - Uses twine to upload to PyPI
6. **Verification** - Package appears on https://pypi.org/project/empirica/

**Estimated time:** 2-3 minutes

---

## 🎯 After Publishing

1. ✅ Package available: `pip install empirica`
2. ✅ README visible on PyPI
3. ✅ Links work (GitHub, documentation)
4. ✅ Users can install globally
5. ✅ CI/CD can pin versions
6. ✅ Community can discover and use

---

**Ready when you are!** 🚀

Run `./scripts/publish_to_pypi.sh test` to start.
