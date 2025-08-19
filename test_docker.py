#!/usr/bin/env python3
"""
Test script to verify Docker configuration and socket setup.
"""
import os
import subprocess
import time
import socket
import requests


def test_docker_build():
    """Test that Docker image builds successfully."""
    print("🔨 Testing Docker build...")
    try:
        result = subprocess.run(
            ["docker", "build", "-t", "phaderkampit-test", "."],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            print("✅ Docker image builds successfully")
            return True
        else:
            print(f"❌ Docker build failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Docker build timed out")
        return False
    except Exception as e:
        print(f"❌ Docker build error: {e}")
        return False


def test_socket_path():
    """Test that socket path is accessible."""
    socket_path = "/tmp/phaderkampit.sock"
    print(f"🔍 Checking socket path: {socket_path}")

    # Check if directory is writable
    socket_dir = os.path.dirname(socket_path)
    if os.access(socket_dir, os.W_OK):
        print(f"✅ Directory {socket_dir} is writable")
        return True
    else:
        print(f"❌ Directory {socket_dir} is not writable")
        return False


def test_compose_files():
    """Test that docker-compose files are valid."""
    print("📄 Testing docker-compose configurations...")

    # Test base file
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", "docker-compose.yml", "config"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            print("✅ docker-compose.yml is valid")
        else:
            print(f"❌ docker-compose.yml is invalid: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing docker-compose.yml: {e}")
        return False

    # Test combined configurations
    configs = [
        ("Development", ["docker-compose.yml", "docker-compose.dev.yml"]),
        ("Production", ["docker-compose.yml", "docker-compose.prod.yml"]),
    ]

    for config_name, files in configs:
        try:
            cmd = (
                ["docker", "compose"]
                + [item for f in files for item in ["-f", f]]
                + ["config"]
            )
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {config_name} configuration is valid")
            else:
                print(f"❌ {config_name} configuration is invalid: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error testing {config_name} configuration: {e}")
            return False

    return True


def main():
    """Run all Docker tests."""
    print("🐳 Docker Configuration Test Suite")
    print("=" * 50)

    tests = [
        ("Docker Build", test_docker_build),
        ("Socket Path", test_socket_path),
        ("Compose Files", test_compose_files),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        if test_func():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")

    if passed == total:
        print("🎉 All Docker tests passed!")
        print()
        print("🚀 Ready for deployment:")
        print("  Development: make docker-dev")
        print("  Production:  make prod-deploy")
        print("  Socket:      /tmp/phaderkampit.sock")
        return True
    else:
        print("❌ Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
