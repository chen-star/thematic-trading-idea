from google.adk.agents import ParallelAgent, SequentialAgent

from agents.x_kol_rank_agent import x_kol_rank_agent
from agents.momentum_analysis_agent import momentum_analysis_agent

parallel_agent_team = ParallelAgent(
    name = "ParallelAgentTeam",
    sub_agents = [x_kol_rank_agent],
)

root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[parallel_agent_team, momentum_analysis_agent],
)

print("✅ root_agent created.")
