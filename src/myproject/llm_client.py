"""LLM client module - interfaces with Anthropic Claude and OpenAI APIs."""

from typing import Any, Dict, Optional


async def call_llm(
    prompt: str,
    model: str = "claude-3-opus-20240229",
    provider: str = "anthropic",
) -> str:
    """Call LLM API with a prompt."""
    # Mock implementation for development
    return "Bug detected: Using || instead of 'or' operator in Python"


async def generate_bug_explanation(code: str, bug_description: str) -> str:
    """Generate detailed explanation for a bug."""
    return f"This code has an issue: {bug_description}"


async def generate_fix_explanation(old_code: str, new_code: str) -> str:
    """Generate explanation for a fix."""
    return f"Changed from '{old_code}' to '{new_code}'"
