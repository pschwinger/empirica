#!/usr/bin/env python3
"""
🎯 Advanced Uncertainty Engine - Enterprise Component
Multi-dimensional uncertainty assessment and investigation cascades
"""

from .advanced_uncertainty import (
    UncertaintyDimension,
    UncertaintyLevel,
    UncertaintyVector,
    UncertaintyAssessment,
    AdvancedUncertaintyAnalyzer
)

def create_advanced_uncertainty_analyzer() -> AdvancedUncertaintyAnalyzer:
    """
    Create an Advanced Uncertainty Analyzer instance
    
    Returns:
        AdvancedUncertaintyAnalyzer: Instance of the advanced uncertainty analyzer
    """
    return AdvancedUncertaintyAnalyzer()

# Export main classes and instances
__all__ = [
    'AdvancedUncertaintyAnalyzer',
    'UncertaintyVector',
    'UncertaintyAssessment',
    'UncertaintyDimension',
    'UncertaintyLevel',
    'create_advanced_uncertainty_analyzer'
]

__version__ = "1.0.0"
__component__ = "advanced_uncertainty"
__tier__ = "enterprise"
__purpose__ = "Multi-dimensional uncertainty assessment with investigation cascades"

print(f"🎯 Advanced Uncertainty Engine ready for enterprise uncertainty analysis!")