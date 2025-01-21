import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(log_level: Optional[str] = None) -> None:
    """Setup logging configuration with both file and console output.
    
    Args:
        log_level: Optional logging level (DEBUG, INFO, etc.)
    """
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Set up log file path
    log_file = log_dir / "restack_generator.log"
    
    # Determine log level
    level = getattr(logging, (log_level or "INFO").upper())
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Create and configure file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    
    # Create and configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    
    # Get root logger and set its level
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Add handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Create logger for this module
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    logger.debug("Debug logging enabled")
    
    # Set levels for third-party modules
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("cerebras").setLevel(logging.WARNING)