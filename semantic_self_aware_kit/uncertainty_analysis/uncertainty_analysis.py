#!/usr/bin/env python3
"""
🤔 Uncertainty Analysis Module
Advanced uncertainty quantification and investigation for AI systems

This module provides sophisticated uncertainty analysis capabilities including:
- Multi-dimensional uncertainty quantification
- Systematic uncertainty investigation
- Confidence assessment and improvement
- Meta-cognitive validation processes
"""

import json
import math
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class UncertaintyType(Enum):
    """Types of uncertainty in AI reasoning"""
    EPISTEMIC = "epistemic"  # Knowledge uncertainty
    ALEATORIC = "aleatoric"  # Inherent randomness
    CONTEXTUAL = "contextual"  # Context-dependent
    TEMPORAL = "temporal"  # Time-dependent
    SEMANTIC = "semantic"  # Meaning uncertainty
    CAUSAL = "causal"  # Cause-effect uncertainty

class InvestigationDepth(Enum):
    """Investigation depth levels"""
    SURFACE = "surface"  # Quick confidence check
    ANALYTICAL = "analytical"  # Structured analysis
    COMPREHENSIVE = "comprehensive"  # Deep investigation
    RECURSIVE = "recursive"  # Self-improving investigation

@dataclass
class UncertaintyVector:
    """Multi-dimensional uncertainty representation"""
    epistemic: float  # 0.0-1.0
    aleatoric: float  # 0.0-1.0
    contextual: float  # 0.0-1.0
    temporal: float  # 0.0-1.0
    semantic: float  # 0.0-1.0
    causal: float  # 0.0-1.0
    
    @property
    def magnitude(self) -> float:
        """Calculate uncertainty magnitude"""
        return math.sqrt(sum([
            self.epistemic**2, self.aleatoric**2, self.contextual**2,
            self.temporal**2, self.semantic**2, self.causal**2
        ]) / 6)
    
    @property
    def dominant_type(self) -> UncertaintyType:
        """Find the dominant uncertainty type"""
        values = {
            UncertaintyType.EPISTEMIC: self.epistemic,
            UncertaintyType.ALEATORIC: self.aleatoric,
            UncertaintyType.CONTEXTUAL: self.contextual,
            UncertaintyType.TEMPORAL: self.temporal,
            UncertaintyType.SEMANTIC: self.semantic,
            UncertaintyType.CAUSAL: self.causal
        }
        return max(values, key=values.get)

@dataclass
class InvestigationResult:
    """Result of uncertainty investigation"""
    original_uncertainty: float
    final_uncertainty: float
    uncertainty_vector: UncertaintyVector
    investigation_path: List[str]
    confidence_improvement: float
    recommendations: List[str]
    meta_insights: Dict[str, Any]
    investigation_quality: float

