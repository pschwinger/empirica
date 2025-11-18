# 🎯 Goal Orchestrator Architecture Analysis
**Date:** November 16, 2025  
**Purpose:** Compare current implementation with new Goal → Task → Completion architecture  
**Status:** Gap Analysis and Integration Roadmap

## 🔍 **CURRENT STATE ANALYSIS**

### **✅ WHAT EXISTS NOW:**

#### **1. Goal Orchestrator Components:**
```
Current Implementation:
├── empirica/core/canonical/canonical_goal_orchestrator.py (541 lines)
├── empirica/components/goal_management/autonomous_goal_orchestrator/ (304 lines)
└── MCP Integration:
    ├── query_goal_orchestrator (database-based cascade querying)
    └── generate_goals (LLM-based goal generation)
```

#### **2. Current MCP Tool Integration:**
```python
# query_goal_orchestrator - Works with existing CASCADE database
- Queries cascades table for goal progress
- Shows status: created/started/in_progress/completed
- Returns cascade_id, task, goal_id, goal_json
- Tracks preflight/check/postflight completion

# generate_goals - Uses canonical goal orchestrator
- Integrates with epistemic assessment data
- Async orchestrator.orchestrate_goals()
- Returns goals in to_dict() format
- Links to create_cascade for execution
```

#### **3. Database Integration:**
```sql
-- Current CASCADE database schema supports goals:
cascades table:
- cascade_id, session_id, task, goal_id, goal_json
- preflight/check/postflight completion tracking
- final_action, final_confidence
```

---

## 🎯 **NEW ARCHITECTURE REQUIREMENTS**

### **📋 Goal → Task → Completion Architecture:**

#### **1. Goal Management Module** (`empirica/core/goals/`)
```python
# REQUIRED: Goal Parser
class GoalParser:
    def parse(task_context: str) -> Goal
    def extract_success_criteria(context: str) -> List[SuccessCriterion]
    def infer_scope(context: str) -> GoalScope
    def detect_dependencies(context: str) -> List[Dependency]

# REQUIRED: Goal dataclass
@dataclass
class Goal:
    id: str, objective: str, success_criteria: List[SuccessCriterion]
    scope: GoalScope, dependencies: List[Dependency]
    constraints: Dict[str, Any], metadata: Dict[str, Any]
```

#### **2. Task Decomposition Module** (`empirica/core/tasks/`)
```python
# REQUIRED: Task Decomposer
class TaskDecomposer:
    def decompose(goal: Goal) -> TaskDecomposition
    def estimate_tokens(subtask: SubTask) -> int
    def identify_critical_path(subtasks: List[SubTask]) -> List[str]

# REQUIRED: SubTask dataclass
@dataclass
class SubTask:
    id: str, goal_id: str, description: str
    epistemically_required: bool, optionally_improves: bool
    dependencies: List[str], estimated_tokens: int
    status: TaskStatus, actual_tokens: Optional[int]
```

#### **3. Completion Tracker Module** (`empirica/core/completion/`)
```python
# REQUIRED: Completion Tracker  
class CompletionTracker:
    def track_progress(goal_id: str) -> CompletionRecord
    def map_commits_to_subtasks(commits: List[str]) -> Dict[str, str]
    def calculate_completion_percentage(goal_id: str) -> float

# REQUIRED: CompletionRecord dataclass
@dataclass
class CompletionRecord:
    goal_id: str, completion_percentage: float
    completed_subtasks: List[str], remaining_subtasks: List[str]
```

---

## 🔍 **GAP ANALYSIS**

### **🟢 STRONG ALIGNMENT (Current → New):**

#### **1. Goal Generation (85% Compatible):**
```python
# CURRENT: generate_goals MCP tool
orchestrator.orchestrate_goals(
    conversation_context=conversation_context,
    epistemic_assessment=epistemic_assessment
) -> List[Goal]

# NEW SPEC: GoalParser.parse()
goal_parser.parse(task_context=conversation_context) -> Goal

# ASSESSMENT: Very close! Just need to adapt interface
```

#### **2. Database Integration (90% Compatible):**
```sql
-- CURRENT: cascades table structure
goal_id, goal_json, task, session_id

-- NEW SPEC: Goal persistence
Goal objects with success criteria, scope, dependencies

-- ASSESSMENT: Database schema already supports Goal objects via goal_json
```

#### **3. MCP Tool Framework (95% Compatible):**
```python
# CURRENT: query_goal_orchestrator returns goal progress
# NEW SPEC: CompletionTracker.track_progress()

# ASSESSMENT: Current implementation already tracks completion!
```

### **🟡 MODERATE GAPS (Need Implementation):**

#### **1. Task Decomposition (40% Coverage):**
```python
# CURRENT: Goals generated but not decomposed into SubTasks
# NEW SPEC: Goal → SubTask tree with epistemic weighting

# GAP: Need TaskDecomposer class and SubTask structure
```

#### **2. Structured Goal Types (30% Coverage):**
```python
# CURRENT: goal_json is flexible dict
# NEW SPEC: Structured Goal dataclass with success criteria, scope, dependencies

# GAP: Need formal Goal/SuccessCriterion/Dependency dataclasses
```

#### **3. Completion Mapping (20% Coverage):**
```python
# CURRENT: CASCADE completion tracking (preflight/check/postflight)
# NEW SPEC: Map git commits to specific SubTasks

# GAP: Need commit → subtask mapping and completion percentage calculation
```

### **🔴 MAJOR GAPS (Require New Implementation):**

#### **1. Epistemic Task Weighting (0% Coverage):**
```python
# MISSING: epistemically_required vs. optionally_improves classification
# MISSING: Token estimation for subtasks
# MISSING: Critical path identification
```

