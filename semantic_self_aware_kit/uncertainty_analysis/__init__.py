#!/usr/bin/env python3
"""
🤔 Uncertainty Analysis Module
Advanced uncertainty quantification and investigation for AI systems
"""

from .uncertainty_analysis import (
    UncertaintyType,
    InvestigationDepth,
    UncertaintyVector,
    InvestigationResult,
    MultiDimensionalUncertaintyAnalyzer
)

def create_uncertainty_analyzer() -> MultiDimensionalUncertaintyAnalyzer:
    """
    Create a Multi-Dimensional Uncertainty Analyzer instance
    
    Returns:
        MultiDimensionalUncertaintyAnalyzer: Instance of the uncertainty analyzer
    """
    return MultiDimensionalUncertaintyAnalyzer()

def activate_uncertainty_analysis() -> MultiDimensionalUncertaintyAnalyzer:
    """
    Activate multi-dimensional uncertainty analysis capabilities
    
    Returns:
        MultiDimensionalUncertaintyAnalyzer: Active multi-dimensional uncertainty analyzer
    """
    print("🤔 ACTIVATING MULTI-DIMENSIONAL UNCERTAINTY ANALYSIS")
    print("=" * 50)
    print("✅ Epistemic uncertainty assessment")
    print("✅ Aleatoric uncertainty quantification")
    print("✅ Contextual uncertainty analysis")
    print("✅ Temporal uncertainty evaluation")
    print("✅ Semantic uncertainty resolution")
    print("✅ Causal uncertainty investigation")
    
    return create_uncertainty_analyzer()

__all__ = [
    'UncertaintyType',
    'InvestigationDepth',
    'UncertaintyVector',
    'InvestigationResult',
    'MultiDimensionalUncertaintyAnalyzer',
    'create_uncertainty_analyzer',
    'activate_uncertainty_analysis'
]

__version__ = "1.0.0"
__component__ = "uncertainty_analysis"
__purpose__ = "Advanced uncertainty quantification and investigation for AI systems"

print(f"🤔 Multi-dimensional uncertainty analysis ready for AI collaboration!")