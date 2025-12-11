# utils/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(name, log_file, level=logging.INFO):
    """
    Setup a logger with file and console handlers
    """
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation (max 10MB, keep 5 backup files)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create application logger
app_logger = setup_logger('app', 'logs/app.log')
blockchain_logger = setup_logger('blockchain', 'logs/blockchain.log')
ai_logger = setup_logger('ai', 'logs/ai.log')
