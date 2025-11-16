import asyncio
import sys

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from termcolor import colored

from agents.agent import app
from src.utils.cli_utils import print_centered_title, print_centered, center_text

load_dotenv()  # load API keys and settings
# Set a Runner using the imported application object
runner = InMemoryRunner(app=app)


def print_cli_title():
    # Top Border (Bright White)
    print_centered(colored("#" * 60, 'white', attrs=['bold']))

    # Title - ASCII text in BRIGHT WHITE with shadow effect
    print_centered_title('Trading Idea Agent', 'big', 'cyan', attrs=['bold', 'dark'])

    # Separator line with sparkle effect (Yellow/Bright)
    print_centered(colored("💎" * 30, 'yellow', attrs=['bold']))

    # Taglines in contrasting colors
    print_centered(colored("💰 Specialized Stock Analysis Agent CLI! 🤖", 'green', attrs=['bold', 'underline']))
    print_centered(colored("🔥 DISCOVER THE HOTTEST THEMATIC STOCKS! 📈", 'blue', attrs=['bold']))

    # Bottom Border (Bright Cyan)
    print_centered(colored("#" * 60, 'white', attrs=['bold']))


def get_user_thematic_topic_input():
    print("\n\n")
    input_prompt = center_text(
        "🚀 Enter the thematic investment topic you are interested(e.g., 'AI Datacenter', 'Uranium Mining', etc.): ")
    thematic_topic = input(colored(input_prompt, 'white', 'on_blue', attrs=['bold']))
    print("\n")

    if not thematic_topic.strip():
        print_centered(colored("😿 Sorry. Topic cannot be empty. Exiting.", 'white', 'on_red', attrs=['bold']))
        sys.exit(0)

    return thematic_topic.strip()


def thematic_topic_query(thematic_topic):
    return f"The thematic topic is: '{thematic_topic}'. Please execute the task as defined in your system instructions."


async def main():
    print_cli_title()

    agent_query = thematic_topic_query(get_user_thematic_topic_input())

    try:  # run_debug() requires ADK Python 1.18 or higher:
        response = await runner.run_debug(agent_query)

    except Exception as e:
        print(f"An error occurred during agent execution: {e}")


if __name__ == "__main__":
    asyncio.run(main())
