"""Delete all folders except 'Test Folder' via API."""

import requests
import json
import sys
import io

# Add UTF-8 encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE_URL = "http://localhost:8829"
KEEP_FOLDER_NAME = "Test Folder"


def get_all_folders():
    """Get all folders via API."""
    response = requests.get(f"{BASE_URL}/api/v1/folders")
    response.raise_for_status()
    return response.json()["data"]


def delete_folder(folder_id):
    """Delete a folder via API."""
    response = requests.delete(f"{BASE_URL}/api/v1/folders/{folder_id}")
    return response.status_code == 200


def main():
    print("🗑️  Cleaning up folders via API...\n")

    # Get all folders
    folders = get_all_folders()
    print(f"Found {len(folders)} folders total\n")

    folders_to_delete = []
    folder_to_keep = None

    for folder in folders:
        folder_name = folder["name"]
        folder_id = folder["id"]

        if folder_name == KEEP_FOLDER_NAME:
            folder_to_keep = folder
            print(f"✅ Keeping: {folder_name} (ID: {folder_id})")
        else:
            folders_to_delete.append(folder)
            print(f"🗑️  Will delete: {folder_name} (ID: {folder_id})")

    print(f"\n{'='*60}")
    print(f"Deleting {len(folders_to_delete)} folders...")
    print(f"{'='*60}\n")

    deleted_count = 0
    for folder in folders_to_delete:
        folder_id = folder["id"]
        folder_name = folder["name"]

        try:
            if delete_folder(folder_id):
                print(f"✅ Deleted: {folder_name}")
                deleted_count += 1
            else:
                print(f"❌ Failed to delete: {folder_name}")
        except Exception as e:
            print(f"❌ Error deleting {folder_name}: {e}")

    print(f"\n{'='*60}")
    print(f"✅ Cleanup complete! Deleted {deleted_count}/{len(folders_to_delete)} folders")
    print(f"{'='*60}")

    if folder_to_keep:
        print(f"\n📁 Remaining folder:")
        print(f"   Name: {folder_to_keep['name']}")
        print(f"   ID: {folder_to_keep['id']}")
        print(f"   Description: {folder_to_keep['description']}")
    else:
        print(f"\n⚠️  Warning: '{KEEP_FOLDER_NAME}' was not found!")


if __name__ == "__main__":
    main()
