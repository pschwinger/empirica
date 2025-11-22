# FAQs Page Wireframe

## Page: faqs.html

### Header Section
**Layout:** Full-width, centered

- **Page Title:** "Frequently Asked Questions"
- **Sub-Title:** "Find answers to common questions about Empirica"
- **Search Bar:** Real-time search filtering (JavaScript-based)
  - Placeholder: "Search FAQs..."
  - Icon: 🔍
  - Searches across questions and answers

---

## Search & Filter Component

**Layout:** Sticky below navigation

### Search Input
- Full-width search box
- Live filtering as user types
- Clear button (X) when text entered
- Shows match count: "Showing X of Y questions"

### Category Filter Tabs
- All (default, shows count)
- Getting Started
- Epistemic Vectors
- Components & Features
- Configuration & Setup
- Integration & MCP
- Troubleshooting
- Advanced Topics

---

## FAQ Categories

### Category 1: Getting Started

#### Q1: What is Empirica?
**Answer:**
Empirica is a production-grade epistemic reasoning system that helps AI systems measure and validate their knowledge state without interfering with their internal reasoning processes. Unlike traditional approaches using heuristics, Empirica employs genuine LLM-powered self-assessment across 13 epistemic dimensions to provide authentic meta-cognitive awareness.

**Keywords:** introduction, overview, basics, what is

---

#### Q2: How do I install Empirica?
**Answer:**
Installation is straightforward:

```bash
# Clone the repository
git clone https://github.com/your-org/empirica
cd empirica

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 -c "from metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade; print('✅ Ready!')"
```

For detailed setup instructions, see our [Quick Start Guide](/getting-started.html).

**Keywords:** install, setup, installation, dependencies

---

#### Q3: What's the simplest way to use Empirica?
**Answer:**
The minimal setup requires just a few lines:

```python
from metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade

cascade = CanonicalEpistemicCascade()
result = await cascade.run_epistemic_cascade(
    task="Your task here",
    context={"cwd": "/path"}
)
```

This gives you basic epistemic assessment. Enable additional features like Bayesian Guardian and Drift Monitor by passing flags to the constructor.

**Keywords:** quick start, basic usage, simple, minimal

---

