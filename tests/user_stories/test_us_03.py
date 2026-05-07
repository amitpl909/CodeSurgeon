"""User Story US-03 [ERROR PATH]: User enters empty code and sees validation error."""

import pytest


def test_us_03_empty_code_validation():
    """Given empty code input, when analyzed, then error is shown."""
    # TODO: Implement using FastAPI TestClient
    # 1. Send POST /api/v1/analyze with code=""
    # 2. Verify response is 400 Bad Request
    # 3. Verify error message says "Please enter some code"
    pass
