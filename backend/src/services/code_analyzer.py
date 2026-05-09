"""
Code analyzer service for static code analysis.
"""

import ast
from typing import Dict, List, Optional

from src.exceptions import CodeParseError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CodeAnalyzer:
    """Service for analyzing code structure."""

    SUPPORTED_LANGUAGES = {"python", "javascript", "typescript", "java", "go"}

    def __init__(self, language: str = "python"):
        """Initialize code analyzer.

        Args:
            language: Programming language
        """
        self.language = language.lower()
        if self.language not in self.SUPPORTED_LANGUAGES:
            logger.warning(f"Language {language} not fully supported, using generic analysis")

    def analyze(self, code: str) -> Dict:
        """Analyze code structure.

        Args:
            code: Source code to analyze

        Returns:
            Dict with analysis results
        """
        try:
            if self.language == "python":
                return self._analyze_python(code)
            else:
                return self._analyze_generic(code)
        except Exception as e:
            logger.error(f"Error analyzing code: {e}")
            raise CodeParseError(f"Failed to analyze code: {e}")

    def _analyze_python(self, code: str) -> Dict:
        """Analyze Python code.

        Args:
            code: Python source code

        Returns:
            Dict with analysis results
        """
        try:
            tree = ast.parse(code)

            analysis = {
                "language": "python",
                "lines_of_code": len(code.split("\n")),
                "functions": [],
                "classes": [],
                "imports": [],
                "has_syntax_errors": False,
            }

            # Extract functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append(
                        {
                            "name": node.name,
                            "lineno": node.lineno,
                            "args": [arg.arg for arg in node.args.args],
                        }
                    )

                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append(
                        {
                            "name": node.name,
                            "lineno": node.lineno,
                            "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        }
                    )

                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(alias.name)
                    else:
                        analysis["imports"].append(node.module)

            logger.info(f"Analyzed Python code: {len(analysis['functions'])} functions, "
                       f"{len(analysis['classes'])} classes")
            return analysis

        except SyntaxError as e:
            logger.error(f"Syntax error in Python code: {e}")
            return {
                "language": "python",
                "has_syntax_errors": True,
                "error": str(e),
                "error_lineno": e.lineno,
            }

    def _analyze_generic(self, code: str) -> Dict:
        """Generic code analysis for unsupported languages.

        Args:
            code: Source code

        Returns:
            Dict with basic analysis
        """
        lines = code.split("\n")
        return {
            "language": self.language,
            "lines_of_code": len(lines),
            "functions": self._find_functions_generic(code),
            "imports": self._find_imports_generic(code),
        }

    @staticmethod
    def _find_functions_generic(code: str) -> List[Dict]:
        """Find function definitions in generic language.

        Args:
            code: Source code

        Returns:
            List of function definitions
        """
        functions = []
        lines = code.split("\n")

        for i, line in enumerate(lines):
            if "function " in line or "def " in line or "func " in line:
                functions.append({"lineno": i + 1, "line": line.strip()})

        return functions

    @staticmethod
    def _find_imports_generic(code: str) -> List[str]:
        """Find imports in generic language.

        Args:
            code: Source code

        Returns:
            List of imports
        """
        imports = []
        lines = code.split("\n")

        for line in lines:
            if "import " in line or "require " in line:
                imports.append(line.strip())

        return imports

    def validate_syntax(self, code: str) -> bool:
        """Validate code syntax.

        Args:
            code: Source code to validate

        Returns:
            True if valid, False otherwise
        """
        if self.language == "python":
            try:
                ast.parse(code)
                return True
            except SyntaxError:
                return False

        # Generic validation - just check it's not empty
        return bool(code.strip())
