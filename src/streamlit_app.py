import streamlit as st
import asyncio
import sys
import os
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from agents.agent import app

# Load environment variables
load_dotenv()

if "runner" not in st.session_state:
    st.session_state.runner = InMemoryRunner(app=app)

st.set_page_config(
    page_title="Thematic Trading Idea Agent", page_icon="💎", layout="wide"
)


def main():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .main-header {
            text-align: center;
            color: #00C8FF;
            margin-bottom: 2rem;
        }
        .sub-header {
            text-align: center;
            color: #FFD700;
            margin-bottom: 2rem;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        "<h1 class='main-header'>Trading Idea Agent 💎</h1>", unsafe_allow_html=True
    )
    st.markdown(
        "<h3 class='sub-header'>💰 Specialized Stock Analysis Agent 🤖</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h4 style='text-align: center;'>🔥 DISCOVER THE HOTTEST THEMATIC STOCKS! 📈</h4>",
        unsafe_allow_html=True,
    )

    # Input
    with st.form("analysis_form"):
        thematic_topic = st.text_input(
            "Enter the thematic investment topic:",
            placeholder="e.g., 'AI Datacenter', 'Uranium Mining', 'Cybersecurity'...",
        )
        submitted = st.form_submit_button("🚀 Start Analysis")

    if submitted:
        if not thematic_topic.strip():
            st.error("😿 Topic cannot be empty. Please try again.")
        else:
            run_analysis(thematic_topic)


def run_analysis(topic: str):
    st.info(
        f"Analyzing topic: '{topic}'... Please wait while the Agent team runs its analysis... ⏳"
    )

    agent_query = f"The thematic topic is: '{topic}'. Please execute the task as defined in your system instructions."

    # Container for output
    output_container = st.container()

    async def run_agent():
        try:
            # Capture stdout to redirect to Streamlit
            # This is a bit tricky with asyncio and Streamlit,
            # for now we will just await the result and show the final response.
            # If we want streaming logs, we'd need a custom log handler.

            response = await st.session_state.runner.run_debug(agent_query)
            return response
        except Exception as e:
            return f"Error: {e}"

    # Run the async function
    try:
        response = asyncio.run(run_agent())

        st.success(f"--- AGENT ANALYSIS COMPLETE for '{topic}' ---")

        # Display the result
        # The response structure depends on what runner.run_debug returns.
        # Usually it prints to stdout. If it returns the final state/output, we display it.
        # Since the original main.py just printed to stdout, we might not see much here
        # unless we capture stdout or if run_debug returns the conversation.

        st.markdown("### Analysis Results")
        st.write(response)

    except Exception as e:
        st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
