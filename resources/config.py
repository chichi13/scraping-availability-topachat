from pydantic import BaseSettings


class Settings(BaseSettings):
    IFTTT_WEBHOOK_URL: str
    REDIS_CONNECTION: bool = True
    REDIS_URL: str = "localhost"
    REDIS_SOCKET_TIMEOUT: int = 5


settings = Settings(_env_file="config/.env", _env_file_encoding="utf-8")
