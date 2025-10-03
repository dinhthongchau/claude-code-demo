# 🚀 Enzo English Test Project - Full-Stack Learning Demo

A comprehensive full-stack application demonstrating modern software development practices with **FastAPI (Python)** backend and **Flutter (Dart)** frontend. This project serves as an excellent learning resource for understanding clean architecture, test-driven development, and API integration.

## 📋 Project Overview

This is a vocabulary management application that allows users to organize words into folders. It demonstrates:

- **Backend**: RESTful API with FastAPI, MongoDB, and Firebase Authentication
- **Frontend**: Flutter mobile app with Clean Architecture and BLoC pattern
- **Testing**: Comprehensive test suites for both backend and frontend
- **DevOps**: Environment configuration, dependency injection, and error handling

## 🏗️ Architecture

### Backend Architecture (FastAPI + Python)
```
be_enzo_english_test/
├── main.py                 # FastAPI application entry point
├── dependencies.py         # Database & Firebase dependencies
├── models/                 # Pydantic models for request/response
│   ├── user_folder.py     # Folder CRUD models
│   ├── word.py            # Word CRUD models
│   └── simplified_word.py # Simplified word models
├── routers/               # API route handlers
│   ├── auth_router.py     # Authentication endpoints
│   ├── folders_router.py  # Folder CRUD operations
│   ├── words_router.py    # Word CRUD operations
│   └── wordlists_router.py # WordList management
└── tests/                 # Comprehensive API tests
    ├── test_auth.py       # Authentication tests
    ├── test_folders.py    # Folder CRUD tests
    └── test_words.py      # Word CRUD tests
```

### Frontend Architecture (Flutter + Clean Architecture)
```
flutter_enzo_english_test/lib/
├── main.dart              # Application entry point
├── core/                  # Core utilities and configuration
│   ├── api/              # API configuration
│   ├── constants/        # App constants
│   ├── errors/           # Error handling
│   ├── get_it/           # Dependency injection
│   ├── network/          # HTTP client setup
│   └── theme/            # App theming
├── data/                  # Data layer (Clean Architecture)
│   ├── models/           # Data models with JSON serialization
│   ├── repository/       # Repository implementations
│   └── source/           # Remote data sources
├── domain/                # Domain layer (Business Logic)
│   ├── entity/           # Business entities
│   ├── repository/       # Repository interfaces
│   └── use_case/         # Business use cases
└── presentation/          # Presentation layer (UI)
    ├── blocs/            # State management with BLoC
    ├── screens/          # UI screens
    └── widgets/          # Reusable UI components
```

## 🛠️ Technologies Used

### Backend Stack
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database with Motor async driver
- **Firebase Admin**: Authentication and user management
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for production deployment

### Frontend Stack
- **Flutter**: Cross-platform mobile framework
- **BLoC Pattern**: State management with flutter_bloc
- **Clean Architecture**: Separation of concerns with layers
- **Dio**: HTTP client for API communication
- **Get It**: Dependency injection container
- **Equatable**: Value equality for entities

### Development Tools
- **Python Virtual Environment**: Isolated Python dependencies
- **Environment Variables**: Configuration management
- **Comprehensive Testing**: Unit and integration tests
- **Code Quality**: Linting and formatting tools

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Flutter SDK 3.0+
- MongoDB Atlas account
- Firebase project

### Backend Setup

1. **Navigate to backend directory**
```bash
cd be_enzo_english_test
```

2. **Create virtual environment**
```bash
# Windows
python -m venv myenv
.\myenv\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv myenv
source myenv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your MongoDB and Firebase credentials
```

5. **Add Firebase credentials**
```bash
# Place your firebase-adminsdk.json in assets/ directory
mkdir assets
# Copy your Firebase service account key to assets/firebase-adminsdk.json
```

6. **Run the server**
```bash
python main.py
# Server starts at http://localhost:8829
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd flutter_enzo_english_test
```

2. **Install Flutter dependencies**
```bash
flutter pub get
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API base URL
```

4. **Run the app**
```bash
flutter run
```

## 🧪 Testing

### Backend Tests
The backend includes comprehensive API tests that verify all endpoints:

```bash
cd be_enzo_english_test
# Activate virtual environment first
.\myenv\Scripts\Activate.ps1

# Run authentication tests
python tests/test_auth.py

# Run folder CRUD tests  
python tests/test_folders.py

# Run word CRUD tests
python tests/test_words.py
```

