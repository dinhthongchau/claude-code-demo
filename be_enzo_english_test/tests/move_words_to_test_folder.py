"""Move test words to Test Folder."""

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

TEST_USER_ID = "dinhthongchau@gmail.com"
TEST_FOLDER_ID = "68ddfd892672034cf5484e2e"  # Test Folder ID
WORD_IDS = ["APPLE_001", "BANANA_002", "GRAPE_003", "ORANGE_004"]


async def move_words():
    """Move words to Test Folder."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    user_folder_words_collection = db["user_folder_words"]

    print("📝 Moving words to Test Folder...\n")

    # First, delete all existing assignments for this user
    delete_result = await user_folder_words_collection.delete_many(
        {"user_id": TEST_USER_ID}
    )
    print(f"🗑️  Deleted {delete_result.deleted_count} existing word assignments\n")

    # Add words to Test Folder
    for word_id in WORD_IDS:
        now = datetime.utcnow()
        assignment_doc = {
            "word_id": word_id,
            "folder_id": TEST_FOLDER_ID,
            "user_id": TEST_USER_ID,
            "created_at": now,
            "updated_at": now,
        }

        result = await user_folder_words_collection.insert_one(assignment_doc)
        if result.inserted_id:
            print(f"✅ Added {word_id} to Test Folder")
        else:
            print(f"❌ Failed to add {word_id}")

    print("\n🎉 Success! Words moved to Test Folder")
    print("\n📱 Now test in Flutter:")
    print("   Folder: Test Folder")
    print(f"   Folder ID: {TEST_FOLDER_ID}")
    print(f"   User ID: {TEST_USER_ID}")
    print("\n🔍 Test API endpoint:")
    print(
        f"   http://localhost:8829/api/v1/users/{TEST_USER_ID}/folders/{TEST_FOLDER_ID}/words"
    )

    client.close()


if __name__ == "__main__":
    asyncio.run(move_words())
