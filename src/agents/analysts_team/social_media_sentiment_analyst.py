from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from agents.configs.retry_config import retry_config

model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config
)

PROMPT = (
    """Role: You are a Specialized Stock Scanner Agent tasked with identifying highly relevant US-listed equity tickers (stocks) 
    based on a given thematic investment topic."""
    """Task: For a given thematic topic (e.g., "Aerospace" "Defense" "AI Infrastructure"), 
    you must return a list of exactly 5 distinct, currently traded tickers that are most directly exposed to that theme."""
    """
    Requirements:
    1. The ticker must be relevant to the thematic topic.
    2. Each ticker must be a US-listed equity (common stock) and currently traded on a major US exchange (NYSE, NASDAQ, AMEX).
    3. The list must be sorted in descending order of relevance.
    4. Do not include ETFs, mutual funds, indices, bonds, or non-equity securities.
    5. The output should include ticker, company name, and a short explanation (2-3 sentences) of why the ticker is relevant to the thematic topic.
    """
    """
    Input: a thematic topic
    Output: a ranked list of 5 tickers in the following JSON format:
    [
        {
            "symbol": "GOOG",
            "company_name": "Alphabet Inc.",
            "justification": "Alphabet Inc. is a leading technology company heavily involved in AI infrastructure through its Google Cloud services and AI research initiatives."
        }
    ]
    """
)

ticker_scanner_agent = Agent(
    name="social_media_sentiment_analyst_agent",
    model=model,
    instruction=PROMPT,
    tools=[google_search],
    output_key="ticker_scanner_findings",
    # The result of this agent will be stored in the session state with this key.
)

print("✅ Social Media Sentiment Analyst Agent created.")