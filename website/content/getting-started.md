# Getting Started with Empirica

Welcome to Empirica! This guide will get you up and running with the Empirica framework in under 10 minutes. You'll learn how to install Empirica, run your first epistemic assessment, and understand the CASCADE workflow.

---

## What You'll Learn

- ✅ How to install Empirica and set up your environment
- ✅ Running your first CASCADE workflow  
- ✅ Understanding epistemic assessment results
- ✅ Basic CLI and Python API usage
- ✅ Setting up the tmux dashboard for visualization

**Time Required:** 10-15 minutes  
**Prerequisites:** Python 3.10+, Git

---

## Quick Installation

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-org/empirica.git
cd empirica

# Create virtual environment (recommended)
python3 -m venv .venv-empirica

# Activate virtual environment
# Linux/Mac:
source .venv-empirica/bin/activate

# Windows:
.venv-empirica\Scripts\activate

# Install Empirica in development mode
pip install -e .
```

### 2. Verify Installation

```bash
# Check that Empirica is installed correctly
empirica --version

# You should see: Empirica v1.0.0 or similar
```

### 3. Test Your Setup

```bash
# Run a simple test
empirica demo --task "Test installation"
```

If this works, you're ready to go! Let's run your first CASCADE.

---

## Your First CASCADE

Let's walk through a complete CASCADE workflow step by step.

### Step 1: Start with a Task

Imagine you need to analyze some code for potential improvements. Let's see how Empirica handles this:

```bash
# Start a CASCADE assessment
empirica preflight "Analyze my Python project structure for improvements"

# The system will ask you to assess yourself across 13 epistemic vectors
# Be honest! This is about building self-awareness, not performance.
```

### Step 2: Understand Your Assessment

When you complete the preflight assessment, you'll get results like:

```bash
Session ID: 2b7c3d8e-1f4a-4c6b-9d2e-5f8a7c9b0e3d

Epistemic Assessment Results:
============================
ENGAGEMENT: 0.85 ✅ (Good collaboration quality)
KNOW: 0.70     (Moderate project knowledge)
DO: 0.80       (Good code analysis capability)
CONTEXT: 0.60  (Adequate environmental awareness)
UNCERTAINTY: 0.40 (Moderate uncertainty about approach)

Recommendation: PROCEED (Confidence: 0.75)
```

**What this means:**
- Your engagement is high (collaborative quality)
- You have good execution capability 
- Uncertainty is moderate - you might benefit from some investigation
- Overall confidence is good enough to proceed

### Step 3: Investigation (if needed)

If your uncertainty is high, Empirica will recommend investigation:

```bash
# Empirica suggests investigation areas
Recommended Investigation:
- Current project structure patterns
- Python best practices for the specific modules
- Performance bottlenecks in the codebase

Would you like to investigate these areas? (y/n): y

# Empirica would then provide targeted guidance
```

### Step 4: Execute and Learn

```bash
# Complete your work, then run postflight
empirica postflight 2b7c3d8e-1f4a-4c6b-9d2e-5f8a7c9b0e3d \
  --summary "Analyzed project structure, identified 3 refactoring opportunities"

# See your learning and calibration
Postflight Results:
====================
Initial Uncertainty: 0.40
Final Uncertainty: 0.15
Learning Delta: +0.25 (25% uncertainty reduction)

Calibration: 89% (Your confidence was well-matched to reality)
Key Learning: Project structure patterns are more systematic than initially assessed
```

---

## Using the Python API

While the CLI is great for quick tasks, the Python API gives you more control:

### Basic Example

```python
from empirica import CanonicalEpistemicCascade
from empirica.types import Task, Context

# Initialize your CASCADE
cascade = CanonicalEpistemicCascade(
    enable_bayesian=True,
    enable_drift_monitor=True,
    enable_tracking=True
)

# Define your task
task = Task(
    description="Review authentication system for security improvements",
    context=Context(
        files=["./auth/", "./security/"],
        requirements=["security_focus", "performance_aware"]
    )
)

# Run the CASCADE
result = await cascade.run_cascade(task)

# Handle the results
if result.confidence > 0.7:
    print(f"Ready to act! Confidence: {result.confidence:.2f}")
    print(f"Recommended actions: {result.recommendations}")
else:
    print(f"Need investigation. Uncertainty: {result.uncertainty:.2f}")
    print(f"Investigation suggestions: {result.investigation_plan}")
```

### Advanced Configuration

```python
from empirica import EmpiricaConfig

# Configure for your use case
config = EmpiricaConfig(
    epistemic_vectors=EpistemicVectors.FOUNDATION_PLUS_UNCERTAINTY,
    cascade=CascadeConfig(
        auto_investigate=True,
        confidence_threshold=0.75
    ),
    tracking=TrackingConfig(
        enable_sqlite=True,
        session_retention="7d"
    )
)

