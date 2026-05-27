import logging
import os
from langchain_core.tools import tool
from tavily import TavilyClient

def _get_tavily_client() -> TavilyClient:
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))

log = logging.getLogger(__name__)

@tool
def tavily_search(query: str) -> str:
    """Search the web for current information about a topic.

    Args:
        query: Search query to execute.
    Returns:
        Search results with title, URL, and content snippet.
    """
    try:
        response = _get_tavily_client().search(query)
        lines = []
        for r in response.get("results", []):
            lines.append(f"**{r['title']}**\n{r['url']}\n{r.get('content', '')}\n---")
        return "\n\n".join(lines) or "No results found."
    except Exception as e:
        log.error(f"tavily_search failed for '{query}': {e}", exc_info=True)
        raise