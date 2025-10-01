"""
Folder management router - simplified version using hardcoded user email.
No Firebase token required for testing purposes.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from bson.errors import InvalidId

from dependencies import (
    get_folders_collection,
    get_users_collection,
    ApiResponse,
)
from models.user_folder import (
    CreateFolderRequest,
    UpdateFolderRequest,
    FolderResponse,
)


router = APIRouter(
    prefix="/api/v1/folders",
    tags=["Folders"]
)


# Hardcoded email for testing (same as auth_router.py)
HARDCODED_EMAIL = "dinhthongchau@gmail.com"


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


def validate_object_id(folder_id: str) -> ObjectId:
    """
    Validate and convert folder ID to ObjectId.

    Args:
        folder_id: String representation of ObjectId

    Returns:
        ObjectId: Validated ObjectId

    Raises:
        HTTPException: If ID format is invalid
    """
    try:
        return ObjectId(folder_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Invalid folder ID format",
                "code": "INVALID_OBJECT_ID",
                "error": f"'{folder_id}' is not a valid ObjectId"
            }
        )


def convert_folder_to_response(folder: dict) -> dict:
    """
    Convert MongoDB folder document to response format.
    Converts ObjectId to string and removes _id field.

    Args:
        folder: MongoDB folder document

    Returns:
        dict: Folder data with id as string
    """
    folder["id"] = str(folder["_id"])
    del folder["_id"]
    return folder


@router.get(
    "",
    response_model=ApiResponse[List[FolderResponse]],
    summary="List all user folders",
    description="""
    Get all folders for the authenticated user (hardcoded: dinhthongchau@gmail.com).

    Returns a list of folders sorted by creation date (newest first).
    """
)
async def list_folders(
    folders_col: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[List[FolderResponse]]:
    """
    List all folders for the hardcoded user.

    Args:
        folders_col: Folders collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[List[FolderResponse]]: List of user folders

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Query folders for this user
        cursor = folders_col.find({"user_id": user["email"]})
        folders = await cursor.to_list(length=100)

        # Convert ObjectId to string for each folder
        folders_data = [convert_folder_to_response(folder) for folder in folders]

        # Convert to FolderResponse objects
        folder_responses = [FolderResponse(**folder) for folder in folders_data]

        return ApiResponse[List[FolderResponse]](
            success=True,
            message=f"Retrieved {len(folder_responses)} folder(s)",
            data=folder_responses,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to retrieve folders",
                "code": "FOLDER_RETRIEVAL_ERROR",
                "error": str(e)
            }
        )


@router.post(
    "",
    response_model=ApiResponse[FolderResponse],
    summary="Create new folder",
    description="""
    Create a new folder for the authenticated user.

    Required fields:
    - name: Folder name (1-100 characters)

    Optional fields:
    - description: Folder description (max 500 characters)
    - color: Hex color code (e.g., #FF5733)
    - icon: Emoji or icon
    """
)
async def create_folder(
    request: CreateFolderRequest,
    folders_col: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[FolderResponse]:
    """
    Create a new folder.

    Args:
        request: Folder creation request data
        folders_col: Folders collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[FolderResponse]: Created folder data

    Raises:
        HTTPException: If creation fails
    """
    try:
        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Create folder document
        folder_data = {
            "name": request.name,
            "description": request.description,
            "color": request.color,
            "icon": request.icon,
            "user_id": user["email"],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        # Insert into database
        result = await folders_col.insert_one(folder_data)

        # Retrieve the created folder
        created_folder = await folders_col.find_one({"_id": result.inserted_id})

        # Convert ObjectId to string
        folder_response_data = convert_folder_to_response(created_folder)

        # Convert to FolderResponse
        folder_response = FolderResponse(**folder_response_data)

        return ApiResponse[FolderResponse](
            success=True,
            message="Folder created successfully",
            data=folder_response,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to create folder",
                "code": "FOLDER_CREATION_ERROR",
                "error": str(e)
            }
        )


@router.get(
    "/{folder_id}",
    response_model=ApiResponse[FolderResponse],
    summary="Get single folder",
    description="""
    Get detailed information about a specific folder.

    Validates that the folder belongs to the authenticated user.
    """
)
async def get_folder(
    folder_id: str,
    folders_col: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[FolderResponse]:
    """
    Get a single folder by ID.

    Args:
        folder_id: Folder ID (MongoDB ObjectId as string)
        folders_col: Folders collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[FolderResponse]: Folder data

    Raises:
        HTTPException: 400 if invalid ID, 404 if not found, 500 on other errors
    """
    try:
        # Validate ObjectId format
        obj_id = validate_object_id(folder_id)

        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Query folder with user validation
        folder = await folders_col.find_one({
            "_id": obj_id,
            "user_id": user["email"]
        })

        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Folder not found",
                    "code": "FOLDER_NOT_FOUND",
                    "error": f"No folder found with ID {folder_id}"
                }
            )

        # Convert ObjectId to string
        folder_response_data = convert_folder_to_response(folder)

        # Convert to FolderResponse
        folder_response = FolderResponse(**folder_response_data)

        return ApiResponse[FolderResponse](
            success=True,
            message="Folder retrieved successfully",
            data=folder_response,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to retrieve folder",
                "code": "FOLDER_RETRIEVAL_ERROR",
                "error": str(e)
            }
        )


