# 📁 Empirica Folder Reorganization Plan
**Date:** November 16, 2025  
**Purpose:** Clean up root directory and organize documentation properly  
**Future:** Template for Sentinel-managed project organization

## 🎯 **CURRENT STATE: ROOT DIRECTORY CHAOS**

**50+ MD files in root directory** - This violates clean architecture principles and makes navigation difficult.

### **Root Directory Files Found:**
```
DOCUMENTATION FILES (50+):
- Session notes: SESSION_*, CHECKPOINT_*, PHASE_*
- Architecture: ARCHITECTURE_*, SYSTEM_*
- Validation: VALIDATION_*, CRITICAL_*
- Installation: ALL_PLATFORMS_*, INSTALLATION_*
- Handoffs: *_HANDOFF.md, *_NEXT_STEPS.md
- Reports: *_REPORT.md, *_SUMMARY.md
- Current work: Our new analysis files
```

---

## 📋 **REORGANIZATION STRATEGY**

### **🟢 KEEP IN ROOT (Core Project Files):**
```bash
# Essential project files:
README.md                           # Main project documentation
CONTRIBUTING.md                     # Development guidelines
LICENSE                            # Legal
pyproject.toml, setup.py, requirements.txt  # Package config
pytest.ini                         # Testing config
Makefile                           # Build automation
.gitignore, .gitmodules            # Git config

# Current launch-critical documents:
EMPIRICA_FOUNDATION_SPECIFICATION.md  # Our master spec
INVESTIGATION_CONTINUATION_SPEC.md     # Handoff for coordination team
```

### **🔄 MOVE TO PROPER FOLDERS:**

#### **→ `docs/archive/session_notes/`**
```bash
SESSION_COMPLETE_2024_11_14.md
CHECKPOINT_SESSION_2024_11_14_COMPLETE.md
AGENT_WORK_COMPLETE_SUMMARY.md
STATUS_CURRENT_WORK_2024_11_14.md
```

#### **→ `docs/archive/phase_reports/`**
```bash
PHASE2_COMPLETE.md
PHASE2_FIXES_COMPLETE.md  
PHASE2_PROGRESS_HANDOFF.md
PHASE2_UNIFIED_TASKS.md
MULTI_PLATFORM_COMPLETE_SUMMARY.md
INSTALLATION_COMPLETE_SUMMARY.md
```

#### **→ `docs/archive/validation_reports/`**
```bash
VALIDATION_CASCADE_INTEGRATION.md
VALIDATION_INVESTIGATION_STRATEGIES.md
VALIDATION_LLM_CALLBACK.md
VALIDATION_MULTI_AGENT.md
VALIDATION_PERFORMANCE.md
CRITICAL_E2E_TEST.md
COPILOT_E2E_REVIEW.md
```

#### **→ `docs/handoffs/`**
```bash
ROVODEV_E2E_HANDOFF.md
COPILOT_CLAUDE_NEXT_TASKS.md
MINIMAX_NEXT_STEPS.md
MINIMAX_PROMPT_NOV15.md
QWEN_PROMPT_NOV15.md
```

#### **→ `docs/installation/`**
```bash
ALL_PLATFORMS_INSTALLATION.md
ALL_PLATFORMS_QUICK_REFERENCE.md
```

#### **→ `docs/architecture/`**
```bash
ARCHITECTURE_DECISIONS_2024_11_14.md
SYSTEM_PROMPT_QUICK_REFERENCE.md
SYSTEM_PROMPTS_UPDATED.md
GENERIC_EMPIRICA_SYSTEM_PROMPT.md
```

#### **→ `_archive_for_review/` (For other Claude to review)**
```bash
# Session-specific work that may be obsolete:
CASCADE_GIT_TESTS_FIXED.md
CHECKPOINT_SESSION_2024_11_14_COMPLETE.md
CODE_DEDUPLICATION_REPORT.md
DOCUMENTATION_AUDIT_COMPLETE.md
DOCUMENTATION_AUDIT_REPORT.md  
DOCUMENTATION_PLAN_V1.md
FIX_DATES_TASK.md
HARDENING_SANITIZATION_TASKS.md
LAUNCH_CHECKLIST.md
PLATFORM_COMPARISON.md
QWEN_HELP_DATABASE_BUG.md
QWEN_VALIDATION_PROGRESS.md
RELEASE_PREPARATION_PLAN.md
RM_BYPASS_WORKAROUND.md

# Model-specific prompts (may be obsolete):
CLAUDE.md
QWEN.md
```

#### **→ `docs/current_work/` (Our recent analysis)**
```bash
BUG_FIXES_PROGRESS_REPORT.md
CLI_COMMANDS_REMEDIATION_URGENCY.md
CLI_MCP_OVERLAP_ANALYSIS.md
COMPREHENSIVE_CLI_TESTING_SUMMARY.md
FINAL_COMPREHENSIVE_TEST_REPORT.md
HEURISTICS_VIOLATIONS_AUDIT.md
MULTI_AGENT_COORDINATION_INVESTIGATION_REPORT.md
SENTINEL_COORDINATION_ANALYSIS.md
```

