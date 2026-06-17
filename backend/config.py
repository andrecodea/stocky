"""Centralized application settings loaded from environment variables."""

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration backed by .env file."""

    # Supabase
    supabase_url: str = Field(validation_alias=AliasChoices("SUPABASE_URL", "API_URL"))
    supabase_anon_key: str = Field(
        validation_alias=AliasChoices("SUPABASE_ANON_KEY", "ANON_KEY", "PUBLISHABLE_KEY")
    )
    supabase_service_role_key: str = Field(
        validation_alias=AliasChoices("SUPABASE_SERVICE_ROLE_KEY", "SERVICE_ROLE_KEY", "SECRET_KEY")
    )
    supabase_jwt_secret: str = Field(
        default="", validation_alias=AliasChoices("SUPABASE_JWT_SECRET", "JWT_SECRET")
    )

    # Server
    server_host: str = "127.0.0.1"
    server_port: int = 8500

    # LLM — primary (Anthropic via OpenRouter)
    anthropic_api_key: str = ""
    model_name: str = "claude-sonnet-4-6"
    base_url: str = "https://openrouter.ai/api/v1"

    # LLM — fallback (OpenAI via OpenRouter)
    openai_api_key: str = ""
    fallback_model: str = "openai/gpt-4o-mini"
    fallback_url: str = "https://openrouter.ai/api/v1"

    # OpenRouter direct
    openrouter_api_key: str = ""
    openrouter_model_chat: str = "mistralai/mistral-7b-instruct"
    openrouter_model_vision: str = "openai/gpt-4o-mini"

    # Tavily
    tavily_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