@router.put(
    "/{folder_id}",
    response_model=ApiResponse[FolderResponse],
    summary="Update folder",
    description="""
    Update an existing folder.

    All fields are optional - only provided fields will be updated.
    The updated_at timestamp is automatically set.
    """
)
async def update_folder(
    folder_id: str,
    request: UpdateFolderRequest,
    folders_col: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[FolderResponse]:
    """
    Update a folder by ID.

    Args:
        folder_id: Folder ID (MongoDB ObjectId as string)
        request: Update request data
        folders_col: Folders collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[FolderResponse]: Updated folder data

    Raises:
        HTTPException: 400 if invalid ID, 404 if not found, 500 on other errors
    """
    try:
        # Validate ObjectId format
        obj_id = validate_object_id(folder_id)

        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Build update dict (only include fields that were provided)
        update_data = {
            k: v for k, v in request.model_dump(exclude_unset=True).items()
        }

        # Always update the updated_at timestamp
        update_data["updated_at"] = datetime.now()

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "No fields to update",
                    "code": "NO_UPDATE_FIELDS",
                    "error": "At least one field must be provided for update"
                }
            )

        # Update folder
        result = await folders_col.update_one(
            {"_id": obj_id, "user_id": user["email"]},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Folder not found",
                    "code": "FOLDER_NOT_FOUND",
                    "error": f"No folder found with ID {folder_id}"
                }
            )

        # Retrieve updated folder
        updated_folder = await folders_col.find_one({"_id": obj_id})

        # Convert ObjectId to string
        folder_response_data = convert_folder_to_response(updated_folder)

        # Convert to FolderResponse
        folder_response = FolderResponse(**folder_response_data)

        return ApiResponse[FolderResponse](
            success=True,
            message="Folder updated successfully",
            data=folder_response,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to update folder",
                "code": "FOLDER_UPDATE_ERROR",
                "error": str(e)
            }
        )


@router.delete(
    "/{folder_id}",
    response_model=ApiResponse[None],
    summary="Delete folder",
    description="""
    Delete an existing folder.

    Validates that the folder belongs to the authenticated user before deletion.
    """
)
async def delete_folder(
    folder_id: str,
    folders_col: AsyncIOMotorCollection = Depends(get_folders_collection),
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[None]:
    """
    Delete a folder by ID.

    Args:
        folder_id: Folder ID (MongoDB ObjectId as string)
        folders_col: Folders collection from MongoDB
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[None]: Success confirmation

    Raises:
        HTTPException: 400 if invalid ID, 404 if not found, 500 on other errors
    """
    try:
        # Validate ObjectId format
        obj_id = validate_object_id(folder_id)

        # Get hardcoded user
        user = await get_hardcoded_user(users_col)

        # Delete folder
        result = await folders_col.delete_one({
            "_id": obj_id,
            "user_id": user["email"]
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": "Folder not found",
                    "code": "FOLDER_NOT_FOUND",
                    "error": f"No folder found with ID {folder_id}"
                }
            )

        return ApiResponse[None](
            success=True,
            message="Folder deleted successfully",
            data=None,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to delete folder",
                "code": "FOLDER_DELETION_ERROR",
                "error": str(e)
            }
        )
