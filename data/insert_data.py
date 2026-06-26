import sys
import os

# On ajoute le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database import db, PhraseMultilingue

def insert_data():
    """
    Fonction pour insérer les données d'entraînement nettoyées.
    """
    
    # Liste des données nettoyées basées sur votre contenu
    # Structure : Dictionnaire correspondant à la table PhraseMultilingue
    data_to_insert = [
        
        # --- 1. FIÈVRE (F001 à F050) ---
        {
            "theme": "Santé",
            "categorie": "fièvre",
            "francais_local": "fièvre, je chauffe, j'ai de la fièvre, température, fièvre élevée, j'ai très chaud, corps chaud, je ne sais pas ma température, j'ai la fièvre",
            "kiswahili": "homa, mwili wangu una motomoto, nina joto la mwili",
            "kifuliiru": "", # Laisser vide si pas de traduction
            "kibembe": "",
            "intent": "fievre",
            "reponse_fr": """🤒 **FIÈVRE (MALADIE FIÈVRE 🤒)**

La fièvre est souvent un signe que votre corps lutte contre une infection.
👉 **CE QUE CELA SIGNIFIE :** Le paludisme (Malaria) est une maladie très sérieuse en RDC.

📋 **CONSEILS :**
*   Si vous avez de la fièvre (> 3 jours), vous devez faire un test rapide pour le paludisme.
*   **DANGER SIGNES :** Si vous avez des douleurs dans la poitrine, une difficulté respiratoire ou de la confusion, c'est une urgence.

🔍 **QUOI FAIRE :**
*   Si forte fièvre (>39.5°C), c'est une urgence. Allez rapidement au centre de santé ! 

💡 **CE QU'IL FAUT FAIRE :**
*   **Hygiène :** Buvez beaucoup d'eau propre.
*   **Repos :** Reposez-vous et surveillez votre température.
*   **Consultation :** Prenez rendez-vous rapidement avec un médecin ou un agent de santé.

👍 **CONCLUSION :**
Vous devez absolument effectuer un test de diagnostique (Test de Paludisme / Test de Covid-19)."""
        },

        # --- 2. FIÈVRE URGENCE (Critique) ---
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
*   Restez calme et rassurez la personne.
*   Appelez les secours (ambulance ou centre de santé) immédiatement.
*   Ne faites pas boire ou manger la personne si elle est inconsciente.

**ALLEZ URGENCE THÉRAPIE 🔴 :**
*   Vérifiez la respiration.
*   Si la personne ne respire pas, commencez le massage cardiaque si vous savez le faire."""
        },

        # --- 3. TOUX (T001 à T050) ---
        {
            "theme": "Santé",
            "categorie": "respiratoire",
            "francais_local": "toux, je tousse, toux grasse, toux sèche, crachats, kifungi",
            "kiswahili": "kikohozi, Nina kikohozi, kikohozi makali, inua kikohozi, ma kiko",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "toux",
            "reponse_fr": """🌡 **TOUX (Symptômes respiratoires)**

Une toux persistante peut être un signe de tuberculose, de grippe ou de COVID-19.

⚠️ **SYMPTÔMES ASSOCIÉS :**
*   Avez-vous de la fièvre ?
*   Avez-vous des crachats (avec ou sans sang) ?
*   Avez-vous des douleurs thoraciques ?

🏥 **CONSEILS :**
*   Portez un masque pour protéger les autres.
*   Si vous toussez depuis plus de 2 semaines, allez au centre de santé pour un dépistage de la tuberculose."""
        },

        # --- 4. DIARRHÉE (D001 à D050) ---
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
*   **SRO (Sérum de Réhydratation Orale) :** Buvez beaucoup d'eau propre ou du SRO.
*   **Alimentation :** Continuez à manger si vous avez faim (évitez les aliments gras).

🏥 **URGENCE :**
Si vous voyez du sang dans les selles ou si la personne est très faible et ne boit pas, allez au centre de santé immédiatement (Risque de Choléra)."""
        },

        # --- 5. GROSSESSE (G001 à G050) ---
        {
            "theme": "Maternité",
            "categorie": "grossesse",
            "francais_local": "je suis enceinte, je vais accoucher, sage prévu, ventre, grosesse",
            "kiswahili": "mimba, nina mimba, nitazaa, tumbo",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "grossesse",
            "reponse_fr": """🤰 **GROSSESSE**

Félicitations. Suivez vos consultations prénatales (CPN).

⚠️ **SIGNES D'ALERTE :**
*   Saignements vaginaux.
*   Maux de tête violents ou vision trouble (Pré-éclampsie).
*   Perte de liquide.

**CONSEIL :**
Allez voir une sage-femme ou à un centre de santé ou hopital pour un suivi régulier."""
        },

        # --- 6. URGENCES GÉNÉRALES (U001 à U050) ---
        {
            "theme": "Urgence",
            "categorie": "urgence critique",
            "francais_local": "tremble, saigne beaucoup, je suis malade, rouge coule, je perds connaissance, ça devient grave",
            "kiswahili": "miguu inatetemeka, damu linatoka, niko hatarini",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "urgence_critique",
            "reponse_fr": """🚑 **URGENCE MÉDICALE 🔴**

La situation semble critique.

1.  **APPEL :** Contactez immédiatement les secours ou le centre de santé le plus proche.
2.  **SÉCURITÉ :** Éloignez la personne du danger (feu, route...).
3.  **SURVEILLANCE :** Parlez-lui, vérifiez si elle respire.
4.  **NE BOUGEZ PAS :** Si vous soupçonnez une blessure au dos ou au cou.

Ne restez pas seul, appelez de l'aide !"""
        },

        # --- 7. RESPIRATION DIFFICILE (Supplément) ---
        {
            "theme": "Urgence",
            "categorie": "respiratoire",
            "francais_local": "je respire difficilement, j'ai une maladie respiratoire, je n'ai plus de souffle",
            "kiswahili": "nina shida ya kupumua, hewa inapungua",
            "kifuliiru": "",
            "kibembe": "",
            "intent": "respiration",
            "reponse_fr": """🫁 **DIFFICULTÉ RESPIRATOIRE**

C'est un signe très sérieux.

*   Avez-vous des douleurs dans la poitrine ?
*   Est-ce de l'asthme, une allergie ou une infection ?

**ACTION :**
Asseyez la personne. Si elle a de l'asthme et de la médication, aidez-la à la prendre. Sinon, appelez l'urgence tout de suite."""
        }
    ]

    with app.app_context():
        # Compte avant
        count_before = PhraseMultilingue.query.count()
        
        count = 0
        for item in data_to_insert:
            # Création de l'objet PhraseMultilingue
            phrase = PhraseMultilingue(
                theme=item.get('theme'),
                categorie=item.get('categorie'),
                francais_local=item.get('francais_local'),
                kiswahili=item.get('kiswahili'),
                kifuliiru=item.get('kifuliiru'),
                kibembe=item.get('kibembe'),
                intent=item.get('intent'),
                reponse_fr=item.get('reponse_fr'),
                reponse_sw="", # On peut laisser vide pour l'instant
                reponse_kir="",
                reponse_kib=""
            )
            
            db.session.add(phrase)
            count += 1
            
        try:
            db.session.commit()
            count_after = PhraseMultilingue.query.count()
            print(f"✅ Succès : {count} entrées ont été ajoutées.")
            print(f"📊 Total d'entrées dans la base : {count_after}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de l'insertion : {e}")

if __name__ == "__main__":
    insert_data()