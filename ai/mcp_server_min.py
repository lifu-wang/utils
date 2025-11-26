# file: mcp_server_minimal.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Tiny MCP Test Server")

@mcp.tool()
def read_file(path: str) -> str:
    """Dummy tool to test MCP integration."""
    return f"Fake content of {path}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Dummy tool to test MCP integration."""
    return f"Pretend wrote {len(content)} chars to {path}"

if __name__ == "__main__":
    # ✅ This starts the MCP server loop so Cline can connect
    mcp.run()

