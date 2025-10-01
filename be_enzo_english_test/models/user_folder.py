"""
Pydantic models for user folder management.

Defines request/response schemas for folder CRUD operations.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateFolderRequest(BaseModel):
    """Request model for creating a new folder."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Folder name (1-100 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional folder description (max 500 characters)"
    )
    color: Optional[str] = Field(
        None,
        pattern="^#[0-9A-Fa-f]{6}$",
        description="Optional hex color code (e.g., #FF5733)"
    )
    icon: Optional[str] = Field(
        None,
        description="Optional emoji or icon"
    )

    class Config:
        """Pydantic config with example schema."""
        json_schema_extra = {
            "example": {
                "name": "My Vocabulary",
                "description": "Collection of English vocabulary words",
                "color": "#FF5733",
                "icon": "📚"
            }
        }


class UpdateFolderRequest(BaseModel):
    """Request model for updating an existing folder."""

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated folder name (1-100 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Updated folder description (max 500 characters)"
    )
    color: Optional[str] = Field(
        None,
        pattern="^#[0-9A-Fa-f]{6}$",
        description="Updated hex color code (e.g., #00FF00)"
    )
    icon: Optional[str] = Field(
        None,
        description="Updated emoji or icon"
    )

    class Config:
        """Pydantic config with example schema."""
        json_schema_extra = {
            "example": {
                "name": "Updated Vocabulary",
                "color": "#00FF00"
            }
        }


class FolderResponse(BaseModel):
    """Response model for folder data."""

    id: str = Field(..., description="Folder ID (MongoDB ObjectId as string)")
    name: str = Field(..., description="Folder name")
    description: Optional[str] = Field(None, description="Folder description")
    user_id: str = Field(..., description="User ID (email)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    color: Optional[str] = Field(None, description="Folder color (hex)")
    icon: Optional[str] = Field(None, description="Folder icon (emoji)")

    class Config:
        """Pydantic config with example schema."""
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "My Vocabulary",
                "description": "Collection of English vocabulary words",
                "user_id": "dinhthongchau@gmail.com",
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00",
                "color": "#FF5733",
                "icon": "📚"
            }
        }
