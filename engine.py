# engine.py
"""
Moteur IA hybride UviraTalk (version numpy-only).
Aucune dependance a sklearn ou scipy (bloques par Windows Device Guard).

4 niveaux de comprehension :
  0. Small talk (salutations, comment ca va...)
  1. Reponses courtes (oui/non/duree)
  2. Recherche exacte par mots-cles
  3. Recherche semantique TF-IDF maison (numpy)
  4. Fallback Gemini (IA generative)
"""

import os
import re
import math
import logging
from collections import Counter
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

from database import DialogueTriage, QAEducation
from smalltalk import detect_smalltalk_intent, get_smalltalk_response
from dialogue_state import classify_response, get_followup_response

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# =============================================
# UTILITAIRES
# =============================================
def strip_accents(s: str) -> str:
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


# =============================================
# TF-IDF MAISON (remplace sklearn)
# =============================================
class SimpleTfidf:
    """TF-IDF implemente avec numpy pur. Pas de sklearn."""

    def __init__(self, ngram_range=(1, 2), max_features=10000):
        self.ngram_range = ngram_range
        self.max_features = max_features
        self.vocab = {}
        self.idf = None
        self.n_docs = 0

    def _tokenize(self, text: str):
        text = strip_accents(text.lower())
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        tokens = list(words)
        # Ajouter les n-grams
        for n in range(2, self.ngram_range[1] + 1):
            for i in range(len(words) - n + 1):
                tokens.append(' '.join(words[i:i+n]))
        return tokens

    def fit(self, texts):
        self.n_docs = len(texts)
        df_counter = Counter()
        tokenized_docs = []

        for t in texts:
            tokens = self._tokenize(t)
            tokenized_docs.append(tokens)
            for tok in set(tokens):
                df_counter[tok] += 1

        # Filtrer : garder les tokens qui apparaissent au moins 1 fois
        # et limiter à max_features par fréquence
        most_common = df_counter.most_common(self.max_features)
        self.vocab = {tok: i for i, (tok, _) in enumerate(most_common)}
        
        # IDF
        self.idf = np.zeros(len(self.vocab))
        for tok, df in df_counter.items():
            if tok in self.vocab:
                self.idf[self.vocab[tok]] = math.log((self.n_docs + 1) / (df + 1)) + 1

        # Matrice TF-IDF
        matrix = np.zeros((self.n_docs, len(self.vocab)))
        for i, tokens in enumerate(tokenized_docs):
            tf = Counter(tokens)
            for tok, count in tf.items():
                if tok in self.vocab:
                    matrix[i, self.vocab[tok]] = count * self.idf[self.vocab[tok]]

        # Normaliser (L2)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return matrix / norms

    def transform(self, text: str):
        tokens = self._tokenize(text)
        tf = Counter(tokens)
        vec = np.zeros(len(self.vocab))
        for tok, count in tf.items():
            if tok in self.vocab:
                vec[self.vocab[tok]] = count * self.idf[self.vocab[tok]]
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def cosine_sim(self, vec, matrix):
        """Similarite cosinus entre un vecteur et une matrice."""
        return matrix @ vec


