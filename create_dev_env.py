#!/usr/bin/env python3
"""
Test script to demonstrate the environment setup with default values
This creates a .env file with sensible defaults for development
"""
import os
import secrets
from pathlib import Path


def create_dev_env():
    """Create a development .env file with good defaults"""

    print("🧪 Creating development .env file with defaults...")

    # Generate secure secret key
    secret_key = secrets.token_urlsafe(32)

    # Development defaults
    env_content = f"""# Environment Variables for phaderkampit Flask App
# Auto-generated development configuration

# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=development
FLASK_DEBUG=true

# Database Configuration (SQLite for development)
DATABASE_URL=sqlite:///app.db

# File Upload Configuration
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=104857600

# Application Settings
"""

    # Write .env file
    try:
        with open(".env", "w") as f:
            f.write(env_content)

        print("✅ Development .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")

        # Create upload directory
        upload_path = Path("./uploads")
        upload_path.mkdir(exist_ok=True)
        print(f"📁 Created upload directory: {upload_path.absolute()}")

        return True

    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


if __name__ == "__main__":
    success = create_dev_env()
    exit(0 if success else 1)
