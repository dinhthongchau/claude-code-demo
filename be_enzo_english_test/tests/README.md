# Testing Guide

## Running Authentication Tests

### Prerequisites
1. Make sure the test server is running on port 8899:
   ```bash
   cd be_enzo_english_test
   python main.py
   ```

2. Install the `requests` library if not already installed:
   ```bash
   pip install requests
   ```

### Running the Tests

```bash
cd tests
python test_auth.py
```

### Getting a Firebase ID Token

To test the authenticated endpoints, you need a valid Firebase ID token:

#### Option 1: Using Firebase Console (Web)
1. Go to https://console.firebase.google.com
2. Open your project (fir-enzo-english)
3. Go to Authentication → Users
4. Sign in as dinhthongchau@gmail.com

#### Option 2: Using Firebase REST API
```bash
curl -X POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=YOUR_API_KEY \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "dinhthongchau@gmail.com",
    "password": "your_password",
    "returnSecureToken": true
  }'
```

The response will include `idToken` which you can use for testing.

#### Option 3: Using Flutter App
If you have the Flutter app running:
1. Sign in with dinhthongchau@gmail.com
2. Get the token from FirebaseAuth instance:
   ```dart
   final token = await FirebaseAuth.instance.currentUser?.getIdToken();
   print(token);
   ```

### Using the Token

Once you have a Firebase ID token, edit `test_auth.py` and replace:
```python
FIREBASE_ID_TOKEN = "YOUR_FIREBASE_ID_TOKEN_HERE"
```

With your actual token:
```python
FIREBASE_ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ij..."
```

Then run the tests again.

## Manual Testing with CURL

### 1. Health Check (No Auth Required)
```bash
curl http://localhost:8899/api/v1/health
```

### 2. Get Current User (With Token)
```bash
curl -X GET http://localhost:8899/api/v1/auth/current-user \
  -H "Authorization: Bearer YOUR_FIREBASE_ID_TOKEN"
```

### 3. Expected Responses

#### Success Response:
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "id": "6523abc...",
    "email": "dinhthongchau@gmail.com",
    "name": "Dinh Thong Chau",
    "created_at": "2025-10-01T10:30:00.000Z",
    "firebase_uid": "abc123..."
  },
  "code": null,
  "error_code": null,
  "error_message": null,
  "timestamp": "2025-10-01T10:35:00.000Z"
}
```

#### Error Response (No Token):
```json
{
  "detail": "Not authenticated"
}
```

#### Error Response (Invalid Token):
```json
{
  "success": false,
  "message": "Invalid authentication token",
  "code": "INVALID_ID_TOKEN",
  "error_code": 401,
  "error_message": "The provided Firebase ID token is invalid"
}
```

## Testing with Swagger UI

The easiest way to test is using the interactive API documentation:

1. Open http://localhost:8899/docs in your browser
2. Click on the "Authorize" button (lock icon)
3. Enter your Firebase ID token in the format: `Bearer YOUR_TOKEN`
4. Click "Authorize"
5. Try the `/api/v1/auth/current-user` endpoint

## Troubleshooting

### "Connection refused" error
- Make sure the server is running on port 8899
- Run: `python main.py` from the `be_enzo_english_test` directory

### "Invalid token" error
- Your Firebase ID token may have expired (tokens expire after 1 hour)
- Get a fresh token using one of the methods above

### "Forbidden user" error
- The endpoint only allows `dinhthongchau@gmail.com`
- Make sure you're signed in with the correct email
