"""
Fix generator service for generating code fixes.
"""

from typing import List, Optional

from src.exceptions import LLMAnalysisError
from src.integrations.llm_client import LLMClient
from src.models.schemas import AlternativeFix, Bug, Fix
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FixGenerator:
    """Service for generating fixes for bugs."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize fix generator.

        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client

    def generate_fix(self, code: str, bug: Bug, language: str = "python") -> Fix:
        """Generate fix for a bug.

        Args:
            code: Original source code
            bug: Bug object to fix
            language: Programming language

        Returns:
            Fix suggestion

        Raises:
            LLMAnalysisError: If generation fails
        """
        if not self.llm_client:
            raise LLMAnalysisError("LLM client not initialized")

        try:
            # Get the buggy code snippet
            buggy_code = bug.code_snippet

            # Generate fix
            fixed_code = self.llm_client.generate_fix(buggy_code, bug.explanation, language)

            # Validate fix
            if not self._validate_fix_format(fixed_code, language):
                logger.warning("Generated fix may have formatting issues")

            # Generate explanation
            explanation = self._generate_fix_explanation(bug, fixed_code)

            fix = Fix(
                corrected_code=fixed_code.strip(),
                explanation=explanation,
                confidence=min(0.95, bug.confidence + 0.05),  # Boost confidence slightly
            )

            logger.info(f"Generated fix for bug on line {bug.line}")
            return fix

        except Exception as e:
            logger.error(f"Failed to generate fix: {e}")
            raise LLMAnalysisError(f"Fix generation failed: {e}")

    def generate_alternatives(
        self, code: str, bug: Bug, language: str = "python", count: int = 2
    ) -> List[AlternativeFix]:
        """Generate alternative fixes for a bug.

        Args:
            code: Original source code
            bug: Bug object
            language: Programming language
            count: Number of alternatives to generate

        Returns:
            List of alternative fixes

        Raises:
            LLMAnalysisError: If generation fails
        """
        if not self.llm_client:
            return []

        alternatives = []

        try:
            for i in range(count):
                prompt = f"""Generate an alternative fix for this bug (option {i+1}):

Bug: {bug.explanation}
Buggy Code: {bug.code_snippet}

Provide a DIFFERENT fix approach, not the same as previous ones.
Return ONLY the code, no explanation."""

                # Use higher temperature for more variety
                fixed_code = self.llm_client._call_llm(
                    [
                        {
                            "role": "system",
                            "content": "You are an expert programmer generating alternative code fixes.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )

                alt_fix = AlternativeFix(
                    code=fixed_code.strip(),
                    note=f"Alternative approach {i+1}",
                )

                alternatives.append(alt_fix)
                logger.info(f"Generated alternative fix {i+1}")

        except Exception as e:
            logger.error(f"Failed to generate alternatives: {e}")

        return alternatives

    @staticmethod
    def _validate_fix_format(code: str, language: str) -> bool:
        """Validate fix code format.

        Args:
            code: Code to validate
            language: Programming language

        Returns:
            True if valid, False otherwise
        """
        # Basic validation - just check it's not empty and looks like code
        if not code or len(code) < 3:
            return False

        # Check for common syntax elements
        if language == "python":
            # Should have some Python-like structure
            return ":" in code or "=" in code or "(" in code

        return len(code) > 0

    @staticmethod
    def _generate_fix_explanation(bug: Bug, fixed_code: str) -> str:
        """Generate explanation for the fix.

        Args:
            bug: Original bug
            fixed_code: Fixed code

        Returns:
            Explanation string
        """
        explanations = {
            "syntax_error": "Fixed syntax error by correcting invalid operators/syntax",
            "logic_error": "Fixed logic error by correcting the conditional logic",
            "security_vulnerability": "Fixed security vulnerability by using safer methods",
            "performance_issue": "Improved performance by optimizing the code",
            "type_mismatch": "Fixed type mismatch by using correct data types",
            "null_reference": "Fixed null reference by adding proper null checks",
        }

        base_explanation = explanations.get(bug.type.value, "Fixed the issue")

        return f"{base_explanation}. Changed from '{bug.code_snippet}' to '{fixed_code}'"
