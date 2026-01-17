import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Add sibling directories to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent / "weather"))
sys.path.append(str(current_dir.parent / "timer"))

try:
    from mcp_weather import get_weather as weather_logic
    from mcp_timer import get_time as timer_logic
except ImportError as e:
    print(f"Error importing services: {e}", file=sys.stderr)
    sys.exit(1)

# Initialize the Proxy Server
mcp = FastMCP("mcp_proxy")

@mcp.tool()
def secure_gateway(user_name: str, service_requested: str, city: str) -> str:
    """
    Gateway to access protected services.
    
    Args:
        user_name: The name of the user requesting access (e.g. "X" or "Y").
        service_requested: The service to use (e.g., "weather", "timer", "time").
        city: The city name.
    """
    user_name = user_name.upper().strip()
    service_requested = service_requested.lower().strip()

    # --- Debugging ---
    # This print will show up in LM Studio logs if you need to debug
    print(f"DEBUG: User='{user_name}', Service='{service_requested}', City='{city}'")

    # --- Logic ---
    if user_name == "X" and "weather" in service_requested:
        return weather_logic(city)
    
    elif user_name == "Y" and ("timer" in service_requested or "time" in service_requested):
        return timer_logic(city)
    
    else:
        return f"ACCESS DENIED: User '{user_name}' is not allowed to use '{service_requested}'. (Hint: User X -> Weather, User Y -> Timer)"

if __name__ == "__main__":
    mcp.run(transport="stdio")