#### Q4: Can I use Empirica with Claude Desktop?
**Answer:**
Yes! Empirica includes full MCP (Model Context Protocol) integration. Add the following to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": ["/path/to/empirica/empirica_mcp_server.py"]
    }
  }
}
```

See our [MCP Integration Guide](/docs.html) for complete setup instructions.

**Keywords:** Claude, MCP, Claude Desktop, integration

---

#### Q5: What programming languages does Empirica support?
**Answer:**
Empirica is written in Python and primarily designed for Python applications. However, it can be accessed from any language through:
- The MCP server interface (JSON-RPC)
- The CLI interface (command-line tool)
- REST API (if running the web server component)

**Keywords:** Python, language support, programming languages

---

### Category 2: Epistemic Vectors

#### Q6: What are the 13 epistemic vectors?
**Answer:**
Empirica assesses epistemic state across 13 dimensions organized into 5 groups:

1. **ENGAGEMENT** (Gate, 15% weight) - Collaborative intelligence quality
2. **FOUNDATION** (35% weight) - KNOW, DO, CONTEXT
3. **COMPREHENSION** (25% weight) - CLARITY, COHERENCE, SIGNAL, DENSITY
4. **EXECUTION** (25% weight) - STATE, CHANGE, COMPLETION, IMPACT
5. **UNCERTAINTY** (Meta) - The 13th dimension measuring "what you don't know about what you don't know"

See our [Epistemic Vectors Deep Dive](/epistemic-awareness.html) for detailed explanations.

**Keywords:** vectors, dimensions, 13 vectors, epistemic dimensions

---

#### Q7: What is the UNCERTAINTY vector and why is it important?
**Answer:**
UNCERTAINTY is the 13th epistemic dimension and represents meta-epistemic self-awareness - the AI's understanding of "what it doesn't know about what it doesn't know." This vector:

- Tracks implicit uncertainty that can't be captured by the other 12 vectors
- Compares pre-flight and post-flight assessments
- Measures investigation effectiveness (Δuncertainty should decrease after investigation)
- Prevents overconfidence by exposing hidden knowledge gaps

This is a breakthrough in AI self-awareness, making uncertainty explicit and measurable.

**Keywords:** uncertainty, 13th vector, meta-epistemic, unknown unknowns

---

#### Q8: What is the ENGAGEMENT gate?
**Answer:**
ENGAGEMENT is the first dimension assessed (15% weight) and acts as a gate. It measures collaborative intelligence quality - the degree to which meaningful collaboration is occurring. 

If ENGAGEMENT < 0.60, the task is unclear or poorly specified, and the cascade recommends user clarification before proceeding. This prevents wasted computational effort on ambiguous tasks.

**Keywords:** engagement, gate, collaborative intelligence, threshold

---

#### Q9: How are vector weights determined?
**Answer:**
The canonical weight distribution is:
- ENGAGEMENT: 15% (gate function)
- FOUNDATION: 35% (KNOW, DO, CONTEXT - most critical)
- COMPREHENSION: 25% (understanding quality)
- EXECUTION: 25% (execution readiness)

These weights can be tuned for specific domains. See our [Tuning Thresholds Guide](/docs.html) for domain-specific calibration examples.

**Keywords:** weights, calibration, tuning, thresholds

---

### Category 3: Components & Features

#### Q10: What is the Bayesian Guardian?
**Answer:**
The Bayesian Guardian provides real-time evidence-based belief tracking. It:
- Maintains a probability distribution over possible beliefs
- Updates beliefs as new evidence arrives
- Detects when intuition diverges from accumulated evidence
- Prevents both overconfidence and underconfidence
- Activates selectively for precision-critical domains

Think of it as a "second opinion" system that alerts when your confidence doesn't match the evidence.

**Keywords:** Bayesian, guardian, evidence, belief tracking

---

#### Q11: What is the Drift Monitor?
**Answer:**
The Drift Monitor maintains behavioral integrity by detecting:
- **Sycophancy drift**: Agreement without genuine justification
- **Tension avoidance**: Conflict avoidance that compromises truth
- **Behavioral inconsistencies**: Actions misaligned with stated beliefs

It ensures intellectual honesty throughout the reasoning process, preventing the AI from "people-pleasing" at the expense of accuracy.

**Keywords:** drift, sycophancy, integrity, behavioral monitoring

---

#### Q12: What is the Plugin System?
**Answer:**
Empirica's plugin system enables universal extensibility without modifying core code. You can:
- Add domain-specific investigation tools
- Integrate with custom data sources
- Extend capabilities with automatic LLM explanation
- Maintain separation of concerns

Plugins implement the `InvestigationPlugin` interface and are automatically discovered and documented by the system.

**Keywords:** plugins, extensibility, custom tools

---

#### Q13: How does auto-tracking work?
**Answer:**
Auto-tracking automatically records all epistemic assessments and cascade executions in three formats:

1. **SQLite Database**: Structured queryable data for analysis
2. **JSON Files**: Session logs for archival and export
3. **Reflex Logs**: Real-time streaming for dashboard visualization

Enable it with:
```python
cascade = CanonicalEpistemicCascade(enable_action_hooks=True)
```

Zero overhead when disabled. See our [Monitoring & Logging Guide](/docs.html) for details.

**Keywords:** tracking, logging, auto-tracking, monitoring

---

#### Q14: What components are included in Empirica?
**Answer:**
Empirica includes 24+ production-ready components across 6 categories:

1. **Code Intelligence & Navigation** - Code analysis, intelligent navigation
2. **Context & Environment** - Context validation, workspace awareness
3. **Goal & Task Management** - Goal decomposition, task tracking
4. **Analysis & Validation** - Runtime validation, procedural analysis
5. **Security & Monitoring** - Security scanning, drift detection
6. **Infrastructure** - Tool management, session handling

See our [Components Page](/components.html) for the complete catalog with examples.

**Keywords:** components, tools, catalog

---

### Category 4: Configuration & Setup

#### Q15: How do I enable all features?
**Answer:**
To enable all Empirica features:

```python
cascade = CanonicalEpistemicCascade(
    enable_bayesian=True,           # Bayesian Guardian
    enable_drift_monitor=True,      # Drift Monitor
    enable_action_hooks=True,       # Auto-tracking
    auto_start_dashboard=False      # Manual tmux start
)
```

Each feature can be toggled independently based on your needs.

**Keywords:** configuration, enable features, setup

---

#### Q16: How do I configure confidence thresholds?
**Answer:**
The default action threshold is 0.70. To change it:

```python
cascade = CanonicalEpistemicCascade(
    action_confidence_threshold=0.80  # Higher threshold = more investigation
)
```

Lower thresholds (0.60-0.70) suit creative/exploratory tasks. Higher thresholds (0.80-0.90) suit high-stakes decisions. See [Tuning Thresholds](/docs.html) for domain-specific recommendations.

**Keywords:** thresholds, confidence, configuration

---

#### Q17: Where are data files stored?
**Answer:**
Empirica stores data in the `.empirica` directory:

- `.empirica/sessions.db` - SQLite database with all sessions
- `.empirica/json_sessions/` - JSON session logs
- `.empirica/empirica_reflex_logs/` - Real-time reflex frames
- `.empirica/config.yaml` - User configuration (optional)

Location can be customized via environment variable: `EMPIRICA_DATA_DIR`

**Keywords:** data storage, files, location, directory

---

#### Q18: How do I configure for multi-AI collaboration?
**Answer:**
Each AI needs a unique ID:

```python
cascade = CanonicalEpistemicCascade(ai_id="researcher_1")
```

Or via environment variable:
```bash
export EMPIRICA_AI_ID="researcher_1"
```

This enables session tracking per AI and supports shared belief space management. See our [Multi-AI Collaboration Guide](/docs.html).

**Keywords:** multi-AI, collaboration, AI ID

---

### Category 5: Integration & MCP

#### Q19: What is MCP integration?
**Answer:**
MCP (Model Context Protocol) integration exposes Empirica's capabilities to Claude Desktop and other MCP-compatible clients. Features include:

- Run epistemic cascades through Claude
- Access all components and tools
- Configure features client-side
- View epistemic assessments in conversations

See our [MCP Integration Guide](/docs.html) for setup and usage.

**Keywords:** MCP, Model Context Protocol, integration

---

#### Q20: Can I use Empirica with other AI models (not Claude)?
**Answer:**
Yes! Empirica is model-agnostic. It uses:
- OpenAI API (GPT-4, GPT-3.5, etc.)
- Anthropic API (Claude)
- Local models via compatible APIs
- Custom model endpoints

Configure via environment variables or constructor parameters. The epistemic reasoning logic is independent of the model provider.

**Keywords:** models, AI models, providers, compatibility

---

#### Q21: How do I integrate Empirica into my existing codebase?
**Answer:**
Three integration approaches:

1. **Direct API**: Import and use `CanonicalEpistemicCascade` directly
2. **CLI Tool**: Call `empirica` command-line tool from your code
3. **MCP Server**: Run as a service and communicate via JSON-RPC

Choose based on your architecture. See [API Reference](/api.html) for detailed integration patterns.

**Keywords:** integration, API, existing code

---

### Category 6: Troubleshooting

#### Q22: Why does my cascade always return "investigate"?
**Answer:**
Common causes:

1. **Threshold too high**: Lower `action_confidence_threshold` (default 0.70)
2. **Insufficient context**: Provide more context in the `context` parameter
3. **Ambiguous task**: Rephrase task to be more specific
4. **ENGAGEMENT failure**: Task may be too vague (check ENGAGEMENT score)

Enable debug logging to see vector scores: `logging.basicConfig(level=logging.DEBUG)`

**Keywords:** troubleshooting, investigate, debugging

---

#### Q23: The dashboard isn't updating in real-time
**Answer:**
Check these items:

1. **Enable hooks**: Set `enable_action_hooks=True`
2. **Tmux running**: Start dashboard with `tmux new -s empirica`
3. **Reflex logs writing**: Check `.empirica/empirica_reflex_logs/` has recent files
4. **File permissions**: Ensure write access to `.empirica/` directory

See [Dashboard Monitoring Guide](/docs.html) for troubleshooting steps.

**Keywords:** dashboard, tmux, real-time, not updating

---

#### Q24: I'm getting "Investigation tool not found" errors
**Answer:**
This means the investigation system cannot find the specified tool. Solutions:

1. **Check plugin registration**: Ensure custom plugins are passed to constructor
2. **Verify tool name**: Tool names are case-sensitive
3. **Check imports**: Ensure investigation tools are properly imported
4. **Review tool catalog**: Use `empirica list-tools` to see available tools

**Keywords:** tool not found, investigation, errors

---

#### Q25: How do I debug low confidence scores?
**Answer:**
Enable detailed logging to see individual vector scores:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

cascade = CanonicalEpistemicCascade()
result = await cascade.run_epistemic_cascade(task, context)

# Examine result['vectors'] for individual scores
print(result['vectors'])
```

