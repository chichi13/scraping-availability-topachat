import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}

urls = []
products = []
prices = []
stocks = []


def send_ifttt_notification(first, second, third):
    ifttt_webhook_url = "https://maker.ifttt.com/trigger/disponibilite_topachat/with/key/c88QyHay9oOR4eBevrdUDP"
    report = {}
    print("Send notification...")

    report["value1"] = first
    report["value2"] = second
    report["value3"] = third
    requests.post(ifttt_webhook_url, data=report)


def search_disponibility():
    prod_tracker = pd.read_csv("trackers/products.csv")
    prod_tracker_urls = prod_tracker.url
    print("Scraping...")

    for url in prod_tracker_urls:
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, features="lxml")

        name = soup.find("h1", attrs={"class": "fn"})
        price = soup.find("span", attrs={"class": "priceFinal fp44"})

        if soup.find("section", attrs={"class": "cart-box en-rupture"}) is not None:
            stock = "En rupture"
        else:
            stock = "Disponible"

        if stock == "Disponible":
            products.append(name.text)
            prices.append(price.text)
            stocks.append(stock)
            urls.append(url)
            send_ifttt_notification(name.text, price.text, url)

    df = pd.DataFrame(
        {"Nom du produit": products, "Prix": prices, "Stock": stocks, "URL": urls}
    )
    df.to_csv("stock.csv", index=False, encoding="utf-8")


while True:
    search_disponibility()
    time.sleep(10)
