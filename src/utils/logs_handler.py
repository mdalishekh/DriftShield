import logging
import sys
from pathlib import Path
from datetime import datetime

# Log file path
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"

# Formatter
formatter = logging.Formatter(
    fmt="%(asctime)s.%(msecs)03d | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Logger
logger = logging.getLogger("DriftShield")
logger.setLevel(logging.DEBUG)

# Console handler (dev mein sab dikhega)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# File handler (append mode)
file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)