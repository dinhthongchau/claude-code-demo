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

#### Phase B: Write Tests First (RED) ✅ ✅
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

#### Phase C: Implement Code (GREEN) ✅ ✅
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
- [x] **Clean up test imports**: Remove unused Dict, Any imports from test files
- [x] **Update Claude settings**: Simplify notification system and add test permissions


### Task 1.4: Implement Word Endpoints (TDD)
**Based on:** `be_enzo_english` existing folder
**Auth Strategy:** Simplified (no Firebase token required, hardcoded user like Tasks 1.2 & 1.3)

---

#### Phase A: Design & Plan (BLUE) ✅
- [x] **Decide authentication approach**:
  - [x] **Decision**: Use simplified auth (no token) for consistency with Tasks 1.2 & 1.3
  - [x] Words belong to hardcoded user (dinhthongchau@gmail.com)
  - [x] Must validate folder ownership before word operations
  - [x] Document: Will add real Firebase auth in future iteration

- [x] **Design data models**:
  - [x] **WordResponse** (output): `{id: str, word: str, definition: str, examples: List[str], image_urls: List[str], part_of_speech: str, pronunciation: str, notes: str, folder_id: str, user_id: str, created_at: datetime, updated_at: datetime}`
  - [x] **CreateWordRequest** (input): `{word: str, folder_id: str, definition: str, examples: Optional[List[str]], image_urls: Optional[List[str]], part_of_speech: Optional[str], pronunciation: Optional[str], notes: Optional[str]}`
  - [x] **UpdateWordRequest** (input): All fields optional except no folder_id change allowed
  - [x] **MongoDB document**: Use existing `wordlists` collection, structure: `{_id: ObjectId, word, definition, examples: [], image_urls: [], part_of_speech, pronunciation, notes, folder_id: str, user_id: str (email), created_at, updated_at}`
  - [x] Note: Must convert `_id` (ObjectId) → `id` (str) in responses

- [x] **Define field validation rules**:
  - [x] **word**: Required, 1-100 chars, string
  - [x] **definition**: Required, 1-2000 chars, string
  - [x] **folder_id**: Required, must be valid ObjectId, must exist, must belong to user
  - [x] **examples**: Optional, List[str], max 20 items, each item max 500 chars, default empty list
  - [x] **image_urls**: Optional, List[str], max 10 items, each item max 500 chars (URL validation optional), default empty list
  - [x] **part_of_speech**: Optional, max 50 chars (noun, verb, adjective, etc. - free text for now)
  - [x] **pronunciation**: Optional, max 200 chars (IPA or phonetic spelling)
  - [x] **notes**: Optional, max 2000 chars
  - [x] **user_id**: Auto-set from hardcoded user (email)
  - [x] **created_at/updated_at**: Auto-set by system

- [x] **Define API response format**:
  - [x] Use existing `ApiResponse[T]` from dependencies.py (consistent with folders)
  - [x] Success: `{success: true, message: "...", data: {...}, timestamp: datetime}`
  - [x] Error: `{success: false, message: "...", code: str, error: str, timestamp: datetime}`
  - [x] All endpoints return 200 status (consistent with Task 1.3 pattern)

- [x] **Design API endpoints**:
  - [x] **GET /api/v1/folders/{folder_id}/words** - List words in folder (nested under folder for clarity)
  - [x] **POST /api/v1/words** - Create word (flat URL, folder_id in body)
  - [x] **GET /api/v1/words/{word_id}** - Get single word
  - [x] **PUT /api/v1/words/{word_id}** - Update word
  - [x] **DELETE /api/v1/words/{word_id}** - Delete word
  - [x] Note: Mixed nested/flat pattern for pragmatism (list is folder-centric, operations are word-centric)

- [x] **Plan helper functions**:
  - [x] **Reuse from folders_router.py**:
    - `get_hardcoded_user(users_col)` → Get/create test user
    - `validate_object_id(id_str)` → Validate ObjectId format, return ObjectId or raise 400
  - [x] **New word-specific helpers**:
    - `validate_folder_ownership(folder_id: ObjectId, user_email: str, folders_col)` → Check folder exists and belongs to user, raise 404 if not
    - `convert_word_to_response(word: dict)` → Convert MongoDB doc to response format (ObjectId → string)

- [x] **Define error handling strategy**:
  - [x] 400 BAD_REQUEST: Invalid ObjectId format, validation failures, empty update
  - [x] 404 NOT_FOUND: Word not found, folder not found, word doesn't belong to user
  - [x] 404 FOLDER_NOT_FOUND: Folder doesn't exist when creating word
  - [x] 500 INTERNAL_SERVER_ERROR: Database errors, unexpected exceptions
  - [x] Consistent error format: `{message: str, code: str, error: str}`

