# Empirica Cross-Platform Distribution Guide

This guide documents the complete distribution pipeline for Empirica across multiple platforms.

## 🚀 Quick Start: One-Click Distribution

```bash
# Test mode (TestPyPI only)
./scripts/distribute_all.sh test

# Production mode (publish to PyPI)
./scripts/distribute_all.sh prod
```

This script orchestrates the entire pipeline: PyPI → Homebrew → Chocolatey → Docker

---

## 📦 Distribution Channels

### 1. PyPI (Python Package Index)

**Installation:**
```bash
pip install empirica
```

**Files:**
- `dist/empirica-1.0.0b0-py3-none-any.whl` - Wheel distribution
- `dist/empirica-1.0.0b0.tar.gz` - Source distribution

**Publishing:**
```bash
./scripts/publish_to_pypi.sh test   # TestPyPI
./scripts/publish_to_pypi.sh prod   # PyPI
```

**Configuration:**
- `pyproject.toml` - Package metadata and dependencies
- `MANIFEST.in` - Controls what files are included in source distribution
- `requirements.txt` - Runtime dependencies

---

### 2. Homebrew (macOS/Linux Package Manager)

**Installation:**
```bash
# Via tap (after publishing)
brew tap empirica/tap
brew install empirica

# Or directly from formula
brew install --build-from-source ./packaging/homebrew/empirica.rb
```

**Files:**
- `packaging/homebrew/empirica.rb` - Homebrew formula

**Building:**
```bash
# Auto-generate complete formula with all dependencies
python3 scripts/generate_homebrew_formula.py
```

**Testing:**
```bash
brew install --build-from-source ./packaging/homebrew/empirica.rb
empirica bootstrap --help
brew test empirica
```

**Publishing to Homebrew Tap:**
1. Create tap repository: `brew tap-new empirica/tap`
2. Copy formula to tap: `cp packaging/homebrew/empirica.rb $(brew --repo empirica/tap)/Formula/`
3. Push to GitHub
4. Users install: `brew tap empirica/tap && brew install empirica`

---

### 3. Chocolatey (Windows Package Manager)

**Installation:**
```powershell
choco install empirica
```

**Files:**
- `packaging/chocolatey/empirica.nuspec` - Package specification
- `packaging/chocolatey/tools/chocolateyinstall.ps1` - Install script
- `packaging/chocolatey/tools/chocolateyuninstall.ps1` - Uninstall script

**Building:**
```bash
# Prepare package (updates SHA256)
./scripts/build_chocolatey_package.sh

# On Windows, build .nupkg
cd packaging/chocolatey
choco pack
```

**Testing:**
```powershell
cd packaging/chocolatey
choco pack
choco install empirica -s . -y
empirica bootstrap --help
```

**Publishing to Chocolatey Community:**
```powershell
choco apikey --key YOUR_API_KEY --source https://push.chocolatey.org/
choco push empirica.1.0.0-beta.nupkg --source https://push.chocolatey.org/
```

---

### 4. Docker (Container Platform)

**Installation:**
```bash
docker pull soulentheo/empirica:latest
```

**Files:**
- `Dockerfile` - Multi-stage build with Python 3.11-slim
- `docker-compose.yml` - Orchestration for CLI and MCP server

**Building:**
```bash
docker build -t empirica:1.0.0-beta .
```

**Testing:**
```bash
docker run --rm empirica:1.0.0-beta bootstrap --help
docker run -v $(pwd)/.empirica:/data/.empirica empirica:1.0.0-beta bootstrap --ai-id docker-agent
```

**Publishing to Docker Hub:**
```bash
docker tag empirica:1.0.0-beta soulentheo/empirica:1.0.0-beta
docker tag empirica:1.0.0-beta soulentheo/empirica:latest
docker push soulentheo/empirica:1.0.0-beta
docker push soulentheo/empirica:latest
```

**Docker Compose Usage:**
```bash
# Start MCP server
docker-compose up -d mcp-server

# Run CLI commands
docker-compose run cli bootstrap --ai-id myagent
```

---

## 🔧 Manual Build Process

