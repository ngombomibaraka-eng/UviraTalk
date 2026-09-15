# smalltalk.py
"""
Gestion des salutations et du small talk.
Détecte les salutations (FR + SW) et les intentions conversationnelles.
Adapte la réponse selon l'heure actuelle.
"""

import re
from datetime import datetime


# =============================================
# DETECTION DES SALUTATIONS
# =============================================
SALUTATIONS_FR = [
    "bonjour", "bonsoir", "salut", "slt", "coucou", "hello", "bjr",
    "hey", "bonne journee", "bonne soiree", "bonne nuit",
]

SALUTATIONS_SW = [
    "habari", "jambo", "hujambo", "sijambo", "mambo", "vipi",
    "shikamoo", "marahaba", "salama", "habari yako", "habari za",
]

SALUTATIONS = SALUTATIONS_FR + SALUTATIONS_SW


# =============================================
# DETECTION DES QUESTIONS DE SMALL TALK
# =============================================
SMALLTALK_PATTERNS = {
    "how_are_you": [
        # Français
        r"comment (vas[- ]tu|allez[- ]vous|ca va|va[- ]tu)",
        r"ca va",
        r"comment te sens[- ]tu",
        r"tu vas bien",
        r"vous allez bien",
        # Swahili
        r"habari yako",
        r"habari gani",
        r"u hali gani",
        r"uko (a)?je",
        r"vipi",
    ],
    "who_are_you": [
        r"qui (es[- ]tu|etes[- ]vous)",
        r"c'est quoi ton nom",
        r"quel est ton nom",
        r"tu es qui",
        r"wewe ni nani",
        r"jina lako ni nani",
    ],
    "what_can_you_do": [
        r"que (peux[- ]tu|pouvez[- ]vous) faire",
        r"qu'est[- ]ce que tu (peux|sais) faire",
        r"aide[- ]moi",
        r"j'ai besoin d'aide",
        r"nisaidie",
        r"unaweza kufanya nini",
        r"unaweza kunisaidia",
    ],
    "thank_you": [
        r"merci",
        r"merci beaucoup",
        r"asante",
        r"asante sana",
    ],
    "goodbye": [
        r"au revoir",
        r"a bientot",
        r"bye",
        r"kwaheri",
        r"tutaonana",
    ],
}


# =============================================
# REPONSES DYNAMIQUES SELON L'HEURE
# =============================================
def get_greeting_period():
    """Retourne 'matin', 'apres_midi', 'soir', 'nuit' selon l'heure."""
    heure = datetime.now().hour
    if 5 <= heure < 12:
        return "matin"
    elif 12 <= heure < 18:
        return "apres_midi"
    elif 18 <= heure < 22:
        return "soir"
    else:
        return "nuit"


def get_greeting_response(langue='fr'):
    """Retourne la salutation adaptée à l'heure."""
    period = get_greeting_period()
    
    if langue == 'sw':
        greetings = {
            "matin": "Habari za asubuhi !",
            "apres_midi": "Habari za mchana !",
            "soir": "Habari za jioni !",
            "nuit": "Habari za usiku !",
        }
        return greetings[period]
    else:
        greetings = {
            "matin": "Bonjour !",
            "apres_midi": "Bon apres-midi !",
            "soir": "Bonsoir !",
            "nuit": "Bonne nuit !",
        }
        return greetings[period]


def get_welcome_message(langue='fr'):
    """Message d'accueil complet, adapté à l'heure."""
    greeting = get_greeting_response(langue)
    
    if langue == 'sw':
        return (
            f"{greeting} Je suis **Daktari IA Uvira**, votre assistant sante virtuel. 🩺\n\n"
            "**Ninaweza kukusaidia kwa :**\n"
            "- Kueleza dalili zako na kukuelekeza\n"
            "- Kujibu maswali yako kuhusu afya\n"
            "- Kukupa taarifa kuhusu magonjwa ya kawaida\n\n"
            "**Lugha ninazotumia :** Francais, Kiswahili\n\n"
            "Niambie, una shida gani leo ?"
        )
    else:
        return (
            f"{greeting} Je suis **Docteur IA Uvira**, votre assistant sante virtuel. 🩺\n\n"
            "**Je peux vous aider a :**\n"
            "- Decrire vos symptomes et vous orienter\n"
            "- Repondre a vos questions de sante\n"
            "- Vous informer sur les maladies courantes\n\n"
            "**Langues supportees :** Francais, Kiswahili\n\n"
            "Dites-moi, comment puis-je vous aider aujourd'hui ?"
        )


# =============================================
# DETECTION DE L'INTENTION
# =============================================
def detect_smalltalk_intent(user_message: str):
    """
    Détecte si le message est du small talk.
    Retourne (intent, langue) ou (None, None) si ce n'est pas du small talk.
    """
    if not user_message:
        return None, None
    
    msg = user_message.lower().strip()
    
    # Détecter la langue
    langue = 'sw' if any(s in msg for s in SALUTATIONS_SW) else 'fr'
    
    # Vérifier chaque pattern
    for intent, patterns in SMALLTALK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, msg, re.IGNORECASE):
                return intent, langue
    
    # Vérifier les salutations simples
    if any(s in msg for s in SALUTATIONS):
        return "greeting", langue
    
    return None, None


