#!/bin/bash

# Empirica Outreach Project Initialization Script

echo "🚀 Initializing Empirica Outreach Project..."

cd /home/yogapad/empirical-ai/empirica-outreach

# Create initial project structure
echo "Creating project structure..."
mkdir -p .empirica/{sessions,messages,metrics,identity,personas}
touch .empirica/sessions.db

# Create project.yaml
cat > .empirica/project.yaml << 'EOF'
version: '2.0'
name: Empirica Outreach
description: Outreach materials and community engagement for the Empirica project
beads:
  default_enabled: true
subjects: {}
auto_detect:
  enabled: true
  method: path_match
project_id: null
EOF

# Create outreach directories
mkdir -p {reddit,hackernews,devto,discord,twitter,github,linkedin,newsletter}

# Initialize git
git init -q
git branch -m main

# Create README
cat > README.md << 'EOF'
# Empirica Outreach

Community engagement and outreach materials for the Empirica project.

## Structure

- `reddit/` - Reddit post templates and engagement
- `hackernews/` - Hacker News submissions
- `devto/` - Dev.to articles
- `discord/` - Discord community management
- `twitter/` - Twitter/X posts
- `github/` - GitHub discussions and issues
- `linkedin/` - LinkedIn posts
- `newsletter/` - Newsletter content

## Tracking

All outreach activities are tracked using Empirica's epistemic framework.

## Setup

```bash
empirica project-init
empirica project-bootstrap
```
EOF

# Create initial gitignore
cat > .gitignore << 'EOF'
# Empirica
.empirica/sessions.db
.empirica/messages/
.empirica/metrics/
.empirica/identity/
.empirica/personas/

# General
.DS_Store
*.log
*.swp
*.swo
EOF

echo "✅ Project structure created"
echo "📋 Run these commands to complete setup:"
echo "  cd /home/yogapad/empirical-ai/empirica-outreach"
echo "  empirica project-init"
echo "  empirica project-bootstrap"
