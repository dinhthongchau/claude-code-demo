"""Check what's actually in the user_folder_words collection."""
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

TEST_USER_ID = "dinhthongchau@gmail.com"
FOLDER_ID = "68dd31710fd9f8d89b0dd93b"


async def check_folder_words():
    """Check what's in the database."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("=" * 60)
    print("Checking user_folder_words collection")
    print("=" * 60)
    
    # Check assignments
    collection = db["user_folder_words"]
    assignments = await collection.find({
        "user_id": TEST_USER_ID,
        "folder_id": FOLDER_ID
    }).to_list(100)
    
    print(f"\nFound {len(assignments)} assignments in database:")
    for a in assignments:
        print(f"  - word_id: {a['word_id']}, folder_id: {a['folder_id']}, user_id: {a['user_id']}")
    
    print("\n" + "=" * 60)
    print("Checking words collection")
    print("=" * 60)
    
    # Check words
    words_collection = db["words"]
    for a in assignments:
        word = await words_collection.find_one({"word_id": a["word_id"]})
        if word:
            print(f"\n✅ Found word: {word['word']}")
            print(f"   word_id: {word['word_id']}")
            print(f"   image_url: {word.get('image_url', 'None')}")
        else:
            print(f"\n❌ Word not found: {a['word_id']}")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(check_folder_words())

