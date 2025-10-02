"""Create words directly in the database with proper structure."""
import os
import sys
from pathlib import Path
from datetime import datetime
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


async def create_words():
    """Create words directly in database."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db["words"]
    
    words = [
        {
            "word_id": "APPLE_001",
            "word": "apple",
            "definition": "A round red or green fruit that grows on trees",
            "example": "I ate a delicious apple for breakfast",
            "image_url": "image_users/APPLE_001.jpg",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "word_id": "BANANA_002",
            "word": "banana",
            "definition": "A long yellow fruit with soft sweet flesh",
            "example": "She peeled a banana and ate it",
            "image_url": "image_users/BANANA_002.jpg",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "word_id": "GRAPE_003",
            "word": "grape",
            "definition": "A small round fruit that grows in clusters",
            "example": "The grapes were sweet and juicy",
            "image_url": "image_users/GRAPE_003.jpg",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "word_id": "ORANGE_004",
            "word": "orange",
            "definition": "A round citrus fruit with thick orange skin",
            "example": "I squeezed fresh orange juice this morning",
            "image_url": "image_users/ORANGE_004.jpg",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
    ]
    
    print("📝 Creating words in database...\n")
    
    for word_data in words:
        # Check if exists
        existing = await collection.find_one({"word_id": word_data["word_id"]})
        if existing:
            print(f"⚠️  {word_data['word_id']} already exists, skipping")
            continue
        
        # Insert
        result = await collection.insert_one(word_data)
        if result.inserted_id:
            print(f"✅ Created: {word_data['word']} ({word_data['word_id']})")
        else:
            print(f"❌ Failed: {word_data['word_id']}")
    
    client.close()
    print("\n🎉 Done! Now try your Flutter app again!")


if __name__ == "__main__":
    asyncio.run(create_words())

