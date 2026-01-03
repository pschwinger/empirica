#!/usr/bin/env python3
"""
Epistemic Documentation Assessment Agent - docs-assess command

Applies epistemic principles to documentation coverage:
1. CLI Coverage - Which commands are documented?
2. Core Module Coverage - Which modules have docs?
3. Feature Discovery - What features exist vs documented?
4. Staleness Detection - Are docs up to date with code?

Philosophy:
- "Know what you know" - Measure actual documentation coverage
- "Know what you don't know" - Reveal undocumented features
- "Honest uncertainty" - Report coverage gaps with precision

Usage:
    empirica docs-assess                     # Full documentation assessment
    empirica docs-assess --output json       # JSON output for automation
    empirica docs-assess --verbose           # Show all details
"""

import ast
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..cli_utils import handle_cli_error


@dataclass
class FeatureCoverage:
    """Tracks coverage for a feature category."""
    name: str
    total: int
    documented: int
    undocumented: list[str] = field(default_factory=list)

    @property
    def coverage(self) -> float:
        return self.documented / self.total if self.total > 0 else 0.0

    @property
    def moon(self) -> str:
        """Convert coverage to moon phase."""
        if self.coverage >= 0.85:
            return "🌕"
        elif self.coverage >= 0.70:
            return "🌔"
        elif self.coverage >= 0.50:
            return "🌓"
        elif self.coverage >= 0.30:
            return "🌒"
        else:
            return "🌑"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "total": self.total,
            "documented": self.documented,
            "coverage": round(self.coverage * 100, 1),
            "moon": self.moon,
            "undocumented": self.undocumented[:10]  # Top 10
        }


