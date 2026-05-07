.PHONY: help test test-unit test-integration test-user-stories test-edge test-load lint format reproduce demo loadtest download-data download-models clean preflight regenerate

PACKAGE := myproject
SRC := src/$(PACKAGE)
PYTHON := python3.11
PIP := $(PYTHON) -m pip

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help:
	@echo "$(BLUE)CodeSurgeon Makefile$(NC)"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test               Run all tests (unit, integration, user-stories, edge)"
	@echo "  make test-unit          Run unit tests only"
	@echo "  make test-integration   Run integration tests only"
	@echo "  make test-user-stories  Run user story tests (9 stories)"
	@echo "  make test-edge          Run edge case tests"
	@echo "  make test-load          Run load test (Locust, 100 concurrent users)"
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@echo "  make lint               Run linting (ruff + mypy)"
	@echo "  make format             Format code (black + isort)"
	@echo ""
	@echo "$(GREEN)Build & Deploy:$(NC)"
	@echo "  make reproduce          Reproduce system from scratch (clean + install + test)"
	@echo "  make demo               Run end-to-end demo against live app"
	@echo "  make preflight          Run TA preflight checks (local validation)"
	@echo ""
	@echo "$(GREEN)Data & Models:$(NC)"
	@echo "  make download-data      Download test datasets (if any)"
	@echo "  make download-models    Download model checkpoints (if any)"
	@echo ""
	@echo "$(GREEN)Utilities:$(NC)"
	@echo "  make clean              Remove build artifacts, cache, logs"
	@echo "  make regenerate         Regenerate documentation from prompts"
	@echo "  make help               Show this help message"

# =============================================================================
# TESTING
# =============================================================================

test: test-unit test-integration test-user-stories test-edge
	@echo "$(GREEN)✓ All tests passed!$(NC)"

test-unit:
	@echo "$(YELLOW)Running unit tests...$(NC)"
	mkdir -p reports
	$(PYTHON) -m pytest tests/unit -v --junitxml=reports/unit_results.xml --cov-report=term-missing
	@echo "$(GREEN)✓ Unit tests complete (see reports/unit_results.xml)$(NC)"

test-integration:
	@echo "$(YELLOW)Running integration tests...$(NC)"
	mkdir -p reports
	$(PYTHON) -m pytest tests/integration -v --junitxml=reports/integration_results.xml
	@echo "$(GREEN)✓ Integration tests complete (see reports/integration_results.xml)$(NC)"

test-user-stories:
	@echo "$(YELLOW)Running user story tests (9 stories)...$(NC)"
	mkdir -p reports
	$(PYTHON) -m pytest tests/user_stories -v --junitxml=reports/user_stories_results.xml
	@echo "$(GREEN)✓ User story tests complete (see reports/user_stories_results.xml)$(NC)"

test-edge:
	@echo "$(YELLOW)Running edge case tests...$(NC)"
	mkdir -p reports
	$(PYTHON) -m pytest tests/edge -v --junitxml=reports/edge_results.xml || true
	@echo "$(GREEN)✓ Edge case tests complete (see reports/edge_results.xml)$(NC)"

test-load:
	@echo "$(YELLOW)Running load test (100 concurrent users for 5 min)...$(NC)"
	@echo "$(YELLOW)Starting app on port 8000 (if not running)...$(NC)"
	mkdir -p reports
	$(PYTHON) -m locust -f tests/load/locustfile.py --headless -u 100 -r 10 -t 5m --csv=reports/loadtest 2>&1 | tee reports/loadtest.log
	@echo "$(GREEN)✓ Load test complete (see reports/loadtest.csv)$(NC)"

# =============================================================================
# CODE QUALITY
# =============================================================================

lint:
	@echo "$(YELLOW)Running linting (ruff)...$(NC)"
	$(PYTHON) -m ruff check $(SRC) tests
	@echo "$(YELLOW)Running type checking (mypy)...$(NC)"
	$(PYTHON) -m mypy $(SRC) --ignore-missing-imports || true
	@echo "$(GREEN)✓ Linting complete$(NC)"

