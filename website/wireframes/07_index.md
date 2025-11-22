# Index Page Wireframe (Home Page)

## Page: index.html

### Hero Section
**Background:** Gradient purple/blue (matching brand)
**Layout:** Full-width, centered content

- **Logo:** Empirica logo (centered)
- **Main Headline:** "Empirica: Epistemic Humility through Thoughtful AI Self-Reflection"
- **Sub-Headline:** "A production-grade framework enabling AI systems to measure, validate, and improve their knowledge state through genuine epistemic reasoning"
- **Primary CTA:** "Get Started" → /getting-started.html
- **Secondary CTA:** "View Documentation" → /docs.html

---

## Section 1: Foundation (What/Why/How/Who)

**Layout:** 4-column grid (responsive: 2x2 on mobile)

### Box 1: WHAT is Empirica?
**Icon:** 🧠 Brain
**Content:**
Empirica is a production-grade epistemic reasoning system that helps AI systems measure and validate their knowledge state without interfering with their internal reasoning processes. Unlike traditional approaches that rely on heuristics, Empirica uses genuine LLM-powered self-assessment across 13 epistemic dimensions to provide authentic meta-cognitive awareness.

**Key Features:**
- 13 epistemic vectors (including UNCERTAINTY)
- No heuristics - genuine LLM assessment
- Auto-tracking with SQLite + JSON + Reflex logs
- Real-time tmux dashboard visualization

---

### Box 2: WHY Epistemic Humility?
**Icon:** 🎯 Target
**Content:**
AI systems often operate with overconfidence or miss critical knowledge gaps. Empirica grounds AI reasoning in epistemic humility - the recognition that "knowing what you don't know" is as important as knowing what you do know. This prevents costly mistakes, enables better decision-making, and builds trust through transparent uncertainty acknowledgment.

**Benefits:**
- Reduces overconfident errors
- Enables strategic investigation
- Improves decision quality
- Builds user trust through transparency

---

### Box 3: HOW it Works
**Icon:** ⚙️ Gear
**Content:**
Empirica implements a canonical cascade flow: ENGAGEMENT → UNCERTAINTY → INVESTIGATE → CHECK → ACT. Each task is assessed across 13 dimensions, uncertainty is quantified pre and post-investigation, and the system determines whether to act confidently, investigate further, or seek user clarification.

**Cascade Flow:**
1. ENGAGEMENT Gate (collaborative quality check)
2. UNCERTAINTY Assessment (meta-epistemic awareness)
3. INVESTIGATE Phase (strategic knowledge gathering)
4. CHECK Phase (Bayesian Guardian + Drift Monitor)
5. ACT Phase (confident execution)

---

### Box 4: WHO is it For?
**Icon:** 👥 People
**Content:**
Empirica is designed for developers, researchers, and organizations building AI-powered applications who need transparent, reliable, and epistemically-grounded AI reasoning. Whether you're building autonomous agents, decision-support systems, or research tools, Empirica provides the foundation for trustworthy AI.

**Use Cases:**
- Autonomous AI agents
- Decision-support systems
- Research and analysis tools
- Multi-AI collaboration systems
- Production AI applications requiring transparency

---

## Section 2: Core Concepts

**Layout:** 3-column feature cards

### Card 1: Semantic Engineering
**Icon:** 📐
**Title:** Semantic Engineering
**Content:**
Build AI systems grounded in meaningful conceptual structures rather than surface-level pattern matching. Empirica's semantic approach ensures AI reasoning aligns with genuine understanding.

**Link:** "Learn about Semantic Engineering" → (internal anchor or page)

---

### Card 2: Tmux Dashboard
**Icon:** 📊
**Title:** Real-Time Visualization
**Content:**
Watch your AI's epistemic state evolve in real-time through our tmux-based dashboard. See 13D vector changes, cascade phases, investigation decisions, and reflex frame streams as they happen.

**Link:** "Explore Dashboard Features" → (internal anchor or page)

---

### Card 3: Integration & Examples
**Icon:** 🔌
**Title:** Integration & Examples
**Content:**
Explore practical examples of Empirica in action - from modality switching to collaborative AI systems. See how Empirica components integrate into real-world workflows.

**Link:** "View Examples" → /examples.html (or integration page)

---

## Section 3: The 13 Epistemic Vectors

**Layout:** Accordion or expandable panels (5 groups)

### Visualization
Display a simplified 13D vector radar chart or visual representation

### Groups (Expandable)

