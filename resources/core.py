import logging
from datetime import timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup

from resources.config import settings

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/41.0.2228.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}

urls = []
products = []
prices = []
stocks = []


def send_ifttt_notification(name, price, url, storage):
    report = {}

    if url not in storage:
        logging.info("Send notification for %s", name)

        report["value1"] = name
        report["value2"] = price
        report["value3"] = url
        requests.post(settings.IFTTT_WEBHOOK_URL, data=report)
        storage.set_key(url, timedelta(hours=3))


def search_disponibility(storage):
    disponibility = ""
    prod_tracker = pd.read_csv("trackers/products.csv")
    prod_tracker_urls = prod_tracker.url

    session = requests.Session()    

    for url in prod_tracker_urls:
        page = session.get(url)
        soup = BeautifulSoup(page.content, features="lxml")

        name = soup.find("h1", attrs={"class": "fn"})
        price = soup.find("span", attrs={"class": "priceFinal fp44"})
        logging.info(f"Scraping TopAchat {name.text}...")
        disponibility = soup.find(
            "section", attrs={"class": "cart-box en-rupture"}
        )

        if disponibility is not None:
            logging.info(f"{name.text} en rupture de stock.")
        else:
            stock = "Disponible"
            products.append(name.text)
            prices.append(price.text)
            stocks.append(stock)
            urls.append(url)
            send_ifttt_notification(name.text, price.text, url, storage)
