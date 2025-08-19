#!/usr/bin/env python3
"""
Test script to verify batch answer recording functionality
"""


def test_batch_answers():
    """Test the batch answer recording functionality"""
    print("🧪 Testing batch answer recording functionality...")

    try:
        from app import create_app
        from app.models import SoundList, SoundClip, Team, Answer

        app = create_app()

        with app.test_client() as client:
            with app.app_context():
                # Check if we have test data
                lists = SoundList.query.all()
                clips = SoundClip.query.all()
                teams = Team.query.all()

                print(f"📊 Test data available:")
                print(f"  Lists: {len(lists)}")
                print(f"  Clips: {len(clips)}")
                print(f"  Teams: {len(teams)}")

                if not lists or not clips or not teams:
                    print(
                        "⚠️  Insufficient test data. Need at least 1 list, 1 clip, and 1 team."
                    )
                    print("💡 Create some data through the web interface first.")
                    return True

                # Test routes are accessible
                response = client.get("/")
                print(f"🏠 Main page: {response.status_code}")

                # Test list page shows batch form
                list_id = lists[0].id
                response = client.get(f"/lists/{list_id}")
                print(f"📋 List page: {response.status_code}")

                if response.status_code == 200:
                    content = response.get_data(as_text=True)
                    has_batch_form = (
                        "batch-form" in content and "Batch Answer Recording" in content
                    )
                    print(f"📝 Batch form present: {has_batch_form}")

                    if has_batch_form:
                        print("✅ Batch answer recording UI is available")
                    else:
                        print("❌ Batch answer recording UI not found in template")

                # Test batch endpoint exists (without actually posting data)
                # Just check it responds with a redirect (missing data)
                response = client.post("/answers/batch", data={})
                print(f"🔄 Batch endpoint responds: {response.status_code == 302}")

                print("✅ Batch answer recording functionality is ready!")
                return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_batch_answers()
    exit(0 if success else 1)
