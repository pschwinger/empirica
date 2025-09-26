#!/usr/bin/env python3
"""
Programmatic Example of using the Semantic Self-Aware Kit
"""

import asyncio
from semantic_self_aware_kit import SemanticFramework

async def demonstrate_programmatic_usage():
    """
    Demonstrate programmatic usage of the Semantic Self-Aware Kit
    """
    print("🖥️ Programmatic Usage Example with Semantic Self-Aware Kit")
    print("=" * 55)
    
    # Initialize the complete framework
    print("\n1. Initializing Semantic Framework...")
    framework = SemanticFramework()
    await framework.startup()
    print("   ✅ Semantic Framework initialized")
    
    # Test self-awareness
    print("\n2. Testing self-awareness...")
    try:
        self_awareness_results = await framework.meta_cognitive.evaluate("self")
        print("   ✅ Self-awareness test completed")
        
        if isinstance(self_awareness_results, dict):
            quality_score = self_awareness_results.get('quality_score', 0.0)
            confidence_level = self_awareness_results.get('confidence_level', 'low')
        else:
            quality_score = getattr(self_awareness_results, 'quality_score', 0.0)
            confidence_level = getattr(self_awareness_results, 'confidence_level', 'low')
            
        print(f"   📊 Quality Score: {quality_score:.2f}")
        print(f"   🎯 Confidence Level: {confidence_level}")
        
    except Exception as e:
        print(f"   ⚠️  Error during self-awareness test: {e}")
    
    # Run performance benchmark
    print("\n3. Running performance benchmark...")
    try:
        benchmark_results = await framework.performance.benchmark("framework")
        print("   ✅ Performance benchmark completed")
        
        if isinstance(benchmark_results, dict):
            overall_score = benchmark_results.get('overall_score', 0.0)
            tests_executed = benchmark_results.get('tests_executed', 0)
        else:
            overall_score = getattr(benchmark_results, 'overall_score', 0.0)
            tests_executed = getattr(benchmark_results, 'tests_executed', 0)
            
        print(f"   📊 Overall Score: {overall_score:.2f}")
        print(f"   🎯 Tests Executed: {tests_executed}")
        
    except Exception as e:
        print(f"   ⚠️  Error during performance benchmark: {e}")
    
    # Analyze code
    print("\n4. Analyzing code...")
    try:
        analysis_results = framework.code_intelligence.analyze(".")
        print("   ✅ Code analysis completed")
        
        if isinstance(analysis_results, dict):
            metadata = analysis_results.get('metadata', {})
            synthesis = analysis_results.get('synthesis', {})
        else:
            metadata = getattr(analysis_results, 'metadata', {})
            synthesis = getattr(analysis_results, 'synthesis', {})
            
        total_artifacts = metadata.get('total_artifacts', 0)
        total_clusters = metadata.get('total_clusters', 0)
        
        print(f"   📊 Files Analyzed: {total_artifacts}")
        print(f"   🏗️  Code Clusters: {total_clusters}")
        
        recommendations = synthesis.get('key_recommendations', [])
        if recommendations:
            print("   💡 Key Recommendations:")
            for i, recommendation in enumerate(recommendations[:3], 1):  # Show top 3
                print(f"      {i}. {recommendation}")
        else:
            print("   📋 No specific recommendations at this time")
            
    except Exception as e:
        print(f"   ⚠️  Error during code analysis: {e}")
    
    # Enable collaboration
    print("\n5. Enabling collaboration...")
    try:
        partnership = await framework.collaboration.establish_partnership("example_partner")
        print("   ✅ Collaboration partnership established")
        
        if isinstance(partnership, dict):
            partnership_id = partnership.get('partnership_id', 'N/A')
            trust_level = partnership.get('trust_level', 0.0)
        else:
            partnership_id = getattr(partnership, 'partnership_id', 'N/A')
            trust_level = getattr(partnership, 'trust_level', 0.0)
            
        print(f"   🆔 Partnership ID: {partnership_id}")
        print(f"   🤝 Trust Level: {trust_level:.2f}")
        
    except Exception as e:
        print(f"   ⚠️  Error establishing collaboration partnership: {e}")
    
    # Analyze uncertainty
    print("\n6. Analyzing uncertainty...")
    try:
        uncertainty_context = {
            "decision": "Should we refactor this module?",
            "project_complexity": "high",
            "team_experience": "intermediate",
            "time_constraints": "moderate"
        }
        
        uncertainty_results = await framework.uncertainty.analyze(uncertainty_context)
        print("   ✅ Uncertainty analysis completed")
        
        if isinstance(uncertainty_results, dict):
            uncertainty_score = uncertainty_results.get('uncertainty_score', 0.0)
            confidence_level = uncertainty_results.get('confidence_level', 'low')
            dominant_type = uncertainty_results.get('dominant_uncertainty_type', 'unknown')
        else:
            uncertainty_score = getattr(uncertainty_results, 'uncertainty_score', 0.0)
            confidence_level = getattr(uncertainty_results, 'confidence_level', 'low')
            dominant_type = getattr(uncertainty_results, 'dominant_uncertainty_type', 'unknown')
            
        print(f"   📊 Uncertainty Score: {uncertainty_score:.2f}")
        print(f"   🎯 Confidence Level: {confidence_level}")
        print(f"   🤔 Dominant Uncertainty Type: {dominant_type}")
        
    except Exception as e:
        print(f"   ⚠️  Error during uncertainty analysis: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("This programmatic example demonstrates the core functionality of the Semantic")
    print("Self-Aware Kit through direct API access. The framework provides:")
    print("")
    print("🧠 Meta-Cognitive Evaluation for self-awareness assessment")
    print("📊 Performance Benchmarking for empirical validation")
    print("🔍 Code Intelligence Analysis for deep programmatic understanding")
    print("🤝 Collaboration Framework for AI-to-AI coordination")
    print("🤔 Uncertainty Analysis for multi-dimensional uncertainty quantification")
    print("")
    print("All components are accessible through the unified SemanticFramework interface.")

async def main():
    await demonstrate_programmatic_usage()
    print("\n✅ Programmatic usage example completed!")

if __name__ == "__main__":
    asyncio.run(main())