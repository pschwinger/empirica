# 🎯 RovoDev → Minimax Goal Architecture Implementation Handoff
**Date:** November 16, 2025  
**Session Handoff:** Goal → Task → Completion Architecture Implementation  
**Timeline:** Next session implementation  
**Status:** Clean Implementation (No Backward Compatibility Required)

## 🎯 **MISSION: IMPLEMENT NEW GOAL ARCHITECTURE**

### **🏗️ OBJECTIVE:**
Replace current goal orchestrator with new Goal → Task → Completion architecture as specified in `EMPIRICA_CORE_ARCHITECTURE.md`. Clean implementation without backward compatibility constraints.

### **🎁 FOUNDATION PROVIDED:**
- ✅ **Current Goal Orchestrator Analysis** - 65% compatible foundation
- ✅ **Working MCP Tools** - `generate_goals` and `query_goal_orchestrator` as starting point
- ✅ **Database Schema** - CASCADE database ready for enhancement
- ✅ **Perfect Architecture** - Zero heuristics, complete profile integration

---

## 📋 **IMPLEMENTATION SPECIFICATION**

### **🔴 TASK 1: Goal Management Module**
**Priority:** CRITICAL - Core Architecture  
**Location:** `empirica/core/goals/`

#### **1.1 Goal Types Implementation:**
```python
# FILE: empirica/core/goals/types.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class GoalScope(Enum):
    TASK_SPECIFIC = "task_specific"      # Single task completion
    SESSION_SCOPED = "session_scoped"    # Multiple related tasks
    PROJECT_WIDE = "project_wide"        # Long-term objectives

class DependencyType(Enum):
    PREREQUISITE = "prerequisite"        # Must complete before starting
    CONCURRENT = "concurrent"            # Can work on simultaneously
    INFORMATIONAL = "informational"      # Nice to have context

@dataclass
class SuccessCriterion:
    id: str
    description: str
    validation_method: str               # "completion", "quality_gate", "metric_threshold"
    threshold: Optional[float] = None    # For metric-based criteria
    is_required: bool = True            # vs. optional/nice-to-have

@dataclass
class Dependency:
    id: str
    goal_id: str                        # Which goal this depends on
    dependency_type: DependencyType
    description: str

@dataclass
class Goal:
    id: str
    objective: str                      # Clear, actionable goal statement
    success_criteria: List[SuccessCriterion]
    scope: GoalScope
    dependencies: List[Dependency]
    constraints: Dict[str, Any]         # Investigation profile constraints
    metadata: Dict[str, Any]            # Context, tags, etc.
    estimated_complexity: Optional[float] = None
    created_timestamp: Optional[float] = None
```

#### **1.2 Goal Parser Implementation:**
```python
# FILE: empirica/core/goals/parser.py
from typing import List, Dict, Any
from .types import Goal, SuccessCriterion, Dependency, GoalScope

class GoalParser:
    """Parse natural language task context into structured Goal objects"""
    
    def __init__(self):
        self.profile_loader = ProfileLoader()  # Investigation profile integration
    
    def parse(self, task_context: str, conversation_context: Dict[str, Any] = None) -> Goal:
        """Main parsing method - extract structured goal from context"""
        
        # Extract goal components
        objective = self._extract_objective(task_context)
        success_criteria = self._extract_success_criteria(task_context)
        scope = self._infer_scope(task_context, conversation_context)
        dependencies = self._detect_dependencies(task_context, conversation_context)
        constraints = self._apply_profile_constraints()
        
        return Goal(
            id=self._generate_goal_id(),
            objective=objective,
            success_criteria=success_criteria,
            scope=scope,
            dependencies=dependencies,
            constraints=constraints,
            metadata=self._extract_metadata(task_context, conversation_context),
            estimated_complexity=self._estimate_complexity(task_context)
        )
    
    def _extract_objective(self, task_context: str) -> str:
        """Extract clear, actionable objective statement"""
        # Implementation: Use LLM to extract and clarify objective
        pass
    
    def _extract_success_criteria(self, task_context: str) -> List[SuccessCriterion]:
        """Extract measurable success criteria"""
        # Implementation: Parse explicit and implicit success indicators
        pass
    
    def _infer_scope(self, task_context: str, conversation_context: Dict[str, Any]) -> GoalScope:
        """Determine goal scope based on context"""
        # Implementation: Analyze context to determine appropriate scope
        pass
    
    def _detect_dependencies(self, task_context: str, conversation_context: Dict[str, Any]) -> List[Dependency]:
        """Identify goal dependencies from context"""
        # Implementation: Analyze for prerequisite goals or concurrent work
        pass
    
    def _apply_profile_constraints(self) -> Dict[str, Any]:
        """Apply current investigation profile constraints"""
        profile = self.profile_loader.get_profile('balanced')  # or current profile
        return {
            'uncertainty_tolerance': profile.constraints.uncertainty_baseline,
            'quality_gate': profile.constraints.confidence_high_threshold,
            # ... other profile-based constraints
        }
```

