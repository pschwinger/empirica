#!/usr/bin/env python3
"""
Example of using Tool Management with the Semantic Self-Aware Kit
"""

import asyncio
from semantic_self_aware_kit.tool_management import create_tool_registry, AIEnhancedToolManager

async def demonstrate_tool_management():
    """
    Demonstrate tool management capabilities
    """
    print("🛠️ Tool Management with Semantic Self-Aware Kit")
    print("=" * 45)
    
    # Create the tool registry
    print("\n1. Initializing Tool Registry...")
    try:
        tool_registry = create_tool_registry()
        print("   ✅ Tool Registry initialized")
        
        # Display initial tool statistics
        stats = tool_registry.get_tool_stats()
        print("   📊 Initial Tool Statistics:")
        
        if isinstance(stats, dict):
            total_tools = stats.get('total_tools', 0)
            categories = stats.get('categories', [])
        else:
            total_tools = getattr(stats, 'total_tools', 0)
            categories = getattr(stats, 'categories', [])
            
        print(f"      Total Tools: {total_tools}")
        print(f"      Categories: {len(categories) if isinstance(categories, list) else 'N/A'}")
        
        if isinstance(categories, list) and categories:
            print("      Category List:")
            for i, category in enumerate(categories[:5], 1):  # Show top 5
                print(f"         {i}. {category}")
        elif isinstance(categories, list) and not categories:
            print("      Category List: No categories available")
        else:
            print("      Category List: Unable to determine categories")
            
    except Exception as e:
        print(f"   ⚠️  Error initializing tool registry: {e}")
        return
    
    # Example 1: Register tools
    print("\n2. Registering tools...")
    try:
        # Define example tools to register
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
            },
            {
                "tool_id": "performance_analyzer",
                "name": "Performance Analyzer",
                "description": "Analyzes code performance and identifies bottlenecks",
                "category": "performance",
                "capabilities": ["profile", "benchmark", "optimize"],
                "version": "1.5.0"
            },
            {
                "tool_id": "documentation_generator",
                "name": "Documentation Generator",
                "description": "Generates comprehensive documentation for codebases",
                "category": "documentation",
                "capabilities": ["generate", "format", "publish"],
                "version": "1.2.0"
            },
            {
                "tool_id": "test_runner",
                "name": "Test Runner",
                "description": "Runs comprehensive test suites and generates reports",
                "category": "testing",
                "capabilities": ["execute", "report", "analyze"],
                "version": "1.8.0"
            }
        ]
        
        # Register each tool
        registered_count = 0
        for tool_data in example_tools:
            success = tool_registry.register_tool(tool_data)
            if success:
                registered_count += 1
                print(f"   ✅ Registered tool: {tool_data['name']}")
            else:
                print(f"   ⚠️  Failed to register tool: {tool_data['name']}")
                
        print(f"   📈 Total Tools Registered: {registered_count}")
        
        # Update tool statistics
        updated_stats = tool_registry.get_tool_stats()
        print("   📊 Updated Tool Statistics:")
        
        if isinstance(updated_stats, dict):
            new_total = updated_stats.get('total_tools', 0)
            new_categories = updated_stats.get('categories', [])
        else:
            new_total = getattr(updated_stats, 'total_tools', 0)
            new_categories = getattr(updated_stats, 'categories', [])
            
        print(f"      Updated Total Tools: {new_total}")
        print(f"      Updated Categories: {len(new_categories) if isinstance(new_categories, list) else 'N/A'}")
        
        if isinstance(new_categories, list) and new_categories:
            print("      Updated Category List:")
            for i, category in enumerate(new_categories[:5], 1):  # Show top 5
                print(f"         {i}. {category}")
        elif isinstance(new_categories, list) and not new_categories:
            print("      Updated Category List: No categories available")
        else:
            print("      Updated Category List: Unable to determine categories")
            
    except Exception as e:
        print(f"   ⚠️  Error during tool registration: {e}")
    
    # Example 2: Search for tools based on context
    print("\n3. Searching for contextually relevant tools...")
    try:
        # Define a task context
        task_context = {
            "task_type": "code_review",
            "language": "python",
            "focus_areas": ["security", "performance", "readability"],
            "urgency": "high",
            "expertise_required": ["intermediate", "security"],
            "time_available": "2 hours"
        }
        
        # Search for relevant tools
        search_results = tool_registry.search_tools("security")
        print("   ✅ Tool search completed")
        
        if isinstance(search_results, list) and search_results:
            print(f"   🔍 {len(search_results)} Security-Related Tools Found:")
            for i, tool in enumerate(search_results[:5], 1):  # Show top 5
                if isinstance(tool, dict):
                    tool_name = tool.get('name', 'Unknown')
                    tool_desc = tool.get('description', 'No description')
                else:
                    tool_name = getattr(tool, 'name', 'Unknown')
                    tool_desc = getattr(tool, 'description', 'No description')
                    
                print(f"      {i}. {tool_name}: {tool_desc}")
        elif isinstance(search_results, list) and not search_results:
            print("   ⚠️  No security-related tools found")
        else:
            print("   ⚠️  Error retrieving search results")
            
        # Search for performance-related tools
        perf_search_results = tool_registry.search_tools("performance")
        print("   ✅ Performance tool search completed")
        
        if isinstance(perf_search_results, list) and perf_search_results:
            print(f"   ⚡ {len(perf_search_results)} Performance-Related Tools Found:")
            for i, tool in enumerate(perf_search_results[:3], 1):  # Show top 3
                if isinstance(tool, dict):
                    tool_name = tool.get('name', 'Unknown')
                    tool_desc = tool.get('description', 'No description')
                else:
                    tool_name = getattr(tool, 'name', 'Unknown')
                    tool_desc = getattr(tool, 'description', 'No description')
                    
                print(f"      {i}. {tool_name}: {tool_desc}")
        elif isinstance(perf_search_results, list) and not perf_search_results:
            print("   ⚠️  No performance-related tools found")
        else:
            print("   ⚠️  Error retrieving performance search results")
            
    except Exception as e:
        print(f"   ⚠️  Error during tool search: {e}")
    
    # Example 3: Get intelligent tool recommendations
    print("\n4. Getting intelligent tool recommendations...")
    try:
        # Create the AI-Enhanced Tool Manager
        tool_manager = AIEnhancedToolManager()
        print("   ✅ AI-Enhanced Tool Manager created")
        
        # Define a more specific task context
        specific_context = {
            "task": "security_audit",
            "domain": "web_application",
            "complexity": "high",
            "required_capabilities": ["vulnerability_scanning", "code_analysis", "reporting"],
            "time_constraint": "urgent"
        }
        
        # Get recommendations for an AI system
        recommendations = await tool_manager.get_intelligent_tool_recommendations(
            "qwen_ai", 
            specific_context
        )
        print("   ✅ Tool recommendations generated")
        
        if isinstance(recommendations, list) and recommendations:
            print(f"   🎯 {len(recommendations)} Recommended Tools:")
            for i, recommendation in enumerate(recommendations[:5], 1):  # Show top 5
                if isinstance(recommendation, dict):
                    tool_id = recommendation.get('tool_id', 'Unknown')
                    confidence = recommendation.get('confidence_score', 0.0)
                    reasoning = recommendation.get('reasoning', ['No reasoning provided'])
                else:
                    tool_id = getattr(recommendation, 'tool_id', 'Unknown')
                    confidence = getattr(recommendation, 'confidence_score', 0.0)
                    reasoning = getattr(recommendation, 'reasoning', ['No reasoning provided'])
                    
                print(f"      {i}. {tool_id} (Confidence: {confidence:.2f})")
                if isinstance(reasoning, list) and reasoning:
                    print(f"         Reasoning: {reasoning[0] if reasoning else 'No reasoning'}")
                elif isinstance(reasoning, list) and not reasoning:
                    print("         Reasoning: No specific reasoning provided")
                else:
                    print("         Reasoning: Unable to determine reasoning")
        elif isinstance(recommendations, list) and not recommendations:
            print("   📋 No specific tool recommendations at this time")
        else:
            print("   ⚠️  Error retrieving tool recommendations")
            
    except Exception as e:
        print(f"   ⚠️  Error during tool recommendation: {e}")
    
    # Example 4: Predict tool performance
    print("\n5. Predicting tool performance...")
    try:
        # Predict performance for a specific tool in a given context
        context = {'task': 'security_scan', 'urgency': 'high'}
        prediction = await tool_manager.predict_tool_performance(
            "security_scanner",
            "qwen_ai", 
            context
        )
        print("   ✅ Tool performance prediction completed")
        
        if isinstance(prediction, dict):
            success_rate = prediction.get('predicted_success_rate', 'N/A')
            duration = prediction.get('predicted_duration', 'N/A')
            recommendation = prediction.get('recommendation', 'N/A')
        else:
            success_rate = getattr(prediction, 'predicted_success_rate', 'N/A')
            duration = getattr(prediction, 'predicted_duration', 'N/A')
            recommendation = getattr(prediction, 'recommendation', 'N/A')
            
        print(f"   📊 Predicted Success Rate: {success_rate}")
        print(f"   🕐 Predicted Duration: {duration} seconds")
        print(f"   💡 Recommendation: {recommendation}")
        
    except Exception as e:
        print(f"   ⚠️  Error during performance prediction: {e}")
    
    # Example 5: Optimize tool access
    print("\n6. Optimizing tool access for AI...")
    try:
        optimizations = await tool_manager.optimize_tool_access_for_ai("qwen_ai")
        print("   ✅ Tool access optimization completed")
        
        if isinstance(optimizations, dict):
            recommendations = optimizations.get('recommendations', [])
        else:
            recommendations = getattr(optimizations, 'recommendations', [])
            
        if isinstance(recommendations, list) and recommendations:
            print("   🚀 Optimization Recommendations:")
            for i, recommendation in enumerate(recommendations[:5], 1):  # Show top 5
                print(f"      {i}. {recommendation}")
        elif isinstance(recommendations, list) and not recommendations:
            print("   ✅ Tool access is already optimized")
        else:
            print("   ⚠️  Unable to determine optimization recommendations")
            
    except Exception as e:
        print(f"   ⚠️  Error during tool access optimization: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The Tool Management component provides intelligent discovery, registration,")
    print("recommendation, and optimization of tools based on task context and usage patterns.")
    print("This enables AI systems to select the most appropriate tools for specific tasks")
    print("and continuously improve their tool usage.")
    
    return {
        "tool_registry": tool_registry if 'tool_registry' in locals() else None,
        "tool_manager": tool_manager if 'tool_manager' in locals() else None,
        "search_results": search_results if 'search_results' in locals() else None,
        "recommendations": recommendations if 'recommendations' in locals() else None,
        "performance_prediction": prediction if 'prediction' in locals() else None,
        "optimizations": optimizations if 'optimizations' in locals() else None
    }

async def main():
    results = await demonstrate_tool_management()
    print("\n✅ Tool management demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main())