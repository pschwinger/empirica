# API Reference

Complete reference for the Empirica Python API. This documentation covers core modules, CASCADE phases, configuration classes, and integration interfaces.

---

## Quick Reference

### Essential Imports

```python
# Core classes
from empirica import CanonicalEpistemicCascade, run_cascade
from empirica.config import EmpiricaConfig
from empirica.types import Task, Context, EpistemicVectors

# Individual phases
from empirica.core.canonical.preflight import PreflightAssessment
from empirica.core.canonical.investigate import InvestigationPhase  
from empirica.core.canonical.check import CheckAssessment
from empirica.core.canonical.act import ActionExecution
from empirica.core.canonical.postflight import PostflightLearning

# Advanced features
from empirica.bayesian.guardian import BayesianGuardian
from empirica.drift.monitor import DriftMonitor
from empirica.investigation.strategy import InvestigationStrategy
```

### Most Common Usage Patterns

```python
# Simple workflow
result = await run_cascade("your task", domain="code_analysis")

# Full configuration
cascade = CanonicalEpistemicCascade(
    config=config,
    enable_bayesian=True,
    enable_drift_monitor=True
)
result = await cascade.run_cascade(task)

# MCP integration
from empirica.mcp.server import EmpiricaMCPServer
```

---

## Core Classes

### CanonicalEpistemicCascade

The main class for running complete epistemic reasoning workflows.

```python
class CanonicalEpistemicCascade:
    """Complete CASCADE workflow implementation"""
    
    def __init__(
        self,
        config: Optional[EmpiricaConfig] = None,
        enable_bayesian: bool = False,
        enable_drift_monitor: bool = False,
        enable_tracking: bool = True,
        enable_visualization: bool = False
    ):
        """Initialize CASCADE with optional features"""
    
    async def run_cascade(
        self, 
        task: Union[str, Task],
        context: Optional[Context] = None,
        domain: Optional[str] = None
    ) -> CascadeResult:
        """Execute complete CASCADE workflow"""
    
    async def preflight_assessment(self, task: Task) -> PreflightResult:
        """Execute PREFLIGHT phase"""
    
    async def investigate_uncertainty(
        self, 
        preflight: PreflightResult,
        investigation_config: Optional[InvestigationConfig] = None
    ) -> InvestigationResult:
        """Execute INVESTIGATE phase"""
    
    async def check_confidence(
        self,
        investigation: InvestigationResult,
        confidence_threshold: float = 0.7
    ) -> CheckResult:
        """Execute CHECK phase"""
    
    async def execute_action(
        self,
        check: CheckResult,
        action_config: Optional[ActionConfig] = None
    ) -> ActionResult:
        """Execute ACT phase"""
    
    async def postflight_learning(
        self,
        full_results: CascadeResult
    ) -> LearningResult:
        """Execute POSTFLIGHT phase"""
```

**Parameters:**
- `config`: Complete system configuration
- `enable_bayesian`: Enable Bayesian belief tracking
- `enable_drift_monitor`: Enable drift detection
- `enable_tracking`: Enable data persistence
- `enable_visualization`: Enable real-time dashboard

**Returns:** `CascadeResult` with confidence, recommendations, learning deltas

### Task & Context

```python
@dataclass
class Task:
    """Represents a task to be assessed"""
    description: str
    context: Optional[Context] = None
    domain: Optional[str] = None
    requirements: Optional[List[str]] = None
    constraints: Optional[Dict[str, Any]] = None
    priority: Optional[TaskPriority] = None

@dataclass  
class Context:
    """Task execution context"""
    files: Optional[List[str]] = None
    environment: Optional[Dict[str, Any]] = None
    capabilities: Optional[List[str]] = None
    history: Optional[List[Dict]] = None
    metadata: Optional[Dict[str, Any]] = None
```

---

## CASCADE Phases

### 1. PREFLIGHT Assessment

```python
class PreflightAssessment:
    """Initial epistemic state assessment"""
    
    async def assess_task(
        self, 
        task: Task,
        epistemic_vectors: EpistemicVectors = EpistemicVectors.ALL_13
    ) -> PreflightResult:
        """Assess task across 13 epistemic dimensions"""
    
    def validate_engagement_threshold(self, engagement: float) -> bool:
        """Check if engagement meets minimum threshold (0.6)"""

@dataclass
class PreflightResult:
    """Results from PREFLIGHT assessment"""
    session_id: str
    epistemic_state: Dict[str, float]  # 13 vector values
    engagement: float
    uncertainty: float
    confidence: float
    recommendation: str  # "proceed" | "investigate" | "clarify"
    gaps_identified: List[str]
    investigation_needed: bool
```

