import logging
from logging.config import dictConfig

# Define logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "[%(asctime)s] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "logs/app.log",
            "formatter": "detailed",
            "mode": "a",  # Append mode
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

# Apply logging configuration
dictConfig(LOGGING_CONFIG)

# Create logger instance
logger = logging.getLogger("ecommerce")
