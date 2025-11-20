from agents.analysts_team.institution_rating_analyst import root_institution_rating_agent
from agents.analysts_team.social_media_sentiment_analyst import root_social_media_sentiment_agent
from agents.analysts_team.technical_analyst import root_technical_analyst_agent
from agents.configs.context_compaction_config import context_compaction_config
from agents.plugin.count_model_call_plugin import CountModelCallPlugin
from agents.ticker_scanner_agent import root_ticker_scanner_agent
from agents.summarize_agent import summarizer_agent
from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.apps import App

parallel_analyst_agent_team = ParallelAgent(
    name="ParallelAnalystAgentTeam",
    sub_agents=[
        root_social_media_sentiment_agent,
        root_institution_rating_agent,
        root_technical_analyst_agent,
    ],
    description="A team of analysts working in parallel to analyze trading ideas from multiple perspectives.",
)

analysis_summary_agent = SequentialAgent(
    name="AnalysisSummaryAgent",
    sub_agents=[parallel_analyst_agent_team, summarizer_agent],
)

root_agent = SequentialAgent(
    name="RootAgent",
    sub_agents=[
        root_ticker_scanner_agent,
        analysis_summary_agent,
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
