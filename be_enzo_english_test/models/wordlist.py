"""
WordList models for managing collections of words.

Defines request/response schemas for WordList CRUD operations.
WordLists contain arrays of word IDs that reference the global words collection.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


def generate_wordlist_id(user_id: str, folder_id: str) -> str:
    """
    Generate a WordList ID in the format: list_{user_id}_{folder_id}

    Args:
        user_id: User identifier (email or ID)
        folder_id: Folder identifier

    Returns:
        str: Generated WordList ID

    Example:
        generate_wordlist_id("user123", "folder456")
        -> "list_user123_folder456"
    """
    # Clean user_id and folder_id for safe ID generation
    clean_user_id = user_id.replace("@", "_").replace(".", "_")
    clean_folder_id = folder_id.replace("-", "_")
    return f"list_{clean_user_id}_{clean_folder_id}"


class CreateWordListRequest(BaseModel):
    """Request model for creating a new WordList."""

    user_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User identifier (email or ID)",
        example="dinhthongchau@gmail.com",
    )
    folder_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Folder identifier",
        example="68ddfd892672034cf5484e2e",
    )
    words: Optional[List[str]] = Field(
        default_factory=list,
        max_length=1000,
        description="Array of word IDs to include in the WordList",
        example=["APPLE_001", "BANANA_002"],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "dinhthongchau@gmail.com",
                "folder_id": "68ddfd892672034cf5484e2e",
                "words": ["APPLE_001", "BANANA_002", "GRAPE_003"],
            }
        }


class UpdateWordListRequest(BaseModel):
    """Request model for updating WordList metadata (not the words array)."""

    user_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated user identifier",
    )
    folder_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Updated folder identifier",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "folder_id": "new_folder_id_123",
            }
        }


class AddWordsToListRequest(BaseModel):
    """Request model for adding words to a WordList."""

    word_ids: List[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Array of word IDs to add to the WordList",
        example=["APPLE_001", "BANANA_002"],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "word_ids": ["APPLE_001", "BANANA_002", "GRAPE_003"],
            }
        }


class RemoveWordsFromListRequest(BaseModel):
    """Request model for removing words from a WordList."""

    word_ids: List[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Array of word IDs to remove from the WordList",
        example=["APPLE_001"],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "word_ids": ["APPLE_001"],
            }
        }


class WordListResponse(BaseModel):
    """Response model for WordList data (without resolved words)."""

    word_list_id: str = Field(description="Unique WordList identifier")
    user_id: str = Field(description="User identifier")
    folder_id: str = Field(description="Folder identifier")
    words: List[str] = Field(description="Array of word IDs")
    created_at: datetime = Field(description="When the WordList was created")
    updated_at: datetime = Field(description="When the WordList was last updated")

    class Config:
        json_schema_extra = {
            "example": {
                "word_list_id": "list_dinhthongchau_gmail_com_68ddfd892672034cf5484e2e",
                "user_id": "dinhthongchau@gmail.com",
                "folder_id": "68ddfd892672034cf5484e2e",
                "words": ["APPLE_001", "BANANA_002", "GRAPE_003", "ORANGE_004"],
                "created_at": "2025-10-02T10:30:00Z",
                "updated_at": "2025-10-02T11:45:00Z",
            }
        }


class WordListWithWordsResponse(BaseModel):
    """Response model for WordList with resolved word details."""

    word_list_id: str = Field(description="Unique WordList identifier")
    user_id: str = Field(description="User identifier")
    folder_id: str = Field(description="Folder identifier")
    words: List[dict] = Field(description="Array of resolved word objects")
    created_at: datetime = Field(description="When the WordList was created")
    updated_at: datetime = Field(description="When the WordList was last updated")

    class Config:
        json_schema_extra = {
            "example": {
                "word_list_id": "list_dinhthongchau_gmail_com_68ddfd892672034cf5484e2e",
                "user_id": "dinhthongchau@gmail.com",
                "folder_id": "68ddfd892672034cf5484e2e",
                "words": [
                    {
                        "word_id": "APPLE_001",
                        "word": "apple",
                        "definition": "A round red fruit that grows on trees",
                        "example": "I ate an apple for breakfast",
                        "image_url": "image_users/APPLE_001.jpg",
                        "created_at": "2025-10-02T10:00:00Z",
                        "updated_at": "2025-10-02T10:00:00Z",
                    }
                ],
                "created_at": "2025-10-02T10:30:00Z",
                "updated_at": "2025-10-02T11:45:00Z",
            }
        }


class WordListStatsResponse(BaseModel):
    """Response model for WordList statistics."""

    word_list_id: str = Field(description="WordList identifier")
    total_words: int = Field(description="Total number of words in the list")
    words_with_images: int = Field(description="Number of words that have images")
    words_with_examples: int = Field(description="Number of words that have examples")
    last_updated: datetime = Field(description="When the WordList was last updated")

    class Config:
        json_schema_extra = {
            "example": {
                "word_list_id": "list_dinhthongchau_gmail_com_68ddfd892672034cf5484e2e",
                "total_words": 4,
                "words_with_images": 4,
                "words_with_examples": 4,
                "last_updated": "2025-10-02T11:45:00Z",
            }
        }
