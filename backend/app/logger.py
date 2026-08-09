import logging
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

file_handler = RotatingFileHandler(
    "app.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(LOG_FORMAT)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger = logging.getLogger("complianceai")
logger.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger.propagate = False