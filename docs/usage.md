# Usage Guide

## Quick Start

### 1. Installation

```bash
git clone https://github.com/yourorg/codesurgeon.git
cd codesurgeon
cp .env.example .env
# Edit .env with your API keys
docker compose up
```

App available at: http://localhost:8000

### 2. Analyze Code Snippet

**Web UI:**
1. Open http://localhost:8000
2. Select language (Python / JavaScript)
3. Paste code
4. Click "Analyze Code"
5. Review detected bugs and fixes

**API:**
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "x = 1 || 2",
    "language": "python"
  }'
```

**Response:**
```json
{
  "id": "uuid-1",
  "code_snippet": "x = 1 || 2",
  "language": "python",
  "bugs": [
    {
      "id": "bug-1",
      "type": "SYNTAX_ERROR",
      "severity": "CRITICAL",
      "line": 1,
      "description": "Using || instead of 'or' operator in Python",
      "confidence": 0.95
    }
  ],
  "fixes": {
    "bug-1": {
      "primary": {
        "code": "x = 1 or 2",
        "explanation": "Changed || to 'or' (correct Python syntax)"
      },
      "alternatives": [
        {
          "code": "x = bool(1) or bool(2)",
          "explanation": "Explicit boolean conversion"
        }
      ]
    }
  },
  "analysis_time_ms": 2500,
  "timestamp": "2026-05-07T10:30:00Z"
}
```

---

## API Reference

### POST /api/v1/analyze

Analyze code or GitHub PR for bugs.

**Request:**

Option 1: Code snippet
```json
{
  "code": "string (required)",
  "language": "string (required: python, javascript, auto)"
}
```

Option 2: GitHub PR
```json
{
  "pr_url": "string (required: https://github.com/owner/repo/pull/123)",
  "github_token": "string (optional; falls back to .env GITHUB_TOKEN)"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "bugs": [...],
  "fixes": {...},
  "analysis_time_ms": 2500,
  "timestamp": "2026-05-07T10:30:00Z"
}
```

**Response (400 - Bad Request):**
```json
{
  "error": "Code or PR URL required"
}
```

**Response (401 - Unauthorized):**
```json
{
  "error": "Invalid GitHub token"
}
```

**Response (503 - Service Unavailable):**
```json
{
  "error": "LLM service unavailable; try again"
}
```

---

### GET /api/v1/analysis/{id}

Retrieve cached analysis result.

**Response (200):**
```json
{
  "id": "uuid-1",
  "bugs": [...],
  ...
}
```

**Response (404):**
```json
{
  "error": "Analysis not found"
}
```

---

### POST /api/v1/fixes

Generate fixes for a specific bug.

**Request:**
```json
{
  "bug_id": "string (required)",
  "code": "string (required: full code context)"
}
```

**Response (200):**
```json
{
  "primary_fix": {
    "code": "string",
    "explanation": "string"
  },
  "alternatives": [
    {
      "code": "string",
      "explanation": "string"
    }
  ],
  "confidence": 0.72
}
```

---

### GET /api/v1/health

Health check endpoint.

**Response (200):**
```json
{
  "status": "healthy",
  "service": "CodeSurgeon",
  "timestamp": "2026-05-07T10:30:00Z"
}
```

---

## Configuration

### Environment Variables

Create `.env` file:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...  # OR
OPENAI_API_KEY=sk-...

# Optional
GITHUB_TOKEN=ghp_...
LLM_PROVIDER=anthropic  # or "openai"
LLM_MODEL=claude-3-opus-20240229
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CACHE_TTL_GITHUB=86400  # 24 hours
CACHE_TTL_ANALYSIS=3600  # 1 hour
```

### Docker Compose Override

To use custom settings, create `docker-compose.override.yml`:

```yaml
services:
  api:
    environment:
      LOG_LEVEL: DEBUG
      API_PORT: 9000
    ports:
      - "9000:9000"
```

---

## Use Cases

### Use Case 1: Developer Code Review

```bash
# 1. Analyze code locally
curl -X POST http://localhost:8000/api/v1/analyze \
  -d '{
    "code": "$(cat src/main.py)",
    "language": "python"
  }'

# 2. Review bugs in UI
# 3. Copy fixes to editor
# 4. Run tests locally before commit
```

### Use Case 2: CI/CD Pipeline Integration

```bash
# In GitHub Actions or GitLab CI
curl -X POST http://localhost:8000/api/v1/analyze \
  -d "{
    \"pr_url\": \"$CI_MERGE_REQUEST_PROJECT_URL/merge_requests/$CI_MERGE_REQUEST_IID\",
    \"github_token\": \"$GITHUB_TOKEN\"
  }" > analysis.json

# Fail if CRITICAL bugs > 0
critical=$(jq '[.bugs[] | select(.severity=="CRITICAL")] | length' analysis.json)
if [ "$critical" -gt 0 ]; then
  echo "Found $critical CRITICAL bugs"
  exit 1
fi
```

### Use Case 3: Learning Tool

```
1. Submit a snippet with intentional bugs
2. Get detailed explanations
3. Review alternative fixes
4. Learn idiomatic patterns
```

---

## Common Tasks

### Task: Analyze a GitHub PR

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "pr_url": "https://github.com/python/cpython/pull/12345",
    "github_token": "ghp_XXXXX"
  }'
```

### Task: Check API Status

```bash
curl http://localhost:8000/api/v1/health
```

### Task: Generate Fix for a Bug

```bash
# 1. Get analysis result
curl -X POST http://localhost:8000/api/v1/analyze \
  -d '{"code": "x = 1 || 2", "language": "python"}' | jq .

# 2. Extract bug_id from response
BUG_ID=$(curl -s -X POST http://localhost:8000/api/v1/analyze \
  -d '{"code": "x = 1 || 2", "language": "python"}' | jq -r '.bugs[0].id')

# 3. Generate fixes
curl -X POST http://localhost:8000/api/v1/fixes \
  -d "{\"bug_id\": \"$BUG_ID\", \"code\": \"x = 1 || 2\"}"
```

### Task: View Analysis Metrics

```bash
# In Python
import requests
response = requests.post('http://localhost:8000/api/v1/analyze',
  json={'code': 'x = 1 || 2', 'language': 'python'})
result = response.json()
print(f"Found {len(result['bugs'])} bugs in {result['analysis_time_ms']}ms")
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---|---|---|
| 503 Service Unavailable | LLM API timeout | Retry with exponential backoff; check API status |
| 400 Invalid language | Unsupported language | Use python, javascript, or auto-detect |
| 404 Analysis not found | Cache expired (>1hr) | Re-run analysis; results auto-expire after 1 hour |
| 401 GitHub auth error | Invalid token | Check GITHUB_TOKEN in .env; regenerate token if needed |

---

**Last updated:** May 7, 2026
