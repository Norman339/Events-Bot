import os
from dotenv import load_dotenv
import os

# Load .env from project root and override any existing shell env
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)

class Config:
    TOKEN = os.getenv("DISCORD_TOKEN")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DEFAULT_PREFIX = "!"
    
    @classmethod
    def verify_config(cls):
        if not cls.TOKEN:
            raise ValueError("DISCORD_TOKEN is not set in environment variables")
        return True
