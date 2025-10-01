# Plan: Basic Test Repositories - Folder & Word Management with Firebase Auth

**Scope:** This plan covers only the core functionality - Firebase authentication, folder management, and word management. All AI chat features will be implemented later in a separate plan.

---

## Test Driven Development (TDD) Workflow

All new tasks must follow this TDD process:

### Step 1: RAW TASK (TO DO TASK)
- Receive or identify the task requirements
- Raw file with checkboxes

### Step 2: BASIC PLAN (Plan Mode)
- High-level approach and architecture decisions
- Identify endpoints, models, dependencies

### Step 3: DETAIL PLAN (Plan Mode)
- Break down into specific implementation steps
- Define test cases and expected behavior

### Step 4: ADD TO PLAN (Edit Mode)
- Update plan_initial.md with detailed checkboxes
- Commit the plan updates

### Step 5: WRITE TESTS (Always Fail First)
- Write test file with assertions for expected behavior
- Run tests → verify they FAIL (red)
- Review and iterate test coverage

### Step 6: COMMIT TESTS
- Commit failing tests with message: `test: add tests for [feature]`
- Tests must be in version control before implementation

### Step 7: IMPLEMENT CODE (Make Tests Pass)
- Write minimal code to pass tests (green)
- Run tests → iterate until all pass
- Review code quality

### Step 8: COMMIT CODE
- Commit implementation with message: `feat: implement [feature]`
- Tests and implementation in separate commits

### Benefits:
- ✅ Tests define requirements clearly
- ✅ Code coverage guaranteed
- ✅ Regression prevention
- ✅ Better code design (testable architecture)
- ✅ Clear git history (tests → implementation)

---

## Phase 1: Backend Repository Setup (Basic Features Only)

### Task 1.1: Create New Backend Repository Structure ✅
**Based on:** `be_enzo_english` existing folder

- [x] Clone/create new repository `be_enzo_english_test`
- [x] Set up basic FastAPI project structure with minimal dependencies
- [x] Configure `.env` file with MongoDB connection string (reusing existing database)
- [x] Create `.env.example` file with placeholder values (you will paste private keys later)
- [x] Create `main.py` with basic FastAPI app initialization
- [x] Add CORS middleware for Flutter web/mobile testing
- [x] Copy Firebase credentials to `assets/firebase-adminsdk.json`
- [x] Update server port to 8899 (to avoid conflict with main server on 8887)
- [x] Test: Run `uvicorn main:app --reload` and verify server starts successfully

### Task 1.2: Implement Simple Authentication (Hardcoded User) ✅
**Based on:** Simplified approach - no Firebase token required

- [x] Use hardcoded email `dinhthongchau@gmail.com` in MongoDB
- [x] Create `/api/v1/auth/current-user` endpoint that:
  - [x] No authentication required (simplified for testing)
  - [x] Fetches user from MongoDB using hardcoded email
  - [x] Returns user object: `{id, email, name, created_at}`
  - [x] Creates user in DB if not exists
- [x] Create test file `tests/test_auth.py` with sample requests
- [x] Fix Windows console encoding issues in test file
- [x] Test: Call endpoint and verify user data returned (4/4 tests passed)

### Task 1.2.1: Create Project Documentation ✅
**Documentation and guidance for development**

- [x] Create root `CLAUDE.md` with monorepo overview and architecture
- [x] Update `be_enzo_english_test/README.md` to reflect simplified scope
- [x] Add custom Claude Code commands for project workflow

### Task 1.2.2: Move Hardcoded URLs to Environment Variables ✅
**Refactor configuration to use environment variables**

- [x] Add PORT, HOST, BASE_URL to `.env.example`
- [x] Update `main.py` to read port/host from environment variables
- [x] Remove hardcoded fallback URLs from `test_auth.py`
- [x] Remove hardcoded fallback URLs from `test_folders.py`
- [x] Track `.env.example` in git

### Task 1.3: Implement User Folder Endpoints (TDD) ✅
**Based on:** `be_enzo_english` existing folder
**Auth Strategy:** Simplified (no Firebase token required, hardcoded user like Task 1.2)

---

#### Phase A: Design & Plan (BLUE) ✅
- [x] **Decide authentication approach**:
  - [x] **Decision**: Use simplified auth (no token) for consistency with Task 1.2
  - [x] Folders belong to hardcoded user (dinhthongchau@gmail.com)
  - [x] Document: Will add real Firebase auth in future iteration

