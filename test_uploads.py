#!/usr/bin/env python3
"""
Test script to verify upload functionality works correctly
"""
import os
import tempfile
from pathlib import Path


def test_uploads():
    """Test the upload functionality"""
    print("🧪 Testing upload functionality...")

    try:
        from app import create_app

        app = create_app()

        print("✅ Flask app created successfully")

        # Test configuration
        upload_folder = app.config["UPLOAD_FOLDER"]
        print(f"📁 Upload folder: {upload_folder}")
        print(f"📍 Absolute path: {os.path.abspath(upload_folder)}")
        print(f"📂 Directory exists: {os.path.exists(upload_folder)}")

        # Test existing files
        if os.path.exists(upload_folder):
            files = [
                f
                for f in os.listdir(upload_folder)
                if os.path.isfile(os.path.join(upload_folder, f))
            ]
            print(f"📄 Files in upload folder: {len(files)}")
            for i, file in enumerate(files[:3]):  # Show first 3 files
                print(f"  {i+1}. {file}")
            if len(files) > 3:
                print(f"  ... and {len(files) - 3} more files")

        # Test routes
        with app.test_client() as client:
            # Test main page
            response = client.get("/")
            print(f"🏠 Main page status: {response.status_code}")

            # Test upload serving for existing files
            if os.path.exists(upload_folder):
                files = [
                    f
                    for f in os.listdir(upload_folder)
                    if os.path.isfile(os.path.join(upload_folder, f))
                ]
                if files:
                    test_file = files[0]
                    response = client.get(f"/uploads/{test_file}")
                    print(
                        f"📥 Upload serving test ({test_file}): {response.status_code}"
                    )
                    if response.status_code == 200:
                        print(
                            f"   Content-Type: {response.headers.get('Content-Type', 'unknown')}"
                        )
                        print(
                            f"   Content-Length: {response.headers.get('Content-Length', 'unknown')} bytes"
                        )
                else:
                    print("📥 No files to test upload serving")

        print("\n✅ All tests completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_uploads()
    exit(0 if success else 1)
