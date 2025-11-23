import asyncio
import sys
import logging

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from termcolor import colored

from agents.agent import app
from utils.cli_utils import print_centered_title, print_centered, center_text

# For debugging purposes
# Comment out for production
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# load API keys and settings
load_dotenv()

# Set a Runner using the imported application object
runner = InMemoryRunner(app=app)


def print_cli_title() -> None:
    # Top Border (Bright White)
    print_centered(colored("#" * 60, "white", attrs=["bold"]))

    # Title - ASCII text in BRIGHT WHITE with shadow effect
    print_centered_title("Trading Idea Agent", "big", "cyan", attrs=["bold", "dark"])

    # Separator line with sparkle effect (Yellow/Bright)
    print_centered(colored("💎" * 30, "yellow", attrs=["bold"]))

    # Taglines in contrasting colors
    print_centered(
        colored(
            "💰 Specialized Stock Analysis Agent CLI! 🤖",
            "green",
            attrs=["bold", "underline"],
        )
    )
    print_centered(
        colored("🔥 DISCOVER THE HOTTEST THEMATIC STOCKS! 📈", "blue", attrs=["bold"])
    )

    # Bottom Border (Bright Cyan)
    print_centered(colored("#" * 60, "white", attrs=["bold"]))


def get_user_thematic_topic_input() -> str | None:
    # Loop until valid input is received
    while True:
        try:
            print("\n")
            print(
                colored(
                    center_text(
                        "🚀 Enter the thematic investment topic (e.g., 'Mega 7', 'AI Application', 'Robotics', etc.)"
                    ),
                    "cyan",
                    attrs=["bold"],
                )
            )
            thematic_topic = input(colored(">>> ", "green", attrs=["bold"]))

            if not thematic_topic.strip():
                print_centered(
                    colored(
                        "😿 Sorry. Topic cannot be empty. Please try again.",
                        "white",
                        "on_red",
                        attrs=["bold"],
                    )
                )
                continue

            print("\n")
            return thematic_topic.strip()

        except KeyboardInterrupt:
            print_centered(
                colored(
                    "\n\n😿 Input cancelled by user. Exiting.",
                    "white",
                    "on_red",
                    attrs=["bold"],
                )
            )
            sys.exit(0)


def thematic_topic_query(thematic_topic: str) -> str:
    return f"The thematic topic is: '{thematic_topic}'. Please execute the task as defined in your system instructions."


def print_waiting_analysis(thematic_topic: str) -> None:
    print_centered(
        colored(f"Analyzing topic: '{thematic_topic}'...", "magenta", attrs=["bold"])
    )
    print_centered(
        colored("⏳ Please wait while the Agent team runs its analysis...", "yellow")
    )


from agents.email_agent import email_mcp_connection


async def main():
    print_cli_title()

    thematic_topic = get_user_thematic_topic_input()
    agent_query = thematic_topic_query(thematic_topic)

    if not thematic_topic:
        sys.exit(0)

    # Restored the call to the waiting agents' response
    print_waiting_analysis(thematic_topic)

    try:  # run_debug() requires ADK Python 1.18 or higher:
        response = await runner.run_debug(agent_query)
        print_centered(
            colored(
                f"--- AGENT ANALYSIS COMPLETE for the thematic topic '{thematic_topic}' ---",
                "green",
                attrs=["bold"],
            )
        )

    except Exception as e:
        print(f"An error occurred during agent execution: {e}")

    finally:
        # Explicitly close the MCP connection to avoid asyncio errors on exit
        await email_mcp_connection.close()


if __name__ == "__main__":
    asyncio.run(main())
