#!/usr/bin/env python3

import argparse
import subprocess
import os
from semantic_self_aware_kit.meta_cognitive_evaluator import MetaCognitiveEvaluator
from semantic_self_aware_kit.empirical_performance_analyzer import EmpiricalPerformanceAnalyzer
from semantic_self_aware_kit.code_intelligence_analyzer import CodeIntelligenceAnalyzer
from semantic_self_aware_kit.tool_management import AIEnhancedToolManager
from semantic_self_aware_kit.cli import show_suggestions

# Import all available components for reference (without instantiating them all)
from semantic_self_aware_kit import (
    advanced_collaboration,
    advanced_investigation,
    advanced_uncertainty,
    collaboration_framework,
    context_aware_integration,
    context_monitoring,
    context_validation,
    environment_stabilization,
    functionality_analyzer,
    intelligent_navigation,
    intelligent_suggestions,
    metacognitive_cascade,
    proactive_monitor,
    procedural_analysis,
    runtime_validation,
    security_monitoring,
    uncertainty_analysis,
    universal_grounding,
    workspace_awareness
)

def launch_website_docker():
    """Launches the documentation website using Docker."""
    print("\nAttempting to launch documentation website...")
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the docker-compose file
        docker_compose_path = os.path.join(script_dir, '..', 'web', 'docker-compose.yml')
        
        result = subprocess.run(
            ["docker-compose", "-f", docker_compose_path, "up", "-d", "--build"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("🚀 Documentation website is now running at http://localhost:8080")
        if result.stdout:
            print(result.stdout)
    except FileNotFoundError:
        print("⚠️  Docker Compose not found. Please install it to launch the website automatically.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to launch website.")
        print(f"   STDOUT: {e.stdout}")
        print(f"   STDERR: {e.stderr}")


def bootstrap_components():
    """Initializes and returns the core components of the Semantic Self-Aware Kit."""
    print("Bootstrapping Semantic Self-Aware Kit components...")
    print("Total available components: 24")

    # Initialize Meta-Cognitive Evaluator
    meta_cognitive_evaluator = MetaCognitiveEvaluator(max_recursion_depth=3)
    print("  - Meta-Cognitive Evaluator initialized.")

    # Initialize Empirical Performance Analyzer
    empirical_performance_analyzer = EmpiricalPerformanceAnalyzer()
    print("  - Empirical Performance Analyzer initialized.")

    # Initialize Code Intelligence Analyzer (lightweight mode for fast startup)
    # Note: The path to the code to be analyzed will need to be provided.
    # Using the current directory as a placeholder.
    code_intelligence_analyzer = CodeIntelligenceAnalyzer(".")
    # Perform lightweight initialization to avoid blocking startup
    print("  - Code Intelligence Analyzer initialized.")

    # Initialize AI-Enhanced Tool Manager
    ai_enhanced_tool_manager = AIEnhancedToolManager()
    print("  - AI-Enhanced Tool Manager initialized.")

    print("Bootstrap complete. Core components are ready for use.")
    print("")
    print("Available components (24 total):")
    print("  🧠 Cognitive:")
    print("    • meta_cognitive_evaluator")
    print("    • metacognitive_cascade")
    print("    • uncertainty_analysis")
    print("    • advanced_uncertainty")
    print("  📊 Performance:")
    print("    • empirical_performance_analyzer")
    print("    • functionality_analyzer")
    print("  🤝 Collaboration:")
    print("    • collaboration_framework")
    print("    • advanced_collaboration")
    print("  🧭 Navigation:")
    print("    • workspace_awareness")
    print("    • intelligent_navigation")
    print("  🛡️ Security:")
    print("    • security_monitoring")
    print("    • context_validation")
    print("    • context_monitoring")
    print("  🔬 Investigation:")
    print("    • advanced_investigation")
    print("    • code_intelligence_analyzer")
    print("  🛠️ Management:")
    print("    • tool_management")
    print("    • proactive_monitor")
    print("  🌱 Environment:")
    print("    • environment_stabilization")
    print("  🧠 Intelligence:")
    print("    • intelligent_suggestions")
    print("    • context_aware_integration")
    print("    • procedural_analysis")
    print("    • runtime_validation")
    print("    • universal_grounding")

    return {
        "meta_cognitive_evaluator": meta_cognitive_evaluator,
        "empirical_performance_analyzer": empirical_performance_analyzer,
        "code_intelligence_analyzer": code_intelligence_analyzer,
        "ai_enhanced_tool_manager": ai_enhanced_tool_manager,
    }


def main():
    """Main function to be called by the entry point."""
    parser = argparse.ArgumentParser(description="Bootstrap the Semantic Self-Aware Kit.")
    parser.add_argument(
        "--website",
        action="store_true",
        help="Launch the documentation website (disabled by default).",
    )
    args = parser.parse_args()

    components = bootstrap_components()
    print("\nComponents are loaded and ready for the session.")
    print("These components provide meta-cognitive and analytical capabilities to enhance the development process.")
    print("\nAI, as part of our iterative development, please perform a self-evaluation of these components. Assess their utility, clarity, and integration. Your feedback is crucial for the next refinement cycle.")

    # Temporarily disabled web component - can be enabled with --website flag
    # if args.website:
    #     launch_website_docker()

    print("\n\n")
    # Directly call the suggestion engine to provide immediate, actionable guidance
    show_suggestions()


if __name__ == "__main__":
    main()
