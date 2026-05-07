# CodeSurgeon: System Specification

> This is the source of truth for the project. The TA will feed this document
> to an LLM during grading and verify that the generated code passes the user
> story tests. Write it as if it must be enough for someone (or an LLM) to
> implement the project from scratch with no other reference.

## 1. Purpose and Scope

**CodeSurgeon** is an AI-powered GitHub bug repair agent that analyzes code pull requests and software repositories to automatically detect bugs, vulnerabilities, and code quality issues, then generates fixes with explanations. The system is designed for software developers and DevOps engineers who want AI-assisted code review and bug remediation. The system integrates with GitHub APIs to fetch PR changes, uses LLM (Claude/GPT) for intelligent bug detection, and provides a web UI for reviewing and accepting fixes. Out of scope: deployment to production repositories, git push operations, and multi-language support beyond Python/JavaScript.

## 2. Component Inventory

Every component listed here maps to a source module under `src/myproject/`. The grading script verifies this mapping via `grading/traceability.yaml`.

| Component | Source module | Responsibility |
|---|---|---|
| GitHubAnalyzer | src/myproject/github_analyzer.py | Fetch PR data and code from GitHub API |
| CodeAnalyzer | src/myproject/code_analyzer.py | Parse code structure using AST/regex |
| BugDetector | src/myproject/bug_detector.py | Detect bugs using static analysis + LLM |
| FixGenerator | src/myproject/fix_generator.py | Generate fixes and explanations via LLM |
| LLMClient | src/myproject/llm_client.py | Manage LLM API calls (Claude/GPT with retry) |
| API | src/myproject/api.py | FastAPI HTTP interface and routing |
| Frontend | src/myproject/frontend.py | Static HTML/JS UI served by FastAPI |

## 3. Data Flow

### Input: Code to Analyze

User provides either:
1. **GitHub PR URL**: `https://github.com/owner/repo/pull/123`
2. **Code snippet**: Raw Python/JavaScript code as text

### Processing Pipeline

1. **GitHub Analyzer** (if PR URL):
   - Authenticate with GitHub API
   - Fetch PR metadata and changed files
   - Extract diff for each file
   - Return: `{files: [{path, language, content, diff}]}`

2. **Code Analyzer**:
   - Parse code structure (AST for Python, regex for others)
   - Extract functions, classes, imports, error patterns
   - Validate syntax
   - Return: `{ast, functions, imports, syntax_errors}`

3. **Bug Detector**:
   - Run static analysis (pattern matching for common bugs)
   - Call LLM with code and analysis context
   - Parse LLM response into structured bugs
   - Deduplicate overlapping bugs
   - Return: `{bugs: [{id, file, line, type, severity, description, confidence}]}`

4. **Fix Generator** (per bug):
   - Call LLM with bug context and code snippet
   - Generate primary fix + 2+ alternatives
   - Return: `{fix: {code, explanation}, alternatives: [{code, explanation}]}`

### Output: Analysis Result

```json
{
  "id": "uuid",
  "code_snippet": "...",
  "language": "python",
  "bugs": [
    {
      "id": "bug-uuid",
      "file": "main.py",
      "line": 5,
      "type": "SYNTAX_ERROR",
      "severity": "CRITICAL",
      "description": "Using || instead of 'or' operator in Python",
      "confidence": 0.95
    }
  ],
  "fixes": {
    "bug-uuid": {
      "primary": {"code": "...", "explanation": "..."},
      "alternatives": [{"code": "...", "explanation": "..."}]
    }
  },
  "analysis_time_ms": 2500,
  "timestamp": "2026-05-07T10:30:00Z"
}
```

### Error Paths

- **Invalid GitHub token**: Return 401 with message "GitHub authentication failed"
- **PR not found**: Return 404 with message "PR not accessible"
- **Code parse error**: Return 400 with message "Code syntax invalid for language X"
- **LLM API timeout**: Return 503 with message "LLM service unavailable; try again"
- **Empty input**: Return 400 with message "Code or PR URL required"

## 4. Public Interfaces

This section is the contract. The user story tests import these exact module paths and call these exact function signatures.

### 4.1 HTTP API

