"""
WordLists router - manages collections of words for users and folders.

Provides CRUD operations for WordLists that contain arrays of word IDs.
WordLists enable better organization and performance compared to individual word assignments.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from bson.errors import InvalidId

from dependencies import (
    get_wordlists_collection,
    get_words_collection,
    get_folders_collection,
    ApiResponse,
    HARDCODED_EMAIL,
)
from models.wordlist import (
    CreateWordListRequest,
    UpdateWordListRequest,
    AddWordsToListRequest,
    RemoveWordsFromListRequest,
    WordListResponse,
    WordListWithWordsResponse,
    WordListStatsResponse,
    generate_wordlist_id,
)

router = APIRouter(prefix="/api/v1", tags=["WordLists"])


# ==============================================================================
# Helper Functions
# ==============================================================================


async def validate_word_exists(word_id: str, words_collection: AsyncIOMotorCollection) -> dict:
    """
    Validate that a word exists in the global dictionary.
    
    Args:
        word_id: Word identifier to validate
        words_collection: Words collection from MongoDB
        
    Returns:
        dict: Word document if found
        
    Raises:
        HTTPException: If word not found
    """
    word = await words_collection.find_one({"word_id": word_id})
    if not word:
        raise HTTPException(
            status_code=404,
            detail=f"Word '{word_id}' not found in global dictionary"
        )
    return word


async def validate_folder_exists(folder_id: str, folders_collection: AsyncIOMotorCollection) -> dict:
    """
    Validate that a folder exists.
    
    Args:
        folder_id: Folder identifier to validate
        folders_collection: Folders collection from MongoDB
        
    Returns:
        dict: Folder document if found
        
    Raises:
        HTTPException: If folder not found
    """
    try:
        from bson import ObjectId
        folder_obj_id = ObjectId(folder_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid folder ID format: {folder_id}"
        )
    
    folder = await folders_collection.find_one({"_id": folder_obj_id})
    if not folder:
        raise HTTPException(
            status_code=404,
            detail=f"Folder '{folder_id}' not found"
        )
    return folder


async def resolve_words_in_wordlist(wordlist: dict, words_collection: AsyncIOMotorCollection) -> dict:
    """
    Resolve word IDs in a WordList to full word objects.
    
    Args:
        wordlist: WordList document from database
        words_collection: Words collection from MongoDB
        
    Returns:
        dict: WordList with resolved words array
    """
    resolved_words = []
    
    for word_id in wordlist.get("words", []):
        word = await words_collection.find_one({"word_id": word_id})
        if word:
            # Convert MongoDB ObjectId to string and remove it
            word.pop("_id", None)
            resolved_words.append(word)
        else:
            # Log missing word but don't fail the entire request
            print(f"Warning: Word '{word_id}' not found in global dictionary")
    
    # Return WordList with resolved words
    return {
        "word_list_id": wordlist["word_list_id"],
        "user_id": wordlist["user_id"],
        "folder_id": wordlist["folder_id"],
        "words": resolved_words,
        "created_at": wordlist["created_at"],
        "updated_at": wordlist["updated_at"],
    }


def convert_wordlist_to_response(wordlist_doc: dict) -> dict:
    """Convert WordList document to response format."""
    return {
        "word_list_id": wordlist_doc["word_list_id"],
        "user_id": wordlist_doc["user_id"],
        "folder_id": wordlist_doc["folder_id"],
        "words": wordlist_doc.get("words", []),
        "created_at": wordlist_doc["created_at"],
        "updated_at": wordlist_doc["updated_at"],
    }


# ==============================================================================
# WordList CRUD Endpoints
# ==============================================================================


@router.post("/wordlists", response_model=ApiResponse[WordListResponse])
async def create_wordlist(
    request: CreateWordListRequest,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
    folders_collection: AsyncIOMotorCollection = Depends(get_folders_collection),
):
    """
    Create a new WordList.
    
    - **user_id**: User identifier (email)
    - **folder_id**: Folder identifier (ObjectId as string)
    - **words**: Optional array of word IDs to include initially
    """
    try:
        # Generate WordList ID
        word_list_id = generate_wordlist_id(request.user_id, request.folder_id)
        
        # Check if WordList already exists
        existing_wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if existing_wordlist:
            raise HTTPException(
                status_code=409,
                detail=f"WordList already exists for user '{request.user_id}' and folder '{request.folder_id}'"
            )
        
        # Validate folder exists
        await validate_folder_exists(request.folder_id, folders_collection)
        
        # Validate all words exist if provided
        validated_words = []
        if request.words:
            for word_id in request.words:
                await validate_word_exists(word_id, words_collection)
                validated_words.append(word_id)
        
        # Create WordList document
        now = datetime.utcnow()
        wordlist_doc = {
            "word_list_id": word_list_id,
            "user_id": request.user_id,
            "folder_id": request.folder_id,
            "words": validated_words,
            "created_at": now,
            "updated_at": now,
        }
        
        # Insert into database
        result = await wordlists_collection.insert_one(wordlist_doc)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create WordList")
        
        # Return response
        response_data = convert_wordlist_to_response(wordlist_doc)
        return ApiResponse(
            success=True,
            message="WordList created successfully",
            data=response_data,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/wordlists/{word_list_id}", response_model=ApiResponse[WordListResponse])
async def get_wordlist(
    word_list_id: str,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
):
    """
    Get a WordList by ID (without resolving words).
    
    Returns the WordList metadata and array of word IDs.
    """
    try:
        wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if not wordlist:
            raise HTTPException(
                status_code=404,
                detail=f"WordList '{word_list_id}' not found"
            )
        
        response_data = convert_wordlist_to_response(wordlist)
        return ApiResponse(
            success=True,
            message="WordList retrieved successfully",
            data=response_data,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/wordlists/{word_list_id}/words", response_model=ApiResponse[WordListWithWordsResponse])
async def get_wordlist_with_words(
    word_list_id: str,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Get a WordList with resolved word details.
    
    Returns the WordList with full word objects instead of just IDs.
    This is the main endpoint for displaying words in Flutter.
    """
    try:
        wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if not wordlist:
            raise HTTPException(
                status_code=404,
                detail=f"WordList '{word_list_id}' not found"
            )
        
        # Resolve words
        resolved_wordlist = await resolve_words_in_wordlist(wordlist, words_collection)
        
        return ApiResponse(
            success=True,
            message=f"WordList retrieved with {len(resolved_wordlist['words'])} words",
            data=resolved_wordlist,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/wordlists/{word_list_id}", response_model=ApiResponse[WordListResponse])
async def update_wordlist(
    word_list_id: str,
    request: UpdateWordListRequest,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    folders_collection: AsyncIOMotorCollection = Depends(get_folders_collection),
):
    """
    Update WordList metadata (user_id, folder_id).
    
    Note: This does not update the words array. Use add/remove endpoints for that.
    """
    try:
        # Check if WordList exists
        existing_wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if not existing_wordlist:
            raise HTTPException(
                status_code=404,
                detail=f"WordList '{word_list_id}' not found"
            )
        
        # Build update data
        update_data = {"updated_at": datetime.utcnow()}
        
        if request.user_id is not None:
            update_data["user_id"] = request.user_id
        
        if request.folder_id is not None:
            # Validate new folder exists
            await validate_folder_exists(request.folder_id, folders_collection)
            update_data["folder_id"] = request.folder_id
        
        # Update WordList
        result = await wordlists_collection.update_one(
            {"word_list_id": word_list_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="WordList not found")
        
        # Get updated WordList
        updated_wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        
        response_data = convert_wordlist_to_response(updated_wordlist)
        return ApiResponse(
            success=True,
            message="WordList updated successfully",
            data=response_data,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/wordlists/{word_list_id}", response_model=ApiResponse[dict])
async def delete_wordlist(
    word_list_id: str,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
):
    """
    Delete a WordList.
    
    This removes the WordList but does not delete the words from the global dictionary.
    """
    try:
        # Check if WordList exists
        existing_wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if not existing_wordlist:
            raise HTTPException(
                status_code=404,
                detail=f"WordList '{word_list_id}' not found"
            )
        
        # Delete WordList
        result = await wordlists_collection.delete_one({"word_list_id": word_list_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete WordList")
        
        return ApiResponse(
            success=True,
            message="WordList deleted successfully",
            data={"word_list_id": word_list_id, "deleted": True},
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ==============================================================================
# Word Management Endpoints
# ==============================================================================


@router.post("/wordlists/{word_list_id}/words", response_model=ApiResponse[WordListResponse])
async def add_words_to_wordlist(
    word_list_id: str,
    request: AddWordsToListRequest,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Add words to a WordList.
    
    - **word_ids**: Array of word IDs to add
    - Validates that all words exist in the global dictionary
    - Prevents duplicate words in the same WordList
    """
    try:
        # Check if WordList exists
        existing_wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if not existing_wordlist:
            raise HTTPException(
                status_code=404,
                detail=f"WordList '{word_list_id}' not found"
            )
        
        # Validate all words exist
        for word_id in request.word_ids:
            await validate_word_exists(word_id, words_collection)
        
        # Get current words in WordList
        current_words = set(existing_wordlist.get("words", []))
        
        # Add new words (avoid duplicates)
        new_words = []
        for word_id in request.word_ids:
            if word_id not in current_words:
                new_words.append(word_id)
                current_words.add(word_id)
        
        # Update WordList
        result = await wordlists_collection.update_one(
            {"word_list_id": word_list_id},
            {
                "$set": {
                    "words": list(current_words),
                    "updated_at": datetime.utcnow(),
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="WordList not found")
        
        # Get updated WordList
        updated_wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        
        response_data = convert_wordlist_to_response(updated_wordlist)
        return ApiResponse(
            success=True,
            message=f"Added {len(new_words)} words to WordList (skipped {len(request.word_ids) - len(new_words)} duplicates)",
            data=response_data,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/wordlists/{word_list_id}/words/{word_id}", response_model=ApiResponse[WordListResponse])
async def remove_word_from_wordlist(
    word_list_id: str,
    word_id: str,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
):
    """
    Remove a single word from a WordList.
    
    - **word_id**: Word ID to remove
    - Does not delete the word from the global dictionary
    """
    try:
        # Check if WordList exists
        existing_wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if not existing_wordlist:
            raise HTTPException(
                status_code=404,
                detail=f"WordList '{word_list_id}' not found"
            )
        
        # Get current words
        current_words = existing_wordlist.get("words", [])
        
        # Remove word if it exists
        if word_id in current_words:
            current_words.remove(word_id)
            
            # Update WordList
            result = await wordlists_collection.update_one(
                {"word_list_id": word_list_id},
                {
                    "$set": {
                        "words": current_words,
                        "updated_at": datetime.utcnow(),
                    }
                }
            )
            
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="WordList not found")
            
            message = f"Word '{word_id}' removed from WordList"
        else:
            message = f"Word '{word_id}' was not in WordList"
        
        # Get updated WordList
        updated_wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        
        response_data = convert_wordlist_to_response(updated_wordlist)
        return ApiResponse(
            success=True,
            message=message,
            data=response_data,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ==============================================================================
# Convenience Endpoints
# ==============================================================================


@router.get("/users/{user_id}/folders/{folder_id}/wordlist", response_model=ApiResponse[WordListWithWordsResponse])
async def get_folder_wordlist_with_words(
    user_id: str,
    folder_id: str,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Get the WordList for a specific user and folder with resolved words.
    
    This is the main endpoint that Flutter will use to display words in a folder.
    Replaces the old `/users/{user_id}/folders/{folder_id}/words` endpoint.
    """
    try:
        # Generate WordList ID
        word_list_id = generate_wordlist_id(user_id, folder_id)
        
        # Find WordList
        wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if not wordlist:
            # Return empty WordList if not found (folder has no words yet)
            return ApiResponse(
                success=True,
                message="No WordList found for this folder",
                data={
                    "word_list_id": word_list_id,
                    "user_id": user_id,
                    "folder_id": folder_id,
                    "words": [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                },
                timestamp=datetime.utcnow(),
            )
        
        # Resolve words
        resolved_wordlist = await resolve_words_in_wordlist(wordlist, words_collection)
        
        return ApiResponse(
            success=True,
            message=f"Retrieved WordList with {len(resolved_wordlist['words'])} words",
            data=resolved_wordlist,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/wordlists/{word_list_id}/stats", response_model=ApiResponse[WordListStatsResponse])
async def get_wordlist_stats(
    word_list_id: str,
    wordlists_collection: AsyncIOMotorCollection = Depends(get_wordlists_collection),
    words_collection: AsyncIOMotorCollection = Depends(get_words_collection),
):
    """
    Get statistics for a WordList.
    
    Returns counts of total words, words with images, words with examples, etc.
    """
    try:
        # Find WordList
        wordlist = await wordlists_collection.find_one({"word_list_id": word_list_id})
        if not wordlist:
            raise HTTPException(
                status_code=404,
                detail=f"WordList '{word_list_id}' not found"
            )
        
        # Count statistics
        word_ids = wordlist.get("words", [])
        total_words = len(word_ids)
        words_with_images = 0
        words_with_examples = 0
        
        # Check each word for images and examples
        for word_id in word_ids:
            word = await words_collection.find_one({"word_id": word_id})
            if word:
                if word.get("image_url"):
                    words_with_images += 1
                if word.get("example"):
                    words_with_examples += 1
        
        stats_data = {
            "word_list_id": word_list_id,
            "total_words": total_words,
            "words_with_images": words_with_images,
            "words_with_examples": words_with_examples,
            "last_updated": wordlist["updated_at"],
        }
        
        return ApiResponse(
            success=True,
            message="WordList statistics retrieved successfully",
            data=stats_data,
            timestamp=datetime.utcnow(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
