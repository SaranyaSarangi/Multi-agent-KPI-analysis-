"""
Configuration Management for KPI Agent System
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    """System configuration"""
    
    # API Configuration
    google_api_key: str
    default_model: str = "gemini-2.0-flash-exp"
    
    # Detection Configuration
    default_method: str = "ensemble"
    default_sensitivity: str = "medium"
    default_z_threshold: float = 2.0
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: Optional[str] = "kpi_agent.log"
    
    # Performance Configuration
    max_data_points: int = 10000
    enable_caching: bool = True


def load_config() -> Config:
    """
    Load configuration from environment variables.
    
    Returns:
        Config object with all settings
    """
    # Load .env file if it exists
    load_dotenv()
    
    # Get API key (required)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables. "
            "Please set it in your .env file or environment."
        )
    
    # Create config with defaults from env or use built-in defaults
    config = Config(
        google_api_key=api_key,
        default_model=os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp"),
        default_method=os.getenv("DEFAULT_METHOD", "ensemble"),
        default_sensitivity=os.getenv("DEFAULT_SENSITIVITY", "medium"),
        default_z_threshold=float(os.getenv("DEFAULT_Z_THRESHOLD", "2.0")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", "kpi_agent.log"),
    )
    
    return config


# Sensitivity to threshold mappings
SENSITIVITY_THRESHOLDS = {
    "low": {
        "z": 3.0,
        "iqr": 2.0,
        "isolation": 0.05
    },
    "medium": {
        "z": 2.0,
        "iqr": 1.5,
        "isolation": 0.1
    },
    "high": {
        "z": 1.5,
        "iqr": 1.2,
        "isolation": 0.15
    }
}


# Severity classification rules
SEVERITY_RULES = {
    "critical": lambda score, threshold: score > threshold * 3,
    "high": lambda score, threshold: score > threshold * 2,
    "medium": lambda score, threshold: score > threshold * 1.5,
    "low": lambda score, threshold: score > threshold
}
