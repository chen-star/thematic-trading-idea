from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from agents.retry_config import retry_config

PROMPT = (
    "Directly output the final output ranked list: {x_kol_rank_agent_findings}."
)

momentum_analysis_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=PROMPT,
    output_key="executive_summary",  # This will be the final output of the entire system.
)

print("✅ momentum_analysis_agent created.")
