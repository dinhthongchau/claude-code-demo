"""
Word management router - simplified version using hardcoded user email.
No Firebase token required for testing purposes.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId

from dependencies import (
    get_wordlists_collection,
    get_folders_collection,
    get_users_collection,
    ApiResponse,
    HARDCODED_EMAIL,
)
from models.word import (
    CreateWordRequest,
    UpdateWordRequest,
    WordResponse,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["Words"]
)


# ==============================================================================
# Helper Functions
# ==============================================================================

async def get_hardcoded_user(users_col: AsyncIOMotorCollection):
    """
    Get or create the hardcoded test user.

    Args:
        users_col: Users collection from MongoDB

    Returns:
        dict: User document

    Raises:
        HTTPException: If user retrieval/creation fails
    """
    try:
        user = await users_col.find_one({"email": HARDCODED_EMAIL})

        if not user:
            # Create user if doesn't exist
            user_data = {
                "email": HARDCODED_EMAIL,
                "name": "Dinh Thong Chau",
                "created_at": datetime.now()
            }
            result = await users_col.insert_one(user_data)
            user_data["_id"] = result.inserted_id
            user = user_data

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to retrieve user",
                "code": "USER_RETRIEVAL_ERROR",
                "error": str(e)
            }
        )


def validate_object_id(id_str: str, id_type: str = "ID") -> ObjectId:
    """
    Validate and convert ID string to ObjectId.

    Args:
        id_str: String representation of ObjectId
        id_type: Type of ID for error message (e.g., "word", "folder")

    Returns:
        ObjectId: Validated ObjectId

    Raises:
        HTTPException: If ID format is invalid
    """
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": f"Invalid {id_type} ID format",
                "code": "INVALID_OBJECT_ID",
                "error": f"'{id_str}' is not a valid ObjectId"
            }
        )


async def validate_folder_ownership(
    folder_id: ObjectId,
    user_email: str,
    folders_col: AsyncIOMotorCollection
) -> dict:
    """
    Validate that folder exists and belongs to user.

    Args:
        folder_id: Folder ObjectId
        user_email: User's email
        folders_col: Folders collection from MongoDB

    Returns:
        dict: Folder document

    Raises:
        HTTPException: If folder not found or doesn't belong to user
    """
    try:
        folder = await folders_col.find_one({
            "_id": folder_id,
            "user_id": user_email
        })

        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Folder not found or does not belong to user",
                    "code": "FOLDER_NOT_FOUND",
                    "error": f"No folder with ID {folder_id} for user {user_email}"
                }
            )

        return folder
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to validate folder ownership",
                "code": "FOLDER_VALIDATION_ERROR",
                "error": str(e)
            }
        )


def convert_word_to_response(word: dict) -> dict:
    """
    Convert MongoDB word document to response format.
    Converts ObjectId to string and ensures arrays default to empty lists.

    Args:
        word: MongoDB word document

    Returns:
        dict: Word data with id as string
    """
    word["id"] = str(word["_id"])
    del word["_id"]

    # Ensure arrays are lists (not None)
    if word.get("examples") is None:
        word["examples"] = []
    if word.get("image_urls") is None:
        word["image_urls"] = []

    return word


# ==============================================================================
# Endpoints
# ==============================================================================

@router.get(
    "/folders/{folder_id}/words",
    response_model=ApiResponse[List[WordResponse]],
    summary="List words in folder",
    description="""
    Get all words in a specific folder for the authenticated user.

    Returns words sorted alphabetically by word field.

    Pagination:
    - limit: Maximum number of words to return (default: 100, max: 1000)
    - skip: Number of words to skip for pagination (default: 0)
    """
)
async def list_words_in_folder(
    folder_id: str,
    limit: int = 100,
    skip: int = 0,
    words_col: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    folders_col: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[List[WordResponse]]:
    """
    List all words in a folder for the hardcoded user.

    Args:
        folder_id: Folder ID to list words from
        limit: Maximum number of words to return (1-1000)
        skip: Number of words to skip for pagination
        words_col: Words collection from MongoDB
        folders_col: Folders collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[List[WordResponse]]: List of words in folder

    Raises:
        HTTPException: If folder not found or parameters invalid
    """
    try:
        # Validate pagination parameters
        if limit < 1 or limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Invalid limit parameter",
                    "code": "INVALID_LIMIT",
                    "error": "Limit must be between 1 and 1000"
                }
            )

        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Invalid skip parameter",
                    "code": "INVALID_SKIP",
                    "error": "Skip must be >= 0"
                }
            )

        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Validate folder ID format
        folder_obj_id = validate_object_id(folder_id, "folder")

        # Validate folder ownership
        await validate_folder_ownership(folder_obj_id, user["email"], folders_col)

        # Query words - store folder_id as string in MongoDB
        words_cursor = words_col.find({
            "folder_id": folder_id,  # folder_id stored as string
            "user_id": user["email"]
        }).sort("word", 1).skip(skip).limit(limit)

        words = await words_cursor.to_list(length=limit)

        # Convert ObjectId to string for each word
        words_list = [convert_word_to_response(word) for word in words]

        return ApiResponse(
            success=True,
            message=f"Retrieved {len(words_list)} word(s)",
            data=words_list,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to retrieve words",
                "code": "WORDS_RETRIEVAL_ERROR",
                "error": str(e)
            }
        )


@router.post(
    "/words",
    response_model=ApiResponse[WordResponse],
    summary="Create new word",
    description="""
    Create a new word in a specified folder.

    The word will be automatically associated with the authenticated user.
    """
)
async def create_word(
    request: CreateWordRequest,
    words_col: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    folders_col: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[WordResponse]:
    """
    Create a new word for the hardcoded user.

    Args:
        request: Word creation request
        words_col: Words collection from MongoDB
        folders_col: Folders collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[WordResponse]: Created word data

    Raises:
        HTTPException: If folder not found or creation fails
    """
    try:
        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Validate folder ID format
        folder_obj_id = validate_object_id(request.folder_id, "folder")

        # Validate folder ownership
        await validate_folder_ownership(folder_obj_id, user["email"], folders_col)

        # Create word document
        word_data = {
            "word": request.word,
            "definition": request.definition,
            "examples": request.examples if request.examples else [],
            "image_urls": request.image_urls if request.image_urls else [],
            "part_of_speech": request.part_of_speech,
            "pronunciation": request.pronunciation,
            "notes": request.notes,
            "folder_id": request.folder_id,  # Store as string
            "user_id": user["email"],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        # Insert word
        result = await words_col.insert_one(word_data)

        # Retrieve inserted word
        created_word = await words_col.find_one({"_id": result.inserted_id})

        if not created_word:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Failed to retrieve created word",
                    "code": "WORD_CREATION_ERROR",
                    "error": "Word created but could not be retrieved"
                }
            )

        # Convert ObjectId to string
        word_response = convert_word_to_response(created_word)

        return ApiResponse(
            success=True,
            message="Word created successfully",
            data=word_response,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to create word",
                "code": "WORD_CREATION_ERROR",
                "error": str(e)
            }
        )


@router.get(
    "/words/{word_id}",
    response_model=ApiResponse[WordResponse],
    summary="Get word by ID",
    description="Retrieve a single word by its ID."
)
async def get_word(
    word_id: str,
    words_col: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[WordResponse]:
    """
    Get a single word by ID for the hardcoded user.

    Args:
        word_id: Word ID
        words_col: Words collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[WordResponse]: Word data

    Raises:
        HTTPException: If word not found or invalid ID
    """
    try:
        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Validate word ID format
        word_obj_id = validate_object_id(word_id, "word")

        # Query word with user ownership check
        word = await words_col.find_one({
            "_id": word_obj_id,
            "user_id": user["email"]
        })

        if not word:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Word not found",
                    "code": "WORD_NOT_FOUND",
                    "error": f"No word with ID {word_id} for current user"
                }
            )

        # Convert ObjectId to string
        word_response = convert_word_to_response(word)

        return ApiResponse(
            success=True,
            message="Word retrieved successfully",
            data=word_response,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to retrieve word",
                "code": "WORD_RETRIEVAL_ERROR",
                "error": str(e)
            }
        )


@router.put(
    "/words/{word_id}",
    response_model=ApiResponse[WordResponse],
    summary="Update word",
    description="Update an existing word. Only provided fields will be updated."
)
async def update_word(
    word_id: str,
    request: UpdateWordRequest,
    words_col: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[WordResponse]:
    """
    Update a word for the hardcoded user.

    Args:
        word_id: Word ID to update
        request: Word update request
        words_col: Words collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[WordResponse]: Updated word data

    Raises:
        HTTPException: If word not found or update fails
    """
    try:
        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Validate word ID format
        word_obj_id = validate_object_id(word_id, "word")

        # Build update dict (exclude unset fields)
        update_data = {
            k: v for k, v in request.model_dump(exclude_unset=True).items()
        }

        # Check for empty update BEFORE adding timestamp
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "No fields to update",
                    "code": "NO_UPDATE_FIELDS",
                    "error": "At least one field must be provided for update"
                }
            )

        # Add updated_at timestamp
        update_data["updated_at"] = datetime.now()

        # Update word with user ownership check
        result = await words_col.update_one(
            {
                "_id": word_obj_id,
                "user_id": user["email"]
            },
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Word not found",
                    "code": "WORD_NOT_FOUND",
                    "error": f"No word with ID {word_id} for current user"
                }
            )

        # Retrieve updated word
        updated_word = await words_col.find_one({"_id": word_obj_id})

        if not updated_word:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Failed to retrieve updated word",
                    "code": "WORD_UPDATE_ERROR",
                    "error": "Word updated but could not be retrieved"
                }
            )

        # Convert ObjectId to string
        word_response = convert_word_to_response(updated_word)

        return ApiResponse(
            success=True,
            message="Word updated successfully",
            data=word_response,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to update word",
                "code": "WORD_UPDATE_ERROR",
                "error": str(e)
            }
        )


@router.delete(
    "/words/{word_id}",
    response_model=ApiResponse[None],
    summary="Delete word",
    description="Delete a word by its ID."
)
async def delete_word(
    word_id: str,
    words_col: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[None]:
    """
    Delete a word for the hardcoded user.

    Args:
        word_id: Word ID to delete
        words_col: Words collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[None]: Success message

    Raises:
        HTTPException: If word not found or deletion fails
    """
    try:
        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Validate word ID format
        word_obj_id = validate_object_id(word_id, "word")

        # Delete word with user ownership check
        result = await words_col.delete_one({
            "_id": word_obj_id,
            "user_id": user["email"]
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Word not found",
                    "code": "WORD_NOT_FOUND",
                    "error": f"No word with ID {word_id} for current user"
                }
            )

        return ApiResponse(
            success=True,
            message="Word deleted successfully",
            data=None,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to delete word",
                "code": "WORD_DELETION_ERROR",
                "error": str(e)
            }
        )
