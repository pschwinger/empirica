#!/usr/bin/env python3
"""
Input Validation for Goal Architecture

Provides validation functions to ensure data integrity before database operations.
Designed to catch errors early and provide clear feedback.
"""

from typing import List, Dict, Any, Optional
from .types import Goal, SuccessCriterion, GoalScope


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_objective(objective: str) -> None:
    """
    Validate goal objective
    
    Args:
        objective: Goal objective string
        
    Raises:
        ValidationError: If objective is invalid
    """
    if not objective or not objective.strip():
        raise ValidationError("Objective cannot be empty")
    
    if len(objective) > 1000:
        raise ValidationError("Objective too long (max 1000 characters)")


def validate_success_criteria(success_criteria: List[SuccessCriterion]) -> None:
    """
    Validate success criteria list
    
    Args:
        success_criteria: List of success criteria
        
    Raises:
        ValidationError: If criteria are invalid
    """
    if not success_criteria:
        raise ValidationError("At least one success criterion is required")
    
    valid_methods = ["completion", "quality_gate", "metric_threshold"]
    
    for idx, sc in enumerate(success_criteria):
        # Validate description
        if not sc.description or not sc.description.strip():
            raise ValidationError(f"Success criterion {idx}: description cannot be empty")
        
        # Validate validation_method
        if sc.validation_method not in valid_methods:
            raise ValidationError(
                f"Success criterion {idx}: validation_method must be one of {valid_methods}, "
                f"got '{sc.validation_method}'"
            )
        
        # Validate threshold for metric-based criteria
        if sc.validation_method == "metric_threshold":
            if sc.threshold is None:
                raise ValidationError(
                    f"Success criterion {idx}: threshold required for metric_threshold validation"
                )
            if not (0.0 <= sc.threshold <= 1.0):
                raise ValidationError(
                    f"Success criterion {idx}: threshold must be between 0.0 and 1.0, "
                    f"got {sc.threshold}"
                )


def validate_complexity(complexity: Optional[float]) -> None:
    """
    Validate complexity estimate
    
    Args:
        complexity: Complexity value (should be 0.0-1.0)
        
    Raises:
        ValidationError: If complexity is out of range
    """
    if complexity is not None:
        if not (0.0 <= complexity <= 1.0):
            raise ValidationError(
                f"Complexity must be between 0.0 and 1.0, got {complexity}"
            )


def validate_goal(goal: Goal) -> None:
    """
    Validate complete goal object
    
    Args:
        goal: Goal to validate
        
    Raises:
        ValidationError: If goal is invalid
    """
    validate_objective(goal.objective)
    validate_success_criteria(goal.success_criteria)
    validate_complexity(goal.estimated_complexity)
    
    # Validate scope is valid enum
    if not isinstance(goal.scope, GoalScope):
        raise ValidationError(f"Invalid scope: must be GoalScope enum")


def validate_mcp_goal_input(arguments: Dict[str, Any]) -> None:
    """
    Validate MCP create_goal input arguments
    
    Args:
        arguments: MCP tool arguments dict
        
    Raises:
        ValidationError: If arguments are invalid
    """
    # Validate objective
    objective = arguments.get("objective", "")
    if not objective or not objective.strip():
        raise ValidationError("Missing or empty 'objective' field")
    
    # Validate success_criteria
    success_criteria_data = arguments.get("success_criteria", [])
    if not success_criteria_data:
        raise ValidationError("At least one success criterion is required")
    
    if not isinstance(success_criteria_data, list):
        raise ValidationError("success_criteria must be an array")
    
    valid_methods = ["completion", "quality_gate", "metric_threshold"]
    
    for idx, sc_data in enumerate(success_criteria_data):
        if not isinstance(sc_data, dict):
            raise ValidationError(f"Success criterion {idx} must be an object")
        
        if "description" not in sc_data or not sc_data["description"]:
            raise ValidationError(f"Success criterion {idx}: missing 'description'")
        
        if "validation_method" not in sc_data:
            raise ValidationError(f"Success criterion {idx}: missing 'validation_method'")
        
        if sc_data["validation_method"] not in valid_methods:
            raise ValidationError(
                f"Success criterion {idx}: validation_method must be one of {valid_methods}"
            )
        
        if sc_data["validation_method"] == "metric_threshold" and "threshold" not in sc_data:
            raise ValidationError(
                f"Success criterion {idx}: 'threshold' required for metric_threshold validation"
            )
    
    # Validate scope if provided
    scope = arguments.get("scope")
    if scope:
        valid_scopes = ["task_specific", "session_scoped", "project_wide"]
        if scope not in valid_scopes:
            raise ValidationError(f"scope must be one of {valid_scopes}, got '{scope}'")
    
    # Validate complexity if provided
    complexity = arguments.get("estimated_complexity")
    if complexity is not None:
        try:
            complexity_float = float(complexity)
            if not (0.0 <= complexity_float <= 1.0):
                raise ValidationError(
                    f"estimated_complexity must be between 0.0 and 1.0, got {complexity}"
                )
        except (TypeError, ValueError):
            raise ValidationError(f"estimated_complexity must be a number, got {type(complexity)}")


def validate_mcp_subtask_input(arguments: Dict[str, Any]) -> None:
    """
    Validate MCP add_subtask input arguments
    
    Args:
        arguments: MCP tool arguments dict
        
    Raises:
        ValidationError: If arguments are invalid
    """
    # Validate goal_id
    if not arguments.get("goal_id"):
        raise ValidationError("Missing 'goal_id' field")
    
    # Validate description
    description = arguments.get("description", "")
    if not description or not description.strip():
        raise ValidationError("Missing or empty 'description' field")
    
    if len(description) > 500:
        raise ValidationError("description too long (max 500 characters)")
    
    # Validate epistemic_importance if provided
    importance = arguments.get("epistemic_importance")
    if importance:
        valid_importance = ["critical", "high", "medium", "low"]
        if importance not in valid_importance:
            raise ValidationError(
                f"epistemic_importance must be one of {valid_importance}, got '{importance}'"
            )
    
    # Validate estimated_tokens if provided
    tokens = arguments.get("estimated_tokens")
    if tokens is not None:
        try:
            tokens_int = int(tokens)
            if tokens_int < 0:
                raise ValidationError("estimated_tokens must be non-negative")
        except (TypeError, ValueError):
            raise ValidationError(f"estimated_tokens must be an integer, got {type(tokens)}")
    
    # Validate dependencies if provided
    dependencies = arguments.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, list):
            raise ValidationError("dependencies must be an array")
        for dep in dependencies:
            if not isinstance(dep, str):
                raise ValidationError("dependencies must be array of strings (subtask IDs)")
