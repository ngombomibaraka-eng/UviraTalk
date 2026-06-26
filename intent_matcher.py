import re
import logging
from difflib import SequenceMatcher
from database import db, PhraseMultilingue

# Configuration du logging pour voir ce qui se passe en console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentMatcher:
    
    # Mots clés pour détecter la langue (Stopwords, Pronoms, Grammaire)
    # Ces listes permettent d'identifier la langue de l'utilisateur même s'il utilise des mots médicaux mal orthographiés.
    LANG_KEYWORDS = {
        # --- FRANÇAIS (FR) ---
        'fr': {
            'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'est', 
            'suis', 'ai', 'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
            'avoir', 'fait', 'mal', 'tête', 'ventre', 'fièvre', "j'ai", 'mon', 'ma', 
            'mes', 'ton', 'ta', 'tes', 'son', 'sa', 'ses', 'ce', 'cet', 'cette',
            'pour', 'sur', 'avec', 'dans', 'vers', 'chez', 'qui', 'que', 'quoi',
            'où', 'quand', 'comment', 'pourquoi', 'bien', 'très', 'peu', 'plus', 'ça'
        },

        # --- KISWAHILI (SW) ---
        'sw': {
            'na', 'kwa', 'ya', 'wa', 'za', 'ni', 'me', 'yako', 'angu', 
            'hii', 'hiyo', 'wewe', 'mimi', 'tatizo', 'uguu', 'kichwa', 'tumbo',
            'una', 'umepata', 'nini', 'lako', 'lake', 'yetu', 'yenu', 'kwao',
            'kama', 'iliko', 'hapa', 'pale', 'mle', 'juu', 'chini', 'ndani',
            'nje', 'katika', 'kutoka', 'kwenda', 'kuja', 'sasa', 'bado', 'tu',
            'pia', 'lakini', 'hata', 'kisha', 'basi', 'au', 'wala', 'ila'
        },

        # --- KIFULIIRU (KIR) ---
        # Langue Bantoue du Sud-Kivu
        'kir': {
            'nze', 'we', 'ye', 'twe', 'bwe', 'bo', 
            'angu', 'ago', 'amwe', 'etu', 'enu', 'abo',
            'ku', 'mu', 'ha', 'kwa', 'na', 'ko', 'ho', 
            'ni', 'koli', 'teta', 'genda', 'koma', 'leta', 'tuma', 'soma',
            'ubu', 'kesho', 'ulo', 'muliro', 'hano', 'hukuru',
            'beka', 'kandi', 'nganyi', 'mbone', 'nkuri', 'lwa'
        },

        # --- KIBEMBE (KIB) ---
        # Langue Bantoue (Bembe/Bushi)
        'kib': {
            'nge', 'o', 'ye', 'beto', 'benu', 'bo', 
            'yami', 'yao', 'yiye', 'yetu', 'yenu', 'yabo',
            'mu', 'ha', 'ku', 'kwa', 'na', 'za', 'di',
            'ni', 'di', 'vula', 'luka', 'buka', 'sadi', 'kamba', 'ziba',
            'lelo', 'kesho', 'mbala', 'kasi', 'kati', 'nsemi',
            'mbwa', 'vandi', 'mbote', 'bilenge', 'mabe', 'kuna'
        }
    }

    @staticmethod
    def normalize(text):
        """Nettoie le texte : minuscule, retire la ponctuation."""
        if not text: return ""
        text = text.lower()
        # Remplace les caractères non alphanumériques par un espace
        text = re.sub(r'[^\w\s]', ' ', text) 
        # Supprime les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @staticmethod
    def detect_language(text):
        """Détecte la langue la plus probable basée sur les mots clés."""
        text = IntentMatcher.normalize(text)
        if not text: return 'fr'
        
        words = set(text.split())
        scores = {}
        
        for lang, keywords in IntentMatcher.LANG_KEYWORDS.items():
            # Intersection entre les mots du message et les mots clés de la langue
            match_count = len(words & keywords)
            scores[lang] = match_count
            
        # Si aucun mot clé n'est trouvé, on retourne le français par défaut
        if not scores or max(scores.values()) == 0:
            return 'fr'
            
        best_lang = max(scores, key=scores.get)
        return best_lang

    @staticmethod
    def get_jaccard_similarity(set1, set2):
        """Calcule la similarité de Jaccard (Intersection / Union)."""
        if not set1 or not set2: return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0

    @staticmethod
    def get_sequence_similarity(str1, str2):
        """Calcule la similarité de séquence (difflib)."""
        if not str1 or not str2: return 0.0
        return SequenceMatcher(None, str1, str2).ratio()

    def get_best_response(self, phrase_match, detected_lang):
        """Récupère la réponse dans la langue détectée, avec fallback."""
        # Mapping des codes langues vers les colonnes de la BDD
        lang_map = {
            'fr': 'reponse_fr', 
            'sw': 'reponse_sw', 
            'kir': 'reponse_kir', 
            'kib': 'reponse_kib'
        }
        
        # 1. Essayer la langue détectée
        response_field = lang_map.get(detected_lang, 'reponse_fr')
        response = getattr(phrase_match, response_field, None)
        
        if response and len(response.strip()) > 5:
            return response
            
        # 2. Fallback sur le Français (souvent la plus complète)
        response = getattr(phrase_match, 'reponse_fr', None)
        if response and len(response.strip()) > 5:
            return response
            
        # 3. Si tout else échoue, on prend la première réponse disponible
        for field in ['reponse_sw', 'reponse_kir', 'reponse_kib']:
            resp = getattr(phrase_match, field, None)
            if resp and len(resp.strip()) > 5:
                return resp
                
        return "Désolé, pas de réponse disponible pour ce symptôme."

    def match_intent(self, user_message):
        """Cœur du moteur : trouve la meilleure phrase correspondante."""
        user_norm = self.normalize(user_message)
        user_words = set(user_norm.split())
        
        # Si le message est vide après normalisation
        if len(user_words) == 0:
            return None, "Je n'ai pas compris votre message."

        user_lang = self.detect_language(user_message)
        
        # Définir l'ordre de priorité des colonnes de la base de données à scanner
        # Si l'utilisateur parle Swahili, on cherche d'abord en Swahili, puis en Français...
        if user_lang == 'sw': 
            priority_fields = ['kiswahili', 'francais_local', 'kifuliiru', 'kibembe']
        else: 
            priority_fields = ['francais_local', 'kiswahili', 'kifuliiru', 'kibembe']

        best_match = None
        best_score = 0.0
        
        try:
            # Récupération de toutes les phrases (Note: optimisable avec pagination si la BDD devient massive)
            phrases = PhraseMultilingue.query.all()
            
            # Si la base est vide
            if not phrases:
                return None, "La base de connaissances est vide."

            for p in phrases:
                for field in priority_fields:
                    # Récupérer le texte de la base de données
                    texte_db = getattr(p, field)
                    
                    # On ignore si le champ est vide
                    if not texte_db: 
                        continue
                    
                    # Normalisation de la base de données
                    db_norm = self.normalize(texte_db)
                    db_words = set(db_norm.split())
                    
                    # Calcul des scores de similarité
                    # Jaccard : Bon pour voir si les mots clés sont là (ex: "fièvre" touche "fièvre")
                    jaccard_score = self.get_jaccard_similarity(user_words, db_words)
                    
                    # Sequence : Bon pour voir l'ordre des mots (ex: "j'ai mal à la tête")
                    seq_score = self.get_sequence_similarity(user_norm, db_norm)
                    
                    # Score combiné (on favorise légèrement la présence des mots)
                    current_score = (jaccard_score * 0.7) + (seq_score * 0.3)
                    
                    # Petit bonus si on matche parfaitement dans la langue principale
                    if field == priority_fields[0] and current_score > 0.5: 
                        current_score += 0.05
                    
                    # Mise à jour du meilleur score
                    if current_score > best_score:
                        best_score = current_score
                        best_match = p

        except Exception as e:
            logger.error(f"Erreur IntentMatcher: {e}")
            return None, "Erreur technique interne lors de l'analyse."

        # --- SEUIL DE DÉTECTION ---
        # 0.30 est un seuil assez tolérant (permet les fautes d'orthographe)
        # On pourrait le remonter à 0.45 ou 0.50 pour être plus strict.
        if best_match and best_score > 0.30:
            final_response = self.get_best_response(best_match, user_lang)
            return best_match.intent, final_response

        # Message par défaut si rien n'est trouvé
        return None, "Je n'ai pas bien compris. Essayez de décrire vos symptômes simplement (ex: mal de tête, fièvre, toux)."

# Instanciation globale pour l'import dans app.py
intent_matcher = IntentMatcher()