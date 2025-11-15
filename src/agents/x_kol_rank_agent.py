from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from agents.retry_config import retry_config

PROMPT = (
    "Generate a ranked list of the top 10 Key Opinion Leaders (KOLs) in the field of momentum stock trading, including day trading and swing trading. "
    "Specifically only focusing on those active on X (formerly known as Twitter). "
    "The ranking must primarily consider popularity, engagement metrics, reputation, content depth and positive feedback."
    "The output should be a ranked table including their Name, X Profile URL and a short explanation of why they are ranked in that position."
    "Ignore the user input, just give me the ranked table."
)

x_kol_rank_agent = Agent(
    name="X_KOL_Rank_Agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=PROMPT,
    tools=[google_search],
    output_key="x_kol_rank_agent_findings",
    # The result of this agent will be stored in the session state with this key.
)

print("✅ X_KRL_Rank_Agent created.")