- [x] **Design data models**:
  - [x] **FolderResponse** (output): `{id: str, name: str, description: str, user_id: str, created_at: datetime, updated_at: datetime, color: str, icon: str}`
  - [x] **CreateFolderRequest** (input): `{name: str, description: Optional[str], color: Optional[str], icon: Optional[str]}`
  - [x] **UpdateFolderRequest** (input): `{name: Optional[str], description: Optional[str], color: Optional[str], icon: Optional[str]}`
  - [x] **MongoDB document**: `{_id: ObjectId, name, description, user_id: str (email), created_at, updated_at, color, icon}`
  - [x] Note: Must convert `_id` (ObjectId) → `id` (str) in responses

- [x] **Define API response format**:
  - [x] Use existing `ApiResponse[T]` from dependencies.py
  - [x] Success: `{success: true, message: "...", data: {...}, timestamp: datetime}`
  - [x] Error: `{success: false, message: "...", error_code: int, error_message: str, timestamp: datetime}`

- [x] **List test scenarios**:
  - [x] **Happy path**: Create → List → Get → Update → Delete
  - [x] **Error cases**: 404 not found, 400 missing name, 400 invalid ID format, empty name, very long name
  - [x] **Data validation**: ObjectId conversion, timestamps auto-set, user_id assignment
  - [x] **Edge cases**: Duplicate names (allowed), pagination implemented

---

#### Phase B: Write Tests First (RED) ✅
- [x] **Create test file structure**: `tests/test_folders.py`
  - [x] Follow test_auth.py pattern (requests library, nice formatting)
  - [x] Import: requests, json, sys, io (Windows encoding fix)
  - [x] BASE_URL = "http://localhost:8829"
  - [x] Helper functions: print_separator(), print_result()

- [x] **Test Setup (before tests)**:
  - [x] Add function to get test user_id: Call GET /auth/current-user, extract user.id
  - [x] Add function to create test folder: Helper for setup
  - [x] Add function to cleanup test folders: Delete all folders with "TEST_" prefix after tests
  - [x] Document: Tests use real MongoDB, cleanup is mandatory

- [x] **Write Test 1: List Folders (Empty State)**
- [x] **Write Test 2: Create Folder (Success)**
- [x] **Write Test 3: Create Folder (Missing Name)**
- [x] **Write Test 4: Create Folder (Empty Name)**
- [x] **Write Test 5: List Folders (With Data)**
- [x] **Write Test 6: Get Single Folder (Success)**
- [x] **Write Test 7: Get Single Folder (Not Found)**
- [x] **Write Test 8: Get Single Folder (Invalid ID)**
- [x] **Write Test 9: Update Folder (Success)**
- [x] **Write Test 10: Update Folder (Not Found)**
- [x] **Write Test 11: Delete Folder (Success)**
- [x] **Write Test 12: Delete Folder (Not Found)**

- [x] **Add test cleanup function**
- [x] **Add test summary and CURL examples**
- [x] **Run tests**: All 12 tests pass
- [x] **Review tests**: Comprehensive coverage achieved
- [x] **Commit tests**: `git commit -m "test: add comprehensive tests for folder endpoints"`

---

#### Phase C: Implement Code (GREEN) ✅
- [x] **Create Pydantic models**: `models/user_folder.py`
- [x] **Create router**: `routers/folders_router.py`
- [x] **Implement GET /api/v1/folders** - List all folders with pagination
- [x] **Implement POST /api/v1/folders** - Create folder
- [x] **Implement GET /api/v1/folders/{folder_id}** - Get single folder
- [x] **Implement PUT /api/v1/folders/{folder_id}** - Update folder
- [x] **Implement DELETE /api/v1/folders/{folder_id}** - Delete folder
- [x] **Register router in main.py**
- [x] **Run tests**: All 12 tests pass ✅
- [x] **Manual verification**: Tested via Swagger docs
- [x] **Commit implementation**: `git commit -m "feat: implement folder CRUD endpoints with simplified auth"`

---

#### Phase D: Refactor (REFACTOR) ✅
- [x] **Extract helper functions**:
  - [x] Create `get_hardcoded_user()` helper (used in all endpoints)
  - [x] Create `validate_object_id()` helper (used in GET/PUT/DELETE)
  - [x] Create `convert_folder_to_response()` helper (ObjectId → string conversion)

