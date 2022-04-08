# Scraping Disponibilité TopAchat / IFTTT

## Lancer avec docker :

- Remplir products.csv avec des liens TopAchat
- Avoir un fichier `.env` dans `config/` :

```
IFTTT_WEBHOOK_URL=https://maker.ifttt.com/trigger/{EVENT}/with/key/{API_KEY}
REDIS_CONNECTION=True # default
REDIS_URL=localhost # default
REDIS_SOCKET_TIMEOUT=5 # default
TIME_TO_EXPIRE=3 # default : int in hour
LOG_LEVEL=INFO # default
SLEEP_TIME=10 # default
```

- Remplacer `EVENT_NAME` et `API_KEY` dans `config/.env` (`API_KEY` trouvable https://ifttt.com/maker_webhooks/settings)
- Lancer un container redis :

```bash
docker network create scraping
docker volume create scraping-redis
docker run --name scraping-redis -v scraping-redis:/data --network scraping -d redis
# Ou si on veut lancer le script en local :
docker run --name scraping-redis -v scraping-redis:/data -p 6379:6379 -d redis
```

- On va ensuite build notre app puis l'exécuter :

```bash
docker build . -t scraping:prod -f docker/dockerfile
docker run --name scraping-prod --network scraping --env-file config/.env -it scraping:prod
```