class MultiDimensionalUncertaintyAnalyzer:
    """Multi-Dimensional Uncertainty Analysis system"""
    
    def __init__(self):
        """Initialize the Multi-Dimensional Uncertainty Analyzer"""
        self.investigation_history = []
        self.pattern_library = self._build_pattern_library()
        self.meta_cognitive_threshold = 0.85
    
    def _build_pattern_library(self) -> Dict[str, Any]:
        """Build library of investigation patterns"""
        return {
            "epistemic_patterns": {
                "knowledge_gap": "Identify missing information",
                "source_validation": "Verify information sources",
                "cross_reference": "Compare multiple sources",
                "expert_consultation": "Seek domain expertise"
            },
            "contextual_patterns": {
                "context_expansion": "Broaden contextual understanding",
                "assumption_validation": "Question underlying assumptions",
                "perspective_shift": "Consider alternative viewpoints",
                "boundary_analysis": "Define problem boundaries"
            },
            "causal_patterns": {
                "causal_chain": "Trace cause-effect relationships",
                "confounding_factors": "Identify confounding variables",
                "mechanism_analysis": "Understand underlying mechanisms",
                "counterfactual": "Consider alternative scenarios"
            },
            "semantic_patterns": {
                "definition_clarity": "Clarify term definitions",
                "ambiguity_resolution": "Resolve semantic ambiguity",
                "concept_mapping": "Map conceptual relationships",
                "precision_enhancement": "Increase semantic precision"
            }
        }
    
    def analyze_uncertainty(self, decision: str, context: Dict[str, Any]) -> UncertaintyVector:
        """Analyze uncertainty across multiple dimensions"""
        # Epistemic uncertainty - knowledge gaps
        epistemic = self._assess_epistemic_uncertainty(decision, context)
        
        # Aleatoric uncertainty - inherent randomness
        aleatoric = self._assess_aleatoric_uncertainty(decision, context)
        
        # Contextual uncertainty - context dependency
        contextual = self._assess_contextual_uncertainty(decision, context)
        
        # Temporal uncertainty - time dependency
        temporal = self._assess_temporal_uncertainty(decision, context)
        
        # Semantic uncertainty - meaning clarity
        semantic = self._assess_semantic_uncertainty(decision, context)
        
        # Causal uncertainty - cause-effect clarity
        causal = self._assess_causal_uncertainty(decision, context)
        
        return UncertaintyVector(
            epistemic=epistemic,
            aleatoric=aleatoric,
            contextual=contextual,
            temporal=temporal,
            semantic=semantic,
            causal=causal
        )
    
    def investigate_uncertainty(
        self, 
        decision: str, 
        context: Dict[str, Any],
        depth: InvestigationDepth = InvestigationDepth.ANALYTICAL,
        target_confidence: float = 0.8
    ) -> InvestigationResult:
        """Conduct sophisticated uncertainty investigation"""
        start_time = time.time()
        
        # Initial uncertainty analysis
        uncertainty_vector = self.analyze_uncertainty(decision, context)
        original_uncertainty = uncertainty_vector.magnitude
        
        # Determine investigation strategy
        strategy = self._select_investigation_strategy(uncertainty_vector, depth)
        
        # Execute investigation
        investigation_path = []
        current_uncertainty = original_uncertainty
        
        for step in strategy:
            step_result = self._execute_investigation_step(
                step, decision, context, uncertainty_vector
            )
            investigation_path.append(step_result["description"])
            current_uncertainty *= step_result["uncertainty_reduction"]
            
            # Check if target confidence reached
            if (1 - current_uncertainty) >= target_confidence:
                break
        
        # Meta-cognitive validation
        if (1 - current_uncertainty) >= self.meta_cognitive_threshold:
            meta_validation = self._meta_cognitive_validation(
                decision, context, investigation_path
            )
            investigation_path.extend(meta_validation["additional_steps"])
            current_uncertainty *= meta_validation["uncertainty_reduction"]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            uncertainty_vector, investigation_path, current_uncertainty
        )
        
        # Calculate investigation quality
        investigation_quality = self._assess_investigation_quality(
            original_uncertainty, current_uncertainty, len(investigation_path)
        )
        
        # Meta insights
        meta_insights = {
            "dominant_uncertainty_type": uncertainty_vector.dominant_type.value,
            "investigation_efficiency": (original_uncertainty - current_uncertainty) / len(investigation_path),
            "investigation_time": time.time() - start_time,
            "pattern_effectiveness": self._assess_pattern_effectiveness(investigation_path)
        }
        
        result = InvestigationResult(
            original_uncertainty=original_uncertainty,
            final_uncertainty=current_uncertainty,
            uncertainty_vector=uncertainty_vector,
            investigation_path=investigation_path,
            confidence_improvement=(1 - current_uncertainty) - (1 - original_uncertainty),
            recommendations=recommendations,
            meta_insights=meta_insights,
            investigation_quality=investigation_quality
        )
        
        # Store for learning
        self.investigation_history.append(result)
        
        return result
    
    def _assess_epistemic_uncertainty(self, decision: str, context: Dict[str, Any]) -> float:
        """Assess knowledge-based uncertainty"""
        # Analyze information completeness
        info_completeness = context.get("information_completeness", 0.5)
        source_reliability = context.get("source_reliability", 0.7)
        domain_expertise = context.get("domain_expertise", 0.6)
        
        # Calculate epistemic uncertainty
        epistemic = 1.0 - (info_completeness * source_reliability * domain_expertise)
        return max(0.0, min(1.0, epistemic))
    
    def _assess_aleatoric_uncertainty(self, decision: str, context: Dict[str, Any]) -> float:
        """Assess inherent randomness uncertainty"""
        # Analyze inherent variability
        data_variability = context.get("data_variability", 0.3)
        process_randomness = context.get("process_randomness", 0.2)
        measurement_noise = context.get("measurement_noise", 0.1)
        
        aleatoric = (data_variability + process_randomness + measurement_noise) / 3
        return max(0.0, min(1.0, aleatoric))
    
    def _assess_contextual_uncertainty(self, decision: str, context: Dict[str, Any]) -> float:
        """Assess context-dependent uncertainty"""
        # Analyze context stability and clarity
        context_stability = context.get("context_stability", 0.7)
        assumption_validity = context.get("assumption_validity", 0.8)
        boundary_clarity = context.get("boundary_clarity", 0.6)
        
        contextual = 1.0 - (context_stability * assumption_validity * boundary_clarity)
        return max(0.0, min(1.0, contextual))
    
    def _assess_temporal_uncertainty(self, decision: str, context: Dict[str, Any]) -> float:
        """Assess time-dependent uncertainty"""
        # Analyze temporal factors
        time_sensitivity = context.get("time_sensitivity", 0.5)
        prediction_horizon = context.get("prediction_horizon", 0.3)
        change_rate = context.get("change_rate", 0.4)
        
        temporal = (time_sensitivity + prediction_horizon + change_rate) / 3
        return max(0.0, min(1.0, temporal))
    
    def _assess_semantic_uncertainty(self, decision: str, context: Dict[str, Any]) -> float:
        """Assess meaning and definition uncertainty"""
        # Analyze semantic clarity
        definition_clarity = context.get("definition_clarity", 0.8)
        ambiguity_level = context.get("ambiguity_level", 0.3)
        concept_precision = context.get("concept_precision", 0.7)
        
        semantic = 1.0 - (definition_clarity * (1 - ambiguity_level) * concept_precision)
        return max(0.0, min(1.0, semantic))
    
    def _assess_causal_uncertainty(self, decision: str, context: Dict[str, Any]) -> float:
        """Assess cause-effect relationship uncertainty"""
        # Analyze causal clarity
        causal_clarity = context.get("causal_clarity", 0.6)
        mechanism_understanding = context.get("mechanism_understanding", 0.5)
        confounding_factors = context.get("confounding_factors", 0.4)
        
        causal = 1.0 - (causal_clarity * mechanism_understanding * (1 - confounding_factors))
        return max(0.0, min(1.0, causal))
    
    def _select_investigation_strategy(
        self, 
        uncertainty_vector: UncertaintyVector, 
        depth: InvestigationDepth
    ) -> List[str]:
        """Select investigation strategy based on uncertainty profile"""
        
        strategy = []
        dominant_type = uncertainty_vector.dominant_type
        
        # Base strategy on dominant uncertainty type
        if dominant_type == UncertaintyType.EPISTEMIC:
            strategy.extend(["knowledge_gap_analysis", "source_validation", "expert_consultation"])
        elif dominant_type == UncertaintyType.CONTEXTUAL:
            strategy.extend(["context_expansion", "assumption_validation", "boundary_analysis"])
        elif dominant_type == UncertaintyType.CAUSAL:
            strategy.extend(["causal_chain_analysis", "mechanism_investigation", "counterfactual_analysis"])
        elif dominant_type == UncertaintyType.SEMANTIC:
            strategy.extend(["definition_clarification", "ambiguity_resolution", "concept_mapping"])
        elif dominant_type == UncertaintyType.TEMPORAL:
            strategy.extend(["temporal_analysis", "trend_investigation", "stability_assessment"])
        else:  # ALEATORIC
            strategy.extend(["variability_analysis", "noise_assessment", "randomness_quantification"])
        
        # Add depth-specific steps
        if depth in [InvestigationDepth.COMPREHENSIVE, InvestigationDepth.RECURSIVE]:
            strategy.extend(["cross_validation", "alternative_perspectives", "meta_analysis"])
        
        if depth == InvestigationDepth.RECURSIVE:
            strategy.extend(["recursive_validation", "self_consistency_check", "investigation_quality_assessment"])
        
        return strategy
    
    def _execute_investigation_step(
        self, 
        step: str, 
        decision: str, 
        context: Dict[str, Any],
        uncertainty_vector: UncertaintyVector
    ) -> Dict[str, Any]:
        """Execute a single investigation step"""
        
        # Simulate investigation step execution
        # In real implementation, this would perform actual investigation
        
        step_descriptions = {
            "knowledge_gap_analysis": "Analyzed information gaps and identified missing knowledge areas",
            "source_validation": "Validated information sources and assessed reliability",
            "expert_consultation": "Consulted domain expertise and cross-referenced findings",
            "context_expansion": "Expanded contextual understanding and identified relevant factors",
            "assumption_validation": "Questioned and validated underlying assumptions",
            "boundary_analysis": "Clarified problem boundaries and scope limitations",
            "causal_chain_analysis": "Traced causal relationships and identified key factors",
            "mechanism_investigation": "Investigated underlying mechanisms and processes",
            "counterfactual_analysis": "Considered alternative scenarios and outcomes",
            "definition_clarification": "Clarified definitions and resolved semantic ambiguity",
            "ambiguity_resolution": "Resolved semantic ambiguity and improved precision",
            "concept_mapping": "Mapped conceptual relationships and dependencies",
            "temporal_analysis": "Analyzed temporal factors and time dependencies",
            "trend_investigation": "Investigated trends and temporal patterns",
            "stability_assessment": "Assessed stability and change patterns",
            "variability_analysis": "Analyzed inherent variability and randomness",
            "noise_assessment": "Assessed measurement noise and data quality",
            "randomness_quantification": "Quantified inherent randomness and uncertainty",
            "cross_validation": "Cross-validated findings across multiple approaches",
            "alternative_perspectives": "Considered alternative perspectives and viewpoints",
            "meta_analysis": "Conducted meta-analysis of investigation findings",
            "recursive_validation": "Recursively validated investigation methodology",
            "self_consistency_check": "Checked self-consistency of findings",
            "investigation_quality_assessment": "Assessed quality and completeness of investigation"
        }
        
        # Calculate uncertainty reduction based on step type and uncertainty profile
        base_reduction = 0.85  # 15% reduction per step
        
        # Adjust based on step effectiveness for uncertainty type
        if step in ["knowledge_gap_analysis", "source_validation", "expert_consultation"]:
            if uncertainty_vector.dominant_type == UncertaintyType.EPISTEMIC:
                base_reduction = 0.75  # 25% reduction for matched type
        elif step in ["context_expansion", "assumption_validation", "boundary_analysis"]:
            if uncertainty_vector.dominant_type == UncertaintyType.CONTEXTUAL:
                base_reduction = 0.75
        # ... similar logic for other step types
        
        return {
            "description": step_descriptions.get(step, f"Executed {step}"),
            "uncertainty_reduction": base_reduction,
            "step_quality": 0.8 + (0.2 * (1 - uncertainty_vector.magnitude))
        }
    
    def _meta_cognitive_validation(
        self, 
        decision: str, 
        context: Dict[str, Any], 
        investigation_path: List[str]
    ) -> Dict[str, Any]:
        """Perform meta-cognitive validation of investigation"""
        
        additional_steps = []
        uncertainty_reduction = 1.0
        
        # Check investigation completeness
        if len(investigation_path) < 3:
            additional_steps.append("Investigation depth validation - expanded analysis")
            uncertainty_reduction *= 0.9
        
        # Check for bias in investigation
        if "alternative_perspectives" not in str(investigation_path):
            additional_steps.append("Bias check - considered alternative viewpoints")
            uncertainty_reduction *= 0.95
        
        # Validate investigation methodology
        additional_steps.append("Meta-cognitive validation - verified investigation quality")
        uncertainty_reduction *= 0.92
        
        return {
            "additional_steps": additional_steps,
            "uncertainty_reduction": uncertainty_reduction
        }
    
    def _generate_recommendations(
        self, 
        uncertainty_vector: UncertaintyVector, 
        investigation_path: List[str], 
        final_uncertainty: float
    ) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Confidence-based recommendations
        confidence = 1 - final_uncertainty
        if confidence >= 0.9:
            recommendations.append("High confidence achieved - proceed with decision")
        elif confidence >= 0.7:
            recommendations.append("Moderate confidence - consider additional validation")
        else:
            recommendations.append("Low confidence - further investigation recommended")
        
        # Uncertainty-type specific recommendations
        dominant_type = uncertainty_vector.dominant_type
        if dominant_type == UncertaintyType.EPISTEMIC:
            recommendations.append("Seek additional information or expert consultation")
        elif dominant_type == UncertaintyType.CONTEXTUAL:
            recommendations.append("Clarify context and validate assumptions")
        elif dominant_type == UncertaintyType.CAUSAL:
            recommendations.append("Investigate causal mechanisms more thoroughly")
        
        # Investigation quality recommendations
        if len(investigation_path) < 3:
            recommendations.append("Consider more comprehensive investigation")
        
        return recommendations
    
    def _assess_investigation_quality(
        self, 
        original_uncertainty: float, 
        final_uncertainty: float, 
        steps_taken: int
    ) -> float:
        """Assess the quality of the investigation"""
        
        # Calculate uncertainty reduction efficiency
        uncertainty_reduction = original_uncertainty - final_uncertainty
        efficiency = uncertainty_reduction / steps_taken if steps_taken > 0 else 0
        
        # Quality factors
        completeness = min(1.0, steps_taken / 5)  # Optimal around 5 steps
        effectiveness = uncertainty_reduction / original_uncertainty
        
        # Overall quality score
        quality = (efficiency * 0.4 + completeness * 0.3 + effectiveness * 0.3)
        return max(0.0, min(1.0, quality))
    
    def _assess_pattern_effectiveness(self, investigation_path: List[str]) -> Dict[str, float]:
        """Assess effectiveness of investigation patterns used"""
        
        pattern_counts = {}
        for step in investigation_path:
            for pattern_type, patterns in self.pattern_library.items():
                for pattern_name in patterns:
                    if pattern_name.replace(" ", "_") in step.lower():
                        pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        # Calculate effectiveness scores
        total_steps = len(investigation_path)
        effectiveness = {}
        for pattern_type, count in pattern_counts.items():
            effectiveness[pattern_type] = count / total_steps if total_steps > 0 else 0
        
        return effectiveness
