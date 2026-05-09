"""
CodeSurgeon - Simplified FastAPI Backend (Testing Mode)
This is a minimal version for quick testing without heavy dependencies
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="CodeSurgeon API",
    description="AI-Powered GitHub Bug Repair Agent",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data storage
analysis_results = {}

# ============================================================================
# Data Models (Simple Dicts)
# ============================================================================

def create_bug(file_path, line_num, bug_type, severity, description):
    """Create a bug object"""
    return {
        "id": str(uuid.uuid4()),
        "file": file_path,
        "line": line_num,
        "type": bug_type,
        "severity": severity,
        "description": description,
        "confidence": 0.85
    }

def create_fix(bug_id, code, explanation):
    """Create a fix object"""
    return {
        "id": str(uuid.uuid4()),
        "bug_id": bug_id,
        "code": code,
        "explanation": explanation,
        "confidence": 0.9
    }

# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "CodeSurgeon API",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/analyze")
async def analyze_code(request_data: dict):
    """Analyze code and detect bugs"""
    try:
        code = request_data.get("code", "")
        language = request_data.get("language", "python")
        analysis_id = str(uuid.uuid4())
        
        # Mock analysis results
        bugs = []
        if "||" in code:
            bugs.append(create_bug(
                "main.py", 5, "SYNTAX_ERROR",
                "CRITICAL",
                "Using || instead of 'or' operator in Python"
            ))
        
        if "None ==" in code:
            bugs.append(create_bug(
                "main.py", 10, "BEST_PRACTICE",
                "HIGH",
                "Should use 'is None' instead of '== None'"
            ))
        
        if not bugs:
            bugs.append(create_bug(
                "main.py", 1, "CODE_SMELL",
                "MEDIUM",
                "Consider adding type hints to function parameters"
            ))
        
        result = {
            "id": analysis_id,
            "code": code[:500],
            "language": language,
            "bugs": bugs,
            "analysis_time_ms": 250,
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache result
        analysis_results[analysis_id] = result
        
        return result
    
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

@app.get("/api/v1/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get cached analysis result"""
    if analysis_id in analysis_results:
        return analysis_results[analysis_id]
    
    return JSONResponse(
        status_code=404,
        content={"error": "Analysis not found"}
    )

@app.post("/api/v1/fixes")
async def generate_fixes(request_data: dict):
    """Generate fixes for bugs"""
    try:
        bug_id = request_data.get("bug_id", "")
        code = request_data.get("code", "")
        
        # Mock fixes
        fixes = []
        
        if "||" in code:
            fixes.append(create_fix(
                bug_id,
                code.replace("||", " or "),
                "Changed || operator to 'or' which is the correct Python syntax"
            ))
        
        if "None ==" in code:
            fixes.append(create_fix(
                bug_id,
                code.replace("None ==", "is None"),
                "Changed == None to 'is None' for better Python idiom"
            ))
        
        if not fixes:
            fixes.append(create_fix(
                bug_id,
                f"def function(param: str) -> str:\n    {code}",
                "Added type hints for better code clarity"
            ))
        
        return {
            "bug_id": bug_id,
            "primary_fix": fixes[0] if fixes else None,
            "alternatives": fixes[1:] if len(fixes) > 1 else [],
            "confidence": 0.85
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

@app.get("/docs")
async def api_docs():
    """Redirect to OpenAPI docs"""
    return JSONResponse(content={"redirect": "/api/v1/docs"})

# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    print("🚀 CodeSurgeon API starting...")

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 CodeSurgeon API shutting down...")

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 CodeSurgeon API - Testing Mode")
    print("=" * 60)
    print("\n📊 Server Configuration:")
    print(f"  Host: 0.0.0.0")
    print(f"  Port: 8000")
    print(f"  API URL: http://localhost:8000")
    print(f"  Docs URL: http://localhost:8000/docs")
    print(f"  API Version: v1")
    print("\n🌐 Endpoints:")
    print("  GET  /api/v1/health - Server health check")
    print("  POST /api/v1/analyze - Analyze code for bugs")
    print("  GET  /api/v1/analysis/{id} - Get analysis results")
    print("  POST /api/v1/fixes - Generate fixes for bugs")
    print("\n💡 Usage:")
    print("  1. Start frontend: npm run dev (port 3000)")
    print("  2. API will run on port 8000")
    print("  3. Open http://localhost:3000 in browser")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
