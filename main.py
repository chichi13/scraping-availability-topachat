import asyncio
import logging
import time

from resources.config import settings
from resources.core import get_url
from resources.expiry_method import LocalStorage, RedisStorage


async def main():
    logging.basicConfig(
        format="[%(asctime)s] - [%(levelname)s] - %(message)s",
        level=settings.LOG_LEVEL,
    )
    logging.info("Starting scraping...")

    storage = LocalStorage() if not settings.REDIS_CONNECTION else RedisStorage()

    while True:
        try:
            await get_url(storage)
            logging.info(f"Waiting {settings.SLEEP_TIME} seconds...")
            time.sleep(settings.SLEEP_TIME)
        except Exception as e:
            logging.error(str(e))


if __name__ == "__main__":
    asyncio.run(main())
