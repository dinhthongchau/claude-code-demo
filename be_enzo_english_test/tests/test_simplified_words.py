"""
Test suite for simplified word management endpoints.
Tests both global word dictionary and user folder word assignments.
"""

import io
import os
import sys
import requests
from pathlib import Path

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Load BASE_URL from environment
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    from dotenv import load_dotenv

    load_dotenv(env_path)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8829")

# Global test variables
test_user_id = None
test_folder_id = None
test_word_ids = []


def print_separator(title: str):
    """Print a formatted separator for test sections."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def print_result(test_name: str, response, expected_status: int = 200):
    """Print formatted test result."""
    status_icon = "✅" if response.status_code == expected_status else "❌"
    print(f"{status_icon} {test_name}")
    print(f"   Status: {response.status_code} (expected: {expected_status})")

    try:
        data = response.json()
        if isinstance(data, dict):
            if data.get("success"):
                print(f"   Message: {data.get('message', 'No message')}")
                if data.get("data"):
                    print(
                        f"   Data keys: {list(data['data'].keys()) if isinstance(data['data'], dict) else type(data['data'])}"
                    )
            else:
                print(f"   Error: {data.get('message', 'Unknown error')}")
        else:
            print(f"   Response: {str(data)[:100]}...")
    except Exception:
        print(f"   Response: {response.text[:100]}...")
    print()


def cleanup_test_data():
    """Clean up test data before and after tests."""
    print("🧹 Cleaning up test data...")

    # Clean up test words from global dictionary
    for word_id in ["TEST_001", "TEST_002", "TEST_003", "APPLE_001", "BANANA_002"]:
        try:
            response = requests.delete(f"{BASE_URL}/api/v1/global/words/{word_id}")
            if response.status_code in [200, 404]:
                print(f"   Cleaned word: {word_id}")
        except Exception:
            pass

    # Clean up test folders (reuse existing cleanup)
    try:
        response = requests.get(f"{BASE_URL}/api/v1/folders")
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("data"):
                for folder in data["data"]:
                    if folder.get("name", "").startswith("TEST_"):
                        folder_id = folder.get("id")
                        delete_response = requests.delete(
                            f"{BASE_URL}/api/v1/folders/{folder_id}"
                        )
                        if delete_response.status_code == 200:
                            print(f"   Cleaned folder: {folder['name']}")
    except Exception:
        pass

    print("✅ Cleanup completed\n")


def setup_test_user_and_folder():
    """Setup test user and folder for testing."""
    global test_user_id, test_folder_id

    print_separator("TEST SETUP")

    # Get test user
    response = requests.get(f"{BASE_URL}/api/v1/auth/current-user")
    print_result("Get test user", response)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            # Use email as user_id (matches folder creation logic)
            global test_user_id
            test_user_id = data["data"]["email"]
            print(f"📝 Test user ID: {test_user_id}")

    # Create test folder
    folder_data = {
        "name": "TEST_Simplified Words Folder",
        "description": "Test folder for simplified words",
    }

    response = requests.post(f"{BASE_URL}/api/v1/folders", json=folder_data)
    print_result("Create test folder", response)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            # Handle both possible response formats
            global test_folder_id
            folder_data = data["data"]
            if "folder" in folder_data:
                test_folder_id = folder_data["folder"]["folder_id"]
            else:
                test_folder_id = folder_data.get("folder_id") or folder_data.get("id")
            print(f"📝 Test folder ID: {test_folder_id}")

    return test_user_id and test_folder_id


def test_global_word_dictionary():
    """Test global word dictionary CRUD operations."""
    print_separator("GLOBAL WORD DICTIONARY TESTS")

    # Test 1: Create word (full fields)
    word_data = {
        "word_id": "TEST_001",
        "word": "apple",
        "definition": "A round red fruit that grows on trees",
        "example": "I ate an apple for breakfast",
    }

    response = requests.post(f"{BASE_URL}/api/v1/global/words", json=word_data)
    print_result("Create word (full fields)", response)

    if response.status_code == 200:
        test_word_ids.append("TEST_001")

    # Test 2: Create word (minimal fields)
    word_data_minimal = {
        "word_id": "TEST_002",
        "word": "banana",
        "definition": "A yellow curved fruit",
    }

    response = requests.post(f"{BASE_URL}/api/v1/global/words", json=word_data_minimal)
    print_result("Create word (minimal fields)", response)

    if response.status_code == 200:
        test_word_ids.append("TEST_002")

    # Test 3: Create duplicate word_id
    response = requests.post(f"{BASE_URL}/api/v1/global/words", json=word_data)
    print_result("Create duplicate word_id", response, 409)

    # Test 4: Get word (success)
    response = requests.get(f"{BASE_URL}/api/v1/global/words/TEST_001")
    print_result("Get word (success)", response)

    # Test 5: Get word (not found)
    response = requests.get(f"{BASE_URL}/api/v1/global/words/NONEXISTENT")
    print_result("Get word (not found)", response, 404)

    # Test 6: Update word
    update_data = {
        "definition": "Updated: A round red fruit",
        "example": "Updated: I love eating apples",
    }

    response = requests.put(
        f"{BASE_URL}/api/v1/global/words/TEST_001", json=update_data
    )
    print_result("Update word", response)

    # Test 7: Update non-existent word
    response = requests.put(
        f"{BASE_URL}/api/v1/global/words/NONEXISTENT", json=update_data
    )
    print_result("Update non-existent word", response, 404)


def test_image_upload():
    """Test image upload and serving functionality."""
    print_separator("IMAGE UPLOAD TESTS")

    # Create a simple test image file in memory
    import io
    from PIL import Image

    # Create a simple 100x100 red image
    img = Image.new("RGB", (100, 100), color="red")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    # Test 1: Upload image for existing word
    files = {"image": ("test_apple.jpg", img_bytes, "image/jpeg")}
    response = requests.post(
        f"{BASE_URL}/api/v1/global/words/TEST_001/image", files=files
    )
    print_result("Upload image (success)", response)

    # Test 2: Get uploaded image
    response = requests.get(f"{BASE_URL}/api/v1/global/words/TEST_001/image")
    print_result("Get word image", response)

    # Test 3: Upload image for non-existent word
    img_bytes.seek(0)
    files = {"image": ("test_nonexistent.jpg", img_bytes, "image/jpeg")}
    response = requests.post(
        f"{BASE_URL}/api/v1/global/words/NONEXISTENT/image", files=files
    )
    print_result("Upload image (word not found)", response, 404)

    # Test 4: Upload invalid file format
    text_file = io.StringIO("This is not an image")
    files = {"image": ("test.txt", text_file, "text/plain")}
    response = requests.post(
        f"{BASE_URL}/api/v1/global/words/TEST_001/image", files=files
    )
    print_result("Upload invalid format", response, 400)


def test_user_folder_words():
    """Test user folder word assignment operations."""
    print_separator("USER FOLDER WORDS TESTS")

    # Test 1: Add existing word to folder
    word_assignment = {"word_id": "TEST_001"}

    response = requests.post(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/{test_folder_id}/words",
        json=word_assignment,
    )
    print_result("Add word to folder (success)", response)

    # Test 2: Add non-existent word to folder
    word_assignment_invalid = {"word_id": "NONEXISTENT"}

    response = requests.post(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/{test_folder_id}/words",
        json=word_assignment_invalid,
    )
    print_result("Add non-existent word to folder", response, 404)

    # Test 3: Add duplicate word to same folder
    response = requests.post(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/{test_folder_id}/words",
        json=word_assignment,
    )
    print_result("Add duplicate word to folder", response, 409)

    # Test 4: Add second word to folder
    word_assignment_2 = {"word_id": "TEST_002"}

    response = requests.post(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/{test_folder_id}/words",
        json=word_assignment_2,
    )
    print_result("Add second word to folder", response)

    # Test 5: List words in folder
    response = requests.get(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/{test_folder_id}/words"
    )
    print_result("List words in folder", response)

    # Test 6: List words with pagination
    response = requests.get(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/{test_folder_id}/words?limit=1&skip=0"
    )
    print_result("List words with pagination", response)

    # Test 7: Remove word from folder
    response = requests.delete(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/{test_folder_id}/words/TEST_001"
    )
    print_result("Remove word from folder", response)

    # Test 8: Remove non-existent word from folder
    response = requests.delete(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/{test_folder_id}/words/NONEXISTENT"
    )
    print_result("Remove non-existent word from folder", response, 404)


def test_validation_errors():
    """Test input validation and error handling."""
    print_separator("VALIDATION ERROR TESTS")

    # Test 1: Create word with missing required fields
    invalid_word = {"word_id": "TEST_003"}  # Missing word and definition

    response = requests.post(f"{BASE_URL}/api/v1/global/words", json=invalid_word)
    print_result("Create word (missing required fields)", response, 422)

    # Test 2: Create word with empty word_id
    invalid_word_2 = {"word_id": "", "word": "test", "definition": "test definition"}

    response = requests.post(f"{BASE_URL}/api/v1/global/words", json=invalid_word_2)
    print_result("Create word (empty word_id)", response, 422)

    # Test 3: Update word with empty update
    response = requests.put(f"{BASE_URL}/api/v1/global/words/TEST_001", json={})
    print_result("Update word (empty update)", response, 400)

    # Test 4: Invalid folder ID format
    word_assignment = {"word_id": "TEST_001"}

    response = requests.post(
        f"{BASE_URL}/api/v1/users/{test_user_id}/folders/invalid_folder_id/words",
        json=word_assignment,
    )
    print_result("Add word to invalid folder ID", response, 400)


def print_curl_examples():
    """Print CURL examples for manual testing."""
    print_separator("CURL EXAMPLES FOR MANUAL TESTING")

    print("# Create word:")
    print(f'curl -X POST "{BASE_URL}/api/v1/global/words" \\')
    print('  -H "Content-Type: application/json" \\')
    print(
        '  -d \'{"word_id": "apple_001", "word": "apple", "definition": "A red fruit", "example": "I ate an apple"}\''
    )
    print()

    print("# Upload image:")
    print(f'curl -X POST "{BASE_URL}/api/v1/global/words/apple_001/image" \\')
    print('  -F "image=@path/to/apple.jpg"')
    print()

    print("# Add word to folder:")
    print(
        f'curl -X POST "{BASE_URL}/api/v1/users/{test_user_id or "USER_ID"}/folders/{test_folder_id or "FOLDER_ID"}/words" \\'
    )
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"word_id": "apple_001"}\'')
    print()

    print("# List words in folder:")
    print(
        f'curl "{BASE_URL}/api/v1/users/{test_user_id or "USER_ID"}/folders/{test_folder_id or "FOLDER_ID"}/words"'
    )
    print()


def main():
    """Run all tests."""
    print("🚀 Starting Simplified Words API Tests")
    print(f"📍 Base URL: {BASE_URL}")

    # Cleanup before tests
    cleanup_test_data()

    # Setup
    if not setup_test_user_and_folder():
        print("❌ Failed to setup test environment. Exiting.")
        return

    try:
        # Run tests
        test_global_word_dictionary()

        # Only test image upload if PIL is available
        try:
            from PIL import Image  # noqa: F401

            test_image_upload()
        except ImportError:
            print("⚠️  Skipping image tests (PIL not available)")

        test_user_folder_words()
        test_validation_errors()

        # Print examples
        print_curl_examples()

    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")

    finally:
        # Cleanup after tests
        cleanup_test_data()

    print("✅ All tests completed!")


if __name__ == "__main__":
    main()
