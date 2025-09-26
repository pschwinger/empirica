#!/usr/bin/env python3
"""
Security Monitoring Example with the Semantic Self-Aware Kit
"""

import asyncio
from semantic_self_aware_kit.security_monitoring import activate_security_monitoring

async def demonstrate_security_monitoring():
    """
    Demonstrate security monitoring capabilities
    """
    print("🛡️ Security Monitoring with Semantic Self-Aware Kit")
    print("=" * 50)
    
    # Activate the security monitoring system
    print("\n1. Activating Security Monitoring...")
    try:
        security_monitor = activate_security_monitoring(monitoring_interval=5)  # 5 second interval for demo
        print("   ✅ Security Monitoring activated")
        
        # Display initial security status
        status = security_monitor.get_security_status()
        print("   📊 Initial Security Status:")
        
        if isinstance(status, dict):
            threat_level = status.get('threat_level', 'unknown')
            active_monitors = status.get('active_monitors', [])
            recent_alerts = status.get('recent_alerts', [])
        else:
            threat_level = getattr(status, 'threat_level', 'unknown')
            active_monitors = getattr(status, 'active_monitors', [])
            recent_alerts = getattr(status, 'recent_alerts', [])
            
        print(f"      Threat Level: {threat_level}")
        print(f"      Active Monitors: {len(active_monitors) if isinstance(active_monitors, list) else 'N/A'}")
        
        if recent_alerts:
            print(f"      Recent Alerts: {len(recent_alerts) if isinstance(recent_alerts, list) else 'N/A'}")
        else:
            print("      Recent Alerts: 0")
            
    except Exception as e:
        print(f"   ⚠️  Error activating security monitoring: {e}")
        return
    
    # Example 1: Monitor for threats during a code analysis operation
    print("\n2. Monitoring for security threats during code analysis...")
    try:
        # Simulate a code analysis operation that might trigger security alerts
        print("   🧠 Analyzing code for security vulnerabilities...")
        
        # Run monitoring for a few seconds to detect any threats
        await asyncio.sleep(10)  # Wait for monitoring to detect potential issues
        
        # Check for security threats
        threats = security_monitor.detect_threats()
        print("   ✅ Threat detection completed")
        
        if isinstance(threats, list) and threats:
            print(f"   ⚠️  {len(threats)} Security Threats Detected:")
            for i, threat in enumerate(threats[:5], 1):  # Show top 5
                if isinstance(threat, dict):
                    threat_type = threat.get('type', 'unknown')
                    severity = threat.get('severity', 'unknown')
                    description = threat.get('description', 'no description')
                else:
                    threat_type = getattr(threat, 'type', 'unknown')
                    severity = getattr(threat, 'severity', 'unknown')
                    description = getattr(threat, 'description', 'no description')
                    
                print(f"      {i}. [{severity.upper()}] {threat_type}: {description}")
        elif isinstance(threats, list) and not threats:
            print("   ✅ No security threats detected")
        else:
            print("   ⚠️  Unable to determine threat status")
            
    except Exception as e:
        print(f"   ⚠️  Error during threat detection: {e}")
    
    # Example 2: Analyze code for security vulnerabilities
    print("\n3. Analyzing code for security vulnerabilities...")
    try:
        # Example code to analyze
        sample_code = '''
import os
import subprocess

def dangerous_function(user_input):
    # This is intentionally vulnerable code for demonstration
    os.system(f"echo {user_input}")  # Command injection vulnerability
    subprocess.call(f"ls {user_input}", shell=True)  # Another vulnerability
    return "Processed"
        '''
        
        # Analyze the code for security issues
        analysis_results = security_monitor.analyze_code_security(sample_code)
        print("   ✅ Code security analysis completed")
        
        # Display analysis results
        if isinstance(analysis_results, dict):
            vulnerabilities = analysis_results.get('vulnerabilities', [])
            recommendations = analysis_results.get('recommendations', [])
        else:
            vulnerabilities = getattr(analysis_results, 'vulnerabilities', [])
            recommendations = getattr(analysis_results, 'recommendations', [])
            
        if vulnerabilities:
            print(f"   ⚠️  {len(vulnerabilities)} Security Vulnerabilities Found:")
            for i, vulnerability in enumerate(vulnerabilities[:5], 1):  # Show top 5
                if isinstance(vulnerability, dict):
                    vuln_type = vulnerability.get('type', 'unknown')
                    line_number = vulnerability.get('line', 'unknown')
                    description = vulnerability.get('description', 'no description')
                else:
                    vuln_type = getattr(vulnerability, 'type', 'unknown')
                    line_number = getattr(vulnerability, 'line', 'unknown')
                    description = getattr(vulnerability, 'description', 'no description')
                    
                print(f"      {i}. [{vuln_type}] Line {line_number}: {description}")
        else:
            print("   ✅ No security vulnerabilities found in the code")
            
        if recommendations:
            print("   💡 Security Recommendations:")
            for i, recommendation in enumerate(recommendations[:5], 1):  # Show top 5
                print(f"      {i}. {recommendation}")
                
    except Exception as e:
        print(f"   ⚠️  Error during code security analysis: {e}")
    
    # Example 3: Handle a security incident
    print("\n4. Handling a security incident...")
    try:
        # Simulate a security incident
        incident = {
            "type": "unauthorized_access",
            "severity": "high",
            "timestamp": "2025-09-21T22:30:00Z",
            "source": "network",
            "details": "Multiple failed login attempts from suspicious IP"
        }
        
        response = security_monitor.respond_to_incident(incident)
        print("   ✅ Incident response executed")
        
        if isinstance(response, dict):
            actions_taken = response.get('actions_taken', [])
            mitigation_status = response.get('mitigation_status', 'unknown')
        else:
            actions_taken = getattr(response, 'actions_taken', [])
            mitigation_status = getattr(response, 'mitigation_status', 'unknown')
            
        print(f"   🛡️  Mitigation Status: {mitigation_status}")
        
        if actions_taken:
            print("   🔧 Actions Taken:")
            for i, action in enumerate(actions_taken[:5], 1):  # Show top 5
                print(f"      {i}. {action}")
                
    except Exception as e:
        print(f"   ⚠️  Error during incident response: {e}")
    
    # Deactivate monitoring
    print("\n5. Deactivating security monitoring...")
    try:
        security_monitor.deactivate_monitoring()
        print("   ✅ Security monitoring deactivated")
    except Exception as e:
        print(f"   ⚠️  Error deactivating security monitoring: {e}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The Security Monitoring component provides comprehensive security capabilities including:")
    print("")
    print("🛡️  Threat Detection: Continuous monitoring for security threats and anomalies")
    print("🔍 Code Analysis: Deep inspection of code for vulnerabilities and compliance issues")
    print("⚡ Incident Response: Automated response to security incidents with mitigation strategies")
    print("📊 Security Reporting: Comprehensive reporting on security status and alerts")
    print("🔒 Protection Mechanisms: Built-in safeguards to prevent unauthorized access")
    print("")
    print("These capabilities help maintain system integrity and protect against potential security")
    print("vulnerabilities while ensuring compliance with security best practices.")

async def main():
    await demonstrate_security_monitoring()
    print("\n✅ Security monitoring demonstration completed!")

if __name__ == "__main__":
    asyncio.run(main())