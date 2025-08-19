# Phaderkampit

Minimal Flask app to upload audio clips, organize them into lists, and record team answers (correct/wrong) for a quiz workflow. Files are stored in a Docker volume; Postgres stores metadata.

## Features

- **Create lists** of sound clips organized by category/topic
- **Upload audio** files (mp3, wav, ogg, m4a, flac) with titles/descriptions
- **Play audio** directly in browser with HTML5 controls
- **Create teams** for competition/quiz scenarios
- **Batch answer recording** - efficiently score multiple clips for a team at once
- **Scoreboard tracking** - see correct answers per team
- **Notes support** - add comments/details for each answer
- **Dockerized deployment** with Postgres and persistent file storage

## Quick start

### Prerequisites

- Python 3.13+ with [uv](https://docs.astral.sh/uv/) package manager
- Or Docker and Docker Compose for containerized deployment

### Option 1: Local Development (Recommended for development)

**Super Quick Start:**

```bash
make quickstart
```

This will interactively set up your environment, install dependencies, initialize the database, and start the app.

**Manual Setup:**

```bash
# 1. Set up environment (interactive)
make setup-env

# 2. Install dependencies and run
make dev
```

**Quick Development Setup (non-interactive):**

```bash
# Create .env with sensible defaults
make setup-dev

# Install and run
make dev
```

### Option 2: Docker Deployment

Run the containerized stack:

```bash
# Using Docker Compose
make docker-run

# Or manually
docker compose up --build
```

### Available Commands

Run `make help` to see all available commands:

```bash
# Environment setup
make setup-env      # Interactive environment configuration
make setup-dev      # Quick dev setup with defaults
make show-env       # Show current environment settings

# Development
make dev            # Run in development mode
make prod           # Run with gunicorn (production)
make quickstart     # Complete setup and run

# Database
make db-init        # Initialize database
make db-reset       # Reset database

# Docker
make docker-run     # Build and run with Docker
make docker-stop    # Stop containers

# Utilities
make status         # Check if app is working
make clean          # Clean virtual environment
make reset          # Complete reset
```

Open http://localhost:8000

## Configuration

The application uses environment variables for configuration. You can set these up using:

- `make setup-env` - Interactive setup with prompts and good defaults
- `make setup-dev` - Quick setup with development defaults
- Copy `.env.example` to `.env` and edit manually

### Environment Variables

| Variable             | Description                   | Default             | Example                          |
| -------------------- | ----------------------------- | ------------------- | -------------------------------- |
| `SECRET_KEY`         | Flask secret key for sessions | Auto-generated      | `your-secret-key-here`           |
| `FLASK_ENV`          | Flask environment             | `development`       | `production`                     |
| `FLASK_DEBUG`        | Enable debug mode             | `true`              | `false`                          |
| `DATABASE_URL`       | Database connection string    | `sqlite:///app.db`  | `postgresql://user:pass@host/db` |
| `UPLOAD_FOLDER`      | Directory for uploaded files  | `./uploads`         | `/data/uploads`                  |
| `MAX_CONTENT_LENGTH` | Max upload size in bytes      | `104857600` (100MB) | `52428800` (50MB)                |

### Database Options

**SQLite (Default for Development):**

```
DATABASE_URL=sqlite:///app.db
```

**PostgreSQL (Recommended for Production):**

```
DATABASE_URL=postgresql://username:password@localhost:5432/phaderkampit
```

## Development Features

- Hot reload in development mode
- SQLite database for quick setup
- Local file uploads to `./uploads/` directory
- Automatic database initialization
- Environment variable validation

## Dev notes

- App entrypoint: `main:app` using factory in `app/__init__.py`
- DB models in `app/models.py`
- Routes and simple HTML in `app/routes.py` and `app/templates/`

This is a foundation. Next steps could include authentication, clip ordering, pagination, results views and exports, and API endpoints.
