from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hello")

@mcp.tool()
def hello() -> str:
    """Returns a simple greeting."""
    return "HELLO LIFU"

if __name__ == "__main__":
    mcp.run(transport="stdio")
