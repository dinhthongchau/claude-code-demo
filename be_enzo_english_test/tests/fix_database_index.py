"""Fix the database index from old wordId to new word_id."""
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


async def fix_indexes():
    """Fix database indexes."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db["words"]
    
    print("🔧 Fixing database indexes...\n")
    
    # Get current indexes
    indexes = await collection.index_information()
    print(f"Current indexes: {list(indexes.keys())}\n")
    
    # Drop old wordId index if exists
    if "wordId_1" in indexes:
        await collection.drop_index("wordId_1")
        print("✅ Dropped old 'wordId_1' index")
    
    # Create new word_id index
    await collection.create_index("word_id", unique=True, sparse=True)
    print("✅ Created new 'word_id' index (unique, sparse)")
    
    # Show new indexes
    indexes = await collection.index_information()
    print(f"\nNew indexes: {list(indexes.keys())}")
    
    client.close()
    print("\n🎉 Done! Now run create_words_in_db.py again")


if __name__ == "__main__":
    asyncio.run(fix_indexes())

