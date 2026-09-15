# bootstrap.py
"""
Initialisation automatique de la base de donnees.
A executer une seule fois au demarrage de l'application.
"""

import os
import logging
from database import db, DialogueTriage, QAEducation, Utilisateur

logger = logging.getLogger(__name__)


def auto_import_if_empty(flask_app):
    """
    Verifie si la base contient des dialogues.
    Si non, lance l'importation automatiquement.
    """
    with flask_app.app_context():
        count_dialogues = DialogueTriage.query.count()
        count_qa = QAEducation.query.count()
        count_users = Utilisateur.query.count()

        logger.info(f"Base actuelle : {count_dialogues} dialogues, "
                    f"{count_qa} Q&R, {count_users} utilisateurs")

        # Import des dialogues si vide
        if count_dialogues == 0:
            logger.info("Base vide, importation des dialogues...")
            try:
                from import_data import importer_tout
                importer_tout()
                logger.info("Importation des dialogues reussie.")
            except Exception as e:
                logger.error(f"Erreur importation : {e}")

        # Création de l'admin si absent
        with flask_app.app_context():
            admin = Utilisateur.query.filter_by(email='admin@uviratalk.org').first()
            if not admin:
                logger.info("Creation de l'admin par defaut...")
                from auth import hash_password
                admin = Utilisateur(
                    email='admin@uviratalk.org',
                    password_hash=hash_password('admin2026'),
                    role='admin',
                    prenom='Admin',
                    post_nom='UviraTalk',
                    age=30,
                    sexe='Autre',
                    localisation='Uvira',
                )
                db.session.add(admin)
                db.session.commit()
                logger.info("Admin cree : admin@uviratalk.org / admin2026")