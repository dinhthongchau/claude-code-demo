"""
Simplified words router for global word dictionary management.
Handles CRUD operations for words and image upload/serving.
"""

import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from motor.motor_asyncio import AsyncIOMotorCollection

from dependencies import get_words_collection, ApiResponse
from models.simplified_word import (
    CreateWordRequest,
    UpdateWordRequest,
    WordResponse,
    ImageUploadResponse,
)
from utils.image_helpers import (
    save_word_image,
    get_word_image_path,
    get_image_mime_type,
    delete_word_image,
)


router = APIRouter(prefix="/api/v1/global", tags=["Global Word Dictionary"])


def convert_word_to_response(word_doc: dict) -> dict:
    """Convert MongoDB word document to response format"""
    return {
        "word_id": word_doc["word_id"],
        "word": word_doc["word"],
        "definition": word_doc["definition"],
        "example": word_doc.get("example"),
        "image_url": word_doc.get("image_url"),
        "created_at": word_doc["created_at"],
        "updated_at": word_doc["updated_at"],
    }


@router.post("/words", response_model=ApiResponse[WordResponse])
async def create_word(
    request: CreateWordRequest,
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Create a new word in the global dictionary.

    - **word_id**: Unique business identifier for the word
    - **word**: The actual vocabulary word
    - **definition**: Word meaning/definition
    - **example**: Optional example sentence
    """
    try:
        # Check if word_id already exists
        existing_word = await words_collection.find_one({"word_id": request.word_id})
        if existing_word:
            raise HTTPException(
                status_code=409,
                detail=f"Word with ID '{request.word_id}' already exists",
            )

        # Create word document
        now = datetime.utcnow()
        word_doc = {
            "word_id": request.word_id,
            "word": request.word,
            "definition": request.definition,
            "example": request.example,
            "image_url": None,  # No image initially
            "created_at": now,
            "updated_at": now,
        }

        # Insert into database
        result = await words_collection.insert_one(word_doc)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create word")

        # Return response
        response_data = convert_word_to_response(word_doc)
        return ApiResponse(
            success=True,
            message="Word created successfully",
            data=response_data,
            timestamp=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/words/{word_id}", response_model=ApiResponse[WordResponse])
async def get_word(
    word_id: str,
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Get a word from the global dictionary by word_id.
    """
    try:
        # Find word by word_id
        word_doc = await words_collection.find_one({"word_id": word_id})
        if not word_doc:
            raise HTTPException(
                status_code=404, detail=f"Word with ID '{word_id}' not found"
            )

        # Return response
        response_data = convert_word_to_response(word_doc)
        return ApiResponse(
            success=True,
            message="Word retrieved successfully",
            data=response_data,
            timestamp=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/words/{word_id}", response_model=ApiResponse[WordResponse])
async def update_word(
    word_id: str,
    request: UpdateWordRequest,
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Update a word in the global dictionary.
    All fields are optional - only provided fields will be updated.
    """
    try:
        # Build update dictionary (exclude unset fields)
        update_data = {k: v for k, v in request.model_dump(exclude_unset=True).items()}

        # Check if there's anything to update
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        # Add updated timestamp
        update_data["updated_at"] = datetime.utcnow()

        # Update word
        result = await words_collection.update_one(
            {"word_id": word_id}, {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404, detail=f"Word with ID '{word_id}' not found"
            )

        # Get updated word
        updated_word = await words_collection.find_one({"word_id": word_id})

        # Return response
        response_data = convert_word_to_response(updated_word)
        return ApiResponse(
            success=True,
            message="Word updated successfully",
            data=response_data,
            timestamp=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/words/{word_id}/image", response_model=ApiResponse[ImageUploadResponse])
async def upload_word_image(
    word_id: str,
    image: UploadFile = File(...),
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Upload an image for a word. Saves to image_users/ folder.

    - **Supported formats**: JPG, PNG, WebP
    - **Max size**: 5MB
    - **Naming**: {word_id}.{extension}
    """
    try:
        # Check if word exists
        word_doc = await words_collection.find_one({"word_id": word_id})
        if not word_doc:
            raise HTTPException(
                status_code=404, detail=f"Word with ID '{word_id}' not found"
            )

        # Delete existing image if any
        delete_word_image(word_id)

        # Save new image
        image_path = save_word_image(word_id, image)

        # Update word document with image URL
        await words_collection.update_one(
            {"word_id": word_id},
            {"$set": {"image_url": image_path, "updated_at": datetime.utcnow()}},
        )

        # Return response
        response_data = {
            "message": "Image uploaded successfully",
            "image_url": image_path,
            "word_id": word_id,
        }

        return ApiResponse(
            success=True,
            message="Image uploaded successfully",
            data=response_data,
            timestamp=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/words/{word_id}/image")
async def get_word_image(word_id: str):
    """
    Serve word image file from image_users/ folder.
    Returns the actual image file with proper content-type.
    """
    try:
        # Get image path
        image_path = get_word_image_path(word_id)
        if not image_path or not os.path.exists(image_path):
            raise HTTPException(
                status_code=404, detail=f"Image not found for word '{word_id}'"
            )

        # Get MIME type
        media_type = get_image_mime_type(image_path)

        # Return file
        return FileResponse(
            path=image_path,
            media_type=media_type,
            filename=os.path.basename(image_path),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/words/{word_id}")
async def delete_word(
    word_id: str,
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Delete a word from the global dictionary.
    Also deletes associated image file.
    """
    try:
        # Check if word exists
        word_doc = await words_collection.find_one({"word_id": word_id})
        if not word_doc:
            raise HTTPException(
                status_code=404, detail=f"Word with ID '{word_id}' not found"
            )

        # Delete word from database
        result = await words_collection.delete_one({"word_id": word_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete word")

        # Delete associated image
        delete_word_image(word_id)

        return ApiResponse(
            success=True,
            message="Word deleted successfully",
            data=None,
            timestamp=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
