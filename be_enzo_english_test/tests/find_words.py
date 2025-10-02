"""Find where the words are stored."""
import os
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Add UTF-8 encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Load environment
from dotenv import load_dotenv
base_dir = Path(__file__).parent.parent
load_dotenv(base_dir / ".env")

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("MONGO_DB_NAME")


async def find_words():
    """Find where words are stored."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print(f"Database: {DB_NAME}")
    print("=" * 60)
    
    # List all collections
    collections = await db.list_collection_names()
    print(f"Collections: {collections}\n")
    
    # Check each collection for our words
    word_ids = ["APPLE_001", "BANANA_002", "GRAPE_003", "ORANGE_004"]
    
    for coll_name in collections:
        collection = db[coll_name]
        for word_id in word_ids:
            doc = await collection.find_one({"word_id": word_id})
            if doc:
                print(f"✅ Found {word_id} in collection: {coll_name}")
                print(f"   Keys: {list(doc.keys())}")
                print(f"   Word: {doc.get('word')}")
                print()
    
    client.close()


if __name__ == "__main__":
    asyncio.run(find_words())