def get_smalltalk_response(intent: str, langue: str) -> str:
    """Retourne la réponse appropriée selon l'intention."""
    
    responses = {
        # ============ COMMENT VAS-TU ============
        "how_are_you": {
            "fr": (
                "Je vais tres bien, merci de demander ! 😊 "
                "Je suis la pour vous aider. Dites-moi, comment puis-je vous "
                "assister aujourd'hui ? Vous pouvez me decrire vos symptomes "
                "ou me poser une question de sante."
            ),
            "sw": (
                "Nzuri sana, asante kwa kuuliza ! 😊 Niko hapa kukusaidia. "
                "Niambie, ninaweza kukusaidia vipi leo ? Unaweza kueleza "
                "dalili zako au kuuliza swali kuhusu afya."
            ),
        },
        
        # ============ QUI ES-TU ============
        "who_are_you": {
            "fr": (
                "Je suis **Docteur IA Uvira**, un assistant sante virtuel "
                "developpe pour la communaute d'Uvira. 🩺\n\n"
                "J'utilise l'intelligence artificielle pour :\n"
                "- Comprendre vos symptomes\n"
                "- Vous orienter vers les soins appropries\n"
                "- Repondre a vos questions de sante\n\n"
                "Je fonctionne en **francais** et en **kiswahili**. "
                "Dites-moi ce qui vous amene."
            ),
            "sw": (
                "Mimi ni **Daktari IA Uvira**, msaidizi wa afya wa mtandao "
                "kwa jamii ya Uvira. 🩺\n\n"
                "Ninatumia akili ya bandia kwa :\n"
                "- Kuelewa dalili zako\n"
                "- Kukuelekeza kwa huduma sahihi\n"
                "- Kujibu maswali yako kuhusu afya\n\n"
                "Ninafanya kazi kwa **Kifaransa** na **Kiswahili**. "
                "Niambie kile kinachokuletea."
            ),
        },
        
        # ============ QUE PEUX-TU FAIRE ============
        "what_can_you_do": {
            "fr": (
                "Voici ce que je peux faire pour vous : 🩺\n\n"
                "**1. Analyser vos symptomes**\n"
                "Ex : *« J'ai la fievre depuis 3 jours »*\n\n"
                "**2. Repondre a vos questions de sante**\n"
                "Ex : *« Quels sont les signes du paludisme ? »*\n\n"
                "**3. Detecter les urgences**\n"
                "Ex : *« Je saigne beaucoup »* → alerte immediate\n\n"
                "**4. Vous informer sur les maladies**\n"
                "Paludisme, diarrhee, tuberculose, VIH, grossesse, nutrition, "
                "sante mentale, urgences, sante de l'enfant...\n\n"
                "**Comment commencer ?**\n"
                "Dites-moi simplement ce qui vous arrive, en francais ou en "
                "kiswahili. Je suis la pour vous aider."
            ),
            "sw": (
                "Haya ni mambo ninayoweza kukusaidia : 🩺\n\n"
                "**1. Kuchambua dalili zako**\n"
                "Mf : *« Nina homa kwa siku 3 »*\n\n"
                "**2. Kujibu maswali yako kuhusu afya**\n"
                "Mf : *« Dalili za malaria ni zipi ? »*\n\n"
                "**3. Kutambua dharura**\n"
                "Mf : *« Natoka damu nyingi »* → tahadhari ya haraka\n\n"
                "**4. Kukupa taarifa kuhusu magonjwa**\n"
                "Malaria, kuhara, kifua kikuu, VVU, ujauzito, lishe, "
                "afya ya akili, dharura, afya ya mtoto...\n\n"
                "**Jinsi ya kuanza ?**\n"
                "Niambie tu kinachokupata, kwa Kifaransa au Kiswahili. "
                "Niko hapa kukusaidia."
            ),
        },
        
        # ============ MERCI ============
        "thank_you": {
            "fr": (
                "Avec plaisir ! 😊 N'hesitez pas si vous avez d'autres questions. "
                "Prenez soin de vous."
            ),
            "sw": (
                "Karibu ! 😊 Usisite kama una maswali mengine. "
                "Jiangalie vizuri."
            ),
        },
        
        # ============ AU REVOIR ============
        "goodbye": {
            "fr": (
                "Au revoir ! 👋 Prenez soin de votre sante. "
                "Revenez quand vous voulez."
            ),
            "sw": (
                "Kwaheri ! 👋 Jiangalie vizuri. "
                "Karibu tena wakati wowote."
            ),
        },
        
        # ============ SALUTATION SIMPLE ============
        "greeting": {
            "fr": (
                "Bonjour ! Je suis **Docteur IA Uvira**. 🩺\n\n"
                "Comment puis-je vous aider aujourd'hui ? "
                "Vous pouvez me decrire vos symptomes ou me poser une question "
                "de sante."
            ),
            "sw": (
                "Habari ! Mimi ni **Daktari IA Uvira**. 🩺\n\n"
                "Ninaweza kukusaidia vipi leo ? "
                "Unaweza kueleza dalili zako au kuuliza swali kuhusu afya."
            ),
        },
    }
    
    # Adapter la salutation à l'heure
    if intent == "greeting":
        greeting = get_greeting_response(langue)
        if langue == 'sw':
            return (
                f"{greeting} Mimi ni **Daktari IA Uvira**. 🩺\n\n"
                "Ninaweza kukusaidia vipi leo ? "
                "Unaweza kueleza dalili zako au kuuliza swali kuhusu afya."
            )
        else:
            return (
                f"{greeting} Je suis **Docteur IA Uvira**. 🩺\n\n"
                "Comment puis-je vous aider aujourd'hui ? "
                "Vous pouvez me decrire vos symptomes ou me poser une question "
                "de sante."
            )
    
    return responses.get(intent, {}).get(langue, "Comment puis-je vous aider ?")