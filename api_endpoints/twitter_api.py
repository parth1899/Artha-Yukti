import requests
from config import Settings

def fetch_twitter(query: str) -> dict:
    """
    Fetches recent tweets matching the given query using the Twitter API v2.

    Note:
        You must have a valid Twitter Bearer Token (set in your config).
    
    Args:
        query (str): The search query for tweets.

    Returns:
        dict: The JSON response from the Twitter API or an error message.
    """
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {Settings.TWITTER_BEARER_TOKEN}"
    }
    params = {
        "query": query,
        "max_results": 10  # Adjust this number as needed
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch tweets: {e}"}
