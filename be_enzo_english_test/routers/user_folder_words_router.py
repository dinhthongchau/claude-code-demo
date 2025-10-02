"""
User folder words router for managing word assignments to user folders.
Handles adding/removing words from user's specific folders.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId

from dependencies import (
    get_words_collection,
    get_folders_collection,
    get_users_collection,
    get_user_folder_words_collection,
    ApiResponse,
    HARDCODED_EMAIL,
)
from models.simplified_word import AddWordToFolderRequest, WordInFolderResponse


router = APIRouter(prefix="/api/v1", tags=["User Folder Words"])


def validate_object_id(id_str: str) -> ObjectId:
    """Validate and convert string to ObjectId"""
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(
            status_code=400, detail=f"Invalid ObjectId format: {id_str}"
        )


async def get_hardcoded_user(users_collection: AsyncIOMotorCollection) -> dict:
    """Get or create hardcoded test user"""
    user = await users_collection.find_one({"email": HARDCODED_EMAIL})
    if not user:
        # Create user if not exists
        user_doc = {
            "email": HARDCODED_EMAIL,
            "name": "Test User",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await users_collection.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        user = user_doc

    return user


async def validate_user_folder_ownership(
    user_id: str, folder_id: ObjectId, folders_collection: AsyncIOMotorCollection
) -> dict:
    """Validate that folder belongs to user"""
    print(f"DEBUG: Looking for folder with _id={folder_id} and user_id='{user_id}'")
    folder = await folders_collection.find_one({"_id": folder_id, "user_id": user_id})
    print(f"DEBUG: Found folder: {folder}")

    if not folder:
        raise HTTPException(
            status_code=404, detail="Folder not found or doesn't belong to user"
        )

    return folder


async def validate_word_exists(
    word_id: str, words_collection: AsyncIOMotorCollection
) -> dict:
    """Validate that word exists in global dictionary"""
    word = await words_collection.find_one({"word_id": word_id})
    if not word:
        raise HTTPException(
            status_code=404,
            detail=f"Word with ID '{word_id}' not found in global dictionary",
        )
    return word


def convert_word_in_folder_to_response(word_doc: dict, folder_word_doc: dict) -> dict:
    """Merge word data with folder assignment data"""
    return {
        "id": str(folder_word_doc["_id"]),
        "word_id": word_doc["word_id"],
        "word": word_doc["word"],
        "definition": word_doc["definition"],
        "example": word_doc.get("example"),
        "image_url": word_doc.get("image_url"),
        "folder_id": str(folder_word_doc["folder_id"]),
        "user_id": folder_word_doc["user_id"],
        "created_at": folder_word_doc["created_at"],
        "updated_at": folder_word_doc["updated_at"],
    }


@router.post(
    "/users/{user_id}/folders/{folder_id}/words",
    response_model=ApiResponse[WordInFolderResponse],
)
async def add_word_to_folder(
    user_id: str,
    folder_id: str,
    request: AddWordToFolderRequest,
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
    folders_collection: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection),
    user_folder_words_collection: AsyncIOMotorCollection = Depends(
        get_user_folder_words_collection
    ),
):
    """
    Add an existing word to user's folder.

    - **user_id**: User identifier (email)
    - **folder_id**: Folder ObjectId
    - **word_id**: ID of existing word to add
    """
    try:
        # Validate user exists
        user = await get_hardcoded_user(users_collection)

        # Validate folder ownership
        folder_obj_id = validate_object_id(folder_id)
        await validate_user_folder_ownership(
            user["email"], folder_obj_id, folders_collection
        )

        # Validate word exists
        word = await validate_word_exists(request.word_id, words_collection)

        # Check if word is already in this folder
        existing_assignment = await user_folder_words_collection.find_one(
            {
                "user_id": user["email"],
                "folder_id": folder_id,
                "word_id": request.word_id,
            }
        )

        if existing_assignment:
            raise HTTPException(
                status_code=409,
                detail=f"Word '{request.word_id}' is already in this folder",
            )

        # Create folder assignment
        now = datetime.utcnow()
        assignment_doc = {
            "word_id": request.word_id,
            "folder_id": folder_id,
            "user_id": user["email"],
            "created_at": now,
            "updated_at": now,
        }

        # Insert assignment
        result = await user_folder_words_collection.insert_one(assignment_doc)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to add word to folder")

        assignment_doc["_id"] = result.inserted_id

        # Return merged response
        response_data = convert_word_in_folder_to_response(word, assignment_doc)
        return ApiResponse(
            success=True,
            message="Word added to folder successfully",
            data=response_data,
            timestamp=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/users/{user_id}/folders/{folder_id}/words",
    response_model=ApiResponse[List[WordInFolderResponse]],
)
async def list_words_in_folder(
    user_id: str,
    folder_id: str,
    limit: int = Query(100, ge=1, le=1000, description="Number of words to return"),
    skip: int = Query(0, ge=0, description="Number of words to skip"),
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
    folders_collection: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection),
    user_folder_words_collection: AsyncIOMotorCollection = Depends(
        get_user_folder_words_collection
    ),
):
    """
    List all words in user's folder with pagination.
    Returns merged word data with folder assignment info.
    """
    try:
        # Validate user exists
        user = await get_hardcoded_user(users_collection)

        # Validate folder ownership
        folder_obj_id = validate_object_id(folder_id)
        await validate_user_folder_ownership(
            user["email"], folder_obj_id, folders_collection
        )

        # Get word assignments for this folder
        assignments = (
            await user_folder_words_collection.find(
                {"user_id": user["email"], "folder_id": folder_id}
            )
            .sort("created_at", 1)
            .skip(skip)
            .limit(limit)
            .to_list(limit)
        )

        # Get word details for each assignment
        response_data = []
        for assignment in assignments:
            word = await words_collection.find_one({"word_id": assignment["word_id"]})
            if word:  # Word might be deleted from global dictionary
                merged_data = convert_word_in_folder_to_response(word, assignment)
                response_data.append(merged_data)

        return ApiResponse(
            success=True,
            message=f"Retrieved {len(response_data)} words from folder",
            data=response_data,
            timestamp=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/users/{user_id}/folders/{folder_id}/words/{word_id}")
async def remove_word_from_folder(
    user_id: str,
    folder_id: str,
    word_id: str,
    folders_collection: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection),
    user_folder_words_collection: AsyncIOMotorCollection = Depends(
        get_user_folder_words_collection
    ),
):
    """
    Remove word from user's folder.
    Note: This only removes the assignment, not the word from global dictionary.
    """
    try:
        # Validate user exists
        user = await get_hardcoded_user(users_collection)

        # Validate folder ownership
        folder_obj_id = validate_object_id(folder_id)
        await validate_user_folder_ownership(
            user["email"], folder_obj_id, folders_collection
        )

        # Find and delete assignment
        result = await user_folder_words_collection.delete_one(
            {"user_id": user["email"], "folder_id": folder_id, "word_id": word_id}
        )

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404, detail=f"Word '{word_id}' not found in this folder"
            )

        return ApiResponse(
            success=True,
            message="Word removed from folder successfully",
            data=None,
            timestamp=datetime.utcnow(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
