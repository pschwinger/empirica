#!/usr/bin/env python3
"""
Example of using Advanced Uncertainty Analysis with the Semantic Self-Aware Kit
"""

import asyncio
from semantic_self_aware_kit.advanced_uncertainty import create_advanced_uncertainty_analyzer

async def demonstrate_advanced_uncertainty_analysis():
    """
    Demonstrate advanced uncertainty analysis capabilities
    """
    print("🤔 Advanced Uncertainty Analysis with Semantic Self-Aware Kit")
    print("=" * 58)
    
    # Create the advanced uncertainty analyzer
    print("\n1. Initializing Advanced Uncertainty Analyzer...")
    try:
        uncertainty_analyzer = create_advanced_uncertainty_analyzer()
        print("   ✅ Advanced Uncertainty Analyzer initialized")
        
        # Display analyzer capabilities
        analyzer_status = uncertainty_analyzer.get_analyzer_status()
        if isinstance(analyzer_status, dict):
            is_operational = analyzer_status.get('is_operational', False)
            intelligence_level = analyzer_status.get('intelligence_level', 'unknown')
            safety_limited = analyzer_status.get('safety_limited', True)
        else:
            is_operational = getattr(analyzer_status, 'is_operational', False)
            intelligence_level = getattr(analyzer_status, 'intelligence_level', 'unknown')
            safety_limited = getattr(analyzer_status, 'safety_limited', True)
            
        print(f"   🧠 Intelligence Level: {intelligence_level}")
        print(f"   🔒 Safety Limited: {safety_limited}")
        print(f"   ✅ Operational: {is_operational}")
        
    except Exception as e:
        print(f"   ⚠️  Error initializing advanced uncertainty analyzer: {e}")
        return
    
    # Example 1: Multi-dimensional uncertainty assessment
    print("\n2. Performing multi-dimensional uncertainty assessment...")
    try:
        # Define a decision context
        decision_context = {
            "decision": "Should we implement a neural network for this classification task?",
            "complexity": "high",
            "data_availability": "limited",
            "time_constraints": "tight",
            "resource_constraints": "moderate",
            "expertise_availability": "intermediate"
        }
        
        # Assess uncertainty across multiple dimensions
        assessment_results = uncertainty_analyzer.assess_decision_uncertainty(
            "neural_network_implementation",
            decision_context
        )
        print("   ✅ Multi-dimensional uncertainty assessment completed")
        
        # Display assessment results
        if isinstance(assessment_results, dict):
            overall_uncertainty = assessment_results.get('overall_uncertainty_score', 0.0)
            dominant_dimension = assessment_results.get('dominant_uncertainty_dimension', 'unknown')
            confidence_level = assessment_results.get('confidence_level', 'low')
        else:
            overall_uncertainty = getattr(assessment_results, 'overall_uncertainty_score', 0.0)
            dominant_dimension = getattr(assessment_results, 'dominant_uncertainty_dimension', 'unknown')
            confidence_level = getattr(assessment_results, 'confidence_level', 'low')
            
        print(f"   📊 Overall Uncertainty Score: {overall_uncertainty:.2f}")
        print(f"   🎯 Dominant Uncertainty Dimension: {dominant_dimension}")
        print(f"   🔍 Confidence Level: {confidence_level}")
        
        # Show uncertainty breakdown by dimension
        uncertainty_dimensions = assessment_results.get('uncertainty_dimensions', {}) if isinstance(assessment_results, dict) else getattr(assessment_results, 'uncertainty_dimensions', {})
        if isinstance(uncertainty_dimensions, dict) and uncertainty_dimensions:
            print("   📐 Uncertainty by Dimension:")
            for dimension, score in list(uncertainty_dimensions.items())[:5]:  # Show top 5
                print(f"      • {dimension}: {score:.2f}")
        else:
            print("   📐 No specific uncertainty dimensions available")
            
    except Exception as e:
        print(f"   ⚠️  Error during multi-dimensional uncertainty assessment: {e}")
    
    # Example 2: Systematic uncertainty investigation
    print("\n3. Conducting systematic uncertainty investigation...")
    try:
        # Define investigation parameters
        investigation_params = {
            "investigation_depth": "comprehensive",
            "focus_areas": ["data_quality", "model_selection", "hyperparameter_tuning"],
            "resource_allocation": "moderate"
        }
        
        # Conduct investigation
        investigation_results = await uncertainty_analyzer.investigate_uncertainty(
            "neural_network_implementation",
            investigation_params
        )
        print("   ✅ Systematic uncertainty investigation completed")
        
        # Display investigation results
        if isinstance(investigation_results, dict):
            investigation_status = investigation_results.get('investigation_status', 'unknown')
            findings = investigation_results.get('findings', [])
            recommendations = investigation_results.get('recommendations', [])
        else:
            investigation_status = getattr(investigation_results, 'investigation_status', 'unknown')
            findings = getattr(investigation_results, 'findings', [])
            recommendations = getattr(investigation_results, 'recommendations', [])
            
        print(f"   🔍 Investigation Status: {investigation_status}")
        
        if findings:
            print("   📋 Key Findings:")
            for i, finding in enumerate(findings[:3], 1):  # Show top 3
                print(f"      {i}. {finding}")
        else:
            print("   📋 No specific findings at this time")
            
        if recommendations:
            print("   💡 Recommendations:")
            for i, recommendation in enumerate(recommendations[:3], 1):  # Show top 3
                print(f"      {i}. {recommendation}")
        else:
            print("   💡 No specific recommendations at this time")
            
    except Exception as e:
        print(f"   ⚠️  Error during systematic uncertainty investigation: {e}")
    
    # Example 3: Confidence improvement and action planning
    print("\n4. Planning confidence improvement and actions...")
    try:
        # Define action planning context
        action_context = {
            "desired_confidence_level": "high",
            "available_resources": ["computational_power", "expert_knowledge", "time"],
            "risk_tolerance": "moderate"
        }
        
        # Plan confidence improvement actions
        action_plan = uncertainty_analyzer.plan_confidence_improvement(
            "neural_network_implementation",
            action_context
        )
        print("   ✅ Confidence improvement action plan generated")
        
        # Display action plan
        if isinstance(action_plan, dict):
            required_actions = action_plan.get('required_actions', [])
            expected_improvement = action_plan.get('expected_confidence_improvement', 0.0)
            resource_requirements = action_plan.get('resource_requirements', [])
        else:
            required_actions = getattr(action_plan, 'required_actions', [])
            expected_improvement = getattr(action_plan, 'expected_confidence_improvement', 0.0)
            resource_requirements = getattr(action_plan, 'resource_requirements', [])
            
        print(f"   📈 Expected Confidence Improvement: {expected_improvement:.2f}")
        
        if required_actions:
            print("   🎯 Required Actions:")
            for i, action in enumerate(required_actions[:5], 1):  # Show top 5
                print(f"      {i}. {action}")
        else:
            print("   🎯 No specific actions required at this time")
            
        if resource_requirements:
            print("   🧰 Resource Requirements:")
            for i, requirement in enumerate(resource_requirements[:3], 1):  # Show top 3
                print(f"      {i}. {requirement}")
        else:
            print("   🧰 No specific resource requirements identified")
            
    except Exception as e:
        print(f"   ⚠️  Error during confidence improvement planning: {e}")
    
    # Example 4: Meta-cognitive validation
    print("\n5. Performing meta-cognitive validation...")
    try:
        # Perform validation of the uncertainty analysis process itself
        validation_results = uncertainty_analyzer.validate_analysis_process(
            "neural_network_implementation"
        )
        print("   ✅ Meta-cognitive validation completed")
        
        # Display validation results
        if isinstance(validation_results, dict):
            process_quality = validation_results.get('process_quality_score', 0.0)
            bias_identified = validation_results.get('bias_identified', False)
            improvement_suggestions = validation_results.get('improvement_suggestions', [])
        else:
            process_quality = getattr(validation_results, 'process_quality_score', 0.0)
            bias_identified = getattr(validation_results, 'bias_identified', False)
            improvement_suggestions = getattr(validation_results, 'improvement_suggestions', [])
            
        print(f"   📊 Process Quality Score: {process_quality:.2f}")
        print(f"   🤔 Bias Identified: {bias_identified}")
        
        if improvement_suggestions:
            print("   💡 Improvement Suggestions:")
            for i, suggestion in enumerate(improvement_suggestions[:3], 1):  # Show top 3
                print(f"      {i}. {suggestion}")
        else:
            print("   💡 No specific improvement suggestions at this time")
            
    except Exception as e:
        print(f"   ⚠️  Error during meta-cognitive validation: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The Advanced Uncertainty Analyzer provides sophisticated capabilities for:")
    print("")
    print("🤔 Multi-Dimensional Uncertainty Assessment: Quantifying uncertainty across")
    print("   multiple dimensions (epistemic, aleatoric, contextual, temporal, semantic, causal)")
    print("")
    print("🔬 Systematic Uncertainty Investigation: Conducting thorough investigations")
    print("   to reduce uncertainty and increase confidence in decisions")
    print("")
    print("📈 Confidence Improvement Planning: Generating action plans to increase")
    print("   confidence levels and reduce uncertainty")
    print("")
    print("🧠 Meta-Cognitive Validation: Validating the uncertainty analysis process")
    print("   itself to ensure quality and identify potential biases")
    print("")
    print("These capabilities enable AI systems to make more informed, robust decisions")
    print("by explicitly quantifying and managing uncertainty in complex scenarios.")

async def main():
    results = await demonstrate_advanced_uncertainty_analysis()
    print("\n✅ Advanced uncertainty analysis demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main())