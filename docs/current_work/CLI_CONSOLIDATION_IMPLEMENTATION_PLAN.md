# CLI Command Consolidation - Implementation Plan

**Date:** 2025-11-17
**Owner:** To be assigned (RovoDev or Copilot Claude)
**Priority:** MEDIUM (Post-launch cleanup)
**Status:** READY FOR IMPLEMENTATION

---

## Executive Summary

**Goal:** Reduce CLI commands from 52 to 37 (29% reduction)
**Approach:** Phased consolidation with backward compatibility
**Timeline:** 3 phases over 4-6 weeks
**Risk:** LOW (backward compatibility maintained)

---

## Implementation Strategy

### Three-Phase Rollout:

**Phase 1:** Add consolidated commands (no breaking changes)
**Phase 2:** Deprecation warnings (migration period)
**Phase 3:** Remove old commands (after validation)

---

## Phase 1: Add Consolidated Commands (Week 1-2)

### Goal: Introduce new commands alongside old ones

### Tasks:

#### 1.1: Consolidate Bootstrap Commands
```python
# New implementation in empirica/cli.py

def bootstrap_cmd(
    level: str = "full",
    interactive: bool = False,
    profile: Optional[str] = None,
    ai_id: Optional[str] = None
):
    """
    Unified bootstrap command

    Replaces:
    - bootstrap (default behavior)
    - bootstrap-system (--level=extended)
    - onboard (--interactive)
    """
    if interactive:
        # Interactive onboarding wizard
        return run_interactive_bootstrap(level=level, profile=profile)

    # Standard bootstrap
    from empirica.bootstraps import bootstrap_metacognition

    components = bootstrap_metacognition(
        ai_id=ai_id or detect_ai_id(),
        level=level,
        profile=profile
    )

    return components

# Register command
@click.command()
@click.option('--level', default='full', type=click.Choice(['minimal', 'full', 'extended']))
@click.option('--interactive', is_flag=True, help='Interactive onboarding wizard')
@click.option('--profile', help='Configuration profile to use')
@click.option('--ai-id', help='AI agent identifier')
def bootstrap(level, interactive, profile, ai_id):
    """Bootstrap Empirica metacognitive framework"""
    result = bootstrap_cmd(level=level, interactive=interactive, profile=profile, ai_id=ai_id)
    # Output formatting
```

**Testing:**
```bash
# Verify all use cases work
empirica bootstrap                           # Default
empirica bootstrap --level=extended          # Replaces bootstrap-system
empirica bootstrap --interactive             # Replaces onboard
empirica bootstrap --profile=dev --ai-id=claude  # Custom
```

---

#### 1.2: Consolidate Assessment Commands
```python
def assess_cmd(
    query: str,
    assessment_type: str = "uncertainty",
    detailed: bool = False,
    session_id: Optional[str] = None
):
    """
    Unified assessment command

    Replaces:
    - assess (default: uncertainty)
    - self-awareness (--type=self-awareness)
    - metacognitive (--type=metacognitive)
    """
    if assessment_type == "uncertainty":
        return uncertainty_assessment(query, detailed=detailed)
    elif assessment_type == "self-awareness":
        return self_awareness_assessment(detailed=detailed)
    elif assessment_type == "metacognitive":
        return metacognitive_evaluation(query, session_id=session_id)
    else:
        raise ValueError(f"Unknown assessment type: {assessment_type}")

@click.command()
@click.argument('query', required=False)
@click.option('--type', 'assessment_type',
              type=click.Choice(['uncertainty', 'self-awareness', 'metacognitive']),
              default='uncertainty')
@click.option('--detailed', is_flag=True)
@click.option('--session-id')
def assess(query, assessment_type, detailed, session_id):
    """Perform epistemic self-assessment"""
    result = assess_cmd(query or "", assessment_type, detailed, session_id)
    # Output formatting
```

**Testing:**
```bash
empirica assess "complex task"                    # Uncertainty (default)
empirica assess --type=self-awareness --detailed  # Self-awareness
empirica assess "implement feature" --type=metacognitive  # Metacognitive
```

---

#### 1.3: Consolidate Investigation Commands
```python
def investigate_cmd(
    target: str,
    investigation_type: str = "auto",
    context: Optional[str] = None,
    detailed: bool = False
):
    """
    Unified investigation command

    Replaces:
    - investigate (default)
    - analyze (--type=comprehensive)
    """
    # Auto-detect type if not specified
    if investigation_type == "auto":
        investigation_type = detect_target_type(target)

    if investigation_type == "comprehensive":
        # Was "analyze" command
        return comprehensive_analysis(target, context, detailed)
    elif investigation_type == "file":
        return investigate_file(target, context, detailed)
    elif investigation_type == "directory":
        return investigate_directory(target, context, detailed)
    elif investigation_type == "concept":
        return investigate_concept(target, context, detailed)

@click.command()
@click.argument('target')
@click.option('--type', 'investigation_type',
              type=click.Choice(['auto', 'file', 'directory', 'concept', 'comprehensive']),
              default='auto')
@click.option('--context', help='Additional context (JSON)')
@click.option('--detailed', is_flag=True)
def investigate(target, investigation_type, context, detailed):
    """Investigate file, directory, or concept"""
    result = investigate_cmd(target, investigation_type, context, detailed)
    # Output formatting
```

