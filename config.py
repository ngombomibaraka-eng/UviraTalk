# config.py
"""
Configuration centralisee UviraTalk.
Fonctionne en local (Windows) et sur Streamlit Cloud (Linux).

IMPORTANT :
- En local, la base est stockee dans le dossier du projet (persistante).
- Sur Streamlit Cloud, la base est stockee dans /tmp (NON persistante :
  les donnees sont perdues a chaque redemarrage de l'app).
  Pour la persistance, il faut migrer vers PostgreSQL.
"""

import os

# Repertoire du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Detection de l'environnement Streamlit Cloud
IS_CLOUD = os.environ.get("STREAMLIT_SHARING_MODE") == "streamlit" or \
           os.path.exists("/home/appuser") or \
           os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud"

# Chemin de la base
if IS_CLOUD:
    # Sur le cloud : /tmp (ecriture autorisee)
    DB_FILE = "/tmp/uviratalk.db"
else:
    # En local : dossier du projet
    DB_FILE = os.path.join(BASE_DIR, "uviratalk.db")

# URI SQLAlchemy
DB_PATH = f"sqlite:///{DB_FILE}"

# Secret Flask
SECRET_KEY = os.environ.get("SECRET_KEY", "uviratalk-secret-2026")

# Drapeau exporte
IS_CLOUD_ENV = IS_CLOUD