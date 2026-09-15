# advice_engine.py
"""
Moteur de conseil professionnel.
Génère des conseils adaptés selon le thème, les symptômes et le niveau d'urgence.
"""


# =============================================
# CONSEILS PAR THÈME ET PAR URGENCE
# =============================================
ADVICE_DATABASE = {
    # ===========================================
    # DIARRHÉE
    # ===========================================
    "Diarrhée": {
        "faible": {
            "fr": (
                "**Conseils pour la diarrhée légère :**\n\n"
                "1. Buvez beaucoup d'eau propre ou une solution de réhydratation orale (SRO)\n"
                "2. Mangez léger : riz, bananes, bouillie\n"
                "3. Évitez les aliments gras et épicés\n"
                "4. Lavez-vous les mains avant de manger\n\n"
                "Si la diarrhée dure plus de 3 jours, consultez un centre de santé."
            ),
            "sw": (
                "**Ushauri kwa kuhara kidogo :**\n\n"
                "1. Kunywa maji mengi safi au SRO\n"
                "2. Kula vyakula vyepesi : wali, ndizi, uji\n"
                "3. Epuka vyakula vyenye mafuta na viungo\n"
                "4. Nawa mikono kabla ya kula\n\n"
                "Kama kuhara kunadumu zaidi ya siku 3, nenda kituo cha afya."
            ),
        },
        "modere": {
            "fr": (
                "**Conseils pour la diarrhée modérée :**\n\n"
                "1. Buvez du SRO après chaque selle liquide\n"
                "2. Consultez un centre de santé dans les 24 heures\n"
                "3. Surveillez les signes de déshydratation (bouche sèche, grande soif)\n"
                "4. Ne prenez pas de médicaments sans avis médical"
            ),
            "sw": (
                "**Ushauri kwa kuhara kwa wastani :**\n\n"
                "1. Kunywa SRO baada ya kila haja kubwa\n"
                "2. Nenda kituo cha afya ndani ya masaa 24\n"
                "3. Angalia dalili za kukosa maji mwilini (mdomo mkavu, kiu kubwa)\n"
                "4. Usichukue dawa bila ushauri wa daktari"
            ),
        },
        "eleve": {
            "fr": (
                "**⚠️ CONSULTEZ IMMÉDIATEMENT UN CENTRE DE SANTÉ**\n\n"
                "Votre diarrhée présente des signes de gravité :\n\n"
                "1. Allez au centre de santé le plus proche AUJOURD'HUI\n"
                "2. Continuez à boire du SRO en attendant\n"
                "3. Si vous ne pouvez pas boire, c'est une URGENCE\n"
                "4. Emportez vos selles si possible pour analyse"
            ),
            "sw": (
                "**⚠️ NENDA KITUO CHA AFYA MARA MOJA**\n\n"
                "Kuhara kwako kuna dalili za hatari :\n\n"
                "1. Nenda kituo cha afya kilicho karibu LEO\n"
                "2. Endelea kunywa SRO wakati unasubiri\n"
                "3. Kama hauwezi kunywa, ni DHARURA\n"
                "4. Chukua kinyesi chako kama inawezekana"
            ),
        },
    },

    # ===========================================
    # PALUDISME
    # ===========================================
    "Paludisme": {
        "faible": {
            "fr": (
                "**Conseils pour le paludisme suspecté :**\n\n"
                "1. Faites un test de dépistage au centre de santé\n"
                "2. Buvez beaucoup d'eau\n"
                "3. Reposez-vous\n"
                "4. Prenez du paracétamol contre la fièvre (sans dépasser la dose)\n"
                "5. Dormez sous une moustiquaire imprégnée"
            ),
            "sw": (
                "**Ushauri kwa malaria inayoshukiwa :**\n\n"
                "1. Fanya mtihani kwenye kituo cha afya\n"
                "2. Kunywa maji mengi\n"
                "3. Pumzika\n"
                "4. Chukua paracetamol kwa homa (bila kupita kiwango)\n"
                "5. Lala chini ya chandarua"
            ),
        },
        "eleve": {
            "fr": (
                "**⚠️ CONSultez RAPIDEMENT — SUSPICION DE PALUDISME GRAVE**\n\n"
                "Les signes suivants sont graves :\n"
                "- Convulsions\n"
                "- Perte de connaissance\n"
                "- Difficultés à respirer\n"
                "- Incapacité à boire\n\n"
                "**ALLEZ AU CENTRE DE SANTÉ LE PLUS PROCHE IMMÉDIATEMENT.**\n"
                "Le paludisme grave peut tuer en 24-48h sans traitement."
            ),
            "sw": (
                "**⚠️ NENDA HARAKA — MALARIA KALI INAWEZA KUWA**\n\n"
                "Dalili hizi ni za hatari :\n"
                "- Degedege\n"
                "- Kupoteza fahamu\n"
                "- Shida ya kupumua\n"
                "- Kushindwa kunywa\n\n"
                "**NENDA KITUO CHA AFYA MARA MOJA.**\n"
                "Malaria kali inaweza kuua katika masaa 24-48 bila matibabu."
            ),
        },
    },

    # ===========================================
    # URGENCES
    # ===========================================
    "Urgences": {
        "critique": {
            "fr": (
                "**🚨 URGENCE MÉDICALE — APPELEZ DE L'AIDE IMMÉDIATEMENT**\n\n"
                "1. **Appelez une ambulance** ou faites-vous transporter immédiatement\n"
                "2. **Ne donnez rien à boire** à la personne inconsciente\n"
                "3. **Ne déplacez pas** une personne blessée sauf danger immédiat\n"
                "4. Restez calme et surveillez la respiration\n\n"
                "**Centre de santé le plus proche : à préciser**\n"
                "**Numéro d'urgence : à préciser**"
            ),
            "sw": (
                "**🚨 DHARURA YA KITABIBU — TAFAUTA MSAADA MARA MOJA**\n\n"
                "1. **Piga simu gari la dharura** au mpe mtu akusafirishe haraka\n"
                "2. **Usimpe kitu cha kunywa** mtu asiyefahamu\n"
                "3. **Usimhamishe** mtu aliyejeruhiwa isipokuwa kuna hatari\n"
                "4. Tulia na angalia kupumua\n\n"
                "**Kituo cha afya kilicho karibu : kubainisha**\n"
                "**Namba ya dharura : kubainisha**"
            ),
        },
    },

    # ===========================================
    # SANTÉ ENFANT
    # ===========================================
    "Santé Enfant": {
        "modere": {
            "fr": (
                "**Conseils pour la santé de l'enfant :**\n\n"
                "1. **Surveillez la température** plusieurs fois par jour\n"
                "2. **Donnez à boire souvent** (eau, lait maternel)\n"
                "3. **Ne couvrez pas trop** l'enfant\n"
                "4. Consultez un centre de santé dans les 24h\n\n"
                "**⚠️ Signes d'alerte chez l'enfant :**\n"
                "- Refus de boire ou de téter\n"
                "- Yeux enfoncés\n"
                "- Somnolence inhabituelle\n"
                "- Convulsions\n\n"
                "→ Consultez IMMÉDIATEMENT si un de ces signes apparaît."
            ),
            "sw": (
                "**Ushauri kwa afya ya mtoto :**\n\n"
                "1. **Angalia joto** mara kadhaa kwa siku\n"
                "2. **Mpe maji mara kwa mara** (maji, maziwa ya mama)\n"
                "3. **Usimfunike sana** mtoto\n"
                "4. Nenda kituo cha afya ndani ya masaa 24\n\n"
                "**⚠️ Dalili za hatari kwa mtoto :**\n"
                "- Kukataa kunywa au kunyonya\n"
                "- Macho yaliyochimbika\n"
                "- Kulala kupita kiasi\n"
                "- Degedege\n\n"
                "→ Nenda MARA MOJA kama dalili hizi zinaonekana."
            ),
        },
    },

    # ===========================================
    # GROSSESSE
    # ===========================================
    "Grossesse": {
        "modere": {
            "fr": (
                "**Conseils pour la grossesse :**\n\n"
                "1. **Consultez régulièrement** pour le suivi prénatal (CPN)\n"
                "2. **Prenez de l'acide folique** et du fer selon prescription\n"
                "3. **Dormez sous moustiquaire** (prévention du paludisme)\n"
                "4. **Mangez équilibré** : légumes, fruits, protéines\n"
                "5. **Buvez beaucoup d'eau**\n\n"
                "**⚠️ Consultez immédiatement si :**\n"
                "- Saignements vaginaux\n"
                "- Le bébé bouge moins\n"
                "- Maux de tête intenses\n"
                "- Vision floue\n"
                "- Convulsions"
            ),
            "sw": (
                "**Ushauri kwa ujauzito :**\n\n"
                "1. **Nenda kliniki mara kwa mara** kwa CPN\n"
                "2. **Chukua asidi foliki** na chuma kama ilivyoagizwa\n"
                "3. **Lala chini ya chandarua** (kuzuia malaria)\n"
                "4. **Kula vyakula vyenye lishe** : mboga, matunda, protini\n"
                "5. **Kunywa maji mengi**\n\n"
                "**⚠️ Nenda mara moja kama :**\n"
                "- Kutoka damu ukeni\n"
                "- Mtoto anacheza kidogo\n"
                "- Maumivu makali ya kichwa\n"
                "- Kuona vibaya\n"
                "- Degedege"
            ),
        },
    },

    # ===========================================
    # TUBERCULOSE
    # ===========================================
    "Tuberculose": {
        "eleve": {
            "fr": (
                "**⚠️ SUSPICION DE TUBERCULOSE — CONSULTEZ RAPIDEMENT**\n\n"
                "La tuberculose est **guérissable** avec un traitement complet.\n\n"
                "1. **Allez au centre de santé** pour un test de crachats (GeneXpert)\n"
                "2. **Le traitement est GRATUIT** en RDC\n"
                "3. **Ne toussez pas** sans couvrir votre bouche\n"
                "4. **Aérez** votre chambre\n"
                "5. Faites tester votre famille\n\n"
                "**Ne partagez pas** vos affaires personnelles."
            ),
            "sw": (
                "**⚠️ KIFUA KIKUU INAWEZA KUWA — NENDA HARAKA**\n\n"
                "Kifua kikuu **kinaponywa** kwa matibabu kamili.\n\n"
                "1. **Nenda kituo cha afya** kwa mtihani wa makohozi (GeneXpert)\n"
                "2. **Matibabu ni BURE** katika RDC\n"
                "3. **Usikohoe** bila kufunika mdomo\n"
                "4. **Fungua dirisha** chumba chako\n"
                "5. Wapime familia yako\n\n"
                "**Usishiriki** vitu vyako vya kibinafsi."
            ),
        },
    },

    # ===========================================
    # VIH-SIDA
    # ===========================================
    "VIH-SIDA": {
        "modere": {
            "fr": (
                "**Conseils concernant le VIH :**\n\n"
                "1. **Faites un test de dépistage** — c'est gratuit et confidentiel\n"
                "2. Si positif, **le traitement ARV** permet de vivre longtemps et en bonne santé\n"
                "3. **Prenez vos médicaments** tous les jours sans interruption\n"
                "4. **Utilisez des préservatifs** pour protéger votre partenaire\n"
                "5. **Ne partagez pas** les objets coupants\n\n"
                "**Vous n'êtes pas seul(e).** Le soutien existe."
            ),
            "sw": (
                "**Ushauri kuhusu VVU :**\n\n"
                "1. **Fanya mtihani** — ni bure na ni siri\n"
                "2. Kama ni chanya, **matibabu ya ARV** yanaruhusu kuishi muda mrefu\n"
                "3. **Chukua dawa zako** kila siku bila kukosa\n"
                "4. **Tumia kondomu** kulinda mwenza wako\n"
                "5. **Usishiriki** vifaa vya kukata\n\n"
                "**Hauko peke yako.** Msaada upo."
            ),
        },
    },

    # ===========================================
    # SANTÉ MENTALE
    # ===========================================
    "Santé Mentale": {
        "eleve": {
            "fr": (
                "**Conseils pour la santé mentale :**\n\n"
                "Ce que vous ressentez est **réel et important**.\n\n"
                "1. **Parlez-en** à une personne de confiance\n"
                "2. **Consultez un professionnel** (psychologue, infirmier formé)\n"
                "3. **Ne restez pas seul(e)** — cherchez du soutien\n"
                "4. **Reposez-vous** et mangez régulièrement\n"
                "5. **Évitez l'alcool et les drogues**\n\n"
                "**🚨 Si vous pensez à vous faire du mal :**\n"
                "→ **Cherchez de l'aide immédiatement.**\n"
                "→ Parlez à quelqu'un près de vous.\n"
                "→ Allez au centre de santé le plus proche."
            ),
            "sw": (
                "**Ushauri kwa afya ya akili :**\n\n"
                "Unachohisi ni **kweli na ni muhimu**.\n\n"
                "1. **Zungumza na mtu** unayemwamini\n"
                "2. **Nenda kwa mtaalamu** (mwanasaikolojia, muuguzi)\n"
                "3. **Usibaki peke yako** — tafuta msaada\n"
                "4. **Pumzika** na ule kwa kawaida\n"
                "5. **Epuka pombe na dawa za kulevya**\n\n"
                "**🚨 Kama unafikiria kujidhuru :**\n"
                "→ **Tafuta msaada mara moja.**\n"
                "→ Zungumza na mtu aliye karibu nawe.\n"
                "→ Nenda kituo cha afya kilicho karibu."
            ),
        },
    },

    # ===========================================
    # NUTRITION
    # ===========================================
    "Nutrition": {
        "modere": {
            "fr": (
                "**Conseils nutritionnels :**\n\n"
                "1. **Mangez varié** : céréales, légumineuses, légumes, fruits\n"
                "2. **Protéines** : haricots, arachides, poisson, viande, œufs\n"
                "3. **Vitamines** : légumes verts, fruits de saison\n"
                "4. **Buvez de l'eau propre** régulièrement\n"
                "5. **Évitez** les aliments très sucrés ou très gras\n\n"
                "**Pour les enfants :** allaitez jusqu'à 2 ans, ajoutez des aliments variés après 6 mois."
            ),
            "sw": (
                "**Ushauri wa lishe :**\n\n"
                "1. **Kula vyakula mbalimbali** : nafaka, mikunde, mboga, matunda\n"
                "2. **Protini** : maharage, karanga, samaki, nyama, mayai\n"
                "3. **Vitamini** : mboga za majani, matunda ya msimu\n"
                "4. **Kunywa maji safi** mara kwa mara\n"
                "5. **Epuka** vyakula vyenye sukari nyingi au mafuta mengi\n\n"
                "**Kwa watoto :** nyonyesha hadi miaka 2, ongeza vyakula mbalimbali baada ya miezi 6."
            ),
        },
    },
}


