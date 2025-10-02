"""
Test file for word CRUD endpoints.

Simplified version - no Firebase token required.
Run this file to test all word management endpoints.

Usage:
    python tests/test_words.py
"""

import requests
import json
import sys
import io
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding issues
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Load environment variables from tests/.env
test_dir = Path(__file__).parent
load_dotenv(test_dir / ".env")

# Base URL for the test server (from .env)
BASE_URL = os.getenv("BASE_URL")

# Global variables to store IDs for tests
test_user_id: Optional[str] = None
test_folder_id: Optional[str] = None
created_word_id: Optional[str] = None


def print_separator(title=""):
    """Print a nice separator."""
    if title:
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    else:
        print("=" * 80)


def print_result(test_name, passed, message=""):
    """Print test result."""
    status = "✓ PASSED" if passed else "✗ FAILED"
    print(f"{status}: {test_name}")
    if message:
        print(f"  → {message}")


# ==============================================================================
# Setup Helpers
# ==============================================================================
def get_test_user_id() -> Optional[str]:
    """Get the test user ID by calling the auth endpoint."""
    try:
        url = f"{BASE_URL}/api/v1/auth/current-user"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("id")
        return None
    except Exception:
        return None


def create_test_folder() -> Optional[str]:
    """Create a test folder and return its ID."""
    try:
        url = f"{BASE_URL}/api/v1/folders"
        payload = {
            "name": "TEST_Word Folder",
            "description": "Test folder for word tests",
            "color": "#FF5733",
            "icon": "📚",
        }
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("id")
        return None
    except Exception:
        return None


def cleanup_test_words():
    """Delete all words with TEST_ prefix to clean up after tests."""
    try:
        # Get all folders to find test folders
        folders_url = f"{BASE_URL}/api/v1/folders"
        folders_response = requests.get(folders_url, timeout=3)

        if folders_response.status_code == 200:
            folders_data = folders_response.json()
            folders = folders_data.get("data", [])

            deleted_count = 0
            endpoint_exists = None  # Cache endpoint existence check

            for folder in folders:
                folder_id = folder.get("id")

                # Skip if we already know endpoint doesn't exist
                if endpoint_exists is False:
                    break

                # Get words in this folder
                words_url = f"{BASE_URL}/api/v1/folders/{folder_id}/words"
                try:
                    words_response = requests.get(words_url, timeout=3)

                    if words_response.status_code == 200:
                        endpoint_exists = True
                        words_data = words_response.json()
                        words = words_data.get("data", [])

                        # Delete words with TEST_ prefix
                        for word in words:
                            if word.get("word", "").startswith("TEST_"):
                                word_id = word.get("id")
                                delete_url = f"{BASE_URL}/api/v1/words/{word_id}"
                                delete_response = requests.delete(delete_url, timeout=3)
                                if delete_response.status_code == 200:
                                    deleted_count += 1
                    elif words_response.status_code == 404:
                        # Endpoint doesn't exist yet, skip cleanup entirely
                        endpoint_exists = False
                        break
                except Exception:
                    # Skip if endpoint doesn't exist or times out
                    endpoint_exists = False
                    break

            if deleted_count > 0:
                print(f"\n🧹 Cleaned up {deleted_count} test word(s)")
    except Exception as e:
        print(f"\n⚠ Word cleanup warning: {e}")


def cleanup_test_folders():
    """Delete all folders with TEST_ prefix to clean up after tests."""
    try:
        url = f"{BASE_URL}/api/v1/folders"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            folders = data.get("data", [])

            deleted_count = 0
            for folder in folders:
                if folder.get("name", "").startswith("TEST_"):
                    folder_id = folder.get("id")
                    delete_url = f"{BASE_URL}/api/v1/folders/{folder_id}"
                    delete_response = requests.delete(delete_url, timeout=5)
                    if delete_response.status_code == 200:
                        deleted_count += 1

            if deleted_count > 0:
                print(f"🧹 Cleaned up {deleted_count} test folder(s)")
    except Exception as e:
        print(f"⚠ Folder cleanup warning: {e}")