**Example:**
```python
preflight = PreflightAssessment()
result = await preflight.assess_task(
    task=Task("Analyze security vulnerabilities"),
    epistemic_vectors=EpistemicVectors.FOUNDATION_PLUS_UNCERTAINTY
)

if result.engagement < 0.6:
    print("Task engagement too low - seek clarification")
elif result.uncertainty > 0.4:
    print("High uncertainty - investigation recommended")
else:
    print("Ready to proceed")
```

### 2. INVESTIGATE Phase

```python
class InvestigationPhase:
    """Strategic knowledge gathering phase"""
    
    async def investigate_gaps(
        self,
        gaps: List[str],
        investigation_strategy: InvestigationStrategy,
        context: Context
    ) -> InvestigationResult:
        """Execute investigation based on identified gaps"""
    
    async def select_investigation_strategy(
        self,
        domain: str,
        gaps: List[str],
        context: Context
    ) -> InvestigationStrategy:
        """Select appropriate investigation strategy"""

@dataclass
class InvestigationResult:
    """Results from investigation phase"""
    findings: List[InvestigationFinding]
    uncertainty_reduction: float
    new_knowledge_areas: List[str]
    tool_recommendations: List[str]
    investigation_quality: float
    time_spent: float
    resources_used: List[str]

@dataclass
class InvestigationFinding:
    """Individual finding from investigation"""
    area: str
    confidence: float
    findings: List[str]
    sources: List[str]
    reliability_score: float
```

**Example:**
```python
investigation = InvestigationPhase()
strategy = await investigation.select_investigation_strategy(
    domain="security",
    gaps=["vulnerability_patterns", "compliance_requirements"],
    context=task.context
)

result = await investigation.investigate_gaps(
    gaps=preflight.gaps_identified,
    investigation_strategy=strategy,
    context=task.context
)

print(f"Uncertainty reduced by {result.uncertainty_reduction:.2f}")
```

### 3. CHECK Phase

```python
class CheckAssessment:
    """Confidence validation and risk assessment"""
    
    async def validate_confidence(
        self,
        preflight: PreflightResult,
        investigation: InvestigationResult,
        bayesian_guardian: Optional[BayesianGuardian] = None
    ) -> CheckResult:
        """Validate confidence against evidence"""
    
    async def assess_risks(
        self,
        proposed_action: str,
        context: Context,
        epistemic_state: Dict[str, float]
    ) -> RiskAssessment:
        """Assess risks of proposed action"""

@dataclass
class CheckResult:
    """Results from CHECK phase"""
    validated_confidence: float
    risk_assessment: RiskAssessment
    bayesian_updates: Dict[str, float]
    drift_detection: Optional[DriftReport]
    recommendation: ActionRecommendation
    required_confidence: float
    uncertainty_tolerance: float

@dataclass
class RiskAssessment:
    """Risk evaluation for action"""
    overall_risk: float
    risk_factors: List[RiskFactor]
    mitigation_strategies: List[str]
    confidence_intervals: Dict[str, Tuple[float, float]]
```

**Example:**
```python
check = CheckAssessment()
result = await check.validate_confidence(
    preflight=preflight,
    investigation=investigation,
    bayesian_guardian=guardian
)

if result.validated_confidence > 0.7:
    print("Confidence validated - safe to proceed")
else:
    print(f"Confidence too low ({result.validated_confidence:.2f}) - seek more information")
```

### 4. ACT Phase

```python
class ActionExecution:
    """Execute actions with confidence tracking"""
    
    async def execute_with_tracking(
        self,
        action: ActionRecommendation,
        cascade_context: CascadeContext,
        tracking_enabled: bool = True
    ) -> ActionResult:
        """Execute action with full tracking"""
    
    async def validate_action_completion(
        self,
        expected_outcomes: List[str],
        actual_outcomes: List[str]
    ) -> CompletionValidation:
        """Validate action completion against expectations"""

@dataclass
class ActionResult:
    """Results from action execution"""
    action_type: str
    execution_success: bool
    outcomes_achieved: List[str]
    confidence_actual: float
    time_to_execution: float
    unexpected_issues: List[str]
    next_recommendations: List[str]

@dataclass
class ActionRecommendation:
    """Recommended action with confidence"""
    action_description: str
    confidence_required: float
    expected_outcomes: List[str]
    risk_mitigation: List[str]
    resources_required: List[str]
```

