from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
import pathlib
import os
import sys
import io
from dependencies import get_db, FirebaseAuth
from routers.auth_router import router as auth_router
from routers.folders_router import router as folders_router
from routers.words_router import router as words_router
from routers.simplified_words_router import router as simplified_words_router
from routers.user_folder_words_router import router as user_folder_words_router
import uvicorn

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Load environment variables
basedir = pathlib.Path(__file__).parent
load_dotenv(basedir / ".env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Enzo English Test API",
    description="""
    Simplified Enzo English API for testing core functionality.

    ## Features
    * Firebase Authentication
    * User Folder Management
    * Word List Management
    * Simplified Word Dictionary (Global)
    * User Folder Word Assignments
    * Image Upload/Serving

    ## Authentication
    All endpoints require Firebase authentication except for health check.
    Use Firebase ID token in Authorization header: `Bearer <token>`
    """,
    version="1.0.0-test",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Disable logging from third-party libraries
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Include routers
app.include_router(auth_router)
app.include_router(folders_router)  # Folder CRUD operations
app.include_router(words_router)  # Word CRUD operations
app.include_router(simplified_words_router)  # Simplified word dictionary management
app.include_router(user_folder_words_router)  # User folder word assignments


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize Firebase and test MongoDB connection on startup."""
    try:
        # Initialize Firebase
        FirebaseAuth.initialize()
        logger.info("Firebase Admin SDK initialized")

        # Test MongoDB connection
        db = get_db()
        await db.command("ping")
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Clean up database connection on shutdown."""
    try:
        from dependencies import DatabaseConnection

        await DatabaseConnection().close()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Shutdown error: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Enzo English Test API",
        "version": "1.0.0-test",
        "docs": "/docs",
    }


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    try:
        db = get_db()
        await db.command("ping")
        return {"status": "healthy", "database": "connected", "firebase": "initialized"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=os.getenv("HOST"), port=int(os.getenv("PORT")), reload=True
    )
