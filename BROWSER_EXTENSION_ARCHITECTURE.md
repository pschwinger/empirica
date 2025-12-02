# Empirica Browser Extension Architecture

**Goal:** A single browser extension that shows Empirica epistemic data everywhere, with 4D Cinema as the marquee feature.

---

## 🎯 Core Vision

Instead of plugins for each platform (Forgejo, GitHub, GitLab, etc.), users install **ONE extension** that:

1. **On any git platform** (Forgejo, GitHub, GitLab): Shows epistemic analysis on commits
2. **In a dashboard**: Shows 4D Cinema + learning trajectories
3. **For any AI task**: Shows epistemic state tracking in real-time
4. **Single configuration**: Just enter Dashboard API URL once

---

## 📦 Extension Components

### **Layer 1: Content Scripts** (Platform Integrations)
Run on web pages to inject epistemic data:

```
forgejo-content.js
├─ Detect commit detail pages
├─ Extract commit SHA
├─ Fetch epistemic data from Dashboard API
├─ Inject CommitInsight component
└─ Monitor for new commits

github-content.js
├─ Detect GitHub commit pages
├─ Format for GitHub UI
└─ Inject Empirica badge

gitlab-content.js
├─ Similar pattern for GitLab
└─ Use GitLab's UI components
```

### **Layer 2: Popup UI** (Quick Access)
Users click extension icon to see:

```
┌────────────────────────────┐
│  Empirica                  │
├────────────────────────────┤
│ Current Session            │
│ • AI: claude               │
│ • Confidence: 85%          │
│ • Commits: 3               │
├────────────────────────────┤
│ Recent Commits             │
│ [abc123] Initial commit    │
│ [def456] Fix auth          │
│ [ghi789] Add tests         │
├────────────────────────────┤
│ [Open Dashboard]           │
│ [Settings]                 │
└────────────────────────────┘
```

### **Layer 3: Dashboard** (Full Interface)
Dedicated page for deep analysis:

```
http://localhost:XXXX/dashboard/

┌─────────────────────────────────────────┐
│ Empirica Dashboard                      │
├──────────────┬──────────────────────────┤
│              │                          │
│  Sessions    │  4D Cinema               │
│  ├─Session1  │  ┌────────────────────┐  │
│  ├─Session2  │  │  🌌 Epistemic      │  │
│  └─Session3  │  │     Trajectories   │  │
│              │  │                    │  │
│  Learning    │  │  [Rotate/Zoom]     │  │
│  Curves      │  │                    │  │
│  ├─AI1       │  │  Personas:         │  │
│  ├─AI2       │  │  🔴 Expert         │  │
│  └─AI3       │  │  🔵 Designer       │  │
│              │  │  🟠 Engineer       │  │
│  Commits     │  │  🟣 Architect      │  │
│  └─3 tracked │  └────────────────────┘  │
│              │  Delta Calibration      │
│              │  Collapse Animation     │
└──────────────┴──────────────────────────┘
```

### **Layer 4: Background Service**
Maintains connection to Dashboard API:

```
background-service.js
├─ Websocket to Dashboard API
├─ Listen for session updates
├─ Push notifications for new commits
├─ Cache frequently accessed data
├─ Manage authentication tokens
└─ Sync settings across tabs
```

---

## 🎬 What Extension Shows (By Context)

### **On Forgejo/GitHub/GitLab Commit Pages**

Injects epistemic badge showing:
- ✅ Confidence score (85%)
- 📈 Learning delta (+5%)
- 🎯 Risk assessment (LOW)
- 📊 File confidence heatmap
- 🔒 Signature verification

### **In Extension Dashboard (New Tab)**

Shows comprehensive analytics:

#### **Tab 1: Sessions Browser**
```
Session d8e6255 (claude)
├─ Duration: 2h 14m
├─ Commits: 8
├─ Checkpoints: 5
├─ Overall confidence: 87%
├─ Phases: PREFLIGHT → INVESTIGATE → ACT → POSTFLIGHT
└─ Timeline:
   ├─ PREFLIGHT (2:00 PM): KNOW=0.75
   ├─ INVESTIGATE (2:15 PM): KNOW=0.82
   ├─ CHECK (2:45 PM): KNOW=0.89
   ├─ ACT (3:10 PM): KNOW=0.92
   └─ POSTFLIGHT (4:14 PM): KNOW=0.87
```

#### **Tab 2: 4D Cinema Viewer** ⭐ FLAGSHIP
```
Interactive 3D visualization showing:
- 4 AI personas exploring same task
- Colored ribbons = epistemic trajectories
- Time encoded in marker size
- Gold diamond = final unified output (Sentinel collapse)
- Hover: Show epistemic vectors at that point
- Play/Pause: Animate through session
- Rotate/Zoom: Explore trajectory space
```

#### **Tab 3: Learning Curves**
```
Graph showing:
- KNOW over time
- UNCERTAINTY reduction
- Other vector dimensions
- Compare multiple AIs
- Export as image
```

#### **Tab 4: File Confidence**
```
Repository file browser with:
- Each file colored by confidence
- Green: 90%+ (high confidence)
- Yellow: 70-89% (moderate)
- Orange: 50-69% (low)
- Red: <50% (not investigated)
- Click file: See which commits changed it
```

#### **Tab 5: Verification**
```
Cryptographic verification dashboard:
- Session signatures
- Checkpoint verification
- AI identity proof
- Timestamp validation
- Export verification report
```

---

## 🔌 Configuration

Single popup settings screen:

