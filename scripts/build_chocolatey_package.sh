#!/bin/bash
# Build Chocolatey package (can run on Linux, but needs choco on Windows to test)
# Usage: ./scripts/build_chocolatey_package.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CHOCO_DIR="$PROJECT_ROOT/packaging/chocolatey"

cd "$PROJECT_ROOT"

echo "🍫 Building Chocolatey Package for Empirica"
echo "==========================================="

# Verify files exist
if [ ! -f "$CHOCO_DIR/empirica.nuspec" ]; then
    echo "❌ Error: empirica.nuspec not found"
    exit 1
fi

if [ ! -f "$CHOCO_DIR/tools/chocolateyinstall.ps1" ]; then
    echo "❌ Error: chocolateyinstall.ps1 not found"
    exit 1
fi

# Update SHA256 in install script
echo "📝 Updating SHA256 checksum..."
TARBALL_SHA256=$(sha256sum dist/empirica-*.tar.gz | cut -d' ' -f1)
echo "   SHA256: $TARBALL_SHA256"

# Update the PowerShell script
sed -i "s/\$checksum = '[a-f0-9]*'/\$checksum = '$TARBALL_SHA256'/" "$CHOCO_DIR/tools/chocolateyinstall.ps1"

echo "✅ Chocolatey package files ready in: $CHOCO_DIR"
echo ""
echo "📦 Package structure:"
find "$CHOCO_DIR" -type f
echo ""
echo "To build and test on Windows:"
echo "  1. Copy packaging/chocolatey/ to Windows machine"
echo "  2. cd packaging/chocolatey"
echo "  3. choco pack"
echo "  4. choco install empirica -s . -y"
echo "  5. empirica --version"
echo ""
echo "To publish to Chocolatey Community:"
echo "  choco push empirica.1.0.0-beta.nupkg --source https://push.chocolatey.org/ --api-key YOUR_API_KEY"
