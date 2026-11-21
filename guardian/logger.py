
import logging
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "toolchain_guardian.log"


def get_logger():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("ToolchainGuardian")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_event(message, level="info"):
    logger = get_logger()

    if level.lower() == "error":
        logger.error(message)
    elif level.lower() == "warning":
        logger.warning(message)
    else:
        logger.info(message)
