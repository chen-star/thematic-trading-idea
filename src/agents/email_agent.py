import sys
from agents.configs.retry_config import retry_config
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)

email_mcp_connection = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="fastmcp",
            args=["run", "src/mcp_server/email_server.py"],
        ),
        timeout=240,
    ),
)

PROMPT = f"""
    You are an executive assistant.
    Your goal is to take the analysis summary provided by the previous agent and email it to the client.
    
    1. Look at the conversation history to find the summary text in session state 'final_summary'.
    2. CALL the 'send_email' tool.
    3. Use 'Daily Trading Idea Analysis' as the subject.
    4. Use the summary text as the body.
"""

email_agent = Agent(
    name="EmailAgent", model=model, tools=[email_mcp_connection], instruction=PROMPT
)