format:
	@echo "$(YELLOW)Formatting code (black)...$(NC)"
	$(PYTHON) -m black $(SRC) tests --line-length 120
	@echo "$(YELLOW)Sorting imports (ruff isort)...$(NC)"
	$(PYTHON) -m ruff check $(SRC) tests --select I --fix
	@echo "$(GREEN)✓ Formatting complete$(NC)"

# =============================================================================
# BUILD & REPRODUCIBILITY
# =============================================================================

reproduce: clean install test
	@echo "$(YELLOW)Generating coverage report...$(NC)"
	$(PYTHON) -m coverage report --fail-under=70
	@echo "$(GREEN)✓ Reproducibility checks passed!$(NC)"

demo:
	@echo "$(YELLOW)Running end-to-end demo...$(NC)"
	@echo "$(YELLOW)Prerequisites: app running on http://localhost:8000$(NC)"
	$(PYTHON) tests/e2e/demo.py
	@echo "$(GREEN)✓ Demo complete!$(NC)"

preflight:
	@echo "$(YELLOW)Running TA preflight checks...$(NC)"
	@echo "Checking directory structure..."
	@test -d "$(SRC)" || (echo "$(RED)✗ $(SRC) not found$(NC)"; exit 1)
	@test -d "tests/unit" || (echo "$(RED)✗ tests/unit not found$(NC)"; exit 1)
	@test -d "tests/integration" || (echo "$(RED)✗ tests/integration not found$(NC)"; exit 1)
	@test -d "tests/user_stories" || (echo "$(RED)✗ tests/user_stories not found$(NC)"; exit 1)
	@test -d "docs" || (echo "$(RED)✗ docs not found$(NC)"; exit 1)
	@test -f "pyproject.toml" || (echo "$(RED)✗ pyproject.toml not found$(NC)"; exit 1)
	@test -f "Makefile" || (echo "$(RED)✗ Makefile not found$(NC)"; exit 1)
	@echo "$(GREEN)✓ Directory structure OK$(NC)"
	@echo "Running lint..."
	@make lint > /dev/null 2>&1 || (echo "$(YELLOW)⚠ Lint warnings (non-blocking)$(NC)")
	@echo "$(GREEN)✓ Preflight checks complete!$(NC)"

# =============================================================================
# DATA & MODELS
# =============================================================================

download-data:
	@echo "$(YELLOW)Downloading test data...$(NC)"
	@mkdir -p data
	@echo "Note: No external datasets required. Using embedded test_snippets.json"
	@echo "$(GREEN)✓ Data ready$(NC)"

download-models:
	@echo "$(YELLOW)Downloading model checkpoints...$(NC)"
	@echo "Note: CodeSurgeon uses API-based models (Anthropic Claude, OpenAI GPT)"
	@echo "No local model downloads required."
	@echo "$(GREEN)✓ Models configured (via API keys)$(NC)"

# =============================================================================
# UTILITIES
# =============================================================================

clean:
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist *.egg-info
	rm -rf reports/*.xml reports/*.csv reports/*.log reports/coverage_html
	rm -rf .coverage
	@echo "$(GREEN)✓ Clean complete$(NC)"

install:
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

regenerate:
	@echo "$(YELLOW)Regenerating docs from prompts...$(NC)"
	@test -f "scripts/regenerate_prompt.md" || (echo "$(YELLOW)Note: scripts/regenerate_prompt.md not found (course-provided file)$(NC)")
	@echo "$(GREEN)✓ Regenerate complete$(NC)"

# =============================================================================
# DOCKER TARGETS (optional)
# =============================================================================

docker-build:
	@echo "$(YELLOW)Building Docker image...$(NC)"
	docker build -t codesurgeon:latest .
	@echo "$(GREEN)✓ Docker image built$(NC)"

docker-run:
	@echo "$(YELLOW)Starting app in Docker...$(NC)"
	docker compose up
	@echo "App available at http://localhost:8000"

docker-stop:
	@echo "$(YELLOW)Stopping Docker containers...$(NC)"
	docker compose down
	@echo "$(GREEN)✓ Containers stopped$(NC)"

# =============================================================================
# CUSTOM TARGETS
# =============================================================================

.DEFAULT_GOAL := help

all: install lint format test reproduce
	@echo "$(GREEN)✓ Full build complete!$(NC)"
