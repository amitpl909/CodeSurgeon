# CodeSurgeon - Technical Architecture Document
## AI-Powered GitHub Bug Repair Agent

**Version**: 1.0  
**Date**: May 2026  
**Architecture Pattern**: Microservices (Simplified)

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Component Design](#component-design)
3. [Data Flow](#data-flow)
4. [API Specifications](#api-specifications)
5. [Database Schema](#database-schema)
6. [Technology Stack Details](#technology-stack-details)
7. [Deployment Architecture](#deployment-architecture)
8. [Security Architecture](#security-architecture)
9. [Performance Considerations](#performance-considerations)

---

## Architecture Overview

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CodeSurgeon MVP                             │
├──────────────────────┬──────────────────────┬───────────────────┤
│   Web Dashboard      │   Backend API        │   External APIs   │
│   (React/Vue)        │   (FastAPI/Flask)    │   (OpenAI, GitHub)│
├──────────────────────┼──────────────────────┼───────────────────┤
│  - UI Components     │  - Request Handler   │  - GPT-4/Claude   │
│  - State Mgmt        │  - Code Analyzer     │  - GitHub API     │
│  - Result Display    │  - Bug Detector      │  - Webhooks       │
│  - Bug Visualization │  - Fix Generator     │                   │
└──────────────────────┴──────────────────────┴───────────────────┘
```

### Architectural Layers

```
┌─────────────────────────────────────────────────┐
│         Presentation Layer (Frontend)            │
│  - React Components, State, Routing, HTTP      │
├─────────────────────────────────────────────────┤
│         API Layer (FastAPI)                     │
│  - REST Endpoints, Request Validation          │
├─────────────────────────────────────────────────┤
│      Business Logic Layer (Core Engine)         │
│  - PR Parser, Bug Detector, Fix Generator      │
├─────────────────────────────────────────────────┤
│       External Integration Layer                │
│  - GitHub, OpenAI, LLM APIs                    │
├─────────────────────────────────────────────────┤
│    Data Layer (JSON Files/Session Cache)        │
│  - Results Storage, Session Data               │
└─────────────────────────────────────────────────┘
```

---

## Component Design

### 1. Frontend Layer (React/Vue)

#### Components
```
App/
├── Dashboard
│   ├── PRList
│   ├── AnalysisForm
│   └── StatusIndicator
├── ResultsView
│   ├── BugsList
│   ├── BugDetail
│   ├── FixSuggestion
│   └── CodeComparison
├── Navigation
│   ├── Header
│   └── Sidebar
└── Common
    ├── LoadingSpinner
    ├── ErrorBoundary
    └── Toast Notifications
```

#### State Management
- **Tool**: Redux/Zustand
- **Store Structure**:
  ```
  {
    analysis: {
      status: 'idle' | 'loading' | 'success' | 'error',
      currentPR: { ... },
      results: { ... },
      error: null
    },
    ui: {
      selectedBugId: null,
      theme: 'light' | 'dark'
    }
  }
  ```

---

### 2. API Layer (FastAPI)

#### Core Endpoints

**POST /api/analyze**
- Input: PR URL or code snippet
- Output: Bug analysis results
- Logic:
  1. Validate input
  2. Parse code
  3. Call bug detector
  4. Return results

**GET /api/analysis/{id}**
- Retrieve specific analysis result

**GET /api/health**
- System health check

**POST /api/fixes**
- Generate detailed fix for specific bug

---

### 3. Business Logic Layer

#### Module: GitHub Integration (`github_service.py`)
```python
class GitHubService:
    def __init__(self, token: str)
    def get_pr_files(pr_url: str) -> List[File]
    def parse_pr_diff(diff: str) -> Dict[str, List[Change]]
    def post_comment(pr_url: str, comment: str) -> bool
    def get_repository_info(repo_url: str) -> Dict
```

#### Module: Code Analyzer (`code_analyzer.py`)
```python
class CodeAnalyzer:
    def __init__(self, language: str)
    def extract_code_structure(code: str) -> AST
    def identify_patterns(ast: AST) -> List[Pattern]
    def find_potential_bugs(ast: AST) -> List[BugCandidate]
    def validate_syntax(code: str) -> bool
```

#### Module: Bug Detector (`bug_detector.py`)
```python
class BugDetector:
    def __init__(self, llm_client)
    def analyze_code(code: str, context: Dict) -> List[Bug]
    def classify_severity(bug: Bug) -> Severity
    def validate_bug(bug: Bug) -> bool
    def generate_confidence_score(bug: Bug) -> float
```

Bug Categories:
- **Syntax Errors**: Invalid Python/JS syntax
- **Logic Errors**: Incorrect algorithm implementation
- **Security Vulnerabilities**: SQL injection, XSS, etc.
- **Performance Issues**: N+1 queries, inefficient loops
- **Type Mismatches**: Type inconsistencies

#### Module: Fix Generator (`fix_generator.py`)
```python
class FixGenerator:
    def __init__(self, llm_client)
    def generate_fix(bug: Bug, code: str) -> FixSuggestion
    def generate_alternatives(bug: Bug, code: str) -> List[FixSuggestion]
    def validate_fix(fix: FixSuggestion) -> bool
    def format_fix(fix: FixSuggestion) -> str
```

---

## Data Flow

### Flow 1: Analyze PR Request

```
1. Frontend: User enters PR URL/code
   ↓
2. API: POST /api/analyze
   ↓
3. GitHub Service: Fetch PR details & diff
   ↓
4. Code Analyzer: Parse code structure
   ↓
5. Bug Detector: Identify bugs using LLM + static analysis
   ↓
6. Fix Generator: Generate fixes for each bug
   ↓
7. API: Return results to frontend
   ↓
8. Frontend: Display bugs and fixes to user
```

### Flow 2: Detailed Bug Analysis

```
1. User clicks on specific bug
   ↓
2. Frontend requests details: GET /api/analysis/{id}/bug/{bugId}
   ↓
3. Backend retrieves from cache/storage
   ↓
4. Generate detailed explanation & alternatives
   ↓
5. Return enriched data
   ↓
6. Frontend displays side-by-side comparison
```

---

## API Specifications

### RESTful API Design

#### 1. Analyze Code/PR
**Endpoint**: `POST /api/v1/analyze`

**Request**:
```json
{
  "type": "pr" | "snippet",
  "input": "https://github.com/user/repo/pull/123",
  "language": "python" | "javascript" | "java" | "auto",
  "context": {
    "framework": "django",
    "dependencies": ["numpy", "pandas"]
  }
}
```

**Response (200)**:
```json
{
  "id": "analysis_uuid",
  "status": "success",
  "timestamp": "2026-05-07T10:30:00Z",
  "bugs": [
    {
      "id": "bug_uuid",
      "type": "logic_error",
      "severity": "high",
      "line": 42,
      "code_snippet": "if x == 1 || y == 2:",
      "description": "Incorrect operator usage",
      "explanation": "Should use 'or' instead of '||' in Python",
      "confidence": 0.95
    }
  ],
  "summary": {
    "total_bugs": 5,
    "critical": 1,
    "high": 2,
    "medium": 2,
    "analysis_time_ms": 2500
  }
}
```

#### 2. Get Fix for Bug
**Endpoint**: `POST /api/v1/fixes`

**Request**:
```json
{
  "bug_id": "bug_uuid",
  "analysis_id": "analysis_uuid"
}
```

**Response (200)**:
```json
{
  "bug_id": "bug_uuid",
  "fix": {
    "corrected_code": "if x == 1 or y == 2:",
    "explanation": "Python uses 'or' for logical OR",
    "confidence": 0.98
  },
  "alternatives": [
    {
      "code": "if (x == 1) or (y == 2):",
      "note": "More explicit parentheses"
    }
  ]
}
```

#### 3. Get Analysis Results
**Endpoint**: `GET /api/v1/analysis/{analysisId}`

**Response (200)**:
```json
{
  "id": "analysis_uuid",
  "status": "completed",
  "created_at": "2026-05-07T10:30:00Z",
  "bugs": [ ... ],
  "summary": { ... }
}
```

#### 4. Health Check
**Endpoint**: `GET /api/v1/health`

**Response (200)**:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-07T10:30:00Z",
  "services": {
    "github_api": "operational",
    "llm_service": "operational"
  }
}
```

---

## Database Schema (MVP - JSON File Based)

### File Structure
```
data/
├── analyses/
│   ├── {analysis_uuid}.json
│   └── {analysis_uuid}.json
├── cache/
│   ├── github_repos_cache.json
│   └── analysis_cache.json
└── logs/
    └── analysis_log.jsonl
```

### Analysis Record (analyses/{id}.json)
```json
{
  "id": "uuid",
  "created_at": "ISO-8601",
  "pr_url": "https://github.com/...",
  "language": "python",
  "status": "completed",
  "bugs": [
    {
      "id": "bug_uuid",
      "type": "logic_error",
      "severity": "high",
      "line": 42,
      "code_snippet": "...",
      "description": "...",
      "explanation": "...",
      "confidence": 0.95,
      "fix": {
        "corrected_code": "...",
        "explanation": "..."
      }
    }
  ],
  "analysis_time_ms": 2500,
  "tokens_used": 1250
}
```

---

## Technology Stack Details

### Backend Stack

#### 1. FastAPI
- **Why**: Fast, modern, built-in async support, automatic API docs
- **Usage**:
  ```python
  from fastapi import FastAPI
  app = FastAPI()
  
  @app.post("/api/v1/analyze")
  async def analyze_code(request: AnalysisRequest):
      # Implementation
  ```

#### 2. PyGithub
- **Purpose**: GitHub API client
- **Setup**:
  ```python
  from github import Github
  g = Github(GITHUB_TOKEN)
  repo = g.get_repo("user/repo")
  pr = repo.get_pull(123)
  ```

#### 3. LLM Client (OpenAI/Anthropic)
- **Purpose**: AI-powered bug detection and fix generation
- **Setup**:
  ```python
  from openai import OpenAI
  client = OpenAI(api_key=OPENAI_KEY)
  response = client.chat.completions.create(
      model="gpt-4",
      messages=[...]
  )
  ```

#### 4. Pydantic
- **Purpose**: Data validation and serialization
- **Models**:
  ```python
  class AnalysisRequest(BaseModel):
      type: Literal["pr", "snippet"]
      input: str
      language: str
  ```

#### 5. AST (Python built-in)
- **Purpose**: Static code analysis
- **Usage**: Parse and analyze code structure

### Frontend Stack

#### 1. React/TypeScript
- **Why**: Component-based, strong typing, large ecosystem
- **Project Structure**:
  ```
  src/
  ├── components/
  ├── pages/
  ├── services/
  ├── hooks/
  ├── store/
  └── types/
  ```

#### 2. TailwindCSS
- **Purpose**: Utility-first CSS for rapid UI development
- **Benefits**: Fast prototyping, consistent design

#### 3. Axios
- **Purpose**: HTTP client for API communication
- **Instance Setup**:
  ```typescript
  const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    timeout: 30000
  });
  ```

#### 4. React Query (optional) or Zustand
- **Purpose**: State and data fetching management

---

## Deployment Architecture

### Local Development Setup
```
1. Python Virtual Environment
   └── python -m venv venv

2. Backend Server
   └── FastAPI: uvicorn main:app --reload

3. Frontend Dev Server
   └── React: npm start

4. Environment Variables
   └── .env: GITHUB_TOKEN, OPENAI_API_KEY, etc.
```

### Docker Containerization (Optional)
```
Dockerfile (Backend):
  - Python 3.9 base image
  - Install dependencies from requirements.txt
  - Run FastAPI with Uvicorn

Dockerfile (Frontend):
  - Node.js base for build
  - Build React app
  - Serve with nginx

docker-compose.yml:
  - Backend service
  - Frontend service
  - Network configuration
```

---

## Security Architecture

### 1. API Security
- **CORS**: Configure allowed origins
- **Rate Limiting**: Prevent abuse (requests/minute)
- **Input Validation**: Pydantic validates all inputs
- **Error Handling**: Don't expose sensitive info in errors

### 2. GitHub Token Security
```python
# Store in environment variables, NOT code
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Use GitHub's personal access token with minimal scopes
# Scopes: repo (read-only), workflow (read-only)
```

### 3. LLM API Key Security
```python
# Store securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Never log or expose in responses
```

### 4. Code Analysis Privacy
- **No Logging**: Don't log analyzed code
- **Temporary Storage**: Delete analysis after display
- **Memory Cleanup**: Clear sensitive data after processing

### 5. HTTPS (Production)
- Use SSL/TLS certificates
- Redirect HTTP to HTTPS
- Set security headers (CSP, X-Frame-Options, etc.)

---

## Performance Considerations

### Optimization Strategies

#### 1. Caching
```python
# Cache GitHub repo info (24 hours)
@cache.cached(timeout=86400, key_prefix="github_repo_")
def get_repo_info(repo_url: str):
    pass

# Cache LLM responses (specific bugs)
cache_manager.set(f"bug_fix_{bug_hash}", fix_result, timeout=3600)
```

#### 2. Async Processing
```python
# Use FastAPI async endpoints for I/O operations
@app.post("/api/v1/analyze")
async def analyze_code(request: AnalysisRequest):
    # Parallel requests to GitHub and LLM
    results = await asyncio.gather(
        github_service.get_pr_files(request.input),
        code_analyzer.analyze(request.input)
    )
```

#### 3. Request Timeouts
```python
# Set strict timeouts to prevent hanging requests
GITHUB_API_TIMEOUT = 10  # seconds
LLM_API_TIMEOUT = 20  # seconds
ANALYSIS_TIMEOUT = 30  # seconds
```

#### 4. Batch Processing
```python
# Batch GitHub API calls to respect rate limits
def batch_fetch_file_contents(files: List[str], batch_size=10):
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        yield fetch_batch(batch)
```

#### 5. Frontend Optimization
- Code splitting
- Lazy loading components
- Memoization of expensive calculations
- Debounced search input

### Performance Targets
- **PR Analysis**: < 30 seconds
- **API Response**: < 5 seconds (after analysis)
- **Frontend Load**: < 3 seconds
- **Memory Usage**: < 500MB
- **Concurrent Users**: 20

---

## Scalability (Post-MVP)

### Current Bottlenecks (MVP)
- Single-threaded LLM processing
- No database persistence
- Memory-based caching
- Single server deployment

### Scaling Strategy
1. **Database**: Add PostgreSQL for persistent storage
2. **Task Queue**: Redis + Celery for async processing
3. **Caching Layer**: Redis for distributed caching
4. **Load Balancing**: Nginx/HAProxy
5. **Microservices**: Separate services for analyzer, fixer, etc.
6. **CDN**: Content delivery network for frontend assets

---

## Monitoring & Logging (MVP)

### Logging
```python
# Structured logging
logger.info("PR Analysis Started", extra={
    "analysis_id": analysis_id,
    "pr_url": pr_url,
    "language": language
})

logger.error("Bug Detection Failed", exc_info=True)
```

### Metrics
- API response times
- LLM API usage and costs
- Error rates
- Cache hit rates

---

## Error Handling

### Custom Exceptions
```python
class GitHubAPIError(Exception): pass
class InvalidCodeError(Exception): pass
class LLMAnalysisError(Exception): pass
class CodeParseError(Exception): pass
```

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_PR_URL",
    "message": "Invalid GitHub PR URL format",
    "details": "Expected format: https://github.com/user/repo/pull/number"
  }
}
```

---

## Integration Points

### External APIs
1. **GitHub API v3/v4**
   - Get PR details
   - Fetch file contents
   - Post comments

2. **OpenAI API / Anthropic Claude**
   - Code analysis via LLM
   - Fix generation

3. **Optional: Code Quality APIs**
   - SonarQube
   - CodeClimate

---

## Deployment Checklist

- [ ] Environment variables configured
- [ ] GitHub token with appropriate scopes
- [ ] OpenAI API key validated
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Error handling tested
- [ ] Frontend built for production
- [ ] Security headers configured
- [ ] Logging configured
- [ ] Monitoring setup
- [ ] Docker images built (optional)
- [ ] Documentation complete

---

## Conclusion

This architecture provides a solid foundation for MVP deployment while allowing for scalability and advanced features in future iterations. The layered approach ensures separation of concerns, making the system maintainable and testable.
