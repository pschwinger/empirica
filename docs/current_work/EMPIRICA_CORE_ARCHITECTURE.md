# Empirica Core Architecture: Goal → Task → Completion

## Overview

Empirica Core handles the **single-AI workflow** with intelligent task management. It focuses on:

1. **Goal parsing & structuring** (PREFLIGHT)
2. **Task decomposition** (INVESTIGATE)
3. **Execution tracking** (ACT)
4. **Completion & learning** (POSTFLIGHT)

This layer remains **independent of multi-AI coordination**. Sentinel orchestrates multiple Empirica instances across branches, but each branch runs pure Empirica Core.

---

## Separation of Concerns

### What Lives in Empirica Core

**Goal Management Module** (`empirica/core/goals/`)
- Parse natural language context → Goal object
- Extract success criteria, dependencies, scope
- Store in database + Git

**Task Decomposition Module** (`empirica/core/tasks/`)
- Break Goal into SubTasks with epistemic weight
- Generate task tree with dependencies
- Estimate token cost per subtask
- Flag epistemically-required vs. optional-improves

**Completion Tracker Module** (`empirica/core/completion/`)
- Map actual commits back to planned subtasks
- Track divergence between plan and reality
- Calculate completion percentage
- Store in git notes for learning

**Workflow Integration** (`empirica/core/workflow/`)
- Integrate Goal → Task → Completion into CASCADE phases
- PREFLIGHT: Goal Parser runs, creates initial decomposition
- INVESTIGATE: Refine decomposition based on learning
- ACT: Execute subtasks, track in Completion Tracker
- POSTFLIGHT: Aggregate learning, update epistemic vectors

### What Sentinel Adds (NOT in Core)

- Task routing (single vs. multi-AI decision)
- Branch management (creating reasoning/acting branches)
- Epistemic state handoff (passing state between AIs)
- Multi-branch merging & calibration
- Provider abstraction (Claude vs. Qwen vs. other)

**Key principle:** Empirica Core answers "how do I do this task well?" Sentinel answers "who should do it and how should they coordinate?"

---

## Module 1: Goal Management

### Location
```
empirica/core/goals/
├── __init__.py
├── goal.py           # Goal dataclass
├── parser.py         # Natural language → Goal
└── repository.py     # Goal persistence (DB + Git)
```

### Core Types

```python
# empirica/core/goals/goal.py

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime

class GoalScope(Enum):
    MINIMAL = "minimal"        # Single, well-defined outcome
    BOUNDED = "bounded"        # Multiple related outcomes
    OPEN_ENDED = "open_ended"  # Exploratory, scope may expand

@dataclass
class SuccessCriterion:
    """Single verifiable outcome"""
    id: str
    description: str  # "Authentication system works AND user can login in <2s"
    verifiable: bool  # Can this be checked programmatically?
    dependencies: List[str] = field(default_factory=list)  # Other criterion IDs
    estimated_complexity: float = 0.5  # 0-1 scale

@dataclass
class Goal:
    """Structured representation of a task"""
    id: str
    title: str
    description: str  # Full context from user
    success_criteria: List[SuccessCriterion]
    scope: GoalScope
    dependencies: List[str] = field(default_factory=list)  # External dependencies
    constraints: Dict[str, str] = field(default_factory=dict)  # "token_budget": "10000"
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    created_in_phase: str = "PREFLIGHT"  # Which CASCADE phase created this
    
    # Git integration
    git_commit_sha: Optional[str] = None
    git_notes: Optional[str] = None
```

### Goal Parser

```python
# empirica/core/goals/parser.py

class GoalParser:
    """
    Converts natural language task context into structured Goal
    
    Responsibilities:
    - Extract core objective
    - Identify success criteria
    - Infer scope (minimal/bounded/open_ended)
    - Detect dependencies
    """
    
    def parse(self, task_context: str) -> Goal:
        """
        task_context: User's task description, requirements, constraints
        
        Returns: Goal object ready for decomposition
        
        Steps:
        1. LLM analysis: What is actually being asked?
        2. Criterion extraction: What counts as success?
        3. Scope inference: How big is this?
        4. Dependency detection: What must be true first?
        5. Constraint parsing: Any token/time/other budgets?
        """
        pass
    
    def extract_success_criteria(self, context: str) -> List[SuccessCriterion]:
        """
        Parse context for explicit and implicit success criteria
        
        Examples:
        - "Write an OAuth system" 
          → Criteria: ["Users can authenticate", "Tokens expire correctly"]
        - "Fix the bug where passwords reset randomly"
          → Criteria: ["Password reset uses proper entropy", "No data loss"]
        """
        pass
    
    def infer_scope(self, context: str, criteria_count: int) -> GoalScope:
        """
        Heuristic: Infer scope from context
        
        minimal: 1 criterion, straightforward, <2 hours
        bounded: 2-4 criteria, clear boundaries
        open_ended: >4 criteria OR exploratory language
        """
        pass
```

