"""
Simplified word models for AI bubble feature preparation.
Focuses on essential fields: word_id, word, definition, example, image_url
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateWordRequest(BaseModel):
    """Request model for creating a word in global dictionary"""

    word_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Unique business identifier for the word",
        example="apple_001",
    )
    word: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The actual vocabulary word",
        example="apple",
    )
    definition: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Word meaning/definition",
        example="A round red fruit that grows on trees",
    )
    example: Optional[str] = Field(
        None,
        max_length=500,
        description="Single example sentence using the word",
        example="I ate an apple for breakfast",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "word_id": "apple_001",
                "word": "apple",
                "definition": "A round red fruit that grows on trees",
                "example": "I ate an apple for breakfast",
            }
        }


class UpdateWordRequest(BaseModel):
    """Request model for updating a word (all fields optional)"""

    word: Optional[str] = Field(
        None, min_length=1, max_length=100, description="The actual vocabulary word"
    )
    definition: Optional[str] = Field(
        None, min_length=1, max_length=1000, description="Word meaning/definition"
    )
    example: Optional[str] = Field(
        None, max_length=500, description="Single example sentence using the word"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "definition": "Updated definition of the word",
                "example": "Updated example sentence",
            }
        }


class WordResponse(BaseModel):
    """Response model for word data from global dictionary"""

    word_id: str = Field(description="Unique business identifier")
    word: str = Field(description="The vocabulary word")
    definition: str = Field(description="Word definition")
    example: Optional[str] = Field(description="Example sentence")
    image_url: Optional[str] = Field(
        description="Relative path to image in image_users/ folder"
    )
    created_at: datetime = Field(description="When the word was created")
    updated_at: datetime = Field(description="When the word was last updated")

    class Config:
        json_schema_extra = {
            "example": {
                "word_id": "apple_001",
                "word": "apple",
                "definition": "A round red fruit that grows on trees",
                "example": "I ate an apple for breakfast",
                "image_url": "image_users/apple_001.jpg",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
            }
        }


class AddWordToFolderRequest(BaseModel):
    """Request model for adding existing word to user's folder"""

    word_id: str = Field(
        ..., description="ID of existing word to add to folder", example="apple_001"
    )

    class Config:
        json_schema_extra = {"example": {"word_id": "apple_001"}}


class WordInFolderResponse(BaseModel):
    """Response model for word assigned to user's folder (merged data)"""

    id: str = Field(description="MongoDB ObjectId as string")
    word_id: str = Field(description="Business identifier of the word")
    word: str = Field(description="The vocabulary word")
    definition: str = Field(description="Word definition")
    example: Optional[str] = Field(description="Example sentence")
    image_url: Optional[str] = Field(description="Relative path to image")
    folder_id: str = Field(description="Folder ObjectId as string")
    user_id: str = Field(description="User identifier (email)")
    created_at: datetime = Field(description="When word was added to folder")
    updated_at: datetime = Field(description="When assignment was last updated")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "word_id": "apple_001",
                "word": "apple",
                "definition": "A round red fruit that grows on trees",
                "example": "I ate an apple for breakfast",
                "image_url": "image_users/apple_001.jpg",
                "folder_id": "507f1f77bcf86cd799439012",
                "user_id": "dinhthongchau@gmail.com",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
            }
        }


class ImageUploadResponse(BaseModel):
    """Response model for image upload"""

    message: str = Field(description="Success message")
    image_url: str = Field(description="Relative path to uploaded image")
    word_id: str = Field(description="Word ID the image belongs to")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Image uploaded successfully",
                "image_url": "image_users/apple_001.jpg",
                "word_id": "apple_001",
            }
        }
