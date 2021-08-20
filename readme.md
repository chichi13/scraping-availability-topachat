## Scraping Disponibilité TopAchat / IFTTT

```bash
sudo apt update

sudo apt -y upgrade

git clone https://github.com/chichi13/scrapingDisponibilityTopAchat.git


# python3-pip ou python3.8-pip selon la version par défaut de python3
sudo apt install python3-pip

pip3 install virtualenv

sudo apt install python3-venv

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirement.txt
```

- Remplir products.csv avec des liens TopAchat
- Avoir un fichier `.env` dans `config/` :

```
IFTTT_WEBHOOK_URL=https://maker.ifttt.com/trigger/{EVENT}/with/key/{API_KEY}
REDIS_CONNECTION=False
```

- Remplacer `EVENT_NAME` et `API_KEY` dans `config/.env` (`API_KEY` trouvable https://ifttt.com/maker_webhooks/settings)
- Exécuter le script

```bash
python3 get_stock.py
```
