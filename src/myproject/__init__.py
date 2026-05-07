# CodeSurgeon: AI-powered code analysis and bug detection

__version__ = "0.1.0"
__author__ = "CodeSurgeon Team"
__description__ = "AI-powered code analysis and fix generation"

from . import api, bug_detector, code_analyzer, fix_generator, github_analyzer, llm_client

__all__ = [
    "api",
    "bug_detector",
    "code_analyzer",
    "fix_generator",
    "github_analyzer",
    "llm_client",
]
