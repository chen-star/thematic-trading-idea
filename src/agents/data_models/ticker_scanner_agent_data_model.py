from typing import List

from pydantic import BaseModel, Field


class ScannedTicker(BaseModel):
    """
    Defines the structured output for the stock analysis scanner agent.
    """
    symbol: str = Field(description="The official ticker symbol of the stock (e.g., 'GOOGL', 'AAPL').")
    company_name: str = Field(description="The full legal name of the company corresponding to the ticker symbol.")
    justification: str = Field(
        description="A short explanation (2-3 sentences) of why the ticker is relevant to the thematic topic.")


class ScannerAgentListOutput(BaseModel):
    """
    Defines the top-level structure containing a list of structured stock outputs.
    This is the model the LLM should generate for a complete response.
    """
    scanned_tickers: List[ScannedTicker] = Field(
        description="A list of all stocks that successfully met the screening criteria."
    )
