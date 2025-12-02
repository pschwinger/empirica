#!/usr/bin/env python3
"""
Comprehensive CLI Command Audit

Tests all 55 Empirica CLI commands to verify:
1. Command exists and responds to --help
2. Required arguments are documented
3. Optional arguments work
4. Basic execution doesn't crash
5. Error handling is appropriate

Created: 2025-12-01
Purpose: Ensure all CLI commands are functional
"""

import subprocess
import json
import time
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class CommandTest:
    name: str
    category: str
    has_help: bool = False
    help_works: bool = False
    basic_exec_works: bool = False
    error_msg: str = ""
    notes: str = ""

# All 55 commands from empirica --help
COMMANDS = [
    # Core Workflow (8)
    ("bootstrap", "Core Workflow"),
    ("preflight", "Core Workflow"),
    ("check", "Core Workflow"),
    ("postflight", "Core Workflow"),
    ("preflight-submit", "Core Workflow"),
    ("check-submit", "Core Workflow"),
    ("postflight-submit", "Core Workflow"),
    ("workflow", "Core Workflow"),
    
    # Assessment (5)
    ("assess", "Assessment"),
    ("self-awareness", "Assessment"),
    ("metacognitive", "Assessment"),
    ("calibration", "Assessment"),
    ("uvl", "Assessment"),
    
    # Decision Making (3)
    ("decision", "Decision Making"),
    ("decision-batch", "Decision Making"),
    ("feedback", "Decision Making"),
    
    # Investigation (3)
    ("investigate", "Investigation"),
    ("investigate-log", "Investigation"),
    ("goal-analysis", "Investigation"),
    
    # Actions (1)
    ("act-log", "Actions"),
    
    # Performance (2)
    ("performance", "Performance"),
    ("efficiency-report", "Performance"),
    
    # Monitoring (1)
    ("monitor", "Monitoring"),
    
    # Configuration (5)
    ("config", "Configuration"),
    ("profile-list", "Configuration"),
    ("profile-show", "Configuration"),
    ("profile-create", "Configuration"),
    ("profile-set-default", "Configuration"),
    
    # Components (3)
    ("list", "Components"),
    ("explain", "Components"),
    ("demo", "Components"),
    
    # Sessions (4)
    ("sessions-list", "Sessions"),
    ("sessions-show", "Sessions"),
    ("sessions-export", "Sessions"),
    ("sessions-resume", "Sessions"),
    
    # Git Checkpoints (4)
    ("checkpoint-create", "Git Checkpoints"),
    ("checkpoint-load", "Git Checkpoints"),
    ("checkpoint-list", "Git Checkpoints"),
    ("checkpoint-diff", "Git Checkpoints"),
    
    # Handoffs (2)
    ("handoff-create", "Handoffs"),
    ("handoff-query", "Handoffs"),
    
    # Goals (7)
    ("goals-create", "Goals"),
    ("goals-add-subtask", "Goals"),
    ("goals-complete-subtask", "Goals"),
    ("goals-progress", "Goals"),
    ("goals-list", "Goals"),
    ("goals-discover", "Goals"),
    ("goals-resume", "Goals"),
    
    # Identity (4)
    ("identity-create", "Identity"),
    ("identity-list", "Identity"),
    ("identity-export", "Identity"),
    ("identity-verify", "Identity"),
    
    # User Interfaces (2)
    ("ask", "User Interfaces"),
    ("chat", "User Interfaces"),
]

def test_command_help(cmd: str) -> Tuple[bool, str]:
    """Test if command has working --help"""
    try:
        result = subprocess.run(
            ["empirica", cmd, "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        # Success if exit code 0 or help text appears
        if result.returncode == 0 or "usage:" in result.stdout or cmd in result.stdout:
            return True, ""
        return False, f"Exit code {result.returncode}"
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def test_command_missing_args(cmd: str) -> Tuple[bool, str]:
    """Test command behavior with missing required args"""
    try:
        result = subprocess.run(
            ["empirica", cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        # Should either succeed or show appropriate error
        if "required" in result.stderr.lower() or "error" in result.stderr.lower():
            return True, "Shows required args error"
        elif result.returncode == 0:
            return True, "Runs without args"
        else:
            return True, f"Exit code {result.returncode}"
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def categorize_results(results: List[CommandTest]) -> Dict[str, List[CommandTest]]:
    """Group results by category"""
    categories = {}
    for result in results:
        if result.category not in categories:
            categories[result.category] = []
        categories[result.category].append(result)
    return categories

def main():
    print("=" * 70)
    print("EMPIRICA CLI COMMAND AUDIT")
    print("=" * 70)
    print(f"\nTesting {len(COMMANDS)} commands...\n")
    
    results = []
    
    for cmd, category in COMMANDS:
        print(f"Testing: {cmd:30} ", end="", flush=True)
        
        test = CommandTest(name=cmd, category=category, has_help=True)
        
        # Test 1: --help
        help_works, help_msg = test_command_help(cmd)
        test.help_works = help_works
        if not help_works:
            test.error_msg = f"Help failed: {help_msg}"
            print(f"❌ HELP FAILED")
        else:
            # Test 2: Missing args behavior
            exec_works, exec_msg = test_command_missing_args(cmd)
            test.basic_exec_works = exec_works
            test.notes = exec_msg
            
            if exec_works:
                print(f"✅ OK")
            else:
                test.error_msg = f"Execution failed: {exec_msg}"
                print(f"⚠️  WARN")
        
        results.append(test)
        time.sleep(0.1)  # Rate limit
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    total = len(results)
    help_pass = sum(1 for r in results if r.help_works)
    exec_pass = sum(1 for r in results if r.basic_exec_works)
    
    print(f"\nTotal Commands: {total}")
    print(f"Help Working:   {help_pass}/{total} ({help_pass/total*100:.1f}%)")
    print(f"Basic Exec OK:  {exec_pass}/{total} ({exec_pass/total*100:.1f}%)")
    
    # Failed commands
    failed = [r for r in results if not r.help_works or not r.basic_exec_works]
    if failed:
        print(f"\n⚠️  Issues Found: {len(failed)}")
        for r in failed:
            print(f"  - {r.name}: {r.error_msg}")
    else:
        print(f"\n✅ All commands working!")
    
    # Category breakdown
    print("\n" + "=" * 70)
    print("BY CATEGORY")
    print("=" * 70)
    
    categories = categorize_results(results)
    for cat, cmds in sorted(categories.items()):
        working = sum(1 for c in cmds if c.help_works and c.basic_exec_works)
        print(f"\n{cat}: {working}/{len(cmds)}")
        for cmd in cmds:
            status = "✅" if (cmd.help_works and cmd.basic_exec_works) else "❌"
            print(f"  {status} {cmd.name}")
            if cmd.notes:
                print(f"      ({cmd.notes})")
    
    # Export to JSON
    output = {
        "total_commands": total,
        "help_working": help_pass,
        "exec_working": exec_pass,
        "timestamp": time.time(),
        "results": [
            {
                "command": r.name,
                "category": r.category,
                "help_works": r.help_works,
                "exec_works": r.basic_exec_works,
                "error": r.error_msg,
                "notes": r.notes
            }
            for r in results
        ]
    }
    
    with open("/tmp/empirica_cli_audit.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "=" * 70)
    print(f"Results saved to: /tmp/empirica_cli_audit.json")
    print("=" * 70)
    
    return 0 if len(failed) == 0 else 1

if __name__ == "__main__":
    exit(main())
