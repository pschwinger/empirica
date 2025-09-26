from typing import Dict, List, Any, Optional

"""
Simplified Metacognitive Cascade for Developers and Researchers
THINK → UNCERTAINTY → CHECK → INVESTIGATE → ACT
"""

from .metacognitive_cascade import (
    UncertaintyVector,
    CascadeResult,
    SimpleCascade
)

# Global instance for easy import
cascade = SimpleCascade()

# Convenience function
def think_uncertainty_check_investigate_act(task: str, context: Dict[str, Any] = None) -> CascadeResult:
    """Convenience function for full cascade"""
    return cascade.run_full_cascade(task, context)

__all__ = [
    'UncertaintyVector',
    'CascadeResult',
    'SimpleCascade',
    'cascade', # Expose the global instance
    'think_uncertainty_check_investigate_act' # Expose the convenience function
]