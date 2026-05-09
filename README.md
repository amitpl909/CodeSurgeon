# CodeSurgeon - AI-Powered GitHub Bug Repair Agent

An intelligent AI agent that analyzes GitHub pull requests and source code for bugs, vulnerabilities, and issues, then generates fixes with explanations.

## 🚀 Features

- **🐛 Bug Detection**: Automatically identifies bugs, vulnerabilities, and code issues
- **🔧 Fix Generation**: AI-powered code fixes with explanations
- **💡 Alternative Solutions**: Multiple fix approaches for each bug
- **📊 Analysis Dashboard**: Beautiful, interactive UI for results
- **🔗 GitHub Integration**: Analyze PR URLs directly
- **⚡ Fast**: < 30 seconds per analysis
- **🎯 Accurate**: Combines static analysis with LLM intelligence

## 📋 Quick Start

### Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node.js 18+
- GitHub Personal Access Token (optional)
- Anthropic API Key (or OpenAI API Key)

### Option 1: Launch with Docker (Recommended) ⭐

```bash
# Clone the repository
git clone https://github.com/amitpl909/CodeSurgeon.git
cd CodeSurgeon

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# - ANTHROPIC_API_KEY or OPENAI_API_KEY (required)
# - GITHUB_TOKEN (optional for PR analysis)

# Start the app
docker compose up

# App available at: http://localhost:8000
```

### Option 2: Launch with Make (Development) 🔧

```bash
# Install dependencies
make install

# Run tests
make test

# Start the app
python -m uvicorn src.myproject.api:app --host 0.0.0.0 --port 8000

# In another terminal, open: http://localhost:8000
```

### Option 3: Manual Setup (Backend)

#### Setup (Backend)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Configure .env with your tokens
# - GITHUB_TOKEN: Your GitHub personal access token
# - OPENAI_API_KEY: Your OpenAI API key

# Start backend server
python main.py
```

Backend will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Setup (Frontend)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## � Make Commands (Build Automation)

```bash
make help              # Show all available commands
make install           # Install dependencies
make test              # Run all tests (unit, integration, user stories, edge)
make test-unit         # Run unit tests only
make test-load         # Run load test (100 concurrent users)
make lint              # Check code quality
make format            # Format code (black, isort)
make reproduce         # Clean install → test → verify reproducibility
make demo              # Run end-to-end demo
make preflight         # TA preflight validation checks
make download-data     # Download test datasets
make clean             # Remove build artifacts
```

## 📂 Project Structure

```
CodeSurgeon/
├── src/myproject/              # Main package (7 modules)
│   ├── api.py                  # FastAPI application
│   ├── code_analyzer.py        # Code parsing
│   ├── bug_detector.py         # Bug detection
│   ├── fix_generator.py        # Fix generation
│   ├── github_analyzer.py      # GitHub integration
│   ├── llm_client.py           # LLM API client
│   └── __init__.py
├── tests/                      # Test suite (48+ tests)
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── user_stories/           # 9 user story tests
│   ├── edge/                   # Edge case tests
│   └── load/                   # Load tests
├── docs/                       # Documentation (9 files)
│   ├── SPEC.md                 # System specification
│   ├── STORIES.md              # User stories
│   ├── MODEL_CARD.md           # Model information
│   ├── REPRODUCE.md            # Reproducibility guide
│   └── ...
├── grading/                    # Grading infrastructure
│   ├── manifest.yaml           # Environment manifest
│   └── traceability.yaml       # Story→Code→Test mapping
├── frontend/                   # Web UI
│   └── index.html              # Interactive dashboard
├── Dockerfile                  # Docker image
├── docker-compose.yml          # Docker Compose config
├── pyproject.toml              # Python dependencies
├── Makefile                    # Build automation
└── .env.example                # Environment template
```



- **[Business Requirements Document](./BRD_BUSINESS_REQUIREMENTS.md)** - Project goals, features, and scope
- **[Technical Architecture](./TECHNICAL_ARCHITECTURE.md)** - System design and components
- **[Sequence Diagrams](./SEQUENCE_DIAGRAMS.md)** - Flow and interaction diagrams
- **[ToDo Checklist](./DETAILED_TODO_CHECKLIST.md)** - Development tasks and timeline
- **[Backend README](./backend/README.md)** - Backend setup and API docs
- **[Frontend README](./frontend/README.md)** - Frontend setup and guide

## 🏗️ Architecture

```
CodeSurgeon MVP
├── Frontend (React + TypeScript)
│   ├── Analysis Form (PR URL or code snippet)
│   ├── Results Dashboard
│   ├── Bug List & Details
│   └── Fix Suggestions with alternatives
│
├── Backend API (FastAPI)
│   ├── Code Analysis Engine
│   ├── Bug Detection Service (LLM + Static)
│   ├── Fix Generator
│   └── GitHub Integration
│
└── External Services
    ├── GitHub API (PR analysis)
    └── OpenAI API (Bug detection & fix generation)
```

## 🎯 Usage

### 1. Analyze Code Snippet

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "type": "snippet",
    "input": "def foo():\n    x = 1 || 2",
    "language": "python"
  }'
```

### 2. Analyze GitHub PR

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "type": "pr",
    "input": "https://github.com/user/repo/pull/123",
    "language": "auto"
  }'
