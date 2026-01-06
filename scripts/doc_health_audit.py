#!/usr/bin/env python3
"""
Documentation Health Audit - Immune System for Docs

Applies confidence scoring and decay to documentation:
1. Code Reference Score - Do referenced classes/functions exist?
2. Staleness Score - How old is the doc vs code it documents?
3. Redundancy Score - Is this covered elsewhere?
4. Location Score - Is it in the right place?

Output: JSON report with confidence scores and decay recommendations.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any

# Directories
DOCS_DIR = Path("docs")
CODE_DIR = Path("empirica")
ARCHIVE_DIR = DOCS_DIR / "_archive"

# Scoring weights
WEIGHTS = {
    "code_reference": 0.40,  # Do referenced classes exist?
    "staleness": 0.25,       # How recently updated?
    "redundancy": 0.20,      # Is this unique content?
    "location": 0.15,        # Is it in the right place?
}

# Thresholds
DECAY_THRESHOLD = 0.5       # Below this, flag for decay
ARCHIVE_THRESHOLD = 0.3     # Below this, recommend archive
DELETE_THRESHOLD = 0.2      # Below this, recommend delete


def extract_code_references(content: str) -> Set[str]:
    """Extract class and function names referenced in doc."""
    references = set()

    # Class references: CamelCase words
    class_pattern = r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b'
    references.update(re.findall(class_pattern, content))

    # Function references in code blocks
    func_pattern = r'(?:def |\.|\s)([a-z_][a-z0-9_]*)\s*\('
    references.update(re.findall(func_pattern, content))

    # CLI commands: empirica command-name
    cli_pattern = r'empirica\s+([a-z][-a-z]+)'
    references.update(re.findall(cli_pattern, content))

    return references


def get_existing_classes() -> Set[str]:
    """Get all class names from codebase."""
    classes = set()

    for py_file in CODE_DIR.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        try:
            content = py_file.read_text()
            class_pattern = r'^class\s+(\w+)'
            classes.update(re.findall(class_pattern, content, re.MULTILINE))
        except Exception:
            pass

    return classes


def get_existing_functions() -> Set[str]:
    """Get public function names from codebase."""
    functions = set()

    for py_file in CODE_DIR.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        try:
            content = py_file.read_text()
            # Public functions (not starting with _)
            func_pattern = r'^def\s+([a-z][a-z0-9_]*)\s*\('
            functions.update(re.findall(func_pattern, content, re.MULTILINE))
        except Exception:
            pass

    return functions


def get_cli_commands() -> Set[str]:
    """Get CLI command names."""
    try:
        result = subprocess.run(
            ["empirica", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        # Extract command names from help output
        commands = set()
        for line in result.stdout.split('\n'):
            match = re.match(r'\s+([a-z][-a-z]+)\s', line)
            if match:
                commands.add(match.group(1))
        return commands
    except Exception:
        return set()


def calculate_code_reference_score(
    doc_refs: Set[str],
    existing_classes: Set[str],
    existing_functions: Set[str],
    cli_commands: Set[str]
) -> Tuple[float, List[str]]:
    """Calculate how many referenced items actually exist."""
    if not doc_refs:
        return 1.0, []  # No references = neutral

    existing = existing_classes | existing_functions | cli_commands
    found = doc_refs & existing
    missing = doc_refs - existing

    # Filter out common words that aren't actually code references
    false_positives = {
        'True', 'False', 'None', 'Note', 'Example', 'Usage',
        'Returns', 'Args', 'Optional', 'Default', 'Important'
    }
    missing = missing - false_positives

    if not doc_refs - false_positives:
        return 1.0, []

    score = len(found) / len(doc_refs - false_positives) if doc_refs - false_positives else 1.0
    return score, list(missing)[:10]  # Return up to 10 missing refs


def calculate_staleness_score(doc_path: Path) -> Tuple[float, int]:
    """Calculate staleness based on file modification time."""
    try:
        mtime = datetime.fromtimestamp(doc_path.stat().st_mtime)
        age_days = (datetime.now() - mtime).days

        # Score: 1.0 for today, decays to 0.5 at 90 days, 0.2 at 180 days
        if age_days <= 7:
            score = 1.0
        elif age_days <= 30:
            score = 0.9
        elif age_days <= 90:
            score = 0.7
        elif age_days <= 180:
            score = 0.5
        else:
            score = 0.3

        return score, age_days
    except Exception:
        return 0.5, -1


def calculate_redundancy_score(
    doc_path: Path,
    doc_refs: Set[str],
    all_doc_refs: Dict[Path, Set[str]]
) -> Tuple[float, List[str]]:
    """Check if this doc's content is covered elsewhere."""
    if not doc_refs:
        return 1.0, []

    overlapping_docs = []

    for other_path, other_refs in all_doc_refs.items():
        if other_path == doc_path:
            continue

        overlap = doc_refs & other_refs
        if len(overlap) > len(doc_refs) * 0.5:  # >50% overlap
            overlapping_docs.append(str(other_path))

    # More overlapping docs = lower score
    if len(overlapping_docs) >= 3:
        score = 0.3
    elif len(overlapping_docs) >= 2:
        score = 0.5
    elif len(overlapping_docs) >= 1:
        score = 0.7
    else:
        score = 1.0

    return score, overlapping_docs


