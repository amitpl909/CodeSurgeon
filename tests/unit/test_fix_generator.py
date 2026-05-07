"""Unit tests for fix generator module."""

import pytest

from src.myproject.fix_generator import generate_fix


def test_generate_or_operator_fix():
    """Test fix generation for || operator."""
    code = "x = 1 || 2"
    fix = generate_fix("SYNTAX_ERROR", code)
    assert fix["code"] == "x = 1 or 2"
    assert "or" in fix["explanation"].lower()


def test_generate_none_comparison_fix():
    """Test fix generation for == None."""
    code = "if x == None: pass"
    fix = generate_fix("BEST_PRACTICE", code)
    assert fix["code"] == "if x is None: pass"
    assert "is None" in fix["explanation"]