### Goal Repository

```python
# empirica/core/goals/repository.py

class GoalRepository:
    """
    Persistence layer for goals (database + Git)
    
    Database: Track all goals, search by criteria, link to sessions
    Git: Store Goal as JSON in .empirica/goals/, commit with CASCADE phase
    """
    
    def save(self, goal: Goal, session_id: str) -> str:
        """
        Save goal to database + Git
        
        Returns: goal.id
        
        Steps:
        1. Save to goals table: id, title, description, created_at, etc.
        2. Serialize to JSON: .empirica/goals/{goal_id}.json
        3. Commit to Git: "PREFLIGHT: Create goal '{title}'"
        4. Add git note: goal.id, goal.git_commit_sha
        """
        pass
    
    def load(self, goal_id: str) -> Goal:
        """Load goal from database or Git"""
        pass
    
    def search(self, query: str) -> List[Goal]:
        """Search goals by title/description"""
        pass
```

---

## Module 2: Task Decomposition

### Location
```
empirica/core/tasks/
├── __init__.py
├── subtask.py        # SubTask dataclass
├── decomposer.py     # Goal → Task tree
└── repository.py     # Task persistence
```

### Core Types

```python
# empirica/core/tasks/subtask.py

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class TaskStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    FAILED = "failed"

@dataclass
class SubTask:
    """Single unit of work within a Goal"""
    id: str  # "st-001", "st-002", etc.
    goal_id: str
    description: str
    
    # Epistemic weight: Guides which tasks MUST run vs. NICE-TO-HAVE
    epistemically_required: bool  # Must solve to reduce uncertainty
    optionally_improves: bool     # Nice to have for calibration
    
    # Dependencies: What must complete before this?
    dependencies: List[str] = field(default_factory=list)  # Other SubTask IDs
    
    # Estimation
    estimated_tokens: int  # How many tokens to complete
    estimated_importance: float = 0.5  # 0-1: How critical to goal?
    
    # Execution metadata
    status: TaskStatus = TaskStatus.PLANNED
    git_commit_sha: Optional[str] = None  # If completed, which commit?
    phase_completed: Optional[str] = None  # PREFLIGHT/INVESTIGATE/ACT/POSTFLIGHT
    
    # Learning
    actual_tokens: Optional[int] = None
    divergence_reason: Optional[str] = None  # Why did reality differ from plan?

@dataclass
class TaskDecomposition:
    """Complete task tree for a Goal"""
    goal_id: str
    subtasks: List[SubTask]
    
    # Optimization info
    total_estimated_tokens: int
    critical_path: List[str]  # Subtask IDs in critical path
    
    # Metadata
    created_in_phase: str = "INVESTIGATE"
    version: int = 1  # Decomposition can be refined
```

### Task Decomposer

