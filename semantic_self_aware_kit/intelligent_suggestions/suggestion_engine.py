from typing import List, Dict, Any
import os

class SuggestionEngine:
    def __init__(self):
        self.suggestion_rules = [
            {
                "name": "Code Analysis for Recently Modified Python Files",
                "condition": self._has_recently_modified_python_files,
                "suggestions": [
                    {
                        "description": "Analyze recently modified Python file for insights.",
                        "cli_command_template": "semantic-kit analyze {file_path}",
                        "component": "Code Intelligence Analyzer",
                        "priority": 0.8 # High priority for recent work
                    },
                    {
                        "description": "Perform procedural analysis on a function in a recently modified Python file.",
                        "cli_command_template": "semantic-kit procedural <function_name> --file {file_path}",
                        "component": "Procedural Analysis",
                        "priority": 0.7
                    }
                ]
            },
            {
                "name": "Code Quality Improvement",
                "condition": self._has_low_code_health,
                "suggestions": [
                    {
                        "description": "Codebase health is low. Consider a comprehensive code analysis.",
                        "cli_command_template": "semantic-kit analyze {current_working_directory}",
                        "component": "Code Intelligence Analyzer",
                        "priority": 0.9
                    },
                    {
                        "description": "Focus on improving code quality and reducing complexity.",
                        "cli_command_template": "semantic-kit procedural <function_name> --file <path>", # Generic for now
                        "component": "Procedural Analysis",
                        "priority": 0.8
                    }
                ]
            },
            {
                "name": "Performance Optimization Opportunity",
                "condition": self._has_low_performance_score,
                "suggestions": [
                    {
                        "description": "Overall performance score is low. Run a comprehensive benchmark.",
                        "cli_command_template": "semantic-kit benchmark",
                        "component": "Empirical Performance Analyzer",
                        "priority": 0.95 # Very high priority for performance issues
                    },
                    {
                        "description": "Analyze system resource usage for bottlenecks.",
                        "cli_command_template": "semantic-kit monitor",
                        "component": "Security Monitoring", # Security Monitoring also has resource analysis
                        "priority": 0.85
                    }
                ]
            },
            {
                "name": "Uncertainty Reduction",
                "condition": self._has_high_uncertainty,
                "suggestions": [
                    {
                        "description": "High overall uncertainty detected. Investigate the current task.",
                        "cli_command_template": "semantic-kit uncertainty \"current_task\"",
                        "component": "Uncertainty Analysis",
                        "priority": 0.9
                    },
                    {
                        "description": "Perform a deep investigation to reduce uncertainty.",
                        "cli_command_template": "semantic-kit investigate {current_working_directory}",
                        "component": "Advanced Investigation Engine",
                        "priority": 0.8
                    }
                ]
            },
            {
                "name": "Meta-Cognitive Self-Improvement",
                "condition": self._has_low_meta_cognition_quality,
                "suggestions": [
                    {
                        "description": "Meta-cognitive evaluation quality is low. Run a self-test.",
                        "cli_command_template": "semantic-kit self-test",
                        "component": "Meta-Cognitive Evaluator",
                        "priority": 0.75
                    },
                    {
                        "description": "Analyze and improve the AI's self-awareness and reasoning processes.",
                        "cli_command_template": "semantic-kit awareness",
                        "component": "Workspace Awareness", # Workspace Awareness can also trigger meta-cognitive evaluation
                        "priority": 0.7
                    }
                ]
            },
            {
                "name": "General Workspace Overview",
                "condition": self._no_specific_recent_activity,
                "suggestions": [
                    {
                        "description": "Check the overall workspace awareness status.",
                        "cli_command_template": "semantic-kit awareness",
                        "component": "Workspace Awareness",
                        "priority": 0.5
                    },
                    {
                        "description": "Navigate and explore the current workspace.",
                        "cli_command_template": "semantic-kit navigate .",
                        "component": "Intelligent Navigation",
                        "priority": 0.4
                    }
                ]
            }
        ]

    def _has_recently_modified_python_files(self, context: Dict[str, Any]) -> bool:
        for file_info in context.get("recently_modified_files", []):
            if file_info["path"].endswith(".py"):
                return True
        return False

    def _no_specific_recent_activity(self, context: Dict[str, Any]) -> bool:
        # This rule acts as a fallback if no other specific conditions are met
        # It should be the lowest priority and only trigger if no other specific activity is found
        return not context.get("recently_modified_files") and \
               not self._has_low_code_health(context) and \
               not self._has_low_performance_score(context) and \
               not self._has_high_uncertainty(context) and \
               not self._has_low_meta_cognition_quality(context)

    def _has_low_code_health(self, context: Dict[str, Any]) -> bool:
        code_insights = context.get("sdk_component_insights", {}).get("code_intelligence", {})
        overall_health_score = code_insights.get("overall_health_score")
        # Assuming a score below 0.6 is considered low health
        return overall_health_score is not None and overall_health_score < 0.6

    def _has_low_performance_score(self, context: Dict[str, Any]) -> bool:
        perf_metrics = context.get("sdk_component_insights", {}).get("performance_metrics", {})
        overall_score = perf_metrics.get("overall_score")
        # Assuming a score below 0.5 is considered low performance
        return overall_score is not None and overall_score < 0.5

    def _has_high_uncertainty(self, context: Dict[str, Any]) -> bool:
        uncertainty_analysis = context.get("sdk_component_insights", {}).get("uncertainty_analysis", {})
        overall_uncertainty = uncertainty_analysis.get("overall_uncertainty")
        # Assuming a score above 0.7 is considered high uncertainty
        return overall_uncertainty is not None and overall_uncertainty > 0.7

    def _has_low_meta_cognition_quality(self, context: Dict[str, Any]) -> bool:
        meta_cognition = context.get("sdk_component_insights", {}).get("meta_cognition", {})
        overall_evaluation_quality = meta_cognition.get("overall_evaluation_quality")
        # Assuming a score below 0.7 is considered low quality
        return overall_evaluation_quality is not None and overall_evaluation_quality < 0.7

    def generate_suggestions(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        suggestions = []
        for rule in self.suggestion_rules:
            if rule["condition"](context):
                for suggestion_template in rule["suggestions"]:
                    cli_command = suggestion_template["cli_command_template"]
                    
                    # Fill in dynamic parts of the command if available
                    if "{file_path}" in cli_command:
                        for file_info in context.get("recently_modified_files", []):
                            if file_info["path"].endswith(".py"):
                                cli_command = cli_command.format(file_path=file_info["path"])
                                break
                    if "{current_working_directory}" in cli_command:
                        cli_command = cli_command.format(current_working_directory=context["current_working_directory"])
                    
                    suggestions.append({
                        "description": suggestion_template["description"],
                        "cli_command": cli_command,
                        "component": suggestion_template["component"],
                        "priority": suggestion_template.get("priority", 0.5) # Default priority
                    })
        
        # Sort suggestions by priority (descending)
        suggestions.sort(key=lambda s: s.get("priority", 0.5), reverse=True)
        
        return suggestions