### Phase 0: PyPI Foundation

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build package
pip install --upgrade build twine
python -m build

# Verify
twine check dist/*
ls -lh dist/

# Test installation
python -m venv test_venv
test_venv/bin/pip install dist/*.whl
test_venv/bin/empirica --help
```

### Phase 1a: Homebrew

```bash
# Update SHA256 in formula
SHA256=$(sha256sum dist/*.tar.gz | cut -d' ' -f1)
sed -i "s/sha256 \".*\"/sha256 \"$SHA256\"/" packaging/homebrew/empirica.rb

# Generate complete formula with dependencies
python3 scripts/generate_homebrew_formula.py
```

### Phase 1b: Chocolatey

```bash
# Update SHA256 in install script
SHA256=$(sha256sum dist/*.tar.gz | cut -d' ' -f1)
sed -i "s/\$checksum = '.*'/\$checksum = '$SHA256'/" packaging/chocolatey/tools/chocolateyinstall.ps1
```

### Phase 3: Docker

```bash
# Build image
docker build -t empirica:1.0.0-beta .

# Test
docker run --rm empirica:1.0.0-beta bootstrap --help

# Verify system prompts included
docker run --rm --entrypoint ls empirica:1.0.0-beta -la /app/docs/
```

---

## 📋 Pre-Release Checklist

### Testing
- [ ] Package builds without errors: `python -m build`
- [ ] Package passes validation: `twine check dist/*`
- [ ] Clean install works: Test in fresh virtualenv
- [ ] CLI commands work: `empirica bootstrap --help`
- [ ] All imports succeed: Test modality_switcher import
- [ ] Docker image builds: `docker build -t empirica:test .`
- [ ] Docker container runs: `docker run empirica:test --help`

### Documentation
- [ ] README.md updated with new version
- [ ] CHANGELOG.md includes release notes
- [ ] Installation instructions verified
- [ ] System prompts included: Check /app/docs/ in Docker

### Package Contents
- [ ] Package size reasonable: Should be ~500-600KB wheel
- [ ] No dev files included: Check for empirica-dev/, tests/, website/
- [ ] System prompts included: docs/system-prompts/CANONICAL_SYSTEM_PROMPT.md
- [ ] SKILL.md included: docs/skills/SKILL.md
- [ ] Config files included: empirica/config/*.yaml
- [ ] All plugins included: Check modality_switcher in wheel

### SHA256 Hashes
- [ ] Homebrew formula SHA256 updated
- [ ] Chocolatey install script SHA256 updated
- [ ] Docker builds with correct wheel

---

## 🐛 Known Issues & Fixes

### Issue: modality_switcher Module Not Found

**Symptom:**
```python
ModuleNotFoundError: No module named 'empirica.plugins.modality_switcher'
```

**Cause:** MANIFEST.in was excluding the module with `prune empirica/plugins/modality_switcher`

**Fix:** Removed the prune line from MANIFEST.in (line 49)

**Verification:**
```bash
unzip -l dist/*.whl | grep modality_switcher
# Should show multiple files in empirica/plugins/modality_switcher/
```

---

## 📊 Package Statistics

- **Wheel Size:** ~556KB
- **Source Distribution:** ~556KB
- **Docker Image:** ~478MB (includes Python 3.11 + dependencies)
- **Files in Package:** ~361 files
- **Dependencies:** 12+ core packages (see requirements.txt)

---

## 🔗 Resources

- **PyPI:** https://pypi.org/project/empirica/
- **TestPyPI:** https://test.pypi.org/project/empirica/
- **Docker Hub:** (to be published)
- **Homebrew Tap:** (to be created)
- **Chocolatey:** (to be published)

---

## 🤝 Contributing to Distribution

To improve the distribution pipeline:

1. Test on your platform
2. Report issues in GitHub Issues
3. Submit PRs for platform-specific fixes
4. Update documentation

---

## 📝 Version History

### 1.0.0-beta (Current)
- Initial release
- PyPI, Homebrew, Chocolatey, Docker support
- System prompts and SKILL.md included
- Fixed modality_switcher packaging bug

---

**Last Updated:** 2025-12-03