```python
# empirica/core/tasks/decomposer.py

class TaskDecomposer:
    """
    Converts Goal into task tree
    
    Responsibilities:
    - Break goal into subtasks
    - Identify dependencies
    - Mark epistemic vs. optional tasks
    - Estimate tokens per subtask
    - Identify critical path
    """
    
    def decompose(self, goal: Goal) -> TaskDecomposition:
        """
        goal: Goal object from Goal Parser
        
        Returns: TaskDecomposition with subtask tree
        
        Algorithm:
        1. Per success criterion → subtask(s) to achieve it
        2. Per subtask → dependencies (what must be true first?)
        3. Mark: Is this epistemically required? (Must reduce uncertainty)
        4. Estimate: Token cost for each subtask
        5. Optimize: Find critical path through DAG
        6. Flag: What can be skipped if tokens run low?
        """
        pass
    
    def _create_subtasks_for_criterion(
        self,
        criterion: SuccessCriterion,
        goal: Goal
    ) -> List[SubTask]:
        """
        One criterion might require multiple subtasks
        
        Example criterion: "Users can authenticate in <2s"
        Subtasks:
        - st-1: Design auth flow (epistemically_required=True)
        - st-2: Implement auth handler (epistemically_required=True)
        - st-3: Optimize for <2s latency (epistemically_required=False, optional)
        - st-4: Add rate limiting (epistemically_required=False, optional)
        """
        pass
    
    def _identify_dependencies(
        self,
        subtasks: List[SubTask]
    ) -> None:
        """
        Analyze which subtasks must run in which order
        
        Sets SubTask.dependencies based on semantic relationships
        """
        pass
    
    def _estimate_tokens(
        self,
        subtask: SubTask,
        context: Dict
    ) -> int:
        """
        Estimate tokens needed for this subtask
        
        Factors:
        - Complexity (design vs. implementation vs. testing)
        - Scope (minimal/bounded/open_ended)
        - Estimated_importance (quick wins vs. deep work)
        """
        pass
    
    def _find_critical_path(
        self,
        subtasks: List[SubTask]
    ) -> List[str]:
        """
        Find longest path through dependency DAG
        
        This is the minimum set of subtasks that must complete.
        Other subtasks can be skipped if needed.
        """
        pass
```

### Task Repository

```python
# empirica/core/tasks/repository.py

class TaskRepository:
    """
    Persistence for task decompositions
    
    Database: Link decompositions to goals/sessions
    Git: Store as JSON in .empirica/decompositions/
    """
    
    def save(
        self,
        decomposition: TaskDecomposition,
        session_id: str
    ) -> str:
        """
        Save decomposition to database + Git
        
        Returns: decomposition.goal_id
        
        Steps:
        1. Save to decompositions table
        2. Serialize to JSON: .empirica/decompositions/{goal_id}_v{version}.json
        3. Commit to Git: "INVESTIGATE: Decompose goal {goal_id}"
        4. Add git note: decomposition details
        """
        pass
    
    def load(self, goal_id: str, version: int = None) -> TaskDecomposition:
        """Load decomposition (latest version or specific)"""
        pass
    
    def refine(
        self,
        goal_id: str,
        changes: Dict
    ) -> TaskDecomposition:
        """
        During INVESTIGATE, decomposition can be refined
        
        Changes: {"merge_st_1_and_2": True, "mark_st_4_optional": True}
        
        Creates new version, increments version number
        """
        pass
```

---

## Module 3: Completion Tracking

### Location
```
empirica/core/completion/
├── __init__.py
├── record.py         # CompletionRecord dataclass
├── tracker.py        # Track commits → subtasks
└── repository.py     # Completion persistence
```

### Core Types

```python
# empirica/core/completion/record.py

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class CompletionRecord:
    """Maps a Git commit to planned subtasks"""
    
    # What was done
    git_commit_sha: str
    commit_message: str
    files_changed: List[str]
    
    # What was planned
    subtask_ids_addressed: List[str]
    subtask_ids_planned: List[str]
    
    # How reality matched plan
    plan_accuracy: float  # 0-1: What % of planned work was done?
    divergence_reason: Optional[str]  # Why if != 100%?
    
    # Epistemic impact
    epistemic_delta: Dict[str, float] = field(default_factory=dict)
    # Example: {"KNOW": +0.15, "UNCERTAINTY": -0.10, "DO": +0.20}
    
    # Metadata
    phase: str  # ACT or POSTFLIGHT
    created_at: datetime = field(default_factory=datetime.now)
    
@dataclass
class CompletionSummary:
    """Aggregate completion data for a Goal"""
    goal_id: str
    total_subtasks: int
    completed_subtasks: int
    skipped_subtasks: int
    failed_subtasks: int
    
    completion_percentage: float  # (completed + justified_skipped) / total
    epistemic_progress: Dict[str, float]  # Aggregate deltas
    
    branches_explored: List[str]  # Alternative approaches tried
    branches_abandoned: List[str]  # Why abandoned?
```

### Completion Tracker

