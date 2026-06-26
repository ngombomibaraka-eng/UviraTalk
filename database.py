from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from typing import List, Optional

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    Modèle représentant un utilisateur du système (Admin ou Utilisateur standard).
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' ou 'admin'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relations : Un utilisateur peut avoir plusieurs signalements et articles
    signalements = db.relationship('Signalement', backref='user', lazy=True)
    articles = db.relationship('Article', backref='auteur', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        """Convertit l'objet utilisateur en dictionnaire pour l'API."""
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PhraseMultilingue(db.Model):
    """
    Modèle central pour l'IA : Stocke les phrases d'entraînement, les intents 
    et les réponses multilingues.
    """
    __tablename__ = 'phrases_multilingues'
    
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50), nullable=True)
    categorie = db.Column(db.String(50), nullable=True, index=True)
    
    # Colonnes pour stocker les déclencheurs (Input de l'utilisateur)
    # On utilise Text pour stocker plusieurs variantes séparées par des virgules
    francais_local = db.Column(db.Text, nullable=True)
    kiswahili = db.Column(db.Text, nullable=True)
    kifuliiru = db.Column(db.Text, nullable=True)
    kibembe = db.Column(db.Text, nullable=True)
    
    # Intent (catégorie de détection)
    intent = db.Column(db.String(50), nullable=False, index=True)
    
    # Colonnes pour stocker les réponses de l'IA (Output)
    reponse_fr = db.Column(db.Text, nullable=True)
    reponse_sw = db.Column(db.Text, nullable=True)
    reponse_kir = db.Column(db.Text, nullable=True)
    reponse_kib = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Phrase {self.intent}>'

    def get_response(self, lang_code: str) -> Optional[str]:
        """
        Récupère la réponse dans la langue demandée, avec fallback sur le français.
        lang_code peut être 'fr', 'sw', 'kir', 'kib'.
        """
        lang_map = {
            'fr': self.reponse_fr,
            'sw': self.reponse_sw,
            'kir': self.reponse_kir,
            'kib': self.reponse_kib
        }
        
        # Essayer la langue demandée
        response = lang_map.get(lang_code)
        if response:
            return response
        
        # Fallback sur le français
        if self.reponse_fr:
            return self.reponse_fr
            
        return None

class Signalement(db.Model):
    """
    Modèle pour stocker les signalements communautaires de santé.
    """
    __tablename__ = 'signalements'
    
    id = db.Column(db.Integer, primary_key=True)
    # Peut être null si le visiteur n'est pas connecté
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 
    
    symptome = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    localisation = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    date_signalement = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    def __repr__(self):
        return f'<Signalement {self.symptome} - {self.localisation}>'

    def to_dict(self):
        return {
            'id': self.id,
            'symptome': self.symptome,
            'localisation': self.localisation,
            'date': self.date_signalement.strftime('%d/%m/%Y %H:%M')
        }

class Article(db.Model):
    """
    Modèle pour les articles d'actualité ou de prévention (Blog santé).
    """
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)  # 'actualite', 'conseil', 'campagne'
    
    date_publication = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    auteur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<Article {self.titre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'contenu': self.contenu[:100] + '...' if len(self.contenu) > 100 else self.contenu,
            'categorie': self.categorie,
            'date': self.date_publication.strftime('%d/%m/%Y')
        }

class CentreSante(db.Model):
    """
    Modèle pour référencer les centres de santé géolocalisés.
    """
    __tablename__ = 'centres_sante'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    adresse = db.Column(db.String(300), nullable=True)
    telephone = db.Column(db.String(50), nullable=True)
    
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Centre {self.nom}>'

    def to_dict(self):
        return {
            'nom': self.nom,
            'adresse': self.adresse,
            'telephone': self.telephone,
            'lat': self.latitude,
            'lng': self.longitude
        }
        