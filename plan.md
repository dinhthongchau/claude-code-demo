# Plan: Create Simplified Test Repositories for AI Chat Word Addition Feature

## Phase 1: Backend Repository Setup

### Task 1.1: Create New Backend Repository Structure
- [ ] Clone/create new repository `be_enzo_english_test` or similar name
- [ ] Set up basic FastAPI project structure with minimal dependencies
- [ ] Configure `.env` file with MongoDB connection string (reusing existing database), with `env.example` . I will paste private key to .env
- [ ] Create `main.py` with basic FastAPI app initialization
- [ ] Add CORS middleware for Flutter web/mobile testing
- [ ] Test: Run `uvicorn main:app --reload` and verify server starts successfully

### Task 1.2: Implement User Authentication (Simplified)
- [ ] Create hardcoded user endpoint for dinhthongchau@gmail.com
- [ ] Add `/api/v1/auth/current-user` endpoint returning user object
- [ ] User object structure: `{id, email, name, created_at}`
- [ ] Test: Call endpoint via Postman/browser and verify user data returned ( create test files for me)

### Task 1.3: Implement User Folder Endpoints
- [ ] Create MongoDB connection utility (`database.py`)
- [ ] Create `user_folder` collection schema/models
- [ ] Implement `GET /api/v1/folders` - Get all folders for user dinhthongchau
- [ ] Implement `GET /api/v1/folders/{folder_id}` - Get single folder details
- [ ] Test: Call endpoints and verify folder data from existing MongoDB is returned

### Task 1.4: Implement Word List Endpoints
- [ ] Create `word_list` collection models
- [ ] Implement `GET /api/v1/folders/{folder_id}/words` - Get all words in a folder
- [ ] Implement `GET /api/v1/words/{word_id}` - Get detailed word information
- [ ] Include fields: word, definition, examples, images, part_of_speech, pronunciation, etc.
- [ ] Test: Call endpoints and verify word data with all fields is returned correctly

### Task 1.5: Implement OpenAI Integration for AI Suggestions
- [ ] Add `openai` package to requirements.txt
- [ ] Create `openai_service.py` with API key from .env
- [ ] Implement function `suggest_definition(word: str)` → returns definition text
- [ ] Implement function `suggest_examples(word: str)` → returns list of example sentences
- [ ] Test: Call functions directly in Python and verify OpenAI responses

### Task 1.6: Implement Pixabay Integration for Image Suggestions
- [ ] Add `requests` package for API calls
- [ ] Create `pixabay_service.py` with API key from .env
- [ ] Implement function `search_images(word: str)` → returns list of image URLs
- [ ] Test: Call function and verify image URLs are returned and accessible

### Task 1.7: Implement Word Creation Endpoint
- [ ] Create `POST /api/v1/words` endpoint
- [ ] Request body: `{word, folder_id, definition, examples[], image_url, notes, user_id}`
- [ ] Validate folder belongs to user
- [ ] Save word to MongoDB with metadata (created_at, updated_at)
- [ ] Return created word object with ID
- [ ] Test: Use Postman to create a word and verify it's saved in MongoDB

### Task 1.8: Implement AI-Assisted Word Creation Endpoint
- [ ] Create `POST /api/v1/words/ai-assist` endpoint
- [ ] Request body: `{word, folder_id}`
- [ ] Internally call OpenAI for definition + examples
- [ ] Internally call Pixabay for image suggestions
- [ ] Return: `{word, suggested_definition, suggested_examples[], suggested_images[]}`
- [ ] User can then edit and call regular word creation endpoint
- [ ] Test: Send word "Template", verify AI suggestions returned

### Task 1.9: Backend Documentation & Deployment Prep
- [ ] Create `README.md` with setup instructions
- [ ] Document all API endpoints with example requests/responses
- [ ] Create `requirements.txt` with all dependencies
- [ ] Test: Fresh clone → install deps → run server → all endpoints work

## Phase 2: Flutter Mobile Repository Setup

### Task 2.1: Create New Flutter Project
- [ ] Run `flutter create flutter_enzo_test` or similar name
- [ ] Set up basic project structure following clean architecture
- [ ] Add dependencies: `dio, flutter_bloc, get_it, go_router, equatable`
- [ ] Configure `pubspec.yaml` and run `flutter pub get`
- [ ] Test: Run `flutter run` and verify default app launches

