"""
Simple test runner for word endpoints - RED phase verification.
Runs tests without cleanup to verify they fail as expected.
"""

import sys
sys.path.insert(0, '.')
from tests import test_words as tw

print("\n===== RUNNING WORD ENDPOINT TESTS (RED PHASE) =====\n")

# Set up test folder
print("Setting up test folder...")
tw.test_user_id = tw.get_test_user_id()
print(f"Test user ID: {tw.test_user_id}")

results = []

# Test 1: Create folder for tests
print("\n--- Test 1: Setup ---")
result = tw.test_setup_create_folder()
results.append(("Setup", result))

# Test 2: List words (empty)
print("\n--- Test 2: List words (empty) ---")
result = tw.test_list_words_empty()
results.append(("List empty", result))

# Test 3: Create word
print("\n--- Test 3: Create word ---")
result = tw.test_create_word_success()
results.append(("Create word", result))

# Test 4: List words (with data)
print("\n--- Test 13: List words (with data) ---")
result = tw.test_list_words_with_data()
results.append(("List with data", result))

# Test 5: Get word
print("\n--- Test 17: Get word ---")
result = tw.test_get_word_success()
results.append(("Get word", result))

# Summary
print("\n\n===== TEST SUMMARY =====")
passed = sum(1 for _, r in results if r)
failed = len(results) - passed
print(f"Total: {len(results)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

for name, result in results:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status}: {name}")

print("\nExpected: All tests except 'Setup' should FAIL (endpoints don't exist yet)")
print("This is the RED phase of TDD - tests fail before implementation\n")
