#!/usr/bin/env python3
"""
Cascade Workflow Orchestrator - REFACTORED
Uses canonical metacognitive cascade instead of reimplementing workflow.

This file now serves as a compatibility layer and adapter for the cognitive
benchmarking suite to work with the canonical cascade implementation.
"""

import uuid
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from pathlib import Path

# Import CANONICAL cascade implementation
try:
    # Try relative imports first (when used as package)
    from ..core.metacognitive_cascade.metacognitive_cascade import (
        CanonicalEpistemicCascade,
        EpistemicAssessment,
        Action
    )
except ImportError:
    # Fall back to absolute imports (when used standalone)
    from empirica.core.metacognitive_cascade.metacognitive_cascade import (
        CanonicalEpistemicCascade,
        EpistemicAssessment,
        Action
    )

# Legacy compatibility - map to canonical types
@dataclass
class WorkflowState:
    """Legacy compatibility wrapper for WorkflowState"""
    session_id: str
    current_phase: str = "preflight"
    investigation_cycle: int = 0
    preflight_result: Optional[Dict] = None
    check_result: Optional[Dict] = None
    postflight_result: Optional[Dict] = None

# Legacy assessment types for backward compatibility
@dataclass
class PreflightAssessment:
    """Legacy compatibility wrapper - now uses canonical EpistemicAssessment"""
    session_id: str
    timestamp: str
    prompt_summary: str
    vectors: Dict[str, float]
    initial_uncertainty_notes: str
    
    @classmethod
    def from_canonical(cls, canonical_assessment: EpistemicAssessment) -> 'PreflightAssessment':
        """Convert from canonical EpistemicAssessment to legacy format"""
        return cls(
            session_id=canonical_assessment.session_id,
            timestamp=canonical_assessment.timestamp.isoformat(),
            prompt_summary=canonical_assessment.prompt_summary,
            vectors=canonical_assessment.vectors,
            initial_uncertainty_notes=getattr(canonical_assessment, 'uncertainty_notes', "")
        )

@dataclass
class CheckPhaseResult:
    """Legacy compatibility wrapper - now uses canonical Action enum"""
    decision: str  # "proceed", "investigate", "recalibrate"
    confidence: float
    gaps: List[str]
    reasoning: str
    
    @classmethod
    def from_canonical(cls, action: Action, reasoning: str = "") -> 'CheckPhaseResult':
        """Convert from canonical Action to legacy format"""
        decision_map = {
            Action.PROCEED: "proceed",
            Action.INVESTIGATE: "investigate", 
            Action.RETHINK: "recalibrate"
        }
        
        return cls(
            decision=decision_map.get(action, "investigate"),
            confidence=0.8,  # Canonical doesn't provide confidence separately
            gaps=[],  # Would need to extract from reasoning
            reasoning=reasoning
        )

@dataclass  
class PostflightAssessment:
    """Legacy compatibility wrapper - now uses canonical EpistemicAssessment"""
    session_id: str
    timestamp: str
    task_summary: str
    vectors: Dict[str, float]
    changes_from_preflight: Dict[str, float]
    
    @classmethod
    def from_canonical(cls, canonical_assessment: EpistemicAssessment, 
                      task_summary: str = "", preflight_vectors: Optional[Dict] = None) -> 'PostflightAssessment':
        """Convert from canonical EpistemicAssessment to legacy format"""
        changes = {}
        if preflight_vectors:
            for key, value in canonical_assessment.vectors.items():
                changes[key] = value - preflight_vectors.get(key, 0.5)
        
        return cls(
            session_id=canonical_assessment.session_id,
            timestamp=canonical_assessment.timestamp.isoformat(),
            task_summary=task_summary,
            vectors=canonical_assessment.vectors,
            changes_from_preflight=changes
        )


class CanonicalCascadeAdapter:
    """
    Adapter that provides legacy interface while using canonical implementation.
    
    This allows the cognitive benchmarking suite to migrate to the canonical
    cascade without breaking existing code.
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.canonical_cascade = CanonicalEpistemicCascade(session_id)
        self.state = WorkflowState(session_id=session_id)
    
    def execute_preflight_assessment(
        self,
        prompt: str,
        vectors: Optional[Dict[str, float]] = None,
        uncertainty_notes: str = ""
    ) -> PreflightAssessment:
        """
        Execute preflight assessment using canonical implementation
        """
        # Use canonical preflight method
        preflight_result = self.canonical_cascade.execute_preflight(prompt)
        
        # Convert to legacy format for compatibility
        self.state.preflight_result = preflight_result
        return PreflightAssessment.from_canonical(preflight_result)
    
    def execute_check_phase(
        self,
        investigation_summary: str,
        confidence: Optional[float] = None,
        gaps: Optional[List[str]] = None
    ) -> CheckPhaseResult:
        """
        Execute CHECK phase using canonical implementation
        """
        # Prepare context for canonical check phase
        context = {
            'investigation_summary': investigation_summary,
            'confidence': confidence,
            'gaps': gaps or []
        }
        
        # Use canonical check method
        check_result = self.canonical_cascade.execute_check(context)
        
        # Convert to legacy format
        self.state.check_result = check_result
        return CheckPhaseResult.from_canonical(check_result.recommended_action, check_result.reasoning)
    
    def execute_postflight_assessment(
        self,
        task_summary: str,
        final_vectors: Optional[Dict[str, float]] = None
    ) -> PostflightAssessment:
        """
        Execute postflight assessment using canonical implementation
        """
        # Get preflight vectors for comparison
        preflight_vectors = self.state.preflight_result.vectors if self.state.preflight_result else None
        
        # Prepare context for canonical postflight
        context = {
            'task_summary': task_summary,
            'final_vectors': final_vectors or {}
        }
        
        # Use canonical postflight method  
        postflight_result = self.canonical_cascade.execute_postflight(context)
        
        # Convert to legacy format
        self.state.postflight_result = postflight_result
        return PostflightAssessment.from_canonical(postflight_result, task_summary, preflight_vectors)


# Legacy class name for backward compatibility
class CascadeWorkflowOrchestrator(CanonicalCascadeAdapter):
    """
    Legacy compatibility class - now uses canonical implementation via adapter
    """
    pass