- [x] **Plan pagination and sorting**:
  - [x] Add pagination to GET /api/v1/folders/{folder_id}/words (consistent with folders)
  - [x] Parameters: `limit` (1-1000, default 100), `skip` (≥0, default 0)
  - [x] Sorting: Alphabetically by word (most useful for vocabulary)
  - [x] Use `.sort("word", 1)` in MongoDB query

- [x] **Decide cascade delete behavior**:
  - [x] **Decision**: Do NOT implement cascade delete in this phase
  - [x] When folder deleted, words remain orphaned (acceptable for test version)
  - [x] Document: Add cascade delete or prevent deletion in future iteration
  - [x] Note: Could add background cleanup job or folder deletion validation later

- [x] **Plan database indexes** (for future optimization):
  - [x] Index on `folder_id` (most common query pattern)
  - [x] Index on `user_id` (security queries)
  - [x] Compound index on `(folder_id, user_id)` (best performance)
  - [x] Note: Not implementing in Phase C, documenting for future

- [x] **List test scenarios**:
  - [x] **Happy path**: Create folder → Create word → List words → Get word → Update word → Delete word
  - [x] **Error cases**:
    - Invalid word_id format, invalid folder_id format
    - Word not found, folder not found
    - Create word in non-existent folder, create word in other user's folder
    - Missing required fields (word, definition, folder_id)
    - Empty word name, empty definition
  - [x] **Array validation**: Empty examples[], large examples[] (20 items), very long example strings
  - [x] **Edge cases**: Long word (100 chars), long definition (2000 chars), Unicode characters, special characters
  - [x] **Data validation**: ObjectId conversion, timestamps auto-set, user_id assignment, folder ownership validation

---

#### Phase B: Write Tests First (RED) ✅
- [x] **Create test file structure**: `tests/test_words.py`
  - [x] Follow test_auth.py and test_folders.py patterns
  - [x] Import: requests, json, sys, io (Windows encoding fix)
  - [x] Fix encoding: `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")`
  - [x] Load BASE_URL from tests/.env
  - [x] Helper functions: print_separator(), print_result()

- [x] **Test Setup (before tests)**:
  - [x] Add function to get test user_id: Call GET /auth/current-user, extract user.id
  - [x] Add function to create test folder: POST /folders with TEST_ prefix, return folder_id
  - [x] Add function to cleanup test words: DELETE all words with "TEST_" prefix in word field
  - [x] Add function to cleanup test folders: DELETE all folders with "TEST_" prefix
  - [x] Document: Tests use real MongoDB, cleanup is mandatory

- [x] **Write Test 1: Setup - Create Test Folder**:
  - [x] POST /api/v1/folders
  - [x] Body: `{name: "TEST_Word Folder", description: "Test folder for words"}`
  - [x] Assert: 200 status, save folder_id for subsequent tests
  - [x] Note: Reuses folders endpoint (already tested in Task 1.3)

- [x] **Write Test 2: List Words (Empty State)**:
  - [x] GET /api/v1/folders/{test_folder_id}/words
  - [x] Assert: 200 status, success=true, data=[] (empty list)
  - [x] Verify ApiResponse format

- [x] **Write Test 3: Create Word (Success)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "TEST_apple", folder_id: test_folder_id, definition: "A round fruit", examples: ["I ate an apple", "Apple pie"], image_urls: ["https://example.com/apple.jpg"], part_of_speech: "noun", pronunciation: "/ˈæp.əl/", notes: "Test word"}`
  - [x] Assert: 200 status, success=true
  - [x] Assert: data.id exists (24-char string), data.word matches, all fields present, timestamps exist
  - [x] Save word_id for subsequent tests

- [x] **Write Test 4: Create Word (Missing Required Field - word)**:
  - [x] POST /api/v1/words
  - [x] Body: `{folder_id: test_folder_id, definition: "Missing word"}`
  - [x] Assert: 400 or 422 status, error message about missing "word"

- [x] **Write Test 5: Create Word (Missing Required Field - definition)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "TEST_banana", folder_id: test_folder_id}`
  - [x] Assert: 400 or 422 status, error message about missing "definition"

- [x] **Write Test 6: Create Word (Missing Required Field - folder_id)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "TEST_orange", definition: "A citrus fruit"}`
  - [x] Assert: 400 or 422 status, error message about missing "folder_id"

- [x] **Write Test 7: Create Word (Non-existent Folder)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "TEST_grape", folder_id: "000000000000000000000000", definition: "Small fruit"}`
  - [x] Assert: 404 status, error about folder not found

