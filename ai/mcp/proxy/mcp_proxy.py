import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Add siblings to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent / "weather"))
sys.path.append(str(current_dir.parent / "timer"))

# Import logic
from mcp_weather import get_weather as weather_logic
from mcp_timer import get_time as timer_logic

# Initialize Server
mcp = FastMCP("mcp_secure_proxy")

@mcp.tool()
def get_weather(city: str, user_name: str) -> str:
    """
    Get weather for a city.
    :param city: The city name.
    :param user_name: The name of the user requesting access.
    """
    user_name = user_name.upper().strip()
    print(f"DEBUG: Auth request for User='{user_name}' -> Service='weather'", file=sys.stderr)
    
    if user_name == "X":
        return weather_logic(city)
    else:
        return f"⛔ ACCESS DENIED: User '{user_name}' is not authorized for weather."

@mcp.tool()
def get_time(city: str, user_name: str) -> str:
    """
    Get time for a city.
    :param city: The city name.
    :param user_name: The name of the user requesting access.
    """
    user_name = user_name.upper().strip()
    print(f"DEBUG: Auth request for User='{user_name}' -> Service='timer'", file=sys.stderr)

    if user_name == "Y":
        return timer_logic(city)
    else:
        return f"⛔ ACCESS DENIED: User '{user_name}' is not authorized for timer."

if __name__ == "__main__":
    mcp.run(transport="stdio")
