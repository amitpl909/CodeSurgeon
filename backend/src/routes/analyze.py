"""
API routes for code analysis endpoints.
"""

import time
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from config import get_settings
from src.exceptions import (
    CodeParseError,
    GitHubAPIError,
    InvalidInputError,
    LLMAnalysisError,
)
from src.integrations.llm_client import LLMClient
from src.models.schemas import (
    AnalysisResponse,
    AnalysisSummary,
    AnalysisRequest,
    BugSeverity,
    ErrorResponse,
    FixRequest,
    FixResponse,
)
from src.services.bug_detector import BugDetector
from src.services.code_analyzer import CodeAnalyzer
from src.services.fix_generator import FixGenerator
from src.services.github_service import GitHubService
from src.utils.cache import cache
from src.utils.logger import get_logger
from src.utils.validators import validate_code, validate_github_url, validate_language

logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/v1", tags=["analysis"])

# Initialize services
github_service = None
llm_client = None
bug_detector = None
fix_generator = None


def _initialize_services():
    """Initialize services."""
    global github_service, llm_client, bug_detector, fix_generator

    try:
        github_service = GitHubService()
    except GitHubAPIError as e:
        logger.warning(f"GitHub service not available: {e}")
        github_service = None

    try:
        llm_client = LLMClient()
    except LLMAnalysisError as e:
        logger.warning(f"LLM client not available: {e}")
        llm_client = None

    bug_detector = BugDetector(llm_client)
    fix_generator = FixGenerator(llm_client)


@router.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    _initialize_services()
    logger.info("API services initialized")


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: AnalysisRequest) -> AnalysisResponse:
    """Analyze code for bugs.

    Args:
        request: Analysis request with code or PR URL

    Returns:
        Analysis response with detected bugs

    Raises:
        HTTPException: If analysis fails
    """
    start_time = time.time()

    try:
        # Determine input type and get code
        code = None

        if request.type == "pr":
            # Validate GitHub URL
            validate_github_url(request.input)

            if not github_service:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="GitHub service not available",
                )

            # Get PR code from GitHub
            parsed_url = github_service.parse_pr_url(request.input)
            diff = github_service.get_pr_diff(request.input)
            code = diff[:10000]  # Limit to 10k chars

            logger.info(f"Fetched PR code from GitHub")

        elif request.type == "snippet":
            # Validate code snippet
            validate_code(request.input)
            code = request.input

        else:
            raise InvalidInputError(f"Invalid analysis type: {request.type}")

        # Validate language
        language = request.language if request.language != "auto" else "python"
        validate_language(language)

        # Analyze code
        bugs = bug_detector.detect_bugs(code, language, request.context)

        # Calculate summary
        severity_counts = {
            BugSeverity.CRITICAL: 0,
            BugSeverity.HIGH: 0,
            BugSeverity.MEDIUM: 0,
            BugSeverity.LOW: 0,
        }

        for bug in bugs:
            severity_counts[bug.severity] += 1

        analysis_time_ms = int((time.time() - start_time) * 1000)

        summary = AnalysisSummary(
            total_bugs=len(bugs),
            critical=severity_counts[BugSeverity.CRITICAL],
            high=severity_counts[BugSeverity.HIGH],
            medium=severity_counts[BugSeverity.MEDIUM],
            low=severity_counts[BugSeverity.LOW],
            analysis_time_ms=analysis_time_ms,
        )

        response = AnalysisResponse(
            id=uuid.uuid4(),
            status="success",
            bugs=bugs,
            summary=summary,
        )

        # Cache response
        cache.set(str(response.id), response.dict(), ttl=3600)

        logger.info(f"Analysis completed: {len(bugs)} bugs found in {analysis_time_ms}ms")
        return response

    except InvalidInputError as e:
        logger.error(f"Invalid input: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except GitHubAPIError as e:
        logger.error(f"GitHub API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch code from GitHub",
        )
    except CodeParseError as e:
        logger.error(f"Code parse error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except LLMAnalysisError as e:
        logger.error(f"LLM analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI analysis service is unavailable",
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str) -> AnalysisResponse:
    """Get analysis results by ID.

    Args:
        analysis_id: Analysis ID

    Returns:
        Analysis response

    Raises:
        HTTPException: If analysis not found
    """
    try:
        cached = cache.get(analysis_id)

        if not cached:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found",
            )

        return AnalysisResponse(**cached)

    except Exception as e:
        logger.error(f"Error retrieving analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving analysis",
        )


@router.post("/fixes", response_model=FixResponse)
async def generate_fixes(request: FixRequest) -> FixResponse:
    """Generate fixes for a specific bug.

    Args:
        request: Fix request with bug ID and analysis ID

    Returns:
        Fix suggestions

    Raises:
        HTTPException: If generation fails
    """
    try:
        if not llm_client:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Fix generation service not available",
            )

        # Get cached analysis
        analysis_data = cache.get(str(request.analysis_id))
        if not analysis_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found",
            )

        analysis = AnalysisResponse(**analysis_data)

        # Find the bug
        bug = None
        for b in analysis.bugs:
            if b.id == request.bug_id:
                bug = b
                break

        if not bug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bug not found",
            )

        # Generate fixes
        primary_fix = fix_generator.generate_fix(bug.code_snippet, bug)
        alternatives = fix_generator.generate_alternatives(bug.code_snippet, bug, count=2)

        response = FixResponse(
            bug_id=bug.id,
            fix=primary_fix,
            alternatives=alternatives if alternatives else None,
        )

        logger.info(f"Generated fixes for bug {bug.id}")
        return response

    except LLMAnalysisError as e:
        logger.error(f"Fix generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Fix generation failed",
        )
    except Exception as e:
        logger.error(f"Error generating fixes: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating fixes",
        )


@router.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        Health status
    """
    from src.models.schemas import HealthCheckResponse

    services_status = {
        "api": "operational",
        "github": "operational" if github_service else "unavailable",
        "llm": "operational" if llm_client else "unavailable",
    }

    return HealthCheckResponse(status="healthy", services=services_status)
