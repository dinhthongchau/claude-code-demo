# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

eVibe English is a Flutter mobile with just user folder management and add word with chat AI

## **Test-Driven Development (TDD) Guide**

TDD will be applied in **eVibe English** to ensure high-quality, maintainable code.

### The TDD Cycle
- **Red** → Write a failing test that defines the expected behavior.  
- **Green** → Write the simplest code to make the test pass.  
- **Refactor** → Clean up and optimize code while keeping tests passing.  
- **Commit** → Only commit once tests are green and refactoring is complete.

### Applying TDD in Flutter
1. **Domain Layer**  
   - Write tests for entities and use cases (e.g., `GetUserProfile`).  
   - Implement minimal code until tests pass.  
   - Refactor logic safely.

2. **Data Layer**  
   - Write tests for models (`fromJson`, `toJson`, `copyWith`).  
   - Implement repositories with Either<Failure, Entity> return types.  
   - Mock external dependencies with `mocktail`.

3. **Presentation Layer (Cubit/BLoC)**  
   - Write tests for Cubit/BLoC states: `Initial`, `Loading`, `Success`, `Error`.  
   - Use `bloc_test` to verify state transitions.  
   - Implement Cubit/BLoC and iterate until all tests pass.

### Benefits
- Forces **clearer requirements** (tests define expected behavior before code).  
- Prevents **regressions** (tests are a safety net).  
- Enables **safer refactoring**.  
- Produces **modular, maintainable, and testable code**.  

### Example Workflow (linear)
TASK → DETAIL PLAN → WRITE TEST → RUN (FAIL) → WRITE CODE (PASS) → ITERATE (Refactor/Retest) → COMMIT

Copy code

## Development Commands

### Running the Application
```bash
flutter run                    # Run on connected device/emulator
flutter run -d chrome          # Run on web
flutter run -d windows         # Run on Windows
```

### Code Generation
```bash
flutter pub run build_runner build --delete-conflicting-outputs  # Generate JSON serialization and assets
```

### Linting
```bash
flutter analyze                # Run static analysis
```

### Building
```bash
flutter build apk              # Build Android APK
flutter build appbundle        # Build Android App Bundle
flutter build web              # Build for web
```

### Dependencies
```bash
flutter pub get                # Install dependencies
flutter pub upgrade            # Upgrade dependencies
```

## Architecture

### Clean Architecture Layers

**Domain Layer** (`lib/domain/`)
- `entity/`: Business entities (immutable data classes)
- `repository/`: Repository interfaces (contracts)
- `use_case/`: Business logic use cases

**Data Layer** (`lib/data/`)
- `models/`: Data models with JSON serialization (extends entities)
- `repository/`: Repository implementations
- `source/remote/`: Remote data sources (API calls via Dio)

**Presentation Layer** (`lib/presentation/`)
- `blocs/`: BLoC state management (events, states, blocs)
- `screens/`: Screen implementations
- `widgets/`: Reusable UI components
- `routes.dart`: GoRouter configuration

**Core** (`lib/core/`)
- `api/`: API configuration (base URL from .env)
- `get_it/`: Dependency injection container setup
- `network/`: Dio client with Firebase Auth interceptors
- `theme/`: App theming and colors
- `constants/`: App-wide constants
- `errors/`: Custom exceptions and failures

### Key Architectural Patterns

1. **Dependency Injection**: GetIt container (`lib/core/get_it/injection_container.dart`) manages all service registrations. Register dependencies in order: External → Data Sources → Repositories → Use Cases → BLoCs.

2. **BLoC Pattern**:
   - Events trigger state changes
   - States are immutable with `Equatable`
   - BLoCs are provided globally in `main.dart` via `MultiBlocProvider`
   - Use `context.read<BlocName>().add(Event())` to dispatch events

3. **Repository Pattern**:
   - Domain defines interfaces
   - Data layer implements with `Either<Failure, Data>` return types (using `dartz`)
   - Remote sources handle API calls and map models to entities

4. **Navigation**: GoRouter with nested shell routes for bottom navigation
   - Use `context.push()` or `context.go()` for navigation
   - Use `context.pop()` instead of `Navigator.pop()`
   - Routes defined in `lib/presentation/routes.dart`

### Data Flow

```
UI (Screen) → BLoC (Event) → Use Case → Repository Interface → Repository Impl → Remote Source → API
                ↓
UI ← BLoC (State) ← Use Case ← Either<Failure, Entity> ← Model.toEntity() ← API Response
```

## Important Coding Rules

These rules come from `.cursor/rules/enzo_english_rule.mdc`:

1. **UI Text Constants**: All user-facing strings go in `lib/presentation/screens/text_screens_constant.dart`

2. **Navigation**: Always use GoRouter (`context.pop()`, `context.push()`), never `Navigator.pop(context)`

3. **System Constants**: App version and system-wide constants go in `lib/core/constants/constants.dart`

4. **Widget Creation**: Prefer widget methods over separate classes:
   - ✅ `Widget buildAbc()` or `Widget _buildAbc()`
   - ❌ `class AbcWidget extends StatelessWidget`

5. **API Response Handling**: Use `ApiResponseModel` for all API responses, don't create custom response models

6. **Module Structure**: Keep files organized by layer (core, data, domain, presentation)

## Configuration Requirements

Before running the app, ensure these files exist (provided by admin):

1. **Environment Configuration**:
   - Create `lib/dotenv` file with:
     - `BASE_URL`: API base URL for mobile
     - `BASE_URL_WEB`: API base URL for web
   - Use template from `lib/dotenv(example)` if available

2. **Firebase Configuration**:
   - `android/app/google-services.json`
   - `lib/firebase_options.dart`
   - `firebase.json`

3. **API Configuration**: Base URLs are loaded from `.env` via `ApiConfig.getBaseUrl()` in `lib/core/api/api_config.dart`

## Key Features Implementation

### Authentication
- Firebase Auth with email/password and Google Sign-In
- Managed by `AuthBloc` with `FirebaseAuthService`
- Session tokens stored via `LocalStorageService` (SharedPreferences)

### Dictionary & Learning System
- Hierarchical structure: Dictionary → Groups → Topics → Words
- Custom user folders and word lists
- Spaced repetition algorithm (SRS) for review scheduling
- Multiple learning modes: flashcards, listening, typing, recognition

### AI-Powered Features
- Grammar exercises generation via API
- Dialogue practice with conversation scenarios
- Pronunciation training with Wave2Vec and espeak (IPA matching)

### Media Integration
- Audio playback via `just_audio`
- Text-to-speech via `flutter_tts` (`TtsService`)
- YouTube video integration via `youtube_player_iframe`

## Common Development Tasks

### Adding a New Feature
1. Define entity in `lib/domain/entity/`
2. Create model extending entity in `lib/data/models/` with JSON serialization
3. Define repository interface in `lib/domain/repository/`
4. Implement repository in `lib/data/repository/`
5. Create remote source in `lib/data/source/remote/`
6. Create use case(s) in `lib/domain/use_case/`
7. Create BLoC with events and states in `lib/presentation/blocs/`
8. Register all dependencies in `lib/core/get_it/injection_container.dart`
9. Provide BLoC in `main.dart` if needed globally
10. Build UI in `lib/presentation/screens/`

### Adding a New Screen
1. Create screen file in `lib/presentation/screens/`
2. Add route in `lib/presentation/routes.dart`
3. Use `TopicListScreen` pattern for reference: define both `routePath` and `routeName`

### Working with BLoCs
- BLoCs are singletons registered in GetIt
- Access via `context.read<BlocName>()` for events
- Listen via `BlocBuilder<BlocName, StateName>` for state changes
- States should preserve previous data using `.fromState()` factory constructors

### API Integration
- All remote sources use `DioClient` which handles:
  - Firebase Auth token injection
  - Base URL configuration
  - Error handling and timeouts
- HTTP methods: `get()`, `post()`, `put()`, `delete()`
- API responses wrap data in standard format, handle with `ApiResponseModel`

## Testing

No test files currently exist in the project. When adding tests, create them in `test/` directory following the same structure as `lib/`.

## **Code Style Rules**

1. Always use **package imports**.
2. In `main`, use `BlocProvider`; access via `context.read`, `BlocConsumer`, `BlocBuilder`, or `BlocListener`.
3. Use `withValues(alpha: x)` instead of `withOpacity(x)`.
4. Use `GoRouter` for navigation/deep linking:

   ```dart
   GoRoute(
     path: Screen.routeName,
     builder: (context, state) => Screen(),
   )
   ```
