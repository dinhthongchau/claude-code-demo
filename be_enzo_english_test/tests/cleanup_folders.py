"""Remove all folders except 'Test Folder'."""

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
KEEP_FOLDER_NAME = "Test Folder"


async def cleanup_folders():
    """Remove all folders except 'Test Folder'."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    folders_collection = db["folders"]
    user_folder_words_collection = db["user_folder_words"]

    print("🗑️  Cleaning up folders...\n")

    # Get all folders
    all_folders = await folders_collection.find({"user_id": TEST_USER_ID}).to_list(100)
    print(f"Found {len(all_folders)} folders total\n")

    folders_to_delete = []
    folder_to_keep = None

    for folder in all_folders:
        folder_name = folder.get("name", "")
        folder_id = str(folder["_id"])

        if folder_name == KEEP_FOLDER_NAME:
            folder_to_keep = folder
            print(f"✅ Keeping: {folder_name} (ID: {folder_id})")
        else:
            folders_to_delete.append(folder)
            print(f"🗑️  Will delete: {folder_name} (ID: {folder_id})")

    print(f"\n{'='*60}")
    print(f"Deleting {len(folders_to_delete)} folders...")
    print(f"{'='*60}\n")

    for folder in folders_to_delete:
        folder_id = str(folder["_id"])

        # Delete associated word assignments
        assignments_result = await user_folder_words_collection.delete_many(
            {"folder_id": folder_id, "user_id": TEST_USER_ID}
        )
        print(
            f"  - Deleted {assignments_result.deleted_count} word assignments for '{folder['name']}'"
        )

        # Delete folder
        await folders_collection.delete_one({"_id": folder["_id"]})
        print(f"  - Deleted folder '{folder['name']}'")

    print(f"\n{'='*60}")
    print("✅ Cleanup complete!")
    print(f"{'='*60}")

    if folder_to_keep:
        print("\n📁 Remaining folder:")
        print(f"   Name: {folder_to_keep['name']}")
        print(f"   ID: {str(folder_to_keep['_id'])}")
        print(f"   Description: {folder_to_keep.get('description', 'N/A')}")

        # Count words in the kept folder
        word_count = await user_folder_words_collection.count_documents(
            {"folder_id": str(folder_to_keep["_id"]), "user_id": TEST_USER_ID}
        )
        print(f"   Words: {word_count}")
    else:
        print("\n⚠️  Warning: 'Test Folder' was not found!")

    client.close()


if __name__ == "__main__":
    asyncio.run(cleanup_folders())

