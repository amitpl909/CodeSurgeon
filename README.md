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

- Python 3.9+
- Node.js 18+
- GitHub Personal Access Token
- OpenAI API Key

### Setup (Backend)

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

## 📚 Documentation

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
