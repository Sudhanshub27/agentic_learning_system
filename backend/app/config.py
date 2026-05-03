"""
Agentic Learning System - Configuration Module

Manages all application settings using pydantic-settings.
Loads from .env file with validation and type safety.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables / .env file.
    All LLM provider keys and database configs are managed here.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- Application ----
    app_name: str = "Agentic Learning System"
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # ---- Database ----
    database_url: str = "sqlite+aiosqlite:///./data/learning_system.db"

    # ---- LLM Providers ----
    # Ollama (local, no key needed)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    # Google Gemini (free tier)
    gemini_api_key: Optional[str] = None

    # Groq (free tier)
    groq_api_key: Optional[str] = None

    # DeepSeek (free tier)
    deepseek_api_key: Optional[str] = None

    # ---- ChromaDB ----
    chroma_persist_dir: str = "./chroma_data"

    # ---- Server ----
    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def available_providers(self) -> list[str]:
        """Returns a list of LLM providers that have valid configuration."""
        providers = ["ollama"]  # Always available (local)
        if self.gemini_api_key and self.gemini_api_key != "your_gemini_key_here":
            providers.append("gemini")
        if self.groq_api_key and self.groq_api_key != "your_groq_key_here":
            providers.append("groq")
        if self.deepseek_api_key and self.deepseek_api_key != "your_deepseek_key_here":
            providers.append("deepseek")
        return providers

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


# Singleton instance — import this everywhere
settings = Settings()
