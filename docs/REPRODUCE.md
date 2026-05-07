# Reproducibility

## Overview

This document describes how to reproduce the CodeSurgeon system from scratch, including data preparation, model setup, and full pipeline execution.

**Estimated time:** 20 minutes on a clean machine with internet access.

## Environment

- Python 3.11+
- Docker + Docker Compose
- ~2GB disk space
- Internet connection for API calls (GitHub, Anthropic/OpenAI)

## Steps to Reproduce

### 1. Clone and Setup

```bash
git clone https://github.com/yourorg/codesurgeon.git
cd codesurgeon
cp .env.example .env
# Edit .env with required API keys (see .env.example)
```

### 2. Build and Start Docker

```bash
docker compose up --build
# Waits ~30 seconds for startup
# Check http://localhost:8000/health for readiness
```

### 3. Run Full Test Suite

```bash
make test
# Generates reports/unit.xml, integration.xml, user_stories.xml, coverage.xml
```

### 4. Run Reproducibility Checks

```bash
make reproduce
# Cleans artifacts, downloads data/models (if any), re-runs pipeline
# Compares output metrics to expected baselines
```

### 5. Expected Outputs

After `make reproduce`, verify:

```bash
ls -la reports/
# Expected files:
# - unit.xml (pass)
# - integration.xml (pass)
# - user_stories.xml (pass, 9 stories)
# - coverage.xml (≥70% coverage)
# - coverage_html/index.html (open in browser)
```

Example metric output:

```
Bugs detected in test suite: 42
Average fix generation time: 1.8 sec
API availability: 100% (mock)
Overall test coverage: 78%
```

## Reproducibility Metrics

The following metrics should match within stated tolerance:

| Metric | Expected | Tolerance |
|---|---|---|
| Unit test pass rate | 100% | 0% |
| Integration test pass rate | 100% | 0% |
| User story pass rate | 100% | 0% |
| Code coverage | ≥70% | ±2% |
| API latency (p95) | <3 sec | ±0.5 sec |
| Bug detection recall | ≥80% | ±5% |

## How to Verify

1. **Quick health check:**
   ```bash
   curl http://localhost:8000/api/v1/health
   # Expected: {"status": "healthy"}
   ```

2. **Run one user story manually:**
   ```bash
   pytest tests/user_stories/test_us_01.py -v
   ```

3. **Check code quality:**
   ```bash
   make lint
   # Expected: 0 errors
   ```

4. **Run load test:**
   ```bash
   make loadtest
   # Expected: >50 concurrent users, <5% failure rate
   ```

## Known Issues and Workarounds

1. **GitHub rate limiting:** If testing with real PRs, set `GITHUB_API_TIMEOUT=30` in .env
2. **LLM API costs:** Tests use mocked LLM for cost control; set `MOCK_LLM=true` in .env
3. **Slow first startup:** First Docker build may take 2-3 min; subsequent restarts are <10 sec

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| Port 8000 already in use | Another process listening | `lsof -i :8000` and kill process |
| LLM API timeout | Network or service down | Check API status; retry with backoff |
| Test hangs | Integration test trying real API | Set `MOCK_LLM=true` and `MOCK_GITHUB=true` |
| Coverage <70% | Incomplete test coverage | Run `coverage report` to identify gaps |

## Infrastructure

- **API Server:** FastAPI + Uvicorn on port 8000
- **Frontend:** Static HTML/React on port 8000
- **Storage:** In-memory cache (development); use Redis in production
- **Dependencies:** See `requirements.txt` and `pyproject.toml`

---

**Last verified:** May 7, 2026
