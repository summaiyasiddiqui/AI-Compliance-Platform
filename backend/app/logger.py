import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

formatter = logging.Formatter(LOG_FORMAT)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger("complianceai")
logger.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(console_handler)

logger.propagate = False