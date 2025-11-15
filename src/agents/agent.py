from agents.momentum_analysis_agent import momentum_analysis_agent
from agents.plugin.count_model_call_plugin import CountModelCallPlugin
from agents.x_kol_rank_agent import x_kol_rank_agent
from agents.configs.context_compaction_config import context_compaction_config

from google.adk.agents import ParallelAgent, SequentialAgent
from google.adk.apps import App

parallel_agent_team = ParallelAgent(
    name="ParallelAgentTeam",
    sub_agents=[x_kol_rank_agent],
)

root_agent = SequentialAgent(
    name="RootAgent",
    sub_agents=[parallel_agent_team, momentum_analysis_agent],
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