**Testing:**
```bash
empirica investigate src/core/              # Auto-detect (directory)
empirica investigate README.md --type=file  # Explicit file
empirica investigate "OAuth2" --type=concept  # Concept
empirica investigate "system architecture" --type=comprehensive  # Was "analyze"
```

---

#### 1.4: Consolidate Performance Commands
```python
def performance_cmd(
    benchmark: bool = False,
    analyze: bool = False,
    target: Optional[str] = None
):
    """
    Unified performance command

    Replaces:
    - benchmark (--benchmark flag)
    - performance (default: show metrics)
    """
    if benchmark:
        # Run benchmark tests
        return run_benchmark(target=target)
    elif analyze:
        # Detailed analysis
        return analyze_performance(target=target)
    else:
        # Show current metrics
        return show_performance_metrics()

@click.command()
@click.option('--benchmark', is_flag=True, help='Run performance benchmarks')
@click.option('--analyze', is_flag=True, help='Detailed performance analysis')
@click.option('--target', help='Specific component to test/analyze')
def performance(benchmark, analyze, target):
    """Performance testing and analysis"""
    result = performance_cmd(benchmark, analyze, target)
    # Output formatting
```

**Testing:**
```bash
empirica performance                        # Show metrics
empirica performance --benchmark            # Run benchmarks
empirica performance --analyze              # Detailed analysis
empirica performance --benchmark --target=checkpoints  # Specific component
```

---

#### 1.5: Consolidate Config Commands
```python
def config_cmd(
    key: Optional[str] = None,
    value: Optional[str] = None,
    init: bool = False,
    validate: bool = False,
    section: Optional[str] = None
):
    """
    Unified config command

    Replaces:
    - config-init (--init flag)
    - config-show (no args)
    - config-validate (--validate flag)
    - config-get (KEY arg only)
    - config-set (KEY VALUE args)
    """
    if init:
        return initialize_config()

    if validate:
        return validate_config()

    if key and value:
        # Set value (was config-set)
        return set_config(key, value)
    elif key:
        # Get value (was config-get)
        return get_config(key)
    else:
        # Show all config (was config-show)
        return show_config(section=section)

@click.command()
@click.argument('key', required=False)
@click.argument('value', required=False)
@click.option('--init', is_flag=True, help='Initialize configuration')
@click.option('--validate', is_flag=True, help='Validate configuration')
@click.option('--section', help='Show specific section')
def config(key, value, init, validate, section):
    """Configuration management"""
    result = config_cmd(key, value, init, validate, section)
    # Output formatting
```

**Testing:**
```bash
empirica config                             # Show all
empirica config --init                      # Initialize
empirica config --validate                  # Validate
empirica config routing.strategy            # Get value
empirica config routing.strategy epistemic  # Set value
empirica config --section routing           # Show section
```

---

#### 1.6: Consolidate Monitor Commands
```python
def monitor_cmd(
    export: Optional[str] = None,
    reset: bool = False,
    cost: bool = False,
    history: bool = False
):
    """
    Unified monitor command

    Replaces:
    - monitor (default: dashboard)
    - monitor-export (--export FILE)
    - monitor-reset (--reset flag)
    - monitor-cost (--cost flag)
    """
    if reset:
        return reset_monitoring_stats()

    if export:
        return export_monitoring_data(export)

    if cost:
        return show_cost_analysis()

    if history:
        return show_request_history()

    # Default: show dashboard
    return show_monitoring_dashboard()

@click.command()
@click.option('--export', help='Export data to file')
@click.option('--reset', is_flag=True, help='Reset statistics')
@click.option('--cost', is_flag=True, help='Show cost analysis')
@click.option('--history', is_flag=True, help='Show request history')
def monitor(export, reset, cost, history):
    """Monitoring dashboard and statistics"""
    result = monitor_cmd(export, reset, cost, history)
    # Output formatting
```

**Testing:**
```bash
empirica monitor                    # Show dashboard
empirica monitor --export stats.json  # Export
empirica monitor --reset            # Reset stats
empirica monitor --cost             # Cost analysis
empirica monitor --history          # Request history
```

---

