"""Code analyzer module - parses and analyzes code for patterns."""

from typing import Any, Dict


def analyze(code: str, language: str = "python") -> Dict[str, Any]:
    """Analyze code structure and extract patterns."""
    return {
        "code": code,
        "language": language,
        "lines": len(code.split("\n")),
        "chars": len(code),
    }


def detect_patterns(code: str, language: str = "python") -> list[Dict[str, Any]]:
    """Detect known problematic patterns in code."""
    patterns = []

    if language == "python":
        # Pattern: || operator (should be 'or')
        if "||" in code:
            patterns.append({"pattern": "||", "replacement": "or", "severity": "CRITICAL"})

        # Pattern: == None (should be 'is None')
        if "== None" in code:
            patterns.append({"pattern": "== None", "replacement": "is None", "severity": "HIGH"})

    return patterns