Look for vectors with scores < 0.5 - these are driving down overall confidence. Address the specific gaps (improve context, provide more information, etc.).

**Keywords:** debugging, low confidence, troubleshooting

---

### Category 7: Advanced Topics

#### Q26: What is "Approach B" philosophy?
**Answer:**
"Approach B" is Empirica's investigation philosophy: **measure + suggest (not execute)**. The system:

- Maps available tool capabilities
- Suggests investigation strategies
- Lets the LLM decide and execute
- Doesn't control or enforce actions

This preserves LLM autonomy while providing epistemically-grounded guidance. Contrast with "Approach A" which would automatically execute investigation steps.

**Keywords:** Approach B, philosophy, investigation strategy

---

#### Q27: How does investigation necessity logic work?
**Answer:**
Investigation is skipped when:

1. No significant gaps detected (all vectors > 0.70)
2. Simple tasks with high engagement (confidence > 0.75)
3. Creative tasks with good engagement (ENGAGEMENT > 0.70, creative domain)
4. Acceptable overall confidence for the domain

This prevents over-investigation and unnecessary delays. The necessity logic adapts to task type and domain requirements.

**Keywords:** investigation, necessity, when to investigate

---

#### Q28: Can I create custom epistemic vectors?
**Answer:**
Currently, the 13 canonical vectors are fixed to maintain consistency across deployments. However, you can:

