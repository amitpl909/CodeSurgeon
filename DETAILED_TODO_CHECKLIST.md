# CodeSurgeon MVP - Detailed ToDo Checklist
## Low-Level Tasks for Development & Deployment (1 Day Sprint)

**Total Estimated Time**: 8 hours  
**Recommended Distribution**: 6 hours backend + 1.5 hours frontend + 0.5 hours deployment & testing

---

## ✅ Phase 1: Project Setup & Environment (1 hour)

### 1.1 Backend Project Structure
- [ ] Create `/backend` directory structure:
  - [ ] `/backend/main.py` - FastAPI app entry point
  - [ ] `/backend/config.py` - Configuration and environment variables
  - [ ] `/backend/requirements.txt` - Python dependencies
  - [ ] `/backend/.env.example` - Environment template
  - [ ] `/backend/Dockerfile` - Docker configuration (optional)
  
- [ ] Create `/backend/src/` subdirectories:
  - [ ] `/backend/src/services/` - Business logic services
  - [ ] `/backend/src/models/` - Data models and schemas
  - [ ] `/backend/src/routes/` - API route handlers
  - [ ] `/backend/src/utils/` - Utility functions
  - [ ] `/backend/src/integrations/` - External API integrations

### 1.2 Frontend Project Structure
- [ ] Create `/frontend` directory with React structure:
  - [ ] `src/components/` - React components
  - [ ] `src/pages/` - Page components
  - [ ] `src/services/` - API client and services
  - [ ] `src/store/` - State management
  - [ ] `src/types/` - TypeScript type definitions
  - [ ] `src/hooks/` - Custom React hooks
  - [ ] `public/` - Static assets
  - [ ] `.env.example` - Environment template

### 1.3 Environment Setup
- [ ] Create `.env` file with:
  - [ ] `GITHUB_TOKEN=your_token_here`
  - [ ] `OPENAI_API_KEY=your_key_here`
  - [ ] `API_URL=http://localhost:8000`
  - [ ] `FRONTEND_PORT=3000`
  - [ ] `BACKEND_PORT=8000`

### 1.4 Dependencies Installation
- [ ] Install Python backend dependencies (FastAPI, PyGithub, OpenAI, Pydantic, etc.)
- [ ] Install Node.js frontend dependencies (React, TypeScript, Axios, Tailwind, etc.)
- [ ] Create virtual environment (Python)
- [ ] Test basic imports in main.py

---

## ✅ Phase 2: Backend Development (5 hours)

### 2.1 Data Models & Schemas (30 min)

#### File: `/backend/src/models/schemas.py`
- [ ] Create `AnalysisRequest` Pydantic model:
  - [ ] type: "pr" | "snippet"
  - [ ] input: string
  - [ ] language: string
  - [ ] context: optional object

- [ ] Create `Bug` Pydantic model:
  - [ ] id: UUID
  - [ ] type: string (syntax_error, logic_error, security_vulnerability, etc.)
  - [ ] severity: enum (CRITICAL, HIGH, MEDIUM, LOW)
  - [ ] line: integer
  - [ ] code_snippet: string
  - [ ] description: string
  - [ ] explanation: string
  - [ ] confidence: float (0-1)

- [ ] Create `Fix` Pydantic model:
  - [ ] corrected_code: string
  - [ ] explanation: string
  - [ ] confidence: float

- [ ] Create `AnalysisResponse` Pydantic model:
  - [ ] id: UUID
  - [ ] status: string
  - [ ] bugs: List[Bug]
  - [ ] summary: object with totals
  - [ ] analysis_time_ms: integer

- [ ] Create `AlternativeFix` Pydantic model:
  - [ ] code: string
  - [ ] note: string

### 2.2 Configuration Module (20 min)

#### File: `/backend/config.py`
- [ ] Load environment variables using `python-dotenv`
- [ ] Set API timeouts (GitHub: 10s, LLM: 20s, Analysis: 30s)
- [ ] Configure logging settings
- [ ] Set LLM model selection (GPT-4 or Claude)
- [ ] Set GitHub API version and endpoints
- [ ] Configure CORS settings
- [ ] Set rate limiting parameters

