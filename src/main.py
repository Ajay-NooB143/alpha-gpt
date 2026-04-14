"""Entry point for the Alpha-GPT trading bot."""
import asyncio
import os

from agent.graph import create_graph


async def main():
    """Run the Alpha-GPT trading bot workflow."""
    graph = create_graph()

    config = {
        "configurable": {
            "thread_id": os.environ.get("THREAD_ID", "trading-bot-run"),
        }
    }

    initial_state = {
        "trading_idea": os.environ.get(
            "TRADING_IDEA",
            "Momentum-based strategy using volume and closing price",
        )
    }

    return await graph.ainvoke(initial_state, config=config)


if __name__ == "__main__":
    asyncio.run(main())
