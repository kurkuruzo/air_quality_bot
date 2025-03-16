import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Bot token from environment variable
BOT_TOKEN = os.environ["BOT_TOKEN"]
IQAIR_API_KEY = os.environ["IQAIR_API_KEY"]
IQAIR_API_URL = "https://api.airvisual.com/v2" 