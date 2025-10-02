"""Check the data type of folder_id in user_folder_words."""

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


async def check_types():
    """Check data types."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    collection = db["user_folder_words"]

    # Get one assignment
    assignment = await collection.find_one({"user_id": TEST_USER_ID})

    if assignment:
        print(f"folder_id value: {assignment['folder_id']}")
        print(f"folder_id type: {type(assignment['folder_id'])}")
        print(f"folder_id repr: {repr(assignment['folder_id'])}")

    client.close()


if __name__ == "__main__":
    asyncio.run(check_types())
