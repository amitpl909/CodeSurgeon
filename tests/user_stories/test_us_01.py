"""User Story US-01: User submits code snippet and receives bug analysis."""

import pytest


def test_us_01_analyze_code_snippet():
    """Given code is submitted, when analyzed, then bugs are detected."""
    # TODO: Implement using FastAPI TestClient
    # 1. Send POST /api/v1/analyze with code "x = 1 || 2"
    # 2. Verify response has 1 bug with severity CRITICAL
    # 3. Verify bug description mentions "||"
    pass


def test_us_01_analysis_timing():
    """Verify analysis completes within 5 seconds."""
    # TODO: Measure analysis_time_ms and assert < 5000
    pass