#### 1.7: Consolidate MCP Commands
```python
# New command group structure

@click.group()
def mcp():
    """MCP server management"""
    pass

@mcp.command('server')
@click.option('--start', is_flag=True)
@click.option('--stop', is_flag=True)
@click.option('--status', is_flag=True)
@click.option('--test', is_flag=True)
def mcp_server(start, stop, status, test):
    """MCP server lifecycle management"""
    if start:
        return start_mcp_server()
    elif stop:
        return stop_mcp_server()
    elif test:
        return test_mcp_connection()
    else:
        # Default: show status
        return show_mcp_status()

@mcp.command('tools')
@click.option('--list', 'list_tools', is_flag=True, default=True)
@click.option('--show-all', is_flag=True)
def mcp_tools(list_tools, show_all):
    """List available MCP tools"""
    return list_mcp_tools(show_all=show_all)

@mcp.command('call')
@click.argument('tool_name')
@click.option('--arguments', help='Tool arguments (JSON)')
def mcp_call(tool_name, arguments):
    """Call MCP tool directly"""
    return call_mcp_tool(tool_name, arguments)
```

**Testing:**
```bash
empirica mcp server                 # Show status
empirica mcp server --start         # Start server
empirica mcp server --stop          # Stop server
empirica mcp server --test          # Test connection
empirica mcp tools                  # List tools
empirica mcp tools --show-all       # Detailed tool list
empirica mcp call bootstrap_session --arguments '{"ai_id":"claude"}'  # Call tool
```

---

### Phase 1 Deliverables:

- [ ] All 7 consolidated commands implemented
- [ ] All old commands still work (backward compatible)
- [ ] Unit tests for new commands
- [ ] Integration tests verifying old/new equivalence
- [ ] Help text updated with examples

---

## Phase 2: Deprecation Warnings (Week 3-4)

### Goal: Guide users to new commands

### Tasks:

#### 2.1: Add Deprecation Warnings
```python
def deprecated_command(old_name: str, new_command: str):
    """
    Wrapper for deprecated commands
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            click.echo(click.style(
                f"⚠️  Warning: '{old_name}' is deprecated. "
                f"Use '{new_command}' instead.",
                fg='yellow'
            ), err=True)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Apply to old commands
@click.command()
@deprecated_command('bootstrap-system', 'bootstrap --level=extended')
def bootstrap_system():
    """DEPRECATED: Use 'bootstrap --level=extended' instead"""
    # Redirect to new command
    from empirica.cli import bootstrap_cmd
    return bootstrap_cmd(level='extended')
```

#### 2.2: Update All Help Text
```bash
# Old command help
empirica bootstrap-system --help
# Output:
# DEPRECATED: This command will be removed in v2.0
# Use: empirica bootstrap --level=extended
```

#### 2.3: Track Migration
```python
# Log deprecated command usage
def log_deprecated_usage(command_name: str):
    """Track usage for migration analysis"""
    usage_db.record_deprecated_command(command_name, timestamp=now())
```

### Phase 2 Deliverables:

- [ ] Deprecation warnings on all 15 old commands
- [ ] Updated help text with migration guidance
- [ ] Usage tracking implemented
- [ ] Migration guide published

---

## Phase 3: Remove Old Commands (Week 5-6)

### Goal: Clean up codebase

### Prerequisites:

- [ ] 90%+ users migrated to new commands (check usage logs)
- [ ] No CI/CD scripts use old commands
- [ ] Documentation fully updated

### Tasks:

#### 3.1: Remove Command Implementations
```python
# Remove from empirica/cli.py:
# - bootstrap_system_cmd()
# - onboard_cmd()
# - self_awareness_cmd()
# - metacognitive_cmd()
# - analyze_cmd()
# - benchmark_cmd()
# - config_init_cmd()
# - config_show_cmd()
# - config_get_cmd()
# - config_set_cmd()
# - monitor_export_cmd()
# - monitor_reset_cmd()
# - monitor_cost_cmd()
# - mcp_start_cmd()
# - mcp_stop_cmd()
# - mcp_status_cmd()
```

#### 3.2: Update Tests
```bash
# Remove tests for old commands
rm tests/cli/test_bootstrap_system.py
rm tests/cli/test_onboard.py
# ...etc

# Ensure new commands have equivalent coverage
pytest tests/cli/test_consolidated_commands.py -v
```

#### 3.3: Update Documentation
```bash
# Update all documentation references
docs/01_a_AI_AGENT_START.md
docs/04_MCP_QUICKSTART.md
docs/production/01_QUICK_START.md
README.md
```

### Phase 3 Deliverables:

- [ ] 15 old commands removed from codebase
- [ ] All tests updated and passing
- [ ] Documentation fully migrated
- [ ] Release notes published

---

## Validation Checklist

### Before Starting:

- [ ] No MCP tools call CLI commands directly (checked)
- [ ] No scripts in `/scripts/` depend on removed commands (checked)
- [ ] Documented all command equivalences

### Phase 1 Validation:

