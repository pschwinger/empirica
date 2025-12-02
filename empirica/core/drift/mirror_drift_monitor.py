#!/usr/bin/env python3
"""
Mirror-Based Drift Monitor

Detects epistemic drift by comparing current state to historical baselines
stored in Git checkpoints. Implements the Mirror Principle: past-self
validates present-self through temporal comparison.

No heuristics, no external LLMs, no keyword matching.
Pure temporal self-validation.
"""

from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DriftReport:
    """Result of drift detection"""
    drift_detected: bool
    severity: str  # 'none' | 'low' | 'medium' | 'high' | 'critical'
    recommended_action: str  # 'continue' | 'monitor_closely' | 'investigate' | 'stop_and_reassess'
    drifted_vectors: List[Dict[str, Any]]
    baseline_timestamp: Optional[float] = None
    checkpoints_analyzed: int = 0
    reason: Optional[str] = None


class MirrorDriftMonitor:
    """
    Drift detection using temporal self-validation
    
    Compares current epistemic state to historical baselines from
    Git checkpoints. Detects unexpected drops in epistemic vectors
    that indicate memory corruption, context loss, or other drift.
    
    Philosophy:
    - Increases are expected (learning)
    - Decreases without investigation are drift (corruption)
    - Compare to recent history, not single point
    - No heuristics, just temporal comparison
    """
    
    def __init__(
        self,
        drift_threshold: float = 0.2,
        lookback_window: int = 5,
        enable_logging: bool = True
    ):
        """
        Initialize drift monitor
        
        Args:
            drift_threshold: Minimum drop to flag as drift (default: 0.2)
            lookback_window: Number of recent checkpoints to use for baseline (default: 5)
            enable_logging: Log drift warnings (default: True)
        """
        self.drift_threshold = drift_threshold
        self.lookback_window = lookback_window
        self.enable_logging = enable_logging
    
    def detect_drift(
        self,
        current_assessment: Any,  # EpistemicAssessmentSchema
        session_id: str
    ) -> DriftReport:
        """
        Detect drift by comparing current state to recent history
        
        Args:
            current_assessment: Current epistemic assessment
            session_id: Session UUID
        
        Returns:
            DriftReport with detection results
        """
        # Load recent checkpoints from Git
        history = self._load_recent_checkpoints(session_id, self.lookback_window)
        
        if not history:
            return DriftReport(
                drift_detected=False,
                severity='none',
                recommended_action='continue',
                drifted_vectors=[],
                reason='no_baseline_available'
            )
        
        # Calculate baseline from history
        baseline = self._calculate_baseline(history)
        
        # Compare current to baseline
        drift_report = self._compare_states(baseline, current_assessment)
        
        # Log if enabled
        if self.enable_logging and drift_report.drift_detected:
            self._log_drift(drift_report)
        
        return drift_report
    
    def _load_recent_checkpoints(self, session_id: str, count: int) -> List[Dict]:
        """
        Load recent checkpoints from Git notes
        
        Args:
            session_id: Session UUID
            count: Number of recent checkpoints to load
        
        Returns:
            List of checkpoint dicts with vectors
        """
        try:
            from empirica.core.canonical.empirica_git.checkpoint_manager import CheckpointManager
            
            manager = CheckpointManager()
            checkpoints = manager.load_recent_checkpoints(
                session_id=session_id,
                count=count
            )
            
            return checkpoints
        except Exception as e:
            logger.warning(f"Could not load checkpoints: {e}")
            return []
    
    def _calculate_baseline(self, history: List[Dict]) -> Dict[str, float]:
        """
        Calculate baseline by averaging recent checkpoints
        
        Args:
            history: List of checkpoint dicts
        
        Returns:
            Dict mapping vector names to baseline values
        """
        baseline = {}
        
        # All vectors we track
        vectors = [
            'know', 'do', 'context', 'clarity', 'coherence',
            'signal', 'density', 'uncertainty', 'engagement',
            'state', 'change', 'completion', 'impact'
        ]
        
        for vector in vectors:
            # Collect values from history
            values = []
            for checkpoint in history:
                if 'vectors' in checkpoint and vector in checkpoint['vectors']:
                    values.append(checkpoint['vectors'][vector])
            
            # Average if we have values, else default 0.5
            if values:
                baseline[vector] = sum(values) / len(values)
            else:
                baseline[vector] = 0.5  # Neutral default
        
        return baseline
    
    def _compare_states(
        self,
        baseline: Dict[str, float],
        current: Any  # EpistemicAssessmentSchema
    ) -> DriftReport:
        """
        Compare current state to baseline, detect drift
        
        Args:
            baseline: Baseline vector values
            current: Current epistemic assessment
        
        Returns:
            DriftReport with detection results
        """
        # Extract current vector values
        current_vectors = self._extract_vectors(current)
        
        # Check each vector for unexpected drops
        drifted_vectors = []
        max_drift = 0.0
        
        for vector_name, current_value in current_vectors.items():
            baseline_value = baseline.get(vector_name, 0.5)
            drift = baseline_value - current_value
            
            # Only flag DROPS (increases are expected from learning)
            # Exception: uncertainty can increase (that's drift too)
            if vector_name == 'uncertainty':
                # For uncertainty, increase is drift
                drift = current_value - baseline_value
            
            if drift > self.drift_threshold:
                drifted_vectors.append({
                    'vector': vector_name,
                    'baseline': baseline_value,
                    'current': current_value,
                    'drift': drift,
                    'severity': self._classify_drift_severity(drift)
                })
                
                max_drift = max(max_drift, drift)
        
        # No drift detected
        if not drifted_vectors:
            return DriftReport(
                drift_detected=False,
                severity='none',
                recommended_action='continue',
                drifted_vectors=[],
                checkpoints_analyzed=len(baseline)
            )
        
        # Drift detected
        overall_severity = self._classify_overall_severity(max_drift, len(drifted_vectors))
        recommended_action = self._recommend_action(overall_severity)
        
        return DriftReport(
            drift_detected=True,
            severity=overall_severity,
            recommended_action=recommended_action,
            drifted_vectors=drifted_vectors,
            checkpoints_analyzed=len(baseline)
        )
    
    def _extract_vectors(self, assessment: Any) -> Dict[str, float]:
        """
        Extract vector scores from assessment
        
        Args:
            assessment: EpistemicAssessmentSchema
        
        Returns:
            Dict mapping vector names to scores
        """
        vectors = {}
        
        # Extract from assessment
        vector_names = [
            'engagement', 'know', 'do', 'context', 'clarity',
            'coherence', 'signal', 'density', 'state', 'change',
            'completion', 'impact', 'uncertainty'
        ]
        
        for name in vector_names:
            if hasattr(assessment, name):
                vector_state = getattr(assessment, name)
                if hasattr(vector_state, 'score'):
                    score = vector_state.score
                    
                    # Density is inverted (high density = bad)
                    if name == 'density':
                        score = 1.0 - score
                    
                    vectors[name] = score
        
        return vectors
    
    def _classify_drift_severity(self, drift: float) -> str:
        """Classify single vector drift severity"""
        if drift > 0.5:
            return 'critical'
        elif drift > 0.3:
            return 'high'
        elif drift > 0.2:
            return 'medium'
        else:
            return 'low'
    
    def _classify_overall_severity(self, max_drift: float, vector_count: int) -> str:
        """Classify overall drift severity"""
        if max_drift > 0.5 or vector_count >= 4:
            return 'critical'
        elif max_drift > 0.3 or vector_count >= 3:
            return 'high'
        elif max_drift > 0.2 or vector_count >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _recommend_action(self, severity: str) -> str:
        """Recommend action based on drift severity"""
        if severity == 'critical':
            return 'stop_and_reassess'
        elif severity == 'high':
            return 'investigate'
        elif severity == 'medium':
            return 'monitor_closely'
        else:
            return 'continue'
    
    def _log_drift(self, report: DriftReport):
        """Log drift warning"""
        logger.warning(
            f"⚠️ Epistemic Drift Detected: {report.severity.upper()}"
        )
        logger.warning(
            f"   Drifted vectors: {len(report.drifted_vectors)}"
        )
        
        for vec in report.drifted_vectors:
            logger.warning(
                f"   • {vec['vector']}: {vec['baseline']:.2f} → {vec['current']:.2f} "
                f"(drift: {vec['drift']:.2f}, severity: {vec['severity']})"
            )
        
        logger.warning(
            f"   Recommended action: {report.recommended_action.upper()}"
        )
