"""
Automatically add sample words to ALL existing folders for testing.

Usage:
    python tests/add_sample_words_auto.py
"""

import requests
import sys
import io
import os
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Load environment
test_dir = Path(__file__).parent
load_dotenv(test_dir / ".env")
BASE_URL = os.getenv("BASE_URL")

# Sample words to add (different sets for different folders)
WORD_SETS = {
    "set1": [
        {
            "word": "serendipity",
            "definition": "The occurrence of events by chance in a happy or beneficial way",
            "examples": ["Meeting my best friend was pure serendipity"],
            "part_of_speech": "noun",
            "pronunciation": "/ˌser.ənˈdɪp.ə.ti/",
        },
        {
            "word": "ephemeral",
            "definition": "Lasting for a very short time",
            "examples": ["The ephemeral beauty of cherry blossoms"],
            "part_of_speech": "adjective",
            "pronunciation": "/ɪˈfem.ər.əl/",
        },
        {
            "word": "ubiquitous",
            "definition": "Present, appearing, or found everywhere",
            "examples": ["Smartphones are ubiquitous in modern society"],
            "part_of_speech": "adjective",
            "pronunciation": "/juːˈbɪk.wɪ.təs/",
        },
    ],
    "set2": [
        {
            "word": "ambiguous",
            "definition": "Open to more than one interpretation",
            "examples": ["The ending was deliberately ambiguous"],
            "part_of_speech": "adjective",
            "pronunciation": "/æmˈbɪɡ.ju.əs/",
        },
        {
            "word": "resilient",
            "definition": "Able to recover quickly from difficult conditions",
            "examples": ["She proved to be resilient"],
            "part_of_speech": "adjective",
            "pronunciation": "/rɪˈzɪl.i.ənt/",
        },
        {
            "word": "inevitable",
            "definition": "Certain to happen; unavoidable",
            "examples": ["Change is inevitable in life"],
            "part_of_speech": "adjective",
            "pronunciation": "/ɪˈnev.ɪ.tə.bəl/",
        },
        {
            "word": "profound",
            "definition": "Very great or intense",
            "examples": ["The book had a profound impact"],
            "part_of_speech": "adjective",
            "pronunciation": "/prəˈfaʊnd/",
        },
    ],
    "set3": [
        {
            "word": "eloquent",
            "definition": "Fluent or persuasive in speaking",
            "examples": ["An eloquent speech"],
            "part_of_speech": "adjective",
            "pronunciation": "/ˈel.ə.kwənt/",
        },
        {
            "word": "meticulous",
            "definition": "Very careful and precise",
            "examples": ["She was meticulous in her research"],
            "part_of_speech": "adjective",
            "pronunciation": "/məˈtɪk.jə.ləs/",
        },
        {
            "word": "paradox",
            "definition": "A contradictory statement that may be true",
            "examples": ["The paradox of choice"],
            "part_of_speech": "noun",
            "pronunciation": "/ˈpær.ə.dɒks/",
        },
        {
            "word": "aesthetic",
            "definition": "Concerned with beauty or art",
            "examples": ["The aesthetic design was impressive"],
            "part_of_speech": "adjective",
            "pronunciation": "/esˈθet.ɪk/",
        },
        {
            "word": "quintessential",
            "definition": "Representing the perfect example",
            "examples": ["She is the quintessential professional"],
            "part_of_speech": "adjective",
            "pronunciation": "/ˌkwɪn.tɪˈsen.ʃəl/",
        },
    ],
}


def get_folders():
    """Get all non-test folders."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/folders")
        if response.status_code == 200:
            data = response.json()
            # Filter out TEST_ folders
            return [f for f in data.get("data", []) if not f["name"].startswith("TEST_")]
        return []
    except Exception as e:
        print(f"❌ Error fetching folders: {e}")
        return []


def add_word(folder_id, word_data):
    """Add a word to a folder."""
    word_data["folder_id"] = folder_id
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/words",
            json=word_data,
            headers={"Content-Type": "application/json"}
        )
        return response.status_code == 200
    except Exception:
        return False


def main():
    print("🌟 Adding Sample Words to All Folders\n")

    # Get all folders
    folders = get_folders()
    if not folders:
        print("❌ No folders found. Create a folder first!")
        return

    print(f"📁 Found {len(folders)} folder(s):\n")

    total_added = 0
    word_set_keys = list(WORD_SETS.keys())

    for i, folder in enumerate(folders):
        # Cycle through word sets
        word_set_key = word_set_keys[i % len(word_set_keys)]
        words = WORD_SETS[word_set_key]

        print(f"  {folder.get('icon', '📁')} {folder['name']}")
        print(f"     Adding {len(words)} words...")

        success_count = 0
        for word_data in words:
            if add_word(folder['id'], word_data.copy()):
                success_count += 1

        print(f"     ✓ Added {success_count}/{len(words)} words\n")
        total_added += success_count

    print(f"🎉 Total: Successfully added {total_added} words across {len(folders)} folders")


if __name__ == "__main__":
    main()
