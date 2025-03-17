import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('agentcraft')

# Load environment variables
load_dotenv()
BEARER_TOKEN = os.getenv("AGENTCRAFT_BEARER_TOKEN")
if not BEARER_TOKEN:
    raise ValueError("AGENTCRAFT_BEARER_TOKEN not found in .env file")

DEV_BASE_URL = "127.0.0.1:8000"
PROD_BASE_URL = "api.we-crafted.com"
BASE_URL = PROD_BASE_URL if os.getenv('ENVIRONMENT') == 'PRODUCTION' else DEV_BASE_URL