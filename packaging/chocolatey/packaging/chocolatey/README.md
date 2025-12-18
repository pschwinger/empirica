# Chocolatey Package for Empirica

This directory contains the Chocolatey package definition for Empirica.

## Package Contents

- `empirica.nuspec` - Package metadata and dependencies
- `tools/chocolateyinstall.ps1` - Installation script
- `tools/chocolateyuninstall.ps1` - Uninstall script

## Building the Package (Windows Only)

On a Windows machine with Chocolatey installed:

```powershell
# Navigate to this directory
cd packaging/chocolatey

# Pack the package
choco pack

# Test locally
choco install empirica -s . -y

# Verify
empirica --version
```

## Publishing to Chocolatey.org

### Prerequisites

1. Create account at https://community.chocolatey.org/
2. Get your API key from https://community.chocolatey.org/account

### Publish

```powershell
# Set API key (one time)
choco apikey -k YOUR_API_KEY -s https://push.chocolatey.org/

# Push package
choco push empirica.1.0.0.nupkg -s https://push.chocolatey.org/
```

### Verification

After moderation approval (usually 24-48 hours), users can install via:

```powershell
choco install empirica
```

## Package Updates

When releasing a new version:

1. Update version in `empirica.nuspec`
2. Update `$packageVersion` in `tools/chocolateyinstall.ps1`
3. Update `$checksum` with new SHA256 from PyPI
4. Update release notes in `empirica.nuspec`
5. Pack and push

## Links

- **PyPI Package**: https://pypi.org/project/empirica/
- **Chocolatey Docs**: https://docs.chocolatey.org/en-us/create/create-packages
- **Moderation Process**: https://docs.chocolatey.org/en-us/community-repository/moderation/

## Notes

- Package installs Empirica via pip (requires Python 3.11+)
- Users must have Python installed first (or use `choco install python`)
- SHA256 checksum ensures package integrity