### 2.3 GitHub Integration Service (1 hour)

#### File: `/backend/src/services/github_service.py`
- [ ] Create `GitHubService` class:
  - [ ] `__init__(token: str)` - Initialize with GitHub token
  - [ ] `get_pr_details(pr_url: str) -> dict` - Fetch PR info from URL
  - [ ] `get_pr_files(pr_url: str) -> List[dict]` - Get changed files in PR
  - [ ] `parse_pr_url(url: str) -> dict` - Extract owner, repo, PR number
  - [ ] `fetch_file_content(owner: str, repo: str, path: str, ref: str) -> str`
  - [ ] `get_pr_diff(owner: str, repo: str, pr_number: int) -> str`
  - [ ] `post_comment(pr_url: str, comment: str) -> bool`
  - [ ] `error_handling`: Implement try-catch with custom error messages

- [ ] Use PyGithub library for all GitHub operations
- [ ] Implement rate limiting awareness
- [ ] Add logging for all API calls
- [ ] Handle authentication errors gracefully

### 2.4 Code Analyzer Service (1 hour)

#### File: `/backend/src/services/code_analyzer.py`
- [ ] Create `CodeAnalyzer` class:
  - [ ] `__init__(language: str)` - Support Python, JavaScript, Java
  - [ ] `extract_structure(code: str) -> dict` - Parse code AST
  - [ ] `validate_syntax(code: str) -> bool` - Check for syntax errors
  - [ ] `extract_functions(code: str) -> List[dict]` - Find function definitions
  - [ ] `extract_classes(code: str) -> List[dict]` - Find class definitions
  - [ ] `find_imports(code: str) -> List[str]` - Extract dependencies
  - [ ] `detect_patterns(code: str) -> List[dict]` - Identify code patterns

- [ ] Use `ast` module for Python code analysis
- [ ] Support basic analysis for JavaScript/Java (regex-based)
- [ ] Cache analysis results
- [ ] Handle edge cases (empty files, binary data, etc.)

### 2.5 Bug Detection Service (1.5 hours)

#### File: `/backend/src/services/bug_detector.py`
- [ ] Create `BugDetector` class:
  - [ ] `__init__(llm_client)` - Initialize with LLM client
  - [ ] `detect_bugs(code: str, context: dict) -> List[Bug]` - Main detection logic
  - [ ] `classify_severity(bug: dict) -> str` - Assign severity level
  - [ ] `validate_bug(bug: dict) -> bool` - Verify bug credibility
  - [ ] `generate_confidence_score(bug: dict) -> float` - Calculate confidence

- [ ] Implement prompt engineering for LLM:
  - [ ] System prompt: "You are a code reviewer detecting bugs..."
  - [ ] Context inclusion: code, language, frameworks
  - [ ] Output format: Structured JSON with bug details

- [ ] Bug detection strategy:
  - [ ] Use regex for obvious patterns (common errors)
  - [ ] Use LLM for complex bug analysis
  - [ ] Combine static + dynamic analysis
  - [ ] Filter false positives

- [ ] Implement caching for repeated analyses
- [ ] Add timeout handling for LLM calls

### 2.6 Fix Generation Service (1 hour)

#### File: `/backend/src/services/fix_generator.py`
- [ ] Create `FixGenerator` class:
  - [ ] `__init__(llm_client)` - Initialize with LLM client
  - [ ] `generate_fix(bug: Bug, code: str) -> Fix` - Generate primary fix
  - [ ] `generate_alternatives(bug: Bug, code: str) -> List[Fix]` - Generate 2-3 alternatives
  - [ ] `validate_fix(fix: Fix) -> bool` - Syntax check for generated code
  - [ ] `format_fix_explanation(fix: Fix) -> str` - Create clear explanation

- [ ] LLM prompting:
  - [ ] Provide bug description and code context
  - [ ] Request fix with explanation
  - [ ] Ask for alternative solutions
  - [ ] Include best practices guidance

