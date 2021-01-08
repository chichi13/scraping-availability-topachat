import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import requests
import logging
from config.config import ifttt_webhook_url, redis_connection
from expiry_method import LocalStorage, RedisStorage

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/41.0.2228.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}

urls = []
products = []
prices = []
stocks = []
disponibility = ""
storage = None


def send_ifttt_notification(name, price, url):
    report = {}

    if url not in storage:
        logging.info("Send notification for %s", name)

        report["value1"] = name
        report["value2"] = price
        report["value3"] = url
        requests.post(ifttt_webhook_url, data=report)
        storage.setKey(url, timedelta(hours=3))


def search_disponibility():
    prod_tracker = pd.read_csv("trackers/products.csv")
    prod_tracker_urls = prod_tracker.url

    for url in prod_tracker_urls:
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, features="lxml")
        if url.startswith("https://www.topachat.com"):
            name = soup.find("h1", attrs={"class": "fn"})
            price = soup.find("span", attrs={"class": "priceFinal fp44"})
            logging.info("Scraping TopAchat %s...", str(name.text))
            disponibility = soup.find("section", attrs={"class": "cart-box en-rupture"})
        elif url.startswith("https://www.pccomponentes.com"):
            name = soup.find("h1", attrs={"class": "h4"})
            price = soup.find("span", attrs={"class": "baseprice"})
            logging.info("Scraping PCComponentes %s...", str(name.text))
            disponibility = soup.find("button", attrs={"class": "notify-me"})
        else:
            continue

        if disponibility is not None:
            stock = "En rupture"
        else:
            stock = "Disponible"
            products.append(name.text)
            prices.append(price.text)
            stocks.append(stock)
            urls.append(url)
            send_ifttt_notification(name.text, price.text, url)


def main():
    global storage

    logging.basicConfig(
        filename="scraping.log",
        format="[%(asctime)s] - [%(levelname)s] - %(message)s",
        level=logging.INFO,
    )
    logging.info("Started")

    storage = LocalStorage() if not redis_connection else RedisStorage()

    while True:
        try:
            search_disponibility()
            time.sleep(10)
        except Exception as e:
            logging.error(str(e))


if __name__ == "__main__":
    main()
