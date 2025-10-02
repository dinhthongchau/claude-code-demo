"""
Create sample words with images for testing Flutter app.
This creates words in the NEW simplified structure with images.

Usage:
    cd be_enzo_english_test
    python tests/create_sample_words_with_images.py
"""

import io
import os
import sys
import requests
from pathlib import Path

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Load environment
from dotenv import load_dotenv

test_dir = Path(__file__).parent
load_dotenv(test_dir / ".env")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8829")

# Hardcoded test user
TEST_USER_ID = "dinhthongchau@gmail.com"


def create_test_image(color="red", size=(200, 200)):
    """Create a simple colored test image."""
    try:
        from PIL import Image

        img = Image.new("RGB", size, color=color)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)
        return img_bytes
    except ImportError:
        print("⚠️  PIL not installed. Install with: pip install Pillow")
        return None


def get_or_create_test_folder():
    """Get existing test folder or create one."""
    print("📁 Setting up test folder...")

    # Try to get existing folders
    response = requests.get(f"{BASE_URL}/api/v1/folders")
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("data"):
            folders = data["data"]
            # Find a non-test folder
            for folder in folders:
                if not folder["name"].startswith("TEST_"):
                    print(
                        f"✅ Using existing folder: {folder['name']} (ID: {folder['id']})"
                    )
                    return folder["id"]

    # Create a new test folder
    folder_data = {
        "name": "TEST_Flutter_Words",
        "description": "Test folder with words and images for Flutter",
        "icon": "📚",
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/folders",
        json=folder_data,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        data = response.json()
        folder_id = data["data"]["id"]
        print(f"✅ Created new folder: {folder_data['name']} (ID: {folder_id})")
        return folder_id
    else:
        print(f"❌ Failed to create folder: {response.text}")
        return None


def create_word_with_image(word_id, word, definition, example, image_color):
    """Create a word in global dictionary and upload image."""
    print(f"\n📝 Creating word: {word}")

    # Step 1: Create word in global dictionary
    word_data = {
        "word_id": word_id,
        "word": word,
        "definition": definition,
        "example": example,
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/global/words",
        json=word_data,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        print(f"   ❌ Failed to create word: {response.text}")
        return False

    print("   ✅ Created word in global dictionary")

    # Step 2: Upload image
    img = create_test_image(color=image_color)
    if img:
        files = {"image": (f"{word_id}.jpg", img, "image/jpeg")}
        response = requests.post(
            f"{BASE_URL}/api/v1/global/words/{word_id}/image", files=files
        )

        if response.status_code == 200:
            print(f"   ✅ Uploaded {image_color} image")
        else:
            print(f"   ⚠️  Image upload failed: {response.text}")

    return True


def add_word_to_folder(folder_id, word_id):
    """Add a word from global dictionary to user folder."""
    response = requests.post(
        f"{BASE_URL}/api/v1/users/{TEST_USER_ID}/folders/{folder_id}/words",
        json={"word_id": word_id},
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        print("   ✅ Added to folder")
        return True
    else:
        print(f"   ❌ Failed to add to folder: {response.text}")
        return False


def main():
    print("🌟 Creating Sample Words with Images for Flutter\n")

    # Get or create test folder
    folder_id = get_or_create_test_folder()
    if not folder_id:
        print("❌ Failed to setup folder")
        return

    # Sample words with different colored images
    sample_words = [
        {
            "word_id": "APPLE_001",
            "word": "apple",
            "definition": "A round red or green fruit that grows on trees",
            "example": "I ate a delicious apple for breakfast",
            "image_color": "red",
        },
        {
            "word_id": "BANANA_002",
            "word": "banana",
            "definition": "A long yellow fruit with soft sweet flesh",
            "example": "She peeled a banana and ate it",
            "image_color": "yellow",
        },
        {
            "word_id": "GRAPE_003",
            "word": "grape",
            "definition": "A small round fruit that grows in clusters",
            "example": "The grapes were sweet and juicy",
            "image_color": "purple",
        },
        {
            "word_id": "ORANGE_004",
            "word": "orange",
            "definition": "A round citrus fruit with thick orange skin",
            "example": "I squeezed fresh orange juice this morning",
            "image_color": "orange",
        },
    ]

    print(f"\n{'=' * 60}")
    print(" Creating Words")
    print(f"{'=' * 60}")

    success_count = 0
    for word_data in sample_words:
        word_id = word_data["word_id"]

        # Create word with image
        if create_word_with_image(
            word_id,
            word_data["word"],
            word_data["definition"],
            word_data["example"],
            word_data["image_color"],
        ):
            # Add to folder
            if add_word_to_folder(folder_id, word_id):
                success_count += 1

    print(f"\n{'=' * 60}")
    print(f"🎉 Success! Created {success_count}/{len(sample_words)} words with images")
    print(f"{'=' * 60}")
    print("\n📱 Now check your Flutter app!")
    print(f"   Folder ID: {folder_id}")
    print(f"   User ID: {TEST_USER_ID}")
    print("\n🔍 Test in browser:")
    print(f"   {BASE_URL}/api/v1/users/{TEST_USER_ID}/folders/{folder_id}/words")


if __name__ == "__main__":
    main()
