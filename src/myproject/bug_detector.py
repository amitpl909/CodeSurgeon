"""Bug detector module - identifies bugs using static analysis and LLM."""

from typing import Any, Dict


def detect_bugs(code: str, language: str = "python") -> list[Dict[str, Any]]:
    """Detect bugs in code using static analysis."""
    bugs = []

    # Static pattern detection
    if language == "python":
        if "||" in code:
            bugs.append(
                {
                    "type": "SYNTAX_ERROR",
                    "severity": "CRITICAL",
                    "description": "Using || instead of 'or' operator",
                    "line": 1,
                    "confidence": 0.95,
                }
            )

        if "== None" in code:
            bugs.append(
                {
                    "type": "BEST_PRACTICE",
                    "severity": "HIGH",
                    "description": "Use 'is None' instead of '== None'",
                    "line": 1,
                    "confidence": 0.92,
                }
            )

    return bugs
