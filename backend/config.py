import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict


path = str(pathlib.Path().absolute())

api = dict(
    SERVER_HOST="127.0.0.1",
    SERVER_PORT=8500,
    DEBUG=True,
    RELOAD=True,
)


class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_anon_key: str

    # Anthropic (modelo principal)
    anthropic_api_key: str = ""
    model_name: str = "claude-sonnet-4-6"
    base_url: str = "https://openrouter.ai/api/v1"

    # Fallback (OpenAI / OpenRouter)
    openai_api_key: str = ""
    fallback_model: str = "openai/gpt-4o-mini"
    fallback_url: str = "https://openrouter.ai/api/v1"

    # OpenRouter (visão + chat direto)
    openrouter_api_key: str = ""
    openrouter_model_chat: str = "mistralai/mistral-7b-instruct"
    openrouter_model_vision: str = "openai/gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