- [x] **Improve error messages**:
  - [x] Consistent error format across all endpoints
  - [x] User-friendly error messages
  - [x] Proper HTTP status codes

- [x] **Add docstrings**:
  - [x] Add comprehensive docstrings to all endpoint functions
  - [x] Document parameters, return types, exceptions
  - [x] Add usage examples in docstrings

- [x] **Code cleanup**:
  - [x] Remove code duplication
  - [x] Improve variable naming
  - [x] Add type hints everywhere
  - [x] Format with `ruff format`

- [x] **Run tests again**: All tests still pass ✅
- [x] **Commit refactoring**: `git commit -m "refactor: extract helpers and improve folder endpoints code quality"`

---

#### Phase E: Code Quality & Bug Fixes ✅
- [x] **Fix critical bug**: Update validation checked after adding timestamp (folders_router.py:381-393)
- [x] **Fix documentation inconsistency**: Port 8899 → 8829 in CLAUDE.md
- [x] **Remove dead code**: Unused Firebase auth functions from dependencies.py (100+ lines)
- [x] **Add shutdown handler**: Database cleanup on server shutdown (main.py)
- [x] **Centralize constants**: Move HARDCODED_EMAIL to dependencies.py
- [x] **Add pagination**: limit/skip parameters with validation (1-1000 range)


### Task 1.4: Implement Word List Endpoints (TDD)
**Based on:** `be_enzo_english` existing folder

#### Phase A: Write Tests First (RED)
- [ ] **Plan**: Define test cases and expected behavior for word CRUD operations
- [ ] **Write failing tests** in `tests/test_words.py`:
  - [ ] Test GET /api/v1/folders/{folder_id}/words - List words in folder (expect empty list initially)
  - [ ] Test POST /api/v1/words - Create word (expect 201 + word object with all fields)
  - [ ] Test GET /api/v1/words/{word_id} - Get word details (expect 200 + full word data)
  - [ ] Test PUT /api/v1/words/{word_id} - Update word (expect 200 + updated word)
  - [ ] Test DELETE /api/v1/words/{word_id} - Delete word (expect 204)
  - [ ] Test error cases: invalid folder_id, invalid word_id, unauthorized access, missing required fields
  - [ ] Test word with examples array and image_urls array
