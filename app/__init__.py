import os
from flask import Flask
from .extensions import db


def create_app():
    app = Flask(__name__)

    # Basic config
    app.config.setdefault("SECRET_KEY", os.environ.get("SECRET_KEY", "dev-secret"))
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", os.environ.get("DATABASE_URL", "sqlite:///app.db"))
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.config.setdefault("UPLOAD_FOLDER", os.environ.get("UPLOAD_FOLDER", "/data/uploads"))
    app.config.setdefault("MAX_CONTENT_LENGTH", 100 * 1024 * 1024)  # 100MB

    # Ensure upload path exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
