# routers/auth_router.py
"""
Authentication router - simplified version using hardcoded user email.
No Firebase token required for testing purposes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection

from dependencies import (
    get_users_collection,
    ApiResponse,
)


# Pydantic models for request/response
class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: str
    name: str
    created_at: datetime


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.get(
    "/current-user",
    response_model=ApiResponse[UserResponse],
    summary="Get current user (hardcoded for testing it)",
    description="""
    Get information about the test user (dinhthongchau@gmail.com).

    This is a simplified version for testing - no authentication required.
    Returns hardcoded user from MongoDB.
    """
)
async def get_current_user_info(
    users_col: AsyncIOMotorCollection = Depends(get_users_collection)
) -> ApiResponse[UserResponse]:
    """
    Get current user information (hardcoded email: dinhthongchau@gmail.com).

    Args:
        users_col: Users collection from MongoDB

    Returns:
        ApiResponse[UserResponse]: User information

    Raises:
        HTTPException: If user retrieval fails
    """
    try:
        # Hardcoded email for testing
        HARDCODED_EMAIL = "dinhthongchau@gmail.com"

        # Try to find user in database
        user = await users_col.find_one({"email": HARDCODED_EMAIL})

        # If user doesn't exist, create it
        if not user:
            user_data = {
                "email": HARDCODED_EMAIL,
                "name": "Dinh Thong Chau",
                "created_at": datetime.now()
            }
            result = await users_col.insert_one(user_data)
            user_data["_id"] = result.inserted_id
            user = user_data

        # Convert ObjectId to string for JSON serialization
        user_id = str(user.get("_id", ""))

        user_response = UserResponse(
            id=user_id,
            email=user.get("email", ""),
            name=user.get("name", ""),
            created_at=user.get("created_at", datetime.now())
        )

        return ApiResponse[UserResponse](
            success=True,
            message="User retrieved successfully",
            data=user_response,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Failed to retrieve user information",
                "code": "USER_RETRIEVAL_ERROR",
                "error": str(e)
            }
        )
