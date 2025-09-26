#!/usr/bin/env python3
"""
🎯 Advanced Uncertainty Engine - Enterprise Component
Multi-dimensional uncertainty assessment and investigation cascades

This enterprise component provides advanced uncertainty capabilities including:
- Multi-dimensional uncertainty assessment across multiple vectors
- Investigation cascades for uncertainty resolution
- Advanced confidence modeling and risk assessment
- Sophisticated uncertainty correlation analysis
"""

from typing import Dict, List, Optional, Any, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import math
import statistics
import threading

# ============================================================================
# ADVANCED UNCERTAINTY ANALYZER (from original advanced_uncertainty_investigator.py)
# ============================================================================

class UncertaintyDimension(Enum):
    """Dimensions of uncertainty analysis"""
    EPISTEMIC = "epistemic"  # Knowledge uncertainty
    ALEATORY = "aleatory"    # Inherent randomness
    LINGUISTIC = "linguistic"  # Language/communication uncertainty
    TEMPORAL = "temporal"    # Time-based uncertainty
    CONTEXTUAL = "contextual"  # Context-dependent uncertainty
    BEHAVIORAL = "behavioral"  # Behavioral prediction uncertainty
    DECISION = "decision"    # Decision-making uncertainty

class UncertaintyLevel(Enum):
    """Levels of uncertainty"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    CRITICAL = "critical"

@dataclass
class UncertaintyVector:
    """Represents uncertainty in a specific dimension"""
    dimension: UncertaintyDimension
    value: float  # 0.0 to 1.0
    confidence: float  # Confidence in the uncertainty measurement
    source: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    contributing_factors: List[str] = field(default_factory=list)

@dataclass
class UncertaintyAssessment:
    """Comprehensive uncertainty assessment"""
    assessment_id: str
    target: str
    vectors: List[UncertaintyVector]
    overall_uncertainty: float
    uncertainty_level: UncertaintyLevel
    risk_score: float
    recommendations: List[str]
    assessed_at: datetime
    expires_at: Optional[datetime] = None

class AdvancedUncertaintyAnalyzer:
    """
    Enterprise-grade uncertainty analyzer with multi-dimensional assessment
    """
    
    def __init__(self):
        self.uncertainty_history: Dict[str, List[UncertaintyAssessment]] = {}
        self.dimension_weights: Dict[UncertaintyDimension, float] = self._default_weights()
        self.uncertainty_thresholds: Dict[UncertaintyLevel, Tuple[float, float]] = self._default_thresholds()
        self.assessment_lock = threading.Lock()
        
    def assess_uncertainty(self, target: str, context: Dict[str, Any] = None) -> UncertaintyAssessment:
        """Perform comprehensive uncertainty assessment"""
        try:
            assessment_id = f"uncertainty_{target}_{datetime.now().timestamp()}"
            
            # Collect uncertainty vectors across all dimensions
            vectors = []
            for dimension in UncertaintyDimension:
                vector = self._assess_dimension(target, dimension, context or {})
                if vector:
                    vectors.append(vector)
            
            # Calculate overall uncertainty
            overall_uncertainty = self._calculate_overall_uncertainty(vectors)
            
            # Determine uncertainty level
            uncertainty_level = self._classify_uncertainty_level(overall_uncertainty)
            
            # Calculate risk score
            risk_score = self._calculate_risk_score(vectors, overall_uncertainty)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(vectors, uncertainty_level)
            
            # Create assessment
            assessment = UncertaintyAssessment(
                assessment_id=assessment_id,
                target=target,
                vectors=vectors,
                overall_uncertainty=overall_uncertainty,
                uncertainty_level=uncertainty_level,
                risk_score=risk_score,
                recommendations=recommendations,
                assessed_at=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=1)  # Default expiry
            )
            
            # Store in history
            with self.assessment_lock:
                if target not in self.uncertainty_history:
                    self.uncertainty_history[target] = []
                self.uncertainty_history[target].append(assessment)
                
                # Keep only last 10 assessments per target
                self.uncertainty_history[target] = self.uncertainty_history[target][-10:]
            
            print(f"🎯 Uncertainty assessed: {target} -> {uncertainty_level.value} ({overall_uncertainty:.3f})")
            return assessment
            
        except Exception as e:
            print(f"❌ Failed to assess uncertainty for {target}: {e}")
            # Return default high uncertainty assessment
            return self._create_error_assessment(target, str(e))
    
    def _assess_dimension(self, target: str, dimension: UncertaintyDimension, 
                         context: Dict[str, Any]) -> Optional[UncertaintyVector]:
        """Assess uncertainty in specific dimension"""
        try:
            if dimension == UncertaintyDimension.EPISTEMIC:
                return self._assess_epistemic_uncertainty(target, context)
            elif dimension == UncertaintyDimension.ALEATORY:
                return self._assess_aleatory_uncertainty(target, context)
            elif dimension == UncertaintyDimension.LINGUISTIC:
                return self._assess_linguistic_uncertainty(target, context)
            elif dimension == UncertaintyDimension.TEMPORAL:
                return self._assess_temporal_uncertainty(target, context)
            elif dimension == UncertaintyDimension.CONTEXTUAL:
                return self._assess_contextual_uncertainty(target, context)
            elif dimension == UncertaintyDimension.BEHAVIORAL:
                return self._assess_behavioral_uncertainty(target, context)
            elif dimension == UncertaintyDimension.DECISION:
                return self._assess_decision_uncertainty(target, context)
            
        except Exception as e:
            print(f"❌ Error assessing {dimension.value} uncertainty: {e}")
        
        return None
    
    def _assess_epistemic_uncertainty(self, target: str, context: Dict[str, Any]) -> UncertaintyVector:
        """Assess knowledge-based uncertainty"""
        # Factors: available information, data quality, knowledge gaps
        available_info = context.get('available_information', 0.5)
        data_quality = context.get('data_quality', 0.7)
        knowledge_gaps = context.get('knowledge_gaps', 0.3)
        
        # Calculate epistemic uncertainty
        uncertainty = 1.0 - (available_info * data_quality * (1.0 - knowledge_gaps))
        
        return UncertaintyVector(
            dimension=UncertaintyDimension.EPISTEMIC,
            value=max(0.0, min(1.0, uncertainty)),
            confidence=0.8,
            source="epistemic_analyzer",
            timestamp=datetime.now(),
            contributing_factors=["information_availability", "data_quality", "knowledge_gaps"]
        )
    
    def _assess_aleatory_uncertainty(self, target: str, context: Dict[str, Any]) -> UncertaintyVector:
        """Assess inherent randomness uncertainty"""
        # Factors: system randomness, environmental variability
        system_randomness = context.get('system_randomness', 0.2)
        environmental_variability = context.get('environmental_variability', 0.3)
        
        uncertainty = (system_randomness + environmental_variability) / 2
        
        return UncertaintyVector(
            dimension=UncertaintyDimension.ALEATORY,
            value=max(0.0, min(1.0, uncertainty)),
            confidence=0.7,
            source="aleatory_analyzer",
            timestamp=datetime.now(),
            contributing_factors=["system_randomness", "environmental_variability"]
        )
    
    def _assess_linguistic_uncertainty(self, target: str, context: Dict[str, Any]) -> UncertaintyVector:
        """Assess language/communication uncertainty"""
        # Factors: ambiguity, interpretation variance, communication clarity
        ambiguity = context.get('linguistic_ambiguity', 0.4)
        interpretation_variance = context.get('interpretation_variance', 0.3)
        
        uncertainty = (ambiguity + interpretation_variance) / 2
        
        return UncertaintyVector(
            dimension=UncertaintyDimension.LINGUISTIC,
            value=max(0.0, min(1.0, uncertainty)),
            confidence=0.6,
            source="linguistic_analyzer",
            timestamp=datetime.now(),
            contributing_factors=["ambiguity", "interpretation_variance"]
        )
    
    def _assess_temporal_uncertainty(self, target: str, context: Dict[str, Any]) -> UncertaintyVector:
        """Assess time-based uncertainty"""
        # Factors: prediction horizon, temporal stability, change rate
        prediction_horizon = context.get('prediction_horizon', 1.0)  # Normalized time
        temporal_stability = context.get('temporal_stability', 0.7)
        change_rate = context.get('change_rate', 0.3)
        
        uncertainty = (prediction_horizon * change_rate) / temporal_stability
        
        return UncertaintyVector(
            dimension=UncertaintyDimension.TEMPORAL,
            value=max(0.0, min(1.0, uncertainty)),
            confidence=0.7,
            source="temporal_analyzer",
            timestamp=datetime.now(),
            contributing_factors=["prediction_horizon", "temporal_stability", "change_rate"]
        )
    
    def _assess_contextual_uncertainty(self, target: str, context: Dict[str, Any]) -> UncertaintyVector:
        """Assess context-dependent uncertainty"""
        # Factors: context completeness, context stability, context relevance
        context_completeness = context.get('context_completeness', 0.6)
        context_stability = context.get('context_stability', 0.7)
        context_relevance = context.get('context_relevance', 0.8)
        
        uncertainty = 1.0 - (context_completeness * context_stability * context_relevance)
        
        return UncertaintyVector(
            dimension=UncertaintyDimension.CONTEXTUAL,
            value=max(0.0, min(1.0, uncertainty)),
            confidence=0.8,
            source="contextual_analyzer",
            timestamp=datetime.now(),
            contributing_factors=["context_completeness", "context_stability", "context_relevance"]
        )
    
    def _assess_behavioral_uncertainty(self, target: str, context: Dict[str, Any]) -> UncertaintyVector:
        """Assess behavioral prediction uncertainty"""
        # Factors: behavioral consistency, prediction accuracy, behavioral complexity
        behavioral_consistency = context.get('behavioral_consistency', 0.7)
        prediction_accuracy = context.get('prediction_accuracy', 0.6)
        behavioral_complexity = context.get('behavioral_complexity', 0.4)
        
        uncertainty = (behavioral_complexity + (1.0 - behavioral_consistency) + (1.0 - prediction_accuracy)) / 3
        
        return UncertaintyVector(
            dimension=UncertaintyDimension.BEHAVIORAL,
            value=max(0.0, min(1.0, uncertainty)),
            confidence=0.7,
            source="behavioral_analyzer",
            timestamp=datetime.now(),
            contributing_factors=["behavioral_consistency", "prediction_accuracy", "behavioral_complexity"]
        )
    
    def _assess_decision_uncertainty(self, target: str, context: Dict[str, Any]) -> UncertaintyVector:
        """Assess decision-making uncertainty"""
        # Factors: decision complexity, available options, outcome predictability
        decision_complexity = context.get('decision_complexity', 0.5)
        available_options = context.get('available_options', 3)  # Number of options
        outcome_predictability = context.get('outcome_predictability', 0.6)
        
        # Normalize available options (more options = more uncertainty)
        option_uncertainty = min(1.0, available_options / 10.0)
        
        uncertainty = (decision_complexity + option_uncertainty + (1.0 - outcome_predictability)) / 3
        
        return UncertaintyVector(
            dimension=UncertaintyDimension.DECISION,
            value=max(0.0, min(1.0, uncertainty)),
            confidence=0.8,
            source="decision_analyzer",
            timestamp=datetime.now(),
            contributing_factors=["decision_complexity", "available_options", "outcome_predictability"]
        )
    
    def _calculate_overall_uncertainty(self, vectors: List[UncertaintyVector]) -> float:
        """Calculate weighted overall uncertainty"""
        if not vectors:
            return 1.0  # Maximum uncertainty if no vectors
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for vector in vectors:
            weight = self.dimension_weights.get(vector.dimension, 1.0)
            weighted_sum += vector.value * weight * vector.confidence
            total_weight += weight * vector.confidence
        
        return weighted_sum / total_weight if total_weight > 0 else 1.0
    
    def _classify_uncertainty_level(self, uncertainty: float) -> UncertaintyLevel:
        """Classify uncertainty into discrete levels"""
        for level, (min_val, max_val) in self.uncertainty_thresholds.items():
            if min_val <= uncertainty < max_val:
                return level
        return UncertaintyLevel.CRITICAL  # Default for values >= 1.0
    
    def _calculate_risk_score(self, vectors: List[UncertaintyVector], overall_uncertainty: float) -> float:
        """Calculate risk score based on uncertainty assessment"""
        # Base risk from overall uncertainty
        base_risk = overall_uncertainty
        
        # Risk amplifiers
        high_uncertainty_dimensions = len([v for v in vectors if v.value > 0.7])
        low_confidence_vectors = len([v for v in vectors if v.confidence < 0.6])
        
        # Amplify risk based on problematic dimensions
        risk_amplifier = 1.0 + (high_uncertainty_dimensions * 0.1) + (low_confidence_vectors * 0.05)
        
        return min(1.0, base_risk * risk_amplifier)
    
    def _generate_recommendations(self, vectors: List[UncertaintyVector], 
                                level: UncertaintyLevel) -> List[str]:
        """Generate recommendations based on uncertainty assessment"""
        recommendations = []
        
        # Level-based recommendations
        if level in [UncertaintyLevel.HIGH, UncertaintyLevel.VERY_HIGH, UncertaintyLevel.CRITICAL]:
            recommendations.append("Consider additional information gathering before proceeding")
            recommendations.append("Implement uncertainty monitoring and contingency planning")
        
        # Dimension-specific recommendations
        high_uncertainty_vectors = [v for v in vectors if v.value > 0.6]
        for vector in high_uncertainty_vectors:
            if vector.dimension == UncertaintyDimension.EPISTEMIC:
                recommendations.append("Gather more information to reduce knowledge uncertainty")
            elif vector.dimension == UncertaintyDimension.TEMPORAL:
                recommendations.append("Consider shorter prediction horizons or temporal monitoring")
            elif vector.dimension == UncertaintyDimension.CONTEXTUAL:
                recommendations.append("Improve context understanding and stability")
            elif vector.dimension == UncertaintyDimension.BEHAVIORAL:
                recommendations.append("Enhance behavioral modeling and prediction accuracy")
            elif vector.dimension == UncertaintyDimension.DECISION:
                recommendations.append("Simplify decision space or improve outcome prediction")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _default_weights(self) -> Dict[UncertaintyDimension, float]:
        """Default weights for uncertainty dimensions"""
        return {
            UncertaintyDimension.EPISTEMIC: 1.2,
            UncertaintyDimension.ALEATORY: 0.8,
            UncertaintyDimension.LINGUISTIC: 0.9,
            UncertaintyDimension.TEMPORAL: 1.0,
            UncertaintyDimension.CONTEXTUAL: 1.1,
            UncertaintyDimension.BEHAVIORAL: 1.0,
            UncertaintyDimension.DECISION: 1.3
        }
    
    def _default_thresholds(self) -> Dict[UncertaintyLevel, Tuple[float, float]]:
        """Default thresholds for uncertainty levels"""
        return {
            UncertaintyLevel.VERY_LOW: (0.0, 0.2),
            UncertaintyLevel.LOW: (0.2, 0.4),
            UncertaintyLevel.MEDIUM: (0.4, 0.6),
            UncertaintyLevel.HIGH: (0.6, 0.8),
            UncertaintyLevel.VERY_HIGH: (0.8, 0.9),
            UncertaintyLevel.CRITICAL: (0.9, 1.0)
        }
    
    def _create_error_assessment(self, target: str, error: str) -> UncertaintyAssessment:
        """Create error assessment with maximum uncertainty"""
        return UncertaintyAssessment(
            assessment_id=f"error_{target}_{datetime.now().timestamp()}",
            target=target,
            vectors=[],
            overall_uncertainty=1.0,
            uncertainty_level=UncertaintyLevel.CRITICAL,
            risk_score=1.0,
            recommendations=[f"Assessment failed: {error}", "Manual review required"],
            assessed_at=datetime.now()
        )
    
    def get_uncertainty_trend(self, target: str, window_hours: int = 24) -> Dict[str, Any]:
        """Get uncertainty trend for target over time window"""
        if target not in self.uncertainty_history:
            return {'error': 'No history available'}
        
        cutoff_time = datetime.now() - timedelta(hours=window_hours)
        recent_assessments = [
            a for a in self.uncertainty_history[target] 
            if a.assessed_at >= cutoff_time
        ]
        
        if not recent_assessments:
            return {'error': 'No recent assessments'}
        
        uncertainties = [a.overall_uncertainty for a in recent_assessments]
        risk_scores = [a.risk_score for a in recent_assessments]
        
        return {
            'target': target,
            'assessment_count': len(recent_assessments),
            'uncertainty_trend': {
                'current': uncertainties[-1],
                'average': statistics.mean(uncertainties),
                'min': min(uncertainties),
                'max': max(uncertainties),
                'std_dev': statistics.stdev(uncertainties) if len(uncertainties) > 1 else 0.0
            },
            'risk_trend': {
                'current': risk_scores[-1],
                'average': statistics.mean(risk_scores),
                'min': min(risk_scores),
                'max': max(risk_scores)
            },
            'trend_direction': 'increasing' if uncertainties[-1] > uncertainties[0] else 'decreasing'
        }
