"""User Story US-09: User analyzes code without GitHub token."""

import pytest


def test_us_09_code_analysis_without_github_token():
    """Given no GitHub token, when analyzing code snippet, then analysis succeeds."""
    # TODO: Implement using FastAPI TestClient
    # 1. Verify GITHUB_TOKEN is not set
    # 2. Send POST /api/v1/analyze with code snippet (not PR)
    # 3. Verify analysis succeeds
    pass


def test_us_09_github_pr_fails_without_token():
    """Verify GitHub PR mode fails gracefully without token."""
    # TODO: Send PR URL without token
    # Verify error message mentions "GitHub token not configured"
    pass
