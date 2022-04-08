import asyncio
import logging
from datetime import timedelta

import aiohttp
from bs4 import BeautifulSoup

from resources.config import settings


async def send_ifttt_notification(name, price, url, storage):
    report = {}

    if url in storage:
        return

    logging.info("Send notification for %s", name)

    report["value1"] = name
    report["value2"] = price
    report["value3"] = url
    async with aiohttp.ClientSession() as session:
        await session.post(settings.IFTTT_WEBHOOK_URL, data=report)
    storage.set_key(url, timedelta(hours=settings.TIME_TO_EXPIRE))


async def inspect_and_send(data, url, storage):
    soup = BeautifulSoup(data, features="lxml")

    name = soup.find("h1", attrs={"class": "fn"})
    price = soup.find("span", attrs={"class": "priceFinal fp44"})
    availability = soup.find("section", attrs={"class": "cart-box en-rupture"})
    logging.info(f"Scraping product : {name.text}...")

    if availability is not None:
        logging.info(f"{name.text} en rupture de stock.")
        return
    await send_ifttt_notification(name.text, price.text, url, storage)


async def fetch_all(url, storage):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()
            await inspect_and_send(data, url, storage)


async def get_url(storage):
    prod_tracker = open("trackers/products.csv")
    prod_tracker_urls = prod_tracker.read().splitlines()

    await asyncio.gather(*(fetch_all(url, storage) for url in prod_tracker_urls))
