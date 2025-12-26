# Auto Issue Capture Phase 2: CASCADE Integration

## Objectives
1. Add issues to project-bootstrap output
2. Display active issues in CHECK gate for context
3. Filter resolved issues appropriately

## Implementation Tasks

### Task 1: Integrate Issues into project-bootstrap Output
**File**: `empirica/cli/command_handlers/project_commands.py`
**Function**: `handle_project_bootstrap_command`

Add after existing breadcrumbs:
```python
# Load auto-captured issues
from empirica.core.issue_capture import initialize_auto_capture
service = initialize_auto_capture(session_id)

# Get issues by status
active_issues = service.list_issues(status=None)  # new, investigating, handoff
resolved_issues = service.list_issues(status="resolved")

breadcrumbs_data['issues'] = {
    'active': [
        {
            'id': i['id'],
            'category': i['category'],
            'severity': i['severity'],
            'message': i['message'],
            'status': i['status']
        } for i in active_issues if i['status'] in ['new', 'investigating', 'handoff']
    ],
    'resolved_count': len(resolved_issues),
    'resolved_recent': [
        {
            'id': i['id'],
            'category': i['category'],
            'message': i['message'],
            'resolution': i.get('resolution', 'N/A')
        } for i in resolved_issues[-5:]  # Last 5
    ]
}
```

### Task 2: Display Issues in CHECK Gate
**File**: `empirica/cli/command_handlers/workflow_commands.py`
**Function**: `handle_check_command`

After findings/unknowns, add:
```python
# Load active issues for context
from empirica.core.issue_capture import initialize_auto_capture
service = initialize_auto_capture(session_id)
active_issues = [i for i in service.list_issues() if i['status'] in ['new', 'investigating', 'handoff']]

# Add to output
result['context']['active_issues'] = {
    'count': len(active_issues),
    'by_severity': {},
    'items': active_issues[:5]  # Top 5
}
```

### Task 3: Auto-Capture Errors During CASCADE
**File**: `empirica/cli/command_handlers/workflow_commands.py`

Wrap exception handlers:
```python
except Exception as e:
    # Auto-capture the error
    try:
        auto_capture = initialize_auto_capture(session_id)
        auto_capture.capture_error(
            message=f"Error during {phase}: {str(e)}",
            severity=IssueSeverity.HIGH,
            category=IssueCategory.ERROR,
            exc_info=e
        )
    except:
        pass  # Don't let capture fail affect main flow
    
    # Continue with error handling
```

## Testing Strategy

1. **Unit Test**: Issues appear in bootstrap output
```bash
empirica project-bootstrap --project-id <uuid> --include-issues
# Verify JSON includes 'issues' key with active/resolved
```

2. **Integration Test**: CHECK displays issue context
```bash
empirica check --session-id <uuid>
# Verify output includes 'context.active_issues'
```

3. **End-to-End**: New error during CASCADE gets captured
```bash
# Simulate error scenario
# Verify error appears in issue-list
```

## Definition of Done

- [ ] Issues appear in project-bootstrap JSON
- [ ] Issues displayed in CHECK output
- [ ] Errors during CASCADE auto-captured
- [ ] All tests passing
- [ ] Documentation updated

## Estimated Time: 2-3 hours

## Priority: HIGH
(Enables continuous learning loop)
