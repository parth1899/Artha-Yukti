import requests
from config import Settings

def fetch_news(query: str) -> dict:
    """
    Fetches news articles related to the given query using NewsAPI.org.

    Args:
        query (str): The search query for news articles.

    Returns:
        dict: The JSON response from the news API or an error message.
    """
    url = "https://newsapi.org/v2/everything"
    # print(Settings.NEWS_API_KEY)
    params = {
        "q": query,
        "apiKey": Settings.NEWS_API_KEY,  # Your NewsAPI key from the config
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an error for HTTP error codes
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch news: {e}"}