### Task 2.2: Setup Core Infrastructure
- [ ] Create `lib/core/api/api_config.dart` with base URL configuration
- [ ] Create `lib/core/network/dio_client.dart` for HTTP client
- [ ] Create `lib/core/get_it/injection_container.dart` for dependency injection
- [ ] Add `.env` file with `BASE_URL=http://localhost:8887` (or your backend URL)
- [ ] Test: Initialize GetIt and verify no errors

### Task 2.3: Implement Domain Layer - User Folder
- [ ] Create `lib/domain/entity/user_folder_entity.dart`
- [ ] Create `lib/domain/repository/user_folder_repository.dart` interface
- [ ] Create `lib/domain/use_case/get_user_folders_use_case.dart`
- [ ] Create `lib/domain/use_case/get_folder_words_use_case.dart`
- [ ] Test: Code compiles without errors

### Task 2.4: Implement Data Layer - User Folder
- [ ] Create `lib/data/models/user_folder_model.dart` with fromJson/toJson
- [ ] Create `lib/data/models/word_model.dart` with fromJson/toJson
- [ ] Create `lib/data/source/remote/user_folder_remote_source.dart`
- [ ] Implement API calls: `getFolders()`, `getFolderWords(folderId)`
- [ ] Create `lib/data/repository/user_folder_repository_impl.dart`
- [ ] Test: Repository methods return Either<Failure, Data>

### Task 2.5: Implement Presentation Layer - Folder List
- [ ] Create `lib/presentation/blocs/user_folder/user_folder_bloc.dart`
- [ ] Create events: `LoadUserFoldersEvent`
- [ ] Create states: `UserFolderInitial, UserFolderLoading, UserFolderLoaded, UserFolderError`
- [ ] Create `lib/presentation/screens/folder_list_screen.dart`
- [ ] Display list of user folders in ListView
- [ ] Register BLoC in GetIt and provide in main.dart
- [ ] Test: Run app → see list of folders loaded from backend

### Task 2.6: Implement Presentation Layer - Word List
- [ ] Add event: `LoadFolderWordsEvent` to UserFolderBloc
- [ ] Update states to include words list
- [ ] Create `lib/presentation/screens/word_list_screen.dart`
- [ ] Display words when folder is tapped
- [ ] Add navigation from folder list → word list using GoRouter
- [ ] Test: Tap folder → see words in that folder

### Task 2.7: Implement Presentation Layer - Word Detail
- [ ] Create `lib/domain/use_case/get_word_detail_use_case.dart`
- [ ] Add event: `LoadWordDetailEvent` to bloc
- [ ] Create `lib/presentation/screens/word_detail_screen.dart`
- [ ] Display: word, definition, examples, images, pronunciation, part of speech
- [ ] Add navigation from word list → word detail
- [ ] Test: Tap word → see all word information displayed

### Task 2.8: Implement Domain/Data Layer - AI Word Creation
- [ ] Create `lib/domain/entity/ai_suggestion_entity.dart`
- [ ] Create `lib/domain/repository/ai_word_repository.dart` interface
- [ ] Create `lib/domain/use_case/get_ai_suggestions_use_case.dart`
- [ ] Create `lib/domain/use_case/create_word_use_case.dart`
- [ ] Create `lib/data/models/ai_suggestion_model.dart`
- [ ] Create `lib/data/source/remote/ai_word_remote_source.dart`
- [ ] Implement API calls: `getAiSuggestions(word)`, `createWord(wordData)`
- [ ] Create `lib/data/repository/ai_word_repository_impl.dart`
- [ ] Test: Repository methods compile and return correct types

### Task 2.9: Implement Presentation Layer - AI Chat Input
- [ ] Create `lib/presentation/blocs/ai_word/ai_word_bloc.dart`
- [ ] Events: `RequestAiSuggestionsEvent, CreateWordEvent`
- [ ] States: `AiWordInitial, AiWordLoading, AiSuggestionsLoaded, WordCreated, AiWordError`
- [ ] Create `lib/presentation/screens/ai_chat_screen.dart`
- [ ] Add text input field for entering word
- [ ] Add (+) button to trigger AI suggestions
- [ ] Test: Enter word "Template" → click (+) → loading state shows

