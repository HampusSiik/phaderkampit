#!/usr/bin/env python3
"""
Interactive script to generate .env file for phaderkampit Flask application
"""
import os
import secrets
import getpass
from pathlib import Path


def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_urlsafe(32)


def get_input_with_default(prompt, default, is_password=False):
    """Get user input with a default value"""
    if is_password:
        user_input = getpass.getpass(f"{prompt} [{default}]: ").strip()
    else:
        user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default


def get_yes_no(prompt, default=True):
    """Get yes/no input from user"""
    default_str = "Y/n" if default else "y/N"
    user_input = input(f"{prompt} [{default_str}]: ").strip().lower()

    if not user_input:
        return default
    return user_input in ["y", "yes", "true", "1"]


def main():
    print("🚀 Setting up environment for phaderkampit Flask app")
    print("=" * 50)

    # Check if .env already exists
    env_file = Path(".env")
    if env_file.exists():
        overwrite = get_yes_no("⚠️  .env file already exists. Overwrite?", False)
        if not overwrite:
            print("❌ Setup cancelled.")
            return

    print("\n📝 Please provide the following information:")
    print("(Press Enter to use default values)\n")

    # Environment type
    print("🏗️  Environment Setup:")
    is_production = not get_yes_no("Is this a development environment?", True)

    # Flask configuration
    print("\n🔐 Flask Configuration:")
    secret_key = get_input_with_default(
        "Secret key (leave empty to generate a secure one)", generate_secret_key()
    )

    flask_env = "production" if is_production else "development"
    flask_env = get_input_with_default("Flask environment", flask_env)

    # Database configuration
    print("\n🗄️  Database Configuration:")
    print("1. SQLite (recommended for development)")
    print("2. PostgreSQL (recommended for production)")

    db_choice = get_input_with_default("Choose database type (1 or 2)", "1")

    if db_choice == "2":
        print("\n📊 PostgreSQL Configuration:")
        db_host = get_input_with_default("Database host", "localhost")
        db_port = get_input_with_default("Database port", "5432")
        db_name = get_input_with_default("Database name", "phaderkampit")
        db_user = get_input_with_default("Database user", "postgres")
        db_password = get_input_with_default("Database password", "", is_password=True)

        database_url = (
            f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
    else:
        db_file = get_input_with_default("SQLite database file", "app.db")
        database_url = f"sqlite:///{db_file}"

    # Upload configuration
    print("\n📁 File Upload Configuration:")
    if is_production:
        default_upload = "/data/uploads"
    else:
        default_upload = "./uploads"

    upload_folder = get_input_with_default("Upload folder", default_upload)

    # Max file size
    print("\n📊 File Size Limits:")
    max_size_mb = get_input_with_default("Maximum file size in MB", "100")
    max_content_length = str(int(max_size_mb) * 1024 * 1024)

    # Additional settings
    print("\n⚙️  Additional Settings:")
    debug_mode = (
        "true"
        if not is_production and get_yes_no("Enable debug mode?", True)
        else "false"
    )

    # Generate .env content
    env_content = f"""# Environment Variables for phaderkampit Flask App
# Generated on {os.popen('date').read().strip()}

# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV={flask_env}
FLASK_DEBUG={debug_mode}

# Database Configuration
DATABASE_URL={database_url}

# File Upload Configuration
UPLOAD_FOLDER={upload_folder}
MAX_CONTENT_LENGTH={max_content_length}

# Application Settings
"""

    # Write .env file
    try:
        with open(".env", "w") as f:
            f.write(env_content)

        print("\n✅ .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")

        # Create upload directory if it doesn't exist
        if upload_folder.startswith("./"):
            upload_path = Path(upload_folder)
            upload_path.mkdir(exist_ok=True)
            print(f"📁 Created upload directory: {upload_path.absolute()}")

        print("\n🎉 Environment setup complete!")
        print("\n📋 Next steps:")
        print("1. Review the generated .env file")
        print("2. Run 'make dev' to start the application")
        print("3. Visit http://localhost:8000 to test your app")

        if db_choice == "2":
            print("\n🔔 PostgreSQL Note:")
            print(
                "Make sure your PostgreSQL server is running and the database exists."
            )
            print("You can create it with: createdb phaderkampit")

    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
