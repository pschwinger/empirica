# Examples & Tutorials

**Code Patterns and Real-World Workflows**

[← Back to Developers](getting-started.md) | [Use Cases](use-cases.md) | [API Reference](api-reference.md)

---

## 1. Automated Code Review
**Pattern:** Epistemic filtering to reduce false positives.

```python
from empirica import CanonicalEpistemicCascade
from empirica.types import Task, Context

class EpistemicCodeReviewer:
    def __init__(self):
        self.cascade = CanonicalEpistemicCascade(
            enable_bayesian=True
        )
    
    async def review_code(self, code_files):
        task = Task(
            description=f"Review {len(code_files)} files for security",
            context=Context(files=code_files),
            domain="code_analysis"
        )
        
        result = await self.cascade.run_cascade(task)
        
        # Filter by confidence to reduce noise
        high_confidence_issues = [
            issue for issue in result.findings 
            if issue.confidence > 0.8
        ]
        
        return high_confidence_issues
```

## 2. Strategic Literature Review
**Pattern:** Systematic investigation with uncertainty tracking.

```python
async def review_literature(topic):
    cascade = CanonicalEpistemicCascade()
    
    # Initial assessment
    preflight = await cascade.preflight_assessment(
        Task(f"Review literature on {topic}")
    )
    
    # If uncertainty is high, investigate
    if preflight.uncertainty > 0.4:
        print("High uncertainty detected. Starting deep investigation...")
        investigation = await cascade.investigate_uncertainty(
            vectors=preflight.uncertain_vectors
        )
        print(f"Found {len(investigation.findings)} key sources.")
    
    # Final synthesis
    return await cascade.postflight_learning(preflight)
```

## 3. Multi-AI Collaboration
**Pattern:** Shared belief space for consensus.

```python
from empirica.collaboration import MultiAICollaborator

async def collaborative_design():
    collaborator = MultiAICollaborator()
    
    # Register agents
    await collaborator.register_ai("security_expert", capabilities=["security"])
    await collaborator.register_ai("performance_expert", capabilities=["perf"])
    
    # Execute collaborative task
    result = await collaborator.execute_task(
        task="Design scalable auth system",
        required_capabilities=["security", "perf"],
        epistemic_requirements={"certainty": 0.85}
    )
    
    print(f"Consensus Confidence: {result.collaborative_assessment.confidence}")
```

## 4. CI/CD Gate Check Script
**Pattern:** Shell script integration using CLI.

```bash
#!/bin/bash

# Run assessment
RESULT=$(empirica assess --context ./src --output json)

# Parse confidence
CONFIDENCE=$(echo $RESULT | jq .confidence)

# Gate logic
if (( $(echo "$CONFIDENCE < 0.75" | bc -l) )); then
  echo "❌ Confidence too low for deployment."
  exit 1
else
  echo "✅ Deployment approved."
  exit 0
fi
```

## 5. Custom Investigation Plugin
**Pattern:** Extending Empirica with domain tools.

```python
from empirica.plugins import EmpiricaPlugin

class SecurityScannerPlugin(EmpiricaPlugin):
    name = "security_scanner"
    
    async def execute_investigation(self, gap, context, config):
        if gap == "security_vulnerabilities":
            # Run external tool
            scan_results = await run_security_tool(context.files)
            return InvestigationResult(findings=scan_results)
            
# Register plugin
register_plugin(SecurityScannerPlugin)
```

---

**Next Steps:**
- [Read Use Cases](use-cases.md) for the business context
- [Check API Reference](api-reference.md) for class details
- [Try Getting Started](getting-started.md) to run your first code
