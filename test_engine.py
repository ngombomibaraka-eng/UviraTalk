# test_engine.py
from flask import Flask
from database import db, DialogueTriage, QAEducation
from engine import SmartAIMatcher

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uviratalk.db'
db.init_app(app)

with app.app_context():
    print("\n=== TEST DU MOTEUR IA ===\n")
    matcher = SmartAIMatcher()
    matcher.build_caches()

    tests = [
        ("fr", "J'ai la diarrhée"),
        ("fr", "J'ai de la fièvre"),
        ("fr", "Mon enfant tousse"),
        ("fr", "Je suis enceinte"),
        ("fr", "Qu'est-ce que le paludisme ?"),
        ("fr", "Je saigne beaucoup"),
        ("sw", "Nina kuharisha"),
        ("sw", "Nina homa"),
        ("sw", "Mtoto wangu ana kikohozi"),
    ]

    for langue, question in tests:
        print(f"\n{'=' * 60}")
        print(f"[{langue.upper()}] Q : {question}")
        result = matcher.match_intent(question)
        print(f"   Méthode : {result.get('methode')}")
        print(f"   Thème   : {result.get('theme', 'N/A')}")
        print(f"   Urgence : {result.get('urgence', 'N/A')}")
        rep = result.get('reponse', '')
        print(f"   Réponse : {rep[:150]}")