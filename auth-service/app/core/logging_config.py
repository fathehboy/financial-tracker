import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=1024 * 1024 * 5,  # 5MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(name)s - %(levelname)s - %(message)s"
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    setup_logging()
logger = logging.getLogger(__name__)