```python
# empirica/core/completion/tracker.py

class CompletionTracker:
    """
    When AI commits work, track:
    - Which subtasks does this commit address?
    - Did we follow the plan or diverge?
    - Why?
    """
    
    def track_commit(
        self,
        commit_sha: str,
        goal_id: str,
        decomposition: TaskDecomposition
    ) -> CompletionRecord:
        """
        After AI commits, analyze what was done vs. planned
        
        Steps:
        1. Parse commit: What files changed? What was the message?
        2. Parse decomposition: What subtasks were planned?
        3. Map: Which subtasks does this commit address?
           - Use semantic similarity (commit message vs. subtask description)
           - Use file changes (if subtask mentions file, check if changed)
        4. Calculate: plan_accuracy = matched / expected
        5. If <100%: Extract divergence reason from commit message/notes
        6. Store record
        """
        pass
    
    def _map_commit_to_subtasks(
        self,
        commit_diff: Dict,
        commit_message: str,
        subtasks: List[SubTask]
    ) -> List[str]:
        """
        Semantic mapping: Which subtasks does this commit address?
        
        Heuristics:
        - If commit_message mentions criterion/subtask → match
        - If files changed match subtask scope → match
        - Use embedding similarity if unclear
        """
        pass
    
    def _extract_divergence_reason(
        self,
        commit_sha: str,
        expected_subtasks: List[str],
        actual_subtasks: List[str]
    ) -> Optional[str]:
        """
        If plan_accuracy < 100%, why?
        
        Check:
        - Extended commit message? (git show --format=full)
        - Git notes? (git notes show)
        - Ratio: If 2 subtasks expected, 1 done → "time constraint"?
        """
        pass
    
    def aggregate(
        self,
        goal_id: str,
        records: List[CompletionRecord]
    ) -> CompletionSummary:
        """
        After all commits, aggregate learning
        
        Calculate:
        - Total completion %
        - Which subtasks were done/skipped/failed
        - Why they were skipped (time? unnecessary? discovered optional?)
        - Total epistemic delta
        """
        pass
```

### Completion Repository

```python
# empirica/core/completion/repository.py

class CompletionRepository:
    """
    Persistence for completion records + summaries
    
    Database: completion_records table
    Git notes: Store reasoning per commit
    """
    
    def save_record(
        self,
        record: CompletionRecord,
        session_id: str
    ) -> None:
        """
        Save completion record + git note
        
        Steps:
        1. Insert into completion_records table
        2. Add git note to commit: record as JSON
           git notes add -m '{record.to_json()}' {commit_sha}
        3. Links: session_id → goal_id → commit_sha
        """
        pass
    
    def save_summary(
        self,
        summary: CompletionSummary,
        session_id: str
    ) -> None:
        """
        Save completion summary for POSTFLIGHT
        
        Stores: total completion %, epistemic deltas, lessons learned
        """
        pass
    
    def get_for_goal(self, goal_id: str) -> CompletionSummary:
        """Retrieve aggregated completion data for a goal"""
        pass
    
    def get_all_learnings(self, limit: int = 100) -> List[Dict]:
        """
        For meta-learning: "What patterns predict plan accuracy?"
        
        Query: SELECT goal scope, decomposition complexity, plan accuracy
               ORDER BY created_at DESC LIMIT 100
        """
        pass
```

---

## Module 4: Workflow Integration

### Location
```
empirica/core/workflow/
├── __init__.py
├── goal_workflow.py  # Goal management in CASCADE
└── task_workflow.py  # Task management in CASCADE
```

### Goal Workflow

```python
# empirica/core/workflow/goal_workflow.py

class GoalWorkflow:
    """
    Integrates Goal management into CASCADE phases
    """
    
    async def preflight_goal_phase(
        self,
        task_context: str,
        session_id: str
    ) -> Goal:
        """
        PREFLIGHT: Parse context into Goal
        
        Steps:
        1. GoalParser.parse(task_context) → Goal
        2. GoalRepository.save(goal, session_id)
        3. Add to session.goals table
        4. Return goal
        
        Output: Goal object ready for decomposition
        """
        pass
    
    async def postflight_goal_learning(
        self,
        goal_id: str,
        session_id: str
    ) -> Dict:
        """
        POSTFLIGHT: Learn from goal execution
        
        Uses: CompletionRepository to get summary
        
        Calculates:
        - Did we estimate scope correctly?
        - Were success criteria well-defined?
        - What would we change next time?
        
        Output: Learning record for meta-improvement
        """
        pass
```

