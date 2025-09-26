#!/usr/bin/env python3
"""
Daily Development Example with the Semantic Self-Aware Kit
"""

import asyncio
from semantic_self_aware_kit import SemanticFramework

async def demonstrate_daily_development():
    """
    Demonstrate daily development workflow with the Semantic Self-Aware Kit
    """
    print("📅 Daily Development Workflow with Semantic Self-Aware Kit")
    print("=" * 55)
    
    # Initialize the complete framework
    print("\n1. Initializing Semantic Framework...")
    try:
        framework = SemanticFramework()
        await framework.startup()
        print("   ✅ Semantic Framework initialized")
        
        # Display framework status
        framework_status = framework.get_framework_status()
        print("   📊 Framework Status:")
        
        if isinstance(framework_status, dict):
            framework_version = framework_status.get('framework_version', 'unknown')
            modules_loaded = framework_status.get('modules_loaded', 0)
            status = framework_status.get('status', 'unknown')
        else:
            framework_version = getattr(framework_status, 'framework_version', 'unknown')
            modules_loaded = getattr(framework_status, 'modules_loaded', 0)
            status = getattr(framework_status, 'status', 'unknown')
            
        print(f"      Framework Version: {framework_version}")
        print(f"      Modules Loaded: {modules_loaded}")
        print(f"      Status: {status}")
        
    except Exception as e:
        print(f"   ⚠️  Error initializing framework: {e}")
        return
    
    # Morning routine - System health check
    print("\n2. 🌅 Morning Routine - System Health Check")
    try:
        health_status = framework.get_system_health()
        print("   ✅ System health check completed")
        
        if isinstance(health_status, dict):
            health_score = health_status.get('health_score', 0.0)
            readiness_level = health_status.get('readiness_level', 'unknown')
        else:
            health_score = getattr(health_status, 'health_score', 0.0)
            readiness_level = getattr(health_status, 'readiness_level', 'unknown')
            
        print(f"   📊 Health Score: {health_score:.2f}")
        print(f"   🚀 Readiness Level: {readiness_level}")
        
        # If health is low, suggest improvements
        if health_score < 0.7:
            print("   ⚠️  Health score below threshold, suggesting improvements...")
            suggestions = framework.get_intelligent_suggestions()
            if isinstance(suggestions, list) and suggestions:
                print("   💡 Improvement Suggestions:")
                for i, suggestion in enumerate(suggestions[:3], 1):  # Show top 3
                    if isinstance(suggestion, dict):
                        suggestion_text = suggestion.get('suggestion', 'No suggestion')
                        priority = suggestion.get('priority', 'medium')
                    else:
                        suggestion_text = getattr(suggestion, 'suggestion', 'No suggestion')
                        priority = getattr(suggestion, 'priority', 'medium')
                        
                    print(f"      {i}. [{priority.upper()}] {suggestion_text}")
            elif isinstance(suggestions, list) and not suggestions:
                print("   📋 No specific suggestions at this time")
            else:
                print("   ⚠️  Error retrieving suggestions")
        else:
            print("   ✅ System health is good, ready for development")
            
    except Exception as e:
        print(f"   ⚠️  Error during system health check: {e}")
    
    # Task 1 - Code review and analysis
    print("\n3. 📝 Task 1 - Code Review and Analysis")
    try:
        # Analyze the current project for code quality
        code_analysis = framework.code_intelligence.analyze(".")
        print("   ✅ Code analysis completed")
        
        if isinstance(code_analysis, dict):
            metadata = code_analysis.get('metadata', {})
            synthesis = code_analysis.get('synthesis', {})
        else:
            metadata = getattr(code_analysis, 'metadata', {})
            synthesis = getattr(code_analysis, 'synthesis', {})
            
        files_analyzed = metadata.get('total_artifacts', 0)
        print(f"   📊 Files Analyzed: {files_analyzed}")
        
        # Check for issues
        issues = synthesis.get('identified_issues', [])
        if isinstance(issues, list) and issues:
            print("   ⚠️  Code Issues Found:")
            for i, issue in enumerate(issues[:5], 1):  # Show top 5
                if isinstance(issue, dict):
                    issue_type = issue.get('type', 'unknown')
                    severity = issue.get('severity', 'unknown')
                    description = issue.get('description', 'no description')
                else:
                    issue_type = getattr(issue, 'type', 'unknown')
                    severity = getattr(issue, 'severity', 'unknown')
                    description = getattr(issue, 'description', 'no description')
                    
                print(f"      {i}. [{severity.upper()}] {issue_type}: {description}")
        elif isinstance(issues, list) and not issues:
            print("   ✅ No code issues found")
        else:
            print("   ⚠️  Error determining code issues")
            
        # Get recommendations
        recommendations = synthesis.get('key_recommendations', [])
        if isinstance(recommendations, list) and recommendations:
            print("   💡 Recommendations:")
            for i, recommendation in enumerate(recommendations[:3], 1):  # Show top 3
                print(f"      {i}. {recommendation}")
        elif isinstance(recommendations, list) and not recommendations:
            print("   📋 No specific recommendations at this time")
        else:
            print("   ⚠️  Error retrieving recommendations")
            
    except Exception as e:
        print(f"   ⚠️  Error during code review and analysis: {e}")
    
    # Task 2 - Performance optimization
    print("\n4. ⚡ Task 2 - Performance Optimization")
    try:
        # Run performance benchmarks
        perf_results = await framework.performance.benchmark("daily_development")
        print("   ✅ Performance benchmarks completed")
        
        if isinstance(perf_results, dict):
            overall_score = perf_results.get('overall_score', 0.0)
            tests_executed = perf_results.get('tests_executed', 0)
        else:
            overall_score = getattr(perf_results, 'overall_score', 0.0)
            tests_executed = getattr(perf_results, 'tests_executed', 0)
            
        print(f"   📊 Overall Performance Score: {overall_score:.2f}")
        print(f"   🎯 Tests Executed: {tests_executed}")
        
        # If performance is low, suggest optimizations
        if overall_score < 0.7:
            print("   ⚠️  Performance score below threshold, suggesting optimizations...")
            optimization_suggestions = framework.get_performance_optimization_suggestions()
            if isinstance(optimization_suggestions, list) and optimization_suggestions:
                print("   💡 Optimization Suggestions:")
                for i, suggestion in enumerate(optimization_suggestions[:3], 1):  # Show top 3
                    if isinstance(suggestion, dict):
                        suggestion_text = suggestion.get('suggestion', 'No suggestion')
                        impact = suggestion.get('impact', 'medium')
                    else:
                        suggestion_text = getattr(suggestion, 'suggestion', 'No suggestion')
                        impact = getattr(suggestion, 'impact', 'medium')
                        
                    print(f"      {i}. [{impact.upper()}] {suggestion_text}")
            elif isinstance(optimization_suggestions, list) and not optimization_suggestions:
                print("   📋 No specific optimization suggestions at this time")
            else:
                print("   ⚠️  Error retrieving optimization suggestions")
        else:
            print("   ✅ Performance is good")
            
    except Exception as e:
        print(f"   ⚠️  Error during performance optimization: {e}")
    
    # Task 3 - Security audit
    print("\n5. 🛡️ Task 3 - Security Audit")
    try:
        # Activate security monitoring
        security_monitor = framework.security.activate_monitoring(monitoring_interval=5)
        print("   ✅ Security monitoring activated")
        
        # Check for security issues
        security_status = security_monitor.get_security_status()
        if isinstance(security_status, dict):
            threat_level = security_status.get('threat_level', 'unknown')
            recent_alerts = security_status.get('recent_alerts', [])
        else:
            threat_level = getattr(security_status, 'threat_level', 'unknown')
            recent_alerts = getattr(security_status, 'recent_alerts', [])
            
        print(f"   🛡️  Threat Level: {threat_level}")
        
        if isinstance(recent_alerts, list) and recent_alerts:
            print("   ⚠️  Security Alerts:")
            for i, alert in enumerate(recent_alerts[:3], 1):  # Show top 3
                if isinstance(alert, dict):
                    alert_type = alert.get('type', 'unknown')
                    severity = alert.get('severity', 'unknown')
                    description = alert.get('description', 'no description')
                else:
                    alert_type = getattr(alert, 'type', 'unknown')
                    severity = getattr(alert, 'severity', 'unknown')
                    description = getattr(alert, 'description', 'no description')
                    
                print(f"      {i}. [{severity.upper()}] {alert_type}: {description}")
        elif isinstance(recent_alerts, list) and not recent_alerts:
            print("   ✅ No security alerts found")
        else:
            print("   ⚠️  Error determining security alerts")
            
        # Deactivate monitoring
        security_monitor.deactivate_monitoring()
        print("   ✅ Security monitoring deactivated")
        
    except Exception as e:
        print(f"   ⚠️  Error during security audit: {e}")
    
    # Task 4 - Collaboration check
    print("\n6. 🤝 Task 4 - Collaboration Check")
    try:
        # Check collaboration status
        collaboration_status = framework.collaboration.get_collaboration_status()
        print("   ✅ Collaboration status check completed")
        
        if isinstance(collaboration_status, dict):
            active_partnerships = collaboration_status.get('active_partnerships', 0)
            pending_requests = collaboration_status.get('pending_requests', [])
        else:
            active_partnerships = getattr(collaboration_status, 'active_partnerships', 0)
            pending_requests = getattr(collaboration_status, 'pending_requests', [])
            
        print(f"   🤝 Active Partnerships: {active_partnerships}")
        
        if isinstance(pending_requests, list) and pending_requests:
            print("   ⚠️  Pending Collaboration Requests:")
            for i, request in enumerate(pending_requests[:3], 1):  # Show top 3
                if isinstance(request, dict):
                    request_type = request.get('type', 'unknown')
                    sender = request.get('sender', 'unknown')
                    description = request.get('description', 'no description')
                else:
                    request_type = getattr(request, 'type', 'unknown')
                    sender = getattr(request, 'sender', 'unknown')
                    description = getattr(request, 'description', 'no description')
                    
                print(f"      {i}. [{request_type.upper()}] From {sender}: {description}")
        elif isinstance(pending_requests, list) and not pending_requests:
            print("   ✅ No pending collaboration requests")
        else:
            print("   ⚠️  Error determining pending requests")
            
        # If there are partnerships, check their status
        if active_partnerships > 0:
            print("   🔍 Checking partnership health...")
            partnership_health = framework.collaboration.get_partnership_health()
            if isinstance(partnership_health, dict):
                health_score = partnership_health.get('health_score', 0.0)
                trust_levels = partnership_health.get('trust_levels', {})
            else:
                health_score = getattr(partnership_health, 'health_score', 0.0)
                trust_levels = getattr(partnership_health, 'trust_levels', {})
                
            print(f"   📊 Partnership Health Score: {health_score:.2f}")
            
            if isinstance(trust_levels, dict) and trust_levels:
                print("   🤝 Trust Levels by Partner:")
                for partner, trust_level in list(trust_levels.items())[:3]:  # Show top 3
                    print(f"      • {partner}: {trust_level:.2f}")
            elif isinstance(trust_levels, dict) and not trust_levels:
                print("   🤝 No trust levels available")
            else:
                print("   🤝 Unable to determine trust levels")
        else:
            print("   📋 No active partnerships to check")
            
    except Exception as e:
        print(f"   ⚠️  Error during collaboration check: {e}")
    
    # Task 5 - Self-awareness check
    print("\n7. 🧠 Task 5 - Self-Awareness Check")
    try:
        # Run self-awareness evaluation
        self_awareness_results = await framework.meta_cognitive.evaluate("self")
        print("   ✅ Self-awareness evaluation completed")
        
        if isinstance(self_awareness_results, dict):
            quality_score = self_awareness_results.get('quality_score', 0.0)
            confidence_level = self_awareness_results.get('confidence_level', 'low')
            bias_detected = self_awareness_results.get('bias_detected', False)
        else:
            quality_score = getattr(self_awareness_results, 'quality_score', 0.0)
            confidence_level = getattr(self_awareness_results, 'confidence_level', 'low')
            bias_detected = getattr(self_awareness_results, 'bias_detected', False)
            
        print(f"   🧠 Quality Score: {quality_score:.2f}")
        print(f"   🎯 Confidence Level: {confidence_level}")
        print(f"   🤔 Bias Detected: {bias_detected}")
        
        # If bias is detected, suggest mitigation
        if bias_detected:
            print("   ⚠️  Bias detected, suggesting mitigation strategies...")
            bias_mitigation = framework.get_bias_mitigation_strategies()
            if isinstance(bias_mitigation, list) and bias_mitigation:
                print("   💡 Bias Mitigation Strategies:")
                for i, strategy in enumerate(bias_mitigation[:3], 1):  # Show top 3
                    print(f"      {i}. {strategy}")
            elif isinstance(bias_mitigation, list) and not bias_mitigation:
                print("   📋 No specific bias mitigation strategies available")
            else:
                print("   ⚠️  Error retrieving bias mitigation strategies")
        else:
            print("   ✅ No bias detected in self-awareness")
            
    except Exception as e:
        print(f"   ⚠️  Error during self-awareness check: {e}")
    
    # End of day - Generate daily report
    print("\n8. 📋 End of Day - Generating Daily Report")
    try:
        # Generate a comprehensive daily report
        daily_report = framework.generate_daily_report()
        print("   ✅ Daily report generated")
        
        if isinstance(daily_report, dict):
            tasks_completed = daily_report.get('tasks_completed', 0)
            issues_found = daily_report.get('issues_found', 0)
            recommendations = daily_report.get('recommendations', [])
        else:
            tasks_completed = getattr(daily_report, 'tasks_completed', 0)
            issues_found = getattr(daily_report, 'issues_found', 0)
            recommendations = getattr(daily_report, 'recommendations', [])
            
        print(f"   📊 Tasks Completed: {tasks_completed}")
        print(f"   ⚠️  Issues Found: {issues_found}")
        
        if isinstance(recommendations, list) and recommendations:
            print("   💡 Daily Recommendations:")
            for i, recommendation in enumerate(recommendations[:3], 1):  # Show top 3
                print(f"      {i}. {recommendation}")
        elif isinstance(recommendations, list) and not recommendations:
            print("   📋 No specific daily recommendations")
        else:
            print("   ⚠️  Error retrieving daily recommendations")
            
        # Save report to file
        report_file = "daily_report.md"
        with open(report_file, 'w') as f:
            f.write("# 📅 Daily Development Report\n\n")
            f.write(f"## 📊 Summary\n\n")
            f.write(f"- Tasks Completed: {tasks_completed}\n")
            f.write(f"- Issues Found: {issues_found}\n")
            f.write(f"- Quality Score: {quality_score:.2f}\n")
            f.write(f"- Performance Score: {overall_score:.2f}\n")
            f.write(f"- Health Score: {health_score:.2f}\n\n")
            
            if isinstance(recommendations, list) and recommendations:
                f.write("## 💡 Recommendations\n\n")
                for recommendation in recommendations[:5]:  # Show top 5
                    f.write(f"- {recommendation}\n")
                    
        print(f"   📄 Report saved to: {report_file}")
        
    except Exception as e:
        print(f"   ⚠️  Error during daily report generation: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The daily development workflow example demonstrates how the Semantic Self-Aware Kit")
    print("can be used for routine development activities:")
    print("")
    print("🌅 Morning Routine: System health check and preparation")
    print("📝 Code Review: Automated code analysis and issue detection")
    print("⚡ Performance Optimization: Benchmarking and optimization suggestions")
    print("🛡️ Security Audit: Threat detection and security monitoring")
    print("🤝 Collaboration Check: Partnership status and request management")
    print("🧠 Self-Awareness Check: Meta-cognitive evaluation and bias detection")
    print("📋 End of Day: Comprehensive reporting and recommendations")
    print("")
    print("This structured approach ensures consistent, thorough development practices")
    print("while leveraging AI capabilities for automation and intelligence.")

async def main():
    await demonstrate_daily_development()
    print("\n✅ Daily development workflow demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main())