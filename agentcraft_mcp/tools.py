from mcp.types import Tool, TextContent
from typing import List

def get_tools() -> List[Tool]:
    return [
        Tool(name="send_agent_data", description="Send data to an agent", inputSchema={
            "type": "object",
            "properties": {"prompt": {"type": "string"}},
            "required": ["prompt"]
        }),
        Tool(name="receive_agent_data", description="Receive data from an agent", inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "tracking_key": {"type": "string"},
                "response_type": {"type": "string", "default": "markdown"}
            },
            "required": ["query"]
        }),
        Tool(name="get_available_agents", description="Get the list of available agents", inputSchema={
            "type": "object",
            "properties": {}
        })
    ]