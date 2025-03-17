from threading import Lock
from config import logger
from http_client import HTTPClient

class AgentManager:
    def __init__(self):
        self.data_store = {}
        self.lock = Lock()
        self.http_client = HTTPClient()

    async def send_agent_data(self, input_data: dict) -> str:
        if "agent_type" not in input_data:
            raise ValueError("Agent type not found in input data")
            
        tracking_key = await self.http_client.send_data(input_data)
        with self.lock:
            self.data_store[tracking_key] = {
                "agent_type": input_data["agent_type"],
                "input_data": input_data,
                "status": "PENDING",
                "logs": [],
                "output_data": None
            }
        logger.info(f"Sent data to agent, received tracking key: {tracking_key}")
        return tracking_key

    async def receive_agent_data(self, tracking_key: str, query: str, response_type: str):
        async for data in self.http_client.receive_data(tracking_key, query, response_type):
            if tracking_key in self.data_store:
                with self.lock:
                    self.data_store[tracking_key].update({
                        "agent_type": data.get("agent_type"),
                        "input_data": data.get("input_data"),
                        "status": data.get("status", "PENDING"),
                        "logs": data.get("logs", []),
                        "output_data": data.get("output")
                    })
            yield data

    async def get_agent_status(self, tracking_key: str) -> dict:
        data = await self.http_client.get_status(tracking_key)
        if tracking_key in self.data_store:
            with self.lock:
                self.data_store[tracking_key].update({
                    "status": data.get("status", "PENDING"),
                    "logs": data.get("logs", []),
                    "output_data": data.get("output")
                })
        return data