"""User Story US-04 [ERROR PATH]: User submits code with syntax error."""

import pytest


def test_us_04_syntax_error_handling():
    """Given invalid syntax, when analyzed, then error is shown."""
    # TODO: Implement using FastAPI TestClient
    # 1. Send POST /api/v1/analyze with code="def f(: pass"
    # 2. Verify response is 400 Bad Request
    # 3. Verify error message mentions "syntax"
    pass