- [ ] Post-processing:
  - [ ] Extract code blocks from LLM response
  - [ ] Validate syntax of generated code
  - [ ] Parse explanations and alternatives

### 2.7 LLM Client Integration (45 min)

#### File: `/backend/src/integrations/llm_client.py`
- [ ] Create `LLMClient` class:
  - [ ] `__init__(api_key: str, model: str)` - Initialize with API key
  - [ ] `analyze_code(prompt: str) -> str` - Send analysis request
  - [ ] `generate_response(messages: List[dict]) -> str` - Chat completion
  - [ ] `count_tokens(text: str) -> int` - Estimate token usage
  - [ ] `error_handling`: Rate limits, timeouts, API errors

- [ ] Implement OpenAI client:
  - [ ] Use `openai.ChatCompletion.create()`
  - [ ] Set model to GPT-4 or GPT-3.5-turbo
  - [ ] Configure temperature (0.3-0.7)
  - [ ] Set max_tokens appropriately

- [ ] Implement prompt templates:
  - [ ] Bug detection prompt template
  - [ ] Fix generation prompt template
  - [ ] Code review prompt template

- [ ] Add retry logic for failed requests
- [ ] Log token usage for cost tracking

### 2.8 API Routes - Main Endpoints (1.5 hours)

#### File: `/backend/src/routes/analyze.py`
- [ ] Create `POST /api/v1/analyze` endpoint:
  - [ ] Validate request schema
  - [ ] Extract PR URL or code snippet
  - [ ] Call GitHub service (if URL)
  - [ ] Call code analyzer
  - [ ] Call bug detector
  - [ ] Call fix generator
  - [ ] Return formatted response
  - [ ] Error handling with proper status codes

- [ ] Create `GET /api/v1/analysis/{analysisId}` endpoint:
  - [ ] Retrieve cached/stored analysis
  - [ ] Return full details
  - [ ] 404 if not found

- [ ] Create `POST /api/v1/fixes` endpoint:
  - [ ] Generate detailed fix for specific bug
  - [ ] Return with alternatives
  - [ ] Explanations included

- [ ] Create `GET /api/v1/health` endpoint:
  - [ ] Check GitHub API status
  - [ ] Check LLM service status
  - [ ] Return health summary

#### File: `/backend/main.py`
- [ ] Initialize FastAPI app:
  - [ ] Configure CORS middleware
  - [ ] Configure error handlers
  - [ ] Add request logging middleware
  - [ ] Include all route blueprints
  - [ ] Set up lifespan context

- [ ] Create main entry point:
  - [ ] Load configuration
  - [ ] Initialize services
  - [ ] Start server with uvicorn

### 2.9 Utility Functions & Helpers (30 min)

#### File: `/backend/src/utils/cache.py`
- [ ] Create simple cache manager:
  - [ ] `set(key: str, value: dict, ttl: int)`
  - [ ] `get(key: str) -> dict`
  - [ ] `delete(key: str)`
  - [ ] `clear()` - Clear all cache
  - [ ] Use JSON file for storage (MVP)

#### File: `/backend/src/utils/logger.py`
- [ ] Configure logging:
  - [ ] File handler (logs/app.log)
  - [ ] Console handler
  - [ ] Structured logging format
  - [ ] Different levels (DEBUG, INFO, WARNING, ERROR)

#### File: `/backend/src/utils/validators.py`
- [ ] Create validation functions:
  - [ ] `validate_github_url(url: str) -> bool`
  - [ ] `validate_code(code: str) -> bool`
  - [ ] `validate_language(lang: str) -> bool`

### 2.10 Error Handling & Custom Exceptions (20 min)

#### File: `/backend/src/exceptions.py`
- [ ] Create custom exception classes:
  - [ ] `GitHubAPIError` - GitHub API failures
  - [ ] `LLMAnalysisError` - LLM API failures
  - [ ] `CodeParseError` - Code parsing issues
  - [ ] `InvalidInputError` - Invalid user input
  - [ ] `ServiceTimeoutError` - Service timeouts

#### File: `/backend/src/routes/error_handlers.py`
- [ ] Register global error handlers
- [ ] Format error responses consistently
- [ ] Log errors for debugging
- [ ] Return appropriate HTTP status codes

