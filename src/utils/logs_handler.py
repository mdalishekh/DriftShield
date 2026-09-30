import logging
import sys
from pathlib import Path
from datetime import datetime

from src.utils.request_context import get_request_id


# Log file path
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"


class RequestIDFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id() or "-"
        return True


# Formatter
formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d | %(levelname)-8s | %(name)s | req=%(request_id)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# Logger
logger = logging.getLogger("DriftShield")
logger.setLevel(logging.DEBUG)


# Prevent duplicate handlers
logger.handlers.clear()


# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
console_handler.addFilter(RequestIDFilter())


# File handler
file_handler = logging.FileHandler(
    LOG_FILE,
    mode="a",
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
file_handler.addFilter(RequestIDFilter())


# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.propagate = False