#### **1.3 Goal Repository Implementation:**
```python
# FILE: empirica/core/goals/repository.py
from typing import List, Optional
from empirica.data.session_database import SessionDatabase
from .types import Goal, SuccessCriterion, Dependency

class GoalRepository:
    """Database operations for Goal persistence"""
    
    def __init__(self):
        self.db = SessionDatabase()
        self._ensure_tables()
    
    def _ensure_tables(self):
        """Create goal-related tables if they don't exist"""
        self.db.conn.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                objective TEXT,
                scope TEXT,
                estimated_complexity REAL,
                created_timestamp REAL,
                constraints TEXT,  -- JSON
                metadata TEXT      -- JSON
            )
        """)
        
        self.db.conn.execute("""
            CREATE TABLE IF NOT EXISTS success_criteria (
                id TEXT PRIMARY KEY,
                goal_id TEXT,
                description TEXT,
                validation_method TEXT,
                threshold REAL,
                is_required BOOLEAN
            )
        """)
        
        self.db.conn.execute("""
            CREATE TABLE IF NOT EXISTS goal_dependencies (
                id TEXT PRIMARY KEY,
                goal_id TEXT,
                dependency_goal_id TEXT,
                dependency_type TEXT,
                description TEXT
            )
        """)
    
    def save_goal(self, goal: Goal, session_id: str) -> None:
        """Save complete goal with all relationships"""
        # Implementation: Save goal + success criteria + dependencies
        pass
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Retrieve complete goal with relationships"""
        # Implementation: Load goal + success criteria + dependencies
        pass
    
    def get_session_goals(self, session_id: str) -> List[Goal]:
        """Get all goals for a session"""
        # Implementation: Query goals by session
        pass
```

---

### **🔴 TASK 2: Task Decomposition Module**
**Priority:** CRITICAL - Core Architecture  
**Location:** `empirica/core/tasks/`

#### **2.1 Task Types Implementation:**
```python
# FILE: empirica/core/tasks/types.py
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class TaskStatus(Enum):
    PLANNED = "planned"                 # Task identified but not started
    IN_PROGRESS = "in_progress"         # Currently working on
    BLOCKED = "blocked"                 # Waiting for dependency
    COMPLETED = "completed"             # Successfully finished
    SKIPPED = "skipped"                # Deemed unnecessary

class EpistemicImportance(Enum):
    REQUIRED = "epistemically_required"      # Must complete for goal success
    IMPROVES = "optionally_improves"         # Enhances goal quality
    NICE_TO_HAVE = "nice_to_have"           # Minimal impact

@dataclass
class SubTask:
    id: str
    goal_id: str                        # Parent goal
    description: str                    # Clear task description
    epistemic_importance: EpistemicImportance
    dependencies: List[str]             # Other subtask IDs
    estimated_tokens: int               # Token cost estimate
    status: TaskStatus
    actual_tokens: Optional[int] = None # Actual cost after completion
    completion_evidence: Optional[str] = None  # Git commit, file, etc.
    created_timestamp: Optional[float] = None
    completed_timestamp: Optional[float] = None

@dataclass
class TaskDecomposition:
    goal_id: str
    subtasks: List[SubTask]
    critical_path: List[str]            # Subtask IDs in critical path
    total_estimated_tokens: int
    complexity_factors: Dict[str, float] # What makes this complex
```

