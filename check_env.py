#!/usr/bin/env python3
"""
Environment validation script for phaderkampit
Checks if all required environment variables are set correctly
"""
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def check_env():
    """Check environment configuration"""
    print("🔍 Checking environment configuration...")
    errors = []
    warnings = []

    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
    else:
        warnings.append("No .env file found - using system environment variables")

    # Required variables
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        errors.append("SECRET_KEY not set")
    elif secret_key == "dev-secret":
        warnings.append("Using default SECRET_KEY - consider generating a secure one")
    else:
        print("✅ SECRET_KEY is set")

    # Database URL
    database_url = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    print(f"✅ DATABASE_URL: {database_url}")

    # Upload folder
    upload_folder = os.environ.get("UPLOAD_FOLDER")
    if upload_folder:
        upload_path = Path(upload_folder)
        try:
            upload_path.mkdir(parents=True, exist_ok=True)
            if upload_path.is_dir():
                print(f"✅ UPLOAD_FOLDER: {upload_folder} (accessible)")
            else:
                errors.append(
                    f"UPLOAD_FOLDER path exists but is not a directory: {upload_folder}"
                )
        except PermissionError:
            errors.append(f"Cannot create/access UPLOAD_FOLDER: {upload_folder}")
    else:
        warnings.append("UPLOAD_FOLDER not set - using default")

    # Flask environment
    flask_env = os.environ.get("FLASK_ENV", "production")
    print(f"✅ FLASK_ENV: {flask_env}")

    # Max content length
    max_content = os.environ.get("MAX_CONTENT_LENGTH", "104857600")
    try:
        max_size_mb = int(max_content) / (1024 * 1024)
        print(f"✅ MAX_CONTENT_LENGTH: {max_size_mb:.0f}MB")
    except ValueError:
        errors.append(f"Invalid MAX_CONTENT_LENGTH value: {max_content}")

    # Summary
    print("\n" + "=" * 50)
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")

    if warnings:
        print("⚠️  Configuration Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if not errors and not warnings:
        print("✅ All configuration looks good!")
    elif not errors:
        print("✅ Configuration is functional with some warnings")

    print("\n💡 Recommendations:")
    if not env_file.exists():
        print("  - Run 'make setup-env' or 'make setup-dev' to create .env file")
    if secret_key == "dev-secret":
        print("  - Generate a secure SECRET_KEY for production")
    if database_url.startswith("sqlite:") and flask_env == "production":
        print("  - Consider using PostgreSQL for production")

    return len(errors) == 0


if __name__ == "__main__":
    success = check_env()
    sys.exit(0 if success else 1)
