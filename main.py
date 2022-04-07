import asyncio
import logging
import time

from resources.config import settings
from resources.core import fetch
from resources.expiry_method import LocalStorage, RedisStorage


async def main():
    logging.basicConfig(
        format="[%(asctime)s] - [%(levelname)s] - %(message)s",
        level=logging.INFO,
    )
    logging.info("Started")

    storage = LocalStorage() if not settings.REDIS_CONNECTION else RedisStorage()

    while True:
        try:
            await fetch(storage)
            logging.info("Waiting...")
            time.sleep(10)
        except Exception as e:
            logging.error(str(e))


if __name__ == "__main__":
    asyncio.run(main())
