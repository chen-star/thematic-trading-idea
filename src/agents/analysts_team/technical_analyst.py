from agents.configs.retry_config import retry_config
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini

from agents.data_models.technical_agent_data_model import TechnicalSentimentOutput

from function_tools.fetch_prce_and_technical_analysis import (
    fetch_price_and_technical_analysis,
)

model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)


PROMPT = """
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


root_technical_analyst_agent = Agent(
    name="root_technical_analyst_agent",
    model=model,
    instruction=PROMPT,
    tools=[fetch_price_and_technical_analysis],
    output_key="structured_technical_analyst_findings",
    # The result of this agent will be stored in the session state with this key.
)


print("✅ Technical Analysis Agent  created")
