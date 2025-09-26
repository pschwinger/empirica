#!/usr/bin/env python3
"""
Simple CLI example of using the Semantic Self-Aware Kit
"""

import subprocess
import sys
import os

def run_cli_command(command):
    """
    Run a CLI command and return the output
    """
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result = subprocess.run(
            command, 
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

def simple_cli_example():
    """
    Simple example of using the Semantic Self-Aware Kit CLI
    """
    print("⌨️  Simple CLI Example with Semantic Self-Aware Kit")
    print("=" * 50)
    
    # Ensure we're in the right directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_bin = os.path.join(project_dir, ".venv", "bin")
    
    # Test basic CLI commands
    commands = [
        ("self-test", "🧠 Testing self-awareness capabilities"),
        ("list-components", "🧩 Listing available components"),
        ("suggest", "💡 Getting intelligent suggestions"),
        ("cascade \"Should we refactor this module?\"", "🤔 Running metacognitive cascade"),
        ("investigate .", "🔍 Investigating codebase"),
        ("benchmark", "📊 Running performance benchmarks")
    ]
    
    for cmd, description in commands:
        print(f"\n{description}...")
        
        # Construct full command with venv path
        full_cmd = f"{os.path.join(venv_bin, 'semantic-kit')} {cmd}"
        
        stdout, stderr, returncode = run_cli_command(full_cmd)
        
        if returncode == 0:
            print("   ✅ Command executed successfully")
            # Show first few lines of output
            output_lines = stdout.strip().split('\n')
            for line in output_lines[:10]:  # Show first 10 lines
                if line.strip():
                    print(f"      {line}")
            if len(output_lines) > 10:
                print(f"      ... ({len(output_lines) - 10} more lines)")
        else:
            print(f"   ⚠️  Command failed with return code {returncode}")
            if stderr:
                print(f"      Error: {stderr}")
    
    # Summary
    print("\n📋 Summary")
    print("---------")
    print("The Semantic Self-Aware Kit CLI provides an intuitive interface for:")
    print("")
    print("🧠 Self-Awareness Testing: Validate AI self-awareness capabilities")
    print("🧩 Component Discovery: List and explore available components")
    print("💡 Intelligent Suggestions: Get context-aware recommendations")
    print("🤔 Decision Analysis: Run metacognitive cascades on decisions")
    print("🔍 Code Investigation: Deep analysis of codebases")
    print("📊 Performance Benchmarking: Measure framework performance")
    print("")
    print("The CLI is designed as an intelligent co-pilot, making it the ideal")
    print("interface for both human developers and AI systems to interact with")
    print("the framework.")

def main():
    simple_cli_example()
    print("\n✅ Simple CLI example completed!")

if __name__ == "__main__":
    main()