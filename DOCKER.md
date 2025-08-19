# Docker Deployment Guide for Phaderkampit

## Quick Start

### Development Mode

```bash
# Run with port 8000 exposed
make docker-dev
```

### Production Mode (Unix Socket)

```bash
# Run with Unix socket at /tmp/phaderkampit.sock
make prod-deploy
```

## Configuration

### Environment Variables

Create a `.env` file or set these environment variables:

```
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql+psycopg2://user:pass@host:port/dbname
UPLOAD_FOLDER=/data/uploads
```

### Production Deployment

1. **Start the application:**

   ```bash
   make prod-deploy
   ```

2. **Check status:**

   ```bash
   make prod-status
   ```

3. **Configure reverse proxy** (nginx example):
   ```bash
   sudo cp nginx.conf.example /etc/nginx/sites-available/phaderkampit
   sudo ln -s /etc/nginx/sites-available/phaderkampit /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Docker Commands

| Command             | Description                        |
| ------------------- | ---------------------------------- |
| `make docker-dev`   | Development mode with port 8000    |
| `make prod-deploy`  | Production mode with Unix socket   |
| `make prod-status`  | Check production deployment status |
| `make prod-stop`    | Stop production deployment         |
| `make docker-logs`  | View container logs                |
| `make docker-shell` | Open shell in container            |
| `make docker-clean` | Clean up containers and images     |

### Features Included

- **Audio Processing**: FFmpeg for OGG/WAV/M4A to MP3 conversion
- **Unix Socket**: Production ready with `/tmp/phaderkampit.sock`
- **Database**: PostgreSQL with health checks
- **File Uploads**: Persistent volume for audio files
- **Gunicorn**: Production WSGI server with 4 workers
- **Health Checks**: PostgreSQL connection monitoring

### Socket File

The Unix socket will be created at `/tmp/phaderkampit.sock` with proper permissions for web server access.

Configure your reverse proxy (nginx/apache) to proxy requests to:

```
unix:/tmp/phaderkampit.sock
```

### Troubleshooting

1. **Socket not found:**

   ```bash
   make prod-status  # Check if container is running
   make docker-logs  # Check container logs
   ```

2. **Permission issues:**

   ```bash
   ls -la /tmp/phaderkampit.sock  # Check socket permissions
   ```

3. **Audio conversion issues:**
   ```bash
   make docker-shell
   ffmpeg -version  # Check FFmpeg installation
   ```
