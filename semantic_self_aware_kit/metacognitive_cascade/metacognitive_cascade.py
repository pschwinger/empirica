"""
Simplified Metacognitive Cascade for Developers and Researchers
THINK → UNCERTAINTY → CHECK → INVESTIGATE → ACT
"""

import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class UncertaintyVector(Enum):
    """Core uncertainty vectors for decision-making"""
    VERIFICATION = "verification"      # Can claims be traced to sources?
    GROUNDING = "grounding"           # Factual vs speculative content?
    CONFIDENCE = "confidence"         # Overall confidence in approach?
    COMPLEXITY = "complexity"         # Task complexity level?

@dataclass
class CascadeResult:
    """Result from metacognitive cascade"""
    stage: str
    uncertainty_scores: Dict[UncertaintyVector, float]
    confidence_level: str  # "high", "medium", "low"
    required_actions: List[str]
    decision_rationale: str

class SimpleCascade:
    """Simplified metacognitive cascade for developers/researchers"""
    
    def __init__(self):
        self.uncertainty_thresholds = {
            UncertaintyVector.VERIFICATION: 0.7,
            UncertaintyVector.GROUNDING: 0.7,
            UncertaintyVector.CONFIDENCE: 0.6,
            UncertaintyVector.COMPLEXITY: 0.8,
        }
    
    def think(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Stage 1: THINK - Initial task analysis"""
        return {
            "task": task,
            "context": context or {},
            "timestamp": time.time(),
            "stage": "THINK"
        }
    
    def assess_uncertainty(self, analysis: Dict[str, Any]) -> Dict[UncertaintyVector, float]:
        """Stage 2: UNCERTAINTY - Assess uncertainty vectors"""
        task = analysis.get("task", "")
        
        scores = {}
        
        # VERIFICATION - Does this need source verification?
        verification_indicators = ["claims", "facts", "research", "data", "evidence"]
        verification_score = 0.3 + (0.1 * sum(1 for word in verification_indicators if word in task.lower()))
        scores[UncertaintyVector.VERIFICATION] = min(verification_score, 1.0)
        
        # GROUNDING - How speculative is this?
        speculative_indicators = ["might", "could", "potentially", "possibly", "experimental"]
        grounding_score = 0.2 + (0.2 * sum(1 for word in speculative_indicators if word in task.lower()))
        scores[UncertaintyVector.GROUNDING] = min(grounding_score, 1.0)
        
        # CONFIDENCE - Overall confidence
        complex_indicators = ["complex", "difficult", "challenging", "uncertain", "unclear"]
        confidence_score = 0.3 + (0.15 * sum(1 for word in complex_indicators if word in task.lower()))
        scores[UncertaintyVector.CONFIDENCE] = min(confidence_score, 1.0)
        
        # COMPLEXITY - Task complexity
        complexity_indicators = ["system", "architecture", "framework", "integration", "multiple"]
        complexity_score = 0.3 + (0.1 * sum(1 for word in complexity_indicators if word in task.lower()))
        scores[UncertaintyVector.COMPLEXITY] = min(complexity_score, 1.0)
        
        return scores
    
    def check(self, uncertainty_scores: Dict[UncertaintyVector, float]) -> List[str]:
        """Stage 3: CHECK - Verification questions"""
        checks = []
        
        if uncertainty_scores[UncertaintyVector.VERIFICATION] > self.uncertainty_thresholds[UncertaintyVector.VERIFICATION]:
            checks.append("verify_sources")
        
        if uncertainty_scores[UncertaintyVector.GROUNDING] > self.uncertainty_thresholds[UncertaintyVector.GROUNDING]:
            checks.append("mark_speculative")
        
        if uncertainty_scores[UncertaintyVector.CONFIDENCE] > self.uncertainty_thresholds[UncertaintyVector.CONFIDENCE]:
            checks.append("express_uncertainty")
        
        if uncertainty_scores[UncertaintyVector.COMPLEXITY] > self.uncertainty_thresholds[UncertaintyVector.COMPLEXITY]:
            checks.append("break_down_task")
        
        return checks
    
    def investigate(self, checks: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 4: INVESTIGATE - Gather additional information"""
        investigation_results = {
            "searches_needed": [],
            "assumptions_identified": [],
            "alternatives_considered": []
        }
        
        if "verify_sources" in checks:
            investigation_results["searches_needed"].append("source_verification")
        
        if "mark_speculative" in checks:
            investigation_results["assumptions_identified"].append("speculative_content")
        
        if "express_uncertainty" in checks:
            investigation_results["alternatives_considered"].append("alternative_approaches")
        
        if "break_down_task" in checks:
            investigation_results["searches_needed"].append("task_decomposition")
        
        return investigation_results
    
    def act(self, investigation: Dict[str, Any], uncertainty_scores: Dict[UncertaintyVector, float]) -> CascadeResult:
        """Stage 5: ACT - Generate final result with recommendations"""
        
        # Calculate overall confidence
        avg_uncertainty = sum(uncertainty_scores.values()) / len(uncertainty_scores)
        if avg_uncertainty < 0.4:
            confidence_level = "high"
        elif avg_uncertainty < 0.7:
            confidence_level = "medium" 
        else:
            confidence_level = "low"
        
        # Generate required actions
        required_actions = []
        if investigation["searches_needed"]:
            required_actions.extend(investigation["searches_needed"])
        if investigation["assumptions_identified"]:
            required_actions.append("flag_assumptions")
        if investigation["alternatives_considered"]:
            required_actions.append("present_alternatives")
        
        # Generate rationale
        high_uncertainty_vectors = [
            vector.value for vector, score in uncertainty_scores.items()
            if score > self.uncertainty_thresholds[vector]
        ]
        
        if high_uncertainty_vectors:
            rationale = f"High uncertainty in: {', '.join(high_uncertainty_vectors)}"
        else:
            rationale = "All uncertainty vectors within acceptable thresholds"
        
        return CascadeResult(
            stage="ACT",
            uncertainty_scores=uncertainty_scores,
            confidence_level=confidence_level,
            required_actions=required_actions,
            decision_rationale=rationale
        )
    
    def run_full_cascade(self, task: str, context: Dict[str, Any] = None) -> CascadeResult:
        """Run complete THINK→UNCERTAINTY→CHECK→INVESTIGATE→ACT cascade"""
        
        # Stage 1: THINK
        analysis = self.think(task, context)
        
        # Stage 2: UNCERTAINTY
        uncertainty_scores = self.assess_uncertainty(analysis)
        
        # Stage 3: CHECK
        checks = self.check(uncertainty_scores)
        
        # Stage 4: INVESTIGATE  
        investigation = self.investigate(checks, analysis.get("context", {}))
        
        # Stage 5: ACT
        result = self.act(investigation, uncertainty_scores)
        
        return result