### 5. POSTFLIGHT Phase

```python
class PostflightLearning:
    """Learning and calibration after action completion"""
    
    async def assess_learning_delta(
        self,
        initial_state: PreflightResult,
        final_state: Dict[str, float],
        actual_outcomes: List[str]
    ) -> LearningResult:
        """Calculate learning from CASCADE execution"""
    
    async def update_calibration(
        self,
        predicted_confidence: float,
        actual_accuracy: float,
        domain: str
    ) -> CalibrationUpdate:
        """Update confidence calibration model"""

@dataclass
class LearningResult:
    """Learning assessment results"""
    epistemic_delta: Dict[str, float]  # Changes in each vector
    uncertainty_improvement: float
    calibration_quality: float
    key_learnings: List[str]
    confidence_accuracy: float
    domain_specific_insights: List[str]
```

---

## Configuration System

### EmpiricaConfig

```python
@dataclass
class EmpiricaConfig:
    """Complete system configuration"""
    
    # Core settings
    epistemic_vectors: EpistemicVectors = EpistemicVectors.ALL_13
    confidence_threshold: float = 0.7
    engagement_threshold: float = 0.6
    uncertainty_tolerance: float = 0.3
    
    # CASCADE settings
    cascade: CascadeConfig = field(default_factory=CascadeConfig)
    
    # Tracking settings
    tracking: TrackingConfig = field(default_factory=TrackingConfig)
    
    # Visualization settings
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    
    # Security settings
    security: SecurityConfig = field(default_factory=SecurityConfig)

@dataclass
class CascadeConfig:
    """CASCADE workflow configuration"""
    auto_investigate: bool = True
    investigation_timeout: float = 300.0  # 5 minutes
    max_investigation_cycles: int = 3
    enable_bayesian_guardian: bool = False
    enable_drift_monitor: bool = False
    enable_action_hooks: bool = False
    parallel_investigation: bool = True

@dataclass
class TrackingConfig:
    """Data tracking configuration"""
    enable_sqlite: bool = True
    enable_json_logs: bool = True
    enable_reflex_frames: bool = True
    session_retention: str = "30d"
    performance_tracking: bool = True
    auto_cleanup: bool = True
```

**Example Configuration:**
```python
config = EmpiricaConfig(
    epistemic_vectors=EpistemicVectors.FOUNDATION_PLUS_UNCERTAINTY,
    confidence_threshold=0.8,
    cascade=CascadeConfig(
        auto_investigate=True,
        investigation_timeout=600.0,
        enable_bayesian_guardian=True
    ),
    tracking=TrackingConfig(
        enable_sqlite=True,
        session_retention="90d"
    )
)
```

---

## Advanced Features

### BayesianGuardian

```python
class BayesianGuardian:
    """Evidence-based belief tracking"""
    
    def __init__(self, prior_strength: float = 0.1):
        self.prior_strength = prior_strength
        self.beliefs: Dict[str, BeliefState] = {}
    
    async def update_belief(
        self,
        proposition: str,
        evidence: float,
        evidence_strength: float = 1.0
    ) -> BeliefUpdate:
        """Update belief based on new evidence"""
    
    def check_against_evidence(
        self,
        belief: str,
        new_evidence: List[float]
    ) -> EvidenceCheck:
        """Check belief consistency with new evidence"""
    
    def get_calibration_confidence(
        self,
        proposition: str
    ) -> float:
        """Get confidence based on calibration model"""

@dataclass
class BeliefState:
    """Current state of a belief"""
    proposition: str
    current_belief: float
    evidence_count: int
    last_update: datetime
    calibration_quality: float

@dataclass
class BeliefUpdate:
    """Result of belief update"""
    old_belief: float
    new_belief: float
    evidence_strength: float
    confidence_adjustment: float
```

### DriftMonitor

```python
class DriftMonitor:
    """Behavioral integrity monitoring"""
    
    def __init__(self, baseline_window: int = 50):
        self.baseline_window = baseline_window
        self.behavioral_baseline: Dict[str, float] = {}
        self.drift_history: List[DriftEvent] = []
    
    async def assess_response(
        self,
        response: str,
        context: Dict[str, Any],
        expected_behavior: Optional[Dict[str, float]] = None
    ) -> DriftAssessment:
        """Assess response for behavioral drift"""
    
    def detect_sycophancy_drift(
        self,
        conversation_history: List[Dict]
    ) -> SycophancyReport:
        """Detect excessive agreement patterns"""
    
    def analyze_tension_avoidance(
        self,
        discussion_topics: List[str],
        ai_responses: List[str]
    ) -> TensionAnalysis:
        """Analyze avoidance of challenging topics"""

@dataclass
class DriftAssessment:
    """Assessment of behavioral drift"""
    drift_score: float  # 0.0 = no drift, 1.0 = severe drift
    drift_type: DriftType
    confidence: float
    recommendations: List[str]
    behavioral_indicators: Dict[str, float]
```

