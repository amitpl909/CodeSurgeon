"""
Error handling middleware and utilities for FastAPI.
"""

import json
from datetime import datetime
from typing import Dict

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.exceptions import (
    CodeParseError,
    CodeSurgeonError,
    GitHubAPIError,
    InvalidInputError,
    LLMAnalysisError,
    ServiceTimeoutError,
    ValidationError,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """Global error handler middleware."""
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}},
        )


def create_error_response(
    status_code: int, code: str, message: str, details: str = None
) -> Dict:
    """Create standardized error response.

    Args:
        status_code: HTTP status code
        code: Error code
        message: Error message
        details: Additional details

    Returns:
        Error response dict
    """
    response = {
        "error": {
            "code": code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
    }

    if details:
        response["error"]["details"] = details

    return response


# Exception handlers
def handle_github_api_error(error: GitHubAPIError) -> Dict:
    """Handle GitHub API errors."""
    logger.error(f"GitHub API error: {error}")
    return create_error_response(
        status.HTTP_502_BAD_GATEWAY,
        "GITHUB_API_ERROR",
        "Failed to communicate with GitHub API",
        str(error),
    )


def handle_llm_analysis_error(error: LLMAnalysisError) -> Dict:
    """Handle LLM analysis errors."""
    logger.error(f"LLM analysis error: {error}")
    return create_error_response(
        status.HTTP_503_SERVICE_UNAVAILABLE,
        "LLM_SERVICE_ERROR",
        "Failed to analyze code with AI service",
        str(error),
    )


def handle_code_parse_error(error: CodeParseError) -> Dict:
    """Handle code parsing errors."""
    logger.error(f"Code parse error: {error}")
    return create_error_response(
        status.HTTP_400_BAD_REQUEST,
        "CODE_PARSE_ERROR",
        "Failed to parse provided code",
        str(error),
    )


def handle_invalid_input_error(error: InvalidInputError) -> Dict:
    """Handle invalid input errors."""
    logger.warning(f"Invalid input: {error}")
    return create_error_response(
        status.HTTP_400_BAD_REQUEST,
        "INVALID_INPUT",
        "Invalid request input",
        str(error),
    )


def handle_service_timeout_error(error: ServiceTimeoutError) -> Dict:
    """Handle service timeout errors."""
    logger.error(f"Service timeout: {error}")
    return create_error_response(
        status.HTTP_504_GATEWAY_TIMEOUT,
        "SERVICE_TIMEOUT",
        "Request timed out",
        str(error),
    )


def handle_validation_error(error: ValidationError) -> Dict:
    """Handle validation errors."""
    logger.warning(f"Validation error: {error}")
    return create_error_response(
        status.HTTP_400_BAD_REQUEST,
        "VALIDATION_ERROR",
        "Request validation failed",
        str(error),
    )


def handle_generic_codesurgeon_error(error: CodeSurgeonError) -> Dict:
    """Handle generic CodeSurgeon errors."""
    logger.error(f"CodeSurgeon error: {error}")
    return create_error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "CODESURGEON_ERROR",
        "An error occurred while processing your request",
        str(error),
    )
