"""Entry point for the AlphaGPT trading bot workflow."""

import asyncio
import logging
import os
import uuid
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def run_workflow(trading_idea: Optional[str] = None) -> None:
    """Run the alpha generation workflow."""
    from agent.graph import create_graph

    graph = create_graph()

    idea = trading_idea or os.environ.get(
        "TRADING_IDEA",
        "Momentum-based strategy using volume and closing price",
    )

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    logger.info("Starting AlphaGPT workflow with idea: %s", idea)
    logger.info("Thread ID: %s", thread_id)

    result = await graph.ainvoke({"trading_idea": idea}, config=config)

    coded_alphas = result.get("coded_alphas", [])
    logger.info("Workflow completed. Generated %d coded alpha(s).", len(coded_alphas))

    for alpha in coded_alphas:
        logger.info("Alpha ID: %s", alpha.get("alphaID"))
        logger.info("Description: %s", alpha.get("desc"))


def main() -> None:
    """Run the trading bot."""
    asyncio.run(run_workflow())


if __name__ == "__main__":
    main()
