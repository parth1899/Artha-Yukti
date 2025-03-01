import sys
import urllib.parse
from typing import List
from pydantic import BaseModel, Field
from firecrawl import FirecrawlApp
from groq import Groq
from flask import Flask, jsonify, request

# Define extraction schemas for search results
class SearchResult(BaseModel):
    title: str = Field(..., description="Title of search result")
    snippet: str = Field(..., description="Snippet text of search result")
    url: str = Field(..., description="URL of search result")

class ExtractSchema(BaseModel):
    results: List[SearchResult] = Field(..., description="List of top search results")

def recommend(stock_name: str):
    try:
        # Initialize the FirecrawlApp with your API key
        fc_app = FirecrawlApp(api_key='fc-a868b912ef3941489964f39f56a90248')

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

        print("Combined Search Results:")
        print(combined_text)

        # Build a prompt for Groq LLM that requests a detailed analysis and investment recommendation
        prompt = f"""
Based on the following search results regarding {stock_name}, which include financial indicators such as profit, loss, revenue, and current news context, provide a detailed analysis of the stock's current situation. Assess its financial health and market sentiment, then conclude with a clear recommendation on whether to invest in this stock or not, including your reasoning.

Search Results:
{combined_text}
"""

        # Initialize the Groq client with your Groq API key
        groq_client = Groq(api_key="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")

        # Generate the summary/recommendation using Groq LLM
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
        )

        # Extract and print the recommendation
        recommendation = chat_completion.choices[0].message.content
        print("\nInvestment Recommendation Summary:")
        print(recommendation)
        return recommendation
    except Exception as e:
        print(f"Error during recommendation: {e}")
        return f"Error: {str(e)}"