### Task Workflow

```python
# empirica/core/workflow/task_workflow.py

class TaskWorkflow:
    """
    Integrates Task decomposition into CASCADE phases
    """
    
    async def investigate_decomposition_phase(
        self,
        goal: Goal,
        session_id: str
    ) -> TaskDecomposition:
        """
        INVESTIGATE: Decompose Goal into Tasks
        
        Steps:
        1. TaskDecomposer.decompose(goal) → TaskDecomposition
        2. TaskRepository.save(decomposition, session_id)
        3. Add to session.decompositions table
        4. Return decomposition
        
        Output: Task tree ready for execution
        """
        pass
    
    async def check_decomposition_phase(
        self,
        decomposition: TaskDecomposition,
        epistemic_vectors: Dict
    ) -> bool:
        """
        CHECK: Validate decomposition before ACT
        
        Checks:
        - Are dependencies valid (no cycles)?
        - Is critical path feasible within token budget?
        - Are epistemically-required tasks clear?
        
        Output: True if ready to ACT, False if need more INVESTIGATE
        """
        pass
    
    async def act_tracking_phase(
        self,
        goal_id: str,
        decomposition: TaskDecomposition,
        session_id: str
    ) -> None:
        """
        ACT: During execution, track commits
        
        Steps:
        1. Listen for git commits in this session
        2. For each commit:
           - CompletionTracker.track_commit()
           - CompletionRepository.save_record()
           - Update subtask statuses
        3. End of ACT: CompletionTracker.aggregate()
        
        Output: Real-time tracking, completion summary
        """
        pass
    
    async def postflight_completion_phase(
        self,
        goal_id: str,
        decomposition: TaskDecomposition,
        session_id: str
    ) -> CompletionSummary:
        """
        POSTFLIGHT: Aggregate and learn from completion
        
        Steps:
        1. Retrieve all CompletionRecords for goal
        2. CompletionTracker.aggregate() → CompletionSummary
        3. CompletionRepository.save_summary()
        4. Update epistemic vectors based on learning
        5. Store: "For goals with this scope, we estimated X tokens, used Y"
        
        Output: Summary for meta-improvement, updated epistemic vectors
        """
        pass
```

---

## Database Schema Additions

### Goals Table
```sql
CREATE TABLE goals (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    title TEXT,
    description TEXT,
    scope TEXT,  -- minimal|bounded|open_ended
    created_at TIMESTAMP,
    created_in_phase TEXT,
    git_commit_sha TEXT,
    -- Foreign keys
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE success_criteria (
    id TEXT PRIMARY KEY,
    goal_id TEXT,
    description TEXT,
    verifiable BOOLEAN,
    estimated_complexity FLOAT,
    FOREIGN KEY (goal_id) REFERENCES goals(id)
);
```

### Decompositions Table
```sql
CREATE TABLE decompositions (
    id TEXT PRIMARY KEY,
    goal_id TEXT,
    version INTEGER,
    total_estimated_tokens INTEGER,
    created_in_phase TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (goal_id) REFERENCES goals(id)
);

CREATE TABLE subtasks (
    id TEXT PRIMARY KEY,
    decomposition_id TEXT,
    goal_id TEXT,
    description TEXT,
    epistemically_required BOOLEAN,
    optionally_improves BOOLEAN,
    estimated_tokens INTEGER,
    status TEXT,  -- planned|in_progress|completed|skipped|failed
    git_commit_sha TEXT,
    FOREIGN KEY (decomposition_id) REFERENCES decompositions(id),
    FOREIGN KEY (goal_id) REFERENCES goals(id)
);

CREATE TABLE subtask_dependencies (
    from_subtask_id TEXT,
    to_subtask_id TEXT,
    PRIMARY KEY (from_subtask_id, to_subtask_id),
    FOREIGN KEY (from_subtask_id) REFERENCES subtasks(id),
    FOREIGN KEY (to_subtask_id) REFERENCES subtasks(id)
);
```