# =============================================
# MOTEUR PRINCIPAL
# =============================================
class SmartAIMatcher:
    """Moteur hybride de comprehension (numpy-only)."""

    def __init__(self):
        logger.info("Initialisation du moteur IA (numpy-only)...")

        self.dialogues_cache = []
        self.qa_cache = []

        self.dialogue_vectorizer = None
        self.dialogue_matrix = None
        self.qa_vectorizer = None
        self.qa_matrix = None

        self.last_langue = None
        self.last_theme = None
        self.last_urgence = None

        logger.info("Moteur initialise.")

    # =============================================
    # VALIDATION
    # =============================================
    def is_valid_dialogue(self, dialogue) -> bool:
        q = dialogue.question_suivante or ""
        p = dialogue.phrase_patient or ""

        if re.search(r'\b[A-Z]\d{2,3}\b', q):
            return False
        if len(q) > 200:
            return False
        if p and len(p) > 150:
            return False
        if p and p.count('.') > 1:
            return False
        if not q.strip():
            return False
        return True

    # =============================================
    # NORMALISATION
    # =============================================
    def normalize(self, text: str) -> str:
        if not text:
            return ""
        text = strip_accents(text.lower().strip())
        text = re.sub(r'[^\w\s]', ' ', text)
        return re.sub(r'\s+', ' ', text).strip()

    def detect_language(self, text: str) -> str:
        markers = {
            'sw': ['nina', 'naumwa', 'homa', 'kuhara', 'kikohozi', 'kichwa',
                   'mtoto', 'maji', 'dawa', 'hospitali', 'maumivu', 'najisikia',
                   'nataka', 'sijui', 'kwanini', 'nifanye', 'nini', 'mgonjwa'],
            'fr': ["j'ai", 'je suis', 'mal', 'fievre', 'toux', 'enfant',
                   'medecin', 'hopital', 'douleur', 'sante', 'bonjour',
                   'comment', 'pourquoi', 'que faire', 'patient'],
        }
        text_lower = strip_accents(text.lower())
        scores = {l: sum(1 for m in markers[l] if m in text_lower) for l in markers}
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'fr'

    # =============================================
    # CONSTRUCTION DES CACHES
    # =============================================
    def build_caches(self):
        logger.info("Construction des caches...")

        # Dialogues
        self.dialogues_cache = DialogueTriage.query.all()
        if self.dialogues_cache:
            texts = [
                self.normalize(f"{d.phrase_patient} {d.mots_cles or ''}")
                for d in self.dialogues_cache
            ]
            self.dialogue_vectorizer = SimpleTfidf(ngram_range=(1, 2), max_features=10000)
            self.dialogue_matrix = self.dialogue_vectorizer.fit(texts)
            logger.info(f"   {len(self.dialogues_cache)} dialogues indexes")

        # Q&R
        self.qa_cache = QAEducation.query.all()
        if self.qa_cache:
            texts = [self.normalize(q.question) for q in self.qa_cache]
            self.qa_vectorizer = SimpleTfidf(ngram_range=(1, 2), max_features=10000)
            self.qa_matrix = self.qa_vectorizer.fit(texts)
            logger.info(f"   {len(self.qa_cache)} Q&R indexees")

    # =============================================
    # NIVEAU : RECHERCHE EXACTE
    # =============================================
    def search_exact_match(self, user_message: str, langue: str):
        user_norm = self.normalize(user_message)
        user_words = set(user_norm.split())
        best_match, best_score = None, 0

        for dialogue in self.dialogues_cache:
            if dialogue.langue != langue:
                continue
            if not self.is_valid_dialogue(dialogue):
                continue

            keywords = []
            if dialogue.mots_cles:
                keywords = [self.normalize(k) for k in dialogue.mots_cles.split('|')]
            patient_words = set(self.normalize(dialogue.phrase_patient or '').split())

            score = sum(2 for kw in keywords if kw and kw in user_norm)
            score += len(user_words & patient_words)

            if score > best_score:
                best_score, best_match = score, dialogue

        if best_score >= 3:
            return best_match, best_score
        return None, 0

    # =============================================
    # NIVEAU : RECHERCHE SEMANTIQUE
    # =============================================
    def search_semantic(self, user_message: str, langue: str, threshold: float = 0.30):
        user_norm = self.normalize(user_message)

        best_dialogue, best_score_d = None, 0
        if self.dialogue_vectorizer is not None:
            user_vec = self.dialogue_vectorizer.transform(user_norm)
            sims = self.dialogue_vectorizer.cosine_sim(user_vec, self.dialogue_matrix)
            for i, d in enumerate(self.dialogues_cache):
                if d.langue != langue:
                    continue
                if not self.is_valid_dialogue(d):
                    continue
                if sims[i] > best_score_d:
                    best_score_d = float(sims[i])
                    best_dialogue = d

        best_qa, best_score_q = None, 0
        if self.qa_vectorizer is not None:
            user_vec = self.qa_vectorizer.transform(user_norm)
            sims = self.qa_vectorizer.cosine_sim(user_vec, self.qa_matrix)
            for i, q in enumerate(self.qa_cache):
                if q.langue != langue:
                    continue
                if sims[i] > best_score_q:
                    best_score_q = float(sims[i])
                    best_qa = q

        if best_score_d >= threshold and best_score_d >= best_score_q:
            return ('dialogue', best_dialogue, best_score_d)
        elif best_score_q >= threshold:
            return ('qa', best_qa, best_score_q)
        return (None, None, 0)

    # =============================================
    # FALLBACK GEMINI
    # =============================================
    def call_gemini(self, user_message: str):
        if not GEMINI_API_KEY:
            return None
        try:
            system_prompt = (
                "Tu es 'Docteur IA Uvira', un assistant medical virtuel pour les "
                "habitants d'Uvira en RDC. Tu comprends le francais, le kiswahili, "
                "le kifuliiru et le kibembe. Reponds de maniere claire, concise, "
                "et adapte-toi a la langue de l'utilisateur. Rappelle toujours de "
                "consulter un centre de sante en cas de symptome persistant."
            )
            model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=system_prompt
            )
            response = model.generate_content(user_message)
            return response.text
        except Exception as e:
            logger.error(f"Erreur Gemini : {e}")
            return None

    # =============================================
    # FORMATAGE
    # =============================================
    def format_response(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

    # =============================================
    # METHODE PRINCIPALE
    # =============================================
    def match_intent(self, user_message: str) -> dict:
        # === 0. Small talk ===
        smalltalk_intent, smalltalk_langue = detect_smalltalk_intent(user_message)
        if smalltalk_intent:
            logger.info(f"Small talk : {smalltalk_intent} ({smalltalk_langue})")
            return {
                'type': 'smalltalk',
                'reponse': get_smalltalk_response(smalltalk_intent, smalltalk_langue),
                'methode': 'smalltalk'
            }

        # === 0.5. Reponses courtes ===
        response_info = classify_response(user_message)
        if response_info['type'] in ['oui', 'non', 'duree', 'nombre']:
            langue_temp = self.detect_language(user_message)
            if len(user_message.strip()) <= 10:
                langue_temp = self.last_langue or 'fr'

            logger.info(f"Reponse courte : {response_info['type']} ({langue_temp})")

            # Si on a un contexte, on conseille
            if self.last_theme and response_info['type'] in ['oui', 'non']:
                from advice_engine import get_advice
                advice = get_advice(self.last_theme, self.last_urgence, langue_temp)
                if advice:
                    return {
                        'type': 'advice',
                        'reponse': advice,
                        'theme': self.last_theme,
                        'urgence': self.last_urgence,
                        'methode': f'advice_after_{response_info["type"]}'
                    }

            followup = get_followup_response(response_info['type'], langue_temp)
            if followup:
                return {
                    'type': 'short_response',
                    'reponse': followup,
                    'methode': f"short_response_{response_info['type']}"
                }

        # === 1. Langue ===
        langue = self.detect_language(user_message)
        self.last_langue = langue
        logger.info(f"Langue : {langue}")

        # === 2. Recherche exacte ===
        match, score = self.search_exact_match(user_message, langue)
        if match:
            self.last_theme = match.theme
            self.last_urgence = match.urgence
            return {
                'type': 'dialogue',
                'code': match.code,
                'theme': match.theme,
                'reponse': self.format_response(match.question_suivante),
                'urgence': match.urgence,
                'symptomes': match.symptomes_detectes,
                'methode': 'exact_match'
            }

        # === 3. Recherche semantique ===
        match_type, match_obj, score = self.search_semantic(user_message, langue)
        if match_type == 'dialogue':
            self.last_theme = match_obj.theme
            self.last_urgence = match_obj.urgence
            return {
                'type': 'dialogue',
                'code': match_obj.code,
                'theme': match_obj.theme,
                'reponse': self.format_response(match_obj.question_suivante),
                'urgence': match_obj.urgence,
                'symptomes': match_obj.symptomes_detectes,
                'methode': 'semantic'
            }
        elif match_type == 'qa':
            return {
                'type': 'qa',
                'code': match_obj.code,
                'theme': match_obj.theme,
                'reponse': self.format_response(match_obj.reponse),
                'methode': 'semantic'
            }

        # === 4. Gemini fallback ===
        gemini_response = self.call_gemini(user_message)
        if gemini_response:
            return {
                'type': 'gemini',
                'reponse': gemini_response,
                'methode': 'gemini_fallback'
            }

        # === 5. Defaut ===
        return {
            'type': 'default',
            'reponse': (
                "Je n'ai pas bien compris votre message. Pouvez-vous reformuler ? "
                "Vous pouvez me decrire vos symptomes ou poser une question de sante."
            ),
            'methode': 'default'
        }