5. Use `Container` for UI, wrap with `GestureDetector` for clicks (no `ElevatedButton`, no `Card`).
6. Use `ListView` / `GridView` instead of `.map(...).toList()`.
7. Use **enums** for comparisons/case statements, not raw strings.
8. Flutter ≥3.22 → use `spacing` in `Row`/`Column` instead of `SizedBox(width: x)`.
9. Follow existing file style; put utilities in `lib/core/utils`.
10. Fix only requested errors/functions, ignore warnings/hints unless specified.
11. . Nếu có lệnh hoặc hành động cần thực hiện (ví dụ: chạy code, tạo/xóa file, gọi API, thực thi command, chỉnh sửa tài liệu...), phải hỏi và chờ sự xác nhận từ người dùng trước khi thực hiện. Không tự động thực thi.
12. Code and document in English.
13. Keep logic in **BloC**; screens only trigger events.
14. For new functions → create related BloC Events/States; if BloC doesn’t exist → ask if needed.
15. Add concise English comments for complex functions, and use debugPrint for error tracing. However, avoid using debugPrint for functions related to Bloc, as it is already managed by the SimpleBlocObserver which provides observation of events, changes, and transitions for better tracking.
16. When writing a long list of widgets (for example: children: [GestureDetector(), GestureDetector()] or similar), always separate each element into its own widget (method) like _buildButtonABC() or _buildABC() (do not separate into a class, but into a method that returns a Widget at the top of the file). Apply this flexibly to special cases like AppBar (using PreferredSize) or other exceptions. to easy to read, and maintainable, following the principle of separating UI logic into smaller functions/widgets.
17. Dùng BlocConsumer ở Screen, tách toàn bộ logic ra khỏi UI (không dùng kiểu void hay viết hàm xử lý logic trong UI). Trong listener, xử lý các trạng thái như success, error và trả về phản hồi phù hợp; trong builder, hiển thị widget tương ứng với trạng thái (ví dụ loading → return Center(child: CircularProgressIndicator()), success trả về widget chính. không cần error vì listener đã xử lí ).
18. Khi code các widget, không set cứng height, widget. Ưu tiên hiển thị được ở mọi toàn bộ screen với expand, flexible .
---

## **State Rules**

* All states must extend an **abstract Equatable base state** with required `props`.
* Required states: `Initial`, `Loading`, `Success`, `Error`.
* Example:

  ```dart
  sealed class StatisticsState extends Equatable {
    final List<OrderModel>? allDataOrder;
    const StatisticsState({this.allDataOrder});
    @override
    List<Object?> get props => [allDataOrder];
  }

  class StatisticsInitial extends StatisticsState {
    const StatisticsInitial({super.allDataOrder});

  }

  class StatisticsLoading extends StatisticsState {
    const StatisticsLoading.fromState({required StatisticsState state})
        : super(allDataOrder: state.allDataOrder);
 
  }

  class StatisticsSuccess extends StatisticsState {
    const StatisticsSuccess({super.allDataOrder});
  }

  class StatisticsError extends StatisticsState {
    final String? errorMessage;
    const StatisticsError({super.allDataOrder, required this.errorMessage});
    @override
     List<Object?> get props => [...super.props, errorMessage];
  }
  ```

---

## **BloC Rules**

1. Always handle `Loading`, `Success`, `Error` states.
2. Use `try-catch` for specific error handling.
3. Example:

   ```dart
   class StatisticsBloc extends Bloc<StatisticsEvent, StatisticsState> {
     StatisticsBloc() : super(StatisticsInitial(allDataOrder: [])) {
       on<LoadOrdersEvent>(_onLoadOrders);
     }

     Future<void> _onLoadOrders(
       LoadOrdersEvent event,
       Emitter<StatisticsState> emit,
     ) async {
       emit(StatisticsLoading.fromState(state: state));
       try {
         final updatedOrders = await getIt<OrderDataService>().getOrdersAPI();
         if (updatedOrders.isEmpty) throw Exception('No orders found');
         emit(StatisticsSuccess(allDataOrder: updatedOrders));
       } catch (e, stackTrace) {
         final msg = e is TimeoutException
             ? 'Request timed out: ${e.message}'
             : 'Unknown error: ${e.toString()}';
         debugPrint('Stack trace: $stackTrace');
         emit(StatisticsError(errorMessage: msg));
       }
     }
   }
   ```

---

## **Event Rules**

* All events must extend an **abstract Equatable event**.
* Names must end with `Event`.
* Example:

  ```dart
  sealed class StatisticsEvent extends Equatable {
    const StatisticsEvent();
    @override
    List<Object?> get props => [];
  }

  class SetTimeRangeEvent extends StatisticsEvent {
    final TimeRange timeRange;
    const SetTimeRangeEvent(this.timeRange);
    @override
    List<Object?> get props => [timeRange];
  }
  ```

---

## **Config**

* Use package imports instead of relative imports, apply const constructors to optimize performance, add trailing commas to improve formatting and maintainability, and use const for literal collections to optimize memory + formatter:    trailing_commas: preserve