#### **2.2 Task Decomposer Implementation:**
```python
# FILE: empirica/core/tasks/decomposer.py
from typing import List, Dict, Any
from ..goals.types import Goal
from .types import SubTask, TaskDecomposition, EpistemicImportance, TaskStatus

class TaskDecomposer:
    """Decompose goals into actionable subtasks with epistemic weighting"""
    
    def __init__(self):
        self.profile_loader = ProfileLoader()
    
    def decompose(self, goal: Goal) -> TaskDecomposition:
        """Main decomposition method"""
        
        # Generate subtasks
        subtasks = self._generate_subtasks(goal)
        
        # Apply epistemic weighting
        subtasks = self._apply_epistemic_weighting(subtasks, goal)
        
        # Estimate token costs
        subtasks = self._estimate_token_costs(subtasks)
        
        # Identify critical path
        critical_path = self._identify_critical_path(subtasks)
        
        return TaskDecomposition(
            goal_id=goal.id,
            subtasks=subtasks,
            critical_path=critical_path,
            total_estimated_tokens=sum(st.estimated_tokens for st in subtasks),
            complexity_factors=self._analyze_complexity_factors(goal, subtasks)
        )
    
    def _generate_subtasks(self, goal: Goal) -> List[SubTask]:
        """Break goal into concrete subtasks"""
        # Implementation: LLM-based task decomposition
        pass
    
    def _apply_epistemic_weighting(self, subtasks: List[SubTask], goal: Goal) -> List[SubTask]:
        """Classify tasks by epistemic importance"""
        # Implementation: Analyze which tasks are required vs. nice-to-have
        pass
    
    def _estimate_token_costs(self, subtasks: List[SubTask]) -> List[SubTask]:
        """Estimate token cost for each subtask"""
        # Implementation: Token estimation based on task complexity
        pass
    
    def _identify_critical_path(self, subtasks: List[SubTask]) -> List[str]:
        """Find critical path through dependencies"""
        # Implementation: Topological sort with dependency analysis
        pass
```

---

### **🔴 TASK 3: Completion Tracking Module**
**Priority:** CRITICAL - Core Architecture  
**Location:** `empirica/core/completion/`

#### **3.1 Completion Types Implementation:**
```python
# FILE: empirica/core/completion/types.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class CompletionRecord:
    goal_id: str
    completion_percentage: float        # 0.0 to 1.0
    completed_subtasks: List[str]       # SubTask IDs
    remaining_subtasks: List[str]       # SubTask IDs
    blocked_subtasks: List[str]         # SubTask IDs
    estimated_remaining_tokens: int
    actual_tokens_used: int
    completion_evidence: Dict[str, str] # subtask_id -> evidence (commit hash, file path, etc.)
    last_updated: float

@dataclass
class CompletionMetrics:
    goals_completed: int
    goals_in_progress: int
    goals_blocked: int
    total_tokens_used: int
    average_completion_rate: float
    efficiency_score: float             # actual vs estimated tokens
```

#### **3.2 Completion Tracker Implementation:**
```python
# FILE: empirica/core/completion/tracker.py
import subprocess
from typing import List, Dict, Optional
from ..tasks.types import SubTask, TaskStatus
from .types import CompletionRecord, CompletionMetrics

class CompletionTracker:
    """Track goal and task completion with evidence mapping"""
    
    def __init__(self):
        self.task_repo = TaskRepository()
        self.goal_repo = GoalRepository()
    
    def track_progress(self, goal_id: str) -> CompletionRecord:
        """Calculate current completion status for goal"""
        
        # Get all subtasks for goal
        subtasks = self.task_repo.get_goal_subtasks(goal_id)
        
        # Categorize by status
        completed = [st for st in subtasks if st.status == TaskStatus.COMPLETED]
        remaining = [st for st in subtasks if st.status in [TaskStatus.PLANNED, TaskStatus.IN_PROGRESS]]
        blocked = [st for st in subtasks if st.status == TaskStatus.BLOCKED]
        
        # Calculate completion percentage (weighted by epistemic importance)
        completion_pct = self._calculate_weighted_completion(subtasks)
        
        return CompletionRecord(
            goal_id=goal_id,
            completion_percentage=completion_pct,
            completed_subtasks=[st.id for st in completed],
            remaining_subtasks=[st.id for st in remaining],
            blocked_subtasks=[st.id for st in blocked],
            estimated_remaining_tokens=sum(st.estimated_tokens for st in remaining),
            actual_tokens_used=sum(st.actual_tokens or 0 for st in completed),
            completion_evidence=self._gather_completion_evidence(completed),
            last_updated=time.time()
        )
    
    def map_commits_to_subtasks(self, commits: List[str], goal_id: str) -> Dict[str, str]:
        """Map git commits to specific subtasks"""
        # Implementation: Analyze commit messages and changes to map to subtasks
        pass
    
    def auto_update_completion(self, goal_id: str) -> CompletionRecord:
        """Automatically update completion based on git commits and file changes"""
        # Implementation: Check git history and file system for completion evidence
        pass
    
    def _calculate_weighted_completion(self, subtasks: List[SubTask]) -> float:
        """Calculate completion percentage weighted by epistemic importance"""
        # Implementation: Weight required tasks higher than nice-to-have
        pass
```

