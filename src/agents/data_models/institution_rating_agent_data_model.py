from typing import List

from agents.data_models.sentiment import Sentiment
from pydantic import BaseModel, Field

class InstitutionRating(BaseModel):
    symbol: str = Field(description="The official ticker symbol of the stock (e.g., 'GOOGL', 'AAPL').")
    company_name: str = Field(description="The full legal name of the company corresponding to the ticker symbol.")
    aggregated_sentiment: Sentiment = Field(description="The overall sentiment of symbol.")
    justification: str = Field(
        description="A 1-2 sentence summary explaining the sentiment and why it was classified as such.")


class InstitutionRatingOutput(BaseModel):
    institution_ratings: List[InstitutionRating] = Field(
        description="A list of all institution rating results for stocks."
    )
