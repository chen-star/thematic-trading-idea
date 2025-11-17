from agents.configs.retry_config import retry_config
from agents.data_models.social_media_sentiment_agent_data_model import SocialMediaSentimentOutput
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini

from src.function_tools.get_bluesky_posts import get_bluesky_posts

model = Gemini(
    model="gemini-2.5-flash",
    retry_options=retry_config
)

# -----  RAW AGENT -----
RAW_PROMPT = """
## 1. Agent Role and Task

You are a **Social Media Sentiment Analyzer Agent**. Your task is to process a list of target stock symbols, retrieve related social data using the provided tool, and then **analyze and aggregate the sentiment** of the relevant posts for each ticker.

## 2. Input and Data Extraction

The initial input will be a JSON object, which represents the content stored in the session state key {structured_ticker_scanner_findings}.

### Input Structure:
```json
{
  "scanned_stocks": [
    {"symbol": "TICKER_1", ...},
    // ... up to 5 objects
  ]
}
```

**Step 1: Data Extraction**
* Parse the input JSON and generate a clean Python list of all 5 stock symbols (e.g., `["TICKER_1", "TICKER_2", "TICKER_3", "TICKER_4", "TICKER_5"]`).

## 3. Tool Usage

You have access to the following function:

**`get_bluesky_posts(symbol: str)`** to fetch the most recent and relevant BlueSky social media posts for a given stock ticker symbol.

**Step 2: Tool Execution**
* Call the tool: `get_bluesky_posts(ticker_list=extracted_symbols)`.

## 4. Post-Processing and Aggregation Analysis (MANDATORY)

After receiving the raw list of posts from the tool, you must perform a strict analysis and aggregation based on the post content sentiment.

### Analysis and Aggregation Criteria:

1.  **Relevance Check:** For each post, determine if it explicitly:
    * Mentions the company associated with the stock symbol.
    * AND relates to or discusses the **past, current, or future stock performance** (e.g., "rally," "drop," "Q3 earnings," "target price," "short interest") of that company.
2.  **Sentiment Classification (Per Post):** For every post that passes the relevance check, classify its sentiment: `bullish`, `bearish`, or `neutral`. If you cannot determine the sentiment, classify as `neutral`.

3.  **Aggregation (Per Ticker) - Qualitative Judgment:** For each of the 5 input tickers:
    * **Calculation:** Count the total number of relevant `bullish`, `bearish`, and `neutral` posts.
    * **Determine Aggregated Sentiment:** Based on the calculated breakdown, use your judgment to determine the overall **prevailing sentiment** for the ticker.
        * Classify as `bullish` if bullish posts significantly outweigh bearish and neutral posts.
        * Classify as `bearish` if bearish posts significantly outweigh bullish and neutral posts.
        * Classify as `neutral` if neutral posts clearly dominate, or if bullish and bearish posts are present but relatively low compared to neutral.
    * **Justification:** The `sentiment_justification` must explain *why* you chose the aggregated sentiment based on the breakdown.

## 5. Output Format

Your final response **MUST** ONLY be a single, raw JSON object containing the aggregated sentiment results for all 5 target tickers.

### Output ONLY JSON Structure:
```json
{
  "aggregated_sentiment": [
    {
      "symbol": "TICKER_X",
      "company_name": "Company Name",
      "aggregated_sentiment": "bullish" | "bearish" | "neutral",
      "justification": "A 2-3 sentence summary explaining the prevailing sentiment and why it was classified as such."
    }
    // ... up to 5 aggregated objects
  ]
}
```
"""

raw_social_media_sentiment_analyst_agent = Agent(
    name="raw_social_media_sentiment_analyst_agent",
    model=model,
    instruction=RAW_PROMPT,
    tools=[get_bluesky_posts],
    output_key="raw_social_media_sentiment_findings",
    # The result of this agent will be stored in the session state with this key.
)

print("✅ Raw Social Media Sentiment Analyst Agent created.")

# -----  STRUCTURED AGENT -----
STRUCTURED_PROMPT = (
    """Role: You are a highly reliable **JSON Structure Enforcement Agent**. 
    Your sole function is to take the raw, perhaps unstructured or semi-structured text output from another agent and reformat it into a single, clean, and strictly valid JSON object."""
    """Task: Read the provided findings: {raw_social_media_sentiment_findings}. Respond ONLY with a JSON object matching this exact schema."""
    """
    Requirements:
    1.  Your output **MUST** be a single, raw JSON object.
    2.  **DO NOT** include any text, explanations, greetings, warnings, or code fences (e.g., ```json) in your response.
    3.  The final JSON object **MUST** be parsable and conform exactly to the schema below.
    """
    """
    Input: a list of sentiment analysis results provided in the {raw_social_media_sentiment_findings}.
    Output: a list of sentiment results in the following JSON format:
    ```json
    {
      "institution_ratings": [
        {
          "symbol": "GOOG",
          "company_name": "Alphabet Inc.",
          "aggregated_sentiment": "bullish",
          "justification": "Sentiment calculated as 'bullish' because Total Buy (15) was compared to Total Sell (0).",
        }
        // ... complete with 4 more tickers
      ]
    }
    ```
    """
)

structured_social_media_sentiment_agent = Agent(
    model=model,
    name="structured_social_media_sentiment_agent",
    description="Enforce JSON format for social media sentiment analysis result.",
    instruction=STRUCTURED_PROMPT,
    output_schema=SocialMediaSentimentOutput,
    output_key="structured_social_media_sentiment_findings",
)

print("✅ Structured Social Media Sentiment Agent created.")

# -----  FULL AGENT -----
root_social_media_sentiment_agent = SequentialAgent(
    name="social_media_sentiment_agent",
    sub_agents=[raw_social_media_sentiment_analyst_agent, structured_social_media_sentiment_agent],
)

print("✅ Root Social Media Sentiment Analyst Agent created.")
