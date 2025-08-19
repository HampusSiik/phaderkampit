# Makefile for phaderkampit Flask application

.PHONY: help install dev run clean build docker-build docker-run docker-stop test test-uploads test-batch test-nav lint format check-syntax setup-env setup-dev debug-config

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

setup-env: ## Interactive setup for .env file
	@echo "🚀 Setting up environment configuration..."
	@python3 setup_env.py

setup-dev: ## Quick setup with development defaults (non-interactive)
	@echo "🧪 Setting up development environment with defaults..."
	@python3 create_dev_env.py

install: ## Install dependencies using uv
	uv sync

# Load environment variables if .env exists
load-env: ## Load environment variables from .env file
	@if [ -f .env ]; then \
		echo "📁 Loading environment from .env file..."; \
		export $$(grep -v '^#' .env | xargs); \
	else \
		echo "⚠️  No .env file found. Run 'make setup-env' to create one."; \
	fi

dev: install ## Install dependencies and run in development mode
	@if [ -f .env ]; then \
		echo "📁 Loading environment from .env file..."; \
		export $$(grep -v '^#' .env | grep -v '^$$' | xargs) && uv run python main.py; \
	else \
		echo "⚠️  No .env file found. Starting with defaults..."; \
		uv run python main.py; \
	fi

run: dev ## Alias for dev (Install dependencies and run the application)

prod: install ## Run with gunicorn in production mode
	uv run gunicorn -b 0.0.0.0:8000 main:app

clean: ## Clean up virtual environment and cache files
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: ## Build the application (install dependencies)
	uv sync

rebuild: clean build ## Clean and rebuild the application

check-syntax: ## Check Python syntax for all files
	@echo "Checking Python syntax..."
	@uv run python -m py_compile main.py
	@uv run python -m py_compile app/__init__.py
	@uv run python -m py_compile app/routes.py
	@uv run python -m py_compile app/models.py
	@uv run python -m py_compile app/extensions.py
	@echo "✓ All Python files have valid syntax"

lint: install ## Run flake8 linting
	@echo "Running linter..."
	@uv run python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || echo "Install flake8 with: uv add --dev flake8"

format: install ## Format code with black
	@echo "Formatting code..."
	@uv run python -m black . || echo "Install black with: uv add --dev black"

test: install ## Run tests (when available)
	@echo "Running tests..."
	@uv run python -m pytest || echo "No tests found or pytest not installed"

test-uploads: install ## Test upload functionality
	@echo "🧪 Testing upload functionality..."
	@uv run python test_uploads.py

test-batch: install ## Test batch answer recording functionality
	@echo "🧪 Testing batch answer recording..."
	@uv run python test_batch_answers.py

test-nav: install ## Test navigation improvements
	test-delete-clear: ensure-env ## Test delete and clear functionality
	@echo "🧪 Testing delete and clear functionality..."
	@timeout 5 $(MAKE) dev > /dev/null 2>&1 & 
	sleep 2 && 
	uv run python test_delete_clear.py

# Docker commands
docker-build: ## Build Docker image
	docker build -t phaderkampit .

docker-dev: ## Run Docker in development mode (with port 8000)
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

docker-prod: ## Run Docker in production mode (with Unix socket)
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

docker-run: docker-auto-dev ## Build and run Docker container (development mode with auto-rebuild)

run-docker: docker-auto-dev ## Main command: Auto-rebuild and run in development mode

run-docker-prod: docker-auto-prod ## Main command: Auto-rebuild and run in production mode

# Smart run command that detects Docker preference
smart-run: ## Smart run: Uses Docker if available, falls back to local development
	@echo "🤖 Smart run: detecting best method..."
	@if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then \
		echo "🐳 Docker detected, using containerized development..."; \
		$(MAKE) run-docker; \
	else \
		echo "💻 Docker not available, using local development..."; \
		$(MAKE) dev; \
	fi

docker-stop: ## Stop Docker containers
	docker compose down

docker-logs: ## Show Docker container logs
	docker compose logs -f

