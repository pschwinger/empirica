# 🚨 CLI Commands Remediation Urgency Analysis
**Date:** November 16, 2025  
**CRITICAL FINDING:** Core CASCADE commands violate "no heuristics" principle  
**IMPACT:** Launch-blocking architectural violations in core workflow

## 🎯 **CRITICAL REMEDIATION REQUIRED**

### **🔴 IMMEDIATE LAUNCH BLOCKERS (Hardcoded Heuristics)**

#### **1. `cascade_commands.py` - MASSIVE VIOLATIONS**
**Violations Found:**
- **Decision Thresholds:** `know < 0.5`, `uncertainty > 0.7`, `avg_foundation >= 0.7`
- **Weighted Scoring:** `foundation * 0.6 + comprehension * 0.4`
- **Score Interpretation:** `>= 0.8 excellent`, `>= 0.6 good`, `>= 0.4 moderate`
- **Delta Thresholds:** `> 0.1 significant`, `> 0.05 notable`
- **Default Values:** `.get('know', 0.5)` everywhere

**Impact:** **CORE CASCADE WORKFLOW VIOLATES ARCHITECTURE**  
**Priority:** **CRITICAL - FIX BEFORE LAUNCH**

#### **2. `checkpoint_commands.py` - DISPLAY HEURISTICS**
**Violations Found:**
- **Visual Indicators:** `value >= 0.7 📈`, `>= 0.5 📊`, `else 📉`
- **Default Threshold:** `threshold = 0.15` for diff command

**Impact:** Display logic uses arbitrary thresholds  
**Priority:** **HIGH - Should use profiles**

#### **3. `decision_commands.py` - INPUT VALIDATION ONLY**
**Violations Found:**
- **Range Validation:** `0.0 <= value <= 1.0`, `default 0.5`

**Analysis:** These are input validation, not decision heuristics  
**Priority:** **LOW - Acceptable as validation**

---

## 📊 **COMMANDS ANALYSIS: REMOVE vs REMEDIATE**

### **✅ SAFE TO REMOVE (Pure Overlap, No Unique Value):**

#### **Commands with MCP Equivalents:**
```bash
# These have direct MCP equivalents and no unique CLI value:
empirica sessions-export    # Use database queries directly
empirica explain           # Use cli_help MCP tool  
empirica list              # Redundant with other commands
```

#### **Broken/Non-Functional Commands:**
```bash
# These have known issues and MCP alternatives:
empirica preflight         # Hangs - use execute_preflight MCP
empirica postflight        # Hangs - use execute_postflight MCP
```

### **🔧 MUST REMEDIATE (Core Functionality with Heuristics):**

#### **1. CASCADE Commands - CORE WORKFLOW**
```bash
empirica cascade           # Core workflow - MUST fix heuristics
empirica workflow          # Related to cascade - check for heuristics
```
**Action Required:**
- Replace ALL hardcoded thresholds with profile-based values
- Use ProfileLoader for decision logic
- Implement investigation profile weights

#### **2. Checkpoint Commands - DISPLAY LAYER**
```bash
empirica checkpoint-*      # Display formatting - fix indicators
```
**Action Required:**
- Use profile-based thresholds for visual indicators
- Make diff thresholds configurable

### **🟡 KEEP AS-IS (Unique Value, No Major Violations):**

#### **Configuration & Setup:**
```bash
empirica config-*          # Unique CLI functionality
empirica profile-*         # Profile management
empirica bootstrap-system  # System setup
empirica onboard          # User onboarding  
empirica demo             # Demo functionality
```

#### **Development Tools:**
```bash
empirica mcp-*            # MCP server management
empirica monitor          # Development monitoring  
empirica benchmark        # Performance testing
```

#### **Session Management:**
```bash
empirica sessions-list    # Better UX than MCP equivalent
empirica sessions-show    # Better formatting than MCP
```

---

## 🚀 **REMEDIATION IMPLEMENTATION PLAN**

### **🎯 PHASE 1: CRITICAL HEURISTICS (Pre-Launch)**

#### **Fix CASCADE Commands:**
```python
# BEFORE (cascade_commands.py):
if know < 0.5:                    # ❌ HARDCODED
if uncertainty > 0.7:             # ❌ HARDCODED  
foundation * 0.6 + comprehension * 0.4  # ❌ HARDCODED WEIGHTS

# AFTER (profile-based):
thresholds = _get_profile_cascade_thresholds()
if know < thresholds.knowledge_gate:          # ✅ PROFILE-BASED
if uncertainty > thresholds.uncertainty_max:  # ✅ PROFILE-BASED
foundation * thresholds.foundation_weight + comprehension * thresholds.comprehension_weight
```

#### **Implementation Steps:**
1. **Create `_get_cascade_profile_thresholds()`** function
2. **Replace hardcoded values** with profile lookups
3. **Add cascade-specific constraints** to investigation_profiles.yaml
4. **Test with different profiles** to ensure behavior changes appropriately

### **🎯 PHASE 2: REMOVE SAFE COMMANDS (Post-Launch)**

#### **Deprecate and Remove:**
```bash
# Commands to remove completely:
rm empirica preflight      # Broken, MCP works
rm empirica postflight     # Broken, MCP works  
rm empirica explain        # Redundant with cli_help MCP
rm empirica list           # Redundant functionality
rm empirica sessions-export # Use database directly
```

### **🎯 PHASE 3: OPTIMIZE ARCHITECTURE (Month 2)**

#### **CLI as Orchestration Layer:**
```python
# Enhanced investigation command using multiple MCP tools:
def enhanced_investigate_command(target):
    preflight = mcp_call("execute_preflight", prompt=f"Investigate {target}")
    
    if preflight.uncertainty > profile.uncertainty_threshold:
        web_search = mcp_call("firecrawl_search", query=target)
        code_analysis = analyze_codebase(target)
        beliefs = mcp_call("query_bayesian_beliefs", context=target)
    
    postflight = mcp_call("execute_postflight", task_summary=f"Investigation of {target}")
    return create_investigation_report(preflight, findings, postflight)
```

---

## 📊 **FINAL COMMAND COUNT ANALYSIS**

### **Current State: ~50 Commands**

#### **REMOVE (8 commands):**
- `preflight`, `postflight` (broken)
- `explain`, `list`, `sessions-export` (redundant)
- 3 other low-value duplicates

#### **REMEDIATE (5 commands):**  
- `cascade` (critical heuristics)
- `checkpoint-*` commands (display heuristics)
- Related workflow commands

#### **KEEP (37 commands):**
- Configuration & setup (10)
- Development tools (8)
- Session management (5)
- Investigation & analysis (6)  
- Monitoring & utilities (8)

### **Result: 37 commands (26% reduction)**

---

## 🎯 **SUCCESS CRITERIA**

### **Pre-Launch (Critical):**
- [ ] **Zero hardcoded decision thresholds** in CASCADE commands
- [ ] **Profile-based weights** for all scoring algorithms
- [ ] **Investigation profiles control** all threshold behavior
- [ ] **Broken commands deprecated** with migration guidance

### **Post-Launch (Optimization):**
- [ ] **Redundant commands removed** completely  
- [ ] **CLI as orchestration layer** for complex workflows
- [ ] **Consistent architecture** across all commands
- [ ] **Maintainable codebase** with minimal duplication

**This analysis reveals that the real issue isn't CLI vs MCP overlap, but rather that the CORE CASCADE WORKFLOW contains massive architectural violations that must be fixed before launch!**