import requests
from config import Settings

def fetch_stock(query: str) -> dict:
    """
    Fetches stock data for a given company symbol using the Alpha Vantage API.

    Note:
        The query should be a valid stock ticker symbol (for example, 'RELIANCE.NS'
        for Reliance Industries on the NSE). Adjust the parameters as needed.

    Args:
        query (str): The stock ticker symbol.

    Returns:
        dict: The JSON response from the stock API or an error message.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": query,
        "interval": "5min",
        "apikey": Settings.ALPHA_VANTAGE_API_KEY  # Your Alpha Vantage key from the config
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch stock data: {e}"}

