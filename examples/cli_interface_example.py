#!/usr/bin/env python3
"""
CLI Interface Example - The Best Way to Use the Semantic Self-Aware Kit
"""

import subprocess
import sys
import os

def run_semantic_kit_command(command):
    """
    Run a semantic-kit command and return the output
    """
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        venv_bin = os.path.join(project_dir, ".venv", "bin")
        
        # Construct full command with venv path
        full_cmd = f"{os.path.join(venv_bin, 'semantic-kit')} {command}"
        
        result = subprocess.run(
            full_cmd, 
            cwd=project_dir,
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=30  # 30 second timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1

def demonstrate_cli_interface():
    """
    Demonstrate why the CLI interface is the best way to use the Semantic Self-Aware Kit
    """
    print("⌨️  CLI Interface - The Best Way to Use the Semantic Self-Aware Kit")
    print("=" * 65)
    
    # Introduction
    print("\n🧠 Why the CLI Interface is Optimal")
    print("---------------------------------")
    print("The `semantic-kit` CLI provides the most intuitive and effective way to")
    print("interact with the Semantic Self-Aware Kit for both human developers and")
    print("AI systems. It serves as an intelligent co-pilot that:")
    print("")
    print("✅ Provides immediate access to all framework capabilities")
    print("✅ Offers context-aware, prioritized recommendations")
    print("✅ Enables seamless AI-to-AI and AI-to-Human collaboration")
    print("✅ Delivers comprehensive self-assessment and benchmarking")
    print("✅ Facilitates deep code analysis and investigation")
    print("✅ Supports empirical validation and uncertainty quantification")
    print("✅ Ensures security monitoring and environment validation")
    print("")
    print("Designed as a conversational interface, the CLI makes complex AI")
    print("capabilities accessible through simple, semantic commands.")
    
    # Essential CLI Commands
    print("\n🚀 Essential CLI Commands")
    print("------------------------")
    
    commands = [
        ("suggest", "Intelligent suggestions based on current context", "💡"),
        ("self-test", "Test AI self-awareness capabilities", "🧠"),
        ("cascade \"<decision>\"", "Run metacognitive cascade on a decision", "🤔"),
        ("investigate <path>", "Deep investigation of code or files", "🔍"),
        ("benchmark", "Run comprehensive performance benchmarks", "📊"),
        ("list-components", "List all available components", "🧩"),
        ("demo", "Demonstrate framework capabilities", "🎪"),
        ("test-all", "Test all components systematically", "🧪"),
        ("monitor", "Activate security monitoring", "🛡️"),
        ("navigate <path>", "Intelligent workspace navigation", "🧭"),
        ("procedural <function> --file <path>", "Analyze procedural tasks", "⚙️"),
        ("awareness", "Check workspace awareness status", "👁️"),
        ("uncertainty \"<decision>\"", "Analyze uncertainty for decisions", "🤷"),
        ("collaborate", "Test collaboration framework", "🤝")
    ]
    
    for cmd, description, emoji in commands:
        print(f"   {emoji} `semantic-kit {cmd}` - {description}")
    
    # Interactive Demo
    print("\n🎯 Interactive CLI Demonstration")
    print("------------------------------")
    
    # 1. Get intelligent suggestions
    print("\n1. Getting intelligent suggestions...")
    stdout, stderr, returncode = run_semantic_kit_command("suggest")
    if returncode == 0:
        print("   ✅ Suggestions retrieved successfully")
        # Show first few lines of output
        output_lines = stdout.strip().split('\n')
        for line in output_lines[:5]:  # Show first 5 lines
            if line.strip() and not line.startswith("🔍") and not line.startswith("🤔") and not line.startswith("🧭"):
                print(f"      {line}")
    else:
        print(f"   ⚠️  Error retrieving suggestions: {stderr}")
    
    # 2. Self-test
    print("\n2. Running self-awareness test...")
    stdout, stderr, returncode = run_semantic_kit_command("self-test")
    if returncode == 0:
        print("   ✅ Self-awareness test completed")
        # Show key results
        output_lines = stdout.strip().split('\n')
        for line in output_lines:
            if "Self-awareness test complete" in line or "Meta-cognitive evaluator instantiated" in line:
                print(f"      {line}")
    else:
        print(f"   ⚠️  Error during self-test: {stderr}")
    
    # 3. List components
    print("\n3. Listing available components...")
    stdout, stderr, returncode = run_semantic_kit_command("list-components")
    if returncode == 0:
        print("   ✅ Components listed successfully")
        # Show component count
        output_lines = stdout.strip().split('\n')
        for line in output_lines:
            if "Total Components" in line:
                print(f"      {line}")
    else:
        print(f"   ⚠️  Error listing components: {stderr}")
    
    # 4. Run metacognitive cascade
    print("\n4. Running metacognitive cascade...")
    stdout, stderr, returncode = run_semantic_kit_command("cascade \"Should we refactor this module?\"")
    if returncode == 0:
        print("   ✅ Metacognitive cascade completed")
        # Show key results
        output_lines = stdout.strip().split('\n')
        for line in output_lines:
            if "Confidence Level" in line or "Required Actions" in line:
                print(f"      {line}")
    else:
        print(f"   ⚠️  Error during metacognitive cascade: {stderr}")
    
    # 5. Demonstrate framework capabilities
    print("\n5. Demonstrating framework capabilities...")
    stdout, stderr, returncode = run_semantic_kit_command("demo")
    if returncode == 0:
        print("   ✅ Framework demonstration completed")
        # Show key results
        output_lines = stdout.strip().split('\n')
        for line in output_lines:
            if "Framework demonstration complete" in line or "Self-awareness test complete" in line:
                print(f"      {line}")
    else:
        print(f"   ⚠️  Error during framework demonstration: {stderr}")
    
    # Best Practices for CLI Usage
    print("\n📋 Best Practices for CLI Usage")
    print("------------------------------")
    print("To get the most out of the Semantic Self-Aware Kit CLI:")
    print("")
    print("1. 🧠 Start with `semantic-kit suggest` to get context-aware recommendations")
    print("2. 🧪 Use `semantic-kit self-test` regularly to validate self-awareness")
    print("3. 🤔 Run `semantic-kit cascade` on important decisions for meta-cognitive analysis")
    print("4. 🔍 Employ `semantic-kit investigate` for deep code analysis")
    print("5. 📊 Execute `semantic-kit benchmark` to measure performance")
    print("6. 🧩 Try `semantic-kit list-components` to explore available capabilities")
    print("7. 🎪 Run `semantic-kit demo` to see the framework in action")
    print("8. 🧪 Use `semantic-kit test-all` to verify component functionality")
    print("9. 🛡️ Activate `semantic-kit monitor` for security monitoring")
    print("10. 🤝 Test collaboration with `semantic-kit collaborate`")
    print("")
    print("For AI systems, the CLI provides a natural language interface that")
    print("makes framework capabilities immediately accessible and usable.")
    
    # For AI Developers
    print("\n🤖 For AI Developers")
    print("-------------------")
    print("The CLI interface is specifically designed for AI systems to:")
    print("")
    print("🧠 Understand Component Functionality: Semantic naming immediately conveys purpose")
    print("🤝 Enable Collaboration: Natural language commands facilitate AI-to-AI interaction")
    print("🔍 Provide Context-Aware Guidance: Suggestions adapt to current workspace state")
    print("📊 Offer Empirical Validation: Performance benchmarks provide objective metrics")
    print("🤔 Support Uncertainty Quantification: Metacognitive cascades assess decision confidence")
    print("🛡️ Ensure Security: Monitoring capabilities detect and respond to threats")
    print("🌱 Maintain Stability: Environment validation ensures consistent operation")
    print("🛠️ Manage Tools: Intelligent discovery and recommendation of relevant tools")
    print("")
    print("This makes the CLI the optimal interface for AI systems to leverage the")
    print("full capabilities of the Semantic Self-Aware Kit without complex API integration.")
    
    # Summary
    print("\n🏁 Summary")
    print("---------")
    print("The `semantic-kit` CLI is the best way to use the Semantic Self-Aware Kit because:")
    print("")
    print("✅ It's intuitive and immediately understandable")
    print("✅ It provides comprehensive access to all 23 components")
    print("✅ It enables both human and AI interaction")
    print("✅ It offers intelligent, context-aware guidance")
    print("✅ It supports empirical validation and uncertainty quantification")
    print("✅ It facilitates collaboration and security monitoring")
    print("✅ It's designed as an intelligent co-pilot interface")
    print("")
    print("Whether you're a human developer or an AI system, the CLI provides the")
    print("most effective pathway to harness the power of the Semantic Self-Aware Kit.")

def main():
    demonstrate_cli_interface()
    print("\n✅ CLI interface demonstration completed!")

if __name__ == "__main__":
    main()