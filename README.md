# Scraping availability TopAchat

This program was used to retrieve the availability status of one or more products on the TopAchat (FR) website.

**It's now a read only repo.**

When the product is available --> Send an IFTTT notification to alert the user that the product is available.

This script was made to get me a graphics card during the component shortage.
It was made for a **totally personal purpose**.

## Basic configuration

- Fill `/trackers/products.csv` with **TopAchat** products links, example:

```text
https://www.topachat.com/pages/detail2_cat_est_...
https://www.topachat.com/pages/detail2_cat_est_...
```

- Have a `.env` file in `config/` :

```
IFTTT_WEBHOOK_URL=https://maker.ifttt.com/trigger/{EVENT}/with/key/{API_KEY}
REDIS_CONNECTION=True # default
REDIS_URL=localhost # default
REDIS_SOCKET_TIMEOUT=5 # default
TIME_TO_EXPIRE=3 # default : int in hour
LOG_LEVEL=INFO # default
SLEEP_TIME=10 # default
```

- Replace `EVENT_NAME` and `API_KEY` in `config/.env` (`API_KEY` found https://ifttt.com/maker_webhooks/settings)

## Run with Docker

- Run a redis container :

```bash
docker network create scraping
docker volume create scraping-redis
docker run --name scraping-redis -v scraping-redis:/data --network scraping -d redis
```

- Build app and run it :

```bash
docker build . -t scraping:prod -f docker/dockerfile
docker run --name scraping-prod --network scraping --env-file config/.env -it scraping:prod
```

## Run without Docker

- Run a local Redis instance or run redis container with exposed port :

```bash
docker run --name scraping-redis -v scraping-redis:/data -p 6379:6379 -d redis
```

- Create a `venv` :

```bash
python3 -m venv venv
```

- Install requirements :

```bash
# For production :
pip3 install -r requirements/prod.txt
# For dev :
pip3 install -r requirements/dev.txt
```

- Run script :

```bash
python3 main.py
```