- [x] **Write Test 8: Create Word (Invalid Folder ID Format)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "TEST_mango", folder_id: "invalid_id", definition: "Tropical fruit"}`
  - [x] Assert: 400 status, error about invalid ObjectId format

- [x] **Write Test 9: Create Word (Empty Word Name)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "", folder_id: test_folder_id, definition: "Empty word name"}`
  - [x] Assert: 400 or 422 status, error about empty word

- [x] **Write Test 10: Create Word (Empty Definition)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "TEST_kiwi", folder_id: test_folder_id, definition: ""}`
  - [x] Assert: 400 or 422 status, error about empty definition

- [x] **Write Test 11: Create Word (Minimal - No Optional Fields)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "TEST_pear", folder_id: test_folder_id, definition: "A sweet fruit"}`
  - [x] Assert: 200 status, success=true
  - [x] Assert: examples=[], image_urls=[], part_of_speech=None, pronunciation=None, notes=None

- [x] **Write Test 12: Create Word (With Empty Arrays)**:
  - [x] POST /api/v1/words
  - [x] Body: `{word: "TEST_peach", folder_id: test_folder_id, definition: "Fuzzy fruit", examples: [], image_urls: []}`
  - [x] Assert: 200 status, arrays are empty

- [x] **Write Test 13: List Words (With Data)**:
  - [x] GET /api/v1/folders/{test_folder_id}/words
  - [x] Assert: 200 status, data is list, length >= 1
  - [x] Assert: Each word has required fields (id, word, definition, folder_id, user_id, created_at)
  - [x] Assert: Words sorted alphabetically by word field

- [x] **Write Test 14: List Words (Pagination - First Page)**:
  - [x] GET /api/v1/folders/{test_folder_id}/words?limit=2&skip=0
  - [x] Assert: 200 status, data length <= 2

- [x] **Write Test 15: List Words (Pagination - Invalid Limit)**:
  - [x] GET /api/v1/folders/{test_folder_id}/words?limit=2000
  - [x] Assert: 400 status, error about limit range (1-1000)

- [x] **Write Test 16: List Words (Pagination - Negative Skip)**:
  - [x] GET /api/v1/folders/{test_folder_id}/words?skip=-5
  - [x] Assert: 400 status, error about skip must be >= 0

- [x] **Write Test 17: Get Single Word (Success)**:
  - [x] GET /api/v1/words/{word_id}
  - [x] Assert: 200 status, data matches created word
  - [x] Assert: All fields present (including arrays, optional fields)

- [x] **Write Test 18: Get Single Word (Not Found)**:
  - [x] GET /api/v1/words/000000000000000000000000
  - [x] Assert: 404 status, error about word not found

- [x] **Write Test 19: Get Single Word (Invalid ID Format)**:
  - [x] GET /api/v1/words/invalid_word_id
  - [x] Assert: 400 status, error about invalid ObjectId

- [x] **Write Test 20: Update Word (Success - Partial Update)**:
  - [x] PUT /api/v1/words/{word_id}
  - [x] Body: `{definition: "Updated definition", notes: "Updated notes"}`
  - [x] Assert: 200 status, definition updated, notes updated
  - [x] Assert: word unchanged, updated_at > created_at

- [x] **Write Test 21: Update Word (Success - Update Arrays)**:
  - [x] PUT /api/v1/words/{word_id}
  - [x] Body: `{examples: ["New example 1", "New example 2"], image_urls: ["https://new.com/img.jpg"]}`
  - [x] Assert: 200 status, arrays replaced with new values

- [x] **Write Test 22: Update Word (Empty Update)**:
  - [x] PUT /api/v1/words/{word_id}
  - [x] Body: `{}`
  - [x] Assert: 400 status, error about no fields to update

- [x] **Write Test 23: Update Word (Not Found)**:
  - [x] PUT /api/v1/words/000000000000000000000000
  - [x] Assert: 404 status

- [x] **Write Test 24: Delete Word (Success)**:
  - [x] DELETE /api/v1/words/{word_id}
  - [x] Assert: 200 status, success=true
  - [x] Verify: GET /api/v1/words/{word_id} returns 404

- [x] **Write Test 25: Delete Word (Not Found)**:
  - [x] DELETE /api/v1/words/000000000000000000000000
  - [x] Assert: 404 status

- [x] **Add test cleanup function**:
  - [x] Delete all words with "TEST_" prefix in word field
  - [x] Delete all folders with "TEST_" prefix
  - [x] Call in teardown or at end of test suite