# =============================================
# FONCTION PRINCIPALE
# =============================================
def get_advice(theme: str, urgence: str, langue: str = 'fr') -> str:
    """
    Retourne un conseil adapté selon le thème et le niveau d'urgence.
    
    Args:
        theme: le thème médical (Diarrhée, Paludisme, etc.)
        urgence: 'Faible', 'Modérée', 'Élevée', 'Critique', 'Très élevée'
        langue: 'fr' ou 'sw'
    
    Returns:
        Le conseil formaté, ou None si aucun conseil n'est trouvé.
    """
    if not theme:
        return None
    
    # Normaliser l'urgence
    urgence_norm = (urgence or 'faible').lower().strip()
    
    # Mapper les valeurs d'urgence
    urgence_map = {
        'faible': 'faible',
        'modérée': 'modere',
        'modere': 'modere',
        'élevée': 'eleve',
        'eleve': 'eleve',
        'critique': 'critique',
        'très élevée': 'critique',
        'tres elevee': 'critique',
        'ya juu': 'eleve',
        'ya juu sana': 'critique',
    }
    urgence_key = urgence_map.get(urgence_norm, 'modere')
    
    # Récupérer la base de conseils pour ce thème
    theme_advice = ADVICE_DATABASE.get(theme)
    if not theme_advice:
        return None
    
    # Chercher le niveau d'urgence exact, sinon dégrader
    fallback_order = {
        'critique': ['critique', 'eleve', 'modere', 'faible'],
        'eleve':    ['eleve', 'modere', 'faible'],
        'modere':   ['modere', 'faible', 'eleve', 'critique'],
        'faible':   ['faible', 'modere', 'eleve', 'critique'],
    }
    
    for level in fallback_order.get(urgence_key, ['modere']):
        if level in theme_advice:
            advice = theme_advice[level]
            return advice.get(langue, advice.get('fr'))
    
    return None


# =============================================
# SUGGESTION DE CENTRE DE SANTÉ
# =============================================
def get_health_center_suggestion(urgence_key: str, langue: str = 'fr') -> str:
    """Retourne une suggestion de délai de consultation."""
    suggestions = {
        'critique': {
            'fr': "🚨 **Rendez-vous immédiatement au centre de santé le plus proche.**",
            'sw': "🚨 **Nenda mara moja kituo cha afya kilicho karibu.**",
        },
        'eleve': {
            'fr': "⏰ **Consultez un centre de santé dans les 24 heures.**",
            'sw': "⏰ **Nenda kituo cha afya ndani ya masaa 24.**",
        },
        'modere': {
            'fr': "📅 **Consultez un centre de santé dans les 2-3 jours si les symptômes persistent.**",
            'sw': "📅 **Nenda kituo cha afya katika siku 2-3 kama dalili zinaendelea.**",
        },
        'faible': {
            'fr': "🏠 **Restez à la maison et surveillez. Consultez si les symptômes s'aggravent.**",
            'sw': "🏠 **Baki nyumbani na angalia. Nenda kama dalili zinaongezeka.**",
        },
    }
    return suggestions.get(urgence_key, suggestions['modere']).get(langue, '')