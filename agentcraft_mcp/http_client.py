import http.client
import json
import aiohttp
from config import BASE_URL, BEARER_TOKEN, logger

class HTTPClient:
    @staticmethod
    async def send_data(input_data: dict, endpoint="/api/run/") -> str:
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}',
            'Content-Type': 'application/json'
        }
        url = f"http://{BASE_URL}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=input_data, headers=headers) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to send data: {response.status} - {await response.text()}")
                response_json = await response.json()
                tracking_key = response_json.get("tracking_key")
                if not tracking_key:
                    raise ValueError("Server response did not include a tracking_key")
                return tracking_key

    @staticmethod
    async def receive_data(tracking_key: str, query: str, response_type="markdown"):
        url = f"http://{BASE_URL}/api/agent-stream/{tracking_key}/?query={query}"
        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to connect to agent_stream: {response.status}")
                    
                async for line in response.content:
                    if line.startswith(b"data: "):
                        yield json.loads(line[len(b"data: "):].decode('utf-8'))

    @staticmethod
    async def get_status(tracking_key: str) -> dict:
        url = f"http://{BASE_URL}/api/agent-stream/{tracking_key}/"
        headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to fetch agent status: {response.status}")
                    
                async for line in response.content:
                    if line.startswith(b"data: "):
                        return json.loads(line[len(b"data: "):].decode('utf-8'))
                raise ValueError(f"No data received for tracking_key: {tracking_key}")