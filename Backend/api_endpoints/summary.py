# function to generate summary from Groq LLama
import os
import requests
import json

def get_insights_from_groq(user_query, sentiment, news_analysis, stock, adjusted_price, weight_distribution):
    """
    Call Groq's LLama model to get insights based on pricing and weight distribution data.

    Args:
        user_query (str): The user's query.
        sentiment (str): The sentiment analysis result.
        news_analysis (str): The news analysis result.
        stock (str): The stock symbol or description.
        adjusted_price (float or list): The adjusted price data (derived from LSTM predictions on historical data).
        weight_distribution (dict or list): The weight distribution data indicating the confidence levels for sentiment and LSTM predictions.

    Returns:
        dict: A dictionary with either the insights or an error message.
    """
    import requests  # Ensure requests is imported

    # Groq API endpoint and key
    api_key = "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"
    endpoint = "https://api.groq.com/openai/v1/chat/completions"
    
    # Headers for the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Construct a refined prompt with clear sections and context
    prompt = f"""
User Query: {user_query}
Sentiment Analysis: {sentiment}
News Analysis: {news_analysis}
Stock: {stock}
Adjusted Price: {adjusted_price}  (derived from LSTM predictions on historical data)
Weight Distribution: {weight_distribution}  (reflects the confidence in both sentiment analysis and LSTM predictions)

Guidelines:
- The weight distribution determines how much priority to give to LSTM predictions (long-term trends) versus sentiment analysis (immediate reactions like breaking news or influencer statements).
- If the sentiment weight is higher, focus more on short-term market impacts; if the LSTM weight is higher, emphasize long-term predictions.
- When sentiment is bullish but LSTM predictions are flat or declining (or vice versa), explain the discrepancy.
- Provide actionable, unbiased insights based on these indicators.
- Keep the output concise and insightful.
- Ensure that you highlight the varibles adjusted price, {weight_distribution} in your insights.
"""

    # Prepare the payload for Groq's API call
    payload = {
        "model": "llama3-70b-8192",  # Using the LLama 3 model
        "messages": [
            {"role": "system", "content": "You are a data analysis assistant that provides insights based on pricing and distribution data."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,  # Lower temperature for more focused and deterministic responses
        "max_tokens": 1024
    }
    
    # Make the API call
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Extract and return the model's response
        if "choices" in result and len(result["choices"]) > 0:
            insights = result["choices"][0]["message"]["content"]
            return {"status": "success", "insights": insights}
        else:
            return {"status": "error", "message": "No response content found"}
            
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}


# Example usage
# if __name__ == "__main__":
#     # Example data
#     sample_adjusted_price = [102.5, 98.3, 105.7, 99.1, 103.2]
#     sample_weight_distribution = {"low": 0.3, "medium": 0.5, "high": 0.2}
    
#     # Get insights
#     result = get_insights_from_groq(sample_adjusted_price, sample_weight_distribution)
    
#     if result["status"] == "success":
#         print("INSIGHTS:")
#         print(result["insights"])
#     else:
#         print(f"Error: {result['message']}")