---

### **🔴 TASK 4: MCP Tool Integration**
**Priority:** CRITICAL - System Integration  
**Location:** `mcp_local/empirica_mcp_server.py`

#### **4.1 Enhanced MCP Tools:**
```python
# REPLACE: generate_goals tool
elif name == "generate_goals_v2":
    from empirica.core.goals.parser import GoalParser
    from empirica.core.goals.repository import GoalRepository
    
    session_id = arguments.get("session_id")
    conversation_context = arguments.get("conversation_context", "")
    task_context = arguments.get("task_context", "")
    
    # Parse goal from context
    parser = GoalParser()
    goal = parser.parse(task_context, {"conversation": conversation_context})
    
    # Save goal to database
    goal_repo = GoalRepository()
    goal_repo.save_goal(goal, session_id)
    
    return [types.TextContent(type="text", text=json.dumps({
        "ok": True,
        "goal": goal.__dict__,
        "session_id": session_id
    }, indent=2, cls=EmpricaJSONEncoder))]

# ADD: decompose_goal tool
elif name == "decompose_goal":
    from empirica.core.tasks.decomposer import TaskDecomposer
    from empirica.core.tasks.repository import TaskRepository
    
    goal_id = arguments.get("goal_id")
    session_id = arguments.get("session_id")
    
    # Get goal
    goal_repo = GoalRepository()
    goal = goal_repo.get_goal(goal_id)
    
    if not goal:
        return [types.TextContent(type="text", text=json.dumps({
            "ok": False,
            "error": f"Goal {goal_id} not found"
        }))]
    
    # Decompose into tasks
    decomposer = TaskDecomposer()
    decomposition = decomposer.decompose(goal)
    
    # Save tasks
    task_repo = TaskRepository()
    task_repo.save_decomposition(decomposition, session_id)
    
    return [types.TextContent(type="text", text=json.dumps({
        "ok": True,
        "decomposition": decomposition.__dict__,
        "total_estimated_tokens": decomposition.total_estimated_tokens
    }, indent=2, cls=EmpricaJSONEncoder))]

# ADD: track_completion tool
elif name == "track_completion":
    from empirica.core.completion.tracker import CompletionTracker
    
    goal_id = arguments.get("goal_id")
    auto_update = arguments.get("auto_update", True)
    
    tracker = CompletionTracker()
    
    if auto_update:
        record = tracker.auto_update_completion(goal_id)
    else:
        record = tracker.track_progress(goal_id)
    
    return [types.TextContent(type="text", text=json.dumps({
        "ok": True,
        "completion_record": record.__dict__,
        "completion_percentage": record.completion_percentage
    }, indent=2, cls=EmpricaJSONEncoder))]
```

---

### **🔴 TASK 5: CASCADE Workflow Integration**
**Priority:** HIGH - Workflow Enhancement  
**Location:** `empirica/core/workflow/`