---

## ✅ Phase 3: Frontend Development (1.5 hours)

### 3.1 Project Initialization (15 min)

#### File: `/frontend/package.json`
- [ ] Configure React 18+ project
- [ ] Add key dependencies:
  - [ ] axios
  - [ ] react-router-dom
  - [ ] typescript
  - [ ] tailwindcss
  - [ ] zustand (state management)

#### File: `/frontend/tsconfig.json`
- [ ] Configure TypeScript settings

#### File: `/frontend/.env.example`
- [ ] `REACT_APP_API_URL=http://localhost:8000`
- [ ] `REACT_APP_ENV=development`

### 3.2 TypeScript Type Definitions (15 min)

#### File: `/frontend/src/types/index.ts`
- [ ] Define `Bug` interface (matches backend)
- [ ] Define `Fix` interface
- [ ] Define `AlternativeFix` interface
- [ ] Define `AnalysisResult` interface
- [ ] Define `AnalysisRequest` interface
- [ ] Define API response types

### 3.3 API Client Service (20 min)

#### File: `/frontend/src/services/api.ts`
- [ ] Create Axios instance with base URL
- [ ] Implement `analyzeCode()` - POST /api/v1/analyze
- [ ] Implement `getAnalysis()` - GET /api/v1/analysis/{id}
- [ ] Implement `getFixes()` - POST /api/v1/fixes
- [ ] Add error handling
- [ ] Add request/response logging
- [ ] Implement retry logic for network failures

### 3.4 State Management (20 min)

#### File: `/frontend/src/store/analysisStore.ts`
- [ ] Create Zustand store with:
  - [ ] `analysis: AnalysisResult | null`
  - [ ] `selectedBugId: string | null`
  - [ ] `loading: boolean`
  - [ ] `error: string | null`
  - [ ] `actions`: setAnalysis, setSelectedBug, setLoading, setError

- [ ] Store methods:
  - [ ] `performAnalysis(request)` - Call API and update store
  - [ ] `clearAnalysis()` - Reset analysis
  - [ ] `selectBug(bugId)` - Select specific bug for detail view

### 3.5 React Components (40 min)

#### Component: `/frontend/src/components/AnalysisForm.tsx`
- [ ] Text area for GitHub PR URL or code input
- [ ] Language selector dropdown (Python, JavaScript, Java)
- [ ] "Analyze" button with loading state
- [ ] Clear button
- [ ] Input validation
- [ ] Error messages below input

#### Component: `/frontend/src/components/BugsList.tsx`
- [ ] Display list of bugs
- [ ] Show severity badge with color coding:
  - [ ] 🔴 CRITICAL - Red
  - [ ] 🟠 HIGH - Orange
  - [ ] 🟡 MEDIUM - Yellow
  - [ ] 🟢 LOW - Green
- [ ] Show bug count
- [ ] Click to select bug for details
- [ ] Filter by severity (optional)

#### Component: `/frontend/src/components/BugDetail.tsx`
- [ ] Display selected bug details:
  - [ ] Title and description
  - [ ] Code snippet with syntax highlighting
  - [ ] Severity level
  - [ ] Confidence score
  - [ ] Full explanation
- [ ] Show fix suggestion with code block
- [ ] Show alternative fixes (if available)
- [ ] Copy-to-clipboard for fixed code

#### Component: `/frontend/src/components/Dashboard.tsx`
- [ ] Combine analysis form and results display
- [ ] Show/hide results based on state
- [ ] Display loading spinner during analysis
- [ ] Show error messages
- [ ] Summary statistics (total bugs, by severity)

#### Component: `/frontend/src/components/CodeComparison.tsx`
- [ ] Side-by-side diff view:
  - [ ] Left: Original buggy code (red highlight)
  - [ ] Right: Fixed code (green highlight)
  - [ ] Show line numbers
  - [ ] Highlight differences

#### Component: `/frontend/src/components/LoadingSpinner.tsx`
- [ ] Animated spinner during API calls
- [ ] Loading message
- [ ] Optional timeout message

