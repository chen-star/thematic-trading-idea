from agents.configs.retry_config import retry_config
from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini

from agents.data_models.institution_rating_agent_data_model import InstitutionRatingOutput

from src.function_tools.get_and_analyze_institution_rating import run_analysis_for_multiple_tickers

model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config
)

# -----  RAW AGENT -----
RAW_PROMPT = """
    **Role:** Financial Data Processor and Sentiment Aggregator.
    
    **Objective:** The agent's sole purpose is to process raw JSON data from a financial screening source, extract all relevant stock symbols, and use the provided `run_analysis_for_multiple_tickers` function tool to generate a detailed sentiment analysis report.
    
    ### Task Instructions and Workflow
    
    1. Input and Data Extraction

        * The initial input will be a JSON object, which represents the content stored in the session state key {structured_ticker_scanner_findings}.

        ### Input Structure:
        ```json
        {
          "scanned_stocks": [
            {"symbol": "TICKER_1", ...},
            // ... up to 5 objects
          ]
        }
        ```
    
        * Parse the input JSON and generate a clean Python list of all 5 stock symbols (e.g., `["TICKER_1", "TICKER_2", "TICKER_3", "TICKER_4", "TICKER_5"]`).
    
    2. **Tool Execution (Core Task):**
    
       * **Mandatory Tool Use:** You **must** call the `run_analysis_for_multiple_tickers` function tool.
    
       * **Input Argument:** The single argument to this function must be the consolidated list of symbols created in Step 1.
    
    3. **Output Formatting:**
    
       * The agent's final output **must be the raw JSON list of objects** returned directly by the `run_analysis_for_multiple_tickers` tool.
    
       * **DO NOT** add any conversational text, explanation, or wrapper elements (like Markdown code blocks for JSON) to the final output. The output must be the pure, valid JSON string containing the list of sentiment analysis results (symbol, aggregated_sentiment, justification) for all processed tickers.
    
              Output Example:
       ```json
          [
            {
                "symbol": "GOOG",
                "company_name": "Alphabet Inc. (GOOG)",
                "aggregated_sentiment": "bullish",
                "justification": "Sentiment calculated as 'bullish' because Total Buy (25) was compared to Total Sell (1). Breakdown: Strong Buy=10, Buy=15, Hold=4, Sell=1, Strong Sell=0."
            },
            {
                "symbol": "TSLA",
                "company_name": "Tesla, Inc.",
                "aggregated_sentiment": "neutral",
                "justification": "Sentiment calculated as 'neutral' because Total Buy (10) was compared to Total Sell (10). Breakdown: Strong Buy=5, Buy=5, Hold=12, Sell=6, Strong Sell=4."
            },
            {
                "symbol": "HIMS",
                "company_name": "Hims & Hers Health, Inc.",
                "aggregated_sentiment": "bearish",
                "justification": "Sentiment calculated as 'bearish' because Total Buy (8) was compared to Total Sell (15). Breakdown: Strong Buy=1, Buy=7, Hold=2, Sell=10, Strong Sell=5."
            }
        ]
        ```
        
    ### Constraints
    
    * You are forbidden from generating code outside of the function tool execution.
    
    * You must handle cases where the input list is empty or invalid by gracefully returning an empty JSON list or an appropriate error message *within the returned JSON structure*, as handled by the tool.
    
    * The final response must be the JSON output and nothing else.
"""

raw_institution_rating_agent = Agent(
    name="raw_institution_rating_agent",
    model=model,
    instruction=RAW_PROMPT,
    tools=[run_analysis_for_multiple_tickers],
    output_key="raw_institution_rating_findings",
    # The result of this agent will be stored in the session state with this key.
)

print("✅ Raw Institution Rating Agent created.")


# -----  STRUCTURED TICKER SCANNER AGENT -----
STRUCTURED_PROMPT = (
    """Role: You are a highly reliable **JSON Structure Enforcement Agent**. 
    Your sole function is to take the raw, perhaps unstructured or semi-structured text output from another agent and reformat it into a single, clean, and strictly valid JSON object."""
    """Task: Read the provided ticker findings: {raw_institution_rating_findings}. Respond ONLY with a JSON object matching this exact schema."""
    """
    Requirements:
    1.  Your output **MUST** be a single, raw JSON object.
    2.  **DO NOT** include any text, explanations, greetings, warnings, or code fences (e.g., ```json) in your response.
    3.  The final JSON object **MUST** be parsable and conform exactly to the schema below.
    """
    """
    Input: a list of sentiment analysis results provided in the {raw_institution_rating_findings}.
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


structured_institution_rating_agent = Agent(
    model=model,
    name="structured_institution_rating_agent",
    description="Enforce JSON format for institution rating analysis result.",
    instruction=STRUCTURED_PROMPT,
    output_schema=InstitutionRatingOutput,
    output_key="structured_institution_rating_findings",
)

print("✅ Structured Ticker Scanner Agent created.")


# -----  FULL TICKER SCANNER AGENT -----
root_institution_rating_agent = SequentialAgent(
    name="root_institution_rating_agent",
    sub_agents=[raw_institution_rating_agent, structured_institution_rating_agent],
)


print("✅ Root Ticker Scanner Agent created.")