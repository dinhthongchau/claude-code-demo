# CLAUDE.md — Project Context for Claude Code

## Overview
- **App type**: Full-stack English learning app (Flutter + FastAPI)
- **Scope**: Simplified test repositories for folder user management and vocabulary with chat AI
- **Key modules**:
  - `/be_enzo_english_test` (FastAPI backend on port 8829)
  - `/flutter_enzo_english_test` (Flutter mobile/web app - to be implemented)
- **Primary workflow**: Feature development via direct commits; small, focused changes preferred

## Environment
- Python 3.9+, Flutter 3.8+, Dart 3.8+
- MongoDB Atlas (shared database)
- Firebase Authentication
- Local setup: Activate venv → Install deps → Configure `.env` → Run server

## Commands

### Backend (`be_enzo_english_test/`)
```bash
# Setup
.\myenv\Scripts\Activate.ps1       # Activate virtual environment
pip install -r requirements.txt    # Install dependencies

# Development
uvicorn main:app --host 0.0.0.0 --port 8829 --reload
python main.py                     # Alternative entry point

# Code quality
ruff check                         # Check issues
ruff check --fix                   # Auto-fix issues
ruff format                        # Format code

# Testing
python tests/test_auth.py          # Test authentication
python tests/test_folders.py       # Test folders (when implemented)
python tests/test_words.py         # Test words (when implemented)
```

### Flutter (`flutter_enzo_english_test/` - planned)
```bash
# Development
flutter run                        # Run on device
flutter run -d chrome              # Run on web

# Code generation
flutter pub run build_runner build --delete-conflicting-outputs

# Quality
flutter analyze                    # Static analysis
flutter test                       # Run tests

# Build
flutter build apk                  # Android APK
flutter build web                  # Web build
```

## Code Style

### Python (Backend)
- **Linting**: ruff for linting and formatting
- **Type hints**: Required for all function signatures
- **Naming**: lowercase_with_underscores for files and variables
- **Comments**: Always in English; never delete old comments without reason
- **Async**: Use async/await for all I/O operations
- **Error handling**: Guard clauses at function start; early returns preferred

### Dart/Flutter (Frontend - planned)
- **Linting**: flutter analyze with default rules
- **Architecture**: Clean Architecture (Domain → Data → Presentation)
- **State management**: BLoC pattern (flutter_bloc)
- **Naming**: camelCase for variables/functions, PascalCase for classes
- **Navigation**: GoRouter only (never Navigator.pop)
- **Widget methods**: Prefer `Widget _buildXxx()` over separate widget classes

## Architecture

### Backend (FastAPI)
- **Dependencies**: Centralized in `dependencies.py`
  - MongoDB connection via `get_db()`
  - Firebase Auth via `FirebaseAuth.initialize()`
- **Routers**:
  - `auth_router.py`: Authentication endpoints
  - `folders_router.py`: Folder CRUD (planned)
  - `words_router.py`: Word CRUD with AI chat (planned)
- **Response format**: JSON with status, message, data fields
- **Authentication**: Firebase ID token in `Authorization: Bearer <token>` header
- **Database**: MongoDB collections: `users`, `folders`, `words`

### Frontend (Flutter - planned)
- **Domain layer**: Entities, repository interfaces, use cases
- **Data layer**: Models (JSON serialization), repository implementations, API sources
- **Presentation layer**: BLoCs (events/states), screens, widgets
- **DI**: GetIt container in `lib/core/get_it/injection_container.dart`
- **HTTP**: Dio client with Firebase Auth interceptor
- **Storage**: SharedPreferences for local data

## Testing
- **Backend**: Manual testing via `tests/` directory scripts; call endpoints directly
- **Frontend**: Unit tests for use cases, widget tests for UI (when implemented)
- **Integration**: Full stack testing: backend running → Flutter app → end-to-end user flows

## Git & CI
- Direct commits to `main` branch for rapid prototyping
- Keep commits atomic and focused on single features
- Commit message format: `feat: description` or `fix: description`
- No CI/CD pipeline currently configured

## Configuration

### Backend `.env` (required)
```env
MONGO_DB_USER=your_username
MONGO_DB_PASSWORD=your_password
MONGO_DB_CLUSTER=your_cluster.mongodb.net
MONGO_DB_NAME=your_database
FIREBASE_PROJECT_ID=your_project_id
ROOT_BEARER_TOKEN=your_token
```

### Backend `assets/` (required)
- `firebase-adminsdk.json`: Firebase service account credentials

### Flutter `lib/dotenv` (planned)
```env
BASE_URL=http://localhost:8829
BASE_URL_WEB=http://localhost:8829
```

### Flutter Firebase config (planned)
- `android/app/google-services.json`
- `lib/firebase_options.dart`

## API Endpoints

### Current (Implemented)
- `GET /api/v1/health`: Health check
- `POST /api/v1/auth/current-user`: Get/create user (no auth required - simplified)

### Planned
- `GET /api/v1/folders`: List user folders
- `POST /api/v1/folders`: Create folder
- `PUT /api/v1/folders/{id}`: Update folder
- `DELETE /api/v1/folders/{id}`: Delete folder
- `GET /api/v1/folders/{id}/words`: List words in folder
- `POST /api/v1/words`: Create word with AI assistance
- `PUT /api/v1/words/{id}`: Update word
- `DELETE /api/v1/words/{id}`: Delete word

## Instructions to Claude

### General Guidelines
- **Small diffs**: Make focused, incremental changes; avoid refactoring unless requested
- **Explain reasoning**: Add comments explaining non-obvious logic
- **Ask first**: If requirements are unclear, ask clarifying questions before implementing
- **Follow patterns**: Use existing code patterns from the repository
- **Test manually**: After changes, provide test commands to verify functionality

### Backend Development
- Always use `async def` for route handlers
- Use FastAPI's `Depends()` for dependency injection
- Return consistent JSON response format with status, message, data
- Handle errors gracefully with try/except and appropriate HTTP status codes
- Add docstrings to all endpoint functions

### Flutter Development (when started)
- Follow clean architecture layers strictly
- Create BLoC for each feature (events → states → bloc)
- Register all dependencies in GetIt container
- Use `Either<Failure, Data>` for repository return types
- Add loading/error/success states to all BLoCs

### AI Chat Feature (key focus)
- Backend: Integrate OpenAI API for vocabulary suggestions and definitions
- Frontend: Chat interface for adding words conversationally
- Flow: User types word → AI provides definition/examples → User confirms → Save to folder
- Keep chat history in memory (not persisted initially)

## Development Roadmap

See `plan_initial.md` for detailed task breakdown:
- **Phase 1**: Backend setup (Tasks 1.1-1.5)
  - ✅ Task 1.1: Repository structure
  - ✅ Task 1.2: Simplified authentication
  - ⏳ Task 1.3: Folder endpoints
  - ⏳ Task 1.4: Word endpoints with AI
  - ⏳ Task 1.5: Documentation
- **Phase 2**: Flutter setup (Tasks 2.1-2.13)
- **Phase 3**: Integration testing (Tasks 3.1-3.5)

## Reference Projects

- **Production backend**: `be_enzo_english/` (port 8887) - full-featured reference implementation
- **Production frontend**: `flutter_enzo_english/` - full app with extensive features
- Both have their own `CLAUDE.md` files for detailed guidance on complex features
