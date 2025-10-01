# Task 1.2 Testing Guide - Firebase Authentication

## ✅ What's Been Implemented

### 1. Authentication Router (`routers/auth_router.py`)
- **Endpoint**: `GET /api/v1/auth/current-user`
- **Authentication**: Requires Firebase ID token in `Authorization: Bearer <token>` header
- **Access Control**: Only allows `dinhthongchau@gmail.com` (hardcoded)
- **Response**: Returns user information including id, email, name, created_at, firebase_uid

### 2. Files Created
- `routers/auth_router.py` - Authentication endpoints
- `tests/test_auth.py` - Automated test suite
- `tests/README.md` - Testing documentation

### 3. Integration
- Auth router registered in `main.py`
- Uses Firebase authentication from `dependencies.py`
- Full error handling for invalid/expired tokens

---

## 🧪 Testing Instructions

### Method 1: Using Swagger UI (Easiest)

1. **Open Swagger UI**: http://localhost:8899/docs

2. **Get a Firebase ID Token**:
   - Sign in to your Firebase project with `dinhthongchau@gmail.com`
   - Or use the Firebase REST API (see below)

3. **Authorize in Swagger**:
   - Click the "Authorize" button (🔒 lock icon)
   - Enter: `Bearer YOUR_FIREBASE_ID_TOKEN`
   - Click "Authorize"

4. **Test the Endpoint**:
   - Find `GET /api/v1/auth/current-user` under "Authentication"
   - Click "Try it out"
   - Click "Execute"

5. **Expected Success Response**:
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "id": "...",
    "email": "dinhthongchau@gmail.com",
    "name": "...",
    "created_at": "2025-10-01T...",
    "firebase_uid": "..."
  },
  "timestamp": "2025-10-01T..."
}
```

---

### Method 2: Using CURL

#### Test 1: Without Token (Should Fail)
```bash
curl -X GET http://localhost:8899/api/v1/auth/current-user
```

**Expected Response**:
```json
{"detail":"Not authenticated"}
```

#### Test 2: With Invalid Token (Should Fail)
```bash
curl -X GET http://localhost:8899/api/v1/auth/current-user \
  -H "Authorization: Bearer invalid_token"
```

**Expected Response**:
```json
{
  "detail": {
    "message": "Invalid authentication token",
    "code": "INVALID_ID_TOKEN",
    "error": "The provided Firebase ID token is invalid"
  }
}
```

#### Test 3: With Valid Token (Should Succeed)
```bash
# Replace YOUR_FIREBASE_ID_TOKEN with actual token
curl -X GET http://localhost:8899/api/v1/auth/current-user \
  -H "Authorization: Bearer YOUR_FIREBASE_ID_TOKEN"
```

---

### Method 3: Using Python Test Script

```bash
cd be_enzo_english_test/tests
pip install requests  # If not already installed
python test_auth.py
```

**Note**: Edit `test_auth.py` and replace `YOUR_FIREBASE_ID_TOKEN_HERE` with your actual token first.

---

## 🔑 How to Get Firebase ID Token

### Option A: Firebase REST API
```bash
curl -X POST 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=YOUR_FIREBASE_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "dinhthongchau@gmail.com",
    "password": "YOUR_PASSWORD",
    "returnSecureToken": true
  }'
```

The response contains `idToken` which is your Firebase ID token.

**To find your Firebase API Key**:
1. Go to https://console.firebase.google.com
2. Select your project (fir-enzo-english)
3. Go to Project Settings (⚙️) → General
4. Scroll down to "Web API Key"

### Option B: Using Firebase Auth Emulator (Development)
If you have the emulator running:
```bash
curl -X POST 'http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=test' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "dinhthongchau@gmail.com",
    "password": "test123",
    "returnSecureToken": true
  }'
```

### Option C: From Flutter App
If you have the Flutter app:
```dart
final user = FirebaseAuth.instance.currentUser;
final token = await user?.getIdToken();
print('Token: $token');
```

---

## 📊 Test Results Verification

### ✅ Successful Test Checklist

- [ ] Server starts successfully on port 8899
- [ ] Health check endpoint works: `http://localhost:8899/api/v1/health`
- [ ] Swagger UI loads: `http://localhost:8899/docs`
- [ ] Auth endpoint appears in Swagger under "Authentication" tag
- [ ] Request without token returns `{"detail":"Not authenticated"}`
- [ ] Request with invalid token returns 401 error
- [ ] Request with valid Firebase token for `dinhthongchau@gmail.com` returns user data
- [ ] Request with valid token for other email returns 403 Forbidden

---

## 🐛 Troubleshooting

### Issue: "Not authenticated" even with token
**Solution**: Make sure you're including `Bearer ` prefix:
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI...
```

### Issue: "Invalid ID token"
**Causes**:
- Token has expired (tokens expire after 1 hour)
- Token format is incorrect
- Wrong Firebase project

**Solution**: Get a fresh token

### Issue: "Access denied" / "Forbidden user"
**Cause**: Email is not `dinhthongchau@gmail.com`

**Solution**: Sign in with the correct account

### Issue: Server not responding
**Solution**: Make sure server is running:
```bash
cd be_enzo_english_test
python main.py
# Should see: Uvicorn running on http://0.0.0.0:8899
```

---

## 📝 Task 1.2 Completion Checklist

- [x] Add `firebase-admin` package to requirements.txt (already included)
- [x] Firebase Admin SDK initialized in `dependencies.py`
- [x] Firebase service account JSON in `assets/firebase-adminsdk.json`
- [x] Authentication middleware (`verify_firebase_token`) in `dependencies.py`
- [x] Create `/api/v1/auth/current-user` endpoint
  - [x] Accepts Firebase ID token in Authorization header
  - [x] Verifies token with Firebase Admin SDK
  - [x] Returns user object with all required fields
  - [x] Only allows `dinhthongchau@gmail.com`
- [x] Create test file `tests/test_auth.py`
- [ ] **PENDING**: Test with valid Firebase token ← **YOU ARE HERE**

---

## 🎯 Next Steps

After confirming the authentication endpoint works:
1. Mark Task 1.2 as complete
2. Proceed to Task 1.3: Implement User Folder Endpoints

---

## 📚 API Documentation

Full API documentation available at:
- **Swagger UI**: http://localhost:8899/docs
- **ReDoc**: http://localhost:8899/redoc
- **OpenAPI JSON**: http://localhost:8899/openapi.json