class EpistemicDocsAgent:
    """
    Epistemic Documentation Assessment Agent.

    Measures documentation coverage against actual codebase features.
    Returns honest epistemic assessment of what's documented vs hidden.
    """

    def __init__(self, project_root: Path | None = None, verbose: bool = False):
        self.root = project_root or Path.cwd()
        self.verbose = verbose
        self.categories: list[FeatureCoverage] = []

    def _load_all_docs_content(self) -> str:
        """Load all documentation content for searching."""
        docs_dir = self.root / "docs"
        readme = self.root / "README.md"

        content = ""

        # Load README
        if readme.exists():
            content += readme.read_text()

        # Load all non-archived docs
        if docs_dir.exists():
            for md_file in docs_dir.rglob("*.md"):
                if "_archive" not in str(md_file):
                    try:
                        content += "\n" + md_file.read_text()
                    except Exception:
                        pass

        return content.lower()

    def _extract_cli_commands(self) -> list[str]:
        """Extract all CLI commands from cli_core.py."""
        cli_core = self.root / "empirica" / "cli" / "cli_core.py"
        commands = []

        if not cli_core.exists():
            return commands

        content = cli_core.read_text()

        # Find COMMAND_HANDLERS dictionary entries
        # Pattern: 'command-name': handler_function (single quotes)
        pattern = r"'([a-z]+-?[a-z-]*)'\s*:\s*\w+"
        matches = re.findall(pattern, content)
        commands.extend(matches)

        # Also find add_parser calls with either quote style
        parser_pattern = r"add_parser\(\s*['\"]([a-z]+-?[a-z-]*)['\"]"
        parser_matches = re.findall(parser_pattern, content)
        commands.extend(parser_matches)

        return list(set(commands))

    def _extract_core_modules(self) -> list[str]:
        """Extract key classes/modules from core/."""
        core_dir = self.root / "empirica" / "core"
        modules = []

        if not core_dir.exists():
            return modules

        # Key module patterns to look for
        for py_file in core_dir.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            try:
                content = py_file.read_text()
                # Find class definitions
                class_pattern = r"^class\s+(\w+)\s*[\(:]"
                matches = re.findall(class_pattern, content, re.MULTILINE)
                for match in matches:
                    # Filter out internal/private classes
                    if not match.startswith("_") and len(match) > 3:
                        modules.append(match)
            except Exception:
                pass

        return list(set(modules))

    def _check_if_documented(self, term: str, docs_content: str) -> bool:
        """Check if a term appears in documentation."""
        # Normalize the term for searching
        normalized = term.lower().replace("-", " ").replace("_", " ")

        # Check various forms
        return (
            term.lower() in docs_content or
            normalized in docs_content or
            term.replace("-", "_").lower() in docs_content or
            # For camelCase classes, check word boundaries
            re.search(r'\b' + term.lower() + r'\b', docs_content) is not None
        )

    def assess_cli_coverage(self, docs_content: str) -> FeatureCoverage:
        """Assess CLI command documentation coverage."""
        commands = self._extract_cli_commands()
        documented = []
        undocumented = []

        for cmd in commands:
            if self._check_if_documented(cmd, docs_content):
                documented.append(cmd)
            else:
                undocumented.append(cmd)

        return FeatureCoverage(
            name="CLI Commands",
            total=len(commands),
            documented=len(documented),
            undocumented=sorted(undocumented)
        )

    def assess_core_coverage(self, docs_content: str) -> FeatureCoverage:
        """Assess core module documentation coverage."""
        modules = self._extract_core_modules()
        documented = []
        undocumented = []

        # Key user-facing modules to prioritize
        priority_modules = [
            "SessionDatabase", "GitEnhancedReflexLogger", "Sentinel",
            "PersonaProfile", "PersonaManager", "EpistemicBus",
            "BayesianBeliefManager", "ContextLoadBalancer", "MemoryGapDetector",
            "MirrorDriftMonitor", "AIIdentity", "CheckpointSigner",
            "EpistemicAgentConfig", "EmergedPersona", "AutoIssueCaptureService",
            "CoherenceValidator", "CompletionTracker", "FindingsDeprecationEngine"
        ]

        # Focus on priority modules
        for module in priority_modules:
            if module in modules:
                if self._check_if_documented(module, docs_content):
                    documented.append(module)
                else:
                    undocumented.append(module)

        return FeatureCoverage(
            name="Core Modules",
            total=len(priority_modules),
            documented=len(documented),
            undocumented=undocumented
        )

    def assess_feature_categories(self, docs_content: str) -> list[FeatureCoverage]:
        """Assess coverage of major feature categories."""
        categories = {
            "Sentinel System": ["sentinel", "sentinel-orchestrate", "sentinel-status", "domain profile", "safety gate"],
            "Persona System": ["persona", "persona-list", "emerged persona", "persona registry"],
            "Identity/Signing": ["identity", "checkpoint sign", "ed25519", "cryptographic"],
            "Investigation Branching": ["investigate-create-branch", "turtle", "multi-branch", "branch merge"],
            "Issue Capture": ["issue-list", "issue-resolve", "auto-capture", "issue handoff"],
            "Architecture Assessment": ["assess-component", "assess-directory", "architecture health"],
            "Agent Spawning": ["agent-spawn", "agent-aggregate", "sub-agent"],
            "Bayesian Calibration": ["bayesian", "belief calibration", "calibration loop"],
            "Drift Detection": ["drift", "mirror drift", "check-drift"],
            "Context Load Balancing": ["context load", "token reduction", "context routing"]
        }

        results = []
        for category, terms in categories.items():
            found = sum(1 for term in terms if term.lower() in docs_content)
            coverage = FeatureCoverage(
                name=category,
                total=len(terms),
                documented=found,
                undocumented=[t for t in terms if t.lower() not in docs_content]
            )
            results.append(coverage)

        return results

    def run_assessment(self) -> dict[str, Any]:
        """Run full documentation assessment."""
        docs_content = self._load_all_docs_content()

        # Assess each category
        cli_coverage = self.assess_cli_coverage(docs_content)
        core_coverage = self.assess_core_coverage(docs_content)
        feature_categories = self.assess_feature_categories(docs_content)

        self.categories = [cli_coverage, core_coverage] + feature_categories

        # Calculate overall coverage
        total_items = sum(c.total for c in self.categories)
        documented_items = sum(c.documented for c in self.categories)
        overall_coverage = documented_items / total_items if total_items > 0 else 0.0

        # Generate epistemic assessment
        if overall_coverage >= 0.80:
            know = 0.85
            uncertainty = 0.15
            assessment = "Documentation is comprehensive"
        elif overall_coverage >= 0.60:
            know = 0.65
            uncertainty = 0.30
            assessment = "Documentation has notable gaps"
        elif overall_coverage >= 0.40:
            know = 0.45
            uncertainty = 0.50
            assessment = "Significant features undocumented"
        else:
            know = 0.25
            uncertainty = 0.70
            assessment = "Major documentation debt"

        return {
            "overall": {
                "coverage": round(overall_coverage * 100, 1),
                "total_features": total_items,
                "documented": documented_items,
                "moon": self._score_to_moon(overall_coverage)
            },
            "epistemic_assessment": {
                "know": know,
                "uncertainty": uncertainty,
                "assessment": assessment
            },
            "categories": [c.to_dict() for c in self.categories],
            "recommendations": self._generate_recommendations()
        }

    def _score_to_moon(self, score: float) -> str:
        """Convert 0-1 score to moon phase."""
        if score >= 0.85:
            return "🌕"
        elif score >= 0.70:
            return "🌔"
        elif score >= 0.50:
            return "🌓"
        elif score >= 0.30:
            return "🌒"
        else:
            return "🌑"

    def _generate_recommendations(self) -> list[str]:
        """Generate prioritized recommendations."""
        recommendations = []

        for category in self.categories:
            if category.coverage < 0.50 and category.undocumented:
                recommendations.append(
                    f"Document {category.name}: {', '.join(category.undocumented[:3])}"
                )

        return recommendations[:5]  # Top 5 recommendations


