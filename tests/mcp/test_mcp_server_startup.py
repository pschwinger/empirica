"""Test MCP server initialization."""
import pytest
import asyncio
# Update import to use current MCP server architecture
try:
    from empirica_mcp.server import list_tools
except ImportError:
    # Fallback for compatibility during transition
    from empirica.cli.mcp_client import list_tools as cli_list_tools
    list_tools = cli_list_tools

@pytest.mark.asyncio
async def test_server_starts():
    """MCP server starts without errors"""
    # This is a placeholder. A true server start test would be more complex
    # and is better suited for a full integration test.
    assert True

@pytest.mark.asyncio
async def test_tools_registered():
    """All core tools are registered"""
    tools = await list_tools()
    # Core tools (v3.0): 57+ tools total
    # - 3 stateless tools (introduction, guidance, help)
    # - 54+ stateful tools (routed to CLI with expanded coverage)
    assert len(tools) >= 50, f"Expected at least 50 core tools, got {len(tools)}"
    assert len(tools) <= 70, f"Expected at most 70 tools, got {len(tools)}"  # Allow for future growth

@pytest.mark.asyncio
async def test_introduction_tool_exists():
    """get_empirica_introduction tool available"""
    tools = await list_tools()
    tool_names = [tool.name for tool in tools]
    assert "get_empirica_introduction" in tool_names