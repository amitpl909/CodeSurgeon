"""Fix generator module - generates fixes for detected bugs."""

from typing import Any, Dict


def generate_fix(bug_type: str, code: str) -> Dict[str, Any]:
    """Generate a fix for a detected bug."""
    fixes = {
        "SYNTAX_ERROR": {
            "code": code.replace("||", "or"),
            "explanation": "Changed || operator to 'or' (correct Python syntax)",
        },
        "BEST_PRACTICE": {
            "code": code.replace("== None", "is None"),
            "explanation": "Changed '== None' to 'is None' (PEP 8 compliant)",
        },
    }
    return fixes.get(bug_type, {"code": code, "explanation": "No automatic fix available"})
