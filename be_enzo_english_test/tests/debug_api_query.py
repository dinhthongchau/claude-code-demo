"""Debug what the API query is doing."""

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


async def debug_query():
    """Mimic exactly what the API is doing."""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    user_folder_words = db["user_folder_words"]
    words = db["words"]

    print("Step 1: Query for assignments")
    print(f'Query: {{"user_id": "{TEST_USER_ID}", "folder_id": "{FOLDER_ID}"}}\n')

    assignments = await user_folder_words.find(
        {"user_id": TEST_USER_ID, "folder_id": FOLDER_ID}
    ).to_list(100)

    print(f"Found {len(assignments)} assignments\n")

    print("Step 2: Get word details for each assignment")
    response_data = []
    for assignment in assignments:
        print(f"  Looking for word_id: {assignment['word_id']}")
        word = await words.find_one({"word_id": assignment["word_id"]})
        if word:
            print(f"    ✅ Found: {word['word']}")
            response_data.append(
                {
                    "word_id": word["word_id"],
                    "word": word["word"],
                    "image_url": word.get("image_url"),
                }
            )
        else:
            print("    ❌ Not found")

    print(f"\nFinal result: {len(response_data)} words")
    for w in response_data:
        print(f"  - {w['word']} ({w['word_id']})")

    client.close()


if __name__ == "__main__":
    asyncio.run(debug_query())
