"""User Story US-05: User submits GitHub PR URL for analysis."""

import pytest


def test_us_05_github_pr_analysis():
    """Given a GitHub PR URL, when analyzed, then PR files are analyzed."""
    # TODO: Implement using FastAPI TestClient with mock GitHub API
    # 1. Send POST /api/v1/analyze with pr_url
    # 2. Verify response includes bugs from multiple files
    pass


def test_us_05_aggregated_results():
    """Verify results are aggregated from all PR files."""
    # TODO: Verify bugs have correct file paths
    pass
