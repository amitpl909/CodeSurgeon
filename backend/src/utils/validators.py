"""
Validator utilities for CodeSurgeon.
"""

import re
from typing import Optional

from src.exceptions import InvalidInputError
from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_github_url(url: str) -> bool:
    """Validate GitHub PR URL format.

    Args:
        url: URL to validate

    Returns:
        True if valid, raises InvalidInputError otherwise

    Raises:
        InvalidInputError: If URL is invalid
    """
    # Pattern: https://github.com/owner/repo/pull/number
    pattern = r"^https://github\.com/[\w\-]+/[\w\-\.]+/pull/\d+/?$"

    if not re.match(pattern, url):
        raise InvalidInputError(
            f"Invalid GitHub PR URL. Expected format: "
            f"https://github.com/user/repo/pull/123"
        )

    return True


def validate_code(code: str) -> bool:
    """Validate code snippet.

    Args:
        code: Code to validate

    Returns:
        True if valid

    Raises:
        InvalidInputError: If code is invalid
    """
    if not code or not isinstance(code, str):
        raise InvalidInputError("Code must be a non-empty string")

    if len(code) > 50000:  # 50k character limit
        raise InvalidInputError("Code snippet is too large (max 50,000 characters)")

    return True


def validate_language(language: str) -> bool:
    """Validate programming language.

    Args:
        language: Language to validate

    Returns:
        True if valid

    Raises:
        InvalidInputError: If language is invalid
    """
    supported_languages = {
        "python",
        "javascript",
        "typescript",
        "java",
        "go",
        "rust",
        "cpp",
        "c",
        "csharp",
        "php",
        "auto",
    }

    if language.lower() not in supported_languages:
        raise InvalidInputError(
            f"Unsupported language: {language}. "
            f"Supported: {', '.join(supported_languages)}"
        )

    return True


def parse_github_url(url: str) -> Optional[dict]:
    """Parse GitHub PR URL to extract components.

    Args:
        url: GitHub PR URL

    Returns:
        Dict with owner, repo, pr_number or None if invalid

    Example:
        >>> parse_github_url("https://github.com/user/repo/pull/123")
        {'owner': 'user', 'repo': 'repo', 'pr_number': 123}
    """
    try:
        validate_github_url(url)
        parts = url.rstrip("/").split("/")
        return {
            "owner": parts[3],
            "repo": parts[4],
            "pr_number": int(parts[6]),
        }
    except (IndexError, ValueError) as e:
        logger.error(f"Error parsing GitHub URL: {e}")
        return None
