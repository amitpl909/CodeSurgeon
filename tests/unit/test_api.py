"""Unit tests for API module."""

import pytest
from fastapi.testclient import TestClient

from src.myproject.api import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "CodeSurgeon"


def test_analyze_code_basic():
    """Test basic code analysis."""
    response = client.post(
        "/api/v1/analyze",
        json={"code": "x = 1 || 2", "language": "python"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "bugs" in data
    assert len(data["bugs"]) >= 1
    assert data["language"] == "python"


def test_analyze_empty_code():
    """Test error on empty code."""
    response = client.post(
        "/api/v1/analyze",
        json={"code": "", "language": "python"},
    )
    assert response.status_code == 400


def test_analyze_missing_code():
    """Test error on missing code and PR URL."""
    response = client.post("/api/v1/analyze", json={})
    assert response.status_code == 400
