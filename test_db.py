import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database import PhraseMultilingue

def insert_test_data():
    with app.app_context():
        # On vérifie si c'est vraiment vide
        count = PhraseMultilingue.query.count()
        print(f"📊 Nombre de phrases actuelles dans la base : {count}")

        if count == 0:
            print("⚠️ Base vide. Insertion de données de test...")
            
            # On insère un test basique pour la fièvre
            p1 = PhraseMultilingue(
                theme="Test",
                categorie="test",
                francais_local="fièvre, mal de tête, chaud, j'ai mal",
                kiswahili="homa, maumivu ya kichwa",
                kifuliiru="",
                kibembe="",
                intent="test_fievre",
                reponse_fr="🩺 **Diagnostic de Test :** Je comprends que vous avez de la fièvre ou mal à la tête. C'est un symptôme courant. Veuillez boire beaucoup d'eau et aller au centre de santé si cela persiste."
            )

            # On insère un test basique pour l'accueil
            p2 = PhraseMultilingue(
                theme="Test",
                categorie="test",
                francais_local="bonjour, salut, hello",
                kiswahili="jambo, habari",
                kifuliiru="",
                kibembe="",
                intent="greeting_test",
                reponse_fr="Bonjour ! Je suis le Docteur IA. Comment puis-je vous aider aujourd'hui ?"
            )

            db.session.add(p1)
            db.session.add(p2)
            db.session.commit()
            print("✅ Données de test insérées avec succès !")
        else:
            print("ℹ️ La base contient déjà des données.")

if __name__ == "__main__":
    insert_test_data()