**Backend Test Results:**
![Backend Test Results]
https://github.com/dinhthongchau/claude-code-demo/blob/main/backend_test_results.md
*All 16 backend API tests passed, covering authentication, folder CRUD operations, and comprehensive error handling.*

### Frontend Tests
The Flutter app uses comprehensive unit and widget tests:

```bash
cd flutter_enzo_english_test
flutter test
```

**Frontend Test Results:**
![Frontend Test Results](frontend_test_results.png)
https://github.com/dinhthongchau/claude-code-demo/blob/main/frontend_test_results.md
*All 71 Flutter tests passed, covering data models, repositories, use cases, BLoC state management, and UI widgets.*

## 📊 Test Coverage

### Backend API Tests (16 Tests)
- ✅ **Authentication**: Health check, user retrieval, API documentation
- ✅ **Folder CRUD**: Create, read, update, delete operations
- ✅ **Validation**: Input validation and error handling
- ✅ **Error Cases**: 404 not found, 400 bad request handling

### Frontend Tests (71 Tests)
- ✅ **Data Layer**: Model serialization, repository implementations
- ✅ **Domain Layer**: Use case business logic, entity validation
- ✅ **Presentation Layer**: BLoC state management, event handling
- ✅ **UI Layer**: Widget rendering, user interaction testing

## 🔧 API Endpoints

### Authentication
- `GET /api/v1/health` - Health check
- `GET /api/v1/auth/current-user` - Get current user info

### Folders
- `GET /api/v1/folders` - List all folders
- `GET /api/v1/folders/{id}` - Get single folder
- `POST /api/v1/folders` - Create new folder
- `PUT /api/v1/folders/{id}` - Update folder
- `DELETE /api/v1/folders/{id}` - Delete folder

### Words
- `GET /api/v1/folders/{folder_id}/words` - Get words in folder
- `GET /api/v1/words/{id}` - Get single word
- `POST /api/v1/words` - Create new word
- `PUT /api/v1/words/{id}` - Update word
- `DELETE /api/v1/words/{id}` - Delete word

## 🎯 Learning Objectives

This project demonstrates:

1. **Clean Architecture**: Proper separation of concerns across layers
2. **Test-Driven Development**: Comprehensive test coverage for reliability
3. **API Design**: RESTful API principles with proper HTTP status codes
4. **State Management**: BLoC pattern for predictable state changes
5. **Error Handling**: Graceful error handling across all layers
6. **Dependency Injection**: Loose coupling and testable code
7. **Environment Configuration**: Secure configuration management
8. **Modern Development**: Current best practices and tools

## 🔍 Key Features Demonstrated

### Backend Features
- **Async/Await**: Non-blocking database operations
- **Data Validation**: Pydantic models with validation rules
- **Error Handling**: Custom exception handling with proper HTTP codes
- **CORS Configuration**: Cross-origin resource sharing setup
- **Environment Variables**: Secure configuration management
- **Logging**: Structured logging for debugging and monitoring

### Frontend Features
- **Clean Architecture**: Domain-driven design principles
- **State Management**: BLoC pattern with event-driven architecture
- **Dependency Injection**: Service locator pattern with GetIt
- **Error Handling**: User-friendly error messages and states
- **Responsive UI**: Material Design with custom theming
- **Testing**: Comprehensive unit and widget tests

## 📚 Learning Resources

### For Backend Development
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Models](https://pydantic-docs.helpmanual.io/)
- [MongoDB with Motor](https://motor.readthedocs.io/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)

### For Frontend Development
- [Flutter Documentation](https://docs.flutter.dev/)
- [BLoC Pattern Guide](https://bloclibrary.dev/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Dependency Injection in Flutter](https://pub.dev/packages/get_it)

## 🤝 Contributing

This project follows Test-Driven Development (TDD):

1. **Write Tests First**: Define expected behavior with failing tests
2. **Implement Code**: Write minimal code to make tests pass
3. **Refactor**: Improve code quality while keeping tests green
4. **Commit**: Separate commits for tests and implementation

## 📄 License

This project is created for educational purposes and learning with Claude AI. Feel free to use it as a reference for your own projects.

## 🎉 Conclusion

This project showcases modern full-stack development with comprehensive testing, clean architecture, and industry best practices. It serves as an excellent foundation for learning both backend API development with Python/FastAPI and frontend mobile development with Flutter.

The 100% test pass rate demonstrates the reliability and maintainability of the codebase, making it an ideal reference for developers learning these technologies.
