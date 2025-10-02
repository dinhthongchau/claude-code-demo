"""List all folders in foldersList."""

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


async def list_folders():
    """List all folders."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    folders_collection = db["foldersList"]

    # Get all folders
    all_folders = await folders_collection.find({}).to_list(100)
    print(f"Total folders in foldersList: {len(all_folders)}\n")

    for folder in all_folders:
        print(f"Folder: {folder.get('name', 'N/A')}")
        print(f"  ID: {folder.get('_id')}")
        print(f"  user_id: {folder.get('user_id', 'N/A')}")
        print(f"  description: {folder.get('description', 'N/A')}")
        print()

    client.close()


if __name__ == "__main__":
    asyncio.run(list_folders())
