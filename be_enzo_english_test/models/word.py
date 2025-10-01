"""
Pydantic models for word management.

Defines request/response schemas for word CRUD operations.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CreateWordRequest(BaseModel):
    """Request model for creating a new word."""

    word: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The word or phrase (1-100 characters)"
    )
    folder_id: str = Field(
        ...,
        description="Folder ID (MongoDB ObjectId as string)"
    )
    definition: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Word definition (1-2000 characters)"
    )
    examples: Optional[List[str]] = Field(
        default_factory=list,
        max_length=20,
        description="Example sentences (max 20 items, each max 500 chars)"
    )
    image_urls: Optional[List[str]] = Field(
        default_factory=list,
        max_length=10,
        description="Image URLs (max 10 items, each max 500 chars)"
    )
    part_of_speech: Optional[str] = Field(
        None,
        max_length=50,
        description="Part of speech (e.g., noun, verb, adjective)"
    )
    pronunciation: Optional[str] = Field(
        None,
        max_length=200,
        description="Pronunciation (IPA or phonetic spelling)"
    )
    notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Additional notes"
    )

    class Config:
        """Pydantic config with example schema."""
        json_schema_extra = {
            "example": {
                "word": "apple",
                "folder_id": "507f1f77bcf86cd799439011",
                "definition": "A round fruit that grows on trees",
                "examples": [
                    "I ate an apple for breakfast",
                    "Apple pie is delicious"
                ],
                "image_urls": ["https://example.com/apple.jpg"],
                "part_of_speech": "noun",
                "pronunciation": "/ˈæp.əl/",
                "notes": "Common fruit vocabulary"
            }
        }


class UpdateWordRequest(BaseModel):
    """Request model for updating an existing word."""

    word: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated word or phrase (1-100 characters)"
    )
    definition: Optional[str] = Field(
        None,
        min_length=1,
        max_length=2000,
        description="Updated definition (1-2000 characters)"
    )
    examples: Optional[List[str]] = Field(
        None,
        max_length=20,
        description="Updated examples (replaces existing, max 20 items)"
    )
    image_urls: Optional[List[str]] = Field(
        None,
        max_length=10,
        description="Updated image URLs (replaces existing, max 10 items)"
    )
    part_of_speech: Optional[str] = Field(
        None,
        max_length=50,
        description="Updated part of speech"
    )
    pronunciation: Optional[str] = Field(
        None,
        max_length=200,
        description="Updated pronunciation"
    )
    notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Updated notes"
    )

    class Config:
        """Pydantic config with example schema."""
        json_schema_extra = {
            "example": {
                "definition": "Updated definition",
                "notes": "Updated notes"
            }
        }


class WordResponse(BaseModel):
    """Response model for word data."""

    id: str = Field(..., description="Word ID (MongoDB ObjectId as string)")
    word: str = Field(..., description="The word or phrase")
    definition: str = Field(..., description="Word definition")
    examples: List[str] = Field(..., description="Example sentences")
    image_urls: List[str] = Field(..., description="Image URLs")
    part_of_speech: Optional[str] = Field(None, description="Part of speech")
    pronunciation: Optional[str] = Field(None, description="Pronunciation")
    notes: Optional[str] = Field(None, description="Additional notes")
    folder_id: str = Field(..., description="Folder ID")
    user_id: str = Field(..., description="User ID (email)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic config with example schema."""
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "word": "apple",
                "definition": "A round fruit that grows on trees",
                "examples": [
                    "I ate an apple for breakfast",
                    "Apple pie is delicious"
                ],
                "image_urls": ["https://example.com/apple.jpg"],
                "part_of_speech": "noun",
                "pronunciation": "/ˈæp.əl/",
                "notes": "Common fruit vocabulary",
                "folder_id": "507f1f77bcf86cd799439012",
                "user_id": "dinhthongchau@gmail.com",
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
        }
