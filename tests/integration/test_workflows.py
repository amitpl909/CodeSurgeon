"""Integration tests for API workflows."""

import pytest
from fastapi.testclient import TestClient

from src.myproject.api import app

client = TestClient(app)


def test_e2e_analyze_and_fix():
    """Test complete workflow: analyze -> get bugs -> generate fixes."""
    # Step 1: Analyze code
    response = client.post(
        "/api/v1/analyze",
        json={"code": "x = 1 || 2", "language": "python"},
    )
    assert response.status_code == 200
    analysis = response.json()
    assert len(analysis["bugs"]) >= 1

    # Step 2: Verify fixes exist
    bug_id = analysis["bugs"][0]["id"]
    assert bug_id in analysis["fixes"]
    primary_fix = analysis["fixes"][bug_id]["primary"]
    assert "or" in primary_fix["code"]


def test_multiple_bugs_in_single_analysis():
    """Test detection of multiple bugs."""
    code = """x = 1 || 2
if y == None:
    pass"""
    response = client.post(
        "/api/v1/analyze",
        json={"code": code, "language": "python"},
    )
    assert response.status_code == 200
    analysis = response.json()
    assert len(analysis["bugs"]) >= 2
