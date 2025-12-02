# Forgejo Plugin Architecture & Implementation Guide

**Status**: Ready for Plugin Development
**Date**: 2025-12-02
**Foundation**: Dashboard API (Phase 3.3) Complete
**Next**: Build plugin UI and integrate with Forgejo

---

## Executive Summary

The **Empirica Forgejo Plugin** is the visualization and verification layer for Empirica's epistemic reasoning framework. It surfaces crypto-signed learning deltas, git-epistemic correlations, and confidence heatmaps directly within the Forgejo/GitHub interface.

### What Users See

```
┌─────────────────────────────────────────────┐
│ Commit Details: f13d167                     │
├─────────────────────────────────────────────┤
│ Message: feat: improve auth module          │
│ Author: Claude Copilot                      │
│                                              │
│ 📊 EPISTEMIC ANALYSIS                        │
│ ─────────────────────────────────────────  │
│ Confidence: 85% (know: 0.85, do: 0.95)     │
│ ✅ Signature Verified by claude              │
│                                              │
│ Learning Delta:                              │
│ • KNOW: 60% → 85% (+25%) 📈                │
│ • DO:   70% → 95% (+25%) 📈                │
│                                              │
│ Files Changed:                               │
│ ✨ auth.py (+50 lines)        Confidence: 90% │
│ ✨ tests.py (+120 lines)      Confidence: 85% │
│                                              │
│ Risk Assessment: LOW                         │
│ Investigated: [jwt_refresh, session_hijack]  │
│ Not Investigated: [distributed_consensus]    │
└─────────────────────────────────────────────┘
```

---

## Plugin Architecture

### Three-Layer Integration

**Layer 1: Dashboard API** (Phase 3.3 ✅)
- FastAPI/Flask REST endpoints
- Query epistemic state, deltas, verification
- Live git-epistemic correlation

**Layer 2: Plugin UI** (This Phase)
- Forgejo web interface hooks
- React/Vue components for visualizations
- Real-time updates via API polling

**Layer 3: Integration Points**
- Commit detail page enhancement
- PR review with epistemic context
- File/module confidence heatmaps
- Team learning dashboards

### Data Flow

```
Empirica Session
  ↓
Git State Capture (Phase 2.5) ✅
  ├─ Commits made
  ├─ Files changed
  └─ Epistemic vectors (KNOW, DO, etc.)
  ↓
Dashboard API (Phase 3.3) ✅
  ├─ /sessions/{id}/deltas
  ├─ /commits/{sha}/epistemic
  ├─ /sessions/{id}/signatures
  └─ /files/{path}/uncertainty
  ↓
Forgejo Plugin (THIS PHASE)
  ├─ Fetch from API
  ├─ Render visualizations
  ├─ Verify signatures
  └─ Display on UI
  ↓
User sees: Crypto-verified, confidence-aware commits
```

---

## Implementation Plan

### Phase 1: Plugin Skeleton & Manifest (4 hours)

**Create plugin structure:**
```
forgejo-plugin-empirica/
├── manifest.json              # Plugin metadata
├── src/
│   ├── components/            # React/Vue components
│   │   ├── CommitInsight.tsx
│   │   ├── ConfidenceHeatmap.tsx
│   │   ├── LearningDelta.tsx
│   │   ├── VerificationBadge.tsx
│   │   └── TeamDashboard.tsx
│   ├── api/
│   │   └── empirica-client.ts # API wrapper
│   ├── styles/
│   │   └── epistemic.css
│   └── index.ts              # Entry point
├── tests/
│   └── plugin.test.ts
├── package.json
└── README.md
```

**manifest.json example:**
```json
{
  "id": "empirica-epistemic-insight",
  "name": "Empirica Epistemic Insight",
  "version": "1.0.0",
  "description": "Crypto-verified epistemic analysis for Forgejo commits",
  "author": "Empirica Contributors",
  "dashboardUrl": "/empirica-dashboard",
  "hooks": {
    "commit-detail": "CommitInsight",
    "pull-request": "PREpistemicReview",
    "repo-dashboard": "TeamEpistemicDashboard"
  },
  "settings": {
    "apiUrl": {
      "type": "string",
      "description": "Dashboard API endpoint",
      "default": "http://localhost:8000/api/v1"
    },
    "verifySignatures": {
      "type": "boolean",
      "description": "Require signature verification",
      "default": true
    }
  }
}
```

