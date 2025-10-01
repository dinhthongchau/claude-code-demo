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

- [ ] **Define field validation rules**:
  - [ ] **word**: Required, 1-100 chars, string
  - [ ] **definition**: Required, 1-2000 chars, string
  - [ ] **folder_id**: Required, must be valid ObjectId, must exist, must belong to user
  - [ ] **examples**: Optional, List[str], max 20 items, each item max 500 chars, default empty list
  - [ ] **image_urls**: Optional, List[str], max 10 items, each item max 500 chars (URL validation optional), default empty list
  - [ ] **part_of_speech**: Optional, max 50 chars (noun, verb, adjective, etc. - free text for now)
  - [ ] **pronunciation**: Optional, max 200 chars (IPA or phonetic spelling)
  - [ ] **notes**: Optional, max 2000 chars
  - [ ] **user_id**: Auto-set from hardcoded user (email)
  - [ ] **created_at/updated_at**: Auto-set by system

- [ ] **Define API response format**:
  - [ ] Use existing `ApiResponse[T]` from dependencies.py (consistent with folders)
  - [ ] Success: `{success: true, message: "...", data: {...}, timestamp: datetime}`
  - [ ] Error: `{success: false, message: "...", code: str, error: str, timestamp: datetime}`
  - [ ] All endpoints return 200 status (consistent with Task 1.3 pattern)

- [ ] **Design API endpoints**:
  - [ ] **GET /api/v1/folders/{folder_id}/words** - List words in folder (nested under folder for clarity)
  - [ ] **POST /api/v1/words** - Create word (flat URL, folder_id in body)
  - [ ] **GET /api/v1/words/{word_id}** - Get single word
  - [ ] **PUT /api/v1/words/{word_id}** - Update word
  - [ ] **DELETE /api/v1/words/{word_id}** - Delete word
  - [ ] Note: Mixed nested/flat pattern for pragmatism (list is folder-centric, operations are word-centric)

- [ ] **Plan helper functions**:
  - [ ] **Reuse from folders_router.py**:
    - `get_hardcoded_user(users_col)` → Get/create test user
    - `validate_object_id(id_str)` → Validate ObjectId format, return ObjectId or raise 400
  - [ ] **New word-specific helpers**:
    - `validate_folder_ownership(folder_id: ObjectId, user_email: str, folders_col)` → Check folder exists and belongs to user, raise 404 if not
    - `convert_word_to_response(word: dict)` → Convert MongoDB doc to response format (ObjectId → string)

- [ ] **Define error handling strategy**:
  - [ ] 400 BAD_REQUEST: Invalid ObjectId format, validation failures, empty update
  - [ ] 404 NOT_FOUND: Word not found, folder not found, word doesn't belong to user
  - [ ] 404 FOLDER_NOT_FOUND: Folder doesn't exist when creating word
  - [ ] 500 INTERNAL_SERVER_ERROR: Database errors, unexpected exceptions
  - [ ] Consistent error format: `{message: str, code: str, error: str}`

- [ ] **Plan pagination and sorting**:
  - [ ] Add pagination to GET /api/v1/folders/{folder_id}/words (consistent with folders)
  - [ ] Parameters: `limit` (1-1000, default 100), `skip` (≥0, default 0)
  - [ ] Sorting: Alphabetically by word (most useful for vocabulary)
  - [ ] Use `.sort("word", 1)` in MongoDB query

- [ ] **Decide cascade delete behavior**:
  - [ ] **Decision**: Do NOT implement cascade delete in this phase
  - [ ] When folder deleted, words remain orphaned (acceptable for test version)
  - [ ] Document: Add cascade delete or prevent deletion in future iteration
  - [ ] Note: Could add background cleanup job or folder deletion validation later

- [ ] **Plan database indexes** (for future optimization):
  - [ ] Index on `folder_id` (most common query pattern)
  - [ ] Index on `user_id` (security queries)
  - [ ] Compound index on `(folder_id, user_id)` (best performance)
  - [ ] Note: Not implementing in Phase C, documenting for future

- [ ] **List test scenarios**:
  - [ ] **Happy path**: Create folder → Create word → List words → Get word → Update word → Delete word
  - [ ] **Error cases**:
    - Invalid word_id format, invalid folder_id format
    - Word not found, folder not found
    - Create word in non-existent folder, create word in other user's folder
    - Missing required fields (word, definition, folder_id)
    - Empty word name, empty definition
  - [ ] **Array validation**: Empty examples[], large examples[] (20 items), very long example strings
  - [ ] **Edge cases**: Long word (100 chars), long definition (2000 chars), Unicode characters, special characters
  - [ ] **Data validation**: ObjectId conversion, timestamps auto-set, user_id assignment, folder ownership validation