cascade = CanonicalEpistemicCascade(config=config)
```

---

## Setting Up the Dashboard

The tmux dashboard provides real-time visualization of your AI's epistemic state:

### Start the Dashboard

```bash
# In one terminal - start the dashboard
empirica dashboard start --mode tmux

# This opens a tmux session with live epistemic monitoring
```

### Monitor a Session

```bash
# In another terminal - run your CASCADE
empirica preflight "Review database schema for optimization"

# Watch the dashboard update in real-time showing:
# - Current epistemic vector values
# - CASCADE phase progression  
# - Confidence changes over time
```

### Dashboard Features

- **13D Vector Visualization** - See all epistemic dimensions
- **CASCADE Phase Tracker** - Current workflow stage
- **Confidence Timeline** - How confidence evolves
- **Investigation Recommendations** - Real-time suggestions

---

## Common Workflows

### 1. Code Analysis

```bash
empirica preflight "Find performance bottlenecks in my API"

# Empirica assesses your approach
# If uncertainty is high, suggests specific investigation
# Recommends profiling tools, benchmarking approaches
```

### 2. Research Tasks

```bash
empirica preflight "Research quantum computing impact on cryptography"

# Handles uncertainty about rapidly evolving field
# Suggests authoritative sources
# Tracks confidence as you learn
```

### 3. Decision Making

```bash
empirica preflight "Should I refactor the authentication module?"

# Quantifies decision confidence
# Identifies missing information
# Provides risk assessment
```

---

## Understanding Your Results

### Epistemic Vectors Explained

| Vector | What It Measures | Why It Matters |
|--------|------------------|----------------|
| **ENGAGEMENT** | Collaborative quality | Prevents wasted effort |
| **KNOW** | Domain knowledge | Avoids overconfident errors |
| **DO** | Execution capability | Ensures realistic planning |
| **CONTEXT** | Environmental awareness | Prevents context blindness |
| **UNCERTAINTY** | Knowledge gaps | Drives strategic investigation |

### Confidence vs. Uncertainty

- **High Confidence + Low Uncertainty** = Proceed with action
- **Low Confidence + High Uncertainty** = Investigate further  
- **Medium Confidence** = May need targeted research

### Calibration Quality

Empirica tracks how well your confidence matches reality:
- **90%+** = Excellent calibration
- **70-89%** = Good calibration  
- **<70%** = Needs improvement

---

## Next Steps

### Learn More

- **[Features Overview](features.md)** - Deep dive into capabilities
- **[API Reference](api-reference.md)** - Complete Python API documentation
- **[Architecture Guide](architecture.md)** - System design and components
- **[Use Cases](use-cases.md)** - Real-world examples and patterns

### Advanced Usage

- **MCP Integration** - Enhance Claude Desktop with Empirica
- **Multi-AI Collaboration** - Build collaborative AI systems
- **Plugin Development** - Create domain-specific extensions
- **Production Deployment** - Enterprise-grade setup

### Community

- **[GitHub Repository](https://github.com/your-org/empirica)** - Source code and issues
- **[System Prompts](system-prompts.md)** - AI assistant configurations
- **[Examples Gallery](examples.md)** - Community-contributed examples

---

## Troubleshooting

### Installation Issues

```bash
# Virtual environment problems
python3 -m venv --clear .venv-empirica
source .venv-empirica/bin/activate
pip install -e .

# Permission issues (Linux/Mac)
pip install --user -e .

# Missing dependencies
pip install -e .[dev,test,docs]
```

### Common CLI Issues

```bash
# Session not found
empirica sessions list
empirica sessions show <session_id>

# Dashboard not responding
empirica dashboard stop
empirica dashboard start --mode tmux

# MCP integration problems
empirica setup mcp --check
empirica setup mcp --reset
```

### API Issues

```python
# Import errors
from empirica.cascade import CanonicalEpistemicCascade
from empirica.config import EmpiricaConfig

# Configuration validation
config = EmpiricaConfig()
config.validate()  # Check for configuration issues

# Session debugging
cascade.debug_mode = True
result = await cascade.run_cascade(task)
print(result.debug_info)
```

---

## Quick Reference

### Essential Commands

```bash
# Core workflow
empirica preflight "your task"
empirica postflight <session_id> --summary "what you did"

# Session management  
empirica sessions list
empirica sessions show <session_id>
empirica sessions export <session_id> --output results.json

# Dashboard
empirica dashboard start --mode tmux
empirica dashboard stop

# MCP integration
empirica setup mcp --enable-all-tools
```

### Python Quick Start

```python
from empirica import run_cascade

result = await run_cascade(
    task="your task description",
    domain="code_analysis"  # or "research", "decision_making", etc.
)

print(f"Confidence: {result.confidence}")
print(f"Recommendations: {result.recommendations}")
```

---

**Welcome to epistemically-grounded AI development!** 🎯

*Empirica helps you build AI systems that know what they know, and more importantly, what they don't know.*