"""
Custom exceptions for CodeSurgeon backend.
"""


class CodeSurgeonError(Exception):
    """Base exception for CodeSurgeon."""

    pass


class GitHubAPIError(CodeSurgeonError):
    """GitHub API related errors."""

    pass


class LLMAnalysisError(CodeSurgeonError):
    """LLM analysis related errors."""

    pass


class CodeParseError(CodeSurgeonError):
    """Code parsing related errors."""

    pass


class InvalidInputError(CodeSurgeonError):
    """Invalid input errors."""

    pass


class ServiceTimeoutError(CodeSurgeonError):
    """Service timeout errors."""

    pass


class ValidationError(CodeSurgeonError):
    """Validation errors."""

    pass