### Phase 2: Core Components (6 hours)

#### CommitInsight Component
Shows epistemic context when viewing a commit:

```typescript
// Shows:
// - Confidence badge with KNOW/DO scores
// - Learning delta (PREFLIGHT → POSTFLIGHT)
// - Files changed with confidence per-file
// - Signature verification status
```

#### ConfidenceHeatmap Component
Visualizes uncertainty across files:

```typescript
// Color coding:
// - Green (0.9+): High confidence
// - Yellow (0.7-0.89): Moderate confidence
// - Orange (0.5-0.69): Low confidence
// - Red (<0.5): Not investigated
```

#### VerificationBadge Component
Shows crypto signature status:

```typescript
// Shows:
// - ✅ Verified by [AI ID] (if signed)
// - ⏳ Pending verification (if unsigned)
// - ❌ Verification failed (if tampered)
// - Signature date and public key link
```

#### LearningDelta Component
Displays epistemic changes:

```typescript
// Shows timeline:
// PREFLIGHT → CHECK (optional) → POSTFLIGHT
// Delta bars for each vector
// Learning velocity (change/minute)
```

### Phase 3: Integration & Testing (4 hours)

**Forgejo hooks to implement:**
1. `commit-view:after-header` - Show CommitInsight
2. `pull-request:review-section` - Add epistemic review
3. `repo-dashboard:main` - Add team learning dashboard
4. `file-tree:file-item` - Add confidence indicators

**Test scenarios:**
- API connectivity
- Signature verification
- Missing data handling
- Real-time updates
- Cross-browser compatibility

---

## API Integration Guide

### Client Wrapper

```typescript
// src/api/empirica-client.ts
class EmpericaClient {
  constructor(baseUrl: string) {}

  async getSessionDeltas(sessionId: string) {
    // GET /sessions/{sessionId}/deltas
  }

  async getCommitEpistemic(sha: string) {
    // GET /commits/{sha}/epistemic
  }

  async verifyCheckpoint(sessionId: string, phase: string, round: number) {
    // GET /checkpoints/{sessionId}/{phase}/{round}/verify
  }

  async getFileUncertainty(filepath: string) {
    // GET /files/{filepath}/uncertainty
  }

  async getAILearningCurve(aiId: string) {
    // GET /ai/{aiId}/learning-curve
  }
}
```

### Usage Example

```typescript
// In CommitInsight component
const client = new EmpericaClient(config.apiUrl);

// Get epistemic context for this commit
const epistemic = await client.getCommitEpistemic(commitSha);

// Display confidence with color coding
renderConfidenceBadge(epistemic.epistemic_context.know);

// Show what was investigated
renderInvestigatedAreas(epistemic.epistemic_context.investigated);
```

---

## Key Features to Implement

### 1. Confidence Badges
```
Display on commits:
├─ Overall confidence (0-100%)
├─ KNOW score (what AI understood)
├─ DO score (execution confidence)
└─ Uncertainty reduction (how much learned)
```

### 2. File Heatmaps
```
On file diffs:
├─ Background color by confidence
├─ Hover to see epistemic details
├─ Aggregated confidence per file
└─ Risk assessment per section
```

### 3. Signature Verification
```
Verification badge showing:
├─ Signer identity (which AI)
├─ Signature date
├─ Public key (link to identity)
├─ Verification status (✅/❌)
└─ Option to verify manually
```

### 4. Learning Curve Dashboard
```
Team dashboard with:
├─ Learning trajectories per AI
├─ Average confidence over time
├─ Learning velocity metrics
├─ Multi-AI comparison
└─ Risk/uncertainty trends
```

