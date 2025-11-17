# 📋 Archive Review Instructions for Claude
**Purpose:** Files moved here need evaluation for potential deletion  
**Organized by:** RovoDev during root directory cleanup  
**Review Goal:** Determine what can be safely removed vs preserved

## 🎯 **FOLDERS TO REVIEW**

### **📁 `obsolete_sessions/` (4 files)**
**Content:** Session notes from 2024-11-14 work  
**Likely Status:** Probably safe to delete (superseded by current work)  
**Review Question:** Any unique insights not captured elsewhere?

### **📁 `model_prompts/` (4 files)**  
**Content:** LLM-specific prompts (Claude, Qwen, Minimax)  
**Likely Status:** May have historical value or reusable content  
**Review Question:** Still relevant for current system prompts?

### **📁 `old_validation/` (7 files)**
**Content:** Validation reports from earlier phases  
**Likely Status:** Likely obsolete (current validation is more comprehensive)  
**Review Question:** Any unique test cases or validation approaches to preserve?

### **📁 `misc/` (20 files)**
**Content:** Mixed reports, documentation audits, platform comparisons  
**Likely Status:** Mostly obsolete but may contain useful patterns  
**Review Question:** Any architectural decisions or learnings to preserve?

## 🔍 **REVIEW CRITERIA**

### **✅ KEEP IF:**
- Contains unique architectural insights not documented elsewhere
- Has reusable patterns or templates
- Documents important decisions or learnings
- Provides historical context for major changes

### **❌ DELETE IF:**
- Information is superseded by current documentation  
- Content is session-specific and no longer relevant
- Duplicates information available elsewhere
- No unique value for future development

## 📊 **EXPECTED OUTCOME**
**Estimate:** 70% can probably be deleted, 30% may have value to preserve in a historical archive or extract key insights from.

**Goal:** Clean up 35 archived files down to <10 truly valuable documents.