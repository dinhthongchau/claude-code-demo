"""Find which collection has the folders."""

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


async def find_folders():
    """Find folders in all collections."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    # List all collections
    collections = await db.list_collection_names()
    print(f"Database: {DB_NAME}")
    print(f"Collections: {collections}\n")

    # Check each collection for folders
    for coll_name in collections:
        collection = db[coll_name]

        # Try to find documents with user_id
        docs = await collection.find({"user_id": TEST_USER_ID}).to_list(10)

        if docs:
            print(f"Collection: {coll_name} ({len(docs)} documents)")
            for doc in docs:
                if "name" in doc:
                    print(f"  - {doc.get('name')} (ID: {doc.get('_id')})")
            print()

    client.close()


if __name__ == "__main__":
    asyncio.run(find_folders())

