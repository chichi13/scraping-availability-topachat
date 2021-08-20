import os
from typing import Optional

from dotenv import load_dotenv


class Config(object):
    """Base configuration."""

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CONFIG_PATH = os.path.join(ROOT_DIR, "config/.env")

    load_dotenv(CONFIG_PATH)

    def _get(key: str, default: Optional[str] = ""):
        return os.getenv(key, default)

    IFTTT_WEBHOOK_URL = _get("IFTTT_WEBHOOK_URL")
    REDIS_CONNECTION = _get("REDIS_CONNECTION", False)
