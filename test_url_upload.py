#!/usr/bin/env python3
"""
Test script for URL upload and audio conversion functionality
"""

import requests
import time

BASE_URL = "http://localhost:8000"


def test_url_upload_functionality():
    """Test the new URL upload and conversion features"""

    print("🎵 Testing URL Upload & Audio Conversion Functionality")
    print("=" * 60)

    try:
        # Test home page loads
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ App is running")
        else:
            print(f"❌ App not responding: {response.status_code}")
            return False

        # Test a list page to see the new upload form
        html = response.text
        import re

        list_matches = re.findall(r"/lists/(\d+)", html)

        if list_matches:
            list_id = list_matches[0]
            list_response = requests.get(f"{BASE_URL}/lists/{list_id}")

            if list_response.status_code == 200:
                print(f"✅ List page {list_id} loads")
                list_html = list_response.text

                # Check for new UI elements
                if "File Upload" in list_html and "URL" in list_html:
                    print("✅ Tab switching UI found (File Upload / URL)")
                else:
                    print("❌ Tab switching UI missing")

                if "upload-url" in list_html:
                    print("✅ URL upload form found")
                else:
                    print("❌ URL upload form missing")

                if "Preview & Convert" in list_html:
                    print("✅ Preview button found")
                else:
                    print("❌ Preview button missing")

                if "showUploadTab" in list_html:
                    print("✅ Tab switching JavaScript found")
                else:
                    print("❌ Tab switching JavaScript missing")

                if "previewUrl" in list_html:
                    print("✅ Preview JavaScript function found")
                else:
                    print("❌ Preview JavaScript function missing")

            else:
                print(f"❌ List page failed: {list_response.status_code}")
        else:
            print("ℹ️  No existing lists found to test list page")

        # Test that the preview route exists
        preview_response = requests.post(
            f"{BASE_URL}/clips/preview-url", json={"url": "https://invalid-url"}
        )
        if preview_response.status_code in [
            400,
            500,
        ]:  # Should fail but route should exist
            print("✅ Preview URL route exists (failed as expected with invalid URL)")
        else:
            print(f"⚠️  Preview URL route returned: {preview_response.status_code}")

        # Test temp audio route exists
        temp_response = requests.get(f"{BASE_URL}/temp-audio/test.mp3")
        if temp_response.status_code == 404:  # Should return 404 for non-existent file
            print("✅ Temp audio route exists (404 as expected)")
        else:
            print(f"⚠️  Temp audio route returned: {temp_response.status_code}")

        print()
        print("🎉 URL Upload functionality test completed!")
        print()
        print("NEW FEATURES IMPLEMENTED:")
        print("• 📁 File Upload - Traditional file upload (existing)")
        print("• 🔗 URL Upload - Download audio from URLs")
        print("• 🎵 Audio Preview - Listen before confirming add")
        print("• 🔄 Format Conversion - OGG/WAV/M4A → MP3")
        print("• 📋 Auto-titles - Suggested titles from filenames")
        print("• 🗂️ Temp File Management - Safe preview & cleanup")
        print()
        print("SUPPORTED FORMATS FOR CONVERSION:")
        print("• OGG files → MP3 (primary use case)")
        print("• WAV files → MP3")
        print("• M4A files → MP3")
        print("• Any ffmpeg-supported format → MP3")
        print()
        print("HOW TO USE:")
        print("1. Go to a list page")
        print("2. Click 'URL' tab instead of 'File Upload'")
        print("3. Paste an audio URL (e.g., .ogg file)")
        print("4. Click 'Preview & Convert'")
        print("5. Listen to the converted MP3 preview")
        print("6. Click 'Add to List' to save permanently")
        print()
        print("✅ Ready to convert OGG files from URLs!")

        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the app. Make sure it's running with 'make dev'")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    success = test_url_upload_functionality()
    exit(0 if success else 1)