- Use the plugin system to add custom assessment logic
- Extend the cascade with pre/post hooks
- Add domain-specific metadata to context
- Create custom analysis tools that feed into existing vectors

Future versions may support custom vector definitions. See [Plugin System Guide](/docs.html).

**Keywords:** custom vectors, extensibility

---

#### Q29: How does pre-flight vs post-flight comparison work?
**Answer:**
Pre-flight and post-flight assessments enable investigation validation:

1. **Pre-flight**: Assess epistemic state before investigation
2. **Investigation**: Gather knowledge using strategic tools
3. **Post-flight**: Re-assess epistemic state
4. **Comparison**: Calculate Δvectors (especially Δuncertainty)

Successful investigation should show:
- Increased confidence in relevant vectors
- Decreased UNCERTAINTY
- Improved CLARITY and SIGNAL

This validates that investigation actually improved epistemic state.

**Keywords:** pre-flight, post-flight, comparison, delta

---

#### Q30: What is semantic engineering in Empirica?
**Answer:**
Semantic engineering is the practice of building AI systems grounded in meaningful conceptual structures rather than surface-level pattern matching. In Empirica, this means:

- Using genuine LLM assessment (no heuristics)
- Measuring authentic epistemic dimensions
- Preserving conceptual integrity
- Aligning with how knowledge actually works

It's the philosophical foundation ensuring Empirica's assessments reflect true epistemic state, not just statistical correlations.

**Keywords:** semantic engineering, philosophy, grounding

---

## Design Notes

### Search Functionality
- **Live filtering**: JavaScript filters questions as user types
- **Highlight matches**: Matched text highlighted in yellow
- **Case-insensitive**: Search ignores case
- **Searches**: Question text, answer text, and keywords
- **Smooth scroll**: Clicking result scrolls smoothly to question

### Category Filter
- **Tab interface**: Horizontal tabs for categories
- **Active state**: Current category highlighted
- **Count badges**: Show number of questions per category
- **"All" default**: Shows all questions on page load
- **Combines with search**: Can search within a category

### Accordion Behavior
- **Collapsed by default**: Only question visible initially
- **Click to expand**: Click question to reveal answer
- **Smooth animation**: Expand/collapse with CSS transition
- **Icon indicator**: ▶ when collapsed, ▼ when expanded
- **Deep linking**: Support #faq-{id} URLs to link directly to expanded question

### Mobile Responsiveness
- **Stack categories**: Category tabs scroll horizontally on mobile
- **Full-width questions**: Questions take full width
- **Readable text**: Adequate font size and spacing
- **Touch-friendly**: Large click targets for expanding questions

### Content Strategy
- **30 questions**: Comprehensive coverage without overwhelming
- **7 categories**: Logical grouping of related topics
- **Progressive disclosure**: Basic → Advanced flow
- **Cross-linking**: Link to relevant docs for deeper dives
- **Code examples**: Include where helpful
- **Keywords**: Each question tagged for search optimization

### Visual Design
- **Clean hierarchy**: Clear question/answer distinction
- **Code formatting**: Syntax highlighting for code blocks
- **Icons**: Subtle icons for visual interest (optional)
- **Spacing**: Generous white space for readability
- **Consistency**: Matches overall site design (header/footer from wireframe_home.html)
