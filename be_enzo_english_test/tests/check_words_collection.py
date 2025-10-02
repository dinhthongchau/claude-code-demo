"""Check what's in the words collection."""
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


async def check_words():
    """Check words collection."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db["words"]
    
    # Count total
    count = await collection.count_documents({})
    print(f"Total words in collection: {count}\n")
    
    # Get all words
    words = await collection.find({}).to_list(100)
    for word in words:
        print(f"word_id: {word.get('word_id')}, word: {word.get('word')}")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(check_words())

