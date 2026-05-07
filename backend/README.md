# CodeSurgeon Backend

FastAPI backend for CodeSurgeon AI Bug Repair Agent.

## Setup

### Prerequisites
- Python 3.9+
- GitHub Personal Access Token
- OpenAI API Key

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Configure .env file with your credentials
```

### Running

```bash
# Development (with reload)
python main.py

# Or use uvicorn directly
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## Project Structure

```
backend/
├── main.py                    # FastAPI app entry point
├── config.py                  # Configuration from env vars
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
│
└── src/
    ├── models/
    │   └── schemas.py        # Pydantic data models
    │
    ├── services/
    │   ├── github_service.py    # GitHub API integration
    │   ├── code_analyzer.py     # Code structure analysis
    │   ├── bug_detector.py      # Bug detection engine
    │   └── fix_generator.py     # Fix generation
    │
    ├── integrations/
    │   └── llm_client.py      # OpenAI/Claude client
    │
    ├── routes/
    │   ├── analyze.py         # Analysis endpoints
    │   └── error_handlers.py  # Error handling
    │
    ├── utils/
    │   ├── logger.py          # Logging setup
    │   ├── cache.py           # Caching utilities
    │   ├── validators.py      # Input validation
    │   └── __init__.py
    │
    ├── exceptions.py          # Custom exceptions
    │
    └── __init__.py
```

## API Endpoints

### POST /api/v1/analyze
Analyze code for bugs.

**Request:**
```json
{
  "type": "snippet",
  "input": "def foo():\n    x = 1 || 2",
  "language": "python",
  "context": {}
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "success",
  "timestamp": "2026-05-07T10:30:00Z",
  "bugs": [
    {
      "id": "uuid",
      "type": "syntax_error",
      "severity": "HIGH",
      "line": 2,
      "code_snippet": "x = 1 || 2",
      "description": "Invalid Python operators",
      "explanation": "Python uses 'or' and 'and', not '||' and '&&'",
      "confidence": 0.95
    }
  ],
  "summary": {
    "total_bugs": 1,
    "critical": 0,
    "high": 1,
    "medium": 0,
    "low": 0,
    "analysis_time_ms": 2500
  }
}
```

### GET /api/v1/analysis/{analysisId}
Retrieve previous analysis results.

### POST /api/v1/fixes
Generate fixes for a specific bug.

**Request:**
```json
{
  "bug_id": "uuid",
  "analysis_id": "uuid"
}
```

### GET /api/v1/health
Check system health.

### GET /docs
Interactive API documentation (Swagger UI).

## Services

### GitHubService
Handles GitHub API interactions:
- Fetch PR details
- Get diff and changed files
- Post comments on PRs

### CodeAnalyzer
Analyzes code structure:
- Parse AST (for Python)
- Extract functions, classes, imports
- Validate syntax

### BugDetector
Detects bugs using:
- Static analysis (regex patterns)
- LLM analysis (OpenAI/Claude)
- Deduplication and filtering

### FixGenerator
Generates code fixes:
- Primary fix suggestion
- Alternative solutions
- Fix validation

## Configuration

### Environment Variables

```env
# GitHub
GITHUB_TOKEN=your_token_here
GITHUB_API_TIMEOUT=10

# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# API
API_HOST=0.0.0.0
API_PORT=8000
API_ENV=development
ANALYSIS_TIMEOUT=30

# Frontend
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=INFO
```

### Getting Tokens

**GitHub Token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo` (read-only), `workflow` (read-only)
4. Copy the token to `.env` as `GITHUB_TOKEN`

**OpenAI API Key:**
1. Go to https://platform.openai.com/account/api-keys
2. Create new secret key
3. Copy to `.env` as `OPENAI_API_KEY`

## Error Handling

### Custom Exceptions

- `GitHubAPIError` - GitHub API failures
- `LLMAnalysisError` - LLM API failures
- `CodeParseError` - Code parsing issues
- `InvalidInputError` - Invalid user input
- `ServiceTimeoutError` - Service timeouts

### Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": "Additional details"
  }
}
```

## Caching

Results are cached locally in JSON files:
- **Location**: `backend/data/cache/`
- **TTL**: 1 hour for analysis, 24 hours for GitHub data
- **Strategy**: In-memory + file-based persistence

## Logging

Logs are stored in `backend/logs/app.log` and console output.

**Log Levels:**
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warnings
- ERROR: Error messages

Configure level in `.env` with `LOG_LEVEL`.

## Performance Tips

1. **Caching**: Results are cached to reduce redundant analysis
2. **Timeouts**: Set appropriate timeouts for external services
3. **Batch Processing**: Process multiple files efficiently
4. **Async**: Use async endpoints for I/O operations

## Testing

### Manual Testing

```python
# Test bug detection
from src.services.bug_detector import BugDetector

detector = BugDetector()
bugs = detector.detect_bugs("def foo():\n    x = 1 || 2", "python")
for bug in bugs:
    print(f"Found: {bug.description}")
```

### API Testing with Curl

```bash
# Analyze code
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "type": "snippet",
    "input": "def foo():\n    x = 1 || 2",
    "language": "python"
  }'

# Check health
curl http://localhost:8000/api/v1/health
```

## Troubleshooting

### GitHub API Errors

**401 Unauthorized:**
- Verify GitHub token is valid
- Token may have expired, generate new one

**403 Forbidden:**
- Check token has required scopes
- May be rate limited

**404 Not Found:**
- PR URL may be invalid
- Repository may be private or deleted

### LLM API Errors

**401 Unauthorized:**
- Verify OpenAI API key is correct
- Check key has not been revoked

**429 Rate Limited:**
- Too many requests, wait and retry
- Consider upgrading OpenAI plan

**503 Service Unavailable:**
- OpenAI service may be down
- Try again later

### Code Analysis Issues

**Syntax Error:**
- Code contains invalid syntax
- Specify correct language in request

**Empty Results:**
- Code may be too simple
- Try analyzing different code sample

## Docker Setup (Optional)

```bash
# Build image
docker build -t codesurgeon-backend .

# Run container
docker run -p 8000:8000 \
  -e GITHUB_TOKEN=your_token \
  -e OPENAI_API_KEY=your_key \
  codesurgeon-backend
```

## Performance Metrics

- Analysis time: 2-5 seconds
- LLM API time: 3-10 seconds
- Total time: < 30 seconds (target)
- Throughput: 20+ concurrent requests

## Deployment

### Local
```bash
python main.py
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Next Steps

- Add database (PostgreSQL) for persistence
- Implement webhook support
- Add more programming language support
- Create admin dashboard
- Setup CI/CD pipeline

## Support

For issues or questions:
1. Check logs in `backend/logs/app.log`
2. Review error messages in API response
3. Consult TECHNICAL_ARCHITECTURE.md
4. Check environment variables are set correctly
