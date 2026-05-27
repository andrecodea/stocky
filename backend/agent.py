# config
from config import settings, Settings
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# llmops
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
# from langgraph.checkpoint.memory import InMemorySaver
# from langchain.agents.middleware import ToolRetryMiddleware

# tooling
from tools import tavily_search
from tavily import UsageLimitExceededError

def _init_llm(config: Settings, model_name: str | None = None) -> BaseChatModel:
    """Initializes LLM with LLMConfig Pydantic BaseModel and fallback mechanism."""
    resolved_model = model_name or config.model_name
    logger.info(f"[AGENT] Initializing LLM: model={resolved_model}")

    anthropic_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        return ChatAnthropic(model=resolved_model, base_url=config.base_url, api_key=anthropic_key)

    openai_key: str | None = os.getenv("OPENAI_API_KEY")
    if openai_key:
        logger.info(f"[AGENT] LLM initialized: model={config.fallback_model} (fallback)")
        return ChatOpenAI(model=config.fallback_model, base_url=config.fallback_url, api_key=openai_key)

    raise EnvironmentError("No LLM API key found, provide ANTHROPIC_API_KEY or OPENAI_API_KEY in .env")

def build_agent() -> Runnable:
    llm = _init_llm(settings)

    analysis_agent = create_agent(
        model=llm,
        tools=[tavily_search],
        system_prompt="You are a helpful and experienced inventory manager.",
    )

    return analysis_agent