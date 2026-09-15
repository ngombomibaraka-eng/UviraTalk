# dialogue_state.py
"""
Gestion de l'état conversationnel pour UviraTalk.
Permet au système de se souvenir du contexte et de comprendre
les réponses courtes (oui, non, "depuis 2 jours", etc.)
"""

import re


# =============================================
# Mots de confirmation (FR + SW)
# =============================================
OUI_MOTS = [
    "oui", "ouais", "yes", "yep", "ok", "d'accord", "daccord",
    "exact", "exactement", "c'est ca", "c est ca", "affirmatif",
    "ndiyo", "ndio", "sawa", "nakubali", "sahihi",
]

NON_MOTS = [
    "non", "nan", "nope", "pas du tout", "aucunement", "jamais",
    "hapana", "siyo", "sivyo", "la hasha",
]

# =============================================
# Motifs de réponse temporelle
# =============================================
PATTERNS_DUREE = [
    # Français
    (r'depuis\s+(\d+)\s+(jour|jours)', 'jours'),
    (r'depuis\s+(\d+)\s+(semaine|semaines)', 'semaines'),
    (r'depuis\s+(\d+)\s+(mois)', 'mois'),
    (r'depuis\s+(\d+)\s+(heure|heures)', 'heures'),
    (r'(\d+)\s+(jour|jours)', 'jours'),
    (r'(\d+)\s+(semaine|semaines)', 'semaines'),
    (r'(\d+)\s+(mois)', 'mois'),
    (r'(\d+)\s+(heure|heures)', 'heures'),
    (r'ce matin', 'ce matin'),
    (r'hier', 'hier'),
    (r'avant-hier', 'avant-hier'),
    (r'longtemps', 'longtemps'),
    (r'quelques jours', 'quelques jours'),
    (r'quelques heures', 'quelques heures'),
    # Swahili
    (r'siku\s+(\d+)', 'siku'),
    (r'wiki\s+(\d+)', 'wiki'),
    (r'miezi\s+(\d+)', 'miezi'),
    (r'saa\s+(\d+)', 'saa'),
    (r'jana', 'jana'),
    (r'juzi', 'juzi'),
    (r'asubuhi', 'asubuhi'),
]


def is_oui(message: str) -> bool:
    """Détecte si le message est une affirmation."""
    msg = message.lower().strip()
    # Nettoyer la ponctuation
    msg = re.sub(r'[!?.,;:]', '', msg).strip()
    # Vérifier les mots-clés
    for mot in OUI_MOTS:
        if msg == mot or msg.startswith(mot + ' ') or f' {mot} ' in f' {msg} ':
            return True
    # Cas court : "ok", "ouais"
    if len(msg) <= 5 and msg in OUI_MOTS:
        return True
    return False


def is_non(message: str) -> bool:
    """Détecte si le message est une négation."""
    msg = message.lower().strip()
    msg = re.sub(r'[!?.,;:]', '', msg).strip()
    for mot in NON_MOTS:
        if msg == mot or msg.startswith(mot + ' ') or f' {mot} ' in f' {msg} ':
            return True
    return False


def extract_duration(message: str):
    """
    Extrait une durée du message.
    Retourne (valeur, unite) ou None.
    """
    msg = message.lower().strip()
    for pattern, unite in PATTERNS_DUREE:
        match = re.search(pattern, msg)
        if match:
            try:
                valeur = int(match.group(1))
                return (valeur, unite)
            except (IndexError, ValueError):
                return (None, unite)
    return None


def is_numeric_answer(message: str):
    """Détecte si le message contient un âge ou un nombre."""
    msg = message.lower().strip()
    # Patterns : "3 ans", "2 mois", "il a 5 ans", "ana miaka 3"
    patterns = [
        r'(\d+)\s*(ans?|annees?)',
        r'(\d+)\s*(mois)',
        r'(\d+)\s*(jours?)',
        r'(\d+)\s*(miaka)',
        r'il a\s+(\d+)',
        r'elle a\s+(\d+)',
        r'ana\s+(\d+)',
        r'^(\d+)$',  # juste un nombre
    ]
    for p in patterns:
        match = re.search(p, msg)
        if match:
            try:
                return int(match.group(1))
            except (IndexError, ValueError):
                continue
    return None


def classify_response(message: str) -> dict:
    """
    Classe la réponse de l'utilisateur dans une catégorie.
    Retourne un dict avec :
      - type : 'oui' | 'non' | 'duree' | 'nombre' | 'inconnu'
      - valeur : la valeur extraite (si applicable)
    """
    if is_oui(message):
        return {'type': 'oui', 'valeur': None}
    if is_non(message):
        return {'type': 'non', 'valeur': None}

    duree = extract_duration(message)
    if duree:
        return {'type': 'duree', 'valeur': duree}

    nombre = is_numeric_answer(message)
    if nombre is not None:
        return {'type': 'nombre', 'valeur': nombre}

    return {'type': 'inconnu', 'valeur': None}


# =============================================
# Réponses de suivi quand l'utilisateur donne une réponse courte
# =============================================

FOLLOWUP_RESPONSES = {
    'oui': {
        'fr': "D'accord. Pouvez-vous me donner plus de détails ?",
        'sw': "Sawa. Unaweza kuniambia zaidi ?",
    },
    'non': {
        'fr': "D'accord. Avez-vous d'autres symptômes ?",
        'sw': "Sawa. Una dalili nyingine ?",
    },
    'duree': {
        'fr': "Merci. Avez-vous d'autres symptômes à signaler ?",
        'sw': "Asante. Una dalili nyingine unayotaka kutaja ?",
    },
    'nombre': {
        'fr': "Merci pour l'information. Avez-vous d'autres symptômes ?",
        'sw': "Asante kwa taarifa. Una dalili nyingine ?",
    },
}


def get_followup_response(response_type: str, langue: str) -> str:
    """Retourne la réponse de suivi selon le type de réponse utilisateur."""
    if response_type in FOLLOWUP_RESPONSES:
        return FOLLOWUP_RESPONSES[response_type].get(langue, FOLLOWUP_RESPONSES[response_type]['fr'])
    return None