---

## MCP Integration

### EmpiricaMCPServer

```python
class EmpiricaMCPServer:
    """Model Context Protocol server for Empirica"""
    
    def __init__(self, config: EmpiricaConfig):
        self.config = config
        self.cascade_instance: Optional[CanonicalEpistemicCascade] = None
    
    async def start_server(
        self,
        host: str = "localhost",
        port: int = 8765
    ):
        """Start MCP server"""
    
    async def stop_server(self):
        """Stop MCP server"""
    
    def get_available_tools(self) -> List[MCPTool]:
        """Get list of available MCP tools"""

# Available MCP Tools (39 total)
MCP_TOOLS = [
    "bootstrap_session", "execute_preflight", "execute_postflight",
    "create_goal", "add_subtask", "complete_subtask",
    "get_epistemic_state", "get_calibration_report",
    "execute_check", "submit_check_assessment",
    "create_cascade", "get_session_summary",
    # ... and 26 more tools
]

**New in v2.0:**
- **Goal Management**: `create_goal` now accepts `ScopeVector` (3D: breadth, duration, coordination) instead of categorical enum
- **Cross-AI Coordination**: `discover_goals`, `resume_goal` for multi-agent collaboration
- **Decision Logic**: Automatic comprehension + foundation checks guide AI behavior
- **MCO Integration**: Dynamic threshold configuration via YAML personas

See [20_TOOL_CATALOG.md](../docs/production/20_TOOL_CATALOG.md) for complete tool reference.

---

## Plugin System

### EmpiricaPlugin

```python
class EmpiricaPlugin:
    """Base class for Empirica plugins"""
    
    name: str
    description: str
    version: str
    dependencies: List[str] = []
    
    async def initialize(self, config: Dict[str, Any]):
        """Plugin initialization"""
    
    async def execute_investigation(
        self,
        gap: str,
        context: Context,
        investigation_config: InvestigationConfig
    ) -> InvestigationResult:
        """Custom investigation logic"""
    
    def explain_recommendations(
        self,
        recommendations: List[str],
        epistemic_context: Dict[str, float]
    ) -> str:
        """Generate LLM explanation for recommendations"""

# Plugin registration
def register_plugin(plugin_class: Type[EmpiricaPlugin]):
    """Register plugin with Empirica"""
    EmpiricaPluginRegistry.register(plugin_class)

def get_plugin(plugin_name: str) -> Optional[EmpiricaPlugin]:
    """Get registered plugin by name"""
    return EmpiricaPluginRegistry.get(plugin_name)
```

**Example Plugin:**
```python
class SecurityAnalysisPlugin(EmpiricaPlugin):
    name = "security_analysis"
    description = "Security vulnerability detection"
    version = "1.0.0"
    
    async def execute_investigation(
        self,
        gap: str,
        context: Context,
        config: InvestigationConfig
    ) -> InvestigationResult:
        if gap == "security_vulnerabilities":
            # Custom security analysis logic
            return InvestigationResult(...)
    
    def explain_recommendations(
        self,
        recommendations: List[str],
        epistemic_context: Dict[str, float]
    ) -> str:
        return f"Based on security analysis: {', '.join(recommendations)}"

# Register plugin
register_plugin(SecurityAnalysisPlugin)
```

---

## Data Models

### EpistemicVectors

```python
class EpistemicVectors(Enum):
    """Available epistemic assessment vectors"""
    
    # Foundation (35% weight)
    KNOW = "know"
    DO = "do"  
    CONTEXT = "context"
    
    # Comprehension (25% weight)
    CLARITY = "clarity"
    COHERENCE = "coherence"
    SIGNAL = "signal"
    DENSITY = "density"
    
    # Execution (25% weight)
    STATE = "state"
    CHANGE = "change"
    COMPLETION = "completion"
    IMPACT = "impact"
    
    # Meta-epistemic
    UNCERTAINTY = "uncertainty"
    ENGAGEMENT = "engagement"
    CALIBRATION = "calibration"
    
    # Convenience combinations
    FOUNDATION = ["know", "do", "context"]
    COMPREHENSION = ["clarity", "coherence", "signal", "density"]
    EXECUTION = ["state", "change", "completion", "impact"]
    META = ["uncertainty", "engagement", "calibration"]
    ALL_13 = FOUNDATION + COMPREHENSION + EXECUTION + META
