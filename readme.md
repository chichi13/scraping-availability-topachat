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
- Remplacer EVENT_NAME et API_KEY dans config/config.py

```bash
# Dev :
# Afin de ne pas push la modification config.py et de partager la clé sur Github :
git update-index --assume-unchanged config/config.py
```

- Exécuter le script

```bash
python3 get_stock.py
```