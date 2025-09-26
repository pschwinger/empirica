#!/usr/bin/env python3
"""
🔍 Functionality Analyzer Component
Self-contained code analysis and semantic understanding for AI systems
"""

from .functionality_analyzer import (
    CodeAnalyzer,
    FunctionSignature,
    CodeComponent,
    CodeElementType,
    SemanticAnalyzer,
    SemanticPattern,
    SemanticPatternType
)

# Create default instances for immediate use
default_code_analyzer = CodeAnalyzer()
default_semantic_analyzer = SemanticAnalyzer()

__all__ = [
    'CodeAnalyzer',
    'FunctionSignature',
    'CodeComponent',
    'CodeElementType',
    'SemanticAnalyzer',
    'SemanticPattern',
    'SemanticPatternType',
    'default_code_analyzer',
    'default_semantic_analyzer'
]

__version__ = "1.0.0"
__component__ = "functionality_analyzer"
__purpose__ = "Basic code analysis and semantic understanding for AI self-awareness"

print(f"🔍 Functionality Analyzer component ready for AI collaboration!")