import os
from typing import Optional

from dotenv import load_dotenv
from distutils.util import strtobool


class Config(object):
    """Base configuration."""

    APP_DIR = os.path.dirname(__file__)
    CONFIG_PATH = os.path.join(APP_DIR, "config/.env")

    load_dotenv(CONFIG_PATH)

    def _get(key: str, default: Optional[str] = ""):
        return os.getenv(key, default)

    IFTTT_WEBHOOK_URL = _get("IFTTT_WEBHOOK_URL")
    REDIS_CONNECTION = bool(strtobool(_get("REDIS_CONNECTION", True)))
    REDIS_URL = _get("REDIS_URL", "localhost")
    REDIS_SOCKET_TIMEOUT = int(_get("REDIS_SOCKET_TIMEOUT", 5))
