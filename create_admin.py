# create_admin.py
"""Cree le compte administrateur par defaut. A lancer UNE SEULE FOIS."""

from flask import Flask
from database import db, Utilisateur
from auth import hash_password

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uviratalk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Vérifier si un admin existe déjà
    admin = Utilisateur.query.filter_by(email='admin@uviratalk.org').first()
    if admin:
        print("⚠️  Un admin existe deja :", admin.email)
    else:
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
        print("✅ Admin cree avec succes !")
        print("   Email    : admin@uviratalk.org")
        print("   Password : admin2026")
        print("\n⚠️  CHANGEZ CE MOT DE PASSE EN PRODUCTION.")