**1. ENGAGEMENT (Gate) - 15% weight**
- The first dimension: collaborative intelligence quality
- Must pass threshold (0.60) to proceed
- Prevents wasted effort on unclear tasks

**2. FOUNDATION - 35% weight**
- KNOW: Domain knowledge
- DO: Execution capability
- CONTEXT: Situational understanding

**3. COMPREHENSION - 25% weight**
- CLARITY: Task comprehension
- COHERENCE: Logical consistency
- SIGNAL: Information quality
- DENSITY: Information richness

**4. EXECUTION - 25% weight**
- STATE: Current readiness
- CHANGE: Change management understanding
- COMPLETION: Finish-ability confidence
- IMPACT: Consequence awareness

**5. UNCERTAINTY (Meta)**
- NEW: 13th dimension
- Meta-epistemic self-awareness
- "What you don't know about what you don't know"
- Pre/post investigation comparison

**Link:** "Deep Dive into Epistemic Vectors" → /epistemic-awareness.html

---

## Section 4: Advanced Capabilities

**Layout:** 2-column feature list

### Left Column

**Bayesian Guardian**
Real-time evidence-based belief tracking. Detects when intuition diverges from accumulated evidence, preventing overconfidence and underconfidence.

**Drift Monitor**
Behavioral integrity monitoring that catches sycophancy drift and tension avoidance, maintaining intellectual honesty.

**Plugin System**
Universal extensibility without core code modification. Add domain-specific tools with automatic LLM explanation.

---

### Right Column

**Auto-Tracking System**
Automatic session and cascade tracking with three output formats: SQLite database, JSON logs, and Reflex frames. Zero overhead when disabled.

**MCP Integration**
Full Claude Desktop integration. Expose all Empirica features through the Model Context Protocol for seamless AI assistant enhancement.

**Multi-AI Collaboration**
Support for collaborative AI systems with shared belief space management and epistemic state synchronization.

---

## Section 5: Quick Start

**Layout:** Code example + steps

### Python Example
```python
from metacognitive_cascade.metacognitive_cascade import CanonicalEpistemicCascade

# Create cascade with all features
cascade = CanonicalEpistemicCascade(
    enable_bayesian=True,
    enable_drift_monitor=True,
    enable_action_hooks=True
)

# Run epistemic reasoning
result = await cascade.run_epistemic_cascade(
    task="Should I refactor the authentication system?",
    context={"cwd": "/project"}
)

print(f"Action: {result['action']}")
print(f"Confidence: {result['confidence']:.2f}")
```

### Installation Steps
1. Clone repository: `git clone https://github.com/your-org/empirica`
2. Install dependencies: `pip install -r requirements.txt`
3. Run your first cascade (see example above)
4. Optional: Enable tmux dashboard for visualization

**CTA:** "Full Installation Guide" → /getting-started.html

---

## Section 6: Components Overview

**Layout:** Grid of component categories (6 categories, compact)

Brief overview stating:
"Empirica includes 24+ production-ready components organized into 6 categories"

**Categories (Listed, not detailed):**
1. Code Intelligence & Navigation
2. Context & Environment Management
3. Goal & Task Management
4. Analysis & Validation
5. Security & Monitoring
6. Infrastructure & Integration

**CTA:** "Explore All Components" → /components.html

---

## Section 7: Ready to Get Started?

**Layout:** Centered CTA section

**Content:**
"Join developers building epistemically-grounded AI systems. Start with our Quick Start guide or explore the documentation."

**CTAs:**
- Primary: "Get Started" → /getting-started.html
- Secondary: "Read Documentation" → /docs.html
- Tertiary: "Join Community" → /contact.html

---

## Footer
(Standard footer component - already defined in wireframe_home.html)

---

## Design Notes

### Visual Hierarchy
1. Hero section grabs attention
2. Foundation (What/Why/How/Who) provides immediate clarity
3. Core concepts give depth
4. 13 vectors show the uniqueness
5. Advanced capabilities demonstrate power
6. Quick start enables action
7. Components show completeness
8. Final CTA converts

### Content Principles
- Non-marketing language
- Factual and precise
- Small business focus (no "enterprise" or "teams" pricing)
- Emphasize epistemic humility and transparency
- Show technical depth without overwhelming

### Link Strategy
- Minimal duplication (each link appears once)
- Natural flow to deeper content
- Clear hierarchy: Overview → Details → Examples
- Internal anchors for long-form sections

### Mobile Responsiveness
- 4-column grids become 2x2 on mobile
- 3-column cards stack vertically
- Accordions work well on all screen sizes
- Hero section remains impactful on small screens
