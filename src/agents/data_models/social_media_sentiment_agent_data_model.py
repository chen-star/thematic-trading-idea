from typing import List

from agents.data_models.sentiment import Sentiment
from pydantic import BaseModel, Field


class SocialMediaSentiment(BaseModel):
    """
    Defines the structured output for the stock analysis scanner agent.
    """
    symbol: str = Field(description="The official ticker symbol of the stock (e.g., 'GOOGL', 'AAPL').")
    company_name: str = Field(description="The full legal name of the company corresponding to the ticker symbol.")
    aggregated_sentiment: Sentiment = Field(description="The overall sentiment of symbol.")
    justification: str = Field(
        description="A 1-2 sentence summary explaining the sentiment and why it was classified as such.")


class SocialMediaSentimentOutput(BaseModel):
    """
    Defines the top-level structure containing a list of structured stock outputs.
    This is the model the LLM should generate for a complete response.
    """
    social_media_sentiments: List[SocialMediaSentiment] = Field(
        description="A list of all sentiments for stocks that met the screening criteria."
    )
