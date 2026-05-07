"""Unit tests for code analyzer module."""

import pytest

from src.myproject.code_analyzer import analyze, detect_patterns


def test_analyze_python_code():
    """Test Python code analysis."""
    result = analyze("x = 1 || 2", "python")
    assert result["language"] == "python"
    assert result["lines"] == 1


def test_detect_or_operator_pattern():
    """Test detection of || operator pattern."""
    patterns = detect_patterns("x = 1 || 2", "python")
    assert len(patterns) >= 1
    assert any(p["pattern"] == "||" for p in patterns)


def test_detect_none_comparison_pattern():
    """Test detection of == None pattern."""
    patterns = detect_patterns("if x == None: pass", "python")
    assert any(p["pattern"] == "== None" for p in patterns)
