from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp_weather")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get the weather for a specific city."""
    city_lower = city.lower()
    if city_lower == "austin":
        return "60F"
    elif city_lower == "phoenix":
        return "100F"
    else:
        return "Unknown city"

if __name__ == "__main__":
    mcp.run(transport="stdio")
