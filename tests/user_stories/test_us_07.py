"""User Story US-07 [ERROR PATH]: API returns timeout error for slow LLM."""

import pytest


def test_us_07_llm_timeout_error():
    """Given LLM is slow, when timeout occurs, then error is shown."""
    # TODO: Implement using mock that simulates timeout
    # 1. Mock LLM to timeout
    # 2. Send POST /api/v1/analyze
    # 3. Verify response is 503 Service Unavailable
    # 4. Verify UI remains responsive (no hang)
    pass
