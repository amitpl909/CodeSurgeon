"""
LLM client integration for CodeSurgeon.
"""

import time
from typing import List, Optional

from openai import APIError, RateLimitError, Timeout

from config import get_settings
from src.exceptions import LLMAnalysisError, ServiceTimeoutError
from src.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class LLMClient:
    """Client for LLM interactions (OpenAI/Claude)."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize LLM client.

        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4, gpt-3.5-turbo, etc.)
        """
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model

        if not self.api_key:
            raise LLMAnalysisError("OpenAI API key not configured")

        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=self.api_key)
            logger.info(f"LLM client initialized with model: {self.model}")
        except Exception as e:
            raise LLMAnalysisError(f"Failed to initialize LLM client: {e}")

    def analyze_code(self, code: str, language: str = "python", context: Optional[str] = None) -> str:
        """Analyze code for bugs using LLM.

        Args:
            code: Source code to analyze
            language: Programming language
            context: Additional context

        Returns:
            LLM analysis response

        Raises:
            LLMAnalysisError: If analysis fails
            ServiceTimeoutError: If request times out
        """
        prompt = self._build_analysis_prompt(code, language, context)

        try:
            response = self._call_llm(
                [
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer detecting bugs and issues in code.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )

            logger.info("Code analysis completed successfully")
            return response

        except Timeout:
            raise ServiceTimeoutError("LLM request timed out")
        except RateLimitError as e:
            logger.warning(f"Rate limited by LLM: {e}")
            raise LLMAnalysisError(f"LLM rate limited: {e}")
        except APIError as e:
            raise LLMAnalysisError(f"LLM API error: {e}")

    def generate_fix(self, code: str, bug_description: str, language: str = "python") -> str:
        """Generate fix for identified bug.

        Args:
            code: Source code with bug
            bug_description: Description of the bug
            language: Programming language

        Returns:
            Fixed code

        Raises:
            LLMAnalysisError: If generation fails
        """
        prompt = self._build_fix_prompt(code, bug_description, language)

        try:
            response = self._call_llm(
                [
                    {
                        "role": "system",
                        "content": "You are an expert programmer that fixes bugs in code. "
                        "Provide ONLY the corrected code without any explanation.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=2000,
            )

            logger.info("Fix generated successfully")
            return response

        except APIError as e:
            raise LLMAnalysisError(f"Failed to generate fix: {e}")

    def _call_llm(
        self,
        messages: List[dict],
        temperature: float = 0.3,
        max_tokens: int = 2000,
        timeout: int = settings.llm_api_timeout,
    ) -> str:
        """Call LLM API.

        Args:
            messages: Chat messages
            temperature: Temperature for generation
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds

        Returns:
            LLM response text

        Raises:
            Various OpenAI exceptions
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout,
            )

            return response.choices[0].message.content.strip()

        except Timeout:
            raise ServiceTimeoutError("LLM request timed out")
        except RateLimitError as e:
            logger.warning(f"Rate limited: {e}")
            # Retry with exponential backoff
            time.sleep(2)
            return self._call_llm(messages, temperature, max_tokens, timeout)

    @staticmethod
    def _build_analysis_prompt(code: str, language: str, context: Optional[str]) -> str:
        """Build code analysis prompt.

        Args:
            code: Source code
            language: Programming language
            context: Additional context

        Returns:
            Formatted prompt
        """
        prompt = f"""Analyze the following {language} code for bugs, vulnerabilities, and issues.
For each issue found, provide:
1. Type (syntax_error, logic_error, security_vulnerability, etc.)
2. Severity (CRITICAL, HIGH, MEDIUM, LOW)
3. Line number (if applicable)
4. Description
5. Explanation
6. A suggested fix

Format the response as a JSON array of bugs.

Code:
```{language}
{code}
```

Context: {context or 'None'}

Return ONLY valid JSON array."""

        return prompt

    @staticmethod
    def _build_fix_prompt(code: str, bug_description: str, language: str) -> str:
        """Build fix generation prompt.

        Args:
            code: Source code with bug
            bug_description: Bug description
            language: Programming language

        Returns:
            Formatted prompt
        """
        prompt = f"""Fix the following bug in {language} code:

Bug: {bug_description}

Original Code:
```{language}
{code}
```

Provide the corrected code only, without explanation."""

        return prompt
