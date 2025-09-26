import os
import time
import asyncio # Added import
from datetime import datetime, timedelta
import json # Added import for json.dumps in example usage

# Import other SDK components
from semantic_self_aware_kit.code_intelligence_analyzer import CodeIntelligenceAnalyzer
from semantic_self_aware_kit.empirical_performance_analyzer import EmpiricalPerformanceAnalyzer
from semantic_self_aware_kit.uncertainty_analysis import MultiDimensionalUncertaintyAnalyzer
from semantic_self_aware_kit.workspace_awareness import WorkspaceNavigator
from semantic_self_aware_kit.meta_cognitive_evaluator import MetaCognitiveEvaluator # Added for hybrid_evaluate

class ContextMonitor:
    def __init__(self, root_dir: str = None):
        self.root_dir = root_dir if root_dir else os.getcwd()

        # Initialize other SDK components
        self.code_analyzer = CodeIntelligenceAnalyzer(self.root_dir)
        self.perf_analyzer = EmpiricalPerformanceAnalyzer()
        self.uncertainty_analyzer = MultiDimensionalUncertaintyAnalyzer()
        self.workspace_navigator = WorkspaceNavigator()
        self.meta_evaluator = MetaCognitiveEvaluator() # Initialized for hybrid_evaluate

    def get_active_context(self, time_window_minutes: int = 5) -> dict:
        """
        Gathers comprehensive information about the current active context in the workspace.
        """
        context = {
            "timestamp": datetime.now().isoformat(),
            "current_working_directory": os.getcwd(),
            "recently_modified_files": self._get_recently_modified_files(time_window_minutes),
            "sdk_component_insights": {}
        }

        # Add insights from Code Intelligence Analyzer
        try:
            # Note: comprehensive_analysis can be time-consuming. Consider caching or running less frequently.
            code_analysis_summary = asyncio.run(self.code_analyzer.comprehensive_analysis())
            context["sdk_component_insights"]["code_intelligence"] = {
                "overall_health_score": code_analysis_summary.get("synthesis", {}).get("overall_health_score"),
                "total_lines_of_code": code_analysis_summary.get("archaeological_report", {}).get("statistics", {}).get("total_lines_of_code"),
                "key_recommendations": code_analysis_summary.get("synthesis", {}).get("key_recommendations")
            }
        except Exception as e:
            context["sdk_component_insights"]["code_intelligence"] = {"error": str(e)}

        # Add insights from Empirical Performance Analyzer
        try:
            # Note: comprehensive_benchmark can be time-consuming.
            perf_benchmark_summary = asyncio.run(self.perf_analyzer.comprehensive_benchmark("current_workspace"))
            context["sdk_component_insights"]["performance_metrics"] = {
                "overall_score": perf_benchmark_summary.get("executive_summary", {}).get("overall_score"),
                "avg_completion_time": perf_benchmark_summary.get("aggregated_metrics", {}).get("speed_metrics", {}).get("avg_completion_time")
            }
        except Exception as e:
            context["sdk_component_insights"]["performance_metrics"] = {"error": str(e)}

        # Add insights from Uncertainty Analysis
        try:
            # Note: investigate_uncertainty can be time-consuming.
            uncertainty_assessment = asyncio.run(self.uncertainty_analyzer.investigate_uncertainty("current_task", {"cli_context": True}))
            context["sdk_component_insights"]["uncertainty_analysis"] = {
                "overall_uncertainty": uncertainty_assessment.get("overall_uncertainty"),
                "uncertainty_level": uncertainty_assessment.get("uncertainty_level"),
                "recommendations": uncertainty_assessment.get("recommendations")
            }
        except Exception as e:
            context["sdk_component_insights"]["uncertainty_analysis"] = {"error": str(e)}

        # Add insights from Workspace Awareness
        try:
            workspace_intelligence = self.workspace_navigator.get_workspace_intelligence()
            context["sdk_component_insights"]["workspace_awareness"] = {
                "total_tasks": workspace_intelligence.get("total_tasks"),
                "tasks_by_status": workspace_intelligence.get("tasks_by_status")
            }
        except Exception as e:
            context["sdk_component_insights"]["workspace_awareness"] = {"error": str(e)}

        # Add insights from Meta-Cognitive Evaluator
        try:
            # Note: hybrid_evaluate can be time-consuming.
            meta_evaluation_results = asyncio.run(self.meta_evaluator.hybrid_evaluate("self"))
            context["sdk_component_insights"]["meta_cognition"] = {
                "overall_evaluation_quality": meta_evaluation_results.get("synthesis", {}).get("evaluation_quality"),
                "aspect_scores": meta_evaluation_results.get("synthesis", {}).get("aspect_scores")
            }
        except Exception as e:
            context["sdk_component_insights"]["meta_cognition"] = {"error": str(e)}

        return context

    def _get_recently_modified_files(self, time_window_minutes: int) -> list:
        """
        Finds files modified within the last 'time_window_minutes' in the root_dir.
        """
        modified_files = []
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)

        for dirpath, _, filenames in os.walk(self.root_dir):
            for f in filenames:
                filepath = os.path.join(dirpath, f)
                try:
                    # Get modification time as datetime object
                    mod_timestamp = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if mod_timestamp > cutoff_time:
                        # Make path relative to root_dir for cleaner context
                        relative_path = os.path.relpath(filepath, self.root_dir)
                        modified_files.append({
                            "path": relative_path,
                            "last_modified": mod_timestamp.isoformat()
                        })
                except OSError:
                    # Handle cases where file might be inaccessible or deleted
                    continue
        return modified_files

# Example usage (for testing purposes, not part of the class itself)
if __name__ == "__main__":
    monitor = ContextMonitor()
    context = monitor.get_active_context(time_window_minutes=10)
    print(json.dumps(context, indent=2))