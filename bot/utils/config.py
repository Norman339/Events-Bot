import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv("DISCORD_TOKEN")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DEFAULT_PREFIX = "!"
    
    @classmethod
    def verify_config(cls):
        if not cls.TOKEN:
            raise ValueError("DISCORD_TOKEN is not set in environment variables")
        return True