### 5. PR Epistemic Review
```
Enhanced PR review with:
├─ Overall learning delta
├─ Confidence by reviewer (AI)
├─ Risk assessment
├─ Untested areas warning
└─ Merge gate based on uncertainty threshold
```

---

## Configuration & Deployment

### Environment Variables

```bash
# Empirica Dashboard API
EMPIRICA_API_URL=http://localhost:8000/api/v1

# Plugin settings
PLUGIN_VERIFY_SIGNATURES=true
PLUGIN_CONFIDENCE_THRESHOLD=0.7
PLUGIN_REFRESH_INTERVAL=30000  # milliseconds
```

### Installation in Forgejo

```bash
# Clone plugin
git clone https://github.com/empirica/forgejo-plugin-epistemic.git

# Install to Forgejo plugins directory
cp -r forgejo-plugin-epistemic /path/to/forgejo/plugins/

# Restart Forgejo
systemctl restart forgejo
```

### Docker Integration

```dockerfile
FROM forgejo:latest
COPY forgejo-plugin-epistemic /app/plugins/empirica-epistemic
ENV EMPIRICA_API_URL=http://api:8000/api/v1
```

---

## Testing Strategy

### Unit Tests

```typescript
// Test confidence score calculation
test('renders confidence badge with correct color', () => {
  const { getByText } = render(
    <ConfidenceBadge score={0.85} />
  );
  expect(getByText('85%')).toHaveClass('confidence-high');
});

// Test API client
test('fetches commit epistemic data', async () => {
  const client = new EmpericaClient('http://localhost:8000/api/v1');
  const result = await client.getCommitEpistemic('abc123');
  expect(result.ok).toBe(true);
});
```

### Integration Tests

```typescript
// Test Forgejo hook integration
test('CommitInsight renders on commit page', () => {
  // Simulate Forgejo hook firing
  // Verify CommitInsight component loads
  // Verify API call succeeds
  // Verify data displays correctly
});
```

### E2E Tests

```typescript
// Test full workflow
test('User sees confidence heatmap on file diff', async () => {
  // Navigate to commit page
  // Wait for CommitInsight to load
  // Check that files show confidence colors
  // Hover on file to see details
  // Click signature badge to verify
});
```

---

## Success Criteria

- ✅ Dashboard API fully functional (Phase 3.3 COMPLETE)
- ✅ Plugin loads without errors in Forgejo
- ✅ Commits show epistemic confidence badges
- ✅ Files display uncertainty heatmaps
- ✅ Signatures verify correctly
- ✅ PRs can be gated by epistemic criteria
- ✅ Team dashboard shows learning trajectories
- ✅ All tests passing
- ✅ Documentation complete

---

## Timeline

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| 3.3 | Dashboard API | 8 hours | ✅ DONE |
| 4.1 | Plugin Skeleton | 4 hours | 🔄 NEXT |
| 4.2 | Core Components | 6 hours | ⏳ Pending |
| 4.3 | Integration & Testing | 4 hours | ⏳ Pending |
| 4.4 | Documentation & Release | 2 hours | ⏳ Pending |
| **TOTAL** | **Forgejo Plugin** | **16 hours** | **3.3 DONE, 4.1+ NEXT** |

---

## Related Documentation

- `/docs/production/31_DASHBOARD_API_SPECIFICATION.md` - Complete API spec
- `/docs/production/ONBOARDING_GUIDE.md` - General Empirica setup
- `/docs/architecture/STORAGE_ARCHITECTURE_VISUAL_GUIDE.md` - Data storage
- `HANDOFF_EPISTEMIC_ARCHITECTURE_CRYPTO_SIGNING.md` - Previous session context

---

## Next Steps

1. **Create plugin repository** with manifest and package.json
2. **Implement CommitInsight component** - highest priority
3. **Build ConfidenceHeatmap** - key visualization
4. **Add signature verification** - security feature
5. **Create team dashboard** - aggregate insights
6. **Write comprehensive tests** - ensure reliability
7. **Deploy to Forgejo** - production ready

---

**This specification is the foundation for the Forgejo plugin.**
**All components reference the working Dashboard API (Phase 3.3).**
**Ready for component development to begin!**
