# 🧠 Empirica - Honest AI Through Genuine Self-Awareness

> AI agents that know what they know—and what they don't

[![Status](https://img.shields.io/badge/status-beta-yellow)]()
[![Version](https://img.shields.io/badge/version-1.0.0--beta-green)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![License](https://img.shields.io/badge/license-LGPL--3.0%20OR%20MIT-green)]()

## What is Empirica?

**Empirica enables AI agents to genuinely know what they know—and what they don't.**

Instead of false confidence and hallucinations, Empirica gives agents:
- **Honest uncertainty**: "I don't know" becomes a valid response
- **Focused investigation**: Spend time where knowledge is weakest
- **Genuine learning**: Track what you learned, not just what you did
- **Calibrated confidence**: Get better at knowing what you know over time

This produces AI you can trust—not because it's always right, but because **it knows when it might be wrong**.

**Learn more:** [Why Empirica?](WHY_EMPIRICA.md) | [Full Documentation](docs/production/00_COMPLETE_SUMMARY.md)

---

## 🚀 Installation

Choose your preferred method:

### PyPI (Recommended)
```bash
pip install empirica
empirica bootstrap --ai-id myagent --level extended
```

### Homebrew (macOS/Linux)
```bash
brew tap empirica/tap
brew install empirica
```

### Chocolatey (Windows)
```powershell
choco install empirica
```

### Docker
```bash
docker pull soulentheo/empirica:latest
docker run -v $(pwd)/.empirica:/data/.empirica soulentheo/empirica:latest bootstrap --ai-id myagent
```

**Advanced installation:** System prompts, MCP server, and more → [Complete Installation Guide](docs/COMPLETE_INSTALLATION_GUIDE.md)

---

## ✨ What Can Empirica Do?

### 📊 13-Vector Epistemic Assessment
Track your knowledge state across 13 dimensions:
- **Foundation**: What you KNOW, can DO, and understand about CONTEXT
- **Comprehension**: CLARITY, COHERENCE, SIGNAL quality, cognitive DENSITY
- **Execution**: Current STATE, CHANGE tracking, COMPLETION progress, downstream IMPACT
- **Meta**: Task ENGAGEMENT and overall UNCERTAINTY

**Result:** Know exactly where your knowledge gaps are.

### 🔄 CASCADE Workflow
Natural work rhythm with built-in calibration:
1. **PREFLIGHT** - Assess what you know before starting
2. **Investigate/Act** - Do the work (implicit loop)
3. **CHECK** - Pause to assess: "Am I still confident?"
4. **POSTFLIGHT** - Measure what you learned

**Result:** Measurable learning and well-calibrated predictions.

### 🗄️ Triple Storage for Session Continuity
- **Git Notes** - 97.5% token reduction (46 vs 1,821 tokens)
- **SQLite Database** - Full audit trail with queryable state
- **Handoff Reports** - 98% token reduction (~400 vs 20,000 tokens)

**Result:** Resume work across days/weeks without context loss.

### 🤝 Multi-Agent Coordination
- Create and share goals across AI agents
- Track task completion with evidence
- Transfer epistemic state efficiently
- Collaborate without duplicating work

**Result:** Multiple agents can work on the same project coherently.

### 🔗 MCP Server Integration
21 tools for Claude Desktop, VS Code extensions (Cline, Continue.dev), and more.

**Result:** Use Empirica directly from your IDE.

---

## 💡 Quick Start

```bash
# Install
pip install empirica

# Start your first session
empirica bootstrap --ai-id myagent --level extended

# View all commands
empirica --help
```

**Next steps:**
- **AI Agents**: Read [`docs/01_a_AI_AGENT_START.md`](docs/01_a_AI_AGENT_START.md) - 10-minute interactive guide
- **Developers**: See [`docs/COMPLETE_INSTALLATION_GUIDE.md`](docs/COMPLETE_INSTALLATION_GUIDE.md) for MCP server, system prompts, Python API
- **Full Documentation**: [`docs/production/00_COMPLETE_SUMMARY.md`](docs/production/00_COMPLETE_SUMMARY.md)

---

## 🌐 Learn More

- **[Why Empirica?](WHY_EMPIRICA.md)** - Philosophy and the Mirror Principle
- **[Distribution Guide](DISTRIBUTION_README.md)** - Publishing and packaging details
- **[Complete Installation](docs/COMPLETE_INSTALLATION_GUIDE.md)** - All platforms and integrations
- **[Full Documentation](docs/production/)** - Comprehensive guides and API reference
- **Website** - (Coming soon with interactive demos)

---

## 👥 Who Uses Empirica?

**🤖 AI Agents** - Primary users (Claude, GPT, Gemini, Qwen, etc.)  
**👤 Developers** - Building in critical domains (healthcare, finance, research)  
**🏢 Teams** - Requiring AI transparency and audit trails

⚠️ **Note:** Empirica requires genuine epistemic engagement. It's not a quick wrapper—it's a methodology for honest AI

---

## 📄 License

Dual-licensed under **LGPL-3.0-or-later** OR **MIT** - Choose the license that works for your project.

See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📬 Support

- **Issues**: [GitHub Issues](https://github.com/nubaeon/empirica/issues)
- **Documentation**: [`docs/`](docs/)
- **Questions**: (Discussion forum coming soon)

---

**Made with ❤️ for honest AI**

