# Enzo English Test Backend

Simplified FastAPI backend for testing core Enzo English functionality:
- Firebase Authentication
- User Folder Management
- Word List Management

## Prerequisites

- Python 3.9+
- MongoDB Atlas account (or MongoDB instance)
- Firebase project with Authentication enabled

## Setup Instructions

### 1. Clone and Navigate

```bash
cd be_enzo_english_test
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv myenv
.\myenv\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# MongoDB Configuration
MONGO_DB_USER=your_mongo_username
MONGO_DB_PASSWORD=your_mongo_password
MONGO_DB_CLUSTER=your_cluster.mongodb.net
MONGO_DB_NAME=your_database_name

# Firebase Configuration
FIREBASE_PROJECT_ID=your_firebase_project_id

# Authentication
ROOT_BEARER_TOKEN=your_root_bearer_token_here
```

### 5. Add Firebase Service Account

1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Save the JSON file as `assets/firebase-adminsdk.json`

Create the assets directory first:
```bash
mkdir assets
```

### 6. Run the Server

```bash
# Development mode with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8887 --reload

# Or use the main.py entry point
python main.py
```

The server will start at: `http://localhost:8899`

## API Documentation

Once the server is running:

- **Swagger UI**: http://localhost:8899/docs
- **ReDoc**: http://localhost:8899/redoc
- **OpenAPI JSON**: http://localhost:8899/openapi.json

## Testing the API

### Health Check

```bash
curl http://localhost:8899/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "firebase": "initialized"
}
```

### Authentication

All endpoints (except `/api/v1/health`) require Firebase authentication.

1. Sign in via Firebase (in your Flutter app or web console)
2. Get the ID token
3. Use in Authorization header:

```bash
curl -H "Authorization: Bearer <your_firebase_id_token>" \
     http://localhost:8899/api/v1/auth/current-user
```

**Note**: Currently only `dinhthongchau@gmail.com` is allowed access (hardcoded in dependencies.py).

## Project Structure

```
be_enzo_english_test/
├── main.py                 # FastAPI application entry point
├── dependencies.py         # Database & Firebase dependencies
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── models/                # Pydantic models
├── routers/               # API route handlers
│   ├── auth_router.py
│   ├── folders_router.py
│   └── words_router.py
└── tests/                 # Test files
    ├── test_auth.py
    ├── test_folders.py
    └── test_words.py
```

## Available Endpoints

### Authentication
- `POST /api/v1/auth/current-user` - Get current user info

### Folders
- `GET /api/v1/folders` - Get all folders for authenticated user
- `GET /api/v1/folders/{folder_id}` - Get single folder
- `POST /api/v1/folders` - Create new folder
- `PUT /api/v1/folders/{folder_id}` - Update folder
- `DELETE /api/v1/folders/{folder_id}` - Delete folder

### Words
- `GET /api/v1/folders/{folder_id}/words` - Get all words in folder
- `GET /api/v1/words/{word_id}` - Get word details
- `POST /api/v1/words` - Create new word
- `PUT /api/v1/words/{word_id}` - Update word
- `DELETE /api/v1/words/{word_id}` - Delete word

## Development

### Code Quality

```bash
# Install development dependencies
pip install ruff

# Check code
ruff check

# Auto-fix issues
ruff check --fix

# Format code
ruff format
```

### Update Requirements

```bash
pip freeze > requirements.txt
```

## Troubleshooting

### MongoDB Connection Issues

- Verify credentials in `.env`
- Check network access in MongoDB Atlas (whitelist your IP)
- Ensure database user has read/write permissions

### Firebase Authentication Issues

- Verify `firebase-adminsdk.json` is in `assets/` directory
- Check `FIREBASE_PROJECT_ID` matches your Firebase project
- Ensure Firebase Authentication is enabled in console

### Port Already in Use

```bash
# Test server runs on port 8899 (original server on 8887)
# To use a different port:
uvicorn main:app --host 0.0.0.0 --port 8900 --reload
```

## Next Steps

After basic setup works:

1. Implement authentication router (Task 1.2)
2. Implement folders router (Task 1.3)
3. Implement words router (Task 1.4)
4. Add tests for each endpoint

## Support

For issues or questions, refer to the main `plan_initial.md` document.
