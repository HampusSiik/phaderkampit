# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml /app/
COPY . /app

# Install deps via pip (fallback for simple pyproject)
RUN python -m pip install --upgrade pip && \
    pip install -e .

# Create data volume mount point and socket directory
VOLUME ["/data/uploads"]
RUN mkdir -p /tmp && chmod 755 /tmp

# Expose port (for development, but production uses socket)
EXPOSE 8000

# Default envs
ENV FLASK_ENV=production \
    UPLOAD_FOLDER=/data/uploads

# Start with gunicorn using Unix socket
CMD ["gunicorn", "--bind", "unix:/tmp/phaderkampit.sock", "--workers", "4", "--worker-class", "sync", "--timeout", "120", "main:app"]