- [x] **Add test summary and CURL examples**:
  - [x] Follow test_auth.py and test_folders.py format
  - [x] Print all passed/failed tests
  - [x] Show example CURL commands for each endpoint
  - [x] Include examples with arrays in request body

- [x] **Run tests**: Execute `python tests/test_words.py`
  - [x] Verify all tests FAIL (endpoints don't exist yet) ✅ RED phase complete
  - [x] Check error messages are clear (ImportError, ConnectionRefused, 404, etc.)

- [x] **Review tests**: Ensure comprehensive coverage
  - [x] All CRUD operations covered
  - [x] All error cases covered
  - [x] Array validation covered
  - [x] Pagination covered
  - [x] Folder ownership validation covered

- [x] **Commit tests**: `git commit -m "test: add comprehensive tests for word endpoints"`

---

#### Phase C: Implement Code (GREEN) ✅
- [x] **Create Pydantic models**: `models/word.py`
  - [x] Import: BaseModel, Field, Optional, List from pydantic
  - [x] **CreateWordRequest**:
    - word: str = Field(..., min_length=1, max_length=100)
    - folder_id: str = Field(..., description="Folder ObjectId as string")
    - definition: str = Field(..., min_length=1, max_length=2000)
    - examples: Optional[List[str]] = Field(default_factory=list, max_length=20)
    - image_urls: Optional[List[str]] = Field(default_factory=list, max_length=10)
    - part_of_speech: Optional[str] = Field(None, max_length=50)
    - pronunciation: Optional[str] = Field(None, max_length=200)
    - notes: Optional[str] = Field(None, max_length=2000)
  - [x] **UpdateWordRequest**:
    - word: Optional[str] = Field(None, min_length=1, max_length=100)
    - definition: Optional[str] = Field(None, min_length=1, max_length=2000)
    - examples: Optional[List[str]] = Field(None, max_length=20)
    - image_urls: Optional[List[str]] = Field(None, max_length=10)
    - part_of_speech: Optional[str] = Field(None, max_length=50)
    - pronunciation: Optional[str] = Field(None, max_length=200)
    - notes: Optional[str] = Field(None, max_length=2000)
    - Note: Do NOT allow folder_id update (words can't move between folders in this version)
  - [x] **WordResponse**:
    - id: str
    - word: str
    - definition: str
    - examples: List[str]
    - image_urls: List[str]
    - part_of_speech: Optional[str]
    - pronunciation: Optional[str]
    - notes: Optional[str]
    - folder_id: str
    - user_id: str
    - created_at: datetime
    - updated_at: datetime
  - [x] Add Config class with example schemas

- [x] **Create router**: `routers/words_router.py`
  - [x] Import: APIRouter, Depends, HTTPException, status, List
  - [x] Import: get_wordlists_collection, get_folders_collection, get_users_collection, ApiResponse, HARDCODED_EMAIL from dependencies
  - [x] Import: CreateWordRequest, UpdateWordRequest, WordResponse from models.word
  - [x] Import: ObjectId from bson, InvalidId from bson.errors
  - [x] Import: datetime
  - [x] Create router with prefix="/api/v1", tags=["Words"]

- [x] **Create helper functions in words_router.py**:
  - [x] **get_hardcoded_user()**: Copy from folders_router.py (or extract to shared utils)
  - [x] **validate_object_id(id_str: str) -> ObjectId**: Copy from folders_router.py
  - [x] **validate_folder_ownership(folder_id: ObjectId, user_email: str, folders_col) -> dict**:
    - Query: folder = await folders_col.find_one({"_id": folder_id, "user_id": user_email})
    - If not found: raise HTTPException 404 FOLDER_NOT_FOUND
    - Return: folder document
  - [x] **convert_word_to_response(word: dict) -> dict**:
    - Convert: word["id"] = str(word["_id"]), del word["_id"]
    - Ensure arrays default to empty lists if missing
    - Return: word dict

- [x] **Implement GET /api/v1/folders/{folder_id}/words** - List words in folder:
  - [x] Async function with path param folder_id: str
  - [x] Query params: limit: int = 100, skip: int = 0
  - [x] Dependencies: get_wordlists_collection, get_folders_collection, get_users_collection
  - [x] Validate pagination parameters (limit 1-1000, skip >= 0)
  - [x] Get hardcoded user
  - [x] Validate folder_id format (ObjectId)
  - [x] Validate folder ownership (folder exists and belongs to user)
  - [x] Query words: words = await words_col.find({"folder_id": folder_id_str, "user_id": user["email"]}).sort("word", 1).skip(skip).limit(limit).to_list(limit)
  - [x] Note: Store folder_id as string in MongoDB (not ObjectId) for simplicity
  - [x] Convert ObjectId → string for each word
  - [x] Map to WordResponse objects
  - [x] Return ApiResponse[List[WordResponse]] with success=True
  - [x] Error handling: 400 invalid IDs/pagination, 404 folder not found, 500 DB errors

- [x] **Implement POST /api/v1/words** - Create word:
  - [x] Async function with request: CreateWordRequest
  - [x] Dependencies: get_wordlists_collection, get_folders_collection, get_users_collection
  - [x] Get hardcoded user
  - [x] Validate folder_id format (ObjectId)
  - [x] Validate folder ownership (folder exists and belongs to user)
  - [x] Create word document:
    - word, definition, examples (default []), image_urls (default []), part_of_speech, pronunciation, notes from request
    - folder_id = request.folder_id (store as string)
    - user_id = user["email"]
    - created_at = datetime.now()
    - updated_at = datetime.now()
  - [x] Insert: result = await words_col.insert_one(word_data)
  - [x] Retrieve inserted word: await words_col.find_one({"_id": result.inserted_id})
  - [x] Convert ObjectId → string
  - [x] Return ApiResponse[WordResponse] with success=True
  - [x] Error handling: 400 validation errors, 404 folder not found, 500 DB errors

- [x] **Implement GET /api/v1/words/{word_id}** - Get single word:
  - [x] Async function with path param: word_id: str
  - [x] Dependencies: get_wordlists_collection, get_users_collection
  - [x] Get hardcoded user
  - [x] Validate word_id format (ObjectId)
  - [x] Query: word = await words_col.find_one({"_id": ObjectId(word_id), "user_id": user["email"]})
  - [x] If not found: 404 HTTPException
  - [x] Convert ObjectId → string
  - [x] Return ApiResponse[WordResponse]
  - [x] Error handling: 400 invalid ID, 404 not found, 500 DB error

- [x] **Implement PUT /api/v1/words/{word_id}** - Update word:
  - [x] Async function with word_id: str, request: UpdateWordRequest
  - [x] Dependencies: get_wordlists_collection, get_users_collection
  - [x] Get hardcoded user
  - [x] Validate word_id format (ObjectId)
  - [x] Build update dict: {k: v for k, v in request.model_dump(exclude_unset=True).items()}
  - [x] Check for empty update BEFORE adding timestamp (avoid bug from Task 1.3)
  - [x] If empty: raise HTTPException 400 NO_UPDATE_FIELDS
  - [x] Add updated_at = datetime.now()
  - [x] Update: result = await words_col.update_one({"_id": ObjectId(word_id), "user_id": user["email"]}, {"$set": update_data})
  - [x] If result.matched_count == 0: 404 HTTPException
  - [x] Retrieve updated word
  - [x] Return ApiResponse[WordResponse]
  - [x] Error handling: 400 invalid ID/empty update, 404 not found, 500 DB error

- [x] **Implement DELETE /api/v1/words/{word_id}** - Delete word:
  - [x] Async function with word_id: str
  - [x] Dependencies: get_wordlists_collection, get_users_collection
  - [x] Get hardcoded user
  - [x] Validate word_id format (ObjectId)
  - [x] Delete: result = await words_col.delete_one({"_id": ObjectId(word_id), "user_id": user["email"]})
  - [x] If result.deleted_count == 0: 404 HTTPException
  - [x] Return ApiResponse with success=True, message="Word deleted successfully"
  - [x] Error handling: 400 invalid ID, 404 not found, 500 DB error

- [x] **Register router in main.py**:
  - [x] Import: from routers.words_router import router as words_router
  - [x] Add: app.include_router(words_router)

- [x] **Run tests**: Execute `python tests/test_words.py`
  - [x] Iterate on failing tests
  - [x] Fix bugs, adjust response formats
  - [x] Ensure ObjectId conversion works
  - [x] Verify timestamps are set correctly
  - [x] Verify folder ownership validation works
  - [x] Verify array handling works (empty lists, populated lists)
  - [x] Verify pagination works
  - [x] Continue until all tests PASS ✅ GREEN phase complete

- [x] **Manual verification**:
  - [x] Start server: `python main.py`
  - [x] Open Swagger docs: http://localhost:8829/docs
  - [x] Test each endpoint manually:
    - Create test folder
    - Create word with all fields
    - Create word with minimal fields
    - List words (verify sorting)
    - Get single word
    - Update word
    - Delete word
  - [x] Verify MongoDB data via Compass/shell:
    - Check wordlists collection
    - Verify folder_id stored as string
    - Verify arrays stored correctly
    - Verify timestamps
  - [x] Test edge cases not covered by automated tests:
    - Very long strings (approaching limits)
    - Unicode characters (emoji, Chinese, Arabic)
    - Special characters in pronunciation (IPA symbols)
    - Large arrays (20 examples, 10 image_urls)

- [x] **Commit implementation**: `git commit -m "feat: implement word CRUD endpoints with simplified auth"`

---

#### Phase D: Refactor (REFACTOR)
- [x] **Extract shared helper functions**:
  - [x] Option A: Create `utils/helpers.py` with get_hardcoded_user(), validate_object_id()
  - [x] Option B: Keep duplicated in both routers (acceptable for small project)
  - [x] Decision: Keep duplicated for now (simpler, no circular imports)
  - [x] Document: Consider extracting to shared utils in future refactor

- [x] **Create word-specific helper module** (optional):
  - [x] If logic becomes complex, extract to `utils/word_helpers.py`
  - [x] Functions: validate_folder_ownership, convert_word_to_response
  - [x] For now: Keep in words_router.py (simpler)

- [x] **Improve error messages**:
  - [x] Consistent error format across all endpoints
  - [x] User-friendly error messages (avoid technical jargon)
  - [x] Proper HTTP status codes (400 vs 404 vs 500)
  - [x] Specific error codes: INVALID_OBJECT_ID, WORD_NOT_FOUND, FOLDER_NOT_FOUND, NO_UPDATE_FIELDS, etc.

- [x] **Add comprehensive docstrings**:
  - [x] Add docstrings to all endpoint functions
  - [x] Document parameters, return types, exceptions
  - [x] Add usage examples in docstrings
  - [x] Document helper functions

- [x] **Code cleanup**:
  - [x] Remove code duplication where reasonable
  - [x] Improve variable naming (e.g., words_col vs wordlists_col for clarity)
  - [x] Add type hints everywhere (params, return types, variables)
  - [x] Format with `ruff format`
  - [ ] Run `ruff check --fix` for any linting issues

- [x] **Review array handling**:
  - [x] Ensure empty arrays default correctly
  - [x] Verify None vs [] handling in optional fields
  - [x] Check array validation (max length enforced)
  - [x] Test updating arrays (replace vs append - currently replace)

- [x] **Run tests again**: Ensure refactoring didn't break anything
  - [x] Execute: `python tests/test_words.py`
  - [x] All tests still pass ✅
  - [x] No regressions introduced

- [x] **Commit refactoring**: `git commit -m "refactor: extract helpers and improve word endpoints code quality"`

---

#### Phase E: Code Quality & Bug Fixes ✅
- [x] **Validation review**: Check all endpoints work correctly
- [x] **Critical bug fixes review**: Fix ApiResponse timestamp field issue
- [x] **Performance considerations documentation**: Document any performance notes
- [x] **Security review**: Ensure proper validation and error handling
- [x] **Edge case handling testing**: Test edge cases
- [x] **Final test run**: Run all tests to ensure everything works
  - [x] Clear error messages

#### Phase F: Testing Utilities ✅
- [x] **Create sample word insertion scripts**:
  - [x] Create `tests/add_sample_words.py` - Interactive script to add words to selected folder
  - [x] Create `tests/add_sample_words_auto.py` - Automatic script to populate all folders with sample words
  - [x] Both scripts include diverse vocabulary with definitions, examples, pronunciation
  - [x] Auto script filters out TEST_ folders and cycles through different word sets

- [x] **Performance considerations** (document for future):
  - [x] Note: Add database indexes in production
  - [x] Index on folder_id for fast word listing
  - [x] Index on user_id for security
  - [x] Compound index (folder_id, user_id) for best performance
  - [x] Note: Not implementing now (test environment, small data)

- [x] **Security review**:
  - [x] Verify user_id always set from authenticated user (hardcoded)
  - [x] Verify folder ownership checked before word creation
  - [x] Verify word ownership checked before get/update/delete
  - [x] Verify no way to access other users' words
  - [x] Verify no SQL injection vectors (using MongoDB, low risk)

- [x] **Edge case handling**:
  - [x] Test with maximum field lengths
  - [x] Test with Unicode characters
  - [x] Test with empty arrays vs None
  - [x] Test concurrent updates (acceptable data loss for test version)

- [x] **Documentation review**:
  - [x] Verify all endpoints documented in docstrings
  - [x] Verify Swagger UI shows correct examples
  - [x] Verify error responses documented
  - [x] Update main README if needed (API endpoints section)

- [x] **Final test run**:
  - [x] Execute all test files: test_auth.py, test_folders.py, test_words.py
  - [x] All tests pass ✅
  - [x] No warnings or errors
  - [x] Test summary shows 100% pass rate

- [x] **Commit quality improvements**: `git commit -m "fix: resolve bugs and improve word endpoints quality"`

---

#### Phase G: Documentation ✅
- [x] **Update CLAUDE.md** (if needed):
  - [x] Add word endpoints to API section
  - [x] Update task 1.4 status to completed
  - [x] Document any architectural decisions

- [x] **Update README.md** (if exists):
  - [x] Add word endpoints to API documentation (already present)
  - [x] Add example requests/responses (available via Swagger)
  - [x] Update feature list (already complete)

- [x] **Create API documentation** (optional):
  - [x] Swagger UI already auto-generated ✅
  - [x] Consider exporting OpenAPI spec for reference (available at /openapi.json)
  - [x] Consider creating Postman collection (optional - Swagger sufficient)

- [x] **Commit documentation**: `git commit -m "docs: update CLAUDE.md with completed word endpoints"`

## Phase 2: Flutter Mobile Repository Setup (Basic Features Only)

### Task 2.1: Migrate Flutter App to Clean Architecture + BLoC (Android Only) ✅
**Goal:** Refactor existing Flutter app from basic FutureBuilder to Clean Architecture with BLoC pattern

#### Phase 1: Project Setup & Dependencies ✅
- [x] Create new Flutter project `flutter_enzo_english_test` (already exists)
- [x] Update `pubspec.yaml` with Clean Architecture dependencies:
  - [x] State Management: `flutter_bloc: ^8.1.6`, `equatable: ^2.0.7`
  - [x] Networking: `dio: ^5.7.0`, `dartz: ^0.10.1`
  - [x] Dependency Injection: `get_it: ^8.0.3`
  - [x] Navigation: `go_router: ^14.6.2`
  - [x] Environment: `flutter_dotenv: ^5.1.0`
  - [x] Testing: `mocktail: ^1.0.4`, `bloc_test: ^9.1.7`
  - [x] Remove: `cupertino_icons` (Android only, use Material icons)
- [x] Run `flutter pub get`

#### Phase 2: Core Infrastructure ✅
- [x] Create core layer folder structure
- [x] Create `lib/core/api/api_config.dart` - API configuration (BASE_URL from .env)
- [x] Create `lib/core/network/dio_client.dart` - Dio client with logging and error interceptors
- [x] Create `lib/core/get_it/injection_container.dart` - GetIt dependency injection container
- [x] Create `lib/core/theme/app_theme.dart` - Material Design 3 theme
- [x] Create `lib/core/constants/constants.dart` - App constants (pagination, messages)
- [x] Create `lib/core/errors/failures.dart` - Failure classes (ServerFailure, NetworkFailure, etc.)
- [x] Create `lib/core/errors/exceptions.dart` - Exception classes

#### Phase 3: Domain Layer - Folders ✅
- [x] Create `lib/domain/entity/folder_entity.dart` - Immutable entity with Equatable
- [x] Create `lib/domain/repository/folder_repository.dart` - Repository interface
- [x] Create `lib/domain/use_case/get_folders_use_case.dart` - Use case with pagination

#### Phase 4: Domain Layer - Words ✅
- [x] Create `lib/domain/entity/word_entity.dart` - Immutable entity with Equatable
- [x] Create `lib/domain/repository/word_repository.dart` - Repository interface
- [x] Create `lib/domain/use_case/get_words_by_folder_use_case.dart` - Use case with folder filtering

#### Phase 5: Data Layer - Folders ✅
- [x] Update `lib/data/models/folder_model.dart` - Extend FolderEntity with JSON serialization
- [x] Create `lib/data/source/remote/folder_remote_source.dart` - Remote data source using DioClient
- [x] Create `lib/data/repository/folder_repository_impl.dart` - Repository implementation with Either error handling

#### Phase 6: Data Layer - Words ✅
- [x] Update `lib/data/models/word_model.dart` - Extend WordEntity with JSON serialization
- [x] Create `lib/data/source/remote/word_remote_source.dart` - Remote data source using DioClient
- [x] Create `lib/data/repository/word_repository_impl.dart` - Repository implementation with Either error handling

#### Phase 7: Presentation Layer - Folders BLoC ✅
- [x] Create `lib/presentation/blocs/folders/folders_event.dart` - Events (LoadFoldersEvent, RefreshFoldersEvent)
- [x] Create `lib/presentation/blocs/folders/folders_state.dart` - States (Initial, Loading.fromState(), Success, Error)
- [x] Create `lib/presentation/blocs/folders/folders_bloc.dart` - BLoC handling state transitions

#### Phase 8: Presentation Layer - Words BLoC ✅
- [x] Create `lib/presentation/blocs/words/words_event.dart` - Events (LoadWordsByFolderEvent, RefreshWordsEvent)
- [x] Create `lib/presentation/blocs/words/words_state.dart` - States (Initial, Loading.fromState(), Success, Error)
- [x] Create `lib/presentation/blocs/words/words_bloc.dart` - BLoC handling state transitions

#### Phase 9: Dependency Injection Setup ✅
- [x] Setup GetIt Container (`lib/core/get_it/injection_container.dart`)
- [x] Register DioClient as lazy singleton
- [x] Register remote sources as lazy singletons
- [x] Register repositories as lazy singletons
- [x] Register use cases as lazy singletons
- [x] Register BLoCs as factories

#### Phase 10: UI Layer - Navigation ✅
- [x] Create `lib/presentation/routes.dart` with GoRouter configuration
- [x] Define routes: `/` (FoldersScreen), `/folder/:folderId` (WordsScreen)
- [x] Add error handling for 404 pages

#### Phase 11: UI Layer - Folders Screen ✅
- [x] Update `lib/main.dart` - Initialize dotenv and GetIt
- [x] Create `lib/presentation/screens/folders_screen.dart` with BlocConsumer
- [x] Implement state rendering: loading, error, success, empty states
- [x] Add pull-to-refresh functionality
- [x] Update `lib/presentation/widgets/folder_card.dart` - Use FolderEntity

#### Phase 12: UI Layer - Words Screen ✅
- [x] Create `lib/presentation/screens/words_screen.dart` with BlocConsumer
- [x] Implement state rendering: loading, error, success, empty states
- [x] Add pull-to-refresh functionality
- [x] Create `lib/presentation/widgets/word_card.dart` - Display word details

#### Phase 13: Code Cleanup ✅
- [x] Delete `lib/data/api_client.dart` (replaced by DioClient)
- [x] Delete `lib/data/models/api_response.dart` (not used)
- [x] Delete `lib/presentation/folders_screen.dart` (moved to screens/)
- [x] Delete `test/widget_test.dart` (replaced by comprehensive tests)
- [x] Fix all imports to use package imports
- [x] Fix CardTheme → CardThemeData in app_theme.dart
- [x] Remove const from FoldersLoading.fromState() and WordsLoading.fromState()

#### Phase 14: Test Coverage ✅
- [x] Add test dependencies: `mocktail: ^1.0.4`, `bloc_test: ^9.1.7`
- [x] Create `test/helpers/test_fixtures.dart` - Centralized test data
- [x] Create `test/domain/use_case/get_folders_use_case_test.dart` - 4 tests
- [x] Create `test/domain/use_case/get_words_by_folder_use_case_test.dart` - 5 tests
- [x] Create `test/data/models/folder_model_test.dart` - 4 tests
- [x] Create `test/data/models/word_model_test.dart` - 4 tests
- [x] Create `test/data/repository/folder_repository_impl_test.dart` - 5 tests
- [x] Create `test/data/repository/word_repository_impl_test.dart` - 5 tests
- [x] Create `test/presentation/blocs/folders/folders_bloc_test.dart` - 7 tests
- [x] Create `test/presentation/blocs/words/words_bloc_test.dart` - 8 tests
- [x] Create `test/presentation/widgets/folder_card_test.dart` - 4 tests
- [x] Create `test/presentation/widgets/word_card_test.dart` - 7 tests
- [x] Fix DateTime type mismatches in model tests
- [x] Fix empty list matcher issues in repository tests
- [x] Fix missing WordEntity import in word_card_test.dart
- [x] All 56 tests passing ✅

#### Phase 15: Code Quality ✅
- [x] Run `flutter analyze` - Found 3 warnings
- [x] Run `dart format .` - Formatted 26 files
- [x] Remove unused import from `test/domain/use_case/get_folders_use_case_test.dart`
- [x] Remove unused import from `test/domain/use_case/get_words_by_folder_use_case_test.dart`
- [x] Fix unused variable warning in `test/presentation/widgets/folder_card_test.dart`
- [x] Re-run `flutter analyze` - Zero warnings ✅

#### Migration Summary
- ✅ Clean Architecture: Domain → Data → Presentation layers
- ✅ BLoC pattern with proper state management
- ✅ Dio for HTTP client (no auth interceptor - simplified)
- ✅ GetIt for dependency injection
- ✅ Android Material Design only (no Cupertino)
- ✅ READ-ONLY features (Folders + Words)
- ✅ Comprehensive test coverage (56 tests)
- ✅ Zero code quality warnings
- ✅ Follow CLAUDE.md coding rules

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
