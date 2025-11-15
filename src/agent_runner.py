import asyncio
from google.adk.runners import InMemoryRunner
from src.agents.x_kol_rank_agent import x_kol_rank_agent


async def main() -> None:
    runner = InMemoryRunner(agent=x_kol_rank_agent)
    response = await runner.run_debug("hello")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())