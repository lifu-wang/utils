from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp_timer")

@mcp.tool()
def get_time(city: str) -> str:
    """Get the time for a specific city."""
    city_lower = city.lower()
    if city_lower == "austin":
        return "3:00am"
    elif city_lower == "phoenix":
        return "1:00am"
    else:
        return "Unknown city"

if __name__ == "__main__":
    mcp.run(transport="stdio")
