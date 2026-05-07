"""Conftest - pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.myproject.api import app


@pytest.fixture(scope="session")
def client():
    """Provide FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_code():
    """Provide sample buggy code."""
    return "x = 1 || 2\nif y == None: pass"


@pytest.fixture
def sample_clean_code():
    """Provide sample clean code."""
    return "x = 1 or 2\nif y is None: pass"


@pytest.fixture
def mock_lLM(monkeypatch):
    """Mock LLM client for testing."""
    def mock_call_llm(*args, **kwargs):
        return "Mock LLM response"

    monkeypatch.setattr("src.myproject.llm_client.call_llm", mock_call_llm)