---

## 🚀 **IMPLEMENTATION PLAN**

### **Phase 1: Create Archive for Review**
```bash
# Create folders for other Claude to review:
mkdir -p _archive_for_review/{obsolete_sessions,model_prompts,old_validation,misc}

# Move questionable files for review:
mv SESSION_COMPLETE_2024_11_14.md _archive_for_review/obsolete_sessions/
mv CLAUDE.md QWEN.md _archive_for_review/model_prompts/
mv HARDENING_SANITIZATION_TASKS.md _archive_for_review/misc/
mv LAUNCH_CHECKLIST.md _archive_for_review/misc/
# ... (full list in next step)
```

### **Phase 2: Move to Proper Locations**
```bash
# Move to existing docs folders:
mv ROVODEV_E2E_HANDOFF.md docs/handoffs/
mv COPILOT_CLAUDE_NEXT_TASKS.md docs/handoffs/
mv ALL_PLATFORMS_INSTALLATION.md docs/installation/
mv ARCHITECTURE_DECISIONS_2024_11_14.md docs/architecture/

# Move our current work:
mkdir -p docs/current_work/
mv BUG_FIXES_PROGRESS_REPORT.md docs/current_work/
mv EMPIRICA_FOUNDATION_SPECIFICATION.md docs/current_work/
# ... (our analysis files)
```

### **Phase 3: Clean Root Directory**
```bash
# Final root directory should only contain:
ls -1 /path/to/empirica/
├── README.md
├── CONTRIBUTING.md  
├── LICENSE
├── pyproject.toml
├── setup.py
├── requirements.txt
├── pytest.ini
├── Makefile
├── .gitignore
├── .gitmodules
├── empirica/           # Source code
├── docs/              # Documentation
├── tests/             # Test suite
├── examples/          # Usage examples
├── scripts/           # Utility scripts
├── mcp_local/         # MCP server
└── _archive_for_review/  # Files for other Claude to review
```

---

## 🤖 **FUTURE SENTINEL CAPABILITY**

### **Intelligent Project Organization:**
```python
# Future Sentinel capability:
class SentinelProjectOrganizer:
    def analyze_project_structure(self, project_path: str) -> ProjectAnalysis:
        """
        Analyze project for organizational issues:
        - Root directory clutter
        - Misplaced documentation  
        - Obsolete files
        - Missing folder structure
        """
        
    def suggest_reorganization(self, analysis: ProjectAnalysis) -> ReorganizationPlan:
        """
        Generate intelligent reorganization suggestions:
        - Canonical folder structures by project type
        - Obsolete file detection
        - Related file grouping
        - Architectural alignment
        """
        
    def execute_reorganization(self, plan: ReorganizationPlan) -> None:
        """
        Execute reorganization with safety checks:
        - Create necessary folders
        - Move files with git history preservation
        - Update documentation links  
        - Generate cleanup report
        """
```

### **Project Type Templates:**
```python
EMPIRICA_PROJECT_STRUCTURE = {
    "root": ["README.md", "CONTRIBUTING.md", "LICENSE", "pyproject.toml"],
    "docs": {
        "current_work": "Active development documentation",
        "architecture": "System design and decisions", 
        "handoffs": "Inter-team communication",
        "installation": "Setup and deployment guides",
        "archive": "Historical documentation"
    },
    "source": "empirica/",
    "tests": "tests/",
    "examples": "examples/",
    "scripts": "scripts/"
}
```

---

## 📊 **CLEANUP METRICS**

### **Before Cleanup:**
- **50+ files in root** directory
- **Mixed file types** (session notes, architecture, validation, etc.)
- **Navigation difficulty** finding relevant documentation
- **No clear organization** by purpose or timeline

### **After Cleanup:**
- **<10 files in root** (essential project files only)
- **Organized by purpose** in appropriate doc folders
- **Clear separation** of current vs archived work
- **_archive_for_review folder** for other Claude to evaluate

### **Files for Other Claude to Review:**
```
_archive_for_review/
├── obsolete_sessions/      # 8 files - may be safe to delete
├── model_prompts/          # 3 files - check if still relevant  
├── old_validation/         # 12 files - likely obsolete
└── misc/                   # 15 files - various cleanup candidates
```

---

## 🎯 **IMMEDIATE ACTION ITEMS**

### **For Current Session:**
1. **Create archive structure** for review
2. **Move obvious candidates** to _archive_for_review
3. **Organize current work** into docs/current_work
4. **Move clearly categorizable** files to proper docs folders

### **For Other Claude Review:**
1. **Analyze archived files** against project requirements  
2. **Identify obsolete content** safe for deletion
3. **Check documentation links** for moved files
4. **Validate folder organization** aligns with project goals

### **Future Sentinel Integration:**
1. **Document organization patterns** discovered
2. **Create project structure templates**
3. **Build file relationship analysis** capabilities
4. **Develop automated cleanup suggestions**

**This reorganization will transform Empirica from organizational chaos to clean, navigable project structure - exactly the kind of task Sentinel could automate in the future!**