---

#### Phase B: Write Tests First (RED) ✅
- [ ] **Create test file structure**: `tests/test_words.py`
  - [ ] Follow test_auth.py and test_folders.py patterns
  - [ ] Import: requests, json, sys, io (Windows encoding fix)
  - [ ] Fix encoding: `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")`
  - [ ] Load BASE_URL from tests/.env
  - [ ] Helper functions: print_separator(), print_result()

- [ ] **Test Setup (before tests)**:
  - [ ] Add function to get test user_id: Call GET /auth/current-user, extract user.id
  - [ ] Add function to create test folder: POST /folders with TEST_ prefix, return folder_id
  - [ ] Add function to cleanup test words: DELETE all words with "TEST_" prefix in word field
  - [ ] Add function to cleanup test folders: DELETE all folders with "TEST_" prefix
  - [ ] Document: Tests use real MongoDB, cleanup is mandatory

- [ ] **Write Test 1: Setup - Create Test Folder**:
  - [ ] POST /api/v1/folders
  - [ ] Body: `{name: "TEST_Word Folder", description: "Test folder for words"}`
  - [ ] Assert: 200 status, save folder_id for subsequent tests
  - [ ] Note: Reuses folders endpoint (already tested in Task 1.3)

- [ ] **Write Test 2: List Words (Empty State)**:
  - [ ] GET /api/v1/folders/{test_folder_id}/words
  - [ ] Assert: 200 status, success=true, data=[] (empty list)
  - [ ] Verify ApiResponse format

- [ ] **Write Test 3: Create Word (Success)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "TEST_apple", folder_id: test_folder_id, definition: "A round fruit", examples: ["I ate an apple", "Apple pie"], image_urls: ["https://example.com/apple.jpg"], part_of_speech: "noun", pronunciation: "/ˈæp.əl/", notes: "Test word"}`
  - [ ] Assert: 200 status, success=true
  - [ ] Assert: data.id exists (24-char string), data.word matches, all fields present, timestamps exist
  - [ ] Save word_id for subsequent tests

- [ ] **Write Test 4: Create Word (Missing Required Field - word)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{folder_id: test_folder_id, definition: "Missing word"}`
  - [ ] Assert: 400 or 422 status, error message about missing "word"

- [ ] **Write Test 5: Create Word (Missing Required Field - definition)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "TEST_banana", folder_id: test_folder_id}`
  - [ ] Assert: 400 or 422 status, error message about missing "definition"

- [ ] **Write Test 6: Create Word (Missing Required Field - folder_id)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "TEST_orange", definition: "A citrus fruit"}`
  - [ ] Assert: 400 or 422 status, error message about missing "folder_id"

- [ ] **Write Test 7: Create Word (Non-existent Folder)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "TEST_grape", folder_id: "000000000000000000000000", definition: "Small fruit"}`
  - [ ] Assert: 404 status, error about folder not found

- [ ] **Write Test 8: Create Word (Invalid Folder ID Format)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "TEST_mango", folder_id: "invalid_id", definition: "Tropical fruit"}`
  - [ ] Assert: 400 status, error about invalid ObjectId format

- [ ] **Write Test 9: Create Word (Empty Word Name)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "", folder_id: test_folder_id, definition: "Empty word name"}`
  - [ ] Assert: 400 or 422 status, error about empty word

- [ ] **Write Test 10: Create Word (Empty Definition)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "TEST_kiwi", folder_id: test_folder_id, definition: ""}`
  - [ ] Assert: 400 or 422 status, error about empty definition

