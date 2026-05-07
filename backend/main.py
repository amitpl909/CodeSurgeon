"""
CodeSurgeon - AI-powered GitHub bug repair agent
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from src.routes.analyze import router as analyze_router
from src.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="CodeSurgeon",
    description="AI-powered GitHub bug repair agent",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(analyze_router)


@app.on_event("startup")
async def startup_event():
    """App startup event."""
    logger.info("CodeSurgeon API starting up...")
    logger.info(f"Environment: {settings.api_env}")
    logger.info(f"CORS Origins: {settings.allowed_origins}")


@app.on_event("shutdown")
async def shutdown_event():
    """App shutdown event."""
    logger.info("CodeSurgeon API shutting down...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "CodeSurgeon",
        "description": "AI-powered GitHub bug repair agent",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_url": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_env == "development",
        log_level=settings.log_level.lower(),
    )
