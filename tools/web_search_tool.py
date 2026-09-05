import os

from langchain_core.tools import tool
from tavily import TavilyClient


@tool
def web_search(query: str) -> str:
    """Search the internet for information about books, authors, or general topics."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "Tavily API key is not configured."

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return "No web search results found."

    output = []

    for result in results:
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")

        output.append(
            f"Title: {title}\n"
            f"Information: {content}\n"
            f"URL: {url}"
        )

    return "\n\n".join(output)