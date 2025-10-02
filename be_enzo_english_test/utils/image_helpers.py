"""
Image handling utilities for word images.
Handles upload, validation, and serving of images from image_users/ folder.
"""

import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
import mimetypes


# Constants
IMAGE_USERS_DIR = "image_users"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}


def ensure_image_directory():
    """Ensure image_users directory exists"""
    os.makedirs(IMAGE_USERS_DIR, exist_ok=True)


def validate_image_file(file: UploadFile) -> None:
    """
    Validate uploaded image file format and size.

    Args:
        file: FastAPI UploadFile object

    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    if file.filename:
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
            )

    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type. Allowed: {', '.join(ALLOWED_MIME_TYPES)}",
        )

    # Check file size (if available)
    if hasattr(file, "size") and file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024 * 1024)}MB",
        )


def save_word_image(word_id: str, image_file: UploadFile) -> str:
    """
    Save uploaded image to image_users/ folder.

    Args:
        word_id: Unique word identifier
        image_file: FastAPI UploadFile object

    Returns:
        str: Relative path to saved image

    Raises:
        HTTPException: If save operation fails
    """
    try:
        # Validate file
        validate_image_file(image_file)

        # Ensure directory exists
        ensure_image_directory()

        # Get file extension
        file_ext = (
            Path(image_file.filename).suffix.lower() if image_file.filename else ".jpg"
        )

        # Generate filename: {word_id}.{extension}
        filename = f"{word_id}{file_ext}"
        file_path = os.path.join(IMAGE_USERS_DIR, filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image_file.file, buffer)

        # Return relative path
        return file_path.replace("\\", "/")  # Normalize path separators

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")


def get_word_image_path(word_id: str) -> Optional[str]:
    """
    Get full file path for word image.

    Args:
        word_id: Unique word identifier

    Returns:
        str: Full file path if image exists, None otherwise
    """
    # Check for any supported extension
    for ext in ALLOWED_EXTENSIONS:
        filename = f"{word_id}{ext}"
        file_path = os.path.join(IMAGE_USERS_DIR, filename)
        if os.path.exists(file_path):
            return file_path

    return None


def delete_word_image(word_id: str) -> bool:
    """
    Delete word image if it exists.

    Args:
        word_id: Unique word identifier

    Returns:
        bool: True if image was deleted, False if not found
    """
    image_path = get_word_image_path(word_id)
    if image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
            return True
        except Exception:
            return False
    return False


def get_image_mime_type(file_path: str) -> str:
    """
    Get MIME type for image file.

    Args:
        file_path: Path to image file

    Returns:
        str: MIME type (defaults to 'image/jpeg')
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or "image/jpeg"


def get_relative_image_url(word_id: str) -> Optional[str]:
    """
    Get relative URL for word image (for storing in database).

    Args:
        word_id: Unique word identifier

    Returns:
        str: Relative path if image exists, None otherwise
    """
    image_path = get_word_image_path(word_id)
    if image_path:
        return image_path.replace("\\", "/")  # Normalize path separators
    return None
