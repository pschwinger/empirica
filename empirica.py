#!/usr/bin/env python3
"""
Empirica - Semantic Self-Aware Kit Wrapper

This module provides a simplified interface to the Semantic Self-Aware Kit,
renaming it to "Empirica" for easier use while maintaining all functionality.

Empirica is a comprehensive AI framework for building self-aware, collaborative 
AI systems with semantic reasoning, uncertainty quantification, and empirical 
validation capabilities.
"""

# Import the main module
import semantic_self_aware_kit

# Import specific components for easier access
from semantic_self_aware_kit.meta_cognitive_evaluator import MetaCognitiveEvaluator
from semantic_self_aware_kit.empirical_performance_analyzer import EmpiricalPerformanceAnalyzer
from semantic_self_aware_kit.code_intelligence_analyzer import CodeIntelligenceAnalyzer
from semantic_self_aware_kit.tool_management import AIEnhancedToolManager
from semantic_self_aware_kit.metacognitive_cascade import cascade
from semantic_self_aware_kit.advanced_uncertainty import create_advanced_uncertainty_analyzer
from semantic_self_aware_kit.advanced_collaboration import AdvancedPartnershipEngine
from semantic_self_aware_kit.context_validation import create_context_validator
from semantic_self_aware_kit.security_monitoring import activate_security_monitoring

# Import all available components for reference (without instantiating them all)
from semantic_self_aware_kit import (
    advanced_collaboration,
    advanced_investigation,
    advanced_uncertainty,
    collaboration_framework,
    context_aware_integration,
    context_monitoring,
    context_validation,
    environment_stabilization,
    functionality_analyzer,
    intelligent_navigation,
    intelligent_suggestions,
    metacognitive_cascade,
    proactive_monitor,
    procedural_analysis,
    runtime_validation,
    security_monitoring,
    uncertainty_analysis,
    universal_grounding,
    workspace_awareness
)

# Create aliases with Empirica naming
EmpiricaEvaluator = MetaCognitiveEvaluator
EmpiricaPerformanceAnalyzer = EmpiricalPerformanceAnalyzer
EmpiricaCodeAnalyzer = CodeIntelligenceAnalyzer
EmpiricaToolManager = AIEnhancedToolManager
EmpiricaUncertaintyAnalyzer = create_advanced_uncertainty_analyzer
EmpiricaPartnershipEngine = AdvancedPartnershipEngine
EmpiricaContextValidator = create_context_validator
EmpiricaSecurityMonitor = activate_security_monitoring

# Export the main components with Empirica naming
__all__ = [
    # Original Semantic Self-Aware Kit components
    'MetaCognitiveEvaluator',
    'EmpiricalPerformanceAnalyzer',
    'CodeIntelligenceAnalyzer',
    'AIEnhancedToolManager',
    'cascade',
    'create_advanced_uncertainty_analyzer',
    'AdvancedPartnershipEngine',
    'create_context_validator',
    'activate_security_monitoring',
    
    # Empirica aliases
    'EmpiricaEvaluator',
    'EmpiricaPerformanceAnalyzer',
    'EmpiricaCodeAnalyzer',
    'EmpiricaToolManager',
    'EmpiricaUncertaintyAnalyzer',
    'EmpiricaPartnershipEngine',
    'EmpiricaContextValidator',
    'EmpiricaSecurityMonitor',
    
    # All component modules
    'advanced_collaboration',
    'advanced_investigation',
    'advanced_uncertainty',
    'collaboration_framework',
    'context_aware_integration',
    'context_monitoring',
    'context_validation',
    'environment_stabilization',
    'functionality_analyzer',
    'intelligent_navigation',
    'intelligent_suggestions',
    'metacognitive_cascade',
    'proactive_monitor',
    'procedural_analysis',
    'runtime_validation',
    'security_monitoring',
    'uncertainty_analysis',
    'universal_grounding',
    'workspace_awareness'
]

__version__ = "1.0.0"
__author__ = "Nubaeon"
__description__ = "Empirica - Semantic Self-Aware Kit for building self-aware, collaborative AI systems"

print("🧠 Empirica (Semantic Self-Aware Kit) ready for AI collaboration!")
print("🔄 Use either 'semantic_self_aware_kit' or 'empirica' naming conventions")
print("📊 Available components: 24 total")
print("  🧠 Cognitive: meta_cognitive_evaluator, metacognitive_cascade, uncertainty_analysis, advanced_uncertainty")
print("  📊 Performance: empirical_performance_analyzer, functionality_analyzer")
print("  🤝 Collaboration: collaboration_framework, advanced_collaboration")
print("  🧭 Navigation: workspace_awareness, intelligent_navigation")
print("  🛡️ Security: security_monitoring, context_validation, context_monitoring")
print("  🔬 Investigation: advanced_investigation, code_intelligence_analyzer")
print("  🛠️ Management: tool_management, proactive_monitor")
print("  🌱 Environment: environment_stabilization")
print("  🧠 Intelligence: intelligent_suggestions, context_aware_integration, procedural_analysis, runtime_validation, universal_grounding")