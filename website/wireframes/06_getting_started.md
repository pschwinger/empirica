# Getting Started Page Wireframe

## Page: /getting-started.html

### Purpose
Guide users through their first experience with Empirica, with links to key resources.

---

## Content Structure

### Hero Section
**Headline:** Get Started with Empirica  
**Subheadline:** Choose your integration path and start building epistemically-aware AI systems in minutes.

---

### Section 1: Choose Your Path

**Four Integration Options:**

#### 1. Empirica Skills (Fastest)
**For:** AI assistants (Claude, Copilot, etc.)  
**Time:** 5 minutes  
**How:** Configure MCP server, use pre-built skills  
**Link:** [Skills Documentation](/docs/empirica_skills/)

#### 2. Empirica CLI  
**For:** Command-line workflows  
**Time:** 10 minutes  
**How:** Install CLI, run bootstrap, analyze sessions  
**Link:** [CLI Guide](/docs/cli-guide.html)

#### 3. Bootstrap Integration
**For:** Python projects  
**Time:** 15 minutes  
**How:** Import bootstrap, initialize session tracking  
**Link:** [Bootstrap Guide](/docs/bootstrap-guide.html)

#### 4. MCP Server (Custom)
**For:** Custom AI tools and integrations  
**Time:** 20 minutes  
**How:** Run MCP server, connect your tools  
**Link:** [MCP Integration](/docs/12_MCP_INTEGRATION.md)

---

### Section 2: Quick Start - Skills (Recommended)

**Step 1: Install Empirica**
```bash
pip install empirica
```

**Step 2: Configure MCP Server**
Add to your AI tool's MCP configuration:
```json
{
  "mcpServers": {
    "empirica": {
      "command": "python",
      "args": ["-m", "empirica.empirica_mcp_server"]
    }
  }
}
```

**Step 3: Use Skills**
Your AI assistant now has access to:
- `empirica.assess` - Evaluate epistemic state
- `empirica.investigate` - Trigger cascade analysis
- `empirica.validate` - Post-flight verification

**Example:**
```
User: "Can you build me a complex e-commerce site?"
AI: [Uses empirica.assess skill]
AI: "I've detected high novelty and complexity. Let me investigate systematically..."
AI: [Uses empirica.investigate skill]
AI: [Provides phased approach based on investigation]
```

**Link:** [Complete Skills Guide](/docs/empirica_skills/)

---

### Section 3: Quick Start - CLI

**Step 1: Install**
```bash
pip install empirica
```

**Step 2: Run Bootstrap**
```bash
python -m empirica.bootstraps.optimal_metacognitive_bootstrap
```

**Step 3: Analyze Sessions**
```bash
empirica-cli sessions list
empirica-cli sessions show <session-id>
empirica-cli investigate --session <session-id>
```

**Link:** [CLI Documentation](/docs/cli-guide.html)

---

### Section 4: Quick Start - Bootstrap

**Step 1: Install**
```bash
pip install empirica
```

**Step 2: Initialize in Your Code**
```python
from empirica import bootstrap_empirica

# Start session with epistemic tracking
session = bootstrap_empirica(
    session_name="my_ai_task",
    enable_cascade=True
)

# Your AI code here...
# Empirica tracks epistemic state automatically

# End session
session.end()
```

**Step 3: Review Sessions**
Sessions are stored in `.empirica/` directory with full epistemic tracking.

**Link:** [Bootstrap Guide](/docs/bootstrap-guide.html)

---

### Section 5: Quick Start - MCP Server

**Step 1: Install**
```bash
pip install empirica
```

**Step 2: Start Server**
```bash
python -m empirica.empirica_mcp_server
```

**Step 3: Connect Your Tool**
Configure your AI tool to use the MCP server endpoint.

**Step 4: Available Tools**
- Epistemic assessment
- Cascade investigation
- Session management
- Drift monitoring

**Link:** [MCP Integration Guide](/docs/12_MCP_INTEGRATION.md)

---

### Section 6: What's Next?

**After Getting Started:**

#### Learn Core Concepts
- [Epistemic Awareness](/epistemic-awareness.html)
- [The 13 Vectors](/docs/05_EPISTEMIC_VECTORS.md)
- [Cascade System](/docs/06_CASCADE_FLOW.md)

#### Explore Components
- [Investigation System](/docs/07_INVESTIGATION_SYSTEM.md)
- [Bayesian Guardian](/docs/08_BAYESIAN_GUARDIAN.md)
- [Drift Monitor](/docs/09_DRIFT_MONITOR.md)

#### Build Something
- Try the example workflows
- Integrate with your project
- Customize for your domain

#### Join Community
- GitHub Discussions
- Share your use case
- Contribute improvements

---

### Section 7: Need Help?

**Resources:**
- [Complete Documentation](/docs.html)
- [API Reference](/api.html)
- [Troubleshooting](/docs/21_TROUBLESHOOTING.md)
- [FAQ](/docs/22_FAQ.md)
- [Contact Us](/contact.html)

**Common Issues:**
- Installation problems → [Troubleshooting](/docs/21_TROUBLESHOOTING.md)
- Configuration questions → [Configuration Guide](/docs/15_CONFIGURATION.md)
- Integration help → [GitHub Discussions](link)

---

### Call-to-Action
- Start with Skills (easiest)
- Read Full Documentation
- Join GitHub Community