### Task 2.10: Implement Presentation Layer - Word Edit Screen
- [ ] Create `lib/presentation/screens/word_edit_screen.dart`
- [ ] Display AI suggestions: definition (editable), examples (editable list), images (selectable)
- [ ] Add folder dropdown/selector to choose destination folder
- [ ] Add notes/custom definition text field
- [ ] Add image selector from suggested images
- [ ] Add "Save" button to create word
- [ ] Test: View AI suggestions → edit definition → select folder → select image → save

### Task 2.11: Implement Word Save & Refresh
- [ ] Connect "Save" button to `CreateWordEvent`
- [ ] Show loading indicator during save
- [ ] On success: show success message, navigate back to folder/word list
- [ ] Refresh word list to show newly added word
- [ ] On error: show error message
- [ ] Test: Save word → verify it appears in word list → verify it's in MongoDB

### Task 2.12: Polish UI/UX
- [ ] Add loading indicators for all async operations
- [ ] Add error handling and user-friendly error messages
- [ ] Add pull-to-refresh on folder list and word list
- [ ] Add empty states when no folders/words exist
- [ ] Add confirmation dialogs where appropriate
- [ ] Test: All user interactions feel smooth and responsive

## Phase 3: Integration Testing & Documentation

### Task 3.1: End-to-End Testing
- [ ] Start backend server on localhost:8887
- [ ] Run Flutter app on emulator/device
- [ ] Test complete flow:
  - [ ] Open app → see folders
  - [ ] Tap folder → see words
  - [ ] Tap word → see full details
  - [ ] Go to AI Chat → enter "Template"
  - [ ] Click (+) → see AI suggestions
  - [ ] Edit definition, select image, choose folder
  - [ ] Save → word appears in selected folder
  - [ ] Verify word persists after app restart
- [ ] Document any bugs found and fix them

### Task 3.2: Backend Documentation
- [ ] Create comprehensive `README.md` for backend repository
- [ ] Include: setup instructions, environment variables, API documentation
- [ ] Add example `.env.example` file
- [ ] Add deployment instructions
- [ ] Test: Give README to someone unfamiliar → they can set up and run backend

### Task 3.3: Mobile Documentation
- [ ] Create comprehensive `README.md` for Flutter repository
- [ ] Include: setup instructions, environment variables, architecture overview
- [ ] Add example `.env.example` file
- [ ] Document the AI word addition flow with screenshots
- [ ] Test: Give README to someone unfamiliar → they can set up and run app

### Task 3.4: Create Demo Video/Screenshots
- [ ] Record video showing complete user flow
- [ ] Take screenshots of each screen
- [ ] Create visual documentation of the AI word addition feature
- [ ] Prepare presentation materials for boss

### Task 3.5: Code Repository Preparation
- [ ] Push backend code to GitHub repository
- [ ] Push Flutter code to GitHub repository
- [ ] Ensure `.gitignore` excludes `.env` and sensitive files
- [ ] Add proper commit messages describing features
- [ ] Create release tags for stable versions
- [ ] Test: Clone both repos fresh → follow README → everything works

### Task 3.6: Deployment & Sharing
- [ ] Deploy backend to test server (optional: Heroku, Railway, DigitalOcean)
- [ ] Update Flutter app `.env` with deployed backend URL
- [ ] Build APK for Android testing
- [ ] Share repository links with boss
- [ ] Prepare presentation explaining the architecture and features

## Deliverables

- [ ] Backend repository with complete API for folder/word management + AI integration
- [ ] Flutter repository with clean architecture and AI word addition feature
- [ ] Both repositories running and connecting to existing MongoDB
- [ ] Complete documentation for both projects
- [ ] Testable at each phase with manual verification
- [ ] Ready to demo and share with stakeholders

## User Flow Summary

**AI Chat Word Addition Flow:**

1. [ ] User opens AI Chat screen
2. [ ] User enters word (e.g., "Template")
3. [ ] User clicks (+) button
4. [ ] App shows loading state
5. [ ] App displays AI suggestions:
   - [ ] Definition from OpenAI
   - [ ] Example sentences from OpenAI
   - [ ] Images from Pixabay
6. [ ] User edits definition and examples if needed
7. [ ] User selects target folder (e.g., "folder test")
8. [ ] User selects preferred image from suggestions
9. [ ] User adds custom notes (optional)
10. [ ] User clicks "Save"
11. [ ] App saves word to MongoDB with all metadata
12. [ ] App shows success message
13. [ ] App navigates back to folder/word list
14. [ ] New word appears in selected folder
