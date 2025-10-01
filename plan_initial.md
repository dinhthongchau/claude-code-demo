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

### Task 1.3: Implement User Folder Endpoints (TDD)
**Based on:** `be_enzo_english` existing folder
**Auth Strategy:** Simplified (no Firebase token required, hardcoded user like Task 1.2)

---

#### Phase A: Design & Plan (BLUE)
- [ ] **Decide authentication approach**:
  - [ ] **Decision**: Use simplified auth (no token) for consistency with Task 1.2
  - [ ] Folders belong to hardcoded user (dinhthongchau@gmail.com)
  - [ ] Document: Will add real Firebase auth in future iteration

- [ ] **Design data models**:
  - [ ] **FolderResponse** (output): `{id: str, name: str, description: str, user_id: str, created_at: datetime, updated_at: datetime, color: str, icon: str}`
  - [ ] **CreateFolderRequest** (input): `{name: str, description: Optional[str], color: Optional[str], icon: Optional[str]}`
  - [ ] **UpdateFolderRequest** (input): `{name: Optional[str], description: Optional[str], color: Optional[str], icon: Optional[str]}`
  - [ ] **MongoDB document**: `{_id: ObjectId, name, description, user_id: str (email), created_at, updated_at, color, icon}`
  - [ ] Note: Must convert `_id` (ObjectId) → `id` (str) in responses

- [ ] **Define API response format**:
  - [ ] Use existing `ApiResponse[T]` from dependencies.py
  - [ ] Success: `{success: true, message: "...", data: {...}, timestamp: datetime}`
  - [ ] Error: `{success: false, message: "...", error_code: int, error_message: str, timestamp: datetime}`

- [ ] **List test scenarios**:
  - [ ] **Happy path**: Create → List → Get → Update → Delete
  - [ ] **Error cases**: 404 not found, 400 missing name, 400 invalid ID format, empty name, very long name
  - [ ] **Data validation**: ObjectId conversion, timestamps auto-set, user_id assignment
  - [ ] **Edge cases**: Duplicate names (allowed), pagination (defer to later)

---

#### Phase B: Write Tests First (RED)
- [ ] **Create test file structure**: `tests/test_folders.py`
  - [ ] Follow test_auth.py pattern (requests library, nice formatting)
  - [ ] Import: requests, json, sys, io (Windows encoding fix)
  - [ ] BASE_URL = "http://localhost:8829"
  - [ ] Helper functions: print_separator(), print_result()

- [ ] **Test Setup (before tests)**:
  - [ ] Add function to get test user_id: Call GET /auth/current-user, extract user.id
  - [ ] Add function to create test folder: Helper for setup
  - [ ] Add function to cleanup test folders: Delete all folders with "TEST_" prefix after tests
  - [ ] Document: Tests use real MongoDB, cleanup is mandatory

- [ ] **Write Test 1: List Folders (Empty State)**:
  - [ ] GET /api/v1/folders
  - [ ] Assert: 200 status, success=true, data=[] (empty list)
  - [ ] Verify ApiResponse format

- [ ] **Write Test 2: Create Folder (Success)**:
  - [ ] POST /api/v1/folders
  - [ ] Body: `{name: "TEST_My Vocabulary", description: "Test folder", color: "#FF5733", icon: "📚"}`
  - [ ] Assert: 200 status, success=true
  - [ ] Assert: data.id exists (string), data.name matches, timestamps exist
  - [ ] Save folder_id for subsequent tests

- [ ] **Write Test 3: Create Folder (Missing Name)**:
  - [ ] POST /api/v1/folders
  - [ ] Body: `{description: "No name"}`
  - [ ] Assert: 400 or 422 status, success=false, error message about missing name

- [ ] **Write Test 4: Create Folder (Empty Name)**:
  - [ ] POST /api/v1/folders
  - [ ] Body: `{name: ""}`
  - [ ] Assert: 400 status, error about empty name

- [ ] **Write Test 5: List Folders (With Data)**:
  - [ ] GET /api/v1/folders
  - [ ] Assert: 200 status, data is list, length > 0
  - [ ] Assert: Each folder has id, name, user_id, created_at

- [ ] **Write Test 6: Get Single Folder (Success)**:
  - [ ] GET /api/v1/folders/{folder_id}
  - [ ] Assert: 200 status, data matches created folder
  - [ ] Assert: All fields present