def calculate_location_score(doc_path: Path, doc_refs: Set[str]) -> Tuple[float, str]:
    """Check if doc is in appropriate location."""
    path_str = str(doc_path)

    # Archive should not exist in active docs
    if "_archive" in path_str:
        return 0.0, "In archive - should be excluded from assessment"

    # Check location appropriateness
    if "architecture" in path_str:
        # Architecture docs should reference core classes
        if any(ref in doc_refs for ref in ['Sentinel', 'EpistemicBus', 'Session', 'Goal']):
            return 1.0, "Appropriate location"
        return 0.7, "Architecture doc but few core class references"

    if "reference/api" in path_str:
        # API docs should have code examples
        return 1.0, "API reference location"

    if "guides" in path_str:
        # Guides are for humans
        return 0.8, "Guide (human-focused, may be less AI-useful)"

    if path_str.startswith("docs/0"):
        # Numbered top-level docs are onboarding
        return 0.6, "Onboarding doc (human-focused)"

    return 0.8, "Standard location"


def audit_doc(
    doc_path: Path,
    existing_classes: Set[str],
    existing_functions: Set[str],
    cli_commands: Set[str],
    all_doc_refs: Dict[Path, Set[str]]
) -> Dict[str, Any]:
    """Audit a single documentation file."""
    try:
        content = doc_path.read_text()
    except Exception as e:
        return {
            "path": str(doc_path),
            "error": str(e),
            "confidence": 0.0,
            "recommendation": "ERROR"
        }

    # Extract references
    doc_refs = extract_code_references(content)

    # Calculate scores
    code_score, missing_refs = calculate_code_reference_score(
        doc_refs, existing_classes, existing_functions, cli_commands
    )
    staleness_score, age_days = calculate_staleness_score(doc_path)
    redundancy_score, overlapping = calculate_redundancy_score(
        doc_path, doc_refs, all_doc_refs
    )
    location_score, location_note = calculate_location_score(doc_path, doc_refs)

    # Weighted confidence score
    confidence = (
        code_score * WEIGHTS["code_reference"] +
        staleness_score * WEIGHTS["staleness"] +
        redundancy_score * WEIGHTS["redundancy"] +
        location_score * WEIGHTS["location"]
    )

    # Recommendation
    if confidence >= DECAY_THRESHOLD:
        recommendation = "KEEP"
    elif confidence >= ARCHIVE_THRESHOLD:
        recommendation = "REVIEW"
    elif confidence >= DELETE_THRESHOLD:
        recommendation = "ARCHIVE"
    else:
        recommendation = "DELETE"

    return {
        "path": str(doc_path),
        "confidence": round(confidence, 3),
        "recommendation": recommendation,
        "scores": {
            "code_reference": round(code_score, 3),
            "staleness": round(staleness_score, 3),
            "redundancy": round(redundancy_score, 3),
            "location": round(location_score, 3)
        },
        "details": {
            "references_found": len(doc_refs),
            "missing_refs": missing_refs[:5],
            "age_days": age_days,
            "overlapping_docs": overlapping[:3],
            "location_note": location_note
        }
    }


