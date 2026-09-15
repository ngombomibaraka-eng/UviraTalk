# database.py
"""
Modeles de donnees UviraTalk.
Toutes les tables sont definies ici.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


# =============================================
# TABLES DE CONTENU MEDICAL
# =============================================

class DialogueTriage(db.Model):
    __tablename__ = 'dialogues_triage'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True)
    theme = db.Column(db.String(50), index=True)
    langue = db.Column(db.String(5), index=True)
    phrase_patient = db.Column(db.Text, nullable=False)
    mots_cles = db.Column(db.Text)
    symptomes_detectes = db.Column(db.Text)
    urgence = db.Column(db.String(30))
    intention = db.Column(db.String(150))
    question_suivante = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Dialogue {self.code} [{self.langue}] {self.theme}>'


class QAEducation(db.Model):
    __tablename__ = 'qa_education'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True)
    theme = db.Column(db.String(80), index=True)
    langue = db.Column(db.String(5), index=True)
    question = db.Column(db.Text, nullable=False)
    reponse = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<QA {self.code} [{self.langue}] {self.theme}>'


class Maladie(db.Model):
    __tablename__ = 'maladies'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    langue = db.Column(db.String(5), index=True)
    nom = db.Column(db.String(200), nullable=False)
    categorie = db.Column(db.String(80), index=True)


class Symptome(db.Model):
    __tablename__ = 'symptomes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    langue = db.Column(db.String(5), index=True)
    description = db.Column(db.Text, nullable=False)


# =============================================
# TABLES D'AUTHENTIFICATION + TRACABILITE
# =============================================

class Utilisateur(db.Model):
    """Utilisateur de l'application (patient ou admin)."""
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='patient')  # 'patient' ou 'admin'

    prenom = db.Column(db.String(80), nullable=False)
    post_nom = db.Column(db.String(80))
    age = db.Column(db.Integer)
    sexe = db.Column(db.String(10))
    localisation = db.Column(db.String(150))

    date_inscription = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    derniere_connexion = db.Column(db.DateTime)

    conversations = db.relationship(
        'Conversation', backref='utilisateur', lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Utilisateur {self.email} ({self.role})>'


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False
    )
    date_debut = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    date_fin = db.Column(db.DateTime)
    nb_messages = db.Column(db.Integer, default=0)

    messages = db.relationship(
        'Message', backref='conversation', lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Conversation #{self.id} user={self.user_id}>'


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.Integer, db.ForeignKey('conversations.id'), nullable=False
    )
    role = db.Column(db.String(20), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    theme = db.Column(db.String(80))
    urgence = db.Column(db.String(30))
    methode = db.Column(db.String(50))
    langue = db.Column(db.String(5))
    date_envoi = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )

    def __repr__(self):
        return f'<Message {self.role} conv={self.conversation_id}>'