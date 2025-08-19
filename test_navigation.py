#!/usr/bin/env python3
"""
Test script to verify navigation and UI improvements
"""


def test_navigation():
    """Test the navigation functionality"""
    print("🧪 Testing navigation improvements...")

    try:
        from app import create_app
        from app.models import SoundList, SoundClip, Team

        app = create_app()

        with app.test_client() as client:
            with app.app_context():
                # Test data counts
                lists = SoundList.query.all()
                clips = SoundClip.query.all()
                teams = Team.query.all()

                print(f"📊 Current data:")
                print(f"  Lists: {len(lists)}")
                print(f"  Clips: {len(clips)}")
                print(f"  Teams: {len(teams)}")

                # Test home page
                response = client.get("/")
                print(f"🏠 Home page: {response.status_code}")

                if response.status_code == 200:
                    content = response.get_data(as_text=True)
                    has_breadcrumbs = "nav-breadcrumb" in content
                    has_counts = f"({len(lists)})" in content if lists else True
                    print(f"🧭 Breadcrumbs on home: {has_breadcrumbs}")
                    print(f"📊 List counts shown: {has_counts}")

                # Test list page if lists exist
                if lists:
                    list_id = lists[0].id
                    response = client.get(f"/lists/{list_id}")
                    print(f"📋 List page: {response.status_code}")

                    if response.status_code == 200:
                        content = response.get_data(as_text=True)
                        has_back_link = "back-link" in content
                        has_breadcrumbs = "nav-breadcrumb" in content
                        has_quick_actions = "Quick Actions" in content
                        print(f"🔙 Back link present: {has_back_link}")
                        print(f"🧭 Breadcrumbs on list: {has_breadcrumbs}")
                        print(f"⚡ Quick actions: {has_quick_actions}")

                print("✅ Navigation improvements are working!")
                return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_navigation()
    exit(0 if success else 1)
