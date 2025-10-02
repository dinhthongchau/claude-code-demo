"""
Quick script to add sample words to existing folders for testing.

Usage:
    python tests/add_sample_words.py
"""

import requests
import json
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

# Sample words to add
SAMPLE_WORDS = [
    {
        "word": "serendipity",
        "definition": "The occurrence of events by chance in a happy or beneficial way",
        "examples": [
            "Meeting my best friend was pure serendipity",
            "The serendipitous discovery changed everything"
        ],
        "part_of_speech": "noun",
        "pronunciation": "/ˌser.ənˈdɪp.ə.ti/",
    },
    {
        "word": "ephemeral",
        "definition": "Lasting for a very short time",
        "examples": [
            "The ephemeral beauty of cherry blossoms",
            "Fame can be ephemeral"
        ],
        "part_of_speech": "adjective",
        "pronunciation": "/ɪˈfem.ər.əl/",
    },
    {
        "word": "ubiquitous",
        "definition": "Present, appearing, or found everywhere",
        "examples": [
            "Smartphones are ubiquitous in modern society",
            "Coffee shops have become ubiquitous"
        ],
        "part_of_speech": "adjective",
        "pronunciation": "/juːˈbɪk.wɪ.təs/",
    },
    {
        "word": "ambiguous",
        "definition": "Open to more than one interpretation; not having one obvious meaning",
        "examples": [
            "The ending of the movie was deliberately ambiguous",
            "His answer was ambiguous and unclear"
        ],
        "part_of_speech": "adjective",
        "pronunciation": "/æmˈbɪɡ.ju.əs/",
    },
    {
        "word": "resilient",
        "definition": "Able to withstand or recover quickly from difficult conditions",
        "examples": [
            "She proved to be resilient after the setback",
            "The resilient community rebuilt after the disaster"
        ],
        "part_of_speech": "adjective",
        "pronunciation": "/rɪˈzɪl.i.ənt/",
    },
    {
        "word": "inevitable",
        "definition": "Certain to happen; unavoidable",
        "examples": [
            "Change is inevitable in life",
            "The outcome seemed inevitable"
        ],
        "part_of_speech": "adjective",
        "pronunciation": "/ɪˈnev.ɪ.tə.bəl/",
    },
    {
        "word": "profound",
        "definition": "Very great or intense; showing great knowledge or insight",
        "examples": [
            "The book had a profound impact on me",
            "She made a profound observation"
        ],
        "part_of_speech": "adjective",
        "pronunciation": "/prəˈfaʊnd/",
    },
    {
        "word": "eloquent",
        "definition": "Fluent or persuasive in speaking or writing",
        "examples": [
            "The speaker gave an eloquent speech",
            "Her eloquent words moved the audience"
        ],
        "part_of_speech": "adjective",
        "pronunciation": "/ˈel.ə.kwənt/",
    },
    {
        "word": "meticulous",
        "definition": "Showing great attention to detail; very careful and precise",
        "examples": [
            "She was meticulous in her research",
            "The artist's meticulous work was impressive"
        ],
        "part_of_speech": "adjective",
        "pronunciation": "/məˈtɪk.jə.ləs/",
    },
    {
        "word": "paradox",
        "definition": "A seemingly absurd or contradictory statement that may be true",
        "examples": [
            "The paradox of choice: more options can make us less happy",
            "It's a paradox that technology connects yet isolates us"
        ],
        "part_of_speech": "noun",
        "pronunciation": "/ˈpær.ə.dɒks/",
    },
]


def get_folders():
    """Get all folders."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/folders")
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        return []
    except Exception as e:
        print(f"Error fetching folders: {e}")
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
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)


def main():
    print("🌟 Adding Sample Words to Folders\n")

    # Get all folders
    folders = get_folders()
    if not folders:
        print("❌ No folders found. Create a folder first!")
        return

    print(f"📁 Found {len(folders)} folder(s):\n")
    for i, folder in enumerate(folders, 1):
        print(f"  {i}. {folder.get('icon', '📁')} {folder['name']} (ID: {folder['id']})")

    # Ask user to select folder
    print()
    try:
        choice = int(input(f"Select folder (1-{len(folders)}): "))
        if choice < 1 or choice > len(folders):
            print("❌ Invalid choice")
            return
    except ValueError:
        print("❌ Invalid input")
        return

    selected_folder = folders[choice - 1]
    print(f"\n✅ Selected: {selected_folder['name']}\n")

    # Add words
    print(f"📝 Adding {len(SAMPLE_WORDS)} sample words...\n")

    success_count = 0
    for word_data in SAMPLE_WORDS:
        success, result = add_word(selected_folder['id'], word_data.copy())
        if success:
            print(f"  ✓ {word_data['word']}")
            success_count += 1
        else:
            print(f"  ✗ {word_data['word']} - {result}")

    print(f"\n🎉 Successfully added {success_count}/{len(SAMPLE_WORDS)} words to '{selected_folder['name']}'")


if __name__ == "__main__":
    main()
