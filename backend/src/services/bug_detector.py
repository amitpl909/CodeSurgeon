"""
Bug detector service using LLM and static analysis.
"""

import json
import re
from typing import Dict, List, Optional

from src.exceptions import LLMAnalysisError
from src.integrations.llm_client import LLMClient
from src.models.schemas import Bug, BugSeverity, BugType
from src.services.code_analyzer import CodeAnalyzer
from src.utils.cache import cache
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BugDetector:
    """Service for detecting bugs in code."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize bug detector.

        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client
        self.analyzer = CodeAnalyzer()

    def detect_bugs(self, code: str, language: str = "python", context: Optional[Dict] = None) -> List[Bug]:
        """Detect bugs in code.

        Args:
            code: Source code to analyze
            language: Programming language
            context: Additional context

        Returns:
            List of detected bugs
        """
        try:
            # Check cache first
            cache_key = f"bugs_{hash(code)}_{language}"
            cached_bugs = cache.get(cache_key)
            if cached_bugs:
                logger.info("Returning cached bug detection results")
                return cached_bugs

            # Perform static analysis first
            static_bugs = self._static_analysis(code, language)
            logger.info(f"Found {len(static_bugs)} static analysis bugs")

            # Then use LLM for deeper analysis if available
            llm_bugs = []
            if self.llm_client:
                llm_bugs = self._llm_analysis(code, language, context)
                logger.info(f"Found {len(llm_bugs)} LLM analysis bugs")

            # Combine and deduplicate bugs
            all_bugs = self._deduplicate_bugs(static_bugs + llm_bugs)

            # Cache results for 1 hour
            cache.set(cache_key, all_bugs, ttl=3600)

            return all_bugs

        except Exception as e:
            logger.error(f"Error detecting bugs: {e}")
            raise LLMAnalysisError(f"Bug detection failed: {e}")

    def _static_analysis(self, code: str, language: str) -> List[Bug]:
        """Perform static code analysis.

        Args:
            code: Source code
            language: Programming language

        Returns:
            List of detected bugs
        """
        bugs = []

        # Basic syntax checks
        if not self.analyzer.validate_syntax(code):
            bugs.append(
                Bug(
                    type=BugType.SYNTAX_ERROR,
                    severity=BugSeverity.CRITICAL,
                    line=1,
                    code_snippet=code[:100],
                    description="Syntax error in code",
                    explanation="The code has invalid syntax",
                    confidence=0.95,
                )
            )

        # Common patterns to check
        if language == "python":
            bugs.extend(self._check_python_patterns(code))

        return bugs

    def _check_python_patterns(self, code: str) -> List[Bug]:
        """Check for common Python issues.

        Args:
            code: Python source code

        Returns:
            List of detected bugs
        """
        bugs = []
        lines = code.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for common logical operators issues
            if " || " in line or " && " in line:
                bugs.append(
                    Bug(
                        type=BugType.SYNTAX_ERROR,
                        severity=BugSeverity.HIGH,
                        line=i,
                        code_snippet=line.strip(),
                        description="Invalid Python operators",
                        explanation="Python uses 'or' and 'and', not '||' and '&&'",
                        confidence=0.9,
                    )
                )

            # Check for common mistakes
            if " = " in line and " == " not in line:
                if "if " in line or "while " in line:
                    if " = " in line.split("if ")[-1].split("while ")[-1]:
                        bugs.append(
                            Bug(
                                type=BugType.LOGIC_ERROR,
                                severity=BugSeverity.HIGH,
                                line=i,
                                code_snippet=line.strip(),
                                description="Assignment in conditional",
                                explanation="Likely meant to use '==' for comparison",
                                confidence=0.7,
                            )
                        )

        return bugs

    def _llm_analysis(self, code: str, language: str, context: Optional[Dict]) -> List[Bug]:
        """Perform LLM-based code analysis.

        Args:
            code: Source code
            language: Programming language
            context: Additional context

        Returns:
            List of detected bugs

        Raises:
            LLMAnalysisError: If LLM analysis fails
        """
        if not self.llm_client:
            return []

        try:
            context_str = json.dumps(context) if context else None
            response = self.llm_client.analyze_code(code, language, context_str)

            # Parse JSON response
            bugs = self._parse_llm_response(response)
            logger.info(f"LLM found {len(bugs)} bugs")

            return bugs

        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return []  # Return empty list instead of failing

    @staticmethod
    def _parse_llm_response(response: str) -> List[Bug]:
        """Parse LLM response into Bug objects.

        Args:
            response: LLM response text

        Returns:
            List of Bug objects
        """
        bugs = []

        try:
            # Extract JSON from response
            json_match = re.search(r"\[.*\]", response, re.DOTALL)
            if not json_match:
                logger.warning("No JSON found in LLM response")
                return []

            json_str = json_match.group(0)
            bug_data_list = json.loads(json_str)

            for bug_data in bug_data_list:
                try:
                    bug = Bug(
                        type=BugType(bug_data.get("type", "other")),
                        severity=BugSeverity(bug_data.get("severity", "LOW")),
                        line=bug_data.get("line", 1),
                        code_snippet=bug_data.get("code_snippet", ""),
                        description=bug_data.get("description", ""),
                        explanation=bug_data.get("explanation", ""),
                        confidence=float(bug_data.get("confidence", 0.5)),
                    )
                    bugs.append(bug)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Failed to parse bug data: {e}")

            return bugs

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            return []

    @staticmethod
    def _deduplicate_bugs(bugs: List[Bug]) -> List[Bug]:
        """Remove duplicate bugs.

        Args:
            bugs: List of bugs

        Returns:
            Deduplicated list of bugs
        """
        seen = set()
        unique_bugs = []

        for bug in bugs:
            # Create a key based on line and description
            key = (bug.line, bug.description[:50])
            if key not in seen:
                seen.add(key)
                unique_bugs.append(bug)

        return unique_bugs
