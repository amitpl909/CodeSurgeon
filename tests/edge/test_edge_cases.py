"""Edge case tests."""

import pytest
from fastapi.testclient import TestClient

from src.myproject.api import app

client = TestClient(app)


def test_whitespace_only_code():
    """Test code with only whitespace."""
    response = client.post(
        "/api/v1/analyze",
        json={"code": "   \n\t\n   ", "language": "python"},
    )
    assert response.status_code == 400


def test_very_long_code():
    """Test very long code snippet (stress test)."""
    long_code = "x = 1 || 2\n" * 1000  # 10KB
    response = client.post(
        "/api/v1/analyze",
        json={"code": long_code, "language": "python"},
    )
    # Should succeed or gracefully fail
    assert response.status_code in [200, 400, 503]


def test_unsupported_language():
    """Test unsupported language."""
    response = client.post(
        "/api/v1/analyze",
        json={"code": "print('hello')", "language": "rust"},
    )
    # Should fail or default to safe behavior
    assert response.status_code in [400, 200]


def test_special_characters_in_code():
    """Test code with special characters."""
    code = "x = '你好世界' || y"  # Unicode
    response = client.post(
        "/api/v1/analyze",
        json={"code": code, "language": "python"},
    )
    assert response.status_code in [200, 400]
