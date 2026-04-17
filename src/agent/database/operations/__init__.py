"""Database operations package.

This package contains database operations for the AlphaGPT database.
"""
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
    get_db_engine,
    get_session_factory,
)
from agent.database.operations.hypothesis_operations import (
    get_hypothesis_history,
    save_hypothesis,
)

__all__ = [
    "get_db_engine", 
    "get_session_factory", 
    "create_tables",
    "save_hypothesis", 
    "get_hypothesis_history",
    "save_alphas", 
    "get_alphas_for_hypothesis",
    "save_backtest_results", 
    "get_backtest_results_for_alpha"
]
