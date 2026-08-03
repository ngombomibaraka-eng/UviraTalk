import os
import re
import logging
import torch
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai
from database import PhraseMultilingue

# Configuration des journaux d'exécution
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration de la clé d'API pour le LLM Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class SmartAIMatcher:
    """
    Système hybride d'IA :
    1. Deep Learning (Vectors / Embeddings) : Recherche la correspondance sémantique dans la BDD.
    2. GenAI (LLM Gemini) : Génère une réponse personnalisée si aucune correspondance exacte n'est trouvée.
    """
    def __init__(self):
        # Chargement d'un modèle Deep Learning NLP multilingue ultra-rapide
        logger.info("Chargement du modèle Deep Learning NLP (SentenceTransformer)...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.db_embeddings = None
        self.cached_phrases = []

    def normalize(self, text: str) -> str:
        """Nettoie le texte utilisateur avant analyse."""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.strip()

    def build_embeddings_cache(self):
        """Vectorise l'intégralité de la BDD de connaissances pour la recherche rapide en mémoire."""
        try:
            phrases = PhraseMultilingue.query.all()
            if not phrases:
                logger.warning("Base de données de connaissances vide.")
                return

            self.cached_phrases = phrases
            texts_to_embed = []

            # Concaténation des phrases déclencheuses multilingues
            for p in phrases:
                combined_text = f"{p.francais_local or ''} {p.kiswahili or ''} {p.kifuliiru or ''} {p.kibembe or ''}"
                texts_to_embed.append(self.normalize(combined_text))

            # Transformation du texte en vecteurs numériques (Embeddings)
            self.db_embeddings = self.model.encode(texts_to_embed, convert_to_tensor=True)
            logger.info("Vecteurs d'embeddings générés et mis en cache avec succès.")
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul des embeddings : {e}")

    def get_generative_ai_response(self, user_message: str) -> str:
        """Fait appel au modèle Génératif (GenAI/Gemini) pour traiter des demandes complexes."""
        if not GEMINI_API_KEY:
            return "Je n'ai pas pu comprendre précisément votre demande. Veuillez consulter le centre de santé le plus proche."

        try:
            # Consigne système (Prompt) adaptée au contexte médical d'Uvira
            system_instruction = (
                "Tu es un assistant médical virtuel bienveillant nommé 'Docteur IA Uvira'. "
                "Tu réponds aux questions de santé des habitants de la région d'Uvira (RDC). "
                "Tu comprends le Français, le Kiswahili, le Kifuliiru et le Kibembe. "
                "Sois clair, concis, adapte-toi à la langue de l'utilisateur, et rappelle-lui "
                "toujours de consulter un médecin en cas de symptôme persistant."
            )
            
            # Appel de la GenAI avec le modèle Gemini
            model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
            response = model.generate_content(user_message)
            return response.text
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement GenAI : {e}")
            return "Une erreur technique s'est produite lors du traitement par l'IA."

    def match_intent(self, user_message: str):
        """Analyse le message de l'utilisateur et retourne la meilleure réponse."""
        user_norm = self.normalize(user_message)
        if not user_norm:
            return None, "Veuillez poser une question ou décrire vos symptômes."

        # Reconstruire le cache si au démarrage il était vide
        if self.db_embeddings is None or len(self.cached_phrases) == 0:
            self.build_embeddings_cache()

        # Si toujours aucune donnée locale, basculer immédiatement vers la GenAI
        if self.db_embeddings is None:
            gen_resp = self.get_generative_ai_response(user_message)
            return "genai_fallback", gen_resp

        # 1. Encodage du message de l'utilisateur
        user_embedding = self.model.encode(user_norm, convert_to_tensor=True)

        # 2. Calcul du score de similarité cosinus (Cosine Similarity)
        cosine_scores = util.cos_sim(user_embedding, self.db_embeddings)[0]

        # 3. Récupération de la meilleure correspondance
        best_score_idx = int(torch.argmax(cosine_scores))
        best_score = float(cosine_scores[best_score_idx])

        logger.info(f"Score de correspondance sémantique : {best_score:.4f}")

        # --- SEUIL SÉMANTIQUE ---
        # Si le score de compréhension est suffisant (> 0.40)
        if best_score > 0.40:
            matched_item = self.cached_phrases[best_score_idx]
            response = matched_item.reponse_fr or matched_item.reponse_sw or matched_item.reponse_kir
            return matched_item.intent, response

        # Sinon, l'IA générative prend le relais dynamiquement
        logger.info("Pas de correspondance directe dans la BDD local -> Bascule vers GenAI.")
        gen_response = self.get_generative_ai_response(user_message)
        return "genai_response", gen_response

# Instance globale
intent_matcher = SmartAIMatcher()