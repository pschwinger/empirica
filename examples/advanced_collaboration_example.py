#!/usr/bin/env python3
"""
Example of using Advanced Collaboration with the Semantic Self-Aware Kit
"""

import asyncio
from semantic_self_aware_kit.advanced_collaboration import create_advanced_partnership_engine

async def demonstrate_advanced_collaboration():
    """
    Demonstrate advanced collaboration capabilities
    """
    print("🤝 Advanced Collaboration with Semantic Self-Aware Kit")
    print("=" * 50)
    
    # Create the advanced partnership engine
    print("\n1. Initializing Advanced Partnership Engine...")
    try:
        partnership_engine = create_advanced_partnership_engine("qwen_collaborator")
        print("   ✅ Advanced Partnership Engine initialized")
        
        # Display engine status
        engine_status = partnership_engine.get_engine_status()
        if isinstance(engine_status, dict):
            is_operational = engine_status.get('is_operational', False)
            intelligence_level = engine_status.get('intelligence_level', 'unknown')
            safety_limited = engine_status.get('safety_limited', True)
        else:
            is_operational = getattr(engine_status, 'is_operational', False)
            intelligence_level = getattr(engine_status, 'intelligence_level', 'unknown')
            safety_limited = getattr(engine_status, 'safety_limited', True)
            
        print(f"   🧠 Intelligence Level: {intelligence_level}")
        print(f"   🔒 Safety Limited: {safety_limited}")
        print(f"   ✅ Operational: {is_operational}")
        
    except Exception as e:
        print(f"   ⚠️  Error initializing advanced partnership engine: {e}")
        return
    
    # Example 1: Establish partnership with another AI
    print("\n2. Establishing partnership with another AI...")
    try:
        # Define partnership parameters
        partner_info = {
            "partner_id": "developer_partner_1",
            "partner_type": "human_developer",
            "capabilities": ["coding", "design", "review"],
            "trust_level": "medium",
            "communication_preferences": {
                "preferred_channels": ["direct_api", "file_based"],
                "message_format": "structured_json",
                "response_time_expectations": "within_24_hours"
            }
        }
        
        # Establish partnership
        partnership = await partnership_engine.establish_partnership(
            "developer_partner_1",
            partner_info
        )
        print("   ✅ Partnership established successfully")
        
        # Display partnership details
        if isinstance(partnership, dict):
            partnership_id = partnership.get('partnership_id', 'N/A')
            trust_level = partnership.get('trust_level', 'unknown')
            collaboration_mode = partnership.get('collaboration_mode', 'unknown')
            communication_protocols = partnership.get('communication_protocols', {})
        else:
            partnership_id = getattr(partnership, 'partnership_id', 'N/A')
            trust_level = getattr(partnership, 'trust_level', 'unknown')
            collaboration_mode = getattr(partnership, 'collaboration_mode', 'unknown')
            communication_protocols = getattr(partnership, 'communication_protocols', {})
            
        print(f"   🆔 Partnership ID: {partnership_id}")
        print(f"   🤝 Trust Level: {trust_level}")
        print(f"   🔄 Collaboration Mode: {collaboration_mode}")
        
        if isinstance(communication_protocols, dict) and communication_protocols:
            primary_channel = communication_protocols.get('primary_channel', 'unknown')
            backup_channels = communication_protocols.get('backup_channels', [])
        else:
            primary_channel = getattr(communication_protocols, 'primary_channel', 'unknown')
            backup_channels = getattr(communication_protocols, 'backup_channels', [])
            
        print(f"   📡 Primary Channel: {primary_channel}")
        if backup_channels:
            print(f"   🔁 Backup Channels: {', '.join(backup_channels[:3]) if isinstance(backup_channels, list) else 'N/A'}")
        else:
            print("   🔁 No backup channels specified")
            
    except Exception as e:
        print(f"   ⚠️  Error establishing partnership: {e}")
    
    # Example 2: Coordinate collaborative task
    print("\n3. Coordinating collaborative task...")
    try:
        # Define a collaborative task
        task_definition = {
            "task_id": "code_refactor_task_1",
            "task_type": "code_review_and_refactor",
            "description": "Review and refactor the authentication module for improved security and performance",
            "complexity": "high",
            "required_skills": ["security", "python", "refactoring"],
            "estimated_duration": "3 days",
            "priority": "high",
            "dependencies": ["security_audit_complete", "performance_benchmark_available"]
        }
        
        # Coordinate the task with the partnership
        task_coordination = await partnership_engine.coordinate_task_execution(
            "developer_partner_1",
            task_definition
        )
        print("   ✅ Task coordination completed")
        
        # Display coordination results
        if isinstance(task_coordination, dict):
            coordination_status = task_coordination.get('coordination_status', 'unknown')
            assigned_resources = task_coordination.get('assigned_resources', [])
            timeline_adjustments = task_coordination.get('timeline_adjustments', {})
        else:
            coordination_status = getattr(task_coordination, 'coordination_status', 'unknown')
            assigned_resources = getattr(task_coordination, 'assigned_resources', [])
            timeline_adjustments = getattr(task_coordination, 'timeline_adjustments', {})
            
        print(f"   📊 Coordination Status: {coordination_status}")
        
        if isinstance(assigned_resources, list) and assigned_resources:
            print("   👥 Assigned Resources:")
            for i, resource in enumerate(assigned_resources[:3], 1):  # Show top 3
                if isinstance(resource, dict):
                    resource_id = resource.get('resource_id', 'unknown')
                    resource_type = resource.get('resource_type', 'unknown')
                else:
                    resource_id = getattr(resource, 'resource_id', 'unknown')
                    resource_type = getattr(resource, 'resource_type', 'unknown')
                    
                print(f"      {i}. {resource_id} ({resource_type})")
        elif isinstance(assigned_resources, list) and not assigned_resources:
            print("   👥 No specific resources assigned")
        else:
            print("   👥 Unable to determine assigned resources")
            
        if isinstance(timeline_adjustments, dict) and timeline_adjustments:
            print("   📅 Timeline Adjustments:")
            for adjustment_type, adjustment_value in list(timeline_adjustments.items())[:3]:  # Show top 3
                print(f"      • {adjustment_type}: {adjustment_value}")
        elif isinstance(timeline_adjustments, dict) and not timeline_adjustments:
            print("   📅 No timeline adjustments required")
        else:
            print("   📅 Unable to determine timeline adjustments")
            
    except Exception as e:
        print(f"   ⚠️  Error during task coordination: {e}")
    
    # Example 3: Facilitate multi-agent collaboration
    print("\n4. Facilitating multi-agent collaboration...")
    try:
        # Define multiple partners for collaboration
        partners = [
            {
                "partner_id": "security_expert",
                "partner_type": "ai_specialist",
                "specialization": "cybersecurity",
                "capabilities": ["threat_modeling", "vulnerability_assessment", "penetration_testing"]
            },
            {
                "partner_id": "performance_optimization_expert",
                "partner_type": "ai_specialist",
                "specialization": "performance_optimization",
                "capabilities": ["profiling", "benchmarking", "optimization"]
            },
            {
                "partner_id": "code_quality_expert",
                "partner_type": "ai_specialist",
                "specialization": "code_quality",
                "capabilities": ["linting", "refactoring", "best_practices"]
            }
        ]
        
        # Establish partnerships with all partners
        partnerships = []
        for partner in partners:
            partnership = await partnership_engine.establish_partnership(
                partner["partner_id"],
                partner
            )
            partnerships.append(partnership)
            print(f"   ✅ Partnership established with {partner['partner_id']}")
            
        print(f"   🤝 {len(partnerships)} partnerships established")
        
        # Coordinate a complex multi-partner task
        complex_task = {
            "task_id": "comprehensive_code_analysis_task_1",
            "task_type": "multi_dimensional_code_analysis",
            "description": "Comprehensive analysis of the entire codebase covering security, performance, and quality aspects",
            "complexity": "very_high",
            "required_skills": ["security", "performance", "code_quality", "refactoring"],
            "estimated_duration": "1 week",
            "priority": "critical",
            "dependencies": []
        }
        
        # Create a temporary collaboration group
        collaboration_group = await partnership_engine.create_collaboration_group(
            "comprehensive_analysis_group",
            [p["partner_id"] for p in partners]
        )
        print("   ✅ Collaboration group created")
        
        # Coordinate the complex task with the group
        group_coordination = await partnership_engine.coordinate_group_task_execution(
            "comprehensive_analysis_group",
            complex_task
        )
        print("   ✅ Group task coordination completed")
        
        # Display group coordination results
        if isinstance(group_coordination, dict):
            group_coordination_status = group_coordination.get('coordination_status', 'unknown')
            task_distribution = group_coordination.get('task_distribution', {})
        else:
            group_coordination_status = getattr(group_coordination, 'coordination_status', 'unknown')
            task_distribution = getattr(group_coordination, 'task_distribution', {})
            
        print(f"   📊 Group Coordination Status: {group_coordination_status}")
        
        if isinstance(task_distribution, dict) and task_distribution:
            print("   📋 Task Distribution:")
            for partner_id, tasks in list(task_distribution.items())[:3]:  # Show top 3
                print(f"      • {partner_id}: {len(tasks) if isinstance(tasks, list) else 'N/A'} tasks")
        elif isinstance(task_distribution, dict) and not task_distribution:
            print("   📋 No specific task distribution")
        else:
            print("   📋 Unable to determine task distribution")
            
    except Exception as e:
        print(f"   ⚠️  Error during multi-agent collaboration: {e}")
    
    # Example 4: Monitor collaboration effectiveness
    print("\n5. Monitoring collaboration effectiveness...")
    try:
        # Get collaboration metrics
        collaboration_metrics = partnership_engine.get_collaboration_metrics()
        print("   ✅ Collaboration metrics retrieved")
        
        # Display metrics
        if isinstance(collaboration_metrics, dict):
            partnership_count = collaboration_metrics.get('partnership_count', 0)
            task_completion_rate = collaboration_metrics.get('task_completion_rate', 0.0)
            collaboration_efficiency = collaboration_metrics.get('collaboration_efficiency', 0.0)
            trust_evolution = collaboration_metrics.get('trust_evolution', {})
        else:
            partnership_count = getattr(collaboration_metrics, 'partnership_count', 0)
            task_completion_rate = getattr(collaboration_metrics, 'task_completion_rate', 0.0)
            collaboration_efficiency = getattr(collaboration_metrics, 'collaboration_efficiency', 0.0)
            trust_evolution = getattr(collaboration_metrics, 'trust_evolution', {})
            
        print(f"   🤝 Active Partnerships: {partnership_count}")
        print(f"   📈 Task Completion Rate: {task_completion_rate:.2f}")
        print(f"   ⚡ Collaboration Efficiency: {collaboration_efficiency:.2f}")
        
        if isinstance(trust_evolution, dict) and trust_evolution:
            print("   📈 Trust Evolution:")
            for partner_id, trust_trend in list(trust_evolution.items())[:3]:  # Show top 3
                print(f"      • {partner_id}: {trust_trend}")
        elif isinstance(trust_evolution, dict) and not trust_evolution:
            print("   📈 No trust evolution data available")
        else:
            print("   📈 Unable to determine trust evolution")
            
        # Get partnership recommendations
        recommendations = await partnership_engine.get_partnership_recommendations()
        print("   ✅ Partnership recommendations generated")
        
        if isinstance(recommendations, list) and recommendations:
            print(f"   💡 {len(recommendations)} Partnership Recommendations:")
            for i, recommendation in enumerate(recommendations[:3], 1):  # Show top 3
                if isinstance(recommendation, dict):
                    partner_id = recommendation.get('partner_id', 'unknown')
                    reason = recommendation.get('reason', 'no reason')
                    confidence = recommendation.get('confidence_score', 0.0)
                else:
                    partner_id = getattr(recommendation, 'partner_id', 'unknown')
                    reason = getattr(recommendation, 'reason', 'no reason')
                    confidence = getattr(recommendation, 'confidence_score', 0.0)
                    
                print(f"      {i}. {partner_id} (Confidence: {confidence:.2f}) - {reason}")
        elif isinstance(recommendations, list) and not recommendations:
            print("   💡 No specific partnership recommendations at this time")
        else:
            print("   💡 Unable to retrieve partnership recommendations")
            
    except Exception as e:
        print(f"   ⚠️  Error during collaboration monitoring: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The Advanced Collaboration component provides sophisticated capabilities for:")
    print("")
    print("🤝 Partnership Establishment: Creating and managing AI-to-AI and AI-to-Human partnerships")
    print("📋 Task Coordination: Distributing and coordinating complex tasks among multiple partners")
    print("🧠 Multi-Agent Collaboration: Facilitating collaboration among groups of AI specialists")
    print("📊 Performance Monitoring: Tracking collaboration effectiveness and trust evolution")
    print("💡 Intelligent Recommendations: Providing suggestions for optimal partnership formation")
    print("")
    print("These capabilities enable AI systems to work effectively with both human developers")
    print("and other AI systems, forming collaborative networks that can tackle complex problems")
    print("beyond the scope of any single agent.")

async def main():
    results = await demonstrate_advanced_collaboration()
    print("\n✅ Advanced collaboration demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main())