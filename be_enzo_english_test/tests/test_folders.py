"""
Test file for folder CRUD endpoints.

Simplified version - no Firebase token required.
Run this file to test all folder management endpoints.

Usage:
    python tests/test_folders.py
"""

import requests
import json
import sys
import io
import os
from typing import Optional, Dict, Any
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

# Global variable to store created folder ID for tests
created_folder_id: Optional[str] = None
test_user_id: Optional[str] = None


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


def cleanup_test_folders():
    """Delete all folders with TEST_ prefix to clean up after tests."""
    try:
        # Get all folders
        url = f"{BASE_URL}/api/v1/folders"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            folders = data.get("data", [])

            # Delete folders with TEST_ prefix
            deleted_count = 0
            for folder in folders:
                if folder.get("name", "").startswith("TEST_"):
                    folder_id = folder.get("id")
                    delete_url = f"{BASE_URL}/api/v1/folders/{folder_id}"
                    delete_response = requests.delete(delete_url, timeout=5)
                    if delete_response.status_code == 200:
                        deleted_count += 1

            if deleted_count > 0:
                print(f"\n🧹 Cleaned up {deleted_count} test folder(s)")
    except Exception as e:
        print(f"\n⚠ Cleanup warning: {e}")


# ==============================================================================
# Test 1: List Folders (Empty State - after cleanup)
# ==============================================================================
def test_list_folders_empty():
    """Test listing folders when empty."""
    print_separator("TEST 1: List Folders (Empty State)")

    url = f"{BASE_URL}/api/v1/folders"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"] == True, "Response should be successful"
        assert "data" in data, "Response should contain data"
        assert isinstance(data["data"], list), "Data should be a list"

        # After cleanup, should have no TEST_ folders
        test_folders = [
            f for f in data["data"] if f.get("name", "").startswith("TEST_")
        ]
        assert len(test_folders) == 0, "Should have no TEST_ folders after cleanup"

        print_result(
            "List Folders (Empty)",
            True,
            f"Total folders: {len(data['data'])}, TEST_ folders: 0",
        )
        return True

    except requests.exceptions.ConnectionError:
        print_result("List Folders (Empty)", False, "Could not connect to server")
        return False
    except AssertionError as e:
        print_result("List Folders (Empty)", False, str(e))
        return False
    except Exception as e:
        print_result("List Folders (Empty)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 2: Create Folder (Success)
# ==============================================================================
def test_create_folder_success():
    """Test creating a new folder successfully."""
    global created_folder_id

    print_separator("TEST 2: Create Folder (Success)")

    url = f"{BASE_URL}/api/v1/folders"
    print(f"POST {url}")

    payload = {
        "name": "TEST_My Vocabulary",
        "description": "Test folder for vocabulary words",
        "color": "#FF5733",
        "icon": "📚",
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"] == True, "Response should be successful"
        assert "data" in data, "Response should contain data"

        folder = data["data"]
        assert "id" in folder, "Folder should have an id"
        assert isinstance(folder["id"], str), "Folder id should be a string"
        assert len(folder["id"]) == 24, "Folder id should be 24 characters (ObjectId)"

        assert folder["name"] == payload["name"], "Folder name should match"
        assert folder["description"] == payload["description"], (
            "Description should match"
        )
        assert folder["color"] == payload["color"], "Color should match"
        assert folder["icon"] == payload["icon"], "Icon should match"

        assert "user_id" in folder, "Folder should have user_id"
        assert "created_at" in folder, "Folder should have created_at"
        assert "updated_at" in folder, "Folder should have updated_at"

        # Save folder ID for subsequent tests
        created_folder_id = folder["id"]

        print_result("Create Folder (Success)", True)
        print(f"  → Folder ID: {created_folder_id}")
        print(f"  → Name: {folder['name']}")
        return True

    except requests.exceptions.ConnectionError:
        print_result("Create Folder (Success)", False, "Could not connect to server")
        return False
    except AssertionError as e:
        print_result("Create Folder (Success)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Folder (Success)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 3: Create Folder (Missing Name)
# ==============================================================================
def test_create_folder_missing_name():
    """Test creating folder without name (should fail)."""
    print_separator("TEST 3: Create Folder (Missing Name)")

    url = f"{BASE_URL}/api/v1/folders"
    print(f"POST {url}")

    payload = {"description": "No name provided"}

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions - should fail with 400 or 422
        assert response.status_code in [400, 422], (
            f"Expected 400 or 422, got {response.status_code}"
        )

        data = response.json()
        # FastAPI validation errors have "detail" field
        assert "detail" in data, "Error response should contain detail"

        print_result(
            "Create Folder (Missing Name)", True, "Correctly rejected missing name"
        )
        return True

    except AssertionError as e:
        print_result("Create Folder (Missing Name)", False, str(e))
        return False
    except Exception as e:
        print_result(
            "Create Folder (Missing Name)", False, f"Unexpected error: {str(e)}"
        )
        return False


# ==============================================================================
# Test 4: Create Folder (Empty Name)
# ==============================================================================
def test_create_folder_empty_name():
    """Test creating folder with empty name (should fail)."""
    print_separator("TEST 4: Create Folder (Empty Name)")

    url = f"{BASE_URL}/api/v1/folders"
    print(f"POST {url}")

    payload = {"name": "", "description": "Empty name"}

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions - should fail with 400 or 422
        assert response.status_code in [400, 422], (
            f"Expected 400 or 422, got {response.status_code}"
        )

        data = response.json()
        assert "detail" in data, "Error response should contain detail"

        print_result(
            "Create Folder (Empty Name)", True, "Correctly rejected empty name"
        )
        return True

    except AssertionError as e:
        print_result("Create Folder (Empty Name)", False, str(e))
        return False
    except Exception as e:
        print_result("Create Folder (Empty Name)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 5: List Folders (With Data)
# ==============================================================================
def test_list_folders_with_data():
    """Test listing folders when data exists."""
    print_separator("TEST 5: List Folders (With Data)")

    url = f"{BASE_URL}/api/v1/folders"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"] == True, "Response should be successful"
        assert "data" in data, "Response should contain data"
        assert isinstance(data["data"], list), "Data should be a list"
        assert len(data["data"]) > 0, "Should have at least one folder"

        # Check each folder has required fields
        for folder in data["data"]:
            assert "id" in folder, "Each folder should have id"
            assert "name" in folder, "Each folder should have name"
            assert "user_id" in folder, "Each folder should have user_id"
            assert "created_at" in folder, "Each folder should have created_at"

        # Check that our test folder exists
        test_folder = next(
            (f for f in data["data"] if f["id"] == created_folder_id), None
        )
        assert test_folder is not None, "Created test folder should be in the list"

        print_result(
            "List Folders (With Data)", True, f"Found {len(data['data'])} folder(s)"
        )
        return True

    except AssertionError as e:
        print_result("List Folders (With Data)", False, str(e))
        return False
    except Exception as e:
        print_result("List Folders (With Data)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 6: Get Single Folder (Success)
# ==============================================================================
def test_get_folder_success():
    """Test getting a single folder by ID."""
    print_separator("TEST 6: Get Single Folder (Success)")

    if not created_folder_id:
        print_result("Get Single Folder (Success)", False, "No folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/folders/{created_folder_id}"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"] == True, "Response should be successful"
        assert "data" in data, "Response should contain data"

        folder = data["data"]
        assert folder["id"] == created_folder_id, "Folder ID should match"
        assert folder["name"] == "TEST_My Vocabulary", "Name should match"
        assert "description" in folder, "Should have description"
        assert "color" in folder, "Should have color"
        assert "icon" in folder, "Should have icon"
        assert "user_id" in folder, "Should have user_id"
        assert "created_at" in folder, "Should have created_at"
        assert "updated_at" in folder, "Should have updated_at"

        print_result(
            "Get Single Folder (Success)", True, f"Retrieved folder: {folder['name']}"
        )
        return True

    except AssertionError as e:
        print_result("Get Single Folder (Success)", False, str(e))
        return False
    except Exception as e:
        print_result(
            "Get Single Folder (Success)", False, f"Unexpected error: {str(e)}"
        )
        return False


# ==============================================================================
# Test 7: Get Single Folder (Not Found)
# ==============================================================================
def test_get_folder_not_found():
    """Test getting a folder that doesn't exist."""
    print_separator("TEST 7: Get Single Folder (Not Found)")

    # Valid ObjectId format but doesn't exist
    fake_id = "000000000000000000000000"
    url = f"{BASE_URL}/api/v1/folders/{fake_id}"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, (
            "Error response should have detail/message"
        )

        print_result("Get Single Folder (Not Found)", True, "Correctly returned 404")
        return True

    except AssertionError as e:
        print_result("Get Single Folder (Not Found)", False, str(e))
        return False
    except Exception as e:
        print_result(
            "Get Single Folder (Not Found)", False, f"Unexpected error: {str(e)}"
        )
        return False


# ==============================================================================
# Test 8: Get Single Folder (Invalid ID)
# ==============================================================================
def test_get_folder_invalid_id():
    """Test getting a folder with invalid ObjectId format."""
    print_separator("TEST 8: Get Single Folder (Invalid ID)")

    invalid_id = "invalid_id_format"
    url = f"{BASE_URL}/api/v1/folders/{invalid_id}"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions - should fail with 400
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, (
            "Error response should have detail/message"
        )

        print_result(
            "Get Single Folder (Invalid ID)", True, "Correctly rejected invalid ID"
        )
        return True

    except AssertionError as e:
        print_result("Get Single Folder (Invalid ID)", False, str(e))
        return False
    except Exception as e:
        print_result(
            "Get Single Folder (Invalid ID)", False, f"Unexpected error: {str(e)}"
        )
        return False


# ==============================================================================
# Test 9: Update Folder (Success)
# ==============================================================================
def test_update_folder_success():
    """Test updating a folder successfully."""
    print_separator("TEST 9: Update Folder (Success)")

    if not created_folder_id:
        print_result("Update Folder (Success)", False, "No folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/folders/{created_folder_id}"
    print(f"PUT {url}")

    payload = {
        "name": "TEST_Updated Vocabulary",
        "color": "#00FF00",
        "description": "Updated description",
    }

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.put(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"] == True, "Response should be successful"
        assert "data" in data, "Response should contain data"

        folder = data["data"]
        assert folder["id"] == created_folder_id, "Folder ID should not change"
        assert folder["name"] == payload["name"], "Name should be updated"
        assert folder["color"] == payload["color"], "Color should be updated"
        assert folder["description"] == payload["description"], (
            "Description should be updated"
        )

        # updated_at should be more recent than created_at
        assert "updated_at" in folder, "Should have updated_at"
        assert "created_at" in folder, "Should have created_at"

        print_result("Update Folder (Success)", True, f"Updated to: {folder['name']}")
        return True

    except AssertionError as e:
        print_result("Update Folder (Success)", False, str(e))
        return False
    except Exception as e:
        print_result("Update Folder (Success)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 10: Update Folder (Not Found)
# ==============================================================================
def test_update_folder_not_found():
    """Test updating a folder that doesn't exist."""
    print_separator("TEST 10: Update Folder (Not Found)")

    fake_id = "000000000000000000000000"
    url = f"{BASE_URL}/api/v1/folders/{fake_id}"
    print(f"PUT {url}")

    payload = {"name": "TEST_Should Not Exist"}

    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.put(url, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, (
            "Error response should have detail/message"
        )

        print_result("Update Folder (Not Found)", True, "Correctly returned 404")
        return True

    except AssertionError as e:
        print_result("Update Folder (Not Found)", False, str(e))
        return False
    except Exception as e:
        print_result("Update Folder (Not Found)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 11: Delete Folder (Success)
# ==============================================================================
def test_delete_folder_success():
    """Test deleting a folder successfully."""
    global created_folder_id

    print_separator("TEST 11: Delete Folder (Success)")

    if not created_folder_id:
        print_result("Delete Folder (Success)", False, "No folder ID available")
        return False

    url = f"{BASE_URL}/api/v1/folders/{created_folder_id}"
    print(f"DELETE {url}")

    try:
        response = requests.delete(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"] == True, "Response should be successful"

        # Verify folder is actually deleted by trying to get it
        get_url = f"{BASE_URL}/api/v1/folders/{created_folder_id}"
        get_response = requests.get(get_url, timeout=5)
        assert get_response.status_code == 404, "Deleted folder should return 404"

        print_result("Delete Folder (Success)", True, "Folder deleted and verified")

        # Clear the folder ID since it's deleted
        created_folder_id = None
        return True

    except AssertionError as e:
        print_result("Delete Folder (Success)", False, str(e))
        return False
    except Exception as e:
        print_result("Delete Folder (Success)", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 12: Delete Folder (Not Found)
# ==============================================================================
def test_delete_folder_not_found():
    """Test deleting a folder that doesn't exist."""
    print_separator("TEST 12: Delete Folder (Not Found)")

    fake_id = "000000000000000000000000"
    url = f"{BASE_URL}/api/v1/folders/{fake_id}"
    print(f"DELETE {url}")

    try:
        response = requests.delete(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

        data = response.json()
        assert "detail" in data or "message" in data, (
            "Error response should have detail/message"
        )

        print_result("Delete Folder (Not Found)", True, "Correctly returned 404")
        return True

    except AssertionError as e:
        print_result("Delete Folder (Not Found)", False, str(e))
        return False
    except Exception as e:
        print_result("Delete Folder (Not Found)", False, f"Unexpected error: {str(e)}")
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

    print("\n1. List All Folders:")
    print(f"   curl -X GET {BASE_URL}/api/v1/folders")

    print("\n2. Create Folder:")
    print(f"   curl -X POST {BASE_URL}/api/v1/folders \\")
    print('     -H "Content-Type: application/json" \\')
    print(
        '     -d \'{"name":"My Vocabulary","description":"My words","color":"#FF5733","icon":"📚"}\''
    )

    print("\n3. Get Single Folder:")
    print(f"   curl -X GET {BASE_URL}/api/v1/folders/{{folder_id}}")

    print("\n4. Update Folder:")
    print(f"   curl -X PUT {BASE_URL}/api/v1/folders/{{folder_id}} \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"name":"Updated Name","color":"#00FF00"}\'')

    print("\n5. Delete Folder:")
    print(f"   curl -X DELETE {BASE_URL}/api/v1/folders/{{folder_id}}")

    print("\n6. Open API Documentation in Browser:")
    print(f"   {BASE_URL}/docs")

    print_separator()


# ==============================================================================
# Run All Tests
# ==============================================================================
def run_all_tests():
    """Run all tests and return success status."""
    global test_user_id

    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 24 + "FOLDER CRUD ENDPOINT TESTS" + " " * 28 + "║")
    print("║" + " " * 25 + "(Simplified - No Token)" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")

    # Setup: Get test user ID
    print("\n🔧 Setup: Getting test user ID...")
    test_user_id = get_test_user_id()
    if test_user_id:
        print(f"✓ Test User ID: {test_user_id}")
    else:
        print("⚠ Could not get test user ID (will continue anyway)")

    # Cleanup before tests
    print("\n🧹 Cleanup: Removing old test folders...")
    cleanup_test_folders()

    results = {}

    # Run all tests in order
    results["List Folders (Empty)"] = test_list_folders_empty()
    results["Create Folder (Success)"] = test_create_folder_success()
    results["Create Folder (Missing Name)"] = test_create_folder_missing_name()
    results["Create Folder (Empty Name)"] = test_create_folder_empty_name()
    results["List Folders (With Data)"] = test_list_folders_with_data()
    results["Get Single Folder (Success)"] = test_get_folder_success()
    results["Get Single Folder (Not Found)"] = test_get_folder_not_found()
    results["Get Single Folder (Invalid ID)"] = test_get_folder_invalid_id()
    results["Update Folder (Success)"] = test_update_folder_success()
    results["Update Folder (Not Found)"] = test_update_folder_not_found()
    results["Delete Folder (Success)"] = test_delete_folder_success()
    results["Delete Folder (Not Found)"] = test_delete_folder_not_found()

    # Cleanup after tests
    print("\n🧹 Final Cleanup: Removing test folders...")
    cleanup_test_folders()

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
