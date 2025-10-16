.PHONY: help install dev run test format lint clean docker-build docker-up docker-down vercel-deploy vercel-build ui-install ui-build ui-dev

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Install dev dependencies"
	@echo "  make run          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Lint code with ruff"
	@echo "  make clean        - Clean cache files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make vercel-deploy - Deploy to Vercel"
	@echo "  make vercel-build - Build for Vercel deployment"
	@echo "  make ui-install   - Install frontend dependencies"
	@echo "  make ui-build     - Build frontend for production"
	@echo "  make ui-dev       - Run frontend development server"

install:
	uv sync

dev:
	uv sync --extra dev

run:
	uv run python run.py

test:
	uv run pytest -v

format:
	uv run black app/ tests/
	uv run ruff check --fix app/ tests/

lint:
	uv run ruff check app/ tests/
	uv run mypy app/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

docker-build:
	docker build -t face-flip-server .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Vercel deployment commands
vercel-deploy:
	@echo "Deploying to Vercel..."
	vercel --prod

vercel-build:
	@echo "Building for Vercel deployment..."
	@echo "Installing backend dependencies..."
	uv sync
	@echo "Installing frontend dependencies..."
	cd ui && npm install
	@echo "Building frontend..."
	cd ui && npm run build
	@echo "Build completed successfully!"

# Frontend commands
ui-install:
	@echo "Installing frontend dependencies..."
	cd ui && npm install

ui-build:
	@echo "Building frontend for production..."
	cd ui && npm run build

ui-dev:
	@echo "Starting frontend development server..."
	cd ui && npm run dev

