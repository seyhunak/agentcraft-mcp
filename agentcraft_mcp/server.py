import sys
import os
sys.path.append(os.path.dirname(__file__))

import json
import yaml
import asyncio
import uuid
from typing import Dict

import mcp.server.stdio
from mcp.server import Server
from mcp.types import TextContent

from config import logger, BEARER_TOKEN
from tools import get_tools
from data_processor import DataProcessor
from agent_manager import AgentManager

class AgentCraftServer(Server):
    def __init__(self):
        super().__init__(name="agentcraft-server")
        self.bearer_token = BEARER_TOKEN
        self.data_processor = DataProcessor()
        self.agent_manager = AgentManager()
        logger.info("AgentCraftServer initialized with agents: %s", list(self.data_processor.agents.keys()))

        @self.list_tools()
        async def handle_tools():
            return get_tools()

        @self.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            try:
                logger.debug(f"Tool called: {name} with arguments: {arguments}")

                if name in ["send_agent_data"]:
                    input_data = self.data_processor.translate_prompt_to_input_data(arguments["prompt"])
                    tracking_key = await self.agent_manager.send_agent_data(input_data)
                    return [TextContent(type="text", text=f"Tracking key: {tracking_key}")]

                elif name in ["receive_agent_data"]:
                    tracking_key = self.get_tracking_key(arguments)
                    logger.info(f"Resolved tracking_key: {tracking_key}")

                    if not tracking_key:
                        return [TextContent(type="text", text="Error: No valid tracking_key found")]
                    updates = []
                    async for update in self.agent_manager.receive_agent_data(
                        tracking_key,
                        arguments.get("query", "fetch"),
                        arguments.get("response_type", "markdown")
                    ):
                        updates.append(update)
                    if not updates:
                        return [TextContent(type="text", text="No data received")]
                    return [TextContent(type="text", text=json.dumps(updates[-1]))]

                elif name in ["status_agent_data"]:
                    tracking_key = self.get_tracking_key(arguments)
                    if not tracking_key:
                        return [TextContent(type="text", text="Error: Please provide a tracking_key")]
                    update = await self.agent_manager.get_agent_status(tracking_key)
                    return [TextContent(type="text", text=json.dumps(update))]

                elif name in ["get_available_agents"]:
                    return [TextContent(type="text", text=yaml.dump(self.data_processor.agents))]

                raise ValueError(f"Unknown tool name: {name}")

            except ValueError as e:
                logger.error(f"ValueError in tool {name}: {str(e)}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
            except Exception as e:
                logger.error(f"Unexpected error in tool {name}: {str(e)}", exc_info=True)
                return [TextContent(type="text", text="Internal server error")]

    # Tracking key
    def get_tracking_key(self, arguments: dict) -> str | None:
        with self.agent_manager.lock:
            # Step 1: Check self.agent_manager.data_store first
            if self.agent_manager.data_store:
                tracking_key = next(iter(self.agent_manager.data_store), None)
                if tracking_key:
                    try:
                        uuid.UUID(tracking_key)  # Validate UUID format
                        logger.debug(f"Using tracking_key from data_store: {tracking_key}")
                        return tracking_key
                    except ValueError:
                        logger.error(f"Invalid UUID in data_store: {tracking_key}")

            # Step 2: Fall back to arguments if data_store doesn’t provide a valid UUID
            tracking_key = arguments.get("tracking_key")
            if tracking_key:
                try:
                    uuid.UUID(tracking_key)  # Validate UUID format
                    logger.debug(f"Using tracking_key from arguments: {tracking_key}")
                    return tracking_key
                except ValueError:
                    logger.error(f"Invalid tracking_key in arguments: {tracking_key}")
                    return None

        # Return None if no valid tracking_key is found
        return None

async def main():
    try:
        server = AgentCraftServer()
        initialization_options = server.create_initialization_options()
        logger.info("Starting server")

        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, initialization_options)
    except Exception as e:
        logger.critical(f"Server failed: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Server shutting down")

if __name__ == "__main__":
    print("AGENTCRAFT_BEARER_TOKEN:", os.getenv("AGENTCRAFT_BEARER_TOKEN"))
    print("ENVIRONMENT:", os.getenv("ENVIRONMENT"))
    
    asyncio.run(main())