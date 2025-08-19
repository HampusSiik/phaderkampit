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
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml /app/
COPY . /app

# Install deps via pip (fallback for simple pyproject)
RUN python -m pip install --upgrade pip && \
    pip install -e .

# Create data volume mount point
VOLUME ["/data/uploads"]

# Expose port
EXPOSE 8000

# Default envs
ENV FLASK_ENV=production \
    UPLOAD_FOLDER=/data/uploads

# Start with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]
