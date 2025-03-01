import sys
import re
import urllib.parse
import json
from typing import List
from pydantic import BaseModel, Field
from firecrawl import FirecrawlApp
from groq import Groq
# from config import Settings

# Define extraction schemas for search results
class SearchResult(BaseModel):
    title: str = Field(..., description="Title of search result")
    snippet: str = Field(..., description="Snippet text of search result")
    url: str = Field(..., description="URL of search result")

class ExtractSchema(BaseModel):
    results: List[SearchResult] = Field(..., description="List of top search results")

# Define the structured response model for the investment recommendation
class ExtractionResponse(BaseModel):
    financial_Health: str = Field(..., alias="Financial Health", description="Analysis of the company's financial health")
    market_sentiment: str = Field(..., alias="Market Sentiment", description="Analysis of the market sentiment towards the company")
    recommendation: str = Field(..., alias="Recommendation", description="Final investment recommendation with reasoning")

def recommend(stock_name: str):
    try:
        # Initialize the FirecrawlApp with your API key
        fc_app = FirecrawlApp(api_key='fc-7174987a5f824e74b688ce1392114077')

        # Build a search query string with factors needed for analysis
        search_query = f"{stock_name} stock analysis profit loss revenue news"
        encoded_query = urllib.parse.quote(search_query)

        # Construct the Bing search URL
        search_url = f"https://www.bing.com/search?q={encoded_query}"

        print("\nScraping search results...")
        # Use Firecrawl to scrape the search results page with our schema
        data = fc_app.scrape_url(search_url, {
            'formats': ['json'],
            'jsonOptions': {
                'schema': ExtractSchema.model_json_schema(),
            }
        })

        # Extract the results from the scraped JSON
        results = data.get("json", {}).get("results", [])
        if not results:
            raise ValueError("No results found in the Firecrawl response.")

        # Combine the top 5 search results into a single text block for context
        combined_text = ""
        for i, result in enumerate(results[:5], start=1):
            combined_text += (
                f"Result {i}:\n"
                f"Title: {result.get('title', 'N/A')}\n"
                f"Snippet: {result.get('snippet', 'N/A')}\n"
                f"URL: {result.get('url', 'N/A')}\n\n"
            )

        print("Combined Search Results:")
        print(combined_text)

        # Build a prompt for Groq LLM that requests a structured investment recommendation
        prompt = f"""
Based on the following search results regarding {stock_name} stock analysis, provide a detailed and structured investment recommendation.
Return your response strictly in JSON format with exactly these keys:
"Financial Health": An analysis of the company's financial health.
"Market Sentiment": An analysis of the market sentiment towards the company.
"Recommendation": Your final investment recommendation with supporting reasoning.

Search Results:
{combined_text}
        """

        # Initialize the Groq client with your Groq API key
        groq_client = Groq(api_key="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")

        # Generate the structured recommendation using Groq LLM
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
        )

        # Extract the response content
        response_content = response.choices[0].message.content
        print("Raw Groq Response:")
        print(response_content)

        # Use regex to extract a JSON object from the response
        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the Groq response.")
        json_str = json_match.group()

        # Parse the JSON string into a dictionary
        extraction_data = json.loads(json_str)

        # Create an ExtractionResponse object from the dictionary using model_validate
        extraction = ExtractionResponse.model_validate(extraction_data)

        print("\nStructured Investment Recommendation:")
        print(json.dumps(extraction.model_dump(), indent=4))
        return extraction

    except Exception as e:
        print(f"Error during recommendation: {e}")
        # Return a default extraction response in case of errors
        default_extraction = ExtractionResponse.model_validate({
            "Financial Health": "",
            "Market Sentiment": "",
            "Recommendation": f"Error: {str(e)}"
        })
        return default_extraction

# if _name_ == "_main_":
#     # Example usage of the recommend function.
#     recommendation = recommend("Adani Ports")
#     print("\nFinal Recommendation Output:")
#     print(json.dumps(recommendation.model_dump(), indent=4))