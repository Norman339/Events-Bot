import os
import json
import random
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    from motor.motor_asyncio import AsyncIOMotorClient
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False

class Database:
    def __init__(self, use_mongodb: bool = True):
        self.use_mongodb = use_mongodb and MONGO_AVAILABLE
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        if self.use_mongodb:
            self._init_mongodb()
        else:
            self._init_json_storage()
    
    def _init_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            self.client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
            self.db = self.client.get_database("cyberbot_db")
            self.events_collection = self.db.events
            self.facts_collection = self.db.facts
            print("Using MongoDB for data storage")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}. Falling back to JSON storage.")
            self.use_mongodb = False
            self._init_json_storage()
    
    def _init_json_storage(self):
        """Initialize JSON file storage"""
        self.events_file = self.data_dir / "events.json"
        self.facts_file = self.data_dir / "facts.json"
        
        # Initialize files if they don't exist
        if not self.events_file.exists():
            self.events_file.write_text("[]")
        if not self.facts_file.exists():
            default_facts = [
                "The first computer virus was created in 1971 and was called 'Creeper'.",
                "Phishing attacks account for more than 80% of reported security incidents.",
                "A strong password should be at least 12 characters long.",
                "Multi-factor authentication (MFA) can prevent 99.9% of account compromise attacks.",
                "The cost of cybercrime is expected to reach $10.5 trillion annually by 2025."
            ]
            self.facts_file.write_text(json.dumps(default_facts, indent=2))
        
        print("Using JSON files for data storage")
    
    # Event methods
    async def add_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        if self.use_mongodb:
            await self.events_collection.insert_one(event_data)
        else:
            events = self._read_json(self.events_file)
            events.append(event_data)
            self._write_json(self.events_file, events)
        return event_data
    
    async def get_events(self) -> List[Dict[str, Any]]:
        if self.use_mongodb:
            return await self.events_collection.find().sort("date", 1).to_list(length=100)
        else:
            return self._read_json(self.events_file)
    
    async def remove_event(self, title: str) -> bool:
        if self.use_mongodb:
            result = await self.events_collection.delete_one(
                {"title": {"$regex": f"^{title}$", "$options": "i"}}
            )
            return result.deleted_count > 0
        else:
            events = self._read_json(self.events_file)
            initial_length = len(events)
            events = [e for e in events if e["title"].lower() != title.lower()]
            if len(events) < initial_length:
                self._write_json(self.events_file, events)
                return True
            return False
    
    # Fact methods
    async def add_fact(self, fact: str) -> None:
        if self.use_mongodb:
            await self.facts_collection.insert_one({"text": fact})
        else:
            facts = self._read_json(self.facts_file)
            if fact not in facts:
                facts.append(fact)
                self._write_json(self.facts_file, facts)
    
    async def get_random_fact(self) -> Optional[str]:
        if self.use_mongodb:
            count = await self.facts_collection.count_documents({})
            if count == 0:
                return None
            random_skip = random.randint(0, count - 1)
            fact = await self.facts_collection.find().skip(random_skip).limit(1).to_list(1)
            return fact[0]["text"] if fact else None
        else:
            facts = self._read_json(self.facts_file)
            return random.choice(facts) if facts else None
    
    async def initialize_default_facts(self):
        if self.use_mongodb:
            default_facts = [
                "The first computer virus was created in 1971 and was called 'Creeper'.",
                "Phishing attacks account for more than 80% of reported security incidents.",
                "A strong password should be at least 12 characters long.",
                "Multi-factor authentication (MFA) can prevent 99.9% of account compromise attacks.",
                "The cost of cybercrime is expected to reach $10.5 trillion annually by 2025."
            ]
            for fact in default_facts:
                if not await self.facts_collection.find_one({"text": fact}):
                    await self.add_fact(fact)
    
    # Helper methods for JSON storage
    def _read_json(self, file_path: Path) -> Any:
        try:
            return json.loads(file_path.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_json(self, file_path: Path, data: Any) -> None:
        file_path.write_text(json.dumps(data, indent=2))

# Create a single database instance
# Set to False to use JSON storage instead of MongoDB
db = Database(use_mongodb=False)

# Initialize default facts when module loads
import asyncio
if not MONGO_AVAILABLE:
    # For JSON storage, we don't need to initialize facts as they're in the file
    pass