- [ ] **Write Test 11: Create Word (Minimal - No Optional Fields)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "TEST_pear", folder_id: test_folder_id, definition: "A sweet fruit"}`
  - [ ] Assert: 200 status, success=true
  - [ ] Assert: examples=[], image_urls=[], part_of_speech=None, pronunciation=None, notes=None

- [ ] **Write Test 12: Create Word (With Empty Arrays)**:
  - [ ] POST /api/v1/words
  - [ ] Body: `{word: "TEST_peach", folder_id: test_folder_id, definition: "Fuzzy fruit", examples: [], image_urls: []}`
  - [ ] Assert: 200 status, arrays are empty

- [ ] **Write Test 13: List Words (With Data)**:
  - [ ] GET /api/v1/folders/{test_folder_id}/words
  - [ ] Assert: 200 status, data is list, length >= 1
  - [ ] Assert: Each word has required fields (id, word, definition, folder_id, user_id, created_at)
  - [ ] Assert: Words sorted alphabetically by word field

- [ ] **Write Test 14: List Words (Pagination - First Page)**:
  - [ ] GET /api/v1/folders/{test_folder_id}/words?limit=2&skip=0
  - [ ] Assert: 200 status, data length <= 2

- [ ] **Write Test 15: List Words (Pagination - Invalid Limit)**:
  - [ ] GET /api/v1/folders/{test_folder_id}/words?limit=2000
  - [ ] Assert: 400 status, error about limit range (1-1000)

- [ ] **Write Test 16: List Words (Pagination - Negative Skip)**:
  - [ ] GET /api/v1/folders/{test_folder_id}/words?skip=-5
  - [ ] Assert: 400 status, error about skip must be >= 0

- [ ] **Write Test 17: Get Single Word (Success)**:
  - [ ] GET /api/v1/words/{word_id}
  - [ ] Assert: 200 status, data matches created word
  - [ ] Assert: All fields present (including arrays, optional fields)

- [ ] **Write Test 18: Get Single Word (Not Found)**:
  - [ ] GET /api/v1/words/000000000000000000000000
  - [ ] Assert: 404 status, error about word not found

- [ ] **Write Test 19: Get Single Word (Invalid ID Format)**:
  - [ ] GET /api/v1/words/invalid_word_id
  - [ ] Assert: 400 status, error about invalid ObjectId

- [ ] **Write Test 20: Update Word (Success - Partial Update)**:
  - [ ] PUT /api/v1/words/{word_id}
  - [ ] Body: `{definition: "Updated definition", notes: "Updated notes"}`
  - [ ] Assert: 200 status, definition updated, notes updated
  - [ ] Assert: word unchanged, updated_at > created_at

- [ ] **Write Test 21: Update Word (Success - Update Arrays)**:
  - [ ] PUT /api/v1/words/{word_id}
  - [ ] Body: `{examples: ["New example 1", "New example 2"], image_urls: ["https://new.com/img.jpg"]}`
  - [ ] Assert: 200 status, arrays replaced with new values

- [ ] **Write Test 22: Update Word (Empty Update)**:
  - [ ] PUT /api/v1/words/{word_id}
  - [ ] Body: `{}`
  - [ ] Assert: 400 status, error about no fields to update

- [ ] **Write Test 23: Update Word (Not Found)**:
  - [ ] PUT /api/v1/words/000000000000000000000000
  - [ ] Assert: 404 status

- [ ] **Write Test 24: Delete Word (Success)**:
  - [ ] DELETE /api/v1/words/{word_id}
  - [ ] Assert: 200 status, success=true
  - [ ] Verify: GET /api/v1/words/{word_id} returns 404

- [ ] **Write Test 25: Delete Word (Not Found)**:
  - [ ] DELETE /api/v1/words/000000000000000000000000
  - [ ] Assert: 404 status

- [ ] **Add test cleanup function**:
  - [ ] Delete all words with "TEST_" prefix in word field
  - [ ] Delete all folders with "TEST_" prefix
  - [ ] Call in teardown or at end of test suite

- [ ] **Add test summary and CURL examples**:
  - [ ] Follow test_auth.py and test_folders.py format
  - [ ] Print all passed/failed tests
  - [ ] Show example CURL commands for each endpoint
  - [ ] Include examples with arrays in request body

- [x] **Run tests**: Execute `python tests/test_words.py`
  - [ ] Verify all tests FAIL (endpoints don't exist yet) ✅ RED phase complete
  - [ ] Check error messages are clear (ImportError, ConnectionRefused, 404, etc.)

- [x] **Review tests**: Ensure comprehensive coverage
  - [ ] All CRUD operations covered
  - [ ] All error cases covered
  - [ ] Array validation covered
  - [ ] Pagination covered
  - [ ] Folder ownership validation covered

- [x] **Commit tests**: `git commit -m "test: add comprehensive tests for word endpoints"`

---

#### Phase C: Implement Code (GREEN) ✅
- [x] **Create Pydantic models**: `models/word.py`
  - [ ] Import: BaseModel, Field, Optional, List from pydantic
  - [ ] **CreateWordRequest**:
    - word: str = Field(..., min_length=1, max_length=100)
    - folder_id: str = Field(..., description="Folder ObjectId as string")
    - definition: str = Field(..., min_length=1, max_length=2000)
    - examples: Optional[List[str]] = Field(default_factory=list, max_length=20)
    - image_urls: Optional[List[str]] = Field(default_factory=list, max_length=10)
    - part_of_speech: Optional[str] = Field(None, max_length=50)
    - pronunciation: Optional[str] = Field(None, max_length=200)
    - notes: Optional[str] = Field(None, max_length=2000)
  - [ ] **UpdateWordRequest**:
    - word: Optional[str] = Field(None, min_length=1, max_length=100)
    - definition: Optional[str] = Field(None, min_length=1, max_length=2000)
    - examples: Optional[List[str]] = Field(None, max_length=20)
    - image_urls: Optional[List[str]] = Field(None, max_length=10)
    - part_of_speech: Optional[str] = Field(None, max_length=50)
    - pronunciation: Optional[str] = Field(None, max_length=200)
    - notes: Optional[str] = Field(None, max_length=2000)
    - Note: Do NOT allow folder_id update (words can't move between folders in this version)
  - [ ] **WordResponse**:
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
  - [ ] Add Config class with example schemas

- [x] **Create router**: `routers/words_router.py`
  - [ ] Import: APIRouter, Depends, HTTPException, status, List
  - [ ] Import: get_wordlists_collection, get_folders_collection, get_users_collection, ApiResponse, HARDCODED_EMAIL from dependencies
  - [ ] Import: CreateWordRequest, UpdateWordRequest, WordResponse from models.word
  - [ ] Import: ObjectId from bson, InvalidId from bson.errors
  - [ ] Import: datetime
  - [ ] Create router with prefix="/api/v1", tags=["Words"]

- [ ] **Create helper functions in words_router.py**:
  - [ ] **get_hardcoded_user()**: Copy from folders_router.py (or extract to shared utils)
  - [ ] **validate_object_id(id_str: str) -> ObjectId**: Copy from folders_router.py
  - [ ] **validate_folder_ownership(folder_id: ObjectId, user_email: str, folders_col) -> dict**:
    - Query: folder = await folders_col.find_one({"_id": folder_id, "user_id": user_email})
    - If not found: raise HTTPException 404 FOLDER_NOT_FOUND
    - Return: folder document
  - [ ] **convert_word_to_response(word: dict) -> dict**:
    - Convert: word["id"] = str(word["_id"]), del word["_id"]
    - Ensure arrays default to empty lists if missing
    - Return: word dict

- [x] **Implement GET /api/v1/folders/{folder_id}/words** - List words in folder:
  - [ ] Async function with path param folder_id: str
  - [ ] Query params: limit: int = 100, skip: int = 0
  - [ ] Dependencies: get_wordlists_collection, get_folders_collection, get_users_collection
  - [ ] Validate pagination parameters (limit 1-1000, skip >= 0)
  - [ ] Get hardcoded user
  - [ ] Validate folder_id format (ObjectId)
  - [ ] Validate folder ownership (folder exists and belongs to user)
  - [ ] Query words: words = await words_col.find({"folder_id": folder_id_str, "user_id": user["email"]}).sort("word", 1).skip(skip).limit(limit).to_list(limit)
  - [ ] Note: Store folder_id as string in MongoDB (not ObjectId) for simplicity
  - [ ] Convert ObjectId → string for each word
  - [ ] Map to WordResponse objects
  - [ ] Return ApiResponse[List[WordResponse]] with success=True
  - [ ] Error handling: 400 invalid IDs/pagination, 404 folder not found, 500 DB errors

- [x] **Implement POST /api/v1/words** - Create word:
  - [ ] Async function with request: CreateWordRequest
  - [ ] Dependencies: get_wordlists_collection, get_folders_collection, get_users_collection
  - [ ] Get hardcoded user
  - [ ] Validate folder_id format (ObjectId)
  - [ ] Validate folder ownership (folder exists and belongs to user)
  - [ ] Create word document:
    - word, definition, examples (default []), image_urls (default []), part_of_speech, pronunciation, notes from request
    - folder_id = request.folder_id (store as string)
    - user_id = user["email"]
    - created_at = datetime.now()
    - updated_at = datetime.now()
  - [ ] Insert: result = await words_col.insert_one(word_data)
  - [ ] Retrieve inserted word: await words_col.find_one({"_id": result.inserted_id})
  - [ ] Convert ObjectId → string
  - [ ] Return ApiResponse[WordResponse] with success=True
  - [ ] Error handling: 400 validation errors, 404 folder not found, 500 DB errors

- [x] **Implement GET /api/v1/words/{word_id}** - Get single word:
  - [ ] Async function with path param: word_id: str
  - [ ] Dependencies: get_wordlists_collection, get_users_collection
  - [ ] Get hardcoded user
  - [ ] Validate word_id format (ObjectId)
  - [ ] Query: word = await words_col.find_one({"_id": ObjectId(word_id), "user_id": user["email"]})
  - [ ] If not found: 404 HTTPException
  - [ ] Convert ObjectId → string
  - [ ] Return ApiResponse[WordResponse]
  - [ ] Error handling: 400 invalid ID, 404 not found, 500 DB error

- [x] **Implement PUT /api/v1/words/{word_id}** - Update word:
  - [ ] Async function with word_id: str, request: UpdateWordRequest
  - [ ] Dependencies: get_wordlists_collection, get_users_collection
  - [ ] Get hardcoded user
  - [ ] Validate word_id format (ObjectId)
  - [ ] Build update dict: {k: v for k, v in request.model_dump(exclude_unset=True).items()}
  - [ ] Check for empty update BEFORE adding timestamp (avoid bug from Task 1.3)
  - [ ] If empty: raise HTTPException 400 NO_UPDATE_FIELDS
  - [ ] Add updated_at = datetime.now()
  - [ ] Update: result = await words_col.update_one({"_id": ObjectId(word_id), "user_id": user["email"]}, {"$set": update_data})
  - [ ] If result.matched_count == 0: 404 HTTPException
  - [ ] Retrieve updated word
  - [ ] Return ApiResponse[WordResponse]
  - [ ] Error handling: 400 invalid ID/empty update, 404 not found, 500 DB error

- [x] **Implement DELETE /api/v1/words/{word_id}** - Delete word:
  - [ ] Async function with word_id: str
  - [ ] Dependencies: get_wordlists_collection, get_users_collection
  - [ ] Get hardcoded user
  - [ ] Validate word_id format (ObjectId)
  - [ ] Delete: result = await words_col.delete_one({"_id": ObjectId(word_id), "user_id": user["email"]})
  - [ ] If result.deleted_count == 0: 404 HTTPException
  - [ ] Return ApiResponse with success=True, message="Word deleted successfully"
  - [ ] Error handling: 400 invalid ID, 404 not found, 500 DB error

- [x] **Register router in main.py**:
  - [ ] Import: from routers.words_router import router as words_router
  - [ ] Add: app.include_router(words_router)

- [x] **Run tests**: Execute `python tests/test_words.py`
  - [ ] Iterate on failing tests
  - [ ] Fix bugs, adjust response formats
  - [ ] Ensure ObjectId conversion works
  - [ ] Verify timestamps are set correctly
  - [ ] Verify folder ownership validation works
  - [ ] Verify array handling works (empty lists, populated lists)
  - [ ] Verify pagination works
  - [ ] Continue until all tests PASS ✅ GREEN phase complete

- [ ] **Manual verification**:
  - [ ] Start server: `python main.py`
  - [ ] Open Swagger docs: http://localhost:8829/docs
  - [ ] Test each endpoint manually:
    - Create test folder
    - Create word with all fields
    - Create word with minimal fields
    - List words (verify sorting)
    - Get single word
    - Update word
    - Delete word
  - [ ] Verify MongoDB data via Compass/shell:
    - Check wordlists collection
    - Verify folder_id stored as string
    - Verify arrays stored correctly
    - Verify timestamps
  - [ ] Test edge cases not covered by automated tests:
    - Very long strings (approaching limits)
    - Unicode characters (emoji, Chinese, Arabic)
    - Special characters in pronunciation (IPA symbols)
    - Large arrays (20 examples, 10 image_urls)

- [ ] **Commit implementation**: `git commit -m "feat: implement word CRUD endpoints with simplified auth"`

---

#### Phase D: Refactor (REFACTOR)
- [ ] **Extract shared helper functions**:
  - [ ] Option A: Create `utils/helpers.py` with get_hardcoded_user(), validate_object_id()
  - [ ] Option B: Keep duplicated in both routers (acceptable for small project)
  - [ ] Decision: Keep duplicated for now (simpler, no circular imports)
  - [ ] Document: Consider extracting to shared utils in future refactor

- [ ] **Create word-specific helper module** (optional):
  - [ ] If logic becomes complex, extract to `utils/word_helpers.py`
  - [ ] Functions: validate_folder_ownership, convert_word_to_response
  - [ ] For now: Keep in words_router.py (simpler)

- [ ] **Improve error messages**:
  - [ ] Consistent error format across all endpoints
  - [ ] User-friendly error messages (avoid technical jargon)
  - [ ] Proper HTTP status codes (400 vs 404 vs 500)
  - [ ] Specific error codes: INVALID_OBJECT_ID, WORD_NOT_FOUND, FOLDER_NOT_FOUND, NO_UPDATE_FIELDS, etc.

- [ ] **Add comprehensive docstrings**:
  - [ ] Add docstrings to all endpoint functions
  - [ ] Document parameters, return types, exceptions
  - [ ] Add usage examples in docstrings
  - [ ] Document helper functions

- [ ] **Code cleanup**:
  - [ ] Remove code duplication where reasonable
  - [ ] Improve variable naming (e.g., words_col vs wordlists_col for clarity)
  - [ ] Add type hints everywhere (params, return types, variables)
  - [ ] Format with `ruff format`
  - [ ] Run `ruff check --fix` for any linting issues

- [ ] **Review array handling**:
  - [ ] Ensure empty arrays default correctly
  - [ ] Verify None vs [] handling in optional fields
  - [ ] Check array validation (max length enforced)
  - [ ] Test updating arrays (replace vs append - currently replace)

- [ ] **Run tests again**: Ensure refactoring didn't break anything
  - [ ] Execute: `python tests/test_words.py`
  - [ ] All tests still pass ✅
  - [ ] No regressions introduced

- [ ] **Commit refactoring**: `git commit -m "refactor: extract helpers and improve word endpoints code quality"`

---

#### Phase E: Code Quality & Bug Fixes
- [ ] **Validation review**:
  - [ ] Run `/validate all code in @be_enzo_english_test\`
  - [ ] Review critical issues
  - [ ] Review medium issues
  - [ ] Prioritize fixes

- [ ] **Fix any critical bugs found**:
  - [ ] Empty update validation (check BEFORE adding timestamp)
  - [ ] ObjectId conversion edge cases
  - [ ] Array handling edge cases
  - [ ] Folder ownership validation edge cases

- [ ] **Add missing pagination validation** (if not already done):
  - [ ] Ensure limit 1-1000
  - [ ] Ensure skip >= 0
  - [ ] Clear error messages

- [ ] **Performance considerations** (document for future):
  - [ ] Note: Add database indexes in production
  - [ ] Index on folder_id for fast word listing
  - [ ] Index on user_id for security
  - [ ] Compound index (folder_id, user_id) for best performance
  - [ ] Note: Not implementing now (test environment, small data)

- [ ] **Security review**:
  - [ ] Verify user_id always set from authenticated user (hardcoded)
  - [ ] Verify folder ownership checked before word creation
  - [ ] Verify word ownership checked before get/update/delete
  - [ ] Verify no way to access other users' words
  - [ ] Verify no SQL injection vectors (using MongoDB, low risk)

- [ ] **Edge case handling**:
  - [ ] Test with maximum field lengths
  - [ ] Test with Unicode characters
  - [ ] Test with empty arrays vs None
  - [ ] Test concurrent updates (acceptable data loss for test version)

- [ ] **Documentation review**:
  - [ ] Verify all endpoints documented in docstrings
  - [ ] Verify Swagger UI shows correct examples
  - [ ] Verify error responses documented
  - [ ] Update main README if needed (API endpoints section)

- [ ] **Final test run**:
  - [ ] Execute all test files: test_auth.py, test_folders.py, test_words.py
  - [ ] All tests pass ✅
  - [ ] No warnings or errors
  - [ ] Test summary shows 100% pass rate

- [ ] **Commit quality improvements**: `git commit -m "fix: resolve bugs and improve word endpoints quality"`

---

#### Phase F: Documentation ✅
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
