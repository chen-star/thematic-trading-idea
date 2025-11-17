from agents.analysts_team.social_media_sentiment_analyst import root_social_media_sentiment_agent
from agents.analysts_team.institution_rating_analyst import root_institution_rating_agent
from agents.configs.context_compaction_config import context_compaction_config
from agents.plugin.count_model_call_plugin import CountModelCallPlugin
from agents.ticker_scanner_agent import root_ticker_scanner_agent
from google.adk.agents import SequentialAgent
from google.adk.apps import App

# parallel_agent_team = ParallelAgent(
#     name="ParallelAgentTeam",
#     sub_agents=[root_ticker_scanner_agent],
# )
#
# root_agent = SequentialAgent(
#     name="RootAgent",
#     sub_agents=[parallel_agent_team, momentum_analysis_agent],
# )

root_agent = SequentialAgent(
    name="RootAgent",
    sub_agents=[
        root_ticker_scanner_agent,
        # root_social_media_sentiment_agent,
        root_institution_rating_agent,
    ],
)

app = App(
    name="TradingIdeaApp",
    root_agent=root_agent,
    plugins=[
        CountModelCallPlugin()
    ],
    events_compaction_config=context_compaction_config,
)

print("✅ root_agent created.")