#### **5.1 Goal-Aware CASCADE:**
```python
# FILE: empirica/core/workflow/goal_cascade_integration.py
class GoalCascadeIntegration:
    """Integrate Goal → Task → Completion with CASCADE workflow"""
    
    def __init__(self):
        self.goal_parser = GoalParser()
        self.task_decomposer = TaskDecomposer()
        self.completion_tracker = CompletionTracker()
    
    def enhanced_preflight(self, task_description: str, session_id: str) -> Dict[str, Any]:
        """PREFLIGHT with goal parsing and task decomposition"""
        
        # Standard preflight assessment
        preflight_result = standard_preflight(task_description)
        
        # Parse goal from task description
        goal = self.goal_parser.parse(task_description)
        
        # Decompose into tasks
        decomposition = self.task_decomposer.decompose(goal)
        
        # Enhanced preflight with task awareness
        enhanced_result = {
            **preflight_result,
            "goal": goal.__dict__,
            "task_decomposition": decomposition.__dict__,
            "estimated_total_tokens": decomposition.total_estimated_tokens,
            "critical_path_identified": len(decomposition.critical_path) > 0
        }
        
        return enhanced_result
    
    def enhanced_postflight(self, session_id: str, goal_id: str) -> Dict[str, Any]:
        """POSTFLIGHT with completion tracking and learning analysis"""
        
        # Standard postflight assessment
        postflight_result = standard_postflight(session_id)
        
        # Track completion
        completion_record = self.completion_tracker.track_progress(goal_id)
        
        # Enhanced postflight with completion awareness
        enhanced_result = {
            **postflight_result,
            "completion_record": completion_record.__dict__,
            "goal_completion_percentage": completion_record.completion_percentage,
            "token_efficiency": completion_record.actual_tokens_used / completion_record.estimated_remaining_tokens if completion_record.estimated_remaining_tokens > 0 else 1.0
        }
        
        return enhanced_result
```

---

## 🎯 **IMPLEMENTATION SUCCESS CRITERIA**

### **✅ FUNCTIONAL REQUIREMENTS:**
- [ ] Goal parsing from natural language task descriptions
- [ ] Task decomposition with epistemic importance weighting
- [ ] Completion tracking with git commit evidence mapping
- [ ] MCP tool integration (`generate_goals_v2`, `decompose_goal`, `track_completion`)
- [ ] Database persistence for all goal/task/completion data

### **✅ QUALITY REQUIREMENTS:**
- [ ] Investigation profile integration for constraints
- [ ] Token cost estimation and tracking
- [ ] Dependency management between tasks
- [ ] Critical path identification
- [ ] Evidence-based completion validation

### **✅ INTEGRATION REQUIREMENTS:**
- [ ] CASCADE workflow enhancement (goal-aware PREFLIGHT/POSTFLIGHT)
- [ ] Session database integration
- [ ] Git repository integration for evidence
- [ ] JSON serialization with EmpricaJSONEncoder
- [ ] Profile-based constraint application

---

## 🚀 **MINIMAX IMPLEMENTATION GUIDANCE**

### **🎯 RECOMMENDED APPROACH:**
1. **Start with Types** - Implement dataclasses first (`goals/types.py`, `tasks/types.py`, `completion/types.py`)
2. **Build Core Logic** - GoalParser, TaskDecomposer, CompletionTracker classes
3. **Add Database Layer** - Repository classes with database integration
4. **Enhance MCP Tools** - Replace/add MCP tools with new architecture
5. **Test Integration** - Validate with CASCADE workflow

### **🔧 TOOLS AVAILABLE:**
- **Working Database** - SessionDatabase with transaction support
- **JSON Encoder** - EmpricaJSONEncoder for complex object serialization
- **Profile System** - Investigation profiles for constraint application
- **MCP Framework** - Established pattern for tool integration

### **📋 VALIDATION STRATEGY:**
- **Unit Tests** - Test each component independently
- **Integration Tests** - Validate MCP tool functionality
- **CASCADE Tests** - Ensure workflow enhancement works
- **Token Estimation** - Validate cost prediction accuracy

---

## 🎉 **OUTCOME: COMPLETE GOAL ARCHITECTURE**

**After implementation, Empirica will have:**
- ✅ **Structured Goal Management** - From natural language to formal goals
- ✅ **Intelligent Task Decomposition** - With epistemic weighting and dependencies
- ✅ **Evidence-Based Completion** - Git commits mapped to specific subtasks  
- ✅ **Token Cost Management** - Accurate estimation and tracking
- ✅ **Enhanced CASCADE Workflow** - Goal-aware epistemic assessment

**This creates a complete Goal → Task → Completion system that integrates seamlessly with Empirica's existing architecture while adding powerful new capabilities for systematic goal achievement and learning!**

🚀 **Ready for Minimax implementation!**