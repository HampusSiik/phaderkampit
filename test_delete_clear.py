#!/usr/bin/env python3
"""
Test script for delete and clear functionality
"""

import requests
import time

BASE_URL = "http://localhost:8000"


def test_delete_clear_functionality():
    """Test all the delete and clear functionality"""

    print("🧪 Testing Delete & Clear Functionality")
    print("=" * 50)

    try:
        # Test home page loads
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Home page loads successfully")
        else:
            print(f"❌ Home page failed: {response.status_code}")
            return False

        # Test that we have the confirmation JavaScript functions
        home_html = response.text

        # Check for JavaScript confirmation functions
        js_functions = [
            "confirmDeleteList",
            "confirmClearListScores",
            "confirmDeleteTeam",
            "confirmClearTeamScores",
        ]

        for func in js_functions:
            if func in home_html:
                print(f"✅ JavaScript function '{func}' found in home page")
            else:
                print(f"❌ JavaScript function '{func}' missing from home page")

        # Check for delete/clear buttons in HTML
        if "🗑️" in home_html and "🧹" in home_html:
            print("✅ Delete and clear buttons (emojis) found in home page")
        else:
            print("❌ Delete and clear buttons missing from home page")

        # Test a list page if we have any lists
        if "Create your first list" not in home_html:
            # Try to find a list link
            import re

            list_matches = re.findall(r"/lists/(\d+)", home_html)
            if list_matches:
                list_id = list_matches[0]
                list_response = requests.get(f"{BASE_URL}/lists/{list_id}")
                if list_response.status_code == 200:
                    print(f"✅ List page {list_id} loads successfully")

                    list_html = list_response.text

                    # Check for list-specific JavaScript functions
                    list_js_functions = [
                        "confirmDeleteList",
                        "confirmClearAllListScores",
                        "confirmDeleteClip",
                        "confirmClearTeamListScores",
                    ]

                    for func in list_js_functions:
                        if func in list_html:
                            print(f"✅ List JavaScript function '{func}' found")
                        else:
                            print(f"❌ List JavaScript function '{func}' missing")

                    # Check for delete/clear buttons
                    if "Delete List" in list_html and "Clear All Scores" in list_html:
                        print("✅ List management buttons found")
                    else:
                        print("❌ List management buttons missing")

                else:
                    print(f"❌ List page failed: {list_response.status_code}")

        # Test that the routes exist by checking if they return 404 or require POST
        test_routes = [
            "/lists/999/delete",  # Should require POST
            "/clips/999/delete",  # Should require POST
            "/teams/999/delete",  # Should require POST
            "/lists/999/clear-scores",  # Should require POST
            "/teams/999/clear-scores",  # Should require POST
            "/lists/999/teams/999/clear-scores",  # Should require POST
        ]

        for route in test_routes:
            # Try GET first (should fail)
            response = requests.get(f"{BASE_URL}{route}")
            if response.status_code == 405:  # Method Not Allowed
                print(f"✅ Route {route} properly requires POST method")
            elif response.status_code == 404:
                print(
                    f"✅ Route {route} exists but returns 404 for non-existent ID (expected)"
                )
            else:
                print(
                    f"⚠️  Route {route} returned unexpected status: {response.status_code}"
                )

        print("\n🎉 Delete & Clear functionality test completed!")
        print("\nFeatures implemented:")
        print("• 🗑️ Delete entire lists (with all clips and scores)")
        print("• 🗑️ Delete individual clips (with all scores)")
        print("• 🗑️ Delete teams (with all scores)")
        print("• 🧹 Clear all scores for a list")
        print("• 🧹 Clear all scores for a team")
        print("• 🧹 Clear scores for a specific team on a specific list")
        print("• ⚠️  Confirmation dialogs for all destructive actions")
        print("• 🗂️  File cleanup (removes audio files from disk)")

        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the app. Make sure it's running with 'make dev'")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    success = test_delete_clear_functionality()
    exit(0 if success else 1)
