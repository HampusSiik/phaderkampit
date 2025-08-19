import os
from flask import Flask
from .extensions import db

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # python-dotenv not installed, environment variables will be loaded from shell
    pass


def create_app():
    app = Flask(__name__)

    # Basic config
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Use local uploads directory for development, /data/uploads for production
    default_upload_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "uploads"
    )
    app.config["UPLOAD_FOLDER"] = os.environ.get("UPLOAD_FOLDER", default_upload_folder)
    app.config["MAX_CONTENT_LENGTH"] = int(
        os.environ.get("MAX_CONTENT_LENGTH", "104857600")
    )  # 100MB default

    # Ensure upload path exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    with app.app_context():
        from . import models  # noqa: F401

        db.create_all()

    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)

    return app
