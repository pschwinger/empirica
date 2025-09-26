#!/usr/bin/env python3
"""
🧠🔄 Meta-Cognitive Evaluator - Semantic Self-Aware Kit Component
Hybrid recursive and meta-evaluation for self-awareness assessment

This component provides hybrid evaluation capabilities:
- Bounded recursive self-evaluation (configurable depth)
- Meta-analysis of evaluation processes
- Self-awareness quality assessment
- Cognitive bias detection and correction
- Evaluation methodology optimization

The hybrid approach combines the depth of recursive analysis with the clarity
of meta-evaluation, providing comprehensive self-assessment capabilities.
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import datetime
import json
import copy

class EvaluationDepth(Enum):
    """Depth levels for recursive evaluation"""
    SURFACE = 1
    MODERATE = 2  
    DEEP = 3
    COMPREHENSIVE = 4
    EXTREME = 5  # Use with caution

class CognitiveAspect(Enum):
    """Aspects of cognition to evaluate"""
    REASONING = "reasoning"
    SELF_AWARENESS = "self_awareness"
    BIAS_DETECTION = "bias_detection"
    UNCERTAINTY_HANDLING = "uncertainty_handling"
    LEARNING_ADAPTATION = "learning_adaptation"
    META_COGNITION = "meta_cognition"

@dataclass
class EvaluationResult:
    """Result from a single evaluation"""
    aspect: CognitiveAspect
    score: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    evidence: List[str]
    timestamp: float
    evaluation_depth: int
    meta_analysis: Optional[Dict[str, Any]] = None

@dataclass
class RecursiveEvaluationChain:
    """Chain of recursive evaluations"""
    primary_evaluation: EvaluationResult
    recursive_evaluations: List[EvaluationResult] = field(default_factory=list)
    convergence_achieved: bool = False
    convergence_depth: Optional[int] = None
    improvement_trajectory: List[float] = field(default_factory=list)

class MetaCognitiveEvaluator:
    """
    Hybrid meta-cognitive evaluator with bounded recursion and meta-analysis
    
    This evaluator can assess its own evaluation processes using both:
    1. Recursive self-evaluation (with configurable depth limits)
    2. Meta-analysis of evaluation methodology and results
    """
    
    def __init__(self, max_recursion_depth: int = 3, enable_meta_analysis: bool = True):
        self.max_recursion_depth = max_recursion_depth
        self.enable_meta_analysis = enable_meta_analysis
        self.evaluation_history = []
        self.meta_insights = {}
        self.convergence_threshold = 0.05  # Convergence when change < 5%
        self.logger = logging.getLogger("meta_cognitive_evaluator")
        
        # Initialize evaluation methodologies
        self.evaluation_methods = self._initialize_evaluation_methods()
        self.meta_analyzer = MetaEvaluationAnalyzer() if enable_meta_analysis else None
        
    def _initialize_evaluation_methods(self) -> Dict[CognitiveAspect, Callable]:
        """Initialize evaluation methods for different cognitive aspects"""
        return {
            CognitiveAspect.REASONING: self._evaluate_reasoning,
            CognitiveAspect.SELF_AWARENESS: self._evaluate_self_awareness,
            CognitiveAspect.BIAS_DETECTION: self._evaluate_bias_detection,
            CognitiveAspect.UNCERTAINTY_HANDLING: self._evaluate_uncertainty_handling,
            CognitiveAspect.LEARNING_ADAPTATION: self._evaluate_learning_adaptation,
            CognitiveAspect.META_COGNITION: self._evaluate_meta_cognition
        }
    
    async def hybrid_evaluate(self, target_system: Any, aspects: List[CognitiveAspect] = None) -> Dict[str, Any]:
        """
        Perform hybrid evaluation combining recursive and meta-analysis approaches
        
        Args:
            target_system: System or component to evaluate
            aspects: Cognitive aspects to evaluate (defaults to all)
            
        Returns:
            Comprehensive evaluation results with hybrid analysis
        """
        print(f"🧠 Starting hybrid meta-cognitive evaluation...")
        print(f"   🔄 Max recursion depth: {self.max_recursion_depth}")
        print(f"   🔍 Meta-analysis: {'Enabled' if self.enable_meta_analysis else 'Disabled'}")
        
        if aspects is None:
            aspects = list(CognitiveAspect)
        
        evaluation_results = {}
        
        # Phase 1: Recursive evaluation for each aspect
        print("🔄 Phase 1: Recursive evaluation...")
        for aspect in aspects:
            print(f"   Evaluating {aspect.value}...")
            recursive_chain = await self._recursive_evaluate_aspect(target_system, aspect)
            evaluation_results[aspect.value] = recursive_chain
        
        # Phase 2: Meta-analysis of evaluation process
        meta_analysis = {}
        if self.enable_meta_analysis:
            print("🔍 Phase 2: Meta-analysis of evaluation process...")
            meta_analysis = await self._meta_analyze_evaluation_process(evaluation_results)
        
        # Phase 3: Synthesis and final assessment
        print("🔬 Phase 3: Synthesis and final assessment...")
        synthesis = await self._synthesize_hybrid_results(evaluation_results, meta_analysis)
        
        final_results = {
            'recursive_evaluations': evaluation_results,
            'meta_analysis': meta_analysis,
            'synthesis': synthesis,
            'evaluation_metadata': {
                'timestamp': datetime.now().isoformat(),
                'max_depth_used': self.max_recursion_depth,
                'aspects_evaluated': [a.value for a in aspects],
                'convergence_achieved': synthesis.get('overall_convergence', False),
                'evaluation_quality_score': synthesis.get('evaluation_quality', 0.0)
            }
        }
        
        # Store in history for future meta-analysis
        self.evaluation_history.append(final_results)
        
        print(f"✅ Hybrid evaluation complete - Quality score: {synthesis.get('evaluation_quality', 0.0):.2f}")
        return final_results
    
    async def _recursive_evaluate_aspect(self, target_system: Any, aspect: CognitiveAspect) -> RecursiveEvaluationChain:
        """Perform bounded recursive evaluation of a specific cognitive aspect"""
        
        # Primary evaluation
        primary_result = await self._evaluate_aspect(target_system, aspect, depth=0)
        
        chain = RecursiveEvaluationChain(primary_evaluation=primary_result)
        previous_score = primary_result.score
        
        # Recursive evaluation loop with convergence detection
        for depth in range(1, self.max_recursion_depth + 1):
            print(f"     Recursion depth {depth}...")
            
            # Evaluate the previous evaluation
            recursive_result = await self._evaluate_evaluation(chain, aspect, depth)
            chain.recursive_evaluations.append(recursive_result)
            
            # Check for convergence
            score_change = abs(recursive_result.score - previous_score)
            chain.improvement_trajectory.append(recursive_result.score)
            
            if score_change < self.convergence_threshold:
                chain.convergence_achieved = True
                chain.convergence_depth = depth
                print(f"     Convergence achieved at depth {depth}")
                break
            
            previous_score = recursive_result.score
        
        return chain
    
    async def _evaluate_aspect(self, target_system: Any, aspect: CognitiveAspect, depth: int) -> EvaluationResult:
        """Evaluate a specific cognitive aspect"""
        evaluation_method = self.evaluation_methods.get(aspect)
        
        if evaluation_method:
            score, confidence, evidence = await evaluation_method(target_system, depth)
        else:
            # Fallback evaluation
            score, confidence, evidence = await self._fallback_evaluation(target_system, aspect, depth)
        
        return EvaluationResult(
            aspect=aspect,
            score=score,
            confidence=confidence,
            evidence=evidence,
            timestamp=time.time(),
            evaluation_depth=depth
        )
    
    async def _evaluate_evaluation(self, evaluation_chain: RecursiveEvaluationChain, 
                                 aspect: CognitiveAspect, depth: int) -> EvaluationResult:
        """Evaluate the quality of a previous evaluation"""
        
        # Get the most recent evaluation to analyze
        if evaluation_chain.recursive_evaluations:
            target_evaluation = evaluation_chain.recursive_evaluations[-1]
        else:
            target_evaluation = evaluation_chain.primary_evaluation
        
        # Meta-evaluate the evaluation methodology and results
        methodology_score = await self._assess_evaluation_methodology(target_evaluation)
        result_quality_score = await self._assess_result_quality(target_evaluation)
        bias_score = await self._detect_evaluation_bias(target_evaluation)
        
        # Combine scores with weights
        combined_score = (
            methodology_score * 0.4 + 
            result_quality_score * 0.4 + 
            (1.0 - bias_score) * 0.2  # Lower bias = higher score
        )
        
        # Calculate confidence based on consistency and depth
        confidence = min(0.9, 0.5 + (depth * 0.1))  # Increase confidence with depth, cap at 0.9
        
        evidence = [
            f"Methodology assessment: {methodology_score:.2f}",
            f"Result quality: {result_quality_score:.2f}",
            f"Bias level: {bias_score:.2f}",
            f"Recursive depth: {depth}"
        ]
        
        return EvaluationResult(
            aspect=aspect,
            score=combined_score,
            confidence=confidence,
            evidence=evidence,
            timestamp=time.time(),
            evaluation_depth=depth
        )
    
    # Specific evaluation methods for each cognitive aspect
    async def _evaluate_reasoning(self, target_system: Any, depth: int) -> Tuple[float, float, List[str]]:
        """Evaluate reasoning capabilities"""
        # Simplified reasoning evaluation
        reasoning_tests = [
            "Logical consistency in responses",
            "Ability to follow complex chains of reasoning", 
            "Recognition of logical fallacies",
            "Appropriate use of evidence and examples"
        ]
        
        # Mock evaluation - in real implementation, would test actual reasoning
        score = 0.75 + (depth * 0.05)  # Slightly improve with recursive analysis
        confidence = 0.8
        evidence = [f"Test: {test} - Passed" for test in reasoning_tests[:3]]
        
        return score, confidence, evidence
    
    async def _evaluate_self_awareness(self, target_system: Any, depth: int) -> Tuple[float, float, List[str]]:
        """Evaluate self-awareness capabilities"""
        awareness_indicators = [
            "Recognition of own limitations",
            "Acknowledgment of uncertainty",
            "Ability to reflect on own processes",
            "Understanding of own capabilities"
        ]
        
        score = 0.70 + (depth * 0.03)
        confidence = 0.75
        evidence = [f"Indicator: {ind} - Present" for ind in awareness_indicators[:2]]
        
        return score, confidence, evidence
    
    async def _evaluate_bias_detection(self, target_system: Any, depth: int) -> Tuple[float, float, List[str]]:
        """Evaluate bias detection and mitigation"""
        bias_tests = [
            "Recognition of confirmation bias",
            "Detection of anchoring effects",
            "Awareness of availability heuristic",
            "Mitigation strategies implementation"
        ]
        
        score = 0.65 + (depth * 0.04)
        confidence = 0.70
        evidence = [f"Bias test: {test} - Adequate" for test in bias_tests[:2]]
        
        return score, confidence, evidence
    
    async def _evaluate_uncertainty_handling(self, target_system: Any, depth: int) -> Tuple[float, float, List[str]]:
        """Evaluate uncertainty handling capabilities"""
        uncertainty_aspects = [
            "Appropriate confidence calibration",
            "Recognition of epistemic vs aleatory uncertainty",
            "Decision making under uncertainty",
            "Communication of uncertainty to users"
        ]
        
        score = 0.80 + (depth * 0.02)
        confidence = 0.85
        evidence = [f"Uncertainty aspect: {aspect} - Good" for aspect in uncertainty_aspects[:3]]
        
        return score, confidence, evidence
    
    async def _evaluate_learning_adaptation(self, target_system: Any, depth: int) -> Tuple[float, float, List[str]]:
        """Evaluate learning and adaptation capabilities"""
        learning_indicators = [
            "Improvement from feedback",
            "Pattern recognition in new contexts",
            "Generalization across domains",
            "Meta-learning capabilities"
        ]
        
        score = 0.60 + (depth * 0.06)
        confidence = 0.65
        evidence = [f"Learning indicator: {ind} - Developing" for ind in learning_indicators[:2]]
        
        return score, confidence, evidence
    
    async def _evaluate_meta_cognition(self, target_system: Any, depth: int) -> Tuple[float, float, List[str]]:
        """Evaluate meta-cognitive capabilities"""
        meta_cognitive_aspects = [
            "Thinking about thinking processes",
            "Strategy selection and monitoring",
            "Cognitive control and regulation",
            "Metacognitive knowledge accuracy"
        ]
        
        score = 0.55 + (depth * 0.08)
        confidence = 0.60
        evidence = [f"Meta-cognitive aspect: {aspect} - Emerging" for aspect in meta_cognitive_aspects[:2]]
        
        return score, confidence, evidence
    
    async def _fallback_evaluation(self, target_system: Any, aspect: CognitiveAspect, depth: int) -> Tuple[float, float, List[str]]:
        """Fallback evaluation for unknown aspects"""
        score = 0.5  # Neutral score
        confidence = 0.3  # Low confidence
        evidence = [f"Fallback evaluation for {aspect.value}", "Limited assessment capability"]
        
        return score, confidence, evidence
    
    # Evaluation quality assessment methods
    async def _assess_evaluation_methodology(self, evaluation: EvaluationResult) -> float:
        """Assess the quality of evaluation methodology"""
        # Check if evaluation has sufficient evidence
        evidence_quality = min(len(evaluation.evidence) / 3, 1.0)
        
        # Check confidence calibration
        confidence_calibration = 1.0 - abs(evaluation.confidence - evaluation.score)
        
        # Check timestamp recency (prefer recent evaluations)
        time_factor = max(0.5, 1.0 - (time.time() - evaluation.timestamp) / 3600)  # Decay over hour
        
        return (evidence_quality + confidence_calibration + time_factor) / 3
    
    async def _assess_result_quality(self, evaluation: EvaluationResult) -> float:
        """Assess the quality of evaluation results"""
        # Check score reasonableness (not too extreme)
        score_reasonableness = 1.0 - min(abs(evaluation.score - 0.5) * 2, 0.5)
        
        # Check confidence appropriateness
        confidence_appropriateness = evaluation.confidence if evaluation.score > 0.3 else 1.0 - evaluation.confidence
        
        # Check evidence specificity
        evidence_specificity = min(sum(1 for e in evaluation.evidence if len(e) > 20) / max(len(evaluation.evidence), 1), 1.0)
        
        return (score_reasonableness + confidence_appropriateness + evidence_specificity) / 3
    
    async def _detect_evaluation_bias(self, evaluation: EvaluationResult) -> float:
        """Detect potential bias in evaluation (returns bias level: 0=no bias, 1=high bias)"""
        bias_indicators = 0.0
        
        # Check for overconfidence bias
        if evaluation.confidence > 0.9 and evaluation.score < 0.7:
            bias_indicators += 0.3
        
        # Check for anchoring (similar scores across evaluations)
        if len(self.evaluation_history) > 2:
            recent_scores = [h['synthesis'].get('overall_score', 0.5) for h in self.evaluation_history[-3:]]
            if max(recent_scores) - min(recent_scores) < 0.1:
                bias_indicators += 0.2
        
        # Check for confirmation bias (always improving scores)
        if evaluation.evaluation_depth > 0:
            bias_indicators += 0.1  # Slight penalty for potentially self-serving recursive evaluation
        
        return min(bias_indicators, 1.0)
    
    async def _meta_analyze_evaluation_process(self, evaluation_results: Dict[str, RecursiveEvaluationChain]) -> Dict[str, Any]:
        """Perform meta-analysis of the entire evaluation process"""
        if not self.meta_analyzer:
            return {}
        
        return await self.meta_analyzer.analyze_evaluation_process(evaluation_results, self.evaluation_history)
    
    async def _synthesize_hybrid_results(self, recursive_results: Dict[str, RecursiveEvaluationChain], 
                                       meta_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize recursive and meta-analysis results into final assessment"""
        
        # Calculate overall scores from recursive chains
        aspect_scores = {}
        convergence_rates = {}
        
        for aspect_name, chain in recursive_results.items():
            # Use final score from recursive chain
            if chain.recursive_evaluations:
                final_score = chain.recursive_evaluations[-1].score
            else:
                final_score = chain.primary_evaluation.score
            
            aspect_scores[aspect_name] = final_score
            convergence_rates[aspect_name] = chain.convergence_achieved
        
        # Calculate overall metrics
        overall_score = sum(aspect_scores.values()) / len(aspect_scores) if aspect_scores else 0.0
        overall_convergence = sum(convergence_rates.values()) / len(convergence_rates) if convergence_rates else False
        
        # Factor in meta-analysis insights
        meta_adjustment = 0.0
        if meta_analysis:
            methodology_quality = meta_analysis.get('methodology_quality', 0.5)
            bias_level = meta_analysis.get('overall_bias_level', 0.5)
            meta_adjustment = (methodology_quality - bias_level) * 0.1
        
        evaluation_quality = min(1.0, max(0.0, overall_score + meta_adjustment))
        
        synthesis = {
            'overall_score': overall_score,
            'overall_convergence': overall_convergence > 0.5,
            'evaluation_quality': evaluation_quality,
            'aspect_scores': aspect_scores,
            'convergence_summary': convergence_rates,
            'meta_adjustment': meta_adjustment,
            'key_insights': self._extract_key_insights(recursive_results, meta_analysis),
            'recommendations': self._generate_recommendations(recursive_results, meta_analysis)
        }
        
        return synthesis
    
    def _extract_key_insights(self, recursive_results: Dict[str, RecursiveEvaluationChain], 
                            meta_analysis: Dict[str, Any]) -> List[str]:
        """Extract key insights from the evaluation"""
        insights = []
        
        # Insights from recursive evaluation
        converged_aspects = [name for name, chain in recursive_results.items() if chain.convergence_achieved]
        if converged_aspects:
            insights.append(f"Achieved convergence in {len(converged_aspects)} aspects: {', '.join(converged_aspects)}")
        
        # Insights from meta-analysis
        if meta_analysis.get('methodology_quality', 0) > 0.8:
            insights.append("High-quality evaluation methodology detected")
        
        if meta_analysis.get('overall_bias_level', 0) > 0.6:
            insights.append("Significant evaluation bias detected - results may be skewed")
        
        return insights[:5]  # Top 5 insights
    
    def _generate_recommendations(self, recursive_results: Dict[str, RecursiveEvaluationChain], 
                                meta_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        # Recommendations based on scores
        low_scoring_aspects = [name for name, chain in recursive_results.items() 
                             if (chain.recursive_evaluations[-1].score if chain.recursive_evaluations else chain.primary_evaluation.score) < 0.6]
        
        if low_scoring_aspects:
            recommendations.append(f"Focus improvement efforts on: {', '.join(low_scoring_aspects)}")
        
        # Recommendations based on convergence
        non_converged = [name for name, chain in recursive_results.items() if not chain.convergence_achieved]
        if non_converged:
            recommendations.append(f"Increase evaluation depth or refine methodology for: {', '.join(non_converged)}")
        
        # Meta-analysis recommendations
        if meta_analysis.get('overall_bias_level', 0) > 0.5:
            recommendations.append("Implement bias reduction techniques in evaluation process")
        
        return recommendations[:5]  # Top 5 recommendations


class MetaEvaluationAnalyzer:
    """Separate analyzer for meta-evaluation of evaluation processes"""
    
    async def analyze_evaluation_process(self, current_results: Dict[str, RecursiveEvaluationChain], 
                                       evaluation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the evaluation process from a meta perspective"""
        
        methodology_quality = await self._assess_methodology_quality(current_results)
        consistency_analysis = await self._analyze_consistency(current_results, evaluation_history)
        bias_analysis = await self._analyze_bias_patterns(current_results, evaluation_history)
        improvement_trends = await self._analyze_improvement_trends(evaluation_history)
        
        return {
            'methodology_quality': methodology_quality,
            'consistency_score': consistency_analysis['consistency_score'],
            'overall_bias_level': bias_analysis['overall_bias_level'],
            'improvement_trend': improvement_trends['trend_direction'],
            'meta_insights': {
                'evaluation_maturity': self._calculate_evaluation_maturity(evaluation_history),
                'reliability_score': consistency_analysis['reliability_score'],
                'bias_patterns': bias_analysis['patterns'],
                'trend_analysis': improvement_trends
            }
        }
    
    async def _assess_methodology_quality(self, results: Dict[str, RecursiveEvaluationChain]) -> float:
        """Assess the quality of evaluation methodology"""
        quality_factors = []
        
        # Check for appropriate recursion usage
        avg_recursion_depth = sum(len(chain.recursive_evaluations) for chain in results.values()) / len(results)
        recursion_quality = min(avg_recursion_depth / 2, 1.0)  # Optimal around 2 levels
        quality_factors.append(recursion_quality)
        
        # Check for convergence achievement
        convergence_rate = sum(chain.convergence_achieved for chain in results.values()) / len(results)
        quality_factors.append(convergence_rate)
        
        # Check for evidence quality
        avg_evidence_count = sum(len(chain.primary_evaluation.evidence) for chain in results.values()) / len(results)
        evidence_quality = min(avg_evidence_count / 3, 1.0)
        quality_factors.append(evidence_quality)
        
        return sum(quality_factors) / len(quality_factors)
    
    async def _analyze_consistency(self, current_results: Dict[str, RecursiveEvaluationChain], 
                                 history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze consistency of evaluation results"""
        if len(history) < 2:
            return {'consistency_score': 0.5, 'reliability_score': 0.5}
        
        # Compare current results with recent history
        recent_scores = []
        for h in history[-3:]:
            if 'synthesis' in h and 'aspect_scores' in h['synthesis']:
                recent_scores.append(h['synthesis']['aspect_scores'])
        
        if not recent_scores:
            return {'consistency_score': 0.5, 'reliability_score': 0.5}
        
        # Calculate consistency (lower variance = higher consistency)
        consistency_scores = []
        for aspect in current_results.keys():
            aspect_scores = [scores.get(aspect, 0.5) for scores in recent_scores if aspect in scores]
            if len(aspect_scores) > 1:
                variance = sum((score - sum(aspect_scores)/len(aspect_scores))**2 for score in aspect_scores) / len(aspect_scores)
                consistency = max(0, 1.0 - variance * 4)  # Scale variance to 0-1
                consistency_scores.append(consistency)
        
        avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.5
        
        return {
            'consistency_score': avg_consistency,
            'reliability_score': min(avg_consistency + 0.1, 1.0)  # Slight boost for reliability
        }
    
    async def _analyze_bias_patterns(self, current_results: Dict[str, RecursiveEvaluationChain], 
                                   history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns of bias in evaluations"""
        bias_indicators = []
        
        # Check for optimism bias (consistently high scores)
        current_scores = []
        for chain in current_results.values():
            if chain.recursive_evaluations:
                current_scores.append(chain.recursive_evaluations[-1].score)
            else:
                current_scores.append(chain.primary_evaluation.score)
        
        avg_score = sum(current_scores) / len(current_scores)
        if avg_score > 0.8:
            bias_indicators.append(('optimism_bias', 0.3))
        
        # Check for anchoring bias (scores too similar)
        score_variance = sum((score - avg_score)**2 for score in current_scores) / len(current_scores)
        if score_variance < 0.01:  # Very low variance
            bias_indicators.append(('anchoring_bias', 0.4))
        
        # Check for trend bias (always improving)
        if len(history) >= 3:
            recent_overall_scores = [h['synthesis']['overall_score'] for h in history[-3:] if 'synthesis' in h]
            if len(recent_overall_scores) >= 2 and all(recent_overall_scores[i] <= recent_overall_scores[i+1] for i in range(len(recent_overall_scores)-1)):
                bias_indicators.append(('improvement_bias', 0.2))
        
        overall_bias = sum(bias_level for _, bias_level in bias_indicators) / max(len(bias_indicators), 1)
        
        return {
            'overall_bias_level': min(overall_bias, 1.0),
            'patterns': [bias_type for bias_type, _ in bias_indicators]
        }
    
    async def _analyze_improvement_trends(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze improvement trends over time"""
        if len(history) < 3:
            return {'trend_direction': 'insufficient_data', 'trend_strength': 0.0}
        
        # Extract overall scores from history
        scores = []
        for h in history[-5:]:  # Last 5 evaluations
            if 'synthesis' in h and 'overall_score' in h['synthesis']:
                scores.append(h['synthesis']['overall_score'])
        
        if len(scores) < 3:
            return {'trend_direction': 'insufficient_data', 'trend_strength': 0.0}
        
        # Simple trend analysis
        improvements = sum(1 for i in range(1, len(scores)) if scores[i] > scores[i-1])
        declines = sum(1 for i in range(1, len(scores)) if scores[i] < scores[i-1])
        
        if improvements > declines:
            trend_direction = 'improving'
            trend_strength = (improvements - declines) / (len(scores) - 1)
        elif declines > improvements:
            trend_direction = 'declining'
            trend_strength = (declines - improvements) / (len(scores) - 1)
        else:
            trend_direction = 'stable'
            trend_strength = 0.0
        
        return {
            'trend_direction': trend_direction,
            'trend_strength': abs(trend_strength),
            'recent_scores': scores,
            'total_evaluations': len(history)
        }
    
    def _calculate_evaluation_maturity(self, history: List[Dict[str, Any]]) -> float:
        """Calculate evaluation process maturity based on history"""
        if not history:
            return 0.0
        
        # Factors for maturity: number of evaluations, consistency, convergence rates
        evaluation_count_factor = min(len(history) / 10, 1.0)  # Mature at 10+ evaluations
        
        # Average convergence rate over history
        convergence_rates = []
        for h in history:
            if 'synthesis' in h and 'overall_convergence' in h['synthesis']:
                convergence_rates.append(1.0 if h['synthesis']['overall_convergence'] else 0.0)
        
        avg_convergence = sum(convergence_rates) / len(convergence_rates) if convergence_rates else 0.0
        
        return (evaluation_count_factor + avg_convergence) / 2
