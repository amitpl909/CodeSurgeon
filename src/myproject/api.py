"""FastAPI application entry point for CodeSurgeon."""

import os
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# ============================================================================
# Request/Response Models
# ============================================================================


class AnalyzeRequest(BaseModel):
    """Request model for code analysis."""

    code: Optional[str] = None
    language: Optional[str] = "python"
    pr_url: Optional[str] = None
    github_token: Optional[str] = None


class BugModel(BaseModel):
    """Bug detection result."""

    id: str
    type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    line: int
    description: str
    confidence: float


class FixModel(BaseModel):
    """Generated fix."""

    code: str
    explanation: str


class AnalysisResult(BaseModel):
    """Complete analysis result."""

    id: str
    code_snippet: str
    language: str
    bugs: list[BugModel]
    fixes: Dict[str, Dict[str, Any]]
    analysis_time_ms: int
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    timestamp: str


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="CodeSurgeon",
    description="AI-powered code analysis and fix generation",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Mock Analysis Functions (Development Mode)
# ============================================================================


def mock_analyze_code(code: str, language: str) -> Dict[str, Any]:
    """Mock code analysis (for development without LLM)."""
    bugs = []

    # Pattern 1: || operator in Python
    if language == "python" and "||" in code:
        bugs.append(
            {
                "id": f"bug-{uuid.uuid4()}",
                "type": "SYNTAX_ERROR",
                "severity": "CRITICAL",
                "line": code.split("\n")[0].find("||") > -1 and 1 or 2,
                "description": "Using || instead of 'or' operator in Python",
                "confidence": 0.95,
            }
        )

    # Pattern 2: == None instead of is None
    if language == "python" and "== None" in code:
        bugs.append(
            {
                "id": f"bug-{uuid.uuid4()}",
                "type": "BEST_PRACTICE",
                "severity": "HIGH",
                "line": 1,
                "description": "Use 'is None' instead of '== None' for None comparison",
                "confidence": 0.92,
            }
        )

    # Pattern 3: Unused variable
    if language == "python" and "x = 1" in code and "x" not in code[code.find("x = 1") + 5 :]:
        bugs.append(
            {
                "id": f"bug-{uuid.uuid4()}",
                "type": "UNUSED_VAR",
                "severity": "LOW",
                "line": 1,
                "description": "Variable 'x' is assigned but never used",
                "confidence": 0.88,
            }
        )

    return {
        "bugs": bugs,
        "language": language,
        "code_snippet": code[:500],  # Truncate for display
    }


def mock_generate_fix(bug_id: str, bug_type: str, code: str) -> Dict[str, Any]:
    """Mock fix generation."""
    fixes = {
        "SYNTAX_ERROR": {
            "code": code.replace("||", "or"),
            "explanation": "Changed || operator to 'or' (correct Python syntax)",
        },
        "BEST_PRACTICE": {
            "code": code.replace("== None", "is None"),
            "explanation": "Changed '== None' to 'is None' (PEP 8 style)",
        },
        "UNUSED_VAR": {
            "code": "# TODO: Remove unused variable 'x'",
            "explanation": "Remove or use the variable",
        },
    }
    return fixes.get(bug_type, {"code": code, "explanation": "No fix available"})


# ============================================================================
# API Routes
# ============================================================================


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="CodeSurgeon",
        timestamp=datetime.utcnow().isoformat() + "Z",
    )


@app.post("/api/v1/analyze", response_model=AnalysisResult)
async def analyze_code(request: AnalyzeRequest) -> AnalysisResult:
    """Analyze code for bugs and generate fixes."""
    import time

    start_time = time.time()

    # Validate input
    if not request.code and not request.pr_url:
        raise HTTPException(status_code=400, detail="Code or PR URL required")

    if request.code and not request.code.strip():
        raise HTTPException(status_code=400, detail="Please enter some code")

    # Mock analysis
    code = request.code or "# GitHub PR content"
    language = request.language or "python"

    analysis = mock_analyze_code(code, language)

    # Generate fixes for each bug
    fixes = {}
    for bug in analysis["bugs"]:
        fix = mock_generate_fix(bug["id"], bug["type"], code)
        fixes[bug["id"]] = {
            "primary": fix,
            "alternatives": [
                {
                    "code": fix["code"],
                    "explanation": f"Alternative approach: {fix['explanation']}",
                }
            ],
        }

    analysis_time_ms = int((time.time() - start_time) * 1000)

    return AnalysisResult(
        id=str(uuid.uuid4()),
        code_snippet=code[:500],
        language=language,
        bugs=[BugModel(**bug) for bug in analysis["bugs"]],
        fixes=fixes,
        analysis_time_ms=analysis_time_ms,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )


@app.get("/api/v1/analysis/{analysis_id}")
async def get_analysis(analysis_id: str) -> Dict[str, Any]:
    """Retrieve cached analysis result."""
    # In production, fetch from cache (Redis, etc.)
    raise HTTPException(status_code=404, detail="Analysis not found")


@app.post("/api/v1/fixes")
async def generate_fixes(bug_id: str, code: str) -> Dict[str, Any]:
    """Generate fixes for a specific bug."""
    # Mock fix generation
    return {
        "primary_fix": {
            "code": code.replace("||", "or"),
            "explanation": "Changed || to 'or'",
        },
        "alternatives": [],
        "confidence": 0.72,
    }


@app.get("/")
async def serve_frontend() -> FileResponse:
    """Serve frontend HTML."""
    frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend/index_simple.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path, media_type="text/html")
    return JSONResponse({"message": "CodeSurgeon API - Frontend not found"}, status_code=404)


@app.get("/api/v1")
async def api_root() -> Dict[str, Any]:
    """API root endpoint."""
    return {
        "service": "CodeSurgeon",
        "version": "0.1.0",
        "endpoints": {
            "health": "/api/v1/health",
            "analyze": "/api/v1/analyze",
            "analysis": "/api/v1/analysis/{id}",
            "fixes": "/api/v1/fixes",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
