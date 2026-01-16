import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp_hello")

@mcp.tool()
def say_hello() -> str:
    """Greets the current user based on the MCP_USER environment variable."""
    name = os.environ.get("MCP_USER", "Stranger")
    return f"Hello, nice to meet you, {name}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
