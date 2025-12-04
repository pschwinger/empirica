#!/bin/bash
# PyPI Publishing Automation Script
# Usage: ./scripts/publish_to_pypi.sh [test|prod]
#
# Requirements:
# - PyPI credentials in ~/.pypirc or TWINE_USERNAME/TWINE_PASSWORD env vars
# - For test: TestPyPI account
# - For prod: PyPI account with access to 'empirica' package

set -e

MODE="${1:-test}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "🚀 Empirica PyPI Publishing Script"
echo "Mode: $MODE"
echo "=================================="

# Clean old builds
echo "🧹 Cleaning old build artifacts..."
python3 "$SCRIPT_DIR/safe_delete.py" --force dist build empirica.egg-info 2>/dev/null || true

# Install/upgrade build tools
echo "📦 Installing build tools..."
pip install --upgrade build twine

# Build package
echo "🔨 Building package..."
python -m build

# Verify package
echo "✅ Verifying package..."
twine check dist/*

# Show package info
echo ""
echo "📊 Package Details:"
ls -lh dist/
echo ""
tar -tzf dist/*.tar.gz | wc -l | xargs echo "Files in tarball:"
du -h dist/*.tar.gz | cut -f1 | xargs echo "Tarball size:"
echo ""

# Test installation in clean venv
echo "🧪 Testing installation in clean venv..."
TEST_VENV="/tmp/test_empirica_$(date +%s)"
python3 -m venv "$TEST_VENV"
"$TEST_VENV/bin/pip" install --quiet dist/*.whl
"$TEST_VENV/bin/empirica" --version
echo "✅ Test installation successful"
rm -rf "$TEST_VENV"

# Upload
if [ "$MODE" = "test" ]; then
    echo ""
    echo "📤 Uploading to TestPyPI..."
    echo "TestPyPI URL: https://test.pypi.org/project/empirica/"
    twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Upload complete!"
    echo "Test install with:"
    echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ empirica"
elif [ "$MODE" = "prod" ]; then
    echo ""
    echo "⚠️  WARNING: About to upload to PRODUCTION PyPI"
    echo "This will make the package publicly available."
    read -p "Continue? (yes/no): " -r
    if [[ $REPLY != "yes" ]]; then
        echo "Upload cancelled."
        exit 0
    fi
    echo "📤 Uploading to PyPI..."
    twine upload dist/*
    echo ""
    echo "✅ Upload complete!"
    echo "PyPI URL: https://pypi.org/project/empirica/"
    echo "Install with: pip install empirica"
else
    echo "❌ Invalid mode: $MODE"
    echo "Usage: $0 [test|prod]"
    exit 1
fi
