from agents.configs.retry_config import retry_config
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini

from agents.data_models.technical_agent_data_model import TechnicalSentimentOutput

from src.function_tools.fetch_prce_and_technical_analysis import fetch_price_and_technical_analysis

model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config
)

# -----  RAW AGENT -----
RAW_PROMPT = """
You are an analytical engine responsible for processing structured input, running technical analysis, and compiling a final list of trading signals.

### 1. Input Processing
1.  **Source:** The initial input will be a JSON object, which represents the content stored in the session state key {structured_ticker_scanner_findings}.
    ### Input Structure:
    ```json
    {
      "scanned_stocks": [
        {"symbol": "TICKER_1", ...},
        // ... up to 5 objects
      ]
    }
    ```

2.  **Extraction:** Parse the input JSON content to extract a Python list of all stock symbols found in the `scanned_stocks` array (e.g., `["TSLA", "GOOG", "NVDA", "BA", "AAPL"]`).


### 2. Analysis Execution
1.  For the extracted symbols in the last step, you must retrieve historical price data for the symbol and generate an aggregated technical signal (BULLISH, BEARISH, or NEUTRAL) with a detailed justification based on the 2-out-of-3 TA rule (SMA, RSI, MACD).


### 3. Final Output Format
The final output **MUST** be a single JSON list of dictionaries. Each dictionary must contain the following four keys:

```json
[
  {
    "symbol": "TICKER_1",
    "company_name": "Company Name 1",
    "aggregated_sentiment": "BULLISH" | "BEARISH" | "NEUTRAL",
    "justification": "Detailed indicator breakdown and consensus score."
  },
  // ... 
]
```
"""


raw_technical_analyst_agent = Agent(
    name="raw_technical_analyst_agent",
    model=model,
    instruction=RAW_PROMPT,
    tools=[
        fetch_price_and_technical_analysis
    ],
    output_key="raw_technical_analyst_findings",
    # The result of this agent will be stored in the session state with this key.
)

print("✅ Raw Technical Analysis Agent created.")


# -----  STRUCTURED TICKER SCANNER AGENT -----
STRUCTURED_PROMPT = (
    """Role: You are a highly reliable **JSON Structure Enforcement Agent**. 
    Your sole function is to take the raw, perhaps unstructured or semi-structured text output from another agent and reformat it into a single, clean, and strictly valid JSON object."""
    """Task: Read the provided ticker findings: {raw_technical_analyst_findings}. Respond ONLY with a JSON object matching this exact schema."""
    """
    Requirements:
    1.  Your output **MUST** be a single, raw JSON object.
    2.  **DO NOT** include any text, explanations, greetings, warnings, or code fences (e.g., ```json) in your response.
    3.  The final JSON object **MUST** be parsable and conform exactly to the schema below.
    """
    """
    Input: a list of sentiment analysis results provided in the {raw_technical_analyst_findings}.
    Output: a list of sentiment results in the following JSON format:
    ```json
    {
      "social_media_sentiments": [
        {
          "symbol": "GOOG",
          "company_name": "Alphabet Inc.",
          "aggregated_sentiment": "bullish",
          "justification": "Sentiment is highly divided; bullish posts cited new government contracts",
        }
        // ... complete with 4 more tickers
      ]
    }
    ```
    """
)


structured_technical_analyst_agent = Agent(
    model=model,
    name="structured_technical_analyst_agent",
    description="Enforce JSON format for technical analysis result.",
    instruction=STRUCTURED_PROMPT,
    output_schema=TechnicalSentimentOutput,
    output_key="structured_technical_analyst_findings",
)

print("✅ Structured Technical Analysis Agent created")


# -----  FULL TICKER SCANNER AGENT -----
root_technical_analyst_agent = SequentialAgent(
    name="root_technical_analyst_agent",
    sub_agents=[raw_technical_analyst_agent, structured_technical_analyst_agent],
)

print("✅ Technical Analysis Agent  created")
