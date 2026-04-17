"""AlphaGPT Checkpointer API.

This file serves as the main interface for the checkpointing system in AlphaGPT.
It provides a clean API for integrating with LangGraph and working with the database.
"""

import logging
from typing import Any, Dict, List, Union

import sqlalchemy.exc
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from agent.database.operations.alpha_operations import (
    get_alphas_for_hypothesis,
    save_alphas,
)
from agent.database.operations.backtest_operations import (
    get_backtest_results_for_alpha,
    save_backtest_results,
)
from agent.database.operations.db_connection import (
    create_tables,
    get_db_connection_params,
    get_db_engine,
    get_db_url,
)
from agent.database.operations.hypothesis_operations import (
    get_hypothesis_history,
    save_hypothesis,
)

logger = logging.getLogger(__name__)


class AlphaGPTCheckpointer:
    """Custom checkpointer for AlphaGPT.

    Saves state data to both LangGraph checkpointer and our custom database
    tables for querying later.
    """

    def __init__(self, postgres_saver: Union[PostgresSaver, AsyncPostgresSaver] = None):
        """Initialize the AlphaGPT checkpointer with a PostgreSQL saver.

        Args:
            postgres_saver: The LangGraph PostgreSQL saver to use
        """
        self.postgres_saver = postgres_saver or self._create_postgres_saver()
        self.engine = get_db_engine()

        # Ensure tables exist (skip if database is unavailable)
        try:
            create_tables(self.engine)
        except (sqlalchemy.exc.OperationalError, sqlalchemy.exc.DatabaseError) as e:
            logger.warning("Could not create database tables: %s", e)
            logger.warning("Continuing without persistent storage.")

    def _create_postgres_saver(self) -> PostgresSaver:
        """Create a PostgresSaver instance for LangGraph."""
        # Get database URL from centralized function
        db_url = get_db_url()

        # Get individual parameters for error reporting
        db_params = get_db_connection_params()

        try:
            # Try newer LangGraph versions API
            return PostgresSaver.from_conn_string(db_url)
        except Exception as e:
            # Last resort fallback
            import traceback

            from langgraph.checkpoint.memory import MemorySaver

            logger.warning(
                "Using MemorySaver as fallback - PostgreSQL connection failed: %s", e
            )
            logger.warning(
                "Connection details: host=%s, port=%s, db=%s, user=%s",
                db_params['host'], db_params['port'], db_params['db'], db_params['user'],
            )
            logger.debug("Error details: %s", traceback.format_exc())

            return MemorySaver()

    def get_saver(self) -> BaseCheckpointSaver:
        """Return the underlying PostgreSQL saver for LangGraph."""
        return self.postgres_saver

    def save_state(self, config: RunnableConfig, state_values: Dict[str, Any]) -> None:
        """Save all state data to our custom database tables.

        Args:
            config: LangGraph config
            state_values: The current state values
        """
        thread_id = config.get("configurable", {}).get("thread_id")
        checkpoint_id = config.get("configurable", {}).get("checkpoint_id")

        if not thread_id or not checkpoint_id:
            return

        # Save hypothesis first
        hypothesis = save_hypothesis(thread_id, checkpoint_id, state_values)

        # Save alphas if we have a hypothesis
        if hypothesis:
            save_alphas(thread_id, checkpoint_id, state_values, hypothesis.id)

        # Save backtest results
        save_backtest_results(thread_id, checkpoint_id, state_values)

    def get_hypothesis_history(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get the history of hypotheses for a thread.

        Args:
            thread_id: The thread ID to query

        Returns:
            List of hypothesis dictionaries
        """
        return get_hypothesis_history(thread_id)

    def get_alphas_for_hypothesis(self, hypothesis_id: int) -> List[Dict[str, Any]]:
        """Get all alphas for a specific hypothesis.

        Args:
            hypothesis_id: The hypothesis ID to query

        Returns:
            List of alpha dictionaries
        """
        return get_alphas_for_hypothesis(hypothesis_id)

    def get_backtest_results_for_alpha(self, alpha_id: int) -> List[Dict[str, Any]]:
        """Get all backtest results for a specific alpha.

        Args:
            alpha_id: The alpha ID to query

        Returns:
            List of backtest result dictionaries
        """
        return get_backtest_results_for_alpha(alpha_id)


def get_checkpoint_manager() -> AlphaGPTCheckpointer:
    """Create and return an AlphaGPT checkpointer instance.

    This manages both LangGraph checkpointing and our custom data storage.

    Returns:
        AlphaGPTCheckpointer instance
    """
    return AlphaGPTCheckpointer()
