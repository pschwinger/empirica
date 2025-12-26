"""
Edit Verification Command - Metacognitive Edit Guard for Reliable File Modifications

Implements the Empirica Edit Guard system as a CLI command.
Prevents 80% of AI edit failures by assessing epistemic confidence BEFORE attempting edits.
"""

import json
import logging
from pathlib import Path

from ..cli_utils import handle_cli_error, parse_json_safely

logger = logging.getLogger(__name__)


def handle_edit_with_confidence_command(args):
    """Handle edit-with-confidence command - Assess confidence before editing"""
    try:
        from empirica.components.edit_verification.confidence_assessor import EditConfidenceAssessor
        from empirica.components.edit_verification.strategy_executor import EditStrategyExecutor

        # Parse arguments
        file_path = args.file_path
        old_str = args.old_str
        new_str = args.new_str
        context_source = getattr(args, 'context_source', 'memory')
        output_format = getattr(args, 'output', 'json')

        # Validate required arguments
        if not file_path or old_str is None or new_str is None:
            result = {
                "ok": False,
                "error": "Missing required arguments: --file-path, --old-str, --new-str",
                "received": {
                    "file_path": bool(file_path),
                    "old_str": old_str is not None,
                    "new_str": new_str is not None
                }
            }
            if output_format == 'json':
                print(json.dumps(result, indent=2))
            else:
                print(f"❌ Missing required arguments")
            return None

        # Validate file exists
        if not Path(file_path).exists():
            result = {
                "ok": False,
                "error": f"File does not exist: {file_path}"
            }
            if output_format == 'json':
                print(json.dumps(result, indent=2))
            else:
                print(f"❌ File does not exist: {file_path}")
            return None

        # Initialize components
        assessor = EditConfidenceAssessor()
        executor = EditStrategyExecutor()

        # Assess epistemic confidence
        assessment = assessor.assess(
            file_path=file_path,
            old_str=old_str,
            context_source=context_source
        )

        # Get recommended strategy
        strategy, reasoning = assessor.recommend_strategy(assessment)

        # Execute with chosen strategy
        result = executor.execute_strategy(
            strategy=strategy,
            file_path=file_path,
            old_str=old_str,
            new_str=new_str,
            assessment=assessment
        )

        # Format output
        output_result = {
            "ok": result.get("success", False),
            "strategy": strategy,
            "reasoning": reasoning,
            "confidence": assessment["overall"],
            "result": result.get("message", ""),
            "changes_made": result.get("changes_made", False),
            "file_path": file_path,
            "assessment_details": {
                "context_freshness": assessment["context"],
                "whitespace_uncertainty": assessment["uncertainty"],
                "pattern_signal": assessment["signal"],
                "truncation_clarity": assessment["clarity"]
            }
        }

        if output_format == 'json':
            print(json.dumps(output_result, indent=2))
        else:
            status = "✅" if output_result["ok"] else "❌"
            print(f"{status} Edit operation: {output_result['result']}")
            print(f"   Strategy: {strategy} (confidence: {assessment['overall']:.2f})")
            print(f"   Changes: {'Yes' if output_result['changes_made'] else 'No'}")
            print(f"   File: {file_path}")

        return None  # Avoid duplicate output and exit code issues

    except Exception as e:
        handle_cli_error(e, "Edit with confidence", getattr(args, 'verbose', False))
        return None