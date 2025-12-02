# Getting Started with Empirica

**Up and running in under 10 minutes.**

---

## Quick Start Steps

<!-- BENTO_START -->

## 1. Installation
**Setup in seconds.**

```bash
# Install from source
git clone https://github.com/your-org/empirica.git
cd empirica
pip install -e .

# Verify
empirica --version
```

## 2. First CASCADE
**Run your first assessment.**

```bash
# Start assessment
empirica preflight "Analyze my project structure"

# Follow prompts to assess 13 vectors
```

## 3. Dashboard
**Visualize in real-time.**

```bash
# Start tmux dashboard
empirica dashboard start --mode tmux
```
Watch epistemic state evolve live.

<!-- BENTO_END -->

---

## Python API Usage

### Basic Example
```python
from empirica import CanonicalEpistemicCascade

cascade = CanonicalEpistemicCascade(agent_id="security-reviewer")
result = await cascade.run_epistemic_cascade(
    task="Review auth system",
    context={"domain": "security"}
)
```

### Advanced Configuration
```python
cascade = CanonicalEpistemicCascade(
    profile_name="autonomous_agent",
    enable_bayesian=True,
    enable_git_notes=True
)
```

---

## Common Workflows

### Code Analysis
`empirica preflight "Find performance bottlenecks"`
- Suggests profiling tools
- Identifies specific gaps

### Research Tasks
`empirica preflight "Research quantum cryptography"`
- Handles uncertainty
- Tracks confidence growth

### Decision Making
`empirica preflight "Should I refactor auth?"`
- Quantifies decision confidence
- Risk assessment

---

## New in v2.0

**MCO Architecture**: Dynamic configuration with persona selection and model-specific bias correction.

**ScopeVector Goals**: 3D goal scoping (`breadth`, `duration`, `coordination`) instead of categorical enums.

**Cross-AI Coordination**: Discover and resume goals from other AIs via git notes.

---

**Next Steps:**
- [Features Overview](features.md)
- [API Reference](developers/api-reference.md)
- [Architecture Guide](developers/architecture.md)