```

### CascadeResult

```python
@dataclass
class CascadeResult:
    """Complete results from CASCADE execution"""
    
    session_id: str
    task_description: str
    domain: Optional[str]
    
    # Overall results
    confidence: float
    uncertainty: float
    recommendation: str
    
    # Phase results
    preflight_result: Optional[PreflightResult]
    investigation_result: Optional[InvestigationResult]
    check_result: Optional[CheckResult]
    action_result: Optional[ActionResult]
    learning_result: Optional[LearningResult]
    
    # Metadata
    execution_time: float
    total_cycles: int
    tools_used: List[str]
    epistemic_trajectory: List[Dict[str, float]]
    confidence_evolution: List[Tuple[float, float]]  # (time, confidence)
```

---

## Error Handling

### Custom Exceptions

```python
class EmpiricaError(Exception):
    """Base exception for Empirica"""
    pass

class CascadeError(EmpiricaError):
    """CASCADE execution error"""
    pass

class EpistemicAssessmentError(EmpiricaError):
    """Error in epistemic assessment"""
    pass

class InvestigationError(EmpiricaError):
    """Error during investigation phase"""
    pass

class ConfidenceValidationError(EmpiricaError):
    """Error in confidence validation"""
    pass

class PluginError(EmpiricaError):
    """Plugin-related error"""
    pass
```

### Error Handling Patterns

```python
try:
    result = await cascade.run_cascade(task)
except CascadeError as e:
    logger.error(f"CASCADE execution failed: {e}")
    return CascadeResult(error=str(e), confidence=0.0)
except EpistemicAssessmentError as e:
    logger.warning(f"Assessment issue: {e}")
    # Fall back to default assessment
    result = await cascade.run_cascade(task, use_defaults=True)
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise
```

---

## Performance & Monitoring

### Performance Metrics

```python
@dataclass
class PerformanceMetrics:
    """Performance measurement results"""
    
    assessment_time: float
    investigation_time: float
    validation_time: float
    action_time: float
    total_time: float
    
    memory_usage: Dict[str, int]
    cpu_usage: float
    api_calls: int
    cache_hits: int
    cache_misses: int

class PerformanceMonitor:
    """Monitor Empirica performance"""
    
    def start_assessment_timer(self):
        """Start timing assessment phase"""
    
    def record_investigation_performance(
        self, 
        investigation_id: str, 
        duration: float
    ):
        """Record investigation performance"""
    
    def get_metrics_summary(self) -> PerformanceMetrics:
        """Get performance metrics summary"""
```

---

## Best Practices

### 1. Configuration Management

```python
# Use configuration objects for consistent setup
config = EmpiricaConfig(
    confidence_threshold=0.8,  # Higher for production
    cascade=CascadeConfig(
        auto_investigate=True,
        investigation_timeout=300.0
    )
)

cascade = CanonicalEpistemicCascade(config=config)
```

### 2. Error Handling

```python
# Always handle CASCADE errors gracefully
async def safe_cascade_execution(task: Task) -> Optional[CascadeResult]:
    try:
        result = await cascade.run_cascade(task)
        if result.confidence < 0.5:
            logger.warning(f"Low confidence result: {result.confidence}")
        return result
    except CascadeError as e:
        logger.error(f"CASCADE failed: {e}")
        return None
```

### 3. Performance Optimization

```python
# Enable caching for repeated assessments
config = EmpiricaConfig(
    caching=CacheConfig(
        enable_epistemic_cache=True,
        cache_size=1000,
        ttl=3600  # 1 hour
    )
)

# Use appropriate epistemic vectors for your domain
if domain == "code_analysis":
    vectors = EpistemicVectors.FOUNDATION + [EpistemicVectors.UNCERTAINTY]
else:
    vectors = EpistemicVectors.ALL_13
```

### 4. Memory Management

```python
# Clean up resources after use
async def with_cascade_session():
    cascade = CanonicalEpistemicCascade()
    try:
        result = await cascade.run_cascade(task)
        return result
    finally:
        await cascade.cleanup()
```

---

*This API reference covers the complete Empirica interface. For more specific examples and advanced usage patterns, see the [Examples Gallery](examples/) and [Plugin Development Guide](plugin-development.md).*