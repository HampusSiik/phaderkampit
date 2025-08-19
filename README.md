# Phaderkampit

Minimal Flask app to upload audio clips, organize them into lists, and record team answers (correct/wrong) for a quiz workflow. Files are stored in a Docker volume; Postgres stores metadata.

## Features

- Create lists of sound clips
- Upload audio (mp3, wav, ogg, m4a, flac) with title/description
- Play audio in browser
- Create teams and record per-clip answer results (correct/wrong) with optional notes
- Dockerized with Postgres and a volume for uploads

## Quick start

Prereqs: Docker and Docker Compose.

Run the stack:

```bash
docker compose up --build
```

Open http://localhost:8000

## Config

- DATABASE_URL (default in compose to Postgres service)
- SECRET_KEY (default dev-secret)
- UPLOAD_FOLDER (/data/uploads mapped to Docker volume)

## Dev notes

- App entrypoint: `main:app` using factory in `app/__init__.py`
- DB models in `app/models.py`
- Routes and simple HTML in `app/routes.py` and `app/templates/`

This is a foundation. Next steps could include authentication, clip ordering, pagination, results views and exports, and API endpoints.
