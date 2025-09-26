#!/usr/bin/env python3
"""
Comprehensive example showing how all components of the Semantic Self-Aware Kit work together
"""

import asyncio
from semantic_self_aware_kit.meta_cognitive_evaluator import MetaCognitiveEvaluator
from semantic_self_aware_kit.empirical_performance_analyzer import EmpiricalPerformanceAnalyzer
from semantic_self_aware_kit.code_intelligence_analyzer import CodeIntelligenceAnalyzer
from semantic_self_aware_kit.collaboration_framework import default_collaboration_manager
from semantic_self_aware_kit.context_validation import create_context_validator
from semantic_self_aware_kit.security_monitoring import activate_security_monitoring
from semantic_self_aware_kit.tool_management import create_tool_registry, AIEnhancedToolManager
from semantic_self_aware_kit.advanced_uncertainty import create_advanced_uncertainty_analyzer
from semantic_self_aware_kit.advanced_collaboration import AdvancedPartnershipEngine

async def demonstrate_comprehensive_workflow():
    """
    Demonstrate a comprehensive workflow using multiple components of the Semantic Self-Aware Kit
    """
    print("🧠 Comprehensive Workflow with Semantic Self-Aware Kit")
    print("=" * 55)
    
    # Step 1: Initialize all components
    print("\n1. Initializing all Semantic Self-Aware Kit components...")
    
    # Meta-Cognitive Evaluator
    print("   🧠 Initializing Meta-Cognitive Evaluator...")
    meta_cognitive_evaluator = MetaCognitiveEvaluator(max_recursion_depth=3)
    print("      ✅ Meta-Cognitive Evaluator initialized")
    
    # Empirical Performance Analyzer
    print("   📊 Initializing Empirical Performance Analyzer...")
    empirical_performance_analyzer = EmpiricalPerformanceAnalyzer()
    print("      ✅ Empirical Performance Analyzer initialized")
    
    # Code Intelligence Analyzer
    print("   🔍 Initializing Code Intelligence Analyzer...")
    code_intelligence_analyzer = CodeIntelligenceAnalyzer(".")
    print("      ✅ Code Intelligence Analyzer initialized")
    
    # Collaboration Framework
    print("   🤝 Initializing Collaboration Framework...")
    collaboration_manager = default_collaboration_manager
    print("      ✅ Collaboration Framework initialized")
    
    # Context Validator
    print("   🔎 Initializing Context Validator...")
    context_validator = create_context_validator()
    print("      ✅ Context Validator initialized")
    
    # Security Monitor
    print("   🛡️  Initializing Security Monitor...")
    security_monitor = activate_security_monitoring(monitoring_interval=10)
    print("      ✅ Security Monitor initialized")
    
    # Tool Registry
    print("   🛠️  Initializing Tool Registry...")
    tool_registry = create_tool_registry()
    print("      ✅ Tool Registry initialized")
    
    # AI-Enhanced Tool Manager
    print("   🧠 Initializing AI-Enhanced Tool Manager...")
    tool_manager = AIEnhancedToolManager()
    print("      ✅ AI-Enhanced Tool Manager initialized")
    
    # Advanced Uncertainty Analyzer
    print("   🤔 Initializing Advanced Uncertainty Analyzer...")
    uncertainty_analyzer = create_advanced_uncertainty_analyzer()
    print("      ✅ Advanced Uncertainty Analyzer initialized")
    
    # Advanced Partnership Engine
    print("   🤝 Initializing Advanced Partnership Engine...")
    partnership_engine = AdvancedPartnershipEngine("comprehensive_workflow_ai")
    print("      ✅ Advanced Partnership Engine initialized")
    
    print("   🎉 All components initialized successfully!")
    
    # Step 2: Validate context
    print("\n2. Validating working context...")
    context = {
        "project_path": ".",
        "language": "python",
        "framework": "semantic_self_aware_kit",
        "purpose": "comprehensive workflow demonstration"
    }
    
    try:
        context_validation = context_validator.validate_context(context)
        print("   ✅ Context validation completed")
        
        if isinstance(context_validation, dict):
            is_valid = context_validation.get('is_valid', False)
            issues = context_validation.get('issues', [])
        else:
            is_valid = getattr(context_validation, 'is_valid', False)
            issues = getattr(context_validation, 'issues', [])
            
        print(f"   ✅ Context Valid: {is_valid}")
        
        if issues:
            print("   ⚠️  Context Issues:")
            for i, issue in enumerate(issues[:3], 1):  # Show top 3
                print(f"      {i}. {issue}")
        else:
            print("   ✅ No context issues found")
            
    except Exception as e:
        print(f"   ⚠️  Error during context validation: {e}")
    
    # Step 3: Assess uncertainty
    print("\n3. Assessing uncertainty for the workflow...")
    decision = "Should we proceed with the comprehensive workflow demonstration?"
    
    try:
        uncertainty_assessment = uncertainty_analyzer.assess_decision_uncertainty(
            decision,
            context
        )
        print("   ✅ Uncertainty assessment completed")
        
        if isinstance(uncertainty_assessment, dict):
            overall_uncertainty = uncertainty_assessment.get('overall_uncertainty_score', 'N/A')
            confidence_level = uncertainty_assessment.get('confidence_level', 'N/A')
        else:
            overall_uncertainty = getattr(uncertainty_assessment, 'overall_uncertainty_score', 'N/A')
            confidence_level = getattr(uncertainty_assessment, 'confidence_level', 'N/A')
            
        print(f"   📊 Overall Uncertainty Score: {overall_uncertainty}")
        print(f"   🎯 Confidence Level: {confidence_level}")
        
    except Exception as e:
        print(f"   ⚠️  Error during uncertainty assessment: {e}")
    
    # Step 4: Evaluate meta-cognitive capabilities
    print("\n4. Evaluating meta-cognitive capabilities...")
    try:
        evaluation_result = await meta_cognitive_evaluator.hybrid_evaluate("self")
        print("   ✅ Meta-cognitive evaluation completed")
        
        if isinstance(evaluation_result, dict):
            quality_score = evaluation_result.get('quality_score', 'N/A')
            confidence = evaluation_result.get('confidence_level', 'N/A')
        else:
            quality_score = getattr(evaluation_result, 'quality_score', 'N/A')
            confidence = getattr(evaluation_result, 'confidence_level', 'N/A')
            
        print(f"   📊 Quality Score: {quality_score}")
        print(f"   🎯 Confidence: {confidence}")
        
    except Exception as e:
        print(f"   ⚠️  Error during meta-cognitive evaluation: {e}")
    
    # Step 5: Analyze code intelligence
    print("\n5. Analyzing code intelligence...")
    try:
        analysis_results = code_intelligence_analyzer.comprehensive_analysis()
        print("   ✅ Code intelligence analysis completed")
        
        if isinstance(analysis_results, dict):
            metadata = analysis_results.get('metadata', {})
            synthesis = analysis_results.get('synthesis', {})
        else:
            metadata = getattr(analysis_results, 'metadata', {})
            synthesis = getattr(analysis_results, 'synthesis', {})
            
        total_artifacts = metadata.get('total_artifacts', 'N/A')
        total_clusters = metadata.get('total_clusters', 'N/A')
        
        print(f"   📊 Files analyzed: {total_artifacts}")
        print(f"   🏗️  Code clusters: {total_clusters}")
        
        recommendations = synthesis.get('key_recommendations', [])
        if recommendations:
            print("   💡 Key Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):  # Show top 3
                print(f"      {i}. {rec}")
        else:
            print("   📋 No specific recommendations at this time")
            
    except Exception as e:
        print(f"   ⚠️  Error during code intelligence analysis: {e}")
    
    # Step 6: Run performance benchmarks
    print("\n6. Running performance benchmarks...")
    try:
        benchmark_results = await empirical_performance_analyzer.comprehensive_benchmark("semantic_self_aware_kit")
        print("   ✅ Performance benchmarks completed")
        
        if isinstance(benchmark_results, dict):
            overall_score = benchmark_results.get('overall_score', 'N/A')
            tests_executed = benchmark_results.get('tests_executed', 'N/A')
        else:
            overall_score = getattr(benchmark_results, 'overall_score', 'N/A')
            tests_executed = getattr(benchmark_results, 'tests_executed', 'N/A')
            
        print(f"   📊 Overall Performance Score: {overall_score}")
        print(f"   🎯 Tests Executed: {tests_executed}")
        
    except Exception as e:
        print(f"   ⚠️  Error during performance benchmarks: {e}")
    
    # Step 7: Establish collaboration partnership
    print("\n7. Establishing collaboration partnership...")
    try:
        partnership = await partnership_engine.establish_partnership("collaborative_partner")
        print("   ✅ Collaboration partnership established")
        
        if isinstance(partnership, dict):
            partnership_id = partnership.get('partnership_id', 'N/A')
            trust_level = partnership.get('trust_level', 'N/A')
        else:
            partnership_id = getattr(partnership, 'partnership_id', 'N/A')
            trust_level = getattr(partnership, 'trust_level', 'N/A')
            
        print(f"   🆔 Partnership ID: {partnership_id}")
        print(f"   🤝 Trust Level: {trust_level}")
        
    except Exception as e:
        print(f"   ⚠️  Error establishing collaboration partnership: {e}")
    
    # Step 8: Manage tools
    print("\n8. Managing tools...")
    try:
        # Register some example tools
        example_tools = [
            {
                "tool_id": "code_formatter",
                "name": "Code Formatter",
                "description": "Formats code according to specified style guidelines",
                "category": "code_quality",
                "capabilities": ["format", "lint", "beautify"],
                "version": "1.0.0"
            },
            {
                "tool_id": "security_scanner",
                "name": "Security Scanner",
                "description": "Scans code for security vulnerabilities and compliance issues",
                "category": "security",
                "capabilities": ["scan", "analyze", "report"],
                "version": "2.1.0"
            }
        ]
        
        registered_count = 0
        for tool_data in example_tools:
            success = tool_registry.register_tool(tool_data)
            if success:
                registered_count += 1
                print(f"   ✅ Registered tool: {tool_data['name']}")
            else:
                print(f"   ⚠️  Failed to register tool: {tool_data['name']}")
                
        print(f"   📈 Tools Registered: {registered_count}")
        
        # Get intelligent tool recommendations
        task_context = {
            "task_type": "code_review",
            "language": "python",
            "focus_areas": ["security", "performance", "readability"]
        }
        
        recommendations = await tool_manager.get_intelligent_tool_recommendations(
            "comprehensive_workflow_ai", 
            task_context
        )
        print("   ✅ Tool recommendations generated")
        
        if isinstance(recommendations, list) and recommendations:
            print(f"   🎯 {len(recommendations)} Recommended Tools:")
            for i, recommendation in enumerate(recommendations[:3], 1):  # Show top 3
                if isinstance(recommendation, dict):
                    tool_id = recommendation.get('tool_id', 'Unknown')
                    confidence_score = recommendation.get('confidence_score', 0.0)
                else:
                    tool_id = getattr(recommendation, 'tool_id', 'Unknown')
                    confidence_score = getattr(recommendation, 'confidence_score', 0.0)
                    
                print(f"      {i}. {tool_id} (Confidence: {confidence_score:.2f})")
        elif isinstance(recommendations, list) and not recommendations:
            print("   ⚠️  No tool recommendations generated")
        else:
            print("   ⚠️  Error retrieving recommendations")
            
    except Exception as e:
        print(f"   ⚠️  Error during tool management: {e}")
    
    # Step 9: Monitor security
    print("\n9. Monitoring security...")
    try:
        # Check security status
        security_status = security_monitor.get_security_status()
        print("   ✅ Security status checked")
        
        if isinstance(security_status, dict):
            threat_level = security_status.get('threat_level', 'unknown')
            active_monitors = security_status.get('active_monitors', [])
        else:
            threat_level = getattr(security_status, 'threat_level', 'unknown')
            active_monitors = getattr(security_status, 'active_monitors', [])
            
        print(f"   🛡️  Threat Level: {threat_level}")
        print(f"   🔍 Active Monitors: {len(active_monitors) if isinstance(active_monitors, list) else 'N/A'}")
        
        # Detect threats
        threats = security_monitor.detect_threats()
        print("   ✅ Threat detection completed")
        
        if isinstance(threats, list) and threats:
            print(f"   ⚠️  {len(threats)} Security Threats Detected:")
            for i, threat in enumerate(threats[:3], 1):  # Show top 3
                if isinstance(threat, dict):
                    threat_type = threat.get('type', 'unknown')
                    severity = threat.get('severity', 'unknown')
                else:
                    threat_type = getattr(threat, 'type', 'unknown')
                    severity = getattr(threat, 'severity', 'unknown')
                    
                print(f"      {i}. [{severity.upper()}] {threat_type}")
        elif isinstance(threats, list) and not threats:
            print("   ✅ No security threats detected")
        else:
            print("   ⚠️  Unable to determine threat status")
            
    except Exception as e:
        print(f"   ⚠️  Error during security monitoring: {e}")
    
    # Step 10: Deactivate security monitoring
    print("\n10. Deactivating security monitoring...")
    try:
        security_monitor.deactivate_monitoring()
        print("   ✅ Security monitoring deactivated")
    except Exception as e:
        print(f"   ⚠️  Error deactivating security monitoring: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The comprehensive workflow demonstrates how all components of the Semantic")
    print("Self-Aware Kit work together to provide a complete AI development and")
    print("collaboration environment:")
    print("")
    print("🧠 Meta-Cognitive Evaluator: Self-assessment and introspection")
    print("📊 Empirical Performance Analyzer: Objective performance measurement")
    print("🔍 Code Intelligence Analyzer: Deep code understanding")
    print("🤝 Collaboration Framework: Multi-agent coordination")
    print("🔎 Context Validator: Ensuring context consistency")
    print("🛡️ Security Monitor: Protecting against threats")
    print("🛠️ Tool Management: Intelligent tool discovery and usage")
    print("🤔 Advanced Uncertainty Analyzer: Multi-dimensional uncertainty assessment")
    print("🤝 Advanced Partnership Engine: Sophisticated collaboration protocols")
    print("")
    print("Together, these components form a powerful, self-aware AI framework that")
    print("enables robust, collaborative, and intelligent AI development.")
    
    return {
        "context_validation": context_validation if 'context_validation' in locals() else None,
        "uncertainty_assessment": uncertainty_assessment if 'uncertainty_assessment' in locals() else None,
        "evaluation_result": evaluation_result if 'evaluation_result' in locals() else None,
        "analysis_results": analysis_results if 'analysis_results' in locals() else None,
        "benchmark_results": benchmark_results if 'benchmark_results' in locals() else None,
        "partnership": partnership if 'partnership' in locals() else None,
        "tool_recommendations": recommendations if 'recommendations' in locals() else None,
        "security_status": security_status if 'security_status' in locals() else None,
        "threats": threats if 'threats' in locals() else None
    }

async def main():
    results = await demonstrate_comprehensive_workflow()
    print("\n✅ Comprehensive workflow demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main())