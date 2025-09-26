#!/usr/bin/env python3
"""
Code Analysis Example with the Semantic Self-Aware Kit
"""

import asyncio
from semantic_self_aware_kit.code_intelligence_analyzer import CodeIntelligenceAnalyzer

async def demonstrate_code_analysis():
    """
    Demonstrate code analysis capabilities
    """
    print("🔍 Code Analysis with Semantic Self-Aware Kit")
    print("=" * 45)
    
    # Initialize the code intelligence analyzer
    print("\n1. Initializing Code Intelligence Analyzer...")
    code_analyzer = CodeIntelligenceAnalyzer(".")
    print("   ✅ Code Intelligence Analyzer initialized")
    
    # Perform comprehensive analysis
    print("\n2. Performing comprehensive code analysis...")
    try:
        analysis_results = code_analyzer.comprehensive_analysis()
        print("   ✅ Comprehensive code analysis completed")
        
        # Display analysis results
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
        
        # Show key insights
        insights = synthesis.get('key_insights', [])
        if isinstance(insights, list) and insights:
            print("   💡 Key Insights:")
            for i, insight in enumerate(insights[:5], 1):  # Show top 5
                print(f"      {i}. {insight}")
        elif isinstance(insights, list) and not insights:
            print("   💡 No specific insights at this time")
        else:
            print("   💡 Unable to determine key insights")
            
        # Show recommendations
        recommendations = synthesis.get('key_recommendations', [])
        if isinstance(recommendations, list) and recommendations:
            print("   📋 Key Recommendations:")
            for i, recommendation in enumerate(recommendations[:5], 1):  # Show top 5
                print(f"      {i}. {recommendation}")
        elif isinstance(recommendations, list) and not recommendations:
            print("   📋 No specific recommendations at this time")
        else:
            print("   📋 Unable to determine recommendations")
            
    except Exception as e:
        print(f"   ⚠️  Error during comprehensive code analysis: {e}")
    
    # Perform archaeological excavation
    print("\n3. Performing archaeological excavation...")
    try:
        archaeological_report = code_analyzer.excavate_project()
        print("   ✅ Archaeological excavation completed")
        
        # Display archaeological results
        if isinstance(archaeological_report, dict):
            artifacts = archaeological_report.get('artifacts', [])
            clusters = archaeological_report.get('clusters', {})
            dependency_graph = archaeological_report.get('dependency_graph', {})
        else:
            artifacts = getattr(archaeological_report, 'artifacts', [])
            clusters = getattr(archaeological_report, 'clusters', {})
            dependency_graph = getattr(archaeological_report, 'dependency_graph', {})
            
        total_artifacts = len(artifacts) if isinstance(artifacts, list) else 0
        total_clusters = len(clusters) if isinstance(clusters, dict) else 0
        edges = dependency_graph.get('edges', []) if isinstance(dependency_graph, dict) else getattr(dependency_graph, 'edges', [])
        total_edges = len(edges) if isinstance(edges, list) else 0
        
        print(f"   🏛️  Artifacts Discovered: {total_artifacts}")
        print(f"   📦 Clusters Formed: {total_clusters}")
        print(f"   🔗 Dependencies Found: {total_edges}")
        
        if isinstance(artifacts, list) and artifacts:
            print("   📁 Sample Artifacts:")
            for i, artifact in enumerate(artifacts[:3], 1):  # Show top 3
                if isinstance(artifact, dict):
                    path = artifact.get('path', 'unknown')
                    file_type = artifact.get('type', 'unknown')
                else:
                    path = getattr(artifact, 'path', 'unknown')
                    file_type = getattr(artifact, 'type', 'unknown')
                    
                print(f"      {i}. {path} ({file_type})")
        elif isinstance(artifacts, list) and not artifacts:
            print("   📁 No artifacts discovered")
        else:
            print("   📁 Unable to determine artifacts")
            
        if isinstance(clusters, dict) and clusters:
            print("   📦 Sample Clusters:")
            for i, (cluster_name, cluster_data) in enumerate(list(clusters.items())[:3], 1):  # Show top 3
                if isinstance(cluster_data, list):
                    cluster_size = len(cluster_data)
                elif isinstance(cluster_data, dict):
                    cluster_size = len(cluster_data.get('artifacts', []))
                else:
                    cluster_size = getattr(cluster_data, 'artifacts_count', 0) if hasattr(cluster_data, 'artifacts_count') else 0
                    
                print(f"      {i}. {cluster_name}: {cluster_size} artifacts")
        elif isinstance(clusters, dict) and not clusters:
            print("   📦 No clusters formed")
        else:
            print("   📦 Unable to determine clusters")
            
    except Exception as e:
        print(f"   ⚠️  Error during archaeological excavation: {e}")
    
    # Perform extended semantic analysis
    print("\n4. Performing extended semantic analysis...")
    try:
        extended_analysis = code_analyzer.analyze_codebase()
        print("   ✅ Extended semantic analysis completed")
        
        # Display extended analysis results
        if isinstance(extended_analysis, dict):
            patterns = extended_analysis.get('patterns', [])
            anti_patterns = extended_analysis.get('anti_patterns', [])
            complexity_hotspots = extended_analysis.get('complexity_hotspots', [])
        else:
            patterns = getattr(extended_analysis, 'patterns', [])
            anti_patterns = getattr(extended_analysis, 'anti_patterns', [])
            complexity_hotspots = getattr(extended_analysis, 'complexity_hotspots', [])
            
        print(f"   🧩 Design Patterns: {len(patterns) if isinstance(patterns, list) else 'N/A'}")
        print(f"   ⚠️  Anti-Patterns: {len(anti_patterns) if isinstance(anti_patterns, list) else 'N/A'}")
        print(f"   🔥 Complexity Hotspots: {len(complexity_hotspots) if isinstance(complexity_hotspots, list) else 'N/A'}")
        
        if isinstance(patterns, list) and patterns:
            print("   🧩 Top Design Patterns:")
            for i, pattern in enumerate(patterns[:3], 1):  # Show top 3
                if isinstance(pattern, dict):
                    pattern_type = pattern.get('type', 'unknown')
                    pattern_desc = pattern.get('description', 'no description')
                else:
                    pattern_type = getattr(pattern, 'type', 'unknown')
                    pattern_desc = getattr(pattern, 'description', 'no description')
                    
                print(f"      {i}. {pattern_type}: {pattern_desc}")
        elif isinstance(patterns, list) and not patterns:
            print("   🧩 No design patterns identified")
        else:
            print("   🧩 Unable to determine design patterns")
            
        if isinstance(anti_patterns, list) and anti_patterns:
            print("   ⚠️  Top Anti-Patterns:")
            for i, anti_pattern in enumerate(anti_patterns[:3], 1):  # Show top 3
                if isinstance(anti_pattern, dict):
                    anti_pattern_type = anti_pattern.get('type', 'unknown')
                    anti_pattern_desc = anti_pattern.get('description', 'no description')
                else:
                    anti_pattern_type = getattr(anti_pattern, 'type', 'unknown')
                    anti_pattern_desc = getattr(anti_pattern, 'description', 'no description')
                    
                print(f"      {i}. {anti_pattern_type}: {anti_pattern_desc}")
        elif isinstance(anti_patterns, list) and not anti_patterns:
            print("   ⚠️  No anti-patterns identified")
        else:
            print("   ⚠️  Unable to determine anti-patterns")
            
        if isinstance(complexity_hotspots, list) and complexity_hotspots:
            print("   🔥 Top Complexity Hotspots:")
            for i, hotspot in enumerate(complexity_hotspots[:3], 1):  # Show top 3
                if isinstance(hotspot, dict):
                    hotspot_file = hotspot.get('file', 'unknown')
                    hotspot_complexity = hotspot.get('complexity', 'unknown')
                else:
                    hotspot_file = getattr(hotspot, 'file', 'unknown')
                    hotspot_complexity = getattr(hotspot, 'complexity', 'unknown')
                    
                print(f"      {i}. {hotspot_file}: {hotspot_complexity}")
        elif isinstance(complexity_hotspots, list) and not complexity_hotspots:
            print("   🔥 No complexity hotspots identified")
        else:
            print("   🔥 Unable to determine complexity hotspots")
            
    except Exception as e:
        print(f"   ⚠️  Error during extended semantic analysis: {e}")
    
    # Perform RSA enhancement analysis
    print("\n5. Performing RSA enhancement analysis...")
    try:
        rsa_results = code_analyzer.analyze_component_with_rsa("code_intelligence_analyzer")
        print("   ✅ RSA enhancement analysis completed")
        
        # Display RSA analysis results
        if isinstance(rsa_results, dict):
            optimization_score = rsa_results.get('optimization_score', 0.0)
            recommendations = rsa_results.get('recommendations', [])
        else:
            optimization_score = getattr(rsa_results, 'optimization_score', 0.0)
            recommendations = getattr(rsa_results, 'recommendations', [])
            
        print(f"   📈 Optimization Score: {optimization_score:.2f}")
        
        if isinstance(recommendations, list) and recommendations:
            print("   💡 RSA Recommendations:")
            for i, recommendation in enumerate(recommendations[:3], 1):  # Show top 3
                print(f"      {i}. {recommendation}")
        elif isinstance(recommendations, list) and not recommendations:
            print("   💡 No specific RSA recommendations at this time")
        else:
            print("   💡 Unable to determine RSA recommendations")
            
    except Exception as e:
        print(f"   ⚠️  Error during RSA enhancement analysis: {e}")
    
    # Generate analysis report
    print("\n6. Generating analysis report...")
    try:
        report = code_analyzer.generate_report("code_analysis_report.md")
        print("   ✅ Analysis report generated")
        
        if isinstance(report, str):
            report_length = len(report)
        else:
            report_length = len(str(report)) if report else 0
            
        print(f"   📄 Report Length: {report_length} characters")
        print("   📂 Report saved to: code_analysis_report.md")
        
    except Exception as e:
        print(f"   ⚠️  Error generating analysis report: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The Code Intelligence Analyzer provides comprehensive capabilities for:")
    print("")
    print("🔍 Deep Code Understanding: Archaeological excavation and semantic analysis")
    print("🏛️  Project Structure Discovery: Artifact identification and clustering")
    print("🔗 Dependency Mapping: Graph-based relationship analysis")
    print("🧩 Pattern Recognition: Design pattern and anti-pattern detection")
    print("🔥 Complexity Analysis: Hotspot identification and optimization")
    print("🔧 RSA Enhancement: Recursive self-architecture improvement recommendations")
    print("📄 Report Generation: Comprehensive documentation of findings")
    print("")
    print("These capabilities enable AI systems to truly understand codebases as")
    print("complex, evolving entities, much like experienced human software engineers.")

async def main():
    results = await demonstrate_code_analysis()
    print("\n✅ Code analysis demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main())