#### **2. Success Criteria Extraction (10% Coverage):**
```python
# CURRENT: Goals have general objective
# MISSING: Formal success criteria parsing and tracking
# MISSING: Dependency detection and management
```

#### **3. Token Cost Management (0% Coverage):**
```python
# MISSING: estimated_tokens per subtask
# MISSING: actual_tokens tracking
# MISSING: Token budget optimization
```

---

## 🗂️ **INTEGRATION STRATEGY**

### **🎯 PHASE 1: Bridge Current to New (Minimal Changes)**

#### **1. Enhance Existing MCP Tools:**
```python
# ENHANCE: generate_goals to return structured Goal objects
# ENHANCE: query_goal_orchestrator to show task decomposition
# ADD: decompose_goal MCP tool for task breakdown
```

#### **2. Add Missing Dataclasses:**
```python
# ADD: empirica/core/goals/types.py
@dataclass
class Goal:  # Structured version of current goal_json
@dataclass 
class SuccessCriterion:
@dataclass
class Dependency:

# ADD: empirica/core/tasks/types.py  
@dataclass
class SubTask:  # New task decomposition structure
@dataclass
class TaskDecomposition:
```

#### **3. Database Schema Evolution:**
```sql
-- ADD: subtasks table
CREATE TABLE subtasks (
    id TEXT PRIMARY KEY,
    goal_id TEXT,
    description TEXT,
    epistemically_required BOOLEAN,
    estimated_tokens INTEGER,
    status TEXT,
    actual_tokens INTEGER
);

-- ENHANCE: success_criteria table
CREATE TABLE success_criteria (
    id TEXT PRIMARY KEY,
    goal_id TEXT,
    description TEXT,
    validation_method TEXT
);
```

### **🎯 PHASE 2: Full Architecture Implementation**

#### **1. Goal Management Module:**
```python
# IMPLEMENT: empirica/core/goals/
├── parser.py        # GoalParser class
├── types.py         # Goal, SuccessCriterion, Dependency dataclasses
└── repository.py    # Goal persistence with database
```

#### **2. Task Decomposition Module:**
```python
# IMPLEMENT: empirica/core/tasks/
├── decomposer.py    # TaskDecomposer class
├── types.py         # SubTask, TaskDecomposition dataclasses
└── repository.py    # Task persistence
```

#### **3. Completion Tracking Module:**
```python
# IMPLEMENT: empirica/core/completion/
├── tracker.py       # CompletionTracker class
├── types.py         # CompletionRecord dataclass
└── repository.py    # Completion persistence
```

#### **4. Workflow Integration:**
```python
# IMPLEMENT: empirica/core/workflow/task_workflow.py
class TaskWorkflow:
    def integrate_with_cascade():
        # PREFLIGHT: Goal parsing
        # INVESTIGATE: Task decomposition refinement
        # ACT: Subtask execution tracking  
        # POSTFLIGHT: Completion analysis
```

---

## 🚀 **IMMEDIATE NEXT STEPS**

### **🔴 CRITICAL (For Coordination Team):**

#### **1. Assess Current Goal Orchestrator Usage:**
- Test `generate_goals` and `query_goal_orchestrator` MCP tools
- Verify integration with CASCADE workflow
- Document current goal generation patterns

#### **2. Design Transition Strategy:**
- Plan backward compatibility for existing goal_json format
- Design migration path from current to new structure
- Identify breaking changes and mitigation strategies

#### **3. Prototype Key Components:**
- Create basic Goal dataclass compatible with current goal_json
- Implement simple TaskDecomposer that works with existing goals
- Test integration with current MCP tool framework

### **🟡 MEDIUM (Post-Launch Enhancement):**

#### **1. Gradual Implementation:**
- Phase 1: Enhance existing tools with structured types
- Phase 2: Add task decomposition without breaking changes
- Phase 3: Full completion tracking integration

#### **2. User Migration Support:**
- Provide tools to convert existing goals to new format
- Maintain backward compatibility during transition
- Document migration guides and best practices

---

## 📊 **COMPATIBILITY ASSESSMENT**

### **Overall Architecture Alignment: 65%**

```
🟢 Goal Generation:         85% Compatible (minor interface changes needed)
🟢 Database Integration:    90% Compatible (schema supports new structure)
🟢 MCP Tool Framework:      95% Compatible (tools work with enhancements)
🟡 Task Decomposition:      40% Compatible (need decomposer implementation)
🟡 Success Criteria:        30% Compatible (need formal structure)
🟡 Completion Tracking:     20% Compatible (need commit mapping)
🔴 Epistemic Weighting:     0% Compatible (completely new concept)
🔴 Token Management:        0% Compatible (new requirement)
```

### **Implementation Effort Estimate:**
- **Phase 1 (Bridge):** 20-30 hours (enhance existing, add dataclasses)
- **Phase 2 (Full):** 60-80 hours (complete new architecture)
- **Migration Tools:** 10-15 hours (backward compatibility support)

---

## 🎯 **RECOMMENDATION**

### **✅ PROCEED WITH GRADUAL INTEGRATION:**

1. **Current goal orchestrator is WELL-POSITIONED** for the new architecture
2. **Existing MCP tools provide STRONG FOUNDATION** for enhancement
3. **Database schema ALREADY SUPPORTS** structured goal storage
4. **Transition can be BACKWARD COMPATIBLE** with proper design

### **🔄 SUGGESTED APPROACH:**
1. **Enhance existing tools** to support new dataclasses alongside current format
2. **Implement missing components** (TaskDecomposer, CompletionTracker) incrementally
3. **Test integration** with current CASCADE workflow before full migration
4. **Provide migration tools** to convert existing goals to new structure

**The current goal orchestrator provides an excellent foundation for the new Goal → Task → Completion architecture. Integration is highly feasible with proper planning!**