# Empirica Epistemic Insight Plugin for Forgejo

🔍 **See AI confidence, learning, and verification on every commit**

The Empirica Epistemic Insight Plugin brings transparent AI reasoning to Forgejo. See confidence scores, learning deltas, and cryptographic verification badges directly on commits and pull requests.

## Features

### 📊 Commit Insight
When viewing a commit, see:
- **Confidence Badge** - AI's overall confidence (KNOW/DO scores)
- **Learning Delta** - How much the AI learned during the session
- **File Confidence** - Confidence score for each file changed
- **Risk Assessment** - What was investigated vs. not investigated
- **Signature Verification** - Crypto-signed proof of epistemic state

### 🔐 Cryptographic Verification
- Ed25519 signatures on AI reasoning chains
- Verify that epistemic analysis wasn't tampered
- See which AI system performed the analysis
- Timestamp and public key information

### 📈 Team Dashboards
- View AI learning curves over time
- Compare multiple AIs' performance
- Track epistemic improvements across projects
- Identify areas of uncertainty

### 🎨 File Confidence Heatmaps
- Color-coded confidence levels on file diffs
- Green (90%+): High confidence
- Yellow (70-89%): Moderate confidence
- Orange (50-69%): Low confidence
- Red (<50%): Not investigated

## Installation

### Prerequisites
- Forgejo 2.0.0 or later
- Node.js 18.0.0 or later
- Empirica Dashboard API running (http://localhost:8000/api/v1 by default)

### Setup

1. **Clone the plugin**
```bash
cd /path/to/forgejo/plugins
git clone https://github.com/Nubaeon/empirica.git empirica-epistemic
cd empirica-epistemic/forgejo-plugin-empirica
```

2. **Install dependencies**
```bash
npm install
```

3. **Build the plugin**
```bash
npm run build
```

4. **Configure in Forgejo**

Edit `/path/to/forgejo/app.ini`:
```ini
[plugins]
; Enable plugins
ENABLED = true

; Add plugin location
PLUGIN_PATH = /path/to/forgejo/plugins

; Empirica Dashboard API endpoint
EMPIRICA_API_URL = http://localhost:8000/api/v1
```

5. **Restart Forgejo**
```bash
systemctl restart forgejo
```

## Configuration

### Environment Variables

Set these before starting Forgejo or in `app.ini`:

```bash
# Dashboard API URL
EMPIRICA_API_URL=http://localhost:8000/api/v1

# Verify crypto signatures
EMPIRICA_VERIFY_SIGNATURES=true

# Minimum confidence to highlight (0-1)
EMPIRICA_CONFIDENCE_THRESHOLD=0.75

# Show file confidence heatmaps
EMPIRICA_SHOW_HEATMAP=true

# Auto-refresh interval (seconds, 0 = disabled)
EMPIRICA_AUTO_REFRESH=30
```

### Plugin Settings

In Forgejo's admin UI under "Plugins" → "Empirica Epistemic Insight":

- **API URL** - Dashboard API endpoint
- **Verify Signatures** - Require signature verification
- **Confidence Threshold** - Minimum confidence to highlight
- **Show Heatmap** - Display file confidence visualization
- **Auto-Refresh Interval** - How often to refresh data

## Usage

### On Commit Pages

When viewing a commit that was made by an Empirica-tracked AI system:

1. Scroll to the commit details section
2. Look for the "📊 Epistemic Analysis" section
3. See confidence badge and learning delta
4. Check what areas were investigated
5. Verify the cryptographic signature

### On Pull Requests

1. View the PR changes
2. Each commit shows epistemic context
3. Files are color-coded by confidence
4. Hover over files to see detailed confidence metrics

### In Repository Dashboard

1. Go to the repository dashboard
2. Click "Learning Curves" tab
3. See AI learning trajectories
4. Compare multiple AIs' performance
5. Track epistemic improvements over time

## API Integration

The plugin communicates with the Empirica Dashboard API:

**Base Endpoint**: `http://localhost:8000/api/v1`

**Key Endpoints**:
- `GET /commits/{sha}/epistemic` - Get epistemic data for a commit
- `GET /files/{path}/uncertainty` - Get file confidence
- `GET /sessions/{id}/deltas` - Get learning deltas
- `GET /checkpoints/{id}/{phase}/{round}/verify` - Verify signatures

See [Dashboard API Specification](../docs/production/31_DASHBOARD_API_SPECIFICATION.md) for complete documentation.

## Development

### Project Structure

```
forgejo-plugin-empirica/
├── src/
│   ├── api/
│   │   └── empirica-client.ts      # API client
│   ├── components/
│   │   ├── CommitInsight.tsx       # Main commit analysis
│   │   ├── ConfidenceBadge.tsx     # Confidence visualization
│   │   ├── LearningDelta.tsx       # Learning progress
│   │   └── VerificationBadge.tsx   # Signature verification
│   ├── styles/
│   │   ├── badges.css             # Badge styling
│   │   ├── commit-insight.css      # Commit insight styling
│   │   └── learning-delta.css      # Learning delta styling
│   └── index.ts                    # Entry point
├── tests/
│   └── plugin.test.ts             # Tests
├── manifest.json                  # Plugin manifest
├── package.json                   # Dependencies
└── README.md                       # This file
```

### Commands

```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Type check
npm run type-check

# Lint code
npm run lint
```

### Testing

Write tests in `tests/` directory:

```typescript
import { describe, it, expect } from 'vitest';
import { CommitInsight } from '../src/components/CommitInsight';

describe('CommitInsight', () => {
  it('renders confidence badge', () => {
    // Test implementation
  });
});
```

## Troubleshooting

### Plugin not loading
- Check Forgejo logs: `journalctl -u forgejo -f`
- Verify plugin is in correct directory
- Ensure `PLUGIN_PATH` is set correctly in config
- Rebuild plugin: `npm run build`

### "API unavailable" error
- Check Dashboard API is running: `curl http://localhost:8000/health`
- Verify `EMPIRICA_API_URL` is correct
- Check firewall allows connection
- Review Dashboard API logs

### No epistemic data showing
- Commit must be made by Empirica-tracked AI system
- Check if Dashboard API has epistemic data for commit SHA
- Verify session exists in Dashboard API
- Review browser console for errors

### Signature verification failing
- Check crypto identity is set up: `empirica list-identities`
- Verify checkpoint has been signed
- Check public key is accessible
- Review verification logs

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Submit a pull request

## License

MIT - See LICENSE file for details

## Related Documentation

- [Dashboard API Specification](../docs/production/31_DASHBOARD_API_SPECIFICATION.md)
- [Forgejo Plugin Architecture](../docs/production/32_FORGEJO_PLUGIN_ARCHITECTURE.md)
- [Empirica Overview](../README.md)

## Support

- **Issues**: [GitHub Issues](https://github.com/Nubaeon/empirica/issues)
- **Documentation**: [Empirica Docs](../docs/)
- **API Docs**: [Dashboard API](../docs/production/31_DASHBOARD_API_SPECIFICATION.md)

---

**Making AI reasoning transparent and verifiable, one commit at a time.** ✨
