#!/usr/bin/env python3
"""
Goal Type Definitions

Core dataclasses for structured goal representation.
Designed for explicit AI-driven goal creation (MVP - no automatic parsing).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import time
import uuid


class GoalScope(Enum):
    """Goal scope classification"""
    TASK_SPECIFIC = "task_specific"      # Single task completion
    SESSION_SCOPED = "session_scoped"    # Multiple related tasks
    PROJECT_WIDE = "project_wide"        # Long-term objectives


class DependencyType(Enum):
    """Dependency relationship types"""
    PREREQUISITE = "prerequisite"        # Must complete before starting
    CONCURRENT = "concurrent"            # Can work on simultaneously
    INFORMATIONAL = "informational"      # Nice to have context


@dataclass
class SuccessCriterion:
    """Measurable success criterion for goal completion"""
    id: str
    description: str
    validation_method: str               # "completion", "quality_gate", "metric_threshold"
    threshold: Optional[float] = None    # For metric-based criteria
    is_required: bool = True             # vs. optional/nice-to-have
    is_met: bool = False                 # Completion status


@dataclass
class Dependency:
    """Goal dependency specification"""
    id: str
    goal_id: str                         # Which goal this depends on
    dependency_type: DependencyType
    description: str


@dataclass
class Goal:
    """
    Structured goal representation
    
    MVP Design: AI creates goals explicitly via MCP tools.
    No automatic parsing - keeps it simple and heuristic-free.
    """
    id: str
    objective: str                       # Clear, actionable goal statement
    success_criteria: List[SuccessCriterion]
    scope: GoalScope
    dependencies: List[Dependency] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    estimated_complexity: Optional[float] = None
    created_timestamp: float = field(default_factory=time.time)
    completed_timestamp: Optional[float] = None
    is_completed: bool = False
    
    @staticmethod
    def create(
        objective: str,
        success_criteria: List[SuccessCriterion],
        scope: GoalScope = GoalScope.TASK_SPECIFIC,
        **kwargs
    ) -> 'Goal':
        """Convenience factory method"""
        return Goal(
            id=str(uuid.uuid4()),
            objective=objective,
            success_criteria=success_criteria,
            scope=scope,
            **kwargs
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'id': self.id,
            'objective': self.objective,
            'success_criteria': [
                {
                    'id': sc.id,
                    'description': sc.description,
                    'validation_method': sc.validation_method,
                    'threshold': sc.threshold,
                    'is_required': sc.is_required,
                    'is_met': sc.is_met
                }
                for sc in self.success_criteria
            ],
            'scope': self.scope.value,
            'dependencies': [
                {
                    'id': dep.id,
                    'goal_id': dep.goal_id,
                    'dependency_type': dep.dependency_type.value,
                    'description': dep.description
                }
                for dep in self.dependencies
            ],
            'constraints': self.constraints,
            'metadata': self.metadata,
            'estimated_complexity': self.estimated_complexity,
            'created_timestamp': self.created_timestamp,
            'completed_timestamp': self.completed_timestamp,
            'is_completed': self.is_completed
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Goal':
        """Deserialize from dictionary"""
        return Goal(
            id=data['id'],
            objective=data['objective'],
            success_criteria=[
                SuccessCriterion(
                    id=sc['id'],
                    description=sc['description'],
                    validation_method=sc['validation_method'],
                    threshold=sc.get('threshold'),
                    is_required=sc.get('is_required', True),
                    is_met=sc.get('is_met', False)
                )
                for sc in data['success_criteria']
            ],
            scope=GoalScope(data['scope']),
            dependencies=[
                Dependency(
                    id=dep['id'],
                    goal_id=dep['goal_id'],
                    dependency_type=DependencyType(dep['dependency_type']),
                    description=dep['description']
                )
                for dep in data.get('dependencies', [])
            ],
            constraints=data.get('constraints', {}),
            metadata=data.get('metadata', {}),
            estimated_complexity=data.get('estimated_complexity'),
            created_timestamp=data.get('created_timestamp', time.time()),
            completed_timestamp=data.get('completed_timestamp'),
            is_completed=data.get('is_completed', False)
        )
