from agents.configs.retry_config import retry_config
from agents.data_models.ticker_scanner_agent_data_model import ScannerAgentListOutput
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config
)

# -----  RAW TICKER SCANNER AGENT -----
RAW_PROMPT = (
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

raw_ticker_scanner_agent = Agent(
    name="ticker_scanner_agent",
    model=model,
    instruction=RAW_PROMPT,
    tools=[google_search],
    output_key="raw_ticker_scanner_findings",
    # The result of this agent will be stored in the session state with this key.
)

print("✅ Raw Ticker Scanner Agent created.")

# -----  STRUCTURED TICKER SCANNER AGENT -----
STRUCTURED_PROMPT = (
    """Role: You are a highly reliable **JSON Structure Enforcement Agent**. 
    Your sole function is to take the raw, perhaps unstructured or semi-structured text output from another agent and reformat it into a single, clean, and strictly valid JSON object."""
    """Task: Read the provided ticker findings: {raw_ticker_scanner_findings}. Respond ONLY with a JSON object matching this exact schema."""
    """
    Requirements:
    1.  Your output **MUST** be a single, raw JSON object.
    2.  **DO NOT** include any text, explanations, greetings, warnings, or code fences (e.g., ```json) in your response.
    3.  The final JSON object **MUST** be parsable and conform exactly to the schema below.
    """
    """
    Input: a list of tickers (symbol, company name, justification) provided in the {raw_ticker_scanner_findings}.
    Output: a ranked list of 5 tickers in the following JSON format:
    ```json
    {
      "scanned_stocks": [
        {
          "symbol": "BA",
          "company_name": "Boeing Co.",
          "justification": "Boeing is the largest US-based manufacturer of defense and commercial aircraft, making it highly relevant to the Aerospace and Defense theme."
        },
        {
          "symbol": "LMT",
          "company_name": "Lockheed Martin Corp.",
          "justification": "The company is the world's largest defense contractor, focusing on advanced technologies like fighter jets and missile systems, essential for the Defense theme."
        },
        {
          "symbol": "RTX",
          "company_name": "RTX Corporation",
          "justification": "A major supplier of defense electronics, missile systems, and engines for military and commercial aircraft, providing deep exposure to both sectors."
        },
        {
          "symbol": "GD",
          "company_name": "General Dynamics Corp.",
          "justification": "General Dynamics provides a broad range of defense products, including land combat vehicles, naval ships, and Gulfstream business jets."
        },
        {
          "symbol": "NOC",
          "company_name": "Northrop Grumman Corp.",
          "justification": "A key player in advanced military hardware, including stealth bombers, autonomous systems, and strategic missile defense technologies."
        }
      ]
    }
    ```
    """
)

structured_ticker_scanner_agent = Agent(
    model=model,
    name="structured_ticker_scanner_agent",
    description="Enforce JSON format for scanned tickers.",
    instruction=STRUCTURED_PROMPT,
    output_schema=ScannerAgentListOutput,
    output_key="structured_ticker_scanner_findings",
)

print("✅ Structured Ticker Scanner Agent created.")

# -----  FULL TICKER SCANNER AGENT -----
root_ticker_scanner_agent = SequentialAgent(
    name="root_ticker_scanner_agent",
    sub_agents=[raw_ticker_scanner_agent, structured_ticker_scanner_agent],
)

print("✅ Root Ticker Scanner Agent created.")
