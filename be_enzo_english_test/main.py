from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
import pathlib
from dependencies import get_db, FirebaseAuth
import uvicorn

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


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Enzo English Test API",
        "version": "1.0.0-test",
        "docs": "/docs"
    }


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    try:
        db = get_db()
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "firebase": "initialized"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8899, reload=True)
