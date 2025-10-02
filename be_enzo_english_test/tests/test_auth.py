"""
Test file for authentication endpoints.

Simplified version - no Firebase token required.
Run this file to test all authentication endpoints.

Usage:
    python test_auth.py
"""

import requests
import json
import sys
import io
import os
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding issues
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Load environment variables from tests/.env
test_dir = Path(__file__).parent
load_dotenv(test_dir / ".env")

# Base URL for the test server (from .env)
BASE_URL = os.getenv("BASE_URL")


def print_separator(title=""):
    """Print a nice separator."""
    if title:
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    else:
        print("=" * 80)


def print_result(test_name, passed, message=""):
    """Print test result."""
    status = "✓ PASSED" if passed else "✗ FAILED"
    print(f"{status}: {test_name}")
    if message:
        print(f"  → {message}")


# ==============================================================================
# Test 1: Health Check
# ==============================================================================
def test_health_check():
    """Test the health check endpoint."""
    print_separator("TEST 1: Health Check")

    url = f"{BASE_URL}/api/v1/health"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "healthy", "Status should be 'healthy'"
        assert data["database"] == "connected", "Database should be connected"

        print_result("Health Check", True, "Server is healthy and DB connected")
        return True

    except requests.exceptions.ConnectionError:
        print_result("Health Check", False, "Could not connect to server")
        print("  Make sure the server is running: python main.py")
        return False
    except Exception as e:
        print_result("Health Check", False, str(e))
        return False


# ==============================================================================
# Test 2: Get Current User (No Token Required)
# ==============================================================================
def test_current_user():
    """Test the current user endpoint - no authentication required."""
    print_separator("TEST 2: Get Current User (Hardcoded)")

    url = f"{BASE_URL}/api/v1/auth/current-user"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        data = response.json()
        assert data["success"], "Response should be successful"
        assert "data" in data, "Response should contain data"

        user_data = data["data"]
        assert user_data["email"] == "dinhthongchau@gmail.com", (
            "Email should be dinhthongchau@gmail.com"
        )
        assert "id" in user_data, "User should have an id"
        assert "name" in user_data, "User should have a name"
        assert "created_at" in user_data, "User should have created_at"

        print_result("Get Current User", True)
        print(f"  → User ID: {user_data['id']}")
        print(f"  → Email: {user_data['email']}")
        print(f"  → Name: {user_data['name']}")
        return True

    except requests.exceptions.ConnectionError:
        print_result("Get Current User", False, "Could not connect to server")
        return False
    except AssertionError as e:
        print_result("Get Current User", False, str(e))
        return False
    except Exception as e:
        print_result("Get Current User", False, f"Unexpected error: {str(e)}")
        return False


# ==============================================================================
# Test 3: Check API Documentation
# ==============================================================================
def test_api_docs():
    """Test that API documentation is accessible."""
    print_separator("TEST 3: API Documentation")

    url = f"{BASE_URL}/docs"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert "swagger" in response.text.lower(), "Should contain Swagger UI"

        print_result("API Documentation", True, "Swagger UI is accessible")
        return True

    except Exception as e:
        print_result("API Documentation", False, str(e))
        return False


# ==============================================================================
# Test 4: Check OpenAPI Spec
# ==============================================================================
def test_openapi_spec():
    """Test that OpenAPI specification is accessible."""
    print_separator("TEST 4: OpenAPI Specification")

    url = f"{BASE_URL}/openapi.json"
    print(f"GET {url}")

    try:
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        spec = response.json()
        assert "openapi" in spec, "Should contain OpenAPI version"
        assert "paths" in spec, "Should contain API paths"
        assert "/api/v1/auth/current-user" in spec["paths"], (
            "Should contain auth endpoint"
        )

        print_result("OpenAPI Spec", True, "OpenAPI specification is valid")
        print(f"  → OpenAPI Version: {spec.get('openapi', 'unknown')}")
        print(f"  → API Title: {spec.get('info', {}).get('title', 'unknown')}")
        return True

    except Exception as e:
        print_result("OpenAPI Spec", False, str(e))
        return False


# ==============================================================================
# Test Summary
# ==============================================================================
def print_test_summary(results):
    """Print summary of all tests."""
    print_separator()
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 28 + "TEST SUMMARY" + " " * 38 + "║")
    print("╚" + "=" * 78 + "╝")

    total = len(results)
    passed = sum(results.values())
    failed = total - passed

    print(f"\n  Total Tests: {total}")
    print(f"  ✓ Passed: {passed}")
    print(f"  ✗ Failed: {failed}")

    if failed == 0:
        print("\n  🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"\n  ⚠ {failed} test(s) failed")

    print_separator()
    return failed == 0


# ==============================================================================
# CURL Examples (for manual testing)
# ==============================================================================
def print_curl_examples():
    """Print CURL command examples for manual testing."""
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 26 + "CURL EXAMPLES" + " " * 39 + "║")
    print("╚" + "=" * 78 + "╝")

    print("\n1. Health Check:")
    print(f"   curl -X GET {BASE_URL}/api/v1/health")

    print("\n2. Get Current User:")
    print(f"   curl -X GET {BASE_URL}/api/v1/auth/current-user")

    print("\n3. Open API Documentation in Browser:")
    print(f"   {BASE_URL}/docs")

    print_separator()


# ==============================================================================
# Run All Tests
# ==============================================================================
def run_all_tests():
    """Run all tests and return success status."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "AUTHENTICATION ENDPOINT TESTS" + " " * 28 + "║")
    print("║" + " " * 25 + "(Simplified - No Token)" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")

    results = {}

    # Run all tests
    results["Health Check"] = test_health_check()
    results["Current User"] = test_current_user()
    results["API Documentation"] = test_api_docs()
    results["OpenAPI Spec"] = test_openapi_spec()

    # Print summary
    all_passed = print_test_summary(results)

    # Print CURL examples
    print_curl_examples()

    return all_passed


# ==============================================================================
# Main Entry Point
# ==============================================================================
if __name__ == "__main__":
    try:
        all_passed = run_all_tests()
        sys.exit(0 if all_passed else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ FATAL ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