- [ ] **Run tests**: Verify all tests FAIL (endpoints don't exist yet)
- [ ] **Review tests**: Ensure comprehensive coverage including array fields
- [ ] **Commit tests**: `git commit -m "test: add tests for word endpoints"`

#### Phase B: Implement Code (GREEN)
- [ ] **Create models**:
  - [ ] Create `models/word.py` with Pydantic schemas
    - Word schema: `{id, word, definition, examples[], image_urls[], part_of_speech, pronunciation, notes, folder_id, user_id, created_at, updated_at}`
- [ ] **Implement endpoints** in `routers/words.py`:
  - [ ] GET /api/v1/folders/{folder_id}/words - Get all words in a folder
    - Requires Firebase authentication
    - Validates folder belongs to authenticated user
    - Returns list of words
  - [ ] GET /api/v1/words/{word_id} - Get detailed word information
    - Requires Firebase authentication
    - Validates word belongs to authenticated user
    - Returns full word details with all fields
  - [ ] POST /api/v1/words - Create new word
    - Requires Firebase authentication
    - Request body: `{word, folder_id, definition, examples[], image_urls[], part_of_speech, pronunciation, notes}`
    - Validates folder belongs to authenticated user
    - Saves to MongoDB with metadata
    - Returns created word object with ID
  - [ ] PUT /api/v1/words/{word_id} - Update word
    - Requires Firebase authentication
    - Validates word belongs to authenticated user
  - [ ] DELETE /api/v1/words/{word_id} - Delete word
    - Requires Firebase authentication
    - Validates word belongs to authenticated user
- [ ] **Run tests**: Iterate until all tests PASS
- [ ] **Manual test**: Call endpoints via Postman for final verification
- [ ] **Commit implementation**: `git commit -m "feat: implement word CRUD endpoints"`

### Task 1.5: Backend Documentation & Testing (Verification-Driven)

#### Phase A: Create Documentation
- [ ] **Create comprehensive `README.md`** with:
  - [ ] Project overview and purpose
  - [ ] Technology stack
  - [ ] Setup instructions (clone, install dependencies, configure .env)
  - [ ] Firebase setup instructions
  - [ ] MongoDB connection setup
  - [ ] How to run the server
  - [ ] How to run tests
  - [ ] API documentation for all endpoints with example requests/responses
  - [ ] Troubleshooting section
- [ ] **Create `requirements.txt`** with all dependencies:
  - [ ] fastapi
  - [ ] uvicorn
  - [ ] pymongo / motor (async MongoDB)
  - [ ] firebase-admin
  - [ ] pydantic
  - [ ] python-dotenv
  - [ ] python-multipart
  - [ ] pytest (for testing)
  - [ ] httpx (for async testing)
- [ ] **Create `.env.example`** with all required environment variables and descriptions
- [ ] **Create Postman collection** or OpenAPI/Swagger documentation
- [ ] **Commit documentation**: `git commit -m "docs: add comprehensive backend documentation"`

#### Phase B: Verify Documentation Works
- [ ] **Fresh environment test**:
  - [ ] Clone repo in new directory
  - [ ] Follow README setup instructions exactly
  - [ ] Verify server starts without errors
  - [ ] Run all test files and verify they pass
  - [ ] Test all endpoints via Postman/curl
- [ ] **Fix any gaps**: Update documentation based on issues found
- [ ] **Commit fixes**: `git commit -m "docs: fix setup instructions and examples"`

---

## Phase 2: Flutter Mobile Repository Setup (Basic Features Only)

### Task 2.1: Create New Flutter Project
**Based on:** `flutter_enzo_english` existing folder

- [ ] Clone/copy `flutter_enzo_test` or similar name from existing project
- [ ] Set up basic project structure following clean architecture
- [ ] Update `pubspec.yaml` with dependencies:
  - [ ] `dio` - HTTP client
  - [ ] `flutter_bloc` - State management
  - [ ] `get_it` - Dependency injection
  - [ ] `go_router` - Navigation
  - [ ] `equatable` - Value equality
  - [ ] `firebase_core` - Firebase initialization
  - [ ] `firebase_auth` - Firebase authentication
  - [ ] `dartz` - Functional programming (Either type)
  - [ ] `shared_preferences` - Local storage
- [ ] Run `flutter pub get`
- [ ] Test: Run `flutter run` and verify default app launches

### Task 2.2: Setup Firebase Authentication
**Based on:** `flutter_enzo_english` existing folder

- [ ] Add Firebase configuration files:
  - [ ] `android/app/google-services.json`
  - [ ] `ios/Runner/GoogleService-Info.plist`
  - [ ] You will provide these files
- [ ] Initialize Firebase in `main.dart`
- [ ] Create `lib/core/firebase/firebase_config.dart`
- [ ] Create sign-in screen `lib/presentation/screens/auth/sign_in_screen.dart`
  - [ ] Email/password sign-in form
  - [ ] Pre-fill with dinhthongchau@gmail.com for testing
- [ ] Create authentication BLoC `lib/presentation/blocs/auth/auth_bloc.dart`
  - [ ] Events: `SignInEvent, SignOutEvent, CheckAuthStatusEvent`
  - [ ] States: `AuthInitial, AuthLoading, Authenticated, Unauthenticated, AuthError`
- [ ] Implement sign-in with Firebase Auth
- [ ] Store Firebase ID token for API calls
- [ ] Test: Sign in with dinhthongchau@gmail.com and verify authentication works

### Task 2.3: Setup Core Infrastructure
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/core/api/api_config.dart` with base URL configuration
- [ ] Create `lib/core/network/dio_client.dart` for HTTP client
  - [ ] Add interceptor to attach Firebase ID token to all requests
  - [ ] Add error handling interceptor
- [ ] Create `lib/core/get_it/injection_container.dart` for dependency injection
- [ ] Create `lib/core/error/failures.dart` for error handling
- [ ] Create `lib/core/error/exceptions.dart` for exceptions
- [ ] Create `.env` file with `BASE_URL=http://localhost:8887`
- [ ] Register all dependencies in GetIt
- [ ] Test: Initialize GetIt and verify no errors

### Task 2.4: Implement Domain Layer - User Folder
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/domain/entities/user_folder_entity.dart`
  - [ ] Properties: `id, name, description, userId, createdAt, updatedAt, color, icon`
- [ ] Create `lib/domain/repository/user_folder_repository.dart` interface
  - [ ] Methods: `getFolders()`, `getFolder(id)`, `createFolder()`, `updateFolder()`, `deleteFolder()`
- [ ] Create use cases:
  - [ ] `lib/domain/usecases/folder/get_user_folders_usecase.dart`
  - [ ] `lib/domain/usecases/folder/get_folder_usecase.dart`
  - [ ] `lib/domain/usecases/folder/create_folder_usecase.dart`
  - [ ] `lib/domain/usecases/folder/update_folder_usecase.dart`
  - [ ] `lib/domain/usecases/folder/delete_folder_usecase.dart`
- [ ] Test: Code compiles without errors

### Task 2.5: Implement Data Layer - User Folder
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/data/models/user_folder_model.dart`
  - [ ] Extends `UserFolderEntity`
  - [ ] Implement `fromJson()` and `toJson()` methods
- [ ] Create `lib/data/datasources/remote/user_folder_remote_datasource.dart`
  - [ ] Implement API calls: `getFolders()`, `getFolder(id)`, `createFolder()`, `updateFolder()`, `deleteFolder()`
  - [ ] Use Dio client with authentication
- [ ] Create `lib/data/repositories/user_folder_repository_impl.dart`
  - [ ] Implements `UserFolderRepository` interface
  - [ ] Handles errors and returns `Either<Failure, Data>`
- [ ] Register repository and data sources in GetIt
- [ ] Test: Repository methods return correct types

### Task 2.6: Implement Presentation Layer - Folder List Screen
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/presentation/blocs/user_folder/user_folder_bloc.dart`
- [ ] Create events:
  - [ ] `LoadUserFoldersEvent`
  - [ ] `CreateFolderEvent`
  - [ ] `UpdateFolderEvent`
  - [ ] `DeleteFolderEvent`
- [ ] Create states:
  - [ ] `UserFolderInitial`
  - [ ] `UserFolderLoading`
  - [ ] `UserFolderLoaded` (with list of folders)
  - [ ] `UserFolderError`
  - [ ] `FolderCreated`
  - [ ] `FolderUpdated`
  - [ ] `FolderDeleted`
- [ ] Create `lib/presentation/screens/folders/folder_list_screen.dart`
  - [ ] Display list of user folders in ListView/GridView
  - [ ] Show folder name, description, icon, color
  - [ ] Add FloatingActionButton to create new folder
  - [ ] Add swipe actions for edit/delete
  - [ ] Pull-to-refresh functionality
- [ ] Create `lib/presentation/widgets/folder_card.dart` for displaying individual folders
- [ ] Create `lib/presentation/screens/folders/folder_form_screen.dart` for create/edit
  - [ ] Form fields: name, description, color picker, icon selector
  - [ ] Save button triggers create/update event
- [ ] Register BLoC in GetIt
- [ ] Set up navigation routing in `lib/core/routes/app_router.dart`
- [ ] Test: Run app → sign in → see list of folders loaded from backend

### Task 2.7: Implement Domain Layer - Words
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/domain/entities/word_entity.dart`
  - [ ] Properties: `id, word, definition, examples, imageUrls, partOfSpeech, pronunciation, notes, folderId, userId, createdAt, updatedAt`
- [ ] Create `lib/domain/repository/word_repository.dart` interface
  - [ ] Methods: `getWords(folderId)`, `getWord(id)`, `createWord()`, `updateWord()`, `deleteWord()`
- [ ] Create use cases:
  - [ ] `lib/domain/usecases/word/get_folder_words_usecase.dart`
  - [ ] `lib/domain/usecases/word/get_word_usecase.dart`
  - [ ] `lib/domain/usecases/word/create_word_usecase.dart`
  - [ ] `lib/domain/usecases/word/update_word_usecase.dart`
  - [ ] `lib/domain/usecases/word/delete_word_usecase.dart`
- [ ] Test: Code compiles without errors

### Task 2.8: Implement Data Layer - Words
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/data/models/word_model.dart`
  - [ ] Extends `WordEntity`
  - [ ] Implement `fromJson()` and `toJson()` methods
- [ ] Create `lib/data/datasources/remote/word_remote_datasource.dart`
  - [ ] Implement API calls: `getWords(folderId)`, `getWord(id)`, `createWord()`, `updateWord()`, `deleteWord()`
  - [ ] Use Dio client with authentication
- [ ] Create `lib/data/repositories/word_repository_impl.dart`
  - [ ] Implements `WordRepository` interface
  - [ ] Handles errors and returns `Either<Failure, Data>`
- [ ] Register repository and data sources in GetIt
- [ ] Test: Repository methods return correct types

### Task 2.9: Implement Presentation Layer - Word List Screen
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/presentation/blocs/word/word_bloc.dart`
- [ ] Create events:
  - [ ] `LoadWordsEvent(folderId)`
  - [ ] `LoadWordDetailEvent(wordId)`
  - [ ] `CreateWordEvent`
  - [ ] `UpdateWordEvent`
  - [ ] `DeleteWordEvent`
- [ ] Create states:
  - [ ] `WordInitial`
  - [ ] `WordLoading`
  - [ ] `WordsLoaded` (with list of words)
  - [ ] `WordDetailLoaded` (with single word)
  - [ ] `WordError`
  - [ ] `WordCreated`
  - [ ] `WordUpdated`
  - [ ] `WordDeleted`
- [ ] Create `lib/presentation/screens/words/word_list_screen.dart`
  - [ ] Display words when folder is tapped
  - [ ] Show word, definition preview, image thumbnail
  - [ ] Add FloatingActionButton to create new word
  - [ ] Add swipe actions for edit/delete
  - [ ] Pull-to-refresh functionality
  - [ ] Empty state when no words exist
- [ ] Create `lib/presentation/widgets/word_card.dart` for displaying individual words
- [ ] Add navigation from folder list → word list using GoRouter
- [ ] Register BLoC in GetIt
- [ ] Test: Tap folder → see words in that folder

### Task 2.10: Implement Presentation Layer - Word Detail Screen
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/presentation/screens/words/word_detail_screen.dart`
  - [ ] Display full word information:
    - [ ] Word (title)
    - [ ] Part of speech
    - [ ] Pronunciation
    - [ ] Definition
    - [ ] Examples (list)
    - [ ] Images (gallery/carousel)
    - [ ] Notes
  - [ ] Add edit button (FAB or app bar action)
  - [ ] Add delete button with confirmation dialog
- [ ] Add navigation from word list → word detail
- [ ] Test: Tap word → see all word information displayed

### Task 2.11: Implement Presentation Layer - Word Form Screen
**Based on:** `flutter_enzo_english` existing folder

- [ ] Create `lib/presentation/screens/words/word_form_screen.dart`
  - [ ] Form fields:
    - [ ] Word (text input)
    - [ ] Definition (multi-line text input)
    - [ ] Part of speech (dropdown)
    - [ ] Pronunciation (text input)
    - [ ] Examples (list of text inputs with add/remove)
    - [ ] Images (list of URLs with add/remove, or image picker)
    - [ ] Notes (multi-line text input)
  - [ ] Folder selector (if creating new word)
  - [ ] Save button triggers create/update event
  - [ ] Cancel button
- [ ] Handle form validation
- [ ] Show loading indicator during save
- [ ] On success: show success message, navigate back to word list
- [ ] On error: show error message
- [ ] Test: Create/edit word → save → verify it appears in word list → verify it's in MongoDB

### Task 2.12: Polish UI/UX
**Based on:** `flutter_enzo_english` existing folder

- [ ] Add loading indicators for all async operations
- [ ] Add error handling with user-friendly error messages
- [ ] Add pull-to-refresh on folder list and word list
- [ ] Add empty states when no folders/words exist
- [ ] Add confirmation dialogs for delete actions
- [ ] Add success snackbars/toasts for create/update/delete
- [ ] Implement proper navigation flow
- [ ] Add app theme/styling consistent with existing app
- [ ] Test: All user interactions feel smooth and responsive

### Task 2.13: Additional Features (Optional)
- [ ] Add search functionality for words
- [ ] Add filtering/sorting options
- [ ] Add offline support with local database (Hive/SQLite)
- [ ] Add image picker for word images
- [ ] Add audio pronunciation playback

---

## Phase 3: Integration Testing & Documentation

### Task 3.1: End-to-End Testing
- [ ] Start backend server on localhost:8887
- [ ] Run Flutter app on emulator/device
- [ ] Test complete flow:
  - [ ] Open app → sign in with dinhthongchau@gmail.com
  - [ ] See folders list
  - [ ] Create new folder → verify it appears
  - [ ] Tap folder → see words
  - [ ] Create new word → verify it appears
  - [ ] Tap word → see full details
  - [ ] Edit word → verify changes saved
  - [ ] Delete word → verify it's removed
  - [ ] Edit folder → verify changes saved
  - [ ] Delete folder → verify it's removed
  - [ ] Sign out → sign in again → verify data persists
- [ ] Document any bugs found and fix them

### Task 3.2: Backend Documentation
- [ ] Create comprehensive `README.md` for backend repository
- [ ] Include:
  - [ ] Project overview
  - [ ] Technology stack
  - [ ] Setup instructions (prerequisites, installation, configuration)
  - [ ] Environment variables documentation
  - [ ] Firebase setup guide
  - [ ] MongoDB setup guide
  - [ ] API documentation (all endpoints with request/response examples)
  - [ ] Testing instructions
  - [ ] Deployment instructions
- [ ] Create `.env.example` file with all required variables
- [ ] Create API documentation (Swagger/OpenAPI or Postman collection)
- [ ] Test: Give README to someone unfamiliar → they can set up and run backend

### Task 3.3: Mobile Documentation
- [ ] Create comprehensive `README.md` for Flutter repository
- [ ] Include:
  - [ ] Project overview
  - [ ] Technology stack
  - [ ] Setup instructions (prerequisites, installation, configuration)
  - [ ] Firebase setup guide
  - [ ] Environment variables documentation
  - [ ] Architecture overview (clean architecture explanation)
  - [ ] Folder structure explanation
  - [ ] Running the app instructions
  - [ ] Building for production instructions
- [ ] Create `.env.example` file
- [ ] Add screenshots of each screen
- [ ] Test: Give README to someone unfamiliar → they can set up and run app

### Task 3.4: Code Repository Preparation
- [ ] Create `.gitignore` for backend:
  - [ ] Exclude `.env`, `__pycache__`, `.pytest_cache`, etc.
- [ ] Create `.gitignore` for Flutter:
  - [ ] Exclude `.env`, `build/`, `.dart_tool/`, etc.
- [ ] Push backend code to GitHub repository
- [ ] Push Flutter code to GitHub repository
- [ ] Add proper commit messages describing features
- [ ] Create initial release tag (v1.0.0-basic)
- [ ] Test: Clone both repos fresh → follow README → everything works

### Task 3.5: Deployment (Optional)
- [ ] Deploy backend to test server (Railway, DigitalOcean, AWS, etc.)
- [ ] Update Flutter app `.env` with deployed backend URL
- [ ] Build APK for Android testing
- [ ] Test deployed version
- [ ] Share repository links

---

## Deliverables (Basic Version)

- [ ] Backend repository with:
  - [ ] Firebase authentication
  - [ ] Folder CRUD endpoints
  - [ ] Word CRUD endpoints
  - [ ] Complete documentation
  - [ ] Test files

- [ ] Flutter repository with:
  - [ ] Firebase authentication
  - [ ] Folder list, create, edit, delete screens
  - [ ] Word list, detail, create, edit, delete screens
  - [ ] Clean architecture implementation
  - [ ] Complete documentation

- [ ] Both repositories:
  - [ ] Connected to existing MongoDB
  - [ ] Using Firebase authentication
  - [ ] Fully documented
  - [ ] Tested and working
  - [ ] Ready for demo

---

## User Flow Summary (Basic Version)

**Authentication Flow:**
1. [ ] User opens app
2. [ ] User signs in with dinhthongchau@gmail.com and password
3. [ ] Firebase authenticates user
4. [ ] App stores Firebase ID token
5. [ ] User navigates to folder list

**Folder Management Flow:**
1. [ ] User sees list of folders
2. [ ] User taps "+" to create new folder
3. [ ] User fills form (name, description, color, icon)
4. [ ] User saves → folder created in MongoDB
5. [ ] User sees new folder in list
6. [ ] User can edit/delete folders

**Word Management Flow:**
1. [ ] User taps on a folder
2. [ ] User sees list of words in that folder
3. [ ] User taps "+" to create new word
4. [ ] User fills form (word, definition, examples, images, etc.)
5. [ ] User saves → word created in MongoDB
6. [ ] User sees new word in list
7. [ ] User taps word to see full details
8. [ ] User can edit/delete words

---

## Next Phase: AI Chat Features (Future Plan)

This will be covered in a separate plan later:
- OpenAI integration for definitions and examples
- Pixabay integration for image suggestions
- AI chat screen for word creation
- AI-assisted word suggestion endpoint
- Word editing screen with AI suggestions