### Completion Records Table
```sql
CREATE TABLE completion_records (
    id TEXT PRIMARY KEY,
    git_commit_sha TEXT UNIQUE,
    goal_id TEXT,
    plan_accuracy FLOAT,
    divergence_reason TEXT,
    phase TEXT,  -- ACT|POSTFLIGHT
    created_at TIMESTAMP,
    FOREIGN KEY (goal_id) REFERENCES goals(id)
);

CREATE TABLE completion_record_subtasks (
    record_id TEXT,
    subtask_id TEXT,
    PRIMARY KEY (record_id, subtask_id),
    FOREIGN KEY (record_id) REFERENCES completion_records(id),
    FOREIGN KEY (subtask_id) REFERENCES subtasks(id)
);

CREATE TABLE completion_summaries (
    id TEXT PRIMARY KEY,
    goal_id TEXT,
    session_id TEXT,
    total_subtasks INTEGER,
    completed_subtasks INTEGER,
    skipped_subtasks INTEGER,
    completion_percentage FLOAT,
    created_at TIMESTAMP,
    FOREIGN KEY (goal_id) REFERENCES goals(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

---

## File Structure Summary

```
empirica/
├── core/
│   ├── goals/
│   │   ├── __init__.py
│   │   ├── goal.py           # Goal, SuccessCriterion dataclasses
│   │   ├── parser.py         # GoalParser
│   │   └── repository.py     # GoalRepository
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── subtask.py        # SubTask, TaskDecomposition dataclasses
│   │   ├── decomposer.py     # TaskDecomposer
│   │   └── repository.py     # TaskRepository
│   │
│   ├── completion/
│   │   ├── __init__.py
│   │   ├── record.py         # CompletionRecord, CompletionSummary
│   │   ├── tracker.py        # CompletionTracker
│   │   └── repository.py     # CompletionRepository
│   │
│   └── workflow/
│       ├── __init__.py
│       ├── goal_workflow.py  # GoalWorkflow
│       └── task_workflow.py  # TaskWorkflow
│
└── .empirica/
    ├── goals/                # Goal JSON files
    ├── decompositions/       # TaskDecomposition JSON files
    └── sessions/
        └── sessions.db       # All data
```

---

## Integration Points for Sentinel (Future)

When Sentinel layers on top, it will:

1. **Before Goal creation:** Analyze task context
   - Decide: single-AI? multi-AI?
   - If multi-AI: Create separate Goal instances (or mark for split)

2. **Before Decomposition:** TaskAnalyzer runs
   - Recommend: Single decomposition or per-branch?
   - Route: reasoning decomposition vs. acting decomposition

3. **During Execution:** Branch coordination
   - If multi-AI: reasoning branch → acting branch handoff
   - Sentinel merges branches, aggregates completion

4. **After Completion:** Multi-branch learning
   - Compare: How did different AIs decompose same goal?
   - Learn: What routing decisions worked well?

**But all this stays OUTSIDE Empirica Core.** Core only knows: Goal → Task → Completion, single-AI, single-branch.

---

## Key Design Principles

1. **Separation of concerns:** Goal/Task/Completion are independent modules
2. **Extensibility:** Each module has clear interface (parse, decompose, track)
3. **Persistence:** Everything in database + Git (auditable, learnable)
4. **Epistemic weighting:** Tasks marked as required vs. optional (Sentinel can use this)
5. **Minimal coupling:** Workflow orchestrates modules, but modules don't know about each other
6. **Git-native:** Every decision stored in commits + git notes for future learning

---

## Next Steps (Implementation)

1. **Define interfaces first** (before writing code):
   - GoalParser.parse(context) → Goal
   - TaskDecomposer.decompose(goal) → TaskDecomposition
   - CompletionTracker.track_commit(commit, goal) → CompletionRecord

2. **Implement in order:**
   - Goals (simplest, no dependencies)
   - Tasks (depends on Goals)
   - Completion (depends on Tasks + Git)
   - Workflow (integrates all three)

3. **Test single-AI flow:**
   - PREFLIGHT: Parse "Write OAuth" → Goal
   - INVESTIGATE: Decompose → Task tree
   - ACT: Execute, track commits
   - POSTFLIGHT: Aggregate completion

4. **Then Sentinel adds:**
   - Routing logic (single vs. multi)
   - Branch creation/management
   - Handoff logic
   - Multi-branch merging
