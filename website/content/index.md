# Empirica: Metacognitive AI Framework

## Empowering AI Systems with Epistemic Awareness

Empirica is a production-grade framework that enables AI systems to measure, validate, and improve their knowledge state through genuine epistemic reasoning. By implementing a comprehensive 13-vector epistemic assessment system and the canonical CASCADE workflow, Empirica provides AI systems with the self-awareness needed for reliable, transparent, and trustworthy operation.

---

## What Makes Empirica Different?

Unlike traditional AI approaches that rely on heuristics or surface-level pattern matching, Empirica uses genuine LLM-powered self-assessment across 13 epistemic dimensions to provide authentic meta-cognitive awareness.

### The Empirica Advantage

🧠 **Genuine Self-Assessment** - Real LLM-powered epistemic evaluation, not heuristics

📊 **13-Vector Epistemic System** - Comprehensive framework for knowledge state measurement

🔄 **CASCADE Workflow** - Canonical: PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT

🎯 **Epistemic Humility** - "Knowing what you don't know" prevents costly mistakes

⚡ **Real-Time Visualization** - Watch your AI's reasoning process unfold in tmux dashboard

🔍 **Multi-AI Collaboration** - Shared belief spaces and epistemic state synchronization

---

## The 13 Epistemic Vectors

Empirica's core innovation is the 13-vector epistemic assessment system that evaluates AI reasoning across multiple dimensions:

### Foundation (35% weight)
- **KNOW** - Domain knowledge confidence
- **DO** - Execution capability assessment  
- **CONTEXT** - Environmental awareness

### Comprehension (25% weight)
- **CLARITY** - Task understanding
- **COHERENCE** - Logical consistency
- **SIGNAL** - Information quality
- **DENSITY** - Complexity management

### Execution (25% weight)
- **STATE** - Current readiness
- **CHANGE** - Modification tracking
- **COMPLETION** - Goal proximity confidence
- **IMPACT** - Consequence awareness

### Meta-Epistemic
- **UNCERTAINTY** - Self-awareness of knowledge gaps
- **ENGAGEMENT** - Collaborative intelligence quality
- **CALIBRATION** - Confidence vs. accuracy tracking

---

## How CASCADE Works

Empirica implements a canonical cascade that transforms uncertain tasks into confident actions:

```
PREFLIGHT → assess epistemic state (13 vectors)
INVESTIGATE → strategic knowledge gathering
CHECK → validation and confidence assessment
ACT → confident execution
POSTFLIGHT → learning and calibration
```

### Example Workflow

```python
from empirica.cascade import CanonicalEpistemicCascade

# Initialize cascade
cascade = CanonicalEpistemicCascade(
    task="Analyze codebase for security vulnerabilities",
    enable_bayesian=True,
    enable_drift_monitor=True
)

# Run epistemic assessment
result = await cascade.run_epistemic_cascade()

# CASCADE determines:
# - Confidence level (0.0 - 1.0)
# - Required investigation
# - Final action recommendation
print(f"Confidence: {result['confidence']:.2f}")
print(f"Action: {result['action']}")
```

---

## Core Features

### 🔧 Developer Tools

**MCP Server Integration**
- Full Claude Desktop integration
- 39+ MCP tools for AI assistance
- Seamless workflow enhancement

**Auto-Tracking System**
- SQLite + JSON + Reflex logs
- Session persistence
- Performance analytics

**tmux Dashboard**
- Real-time epistemic state visualization
- 13D vector monitoring
- CASCADE phase tracking

### 🧠 Epistemic Intelligence

**Bayesian Guardian**
- Evidence-based belief tracking
- Prevents overconfidence/underconfidence
- Real-time calibration

**Drift Monitor**
- Detects sycophancy drift
- Maintains intellectual honesty
- Behavioral integrity monitoring

**Investigation Strategy System**
- Domain-specific knowledge gathering
- Extensible strategy framework
- Automated tool recommendations

### 🚀 Production Ready

**Plugin Architecture**
- Universal extensibility
- No core code modification required
- Automatic LLM explanations

**Multi-AI Collaboration**
- Shared belief spaces
- Epistemic state synchronization
- Collaborative reasoning

**Enterprise Security**
- Comprehensive logging
- Audit trails
- Compliance support

---

## Who Uses Empirica?

### Developers
Building AI-powered applications that require transparent, reliable reasoning

### Researchers
Studying AI behavior, epistemic reasoning, and meta-cognitive systems

### Organizations
Implementing trustworthy AI with accountability and transparency

### Use Cases
- **Autonomous AI agents** requiring self-awareness
- **Decision-support systems** needing uncertainty quantification
- **Research tools** demanding epistemic rigor
- **Production applications** requiring transparency and trust

---

## Getting Started

### Quick Installation

```bash
# Clone repository
git clone https://github.com/Nubaeon/empirica
cd empirica

# Install dependencies
pip install -e .

# Configure MCP integration
empirica setup mcp

# Start your first cascade
empirica demo --task "Analyze my project structure"
```

### Your First CASCADE

```python
from empirica import bootstrap_session, run_cascade

# Start epistemic session
session = bootstrap_session(
    ai_id="my-first-agent",
    domain="code_analysis"
)

# Run canonical cascade
result = await run_cascade(
    session_id=session.id,
    task="Review my Python code for improvements"
)

# View results
print(f"Confidence: {result.confidence}")
print(f"Recommendations: {result.recommendations}")
```

### Next Steps

1. **[Installation Guide](getting-started.md)** - Complete setup instructions
2. **[CASCADE Tutorial](docs/cascade.md)** - Deep dive into the workflow
3. **[MCP Integration](docs/mcp.md)** - Enhance your AI assistant
4. **[Examples Gallery](examples.md)** - Real-world use cases

---

## Architecture Overview

Empirica consists of 24+ production-ready components organized into 6 categories:

1. **Core Epistemic Engine** - 13-vector assessment system
2. **CASCADE Workflow** - Canonical reasoning process  
3. **MCP Server** - Claude Desktop integration
4. **Visualization Tools** - tmux dashboard and monitoring
5. **Storage & Persistence** - Multi-format data tracking
6. **Plugin System** - Extensibility framework

---

## Join the Community

Empirica is built by developers, for developers. Join our community to:

- Share use cases and examples
- Contribute to the framework
- Get help and support
- Shape the future of epistemic AI

### Get Involved

- **[Documentation](docs.md)** - Comprehensive guides and references
- **[GitHub Repository](https://github.com/your-org/empirica)** - Source code and issues
- **[Community Forum](community.md)** - Discussion and support
- **[Contributing Guide](contributing.md)** - How to contribute

---

*Built with epistemic humility. Trusted by developers worldwide.*