- [ ] **Write Test 7: Get Single Folder (Not Found)**:
  - [ ] GET /api/v1/folders/000000000000000000000000 (valid ObjectId format but doesn't exist)
  - [ ] Assert: 404 status, success=false

- [ ] **Write Test 8: Get Single Folder (Invalid ID)**:
  - [ ] GET /api/v1/folders/invalid_id
  - [ ] Assert: 400 status, error about invalid ObjectId format

- [ ] **Write Test 9: Update Folder (Success)**:
  - [ ] PUT /api/v1/folders/{folder_id}
  - [ ] Body: `{name: "TEST_Updated Name", color: "#00FF00"}`
  - [ ] Assert: 200 status, data.name updated, updated_at > created_at

- [ ] **Write Test 10: Update Folder (Not Found)**:
  - [ ] PUT /api/v1/folders/000000000000000000000000
  - [ ] Assert: 404 status

- [ ] **Write Test 11: Delete Folder (Success)**:
  - [ ] DELETE /api/v1/folders/{folder_id}
  - [ ] Assert: 200 status, success=true
  - [ ] Verify: GET /api/v1/folders/{folder_id} returns 404

- [ ] **Write Test 12: Delete Folder (Not Found)**:
  - [ ] DELETE /api/v1/folders/000000000000000000000000
  - [ ] Assert: 404 status

- [ ] **Add test cleanup function**:
  - [ ] Delete all folders with "TEST_" prefix
  - [ ] Call in teardown or at end of test suite

- [ ] **Add test summary and CURL examples**:
  - [ ] Follow test_auth.py format
  - [ ] Print all passed/failed tests
  - [ ] Show example CURL commands

- [ ] **Run tests**: Execute `python tests/test_folders.py`
  - [ ] Verify all tests FAIL (endpoints don't exist yet) ✅ RED phase complete
  - [ ] Check error messages are clear (ImportError, ConnectionRefused, 404, etc.)

- [ ] **Review tests**: Ensure comprehensive coverage
  - [ ] All CRUD operations covered
  - [ ] Error cases covered
  - [ ] Response format validated
  - [ ] ObjectId handling considered

- [ ] **Commit tests**: `git commit -m "test: add comprehensive tests for folder endpoints"`

---

#### Phase C: Implement Code (GREEN)
- [ ] **Create Pydantic models**: `models/user_folder.py`
  - [ ] Import: BaseModel, Field, Optional from pydantic
  - [ ] **CreateFolderRequest**:
    - name: str = Field(..., min_length=1, max_length=100)
    - description: Optional[str] = Field(None, max_length=500)
    - color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")  # Hex color
    - icon: Optional[str] = None
  - [ ] **UpdateFolderRequest**:
    - name: Optional[str] = Field(None, min_length=1, max_length=100)
    - description: Optional[str] = Field(None, max_length=500)
    - color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    - icon: Optional[str] = None
  - [ ] **FolderResponse**:
    - id: str
    - name: str
    - description: Optional[str]
    - user_id: str
    - created_at: datetime
    - updated_at: datetime
    - color: Optional[str]
    - icon: Optional[str]
  - [ ] Add Config class with example schemas

- [ ] **Create router**: `routers/folders_router.py`
  - [ ] Import: APIRouter, Depends, HTTPException, status
  - [ ] Import: get_folders_collection, get_users_collection, ApiResponse from dependencies
  - [ ] Import: CreateFolderRequest, UpdateFolderRequest, FolderResponse from models.user_folder
  - [ ] Import: ObjectId from bson
  - [ ] Create router with prefix="/api/v1/folders", tags=["Folders"]

- [ ] **Implement GET /api/v1/folders** - List all folders:
  - [ ] Async function with dependencies: get_folders_collection, get_users_collection
  - [ ] Get hardcoded user: user = await users_col.find_one({"email": "dinhthongchau@gmail.com"})
  - [ ] If user not found: Create user (same as auth_router.py)
  - [ ] Query folders: folders = await folders_col.find({"user_id": user["email"]}).to_list(100)
  - [ ] Convert each folder: `id = str(folder["_id"])`, remove `_id` key
  - [ ] Map to FolderResponse objects
  - [ ] Return ApiResponse[List[FolderResponse]] with success=True
  - [ ] Error handling: HTTPException 500 on failure

- [ ] **Implement POST /api/v1/folders** - Create folder:
  - [ ] Async function with request: CreateFolderRequest
  - [ ] Get hardcoded user (same as above)
  - [ ] Create folder document:
    - name, description, color, icon from request
    - user_id = user["email"]
    - created_at = datetime.now()
    - updated_at = datetime.now()
  - [ ] Insert: result = await folders_col.insert_one(folder_data)
  - [ ] Retrieve inserted folder: await folders_col.find_one({"_id": result.inserted_id})
  - [ ] Convert ObjectId → string
  - [ ] Return ApiResponse[FolderResponse] with success=True
  - [ ] Error handling: 400 for validation errors, 500 for DB errors

- [ ] **Implement GET /api/v1/folders/{folder_id}** - Get single folder:
  - [ ] Async function with path param: folder_id: str
  - [ ] Validate ObjectId format: try ObjectId(folder_id) except InvalidId → 400
  - [ ] Get hardcoded user
  - [ ] Query: folder = await folders_col.find_one({"_id": ObjectId(folder_id), "user_id": user["email"]})
  - [ ] If not found: 404 HTTPException
  - [ ] Convert ObjectId → string
  - [ ] Return ApiResponse[FolderResponse]
  - [ ] Error handling: 400 invalid ID, 404 not found, 500 DB error

- [ ] **Implement PUT /api/v1/folders/{folder_id}** - Update folder:
  - [ ] Async function with folder_id: str, request: UpdateFolderRequest
  - [ ] Validate ObjectId format
  - [ ] Get hardcoded user
  - [ ] Build update dict: {k: v for k, v in request.dict(exclude_unset=True).items()}
  - [ ] Add updated_at = datetime.now()
  - [ ] Update: result = await folders_col.update_one({"_id": ObjectId(folder_id), "user_id": user["email"]}, {"$set": update_data})
  - [ ] If result.matched_count == 0: 404 HTTPException
  - [ ] Retrieve updated folder
  - [ ] Return ApiResponse[FolderResponse]
  - [ ] Error handling: 400 invalid ID, 404 not found, 500 DB error

- [ ] **Implement DELETE /api/v1/folders/{folder_id}** - Delete folder:
  - [ ] Async function with folder_id: str
  - [ ] Validate ObjectId format
  - [ ] Get hardcoded user
  - [ ] Delete: result = await folders_col.delete_one({"_id": ObjectId(folder_id), "user_id": user["email"]})
  - [ ] If result.deleted_count == 0: 404 HTTPException
  - [ ] Return ApiResponse with success=True, message="Folder deleted successfully"
  - [ ] Error handling: 400 invalid ID, 404 not found, 500 DB error

- [ ] **Register router in main.py**:
  - [ ] Import: from routers.folders_router import router as folders_router
  - [ ] Add: app.include_router(folders_router)

- [ ] **Run tests**: Execute `python tests/test_folders.py`
  - [ ] Iterate on failing tests
  - [ ] Fix bugs, adjust response formats
  - [ ] Ensure ObjectId conversion works
  - [ ] Verify timestamps are set correctly
  - [ ] Continue until all tests PASS ✅ GREEN phase complete

- [ ] **Manual verification**:
  - [ ] Start server: `python main.py`
  - [ ] Open Swagger docs: http://localhost:8829/docs
  - [ ] Test each endpoint manually
  - [ ] Verify MongoDB data via Compass/shell
  - [ ] Test edge cases not covered by automated tests

- [ ] **Commit implementation**: `git commit -m "feat: implement folder CRUD endpoints with simplified auth"`

---

#### Phase D: Refactor (REFACTOR)
- [ ] **Extract helper functions**:
  - [ ] Create `get_hardcoded_user()` helper (used in all endpoints)
  - [ ] Create `validate_object_id()` helper (used in GET/PUT/DELETE)
  - [ ] Create `convert_folder_to_response()` helper (ObjectId → string conversion)

- [ ] **Improve error messages**:
  - [ ] Consistent error format across all endpoints
  - [ ] User-friendly error messages
  - [ ] Proper HTTP status codes

- [ ] **Add docstrings**:
  - [ ] Add comprehensive docstrings to all endpoint functions
  - [ ] Document parameters, return types, exceptions
  - [ ] Add usage examples in docstrings

- [ ] **Code cleanup**:
  - [ ] Remove code duplication
  - [ ] Improve variable naming
  - [ ] Add type hints everywhere
  - [ ] Format with `ruff format`

- [ ] **Run tests again**: Ensure refactoring didn't break anything
  - [ ] All tests still pass ✅

- [ ] **Commit refactoring**: `git commit -m "refactor: extract helpers and improve folder endpoints code quality"`


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
