#!/usr/bin/env python3
"""
🧠🔄 Meta-Cognitive Evaluator - Semantic Self-Aware Kit Component
Hybrid recursive and meta-evaluation for self-awareness assessment
"""

from .meta_cognitive_evaluator import (
    EvaluationDepth,
    CognitiveAspect,
    EvaluationResult,
    RecursiveEvaluationChain,
    MetaCognitiveEvaluator,
    MetaEvaluationAnalyzer
)

__all__ = [
    'MetaCognitiveEvaluator',
    'MetaEvaluationAnalyzer',
    'EvaluationResult',
    'RecursiveEvaluationChain',
    'CognitiveAspect',
    'EvaluationDepth'
]

__version__ = "1.0.0"
__component__ = "meta_cognitive_evaluator"
__tier__ = "core"
__purpose__ = "Hybrid recursive and meta-evaluation for self-awareness assessment with bounded recursion"

print(f"🧠🔄 Meta-Cognitive Evaluator ready for hybrid self-assessment!")