"""
Data models and Pydantic schemas for CodeSurgeon API.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BugSeverity(str, Enum):
    """Bug severity levels."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class BugType(str, Enum):
    """Types of bugs detected."""

    SYNTAX_ERROR = "syntax_error"
    LOGIC_ERROR = "logic_error"
    SECURITY_VULNERABILITY = "security_vulnerability"
    PERFORMANCE_ISSUE = "performance_issue"
    TYPE_MISMATCH = "type_mismatch"
    NULL_REFERENCE = "null_reference"
    OTHER = "other"


class AnalysisRequest(BaseModel):
    """Request model for code analysis."""

    type: str = Field(..., description="Type: 'pr' for PR URL or 'snippet' for code")
    input: str = Field(..., description="GitHub PR URL or code snippet")
    language: str = Field(default="auto", description="Programming language")
    context: Optional[Dict[str, str]] = Field(default=None, description="Additional context")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "type": "snippet",
                "input": "def foo():\n    x = 1 || 2",
                "language": "python",
                "context": {"framework": "django"},
            }
        }


class Fix(BaseModel):
    """Fix suggestion for a bug."""

    id: UUID = Field(default_factory=uuid4)
    corrected_code: str = Field(..., description="Fixed code")
    explanation: str = Field(..., description="Explanation of the fix")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")


class AlternativeFix(BaseModel):
    """Alternative fix suggestion."""

    code: str = Field(..., description="Alternative code")
    note: str = Field(..., description="Note about this alternative")


class Bug(BaseModel):
    """Detected bug in code."""

    id: UUID = Field(default_factory=uuid4)
    type: BugType = Field(..., description="Type of bug")
    severity: BugSeverity = Field(..., description="Severity level")
    line: int = Field(..., description="Line number (1-indexed)")
    code_snippet: str = Field(..., description="Code snippet with bug")
    description: str = Field(..., description="Short description")
    explanation: str = Field(..., description="Detailed explanation")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    fix: Optional[Fix] = Field(default=None, description="Primary fix suggestion")
    alternatives: Optional[List[AlternativeFix]] = Field(
        default=None, description="Alternative fixes"
    )


class AnalysisSummary(BaseModel):
    """Summary statistics of analysis."""

    total_bugs: int = Field(..., description="Total bugs found")
    critical: int = Field(default=0, description="Critical bugs")
    high: int = Field(default=0, description="High severity bugs")
    medium: int = Field(default=0, description="Medium severity bugs")
    low: int = Field(default=0, description="Low severity bugs")
    analysis_time_ms: int = Field(..., description="Time taken for analysis in ms")


class AnalysisResponse(BaseModel):
    """Response model for analysis."""

    id: UUID = Field(default_factory=uuid4)
    status: str = Field(..., description="Status: 'success', 'error', etc.")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    bugs: List[Bug] = Field(default_factory=list, description="List of detected bugs")
    summary: AnalysisSummary = Field(..., description="Summary statistics")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Status: 'healthy' or 'unhealthy'")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    services: Dict[str, str] = Field(..., description="Service status")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: Dict[str, str] = Field(..., description="Error details")


# Fix generation request
class FixRequest(BaseModel):
    """Request to generate fix for a bug."""

    bug_id: UUID = Field(..., description="Bug ID to fix")
    analysis_id: UUID = Field(..., description="Analysis ID")


# Fix response
class FixResponse(BaseModel):
    """Response with fix details."""

    bug_id: UUID = Field(..., description="Bug ID")
    fix: Fix = Field(..., description="Primary fix")
    alternatives: Optional[List[AlternativeFix]] = Field(
        default=None, description="Alternative fixes"
    )
