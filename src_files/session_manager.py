"""
Session and Memory Management
"""

from google.adk.sessions import InMemorySessionService
from google.adk.memory import MemoryBank
import logging

logger = logging.getLogger(__name__)

# Initialize global session service
session_service = InMemorySessionService()

# Initialize global memory bank
memory_bank = MemoryBank()


def store_baseline_data(metric_name: str, baseline_stats: dict) -> bool:
    """
    Store historical baseline data in Memory Bank.
    
    Args:
        metric_name: Name of the KPI metric
        baseline_stats: Dictionary with mean, std, percentiles, etc.
    
    Returns:
        Success boolean
    """
    try:
        from datetime import datetime
        memory_key = f"baseline_{metric_name}_{datetime.now().strftime('%Y%m')}"
        memory_bank.store(memory_key, baseline_stats)
        logger.info(f"MEMORY_BANK: Stored baseline for {metric_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to store baseline: {e}")
        return False


def retrieve_baseline_data(metric_name: str, months_back: int = 3) -> dict:
    """
    Retrieve historical baseline data from Memory Bank.
    
    Args:
        metric_name: Name of the KPI metric
        months_back: How many months of history to retrieve
    
    Returns:
        Baseline statistics or None
    """
    try:
        from datetime import datetime
        memory_key = f"baseline_{metric_name}_{datetime.now().strftime('%Y%m')}"
        baseline = memory_bank.retrieve(memory_key)
        logger.info(f"MEMORY_BANK: Retrieved baseline for {metric_name}")
        return baseline
    except Exception as e:
        logger.warning(f"No baseline found for {metric_name}: {e}")
        return None
