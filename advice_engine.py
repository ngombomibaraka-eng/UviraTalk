# advice_engine.py
"""
Moteur de conseil professionnel.
Genere des conseils adaptes selon le theme, les symptomes et le niveau d'urgence.
"""


# =============================================
# CONSEILS PAR THEME ET PAR URGENCE
# =============================================
ADVICE_DATABASE = {
    # ===========================================
    # DIARRHEE
    # ===========================================
    "Diarrhée": {
        "faible": {
            "fr": (
                "**Conseils pour la diarrhee legere :**\n\n"
                "1. Buvez beaucoup d'eau propre ou une solution de rehydratation orale (SRO)\n"
                "2. Mangez leger : riz, bananes, bouillie\n"
                "3. Evitez les aliments gras et epices\n"
                "4. Lavez-vous les mains avant de manger\n\n"
                "Si la diarrhee dure plus de 3 jours, consultez un centre de sante."
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
                "**Conseils pour la diarrhee moderee :**\n\n"
                "1. Buvez du SRO apres chaque selle liquide\n"
                "2. Consultez un centre de sante dans les 24 heures\n"
                "3. Surveillez les signes de deshydratation (bouche seche, grande soif)\n"
                "4. Ne prenez pas de medicaments sans avis medical"
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
                "**CONSULTEZ IMMEDIATEMENT UN CENTRE DE SANTE**\n\n"
                "Votre diarrhee presente des signes de gravite :\n\n"
                "1. Allez au centre de sante le plus proche AUJOURD'HUI\n"
                "2. Continuez a boire du SRO en attendant\n"
                "3. Si vous ne pouvez pas boire, c'est une URGENCE\n"
                "4. Emportez vos selles si possible pour analyse"
            ),
            "sw": (
                "**NENDA KITUO CHA AFYA MARA MOJA**\n\n"
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
                "**Conseils pour le paludisme suspecte :**\n\n"
                "1. Faites un test de depistage au centre de sante\n"
                "2. Buvez beaucoup d'eau\n"
                "3. Reposez-vous\n"
                "4. Prenez du paracetamol contre la fievre (sans depasser la dose)\n"
                "5. Dormez sous une moustiquaire impregnee"
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
                "**CONSULTEZ RAPIDEMENT - SUSPICION DE PALUDISME GRAVE**\n\n"
                "Les signes suivants sont graves :\n"
                "- Convulsions\n"
                "- Perte de connaissance\n"
                "- Difficultes a respirer\n"
                "- Incapacite a boire\n\n"
                "**ALLEZ AU CENTRE DE SANTE LE PLUS PROCHE IMMEDIATEMENT.**\n"
                "Le paludisme grave peut tuer en 24-48h sans traitement."
            ),
            "sw": (
                "**NENDA HARAKA - MALARIA KALI INAWEZA KUWA**\n\n"
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
                "**URGENCE MEDICALE - APPELEZ DE L'AIDE IMMEDIATEMENT**\n\n"
                "1. **Appelez une ambulance** ou faites-vous transporter immediatement\n"
                "2. **Ne donnez rien a boire** a la personne inconsciente\n"
                "3. **Ne deplacez pas** une personne blessee sauf danger immediat\n"
                "4. Restez calme et surveillez la respiration\n\n"
                "**Centre de sante le plus proche : a preciser**\n"
                "**Numero d'urgence : a preciser**"
            ),
            "sw": (
                "**DHARURA YA KITABIBU - TAFAUTA MSAADA MARA MOJA**\n\n"
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
    # SANTE ENFANT
    # ===========================================
    "Santé Enfant": {
        "modere": {
            "fr": (
                "**Conseils pour la sante de l'enfant :**\n\n"
                "1. **Surveillez la temperature** plusieurs fois par jour\n"
                "2. **Donnez a boire souvent** (eau, lait maternel)\n"
                "3. **Ne couvrez pas trop** l'enfant\n"
                "4. Consultez un centre de sante dans les 24h\n\n"
                "**Signes d'alerte chez l'enfant :**\n"
                "- Refus de boire ou de teter\n"
                "- Yeux enfonces\n"
                "- Somnolence inhabituelle\n"
                "- Convulsions\n\n"
                "Consultez IMMEDIATEMENT si un de ces signes apparait."
            ),
            "sw": (
                "**Ushauri kwa afya ya mtoto :**\n\n"
                "1. **Angalia joto** mara kadhaa kwa siku\n"
                "2. **Mpe maji mara kwa mara** (maji, maziwa ya mama)\n"
                "3. **Usimfunike sana** mtoto\n"
                "4. Nenda kituo cha afya ndani ya masaa 24\n\n"
                "**Dalili za hatari kwa mtoto :**\n"
                "- Kukataa kunywa au kunyonya\n"
                "- Macho yaliyochimbika\n"
                "- Kulala kupita kiasi\n"
                "- Degedege\n\n"
                "Nenda MARA MOJA kama dalili hizi zinaonekana."
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
                "1. **Consultez regulierement** pour le suivi prenatal (CPN)\n"
                "2. **Prenez de l'acide folique** et du fer selon prescription\n"
                "3. **Dormez sous moustiquaire** (prevention du paludisme)\n"
                "4. **Mangez equilibre** : legumes, fruits, proteines\n"
                "5. **Buvez beaucoup d'eau**\n\n"
                "**Consultez immediatement si :**\n"
                "- Saignements vaginaux\n"
                "- Le bebe bouge moins\n"
                "- Maux de tete intenses\n"
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
                "**Nenda mara moja kama :**\n"
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
                "**SUSPICION DE TUBERCULOSE - CONSULTEZ RAPIDEMENT**\n\n"
                "La tuberculose est **guerissable** avec un traitement complet.\n\n"
                "1. **Allez au centre de sante** pour un test de crachats (GeneXpert)\n"
                "2. **Le traitement est GRATUIT** en RDC\n"
                "3. **Ne toussez pas** sans couvrir votre bouche\n"
                "4. **Aerez** votre chambre\n"
                "5. Faites tester votre famille\n\n"
                "**Ne partagez pas** vos affaires personnelles."
            ),
            "sw": (
                "**KIFUA KIKUU INAWEZA KUWA - NENDA HARAKA**\n\n"
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
                "1. **Faites un test de depistage** - c'est gratuit et confidentiel\n"
                "2. Si positif, **le traitement ARV** permet de vivre longtemps et en bonne sante\n"
                "3. **Prenez vos medicaments** tous les jours sans interruption\n"
                "4. **Utilisez des preservatifs** pour proteger votre partenaire\n"
                "5. **Ne partagez pas** les objets coupants\n\n"
                "**Vous n'etes pas seul(e).** Le soutien existe."
            ),
            "sw": (
                "**Ushauri kuhusu VVU :**\n\n"
                "1. **Fanya mtihani** - ni bure na ni siri\n"
                "2. Kama ni chanya, **matibabu ya ARV** yanaruhusu kuishi muda mrefu\n"
                "3. **Chukua dawa zako** kila siku bila kukosa\n"
                "4. **Tumia kondomu** kulinda mwenza wako\n"
                "5. **Usishiriki** vifaa vya kukata\n\n"
                "**Hauko peke yako.** Msaada upo."
            ),
        },
    },

    # ===========================================
    # SANTE MENTALE
    # ===========================================
    "Santé Mentale": {
        "eleve": {
            "fr": (
                "**Conseils pour la sante mentale :**\n\n"
                "Ce que vous ressentez est **reel et important**.\n\n"
                "1. **Parlez-en** a une personne de confiance\n"
                "2. **Consultez un professionnel** (psychologue, infirmier forme)\n"
                "3. **Ne restez pas seul(e)** - cherchez du soutien\n"
                "4. **Reposez-vous** et mangez regulierement\n"
                "5. **Evitez l'alcool et les drogues**\n\n"
                "**Si vous pensez a vous faire du mal :**\n"
                "- **Cherchez de l'aide immediatement.**\n"
                "- Parlez a quelqu'un pres de vous.\n"
                "- Allez au centre de sante le plus proche."
            ),
            "sw": (
                "**Ushauri kwa afya ya akili :**\n\n"
                "Unachohisi ni **kweli na ni muhimu**.\n\n"
                "1. **Zungumza na mtu** unayemwamini\n"
                "2. **Nenda kwa mtaalamu** (mwanasaikolojia, muuguzi)\n"
                "3. **Usibaki peke yako** - tafuta msaada\n"
                "4. **Pumzika** na ule kwa kawaida\n"
                "5. **Epuka pombe na dawa za kulevya**\n\n"
                "**Kama unafikiria kujidhuru :**\n"
                "- **Tafuta msaada mara moja.**\n"
                "- Zungumza na mtu aliye karibu nawe.\n"
                "- Nenda kituo cha afya kilicho karibu."
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
                "1. **Mangez varie** : cereales, legumineuses, legumes, fruits\n"
                "2. **Proteines** : haricots, arachides, poisson, viande, oeufs\n"
                "3. **Vitamines** : legumes verts, fruits de saison\n"
                "4. **Buvez de l'eau propre** regulierement\n"
                "5. **Evitez** les aliments tres sucres ou tres gras\n\n"
                "**Pour les enfants :** allaitez jusqu'a 2 ans, ajoutez des aliments varies apres 6 mois."
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
    Retourne un conseil adapte selon le theme et le niveau d'urgence.

    Args:
        theme: le theme medical (Diarrhee, Paludisme, etc.)
        urgence: 'Faible', 'Moderee', 'Elevee', 'Critique', 'Tres elevee'
        langue: 'fr' ou 'sw'

    Returns:
        Le conseil formate, ou None si aucun conseil n'est trouve.
    """
    if not theme:
        return None

    urgence_norm = (urgence or 'faible').lower().strip()

    urgence_map = {
        'faible': 'faible',
        'modérée': 'modere',
        'moderee': 'modere',
        'élevée': 'eleve',
        'elevee': 'eleve',
        'critique': 'critique',
        'très élevée': 'critique',
        'tres elevee': 'critique',
        'ya juu': 'eleve',
        'ya juu sana': 'critique',
    }
    urgence_key = urgence_map.get(urgence_norm, 'modere')

    theme_advice = ADVICE_DATABASE.get(theme)
    if not theme_advice:
        return None

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
# SUGGESTION DE CENTRE DE SANTE
# =============================================
def get_health_center_suggestion(urgence_key: str, langue: str = 'fr') -> str:
    """Retourne une suggestion de delai de consultation."""
    suggestions = {
        'critique': {
            'fr': "**Rendez-vous immediatement au centre de sante le plus proche.**",
            'sw': "**Nenda mara moja kituo cha afya kilicho karibu.**",
        },
        'eleve': {
            'fr': "**Consultez un centre de sante dans les 24 heures.**",
            'sw': "**Nenda kituo cha afya ndani ya masaa 24.**",
        },
        'modere': {
            'fr': "**Consultez un centre de sante dans les 2-3 jours si les symptomes persistent.**",
            'sw': "**Nenda kituo cha afya katika siku 2-3 kama dalili zinaendelea.**",
        },
        'faible': {
            'fr': "**Restez a la maison et surveillez. Consultez si les symptomes s'aggravent.**",
            'sw': "**Baki nyumbani na angalia. Nenda kama dalili zinaongezeka.**",
        },
    }
    return suggestions.get(urgence_key, suggestions['modere']).get(langue, '')