**POST /api/v1/analyze**
- Request: `{code: string, language: string}` OR `{pr_url: string}`
- Response 200: Analysis result (see data flow output above)
- Response 400: `{error: string}`
- Response 401: `{error: string}`
- Response 403: `{error: string}`
- Response 404: `{error: string}`
- Response 503: `{error: string}`

**GET /api/v1/analysis/{id}**
- Response 200: Cached analysis result
- Response 404: `{error: "Analysis not found"}`

**POST /api/v1/fixes**
- Request: `{bug_id: string, code: string}`
- Response 200: `{primary_fix: {...}, alternatives: [...]}`
- Response 400: `{error: string}`

**GET /api/v1/health**
- Response 200: `{status: "healthy"}`

**GET /** (frontend)
- Response 200: Serve `index.html` (React SPA or simple HTML)

### 4.2 Python Interfaces

```python
# src/myproject/github_analyzer.py
async def fetch_pr_details(pr_url: str, token: str) -> dict:
    """Fetch PR metadata and changed files from GitHub."""
    # Returns: {owner, repo, pr_number, files: [{path, language, content, diff}]}

# src/myproject/code_analyzer.py
class CodeAnalyzer:
    def analyze(self, code: str, language: str) -> dict:
        """Parse code structure."""
        # Returns: {ast, functions, imports, syntax_valid, errors}

# src/myproject/bug_detector.py
async def detect_bugs(code: str, language: str, context: dict) -> list[dict]:
    """Detect bugs using static analysis + LLM."""
    # Returns: [{id, line, type, severity, description, confidence}]

# src/myproject/fix_generator.py
async def generate_fix(bug: dict, code: str) -> dict:
    """Generate a primary fix and alternatives."""
    # Returns: {primary: {code, explanation}, alternatives: [...]}

# src/myproject/llm_client.py
async def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call LLM with retry logic."""
    # Supports Anthropic Claude and OpenAI APIs

# src/myproject/api.py
app: FastAPI  # Uvicorn serves on port 8000
```

## 5. External Dependencies

**Production:**
- `fastapi==0.110.0` — HTTP API framework
- `uvicorn==0.27.1` — ASGI server
- `pydantic==2.6.4` — Request/response validation
- `anthropic==0.40.0` — Claude API client
- `requests==2.31.0` — HTTP library for GitHub API
- `PyGithub==2.1.1` — GitHub API Python wrapper
- `python-dotenv==1.0.0` — Environment variable management
- `loguru==0.7.2` — Structured logging

**Development & Testing:**
- `pytest==8.1.1` — Unit/integration tests
- `pytest-cov==5.0.0` — Coverage reporting
- `ruff==0.4.4` — Linter
- `black==24.4.2` — Code formatter
- `mypy==1.10.0` — Type checker
- `locust==2.27.0` — Load testing

## 6. Deployment

The application runs in Docker and is accessible via:

```bash
docker compose up
# Waits ~30 seconds for startup
# API available at http://localhost:8000
# UI available at http://localhost:8000/
# Docs at http://localhost:8000/docs
```

Environment variables (.env file):
- `GITHUB_TOKEN` (optional) — GitHub API authentication
- `ANTHROPIC_API_KEY` (required) — Claude API key
- `OPENAI_API_KEY` (optional, if using GPT)
- `API_HOST` (default: 0.0.0.0)
- `API_PORT` (default: 8000)
- `LOG_LEVEL` (default: INFO)

## 7. Non-Functional Requirements

- **Latency**: Code analysis completes in <5 seconds for typical 500-line files
- **Accuracy**: Bug detection recall ≥80% on common Python anti-patterns
- **Availability**: 99.5% uptime for API health checks
- **Concurrency**: Support ≥20 concurrent requests
- **Caching**: Cache GitHub PR data (24h TTL) and analysis results (1h TTL)

## 8. Limitations and Risks

- **Model hallucinations**: LLM-generated fixes may occasionally be incorrect; users should review
- **Language coverage**: Currently Python and JavaScript only
- **GitHub rate limits**: Requires backoff for high-volume PR analysis
- **Sensitive data**: Code is sent to LLM; use private deployments for proprietary code
