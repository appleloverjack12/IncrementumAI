import os
import requests
from crewai_tools import tool

@tool("Brave Web Search")
def brave_search(query: str) -> str:
    """
    Search the web using Brave Search API for current market data, news, and trends.
    Use this when you need real-time information about markets, competitors, or industry trends.
    
    Args:
        query: Search query string (e.g., "SaaS market Germany 2024")
    
    Returns:
        Formatted search results with titles, descriptions, and URLs
    """
    api_key = os.getenv('BRAVE_API_KEY')
    
    if not api_key:
        return "Error: BRAVE_API_KEY not configured. Please add it to environment variables."
    
    try:
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={
                'q': query,
                'count': 10,
                'text_decorations': False
            },
            headers={
                'Accept': 'application/json',
                'X-Subscription-Token': api_key
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return f"Error: Brave API returned status {response.status_code}"
        
        data = response.json()
        results = data.get('web', {}).get('results', [])
        
        if not results:
            return "No results found for this query."
        
        formatted_results = "WEB SEARCH RESULTS:\n\n"
        
        for i, result in enumerate(results[:10], 1):
            title = result.get('title', 'No title')
            description = result.get('description', 'No description')
            url = result.get('url', '')
            
            formatted_results += f"[{i}] {title}\n"
            formatted_results += f"{description}\n"
            formatted_results += f"Source: {url}\n\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error performing web search: {str(e)}"