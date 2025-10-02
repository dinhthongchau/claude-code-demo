"""
Comprehensive tests for WordLists system.

Tests all CRUD operations, word management, and integration scenarios.
Following TDD principles - these tests should FAIL initially until implementation is complete.
"""

import os
import sys
import io
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

# Add UTF-8 encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Load environment variables
base_dir = Path(__file__).parent.parent
load_dotenv(base_dir / ".env")

# Import app after loading environment
from main import app

# Import pytest after other imports
try:
    import pytest
except ImportError:
    print("pytest not installed. Install with: pip install pytest")
    sys.exit(1)

# Test configuration
BASE_URL = os.getenv("BASE_URL", "http://localhost:8829")
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("MONGO_DB_NAME")

# Test data
TEST_USER_ID = "dinhthongchau@gmail.com"
TEST_FOLDER_ID = "68ddfd892672034cf5484e2e"  # Test Folder from previous setup
TEST_WORD_IDS = ["APPLE_001", "BANANA_002", "GRAPE_003", "ORANGE_004"]


class TestWordListsSystem:
    """Test suite for WordLists system."""

    @pytest.fixture(scope="class")
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture(scope="class")
    async def async_client(self):
        """Create async test client."""
        async with AsyncClient(app=app, base_url=BASE_URL) as client:
            yield client

    @pytest.fixture(scope="class")
    async def db_client(self):
        """Create MongoDB client for direct database operations."""
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        yield db
        client.close()

    @pytest.fixture(autouse=True)
    async def setup_test_data(self, db_client):
        """Set up test data before each test."""
        # Ensure test words exist in global dictionary
        words_collection = db_client["words"]
        
        test_words = [
            {
                "word_id": "APPLE_001",
                "word": "apple",
                "definition": "A round red fruit that grows on trees",
                "example": "I ate an apple for breakfast",
                "image_url": "image_users/APPLE_001.jpg",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "word_id": "BANANA_002",
                "word": "banana",
                "definition": "A long yellow fruit with soft sweet flesh",
                "example": "She peeled a banana and ate it",
                "image_url": "image_users/BANANA_002.jpg",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "word_id": "GRAPE_003",
                "word": "grape",
                "definition": "A small round fruit that grows in clusters",
                "example": "The grapes were sweet and juicy",
                "image_url": "image_users/GRAPE_003.jpg",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "word_id": "ORANGE_004",
                "word": "orange",
                "definition": "A round citrus fruit with thick orange skin",
                "example": "I squeezed fresh orange juice this morning",
                "image_url": "image_users/ORANGE_004.jpg",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
        ]
        
        # Insert test words (ignore duplicates)
        for word in test_words:
            existing = await words_collection.find_one({"word_id": word["word_id"]})
            if not existing:
                await words_collection.insert_one(word)

        # Clean up any existing test WordLists
        wordlists_collection = db_client["wordlists"]
        await wordlists_collection.delete_many({"user_id": TEST_USER_ID})

        yield

        # Cleanup after test
        await wordlists_collection.delete_many({"user_id": TEST_USER_ID})

    # ==============================================================================
    # WordList CRUD Tests
    # ==============================================================================

    def test_create_wordlist_empty(self, client):
        """Test creating a WordList with no words."""
        response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": []
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "WordList created successfully"
        
        wordlist = data["data"]
        assert wordlist["user_id"] == TEST_USER_ID
        assert wordlist["folder_id"] == TEST_FOLDER_ID
        assert wordlist["words"] == []
        assert "word_list_id" in wordlist
        assert "created_at" in wordlist
        assert "updated_at" in wordlist

    def test_create_wordlist_with_words(self, client):
        """Test creating a WordList with initial words."""
        response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001", "BANANA_002"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        wordlist = data["data"]
        assert len(wordlist["words"]) == 2
        assert "APPLE_001" in wordlist["words"]
        assert "BANANA_002" in wordlist["words"]

    def test_create_wordlist_duplicate(self, client):
        """Test creating duplicate WordList should fail."""
        # Create first WordList
        client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": []
            }
        )
        
        # Try to create duplicate
        response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": []
            }
        )
        
        assert response.status_code == 409
        data = response.json()
        assert "already exists" in data["detail"]

    def test_create_wordlist_invalid_word(self, client):
        """Test creating WordList with non-existent word should fail."""
        response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["NONEXISTENT_WORD"]
            }
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "not found in global dictionary" in data["detail"]

    def test_get_wordlist(self, client):
        """Test getting a WordList by ID."""
        # Create WordList first
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001"]
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Get WordList
        response = client.get(f"/api/v1/wordlists/{word_list_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        wordlist = data["data"]
        assert wordlist["word_list_id"] == word_list_id
        assert wordlist["words"] == ["APPLE_001"]

    def test_get_wordlist_not_found(self, client):
        """Test getting non-existent WordList should fail."""
        response = client.get("/api/v1/wordlists/nonexistent_id")
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_get_wordlist_with_words(self, client):
        """Test getting WordList with resolved word details."""
        # Create WordList first
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001", "BANANA_002"]
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Get WordList with resolved words
        response = client.get(f"/api/v1/wordlists/{word_list_id}/words")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        wordlist = data["data"]
        assert len(wordlist["words"]) == 2
        
        # Check that words are resolved (not just IDs)
        for word in wordlist["words"]:
            assert "word_id" in word
            assert "word" in word
            assert "definition" in word
            assert "example" in word
            assert "image_url" in word

    def test_update_wordlist(self, client):
        """Test updating WordList metadata."""
        # Create WordList first
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": []
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Update WordList
        response = client.put(
            f"/api/v1/wordlists/{word_list_id}",
            json={
                "folder_id": "new_folder_id_123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        wordlist = data["data"]
        assert wordlist["folder_id"] == "new_folder_id_123"

    def test_delete_wordlist(self, client):
        """Test deleting a WordList."""
        # Create WordList first
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001"]
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Delete WordList
        response = client.delete(f"/api/v1/wordlists/{word_list_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["deleted"] is True
        
        # Verify WordList is gone
        get_response = client.get(f"/api/v1/wordlists/{word_list_id}")
        assert get_response.status_code == 404

    # ==============================================================================
    # Word Management Tests
    # ==============================================================================

    def test_add_words_to_wordlist(self, client):
        """Test adding words to an existing WordList."""
        # Create WordList first
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001"]
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Add more words
        response = client.post(
            f"/api/v1/wordlists/{word_list_id}/words",
            json={
                "word_ids": ["BANANA_002", "GRAPE_003"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Added 2 words" in data["message"]
        
        wordlist = data["data"]
        assert len(wordlist["words"]) == 3
        assert "APPLE_001" in wordlist["words"]
        assert "BANANA_002" in wordlist["words"]
        assert "GRAPE_003" in wordlist["words"]

    def test_add_duplicate_words(self, client):
        """Test adding duplicate words should be handled gracefully."""
        # Create WordList with initial words
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001", "BANANA_002"]
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Try to add existing and new words
        response = client.post(
            f"/api/v1/wordlists/{word_list_id}/words",
            json={
                "word_ids": ["APPLE_001", "GRAPE_003"]  # APPLE_001 is duplicate
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Added 1 words" in data["message"]
        assert "skipped 1 duplicates" in data["message"]
        
        wordlist = data["data"]
        assert len(wordlist["words"]) == 3  # Should have 3 total (not 4)

    def test_add_invalid_words(self, client):
        """Test adding non-existent words should fail."""
        # Create WordList first
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": []
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Try to add non-existent word
        response = client.post(
            f"/api/v1/wordlists/{word_list_id}/words",
            json={
                "word_ids": ["NONEXISTENT_WORD"]
            }
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "not found in global dictionary" in data["detail"]

    def test_remove_word_from_wordlist(self, client):
        """Test removing a word from WordList."""
        # Create WordList with words
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001", "BANANA_002", "GRAPE_003"]
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Remove one word
        response = client.delete(f"/api/v1/wordlists/{word_list_id}/words/BANANA_002")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "removed from WordList" in data["message"]
        
        wordlist = data["data"]
        assert len(wordlist["words"]) == 2
        assert "APPLE_001" in wordlist["words"]
        assert "GRAPE_003" in wordlist["words"]
        assert "BANANA_002" not in wordlist["words"]

    def test_remove_nonexistent_word(self, client):
        """Test removing word that's not in WordList."""
        # Create WordList with words
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001"]
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Try to remove word that's not in the list
        response = client.delete(f"/api/v1/wordlists/{word_list_id}/words/BANANA_002")
        
        assert response.status_code == 200
        data = response.json()
        assert "was not in WordList" in data["message"]
        
        wordlist = data["data"]
        assert len(wordlist["words"]) == 1  # Should remain unchanged

    # ==============================================================================
    # Convenience Endpoints Tests
    # ==============================================================================

    def test_get_folder_wordlist_with_words(self, client):
        """Test getting WordList for a specific folder (main Flutter endpoint)."""
        # Create WordList first
        client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001", "BANANA_002"]
            }
        )
        
        # Get folder's WordList
        response = client.get(f"/api/v1/users/{TEST_USER_ID}/folders/{TEST_FOLDER_ID}/wordlist")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        wordlist = data["data"]
        assert wordlist["user_id"] == TEST_USER_ID
        assert wordlist["folder_id"] == TEST_FOLDER_ID
        assert len(wordlist["words"]) == 2
        
        # Verify words are resolved
        for word in wordlist["words"]:
            assert "word_id" in word
            assert "word" in word
            assert "definition" in word

    def test_get_folder_wordlist_empty(self, client):
        """Test getting WordList for folder with no WordList (should return empty)."""
        # Don't create WordList, just try to get it
        response = client.get(f"/api/v1/users/{TEST_USER_ID}/folders/nonexistent_folder/wordlist")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "No WordList found" in data["message"]
        
        wordlist = data["data"]
        assert wordlist["words"] == []

    def test_get_wordlist_stats(self, client):
        """Test getting WordList statistics."""
        # Create WordList with words
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": ["APPLE_001", "BANANA_002", "GRAPE_003", "ORANGE_004"]
            }
        )
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # Get stats
        response = client.get(f"/api/v1/wordlists/{word_list_id}/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        stats = data["data"]
        assert stats["total_words"] == 4
        assert stats["words_with_images"] == 4  # All test words have images
        assert stats["words_with_examples"] == 4  # All test words have examples
        assert "last_updated" in stats

    # ==============================================================================
    # Integration Tests
    # ==============================================================================

    def test_complete_workflow(self, client):
        """Test complete WordList workflow: create → add words → get with words → remove word → delete."""
        # 1. Create empty WordList
        create_response = client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": []
            }
        )
        assert create_response.status_code == 200
        word_list_id = create_response.json()["data"]["word_list_id"]
        
        # 2. Add words to WordList
        add_response = client.post(
            f"/api/v1/wordlists/{word_list_id}/words",
            json={
                "word_ids": ["APPLE_001", "BANANA_002", "GRAPE_003"]
            }
        )
        assert add_response.status_code == 200
        assert len(add_response.json()["data"]["words"]) == 3
        
        # 3. Get WordList with resolved words
        get_response = client.get(f"/api/v1/wordlists/{word_list_id}/words")
        assert get_response.status_code == 200
        wordlist = get_response.json()["data"]
        assert len(wordlist["words"]) == 3
        
        # Verify words are fully resolved
        apple_word = next(w for w in wordlist["words"] if w["word_id"] == "APPLE_001")
        assert apple_word["word"] == "apple"
        assert apple_word["definition"] == "A round red fruit that grows on trees"
        
        # 4. Remove one word
        remove_response = client.delete(f"/api/v1/wordlists/{word_list_id}/words/BANANA_002")
        assert remove_response.status_code == 200
        assert len(remove_response.json()["data"]["words"]) == 2
        
        # 5. Delete WordList
        delete_response = client.delete(f"/api/v1/wordlists/{word_list_id}")
        assert delete_response.status_code == 200
        
        # 6. Verify deletion
        final_get_response = client.get(f"/api/v1/wordlists/{word_list_id}")
        assert final_get_response.status_code == 404

    def test_flutter_integration_scenario(self, client):
        """Test the exact scenario Flutter will use: folder → WordList → display words."""
        # 1. Create WordList for folder (simulating folder creation)
        client.post(
            "/api/v1/wordlists",
            json={
                "user_id": TEST_USER_ID,
                "folder_id": TEST_FOLDER_ID,
                "words": []
            }
        )
        
        # 2. Add words to folder (simulating adding words via UI)
        word_list_id = f"list_{TEST_USER_ID.replace('@', '_').replace('.', '_')}_{TEST_FOLDER_ID}"
        client.post(
            f"/api/v1/wordlists/{word_list_id}/words",
            json={
                "word_ids": ["APPLE_001", "BANANA_002", "GRAPE_003", "ORANGE_004"]
            }
        )
        
        # 3. Flutter fetches words for display (main endpoint)
        response = client.get(f"/api/v1/users/{TEST_USER_ID}/folders/{TEST_FOLDER_ID}/wordlist")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        wordlist = data["data"]
        assert len(wordlist["words"]) == 4
        
        # Verify all data needed for Flutter display is present
        for word in wordlist["words"]:
            assert word["word_id"] is not None
            assert word["word"] is not None
            assert word["definition"] is not None
            assert word["example"] is not None
            assert word["image_url"] is not None
            assert word["created_at"] is not None
            assert word["updated_at"] is not None


# ==============================================================================
# Test Runner
# ==============================================================================

if __name__ == "__main__":
    """Run tests directly with pytest."""
    import subprocess
    import sys
    
    print("🧪 Running WordLists System Tests...")
    print("=" * 60)
    
    # Run pytest with verbose output
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        __file__, 
        "-v", 
        "--tb=short",
        "--color=yes"
    ], capture_output=False)
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Tests failed with exit code: {result.returncode}")
    
    sys.exit(result.returncode)
