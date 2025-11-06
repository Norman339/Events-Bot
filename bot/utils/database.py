import os
import random
from typing import List, Dict, Any, Optional

try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from pymongo import ReturnDocument  # needed for MongoDB modify
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False


class Database:
    def __init__(self, use_mongodb: bool = True):
        if not MONGO_AVAILABLE:
            raise ImportError("MongoDB drivers not available. Ensure 'motor' and 'pymongo' are installed.")
        self.use_mongodb = True  # Force MongoDB-only
        self._init_mongodb()

    def _init_mongodb(self):
        """Initialize MongoDB connection"""
        self.client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
        self.db = self.client.get_database("cyberbot_db")
        self.events_collection = self.db.events
        self.facts_collection = self.db.facts
        print("✅ Using MongoDB for data storage")

    # JSON storage removed: MongoDB-only backend

    # -----------------------------
    # Event methods
    # -----------------------------

    async def add_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        await self.events_collection.insert_one(event_data)
        return event_data

    async def get_events(self) -> List[Dict[str, Any]]:
        return await self.events_collection.find().sort("date", 1).to_list(length=100)

    async def remove_event(self, title: str) -> bool:
        result = await self.events_collection.delete_one(
            {"title": {"$regex": f"^{title}$", "$options": "i"}}
        )
        return result.deleted_count > 0

    async def clear_events(self) -> None:
        """Clear all events"""
        await self.events_collection.delete_many({})

    async def modify_event(
        self,
        title: str,
        new_title: Optional[str] = None,
        new_description: Optional[str] = None,
        new_date: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Modify an existing event"""
        updates = {}
        if new_title:
            updates["title"] = new_title
        if new_date:
            updates["date"] = new_date
        if new_description:
            updates["description"] = new_description

        if not updates:
            return None

        updated = await self.events_collection.find_one_and_update(
            {"title": {"$regex": f"^{title}$", "$options": "i"}},
            {"$set": updates},
            return_document=ReturnDocument.AFTER
        )
        return updated

    # -----------------------------
    # Fact methods
    # -----------------------------

    async def add_fact(self, fact: str) -> None:
        await self.facts_collection.insert_one({"text": fact})

    async def get_random_fact(self) -> Optional[str]:
        count = await self.facts_collection.count_documents({})
        if count == 0:
            return None
        random_skip = random.randint(0, count - 1)
        fact = await self.facts_collection.find().skip(random_skip).limit(1).to_list(1)
        return fact[0]["text"] if fact else None

    async def get_all_facts(self) -> List[str]:
        """Return all facts as a list of strings, ordered by insertion."""
        docs = await self.facts_collection.find({}, {"text": 1, "_id": 0}).to_list(length=1000)
        return [d.get("text", "") for d in docs]

    async def remove_fact(self, fact_text: str) -> bool:
        """Remove a fact by exact text (case-insensitive). Returns True if removed."""
        result = await self.facts_collection.delete_one({
            "text": {"$regex": f"^{fact_text}$", "$options": "i"}
        })
        return result.deleted_count > 0

    async def initialize_default_facts(self) -> None:
        """Ensure default facts exist in MongoDB."""
        count = await self.facts_collection.count_documents({})
        if count == 0:
            default_facts = [
                "The first computer virus was created in 1971 and was called 'Creeper'.",
                "Phishing attacks account for more than 80% of reported security incidents.",
                "A strong password should be at least 12 characters long.",
                "Multi-factor authentication (MFA) can prevent 99.9% of account compromise attacks.",
                "The cost of cybercrime is expected to reach $10.5 trillion annually by 2025."
            ]
            await self.facts_collection.insert_many([{ "text": f } for f in default_facts])

    # -----------------------------
    # Helpers
    # -----------------------------

    # JSON helpers removed


# Create global instance (MongoDB-only)
db = Database(use_mongodb=True)
