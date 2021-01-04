import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import requests
import logging


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}

urls = []
products = []
prices = []
stocks = []
notified_urls = {}
logging.basicConfig(filename='scraping.log', filemode='w', format='[%(asctime)s] - [%(levelname)s] - %(message)s')


def send_ifttt_notification(name, price, url, notified_urls):
    ifttt_webhook_url = "https://maker.ifttt.com/trigger/disponibilite_topachat/with/key/c88QyHay9oOR4eBevrdUDP"
    report = {}

    if url not in notified_urls or notified_urls[url] < datetime.now():
        logging.info("Send notification for %s", name)

        report["value1"] = name
        report["value2"] = price
        report["value3"] = url
        requests.post(ifttt_webhook_url, data=report)
        notified_urls[url] = datetime.now() + timedelta(hours=3)


def search_disponibility():
    prod_tracker = pd.read_csv("trackers/products.csv")
    prod_tracker_urls = prod_tracker.url

    for url in prod_tracker_urls:
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, features="lxml")

        name = soup.find("h1", attrs={"class": "fn"})
        price = soup.find("span", attrs={"class": "priceFinal fp44"})

        logging.info("Scraping %s...", str(name.text))

        if soup.find("section", attrs={"class": "cart-box en-rupture"}) is not None:
            stock = "En rupture"
        else:
            stock = "Disponible"

        if stock == "Disponible":
            products.append(name.text)
            prices.append(price.text)
            stocks.append(stock)
            urls.append(url)
            send_ifttt_notification(name.text, price.text, url, notified_urls)

    df = pd.DataFrame(
        {"Nom du produit": products, "Prix": prices, "Stock": stocks, "URL": urls}
    )
    df.to_csv("stock.csv", index=False, encoding="utf-8")


while True:
    try:
        search_disponibility()
        time.sleep(10)
    except Exception as e:
        logging.error(str(e))