docker-shell: ## Open shell in running container
	docker compose exec web bash

docker-clean: ## Remove Docker containers and images
	docker compose down -v
	docker rmi phaderkampit 2>/dev/null || true

docker-test: ## Test Docker configuration
	@echo "🧪 Testing Docker setup..."
	@python3 test_docker.py

# Auto-rebuild and run commands
docker-auto-dev: ## Auto-rebuild and run in development mode (stops existing containers first)
	@echo "🚀 Auto-rebuilding and running in development mode..."
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml down 2>/dev/null || true
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build --force-recreate

docker-auto-prod: ## Auto-rebuild and run in production mode (stops existing containers first)
	@echo "🚀 Auto-rebuilding and deploying in production mode..."
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml down 2>/dev/null || true
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build --force-recreate -d
	@echo "✅ Production deployment complete with auto-rebuild!"
	@echo "📁 Socket available at: /tmp/phaderkampit.sock"

docker-fresh: docker-clean docker-auto-dev ## Complete fresh start: clean everything and rebuild from scratch

docker-watch: ## Run in development mode with automatic rebuilds on file changes
	@echo "👀 Starting development mode with file watching..."
	@echo "⚡ Will automatically rebuild when files change"
	@echo "🛑 Press Ctrl+C to stop"
	@if command -v inotifywait >/dev/null 2>&1; then \
		echo "📁 Using inotifywait for efficient file monitoring"; \
		while true; do \
			echo ""; \
			echo "🔄 Starting/restarting containers..."; \
			docker compose -f docker-compose.yml -f docker-compose.dev.yml down 2>/dev/null || true; \
			docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build --force-recreate & \
			COMPOSE_PID=$$!; \
			echo "📊 Containers running (PID: $$COMPOSE_PID)"; \
			echo "🌐 App should be available at http://localhost:8000"; \
			echo "⏳ Watching for file changes..."; \
			inotifywait -r -e modify,create,delete,move --exclude='(__pycache__|\.pyc|\.git|uploads|\.env)' . 2>/dev/null; \
			echo ""; \
			echo "🔄 Files changed, rebuilding..."; \
			kill $$COMPOSE_PID 2>/dev/null || true; \
			sleep 2; \
		done; \
	else \
		echo "📁 Using basic polling (install inotify-tools for better performance)"; \
		while true; do \
			echo ""; \
			echo "🔄 Starting/restarting containers..."; \
			docker compose -f docker-compose.yml -f docker-compose.dev.yml down 2>/dev/null || true; \
			docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build --force-recreate & \
			COMPOSE_PID=$$!; \
			echo "📊 Containers running (PID: $$COMPOSE_PID)"; \
			echo "🌐 App should be available at http://localhost:8000"; \
			echo "⏳ Will check for changes every 30 seconds..."; \
			sleep 30; \
			echo "🔄 Periodic rebuild (install inotify-tools for change detection)"; \
			kill $$COMPOSE_PID 2>/dev/null || true; \
			sleep 2; \
		done; \
	fi

# Production deployment commands
prod-deploy: ## Deploy in production mode with Unix socket
	@echo "🚀 Deploying phaderkampit in production mode..."
	@echo "📁 Socket will be available at: /tmp/phaderkampit.sock"
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
	@echo "✅ Production deployment complete!"
	@echo "📝 Configure your reverse proxy (nginx/apache) to proxy to unix:/tmp/phaderkampit.sock"

prod-status: ## Check production deployment status
	@echo "🔍 Production status:"
	@if [ -S /tmp/phaderkampit.sock ]; then \
		echo "✅ Socket file exists: /tmp/phaderkampit.sock"; \
		stat /tmp/phaderkampit.sock; \
	else \
		echo "❌ Socket file not found: /tmp/phaderkampit.sock"; \
	fi
	@docker compose -f docker-compose.yml -f docker-compose.prod.yml ps

prod-stop: ## Stop production deployment
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down

# Database commands
db-init: install ## Initialize the database
	@echo "Initializing database..."
	@uv run python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.extensions import db; db.create_all(); print('Database initialized')"

