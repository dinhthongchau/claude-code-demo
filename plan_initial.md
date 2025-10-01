# Plan: Basic Test Repositories - Folder & Word Management with Firebase Auth

**Scope:** This plan covers only the core functionality - Firebase authentication, folder management, and word management. All AI chat features will be implemented later in a separate plan.

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

### Task 1.3: Implement User Folder Endpoints
**Based on:** `be_enzo_english` existing folder

- [ ] Create `database.py` with MongoDB connection utility
- [ ] Create `models/user_folder.py` with Pydantic schemas
  - [ ] UserFolder schema: `{id, name, description, user_id, created_at, updated_at, color, icon}`
- [ ] Create `routers/folders.py` with folder endpoints
- [ ] Implement `GET /api/v1/folders` - Get all folders for authenticated user (dinhthongchau@gmail.com)
  - [ ] Requires Firebase authentication
  - [ ] Returns list of folders from MongoDB
- [ ] Implement `GET /api/v1/folders/{folder_id}` - Get single folder details
  - [ ] Requires Firebase authentication
  - [ ] Validates folder belongs to authenticated user
- [ ] Implement `POST /api/v1/folders` - Create new folder
  - [ ] Requires Firebase authentication
  - [ ] Request body: `{name, description, color, icon}`
  - [ ] Saves to MongoDB with user_id
- [ ] Implement `PUT /api/v1/folders/{folder_id}` - Update folder
  - [ ] Requires Firebase authentication
  - [ ] Validates folder belongs to authenticated user
- [ ] Implement `DELETE /api/v1/folders/{folder_id}` - Delete folder
  - [ ] Requires Firebase authentication
  - [ ] Validates folder belongs to authenticated user
- [ ] Create test file `tests/test_folders.py` with sample requests
- [ ] Test: Call all endpoints via Postman and verify CRUD operations work

### Task 1.4: Implement Word List Endpoints
**Based on:** `be_enzo_english` existing folder

- [ ] Create `models/word.py` with Pydantic schemas
  - [ ] Word schema: `{id, word, definition, examples[], image_urls[], part_of_speech, pronunciation, notes, folder_id, user_id, created_at, updated_at}`
- [ ] Create `routers/words.py` with word endpoints
- [ ] Implement `GET /api/v1/folders/{folder_id}/words` - Get all words in a folder
  - [ ] Requires Firebase authentication
  - [ ] Validates folder belongs to authenticated user
  - [ ] Returns list of words
- [ ] Implement `GET /api/v1/words/{word_id}` - Get detailed word information
  - [ ] Requires Firebase authentication
  - [ ] Validates word belongs to authenticated user
  - [ ] Returns full word details with all fields
- [ ] Implement `POST /api/v1/words` - Create new word
  - [ ] Requires Firebase authentication
  - [ ] Request body: `{word, folder_id, definition, examples[], image_urls[], part_of_speech, pronunciation, notes}`
  - [ ] Validates folder belongs to authenticated user
  - [ ] Saves to MongoDB with metadata
  - [ ] Returns created word object with ID
- [ ] Implement `PUT /api/v1/words/{word_id}` - Update word
  - [ ] Requires Firebase authentication
  - [ ] Validates word belongs to authenticated user
- [ ] Implement `DELETE /api/v1/words/{word_id}` - Delete word
  - [ ] Requires Firebase authentication
  - [ ] Validates word belongs to authenticated user
- [ ] Create test file `tests/test_words.py` with sample requests
- [ ] Test: Call all endpoints via Postman and verify CRUD operations work

### Task 1.5: Backend Documentation & Testing
- [ ] Create comprehensive `README.md` with:
  - [ ] Setup instructions (clone, install dependencies, configure .env)
  - [ ] Firebase setup instructions
  - [ ] MongoDB connection setup
  - [ ] How to run the server
  - [ ] API documentation for all endpoints with example requests/responses
- [ ] Create `requirements.txt` with all dependencies:
  - [ ] fastapi
  - [ ] uvicorn
  - [ ] pymongo / motor (async MongoDB)
  - [ ] firebase-admin
  - [ ] pydantic
  - [ ] python-dotenv
  - [ ] python-multipart
- [ ] Create `.env.example` with all required environment variables
- [ ] Create Postman collection or API documentation file
- [ ] Test: Fresh clone → install deps → configure .env → run server → all endpoints work

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
