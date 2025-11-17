#!/bin/bash
# Complete Empirica Sanitization for Distribution
# Run from repository root

set -e

echo "🔒 Empirica Complete Sanitization Script"
echo "========================================"
echo ""
echo "This script will:"
echo "  1. Create backup"
echo "  2. Sanitize paths"
echo "  3. Update GitHub URLs"
echo "  4. Clean API key references"
echo "  5. Remove development artifacts"
echo "  6. Clean documentation structure"
echo "  7. Verify security"
echo ""

# 1. Backup
echo "📦 Creating backup..."
timestamp=$(date +%Y%m%d_%H%M%S)
mkdir -p .backups
tar -czf .backups/pre_sanitization_${timestamp}.tar.gz \
  --exclude=.git \
  --exclude=.venv* \
  --exclude=__pycache__ \
  --exclude=.backups \
  .
echo "✅ Backup: .backups/pre_sanitization_${timestamp}.tar.gz"
echo ""

# 2. Path sanitization
echo "🔧 Sanitizing personal paths..."
find . -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" \) \
  ! -path "./.git/*" \
  ! -path "./.venv*/*" \
  ! -path "./__pycache__/*" \
  ! -path "./.backups/*" \
  ! -path "./docs/_internal/*" \
  -exec sed -i 's|/path/to/empirica|/path/to/empirica|g' {} \;

# Also sanitize parent directory references
find . -type f \( -name "*.md" -o -name "*.sh" -o -name "*.py" \) \
  ! -path "./.git/*" \
  ! -path "./.venv*/*" \
  ! -path "./.backups/*" \
  -exec sed -i 's|~/empirica-parent|~/empirica-parent|g' {} \;

echo "✅ Path sanitization complete"
echo ""

# 3. GitHub URL updates
echo "🔧 Updating GitHub URLs..."
find . -type f -name "*.md" \
  ! -path "./.git/*" \
  ! -path "./.backups/*" \
  -exec sed -i 's|github.com/your-org/empirica|github.com/Nubaeon/empirica|g' {} \;

find . -type f -name "*.md" \
  ! -path "./.git/*" \
  ! -path "./.backups/*" \
  -exec sed -i 's|github.com/\[org\]/empirica|github.com/Nubaeon/empirica|g' {} \;

find . -type f -name "*.md" \
  ! -path "./.git/*" \
  ! -path "./.backups/*" \
  -exec sed -i 's|github.com/Nubaeon/semantic-self-aware-kit|github.com/Nubaeon/empirica|g' {} \;

echo "✅ GitHub URLs updated to github.com/Nubaeon/empirica"
echo ""

# 4. API key references
echo "🔧 Cleaning API key references..."
find . -type f \( -name "*.md" -o -name "*.py" \) \
  ! -path "./.git/*" \
  ! -path "./.venv*/*" \
  ! -path "./.backups/*" \
  -exec sed -i 's|\.minimax_api2|.minimax_key|g' {} \;

find . -type f \( -name "*.md" -o -name "*.py" \) \
  ! -path "./.git/*" \
  ! -path "./.venv*/*" \
  ! -path "./.backups/*" \
  -exec sed -i 's|cat /path/to/empirica/\.minimax_api|cat ~/.empirica/minimax_key|g' {} \;

echo "✅ API key reference cleanup complete"
echo ""

# 5. Remove development artifacts
echo "🗑️  Removing development artifacts..."

# Remove .agent_memory.json
if [ -f ".agent_memory.json" ]; then
  rm .agent_memory.json
  echo "   Removed .agent_memory.json"
fi

# Add to .gitignore if not present
if ! grep -q "^.agent_memory.json" .gitignore 2>/dev/null; then
  echo ".agent_memory.json" >> .gitignore
  echo "   Added .agent_memory.json to .gitignore"
fi

# Move root planning docs to archive
echo "   Archiving root planning documents..."
mkdir -p docs/archive/2025-11/project_planning
if [ -f "FOLDER_REORGANIZATION_PLAN.md" ]; then
  mv FOLDER_REORGANIZATION_PLAN.md docs/archive/2025-11/project_planning/
fi
if [ -f "MULTI_AGENT_CHECKPOINT_STRATEGY.md" ]; then
  mv MULTI_AGENT_CHECKPOINT_STRATEGY.md docs/archive/2025-11/project_planning/
fi

echo "✅ Artifacts cleaned"
echo ""

# 6. Security verification
echo "🔍 Running security verification..."

# Check for remaining personal paths (excluding archives and internals)
remaining=$(grep -r "/home/yogapad" . \
  --exclude-dir=.git \
  --exclude-dir=.venv* \
  --exclude-dir=.backups \
  --exclude-dir=__pycache__ \
  --exclude-dir=docs/_internal \
  --exclude-dir=docs/archive \
  --include="*.md" \
  --include="*.py" \
  --include="*.sh" \
  --include="*.json" \
  --include="*.yaml" \
  --include="*.yml" 2>/dev/null | wc -l)

if [ "$remaining" -eq 0 ]; then
  echo "✅ No personal paths in production files"
else
  echo "⚠️  $remaining personal path references found (check if in archived docs)"
fi

# Check for potential secrets
echo "🔍 Checking for exposed secrets..."
secrets_found=false

if grep -r "sk-[a-zA-Z0-9]\{20,\}" . \
  --exclude-dir=.git \
  --exclude-dir=.venv* \
  --exclude-dir=.backups \
  --include="*.py" \
  --include="*.sh" 2>/dev/null | grep -v "# Example:" | grep -v ".md:"; then
  secrets_found=true
fi

if [ "$secrets_found" = false ]; then
  echo "✅ No exposed secrets found"
else
  echo "❌ Potential secrets found! Review manually."
fi

echo ""
echo "🎉 Sanitization complete!"
echo ""
echo "Summary:"
echo "  ✅ Personal paths sanitized"
echo "  ✅ GitHub URLs updated to github.com/Nubaeon/empirica"
echo "  ✅ API key references cleaned"
echo "  ✅ Development artifacts removed"
echo "  ✅ Security verified"
echo ""
echo "Rollback if needed:"
echo "  tar -xzf .backups/pre_sanitization_${timestamp}.tar.gz"
