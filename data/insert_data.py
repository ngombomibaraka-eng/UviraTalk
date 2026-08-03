import sys
import os

# Ajout du dossier racine au PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database import PhraseMultilingue

def insert_data():
    """Insère les données d'apprentissage médicales dans la base SQLite."""
    data_to_insert = [
        # --- 1. FIÈVRE ---
        {
            "theme": "Santé",
            "categorie": "fièvre",
            "francais_local": "fièvre, je chauffe, j'ai de la fièvre, température, fièvre élevée, j'ai très chaud, corps chaud, je ne sais pas ma température, j'ai la fièvre",
            "kiswahili": "homa, mwili wangu una motomoto, nina joto la mwili",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "fievre",
            "reponse_fr": """🤒 **FIÈVRE (MALADIE FIÈVRE 🤒)**

La fièvre est souvent un signe que votre corps lutte contre une infection.
👉 **CE QUE CELA SIGNIFIE :** Le paludisme (Malaria) est une maladie très sérieuse en RDC.

📋 **CONSEILS :**
* Si vous avez de la fièvre (> 3 jours), vous devez faire un test rapide pour le paludisme.
* **DANGER SIGNES :** Si vous avez des douleurs dans la poitrine, une difficulté respiratoire ou de la confusion, c'est une urgence.

🔍 **QUOI FAIRE :**
* Si forte fièvre (>39.5°C), c'est une urgence. Allez rapidement au centre de santé !

💡 **CE QU'IL FAUT FAIRE :**
* **Hygiène :** Buvez beaucoup d'eau propre.
* **Repos :** Reposez-vous et surveillez votre température.
* **Consultation :** Prenez rendez-vous rapidement avec un médecin ou un agent de santé."""
        },
        # --- 2. FIÈVRE URGENCE ---
        {
            "theme": "Urgence",
            "categorie": "urgence critique",
            "francais_local": "J'ai très mal à la tête, je perds connaissance, je tourne la tête, douleur à la tête, confusion",
            "kiswahili": "Nina maumivu makali ya kichwa, nina poteza fahamu",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "urgence_cerveau",
            "reponse_fr": """🚨 **C'est une urgence.**

**ALERTES CRITIQUES 🔴 :**
Ces signes nécessitent une action rapide : Perte de connaissance, Confusion, Forts maux de tête.

**CONSEIL :** 
* Restez calme et rassurez la personne.
* Appelez les secours (ambulance ou centre de santé) immédiatement.
* Ne faites pas boire ou manger la personne si elle est inconsciente."""
        },
        # --- 3. TOUX ---
        {
            "theme": "Santé",
            "categorie": "respiratoire",
            "francais_local": "toux, je tousse, toux grasse, toux sèche, crachats, kifungi",
            "kiswahili": "kikohozi, Nina kikohozi, kikohozi makali, inua kikohozi, ma kiko",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "toux",
            "reponse_fr": """🌡 **TOUX (Symptômes respiratoires)**

Une toux persistante peut être un signe de tuberculose, de grippe ou d'infection respiratoire.

⚠️ **SYMPTÔMES ASSOCIÉS :**
* Avez-vous de la fièvre ?
* Avez-vous des crachats (avec ou sans sang) ?

🏥 **CONSEILS :**
* Portez un masque pour protéger les autres.
* Si vous toussez depuis plus de 2 semaines, allez au centre de santé pour un dépistage."""
        },
        # --- 4. DIARRHÉE ---
        {
            "theme": "Santé",
            "categorie": "digestif",
            "francais_local": "diarrhée, je vais souvent aux toilettes, ventre liquide, déshydratation, inza kutapole",
            "kiswahili": "kuhara, tumbo langua, chozi, kukorwa",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "diarrhee",
            "reponse_fr": """🚽 **DIARRHÉE**

La diarrhée peut causer une déshydratation rapide, surtout chez les enfants.

⚠️ **ACTION IMMÉDIATE :**
* **SRO (Sérum de Réhydratation Orale) :** Buvez beaucoup d'eau propre ou du SRO.
* **Alimentation :** Continuez à manger si vous avez faim.

🏥 **URGENCE :**
Si vous voyez du sang dans les selles ou si la personne est très faible, rendez-vous immédiatement au centre de santé."""
        },
        # --- 5. GROSSESSE ---
        {
            "theme": "Maternité",
            "categorie": "grossesse",
            "francais_local": "je suis enceinte, je vais accoucher, sage prévu, ventre, grosesse",
            "kiswahili": "mimba, nina mimba, nitazaa, tumbo",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "grossesse",
            "reponse_fr": """🤰 **GROSSESSE**

Suivez vos consultations prénatales (CPN).

⚠️ **SIGNES D'ALERTE :**
* Saignements vaginaux.
* Maux de tête violents ou vision trouble.
* Perte de liquide.

**CONSEIL :**
Consultez une sage-femme ou un centre de santé pour un suivi régulier."""
        },
        # --- 6. URGENCES GÉNÉRALES ---
        {
            "theme": "Urgence",
            "categorie": "urgence critique",
            "francais_local": "tremble, saigne beaucoup, je suis malade, rouge coule, je perds connaissance, ça devient grave",
            "kiswahili": "miguu inatetemeka, damu linatoka, niko hatarini",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "urgence_critique",
            "reponse_fr": """🚑 **URGENCE MÉDICALE 🔴**

1. **APPEL :** Contactez immédiatement le centre de santé le plus proche.
2. **SÉCURITÉ :** Éloignez la personne du danger.
3. **SURVEILLANCE :** Vérifiez la respiration de la personne.

Ne restez pas seul, demandez de l'aide immédiatement !"""
        }
    ]

    with app.app_context():
        count_before = PhraseMultilingue.query.count()
        count = 0
        for item in data_to_insert:
            phrase = PhraseMultilingue(
                theme=item.get('theme'),
                categorie=item.get('categorie'),
                francais_local=item.get('francais_local'),
                kiswahili=item.get('kiswahili'),
                kifuliiru=item.get('kifuliiru'),
                kibembe=item.get('kibembe'),
                intent=item.get('intent'),
                reponse_fr=item.get('reponse_fr'),
                reponse_sw="",
                reponse_kir="",
                reponse_kib=""
            )
            db.session.add(phrase)
            count += 1
            
        try:
            db.session.commit()
            count_after = PhraseMultilingue.query.count()
            print(f"✅ Succès : {count} entrées ajoutées.")
            print(f"📊 Total d'entrées dans la BDD : {count_after}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de l'insertion : {e}")

if __name__ == "__main__":
    insert_data()