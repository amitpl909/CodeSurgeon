"""Unit tests for bug detector module."""

import pytest

from src.myproject.bug_detector import detect_bugs


def test_detect_or_operator_bug():
    """Test detection of || operator bug."""
    bugs = detect_bugs("x = 1 || 2", "python")
    assert len(bugs) >= 1
    critical_bugs = [b for b in bugs if b["severity"] == "CRITICAL"]
    assert len(critical_bugs) >= 1


def test_detect_none_comparison_bug():
    """Test detection of == None bug."""
    bugs = detect_bugs("if x == None: pass", "python")
    high_bugs = [b for b in bugs if b["severity"] == "HIGH"]
    assert len(high_bugs) >= 1


def test_no_bugs_in_clean_code():
    """Test that clean code produces no bugs."""
    bugs = detect_bugs("x = 1 or 2", "python")
    # Clean code should have no || or == None patterns
    assert len([b for b in bugs if b["severity"] == "CRITICAL"]) == 0