def run_audit() -> Dict[str, Any]:
    """Run full documentation audit."""
    print("🔍 Loading codebase references...")
    existing_classes = get_existing_classes()
    existing_functions = get_existing_functions()
    cli_commands = get_cli_commands()

    print(f"   Found {len(existing_classes)} classes, {len(existing_functions)} functions, {len(cli_commands)} CLI commands")

    # Get all doc files (excluding archive)
    doc_files = [
        p for p in DOCS_DIR.rglob("*.md")
        if "_archive" not in str(p)
    ]

    print(f"📄 Auditing {len(doc_files)} documentation files...")

    # Pre-extract all references for redundancy detection
    all_doc_refs = {}
    for doc_path in doc_files:
        try:
            content = doc_path.read_text()
            all_doc_refs[doc_path] = extract_code_references(content)
        except Exception:
            all_doc_refs[doc_path] = set()

    # Audit each doc
    results = []
    for doc_path in doc_files:
        result = audit_doc(
            doc_path,
            existing_classes,
            existing_functions,
            cli_commands,
            all_doc_refs
        )
        results.append(result)

    # Sort by confidence (lowest first)
    results.sort(key=lambda x: x["confidence"])

    # Summary
    keep = len([r for r in results if r["recommendation"] == "KEEP"])
    review = len([r for r in results if r["recommendation"] == "REVIEW"])
    archive = len([r for r in results if r["recommendation"] == "ARCHIVE"])
    delete = len([r for r in results if r["recommendation"] == "DELETE"])

    return {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_docs": len(results),
            "keep": keep,
            "review": review,
            "archive": archive,
            "delete": delete,
            "average_confidence": round(sum(r["confidence"] for r in results) / len(results), 3) if results else 0
        },
        "thresholds": {
            "decay": DECAY_THRESHOLD,
            "archive": ARCHIVE_THRESHOLD,
            "delete": DELETE_THRESHOLD
        },
        "results": results
    }


if __name__ == "__main__":
    import sys

    audit = run_audit()

    # Print summary
    print("\n" + "="*60)
    print("📊 DOCUMENTATION HEALTH AUDIT")
    print("="*60)

    summary = audit["summary"]
    print(f"\nTotal docs: {summary['total_docs']}")
    print(f"Average confidence: {summary['average_confidence']:.1%}")
    print(f"\nRecommendations:")
    print(f"  ✅ KEEP:    {summary['keep']}")
    print(f"  🔍 REVIEW:  {summary['review']}")
    print(f"  📦 ARCHIVE: {summary['archive']}")
    print(f"  🗑️  DELETE:  {summary['delete']}")

    # Show worst offenders
    print("\n" + "-"*60)
    print("LOWEST CONFIDENCE (candidates for removal):")
    print("-"*60)

    for result in audit["results"][:15]:
        rec_icon = {"KEEP": "✅", "REVIEW": "🔍", "ARCHIVE": "📦", "DELETE": "🗑️"}.get(result["recommendation"], "?")
        print(f"\n{rec_icon} {result['path']}")
        print(f"   Confidence: {result['confidence']:.1%}")
        print(f"   Scores: code={result['scores']['code_reference']:.1%} "
              f"stale={result['scores']['staleness']:.1%} "
              f"redundant={result['scores']['redundancy']:.1%} "
              f"location={result['scores']['location']:.1%}")
        if result['details']['missing_refs']:
            print(f"   Missing refs: {result['details']['missing_refs']}")
        if result['details']['overlapping_docs']:
            print(f"   Overlaps with: {result['details']['overlapping_docs']}")

    # Output full JSON
    if "--json" in sys.argv:
        print("\n" + "="*60)
        print(json.dumps(audit, indent=2))
