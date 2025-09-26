#!/usr/bin/env python3
import os
from pathlib import Path

def validate_migration():
    """Validate that all migrations maintain content integrity"""
    issues = []
    
    for new_file in Path('.').glob('new_*.html'):
        old_file = new_file.name.replace('new_', '')
        
        if Path(old_file).exists():
            old_content = Path(old_file).read_text()
            new_content = Path(new_file).read_text()
            
            # Check critical content preservation
            critical_phrases = [
                "Semantic Self-Aware Kit",
                "meta-cognitive",
                "uncertainty analysis",
                "collaboration framework"
            ]
            
            for phrase in critical_phrases:
                # A simple 'in' check is not enough, as the phrase might be in the template but not in the content.
                # A better check would be to see if the phrase is in the extracted body of the old file, and if so, if it is in the new file.
                # For now, we will stick to the simple check as per the user's instructions.
                if phrase in old_content and phrase not in new_content:
                    issues.append(f"Missing phrase '{phrase}' in {new_file}")
            
            # Check template structure
            if "{% extends" not in new_content:
                issues.append(f"Missing template inheritance in {new_file}")
    
    return issues

# Run validation
issues = validate_migration()
if issues:
    print("❌ Migration issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✅ All migrations validated successfully")
