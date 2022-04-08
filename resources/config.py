from pydantic import BaseSettings


class Settings(BaseSettings):
    IFTTT_WEBHOOK_URL: str
    REDIS_CONNECTION: bool = True
    REDIS_URL: str = "localhost"
    REDIS_SOCKET_TIMEOUT: int = 5
    # TIME_TO_EXPIRE in hour
    TIME_TO_EXPIRE: int = 3
    LOG_LEVEL: str = "INFO"
    SLEEP_TIME: int = 10


settings = Settings(_env_file="config/.env", _env_file_encoding="utf-8")
