#!/usr/bin/env python3
import asyncio
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from tzlocal import get_localzone_name

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("mcp-time")

# -----------------------------
# list tools
# -----------------------------
@server.list_tools()
async def list_tools() -> list[Tool]:
    local_tz = get_localzone_name() or "UTC"
    return [
        Tool(
            name="get_current_time",
            description="Return current time in given timezone (IANA), or local timezone if none provided.",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "description": "IANA timezone, e.g. 'Europe/London'"}
                },
                "required": []
            },
        )
    ]

# -----------------------------
# call tool
# -----------------------------
@server.call_tool()
async def call_tool(name: str, args: dict) -> list[TextContent]:
    if name == "get_current_time":
        tz = args.get("timezone") or (get_localzone_name() or "UTC")
        tzinfo = ZoneInfo(tz)
        now = datetime.now(tzinfo)
        result = {
            "timezone": tz,
            "datetime": now.isoformat(timespec="seconds"),
            "day_of_week": now.strftime("%A"),
            "is_dst": bool(now.dst()),
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        raise ValueError(f"Unknown tool: {name}")

# -----------------------------
# run MCP server using stdio
# -----------------------------
async def main():
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

if __name__ == "__main__":
    asyncio.run(main())