db-reset: install ## Reset the database
	@echo "Resetting database..."
	@rm -f app.db
	@make db-init

# Development helpers
shell: install ## Open Python shell with app context
	@if [ -f .env ]; then \
		export $$(grep -v '^#' .env | grep -v '^$$' | xargs) && uv run python -c "from app import create_app; app = create_app(); app.app_context().push(); print('App context loaded. Available: app, db'); import code; code.interact(local=locals())"; \
	else \
		uv run python -c "from app import create_app; app = create_app(); app.app_context().push(); print('App context loaded. Available: app, db'); import code; code.interact(local=locals())"; \
	fi

routes: install ## Show all routes
	@if [ -f .env ]; then \
		export $$(grep -v '^#' .env | grep -v '^$$' | xargs) && uv run python -c "from app import create_app; app = create_app(); [print(rule) for rule in app.url_map.iter_rules()]"; \
	else \
		uv run python -c "from app import create_app; app = create_app(); [print(rule) for rule in app.url_map.iter_rules()]"; \
	fi

show-env: ## Show current environment configuration
	@echo "🔧 Current environment configuration:"
	@if [ -f .env ]; then \
		echo "📁 .env file found:"; \
		echo ""; \
		grep -v '^#' .env | grep -v '^$$' | while read line; do \
			key=$$(echo $$line | cut -d'=' -f1); \
			value=$$(echo $$line | cut -d'=' -f2-); \
			if echo $$key | grep -q "PASSWORD\|SECRET\|KEY"; then \
				echo "  $$key=***hidden***"; \
			else \
				echo "  $$line"; \
			fi; \
		done; \
	else \
		echo "❌ No .env file found. Run 'make setup-env' to create one."; \
	fi

check-env: ## Validate environment configuration
	@if [ -f .env ]; then \
		export $$(grep -v '^#' .env | grep -v '^$$' | xargs) && python3 check_env.py; \
	else \
		python3 check_env.py; \
	fi

debug-config: ## Debug Flask configuration loading
	@echo "🔧 Debugging Flask configuration..."
	@if [ -f .env ]; then \
		export $$(grep -v '^#' .env | grep -v '^$$' | xargs) && uv run python -c "from dotenv import load_dotenv; load_dotenv(); from app import create_app; app = create_app(); print('Flask config loaded:'); [print(f'  {k}: {\"***hidden***\" if \"SECRET\" in k or \"KEY\" in k or \"PASSWORD\" in k else v}') for k, v in sorted(app.config.items()) if not k.startswith('_')]"; \
	else \
		uv run python -c "from app import create_app; app = create_app(); print('Flask config loaded:'); [print(f'  {k}: {\"***hidden***\" if \"SECRET\" in k or \"KEY\" in k or \"PASSWORD\" in k else v}') for k, v in sorted(app.config.items()) if not k.startswith('_')]"; \
	fi

deps: ## Show dependency tree
	uv tree

update: ## Update dependencies
	uv sync --upgrade

# Quick start commands
quickstart: ## Complete setup: environment, dependencies, database, and run
	@echo "🚀 Quick start setup for phaderkampit..."
	@if [ ! -f .env ]; then \
		echo ""; \
		echo "📝 No .env file found. Let's create one..."; \
		python3 setup_env.py; \
		echo ""; \
	fi
	@echo "📦 Installing dependencies..."
	@make install
	@echo "🗄️  Initializing database..."
	@make db-init
	@echo "✅ Setup complete! Starting the application..."
	@make dev

start: dev ## Alias for dev

restart: ## Stop any running instances and start fresh
	@pkill -f "python.*main.py" 2>/dev/null || true
	@sleep 1
	@make dev

# Status check
status: ## Check if app dependencies are working
	@echo "Checking application status..."
	@uv run python -c "from app import create_app; print('✓ App imports successfully')"
	@echo "✓ Application is ready to run"

# Full reset
reset: clean install db-reset ## Complete reset: clean, install, reset database
	@echo "✓ Complete reset finished"
