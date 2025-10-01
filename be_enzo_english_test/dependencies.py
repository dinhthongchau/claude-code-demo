# dependencies.py
"""
Application dependencies for database connections and Firebase authentication.
Provides FastAPI dependency injection for MongoDB collections and Firebase auth.
"""

import logging
import os
from pathlib import Path
from typing import Optional, Generic, TypeVar
from datetime import datetime
from enum import Enum

import firebase_admin
from dotenv import load_dotenv
from fastapi import Depends
from firebase_admin import credentials
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pydantic import BaseModel


# Generic type for ApiResponse data
T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standardized API response model for all endpoints."""

    success: bool
    message: str
    data: Optional[T] = None
    code: Optional[str] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None
    timestamp: datetime


class UserRole(str, Enum):
    """User role enumeration."""
    SUPER_ADMIN = "super-admin"
    ADMIN = "admin"
    USER = "user"


# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
basedir = Path(__file__).parent
load_dotenv(basedir / ".env")


class DatabaseConfig:
    """Database configuration class."""

    def __init__(self):
        self.user = os.getenv("MONGO_DB_USER")
        self.password = os.getenv("MONGO_DB_PASSWORD")
        self.cluster = os.getenv("MONGO_DB_CLUSTER")
        self.name = os.getenv("MONGO_DB_NAME")

        # Validate required environment variables
        if not all([self.user, self.password, self.cluster, self.name]):
            raise ValueError("Missing required MongoDB environment variables")

    @property
    def url(self) -> str:
        """Generate MongoDB connection URL."""
        return (
            f"mongodb+srv://{self.user}:{self.password}@{self.cluster}/"
            f"?retryWrites=true&w=majority&connectTimeoutMS=30000&socketTimeoutMS=30000"
        )


class DatabaseConnection:
    """Singleton database connection manager."""

    _instance: Optional["DatabaseConnection"] = None
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            config = DatabaseConfig()
            self._client = AsyncIOMotorClient(config.url)
            self._db = self._client[config.name]
            logger.info("Database connection initialized")

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """Get the database instance."""
        if self._db is None:
            raise RuntimeError("Database not initialized")
        return self._db

    async def close(self):
        """Close database connection."""
        if self._client:
            self._client.close()
            logger.info("Database connection closed")


def get_db() -> AsyncIOMotorDatabase:
    """Get database instance for dependency injection."""
    return DatabaseConnection().database


class Collections:
    """MongoDB collection names."""
    USERS = "users"
    FOLDERS = "folders"
    WORDLISTS = "wordlists"


def get_collection(collection_name: str):
    """Factory function to get a specific collection dependency."""
    def _get_collection(db: AsyncIOMotorDatabase = Depends(get_db)) -> AsyncIOMotorCollection:
        return db[collection_name]
    return _get_collection


# Collection-specific dependency getters
def get_users_collection(db: AsyncIOMotorDatabase = Depends(get_db)) -> AsyncIOMotorCollection:
    """Get users collection."""
    return db[Collections.USERS]


def get_folders_collection(db: AsyncIOMotorDatabase = Depends(get_db)) -> AsyncIOMotorCollection:
    """Get folders collection."""
    return db[Collections.FOLDERS]


def get_wordlists_collection(db: AsyncIOMotorDatabase = Depends(get_db)) -> AsyncIOMotorCollection:
    """Get wordlists collection."""
    return db[Collections.WORDLISTS]


class FirebaseAuth:
    """Firebase authentication manager."""

    _initialized = False

    @classmethod
    def initialize(cls):
        """Initialize Firebase Admin SDK."""
        if not cls._initialized:
            try:
                firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
                if not firebase_project_id:
                    raise ValueError("FIREBASE_PROJECT_ID not set in environment variables")

                # Try to load service account from assets directory
                cred_path = basedir / "assets" / "firebase-adminsdk.json"

                if cred_path.exists():
                    cred = credentials.Certificate(str(cred_path))
                    firebase_admin.initialize_app(cred)
                    logger.info("Firebase initialized with service account")
                else:
                    # Use Application Default Credentials or environment
                    firebase_admin.initialize_app()
                    logger.info("Firebase initialized with default credentials")

                cls._initialized = True
            except Exception as e:
                logger.error(f"Firebase initialization failed: {str(e)}")
                raise


# Hardcoded email for simplified testing (no Firebase token required)
HARDCODED_EMAIL = "dinhthongchau@gmail.com"
