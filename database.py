# Importation des modules de gestion de base de données et de sessions
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from typing import Optional

# Initialisation de l'instance SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modèle représentant un utilisateur du système (Administrateur ou Utilisateur standard)."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' ou 'admin'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relations avec les autres tables
    signalements = db.relationship('Signalement', backref='user', lazy=True)
    articles = db.relationship('Article', backref='auteur', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class PhraseMultilingue(db.Model):
    """
    Modèle central pour la base de connaissances IA : 
    Stocke les déclencheurs multilingues, les intents et les réponses.
    """
    __tablename__ = 'phrases_multilingues'
    
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50), nullable=True)
    categorie = db.Column(db.String(50), nullable=True, index=True)
    
    # Textes d'entrée utilisateur (Entraînement/Phrases clés)
    francais_local = db.Column(db.Text, nullable=True)
    kiswahili = db.Column(db.Text, nullable=True)
    kifuliiru = db.Column(db.Text, nullable=True)
    kibembe = db.Column(db.Text, nullable=True)
    
    # Identifiant unique de l'intention
    intent = db.Column(db.String(50), nullable=False, index=True)
    
    # Réponses associées dans les différentes langues
    reponse_fr = db.Column(db.Text, nullable=True)
    reponse_sw = db.Column(db.Text, nullable=True)
    reponse_kir = db.Column(db.Text, nullable=True)
    reponse_kib = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Phrase {self.intent}>'


class Signalement(db.Model):
    """Modèle de données pour les signalements d'urgence ou épidémiologiques."""
    __tablename__ = 'signalements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 
    
    symptome = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    localisation = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    date_signalement = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)


class Article(db.Model):
    """Modèle pour la gestion des articles d'actualités et de prévention."""
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    
    date_publication = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    auteur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


class CentreSante(db.Model):
    """Modèle de référencement des centres de santé et hôpitaux."""
    __tablename__ = 'centres_sante'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    adresse = db.Column(db.String(300), nullable=True)
    telephone = db.Column(db.String(50), nullable=True)
    
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)