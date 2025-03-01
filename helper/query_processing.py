from groq import Groq
import instructor
from pydantic import BaseModel, Field
from config import Settings

class ExtractionResponse(BaseModel):
    news: str = Field(..., description="Query string for fetching news articles")
    stock: str = Field(..., description="Query string for fetching stock data")
    twitter: str = Field(..., description="Query string for fetching Twitter insights")

class QueryProcessor:
    def __init__(self):
        # Set up the structured LLM client with Groq Llama.
        self.groq_client = instructor.from_groq(Groq(), mode=instructor.Mode.JSON)
    
    def process_query(self, user_query: str) -> ExtractionResponse:
        """
        Processes a user query for real-time sentiment analysis on investments.
        
        The structured LLM extracts three components from the query:
            1. A news API query string.
            2. A stock API query string.
            3. A Twitter API query string.
            
        Args:
            user_query (str): The user's investment-related query.
            
        Returns:
            ExtractionResponse: Contains the three query strings needed for downstream API calls.
        """
        prompt = (
            "You are an assistant specialized in real-time sentiment analysis for smarter investment decisions. "
            "Extract the following components from the user's query:\n"
            "1. A query string to retrieve relevant news articles (for the news API).\n"
            "2. A query string to retrieve stock data (for the stock API).\n"
            "3. A query string to retrieve recent insights from Twitter (for the Twitter API).\n"
            "Return your response in JSON format with keys 'news', 'stock', and 'twitter'.\n"
            f"User Query: {user_query}"
        )
        try:
            response = self.groq_client.chat.completions.create(
                model=Settings.GROQ_MODEL,  # Replace with your actual model identifier
                messages=[
                    {"role": "system", "content": "Extract investment-related components from the query."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                response_model=ExtractionResponse,
            )
            return response
        except Exception as e:
            # Log the error and return default empty responses if something goes wrong.
            print(f"Error processing query: {e}")
            return ExtractionResponse(news="", stock="", twitter="")

# Example usage:
# if __name__ == '__main__':
#     # Imagine the user query is related to sentiment analysis for investments.
#     user_query = "Ki should I invest in Adani?"
#     qp = QueryProcessor()
#     extraction = qp.process_query(user_query)
#     print("Extracted Query Components:")
#     print("News API Query:", extraction.news)
#     print("Stock API Query:", extraction.stock)
#     print("Twitter API Query:", extraction.twitter)
