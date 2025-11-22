# MCP Integration - Wireframe

## Page Structure

### Header
- Logo: Empirica
- Primary CTA: "Get Started"
- Secondary CTA: "Empirica MCP"

### Navigation (5 items)
- CLI Interface
- Empirical Confidence
- Components
- Implementation
- Knowledge Base

### Breadcrumbs
Home › Getting Started › MCP Integration

---

## Main Content

### Hero Section
**Title:** Empirica MCP: Seamless Integration with Claude Desktop  
**Subtitle:** Model Context Protocol server exposing full epistemic capabilities to AI assistants

---

### What is MCP Section
**Title:** Understanding MCP Integration

**Content:**
The Model Context Protocol (MCP) allows AI assistants like Claude Desktop to access Empirica's metacognitive capabilities as native tools. Instead of copying code or explaining concepts, Claude can directly:
- Run epistemic cascades
- Assess uncertainty across 13 dimensions
- Make strategic investigation decisions
- Track cognitive processes automatically

This creates a true metacognitive collaboration between you, Claude, and the Empirica framework.

---

### Quick Setup Section
**Title:** 5-Minute Setup for Claude Desktop

#### Step 1: Install Claude Desktop
Download from: [https://claude.ai/download](https://claude.ai/download)

#### Step 2: Locate Config File

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

---

#### Step 3: Add Empirica MCP Server

**Edit config file:**
```json
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": [
        "/full/path/to/empirica/empirica_mcp_server.py"
      ],
      "env": {
        "EMPIRICA_AUTO_BOOTSTRAP": "optimal"
      }
    }
  }
}
```

**Important:** Use absolute paths, not relative paths.

---

#### Step 4: Restart Claude Desktop

The MCP server starts automatically when Claude launches.

---

#### Step 5: Verify Connection

**In Claude Desktop, type:**
```
Can you check if Empirica MCP is connected?
```

**Claude will respond with:**
```
✓ Empirica MCP server connected
✓ Available tools: cascade_run_full, assess_13_vectors, 
  investigate_strategic, monitor_session, and 15 more
✓ Bootstrap: optimal mode
✓ Auto-tracking: enabled
```

---

### Available MCP Tools Section
**Title:** Empirica Tools in Claude Desktop

#### Primary Tools

**1. cascade_run_full**
Run complete epistemic cascade with Think → Assess → Investigate → Act flow.

**Example usage in Claude:**
```
Use Empirica to help me decide if I should refactor the authentication system.
Context: auth.py, 500 lines, last modified 2 years ago, 3 known vulnerabilities
```

---

**2. assess_13_vectors**
Full epistemic state assessment across all 13 dimensions.

**Example usage:**
```
Use Empirica to assess my current understanding of this database schema.
```

---

**3. investigate_strategic**
Strategic investigation with tool recommendations.

**Example usage:**
```
Use Empirica to investigate the best approach for implementing rate limiting.
```

---

**4. monitor_session**
View current session tracking and cognitive state.

**Example usage:**
```
Show me the Empirica session monitoring for this conversation.
```

---

#### Supporting Tools

- `bayesian_update` - Update belief with new evidence
- `drift_check` - Detect behavioral integrity issues
- `tool_recommend` - Get AI-powered tool suggestions
- `necessity_assess` - Multi-phase planning assessment
- `session_export` - Export session data
- `reflex_frame_view` - View cognitive snapshots
- `vector_delta` - Compare pre/post-flight uncertainty
- `collaboration_sync` - Multi-AI state sharing
- `temporal_continuity` - Cross-session awareness
- `benchmark_cognitive` - Run epistemic benchmarks

---

### Usage Patterns Section
**Title:** How to Work with Empirica in Claude

#### Pattern 1: Decision Support
```
You: "I'm considering deploying this code to production. 
     All tests pass but I'm uncertain about edge cases."

Claude: Let me use Empirica to assess this decision.

[Claude calls cascade_run_full]

Empirica Result:
  Action: investigate
  Confidence: 0.62
  Rationale: Edge case concern valid - need to review 
             error handling and timeout scenarios
  
  Recommended investigation:
  1. Error handling analysis
  2. Timeout scenario testing
  3. Load testing review

Claude: Based on Empirica's assessment, I recommend 
        investigating error handling and edge cases before
        deployment. Would you like me to help analyze these?
```

---

#### Pattern 2: Knowledge Gap Detection
```
You: "Explain how our caching layer works"

Claude: Let me assess my knowledge with Empirica first.

[Claude calls assess_13_vectors with topic: "caching layer"]

Empirica Result:
  KNOW: 0.35 ⚠️ - Limited knowledge
  CONTEXT: 0.20 ⚠️ - Insufficient context
  Recommendation: INVESTIGATE

Claude: I have limited knowledge of your specific caching
        implementation. Let me investigate:
        
[Claude calls investigate_strategic]

Empirica suggests:
  1. Review caching configuration files
  2. Check cache-related code
  3. Look for documentation

Claude: Could you point me to the caching configuration 
        or relevant code files?
```

---

#### Pattern 3: Multi-Phase Planning
```
You: "Help me build a new API endpoint for user authentication"

Claude: Let me use Empirica to plan this in phases.

[Claude calls necessity_assess]

Empirica Phase Plan:
  Phase 1 (CRITICAL): Requirements gathering
    - What authentication method? (OAuth, JWT, etc.)
    - What user data needs protection?
    - What are rate limiting requirements?
    
  Phase 2 (HIGH): Design
    - API endpoint structure
    - Security considerations
    - Error handling
    
  Phase 3 (MEDIUM): Implementation
    - Code the endpoint
    - Write tests
    
  Phase 4 (HIGH): Validation
    - Security review
    - Performance testing

Claude: Empirica identified 4 phases. Let's start with Phase 1
        requirements. What authentication method do you prefer?
```

---

### Auto-tracking with MCP Section
**Title:** Automatic Cognitive Monitoring

**What Gets Tracked:**
Every interaction through the MCP server automatically records:

1. **Epistemic Assessments**
   - Pre-flight vector state
   - Post-flight vector state
   - Δuncertainty measurements

2. **Investigation Trails**
   - Tools selected
   - Evidence gathered
   - Confidence changes

3. **Session Continuity**
   - Cross-conversation learning
   - Temporal awareness
   - Pattern recognition

4. **Reflex Frames**
   - Cognitive snapshots at key moments
   - Decision reasoning
   - Uncertainty evolution

**View tracking:**
```
Can you show me the Empirica session tracking?

[Claude calls monitor_session]

Session: dc8e7460-7c01-45aa-b1bb-848124acd13f
Duration: 45 minutes
Interactions: 12
Investigations: 3
Avg confidence: 0.72 → 0.84 (improved)
Learning confirmed: Yes (Δuncertainty: -0.12)
```

---

### Configuration Section
**Title:** MCP Server Configuration

#### Environment Variables

**In config:**
```json
{
  "mcpServers": {
    "empirica": {
      "command": "python3",
      "args": ["empirica_mcp_server.py"],
      "env": {
        "EMPIRICA_AUTO_BOOTSTRAP": "optimal",
        "EMPIRICA_CONFIDENCE_THRESHOLD": "0.7",
        "EMPIRICA_AUTO_DASHBOARD": "false",
        "EMPIRICA_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

---

#### Server Options

**EMPIRICA_AUTO_BOOTSTRAP**
- `optimal` - Full capabilities (recommended)
- `extended` - Standard features
- `minimal` - Lightweight

**EMPIRICA_CONFIDENCE_THRESHOLD**
- Default: `0.7`
- Range: `0.0` to `1.0`
- Higher = more conservative

**EMPIRICA_AUTO_DASHBOARD**
- `true` - Auto-start tmux dashboard
- `false` - Manual dashboard (recommended)

**EMPIRICA_LOG_LEVEL**
- `DEBUG` - Verbose logging
- `INFO` - Standard logging
- `WARNING` - Errors only

---

### Dashboard Integration Section
**Title:** Visual Monitoring with Tmux

**Enable dashboard:**
```json
{
  "env": {
    "EMPIRICA_AUTO_DASHBOARD": "true"
  }
}
```

**Or start manually:**
```bash
# In terminal
tmux new -s empirica-dashboard
empirica dashboard start

# Continue working in Claude Desktop
# Dashboard shows live updates
```

**Dashboard shows:**
- Real-time vector changes
- Cascade phase progression
- Investigation rounds
- Bayesian updates
- Drift detection alerts
- Session continuity

---

### Custom MCP Clients Section
**Title:** Using Empirica with Other MCP Clients

**Any MCP-compatible client can connect:**

```python
import mcp

# Connect to Empirica
client = mcp.Client()
await client.connect(
    command="python3",
    args=["empirica_mcp_server.py"]
)

# Call tools
result = await client.call_tool(
    "cascade_run_full",
    {
        "question": "Should I proceed?",
        "enable_dashboard": True
    }
)

print(result)
```

---

### Troubleshooting Section
**Title:** Common MCP Issues

#### Server Not Starting

**Check logs:**
```bash
# macOS/Linux
tail -f ~/Library/Logs/Claude/mcp*.log

# Or run manually
python3 /path/to/empirica_mcp_server.py
```

**Common issues:**
- Python path incorrect in config
- Missing dependencies (`pip install -r requirements.txt`)
- File permissions on empirica_mcp_server.py

---

#### Tools Not Appearing in Claude

**Verify connection:**
1. Restart Claude Desktop completely
2. Check config JSON syntax (use JSONLint.com)
3. Ensure absolute paths, not relative
4. Check Claude Desktop version (need latest)

---

#### Auto-bootstrap Failing

**Manual bootstrap:**
```bash
cd empirica
empirica bootstrap --mode optimal
```

Then restart Claude Desktop.

---

#### Performance Issues

**Reduce logging:**
```json
{
  "env": {
    "EMPIRICA_LOG_LEVEL": "WARNING"
  }
}
```

**Disable dashboard:**
```json
{
  "env": {
    "EMPIRICA_AUTO_DASHBOARD": "false"
  }
}
```

---

### Best Practices Section
**Title:** MCP Integration Best Practices

1. **Use Absolute Paths**
   - Never use `~` or relative paths in config
   - Use full path: `/Users/you/empirica/...`

2. **Enable Auto-bootstrap**
   - Ensures system ready on startup
   - Prevents initialization errors

3. **Manual Dashboard**
   - Set `AUTO_DASHBOARD: false`
   - Start manually when needed
   - Reduces resource usage

4. **Provide Rich Context**
   - Give Claude full context for decisions
   - Better context = better epistemic assessment

5. **Review Session Tracking**
   - Periodically check `monitor_session`
   - Verify learning is happening (Δuncertainty < 0)

---

### Next Steps CTA
**Title:** Start Using Empirica with Claude  
**Primary Button:** Configure MCP Now  
**Secondary Link:** View All MCP Tools  
**Tertiary Link:** Read Python API Docs

---

## Footer
Standard footer component