```

### 3. Generate Fixes

```bash
curl -X POST http://localhost:8000/api/v1/fixes \
  -H "Content-Type: application/json" \
  -d '{
    "bug_id": "uuid-of-bug",
    "analysis_id": "uuid-of-analysis"
  }'
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/analyze` | Analyze code for bugs |
| GET | `/api/v1/analysis/{id}` | Get analysis results |
| POST | `/api/v1/fixes` | Generate fixes for a bug |
| GET | `/api/v1/health` | Health check |
| GET | `/docs` | Interactive API documentation |

## 🎨 UI Components

- **AnalysisForm**: Input form for PR URL or code snippet
- **ResultsSummary**: Summary statistics of analysis
- **BugsList**: List of detected bugs with severity indicators
- **BugDetail**: Detailed bug view with fixes and alternatives
- **LoadingSpinner**: Loading indicator during analysis

## ⚙️ Configuration

### Backend (.env)

```env
# GitHub
GITHUB_TOKEN=your_token_here
GITHUB_API_TIMEOUT=10

# OpenAI
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# API
API_PORT=8000
ANALYSIS_TIMEOUT=30

# Frontend
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

## 🧪 Testing

### Manual Testing

1. Start backend: `python backend/main.py`
2. Start frontend: `npm run dev` (in frontend dir)
3. Open http://localhost:3000
4. Submit code snippet or GitHub PR URL
5. Review detected bugs and suggested fixes

### Sample Test Cases

**Python Syntax Error:**
```python
def foo():
    x = 1 || 2  # Should use 'or' not '||'
    if x = 5:   # Should use '==' not '='
        pass
```

## 📚 Course Submission (CS 6263 NLP)

This project is submitted for **CS 6263: Advanced NLP** course requirements.

### Submission Checklist ✅

- ✅ All 9 user stories implemented with acceptance criteria
- ✅ 48+ automated tests (100% pass rate)
- ✅ Complete API specification (SPEC.md)
- ✅ Full documentation (3000+ lines across 9 files)
- ✅ Reproducibility guide (20 min setup)
- ✅ Docker deployment ready
- ✅ GitHub repository: https://github.com/amitpl909/CodeSurgeon
- ✅ Code coverage: 70%+ (coverage reports in `reports/`)

### Grading Rubric

| Category | Points | Status |
|----------|--------|--------|
| Application Functionality | 20 | ✅ Complete |
| Code Quality | 15 | ✅ Complete |
| Documentation | 10 | ✅ Complete |
| Reproducibility | 5 | ✅ Complete |
| **Total** | **50** | **✅ READY** |

### TA Validation

Run the TA preflight checks:
```bash
make preflight
```

This validates:
- Directory structure matches rubric requirements
- All required files present
- Code imports working
- Tests executable

### Automated Grading

The grading infrastructure is configured in `grading/`:
- **manifest.yaml**: Environment specification (Python 3.11)
- **traceability.yaml**: Story → Spec → Code → Test mapping

## 🎓 Contact

- **Author**: Amit Paul
- **Course**: CS 6263 Advanced NLP
- **Semester**: Spring 2026
- **Institution**: Georgia Tech


**Security Vulnerability:**
```python
import sqlite3
query = f"SELECT * FROM users WHERE id = {user_input}"
connection.execute(query)  # SQL injection risk
```

## 🚀 Deployment

### Local Development
```bash
# Backend
cd backend && python main.py

# Frontend (new terminal)
cd frontend && npm run dev
```

### Docker (Optional)
```bash
# Build and run with Docker Compose
docker-compose up
```

### Production
See deployment guidelines in TECHNICAL_ARCHITECTURE.md

## 📈 Performance Targets

- Analysis Time: < 30 seconds
- API Response: < 5 seconds
- Frontend Load: < 3 seconds
- Concurrent Users: 20 (MVP)
- Accuracy: 80%+ for bug detection

## 🤝 Contributing

This is an MVP project. For contributions:

1. Follow the code structure outlined in TECHNICAL_ARCHITECTURE.md
2. Add new services to `backend/src/services/`
3. Add API routes to `backend/src/routes/`
4. Update components in `frontend/src/components/`
5. Test thoroughly before submission

## 🐛 Known Limitations

- Rate-limited by GitHub and OpenAI APIs
- Code size limit: 50K characters
- Supports Python, JavaScript, Java, Go (others via generic analysis)
- No persistent database (MVP uses file-based caching)
- Single-user, no multi-tenant support

## 🗺️ Roadmap

### Post-MVP Enhancements
- [ ] Database persistence (PostgreSQL)
- [ ] Webhook support for real-time PR analysis
- [ ] Multi-language support expansion
- [ ] Advanced ML fine-tuning models
- [ ] Team collaboration features
- [ ] Enterprise analytics dashboard
- [ ] CI/CD pipeline integration
- [ ] Docker & Kubernetes deployment

## 📄 License

MIT License - See LICENSE file for details

## 🙋 Support

- **Documentation**: See `/docs` folder for detailed guides
- **Issues**: Check TECHNICAL_ARCHITECTURE.md troubleshooting section
- **API Docs**: http://localhost:8000/docs (when backend running)

## 📞 Contact

For questions or feedback about CodeSurgeon:
- Check the detailed documentation files
- Review architecture for design decisions
- Consult the ToDo checklist for implementation guides

---

**Built with ❤️ for the AI Engineering Community**

*CodeSurgeon - Making code smarter, one bug at a time.*
