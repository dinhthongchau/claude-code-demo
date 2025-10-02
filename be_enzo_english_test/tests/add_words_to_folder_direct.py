"""
Directly add words to folder via MongoDB to bypass API encoding issues.
"""

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

base_dir = Path(__file__).parent.parent  # Go up to be_enzo_english_test directory
load_dotenv(base_dir / ".env")

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("MONGO_DB_NAME")

print(f"Using MongoDB: {MONGO_URL}")
print(f"Database: {DB_NAME}\n")

# Test data
TEST_USER_ID = "dinhthongchau@gmail.com"
FOLDER_ID = "68dd31710fd9f8d89b0dd93b"  # Your existing folder
WORD_IDS = ["APPLE_001", "BANANA_002", "GRAPE_003", "ORANGE_004"]


async def add_words_to_folder():
    """Add words directly to user_folder_words collection."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db["user_folder_words"]

    print("📝 Adding words to folder directly in MongoDB...\n")

    success_count = 0
    for word_id in WORD_IDS:
        # Check if already exists
        existing = await collection.find_one(
            {"user_id": TEST_USER_ID, "folder_id": FOLDER_ID, "word_id": word_id}
        )

        if existing:
            print(f"⚠️  {word_id} already in folder, skipping")
            success_count += 1
            continue

        # Insert assignment
        now = datetime.utcnow()
        doc = {
            "word_id": word_id,
            "folder_id": FOLDER_ID,
            "user_id": TEST_USER_ID,
            "created_at": now,
            "updated_at": now,
        }

        result = await collection.insert_one(doc)
        if result.inserted_id:
            print(f"✅ Added {word_id} to folder")
            success_count += 1
        else:
            print(f"❌ Failed to add {word_id}")

    client.close()

    print(f"\n🎉 Success! Added {success_count}/{len(WORD_IDS)} words to folder")
    print("\n📱 Now open your Flutter app and you should see the words with images!")
    print(f"   Folder ID: {FOLDER_ID}")
    print(f"   User ID: {TEST_USER_ID}")


if __name__ == "__main__":
    asyncio.run(add_words_to_folder())