#### Component: `/frontend/src/components/Header.tsx`
- [ ] Logo/Brand name
- [ ] Navigation links
- [ ] Theme toggle (optional)

### 3.6 Pages (10 min)

#### Page: `/frontend/src/pages/HomePage.tsx`
- [ ] Main dashboard page
- [ ] Import Dashboard component
- [ ] Layout with header and content

### 3.7 Styling (15 min)

#### File: `/frontend/src/index.css`
- [ ] Configure Tailwind CSS
- [ ] Global styles
- [ ] Custom colors for severity levels
- [ ] Responsive breakpoints

#### File: `/frontend/src/components/CodeComparison.module.css` (Optional)
- [ ] Code block styling
- [ ] Diff highlighting
- [ ] Line number styling

### 3.8 Main App Entry (10 min)

#### File: `/frontend/src/App.tsx`
- [ ] Import HomePage
- [ ] Setup routing (React Router if needed)
- [ ] Global error boundary
- [ ] Provider setup (Zustand)

#### File: `/frontend/src/index.tsx`
- [ ] ReactDOM render
- [ ] Root component

### 3.9 Environment Configuration (5 min)

#### File: `/frontend/.env`
- [ ] Set `REACT_APP_API_URL` to backend URL

---

## ✅ Phase 4: Testing & Validation (30 min)

### 4.1 Backend Testing (15 min)
- [ ] Test GitHub service connection:
  - [ ] Verify GitHub token works
  - [ ] Fetch sample PR successfully
  - [ ] Parse PR diff correctly

- [ ] Test LLM integration:
  - [ ] Verify OpenAI API key works
  - [ ] Test prompt and response parsing
  - [ ] Check token counting

- [ ] Test API endpoints manually:
  - [ ] Use Postman or curl to test POST /api/v1/analyze
  - [ ] Verify response format matches schema
  - [ ] Test error handling (invalid input, API failures)

- [ ] Test code analyzer:
  - [ ] Parse sample Python code
  - [ ] Extract functions and classes
  - [ ] Detect syntax errors

### 4.2 Frontend Testing (10 min)
- [ ] Manual component testing:
  - [ ] Input form accepts text
  - [ ] Buttons are clickable
  - [ ] Loading spinner shows during requests
  - [ ] Results display correctly

- [ ] End-to-end flow:
  - [ ] Paste code → Analyze → View results
  - [ ] Click bug → See details
  - [ ] Verify code comparison works

- [ ] Error handling:
  - [ ] Network error handling
  - [ ] Invalid input handling
  - [ ] Empty state handling

### 4.3 Integration Testing (5 min)
- [ ] Full pipeline test:
  - [ ] Frontend → API → GitHub → LLM → Response → Frontend
  - [ ] Measure end-to-end time
  - [ ] Verify data integrity

---

## ✅ Phase 5: Deployment & Documentation (30 min)

### 5.1 Backend Deployment (15 min)
- [ ] Create `/backend/run.sh` or batch script:
  - [ ] Activate virtual environment
  - [ ] Set environment variables
  - [ ] Start Uvicorn server

- [ ] Test local deployment:
  - [ ] Backend runs on http://localhost:8000
  - [ ] API documentation available at /docs
  - [ ] Health check endpoint works

- [ ] Optional Docker setup:
  - [ ] Create Dockerfile
  - [ ] Build image
  - [ ] Test container

### 5.2 Frontend Deployment (10 min)
- [ ] Create start script:
  - [ ] Run `npm start` or build production version

- [ ] Build for production (optional):
  - [ ] Run `npm run build`
  - [ ] Verify build output

- [ ] Test frontend:
  - [ ] Frontend runs on http://localhost:3000
  - [ ] API calls go to backend correctly

### 5.3 Documentation (5 min)

#### File: `/README.md`
- [ ] Project overview
- [ ] Features list
- [ ] Prerequisites
- [ ] Setup instructions (both backend and frontend)
- [ ] Running the application
- [ ] API documentation
- [ ] Screenshot/demo GIFs
- [ ] Troubleshooting section
- [ ] Future improvements

