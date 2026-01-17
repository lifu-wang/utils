from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with dependencies
mcp = FastMCP("mcp_http_hello", dependencies=["uvicorn"])

@mcp.tool()
def say_hello_http(name: str) -> str:
    """Say hello over HTTP."""
    print(f"DEBUG: Received request for {name}")
    return f"Hello, {name}! I am speaking to you via HTTP/SSE."

if __name__ == "__main__":
    # Start the server on port 8000
    mcp.run(transport="sse")
