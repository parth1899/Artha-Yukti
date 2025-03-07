import urllib.parse
import sys
from typing import List
from pydantic import BaseModel, Field
from firecrawl import FirecrawlApp
from groq import Groq
from config import Settings

# Define extraction schemas for search results
class SearchResult(BaseModel):
    title: str = Field(..., description="Title of search result")
    snippet: str = Field(..., description="Snippet text of search result")
    url: str = Field(..., description="URL of search result")

class ExtractSchema(BaseModel):
    results: List[SearchResult] = Field(..., description="List of top search results")

def main(stock_name: str = None):
    # If stock_name is not provided, prompt the user for input
    if not stock_name:
        # stock_name = input("Enter the stock name (e.g., Asian Paints Ltd): ")
        return Exception("Stock name not provided.")

    # Initialize the FirecrawlApp with your API key
    # print("the api key is: ", Settings.FIRE_CRAWL_API_KEY)
    app = FirecrawlApp(api_key=Settings.FIRE_CRAWL_API_KEY)

    # Build a search query string with factors needed for analysis
    search_query = f"{stock_name} stock analysis profit loss revenue news"
    encoded_query = urllib.parse.quote(search_query)

    # Construct the Bing search URL
    search_url = f"https://www.bing.com/search?q={encoded_query}"

    print("\nScraping search results...")

    # Use Firecrawl to scrape the search results page with our schema
    data = app.scrape_url(search_url, {
        'formats': ['json'],
        'jsonOptions': {
            'schema': ExtractSchema.model_json_schema(),
        }
    })

    # Extract the results from the scraped JSON
    results = data["json"]["results"]

    # Combine the top 5 search results into a single text block for context
    combined_text = ""
    for i, result in enumerate(results[:5], start=1):
        combined_text += (
            f"Result {i}:\n"
            f"Title: {result['title']}\n"
            f"Snippet: {result['snippet']}\n"
            f"URL: {result['url']}\n\n"
        )

    # print("Combined Search Results:")
    # print(combined_text)

    # Build a prompt for Groq LLM that requests a detailed analysis and investment recommendation
#     prompt = f"""
# Based on the following search results regarding {stock_name}, which include financial indicators such as profit, loss, revenue, and current news context, provide a detailed analysis of the stock's current situation. Assess its financial health and market sentiment, then conclude with a clear recommendation on whether to invest in this stock or not, including your reasoning.

# Search Results:
# {combined_text}
# """

#     # Initialize the Groq client with your Groq API key
#     client = Groq(api_key="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")

#     # Generate the summary/recommendation using Groq LLM
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         model="llama-3.3-70b-versatile",
#         stream=False,
#     )

    # Print the summary recommendation
    # print("\nInvestment Recommendation Summary:")
    # print(chat_completion.choices[0].message.content)
    return results

# if __name__ == "__main__":
#     # If a stock name is passed as a command-line argument, use it; otherwise, it will be prompted.
#     stock_name_arg = sys.argv[1] if len(sys.argv) > 1 else None
#     main(stock_name_arg)
