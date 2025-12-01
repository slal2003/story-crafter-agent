.PHONY: install dev test deploy clean

# Install dependencies
install:
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	uv venv --python 3.12
	uv pip install -e .

# Run local development server
dev:
	@echo "Starting development server at http://localhost:8080"
	@echo "Try the ADK playground with: make playground"
	uv run uvicorn story_crafter_agent.fast_api_app:app --host 0.0.0.0 --port 8080 --reload

# Launch ADK web interface (requires .env setup)
web:
	@echo "Starting ADK web interface..."
	@echo "Access at http://127.0.0.1:8000"
	adk web

# Run tests (placeholder for now)
test:
	@echo "No tests configured yet"

# ==============================================================================
# Docker Testing
# ==============================================================================

# Build Docker image locally
docker-build:
	@echo "Building Docker image..."
	docker build -t story-crafter-agent:local .

# Run Docker container locally
docker-run:
	@echo "Running Docker container on port 8080..."
	@echo "Visit: http://localhost:8080/docs"
	docker run -p 8080:8080 \
		-e GOOGLE_CLOUD_PROJECT=gen-lang-client-0092086517 \
		-e GOOGLE_GENAI_USE_VERTEXAI=True \
		story-crafter-agent:local

# Test Docker build and run
docker-test: docker-build docker-run

# Stop all running containers
docker-stop:
	@echo "Stopping all story-crafter-agent containers..."
	docker ps -q --filter ancestor=story-crafter-agent:local | xargs -r docker stop

# Clean up Docker images
docker-clean:
	@echo "Removing Docker images..."
	docker rmi story-crafter-agent:local 2>/dev/null || true

# Deploy to Cloud Run (requires gcloud setup)
deploy:
	@echo "Deploying to Cloud Run..."
	gcloud run deploy story-crafter-agent \
		--source . \
		--region europe-west1 \
		--allow-unauthenticated \
		--memory 2Gi

# Clean up Python artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