#### File: `/backend/README_BACKEND.md`
- [ ] Backend setup
- [ ] API endpoints
- [ ] Environment variables
- [ ] Service descriptions
- [ ] Running tests

#### File: `/frontend/README_FRONTEND.md`
- [ ] Frontend setup
- [ ] Component structure
- [ ] State management
- [ ] Development workflow

#### File: `DEPLOYMENT.md`
- [ ] Local deployment instructions
- [ ] Docker deployment (if applicable)
- [ ] Environment variable checklist
- [ ] Troubleshooting deployment issues

---

## ✅ Phase 6: Final Polish & Demo Prep (30 min)

### 6.1 Code Quality (10 min)
- [ ] Remove console.log statements
- [ ] Add docstrings to functions
- [ ] Clean up unused imports
- [ ] Fix any linting errors
- [ ] Format code (Black for Python, Prettier for JS)

### 6.2 Performance Optimization (10 min)
- [ ] Add caching to reduce API calls
- [ ] Optimize code analyzer for speed
- [ ] Minify frontend assets
- [ ] Test response time (should be < 30 seconds)

### 6.3 UI/UX Polish (10 min)
- [ ] Add loading states
- [ ] Improve error messages
- [ ] Add empty states
- [ ] Ensure responsive design
- [ ] Test on mobile (if web)

---

## ✅ Phase 7: Demo & Deliverables (Optional - 30 min)

### 7.1 Demo Preparation
- [ ] Create demo script:
  - [ ] Sample PR URL to test
  - [ ] Expected bug detections
  - [ ] Fix demonstrations

- [ ] Test demo flow:
  - [ ] Paste code → Analyze → Results → Fix

### 7.2 Demo Materials
- [ ] Screenshots of:
  - [ ] Input form
  - [ ] Results dashboard
  - [ ] Bug details
  - [ ] Fix suggestions

- [ ] Optional: Create short video (3-5 minutes) showing:
  - [ ] Full workflow
  - [ ] Features demonstrated
  - [ ] Results quality

### 7.3 Final Checklist
- [ ] All files created and functional
- [ ] No critical errors
- [ ] Documentation complete
- [ ] Code is clean and readable
- [ ] Demo works end-to-end
- [ ] Performance targets met

---

## 🎯 Success Criteria (MVP Definition of Done)

✅ **Must Have:**
- [ ] Analyze GitHub PRs and code snippets
- [ ] Detect at least 3 types of bugs
- [ ] Generate AI-powered fixes
- [ ] Display results in web dashboard
- [ ] All features work end-to-end
- [ ] < 30 second analysis time
- [ ] README with setup instructions

✅ **Nice to Have:**
- [ ] Alternative fix suggestions
- [ ] Confidence scores
- [ ] Severity classification
- [ ] Code comparison view
- [ ] Responsive design
- [ ] Export results

---

## 📋 Dependencies Checklist

### Python Packages (Backend)
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
PyGithub==2.1.1
openai==1.3.0
python-dateutil==2.8.2
```

### Node Packages (Frontend)
```
react==18.2.0
react-dom==18.2.0
typescript==5.3.2
axios==1.6.0
zustand==4.4.0
react-router-dom==6.18.0
tailwindcss==3.3.0
```

---

## ⏱️ Time Breakdown

| Phase | Task | Time |
|-------|------|------|
| 1 | Setup & Environment | 1h |
| 2 | Backend Development | 5h |
| 3 | Frontend Development | 1.5h |
| 4 | Testing & Validation | 0.5h |
| 5 | Deployment | 0.5h |
| **Total** | **MVP Complete** | **8.5h** |

**Buffer for Issues:** 1.5 hours remaining for debugging, adjustments, and demos.

---

## 🚀 Quick Start After ToDos Complete

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Frontend (in new terminal)
cd frontend
npm install
npm start

# Access at http://localhost:3000
```

---

**This checklist is your roadmap. Use it with Copilot to generate code directly for each todo item. Break it down into smaller chunks and ask Copilot to generate specific functions/components.**