def handle_docs_assess(args) -> int:
    """Handle the docs-assess command."""
    try:
        project_root = Path(args.project_root) if args.project_root else None
        verbose = getattr(args, 'verbose', False)
        output_format = getattr(args, 'output', 'human')

        agent = EpistemicDocsAgent(project_root=project_root, verbose=verbose)
        result = agent.run_assessment()

        if output_format == 'json':
            print(json.dumps(result, indent=2))
        else:
            _print_human_output(result, agent.categories, verbose)

        return 0

    except Exception as e:
        return handle_cli_error(e, "docs-assess")


def _print_human_output(result: dict, categories: list[FeatureCoverage], verbose: bool):
    """Print human-readable output."""
    overall = result["overall"]
    epistemic = result["epistemic_assessment"]

    print("\n" + "=" * 60)
    print("📚 EPISTEMIC DOCUMENTATION ASSESSMENT")
    print("=" * 60)

    # Overall score
    print(f"\n{overall['moon']} Overall Coverage: {overall['coverage']}%")
    print(f"   Features: {overall['documented']}/{overall['total_features']} documented")

    # Epistemic assessment
    print(f"\n📊 Epistemic Assessment:")
    print(f"   know: {epistemic['know']:.2f}")
    print(f"   uncertainty: {epistemic['uncertainty']:.2f}")
    print(f"   → {epistemic['assessment']}")

    # Category breakdown
    print("\n📋 Category Coverage:")
    print("-" * 50)

    for cat in categories:
        status = "✅" if cat.coverage >= 0.70 else "⚠️" if cat.coverage >= 0.40 else "❌"
        print(f"   {cat.moon} {cat.name}: {cat.coverage*100:.0f}% ({cat.documented}/{cat.total})")

        if verbose and cat.undocumented:
            for item in cat.undocumented[:5]:
                print(f"      └─ Missing: {item}")

    # Recommendations
    if result["recommendations"]:
        print("\n💡 Recommendations:")
        for rec in result["recommendations"]:
            print(f"   • {rec}")

    print("\n" + "=" * 60)
