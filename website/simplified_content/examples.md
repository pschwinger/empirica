# Examples & Tutorials

**Real-World Implementation Patterns.**

---

## Popular Patterns

<!-- BENTO_START -->

## 1. Automated Code Review
**Epistemic filtering.**

```python
result = await cascade.run(task, context)
if result['confidence'] > 0.8:
    print("✅ High confidence issue")
else:
    print("⚠️ Low confidence - skipping")
```

## 2. Strategic Lit Review
**Uncertainty tracking.**

```python
result = await cascade.run(task, context)
delta = result['epistemic_delta']
print(f"Knowledge gained: {delta['know']}")
print(f"Uncertainty reduced: {delta['uncertainty']}")
```

## 3. Multi-AI Handoffs
**Session continuity.**

```python
create_handoff_report(
    session_id="agent-1",
    key_findings=["Found bug"],
    next_session_context="Ready to fix"
)
# Agent 2 reads this report
```

<!-- BENTO_END -->

---

## Additional Examples

### 4. CI/CD Gate Check
**Bash script integration.**

```bash
CONFIDENCE=$(empirica assess --output json | jq .confidence)
if (( $(echo "$CONFIDENCE < 0.75" | bc -l) )); then
  echo "❌ Confidence too low"
  exit 1
fi
```

### 5. Custom Investigation Plugin
**Extend capabilities.**

```python
class SecurityPlugin(InvestigationPlugin):
    async def investigate(self, gap, context):
        return {"findings": ["Vuln found"], "confidence": 0.9}
```

---

**Next Steps:**
- [Read Use Cases](use-cases.md)
- [API Reference](developers/api-reference.md)
- [Getting Started](getting-started.md)