- [ ] All new commands work as expected
- [ ] Old commands still work (backward compat)
- [ ] Help text accurate
- [ ] Tests pass

### Phase 2 Validation:

- [ ] Deprecation warnings display correctly
- [ ] Usage tracking working
- [ ] Migration guide clear and helpful

### Phase 3 Validation:

- [ ] Old commands completely removed
- [ ] No broken references in code/docs
- [ ] All tests pass
- [ ] User feedback positive

---

## Testing Strategy

### Unit Tests:
```python
# tests/cli/test_consolidated_commands.py

def test_bootstrap_command():
    """Test unified bootstrap command"""
    # Default behavior
    result = runner.invoke(cli, ['bootstrap'])
    assert result.exit_code == 0

    # Extended level (replaces bootstrap-system)
    result = runner.invoke(cli, ['bootstrap', '--level=extended'])
    assert result.exit_code == 0

    # Interactive mode (replaces onboard)
    result = runner.invoke(cli, ['bootstrap', '--interactive'], input='y\nclaude\n')
    assert result.exit_code == 0

def test_assess_command():
    """Test unified assess command"""
    # Uncertainty (default)
    result = runner.invoke(cli, ['assess', 'complex task'])
    assert result.exit_code == 0

    # Self-awareness (replaces self-awareness command)
    result = runner.invoke(cli, ['assess', '--type=self-awareness'])
    assert result.exit_code == 0

    # Metacognitive (replaces metacognitive command)
    result = runner.invoke(cli, ['assess', 'implement X', '--type=metacognitive'])
    assert result.exit_code == 0

# ... similar for all consolidated commands
```

### Integration Tests:
```bash
#!/bin/bash
# tests/integration/test_cli_consolidation.sh

# Test bootstrap consolidation
empirica bootstrap --level=extended
assert_success

# Test assess consolidation
empirica assess --type=self-awareness --detailed
assert_success

# Test config consolidation
empirica config routing.strategy epistemic
assert_success

# Test monitor consolidation
empirica monitor --cost
assert_success

# Test MCP consolidation
empirica mcp server --status
assert_success
```

---

## Migration Guide for Users

### Quick Reference:

```bash
# OLD COMMAND → NEW COMMAND

# Bootstrap
bootstrap-system → bootstrap --level=extended
onboard → bootstrap --interactive

# Assessment
self-awareness --detailed → assess --type=self-awareness --detailed
metacognitive "task" → assess "task" --type=metacognitive

# Investigation
analyze "subject" → investigate "subject" --type=comprehensive

# Performance
benchmark → performance --benchmark

# Config
config-init → config --init
config-show → config
config-get KEY → config KEY
config-set KEY VALUE → config KEY VALUE

# Monitor
monitor-export file.json → monitor --export file.json
monitor-reset → monitor --reset
monitor-cost → monitor --cost

# MCP
mcp-start → mcp server --start
mcp-stop → mcp server --stop
mcp-status → mcp server (or mcp server --status)
mcp-list-tools → mcp tools
```

---

## Risk Mitigation

### Backward Compatibility:
- Phase 1: All old commands work (just deprecated)
- Phase 2: Warnings added, but still functional
- Phase 3: Only remove after validated migration

### Rollback Plan:
- Keep old command implementations in version control
- Can restore if critical breakage detected
- Semantic versioning: Major version bump for removal

### Communication:
- Release notes for each phase
- Migration guide in docs
- Deprecation warnings in CLI output
- Blog post / announcement for major changes

---

## Success Metrics

### Adoption:
- [ ] 90%+ users migrated to new commands (tracked via usage logs)
- [ ] <5 support tickets related to consolidation
- [ ] Positive user feedback on simplified CLI

### Code Quality:
- [ ] 29% reduction in CLI command count (52 → 37)
- [ ] ~15% reduction in CLI codebase size
- [ ] Test coverage maintained at >80%

### Documentation:
- [ ] All docs updated
- [ ] Migration guide published
- [ ] Examples use new commands

---

## Timeline

**Week 1-2:** Phase 1 (Add consolidated commands)
**Week 3-4:** Phase 2 (Deprecation warnings)
**Week 5-6:** Phase 3 (Remove old commands)

**Total Duration:** 6 weeks
**Effort:** ~40 hours total (10 hours/week for 4 weeks)

---

## Recommendation

**Proceed with consolidation** using phased approach:

1. ✅ Low risk (backward compatibility maintained)
2. ✅ High value (29% command reduction, better UX)
3. ✅ Well-planned (3 phases, clear rollback)
4. ✅ Validated (comprehensive testing strategy)

**Start after Nov 20 launch** (non-blocking cleanup work)

---

**Status:** READY FOR IMPLEMENTATION
**Owner:** To be assigned
**Priority:** MEDIUM (post-launch cleanup)