# ==============================================================================
# Test 1: Setup - Create Test Folder
# ==============================================================================
def test_setup_create_folder():
    """Setup test - create a test folder for word tests."""
    global test_folder_id

    print_separator("TEST 1: Setup - Create Test Folder")

    url = f"{BASE_URL}/api/v1/folders"
    print(f"POST {url}")

    payload = {
        "name": "TEST_Word Folder",
        "description": "Test folder for word tests",
        "color": "#FF5733",
        "icon": "📚",
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"

        folder = data["data"]
        assert "id" in folder, "Folder should have an id"

        test_folder_id = folder["id"]

        print_result(
            "Setup - Create Test Folder", True, f"Test folder ID: {test_folder_id}"
        )
        return True

    except requests.exceptions.ConnectionError:
        print_result("Setup - Create Test Folder", False, "Could not connect to server")
        return False
    except AssertionError as e:
        print_result("Setup - Create Test Folder", False, str(e))
        return False
    except Exception as e:
        print_result("Setup - Create Test Folder", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 2: List Words (Empty State)
# ==============================================================================
def test_list_words_empty():
    """Test listing words when folder is empty."""
    print_separator("TEST 2: List Words (Empty State)")

    if not test_folder_id:
        print_result("List Words (Empty)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/folders/{test_folder_id}/words"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"
        assert isinstance(data["data"], list), "Data should be a list"

        # Should be empty initially
        test_words = [w for w in data["data"] if w.get("word", "").startswith("TEST_")]
        assert len(test_words) == 0, "Should have no TEST_ words initially"

        print_result("List Words (Empty)", True, "Empty word list confirmed")
        return True

    except AssertionError as e:
        print_result("List Words (Empty)", False, str(e))
        return False
    except Exception as e:
        print_result("List Words (Empty)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 3: Create Word (Success)
# ==============================================================================
def test_create_word_success():
    """Test creating a new word successfully with all fields."""
    global created_word_id

    print_separator("TEST 3: Create Word (Success)")

    if not test_folder_id:
        print_result("Create Word (Success)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "TEST_apple",
        "folder_id": test_folder_id,
        "definition": "A round fruit that grows on trees",
        "examples": ["I ate an apple for breakfast", "Apple pie is delicious"],
        "image_urls": ["https://example.com/apple.jpg"],
        "part_of_speech": "noun",
        "pronunciation": "/ˈæp.əl/",
        "notes": "Test word for vocabulary",
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"

        word = data["data"]
        assert "id" in word, "Word should have an id"
        assert isinstance(word["id"], str), "Word id should be a string"
        assert len(word["id"]) == 24, "Word id should be 24 characters (ObjectId)"

        assert word["word"] == payload["word"], "Word should match"
        assert word["definition"] == payload["definition"], "Definition should match"
        assert word["folder_id"] == payload["folder_id"], "Folder ID should match"
        assert word["examples"] == payload["examples"], "Examples should match"
        assert word["image_urls"] == payload["image_urls"], "Image URLs should match"
        assert word["part_of_speech"] == payload["part_of_speech"], "Part of speech should match"
        assert word["pronunciation"] == payload["pronunciation"], "Pronunciation should match"
        assert word["notes"] == payload["notes"], "Notes should match"

        assert "user_id" in word, "Word should have user_id"
        assert "created_at" in word, "Word should have created_at"
        assert "updated_at" in word, "Word should have updated_at"

        created_word_id = word["id"]

        print_result("Create Word (Success)", True, f"Word ID: {created_word_id}")
        return True

    except AssertionError as e:
        print_result("Create Word (Success)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Success)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 4: Create Word (Missing Required Field - word)
# ==============================================================================
def test_create_word_missing_word():
    """Test creating word without word field (should fail)."""
    print_separator("TEST 4: Create Word (Missing Required Field - word)")

    if not test_folder_id:
        print_result("Create Word (Missing word)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "folder_id": test_folder_id,
        "definition": "Missing word field"
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"

        data = response.json()
        assert "detail" in data, "Error response should contain detail"

        print_result("Create Word (Missing word)", True, "Correctly rejected missing word")
        return True

    except AssertionError as e:
        print_result("Create Word (Missing word)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Missing word)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 5: Create Word (Missing Required Field - definition)
# ==============================================================================
def test_create_word_missing_definition():
    """Test creating word without definition field (should fail)."""
    print_separator("TEST 5: Create Word (Missing Required Field - definition)")

    if not test_folder_id:
        print_result("Create Word (Missing definition)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "TEST_banana",
        "folder_id": test_folder_id
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"

        data = response.json()
        assert "detail" in data, "Error response should contain detail"

        print_result("Create Word (Missing definition)", True, "Correctly rejected missing definition")
        return True

    except AssertionError as e:
        print_result("Create Word (Missing definition)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Missing definition)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 6: Create Word (Missing Required Field - folder_id)
# ==============================================================================
def test_create_word_missing_folder_id():
    """Test creating word without folder_id field (should fail)."""
    print_separator("TEST 6: Create Word (Missing Required Field - folder_id)")

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "TEST_orange",
        "definition": "A citrus fruit"
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"

        data = response.json()
        assert "detail" in data, "Error response should contain detail"

        print_result("Create Word (Missing folder_id)", True, "Correctly rejected missing folder_id")
        return True

    except AssertionError as e:
        print_result("Create Word (Missing folder_id)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Missing folder_id)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 7: Create Word (Non-existent Folder)
# ==============================================================================
def test_create_word_nonexistent_folder():
    """Test creating word in non-existent folder (should fail)."""
    print_separator("TEST 7: Create Word (Non-existent Folder)")

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "TEST_grape",
        "folder_id": "000000000000000000000000",
        "definition": "Small round fruit"
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("Create Word (Non-existent Folder)", True, "Correctly rejected non-existent folder")
        return True

    except AssertionError as e:
        print_result("Create Word (Non-existent Folder)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Non-existent Folder)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 8: Create Word (Invalid Folder ID Format)
# ==============================================================================
def test_create_word_invalid_folder_id():
    """Test creating word with invalid folder ID format (should fail)."""
    print_separator("TEST 8: Create Word (Invalid Folder ID Format)")

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "TEST_mango",
        "folder_id": "invalid_id",
        "definition": "Tropical fruit"
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("Create Word (Invalid Folder ID)", True, "Correctly rejected invalid folder ID")
        return True

    except AssertionError as e:
        print_result("Create Word (Invalid Folder ID)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Invalid Folder ID)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 9: Create Word (Empty Word Name)
# ==============================================================================
def test_create_word_empty_word():
    """Test creating word with empty word name (should fail)."""
    print_separator("TEST 9: Create Word (Empty Word Name)")

    if not test_folder_id:
        print_result("Create Word (Empty word)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "",
        "folder_id": test_folder_id,
        "definition": "Empty word name"
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"

        data = response.json()
        assert "detail" in data, "Error response should contain detail"

        print_result("Create Word (Empty word)", True, "Correctly rejected empty word")
        return True

    except AssertionError as e:
        print_result("Create Word (Empty word)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Empty word)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 10: Create Word (Empty Definition)
# ==============================================================================
def test_create_word_empty_definition():
    """Test creating word with empty definition (should fail)."""
    print_separator("TEST 10: Create Word (Empty Definition)")

    if not test_folder_id:
        print_result("Create Word (Empty definition)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "TEST_kiwi",
        "folder_id": test_folder_id,
        "definition": ""
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"

        data = response.json()
        assert "detail" in data, "Error response should contain detail"

        print_result("Create Word (Empty definition)", True, "Correctly rejected empty definition")
        return True

    except AssertionError as e:
        print_result("Create Word (Empty definition)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Empty definition)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 11: Create Word (Minimal - No Optional Fields)
# ==============================================================================
def test_create_word_minimal():
    """Test creating word with only required fields."""
    print_separator("TEST 11: Create Word (Minimal - No Optional Fields)")

    if not test_folder_id:
        print_result("Create Word (Minimal)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "TEST_pear",
        "folder_id": test_folder_id,
        "definition": "A sweet fruit with green or yellow skin"
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"

        word = data["data"]
        assert word["word"] == payload["word"], "Word should match"
        assert word["definition"] == payload["definition"], "Definition should match"

        # Optional fields should be empty/null
        assert word["examples"] == [] or word["examples"] is None, "Examples should be empty"
        assert word["image_urls"] == [] or word["image_urls"] is None, "Image URLs should be empty"

        print_result("Create Word (Minimal)", True, "Created with only required fields")
        return True

    except AssertionError as e:
        print_result("Create Word (Minimal)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Minimal)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 12: Create Word (With Empty Arrays)
# ==============================================================================
def test_create_word_empty_arrays():
    """Test creating word with explicitly empty arrays."""
    print_separator("TEST 12: Create Word (With Empty Arrays)")

    if not test_folder_id:
        print_result("Create Word (Empty arrays)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/words"
    print(f"POST {url}")

    payload = {
        "word": "TEST_peach",
        "folder_id": test_folder_id,
        "definition": "Fuzzy fruit with sweet flesh",
        "examples": [],
        "image_urls": []
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"

        word = data["data"]
        assert word["examples"] == [], "Examples should be empty array"
        assert word["image_urls"] == [], "Image URLs should be empty array"

        print_result("Create Word (Empty arrays)", True, "Arrays stored as empty")
        return True

    except AssertionError as e:
        print_result("Create Word (Empty arrays)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Word (Empty arrays)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 13: List Words (With Data)
# ==============================================================================
def test_list_words_with_data():
    """Test listing words when data exists."""
    print_separator("TEST 13: List Words (With Data)")

    if not test_folder_id:
        print_result("List Words (With Data)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/folders/{test_folder_id}/words"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"
        assert isinstance(data["data"], list), "Data should be a list"
        assert len(data["data"]) > 0, "Should have at least one word"

        # Check each word has required fields
        for word in data["data"]:
            assert "id" in word, "Each word should have id"
            assert "word" in word, "Each word should have word"
            assert "definition" in word, "Each word should have definition"
            assert "folder_id" in word, "Each word should have folder_id"
            assert "user_id" in word, "Each word should have user_id"
            assert "created_at" in word, "Each word should have created_at"

        # Verify words are sorted alphabetically
        words_list = [w["word"] for w in data["data"]]
        assert words_list == sorted(words_list), "Words should be sorted alphabetically"

        print_result("List Words (With Data)", True, f"Found {len(data['data'])} word(s)")
        return True

    except AssertionError as e:
        print_result("List Words (With Data)", False, str(e))
        return False
    except Exception as e:
        print_result("List Words (With Data)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 14: List Words (Pagination - First Page)
# ==============================================================================
def test_list_words_pagination():
    """Test listing words with pagination."""
    print_separator("TEST 14: List Words (Pagination - First Page)")

    if not test_folder_id:
        print_result("List Words (Pagination)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/folders/{test_folder_id}/words?limit=2&skip=0"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"
        assert isinstance(data["data"], list), "Data should be a list"
        assert len(data["data"]) <= 2, "Should return at most 2 words"

        print_result("List Words (Pagination)", True, f"Returned {len(data['data'])} word(s)")
        return True

    except AssertionError as e:
        print_result("List Words (Pagination)", False, str(e))
        return False
    except Exception as e:
        print_result("List Words (Pagination)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 15: List Words (Pagination - Invalid Limit)
# ==============================================================================
def test_list_words_invalid_limit():
    """Test listing words with invalid limit value."""
    print_separator("TEST 15: List Words (Pagination - Invalid Limit)")

    if not test_folder_id:
        print_result("List Words (Invalid limit)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/folders/{test_folder_id}/words?limit=2000"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("List Words (Invalid limit)", True, "Correctly rejected invalid limit")
        return True

    except AssertionError as e:
        print_result("List Words (Invalid limit)", False, str(e))
        return False
    except Exception as e:
        print_result("List Words (Invalid limit)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 16: List Words (Pagination - Negative Skip)
# ==============================================================================
def test_list_words_negative_skip():
    """Test listing words with negative skip value."""
    print_separator("TEST 16: List Words (Pagination - Negative Skip)")

    if not test_folder_id:
        print_result("List Words (Negative skip)", False, "No test folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/folders/{test_folder_id}/words?skip=-5"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("List Words (Negative skip)", True, "Correctly rejected negative skip")
        return True

    except AssertionError as e:
        print_result("List Words (Negative skip)", False, str(e))
        return False
    except Exception as e:
        print_result("List Words (Negative skip)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 17: Get Single Word (Success)
# ==============================================================================
def test_get_word_success():
    """Test getting a single word by ID."""
    print_separator("TEST 17: Get Single Word (Success)")

    if not created_word_id:
        print_result("Get Single Word (Success)", False, "No word ID available")
        return False

    url = f"{BASE_URL}/api/v1/words/{created_word_id}"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"

        word = data["data"]
        assert word["id"] == created_word_id, "Word ID should match"
        assert word["word"] == "TEST_apple", "Word should match"
        assert "definition" in word, "Should have definition"
        assert "examples" in word, "Should have examples"
        assert "image_urls" in word, "Should have image_urls"
        assert "part_of_speech" in word, "Should have part_of_speech"
        assert "pronunciation" in word, "Should have pronunciation"
        assert "notes" in word, "Should have notes"
        assert "folder_id" in word, "Should have folder_id"
        assert "user_id" in word, "Should have user_id"
        assert "created_at" in word, "Should have created_at"
        assert "updated_at" in word, "Should have updated_at"

        print_result("Get Single Word (Success)", True, f"Retrieved word: {word['word']}")
        return True

    except AssertionError as e:
        print_result("Get Single Word (Success)", False, str(e))
        return False
    except Exception as e:
        print_result("Get Single Word (Success)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 18: Get Single Word (Not Found)
# ==============================================================================
def test_get_word_not_found():
    """Test getting a word that doesn't exist."""
    print_separator("TEST 18: Get Single Word (Not Found)")

    fake_id = "000000000000000000000000"
    url = f"{BASE_URL}/api/v1/words/{fake_id}"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("Get Single Word (Not Found)", True, "Correctly returned 404")
        return True

    except AssertionError as e:
        print_result("Get Single Word (Not Found)", False, str(e))
        return False
    except Exception as e:
        print_result("Get Single Word (Not Found)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 19: Get Single Word (Invalid ID Format)
# ==============================================================================
def test_get_word_invalid_id():
    """Test getting a word with invalid ObjectId format."""
    print_separator("TEST 19: Get Single Word (Invalid ID Format)")

    invalid_id = "invalid_word_id"
    url = f"{BASE_URL}/api/v1/words/{invalid_id}"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("Get Single Word (Invalid ID)", True, "Correctly rejected invalid ID")
        return True

    except AssertionError as e:
        print_result("Get Single Word (Invalid ID)", False, str(e))
        return False
    except Exception as e:
        print_result("Get Single Word (Invalid ID)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 20: Update Word (Success - Partial Update)
# ==============================================================================
def test_update_word_partial():
    """Test updating a word with partial fields."""
    print_separator("TEST 20: Update Word (Success - Partial Update)")

    if not created_word_id:
        print_result("Update Word (Partial)", False, "No word ID available")
        return False

    url = f"{BASE_URL}/api/v1/words/{created_word_id}"
    print(f"PUT {url}")

    payload = {
        "definition": "Updated definition: A round fruit",
        "notes": "Updated notes for testing"
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.put(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"

        word = data["data"]
        assert word["id"] == created_word_id, "Word ID should not change"
        assert word["definition"] == payload["definition"], "Definition should be updated"
        assert word["notes"] == payload["notes"], "Notes should be updated"
        assert word["word"] == "TEST_apple", "Word should not change"

        print_result("Update Word (Partial)", True, "Partial update successful")
        return True

    except AssertionError as e:
        print_result("Update Word (Partial)", False, str(e))
        return False
    except Exception as e:
        print_result("Update Word (Partial)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 21: Update Word (Success - Update Arrays)
# ==============================================================================
def test_update_word_arrays():
    """Test updating word arrays."""
    print_separator("TEST 21: Update Word (Success - Update Arrays)")

    if not created_word_id:
        print_result("Update Word (Arrays)", False, "No word ID available")
        return False

    url = f"{BASE_URL}/api/v1/words/{created_word_id}"
    print(f"PUT {url}")

    payload = {
        "examples": ["New example 1", "New example 2", "New example 3"],
        "image_urls": ["https://new.com/img1.jpg", "https://new.com/img2.jpg"]
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.put(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"

        word = data["data"]
        assert word["examples"] == payload["examples"], "Examples should be replaced"
        assert word["image_urls"] == payload["image_urls"], "Image URLs should be replaced"

        print_result("Update Word (Arrays)", True, "Arrays updated successfully")
        return True

    except AssertionError as e:
        print_result("Update Word (Arrays)", False, str(e))
        return False
    except Exception as e:
        print_result("Update Word (Arrays)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 22: Update Word (Empty Update)
# ==============================================================================
def test_update_word_empty():
    """Test updating word with no fields (should fail)."""
    print_separator("TEST 22: Update Word (Empty Update)")

    if not created_word_id:
        print_result("Update Word (Empty)", False, "No word ID available")
        return False

    url = f"{BASE_URL}/api/v1/words/{created_word_id}"
    print(f"PUT {url}")

    payload = {}

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.put(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("Update Word (Empty)", True, "Correctly rejected empty update")
        return True

    except AssertionError as e:
        print_result("Update Word (Empty)", False, str(e))
        return False
    except Exception as e:
        print_result("Update Word (Empty)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 23: Update Word (Not Found)
# ==============================================================================
def test_update_word_not_found():
    """Test updating a word that doesn't exist."""
    print_separator("TEST 23: Update Word (Not Found)")

    fake_id = "000000000000000000000000"
    url = f"{BASE_URL}/api/v1/words/{fake_id}"
    print(f"PUT {url}")

    payload = {
        "definition": "Should not exist"
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.put(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("Update Word (Not Found)", True, "Correctly returned 404")
        return True

    except AssertionError as e:
        print_result("Update Word (Not Found)", False, str(e))
        return False
    except Exception as e:
        print_result("Update Word (Not Found)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 24: Delete Word (Success)
# ==============================================================================
def test_delete_word_success():
    """Test deleting a word successfully."""
    global created_word_id

    print_separator("TEST 24: Delete Word (Success)")

    if not created_word_id:
        print_result("Delete Word (Success)", False, "No word ID available")
        return False

    url = f"{BASE_URL}/api/v1/words/{created_word_id}"
    print(f"DELETE {url}")

    try:
        response = requests.delete(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"

        # Verify word is actually deleted
        get_url = f"{BASE_URL}/api/v1/words/{created_word_id}"
        get_response = requests.get(get_url, timeout=5)
        assert get_response.status_code == 404, "Deleted word should return 404"

        print_result("Delete Word (Success)", True, "Word deleted and verified")

        created_word_id = None
        return True

    except AssertionError as e:
        print_result("Delete Word (Success)", False, str(e))
        return False
    except Exception as e:
        print_result("Delete Word (Success)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 25: Delete Word (Not Found)
# ==============================================================================
def test_delete_word_not_found():
    """Test deleting a word that doesn't exist."""
    print_separator("TEST 25: Delete Word (Not Found)")

    fake_id = "000000000000000000000000"
    url = f"{BASE_URL}/api/v1/words/{fake_id}"
    print(f"DELETE {url}")

    try:
        response = requests.delete(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, "Error response should have detail/message"

        print_result("Delete Word (Not Found)", True, "Correctly returned 404")
        return True

    except AssertionError as e:
        print_result("Delete Word (Not Found)", False, str(e))
        return False
    except Exception as e:
        print_result("Delete Word (Not Found)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test Summary
# ==============================================================================
def print_test_summary(results):
    """Print summary of all tests."""
    print_separator()
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 28 + "TEST SUMMARY" + " " * 38 + "║")
    print("╚" + "=" * 78 + "╝")

    total = len(results)
    passed = sum(results.values())
    failed = total - passed

    print(f"\n  Total Tests: {total}")
    print(f"  ✓ Passed: {passed}")
    print(f"  ✗ Failed: {failed}")

    if failed == 0:
        print("\n  🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"\n  ⚠ {failed} test(s) failed")

    print_separator()
    return failed == 0


# ==============================================================================
# CURL Examples (for manual testing)
# ==============================================================================
def print_curl_examples():
    """Print CURL command examples for manual testing."""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 26 + "CURL EXAMPLES" + " " * 39 + "║")
    print("╚" + "=" * 78 + "╝")

    print("\n1. List Words in Folder:")
    print(f"   curl -X GET {BASE_URL}/api/v1/folders/{{folder_id}}/words")

    print("\n2. Create Word:")
    print(f"   curl -X POST {BASE_URL}/api/v1/words \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"word":"apple","folder_id":"...","definition":"A fruit","examples":["I ate an apple"],"image_urls":["https://..."],"part_of_speech":"noun","pronunciation":"/ˈæp.əl/","notes":"Test"}\'')

    print("\n3. Get Single Word:")
    print(f"   curl -X GET {BASE_URL}/api/v1/words/{{word_id}}")

    print("\n4. Update Word:")
    print(f"   curl -X PUT {BASE_URL}/api/v1/words/{{word_id}} \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"definition":"Updated definition","notes":"Updated notes"}\'')

    print("\n5. Delete Word:")
    print(f"   curl -X DELETE {BASE_URL}/api/v1/words/{{word_id}}")

    print("\n6. Open API Documentation in Browser:")
    print(f"   {BASE_URL}/docs")

    print_separator()


# ==============================================================================
# Run All Tests
# ==============================================================================
def run_all_tests():
    """Run all tests and return success status."""
    global test_user_id, test_folder_id

    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "WORD CRUD ENDPOINT TESTS" + " " * 29 + "║")
    print("║" + " " * 25 + "(Simplified - No Token)" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")

    # Setup: Get test user ID
    print("\n🔧 Setup: Getting test user ID...")
    test_user_id = get_test_user_id()
    if test_user_id:
        print(f"✓ Test User ID: {test_user_id}")
    else:
        print("⚠ Could not get test user ID (will continue anyway)")

    # Cleanup before tests (skip if endpoints don't exist yet)
    print("\n🧹 Cleanup: Removing old test data...")
    try:
        cleanup_test_words()
        cleanup_test_folders()
    except Exception:
        print("⚠ Cleanup skipped (endpoints may not exist yet)")

    results = {}

    # Run all tests in order
    results["Setup - Create Test Folder"] = test_setup_create_folder()
    results["List Words (Empty)"] = test_list_words_empty()
    results["Create Word (Success)"] = test_create_word_success()
    results["Create Word (Missing word)"] = test_create_word_missing_word()
    results["Create Word (Missing definition)"] = test_create_word_missing_definition()
    results["Create Word (Missing folder_id)"] = test_create_word_missing_folder_id()
    results["Create Word (Non-existent Folder)"] = test_create_word_nonexistent_folder()
    results["Create Word (Invalid Folder ID)"] = test_create_word_invalid_folder_id()
    results["Create Word (Empty word)"] = test_create_word_empty_word()
    results["Create Word (Empty definition)"] = test_create_word_empty_definition()
    results["Create Word (Minimal)"] = test_create_word_minimal()
    results["Create Word (Empty arrays)"] = test_create_word_empty_arrays()
    results["List Words (With Data)"] = test_list_words_with_data()
    results["List Words (Pagination)"] = test_list_words_pagination()
    results["List Words (Invalid limit)"] = test_list_words_invalid_limit()
    results["List Words (Negative skip)"] = test_list_words_negative_skip()
    results["Get Single Word (Success)"] = test_get_word_success()
    results["Get Single Word (Not Found)"] = test_get_word_not_found()
    results["Get Single Word (Invalid ID)"] = test_get_word_invalid_id()
    results["Update Word (Partial)"] = test_update_word_partial()
    results["Update Word (Arrays)"] = test_update_word_arrays()
    results["Update Word (Empty)"] = test_update_word_empty()
    results["Update Word (Not Found)"] = test_update_word_not_found()
    results["Delete Word (Success)"] = test_delete_word_success()
    results["Delete Word (Not Found)"] = test_delete_word_not_found()

    # Cleanup after tests
    print("\n🧹 Final Cleanup: Removing test data...")
    try:
        cleanup_test_words()
        cleanup_test_folders()
    except Exception as e:
        print(f"⚠ Final cleanup warning: {e}")

    # Print summary
    all_passed = print_test_summary(results)

    # Print CURL examples
    print_curl_examples()

    return all_passed


# ==============================================================================
# Main Entry Point
# ==============================================================================
if __name__ == "__main__":
    try:
        all_passed = run_all_tests()
        sys.exit(0 if all_passed else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ FATAL ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
