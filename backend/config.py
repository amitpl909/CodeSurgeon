"""
Configuration module for CodeSurgeon backend.
Loads environment variables and provides configuration.
"""

import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # GitHub
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_api_timeout: int = int(os.getenv("GITHUB_API_TIMEOUT", "10"))

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    llm_api_timeout: int = int(os.getenv("LLM_API_TIMEOUT", "20"))

    # API
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_env: str = os.getenv("API_ENV", "development")
    analysis_timeout: int = int(os.getenv("ANALYSIS_TIMEOUT", "30"))

    # Frontend
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS
    allowed_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
    ]

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