```
┌─────────────────────────────────┐
│ Empirica Settings               │
├─────────────────────────────────┤
│ Dashboard API URL               │
│ ┌─────────────────────────────┐ │
│ │ http://127.0.0.1:8000/api/v1│ │
│ └─────────────────────────────┘ │
│                                 │
│ ☑ Show on Forgejo               │
│ ☑ Show on GitHub                │
│ ☑ Show on GitLab                │
│ ☑ Auto-refresh every 30s        │
│                                 │
│ Theme: [Light] [Dark] [Auto]    │
│                                 │
│ [Test Connection]               │
│ [Clear Cache]                   │
│ [About]                         │
└─────────────────────────────────┘
```

---

## 📐 Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│          Browser Extension (Popup)                   │
│  ┌──────────────────────────────────────────────┐   │
│  │ popup.js                                     │   │
│  │ ├─ Show current session summary              │   │
│  │ ├─ List recent commits                       │   │
│  │ └─ Quick access to dashboard                 │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│     Background Service Worker                        │
│  ┌──────────────────────────────────────────────┐   │
│  │ background.js                                │   │
│  │ ├─ Maintain API connection                   │   │
│  │ ├─ Handle messaging between tabs             │   │
│  │ ├─ Cache management                          │   │
│  │ └─ Authentication/tokens                     │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
         ↙ Content Scripts    ↘ Dashboard
┌──────────────────┐    ┌──────────────────┐
│ Forgejo Content  │    │  Dashboard Page  │
├──────────────────┤    ├──────────────────┤
│ forgejo-*.js     │    │ dashboard.html   │
├──────────────────┤    ├──────────────────┤
│ Inject on        │    │ 4D Cinema        │
│ commit pages     │    │ Learning Curves  │
│                  │    │ Session Browser  │
│ CommitInsight    │    │ Verification     │
│ Badges           │    │ File Heatmap     │
└──────────────────┘    └──────────────────┘
        ↓                      ↓
        └──────────┬───────────┘
                   ↓
        ┌──────────────────────┐
        │ Dashboard API        │
        │ (http://127.0.0.1    │
        │  :8000/api/v1)       │
        └──────────────────────┘
```

---

## 🚀 Implementation Phases

### **Phase 1: MVP (Week 1)**
- ✅ Manifest v3 setup
- ✅ Popup with session summary
- ✅ Forgejo content script (CommitInsight injection)
- ✅ Settings page
- ✅ API connection testing
- **Users can:** See epistemic data on Forgejo commits

### **Phase 2: Dashboard (Week 2)**
- ✅ Dashboard HTML/CSS/JS structure
- ✅ Session browser tab
- ✅ 4D Cinema viewer integration
- ✅ Learning curves visualization
- **Users can:** View comprehensive epistemic analytics

### **Phase 3: Multi-Platform (Week 3)**
- ✅ GitHub content script
- ✅ GitLab content script
- ✅ Platform-specific styling
- **Users can:** See epistemic data on GitHub/GitLab too

### **Phase 4: Advanced (Week 4+)**
- ✅ Real-time websocket updates
- ✅ Signature verification
- ✅ Export capabilities
- ✅ Performance optimization

---

## 📊 Scope Comparison

### **With Reverse Proxy Approach:**
- Setup: Complex (nginx config)
- Visibility: Only in Forgejo
- Extensibility: Hard to add new features
- Users self-service: No

### **With Browser Extension:**
- Setup: One-click install
- Visibility: On any git platform
- Extensibility: Easy to add new features
- 4D Cinema: **Works beautifully**
- Users self-service: **Yes** ✅

---

## 💾 What Extension Needs

From your current setup:
1. **Dashboard API** (already running) ✅
2. **CommitInsight component** (already built) ✅
3. **4D Cinema HTML files** (already exist) ✅
4. **Learning curve component** (need to build)
5. **Verification badge** (already built) ✅

---

## 🎯 Why This is Better Than Any Single-Platform Plugin

| Aspect | Forgejo Plugin | GitHub App | Extension |
|--------|---|---|---|
| **Install for users** | Replace Forgejo | Grant OAuth | Click install |
| **Works on other platforms** | ❌ | ❌ | ✅ Forgejo, GitHub, GitLab, Gitea, etc. |
| **4D Cinema** | Would require Forgejo modification | Would require GitHub modification | ✅ Works perfectly |
| **Extensibility** | Limited by Forgejo | Limited by GitHub | ✅ Full control |
| **User adoption** | Hard | Medium | ✅ Easy |
| **Maintenance** | High (keep up with Forgejo) | High (keep up with GitHub) | ✅ Low |

---

## 🎨 Extension Icon & Branding

```
Extension icon: A 3D wireframe cube with trajectory lines
Colors: Deep blue background, cyan/neon accents
Badge: Shows current session confidence as number
```

---

## ✅ Decision Point

**Should we build this browser extension?**

✅ **Advantages:**
- One install, works everywhere (Forgejo, GitHub, GitLab, etc.)
- Perfect for 4D Cinema showcase
- Easy for users to install and configure
- Fully in our control
- Can be extended with new features easily
- Makes Empirica **much more visible** to broader dev community

❌ **Disadvantages:**
- Requires Manifest V3 (Chrome/Edge/Brave)
- Firefox version separate (but similar code)
- Depends on Dashboard API being available

---

**My recommendation:** YES - This is the right approach.

A browser extension transforms Empirica from a "thing that modifies Forgejo" into a **standalone epistemic analysis platform** that works with any git platform and showcases the 4D Cinema visualization beautifully.

What do you think? Should we pivot to building this extension?
