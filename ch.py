Voici mon fichier insert_data.py: import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database import db, PhraseMultilingue

# Données multilingues pour l'entraînement de l'IA
phrases_data = [
    # Grossesse
    {
        "theme":"Grossesse","categorie":"conseil",
        "francais_local":"Consultez un centre de Santé régulièrement",
        "kiswahili":"Kendele kito cha afya mara kwa mara",
        "kifuliiru":"Uzairie isibian gisi kimepere",
        "kibembe":"Uye S'gire!",
        "intent":"prenatal_visits",
        "reponse_fr":"Consultez un centre de santé au moins 4 fois pendant la grossesse. Prenez vos vitamines.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Grossesse","categorie":"conseil",
        "francais_local":"Prenez les vitamines pour la grossesse",
        "kiswahili":"Chukua vitamini za uyayizo",
        "kifuliiru":"Uley ikoyokuliyo bili ajaliyo dyo mwajio",
        "kibembe":"Uende v, t, m, n, y, b, y, e, t, e, t, e, t, e, t, e, t, e,",
        "intent":"prenatal_vitamins",
        "reponse_fr":"Les vitamines prénatales aident à prévenir l'anémie et les malformations. Demandez au centre de santé.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    # Covid-19
    {
        "theme":"Covid-19","categorie":"symptom",
        "francais_local":"Avez-vous de la toux ou de la fièvre ?",
        "kiswahili":"Una kikohozi au homa ?",
        "kifuliiru":"Upeweti akakono kifu la dudu ?",
        "kibembe":"Ule n+ eusi 40 EUSEL!",
        "intent":"covid_symptoms",
        "reponse_fr":"Si vous avez de la toux ou de la fièvre, faites-vous tester. Portez un masque et gardez vos distances.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Covid-19","categorie":"prevention",
        "francais_local":"Gardez vos distances",
        "kiswahili":"Kaa mkali na watu",
        "kifuliiru":"Uleerehala na bandu",
        "kibembe":"UENGEBO'E",
        "intent":"social_distance",
        "reponse_fr":"Gardez au moins 1 mètre des autres personnes pour limiter la propagation.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Covid-19","categorie":"vaccination",
        "francais_local":"Vaccinez-vous contre le Covid-19",
        "kiswahili":"Pata chango ya corona",
        "kifuliiru":"Ulonge ishindano ya Corona",
        "kibembe":"Uleest choni ni wa NBO, ya korona!",
        "intent":"covid_vaccine",
        "reponse_fr":"Le vaccin Covid-19 est gratuit et disponible dans les centres de santé. Protégez-vous et protégez les autres.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    # VIH/SIDA
    {
        "theme":"VIH","categorie":"depistage",
        "francais_local":"Faites un test de dépistage",
        "kiswahili":"Fanya kipimo cha viu",
        "kifuliiru":"Ulonge ku mbole",
        "kibembe":"Uye Upenna Bisa Bvuvirus",
        "intent":"hiv_test",
        "reponse_fr":"Le dépistage du VIH est confidentiel et gratuit. Connaître son statut permet d'agir tôt.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"VIH","categorie":"prevention",
        "francais_local":"Utilisez des préservatifs",
        "kiswahili":"Fuma kondomu",
        "kifuliiru":"Kolesa boyokuku",
        "kibembe":"Uvende Bile Bina cita Bile",
        "intent":"condoms",
        "reponse_fr":"Les préservatifs protègent contre le VIH et les IST. Utilisez-les à chaque rapport.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"VIH","categorie":"information",
        "francais_local":"Le VIH n'est pas visible sur le visage",
        "kiswahili":"Vi viwamkana kwa vito",
        "kifuliiru":"Vyrus bila musome kama kumasu",
        "kibembe":"Bisa ya vi vi Takiye MONEA 0'30SOHO.",
        "intent":"hiv_invisible",
        "reponse_fr":"On ne peut pas savoir si une personne a le VIH en regardant son visage. Seul un test le confirme.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    # Symptômes généraux
    {
        "theme":"Symptomes","categorie":"plainte",
        "francais_local":"J'ai mal à la tête",
        "kiswahili":"Nini vima kichwa",
        "kifuliiru":"Nimeyanyanira ni tive",
        "kibembe":"NILE MOSABACHI SANG MEWE",
        "intent":"headache",
        "reponse_fr":"Buvez de l'eau, reposez-vous. Si persistant, consultez un centre de santé.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    
    # --- GUIDE PROFESSIONNEL : FIÈVRE ---
    {
        "theme":"Symptomes","categorie":"plainte",
        "francais_local":"J'ai de la fièvre temperature corps chauffe",
        "kiswahili":"Nini hona",
        "kifuliiru":"Nolipoveti idiliti",
        "kibembe":"NILE GASH CHI SANG MEWE USUSI ELI",
        "intent":"fever",
        "reponse_fr": """La fièvre est souvent un signe que votre corps combat une infection. Voici un guide pour vous aider :

📋 **POUR MIEUX VOUS ORIENTER :**
*   Quel âge avez-vous ?
*   Quelle est votre température si vous l'avez mesurée ?
*   Depuis combien de temps avez-vous de la fièvre ?
*   Avez-vous d'autres symptômes : maux de tête, toux, nez qui coule, douleurs musculaires, diarrhée, vomissements, douleurs abdominales, difficultés à respirer ?
*   Avez-vous déjà pris un médicament (ex: Paracétamol) ?

💡 **EN ATTENDANT DE ME RÉPONDRE :**
*   Buvez beaucoup d'eau ou de tisane pour vous hydrater.
*   Reposez-vous au calme.
*   Évitez les efforts physiques.
*   Si vous avez du Paracétamol, vous pouvez en prendre selon les doses usuelles (sauf contre-indication).

🚨 **CONSULTEZ RAPIDEMENT UN MÉDECIN OU UN CENTRE DE SANTÉ SI :**
*   La température est très élevée (≥ 40°C).
*   Vous avez des difficultés à respirer.
*   Vous êtes très somnolent, confus ou avez des convulsions.
*   Vous avez une raideur importante du cou (nuque).
*   La fièvre dure plus de 3 jours sans amélioration.

Pouvez-vous me donner votre température actuelle et décrire vos autres symptômes ?""",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },

    # --- GUIDE PROFESSIONNEL : TOUX ---
    {
        "theme":"Symptomes","categorie":"plainte",
        "francais_local":"J'ai de la toux je tousse toux grasse toux sèche",
        "kiswahili":"Nini kohana sina",
        "kifuliiru":"Nini ngohola bivienne",
        "kibembe":"NILE MOSOMONA HANGGA",
        "intent":"cough",
        "reponse_fr": """Si vous avez de la fièvre et de la toux, cela peut être lié à plusieurs causes, par exemple un rhume, une grippe, une bronchite, une pneumonie ou une infection respiratoire comme la COVID-19.

Pour mieux vous aider, dites-moi :

*   Depuis combien de jours avez-vous la fièvre et la toux ?
*   La toux est-elle sèche ou avec des crachats ?
*   Avez-vous des difficultés à respirer ?
*   Avez-vous mal à la poitrine ?
*   Quel âge avez-vous ?

💡 **EN ATTENDANT :**
*   Reposez-vous.
*   Buvez beaucoup d'eau, de thé ou de soupe.
*   Évitez la fumée et la poussière.
*   Si possible, mesurez votre température.

🚨 **CONSULTEZ RAPIDEMENT UN CENTRE DE SANTÉ SI :**
*   Des difficultés à respirer.
*   Une douleur thoracique importante.
*   Une forte faiblesse ou une confusion.
*   Une fièvre élevée persistante.

**Répondez-moi avec :**
1. Votre âge
2. Depuis combien de jours vous êtes malade
3. Si vous avez des difficultés à respirer (oui/non).""",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },

    {
        "theme":"Symptomes","categorie":"plainte",
        "francais_local":"J'ai des douleurs dans le ventre",
        "kiswahili":"Tumbo niniwani",
        "kifuliiru":"Tumbo limu bana",
        "kibembe":"",
        "intent":"abdominal_pain",
        "reponse_fr":"Évitez les aliments gras. Buvez beaucoup d'eau. Si douleur intense ou sang dans selles, allez à l'hôpital.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },

    # --- GUIDE PROFESSIONNEL : DIARRHÉE ---
    {
        "theme":"Maladies","categorie":"symptome",
        "francais_local":"J'ai de la diarrhée je cours selles liquides",
        "kiswahili":"Kuharisha",
        "kifuliiru":"Kuhara",
        "kibembe":"KIA LA",
        "intent":"diarrhea",
        "reponse_fr": """Le fait d'avoir de la fièvre, de la toux et de la diarrhée en même temps peut être dû à différentes infections, certaines nécessitant une évaluation médicale.

J'ai besoin de quelques précisions :

*   Quel âge avez-vous ?
*   Depuis combien de jours avez-vous ces symptômes ?
*   Avez-vous des difficultés à respirer ?
*   Avez-vous des vomissements ?
*   Y a-t-il du sang dans les selles ?

💡 **EN ATTENDANT :**
*   Buvez fréquemment de l'eau propre, des soupes ou une solution de réhydratation orale (SRO) si vous en avez.
*   Mangez léger (riz, bananes, bouillie, pommes de terre, etc.).
*   Reposez-vous.
*   Lavez-vous les mains régulièrement.

🚨 **CONSULTEZ RAPIDEMENT UN CENTRE DE SANTÉ SI :**
*   Vous avez des difficultés à respirer.
*   Vous êtes très faible ou somnolent.
*   Vous ne parvenez pas à boire suffisamment.
*   Vous avez du sang dans les selles.
*   La diarrhée est très abondante ou la fièvre est élevée.

**Pouvez-vous me dire :**
*   Votre âge ?
*   Depuis combien de jours les symptômes ont commencé ?
*   Avez-vous des difficultés à respirer ? (oui/non)""",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },

    # --- GUIDE PROFESSIONNEL : PALUDISME ---
    {
        "theme":"Maladies","categorie":"maladie",
        "francais_local":"J'ai de le paludisme j'ai le paludisme malaria",
        "kiswahili":"Malania",
        "kifuliiru":"Byanpa",
        "kibembe":"",
        "intent":"malaria",
        "reponse_fr": """Si vous pensez avoir le paludisme, surtout avec de la fièvre, il est important de faire un test de diagnostic du paludisme dans un centre de santé ou une pharmacie équipée.

Les symptômes fréquents du paludisme incluent :

*   Fièvre
*   Frissons
*   Maux de tête
*   Fatigue importante
*   Douleurs musculaires
*   Nausées ou vomissements

💡 **EN ATTENDANT :**
*   Buvez beaucoup d'eau pour éviter la déshydratation.
*   Reposez-vous.
*   Surveillez votre température.

🚨 **RENDEZ-VOUS RAPIDEMENT DANS UN CENTRE DE SANTÉ SI :**
*   Vous avez des difficultés à respirer.
*   Vous êtes très faible ou confus.
*   Vous ne pouvez pas boire ou manger.
*   Vous faites des convulsions.
*   Vous avez une forte fièvre persistante.

Avez-vous fait un test qui a confirmé le paludisme, ou pensez-vous l'avoir à cause de vos symptômes ? Cela m'aidera à vous conseiller plus précisément.""",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },

    {
        "theme":"Maladies","categorie":"maladie",
        "francais_local":"la grippe",
        "kiswahili":"Mafira",
        "kifuliiru":"Kusama mura",
        "kibembe":"EONGA",
        "intent":"flu",
        "reponse_fr":"Repos, boissons chaudes. Si fièvre haute ou difficultés respiratoires, consultez.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Maladies","categorie":"symptome",
        "francais_local":"la toux",
        "kiswahili":"Kikohogi",
        "kifuliiru":"Tumby",
        "kibembe":"TOSOMONA",
        "intent":"cough_disease",
        "reponse_fr":"Toux prolongée ? Faites vérifier. La tuberculose est fréquente ici, le traitement est gratuit.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    # Vaccination / Prévention
    {
        "theme":"Vaccination","categorie":"question",
        "francais_local":"Avez-vous été vacciné(e) ?",
        "kiswahili":"Umepewa chanjo ?",
        "kifuliiru":"Koka shirikwa kikash shindana",
        "kibembe":"WASHI PATA NGUBAI ?",
        "intent":"ask_vaccinated",
        "reponse_fr":"Si vous n'êtes pas vacciné, allez au centre de santé le plus proche. Les vaccins sauvent des vies.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Vaccination","categorie":"prevention",
        "francais_local":"Il faut se laver les mains régulièrement pour ne pas contaminer",
        "kiswahili":"Lajima kungu miko kik vakati",
        "kifuliiru":"Tukijikanda ama soko ngisi kikile",
        "kibembe":"ISWAWA MABOI KILA CHOSA",
        "intent":"handwash_prevention",
        "reponse_fr":"Lavez-vous les mains à l'eau et au savon : après les toilettes, avant de manger, après avoir toussé.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Vaccination","categorie":"prevention",
        "francais_local":"Portez un masque",
        "kiswahili":"Va Karakoa",
        "kifuliiru":"Uyamala ibiya kufuma akana",
        "kibembe":"WATA BIENGELE CHO",
        "intent":"mask_wearing",
        "reponse_fr":"Le masque réduit la propagation des virus. Portez-le dans les lieux bondés.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    # Hygiène
    {
        "theme":"Hygiène","categorie":"conseil",
        "francais_local":"Lavez-vous les mains avant de manger",
        "kiswahili":"Nawa mikono kala yag kula",
        "kifuliiru":"Ukarae amaboko imsere yop kulyo",
        "kibembe":"ISWAWA MABOI MASE YA ILYA",
        "intent":"handwash_eating",
        "reponse_fr":"Les mains sales transmettent les maladies. Lavez-vous toujours avant les repas.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Hygiène","categorie":"conseil",
        "francais_local":"Utilisez des latrines propres",
        "kiswahili":"Fuma vopo Saft!",
        "kifuliiru":"Ukolee umushuk mwiga",
        "kibembe":"MABWE CHASOSWIKA IYA MCHILE",
        "intent":"clean_latrines",
        "reponse_fr":"Des latrines propres évitent les épidémies de choléra et de diarrhée.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Hygiène","categorie":"conseil",
        "francais_local":"Nettoyez votre environnement",
        "kiswahili":"Safisha mazingira",
        "kifuliiru":"Fanga akaya suyiga",
        "kibembe":"",
        "intent":"clean_environment",
        "reponse_fr":"Un environnement sans eaux stagnantes réduit le paludisme. Nettoyez régulièrement.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    # Pharmacie / Médicaments
    {
        "theme":"Pharmacie","categorie":"medicament",
        "francais_local":"Douleur à la tête",
        "kiswahili":"Maumivu ya kichwa",
        "kifuliiru":"",
        "kibembe":"",
        "intent":"painkiller",
        "reponse_fr":"Pour la tête, vous pouvez prendre du paracétamol (Efezalgan, Zidan) ou de l'aspirine. Demandez conseil à la pharmacie.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Pharmacie","categorie":"medicament",
        "francais_local":"Diarrhée",
        "kiswahili":"Kuharisha",
        "kifuliiru":"",
        "kibembe":"",
        "intent":"ors",
        "reponse_fr":"Pour la diarrhée, prenez de l'ORS (solution de réhydratation orale). Les comprimés de zinc aident aussi.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
    {
        "theme":"Pharmacie","categorie":"medicament",
        "francais_local":"Paludisme",
        "kiswahili":"Malaria",
        "kifuliiru":"",
        "kibembe":"",
        "intent":"antimalaria",
        "reponse_fr":"Les médicaments contre le paludisme : Coartem, Artemether-luméfantrine. Prenez-les après un test positif.",
        "reponse_sw":"",
        "reponse_kir":"",
        "reponse_kib":""
    },
]

def insert_data():
    with app.app_context():
        db.create_all()
        print("Début de la synchronisation des données...")
        
        for p in phrases_data:
            existing = PhraseMultilingue.query.filter_by(intent=p['intent']).first()
            
            if not existing:
                entry = PhraseMultilingue(
                    theme=p['theme'],
                    categorie=p['categorie'],
                    francais_local=p['francais_local'],
                    kiswahili=p['kiswahili'],
                    kifuliiru=p['kifuliiru'],
                    kibembe=p['kibembe'],
                    intent=p['intent'],
                    reponse_fr=p.get('reponse_fr', ''),
                    reponse_sw=p.get('reponse_sw', ''),
                    reponse_kir=p.get('reponse_kir', ''),
                    reponse_kib=p.get('reponse_kib', '')
                )
                db.session.add(entry)
                print(f"✅ Nouvelle entrée ajoutée: {p['intent']}")
            else:
                # Mise à jour intelligente des guides sans casser les traductions existantes
                updated = False
                if p.get('reponse_fr') and p.get('reponse_fr') != existing.reponse_fr:
                    existing.reponse_fr = p.get('reponse_fr')
                    updated = True
                
                if p.get('reponse_sw') and p.get('reponse_sw') != existing.reponse_sw:
                    existing.reponse_sw = p.get('reponse_sw')
                    updated = True
                    
                if p.get('reponse_kir') and p.get('reponse_kir') != existing.reponse_kir:
                    existing.reponse_kir = p.get('reponse_kir')
                    updated = True

                if p.get('reponse_kib') and p.get('reponse_kib') != existing.reponse_kib:
                    existing.reponse_kib = p.get('reponse_kib')
                    updated = True

                if updated:
                    print(f"🔄 Mise à jour du guide: {p['intent']}")
        
        try:
            db.session.commit()
            print("\n✅ Synchronisation terminée avec succès.")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erreur lors de la synchronisation : {e}")

if __name__ == '__main__':
    insert_data()
       Voici mon cerveau alors qui va construire ce systeme: BASE DE DONNEES POUR UviraTalk
Phase 1 : Fondation UviraTalk.
1. Les 200 symptômes à collecter
Symptômes généraux
1.J'ai de la fièvre 
2.Mon corps chauffe 
3.J'ai des frissons 
4.Je transpire beaucoup 
5.Je suis faible 
6.Je suis fatigué 
7.Je n'ai pas de force 
8.J'ai mal à la tête 
9.J'ai des vertiges 
10.Je tremble 
Symptômes respiratoires
11.Je tousse 
12.J'ai une toux sèche 
13.Je crache 
14.J'ai du mal à respirer 
15.Je manque d'air 
16.J'ai mal à la poitrine 
17.J'ai le nez bouché 
18.Mon nez coule 
19.J'éternue 
20.J'ai mal à la gorge 
Symptômes digestifs
21.J'ai la diarrhée 
22.Je cours 
23.Je vomis 
24.J'ai envie de vomir 
25.J'ai mal au ventre 
26.Mon ventre gonfle 
27.Je suis constipé 
28.Je n'ai pas faim 
29.Je perds du poids 
30.J'ai des brûlures d'estomac 
Symptômes urinaires
31.J'urine souvent 
32.J'ai mal quand j'urine 
33.Mon urine est rouge 
34.Je n'urine pas beaucoup 
35.Mon urine sent mauvais 
Symptômes neurologiques
36.Je suis confus 
37.J'oublie facilement 
38.J'ai perdu connaissance 
39.J'ai des convulsions 
40.Je dors beaucoup 
Symptômes de la peau
41.J'ai des boutons 
42.J'ai une éruption 
43.Ma peau gratte 
44.J'ai une plaie 
45.J'ai une brûlure 
Grossesse
46.J'ai raté mes règles 
47.Je suis enceinte 
48.J'ai mal au bas ventre 
49.J'ai des saignements 
50.Le bébé bouge moins
Symptômes 51 à 80 : Douleurs musculaires et articulaires
51.J'ai mal au dos 
52.J'ai mal au cou 
53.J'ai mal aux épaules 
54.J'ai mal aux bras 
55.J'ai mal aux jambes 
56.J'ai mal aux genoux 
57.J'ai mal aux pieds 
58.J'ai mal aux mains 
59.J'ai mal aux articulations 
60.Mes muscles me font mal 
61.J'ai des courbatures 
62.Je ne peux pas marcher correctement 
63.J'ai les jambes lourdes 
64.Mes articulations sont gonflées 
65.J'ai mal en bougeant 
66.J'ai une douleur persistante 
67.J'ai une douleur soudaine 
68.J'ai des crampes 
69.Mes jambes tremblent 
70.Je suis paralysé d'un côté 
71.J'ai mal aux hanches 
72.J'ai mal aux chevilles 
73.Mes doigts sont douloureux 
74.J'ai une raideur articulaire 
75.J'ai des douleurs osseuses 
76.Je boite en marchant 
77.J'ai une entorse 
78.J'ai une fracture suspectée 
79.Mon membre est gonflé 
80.Je ne peux plus lever le bras 
Symptômes 81 à 110 : Yeux, oreilles, nez et bouche
81.J'ai mal aux yeux 
82.Mes yeux sont rouges 
83.Je vois flou 
84.Je vois double 
85.Je perds la vue 
86.J'ai les yeux qui pleurent 
87.J'ai une sensibilité à la lumière 
88.J'ai une infection des yeux 
89.Mes paupières sont gonflées 
90.J'ai quelque chose dans l'œil 
91.J'ai mal aux oreilles 
92.Mon oreille coule 
93.J'entends moins bien 
94.J'ai des bourdonnements d'oreille 
95.J'ai perdu l'audition 
96.J'ai le nez bouché 
97.Mon nez saigne 
98.J'ai perdu l'odorat 
99.J'ai perdu le goût 
100.J'ai une sinusite 
101.J'ai mal aux dents 
102.J'ai une dent cassée 
103.Mes gencives saignent 
104.J'ai mauvaise haleine 
105.J'ai des aphtes 
106.J'ai la bouche sèche 
107.J'ai du mal à avaler 
108.J'ai mal à la langue 
109.Ma mâchoire me fait mal 
110.J'ai une infection buccale 
Symptômes 111 à 140 : Peau et infections
111.J'ai des démangeaisons 
112.J'ai des boutons sur le corps 
113.J'ai une éruption cutanée 
114.J'ai des plaques sur la peau 
115.Ma peau pèle 
116.J'ai une allergie cutanée 
117.J'ai une plaie infectée 
118.J'ai du pus dans une plaie 
119.J'ai une brûlure légère 
120.J'ai une brûlure grave 
121.J'ai une morsure d'animal 
122.J'ai une piqûre d'insecte 
123.J'ai une enflure de la peau 
124.J'ai des taches sur la peau 
125.J'ai une peau très sèche 
126.J'ai des furoncles 
127.J'ai des verrues 
128.J'ai une infection fongique 
129.J'ai des boutons sur le visage 
130.J'ai une perte de cheveux 
131.Mes ongles changent de couleur 
132.Mes ongles se cassent facilement 
133.J'ai des ulcères sur la peau 
134.J'ai une plaie qui ne guérit pas 
135.J'ai des ganglions gonflés 
136.J'ai une rougeur sur la peau 
137.J'ai une douleur dans une plaie 
138.J'ai des cloques 
139.J'ai des lésions cutanées 
140.J'ai une infection généralisée de la peau 
Symptômes 141 à 170 : Santé mentale et neurologique
141.Je suis anxieux 
142.Je suis stressé 
143.Je suis triste tout le temps 
144.Je pleure souvent 
145.Je n'arrive pas à dormir 
146.Je dors très peu 
147.Je dors trop 
148.Je fais des cauchemars 
149.J'ai peur sans raison 
150.Je suis très inquiet 
151.Je manque de concentration 
152.J'oublie souvent 
153.Je suis désorienté 
154.J'entends des voix 
155.Je vois des choses inexistantes 
156.Je suis agité 
157.Je suis déprimé 
158.Je n'ai plus envie de rien 
159.J'ai des pensées suicidaires 
160.Je me sens seul 
161.Je fais des crises de panique 
162.Je suis facilement irrité 
163.Je suis agressif 
164.Je suis confus 
165.J'ai des pertes de mémoire 
166.J'ai des tremblements involontaires 
167.Je fais des convulsions 
168.Je perds connaissance 
169.J'ai des engourdissements 
170.J'ai des fourmillements 
Symptômes 171 à 200 : Nutrition, grossesse et divers
171.Je perds du poids rapidement 
172.Je prends du poids rapidement 
173.Je n'ai pas faim 
174.J'ai toujours faim 
175.J'ai très soif 
176.Je suis déshydraté 
177.Je suis pâle 
178.J'ai les lèvres sèches 
179.Je suis mal nourri 
180.Mon enfant maigrit 
181.Je suis enceinte 
182.J'ai raté mes règles 
183.J'ai des nausées de grossesse 
184.Je vomis pendant la grossesse 
185.J'ai des saignements pendant la grossesse 
186.J'ai des douleurs abdominales pendant la grossesse 
187.Mes pieds sont gonflés pendant la grossesse 
188.J'ai des contractions 
189.Je perds du liquide vaginal 
190.Je sens moins bouger le bébé 
191.J'ai des pertes vaginales anormales 
192.J'ai des démangeaisons génitales 
193.J'ai une douleur pendant les rapports sexuels 
194.J'ai une grosse fatigue 
195.Je transpire la nuit 
196.J'ai des frissons nocturnes 
197.J'ai une mauvaise odeur corporelle inhabituelle 
198.Je me sens très faible 
199.Je ne peux plus me lever du lit 
200.Mon état s'aggrave chaque jour

















Phase 2: 1. Maladies infectieuses et parasitaires (1-40)
1.Paludisme 
2.Choléra 
3.Fièvre typhoïde 
4.Tuberculose 
5.COVID-19 
6.VIH/SIDA 
7.Rougeole 
8.Coqueluche 
9.Pneumonie 
10.Méningite 
11.Hépatite A 
12.Hépatite B 
13.Hépatite C 
14.Poliomyélite 
15.Rage 
16.Tétanos 
17.Oreillons 
18.Varicelle 
19.Rubéole 
20.Dengue 
21.Fièvre jaune 
22.Bilharziose 
23.Amibiase 
24.Giardiase 
25.Ankylostomiase 
26.Ascaridiose 
27.Oxyurose 
28.Gale 
29.Teigne 
30.Conjonctivite infectieuse 
31.Otite infectieuse 
32.Sinusite bactérienne 
33.Bronchite aiguë 
34.Dysenterie 
35.Infection respiratoire aiguë 
36.Infection urinaire 
37.Infection intestinale 
38.Infection de la peau 
39.Septicémie 
40.Leishmaniose 
2. Maladies respiratoires (41-55)
41.Asthme 
42.Bronchiolite 
43.Bronchite chronique 
44.Pneumonie sévère 
45.Allergie respiratoire 
46.Rhinite allergique 
47.Sinusite chronique 
48.Emphysème 
49.Insuffisance respiratoire 
50.Tuberculose pulmonaire 
51.Cancer du poumon 
52.Pleurésie 
53.Œdème pulmonaire 
54.Apnée du sommeil 
55.Laryngite 
3. Maladies digestives (56-75)
56.Gastrite 
57.Ulcère gastrique 
58.Reflux gastro-œsophagien 
59.Appendicite 
60.Hernie abdominale 
61.Constipation chronique 
62.Diarrhée chronique 
63.Hémorroïdes 
64.Cirrhose 
65.Pancréatite 
66.Calculs biliaires 
67.Colite 
68.Péritonite 
69.Occlusion intestinale 
70.Intoxication alimentaire 
71.Malnutrition 
72.Déshydratation sévère 
73.Hépatomégalie 
74.Splénomégalie 
75.Cancer du foie 
4. Maladies cardiovasculaires (76-90)
76.Hypertension artérielle 
77.Insuffisance cardiaque 
78.Crise cardiaque 
79.Accident vasculaire cérébral 
80.Cardiopathie congénitale 
81.Arythmie cardiaque 
82.Tachycardie 
83.Bradycardie 
84.Endocardite 
85.Myocardite 
86.Péricardite 
87.Thrombose 
88.Embolie pulmonaire 
89.Varices 
90.Anévrisme 
5. Maladies neurologiques (91-105)
91.Épilepsie 
92.Migraine 
93.Méningite chronique 
94.Neuropathie 
95.Paralysie faciale 
96.Parkinson 
97.Alzheimer 
98.AVC 
99.Encéphalite 
100.Hydrocéphalie 
101.Névralgie 
102.Traumatisme crânien 
103.Coma 
104.Convulsions fébriles 
105.Tumeur cérébrale 
6. Santé maternelle et reproductive (106-120)
106.Grossesse à risque 
107.Prééclampsie 
108.Éclampsie 
109.Anémie de grossesse 
110.Grossesse extra-utérine 
111.Avortement spontané 
112.Hémorragie obstétricale 
113.Infection post-partum 
114.Travail prématuré 
115.Fistule obstétricale 
116.Infection génitale 
117.Cancer du col de l'utérus 
118.Fibrome utérin 
119.Endométriose 
120.Kyste ovarien 
7. Maladies de l'enfant (121-135)
121.Malnutrition aiguë sévère 
122.Malnutrition modérée 
123.Rougeole infantile 
124.Diarrhée infantile 
125.Pneumonie infantile 
126.Anémie infantile 
127.Déshydratation infantile 
128.Méningite infantile 
129.Convulsions infantiles 
130.Retard de croissance 
131.Faible poids à la naissance 
132.Infection néonatale 
133.Jaunisse du nouveau-né 
134.Asphyxie néonatale 
135.Sepsis néonatal 
8. Maladies endocriniennes et métaboliques (136-145)
136.Diabète 
137.Hypoglycémie 
138.Hyperglycémie 
139.Goitre 
140.Hyperthyroïdie 
141.Hypothyroïdie 
142.Obésité 
143.Syndrome métabolique 
144.Goutte 
145.Carence en vitamine A 
9. Maladies dermatologiques (146-150)
146.Eczéma 
147.Psoriasis 
148.Acné sévère 
149.Dermatite 
150.Albinisme avec complications cutanées




Phase 3: Excellent. Terminons avec les symptômes 176 à 200, ce qui ajoutera les 125 dernières phrases médicales et permettra d'atteindre l'objectif de 1000 phrases médicales en français pour UviraTalk.
Symptôme 176 : Contractions
J'ai des contractions 
Mon ventre se serre régulièrement 
Je ressens des contractions douloureuses 
Mon utérus se contracte 
J'ai des douleurs de travail 
Symptôme 177 : Perte de liquide vaginal
Je perds du liquide vaginal 
Un liquide sort de mon vagin 
J'ai un écoulement important 
Je perds de l'eau 
J'ai une fuite de liquide 
Symptôme 178 : Diminution des mouvements du bébé
Je sens moins bouger mon bébé 
Mon bébé bouge moins que d'habitude 
Les mouvements du bébé diminuent 
Je sens peu mon bébé 
Mon bébé est moins actif 
Symptôme 179 : Pertes vaginales anormales
J'ai des pertes vaginales anormales 
Mes pertes ont changé 
J'ai un écoulement inhabituel 
J'ai des pertes de couleur étrange 
Mes pertes vaginales sont abondantes 
Symptôme 180 : Démangeaisons génitales
J'ai des démangeaisons génitales 
Mes parties intimes me grattent 
J'ai des irritations génitales 
Je ressens des démangeaisons dans la zone intime 
Mes organes génitaux me démangent 
Symptôme 181 : Douleur pendant les rapports sexuels
J'ai mal pendant les rapports sexuels 
Les rapports me font souffrir 
Je ressens une douleur intime pendant les rapports 
Les relations sexuelles sont douloureuses 
J'ai une gêne pendant les rapports 
Symptôme 182 : Grande fatigue
Je suis extrêmement fatigué 
Je n'ai plus d'énergie 
Mon corps est épuisé 
Je suis très faible 
Je me fatigue au moindre effort 
Symptôme 183 : Sueurs nocturnes
Je transpire la nuit 
Je me réveille couvert de sueur 
Je fais des sueurs nocturnes 
Mes vêtements sont mouillés au réveil 
Je transpire beaucoup pendant mon sommeil 
Symptôme 184 : Frissons nocturnes
J'ai des frissons la nuit 
Je tremble pendant la nuit 
Je me réveille avec des frissons 
Mon corps grelotte la nuit 
J'ai froid durant mon sommeil 
Symptôme 185 : Odeur corporelle inhabituelle
Mon corps dégage une odeur inhabituelle 
J'ai une odeur corporelle anormale 
Mon odeur a changé 
Je remarque une mauvaise odeur corporelle 
Mon corps sent différemment 
Symptôme 186 : Faiblesse importante
Je me sens très faible 
Je manque énormément de force 
Mon corps est sans énergie 
Je suis incapable de faire mes activités 
Je me sens épuisé toute la journée 
Symptôme 187 : Difficulté à se lever
Je ne peux plus me lever du lit 
Me lever est très difficile 
Je reste couché à cause de ma faiblesse 
Je manque de force pour me lever 
Mon état m'empêche de sortir du lit 
Symptôme 188 : Aggravation de l'état général
Mon état s'aggrave chaque jour 
Je vais de plus en plus mal 
Mes symptômes augmentent 
Je me sens pire qu'avant 
Ma maladie s'aggrave 
Symptôme 189 : Gonflement du visage
Mon visage est gonflé 
J'ai une enflure du visage 
Mes joues sont gonflées 
Mon visage a augmenté de volume 
J'ai le visage enflé 
Symptôme 190 : Gonflement des mains
Mes mains sont gonflées 
J'ai les mains enflées 
Mes doigts ont grossi 
J'ai une enflure des mains 
Mes mains sont plus grosses que d'habitude 
Symptôme 191 : Gonflement du ventre
Mon ventre est gonflé 
J'ai une enflure abdominale 
Mon abdomen a grossi 
J'ai le ventre anormalement gros 
Mon ventre est tendu 
Symptôme 192 : Palpitations
Mon cœur bat très vite 
J'ai des palpitations 
Je sens mon cœur battre fortement 
Mon cœur s'emballe 
Mes battements sont rapides 
Symptôme 193 : Battements irréguliers du cœur
Mon cœur bat irrégulièrement 
J'ai des battements anormaux 
Mon rythme cardiaque change 
Mon cœur saute des battements 
Je ressens un rythme cardiaque irrégulier 
Symptôme 194 : Essoufflement à l'effort
Je suis essoufflé rapidement 
Je manque d'air en marchant 
L'effort me coupe le souffle 
Je respire difficilement après un petit effort 
Je suis vite à bout de souffle 
Symptôme 195 : Crachat de sang
Je crache du sang 
Du sang sort quand je tousse 
J'ai du sang dans les crachats 
Mes expectorations contiennent du sang 
Je tousse avec du sang 
Symptôme 196 : Sang dans les selles
J'ai du sang dans les selles 
Mes selles contiennent du sang 
Je saigne quand je vais aux toilettes 
Je vois du sang dans mes excréments 
Mes selles sont mélangées à du sang 
Symptôme 197 : Selles noires
Mes selles sont noires 
J'ai des selles très foncées 
Mes excréments sont noirs 
Je remarque des selles noires 
La couleur de mes selles est anormale 
Symptôme 198 : Jaunisse
J'ai la peau jaune 
Mes yeux deviennent jaunes 
Je présente une jaunisse 
Mon corps prend une couleur jaune 
Le blanc de mes yeux est jaune 
Symptôme 199 : Gonflement des ganglions
J'ai des ganglions gonflés 
Je sens des boules sous la peau 
Mes ganglions ont grossi 
J'ai des enflures au cou 
Je ressens des masses sous la peau 
Symptôme 200 : État critique
Je me sens très mal 
Mon état est grave 
J'ai besoin d'aide rapidement 
Je suis dans un état critique 
Je me sens en danger à cause de ma maladie 
Résultat final UviraTalk
✅ 200 symptômes médicaux
✅ 150 maladies fréquentes en RDC
✅ 1000 phrases médicales françaises (200 symptômes × 5 formulations)

Phase 4 : Questions-réponses médicales
Parfait. Continuons avec les questions-réponses sur la diarrhée, un problème très fréquent à Uvira.
Série 3 : Diarrhée (Q31 à Q50)
Q31
Question : J'ai la diarrhée, que faire ?
Réponse : Buvez beaucoup d'eau ou une solution de réhydratation orale pour éviter la déshydratation.
Q32
Question : Pourquoi ai-je la diarrhée ?
Réponse : Elle peut être causée par une infection, de l'eau contaminée ou des aliments avariés.
Q33
Question : La diarrhée est-elle dangereuse ?
Réponse : Oui, surtout chez les jeunes enfants, les personnes âgées et les femmes enceintes.
Q34
Question : Quand dois-je consulter pour une diarrhée ?
Réponse : Consultez rapidement si elle dure plusieurs jours ou s'accompagne de sang dans les selles.
Q35
Question : Que dois-je boire quand j'ai la diarrhée ?
Réponse : De l'eau potable, une solution de réhydratation orale ou des liquides propres.
Q36
Question : Puis-je manger avec la diarrhée ?
Réponse : Oui, mangez des aliments légers et faciles à digérer.
Q37
Question : La diarrhée peut-elle provoquer une déshydratation ?
Réponse : Oui, c'est l'une des principales complications.
Q38
Question : Mon enfant a la diarrhée, que faire ?
Réponse : Donnez-lui davantage de liquides et consultez rapidement s'il devient faible.
Q39
Question : Une diarrhée avec vomissements est-elle grave ?
Réponse : Elle peut entraîner une déshydratation rapide et nécessite une surveillance.
Q40
Question : La diarrhée peut-elle être causée par une eau sale ?
Réponse : Oui, l'eau contaminée est une cause fréquente.
Q41
Question : Combien de fois peut-on aller aux toilettes avec une diarrhée ?
Réponse : Cela varie, mais des selles liquides répétées sont caractéristiques.
Q42
Question : Puis-je continuer à travailler avec une diarrhée ?
Réponse : Il est préférable de se reposer et de bien s'hydrater.
Q43
Question : La diarrhée est-elle contagieuse ?
Réponse : Certaines formes causées par des infections peuvent être contagieuses.
Q44
Question : Dois-je consulter si j'ai du sang dans les selles ?
Réponse : Oui, cela nécessite une évaluation médicale rapide.
Q45
Question : La diarrhée peut-elle être un signe de choléra ?
Réponse : Oui, surtout si elle est abondante et aqueuse.
Q46
Question : Une femme enceinte avec diarrhée doit-elle consulter ?
Réponse : Oui, particulièrement si elle présente des signes de déshydratation.
Q47
Question : Comment prévenir la diarrhée ?
Réponse : En se lavant les mains et en consommant de l'eau potable.
Q48
Question : Pourquoi ai-je des douleurs abdominales avec la diarrhée ?
Réponse : Les infections intestinales provoquent souvent des crampes abdominales.
Q49
Question : Puis-je avoir de la fièvre avec la diarrhée ?
Réponse : Oui, certaines infections digestives provoquent aussi de la fièvre.
Q50
Question : Quels sont les signes de déshydratation ?
Réponse : Grande soif, bouche sèche, faiblesse, yeux enfoncés et diminution des urines.

Série 4 : Paludisme (Q51 à Q70)
Q51
Question : Qu'est-ce que le paludisme ?
Réponse : Le paludisme est une maladie transmise par la piqûre d'un moustique infecté.
Q52
Question : Quels sont les signes du paludisme ?
Réponse : Fièvre, frissons, maux de tête, fatigue et douleurs musculaires.
Q53
Question : Le paludisme est-il fréquent en RDC ?
Réponse : Oui, c'est l'une des maladies les plus fréquentes.
Q54
Question : Puis-je avoir le paludisme sans forte fièvre ?
Réponse : Oui, certains cas commencent avec des symptômes modérés.
Q55
Question : Comment attrape-t-on le paludisme ?
Réponse : Principalement par la piqûre d'un moustique anophèle infecté.
Q56
Question : Comment prévenir le paludisme ?
Réponse : Dormez sous une moustiquaire imprégnée et éliminez les eaux stagnantes.
Q57
Question : Le paludisme peut-il tuer ?
Réponse : Oui, surtout s'il n'est pas traité rapidement.
Q58
Question : Une femme enceinte est-elle plus à risque ?
Réponse : Oui, le paludisme est particulièrement dangereux pendant la grossesse.
Q59
Question : Mon enfant a de la fièvre, est-ce le paludisme ?
Réponse : C'est possible, mais seul un test peut confirmer le diagnostic.
Q60
Question : Pourquoi ai-je des frissons ?
Réponse : Les frissons sont un symptôme fréquent du paludisme.
Q61
Question : Dois-je faire un test de paludisme ?
Réponse : Oui, en cas de suspicion, un test rapide ou un examen de laboratoire est recommandé.
Q62
Question : Puis-je avoir des vomissements avec le paludisme ?
Réponse : Oui, cela peut arriver.
Q63
Question : Le paludisme provoque-t-il des maux de tête ?
Réponse : Oui, c'est un symptôme très fréquent.
Q64
Question : Pourquoi suis-je très faible ?
Réponse : Le paludisme peut provoquer une grande fatigue.
Q65
Question : Le paludisme touche-t-il les enfants ?
Réponse : Oui, les enfants sont parmi les plus vulnérables.
Q66
Question : Puis-je avoir la diarrhée avec le paludisme ?
Réponse : Oui, certains patients présentent aussi des troubles digestifs.
Q67
Question : Quels sont les signes graves du paludisme ?
Réponse : Convulsions, perte de connaissance, difficultés respiratoires ou incapacité à boire.
Q68
Question : Dois-je consulter rapidement pour un paludisme ?
Réponse : Oui, surtout si les symptômes sont importants.
Q69
Question : Puis-je éviter le paludisme ?
Réponse : Le risque peut être fortement réduit grâce à la prévention.
Q70
Question : Quand le paludisme devient-il une urgence ?
Réponse : Lorsqu'il provoque des signes graves ou une détérioration rapide de l'état général.

✅ Total actuel : 70 questions-réponses médicales
Fièvre : 20 
Toux : 20 
Diarrhée : 20 
Paludisme : 20 
Total : 80 Q/R (en comptant les 20 sur la toux complètes dans votre base) 
La prochaine étape recommandée est :
Grossesse (20 Q/R) puis Douleur abdominale (20 Q/R), deux thèmes très importants pour la santé communautaire à Uvira.
Parfait. Continuons avec Méningite (Q491 à Q510). C'est une maladie importante en Afrique centrale et utile pour UviraTalk.
Série 26 : Méningite (Q491 à Q510)
Q491
Question : Qu'est-ce que la méningite ?
Réponse : La méningite est une infection ou une inflammation des membranes qui entourent le cerveau et la moelle épinière.
Q492
Question : Quels sont les signes de la méningite ?
Réponse : Forte fièvre, mal de tête intense, raideur du cou et vomissements.
Q493
Question : Pourquoi ai-je très mal à la tête avec de la fièvre ?
Réponse : Cela peut être causé par plusieurs maladies, dont la méningite.
Q494
Question : Qu'est-ce qu'une raideur de la nuque ?
Réponse : C'est une difficulté ou une douleur lorsqu'on essaie de plier le cou vers l'avant.
Q495
Question : La méningite est-elle dangereuse ?
Réponse : Oui, elle nécessite une prise en charge rapide.
Q496
Question : Les enfants peuvent-ils avoir une méningite ?
Réponse : Oui, particulièrement les nourrissons et les jeunes enfants.
Q497
Question : Une personne atteinte de méningite peut-elle convulser ?
Réponse : Oui, cela peut arriver dans certains cas.
Q498
Question : Pourquoi la lumière me gêne-t-elle ?
Réponse : Une sensibilité à la lumière peut être observée dans certaines formes de méningite.
Q499
Question : Puis-je avoir des vomissements avec une méningite ?
Réponse : Oui.
Q500
Question : La méningite est-elle contagieuse ?
Réponse : Certaines formes peuvent se transmettre d'une personne à une autre.
Q501
Question : Comment savoir si j'ai une méningite ?
Réponse : Un examen médical est nécessaire pour confirmer le diagnostic.
Q502
Question : Une femme enceinte peut-elle avoir une méningite ?
Réponse : Oui.
Q503
Question : Pourquoi mon enfant pleure-t-il sans arrêt avec de la fièvre ?
Réponse : Certaines infections graves peuvent provoquer ce comportement.
Q504
Question : Dois-je consulter rapidement en cas de forte fièvre et raideur du cou ?
Réponse : Oui, c'est une urgence médicale.
Q505
Question : Peut-on guérir de la méningite ?
Réponse : Oui, surtout si elle est prise en charge rapidement.
Q506
Question : La méningite peut-elle laisser des séquelles ?
Réponse : Oui, dans certains cas.
Q507
Question : Existe-t-il des vaccins contre certaines méningites ?
Réponse : Oui.
Q508
Question : Pourquoi suis-je confus ou désorienté ?
Réponse : Cela peut être un signe d'atteinte grave nécessitant une consultation urgente.
Q509
Question : Quels signes sont une urgence absolue ?
Réponse : Convulsions, perte de connaissance, forte fièvre avec raideur du cou ou difficulté respiratoire.
Q510
Question : Comment prévenir certaines méningites ?
Réponse : Grâce à la vaccination, l'hygiène et une prise en charge précoce des infections.

Série 27 : Ulcère gastrique (Q511 à Q530)
Q511
Question : Qu'est-ce qu'un ulcère gastrique ?
Réponse : C'est une plaie qui se forme dans l'estomac ou le début de l'intestin.
Q512
Question : Quels sont les signes d'un ulcère ?
Réponse : Douleur ou brûlure à l'estomac, nausées et parfois vomissements.
Q513
Question : Pourquoi ai-je une brûlure dans l'estomac ?
Réponse : Cela peut être lié à un ulcère ou à d'autres problèmes digestifs.
Q514
Question : La douleur d'un ulcère apparaît-elle après les repas ?
Réponse : Cela peut arriver chez certaines personnes.
Q515
Question : L'ulcère est-il dangereux ?
Réponse : Oui, surtout en cas de complications.
Q516
Question : Puis-je avoir des nausées avec un ulcère ?
Réponse : Oui.
Q517
Question : Pourquoi ai-je souvent mal au haut du ventre ?
Réponse : Plusieurs causes sont possibles, dont l'ulcère.
Q518
Question : Le stress peut-il aggraver les douleurs d'estomac ?
Réponse : Oui, chez certaines personnes.
Q519
Question : Puis-je perdre l'appétit avec un ulcère ?
Réponse : Oui.
Q520
Question : Dois-je consulter si la douleur revient souvent ?
Réponse : Oui.
Q521
Question : Pourquoi ai-je mal la nuit à l'estomac ?
Réponse : Certaines douleurs d'ulcère peuvent survenir la nuit.
Q522
Question : Puis-je vomir du sang avec un ulcère ?
Réponse : Oui, c'est une urgence médicale.
Q523
Question : Des selles noires sont-elles inquiétantes ?
Réponse : Oui, elles peuvent signaler un saignement digestif.
Q524
Question : Comment savoir si j'ai un ulcère ?
Réponse : Une évaluation médicale est nécessaire.
Q525
Question : Peut-on traiter un ulcère ?
Réponse : Oui.
Q526
Question : Dois-je éviter certains aliments ?
Réponse : Certains aliments peuvent aggraver les symptômes chez certaines personnes.
Q527
Question : L'ulcère peut-il revenir ?
Réponse : Oui.
Q528
Question : Pourquoi suivre correctement le traitement ?
Réponse : Pour favoriser la guérison et éviter les complications.
Q529
Question : Quand consulter rapidement ?
Réponse : En cas de vomissements sanglants ou de selles noires.
Q530
Question : Peut-on prévenir certains ulcères ?
Réponse : Oui, en suivant les conseils médicaux et en évitant certains facteurs de risque.

Série 28 : COVID-19 (Q531 à Q550)
Q531
Question : Qu'est-ce que la COVID-19 ?
Réponse : La COVID-19 est une maladie infectieuse causée par un coronavirus.
Q532
Question : Quels sont les signes de la COVID-19 ?
Réponse : Fièvre, toux, fatigue, mal de gorge et difficultés respiratoires peuvent survenir.
Q533
Question : Puis-je perdre l'odorat ou le goût ?
Réponse : Oui, cela peut arriver.
Q534
Question : Comment se transmet la COVID-19 ?
Réponse : Principalement par les gouttelettes respiratoires et les contacts rapprochés.
Q535
Question : La COVID-19 est-elle encore présente ?
Réponse : Oui, elle continue de circuler dans plusieurs régions du monde.
Q536
Question : Dois-je consulter si j'ai des difficultés respiratoires ?
Réponse : Oui.
Q537
Question : Les personnes âgées sont-elles plus à risque ?
Réponse : Oui.
Q538
Question : Une femme enceinte peut-elle avoir la COVID-19 ?
Réponse : Oui.
Q539
Question : Les enfants peuvent-ils être infectés ?
Réponse : Oui.
Q540
Question : Pourquoi suis-je très fatigué ?
Réponse : La fatigue est un symptôme fréquent de nombreuses infections, y compris la COVID-19.
Q541
Question : La vaccination contre la COVID-19 existe-t-elle ?
Réponse : Oui.
Q542
Question : Dois-je rester à la maison si je suis malade ?
Réponse : Il est conseillé de limiter les contacts avec les autres personnes.
Q543
Question : Puis-je avoir une COVID-19 sans symptômes ?
Réponse : Oui.
Q544
Question : Pourquoi ai-je mal à la gorge ?
Réponse : Cela peut être un symptôme de plusieurs infections, y compris la COVID-19.
Q545
Question : Quand consulter rapidement ?
Réponse : En cas de difficultés respiratoires ou d'aggravation importante.
Q546
Question : Comment réduire le risque de transmission ?
Réponse : En respectant les mesures d'hygiène recommandées.
Q547
Question : Puis-je avoir de la fièvre pendant plusieurs jours ?
Réponse : Oui, cela peut arriver.
Q548
Question : Pourquoi ai-je des douleurs musculaires ?
Réponse : Certaines infections virales peuvent provoquer ces douleurs.
Q549
Question : Peut-on guérir de la COVID-19 ?
Réponse : Oui, la majorité des personnes guérissent.
Q550
Question : Quels signes sont une urgence ?
Réponse : Difficultés respiratoires sévères, confusion ou perte de connaissance.

✅ Base UviraTalk : 550 questions-réponses médicales
Nous avons maintenant dépassé la moitié de l'objectif de 1000 Q/R médicales.
Prochaine série recommandée :
Santé mentale (20) 
Dépression (20) 
Anxiété (20) 
Accidents et traumatismes (20) 
Brûlures (20) 
➡️ Cela nous permettra d'atteindre rapidement 650 Q/R médicales.
Parfait. Continuons avec Vaccination (Q851 à Q870), Planification familiale (Q871 à Q890) et VIH/SIDA (Q891 à Q910).
Série 44 : Vaccination (Q851 à Q870)
Q851
Question : Qu'est-ce qu'un vaccin ?
Réponse : Un vaccin aide le corps à se protéger contre certaines maladies.
Q852
Question : Pourquoi faut-il vacciner les enfants ?
Réponse : Pour prévenir certaines maladies graves.
Q853
Question : Les vaccins sont-ils importants ?
Réponse : Oui.
Q854
Question : Un enfant peut-il tomber malade s'il n'est pas vacciné ?
Réponse : Oui, il risque davantage certaines maladies.
Q855
Question : Pourquoi suivre le calendrier vaccinal ?
Réponse : Pour assurer une protection au bon moment.
Q856
Question : Les vaccins sont-ils réservés aux enfants ?
Réponse : Non, certains vaccins concernent aussi les adultes.
Q857
Question : Mon enfant a de la fièvre après un vaccin, est-ce normal ?
Réponse : Une légère fièvre peut parfois survenir.
Q858
Question : Pourquoi conserver le carnet de vaccination ?
Réponse : Pour suivre les vaccins déjà reçus.
Q859
Question : Une femme enceinte peut-elle recevoir certains vaccins ?
Réponse : Oui, selon les recommandations médicales.
Q860
Question : Les vaccins empêchent-ils toutes les maladies ?
Réponse : Non, mais ils protègent contre certaines maladies importantes.
Q861
Question : Puis-je rattraper des vaccins manqués ?
Réponse : Oui, après avis d'un professionnel de santé.
Q862
Question : Pourquoi les campagnes de vaccination sont-elles organisées ?
Réponse : Pour protéger la population contre certaines maladies.
Q863
Question : Les vaccins sauvent-ils des vies ?
Réponse : Oui.
Q864
Question : Dois-je vacciner mon nouveau-né ?
Réponse : Oui, selon le calendrier recommandé.
Q865
Question : Pourquoi certains vaccins nécessitent-ils plusieurs doses ?
Réponse : Pour renforcer la protection.
Q866
Question : Les vaccins sont-ils testés avant leur utilisation ?
Réponse : Oui.
Q867
Question : Puis-je recevoir un vaccin en étant malade ?
Réponse : Cela dépend de la situation et doit être évalué par un professionnel de santé.
Q868
Question : Pourquoi la vaccination protège-t-elle la communauté ?
Réponse : Elle réduit la circulation de certaines maladies.
Q869
Question : Quand consulter après une vaccination ?
Réponse : Si des symptômes importants apparaissent.
Q870
Question : La vaccination est-elle un moyen de prévention ?
Réponse : Oui.

Série 45 : Planification familiale (Q871 à Q890)
Q871
Question : Qu'est-ce que la planification familiale ?
Réponse : C'est l'ensemble des moyens permettant de planifier les grossesses.
Q872
Question : Pourquoi la planification familiale est-elle importante ?
Réponse : Elle aide les familles à prendre des décisions concernant les naissances.
Q873
Question : Puis-je obtenir des conseils en planification familiale ?
Réponse : Oui, auprès d'un professionnel de santé.
Q874
Question : La planification familiale concerne-t-elle seulement les femmes ?
Réponse : Non, les hommes ont également un rôle important.
Q875
Question : Pourquoi espacer les grossesses ?
Réponse : Cela peut contribuer à la santé de la mère et de l'enfant.
Q876
Question : Existe-t-il plusieurs méthodes de planification familiale ?
Réponse : Oui.
Q877
Question : Puis-je choisir la méthode qui me convient ?
Réponse : Oui, avec les conseils d'un professionnel de santé.
Q878
Question : Les adolescents peuvent-ils recevoir des informations sur la santé reproductive ?
Réponse : Oui.
Q879
Question : Pourquoi consulter avant de choisir une méthode ?
Réponse : Pour recevoir des informations adaptées à sa situation.
Q880
Question : La planification familiale protège-t-elle contre toutes les IST ?
Réponse : Certaines méthodes ne protègent pas contre les IST.
Q881
Question : Puis-je arrêter une méthode contraceptive ?
Réponse : Oui, après discussion avec un professionnel de santé.
Q882
Question : Pourquoi mon cycle menstruel a-t-il changé ?
Réponse : Plusieurs causes sont possibles, y compris certaines méthodes contraceptives.
Q883
Question : Une femme qui allaite peut-elle recevoir des conseils de planification familiale ?
Réponse : Oui.
Q884
Question : Quand puis-je reprendre une méthode après un accouchement ?
Réponse : Selon les recommandations du personnel de santé.
Q885
Question : Les services de planification familiale sont-ils confidentiels ?
Réponse : Oui.
Q886
Question : Pourquoi discuter avec son partenaire ?
Réponse : Pour prendre des décisions éclairées ensemble.
Q887
Question : Puis-je changer de méthode ?
Réponse : Oui.
Q888
Question : Où puis-je obtenir des informations fiables ?
Réponse : Dans les centres de santé et auprès des professionnels qualifiés.
Q889
Question : Quand consulter ?
Réponse : Pour toute question ou difficulté liée à une méthode utilisée.
Q890
Question : La planification familiale contribue-t-elle à la santé familiale ?
Réponse : Oui.

Série 46 : VIH/SIDA (Q891 à Q910)
Q891
Question : Qu'est-ce que le VIH ?
Réponse : Le VIH est un virus qui attaque le système immunitaire.
Q892
Question : Qu'est-ce que le SIDA ?
Réponse : Le SIDA est le stade avancé de l'infection par le VIH.
Q893
Question : Comment se transmet le VIH ?
Réponse : Par certaines expositions au sang, aux rapports sexuels non protégés et de la mère à l'enfant.
Q894
Question : Puis-je avoir le VIH sans le savoir ?
Réponse : Oui.
Q895
Question : Pourquoi faire un test de dépistage ?
Réponse : Pour connaître son statut et recevoir une prise en charge adaptée.
Q896
Question : Le VIH se transmet-il par une poignée de main ?
Réponse : Non.
Q897
Question : Le VIH se transmet-il par le partage des repas ?
Réponse : Non.
Q898
Question : Une personne vivant avec le VIH peut-elle avoir une vie normale ?
Réponse : Oui, avec un suivi médical adapté.
Q899
Question : Existe-t-il un traitement contre le VIH ?
Réponse : Oui.
Q900
Question : Pourquoi faut-il prendre le traitement régulièrement ?
Réponse : Pour contrôler le virus et protéger la santé.
Q901
Question : Une femme enceinte vivant avec le VIH peut-elle avoir un enfant non infecté ?
Réponse : Oui, avec une prise en charge appropriée.
Q902
Question : Les enfants peuvent-ils être infectés par le VIH ?
Réponse : Oui.
Q903
Question : Pourquoi certaines personnes maigrissent-elles avec le VIH ?
Réponse : Cela peut être lié à la maladie ou à des infections associées.
Q904
Question : Le VIH est-il une malédiction ?
Réponse : Non, c'est une maladie causée par un virus.
Q905
Question : Puis-je travailler si je vis avec le VIH ?
Réponse : Oui.
Q906
Question : Pourquoi lutter contre la stigmatisation ?
Réponse : Parce que toute personne mérite le respect et l'accès aux soins.
Q907
Question : Le dépistage est-il confidentiel ?
Réponse : Oui.
Q908
Question : Comment prévenir le VIH ?
Réponse : En appliquant les mesures de prévention recommandées par les professionnels de santé.
Q909
Question : Quand faut-il consulter ?
Réponse : Pour le dépistage, le suivi ou en cas de symptômes inquiétants.
Q910
Question : Peut-on vivre longtemps avec le VIH ?
Réponse : Oui, grâce aux traitements modernes et au suivi médical.

✅ Base UviraTalk : 910 questions-réponses médicales
Nouveaux thèmes ajoutés :
Vaccination (20) 
Planification familiale (20) 
VIH/SIDA (20) 
Total actuel : 910 Q/R médicales.
Il reste 90 Q/R pour atteindre l'objectif de 1000 questions-réponses médicales.
Prochains thèmes recommandés :
Premiers secours communautaires (20) 
Santé des adolescents (20) 
Santé des personnes âgées (20) 
Eau, hygiène et assainissement (20) 
Santé environnementale (20) 
Après ces 5 séries, vous atteindrez exactement 1010 questions-réponses médicales, une base très solide pour l'entraînement initial de l'assistant médical communautaire UviraTalk.

Parfait. Continuons avec Premiers secours communautaires (Q911 à Q930).
Série 47 : Premiers secours communautaires (Q911 à Q930)
Q911
Question : Qu'est-ce que les premiers secours ?
Réponse : Ce sont les premiers gestes apportés à une personne malade ou blessée avant l'arrivée des soins médicaux.
Q912
Question : Que faire si une personne s'évanouit ?
Réponse : Vérifiez sa respiration et demandez rapidement de l'aide médicale.
Q913
Question : Que faire en cas de saignement important ?
Réponse : Appliquez une pression sur la plaie avec un tissu propre.
Q914
Question : Que faire si une personne ne respire plus ?
Réponse : Appelez immédiatement les secours ou transportez-la rapidement vers une structure de santé.
Q915
Question : Que faire en cas de brûlure ?
Réponse : Refroidissez la zone avec de l'eau propre à température ambiante.
Q916
Question : Que faire après une morsure de serpent ?
Réponse : Gardez la personne calme et conduisez-la rapidement au centre de santé.
Q917
Question : Que faire en cas de fracture suspectée ?
Réponse : Immobilisez le membre atteint et consultez rapidement.
Q918
Question : Une personne inconsciente doit-elle être surveillée ?
Réponse : Oui.
Q919
Question : Que faire si un enfant convulse ?
Réponse : Éloignez les objets dangereux et cherchez immédiatement une aide médicale.
Q920
Question : Puis-je donner à boire à une personne inconsciente ?
Réponse : Non.
Q921
Question : Que faire en cas d'étouffement ?
Réponse : Cherchez immédiatement de l'aide et appliquez les gestes de secours appropriés si vous les connaissez.
Q922
Question : Pourquoi garder son calme lors d'une urgence ?
Réponse : Cela permet d'agir plus efficacement.
Q923
Question : Dois-je déplacer une personne blessée ?
Réponse : Seulement si elle est exposée à un danger immédiat.
Q924
Question : Que faire si une personne a une forte fièvre ?
Réponse : Surveillez-la et consultez si les symptômes sont importants ou persistants.
Q925
Question : Que faire en cas de noyade ?
Réponse : Sortez la personne de l'eau en sécurité et demandez immédiatement de l'aide médicale.
Q926
Question : Pourquoi faut-il avoir une trousse de premiers secours ?
Réponse : Pour pouvoir réagir rapidement aux urgences courantes.
Q927
Question : Quels éléments doivent être dans une trousse de secours ?
Réponse : Compresses, bandages, gants propres et matériel de base recommandé.
Q928
Question : Quand appeler de l'aide ?
Réponse : Dès qu'une situation semble grave ou menaçante.
Q929
Question : Les premiers secours remplacent-ils l'hôpital ?
Réponse : Non.
Q930
Question : Pourquoi apprendre les premiers secours ?
Réponse : Pour pouvoir aider rapidement en cas d'urgence.

Série 48 : Santé des adolescents (Q931 à Q950)
Q931
Question : Qui est un adolescent ?
Réponse : Une personne en période de transition entre l'enfance et l'âge adulte.
Q932
Question : Pourquoi mon corps change-t-il ?
Réponse : Les changements physiques font partie de la croissance normale.
Q933
Question : Qu'est-ce que la puberté ?
Réponse : C'est la période où le corps devient progressivement capable de se reproduire.
Q934
Question : Pourquoi ai-je plus d'acné ?
Réponse : L'acné est fréquente pendant l'adolescence.
Q935
Question : Les adolescents ont-ils besoin d'une alimentation équilibrée ?
Réponse : Oui.
Q936
Question : Pourquoi suis-je souvent fatigué ?
Réponse : La croissance, le sommeil insuffisant ou certaines maladies peuvent en être la cause.
Q937
Question : Pourquoi ai-je des sautes d'humeur ?
Réponse : Les changements hormonaux peuvent y contribuer.
Q938
Question : Est-il important de faire du sport ?
Réponse : Oui.
Q939
Question : Pourquoi dormir suffisamment ?
Réponse : Le sommeil est essentiel pour la croissance et la santé.
Q940
Question : Les adolescents peuvent-ils souffrir de stress ?
Réponse : Oui.
Q941
Question : Pourquoi parler de santé reproductive ?
Réponse : Pour mieux comprendre son corps et protéger sa santé.
Q942
Question : Puis-je consulter seul un professionnel de santé ?
Réponse : Selon les règles et les situations locales.
Q943
Question : Pourquoi éviter l'alcool et les drogues ?
Réponse : Ils peuvent nuire à la santé et au développement.
Q944
Question : L'hygiène personnelle est-elle importante ?
Réponse : Oui.
Q945
Question : Pourquoi me sens-je parfois triste ou inquiet ?
Réponse : Les émotions varient pendant l'adolescence, mais une souffrance persistante mérite une attention.
Q946
Question : Les adolescents doivent-ils être vaccinés ?
Réponse : Oui, selon les recommandations de santé.
Q947
Question : Pourquoi respecter les visites médicales ?
Réponse : Pour surveiller la santé et le développement.
Q948
Question : Quand consulter un professionnel de santé ?
Réponse : En cas de problème physique ou émotionnel préoccupant.
Q949
Question : Comment rester en bonne santé ?
Réponse : Avec une bonne alimentation, l'activité physique et un sommeil suffisant.
Q950
Question : La santé mentale est-elle importante chez les adolescents ?
Réponse : Oui.

Série 49 : Santé des personnes âgées (Q951 à Q970)
Q951
Question : Pourquoi la santé change-t-elle avec l'âge ?
Réponse : Le vieillissement entraîne des changements naturels dans l'organisme.
Q952
Question : Les personnes âgées doivent-elles consulter régulièrement ?
Réponse : Oui.
Q953
Question : Pourquoi ai-je des douleurs articulaires ?
Réponse : Elles peuvent être liées à l'âge ou à certaines maladies.
Q954
Question : Pourquoi ma vue diminue-t-elle ?
Réponse : Certaines maladies et le vieillissement peuvent affecter la vision.
Q955
Question : Pourquoi j'entends moins bien ?
Réponse : La perte auditive peut augmenter avec l'âge.
Q956
Question : Les personnes âgées ont-elles besoin d'une alimentation adaptée ?
Réponse : Oui.
Q957
Question : Pourquoi est-il important de rester actif ?
Réponse : L'activité physique aide à maintenir la santé et l'autonomie.
Q958
Question : Les chutes sont-elles dangereuses ?
Réponse : Oui.
Q959
Question : Comment prévenir les chutes ?
Réponse : En sécurisant l'environnement et en restant actif.
Q960
Question : Pourquoi surveiller sa tension artérielle ?
Réponse : Pour détecter certaines maladies cardiovasculaires.
Q961
Question : Pourquoi surveiller sa glycémie ?
Réponse : Pour détecter ou suivre un diabète.
Q962
Question : Les troubles de mémoire sont-ils fréquents ?
Réponse : Ils peuvent apparaître avec l'âge.
Q963
Question : Quand consulter pour des pertes de mémoire ?
Réponse : Lorsqu'elles deviennent importantes ou inhabituelles.
Q964
Question : Pourquoi boire suffisamment d'eau ?
Réponse : Pour maintenir une bonne hydratation.
Q965
Question : Les vaccins sont-ils utiles chez les personnes âgées ?
Réponse : Oui.
Q966
Question : Pourquoi surveiller son poids ?
Réponse : Une perte ou un gain important peut signaler un problème de santé.
Q967
Question : Les personnes âgées peuvent-elles souffrir de dépression ?
Réponse : Oui.
Q968
Question : Pourquoi maintenir les liens sociaux ?
Réponse : Ils contribuent au bien-être général.
Q969
Question : Quand consulter rapidement ?
Réponse : En cas de chute grave, confusion soudaine ou difficulté respiratoire.
Q970
Question : Peut-on vieillir en bonne santé ?
Réponse : Oui, avec une bonne hygiène de vie et un suivi médical.

✅ Base UviraTalk : 970 questions-réponses médicales
Nous sommes maintenant à 970 Q/R.
Il reste seulement 30 Q/R pour dépasser l'objectif de 1000 Q/R médicales. La prochaine série couvrira :
Eau, hygiène et assainissement (20) 
Santé environnementale (20) 
Ce qui permettra d'atteindre 1010 Q/R médicales, une base très robuste pour l'entraînement initial d'UviraTalk.
Continuons
Parfait. Terminons la base initiale avec les 30 dernières questions-réponses.
Série 50 : Eau, Hygiène et Assainissement (Q971 à Q990)
Q971
Question : Pourquoi faut-il boire de l'eau potable ?
Réponse : Pour réduire le risque de maladies transmises par l'eau contaminée.
Q972
Question : Comment rendre l'eau plus sûre à boire ?
Réponse : En utilisant les méthodes recommandées localement, comme l'ébullition ou d'autres traitements appropriés.
Q973
Question : Pourquoi faut-il se laver les mains ?
Réponse : Pour réduire la transmission des microbes.
Q974
Question : Quand faut-il se laver les mains ?
Réponse : Avant de manger, avant de préparer les aliments et après être allé aux toilettes.
Q975
Question : Pourquoi utiliser des toilettes propres ?
Réponse : Pour prévenir la propagation des maladies.
Q976
Question : Les enfants doivent-ils se laver les mains ?
Réponse : Oui.
Q977
Question : Pourquoi couvrir les aliments ?
Réponse : Pour les protéger contre les insectes et les contaminations.
Q978
Question : Une eau sale peut-elle provoquer la diarrhée ?
Réponse : Oui.
Q979
Question : Pourquoi nettoyer régulièrement la maison ?
Réponse : Pour réduire certains risques sanitaires.
Q980
Question : Comment éliminer correctement les déchets ?
Réponse : Selon les méthodes recommandées par la communauté ou les autorités locales.
Q981
Question : Pourquoi éviter les eaux stagnantes ?
Réponse : Elles favorisent la prolifération des moustiques.
Q982
Question : Les mouches peuvent-elles transmettre des maladies ?
Réponse : Oui.
Q983
Question : Pourquoi protéger les sources d'eau ?
Réponse : Pour éviter leur contamination.
Q984
Question : Dois-je laver les fruits et légumes ?
Réponse : Oui.
Q985
Question : Pourquoi garder les ustensiles propres ?
Réponse : Pour réduire les risques de contamination alimentaire.
Q986
Question : Une mauvaise hygiène peut-elle favoriser les maladies ?
Réponse : Oui.
Q987
Question : Pourquoi sensibiliser les enfants à l'hygiène ?
Réponse : Pour développer de bonnes habitudes de santé.
Q988
Question : Comment prévenir le choléra ?
Réponse : En utilisant de l'eau potable et en respectant les règles d'hygiène.
Q989
Question : Pourquoi l'assainissement est-il important ?
Réponse : Il contribue à protéger la santé de la communauté.
Q990
Question : L'hygiène est-elle une forme de prévention ?
Réponse : Oui.

Série 51 : Santé environnementale (Q991 à Q1010)
Q991
Question : Qu'est-ce que la santé environnementale ?
Réponse : Elle étudie l'influence de l'environnement sur la santé humaine.
Q992
Question : Pourquoi un environnement propre est-il important ?
Réponse : Il réduit les risques de certaines maladies.
Q993
Question : La pollution peut-elle affecter la santé ?
Réponse : Oui.
Q994
Question : Pourquoi éviter la fumée dans les habitations ?
Réponse : Elle peut provoquer ou aggraver des problèmes respiratoires.
Q995
Question : Les déchets abandonnés peuvent-ils favoriser les maladies ?
Réponse : Oui.
Q996
Question : Pourquoi planter des arbres ?
Réponse : Ils contribuent à un environnement plus sain.
Q997
Question : Les moustiques sont-ils liés à l'environnement ?
Réponse : Oui, ils se développent dans certains milieux favorables.
Q998
Question : Pourquoi protéger les rivières et les sources ?
Réponse : Pour préserver la qualité de l'eau.
Q999
Question : Les fumées de cuisson peuvent-elles être dangereuses ?
Réponse : Oui, surtout dans les espaces mal ventilés.
Q1000
Question : Pourquoi aérer les maisons ?
Réponse : Pour améliorer la qualité de l'air intérieur.
Q1001
Question : Le changement climatique influence-t-il la santé ?
Réponse : Oui.
Q1002
Question : Pourquoi lutter contre les eaux stagnantes ?
Réponse : Pour réduire la prolifération des moustiques.
Q1003
Question : Les catastrophes naturelles peuvent-elles affecter la santé ?
Réponse : Oui.
Q1004
Question : Pourquoi protéger les zones de captage d'eau ?
Réponse : Pour maintenir une eau de meilleure qualité.
Q1005
Question : Comment réduire la pollution domestique ?
Réponse : En améliorant l'hygiène et la gestion des déchets.
Q1006
Question : Pourquoi éviter de brûler les déchets près des habitations ?
Réponse : La fumée peut être nocive pour la santé.
Q1007
Question : Les animaux peuvent-ils transmettre certaines maladies ?
Réponse : Oui.
Q1008
Question : Pourquoi protéger l'environnement ?
Réponse : Parce qu'il influence directement la santé humaine.
Q1009
Question : La participation communautaire est-elle importante ?
Réponse : Oui, pour améliorer durablement la santé publique.
Q1010
Question : La santé environnementale contribue-t-elle au bien-être général ?
Réponse : Oui.
Entrainement dialogues
Catégorie 1 : PALUDISME (Dialogue 1 à 10 sur 100)
Dialogue P001
Patient :
J'ai de la fièvre.
Mots-clés :
fièvre 
UviraTalk :
Depuis combien de temps avez-vous la fièvre ?

Dialogue P002
Patient :
Mon corps est très chaud.
Mots-clés :
corps chaud 
chaleur 
Symptôme détecté :
Fièvre 
UviraTalk :
Avez-vous également des frissons ou des maux de tête ?

Dialogue P003
Patient :
J'ai froid puis après j'ai chaud.
Mots-clés :
froid 
chaud 
Symptômes :
Frissons 
Fièvre 
UviraTalk :
Depuis combien de jours ressentez-vous cela ?

Dialogue P004
Patient :
J'ai beaucoup mal à la tête.
Mots-clés :
mal à la tête 
Symptômes :
Céphalée 
UviraTalk :
Avez-vous aussi de la fièvre ?

Dialogue P005
Patient :
Je vomis depuis hier.
Mots-clés :
vomis 
Symptômes :
Vomissements 
UviraTalk :
Avez-vous de la fièvre ou des frissons ?

Dialogue P006
Patient :
Je suis très faible.
Mots-clés :
faible 
Symptômes :
Fatigue 
Asthénie 
UviraTalk :
Avez-vous de la fièvre ou des douleurs dans le corps ?

Dialogue P007
Patient :
J'ai mal dans tout le corps.
Mots-clés :
mal partout 
douleur corps 
Symptômes :
Douleurs musculaires 
UviraTalk :
Avez-vous également de la fièvre ?

Dialogue P008
Patient :
Je transpire beaucoup la nuit.
Mots-clés :
transpire 
nuit 
Symptômes :
Sueurs 
UviraTalk :
Avez-vous de la fièvre ou des frissons ?

Dialogue P009
Patient :
J'ai la fièvre et je vomis.
Mots-clés :
fièvre 
vomis 
Symptômes :
Fièvre 
Vomissements 
UviraTalk :
Depuis combien de jours présentez-vous ces symptômes ?

Dialogue P010
Patient :
Je pense que j'ai le palu.
Mots-clés :
palu 
paludisme 
Intention :
Suspicion de maladie 
UviraTalk :
Quels symptômes ressentez-vous actuellement ?

Structure de base de données recommandée
{
  "categorie": "Paludisme",
  "id": "P001",
  "phrase_patient": "J'ai de la fièvre",
  "mots_cles": ["fièvre"],
  "symptomes": ["fièvre"],
  "urgence": "faible",
  "reponse": "Depuis combien de temps avez-vous la fièvre ?"
}
P011
Patient :
Je me sens chaud depuis ce matin.
Mots-clés :
chaud 
ce matin 
Symptômes détectés :
Fièvre 
Question suivante :
Avez-vous des frissons ou des maux de tête ?

P012
Patient :
J'ai des frissons chaque nuit.
Mots-clés :
frissons 
nuit 
Symptômes détectés :
Frissons 
Question suivante :
Avez-vous également de la fièvre ?

P013
Patient :
Mon corps me fait très mal.
Mots-clés :
corps 
mal 
Symptômes détectés :
Douleurs musculaires 
Question suivante :
Avez-vous de la fièvre ou des frissons ?

P014
Patient :
Je suis couché depuis deux jours à cause de la fièvre.
Mots-clés :
couché 
fièvre 
deux jours 
Symptômes détectés :
Fièvre 
Fatigue 
Question suivante :
Avez-vous pris un traitement ?

P015
Patient :
Je vomis tout ce que je mange.
Mots-clés :
vomis 
mange 
Symptômes détectés :
Vomissements 
Question suivante :
Avez-vous également de la fièvre ?

P016
Patient :
Je n'ai plus de force.
Mots-clés :
plus de force 
Symptômes détectés :
Fatigue importante 
Question suivante :
Depuis quand ressentez-vous cette faiblesse ?

P017
Patient :
J'ai mal à la tête et aux articulations.
Mots-clés :
tête 
articulations 
Symptômes détectés :
Céphalée 
Douleurs articulaires 
Question suivante :
Avez-vous de la fièvre ?

P018
Patient :
Je transpire beaucoup même quand il fait froid.
Mots-clés :
transpire 
froid 
Symptômes détectés :
Sueurs abondantes 
Question suivante :
Avez-vous récemment eu de la fièvre ?

P019
Patient :
J'ai le corps cassé.
Mots-clés :
corps cassé 
Symptômes détectés :
Douleurs généralisées 
Question suivante :
Avez-vous également des frissons ou de la fièvre ?

P020
Patient :
Je fais souvent le palu.
Mots-clés :
palu 
Symptômes détectés :
Antécédent de paludisme 
Question suivante :
Quels symptômes avez-vous actuellement ?

Nouveaux mots-clés Paludisme collectés
Ajoutez-les dans votre dictionnaire UviraTalk :
fièvre
chaud
corps chaud
corps brûlant
frissons
froid
mal à la tête
céphalée
vomissements
nausées
fatigue
faiblesse
plus de force
courbatures
douleurs articulaires
douleurs musculaires
transpiration
sueurs
corps cassé
palu
paludisme
Structure recommandée
{
  "categorie": "Paludisme",
  "id": "P019",
  "phrase_patient": "J'ai le corps cassé",
  "mots_cles": ["corps cassé"],
  "symptomes": ["douleurs généralisées"],
  "urgence": "faible",
  "question_suivante": "Avez-vous également des frissons ou de la fièvre ?"
}
P021
Patient :
Je tremble beaucoup.
Mots-clés :
tremble 
Symptômes détectés :
Frissons 
Question suivante :
Avez-vous également de la fièvre ?

P022
Patient :
Je sens mon corps brûler.
Mots-clés :
brûler 
corps 
Symptômes détectés :
Fièvre 
Question suivante :
Depuis combien de temps cela a-t-il commencé ?

P023
Patient :
Je suis malade depuis trois jours.
Mots-clés :
malade 
trois jours 
Symptômes détectés :
Symptôme général 
Question suivante :
Quels sont les symptômes que vous ressentez ?

P024
Patient :
Je n'arrive plus à manger.
Mots-clés :
n'arrive plus à manger 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Avez-vous également de la fièvre ?

P025
Patient :
Tout mon corps est douloureux.
Mots-clés :
corps douloureux 
Symptômes détectés :
Douleurs généralisées 
Question suivante :
Avez-vous de la fièvre ou des frissons ?

P026
Patient :
Je me sens très faible quand je marche.
Mots-clés :
faible 
marche 
Symptômes détectés :
Fatigue 
Question suivante :
Depuis quand ressentez-vous cette faiblesse ?

P027
Patient :
J'ai chaud même quand il pleut.
Mots-clés :
chaud 
Symptômes détectés :
Fièvre 
Question suivante :
Avez-vous pris votre température ?

P028
Patient :
Je dors toute la journée.
Mots-clés :
dors 
journée 
Symptômes détectés :
Fatigue importante 
Question suivante :
Avez-vous également de la fièvre ?

P029
Patient :
J'ai mal derrière les yeux.
Mots-clés :
derrière les yeux 
Symptômes détectés :
Céphalée 
Question suivante :
Avez-vous de la fièvre ou des frissons ?

P030
Patient :
Mon enfant a de la fièvre et vomit.
Mots-clés :
enfant 
fièvre 
vomit 
Symptômes détectés :
Fièvre 
Vomissements 
Urgence :
Modérée 
Question suivante :
Quel âge a votre enfant ?

P031
Patient :
J'ai souvent des nausées.
Mots-clés :
nausées 
Symptômes détectés :
Nausées 
Question suivante :
Avez-vous également de la fièvre ?

P032
Patient :
Je transpire toute la nuit.
Mots-clés :
transpire 
nuit 
Symptômes détectés :
Sueurs nocturnes 
Question suivante :
Avez-vous aussi de la fièvre ?

P033
Patient :
J'ai la bouche amère.
Mots-clés :
bouche amère 
Symptômes détectés :
Symptôme fréquemment rapporté localement 
Question suivante :
Avez-vous de la fièvre ou des douleurs dans le corps ?

P034
Patient :
Je n'ai envie de rien manger.
Mots-clés :
pas envie de manger 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Depuis quand avez-vous perdu l'appétit ?

P035
Patient :
J'ai très froid puis très chaud.
Mots-clés :
froid 
chaud 
Symptômes détectés :
Frissons 
Fièvre 
Question suivante :
Depuis combien de jours cela dure-t-il ?

P036
Patient :
Je suis épuisé.
Mots-clés :
épuisé 
Symptômes détectés :
Fatigue sévère 
Question suivante :
Avez-vous de la fièvre ?

P037
Patient :
Mon enfant est tout chaud.
Mots-clés :
enfant 
chaud 
Symptômes détectés :
Fièvre chez l'enfant 
Question suivante :
Quel âge a votre enfant ?

P038
Patient :
Je vomis depuis ce matin.
Mots-clés :
vomis 
matin 
Symptômes détectés :
Vomissements 
Question suivante :
Avez-vous également de la fièvre ?

P039
Patient :
Je n'arrive même plus à me lever.
Mots-clés :
plus se lever 
Symptômes détectés :
Fatigue importante 
Faiblesse 
Urgence :
Élevée 
Question suivante :
Êtes-vous conscient et pouvez-vous boire de l'eau ?

P040
Patient :
Je crois que c'est encore le palu.
Mots-clés :
palu 
encore 
Symptômes détectés :
Suspicion de paludisme 
Question suivante :
Quels symptômes ressentez-vous actuellement ?

Nouveaux mots-clés à ajouter
tremble
corps brûle
malade
plus manger
perte d'appétit
nausées
bouche amère
épuisé
tout chaud
fatigue sévère
sueurs nocturnes
mal derrière les yeux
plus se lever
P041
Patient :
Je me sens très malade.
Mots-clés :
très malade 
Symptômes détectés :
Malaise général 
Question suivante :
Avez-vous de la fièvre ou des frissons ?

P042
Patient :
Mon enfant tremble de froid.
Mots-clés :
enfant 
tremble 
froid 
Symptômes détectés :
Frissons chez l'enfant 
Question suivante :
A-t-il également de la fièvre ?

P043
Patient :
J'ai chaud dans tout le corps.
Mots-clés :
chaud 
corps 
Symptômes détectés :
Fièvre 
Question suivante :
Depuis quand avez-vous cette sensation ?

P044
Patient :
Je suis toujours fatigué.
Mots-clés :
toujours fatigué 
Symptômes détectés :
Fatigue persistante 
Question suivante :
Avez-vous de la fièvre ou des douleurs corporelles ?

P045
Patient :
J'ai passé toute la nuit sans dormir à cause de la fièvre.
Mots-clés :
nuit 
fièvre 
Symptômes détectés :
Fièvre 
Trouble du sommeil 
Question suivante :
Avez-vous aussi des frissons ?

P046
Patient :
Je transpire puis j'ai froid.
Mots-clés :
transpire 
froid 
Symptômes détectés :
Sueurs 
Frissons 
Question suivante :
Depuis combien de jours cela dure-t-il ?

P047
Patient :
Mon corps est faible.
Mots-clés :
faible 
Symptômes détectés :
Faiblesse générale 
Question suivante :
Avez-vous de la fièvre ?

P048
Patient :
J'ai très mal aux os.
Mots-clés :
mal aux os 
Symptômes détectés :
Douleurs osseuses 
Question suivante :
Avez-vous également de la fièvre ?

P049
Patient :
J'ai le vertige.
Mots-clés :
vertige 
Symptômes détectés :
Vertiges 
Question suivante :
Avez-vous de la fièvre ou une faiblesse importante ?

P050
Patient :
Je me sens sans énergie.
Mots-clés :
sans énergie 
Symptômes détectés :
Fatigue 
Question suivante :
Depuis quand ressentez-vous cela ?

P051
Patient :
Je suis enceinte et j'ai la fièvre.
Mots-clés :
enceinte 
fièvre 
Symptômes détectés :
Fièvre pendant la grossesse 
Urgence :
Modérée 
Question suivante :
De combien de mois êtes-vous enceinte ?

P052
Patient :
Mon bébé a très chaud.
Mots-clés :
bébé 
chaud 
Symptômes détectés :
Fièvre chez le nourrisson 
Urgence :
Modérée 
Question suivante :
Quel âge a votre bébé ?

P053
Patient :
J'ai perdu l'appétit depuis plusieurs jours.
Mots-clés :
perdu l'appétit 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Avez-vous également de la fièvre ?

P054
Patient :
J'ai mal aux reins quand j'ai la fièvre.
Mots-clés :
reins 
fièvre 
Symptômes détectés :
Douleurs lombaires 
Fièvre 
Question suivante :
Depuis combien de jours avez-vous ces symptômes ?

P055
Patient :
Je suis couché toute la journée.
Mots-clés :
couché 
Symptômes détectés :
Fatigue sévère 
Question suivante :
Pouvez-vous manger et boire normalement ?

P056
Patient :
J'ai des nausées et des frissons.
Mots-clés :
nausées 
frissons 
Symptômes détectés :
Nausées 
Frissons 
Question suivante :
Avez-vous de la fièvre ?

P057
Patient :
Je me sens cassé.
Mots-clés :
cassé 
Symptômes détectés :
Courbatures 
Douleurs généralisées 
Question suivante :
Avez-vous de la fièvre ?

P058
Patient :
J'ai chaud et je transpire beaucoup.
Mots-clés :
chaud 
transpire 
Symptômes détectés :
Fièvre 
Sueurs 
Question suivante :
Depuis combien de temps ?

P059
Patient :
Mon enfant refuse de manger et a de la fièvre.
Mots-clés :
enfant 
refuse de manger 
fièvre 
Symptômes détectés :
Fièvre 
Perte d'appétit 
Question suivante :
Quel âge a votre enfant ?

P060
Patient :
Je pense que les moustiques m'ont rendu malade.
Mots-clés :
moustiques 
malade 
Symptômes détectés :
Suspicion de paludisme 
Question suivante :
Quels symptômes ressentez-vous actuellement ?

Nouveaux mots-clés ajoutés
très malade
toujours fatigué
sans énergie
mal aux os
vertige
perdu l'appétit
mal aux reins
couché toute la journée
refuse de manger
moustiques
bébé chaud
P061
Patient :
Je chauffe beaucoup.
Mots-clés :
chauffe 
Symptômes détectés :
Fièvre 
Question suivante :
Depuis quand avez-vous cette chaleur ?

P062
Patient :
Mon corps chauffe toute la nuit.
Mots-clés :
corps chauffe 
nuit 
Symptômes détectés :
Fièvre nocturne 
Question suivante :
Avez-vous des frissons ?

P063
Patient :
Je suis faible depuis hier.
Mots-clés :
faible 
hier 
Symptômes détectés :
Faiblesse 
Question suivante :
Avez-vous de la fièvre ?

P064
Patient :
J'ai les yeux lourds.
Mots-clés :
yeux lourds 
Symptômes détectés :
Fatigue 
Malaise général 
Question suivante :
Avez-vous mal à la tête ?

P065
Patient :
Je n'arrive pas à travailler.
Mots-clés :
pas travailler 
Symptômes détectés :
Fatigue importante 
Question suivante :
Quels autres symptômes avez-vous ?

P066
Patient :
Mon enfant est très faible aujourd'hui.
Mots-clés :
enfant 
faible 
Symptômes détectés :
Faiblesse chez l'enfant 
Question suivante :
A-t-il de la fièvre ?

P067
Patient :
J'ai des douleurs partout.
Mots-clés :
douleurs partout 
Symptômes détectés :
Douleurs généralisées 
Question suivante :
Avez-vous de la fièvre ?

P068
Patient :
Je grelotte.
Mots-clés :
grelotte 
Symptômes détectés :
Frissons 
Question suivante :
Avez-vous également de la fièvre ?

P069
Patient :
Je me sens comme si j'avais été battu.
Mots-clés :
battu 
Symptômes détectés :
Courbatures importantes 
Question suivante :
Avez-vous de la fièvre ou des frissons ?

P070
Patient :
J'ai chaud et mal à la tête.
Mots-clés :
chaud 
mal à la tête 
Symptômes détectés :
Fièvre 
Céphalée 
Question suivante :
Depuis combien de jours ?

P071
Patient :
J'ai pris un médicament mais ça ne passe pas.
Mots-clés :
médicament 
ne passe pas 
Symptômes détectés :
Symptômes persistants 
Question suivante :
Quels symptômes avez-vous actuellement ?

P072
Patient :
Je dors beaucoup depuis que je suis malade.
Mots-clés :
dors beaucoup 
Symptômes détectés :
Fatigue 
Question suivante :
Avez-vous de la fièvre ?

P073
Patient :
Je n'ai pas d'appétit.
Mots-clés :
pas d'appétit 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Depuis combien de temps ?

P074
Patient :
J'ai des frissons même sous une couverture.
Mots-clés :
frissons 
couverture 
Symptômes détectés :
Frissons importants 
Question suivante :
Avez-vous de la fièvre ?

P075
Patient :
Je transpire puis je tremble.
Mots-clés :
transpire 
tremble 
Symptômes détectés :
Sueurs 
Frissons 
Question suivante :
Depuis combien de jours ?

P076
Patient :
Mon bébé refuse le sein et a de la fièvre.
Mots-clés :
bébé 
refuse le sein 
fièvre 
Symptômes détectés :
Fièvre du nourrisson 
Difficulté d'alimentation 
Urgence :
Élevée 
Question suivante :
Quel âge a votre bébé ?

P077
Patient :
J'ai mal à la tête depuis plusieurs jours.
Mots-clés :
mal à la tête 
plusieurs jours 
Symptômes détectés :
Céphalée persistante 
Question suivante :
Avez-vous également de la fièvre ?

P078
Patient :
J'ai très froid puis je transpire.
Mots-clés :
froid 
transpire 
Symptômes détectés :
Frissons 
Sueurs 
Question suivante :
Avez-vous de la fièvre ?

P079
Patient :
Je pense que c'est encore le moustique.
Mots-clés :
moustique 
Symptômes détectés :
Suspicion de paludisme 
Question suivante :
Quels symptômes ressentez-vous ?

P080
Patient :
Je suis malade après avoir été piqué par beaucoup de moustiques.
Mots-clés :
piqué 
moustiques 
Symptômes détectés :
Suspicion de paludisme 
Question suivante :
Avez-vous de la fièvre, des frissons ou des maux de tête ?

Nouveaux mots-clés à intégrer
chauffe
corps chauffe
yeux lourds
pas travailler
grelotte
comme battu
ça ne passe pas
dors beaucoup
pas d'appétit
refuse le sein
piqué par moustiques
P081
Patient :
Je me sens très chaud.
Mots-clés :
très chaud 
Symptômes détectés :
Fièvre 
Question suivante :
Depuis quand avez-vous cette fièvre ?

P082
Patient :
Je tremble et j'ai mal à la tête.
Mots-clés :
tremble 
mal à la tête 
Symptômes détectés :
Frissons 
Céphalée 
Question suivante :
Avez-vous également de la fièvre ?

P083
Patient :
Mon enfant a chaud et pleure beaucoup.
Mots-clés :
enfant 
chaud 
pleure 
Symptômes détectés :
Fièvre chez l'enfant 
Question suivante :
Quel âge a votre enfant ?

P084
Patient :
Je suis enceinte et je grelotte.
Mots-clés :
enceinte 
grelotte 
Symptômes détectés :
Frissons pendant la grossesse 
Urgence :
Modérée 
Question suivante :
Avez-vous de la fièvre ?

P085
Patient :
Je vomis et je suis très faible.
Mots-clés :
vomis 
faible 
Symptômes détectés :
Vomissements 
Fatigue 
Question suivante :
Pouvez-vous boire et garder les liquides ?

P086
Patient :
Je n'arrive plus à manger à cause de la maladie.
Mots-clés :
plus manger 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Avez-vous de la fièvre ?

P087
Patient :
J'ai chaud, froid puis chaud encore.
Mots-clés :
chaud 
froid 
Symptômes détectés :
Fièvre 
Frissons 
Question suivante :
Depuis combien de jours cela dure-t-il ?

P088
Patient :
Je me sens très épuisé.
Mots-clés :
épuisé 
Symptômes détectés :
Fatigue sévère 
Question suivante :
Pouvez-vous effectuer vos activités habituelles ?

P089
Patient :
Mon corps chauffe surtout le soir.
Mots-clés :
chauffe 
soir 
Symptômes détectés :
Fièvre 
Question suivante :
Avez-vous des frissons ?

P090
Patient :
J'ai des douleurs dans les jambes et les bras.
Mots-clés :
jambes 
bras 
douleurs 
Symptômes détectés :
Douleurs musculaires 
Question suivante :
Avez-vous de la fièvre ?

P091
Patient :
J'ai le palu chaque saison des pluies.
Mots-clés :
palu 
saison des pluies 
Symptômes détectés :
Antécédent de paludisme 
Question suivante :
Quels symptômes avez-vous aujourd'hui ?

P092
Patient :
Je dors sous moustiquaire mais je suis malade.
Mots-clés :
moustiquaire 
malade 
Symptômes détectés :
Symptôme général 
Question suivante :
Quels symptômes ressentez-vous ?

P093
Patient :
Mon bébé est chaud et ne boit plus.
Mots-clés :
bébé 
chaud 
ne boit plus 
Symptômes détectés :
Fièvre 
Refus de boire 
Urgence :
Élevée 
Question suivante :
Quel âge a votre bébé ?

P094
Patient :
J'ai la tête lourde et le corps faible.
Mots-clés :
tête lourde 
corps faible 
Symptômes détectés :
Céphalée 
Fatigue 
Question suivante :
Avez-vous de la fièvre ?

P095
Patient :
Je suis couché depuis plusieurs jours.
Mots-clés :
couché 
plusieurs jours 
Symptômes détectés :
Faiblesse importante 
Question suivante :
Pouvez-vous manger et boire normalement ?

P096
Patient :
Je transpire beaucoup puis je grelotte.
Mots-clés :
transpire 
grelotte 
Symptômes détectés :
Sueurs 
Frissons 
Question suivante :
Avez-vous de la fièvre ?

P097
Patient :
Mon enfant vomit et a de la fièvre.
Mots-clés :
enfant 
vomit 
fièvre 
Symptômes détectés :
Fièvre 
Vomissements 
Question suivante :
Quel âge a votre enfant ?

P098
Patient :
Je suis faible et j'ai des vertiges.
Mots-clés :
faible 
vertiges 
Symptômes détectés :
Fatigue 
Vertiges 
Question suivante :
Avez-vous de la fièvre ?

P099
Patient :
Je crois que j'ai encore attrapé le palu.
Mots-clés :
attrapé le palu 
Symptômes détectés :
Suspicion de paludisme 
Question suivante :
Quels symptômes présentez-vous actuellement ?

P100
Patient :
J'ai la fièvre, des frissons et des vomissements.
Mots-clés :
fièvre 
frissons 
vomissements 
Symptômes détectés :
Fièvre 
Frissons 
Vomissements 
Urgence :
Modérée 
Question suivante :
Depuis combien de jours avez-vous ces symptômes ?

Catégorie terminée
✅ PALUDISME : P001 à P100 complétés
Résumé des principaux mots-clés collectés
fièvre
chaud
chauffe
corps chaud
corps brûlant
frissons
grelotte
tremble
froid
mal à la tête
tête lourde
yeux lourds
vomissements
vomis
nausées
fatigue
faiblesse
épuisé
sans énergie
courbatures
corps cassé
douleurs partout
mal aux os
vertiges
perte d'appétit
pas d'appétit
refuse de manger
refuse le sein
transpire
sueurs nocturnes
palu
paludisme
moustiques
piqué par moustiques





GROSSESSE (G001 à G020)
G001
Patiente :
Je suis enceinte.
Mots-clés :
enceinte 
Intention :
Déclaration de grossesse 
Question suivante :
De combien de mois êtes-vous enceinte ?

G002
Patiente :
Je pense que je suis enceinte.
Mots-clés :
pense enceinte 
Symptômes détectés :
Suspicion de grossesse 
Question suivante :
Avez-vous un retard de règles ?

G003
Patiente :
Mes règles sont en retard.
Mots-clés :
retard de règles 
Symptômes détectés :
Possible grossesse 
Question suivante :
Depuis combien de temps vos règles sont-elles en retard ?

G004
Patiente :
Je vomis tous les matins.
Mots-clés :
vomis 
matin 
Symptômes détectés :
Nausées de grossesse 
Question suivante :
Êtes-vous enceinte ou pensez-vous l'être ?

G005
Patiente :
J'ai souvent des nausées.
Mots-clés :
nausées 
Symptômes détectés :
Nausées 
Question suivante :
Êtes-vous enceinte ?

G006
Patiente :
Je suis enceinte de 3 mois.
Mots-clés :
enceinte 
3 mois 
Symptômes détectés :
Grossesse confirmée 
Question suivante :
Avez-vous déjà commencé les consultations prénatales ?

G007
Patiente :
Mon ventre commence à grossir.
Mots-clés :
ventre grossit 
Symptômes détectés :
Évolution de grossesse 
Question suivante :
Avez-vous fait un test de grossesse ?

G008
Patiente :
Je suis enceinte et très fatiguée.
Mots-clés :
enceinte 
fatiguée 
Symptômes détectés :
Fatigue pendant la grossesse 
Question suivante :
De combien de mois êtes-vous enceinte ?

G009
Patiente :
J'ai mal au bas-ventre.
Mots-clés :
bas-ventre 
Symptômes détectés :
Douleur abdominale 
Question suivante :
Êtes-vous enceinte ?

G010
Patiente :
Je suis enceinte et j'ai de la fièvre.
Mots-clés :
enceinte 
fièvre 
Symptômes détectés :
Fièvre pendant la grossesse 
Urgence :
Modérée 
Question suivante :
Depuis combien de temps avez-vous la fièvre ?

G011
Patiente :
Je ne sens plus le bébé bouger.
Mots-clés :
bébé ne bouge plus 
Symptômes détectés :
Diminution des mouvements fœtaux 
Urgence :
Élevée 
Question suivante :
Depuis quand ne sentez-vous plus les mouvements du bébé ?

G012
Patiente :
J'ai des saignements.
Mots-clés :
saignements 
Symptômes détectés :
Saignement pendant la grossesse 
Urgence :
Élevée 
Question suivante :
Êtes-vous enceinte ?

G013
Patiente :
Je suis enceinte et j'ai perdu du sang.
Mots-clés :
enceinte 
perdu du sang 
Symptômes détectés :
Hémorragie pendant la grossesse 
Urgence :
Très élevée 
Question suivante :
De combien de mois êtes-vous enceinte ?

G014
Patiente :
Mes pieds sont gonflés.
Mots-clés :
pieds gonflés 
Symptômes détectés :
Œdèmes 
Question suivante :
Êtes-vous enceinte ?

G015
Patiente :
Mon visage est gonflé.
Mots-clés :
visage gonflé 
Symptômes détectés :
Œdème du visage 
Question suivante :
Êtes-vous enceinte et avez-vous des maux de tête ?

G016
Patiente :
J'ai très mal à la tête.
Mots-clés :
mal à la tête 
Symptômes détectés :
Céphalée 
Question suivante :
Êtes-vous enceinte ?

G017
Patiente :
Je vois flou.
Mots-clés :
voit flou 
Symptômes détectés :
Trouble de la vision 
Urgence :
Élevée 
Question suivante :
Êtes-vous enceinte ?

G018
Patiente :
J'ai des douleurs dans le dos.
Mots-clés :
mal au dos 
Symptômes détectés :
Douleur dorsale 
Question suivante :
De combien de mois êtes-vous enceinte ?

G019
Patiente :
Je suis enceinte et je vomis beaucoup.
Mots-clés :
enceinte 
vomissements 
Symptômes détectés :
Vomissements importants 
Question suivante :
Pouvez-vous boire et manger normalement ?

G020
Patiente :
Je suis enceinte de 8 mois.
Mots-clés :
enceinte 
8 mois 
Symptômes détectés :
Grossesse avancée 
Question suivante :
Ressentez-vous des douleurs ou des contractions ?

Dictionnaire initial Grossesse
enceinte
grossesse
retard de règles
absence de règles
nausées
vomissements
fatigue
bas-ventre
ventre grossit
bébé bouge
bébé ne bouge plus
saignements
perte de sang
pieds gonflés
visage gonflé
mal à la tête
voit flou
mal au dos
contractions
consultation prénatale
G021
Patiente :
Je n'ai jamais fait de consultation prénatale.
Mots-clés :
consultation prénatale 
jamais 
Intention :
Suivi de grossesse 
Question suivante :
De combien de mois êtes-vous enceinte ?

G022
Patiente :
C'est ma première grossesse.
Mots-clés :
première grossesse 
Question suivante :
De combien de mois êtes-vous enceinte ?

G023
Patiente :
Mon bébé bouge beaucoup.
Mots-clés :
bébé bouge 
Symptômes détectés :
Mouvements fœtaux présents 
Question suivante :
De combien de mois êtes-vous enceinte ?

G024
Patiente :
Je sens moins le bébé bouger.
Mots-clés :
moins bouger 
Symptômes détectés :
Diminution des mouvements fœtaux 
Urgence :
Élevée 
Question suivante :
Depuis quand avez-vous remarqué cela ?

G025
Patiente :
J'ai faim tout le temps.
Mots-clés :
faim 
Symptômes détectés :
Augmentation de l'appétit 
Question suivante :
De combien de mois êtes-vous enceinte ?

G026
Patiente :
Je ne mange presque plus.
Mots-clés :
ne mange plus 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Avez-vous des nausées ou des vomissements ?

G027
Patiente :
Je suis enceinte et je suis essoufflée.
Mots-clés :
enceinte 
essoufflée 
Symptômes détectés :
Essoufflement 
Question suivante :
Depuis quand avez-vous cette difficulté à respirer ?

G028
Patiente :
J'ai des brûlures d'estomac.
Mots-clés :
brûlures d'estomac 
Symptômes détectés :
Reflux gastrique 
Question suivante :
De combien de mois êtes-vous enceinte ?

G029
Patiente :
J'urine souvent.
Mots-clés :
urine souvent 
Symptômes détectés :
Mictions fréquentes 
Question suivante :
Êtes-vous enceinte ?

G030
Patiente :
Je dors mal depuis que je suis enceinte.
Mots-clés :
dort mal 
enceinte 
Symptômes détectés :
Trouble du sommeil 
Question suivante :
De combien de mois êtes-vous enceinte ?

G031
Patiente :
J'ai des contractions.
Mots-clés :
contractions 
Symptômes détectés :
Contractions utérines 
Question suivante :
De combien de mois êtes-vous enceinte ?

G032
Patiente :
Mon ventre devient dur parfois.
Mots-clés :
ventre dur 
Symptômes détectés :
Possible contraction 
Question suivante :
Ressentez-vous aussi des douleurs ?

G033
Patiente :
J'ai perdu beaucoup d'eau.
Mots-clés :
perdu de l'eau 
Symptômes détectés :
Rupture possible de la poche des eaux 
Urgence :
Très élevée 
Question suivante :
Êtes-vous enceinte de combien de mois ?

G034
Patiente :
Je sens une pression en bas.
Mots-clés :
pression en bas 
Symptômes détectés :
Pression pelvienne 
Question suivante :
Êtes-vous proche du terme ?

G035
Patiente :
J'ai des douleurs régulières.
Mots-clés :
douleurs régulières 
Symptômes détectés :
Travail possible 
Question suivante :
Les douleurs reviennent-elles à intervalles réguliers ?

G036
Patiente :
Je suis enceinte et je fais souvent des vertiges.
Mots-clés :
enceinte 
vertiges 
Symptômes détectés :
Vertiges 
Question suivante :
Avez-vous mangé aujourd'hui ?

G037
Patiente :
J'ai les jambes gonflées.
Mots-clés :
jambes gonflées 
Symptômes détectés :
Œdème 
Question suivante :
Avez-vous aussi des maux de tête ou une vision floue ?

G038
Patiente :
Je suis enceinte et j'ai du mal à respirer.
Mots-clés :
enceinte 
mal respirer 
Symptômes détectés :
Difficulté respiratoire 
Urgence :
Élevée 
Question suivante :
Cette difficulté est-elle soudaine ou progressive ?

G039
Patiente :
Mon bébé bouge moins aujourd'hui.
Mots-clés :
bébé bouge moins 
Symptômes détectés :
Diminution des mouvements fœtaux 
Urgence :
Élevée 
Question suivante :
Depuis combien d'heures avez-vous remarqué ce changement ?

G040
Patiente :
Je crois que je vais accoucher.
Mots-clés :
accoucher 
Symptômes détectés :
Début possible du travail 
Question suivante :
Avez-vous des contractions régulières ou une perte d'eau ?

Nouveaux mots-clés Grossesse
première grossesse
bébé bouge
bébé bouge moins
moins bouger
consultation prénatale
faim
ne mange plus
essoufflée
brûlures d'estomac
urine souvent
dort mal
contractionsG041
Patiente :
Je suis enceinte et je suis toujours fatiguée.
Mots-clés :
enceinte 
toujours fatiguée 
Symptômes détectés :
Fatigue persistante 
Question suivante :
De combien de mois êtes-vous enceinte ?

G042
Patiente :
Je dors toute la journée.
Mots-clés :
dort toute la journée 
Symptômes détectés :
Fatigue excessive 
Question suivante :
Avez-vous d'autres symptômes ?

G043
Patiente :
J'ai mal au ventre depuis ce matin.
Mots-clés :
mal au ventre 
Symptômes détectés :
Douleur abdominale 
Question suivante :
Êtes-vous enceinte de combien de mois ?

G044
Patiente :
Mon ventre est très tendu.
Mots-clés :
ventre tendu 
Symptômes détectés :
Tension abdominale 
Question suivante :
Ressentez-vous des contractions ?

G045
Patiente :
Je ne sens presque plus mon bébé.
Mots-clés :
ne sent plus bébé 
Symptômes détectés :
Diminution importante des mouvements fœtaux 
Urgence :
Très élevée 
Question suivante :
Depuis quand ne sentez-vous presque plus les mouvements ?

G046
Patiente :
J'ai des douleurs dans le bassin.
Mots-clés :
bassin 
Symptômes détectés :
Douleur pelvienne 
Question suivante :
De combien de mois êtes-vous enceinte ?

G047
Patiente :
Je suis enceinte et je saigne un peu.
Mots-clés :
enceinte 
saigne 
Symptômes détectés :
Saignement pendant la grossesse 
Urgence :
Élevée 
Question suivante :
De quelle couleur est le sang et depuis quand cela a commencé ?

G048
Patiente :
Je me sens faible quand je marche.
Mots-clés :
faible 
marche 
Symptômes détectés :
Faiblesse 
Question suivante :
Avez-vous des vertiges ?

G049
Patiente :
Je suis enceinte et j'ai le cœur qui bat vite.
Mots-clés :
cœur bat vite 
Symptômes détectés :
Palpitations 
Question suivante :
Depuis quand ressentez-vous cela ?

G050
Patiente :
Je n'arrive pas à manger normalement.
Mots-clés :
pas manger normalement 
Symptômes détectés :
Difficulté alimentaire 
Question suivante :
Avez-vous des nausées ou des vomissements ?

G051
Patiente :
J'ai souvent envie de dormir.
Mots-clés :
envie de dormir 
Symptômes détectés :
Somnolence 
Question suivante :
Êtes-vous enceinte ?

G052
Patiente :
J'ai des douleurs qui viennent et repartent.
Mots-clés :
douleurs qui viennent et repartent 
Symptômes détectés :
Contractions possibles 
Question suivante :
Les douleurs sont-elles régulières ?

G053
Patiente :
Mon bébé bouge beaucoup aujourd'hui.
Mots-clés :
bébé bouge beaucoup 
Symptômes détectés :
Activité fœtale 
Question suivante :
De combien de mois êtes-vous enceinte ?

G054
Patiente :
Je suis enceinte et j'ai des démangeaisons.
Mots-clés :
démangeaisons 
Symptômes détectés :
Prurit 
Question suivante :
Où ressentez-vous ces démangeaisons ?

G055
Patiente :
J'ai des douleurs au dos et au ventre.
Mots-clés :
dos 
ventre 
Symptômes détectés :
Douleurs dorsales et abdominales 
Question suivante :
Êtes-vous proche de votre date d'accouchement ?

G056
Patiente :
J'ai perdu l'appétit depuis plusieurs jours.
Mots-clés :
perdu l'appétit 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Avez-vous également des nausées ?

G057
Patiente :
Je vois des lumières devant mes yeux.
Mots-clés :
lumières devant les yeux 
Symptômes détectés :
Trouble visuel 
Urgence :
Élevée 
Question suivante :
Avez-vous aussi des maux de tête importants ?

G058
Patiente :
Mon visage et mes mains sont gonflés.
Mots-clés :
visage gonflé 
mains gonflées 
Symptômes détectés :
Œdèmes 
Urgence :
Modérée à élevée 
Question suivante :
Avez-vous des maux de tête ou une vision floue ?

G059
Patiente :
Je suis enceinte de neuf mois et j'ai des douleurs.
Mots-clés :
neuf mois 
douleurs 
Symptômes détectés :
Travail possible 
Question suivante :
Les douleurs sont-elles régulières et rapprochées ?

G060
Patiente :
Je pense que le travail a commencé.
Mots-clés :
travail commencé 
Symptômes détectés :
Début possible de l'accouchement 
Question suivante :
Avez-vous des contractions régulières ou une perte d'eau ?

Nouveaux mots-clés Grossesse à ajouter
ventre tendu
ne sent plus bébé
douleur bassin
saigne un peu
cœur bat vite
palpitations
envie de dormir
douleurs qui viennent et repartent
bébé bouge beaucoup
démangeaisons
lumières devant les yeux
mains gonflées
travail commencé
G061
Patiente :
Je suis enceinte et je suis souvent essoufflée.
Mots-clés :
enceinte 
essoufflée 
Symptômes détectés :
Essoufflement 
Question suivante :
Depuis quand ressentez-vous cet essoufflement ?

G062
Patiente :
Je n'arrive plus à dormir la nuit.
Mots-clés :
ne dort plus 
nuit 
Symptômes détectés :
Insomnie 
Question suivante :
De combien de mois êtes-vous enceinte ?

G063
Patiente :
Mon ventre descend.
Mots-clés :
ventre descend 
Symptômes détectés :
Approche possible de l'accouchement 
Question suivante :
De combien de mois êtes-vous enceinte ?

G064
Patiente :
J'ai des douleurs en bas du ventre.
Mots-clés :
bas du ventre 
Symptômes détectés :
Douleur pelvienne 
Question suivante :
Les douleurs sont-elles régulières ?

G065
Patiente :
Je me sens très faible aujourd'hui.
Mots-clés :
très faible 
Symptômes détectés :
Faiblesse importante 
Question suivante :
Avez-vous des vertiges ou des saignements ?

G066
Patiente :
J'ai des crampes dans les jambes.
Mots-clés :
crampes 
jambes 
Symptômes détectés :
Crampes musculaires 
Question suivante :
Ces crampes surviennent-elles surtout la nuit ?

G067
Patiente :
Je suis enceinte et j'ai des pertes blanches.
Mots-clés :
pertes blanches 
Symptômes détectés :
Écoulement vaginal 
Question suivante :
Les pertes ont-elles une odeur inhabituelle ou provoquent-elles des démangeaisons ?

G068
Patiente :
J'ai mal quand je marche.
Mots-clés :
mal marcher 
Symptômes détectés :
Douleur liée à la grossesse 
Question suivante :
Où ressentez-vous cette douleur ?

G069
Patiente :
Mon bébé donne beaucoup de coups.
Mots-clés :
bébé donne des coups 
Symptômes détectés :
Mouvements fœtaux présents 
Question suivante :
De combien de mois êtes-vous enceinte ?

G070
Patiente :
J'ai une douleur qui serre le ventre.
Mots-clés :
ventre serre 
Symptômes détectés :
Contraction possible 
Question suivante :
Cette douleur revient-elle régulièrement ?

G071
Patiente :
Je suis enceinte et je fais des malaises.
Mots-clés :
malaises 
Symptômes détectés :
Malaise 
Question suivante :
Avez-vous perdu connaissance ou ressenti des vertiges ?

G072
Patiente :
J'ai perdu un liquide clair.
Mots-clés :
liquide clair 
Symptômes détectés :
Rupture possible de la poche des eaux 
Urgence :
Élevée 
Question suivante :
La perte continue-t-elle actuellement ?

G073
Patiente :
Je suis enceinte et j'ai des douleurs dans les reins.
Mots-clés :
reins 
Symptômes détectés :
Douleur lombaire 
Question suivante :
Avez-vous aussi de la fièvre ou des brûlures en urinant ?

G074
Patiente :
Mes pieds gonflent chaque soir.
Mots-clés :
pieds gonflent 
Symptômes détectés :
Œdèmes 
Question suivante :
Avez-vous également des maux de tête ?

G075
Patiente :
J'ai des contractions toutes les dix minutes.
Mots-clés :
contractions 
dix minutes 
Symptômes détectés :
Travail possible 
Urgence :
Élevée 
Question suivante :
De combien de mois êtes-vous enceinte ?

G076
Patiente :
Je ne supporte plus certaines odeurs.
Mots-clés :
odeurs 
Symptômes détectés :
Sensibilité aux odeurs 
Question suivante :
Êtes-vous au début de votre grossesse ?

G077
Patiente :
J'ai souvent envie de vomir.
Mots-clés :
envie de vomir 
Symptômes détectés :
Nausées 
Question suivante :
De combien de mois êtes-vous enceinte ?

G078
Patiente :
J'ai des douleurs qui descendent vers les jambes.
Mots-clés :
douleurs jambes 
Symptômes détectés :
Douleurs pelviennes irradiantes 
Question suivante :
Êtes-vous proche de l'accouchement ?

G079
Patiente :
Mon ventre devient dur plusieurs fois par jour.
Mots-clés :
ventre dur 
Symptômes détectés :
Contractions possibles 
Question suivante :
Les épisodes sont-ils douloureux ?

G080
Patiente :
Je suis enceinte et je crois que l'accouchement approche.
Mots-clés :
accouchement approche 
Symptômes détectés :
Fin de grossesse 
Question suivante :
Avez-vous des contractions régulières, des saignements ou une perte d'eau ?

Nouveaux mots-clés Grossesse
ventre descend
crampes jambes
pertes blanches
bébé donne des coups
ventre serre
malaises
liquide clair
pieds gonflent
odeurs
envie de vomir
douleurs vers les jambes
accouchement approche
G081
Patiente :
J'ai des contractions très rapprochées.
Mots-clés :
contractions rapprochées 
Symptômes détectés :
Travail actif 
Urgence :
Élevée 
Question suivante :
Les contractions reviennent-elles toutes les 5 minutes ou moins ?

G082
Patiente :
Je perds du sang et j'ai des douleurs.
Mots-clés :
perd du sang 
douleurs 
Symptômes détectés :
Saignement pendant la grossesse 
Urgence :
Très élevée 
Question suivante :
De combien de mois êtes-vous enceinte ?

G083
Patiente :
J'ai perdu beaucoup d'eau.
Mots-clés :
beaucoup d'eau 
Symptômes détectés :
Rupture de la poche des eaux 
Urgence :
Très élevée 
Question suivante :
Ressentez-vous également des contractions ?

G084
Patiente :
Je ne vois pas bien aujourd'hui.
Mots-clés :
ne voit pas bien 
Symptômes détectés :
Trouble visuel 
Urgence :
Élevée 
Question suivante :
Avez-vous aussi un fort mal de tête ?

G085
Patiente :
J'ai très mal à la tête et mes pieds sont gonflés.
Mots-clés :
mal à la tête 
pieds gonflés 
Symptômes détectés :
Céphalée 
Œdèmes 
Urgence :
Élevée 
Question suivante :
Voyez-vous flou ou avez-vous des lumières devant les yeux ?

G086
Patiente :
Mon bébé ne bouge plus depuis hier.
Mots-clés :
bébé ne bouge plus 
hier 
Symptômes détectés :
Absence de mouvements fœtaux 
Urgence :
Très élevée 
Question suivante :
Consultez immédiatement. Depuis quelle heure ne sentez-vous plus les mouvements ?

G087
Patiente :
J'ai des douleurs très fortes dans le ventre.
Mots-clés :
douleurs fortes 
ventre 
Symptômes détectés :
Douleur abdominale sévère 
Urgence :
Élevée 
Question suivante :
Avez-vous des saignements ou une perte d'eau ?

G088
Patiente :
Je suis enceinte et je fais de la fièvre.
Mots-clés :
enceinte 
fièvre 
Symptômes détectés :
Fièvre pendant la grossesse 
Urgence :
Modérée à élevée 
Question suivante :
Depuis combien de jours avez-vous la fièvre ?

G089
Patiente :
Je me sens très faible et étourdie.
Mots-clés :
faible 
étourdie 
Symptômes détectés :
Faiblesse 
Vertiges 
Question suivante :
Avez-vous mangé aujourd'hui et avez-vous des saignements ?

G090
Patiente :
J'ai l'impression que le bébé va sortir.
Mots-clés :
bébé va sortir 
Symptômes détectés :
Accouchement imminent 
Urgence :
Très élevée 
Question suivante :
Avez-vous des contractions régulières ?

G091
Patiente :
Les douleurs reviennent toutes les cinq minutes.
Mots-clés :
cinq minutes 
Symptômes détectés :
Travail actif 
Urgence :
Élevée 
Question suivante :
Êtes-vous déjà en route vers une maternité ?

G092
Patiente :
J'ai envie de pousser.
Mots-clés :
envie de pousser 
Symptômes détectés :
Accouchement avancé 
Urgence :
Très élevée 
Question suivante :
Êtes-vous accompagnée actuellement ?

G093
Patiente :
Je perds un liquide verdâtre.
Mots-clés :
liquide verdâtre 
Symptômes détectés :
Liquide amniotique anormal 
Urgence :
Très élevée 
Question suivante :
Depuis quand avez-vous remarqué cela ?

G094
Patiente :
J'ai des bourdonnements dans les oreilles.
Mots-clés :
bourdonnements oreilles 
Symptômes détectés :
Symptôme d'alerte possible 
Question suivante :
Avez-vous aussi des maux de tête ou une vision floue ?

G095
Patiente :
Mon visage est très gonflé aujourd'hui.
Mots-clés :
visage très gonflé 
Symptômes détectés :
Œdème important 
Question suivante :
Avez-vous également des maux de tête ?

G096
Patiente :
Je n'arrive plus à marcher à cause des douleurs.
Mots-clés :
plus marcher 
douleurs 
Symptômes détectés :
Douleurs sévères 
Urgence :
Élevée 
Question suivante :
Les douleurs sont-elles régulières ?

G097
Patiente :
Je suis à terme et j'ai des contractions.
Mots-clés :
à terme 
contractions 
Symptômes détectés :
Travail d'accouchement 
Question suivante :
Toutes les combien de minutes surviennent-elles ?

G098
Patiente :
Mon bébé bouge beaucoup moins qu'avant.
Mots-clés :
bouge moins 
Symptômes détectés :
Diminution des mouvements fœtaux 
Urgence :
Élevée 
Question suivante :
Depuis combien de temps avez-vous constaté ce changement ?

G099
Patiente :
Je suis enceinte et j'ai perdu connaissance.
Mots-clés :
perdu connaissance 
Symptômes détectés :
Malaise grave 
Urgence :
Très élevée 
Question suivante :
Avez-vous été examinée par un professionnel de santé ?

G100
Patiente :
Je vais bientôt accoucher.
Mots-clés :
bientôt accoucher 
Symptômes détectés :
Fin de grossesse 
Question suivante :
Avez-vous déjà préparé votre déplacement vers la maternité ?

Catégorie terminée
✅ GROSSESSE : G001 à G100 complétés
Principaux mots-clés Grossesse collectés
enceinte
retard de règles
nausées
vomissements
fatigue
bébé bouge
bébé bouge moins
bébé ne bouge plus
saignements
perte de sang
perte d'eau
liquide clair
liquide verdâtre
contractions
contractions rapprochées
ventre dur
ventre descend
accouchement approche
envie de pousser
à terme
pieds gonflés
mains gonflées
visage gonflé
voit flou
lumières devant les yeux
mal à la tête
vertiges
perdu connaissance
ventre dur
perdu de l'eau
poche des eaux
pression en bas
douleurs régulières
vertiges
jambes gonflées
mal respirer
accoucher









DIARRHÉE (D001 à D020)
D001
Patient :
J'ai la diarrhée.
Mots-clés :
diarrhée 
Symptômes détectés :
Selles liquides 
Question suivante :
Depuis combien de temps avez-vous la diarrhée ?

D002
Patient :
Je vais souvent aux toilettes.
Mots-clés :
souvent toilettes 
Symptômes détectés :
Diarrhée possible 
Question suivante :
Vos selles sont-elles liquides ?

D003
Patient :
Mes selles sont très liquides.
Mots-clés :
selles liquides 
Symptômes détectés :
Diarrhée 
Question suivante :
Depuis combien de jours cela dure-t-il ?

D004
Patient :
Je fais caca comme de l'eau.
Mots-clés :
caca comme de l'eau 
Symptômes détectés :
Diarrhée aqueuse 
Question suivante :
Combien de fois êtes-vous allé aux toilettes aujourd'hui ?

D005
Patient :
Mon enfant a la diarrhée.
Mots-clés :
enfant 
diarrhée 
Symptômes détectés :
Diarrhée chez l'enfant 
Question suivante :
Quel âge a votre enfant ?

D006
Patient :
J'ai mal au ventre et la diarrhée.
Mots-clés :
mal au ventre 
diarrhée 
Symptômes détectés :
Diarrhée 
Douleurs abdominales 
Question suivante :
Avez-vous également de la fièvre ?

D007
Patient :
Je cours aux toilettes toute la journée.
Mots-clés :
court aux toilettes 
Symptômes détectés :
Diarrhée fréquente 
Question suivante :
Depuis quand cela a-t-il commencé ?

D008
Patient :
J'ai la diarrhée depuis hier.
Mots-clés :
diarrhée 
hier 
Symptômes détectés :
Diarrhée aiguë 
Question suivante :
Avez-vous vomi ?

D009
Patient :
Je vomis et j'ai la diarrhée.
Mots-clés :
vomis 
diarrhée 
Symptômes détectés :
Diarrhée 
Vomissements 
Urgence :
Modérée 
Question suivante :
Pouvez-vous boire des liquides ?

D010
Patient :
Je suis très fatigué à cause de la diarrhée.
Mots-clés :
fatigué 
diarrhée 
Symptômes détectés :
Fatigue 
Diarrhée 
Question suivante :
Buvez-vous suffisamment d'eau ?

D011
Patient :
Mon enfant refuse de boire.
Mots-clés :
enfant 
refuse boire 
Symptômes détectés :
Déshydratation possible 
Urgence :
Élevée 
Question suivante :
A-t-il également la diarrhée ou des vomissements ?

D012
Patient :
J'ai très soif.
Mots-clés :
très soif 
Symptômes détectés :
Déshydratation possible 
Question suivante :
Avez-vous la diarrhée ou des vomissements ?

D013
Patient :
Ma bouche est sèche.
Mots-clés :
bouche sèche 
Symptômes détectés :
Déshydratation 
Question suivante :
Avez-vous perdu beaucoup de liquides aujourd'hui ?

D014
Patient :
Je fais la diarrhée plusieurs fois par jour.
Mots-clés :
plusieurs fois 
Symptômes détectés :
Diarrhée fréquente 
Question suivante :
Combien de fois environ ?

D015
Patient :
Mon bébé a des selles liquides.
Mots-clés :
bébé 
selles liquides 
Symptômes détectés :
Diarrhée du nourrisson 
Question suivante :
Quel âge a votre bébé ?

D016
Patient :
Je me sens faible depuis la diarrhée.
Mots-clés :
faible 
diarrhée 
Symptômes détectés :
Fatigue 
Déshydratation possible 
Question suivante :
Pouvez-vous boire normalement ?

D017
Patient :
J'ai mangé quelque chose et maintenant j'ai la diarrhée.
Mots-clés :
mangé 
diarrhée 
Symptômes détectés :
Intoxication alimentaire possible 
Question suivante :
Qu'avez-vous mangé avant le début des symptômes ?

D018
Patient :
J'ai de la fièvre et la diarrhée.
Mots-clés :
fièvre 
diarrhée 
Symptômes détectés :
Infection digestive possible 
Question suivante :
Depuis combien de jours avez-vous ces symptômes ?

D019
Patient :
Je n'arrive pas à garder l'eau que je bois.
Mots-clés :
ne garde pas l'eau 
Symptômes détectés :
Vomissements 
Risque de déshydratation 
Urgence :
Élevée 
Question suivante :
Depuis combien de temps cela dure-t-il ?

D020
Patient :
Mon enfant a la diarrhée et vomit.
Mots-clés :
enfant 
diarrhée 
vomit 
Symptômes détectés :
Gastro-entérite possible 
Déshydratation possible 
Urgence :
Élevée 
Question suivante :
Quel âge a votre enfant et boit-il encore ?

Dictionnaire initial Diarrhée
diarrhée
selles liquides
caca comme de l'eau
souvent toilettes
court aux toilettes
mal au ventre
vomissements
très soif
bouche sèche
refuse boire
faible
fatigué
ne garde pas l'eau
bébé diarrhée
enfant diarrhée
Parfait. Continuons avec DIARRHÉE (D024 à D040).
DIARRHÉE (D024 à D040)
D024
Patient :
J'ai des crampes au ventre.
Mots-clés :
crampes au ventre 
Symptômes détectés :
Douleurs abdominales 
Trouble digestif 
Question suivante :
Avez-vous aussi la diarrhée ou des vomissements ?

D025
Patient :
Mes selles contiennent du sang.
Mots-clés :
sang dans les selles 
Symptômes détectés :
Diarrhée sanglante possible 
Dysenterie possible 
Urgence :
Élevée 
Question suivante :
Depuis quand voyez-vous du sang dans les selles ?

D026
Patient :
Mon enfant fait des selles avec du sang.
Mots-clés :
enfant 
sang dans les selles 
Symptômes détectés :
Dysenterie possible chez l'enfant 
Urgence :
Très élevée 
Question suivante :
Quel âge a votre enfant ?

D027
Patient :
J'ai beaucoup soif depuis ce matin.
Mots-clés :
beaucoup soif 
Symptômes détectés :
Déshydratation possible 
Question suivante :
Avez-vous la diarrhée ou des vomissements ?

D028
Patient :
Je n'urine presque plus.
Mots-clés :
n'urine plus 
Symptômes détectés :
Déshydratation sévère possible 
Urgence :
Élevée 
Question suivante :
Depuis combien de temps urinez-vous moins que d'habitude ?

D029
Patient :
Je me sens étourdi quand je me lève.
Mots-clés :
étourdi 
Symptômes détectés :
Déshydratation possible 
Faiblesse 
Question suivante :
Avez-vous perdu beaucoup de liquides ?

D030
Patient :
J'ai la diarrhée après chaque repas.
Mots-clés :
après chaque repas 
Symptômes détectés :
Diarrhée fréquente 
Question suivante :
Depuis combien de jours cela dure-t-il ?

D031
Patient :
Mon enfant refuse de manger.
Mots-clés :
refuse manger 
Symptômes détectés :
Maladie digestive possible 
Question suivante :
A-t-il aussi la diarrhée ou de la fièvre ?

D032
Patient :
J'ai perdu beaucoup de forces.
Mots-clés :
perdu forces 
Symptômes détectés :
Faiblesse importante 
Question suivante :
Avez-vous une diarrhée importante ?

D033
Patient :
Je vomis tout ce que je mange.
Mots-clés :
vomis tout 
Symptômes détectés :
Vomissements sévères 
Urgence :
Élevée 
Question suivante :
Pouvez-vous boire de l'eau sans vomir ?

D034
Patient :
Mes yeux semblent enfoncés.
Mots-clés :
yeux enfoncés 
Symptômes détectés :
Déshydratation sévère possible 
Urgence :
Très élevée 
Question suivante :
Avez-vous également une diarrhée importante ?

D035
Patient :
Je suis très faible à cause des selles liquides.
Mots-clés :
faible 
selles liquides 
Symptômes détectés :
Déshydratation possible 
Question suivante :
Combien de fois avez-vous eu des selles aujourd'hui ?

D036
Patient :
Mon bébé pleure sans larmes.
Mots-clés :
pleure sans larmes 
Symptômes détectés :
Déshydratation chez le nourrisson 
Urgence :
Très élevée 
Question suivante :
Votre bébé a-t-il aussi la diarrhée ?

D037
Patient :
J'ai une diarrhée très abondante.
Mots-clés :
diarrhée abondante 
Symptômes détectés :
Diarrhée sévère 
Question suivante :
Avez-vous des signes de déshydratation comme une grande soif ?

D038
Patient :
Plusieurs personnes à la maison ont la diarrhée.
Mots-clés :
plusieurs personnes 
maison 
Symptômes détectés :
Épidémie familiale possible 
Contamination alimentaire ou hydrique 
Question suivante :
Avez-vous tous consommé la même eau ou le même repas ?

D039
Patient :
J'ai bu de l'eau douteuse et maintenant je suis malade.
Mots-clés :
eau douteuse 
Symptômes détectés :
Infection digestive possible 
Choléra possible 
Question suivante :
Avez-vous une diarrhée aqueuse importante ?

D040
Patient :
J'ai la diarrhée et je ne tiens plus debout.
Mots-clés :
ne tient plus debout 
Symptômes détectés :
Faiblesse sévère 
Déshydratation grave possible 
Urgence :
Très élevée 
Question suivante :
Pouvez-vous boire de l'eau actuellement ?

Nouveaux mots-clés Diarrhée
crampes au ventre
sang dans les selles
beaucoup soif
n'urine plus
étourdi
après chaque repas
refuse manger
perdu forces
vomis tout
yeux enfoncés
pleure sans larmes
diarrhée abondante
plusieurs personnes malades
eau douteuse
ne tient plus debout
D041
Patient :
J'ai la diarrhée depuis une semaine.
Mots-clés :
une semaine 
diarrhée 
Symptômes détectés :
Diarrhée prolongée 
Question suivante :
Avez-vous consulté un centre de santé ?

D042
Patient :
Cela fait plusieurs jours que je fais des selles liquides.
Mots-clés :
plusieurs jours 
selles liquides 
Symptômes détectés :
Diarrhée persistante 
Question suivante :
Avez-vous perdu du poids ?

D043
Patient :
Je vais aux toilettes plus de dix fois par jour.
Mots-clés :
dix fois 
toilettes 
Symptômes détectés :
Diarrhée sévère 
Urgence :
Élevée 
Question suivante :
Buvez-vous suffisamment d'eau ou de solution de réhydratation ?

D044
Patient :
Mon enfant a la bouche très sèche.
Mots-clés :
bouche sèche 
enfant 
Symptômes détectés :
Déshydratation chez l'enfant 
Urgence :
Élevée 
Question suivante :
A-t-il aussi des selles liquides ?

D045
Patient :
Mon bébé dort beaucoup et a la diarrhée.
Mots-clés :
dort beaucoup 
bébé 
diarrhée 
Symptômes détectés :
Déshydratation possible 
Urgence :
Élevée 
Question suivante :
Réagit-il normalement quand vous l'appelez ou le stimulez ?

D046
Patient :
J'ai perdu l'appétit depuis que la diarrhée a commencé.
Mots-clés :
perdu appétit 
Symptômes détectés :
Perte d'appétit 
Trouble digestif 
Question suivante :
Depuis combien de jours ?

D047
Patient :
J'ai des selles vertes.
Mots-clés :
selles vertes 
Symptômes détectés :
Modification des selles 
Question suivante :
Avez-vous également de la diarrhée ou de la fièvre ?

D048
Patient :
Mes selles ont une mauvaise odeur.
Mots-clés :
mauvaise odeur 
Symptômes détectés :
Infection digestive possible 
Question suivante :
Depuis quand observez-vous cela ?

D049
Patient :
J'ai des douleurs avant chaque selle.
Mots-clés :
douleurs avant selle 
Symptômes détectés :
Crampes abdominales 
Question suivante :
Les selles sont-elles liquides ?

D050
Patient :
Je fais des selles même pendant la nuit.
Mots-clés :
pendant la nuit 
Symptômes détectés :
Diarrhée importante 
Question suivante :
Depuis combien de jours cela dure-t-il ?

D051
Patient :
Mon enfant a les yeux enfoncés et ne joue plus.
Mots-clés :
yeux enfoncés 
ne joue plus 
Symptômes détectés :
Déshydratation sévère 
Urgence :
Très élevée 
Question suivante :
Peut-il encore boire ou téter ?

D052
Patient :
J'ai la diarrhée après avoir mangé au marché.
Mots-clés :
mangé au marché 
Symptômes détectés :
Intoxication alimentaire possible 
Question suivante :
D'autres personnes ont-elles mangé le même repas ?

D053
Patient :
Mon enfant vomit et refuse le sein.
Mots-clés :
refuse le sein 
vomit 
Symptômes détectés :
Déshydratation grave possible 
Urgence :
Très élevée 
Question suivante :
Quel âge a votre bébé ?

D054
Patient :
Je me sens très faible quand je marche.
Mots-clés :
faible quand marche 
Symptômes détectés :
Déshydratation 
Faiblesse 
Question suivante :
Avez-vous des selles liquides fréquentes ?

D055
Patient :
J'ai la diarrhée depuis mon retour de voyage.
Mots-clés :
retour de voyage 
Symptômes détectés :
Infection digestive possible 
Question suivante :
Où avez-vous voyagé récemment ?

D056
Patient :
Je n'ai plus de force du tout.
Mots-clés :
plus de force 
Symptômes détectés :
Faiblesse sévère 
Urgence :
Élevée 
Question suivante :
Avez-vous une diarrhée importante ou des vomissements ?

D057
Patient :
Mes selles ressemblent à de l'eau de riz.
Mots-clés :
eau de riz 
Symptômes détectés :
Choléra possible 
Urgence :
Très élevée 
Question suivante :
Combien de selles avez-vous eues aujourd'hui ?

D058
Patient :
Toute ma famille a commencé la diarrhée.
Mots-clés :
toute ma famille 
Symptômes détectés :
Foyer épidémique possible 
Question suivante :
Avez-vous tous utilisé la même source d'eau ?

D059
Patient :
Je bois mais la soif ne passe pas.
Mots-clés :
soif ne passe pas 
Symptômes détectés :
Déshydratation 
Urgence :
Élevée 
Question suivante :
Avez-vous aussi des vomissements ?

D060
Patient :
Mon enfant est très mou et a la diarrhée.
Mots-clés :
très mou 
diarrhée 
Symptômes détectés :
Déshydratation sévère chez l'enfant 
Urgence :
Très élevée 
Question suivante :
Réagit-il normalement lorsqu'on lui parle ?

Nouveaux mots-clés Diarrhée
une semaine diarrhée
dix fois par jour
bouche très sèche
dort beaucoup
selles vertes
mauvaise odeur
douleurs avant selle
ne joue plus
mangé au marché
refuse le sein
retour de voyage
plus de force
eau de riz
toute ma famille
soif ne passe pas
très mou
D061
Patient :
J'ai la diarrhée depuis deux semaines.
Mots-clés :
deux semaines 
diarrhée 
Symptômes détectés :
Diarrhée prolongée 
Question suivante :
Avez-vous perdu du poids récemment ?

D062
Patient :
Je maigris depuis que j'ai la diarrhée.
Mots-clés :
maigris 
Symptômes détectés :
Perte de poids 
Question suivante :
Depuis combien de temps avez-vous la diarrhée ?

D063
Patient :
Mon enfant a la diarrhée tous les jours.
Mots-clés :
enfant 
tous les jours 
Symptômes détectés :
Diarrhée chronique possible 
Question suivante :
Depuis combien de semaines cela dure-t-il ?

D064
Patient :
Je n'ai plus envie de manger.
Mots-clés :
plus envie manger 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Avez-vous aussi la diarrhée ou des vomissements ?

D065
Patient :
Chaque fois que je mange, je cours aux toilettes.
Mots-clés :
mange 
cours aux toilettes 
Symptômes détectés :
Diarrhée après repas 
Question suivante :
Depuis quand cela se produit-il ?

D066
Patient :
J'ai la diarrhée surtout la nuit.
Mots-clés :
surtout la nuit 
Symptômes détectés :
Diarrhée nocturne 
Question suivante :
Depuis combien de jours ?

D067
Patient :
Mon bébé a perdu du poids.
Mots-clés :
bébé 
perdu poids 
Symptômes détectés :
Malnutrition possible 
Diarrhée chronique possible 
Question suivante :
A-t-il également des selles liquides fréquentes ?

D068
Patient :
J'ai mal au ventre avant d'aller aux toilettes.
Mots-clés :
mal ventre avant toilettes 
Symptômes détectés :
Crampes intestinales 
Question suivante :
Les selles sont-elles liquides ?

D069
Patient :
Je suis très faible et j'ai la diarrhée depuis longtemps.
Mots-clés :
faible 
depuis longtemps 
Symptômes détectés :
Diarrhée chronique 
Déshydratation possible 
Question suivante :
Depuis combien de semaines ou mois ?

D070
Patient :
Je fais des selles mousseuses.
Mots-clés :
selles mousseuses 
Symptômes détectés :
Trouble digestif 
Question suivante :
Depuis quand observez-vous cela ?

D071
Patient :
Mon enfant ne veut plus jouer.
Mots-clés :
ne veut plus jouer 
Symptômes détectés :
Faiblesse chez l'enfant 
Question suivante :
A-t-il de la diarrhée ou de la fièvre ?

D072
Patient :
J'ai la diarrhée après avoir bu de l'eau du lac.
Mots-clés :
eau du lac 
Symptômes détectés :
Infection hydrique possible 
Question suivante :
Depuis combien de temps après avoir bu cette eau les symptômes ont-ils commencé ?

D073
Patient :
J'ai des selles jaunes très liquides.
Mots-clés :
selles jaunes 
Symptômes détectés :
Diarrhée 
Question suivante :
Avez-vous aussi de la fièvre ?

D074
Patient :
Mon enfant a la diarrhée et semble très fatigué.
Mots-clés :
enfant 
très fatigué 
Symptômes détectés :
Déshydratation possible 
Urgence :
Élevée 
Question suivante :
Boit-il encore normalement ?

D075
Patient :
J'ai des douleurs et du sang dans les selles.
Mots-clés :
douleurs 
sang selles 
Symptômes détectés :
Dysenterie possible 
Urgence :
Élevée 
Question suivante :
Depuis combien de jours voyez-vous du sang ?

D076
Patient :
Je vais à la selle immédiatement après avoir mangé.
Mots-clés :
immédiatement après manger 
Symptômes détectés :
Trouble digestif 
Question suivante :
Depuis quand cela dure-t-il ?

D077
Patient :
Je suis âgé et j'ai la diarrhée depuis plusieurs jours.
Mots-clés :
âgé 
plusieurs jours 
Symptômes détectés :
Diarrhée chez personne âgée 
Question suivante :
Buvez-vous suffisamment d'eau ?

D078
Patient :
Je me sens déshydraté.
Mots-clés :
déshydraté 
Symptômes détectés :
Déshydratation 
Question suivante :
Avez-vous très soif ou la bouche sèche ?

D079
Patient :
J'ai la tête qui tourne depuis la diarrhée.
Mots-clés :
tête tourne 
Symptômes détectés :
Vertiges 
Déshydratation possible 
Question suivante :
Buvez-vous suffisamment de liquides ?

D080
Patient :
Je n'arrive plus à travailler à cause de la diarrhée.
Mots-clés :
plus travailler 
Symptômes détectés :
Faiblesse importante 
Question suivante :
Depuis combien de temps êtes-vous malade ?

Nouveaux mots-clés Diarrhée
deux semaines
maigris
tous les jours
plus envie manger
diarrhée surtout la nuit
perdu poids
selles mousseuses
eau du lac
selles jaunes
immédiatement après manger
personne âgée
déshydraté
tête tourne
plus travailler
D081
Patient :
Je fais la diarrhée depuis presque un mois.
Mots-clés :
un mois 
diarrhée 
Symptômes détectés :
Diarrhée chronique 
Question suivante :
Avez-vous perdu du poids ou de l'appétit ?

D082
Patient :
Je suis très maigre depuis cette maladie.
Mots-clés :
très maigre 
Symptômes détectés :
Perte de poids 
Question suivante :
Depuis combien de temps avez-vous la diarrhée ?

D083
Patient :
Mes selles sont blanches.
Mots-clés :
selles blanches 
Symptômes détectés :
Anomalie des selles 
Question suivante :
Depuis quand observez-vous cela ?

D084
Patient :
Mon enfant a la diarrhée depuis plusieurs semaines.
Mots-clés :
enfant 
plusieurs semaines 
Symptômes détectés :
Diarrhée chronique chez l'enfant 
Urgence :
Élevée 
Question suivante :
A-t-il perdu du poids ?

D085
Patient :
Je ne peux rien manger sans courir aux toilettes.
Mots-clés :
rien manger 
courir toilettes 
Symptômes détectés :
Diarrhée sévère 
Question suivante :
Depuis combien de temps cela dure-t-il ?

D086
Patient :
Mon bébé est très faible et a la diarrhée.
Mots-clés :
bébé faible 
Symptômes détectés :
Déshydratation sévère possible 
Urgence :
Très élevée 
Question suivante :
Boit-il encore du lait ou de l'eau ?

D087
Patient :
J'ai du mucus dans les selles.
Mots-clés :
mucus selles 
Symptômes détectés :
Infection intestinale possible 
Question suivante :
Voyez-vous aussi du sang dans les selles ?

D088
Patient :
J'ai une diarrhée très brutale.
Mots-clés :
diarrhée brutale 
Symptômes détectés :
Diarrhée aiguë 
Question suivante :
Quand les symptômes ont-ils commencé ?

D089
Patient :
Mon enfant est somnolent et a la diarrhée.
Mots-clés :
somnolent 
diarrhée 
Symptômes détectés :
Déshydratation sévère 
Urgence :
Très élevée 
Question suivante :
Réagit-il lorsqu'on l'appelle ?

D090
Patient :
Je fais des selles liquides toute la journée.
Mots-clés :
toute la journée 
Symptômes détectés :
Diarrhée sévère 
Question suivante :
Combien de fois environ aujourd'hui ?

D091
Patient :
J'ai la diarrhée après chaque verre de lait.
Mots-clés :
après lait 
Symptômes détectés :
Intolérance alimentaire possible 
Question suivante :
Cela arrive-t-il uniquement avec le lait ?

D092
Patient :
Je me sens très faible et j'ai les lèvres sèches.
Mots-clés :
lèvres sèches 
faible 
Symptômes détectés :
Déshydratation 
Question suivante :
Avez-vous la diarrhée ou des vomissements ?

D093
Patient :
Toute l'école est touchée par la diarrhée.
Mots-clés :
école 
touchée 
Symptômes détectés :
Épidémie possible 
Question suivante :
Plusieurs élèves utilisent-ils la même source d'eau ?

D094
Patient :
Je n'ai presque plus d'urine.
Mots-clés :
presque plus urine 
Symptômes détectés :
Déshydratation sévère 
Urgence :
Très élevée 
Question suivante :
Depuis combien de temps urinez-vous si peu ?

D095
Patient :
Mon enfant a la diarrhée et les yeux très enfoncés.
Mots-clés :
yeux très enfoncés 
Symptômes détectés :
Déshydratation grave 
Urgence :
Très élevée 
Question suivante :
Peut-il encore boire ou manger ?

D096
Patient :
Je suis malade depuis avoir mangé du poisson.
Mots-clés :
mangé poisson 
Symptômes détectés :
Intoxication alimentaire possible 
Question suivante :
Avez-vous de la diarrhée, des vomissements ou les deux ?

D097
Patient :
J'ai la diarrhée et des douleurs très fortes.
Mots-clés :
douleurs très fortes 
Symptômes détectés :
Infection digestive sévère possible 
Urgence :
Élevée 
Question suivante :
Où ressentez-vous principalement la douleur ?

D098
Patient :
Mon enfant ne boit plus du tout.
Mots-clés :
ne boit plus 
Symptômes détectés :
Déshydratation sévère 
Urgence :
Très élevée 
Question suivante :
A-t-il la diarrhée ou des vomissements ?

D099
Patient :
Je pense que c'est le choléra.
Mots-clés :
choléra 
Symptômes détectés :
Suspicion de choléra 
Urgence :
Très élevée 
Question suivante :
Avez-vous des selles très abondantes comme de l'eau de riz ?

D100
Patient :
Je fais seulement de l'eau depuis ce matin et je suis très faible.
Mots-clés :
seulement de l'eau 
très faible 
Symptômes détectés :
Diarrhée aqueuse sévère 
Déshydratation grave possible 
Urgence :
Très élevée 
Question suivante :
Pouvez-vous encore boire et garder les liquides ?

Catégorie terminée
✅ DIARRHÉE : D001 à D100 complétés
Mots-clés majeurs collectés
diarrhée
selles liquides
caca comme de l'eau
eau de riz
choléra
sang dans les selles
mucus selles
bouche sèche
lèvres sèches
très soif
déshydraté
yeux enfoncés
ne boit plus
refuse boire
refuse le sein
vomissements
faible
somnolent
n'urine plus
presque plus urine
eau douteuse
eau du lac
intoxication alimentaire
maigris
perdu poids















E001
Parent :
Mon enfant a de la fièvre.
Mots-clés :
enfant 
fièvre 
Symptômes détectés :
Fièvre chez l'enfant 
Question suivante :
Quel âge a votre enfant ?

E002
Parent :
Mon bébé chauffe beaucoup.
Mots-clés :
bébé 
chauffe 
Symptômes détectés :
Fièvre 
Question suivante :
Depuis combien de temps votre bébé a-t-il de la fièvre ?

E003
Parent :
Mon enfant tousse.
Mots-clés :
tousse 
Symptômes détectés :
Toux 
Question suivante :
Depuis combien de jours tousse-t-il ?

E004
Parent :
Mon enfant respire difficilement.
Mots-clés :
respire difficilement 
Symptômes détectés :
Difficulté respiratoire 
Urgence :
Élevée 
Question suivante :
Quel âge a votre enfant ?

E005
Parent :
Mon bébé refuse le sein.
Mots-clés :
refuse le sein 
Symptômes détectés :
Difficulté d'alimentation 
Urgence :
Élevée 
Question suivante :
Quel âge a votre bébé ?

E006
Parent :
Mon enfant vomit.
Mots-clés :
vomit 
Symptômes détectés :
Vomissements 
Question suivante :
Depuis quand vomit-il ?

E007
Parent :
Mon enfant a la diarrhée.
Mots-clés :
diarrhée 
Symptômes détectés :
Diarrhée 
Question suivante :
Quel âge a votre enfant ?

E008
Parent :
Mon enfant ne mange plus.
Mots-clés :
ne mange plus 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Depuis combien de jours refuse-t-il de manger ?

E009
Parent :
Mon bébé pleure beaucoup.
Mots-clés :
pleure beaucoup 
Symptômes détectés :
Irritabilité 
Question suivante :
A-t-il de la fièvre ou semble-t-il avoir mal quelque part ?

E010
Parent :
Mon enfant dort toute la journée.
Mots-clés :
dort toute la journée 
Symptômes détectés :
Somnolence 
Question suivante :
Réagit-il normalement quand vous l'appelez ?

E011
Parent :
Mon enfant est très faible.
Mots-clés :
très faible 
Symptômes détectés :
Faiblesse importante 
Urgence :
Élevée 
Question suivante :
Peut-il encore boire ou manger ?

E012
Parent :
Mon bébé ne joue plus.
Mots-clés :
ne joue plus 
Symptômes détectés :
Diminution de l'activité 
Question suivante :
A-t-il de la fièvre ou d'autres symptômes ?

E013
Parent :
Mon enfant a le nez qui coule.
Mots-clés :
nez coule 
Symptômes détectés :
Rhume possible 
Question suivante :
A-t-il également de la fièvre ou une toux ?

E014
Parent :
Mon enfant a mal à la gorge.
Mots-clés :
mal gorge 
Symptômes détectés :
Gorge douloureuse 
Question suivante :
A-t-il de la fièvre ?

E015
Parent :
Mon enfant a des boutons sur le corps.
Mots-clés :
boutons 
corps 
Symptômes détectés :
Éruption cutanée 
Question suivante :
Depuis quand les boutons sont-ils apparus ?

E016
Parent :
Mon enfant se gratte beaucoup.
Mots-clés :
se gratte 
Symptômes détectés :
Démangeaisons 
Question suivante :
Voyez-vous des boutons ou une éruption sur la peau ?

E017
Parent :
Mon bébé a les yeux rouges.
Mots-clés :
yeux rouges 
Symptômes détectés :
Irritation ou infection oculaire 
Question suivante :
Les yeux coulent-ils ou contiennent-ils du pus ?

E018
Parent :
Mon enfant a mal à l'oreille.
Mots-clés :
mal oreille 
Symptômes détectés :
Douleur d'oreille 
Question suivante :
Depuis combien de temps a-t-il mal ?

E019
Parent :
Mon enfant a des convulsions.
Mots-clés :
convulsions 
Symptômes détectés :
Convulsions 
Urgence :
Très élevée 
Question suivante :
Les convulsions sont-elles en cours actuellement ?

E020
Parent :
Mon enfant a perdu connaissance.
Mots-clés :
perdu connaissance 
Symptômes détectés :
Altération de conscience 
Urgence :
Très élevée 
Question suivante :
Respire-t-il normalement actuellement ?

Dictionnaire initial Santé de l'enfant
enfant fièvre
bébé chauffe
toux
respire difficilement
refuse le sein
vomit
diarrhée
ne mange plus
pleure beaucoup
dort toute la journée
très faible
ne joue plus
nez coule
mal gorge
boutons corps
se gratte
yeux rouges
mal oreille
convulsions
perdu connaissance
E021
Parent :
Mon enfant respire vite.
Mots-clés :
respire vite 
Symptômes détectés :
Pneumonie possible 
Urgence :
Élevée 
Question suivante :
Quel âge a votre enfant ?

E022
Parent :
Sa poitrine se creuse quand il respire.
Mots-clés :
poitrine se creuse 
Symptômes détectés :
Détresse respiratoire 
Urgence :
Très élevée 
Question suivante :
Respire-t-il difficilement en ce moment ?

E023
Parent :
Mon enfant tousse depuis deux semaines.
Mots-clés :
tousse 
deux semaines 
Symptômes détectés :
Toux prolongée 
Question suivante :
A-t-il aussi de la fièvre ou perdu du poids ?

E024
Parent :
Mon enfant a beaucoup de fièvre et tousse.
Mots-clés :
fièvre 
tousse 
Symptômes détectés :
Infection respiratoire possible 
Question suivante :
Depuis combien de jours présente-t-il ces symptômes ?

E025
Parent :
Mon enfant est très maigre.
Mots-clés :
très maigre 
Symptômes détectés :
Malnutrition possible 
Question suivante :
Mange-t-il normalement ?

E026
Parent :
Mon enfant a les bras très fins.
Mots-clés :
bras fins 
Symptômes détectés :
Malnutrition possible 
Question suivante :
A-t-il perdu du poids récemment ?

E027
Parent :
Les pieds de mon enfant sont gonflés.
Mots-clés :
pieds gonflés 
Symptômes détectés :
Malnutrition sévère possible 
Urgence :
Élevée 
Question suivante :
Depuis quand les pieds sont-ils gonflés ?

E028
Parent :
Mon enfant ne grandit pas bien.
Mots-clés :
ne grandit pas 
Symptômes détectés :
Retard de croissance possible 
Question suivante :
Quel âge a votre enfant ?

E029
Parent :
Mon bébé est très petit pour son âge.
Mots-clés :
petit pour son âge 
Symptômes détectés :
Retard de croissance possible 
Question suivante :
Quel âge a votre bébé ?

E030
Parent :
Mon enfant a des plaques blanches dans la bouche.
Mots-clés :
plaques blanches bouche 
Symptômes détectés :
Infection buccale possible 
Question suivante :
Depuis combien de temps observez-vous cela ?

E031
Parent :
Mon enfant a des boutons partout avec de la fièvre.
Mots-clés :
boutons partout 
fièvre 
Symptômes détectés :
Rougeole ou autre maladie éruptive possible 
Urgence :
Élevée 
Question suivante :
Depuis quand les boutons sont-ils apparus ?

E032
Parent :
Ses yeux sont rouges et il a des boutons.
Mots-clés :
yeux rouges 
boutons 
Symptômes détectés :
Rougeole possible 
Question suivante :
A-t-il également de la fièvre ?

E033
Parent :
Mon enfant n'a jamais été vacciné.
Mots-clés :
jamais vacciné 
Intention :
Vaccination 
Question suivante :
Quel âge a votre enfant ?

E034
Parent :
J'ai perdu le carnet de vaccination.
Mots-clés :
carnet vaccination 
Intention :
Suivi vaccinal 
Question suivante :
Quel âge a votre enfant ?

E035
Parent :
Mon enfant a raté plusieurs vaccins.
Mots-clés :
raté vaccins 
Intention :
Vaccination incomplète 
Question suivante :
Savez-vous quels vaccins ont été manqués ?

E036
Parent :
Mon enfant a le paludisme.
Mots-clés :
paludisme 
Symptômes détectés :
Paludisme suspecté ou confirmé 
Question suivante :
A-t-il actuellement de la fièvre ?

E037
Parent :
Mon enfant tremble avec la fièvre.
Mots-clés :
tremble 
fièvre 
Symptômes détectés :
Fièvre avec frissons 
Question suivante :
Depuis combien de temps a-t-il de la fièvre ?

E038
Parent :
Mon enfant refuse de jouer et reste couché.
Mots-clés :
reste couché 
Symptômes détectés :
Faiblesse importante 
Urgence :
Élevée 
Question suivante :
Boit-il ou mange-t-il normalement ?

E039
Parent :
Mon bébé pleure quand je le touche.
Mots-clés :
pleure quand touche 
Symptômes détectés :
Douleur possible 
Question suivante :
Où pensez-vous qu'il a mal ?

E040
Parent :
Mon enfant est souvent malade.
Mots-clés :
souvent malade 
Symptômes détectés :
Maladies répétées 
Question suivante :
Quels problèmes de santé revient le plus souvent ?

Nouveaux mots-clés Santé de l'enfant
respire vite
poitrine se creuse
toux deux semaines
très maigre
bras fins
pieds gonflés
ne grandit pas
petit pour son âge
plaques blanches bouche
boutons partout
jamais vacciné
carnet vaccination
raté vaccins
paludisme enfant
tremble avec fièvre
reste couché
pleure quand touche
souvent malade
E041
Parent :
Mon enfant a fait une crise avec la fièvre.
Mots-clés :
crise 
fièvre 
Symptômes détectés :
Convulsion fébrile possible 
Urgence :
Très élevée 
Question suivante :
La crise est-elle terminée actuellement ?

E042
Parent :
Mon enfant roule les yeux.
Mots-clés :
roule les yeux 
Symptômes détectés :
Convulsion possible 
Urgence :
Très élevée 
Question suivante :
Est-il conscient actuellement ?

E043
Parent :
Mon enfant serre les dents pendant la crise.
Mots-clés :
serre les dents 
Symptômes détectés :
Convulsion 
Urgence :
Très élevée 
Question suivante :
Combien de temps la crise a-t-elle duré ?

E044
Parent :
Mon enfant a mal à l'oreille et pleure.
Mots-clés :
mal oreille 
pleure 
Symptômes détectés :
Infection de l'oreille possible 
Question suivante :
A-t-il de la fièvre ?

E045
Parent :
Du liquide sort de son oreille.
Mots-clés :
liquide oreille 
Symptômes détectés :
Écoulement de l'oreille 
Question suivante :
Depuis combien de jours observez-vous cet écoulement ?

E046
Parent :
Mon enfant entend moins bien.
Mots-clés :
entend moins 
Symptômes détectés :
Trouble de l'audition possible 
Question suivante :
A-t-il eu récemment une douleur ou un écoulement de l'oreille ?

E047
Parent :
Mon enfant se gratte l'anus.
Mots-clés :
gratte anus 
Symptômes détectés :
Parasites intestinaux possibles 
Question suivante :
Les démangeaisons sont-elles surtout la nuit ?

E048
Parent :
Mon enfant a des vers dans les selles.
Mots-clés :
vers selles 
Symptômes détectés :
Parasitose intestinale 
Question suivante :
Depuis quand avez-vous observé cela ?

E049
Parent :
Son ventre est gonflé.
Mots-clés :
ventre gonflé 
Symptômes détectés :
Parasitose ou malnutrition possible 
Question suivante :
A-t-il aussi perdu du poids ?

E050
Parent :
Mon enfant mange de la terre.
Mots-clés :
mange terre 
Symptômes détectés :
Carence nutritionnelle possible 
Question suivante :
Quel âge a votre enfant ?

E051
Parent :
Mon enfant est très pâle.
Mots-clés :
très pâle 
Symptômes détectés :
Anémie possible 
Urgence :
Élevée 
Question suivante :
Est-il également fatigué ou essoufflé ?

E052
Parent :
Ses lèvres sont pâles.
Mots-clés :
lèvres pâles 
Symptômes détectés :
Anémie possible 
Question suivante :
Depuis quand remarquez-vous cela ?

E053
Parent :
Mon enfant se fatigue vite.
Mots-clés :
fatigue vite 
Symptômes détectés :
Faiblesse ou anémie possible 
Question suivante :
A-t-il de la fièvre ou semble-t-il pâle ?

E054
Parent :
Mon bébé respire rapidement.
Mots-clés :
respire rapidement 
Symptômes détectés :
Détresse respiratoire possible 
Urgence :
Élevée 
Question suivante :
Quel âge a votre bébé ?

E055
Parent :
Mon enfant boit beaucoup d'eau.
Mots-clés :
boit beaucoup 
Symptômes détectés :
Soif importante 
Question suivante :
A-t-il aussi perdu du poids ou urine-t-il souvent ?

E056
Parent :
Mon enfant urine très souvent.
Mots-clés :
urine souvent 
Symptômes détectés :
Trouble métabolique possible 
Question suivante :
Boit-il également beaucoup d'eau ?

E057
Parent :
Mon enfant mouille encore son lit.
Mots-clés :
mouille lit 
Symptômes détectés :
Énurésie 
Question suivante :
Quel âge a votre enfant ?

E058
Parent :
Mon enfant a une grosse plaie.
Mots-clés :
grosse plaie 
Symptômes détectés :
Blessure 
Question suivante :
Comment cette plaie est-elle survenue ?

E059
Parent :
Mon enfant s'est brûlé.
Mots-clés :
brûlé 
Symptômes détectés :
Brûlure 
Urgence :
Variable selon la gravité 
Question suivante :
Quelle partie du corps a été brûlée ?

E060
Parent :
Mon enfant a été mordu par un chien.
Mots-clés :
mordu par chien 
Symptômes détectés :
Morsure animale 
Urgence :
Élevée 
Question suivante :
Quand la morsure a-t-elle eu lieu ?

Nouveaux mots-clés Santé de l'enfant
roule les yeux
serre les dents
liquide oreille
entend moins
gratte anus
vers selles
ventre gonflé
mange terre
très pâle
lèvres pâles
fatigue vite
boit beaucoup
urine souvent
mouille lit
grosse plaie
brûlé
mordu par chien
E061
Parent :
Mon enfant a avalé du pétrole.
Mots-clés :
avalé pétrole 
Symptômes détectés :
Intoxication possible 
Urgence :
Très élevée 
Question suivante :
Quand l'enfant a-t-il avalé le pétrole ?

E062
Parent :
Mon enfant a bu un produit de nettoyage.
Mots-clés :
produit nettoyage 
Symptômes détectés :
Intoxication chimique 
Urgence :
Très élevée 
Question suivante :
Quel produit a-t-il bu exactement ?

E063
Parent :
Mon enfant a avalé un médicament.
Mots-clés :
avalé médicament 
Symptômes détectés :
Surdosage ou intoxication possible 
Urgence :
Élevée 
Question suivante :
Savez-vous quel médicament et quelle quantité ?

E064
Parent :
Mon enfant a avalé une pièce de monnaie.
Mots-clés :
pièce de monnaie 
Symptômes détectés :
Corps étranger avalé 
Question suivante :
A-t-il des difficultés à respirer ou à avaler ?

E065
Parent :
Mon enfant a avalé un objet.
Mots-clés :
avalé objet 
Symptômes détectés :
Corps étranger digestif possible 
Question suivante :
Quel objet a été avalé ?

E066
Parent :
Mon enfant s'étouffe.
Mots-clés :
s'étouffe 
Symptômes détectés :
Obstruction des voies respiratoires 
Urgence :
Très élevée 
Question suivante :
L'enfant peut-il encore respirer ou parler ?

E067
Parent :
Mon enfant a quelque chose coincé dans le nez.
Mots-clés :
coincé dans le nez 
Symptômes détectés :
Corps étranger nasal 
Question suivante :
Savez-vous quel objet est coincé ?

E068
Parent :
Mon enfant a quelque chose dans l'oreille.
Mots-clés :
dans l'oreille 
Symptômes détectés :
Corps étranger auriculaire 
Question suivante :
Depuis combien de temps ?

E069
Parent :
Mon enfant ne voit pas bien.
Mots-clés :
ne voit pas bien 
Symptômes détectés :
Trouble visuel 
Question suivante :
Ce problème est-il apparu soudainement ou progressivement ?

E070
Parent :
Son œil est rouge et gonflé.
Mots-clés :
œil rouge 
œil gonflé 
Symptômes détectés :
Infection ou inflammation oculaire 
Question suivante :
Y a-t-il un écoulement de l'œil ?

E071
Parent :
Mon enfant a reçu un coup à la tête.
Mots-clés :
coup à la tête 
Symptômes détectés :
Traumatisme crânien 
Urgence :
Élevée 
Question suivante :
A-t-il perdu connaissance ou vomi après le choc ?

E072
Parent :
Mon enfant est tombé d'un arbre.
Mots-clés :
tombé arbre 
Symptômes détectés :
Traumatisme possible 
Urgence :
Élevée 
Question suivante :
Peut-il bouger normalement ?

E073
Parent :
Mon enfant boite après une chute.
Mots-clés :
boite 
chute 
Symptômes détectés :
Blessure ou fracture possible 
Question suivante :
Où a-t-il mal exactement ?

E074
Parent :
Son bras est gonflé après une chute.
Mots-clés :
bras gonflé 
Symptômes détectés :
Fracture ou entorse possible 
Question suivante :
Peut-il encore bouger le bras ?

E075
Parent :
Mon enfant a été mordu par un serpent.
Mots-clés :
mordu serpent 
Symptômes détectés :
Morsure de serpent 
Urgence :
Très élevée 
Question suivante :
Quand la morsure est-elle survenue ?

E076
Parent :
Mon enfant a été piqué par un scorpion.
Mots-clés :
piqué scorpion 
Symptômes détectés :
Piqûre venimeuse possible 
Urgence :
Élevée 
Question suivante :
Où se situe la piqûre ?

E077
Parent :
Mon enfant a été attaqué par des abeilles.
Mots-clés :
abeilles 
Symptômes détectés :
Multiples piqûres 
Question suivante :
A-t-il des difficultés à respirer ou un gonflement important ?

E078
Parent :
Mon enfant saigne beaucoup.
Mots-clés :
saigne beaucoup 
Symptômes détectés :
Hémorragie 
Urgence :
Très élevée 
Question suivante :
D'où provient le saignement ?

E079
Parent :
Mon enfant a une plaie profonde.
Mots-clés :
plaie profonde 
Symptômes détectés :
Blessure grave 
Urgence :
Élevée 
Question suivante :
La plaie continue-t-elle à saigner ?

E080
Parent :
Mon enfant a perdu une dent après une chute.
Mots-clés :
perdu dent 
Symptômes détectés :
Traumatisme dentaire 
Question suivante :
S'agit-il d'une dent de lait ou d'une dent définitive ?

Nouveaux mots-clés Santé de l'enfant
avalé pétrole
produit nettoyage
avalé médicament
pièce de monnaie
avalé objet
s'étouffe
coincé dans le nez
dans l'oreille
ne voit pas bien
œil rouge gonflé
coup à la tête
tombé arbre
boite après chute
bras gonflé
mordu serpent
piqué scorpion
attaqué par des abeilles
saigne beaucoup
plaie profonde
perdu dent
E061
Parent :
Mon enfant a avalé du pétrole.
Mots-clés :
avalé pétrole 
Symptômes détectés :
Intoxication possible 
Urgence :
Très élevée 
Question suivante :
Quand l'enfant a-t-il avalé le pétrole ?

E062
Parent :
Mon enfant a bu un produit de nettoyage.
Mots-clés :
produit nettoyage 
Symptômes détectés :
Intoxication chimique 
Urgence :
Très élevée 
Question suivante :
Quel produit a-t-il bu exactement ?

E063
Parent :
Mon enfant a avalé un médicament.
Mots-clés :
avalé médicament 
Symptômes détectés :
Surdosage ou intoxication possible 
Urgence :
Élevée 
Question suivante :
Savez-vous quel médicament et quelle quantité ?

E064
Parent :
Mon enfant a avalé une pièce de monnaie.
Mots-clés :
pièce de monnaie 
Symptômes détectés :
Corps étranger avalé 
Question suivante :
A-t-il des difficultés à respirer ou à avaler ?

E065
Parent :
Mon enfant a avalé un objet.
Mots-clés :
avalé objet 
Symptômes détectés :
Corps étranger digestif possible 
Question suivante :
Quel objet a été avalé ?

E066
Parent :
Mon enfant s'étouffe.
Mots-clés :
s'étouffe 
Symptômes détectés :
Obstruction des voies respiratoires 
Urgence :
Très élevée 
Question suivante :
L'enfant peut-il encore respirer ou parler ?

E067
Parent :
Mon enfant a quelque chose coincé dans le nez.
Mots-clés :
coincé dans le nez 
Symptômes détectés :
Corps étranger nasal 
Question suivante :
Savez-vous quel objet est coincé ?

E068
Parent :
Mon enfant a quelque chose dans l'oreille.
Mots-clés :
dans l'oreille 
Symptômes détectés :
Corps étranger auriculaire 
Question suivante :
Depuis combien de temps ?

E069
Parent :
Mon enfant ne voit pas bien.
Mots-clés :
ne voit pas bien 
Symptômes détectés :
Trouble visuel 
Question suivante :
Ce problème est-il apparu soudainement ou progressivement ?

E070
Parent :
Son œil est rouge et gonflé.
Mots-clés :
œil rouge 
œil gonflé 
Symptômes détectés :
Infection ou inflammation oculaire 
Question suivante :
Y a-t-il un écoulement de l'œil ?

E071
Parent :
Mon enfant a reçu un coup à la tête.
Mots-clés :
coup à la tête 
Symptômes détectés :
Traumatisme crânien 
Urgence :
Élevée 
Question suivante :
A-t-il perdu connaissance ou vomi après le choc ?

E072
Parent :
Mon enfant est tombé d'un arbre.
Mots-clés :
tombé arbre 
Symptômes détectés :
Traumatisme possible 
Urgence :
Élevée 
Question suivante :
Peut-il bouger normalement ?

E073
Parent :
Mon enfant boite après une chute.
Mots-clés :
boite 
chute 
Symptômes détectés :
Blessure ou fracture possible 
Question suivante :
Où a-t-il mal exactement ?

E074
Parent :
Son bras est gonflé après une chute.
Mots-clés :
bras gonflé 
Symptômes détectés :
Fracture ou entorse possible 
Question suivante :
Peut-il encore bouger le bras ?

E075
Parent :
Mon enfant a été mordu par un serpent.
Mots-clés :
mordu serpent 
Symptômes détectés :
Morsure de serpent 
Urgence :
Très élevée 
Question suivante :
Quand la morsure est-elle survenue ?

E076
Parent :
Mon enfant a été piqué par un scorpion.
Mots-clés :
piqué scorpion 
Symptômes détectés :
Piqûre venimeuse possible 
Urgence :
Élevée 
Question suivante :
Où se situe la piqûre ?

E077
Parent :
Mon enfant a été attaqué par des abeilles.
Mots-clés :
abeilles 
Symptômes détectés :
Multiples piqûres 
Question suivante :
A-t-il des difficultés à respirer ou un gonflement important ?

E078
Parent :
Mon enfant saigne beaucoup.
Mots-clés :
saigne beaucoup 
Symptômes détectés :
Hémorragie 
Urgence :
Très élevée 
Question suivante :
D'où provient le saignement ?

E079
Parent :
Mon enfant a une plaie profonde.
Mots-clés :
plaie profonde 
Symptômes détectés :
Blessure grave 
Urgence :
Élevée 
Question suivante :
La plaie continue-t-elle à saigner ?

E080
Parent :
Mon enfant a perdu une dent après une chute.
Mots-clés :
perdu dent 
Symptômes détectés :
Traumatisme dentaire 
Question suivante :
S'agit-il d'une dent de lait ou d'une dent définitive ?

Nouveaux mots-clés Santé de l'enfant
avalé pétrole
produit nettoyage
avalé médicament
pièce de monnaie
avalé objet
s'étouffe
coincé dans le nez
dans l'oreille
ne voit pas bien
œil rouge gonflé
coup à la tête
tombé arbre
boite après chute
bras gonflé
mordu serpent
piqué scorpion
attaqué par des abeilles
saigne beaucoup
plaie profonde
perdu dent

E081
Parent :
Mon enfant parle très peu.
Mots-clés :
parle peu 
Symptômes détectés :
Retard de langage possible 
Question suivante :
Quel âge a votre enfant ?

E082
Parent :
Mon enfant ne parle pas du tout.
Mots-clés :
ne parle pas 
Symptômes détectés :
Retard de langage important 
Question suivante :
Quel âge a votre enfant ?

E083
Parent :
Mon enfant ne répond pas quand on l'appelle.
Mots-clés :
ne répond pas 
Symptômes détectés :
Trouble auditif ou développemental possible 
Question suivante :
Réagit-il aux bruits forts ?

E084
Parent :
Mon enfant semble ne pas entendre.
Mots-clés :
ne pas entendre 
Symptômes détectés :
Trouble auditif possible 
Question suivante :
Depuis quand avez-vous remarqué cela ?

E085
Parent :
Mon enfant marche plus tard que les autres.
Mots-clés :
marche tard 
Symptômes détectés :
Retard moteur possible 
Question suivante :
Quel âge a votre enfant ?

E086
Parent :
Mon enfant tombe souvent.
Mots-clés :
tombe souvent 
Symptômes détectés :
Trouble moteur possible 
Question suivante :
Depuis quand cela se produit-il ?

E087
Parent :
Mon enfant n'arrive pas à se tenir debout.
Mots-clés :
ne tient pas debout 
Symptômes détectés :
Retard moteur important 
Question suivante :
Quel âge a votre enfant ?

E088
Parent :
Mon enfant ne regarde pas les gens dans les yeux.
Mots-clés :
ne regarde pas les yeux 
Symptômes détectés :
Trouble du développement possible 
Question suivante :
Quel âge a votre enfant ?

E089
Parent :
Mon enfant préfère rester seul.
Mots-clés :
reste seul 
Symptômes détectés :
Difficultés sociales possibles 
Question suivante :
Joue-t-il avec d'autres enfants ?

E090
Parent :
Mon enfant répète toujours les mêmes gestes.
Mots-clés :
mêmes gestes 
Symptômes détectés :
Trouble du comportement possible 
Question suivante :
Depuis quand observez-vous cela ?

E091
Parent :
Mon enfant est très agité.
Mots-clés :
très agité 
Symptômes détectés :
Hyperactivité possible 
Question suivante :
Cela perturbe-t-il ses activités quotidiennes ?

E092
Parent :
Mon enfant a des difficultés à apprendre.
Mots-clés :
difficultés apprendre 
Symptômes détectés :
Difficultés scolaires possibles 
Question suivante :
Quel âge a votre enfant et va-t-il à l'école ?

E093
Parent :
Mon enfant oublie rapidement ce qu'on lui dit.
Mots-clés :
oublie rapidement 
Symptômes détectés :
Difficulté de mémoire ou d'attention 
Question suivante :
Depuis quand avez-vous remarqué cela ?

E094
Parent :
Mon enfant ne joue pas comme les autres enfants.
Mots-clés :
ne joue pas comme les autres 
Symptômes détectés :
Retard du développement possible 
Question suivante :
Quel âge a votre enfant ?

E095
Parent :
Mon enfant est paralysé d'un bras.
Mots-clés :
paralysé bras 
Symptômes détectés :
Paralysie 
Urgence :
Élevée 
Question suivante :
Depuis quand cette paralysie est-elle apparue ?

E096
Parent :
Mon enfant est paralysé d'une jambe.
Mots-clés :
paralysé jambe 
Symptômes détectés :
Paralysie 
Urgence :
Élevée 
Question suivante :
Cette paralysie est-elle apparue soudainement ?

E097
Parent :
Mon enfant a des mouvements inhabituels.
Mots-clés :
mouvements inhabituels 
Symptômes détectés :
Trouble neurologique possible 
Question suivante :
Ces mouvements surviennent-ils plusieurs fois par jour ?

E098
Parent :
Mon enfant a des difficultés à utiliser ses mains.
Mots-clés :
difficultés mains 
Symptômes détectés :
Trouble moteur possible 
Question suivante :
Depuis quel âge observez-vous cela ?

E099
Parent :
Je suis inquiet pour le développement de mon enfant.
Mots-clés :
développement enfant 
Symptômes détectés :
Préoccupation développementale 
Question suivante :
Quel aspect du développement vous inquiète le plus ?

E100
Parent :
Mon enfant n'évolue pas comme les autres enfants.
Mots-clés :
n'évolue pas comme les autres 
Symptômes détectés :
Retard du développement possible 
Question suivante :
Quel âge a votre enfant et quelles différences observez-vous ?

Catégorie terminée
✅ SANTÉ DE L'ENFANT : E001 à E100 complétés
Mots-clés majeurs collectés
fièvre enfant
bébé chauffe
toux
respire vite
poitrine se creuse
refuse le sein
vomit
diarrhée enfant
ne mange plus
ne joue plus
convulsions
perdu connaissance
très maigre
bras fins
pieds gonflés
jamais vacciné
roule les yeux
vers selles
ventre gonflé
très pâle
mordu serpent
avalé pétrole
s'étouffe
coup à la tête
parle peu
ne parle pas
ne répond pas
marche tard
reste seul
très agité
paralysé bras
paralysé jambe
développement enfant



















VIH/SIDA (V001 à V020)
V001
Patient :
Je veux faire le test du VIH.
Mots-clés :
test VIH 
Intention :
Dépistage VIH 
Question suivante :
Avez-vous déjà effectué un test VIH auparavant ?

V002
Patient :
Je ne connais pas mon statut VIH.
Mots-clés :
statut VIH 
Intention :
Dépistage 
Question suivante :
Souhaitez-vous connaître où faire un test de dépistage ?

V003
Patient :
J'ai peur d'avoir le VIH.
Mots-clés :
peur VIH 
Intention :
Préoccupation liée au VIH 
Question suivante :
Y a-t-il une situation particulière qui vous inquiète ?

V004
Patient :
J'ai eu un rapport sexuel non protégé.
Mots-clés :
rapport non protégé 
Facteur de risque :
Exposition possible au VIH 
Question suivante :
Quand ce rapport a-t-il eu lieu ?

V005
Patient :
Mon partenaire est séropositif.
Mots-clés :
partenaire séropositif 
Facteur de risque :
Exposition possible 
Question suivante :
Connaissez-vous votre propre statut VIH ?

V006
Patient :
Je suis séropositif.
Mots-clés :
séropositif 
Information :
VIH connu 
Question suivante :
Prenez-vous actuellement un traitement antirétroviral ?

V007
Patient :
Je prends les ARV.
Mots-clés :
ARV 
Information :
Sous traitement 
Question suivante :
Prenez-vous vos médicaments tous les jours ?

V008
Patient :
J'ai oublié mes médicaments VIH.
Mots-clés :
oublié médicaments 
Information :
Mauvaise observance possible 
Question suivante :
Depuis combien de jours avez-vous oublié votre traitement ?

V009
Patient :
Je n'ai plus mes ARV.
Mots-clés :
plus ARV 
Information :
Rupture de traitement 
Question suivante :
Depuis combien de temps êtes-vous sans traitement ?

V010
Patient :
Je veux arrêter mon traitement.
Mots-clés :
arrêter traitement 
Information :
Risque d'interruption thérapeutique 
Question suivante :
Quelle est la raison principale de cette décision ?

V011
Patient :
Je perds beaucoup de poids.
Mots-clés :
perd poids 
Symptômes détectés :
Amaigrissement 
Question suivante :
Depuis combien de temps perdez-vous du poids ?

V012
Patient :
J'ai une toux qui ne finit pas.
Mots-clés :
toux ne finit pas 
Symptômes détectés :
Toux chronique 
Question suivante :
Depuis combien de semaines toussez-vous ?

V013
Patient :
J'ai de la fièvre presque tous les jours.
Mots-clés :
fièvre tous les jours 
Symptômes détectés :
Fièvre prolongée 
Question suivante :
Depuis combien de temps avez-vous cette fièvre ?

V014
Patient :
Je transpire beaucoup la nuit.
Mots-clés :
transpire nuit 
Symptômes détectés :
Sueurs nocturnes 
Question suivante :
Depuis combien de semaines cela dure-t-il ?

V015
Patient :
J'ai souvent la diarrhée.
Mots-clés :
souvent diarrhée 
Symptômes détectés :
Diarrhée chronique possible 
Question suivante :
Depuis combien de temps avez-vous la diarrhée ?

V016
Patient :
J'ai des plaies dans la bouche.
Mots-clés :
plaies bouche 
Symptômes détectés :
Lésions buccales 
Question suivante :
Depuis combien de temps ces plaies sont-elles présentes ?

V017
Patient :
J'ai des boutons sur la peau.
Mots-clés :
boutons peau 
Symptômes détectés :
Problème dermatologique 
Question suivante :
Depuis quand avez-vous ces boutons ?

V018
Patient :
Je tombe souvent malade.
Mots-clés :
souvent malade 
Symptômes détectés :
Infections répétées 
Question suivante :
Quels types de maladies avez-vous fréquemment ?

V019
Patient :
Je suis enceinte et séropositive.
Mots-clés :
enceinte 
séropositive 
Situation :
Prévention transmission mère-enfant 
Question suivante :
Êtes-vous suivie dans un programme de prévention de la transmission mère-enfant ?

V020
Patient :
Mon enfant est né d'une mère séropositive.
Mots-clés :
enfant mère séropositive 
Situation :
Exposition pédiatrique au VIH 
Question suivante :
L'enfant a-t-il déjà été testé pour le VIH ?

Dictionnaire initial VIH/SIDA
test VIH
statut VIH
peur VIH
rapport non protégé
partenaire séropositif
séropositif
ARV
oublié médicaments
plus ARV
arrêter traitement
perd poids
toux ne finit pas
fièvre tous les jours
transpire nuit
souvent diarrhée
plaies bouche
boutons peau
souvent malade
enceinte séropositive
enfant mère séropositive
V021
Patient :
Peut-on attraper le VIH en serrant la main ?
Mots-clés :
serrer la main 
Intention :
Information sur la transmission 
Réponse attendue :
Non, le VIH ne se transmet pas par une poignée de main. 
Question suivante :
Souhaitez-vous connaître les véritables modes de transmission ?

V022
Patient :
Peut-on attraper le VIH en partageant un repas ?
Mots-clés :
partager repas 
Intention :
Information sur la transmission 
Réponse attendue :
Non, partager un repas ne transmet pas le VIH. 
Question suivante :
Avez-vous d'autres questions sur la transmission ?

V023
Patient :
Les moustiques transmettent-ils le VIH ?
Mots-clés :
moustiques 
Intention :
Croyance populaire 
Réponse attendue :
Non, les moustiques ne transmettent pas le VIH. 
Question suivante :
Souhaitez-vous connaître les modes réels de transmission ?

V024
Patient :
Peut-on reconnaître une personne séropositive à son apparence ?
Mots-clés :
reconnaître séropositif 
Intention :
Information 
Réponse attendue :
Non, seule un test peut confirmer le statut VIH. 
Question suivante :
Avez-vous déjà effectué un test VIH ?

V025
Patient :
Le VIH se soigne-t-il ?
Mots-clés :
VIH se soigne 
Intention :
Information traitement 
Réponse attendue :
Le VIH peut être contrôlé efficacement grâce aux ARV. 
Question suivante :
Souhaitez-vous des informations sur les traitements disponibles ?

V026
Patient :
Puis-je vivre longtemps avec le VIH ?
Mots-clés :
vivre longtemps 
Intention :
Information 
Réponse attendue :
Oui, avec un traitement régulier, une personne vivant avec le VIH peut vivre longtemps. 
Question suivante :
Prenez-vous actuellement un traitement ?

V027
Patient :
J'ai commencé les ARV.
Mots-clés :
commencé ARV 
Information :
Début de traitement 
Question suivante :
Depuis combien de temps avez-vous commencé ce traitement ?

V028
Patient :
Les ARV me donnent des nausées.
Mots-clés :
ARV 
nausées 
Symptômes détectés :
Effet secondaire possible 
Question suivante :
Depuis combien de temps ressentez-vous ces nausées ?

V029
Patient :
Les médicaments me fatiguent.
Mots-clés :
médicaments fatiguent 
Symptômes détectés :
Effet secondaire possible 
Question suivante :
Cette fatigue est-elle apparue après le début du traitement ?

V030
Patient :
J'oublie souvent mes ARV.
Mots-clés :
oublie ARV 
Information :
Observance insuffisante 
Question suivante :
Combien de doses avez-vous oubliées cette semaine ?

V031
Patient :
Je cache mon traitement à ma famille.
Mots-clés :
cache traitement 
Situation :
Difficulté sociale 
Question suivante :
Cette situation vous empêche-t-elle parfois de prendre vos médicaments ?

V032
Patient :
J'ai peur que les autres découvrent mon statut.
Mots-clés :
peur statut 
Situation :
Crainte de stigmatisation 
Question suivante :
Souhaitez-vous parler de vos inquiétudes ?

V033
Patient :
Mon partenaire refuse de faire le test.
Mots-clés :
partenaire refuse test 
Situation :
Dépistage du partenaire 
Question suivante :
Votre partenaire connaît-il les avantages du dépistage ?

V034
Patient :
Mon partenaire est séronégatif.
Mots-clés :
partenaire séronégatif 
Situation :
Couple sérodifférent 
Question suivante :
Bénéficiez-vous d'un suivi médical régulier ?

V035
Patient :
Je suis séropositive et je veux un enfant.
Mots-clés :
séropositive 
veut enfant 
Situation :
Projet de grossesse 
Question suivante :
Êtes-vous suivie par un professionnel de santé ?

V036
Patient :
Je suis enceinte et je prends les ARV.
Mots-clés :
enceinte 
ARV 
Situation :
Prévention transmission mère-enfant 
Question suivante :
Prenez-vous vos médicaments chaque jour ?

V037
Patient :
Mon bébé reçoit un traitement après la naissance.
Mots-clés :
bébé traitement 
Situation :
Prévention pédiatrique 
Question suivante :
Le suivi médical du bébé est-il régulier ?

V038
Patient :
Je veux savoir comment éviter le VIH.
Mots-clés :
éviter VIH 
Intention :
Prévention 
Question suivante :
Souhaitez-vous connaître les principales méthodes de prévention ?

V039
Patient :
Je me suis piqué avec une aiguille.
Mots-clés :
piqué aiguille 
Situation :
Exposition accidentelle 
Urgence :
Élevée 
Question suivante :
Quand cet accident est-il survenu ?

V040
Patient :
J'ai été en contact avec du sang.
Mots-clés :
contact sang 
Situation :
Exposition possible 
Question suivante :
Le sang a-t-il été en contact avec une plaie ou une muqueuse ?

Nouveaux mots-clés VIH/SIDA
serrer la main
partager repas
moustiques
reconnaître séropositif
VIH se soigne
vivre longtemps
commencé ARV
ARV nausées
médicaments fatiguent
oublie ARV
cache traitement
peur statut
partenaire refuse test
partenaire séronégatif
veut enfant
enceinte ARV
bébé traitement
éviter VIH
piqué aiguille
contact sang
V041
Patient :
Je tousse depuis plus d'un mois.
Mots-clés :
tousse un mois 
Symptômes détectés :
Tuberculose possible 
Question suivante :
Avez-vous également perdu du poids ou fait de la fièvre ?

V042
Patient :
Je crache parfois du sang.
Mots-clés :
crache sang 
Symptômes détectés :
Tuberculose possible 
Urgence :
Élevée 
Question suivante :
Depuis combien de temps cela se produit-il ?

V043
Patient :
J'ai perdu beaucoup de poids récemment.
Mots-clés :
beaucoup perdu poids 
Symptômes détectés :
Amaigrissement important 
Question suivante :
Avez-vous aussi une toux ou de la diarrhée ?

V044
Patient :
Je transpire chaque nuit.
Mots-clés :
chaque nuit transpire 
Symptômes détectés :
Sueurs nocturnes 
Question suivante :
Depuis combien de semaines ?

V045
Patient :
J'ai des ganglions dans le cou.
Mots-clés :
ganglions cou 
Symptômes détectés :
Adénopathies 
Question suivante :
Depuis combien de temps ces ganglions sont-ils présents ?

V046
Patient :
J'ai une diarrhée qui dure depuis des semaines.
Mots-clés :
diarrhée semaines 
Symptômes détectés :
Diarrhée chronique 
Question suivante :
Avez-vous perdu du poids ?

V047
Patient :
Je suis souvent hospitalisé.
Mots-clés :
souvent hospitalisé 
Symptômes détectés :
Infections répétées 
Question suivante :
Pour quelles maladies êtes-vous généralement hospitalisé ?

V048
Patient :
J'ai des taches blanches dans la bouche.
Mots-clés :
taches blanches bouche 
Symptômes détectés :
Candidose buccale possible 
Question suivante :
Ressentez-vous une douleur lorsque vous mangez ?

V049
Patient :
J'ai mal quand j'avale.
Mots-clés :
mal avaler 
Symptômes détectés :
Infection buccale ou œsophagienne possible 
Question suivante :
Depuis combien de temps ?

V050
Patient :
J'ai des boutons inhabituels sur la peau.
Mots-clés :
boutons inhabituels 
Symptômes détectés :
Infection ou maladie cutanée 
Question suivante :
Depuis quand ces lésions sont-elles apparues ?

V051
Patient :
J'ai une forte fièvre depuis longtemps.
Mots-clés :
forte fièvre longtemps 
Symptômes détectés :
Infection chronique possible 
Question suivante :
Depuis combien de semaines avez-vous cette fièvre ?

V052
Patient :
Je suis très faible depuis plusieurs semaines.
Mots-clés :
faible plusieurs semaines 
Symptômes détectés :
Altération de l'état général 
Question suivante :
Avez-vous perdu du poids ?

V053
Patient :
Je n'ai plus d'appétit.
Mots-clés :
plus appétit 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Depuis quand avez-vous remarqué cela ?

V054
Patient :
Je suis séropositif et je tousse.
Mots-clés :
séropositif 
tousse 
Symptômes détectés :
Tuberculose ou infection respiratoire possible 
Question suivante :
Depuis combien de temps toussez-vous ?

V055
Patient :
Je suis séropositif et j'ai de la fièvre.
Mots-clés :
séropositif 
fièvre 
Symptômes détectés :
Infection possible 
Question suivante :
Depuis combien de jours avez-vous de la fièvre ?

V056
Patient :
Je suis séropositif et j'ai la diarrhée.
Mots-clés :
séropositif 
diarrhée 
Symptômes détectés :
Infection digestive possible 
Question suivante :
Depuis combien de temps avez-vous la diarrhée ?

V057
Patient :
J'ai arrêté mes ARV depuis plusieurs semaines.
Mots-clés :
arrêté ARV 
Situation :
Interruption de traitement 
Urgence :
Élevée 
Question suivante :
Quelle est la raison de l'arrêt du traitement ?

V058
Patient :
Je ne vais plus au centre de traitement.
Mots-clés :
plus centre traitement 
Situation :
Rupture de suivi 
Question suivante :
Depuis combien de temps n'avez-vous pas été suivi ?

V059
Patient :
Mon dernier test viral n'était pas bon.
Mots-clés :
test viral 
Situation :
Suivi biologique 
Question suivante :
Votre professionnel de santé vous a-t-il expliqué les résultats ?

V060
Patient :
Je veux reprendre mon traitement VIH.
Mots-clés :
reprendre traitement VIH 
Situation :
Retour aux soins 
Question suivante :
Depuis combien de temps avez-vous interrompu le traitement ?

Nouveaux mots-clés VIH/SIDA
tousse un mois
crache sang
beaucoup perdu poids
chaque nuit transpire
ganglions cou
diarrhée semaines
souvent hospitalisé
taches blanches bouche
mal avaler
boutons inhabituels
forte fièvre longtemps
faible plusieurs semaines
plus appétit
arrêté ARV
plus centre traitement
test viral
reprendre traitement VIH
V061
Patient :
Je suis enceinte et je viens d'apprendre que je suis séropositive.
Mots-clés :
enceinte 
vient d'apprendre 
séropositive 
Situation :
Nouveau diagnostic pendant la grossesse 
Question suivante :
Avez-vous déjà commencé un traitement ARV ?

V062
Patient :
J'ai peur de transmettre le VIH à mon bébé.
Mots-clés :
transmettre bébé 
Situation :
Prévention transmission mère-enfant 
Question suivante :
Êtes-vous suivie pour votre grossesse et votre traitement VIH ?

V063
Patient :
Mon bébé vient de naître et je suis séropositive.
Mots-clés :
bébé vient de naître 
Situation :
Suivi postnatal 
Question suivante :
Le bébé a-t-il reçu les soins recommandés après la naissance ?

V064
Patient :
Puis-je allaiter mon bébé si je suis séropositive ?
Mots-clés :
allaiter bébé 
Intention :
Information sur l'allaitement 
Question suivante :
Prenez-vous régulièrement votre traitement ARV ?

V065
Patient :
Mon bébé est exposé au VIH.
Mots-clés :
bébé exposé VIH 
Situation :
Exposition pédiatrique 
Question suivante :
Le bébé est-il suivi dans une structure de santé ?

V066
Patient :
Je n'ai jamais fait tester mon bébé.
Mots-clés :
jamais tester bébé 
Situation :
Dépistage pédiatrique 
Question suivante :
Quel âge a votre bébé ?

V067
Patient :
Je prends mes médicaments tous les jours.
Mots-clés :
tous les jours 
Situation :
Bonne observance 
Question suivante :
Rencontrez-vous des difficultés pour poursuivre le traitement ?

V068
Patient :
Je manque parfois mes rendez-vous médicaux.
Mots-clés :
manque rendez-vous 
Situation :
Suivi irrégulier 
Question suivante :
Quelle est la principale difficulté pour vous rendre aux consultations ?

V069
Patient :
Je voyage souvent et j'oublie mon traitement.
Mots-clés :
voyage souvent 
oublie traitement 
Situation :
Risque de mauvaise observance 
Question suivante :
Souhaitez-vous des conseils pour mieux organiser la prise du traitement ?

V070
Patient :
Je me sens découragé à cause du VIH.
Mots-clés :
découragé 
Situation :
Difficulté psychologique 
Question suivante :
Souhaitez-vous parler davantage de ce que vous ressentez ?

V071
Patient :
Je me sens rejeté par mon entourage.
Mots-clés :
rejeté entourage 
Situation :
Stigmatisation 
Question suivante :
Avez-vous une personne de confiance avec qui parler ?

V072
Patient :
J'ai peur d'annoncer mon statut à mon partenaire.
Mots-clés :
annoncer statut 
Situation :
Révélation du statut VIH 
Question suivante :
Votre partenaire connaît-il déjà votre situation médicale ?

V073
Patient :
Je veux protéger mon partenaire.
Mots-clés :
protéger partenaire 
Situation :
Prévention de transmission 
Question suivante :
Votre partenaire connaît-il son statut VIH ?

V074
Patient :
Mon partenaire refuse les préservatifs.
Mots-clés :
refuse préservatifs 
Situation :
Prévention difficile 
Question suivante :
Avez-vous déjà discuté ensemble des risques de transmission ?

V075
Patient :
J'ai été exposé au VIH il y a quelques heures.
Mots-clés :
exposé VIH 
quelques heures 
Situation :
Exposition récente 
Urgence :
Très élevée 
Question suivante :
Combien d'heures se sont écoulées depuis l'exposition ?

V076
Patient :
Je cherche un traitement après exposition.
Mots-clés :
traitement après exposition 
Situation :
Prophylaxie post-exposition 
Urgence :
Élevée 
Question suivante :
Quand l'exposition a-t-elle eu lieu ?

V077
Patient :
Mon préservatif s'est déchiré.
Mots-clés :
préservatif déchiré 
Situation :
Exposition possible 
Question suivante :
Quand cet incident est-il survenu ?

V078
Patient :
Je veux connaître ma charge virale.
Mots-clés :
charge virale 
Situation :
Suivi du traitement 
Question suivante :
Avez-vous récemment effectué un examen de charge virale ?

V079
Patient :
Mon médecin dit que ma charge virale est indétectable.
Mots-clés :
charge virale indétectable 
Situation :
Bonne réponse au traitement 
Question suivante :
Continuez-vous à prendre vos ARV sans interruption ?

V080
Patient :
Je veux mieux comprendre le VIH.
Mots-clés :
comprendre VIH 
Intention :
Éducation sanitaire 
Question suivante :
Souhaitez-vous des informations sur la transmission, le traitement ou la prévention ?

Nouveaux mots-clés VIH/SIDA
transmettre bébé
allaiter bébé
bébé exposé VIH
jamais tester bébé
manque rendez-vous
voyage souvent
découragé
rejeté entourage
annoncer statut
protéger partenaire
refuse préservatifs
exposé VIH
traitement après exposition
préservatif déchiré
charge virale
charge virale indétectable
comprendre VIH
V081
Patient :
Je suis séropositif depuis plusieurs années.
Mots-clés :
séropositif plusieurs années 
Situation :
Suivi à long terme 
Question suivante :
Prenez-vous toujours votre traitement régulièrement ?

V082
Patient :
Je prends les ARV depuis dix ans.
Mots-clés :
ARV dix ans 
Situation :
Traitement prolongé 
Question suivante :
Avez-vous récemment effectué un contrôle médical ?

V083
Patient :
Je me sens bien mais je suis séropositif.
Mots-clés :
se sent bien 
Situation :
Infection contrôlée 
Question suivante :
Continuez-vous à prendre vos médicaments chaque jour ?

V084
Patient :
Je veux savoir si mon traitement fonctionne.
Mots-clés :
traitement fonctionne 
Situation :
Suivi thérapeutique 
Question suivante :
Avez-vous un résultat récent de charge virale ?

V085
Patient :
Mon résultat de charge virale est élevé.
Mots-clés :
charge virale élevée 
Situation :
Échec thérapeutique possible 
Question suivante :
Prenez-vous vos ARV régulièrement ?

V086
Patient :
Mon médecin m'a changé de traitement.
Mots-clés :
changé traitement 
Situation :
Changement thérapeutique 
Question suivante :
Savez-vous pourquoi le traitement a été modifié ?

V087
Patient :
J'ai des effets secondaires avec mon nouveau traitement.
Mots-clés :
nouveau traitement 
effets secondaires 
Situation :
Tolérance du traitement 
Question suivante :
Quels effets secondaires ressentez-vous ?

V088
Patient :
Je suis traité pour la tuberculose et le VIH.
Mots-clés :
tuberculose 
VIH 
Situation :
Co-infection VIH/TB 
Question suivante :
Prenez-vous les deux traitements conformément aux prescriptions ?

V089
Patient :
On m'a diagnostiqué la tuberculose.
Mots-clés :
diagnostiqué tuberculose 
Situation :
Tuberculose 
Question suivante :
Avez-vous déjà effectué un test VIH récemment ?

V090
Patient :
Je suis séropositif et j'ai une tuberculose.
Mots-clés :
séropositif 
tuberculose 
Situation :
Co-infection 
Question suivante :
Êtes-vous suivi dans un programme spécialisé ?

V091
Patient :
J'ai peur de mourir du VIH.
Mots-clés :
peur mourir 
Situation :
Anxiété liée à la maladie 
Question suivante :
Êtes-vous actuellement sous traitement ARV ?

V092
Patient :
Je suis découragé par mon traitement.
Mots-clés :
découragé traitement 
Situation :
Risque d'abandon 
Question suivante :
Quelle est la principale difficulté que vous rencontrez ?

V093
Patient :
Je ne trouve personne pour me soutenir.
Mots-clés :
personne soutenir 
Situation :
Isolement social 
Question suivante :
Avez-vous accès à un groupe de soutien ou à un conseiller ?

V094
Patient :
Je veux aider une personne vivant avec le VIH.
Mots-clés :
aider personne VIH 
Intention :
Soutien communautaire 
Question suivante :
Souhaitez-vous des conseils sur l'accompagnement des patients ?

V095
Patient :
Mon frère est séropositif.
Mots-clés :
frère séropositif 
Situation :
Soutien familial 
Question suivante :
Votre frère suit-il actuellement un traitement ?

V096
Patient :
Je vis avec une personne séropositive.
Mots-clés :
vit avec séropositif 
Situation :
Information communautaire 
Question suivante :
Souhaitez-vous connaître les précautions recommandées ?

V097
Patient :
Peut-on travailler quand on est séropositif ?
Mots-clés :
travailler séropositif 
Intention :
Vie quotidienne 
Réponse attendue :
Oui, une personne vivant avec le VIH peut travailler normalement si son état de santé le permet. 
Question suivante :
Souhaitez-vous plus d'informations sur la vie avec le VIH ?

V098
Patient :
Peut-on se marier quand on est séropositif ?
Mots-clés :
marier séropositif 
Intention :
Vie familiale 
Réponse attendue :
Oui, avec un suivi médical approprié. 
Question suivante :
Souhaitez-vous des informations sur la prévention pour le couple ?

V099
Patient :
Peut-on avoir des enfants quand on est séropositif ?
Mots-clés :
enfants séropositif 
Intention :
Projet familial 
Réponse attendue :
Oui, avec un accompagnement médical adapté. 
Question suivante :
Souhaitez-vous des informations sur la prévention de la transmission au bébé ?

V100
Patient :
Je veux tout savoir sur le VIH.
Mots-clés :
tout savoir VIH 
Intention :
Éducation sanitaire complète 
Question suivante :
Souhaitez-vous commencer par la transmission, le dépistage, le traitement ou la prévention ?

Catégorie terminée
✅ VIH/SIDA : V001 à V100 complétés
Mots-clés majeurs collectés
test VIH
statut VIH
rapport non protégé
partenaire séropositif
ARV
oublié ARV
charge virale
charge virale indétectable
transmettre bébé
allaiter bébé
préservatif déchiré
piqué aiguille
contact sang
crache sang
ganglions cou
taches blanches bouche
tuberculose VIH
peur mourir
découragé traitement
travailler séropositif
marier séropositif
enfants séropositif
















TUBERCULOSE (T001 à T020)
T001
Patient :
Je tousse depuis plusieurs semaines.
Mots-clés :
tousse plusieurs semaines 
Symptômes détectés :
Toux prolongée 
Question suivante :
Depuis exactement combien de semaines toussez-vous ?

T002
Patient :
Ma toux ne finit pas.
Mots-clés :
toux ne finit pas 
Symptômes détectés :
Toux chronique 
Question suivante :
Depuis combien de temps avez-vous cette toux ?

T003
Patient :
Je tousse depuis plus de deux semaines.
Mots-clés :
plus deux semaines 
Symptômes détectés :
Suspicion de tuberculose 
Question suivante :
Avez-vous également de la fièvre ?

T004
Patient :
Je crache des crachats tous les jours.
Mots-clés :
crache crachats 
Symptômes détectés :
Toux productive 
Question suivante :
Quelle couleur ont les crachats ?

T005
Patient :
Je crache parfois du sang.
Mots-clés :
crache sang 
Symptômes détectés :
Hémoptysie 
Urgence :
Élevée 
Question suivante :
Depuis quand crachez-vous du sang ?

T006
Patient :
J'ai de la fièvre chaque soir.
Mots-clés :
fièvre chaque soir 
Symptômes détectés :
Fièvre prolongée 
Question suivante :
Depuis combien de temps avez-vous cette fièvre ?

T007
Patient :
Je transpire beaucoup la nuit.
Mots-clés :
transpire nuit 
Symptômes détectés :
Sueurs nocturnes 
Question suivante :
Depuis combien de semaines cela dure-t-il ?

T008
Patient :
J'ai perdu beaucoup de poids.
Mots-clés :
perdu poids 
Symptômes détectés :
Amaigrissement 
Question suivante :
Cette perte de poids est-elle récente ?

T009
Patient :
Je suis très maigre maintenant.
Mots-clés :
très maigre 
Symptômes détectés :
Amaigrissement important 
Question suivante :
Depuis quand avez-vous commencé à maigrir ?

T010
Patient :
Je n'ai plus d'appétit.
Mots-clés :
plus appétit 
Symptômes détectés :
Perte d'appétit 
Question suivante :
Depuis combien de temps ?

T011
Patient :
J'ai mal dans la poitrine quand je tousse.
Mots-clés :
mal poitrine 
tousse 
Symptômes détectés :
Douleur thoracique 
Question suivante :
La douleur est-elle forte ?

T012
Patient :
Je suis essoufflé.
Mots-clés :
essoufflé 
Symptômes détectés :
Difficulté respiratoire 
Question suivante :
Depuis quand êtes-vous essoufflé ?

T013
Patient :
Mon voisin dit que j'ai peut-être la tuberculose.
Mots-clés :
peut-être tuberculose 
Intention :
Information / suspicion 
Question suivante :
Avez-vous une toux qui dure depuis plus de deux semaines ?

T014
Patient :
Une personne de ma maison a la tuberculose.
Mots-clés :
maison tuberculose 
Situation :
Contact avec un malade 
Question suivante :
Présentez-vous actuellement une toux ou de la fièvre ?

T015
Patient :
Je vis avec quelqu'un qui a la tuberculose.
Mots-clés :
vit avec tuberculose 
Situation :
Contact étroit 
Question suivante :
Avez-vous déjà été dépisté ?

T016
Patient :
Mon enfant est traité pour la tuberculose.
Mots-clés :
enfant traité tuberculose 
Situation :
Cas familial 
Question suivante :
L'enfant prend-il régulièrement son traitement ?

T017
Patient :
J'ai commencé un traitement contre la tuberculose.
Mots-clés :
commencé traitement tuberculose 
Situation :
Sous traitement 
Question suivante :
Depuis combien de temps avez-vous commencé le traitement ?

T018
Patient :
J'ai oublié plusieurs doses de mon traitement.
Mots-clés :
oublié doses 
Situation :
Mauvaise observance 
Question suivante :
Combien de doses avez-vous manquées ?

T019
Patient :
Je me sens mieux depuis le traitement.
Mots-clés :
mieux traitement 
Situation :
Amélioration clinique 
Question suivante :
Continuez-vous à prendre les médicaments chaque jour ?

T020
Patient :
Je veux faire un test pour la tuberculose.
Mots-clés :
test tuberculose 
Intention :
Dépistage 
Question suivante :
Présentez-vous actuellement une toux ou d'autres symptômes ?

Dictionnaire initial Tuberculose
tousse plusieurs semaines
toux ne finit pas
plus deux semaines
crache crachats
crache sang
fièvre chaque soir
transpire nuit
perdu poids
très maigre
plus appétit
mal poitrine
essoufflé
peut-être tuberculose
maison tuberculose
vit avec tuberculose
enfant traité tuberculose
commencé traitement tuberculose
oublié doses
mieux traitement
test tuberculose
T021
Patient :
Mon enfant tousse depuis longtemps.
Mots-clés :
enfant tousse longtemps 
Symptômes détectés :
Tuberculose pédiatrique possible 
Question suivante :
Depuis combien de semaines votre enfant tousse-t-il ?

T022
Patient :
Mon enfant a perdu du poids et tousse.
Mots-clés :
enfant perdu poids 
tousse 
Symptômes détectés :
Tuberculose possible 
Question suivante :
L'enfant a-t-il aussi de la fièvre ?

T023
Patient :
Mon enfant est souvent malade.
Mots-clés :
enfant souvent malade 
Symptômes détectés :
Infection chronique possible 
Question suivante :
Présente-t-il une toux prolongée ?

T024
Patient :
Mon enfant a été en contact avec un malade de la tuberculose.
Mots-clés :
contact tuberculose 
Situation :
Contact à risque 
Question suivante :
A-t-il déjà été évalué dans un centre de santé ?

T025
Patient :
Je suis séropositif et je tousse.
Mots-clés :
séropositif 
tousse 
Situation :
Co-infection VIH/TB possible 
Question suivante :
Depuis combien de temps avez-vous cette toux ?

T026
Patient :
Je suis sous ARV et j'ai une forte fièvre.
Mots-clés :
ARV 
forte fièvre 
Situation :
Infection opportuniste possible 
Question suivante :
Avez-vous également une toux ?

T027
Patient :
J'ai le VIH et j'ai perdu du poids.
Mots-clés :
VIH 
perdu poids 
Situation :
Tuberculose possible 
Question suivante :
Avez-vous une toux prolongée ?

T028
Patient :
J'ai arrêté mon traitement contre la tuberculose.
Mots-clés :
arrêté traitement 
Situation :
Abandon thérapeutique 
Urgence :
Élevée 
Question suivante :
Depuis combien de temps avez-vous arrêté le traitement ?

T029
Patient :
Je ne prends plus les médicaments.
Mots-clés :
ne prends plus médicaments 
Situation :
Rupture de traitement 
Question suivante :
Quelle est la raison de l'arrêt ?

T030
Patient :
J'ai oublié plusieurs jours de traitement.
Mots-clés :
oublié plusieurs jours 
Situation :
Mauvaise observance 
Question suivante :
Combien de jours exactement ?

T031
Patient :
Les médicaments me donnent des nausées.
Mots-clés :
médicaments nausées 
Symptômes détectés :
Effets secondaires possibles 
Question suivante :
Depuis quand ressentez-vous ces nausées ?

T032
Patient :
Je vomis après avoir pris mes comprimés.
Mots-clés :
vomis comprimés 
Symptômes détectés :
Effets secondaires possibles 
Question suivante :
Cela arrive-t-il à chaque prise ?

T033
Patient :
Mes yeux sont devenus jaunes.
Mots-clés :
yeux jaunes 
Symptômes détectés :
Effet secondaire grave possible 
Urgence :
Élevée 
Question suivante :
Depuis quand vos yeux sont-ils jaunes ?

T034
Patient :
J'ai des démangeaisons depuis le traitement.
Mots-clés :
démangeaisons traitement 
Symptômes détectés :
Réaction médicamenteuse possible 
Question suivante :
Avez-vous aussi une éruption sur la peau ?

T035
Patient :
J'ai une grosse boule dans le cou.
Mots-clés :
boule cou 
Symptômes détectés :
Ganglion tuberculeux possible 
Question suivante :
Depuis combien de temps cette boule est-elle présente ?

T036
Patient :
J'ai des ganglions sous la mâchoire.
Mots-clés :
ganglions mâchoire 
Symptômes détectés :
Tuberculose ganglionnaire possible 
Question suivante :
Ces ganglions sont-ils douloureux ?

T037
Patient :
Mon cou est gonflé depuis plusieurs semaines.
Mots-clés :
cou gonflé 
Symptômes détectés :
Atteinte ganglionnaire possible 
Question suivante :
Avez-vous aussi de la fièvre ou une perte de poids ?

T038
Patient :
J'ai mal au dos depuis longtemps.
Mots-clés :
mal dos longtemps 
Symptômes détectés :
Tuberculose osseuse possible 
Question suivante :
Depuis combien de mois avez-vous cette douleur ?

T039
Patient :
Je ne peux plus marcher normalement à cause du dos.
Mots-clés :
ne peut plus marcher 
dos 
Symptômes détectés :
Atteinte vertébrale possible 
Urgence :
Élevée 
Question suivante :
Depuis quand avez-vous ces difficultés ?

T040
Patient :
On m'a parlé de tuberculose extra-pulmonaire.
Mots-clés :
tuberculose extra pulmonaire 
Intention :
Information 
Question suivante :
Souhaitez-vous des informations sur les différentes formes de tuberculose ?

Nouveaux mots-clés Tuberculose
enfant tousse longtemps
enfant perdu poids
contact tuberculose
VIH tousse
ARV forte fièvre
arrêté traitement tuberculose
ne prends plus médicaments
oublié plusieurs jours
médicaments nausées
vomis comprimés
yeux jaunes
démangeaisons traitement
boule cou
ganglions mâchoire
cou gonflé
mal dos longtemps
ne peut plus marcher
tuberculose extra pulmonaire
T041
Patient :
Le médecin m'a demandé un examen des crachats.
Mots-clés :
examen crachats 
Situation :
Dépistage tuberculose 
Question suivante :
Avez-vous déjà effectué cet examen ?

T042
Patient :
Je vais faire un test GeneXpert.
Mots-clés :
GeneXpert 
Situation :
Diagnostic de la tuberculose 
Question suivante :
Qui vous a orienté vers cet examen ?

T043
Patient :
J'attends les résultats de mes examens.
Mots-clés :
attend résultats 
Situation :
Suivi diagnostique 
Question suivante :
Quels examens avez-vous réalisés ?

T044
Patient :
Mon examen est revenu positif.
Mots-clés :
examen positif 
Situation :
Tuberculose confirmée 
Question suivante :
Avez-vous déjà commencé le traitement ?

T045
Patient :
Mon examen est revenu négatif.
Mots-clés :
examen négatif 
Situation :
Résultat négatif 
Question suivante :
Avez-vous encore des symptômes ?

T046
Patient :
Le médecin suspecte une tuberculose malgré les résultats.
Mots-clés :
suspecte tuberculose 
Situation :
Suspicion persistante 
Question suivante :
Quels symptômes présentez-vous actuellement ?

T047
Patient :
On m'a demandé une radiographie du thorax.
Mots-clés :
radiographie thorax 
Situation :
Investigation complémentaire 
Question suivante :
Avez-vous déjà réalisé cette radiographie ?

T048
Patient :
Ma radiographie montre un problème aux poumons.
Mots-clés :
problème poumons 
Situation :
Anomalie pulmonaire 
Question suivante :
Le médecin vous a-t-il expliqué le résultat ?

T049
Patient :
Je suis traité mais je tousse encore.
Mots-clés :
traité mais tousse 
Situation :
Évolution sous traitement 
Question suivante :
Depuis combien de temps prenez-vous le traitement ?

T050
Patient :
Je suis traité depuis deux mois.
Mots-clés :
traité deux mois 
Situation :
Suivi thérapeutique 
Question suivante :
Observez-vous une amélioration de vos symptômes ?

T051
Patient :
Je fais une rechute de tuberculose.
Mots-clés :
rechute tuberculose 
Situation :
Tuberculose récurrente 
Question suivante :
Quand aviez-vous terminé votre précédent traitement ?

T052
Patient :
J'avais déjà eu la tuberculose auparavant.
Mots-clés :
déjà tuberculose 
Situation :
Antécédent de tuberculose 
Question suivante :
Avez-vous actuellement une toux ou d'autres symptômes ?

T053
Patient :
Les symptômes sont revenus après le traitement.
Mots-clés :
symptômes revenus 
Situation :
Rechute possible 
Question suivante :
Quels symptômes sont réapparus ?

T054
Patient :
On m'a parlé de tuberculose résistante.
Mots-clés :
tuberculose résistante 
Situation :
Tuberculose pharmacorésistante 
Question suivante :
Avez-vous reçu des explications sur votre diagnostic ?

T055
Patient :
Mon traitement a été prolongé.
Mots-clés :
traitement prolongé 
Situation :
Traitement complexe 
Question suivante :
Savez-vous pourquoi le traitement a été prolongé ?

T056
Patient :
Plusieurs personnes de ma famille toussent.
Mots-clés :
famille tousse 
Situation :
Transmission familiale possible 
Question suivante :
Depuis combien de temps ces personnes toussent-elles ?

T057
Patient :
Mon épouse a la tuberculose.
Mots-clés :
épouse tuberculose 
Situation :
Contact familial 
Question suivante :
Avez-vous été dépisté ?

T058
Patient :
Mon enfant vit avec un malade de la tuberculose.
Mots-clés :
enfant vit malade tuberculose 
Situation :
Contact à risque 
Question suivante :
L'enfant a-t-il été examiné par un professionnel de santé ?

T059
Patient :
Je suis enceinte et j'ai la tuberculose.
Mots-clés :
enceinte tuberculose 
Situation :
Grossesse à risque 
Question suivante :
Êtes-vous suivie régulièrement pour votre grossesse ?

T060
Patient :
Je prends un traitement contre la tuberculose pendant ma grossesse.
Mots-clés :
traitement tuberculose grossesse 
Situation :
Suivi grossesse et tuberculose 
Question suivante :
Avez-vous des effets secondaires liés au traitement ?

Nouveaux mots-clés Tuberculose
examen crachats
GeneXpert
attend résultats
examen positif
examen négatif
suspecte tuberculose
radiographie thorax
problème poumons
traité mais tousse
traité deux mois
rechute tuberculose
déjà tuberculose
symptômes revenus
tuberculose résistante
traitement prolongé
famille tousse
épouse tuberculose
enfant vit malade tuberculose
enceinte tuberculose
traitement tuberculose grossesse
T061
Patient :
Comment attrape-t-on la tuberculose ?
Mots-clés :
attraper tuberculose 
Intention :
Information sur la transmission 
Question suivante :
Souhaitez-vous connaître les moyens de prévention ?

T062
Patient :
La tuberculose est-elle contagieuse ?
Mots-clés :
tuberculose contagieuse 
Intention :
Information 
Question suivante :
Vivez-vous avec une personne atteinte de tuberculose ?

T063
Patient :
Puis-je contaminer ma famille ?
Mots-clés :
contaminer famille 
Situation :
Préoccupation familiale 
Question suivante :
Avez-vous déjà commencé le traitement ?

T064
Patient :
Dois-je porter un masque ?
Mots-clés :
porter masque 
Situation :
Prévention 
Question suivante :
Êtes-vous actuellement en traitement contre la tuberculose ?

T065
Patient :
Mon médecin m'a conseillé de porter un masque.
Mots-clés :
conseillé masque 
Situation :
Mesure préventive 
Question suivante :
Avez-vous commencé votre traitement ?

T066
Patient :
Dois-je dormir séparément des autres ?
Mots-clés :
dormir séparément 
Situation :
Prévention familiale 
Question suivante :
Depuis combien de temps êtes-vous sous traitement ?

T067
Patient :
Puis-je continuer à travailler ?
Mots-clés :
continuer travailler 
Situation :
Vie quotidienne 
Question suivante :
Avez-vous déjà commencé le traitement ?

T068
Patient :
Mon enfant vit avec un malade de la tuberculose.
Mots-clés :
enfant contact tuberculose 
Situation :
Prévention pédiatrique 
Question suivante :
L'enfant a-t-il été examiné dans un centre de santé ?

T069
Patient :
On m'a parlé d'un traitement préventif.
Mots-clés :
traitement préventif 
Situation :
Prévention 
Question suivante :
Ce traitement est-il destiné à un enfant ou à un adulte ?

T070
Patient :
Je veux protéger mes enfants.
Mots-clés :
protéger enfants 
Situation :
Prévention familiale 
Question suivante :
Y a-t-il un malade de la tuberculose dans votre foyer ?

T071
Patient :
La tuberculose est-elle causée par la sorcellerie ?
Mots-clés :
sorcellerie 
Intention :
Croyance populaire 
Réponse attendue :
Non, la tuberculose est causée par une bactérie. 
Question suivante :
Souhaitez-vous savoir comment elle se transmet ?

T072
Patient :
Quelqu'un m'a dit que la tuberculose est une malédiction.
Mots-clés :
malédiction 
Intention :
Croyance populaire 
Réponse attendue :
Non, c'est une maladie infectieuse qui peut être soignée. 
Question suivante :
Souhaitez-vous des informations sur le traitement ?

T073
Patient :
Peut-on guérir de la tuberculose ?
Mots-clés :
guérir tuberculose 
Intention :
Information 
Réponse attendue :
Oui, avec un traitement complet et régulier. 
Question suivante :
Êtes-vous actuellement sous traitement ?

T074
Patient :
La tuberculose a-t-elle un traitement gratuit ?
Mots-clés :
traitement gratuit 
Intention :
Information 
Question suivante :
Souhaitez-vous connaître les centres de prise en charge disponibles ?

T075
Patient :
J'ai peur d'être rejeté parce que j'ai la tuberculose.
Mots-clés :
peur rejeté 
Situation :
Stigmatisation 
Question suivante :
Avez-vous déjà parlé de votre maladie à un proche de confiance ?

T076
Patient :
Mes voisins ont peur de moi.
Mots-clés :
voisins peur 
Situation :
Stigmatisation communautaire 
Question suivante :
Avez-vous commencé votre traitement ?

T077
Patient :
Je veux expliquer la tuberculose à ma famille.
Mots-clés :
expliquer famille 
Situation :
Éducation communautaire 
Question suivante :
Souhaitez-vous des informations simples sur la transmission et la prévention ?

T078
Patient :
Je participe à une sensibilisation sur la tuberculose.
Mots-clés :
sensibilisation tuberculose 
Situation :
Activité communautaire 
Question suivante :
Souhaitez-vous les messages clés de prévention ?

T079
Patient :
Comment éviter la tuberculose ?
Mots-clés :
éviter tuberculose 
Intention :
Prévention 
Question suivante :
Vivez-vous avec une personne atteinte de tuberculose ?

T080
Patient :
Je veux en savoir plus sur la tuberculose.
Mots-clés :
savoir plus tuberculose 
Intention :
Éducation sanitaire 
Question suivante :
Souhaitez-vous des informations sur les symptômes, la transmission ou le traitement ?

Nouveaux mots-clés Tuberculose
attraper tuberculose
tuberculose contagieuse
contaminer famille
porter masque
conseillé masque
dormir séparément
continuer travailler
enfant contact tuberculose
traitement préventif
protéger enfants
sorcellerie
malédiction
guérir tuberculose
traitement gratuit
peur rejeté
voisins peur
expliquer famille
sensibilisation tuberculose
éviter tuberculose
savoir plus tuberculose
T081
Patient :
J'arrive à la fin de mon traitement.
Mots-clés :
fin traitement 
Situation :
Suivi thérapeutique 
Question suivante :
Combien de jours de traitement vous reste-t-il ?

T082
Patient :
Il me reste une semaine de médicaments.
Mots-clés :
reste semaine médicaments 
Situation :
Fin proche du traitement 
Question suivante :
Avez-vous pris vos médicaments régulièrement jusqu'à présent ?

T083
Patient :
J'ai terminé mon traitement.
Mots-clés :
terminé traitement 
Situation :
Fin de traitement 
Question suivante :
Avez-vous effectué le contrôle recommandé après le traitement ?

T084
Patient :
Je me sens complètement guéri.
Mots-clés :
complètement guéri 
Situation :
Amélioration clinique 
Question suivante :
Avez-vous confirmé cette guérison avec un professionnel de santé ?

T085
Patient :
Je ne tousse plus.
Mots-clés :
ne tousse plus 
Situation :
Bonne évolution 
Question suivante :
Depuis combien de temps la toux a-t-elle disparu ?

T086
Patient :
J'ai repris du poids.
Mots-clés :
repris poids 
Situation :
Récupération 
Question suivante :
Continuez-vous encore votre traitement ?

T087
Patient :
Les symptômes ont disparu.
Mots-clés :
symptômes disparu 
Situation :
Réponse favorable 
Question suivante :
Avez-vous terminé tout le traitement prescrit ?

T088
Patient :
Je tousse encore après avoir terminé le traitement.
Mots-clés :
tousse après traitement 
Situation :
Évaluation nécessaire 
Question suivante :
Depuis combien de temps la toux persiste-t-elle ?

T089
Patient :
Les symptômes sont revenus quelques mois après ma guérison.
Mots-clés :
symptômes revenus guérison 
Situation :
Rechute possible 
Question suivante :
Quels symptômes sont réapparus ?

T090
Patient :
Je pense avoir rechuté.
Mots-clés :
rechuté 
Situation :
Rechute suspectée 
Question suivante :
Présentez-vous une toux, de la fièvre ou une perte de poids ?

T091
Patient :
Je tousse de nouveau après un ancien traitement.
Mots-clés :
tousse de nouveau 
Situation :
Récidive possible 
Question suivante :
Depuis combien de semaines toussez-vous ?

T092
Patient :
Mon voisin tousse depuis des mois.
Mots-clés :
voisin tousse 
Situation :
Référence communautaire 
Question suivante :
Avez-vous conseillé à cette personne de consulter un centre de santé ?

T093
Patient :
Je connais quelqu'un qui crache du sang.
Mots-clés :
quelqu'un crache sang 
Situation :
Cas communautaire suspect 
Question suivante :
Cette personne a-t-elle déjà consulté un professionnel de santé ?

T094
Patient :
Je veux aider une personne atteinte de tuberculose.
Mots-clés :
aider personne tuberculose 
Situation :
Soutien communautaire 
Question suivante :
Souhaitez-vous connaître les bonnes pratiques d'accompagnement ?

T095
Patient :
Je suis relais communautaire.
Mots-clés :
relais communautaire 
Situation :
Agent communautaire 
Question suivante :
Souhaitez-vous des messages clés sur la tuberculose ?

T096
Patient :
Je fais de la sensibilisation dans mon village.
Mots-clés :
sensibilisation village 
Situation :
Promotion de la santé 
Question suivante :
Souhaitez-vous les principaux signes à surveiller ?

T097
Patient :
Quels sont les signes de la tuberculose ?
Mots-clés :
signes tuberculose 
Intention :
Information 
Question suivante :
Souhaitez-vous connaître les symptômes les plus fréquents ?

T098
Patient :
Quand faut-il consulter pour une toux ?
Mots-clés :
consulter toux 
Intention :
Prévention 
Question suivante :
Depuis combien de temps dure la toux ?

T099
Patient :
Comment savoir si j'ai la tuberculose ?
Mots-clés :
savoir tuberculose 
Intention :
Dépistage 
Question suivante :
Présentez-vous une toux depuis plus de deux semaines ?

T100
Patient :
Je veux tout savoir sur la tuberculose.
Mots-clés :
tout savoir tuberculose 
Intention :
Éducation sanitaire complète 
Question suivante :
Souhaitez-vous commencer par les symptômes, la transmission, le dépistage ou le traitement ?

Catégorie terminée
✅ TUBERCULOSE : T001 à T100 complétés
Mots-clés majeurs collectés
tousse plusieurs semaines
toux ne finit pas
crache sang
fièvre chaque soir
transpire nuit
perdu poids
plus appétit
mal poitrine
essoufflé
contact tuberculose
GeneXpert
radiographie thorax
traité mais tousse
rechute tuberculose
tuberculose résistante
porter masque
guérir tuberculose
peur rejeté
signes tuberculose
tout savoir tuberculose




























URGENCES (U001 à U020)
U001
Patient :
Je saigne beaucoup.
Mots-clés :
saigne beaucoup 
Urgence :
Critique 🔴 
Symptômes détectés :
Hémorragie 
Question suivante :
D'où vient le saignement ?

U002
Patient :
Le sang ne s'arrête pas.
Mots-clés :
sang ne s'arrête pas 
Urgence :
Critique 🔴 
Question suivante :
Depuis combien de temps saignez-vous ?

U003
Patient :
J'ai perdu connaissance.
Mots-clés :
perdu connaissance 
Urgence :
Critique 🔴 
Question suivante :
Êtes-vous réveillé maintenant ?

U004
Patient :
Une personne est inconsciente.
Mots-clés :
personne inconsciente 
Urgence :
Critique 🔴 
Question suivante :
Respire-t-elle normalement ?

U005
Patient :
Je ne respire plus bien.
Mots-clés :
ne respire plus bien 
Urgence :
Critique 🔴 
Symptômes détectés :
Détresse respiratoire 
Question suivante :
Depuis quand avez-vous cette difficulté à respirer ?

U006
Patient :
J'étouffe.
Mots-clés :
étouffe 
Urgence :
Critique 🔴 
Question suivante :
Pouvez-vous encore parler ?

U007
Patient :
Mon enfant convulse.
Mots-clés :
enfant convulse 
Urgence :
Critique 🔴 
Question suivante :
Depuis combien de temps dure la convulsion ?

U008
Patient :
J'ai des convulsions.
Mots-clés :
convulsions 
Urgence :
Critique 🔴 
Question suivante :
Est-ce la première fois ?

U009
Patient :
Mon enfant ne se réveille pas.
Mots-clés :
ne se réveille pas 
Urgence :
Critique 🔴 
Question suivante :
Respire-t-il normalement ?

U010
Patient :
Je suis très faible et je ne peux plus marcher.
Mots-clés :
ne peut plus marcher 
Urgence :
Élevée 🟠 
Question suivante :
Depuis quand cette faiblesse est-elle apparue ?

U011
Patient :
J'ai une douleur très forte dans la poitrine.
Mots-clés :
douleur poitrine forte 
Urgence :
Critique 🔴 
Question suivante :
La douleur est-elle apparue soudainement ?

U012
Patient :
J'ai une douleur brutale au cœur.
Mots-clés :
douleur cœur 
Urgence :
Critique 🔴 
Question suivante :
Avez-vous du mal à respirer ?

U013
Patient :
Mon visage est soudainement paralysé.
Mots-clés :
visage paralysé 
Urgence :
Critique 🔴 
Symptômes détectés :
AVC possible 
Question suivante :
Depuis combien de temps cela a-t-il commencé ?

U014
Patient :
Je ne peux plus bouger un bras.
Mots-clés :
ne peut plus bouger bras 
Urgence :
Critique 🔴 
Question suivante :
Cela est-il apparu soudainement ?

U015
Patient :
Je ne peux plus parler correctement.
Mots-clés :
ne peut plus parler 
Urgence :
Critique 🔴 
Symptômes détectés :
AVC possible 
Question suivante :
Depuis quand avez-vous cette difficulté ?

U016
Patient :
J'ai été mordu par un serpent.
Mots-clés :
mordu serpent 
Urgence :
Critique 🔴 
Question suivante :
Quand la morsure a-t-elle eu lieu ?

U017
Patient :
J'ai été piqué par un scorpion.
Mots-clés :
piqué scorpion 
Urgence :
Élevée 🟠 
Question suivante :
Où avez-vous été piqué ?

U018
Patient :
J'ai avalé un produit toxique.
Mots-clés :
avalé produit toxique 
Urgence :
Critique 🔴 
Question suivante :
Quel produit avez-vous avalé ?

U019
Patient :
Mon enfant a bu du pétrole.
Mots-clés :
bu pétrole 
Urgence :
Critique 🔴 
Question suivante :
Quand cela s'est-il produit ?

U020
Patient :
J'ai été électrocuté.
Mots-clés :
électrocuté 
Urgence :
Critique 🔴 
Question suivante :
Êtes-vous conscient et capable de bouger ?

Dictionnaire initial Urgences
saigne beaucoup
sang ne s'arrête pas
perdu connaissance
personne inconsciente
ne respire plus bien
étouffe
enfant convulse
convulsions
ne se réveille pas
ne peut plus marcher
douleur poitrine forte
douleur cœur
visage paralysé
ne peut plus bouger bras
ne peut plus parler
mordu serpent
piqué scorpion
avalé produit toxique
bu pétrole
électrocuté
U021
Patient :
Je me suis brûlé avec de l'eau chaude.
Mots-clés :
brûlé eau chaude 
Urgence :
Élevée 🟠 
Question suivante :
Quelle partie du corps est brûlée ?

U022
Patient :
Mon enfant s'est brûlé.
Mots-clés :
enfant brûlé 
Urgence :
Élevée 🟠 
Question suivante :
Quel âge a l'enfant et quelle surface est brûlée ?

U023
Patient :
Je me suis brûlé avec le feu.
Mots-clés :
brûlé feu 
Urgence :
Élevée 🟠 
Question suivante :
La brûlure est-elle profonde ou étendue ?

U024
Patient :
J'ai reçu une décharge électrique.
Mots-clés :
décharge électrique 
Urgence :
Critique 🔴 
Question suivante :
Avez-vous perdu connaissance ?

U025
Patient :
J'ai eu un accident de moto.
Mots-clés :
accident moto 
Urgence :
Critique 🔴 
Question suivante :
Êtes-vous blessé ou inconscient ?

U026
Patient :
J'ai eu un accident de voiture.
Mots-clés :
accident voiture 
Urgence :
Critique 🔴 
Question suivante :
Avez-vous des douleurs importantes ou un saignement ?

U027
Patient :
Je suis tombé d'un arbre.
Mots-clés :
tombé arbre 
Urgence :
Élevée 🟠 
Question suivante :
Pouvez-vous bouger vos bras et vos jambes ?

U028
Patient :
Je suis tombé d'un toit.
Mots-clés :
tombé toit 
Urgence :
Critique 🔴 
Question suivante :
Avez-vous perdu connaissance ?

U029
Patient :
J'ai reçu un coup à la tête.
Mots-clés :
coup tête 
Urgence :
Élevée 🟠 
Question suivante :
Avez-vous vomi ou perdu connaissance après le choc ?

U030
Patient :
Ma tête saigne après une chute.
Mots-clés :
tête saigne 
Urgence :
Élevée 🟠 
Question suivante :
Le saignement est-il abondant ?

U031
Patient :
Mon bras semble cassé.
Mots-clés :
bras cassé 
Urgence :
Élevée 🟠 
Question suivante :
Pouvez-vous encore bouger le bras ?

U032
Patient :
Je pense que ma jambe est cassée.
Mots-clés :
jambe cassée 
Urgence :
Élevée 🟠 
Question suivante :
Pouvez-vous poser le pied au sol ?

U033
Patient :
Mon os est visible.
Mots-clés :
os visible 
Urgence :
Critique 🔴 
Symptômes détectés :
Fracture ouverte 
Question suivante :
Le saignement est-il important ?

U034
Patient :
J'ai une blessure profonde.
Mots-clés :
blessure profonde 
Urgence :
Élevée 🟠 
Question suivante :
La plaie continue-t-elle à saigner ?

U035
Patient :
J'ai été poignardé.
Mots-clés :
poignardé 
Urgence :
Critique 🔴 
Question suivante :
Où se situe la blessure ?

U036
Patient :
J'ai reçu une balle.
Mots-clés :
reçu balle 
Urgence :
Critique 🔴 
Question suivante :
La victime est-elle consciente ?

U037
Patient :
Quelqu'un se noie.
Mots-clés :
se noie 
Urgence :
Critique 🔴 
Question suivante :
La personne a-t-elle été sortie de l'eau ?

U038
Patient :
Mon enfant est tombé dans l'eau.
Mots-clés :
tombé eau 
Urgence :
Critique 🔴 
Question suivante :
L'enfant respire-t-il normalement ?

U039
Patient :
J'ai inhalé beaucoup de fumée.
Mots-clés :
inhalé fumée 
Urgence :
Élevée 🟠 
Question suivante :
Avez-vous des difficultés à respirer ?

U040
Patient :
Une maison a brûlé et il y a des blessés.
Mots-clés :
maison brûlé 
blessés incendie 
Urgence :
Critique 🔴 
Question suivante :
Les victimes sont-elles conscientes et respirent-elles ?

Nouveaux mots-clés Urgences
brûlé eau chaude
enfant brûlé
brûlé feu
décharge électrique
accident moto
accident voiture
tombé arbre
tombé toit
coup tête
tête saigne
bras cassé
jambe cassée
os visible
blessure profonde
poignardé
reçu balle
se noie
tombé eau
inhalé fumée
blessés incendie
U041
Patiente :
Je suis enceinte et je saigne beaucoup.
Mots-clés :
enceinte saigne beaucoup 
Urgence :
Critique 🔴 
Question suivante :
De combien de mois est votre grossesse ?

U042
Patiente :
J'ai du sang pendant ma grossesse.
Mots-clés :
sang grossesse 
Urgence :
Critique 🔴 
Question suivante :
La quantité de sang est-elle importante ?

U043
Patiente :
J'ai de fortes douleurs et je suis enceinte.
Mots-clés :
fortes douleurs enceinte 
Urgence :
Élevée 🟠 
Question suivante :
Où ressentez-vous la douleur ?

U044
Patiente :
Mon bébé ne bouge plus dans mon ventre.
Mots-clés :
bébé ne bouge plus 
Urgence :
Critique 🔴 
Question suivante :
Depuis combien d'heures ne sentez-vous plus les mouvements ?

U045
Patiente :
J'ai des convulsions pendant ma grossesse.
Mots-clés :
convulsions grossesse 
Urgence :
Critique 🔴 
Symptômes détectés :
Éclampsie possible 
Question suivante :
Êtes-vous actuellement consciente et accompagnée ?

U046
Patiente :
J'ai très mal à la tête et je suis enceinte.
Mots-clés :
mal tête enceinte 
Urgence :
Élevée 🟠 
Question suivante :
Avez-vous une vision floue ou des convulsions ?

U047
Patiente :
Mon visage est très gonflé pendant la grossesse.
Mots-clés :
visage gonflé grossesse 
Urgence :
Élevée 🟠 
Question suivante :
Avez-vous aussi des maux de tête importants ?

U048
Patiente :
Mes pieds sont très gonflés et je suis enceinte.
Mots-clés :
pieds gonflés enceinte 
Urgence :
Élevée 🟠 
Question suivante :
Ce gonflement est-il apparu soudainement ?

U049
Patiente :
J'ai perdu les eaux.
Mots-clés :
perdu les eaux 
Urgence :
Élevée 🟠 
Question suivante :
Avez-vous déjà des contractions ?

U050
Patiente :
Mes contractions sont très rapprochées.
Mots-clés :
contractions rapprochées 
Urgence :
Élevée 🟠 
Question suivante :
Toutes les combien de minutes surviennent-elles ?

U051
Patiente :
J'accouche mais le bébé ne sort pas.
Mots-clés :
bébé ne sort pas 
Urgence :
Critique 🔴 
Question suivante :
Depuis combien de temps poussez-vous ?

U052
Patiente :
Le travail dure depuis très longtemps.
Mots-clés :
travail très long 
Urgence :
Critique 🔴 
Question suivante :
Depuis combien d'heures avez-vous des contractions ?

U053
Patiente :
J'ai accouché mais je saigne beaucoup.
Mots-clés :
saigne après accouchement 
Urgence :
Critique 🔴 
Question suivante :
Le saignement est-il abondant en ce moment ?

U054
Patiente :
Je perds beaucoup de sang après la naissance du bébé.
Mots-clés :
beaucoup sang naissance 
Urgence :
Critique 🔴 
Question suivante :
Êtes-vous étourdie ou très faible ?

U055
Patiente :
Le placenta n'est pas encore sorti.
Mots-clés :
placenta pas sorti 
Urgence :
Critique 🔴 
Question suivante :
Depuis combien de temps avez-vous accouché ?

U056
Patiente :
J'ai accouché à la maison et je vais mal.
Mots-clés :
accouché maison 
Urgence :
Élevée 🟠 
Question suivante :
Quels symptômes ressentez-vous actuellement ?

U057
Parent :
Le bébé ne pleure pas après la naissance.
Mots-clés :
bébé ne pleure pas 
Urgence :
Critique 🔴 
Question suivante :
Le bébé respire-t-il ?

U058
Parent :
Mon nouveau-né ne respire pas bien.
Mots-clés :
nouveau né respire mal 
Urgence :
Critique 🔴 
Question suivante :
Le bébé devient-il bleu ou très faible ?

U059
Parent :
Mon bébé est né prématurément.
Mots-clés :
bébé prématuré 
Urgence :
Élevée 🟠 
Question suivante :
Le bébé respire-t-il normalement ?

U060
Parent :
Le cordon ombilical du bébé saigne.
Mots-clés :
cordon saigne 
Urgence :
Élevée 🟠 
Question suivante :
Le saignement est-il continu ou léger ?

Nouveaux mots-clés Urgences
enceinte saigne beaucoup
sang grossesse
fortes douleurs enceinte
bébé ne bouge plus
convulsions grossesse
mal tête enceinte
visage gonflé grossesse
pieds gonflés enceinte
perdu les eaux
contractions rapprochées
bébé ne sort pas
travail très long
saigne après accouchement
beaucoup sang naissance
placenta pas sorti
accouché maison
bébé ne pleure pas
nouveau né respire mal
bébé prématuré
cordon saigne
U061
Patient :
Mon enfant a une diarrhée sévère et ne boit plus.
Mots-clés :
diarrhée sévère 
ne boit plus 
Urgence :
Critique 🔴 
Question suivante :
L'enfant urine-t-il encore normalement ?

U062
Patient :
Mon enfant a les yeux très enfoncés.
Mots-clés :
yeux enfoncés 
Urgence :
Critique 🔴 
Symptômes détectés :
Déshydratation sévère 
Question suivante :
Depuis combien de jours l'enfant est-il malade ?

U063
Patient :
Mon enfant est très faible et ne réagit presque plus.
Mots-clés :
très faible 
ne réagit plus 
Urgence :
Critique 🔴 
Question suivante :
L'enfant est-il conscient ?

U064
Patient :
Mon enfant refuse complètement de manger.
Mots-clés :
refuse manger 
Urgence :
Élevée 🟠 
Question suivante :
Depuis combien de temps refuse-t-il de manger ?

U065
Patient :
Je tremble et je transpire beaucoup.
Mots-clés :
tremble 
transpire beaucoup 
Urgence :
Élevée 🟠 
Symptômes détectés :
Hypoglycémie possible 
Question suivante :
Êtes-vous diabétique ou avez-vous jeûné longtemps ?

U066
Patient :
Je me sens très faible et confus.
Mots-clés :
faible 
confus 
Urgence :
Critique 🔴 
Question suivante :
Êtes-vous capable de répondre correctement aux questions ?

U067
Patient :
J'ai une très forte fièvre et je délire.
Mots-clés :
forte fièvre 
délire 
Urgence :
Critique 🔴 
Question suivante :
Depuis quand la fièvre a-t-elle commencé ?

U068
Patient :
Mon enfant a une fièvre très élevée.
Mots-clés :
enfant forte fièvre 
Urgence :
Élevée 🟠 
Question suivante :
Quelle est la température mesurée ?

U069
Patient :
J'ai le cou très raide et de la fièvre.
Mots-clés :
cou raide 
fièvre 
Urgence :
Critique 🔴 
Symptômes détectés :
Méningite possible 
Question suivante :
Avez-vous aussi des maux de tête importants ?

U070
Patient :
Mon enfant ne supporte pas la lumière.
Mots-clés :
ne supporte pas lumière 
Urgence :
Critique 🔴 
Question suivante :
A-t-il aussi de la fièvre ou une raideur du cou ?

U071
Patient :
Mon visage gonfle rapidement.
Mots-clés :
visage gonfle rapidement 
Urgence :
Critique 🔴 
Symptômes détectés :
Réaction allergique grave 
Question suivante :
Avez-vous du mal à respirer ?

U072
Patient :
J'ai mangé quelque chose et je gonfle.
Mots-clés :
mangé quelque chose 
gonfle 
Urgence :
Critique 🔴 
Question suivante :
Avez-vous des difficultés respiratoires ?

U073
Patient :
J'ai une éruption sur tout le corps et je respire mal.
Mots-clés :
éruption corps 
respire mal 
Urgence :
Critique 🔴 
Question suivante :
Depuis combien de temps les symptômes ont-ils commencé ?

U074
Patient :
Mon enfant a avalé des médicaments.
Mots-clés :
avalé médicaments 
Urgence :
Critique 🔴 
Question suivante :
Quels médicaments ont été avalés ?

U075
Patient :
J'ai bu un produit chimique.
Mots-clés :
bu produit chimique 
Urgence :
Critique 🔴 
Question suivante :
Quel produit avez-vous bu ?

U076
Patient :
Mon enfant a avalé du savon liquide.
Mots-clés :
avalé savon liquide 
Urgence :
Élevée 🟠 
Question suivante :
Quelle quantité a été avalée ?

U077
Patient :
Je vomis sans arrêt.
Mots-clés :
vomis sans arrêt 
Urgence :
Élevée 🟠 
Question suivante :
Depuis combien d'heures ou de jours vomissez-vous ?

U078
Patient :
Je ne peux rien garder dans mon estomac.
Mots-clés :
rien garder estomac 
Urgence :
Élevée 🟠 
Question suivante :
Arrivez-vous à boire un peu d'eau ?

U079
Patient :
J'ai perdu beaucoup de liquide à cause des vomissements.
Mots-clés :
beaucoup liquide 
vomissements 
Urgence :
Critique 🔴 
Question suivante :
Avez-vous des vertiges ou une grande faiblesse ?

U080
Patient :
Mon enfant est très malade et devient mou.
Mots-clés :
enfant devient mou 
Urgence :
Critique 🔴 
Question suivante :
L'enfant est-il conscient et réagit-il quand on lui parle ?

Nouveaux mots-clés Urgences
diarrhée sévère
ne boit plus
yeux enfoncés
ne réagit plus
refuse manger
tremble
transpire beaucoup
faible confus
forte fièvre délire
enfant forte fièvre
cou raide
ne supporte pas lumière
visage gonfle rapidement
gonfle après manger
éruption corps
avalé médicaments
bu produit chimique
avalé savon liquide
vomis sans arrêt
enfant devient mou
U081
Patient :
Je suis très pâle et je me sens mourir.
Mots-clés :
très pâle 
se sent mourir 
Urgence :
Critique 🔴 
Question suivante :
Avez-vous un saignement ou une maladie connue ?

U082
Patient :
Je suis tombé dans le coma.
Mots-clés :
coma 
Urgence :
Critique 🔴 
Question suivante :
La personne respire-t-elle normalement ?

U083
Patient :
Mon frère ne répond plus quand on lui parle.
Mots-clés :
ne répond plus 
Urgence :
Critique 🔴 
Question suivante :
Est-il conscient ou inconscient ?

U084
Patient :
Je m'évanouis plusieurs fois.
Mots-clés :
évanouis plusieurs fois 
Urgence :
Critique 🔴 
Question suivante :
Combien de fois cela est-il arrivé aujourd'hui ?

U085
Patient :
Mon cœur bat très vite.
Mots-clés :
cœur bat vite 
Urgence :
Élevée 🟠 
Question suivante :
Avez-vous une douleur dans la poitrine ?

U086
Patient :
Mon cœur bat de façon irrégulière.
Mots-clés :
cœur irrégulier 
Urgence :
Élevée 🟠 
Question suivante :
Ressentez-vous des vertiges ou un malaise ?

U087
Patient :
J'ai une douleur très forte dans la poitrine qui descend vers le bras.
Mots-clés :
douleur poitrine bras 
Urgence :
Critique 🔴 
Symptômes détectés :
Crise cardiaque possible 
Question suivante :
Avez-vous du mal à respirer ?

U088
Patient :
Je transpire beaucoup avec une douleur dans la poitrine.
Mots-clés :
transpire douleur poitrine 
Urgence :
Critique 🔴 
Question suivante :
La douleur est-elle apparue brutalement ?

U089
Patient :
Je respire très rapidement.
Mots-clés :
respire rapidement 
Urgence :
Critique 🔴 
Question suivante :
Avez-vous une maladie respiratoire connue ?

U090
Patient :
Je ne peux presque plus respirer.
Mots-clés :
presque plus respirer 
Urgence :
Critique 🔴 
Question suivante :
Êtes-vous capable de parler normalement ?

U091
Patient :
J'ai les lèvres bleues.
Mots-clés :
lèvres bleues 
Urgence :
Critique 🔴 
Symptômes détectés :
Manque d'oxygène 
Question suivante :
Avez-vous des difficultés respiratoires ?

U092
Patient :
Mon enfant respire difficilement.
Mots-clés :
enfant respire difficilement 
Urgence :
Critique 🔴 
Question suivante :
L'enfant a-t-il de la fièvre ou une toux ?

U093
Patient :
Ma respiration fait un bruit étrange.
Mots-clés :
respiration bruit étrange 
Urgence :
Critique 🔴 
Question suivante :
Depuis quand ce bruit est-il apparu ?

U094
Patient :
J'ai été agressé et je suis blessé.
Mots-clés :
agressé blessé 
Urgence :
Élevée 🟠 
Question suivante :
Où se trouvent les blessures ?

U095
Patient :
Je saigne après une bagarre.
Mots-clés :
saigne bagarre 
Urgence :
Critique 🔴 
Question suivante :
Le saignement est-il abondant ?

U096
Patient :
Une personne a été gravement blessée dans mon village.
Mots-clés :
gravement blessée 
Urgence :
Critique 🔴 
Question suivante :
La personne est-elle consciente ?

U097
Patient :
J'ai besoin d'une ambulance.
Mots-clés :
besoin ambulance 
Urgence :
Critique 🔴 
Question suivante :
Quelle est l'urgence principale ?

U098
Patient :
Faut-il aller immédiatement à l'hôpital ?
Mots-clés :
immédiatement hôpital 
Urgence :
Évaluation rapide nécessaire 
Question suivante :
Quels symptômes présentez-vous actuellement ?

U099
Patient :
C'est une urgence médicale.
Mots-clés :
urgence médicale 
Urgence :
Critique 🔴 
Question suivante :
Décrivez rapidement le principal problème.

U100
Patient :
Aidez-moi, c'est très grave.
Mots-clés :
aidez moi 
très grave 
Urgence :
Critique 🔴 
Question suivante :
Que se passe-t-il exactement ?

Catégorie terminée
✅ URGENCES : U001 à U100 complétés
Mots-clés majeurs collectés
saigne beaucoup
perdu connaissance
personne inconsciente
étouffe
convulsions
visage paralysé
mordu serpent
accident moto
accident voiture
bras cassé
jambe cassée
os visible
poignardé
reçu balle
bébé ne bouge plus
convulsions grossesse
saigne après accouchement
cou raide
lèvres bleues
besoin ambulance





🍽️ NUTRITION (N001 à N020)

N001
Patient :
Je suis toujours fatigué et je n’ai pas de force.
Mots-clés :
fatigue constante
Risque :
Élevé 🟠
Symptômes détectés :
Possible malnutrition / carence
Question suivante :
Mangez-vous régulièrement chaque jour ?

N002
Patient :
Je mange très peu chaque jour.
Mots-clés :
mange peu
Risque :
Élevé 🟠
Symptômes détectés :
Apport alimentaire insuffisant
Question suivante :
Depuis combien de temps mangez-vous peu ?

N003
Patient :
Mon enfant ne grandit pas normalement.
Mots-clés :
retard croissance enfant
Risque :
Critique 🔴
Symptômes détectés :
Retard de croissance
Question suivante :
Quel âge a l’enfant ?

N004
Patient :
Je suis très maigre.
Mots-clés :
amaigrissement
Risque :
Élevé 🟠
Symptômes détectés :
Dénutrition possible
Question suivante :
Avez-vous perdu du poids récemment ?

N005
Patient :
Je n’ai plus d’appétit.
Mots-clés :
perte d’appétit
Risque :
Élevé 🟠
Symptômes détectés :
Trouble nutritionnel
Question suivante :
Depuis quand n’avez-vous plus d’appétit ?

N006
Patient :
Je mange mais je reste faible.
Mots-clés :
faible malgré alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Mauvaise absorption nutritionnelle possible
Question suivante :
Avez-vous des douleurs abdominales ou diarrhée ?

N007
Patient :
Mon enfant a le ventre gonflé.
Mots-clés :
ventre gonflé enfant
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition sévère possible (kwashiorkor)
Question suivante :
L’enfant mange-t-il normalement ?

N008
Patient :
Je mange toujours la même nourriture.
Mots-clés :
alimentation non variée
Risque :
Modéré 🟡
Symptômes détectés :
Carence nutritionnelle possible
Question suivante :
Quels aliments consommez-vous le plus souvent ?

N009
Patient :
Je me sens souvent étourdi.
Mots-clés :
étourdissement alimentation
Risque :
Modéré 🟡
Symptômes détectés :
Possible manque de fer ou vitamines
Question suivante :
Buvez-vous assez d’eau chaque jour ?

N010
Patient :
Je n’ai pas mangé depuis hier.
Mots-clés :
jeûne prolongé
Risque :
Élevé 🟠
Symptômes détectés :
Hypoglycémie possible
Question suivante :
Pourquoi n’avez-vous pas mangé ?

N011
Patient :
Je ressens des crampes fréquentes.
Mots-clés :
crampes nutrition
Risque :
Modéré 🟡
Symptômes détectés :
Manque de minéraux (magnésium/potassium)
Question suivante :
Avez-vous une alimentation riche en fruits et légumes ?

N012
Patient :
Je suis souvent malade.
Mots-clés :
immunité faible
Risque :
Élevé 🟠
Symptômes détectés :
Système immunitaire affaibli
Question suivante :
Comment est votre alimentation quotidienne ?

N013
Patient :
Mon enfant refuse de manger.
Mots-clés :
enfant refuse nourriture
Risque :
Élevé 🟠
Symptômes détectés :
Trouble alimentaire enfant
Question suivante :
Depuis quand l’enfant refuse-t-il de manger ?

N014
Patient :
Je n’ai pas accès à une alimentation équilibrée.
Mots-clés :
manque alimentation équilibrée
Risque :
Élevé 🟠
Symptômes détectés :
Insécurité alimentaire
Question suivante :
Quels aliments sont disponibles chez vous ?

N015
Patient :
Je perds mes cheveux.
Mots-clés :
chute cheveux nutrition
Risque :
Modéré 🟡
Symptômes détectés :
Carence en protéines ou fer
Question suivante :
Depuis quand avez-vous ce problème ?

N016
Patient :
Je suis souvent malade après avoir mangé.
Mots-clés :
mal digestion nourriture
Risque :
Élevé 🟠
Symptômes détectés :
Trouble digestif ou intoxication alimentaire
Question suivante :
Quels aliments provoquent cela ?

N017
Patient :
Je bois très peu d’eau.
Mots-clés :
déshydratation
Risque :
Élevé 🟠
Symptômes détectés :
Risque de déshydratation
Question suivante :
Pourquoi ne buvez-vous pas assez d’eau ?

N018
Patient :
Je mange trop de nourriture sucrée.
Mots-clés :
excès sucre
Risque :
Modéré 🟡
Symptômes détectés :
Déséquilibre alimentaire
Question suivante :
Mangez-vous aussi des légumes et protéines ?

N019
Patient :
Mon enfant est très faible et dort tout le temps.
Mots-clés :
enfant faible somnolent
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition sévère ou infection associée
Question suivante :
Depuis quand cet état a-t-il commencé ?

N020
Patient :
Je n’ai pas les moyens de bien manger.
Mots-clés :
pauvreté alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Insécurité alimentaire
Question suivante :
Quelles sont vos principales sources de nourriture ?
N021
Patient :
Je mange mais je ne prends pas de poids.
Mots-clés :
ne prend pas de poids
Risque :
Élevé 🟠
Symptômes détectés :
Mauvaise assimilation nutritionnelle
Question suivante :
Avez-vous des diarrhées fréquentes ?

N022
Patient :
Mon enfant est très mince pour son âge.
Mots-clés :
enfant maigre
Risque :
Critique 🔴
Symptômes détectés :
Dénutrition infantile
Question suivante :
Quel âge et quel poids fait l’enfant ?

N023
Patient :
Je suis souvent malade après les repas.
Mots-clés :
mal après manger
Risque :
Élevé 🟠
Symptômes détectés :
Trouble digestif ou intoxication alimentaire
Question suivante :
Quels aliments déclenchent ces symptômes ?

N024
Patient :
Je ressens des douleurs dans l’estomac.
Mots-clés :
douleur estomac
Risque :
Modéré 🟡
Symptômes détectés :
Trouble digestif
Question suivante :
La douleur apparaît-elle après les repas ?

N025
Patient :
Je saute souvent des repas.
Mots-clés :
saut repas
Risque :
Élevé 🟠
Symptômes détectés :
Risque de malnutrition
Question suivante :
Pourquoi sautez-vous les repas ?

N026
Patient :
Je me sens faible le matin.
Mots-clés :
faiblesse matin
Risque :
Modéré 🟡
Symptômes détectés :
Hypoglycémie possible
Question suivante :
Que mangez-vous le soir ?

N027
Patient :
Je ne mange presque jamais de viande.
Mots-clés :
pas de protéines animales
Risque :
Modéré 🟡
Symptômes détectés :
Carence en protéines
Question suivante :
Remplacez-vous la viande par d’autres protéines ?

N028
Patient :
Mon enfant a souvent des infections.
Mots-clés :
enfant infections fréquentes
Risque :
Élevé 🟠
Symptômes détectés :
Immunité faible liée à la nutrition
Question suivante :
Comment est son alimentation quotidienne ?

N029
Patient :
Je mange surtout du manioc.
Mots-clés :
alimentation monotone manioc
Risque :
Modéré 🟡
Symptômes détectés :
Alimentation déséquilibrée
Question suivante :
Mangez-vous d’autres aliments avec le manioc ?

N030
Patient :
Je suis souvent essoufflé sans effort.
Mots-clés :
essoufflement fatigue
Risque :
Élevé 🟠
Symptômes détectés :
Carence en fer possible
Question suivante :
Avez-vous des vertiges ou fatigue intense ?

N031
Patient :
Je mange très gras tous les jours.
Mots-clés :
excès gras
Risque :
Modéré 🟡
Symptômes détectés :
Déséquilibre alimentaire
Question suivante :
Avez-vous des douleurs abdominales ou prise de poids ?

N032
Patient :
Mon enfant a les cheveux fins et cassants.
Mots-clés :
cheveux cassants enfant
Risque :
Élevé 🟠
Symptômes détectés :
Carence en protéines ou vitamines
Question suivante :
Depuis quand avez-vous remarqué cela ?

N033
Patient :
Je ne mange pas de fruits.
Mots-clés :
absence fruits
Risque :
Modéré 🟡
Symptômes détectés :
Carence en vitamines
Question suivante :
Mangez-vous des légumes ?

N034
Patient :
Je suis souvent constipé.
Mots-clés :
constipation
Risque :
Modéré 🟡
Symptômes détectés :
Manque de fibres
Question suivante :
Buvez-vous suffisamment d’eau ?

N035
Patient :
Je mange tard le soir.
Mots-clés :
repas tardif
Risque :
Faible 🟢
Symptômes détectés :
Habitude alimentaire déséquilibrée
Question suivante :
Avez-vous des troubles du sommeil ?

N036
Patient :
Je ne prends jamais de petit-déjeuner.
Mots-clés :
pas petit déjeuner
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre énergétique
Question suivante :
Pourquoi ne prenez-vous pas de petit-déjeuner ?

N037
Patient :
Je suis souvent malade en saison des pluies.
Mots-clés :
maladies saisonnières
Risque :
Élevé 🟠
Symptômes détectés :
Immunité faible
Question suivante :
Comment est votre alimentation pendant cette période ?

N038
Patient :
Je mange sans savoir si c’est équilibré.
Mots-clés :
alimentation non contrôlée
Risque :
Modéré 🟡
Symptômes détectés :
Manque d’éducation nutritionnelle
Question suivante :
Avez-vous accès à des conseils nutritionnels ?

N039
Patient :
Mon enfant refuse les légumes.
Mots-clés :
refus légumes enfant
Risque :
Modéré 🟡
Symptômes détectés :
Déséquilibre alimentaire infantile
Question suivante :
Quels aliments préfère-t-il ?

N040
Patient :
Je mange seulement une fois par jour.
Mots-clés :
un repas par jour
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition sévère possible
Question suivante :
Pourquoi mangez-vous si peu ?
N041
Patient :
Je mange mais je reste toujours fatigué.
Mots-clés :
fatigue malgré alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Carence en fer ou vitamines possible
Question suivante :
Avez-vous des vertiges ou maux de tête ?

N042
Patient :
Mon enfant a un retard de développement.
Mots-clés :
retard développement enfant
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition chronique
Question suivante :
Depuis quel âge avez-vous remarqué cela ?

N043
Patient :
Je mange très mal équilibré.
Mots-clés :
alimentation déséquilibrée
Risque :
Élevé 🟠
Symptômes détectés :
Risque de carences multiples
Question suivante :
Quels aliments consommez-vous le plus ?

N044
Patient :
Je n’ai pas assez de nourriture pour toute la famille.
Mots-clés :
insécurité alimentaire famille
Risque :
Critique 🔴
Symptômes détectés :
Risque de malnutrition familiale
Question suivante :
Combien de repas prenez-vous par jour ?

N045
Patient :
Je ressens des douleurs dans les jambes.
Mots-clés :
douleur jambes nutrition
Risque :
Modéré 🟡
Symptômes détectés :
Carence en minéraux possible
Question suivante :
Avez-vous des crampes nocturnes ?

N046
Patient :
Je bois surtout des boissons sucrées.
Mots-clés :
boissons sucrées
Risque :
Modéré 🟡
Symptômes détectés :
Déséquilibre alimentaire
Question suivante :
Buvez-vous aussi de l’eau propre ?

N047
Patient :
Mon enfant mange mais reste très faible.
Mots-clés :
enfant faible malgré nourriture
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition sévère possible
Question suivante :
A-t-il souvent des maladies ?

N048
Patient :
Je n’ai pas assez de protéines dans mon alimentation.
Mots-clés :
manque protéines
Risque :
Élevé 🟠
Symptômes détectés :
Carence protéique
Question suivante :
Mangez-vous des œufs ou des haricots ?

N049
Patient :
Je mange trop salé.
Mots-clés :
excès sel
Risque :
Modéré 🟡
Symptômes détectés :
Risque hypertension future
Question suivante :
Avez-vous des maux de tête fréquents ?

N050
Patient :
Je saute souvent le dîner.
Mots-clés :
saut dîner
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre énergétique
Question suivante :
Pourquoi sautez-vous le dîner ?

N051
Patient :
Je mange mais je suis souvent malade.
Mots-clés :
maladie fréquente alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Immunité faible
Question suivante :
Quels types de maladies avez-vous souvent ?

N052
Patient :
Je n’ai pas accès à des légumes frais.
Mots-clés :
absence légumes
Risque :
Élevé 🟠
Symptômes détectés :
Carence en vitamines
Question suivante :
Quels aliments mangez-vous à la place ?

N053
Patient :
Je mange très vite sans bien mâcher.
Mots-clés :
manger vite
Risque :
Faible 🟢
Symptômes détectés :
Mauvaise digestion possible
Question suivante :
Avez-vous des douleurs d’estomac après repas ?

N054
Patient :
Je suis souvent pâle.
Mots-clés :
pâleur
Risque :
Élevé 🟠
Symptômes détectés :
Carence en fer (anémie possible)
Question suivante :
Vous sentez-vous souvent fatigué ?

N055
Patient :
Je ne mange pas assez de nourriture variée.
Mots-clés :
manque variété alimentaire
Risque :
Élevé 🟠
Symptômes détectés :
Carences multiples possibles
Question suivante :
Quels aliments mangez-vous chaque jour ?

N056
Patient :
Mon enfant est souvent anémique.
Mots-clés :
anémie enfant
Risque :
Critique 🔴
Symptômes détectés :
Carence en fer sévère
Question suivante :
A-t-il une alimentation riche en fer ?

N057
Patient :
Je bois rarement du lait.
Mots-clés :
manque lait
Risque :
Modéré 🟡
Symptômes détectés :
Carence en calcium possible
Question suivante :
Consommez-vous d’autres produits riches en calcium ?

N058
Patient :
Je mange surtout des aliments transformés.
Mots-clés :
aliments transformés
Risque :
Élevé 🟠
Symptômes détectés :
Mauvaise qualité nutritionnelle
Question suivante :
Consommez-vous des aliments naturels ?

N059
Patient :
Je ne mange pas assez de fibres.
Mots-clés :
manque fibres
Risque :
Modéré 🟡
Symptômes détectés :
Risque de constipation
Question suivante :
Avez-vous souvent des problèmes digestifs ?

N060
Patient :
Je mange uniquement ce que je trouve.
Mots-clés :
alimentation non planifiée
Risque :
Élevé 🟠
Symptômes détectés :
Insécurité nutritionnelle
Question suivante :
Avez-vous la possibilité de planifier vos repas ?
N061
Patient :
Je mange mais je n’ai pas d’énergie.
Mots-clés :
pas d’énergie alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Carence énergétique ou vitaminique
Question suivante :
Dormez-vous suffisamment chaque nuit ?

N062
Patient :
Mon enfant a souvent faim mais ne mange pas bien.
Mots-clés :
enfant faim mal alimentation
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition infantile possible
Question suivante :
Quels aliments donnez-vous à l’enfant ?

N063
Patient :
Je saute le déjeuner presque chaque jour.
Mots-clés :
saut déjeuner
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre alimentaire
Question suivante :
Pourquoi sautez-vous ce repas ?

N064
Patient :
Je mange surtout des aliments frits.
Mots-clés :
aliments frits
Risque :
Modéré 🟡
Symptômes détectés :
Alimentation déséquilibrée
Question suivante :
Mangez-vous des fruits ou légumes ?

N065
Patient :
Je me sens faible après chaque repas.
Mots-clés :
faiblesse après repas
Risque :
Élevé 🟠
Symptômes détectés :
Trouble digestif ou glycémique possible
Question suivante :
Quels aliments provoquent cela le plus ?

N066
Patient :
Je n’ai pas assez à manger chaque semaine.
Mots-clés :
manque nourriture semaine
Risque :
Critique 🔴
Symptômes détectés :
Insécurité alimentaire sévère
Question suivante :
Combien de jours par semaine mangez-vous correctement ?

N067
Patient :
Je mange beaucoup de sel dans mes repas.
Mots-clés :
excès sel alimentation
Risque :
Modéré 🟡
Symptômes détectés :
Risque hypertension future
Question suivante :
Avez-vous des maux de tête fréquents ?

N068
Patient :
Je n’ai jamais de repas fixes.
Mots-clés :
repas irréguliers
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre nutritionnel
Question suivante :
Pourquoi vos repas sont-ils irréguliers ?

N069
Patient :
Mon enfant refuse de boire de l’eau.
Mots-clés :
refus eau enfant
Risque :
Élevé 🟠
Symptômes détectés :
Risque de déshydratation
Question suivante :
Depuis quand refuse-t-il de boire ?

N070
Patient :
Je mange mais je reste malade souvent.
Mots-clés :
maladie fréquente alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Immunité faible
Question suivante :
Quelles maladies avez-vous le plus souvent ?

N071
Patient :
Je mange surtout le soir.
Mots-clés :
alimentation soir uniquement
Risque :
Modéré 🟡
Symptômes détectés :
Déséquilibre énergétique
Question suivante :
Mangez-vous quelque chose le matin ?

N072
Patient :
Je me sens souvent faible en marchant.
Mots-clés :
faiblesse marche
Risque :
Élevé 🟠
Symptômes détectés :
Carence énergétique ou anémie possible
Question suivante :
Avez-vous des vertiges aussi ?

N073
Patient :
Je ne mange pas de protéines animales.
Mots-clés :
absence protéines animales
Risque :
Élevé 🟠
Symptômes détectés :
Carence protéique possible
Question suivante :
Consommez-vous des légumineuses ?

N074
Patient :
Je mange très peu par peur de manquer plus tard.
Mots-clés :
peur manque nourriture
Risque :
Élevé 🟠
Symptômes détectés :
Restriction alimentaire excessive
Question suivante :
Avez-vous accès régulier à la nourriture ?

N075
Patient :
Mon enfant est souvent fatigué.
Mots-clés :
enfant fatigue
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition ou anémie possible
Question suivante :
Depuis quand cette fatigue est-elle présente ?

N076
Patient :
Je mange très peu de légumes verts.
Mots-clés :
manque légumes verts
Risque :
Modéré 🟡
Symptômes détectés :
Carence en vitamines
Question suivante :
Quels légumes consommez-vous ?

N077
Patient :
Je saute souvent le petit-déjeuner.
Mots-clés :
saut petit déjeuner
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre énergétique
Question suivante :
Pourquoi sautez-vous ce repas ?

N078
Patient :
Je mange beaucoup mais je reste maigre.
Mots-clés :
maigre malgré nourriture
Risque :
Élevé 🟠
Symptômes détectés :
Trouble d’absorption possible
Question suivante :
Avez-vous des diarrhées fréquentes ?

N079
Patient :
Je bois rarement des boissons nutritives.
Mots-clés :
absence boissons nutritives
Risque :
Modéré 🟡
Symptômes détectés :
Apport nutritionnel faible
Question suivante :
Que buvez-vous habituellement ?

N080
Patient :
Je n’ai pas une alimentation stable.
Mots-clés :
alimentation instable
Risque :
Élevé 🟠
Symptômes détectés :
Insécurité nutritionnelle
Question suivante :
Combien de repas prenez-vous par jour en moyenne ?
N081
Patient :
Je mange mais je reste très faible physiquement.
Mots-clés :
faiblesse malgré alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Carence nutritionnelle ou anémie possible
Question suivante :
Avez-vous souvent des vertiges ?

N082
Patient :
Mon enfant ne mange presque rien.
Mots-clés :
enfant mange peu
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition infantile sévère
Question suivante :
Depuis quand l’enfant mange-t-il peu ?

N083
Patient :
Je saute souvent les repas sans raison.
Mots-clés :
saut repas fréquent
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre alimentaire
Question suivante :
Avez-vous accès facilement à la nourriture ?

N084
Patient :
Je mange surtout du riz et du manioc.
Mots-clés :
alimentation monotone
Risque :
Modéré 🟡
Symptômes détectés :
Carences possibles
Question suivante :
Mangez-vous des protéines ou légumes ?

N085
Patient :
Je suis souvent malade et je mange mal.
Mots-clés :
maladie + mauvaise alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Immunité faible liée à la nutrition
Question suivante :
Quelles maladies avez-vous souvent ?

N086
Patient :
Je mange mais je ne suis jamais rassasié.
Mots-clés :
faim constante
Risque :
Modéré 🟡
Symptômes détectés :
Déséquilibre alimentaire ou diabète possible
Question suivante :
Avez-vous soif excessive aussi ?

N087
Patient :
Je n’ai pas de nourriture variée à la maison.
Mots-clés :
absence variété alimentaire
Risque :
Élevé 🟠
Symptômes détectés :
Carences multiples
Question suivante :
Quels aliments consommez-vous le plus ?

N088
Patient :
Je mange très tard le soir.
Mots-clés :
repas tardif
Risque :
Modéré 🟡
Symptômes détectés :
Déséquilibre du rythme alimentaire
Question suivante :
Avez-vous des troubles du sommeil ?

N089
Patient :
Je mange très peu de fruits.
Mots-clés :
manque fruits
Risque :
Modéré 🟡
Symptômes détectés :
Carence en vitamines
Question suivante :
Mangez-vous des légumes régulièrement ?

N090
Patient :
Je me sens souvent étourdi après avoir mangé.
Mots-clés :
étourdissement après repas
Risque :
Élevé 🟠
Symptômes détectés :
Trouble glycémique possible
Question suivante :
Quels aliments provoquent cela ?

N091
Patient :
Je ne mange pas assez à cause du manque d’argent.
Mots-clés :
manque argent alimentation
Risque :
Critique 🔴
Symptômes détectés :
Insécurité alimentaire sévère
Question suivante :
Combien de repas par jour prenez-vous ?

N092
Patient :
Je mange toujours les mêmes aliments chaque jour.
Mots-clés :
alimentation répétitive
Risque :
Élevé 🟠
Symptômes détectés :
Carences nutritionnelles
Question suivante :
Quels aliments consommez-vous le plus ?

N093
Patient :
Mon enfant est très maigre et faible.
Mots-clés :
enfant maigre faible
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition sévère
Question suivante :
Depuis quand ce problème existe-t-il ?

N094
Patient :
Je mange sans horaires fixes.
Mots-clés :
absence horaires repas
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre alimentaire
Question suivante :
Pourquoi vos repas ne sont-ils pas réguliers ?

N095
Patient :
Je bois très peu d’eau chaque jour.
Mots-clés :
déshydratation alimentation
Risque :
Élevé 🟠
Symptômes détectés :
Risque de déshydratation
Question suivante :
Pourquoi ne buvez-vous pas assez d’eau ?

N096
Patient :
Je mange beaucoup de nourriture pauvre en nutriments.
Mots-clés :
alimentation pauvre
Risque :
Élevé 🟠
Symptômes détectés :
Carences multiples
Question suivante :
Avez-vous accès à des aliments riches ?

N097
Patient :
Je saute souvent le dîner.
Mots-clés :
saut dîner fréquent
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre énergétique
Question suivante :
Pourquoi sautez-vous ce repas ?

N098
Patient :
Je mange mais je perds du poids.
Mots-clés :
perte poids malgré alimentation
Risque :
Critique 🔴
Symptômes détectés :
Malabsorption ou maladie chronique possible
Question suivante :
Avez-vous des diarrhées ou douleurs digestives ?

N099
Patient :
Je n’ai pas une alimentation saine.
Mots-clés :
alimentation non saine
Risque :
Élevé 🟠
Symptômes détectés :
Déséquilibre nutritionnel global
Question suivante :
Que mangez-vous le plus souvent ?

N100
Patient :
Je mange très peu et je me sens toujours faible.
Mots-clés :
faible alimentation
Risque :
Critique 🔴
Symptômes détectés :
Malnutrition sévère
Question suivante :
Depuis quand cet état a-t-il commencé ?
🧠 SANTÉ MENTALE (M001 à M020)

M001
Patient :
Je me sens triste tout le temps.
Mots-clés :
tristesse permanente
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Depuis combien de temps ressentez-vous cette tristesse ?

M002
Patient :
Je n’ai plus envie de rien faire.
Mots-clés :
perte motivation
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Est-ce que cela affecte votre travail ou études ?

M003
Patient :
Je dors très mal la nuit.
Mots-clés :
insomnie
Risque :
Modéré 🟡
Symptômes détectés :
Trouble du sommeil lié au stress
Question suivante :
Depuis quand avez-vous ce problème de sommeil ?

M004
Patient :
Je pense trop et je n’arrive pas à me calmer.
Mots-clés :
pensées excessives
Risque :
Modéré 🟡
Symptômes détectés :
Anxiété possible
Question suivante :
Ces pensées sont-elles liées à un problème précis ?

M005
Patient :
Je me sens inutile.
Mots-clés :
sentiment inutilité
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Avez-vous perdu confiance en vous récemment ?

M006
Patient :
Je pleure souvent sans raison.
Mots-clés :
pleurs fréquents
Risque :
Élevé 🟠
Symptômes détectés :
Trouble émotionnel
Question suivante :
Depuis quand cela se produit-il ?

M007
Patient :
Je n’aime plus parler aux gens.
Mots-clés :
isolement social
Risque :
Élevé 🟠
Symptômes détectés :
Dépression ou anxiété sociale
Question suivante :
Évitez-vous tout le monde ou seulement certaines personnes ?

M008
Patient :
Je suis toujours stressé.
Mots-clés :
stress constant
Risque :
Modéré 🟡
Symptômes détectés :
Anxiété chronique
Question suivante :
Qu’est-ce qui provoque le plus votre stress ?

M009
Patient :
Je n’arrive pas à me concentrer.
Mots-clés :
manque concentration
Risque :
Modéré 🟡
Symptômes détectés :
Fatigue mentale ou stress
Question suivante :
Depuis quand avez-vous ce problème ?

M010
Patient :
Je me sens toujours fatigué mentalement.
Mots-clés :
fatigue mentale
Risque :
Élevé 🟠
Symptômes détectés :
Épuisement psychologique
Question suivante :
Dormez-vous suffisamment chaque nuit ?

M011
Patient :
J’ai peur sans raison.
Mots-clés :
peur inexpliquée
Risque :
Élevé 🟠
Symptômes détectés :
Trouble anxieux
Question suivante :
Quand ces peurs apparaissent-elles le plus ?

M012
Patient :
Je perds facilement patience.
Mots-clés :
irritabilité
Risque :
Modéré 🟡
Symptômes détectés :
Stress ou surcharge mentale
Question suivante :
Dans quelles situations cela arrive-t-il ?

M013
Patient :
Je n’ai plus d’espoir pour l’avenir.
Mots-clés :
désespoir
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Depuis quand ressentez-vous cela ?

M014
Patient :
Je pense que ma vie n’a pas de valeur.
Mots-clés :
perte valeur personnelle
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère / risque suicidaire
Question suivante :
Avez-vous déjà pensé à vous faire du mal ?

M015
Patient :
Je me sens seul même entouré.
Mots-clés :
solitude émotionnelle
Risque :
Élevé 🟠
Symptômes détectés :
Dépression ou isolement émotionnel
Question suivante :
Depuis quand ressentez-vous cette solitude ?

M016
Patient :
Je n’arrive pas à arrêter de penser au passé.
Mots-clés :
rumination passé
Risque :
Modéré 🟡
Symptômes détectés :
Stress post-traumatique possible
Question suivante :
Ces souvenirs sont-ils douloureux ?

M017
Patient :
Je fais souvent des cauchemars.
Mots-clés :
cauchemars fréquents
Risque :
Modéré 🟡
Symptômes détectés :
Anxiété ou stress
Question suivante :
Depuis quand avez-vous ces cauchemars ?

M018
Patient :
Je me sens vide intérieurement.
Mots-clés :
vide émotionnel
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Avez-vous encore du plaisir dans certaines activités ?

M019
Patient :
Je perds facilement le contrôle de mes émotions.
Mots-clés :
instabilité émotionnelle
Risque :
Modéré 🟡
Symptômes détectés :
Trouble émotionnel
Question suivante :
Cela arrive-t-il souvent ou rarement ?

M020
Patient :
Je ne parle à personne de ce que je ressens.
Mots-clés :
silence émotionnel
Risque :
Élevé 🟠
Symptômes détectés :
Isolement émotionnel
Question suivante :
Pourquoi gardez-vous tout pour vous ?
M021
Patient :
Je n’arrive plus à prendre de décisions simples.
Mots-clés :
indécision
Risque :
Modéré 🟡
Symptômes détectés :
Fatigue mentale / anxiété possible
Question suivante :
Depuis quand avez-vous ce problème ?

M022
Patient :
Je me sens toujours inquiet.
Mots-clés :
inquiétude constante
Risque :
Élevé 🟠
Symptômes détectés :
Anxiété généralisée
Question suivante :
Qu’est-ce qui vous inquiète le plus ?

M023
Patient :
Je n’arrive plus à dormir à cause de mes pensées.
Mots-clés :
insomnie pensées
Risque :
Élevé 🟠
Symptômes détectés :
Anxiété sévère
Question suivante :
Ces pensées concernent-elles un problème précis ?

M024
Patient :
Je me sens observé tout le temps.
Mots-clés :
sentiment persécution
Risque :
Critique 🔴
Symptômes détectés :
Trouble psychotique possible
Question suivante :
Depuis quand ressentez-vous cela ?

M025
Patient :
J’entends des voix que les autres n’entendent pas.
Mots-clés :
hallucinations auditives
Risque :
Critique 🔴
Symptômes détectés :
Trouble psychotique sévère
Question suivante :
Ces voix vous parlent-elles directement ?

M026
Patient :
Je perds souvent le contact avec la réalité.
Mots-clés :
perte réalité
Risque :
Critique 🔴
Symptômes détectés :
Trouble mental sévère
Question suivante :
Cela arrive-t-il souvent ou rarement ?

M027
Patient :
Je me sens agressif sans raison.
Mots-clés :
agressivité inexpliquée
Risque :
Élevé 🟠
Symptômes détectés :
Trouble du contrôle émotionnel
Question suivante :
Dans quelles situations cela arrive-t-il ?

M028
Patient :
Je n’ai plus envie de vivre.
Mots-clés :
idées suicidaires
Risque :
Critique 🔴
Symptômes détectés :
Risque suicidaire élevé
Question suivante :
Avez-vous pensé à comment vous feriez ?

M029
Patient :
Je me sens fatigué même sans effort.
Mots-clés :
fatigue mentale persistante
Risque :
Modéré 🟡
Symptômes détectés :
Épuisement psychologique
Question suivante :
Dormez-vous bien la nuit ?

M030
Patient :
Je n’ai plus d’intérêt pour mes activités.
Mots-clés :
perte intérêt
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Depuis quand avez-vous perdu cet intérêt ?

M031
Patient :
Je me sens constamment stressé au travail ou à l’école.
Mots-clés :
stress travail
Risque :
Élevé 🟠
Symptômes détectés :
Stress chronique
Question suivante :
Qu’est-ce qui vous stresse le plus ?

M032
Patient :
Je pleure facilement sans contrôle.
Mots-clés :
pleurs incontrôlés
Risque :
Élevé 🟠
Symptômes détectés :
Instabilité émotionnelle
Question suivante :
Depuis quand cela a-t-il commencé ?

M033
Patient :
Je ne fais confiance à personne.
Mots-clés :
méfiance excessive
Risque :
Modéré 🟡
Symptômes détectés :
Anxiété sociale ou traumatisme
Question suivante :
Avez-vous vécu une expérience difficile ?

M034
Patient :
Je me sens souvent confus.
Mots-clés :
confusion mentale
Risque :
Élevé 🟠
Symptômes détectés :
Fatigue mentale ou trouble neurologique
Question suivante :
Depuis quand ressentez-vous cette confusion ?

M035
Patient :
Je parle seul parfois.
Mots-clés :
parler seul
Risque :
Modéré 🟡
Symptômes détectés :
Stress ou isolement
Question suivante :
Est-ce volontaire ou involontaire ?

M036
Patient :
Je me sens inutile pour ma famille.
Mots-clés :
sentiment inutilité famille
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Qu’est-ce qui vous fait penser cela ?

M037
Patient :
Je perds souvent la mémoire.
Mots-clés :
troubles mémoire
Risque :
Élevé 🟠
Symptômes détectés :
Fatigue mentale ou trouble neurologique
Question suivante :
Depuis quand avez-vous ces oublis ?

M038
Patient :
Je me sens vide même avec ma famille.
Mots-clés :
vide émotionnel famille
Risque :
Élevé 🟠
Symptômes détectés :
Dépression émotionnelle
Question suivante :
Avez-vous encore du plaisir dans la vie ?

M039
Patient :
Je suis toujours fatigué mentalement.
Mots-clés :
épuisement mental
Risque :
Élevé 🟠
Symptômes détectés :
Burn-out possible
Question suivante :
Travaillez-vous beaucoup ou êtes-vous stressé ?

M040
Patient :
Je n’arrive plus à sourire.
Mots-clés :
absence joie
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Depuis quand avez-vous perdu cette joie ?
M041
Patient :
Je me sens souvent fatigué sans raison.
Mots-clés :
fatigue sans raison
Risque :
Élevé 🟠
Symptômes détectés :
Épuisement mental / dépression possible
Question suivante :
Dormez-vous suffisamment la nuit ?

M042
Patient :
Je n’ai plus envie de sortir de ma chambre.
Mots-clés :
isolement chambre
Risque :
Élevé 🟠
Symptômes détectés :
Dépression sévère possible
Question suivante :
Depuis quand vous isolez-vous ainsi ?

M043
Patient :
Je me sens souvent nerveux sans raison.
Mots-clés :
nervosité sans cause
Risque :
Modéré 🟡
Symptômes détectés :
Anxiété
Question suivante :
Dans quelles situations cela arrive-t-il ?

M044
Patient :
Je ne peux plus contrôler mes émotions.
Mots-clés :
perte contrôle émotions
Risque :
Élevé 🟠
Symptômes détectés :
Instabilité émotionnelle
Question suivante :
Cela arrive-t-il souvent ?

M045
Patient :
Je pense que tout est de ma faute.
Mots-clés :
culpabilité excessive
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Pourquoi pensez-vous cela ?

M046
Patient :
Je n’ai plus confiance en moi.
Mots-clés :
perte confiance
Risque :
Élevé 🟠
Symptômes détectés :
Dépression / anxiété
Question suivante :
Depuis quand ressentez-vous cela ?

M047
Patient :
Je me sens souvent perdu dans mes pensées.
Mots-clés :
confusion mentale
Risque :
Modéré 🟡
Symptômes détectés :
Stress ou surcharge mentale
Question suivante :
Avez-vous beaucoup de stress récemment ?

M048
Patient :
Je parle peu avec ma famille.
Mots-clés :
faible communication familiale
Risque :
Modéré 🟡
Symptômes détectés :
Isolement émotionnel
Question suivante :
Pourquoi communiquez-vous peu ?

M049
Patient :
Je me sens toujours inquiet pour l’avenir.
Mots-clés :
inquiétude avenir
Risque :
Élevé 🟠
Symptômes détectés :
Anxiété généralisée
Question suivante :
Qu’est-ce qui vous inquiète le plus ?

M050
Patient :
Je n’ai plus d’énergie pour travailler.
Mots-clés :
fatigue travail
Risque :
Élevé 🟠
Symptômes détectés :
Burn-out possible
Question suivante :
Travaillez-vous beaucoup en ce moment ?

M051
Patient :
Je me sens souvent en colère sans raison.
Mots-clés :
colère incontrôlée
Risque :
Élevé 🟠
Symptômes détectés :
Trouble émotionnel
Question suivante :
Qu’est-ce qui déclenche cette colère ?

M052
Patient :
Je n’ai plus de motivation pour étudier ou travailler.
Mots-clés :
perte motivation
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Depuis quand avez-vous perdu cette motivation ?

M053
Patient :
Je me sens souvent seul même avec des gens autour.
Mots-clés :
solitude sociale
Risque :
Élevé 🟠
Symptômes détectés :
Isolement émotionnel
Question suivante :
Vous sentez-vous compris par les autres ?

M054
Patient :
Je pense que personne ne m’aime.
Mots-clés :
sentiment rejet
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Avez-vous des personnes proches autour de vous ?

M055
Patient :
Je dors trop mais je suis toujours fatigué.
Mots-clés :
hypersomnie fatigue
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Depuis quand dormez-vous autant ?

M056
Patient :
Je n’ai plus de joie dans ma vie.
Mots-clés :
perte joie
Risque :
Élevé 🟠
Symptômes détectés :
Dépression
Question suivante :
Qu’est-ce qui vous rendait heureux avant ?

M057
Patient :
Je me sens souvent vidé émotionnellement.
Mots-clés :
vide émotionnel
Risque :
Élevé 🟠
Symptômes détectés :
Épuisement psychologique
Question suivante :
Avez-vous vécu un choc récent ?

M058
Patient :
Je n’arrive plus à réfléchir correctement.
Mots-clés :
difficulté réflexion
Risque :
Élevé 🟠
Symptômes détectés :
Fatigue mentale
Question suivante :
Depuis quand avez-vous ces difficultés ?

M059
Patient :
Je me sens inutile au monde.
Mots-clés :
sentiment inutilité
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Qu’est-ce qui vous fait ressentir cela ?

M060
Patient :
Je pense que rien ne peut s’améliorer.
Mots-clés :
désespoir total
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère / risque suicidaire
Question suivante :
Avez-vous quelqu’un à qui parler en ce moment ?
M061
Patient :
Je me réveille souvent sans énergie.
Mots-clés :
fatigue au réveil
Risque :
Élevé 🟠
Symptômes détectés :
Dépression ou trouble du sommeil
Question suivante :
À quelle heure vous couchez-vous généralement ?

M062
Patient :
Je pense trop à mes problèmes.
Mots-clés :
rumination mentale
Risque :
Élevé 🟠
Symptômes détectés :
Anxiété / stress chronique
Question suivante :
Ces pensées concernent quel type de problèmes ?

M063
Patient :
Je n’ai plus d’envie même pour manger.
Mots-clés :
perte envie manger
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Depuis quand avez-vous perdu cet appétit ?

M064
Patient :
Je me sens souvent sous pression.
Mots-clés :
pression mentale
Risque :
Modéré 🟡
Symptômes détectés :
Stress élevé
Question suivante :
Qu’est-ce qui vous met le plus sous pression ?

M065
Patient :
Je parle rarement avec les autres.
Mots-clés :
isolement social
Risque :
Élevé 🟠
Symptômes détectés :
Retrait social
Question suivante :
Depuis quand vous isolez-vous ?

M066
Patient :
Je me sens souvent vide dans ma tête.
Mots-clés :
vide mental
Risque :
Élevé 🟠
Symptômes détectés :
Épuisement psychologique
Question suivante :
Cela arrive-t-il toute la journée ou par moments ?

M067
Patient :
Je n’arrive plus à faire confiance à personne.
Mots-clés :
perte confiance autres
Risque :
Modéré 🟡
Symptômes détectés :
Traumatisme ou anxiété
Question suivante :
Avez-vous vécu une déception importante ?

M068
Patient :
Je me sens toujours inquiet sans raison.
Mots-clés :
inquiétude constante
Risque :
Élevé 🟠
Symptômes détectés :
Anxiété généralisée
Question suivante :
Depuis quand ressentez-vous cette inquiétude ?

M069
Patient :
Je me sens souvent agressif.
Mots-clés :
agressivité fréquente
Risque :
Élevé 🟠
Symptômes détectés :
Trouble émotionnel
Question suivante :
Dans quelles situations cela arrive-t-il ?

M070
Patient :
Je ne trouve plus de sens à ma vie.
Mots-clés :
perte sens vie
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Qu’est-ce qui vous faisait du sens auparavant ?

M071
Patient :
Je me sens souvent fatigué mentalement.
Mots-clés :
fatigue mentale
Risque :
Élevé 🟠
Symptômes détectés :
Burn-out possible
Question suivante :
Travaillez-vous ou étudiez-vous beaucoup ?

M072
Patient :
Je n’ai plus envie de voir mes amis.
Mots-clés :
retrait social amis
Risque :
Élevé 🟠
Symptômes détectés :
Isolement social
Question suivante :
Depuis quand évitez-vous vos amis ?

M073
Patient :
Je me sens constamment fatigué même sans activité.
Mots-clés :
fatigue permanente
Risque :
Élevé 🟠
Symptômes détectés :
Dépression ou trouble du sommeil
Question suivante :
Dormez-vous correctement ?

M074
Patient :
Je pleure souvent la nuit.
Mots-clés :
pleurs nocturnes
Risque :
Élevé 🟠
Symptômes détectés :
Trouble émotionnel
Question suivante :
Depuis quand cela se produit-il ?

M075
Patient :
Je me sens inutile pour ma famille.
Mots-clés :
sentiment inutilité famille
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Qu’est-ce qui vous fait penser cela ?

M076
Patient :
Je perds souvent le contrôle de mes pensées.
Mots-clés :
pensées incontrôlées
Risque :
Élevé 🟠
Symptômes détectés :
Anxiété sévère
Question suivante :
Ces pensées sont-elles négatives ou positives ?

M077
Patient :
Je me sens vide même entouré de gens.
Mots-clés :
vide social
Risque :
Élevé 🟠
Symptômes détectés :
Dépression émotionnelle
Question suivante :
Vous sentez-vous compris par les autres ?

M078
Patient :
Je n’ai plus d’énergie pour rien.
Mots-clés :
absence énergie totale
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère / burn-out
Question suivante :
Depuis quand êtes-vous dans cet état ?

M079
Patient :
Je me sens souvent perdu dans la vie.
Mots-clés :
perte repères
Risque :
Élevé 🟠
Symptômes détectés :
Crise existentielle
Question suivante :
Qu’est-ce qui vous faisait avancer avant ?

M080
Patient :
Je n’ai plus envie de continuer mes activités.
Mots-clés :
abandon activités
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Depuis quand avez-vous arrêté vos activités ?
M081
Patient :
Je me sens souvent perdu dans mes pensées.
Mots-clés :
perte concentration mentale
Risque :
Modéré 🟡
Symptômes détectés :
Fatigue mentale / stress
Question suivante :
Avez-vous beaucoup de préoccupations en ce moment ?

M082
Patient :
Je n’ai plus envie de parler à personne.
Mots-clés :
retrait communication
Risque :
Élevé 🟠
Symptômes détectés :
Isolement social
Question suivante :
Depuis quand évitez-vous les conversations ?

M083
Patient :
Je me sens souvent inutile.
Mots-clés :
sentiment inutilité
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Qu’est-ce qui vous fait ressentir cela ?

M084
Patient :
Je pense que ma vie n’a plus de sens.
Mots-clés :
perte sens vie
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère / risque suicidaire
Question suivante :
Avez-vous quelqu’un à qui parler actuellement ?

M085
Patient :
Je me sens très fatigué mentalement et physiquement.
Mots-clés :
fatigue globale
Risque :
Élevé 🟠
Symptômes détectés :
Burn-out possible
Question suivante :
Dormez-vous suffisamment ?

M086
Patient :
Je n’arrive plus à prendre de décisions.
Mots-clés :
indécision sévère
Risque :
Modéré 🟡
Symptômes détectés :
Stress ou anxiété
Question suivante :
Depuis quand avez-vous ce problème ?

M087
Patient :
Je me sens souvent agressif sans raison.
Mots-clés :
agressivité sans cause
Risque :
Élevé 🟠
Symptômes détectés :
Instabilité émotionnelle
Question suivante :
Dans quelles situations cela arrive-t-il ?

M088
Patient :
Je n’ai plus de motivation pour vivre normalement.
Mots-clés :
perte motivation vie
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Depuis quand ressentez-vous cela ?

M089
Patient :
Je me sens toujours stressé même sans raison.
Mots-clés :
stress constant
Risque :
Élevé 🟠
Symptômes détectés :
Anxiété généralisée
Question suivante :
Qu’est-ce qui déclenche ce stress ?

M090
Patient :
Je n’arrive plus à me souvenir des choses.
Mots-clés :
troubles mémoire
Risque :
Élevé 🟠
Symptômes détectés :
Fatigue mentale
Question suivante :
Depuis quand avez-vous ces oublis ?

M091
Patient :
Je me sens vide et sans émotions.
Mots-clés :
vide émotionnel
Risque :
Élevé 🟠
Symptômes détectés :
Dépression possible
Question suivante :
Avez-vous encore du plaisir dans certaines activités ?

M092
Patient :
Je me sens rejeté par tout le monde.
Mots-clés :
sentiment rejet
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Avez-vous des proches autour de vous ?

M093
Patient :
Je n’arrive plus à me concentrer sur rien.
Mots-clés :
perte concentration
Risque :
Élevé 🟠
Symptômes détectés :
Stress ou fatigue mentale
Question suivante :
Depuis quand cela a commencé ?

M094
Patient :
Je pense souvent au passé douloureux.
Mots-clés :
rumination passé
Risque :
Élevé 🟠
Symptômes détectés :
Traumatisme psychologique possible
Question suivante :
Ces souvenirs vous perturbent-ils fortement ?

M095
Patient :
Je ne me reconnais plus moi-même.
Mots-clés :
perte identité
Risque :
Élevé 🟠
Symptômes détectés :
Crise psychologique
Question suivante :
Depuis quand ressentez-vous ce changement ?

M096
Patient :
Je me sens constamment épuisé émotionnellement.
Mots-clés :
épuisement émotionnel
Risque :
Élevé 🟠
Symptômes détectés :
Burn-out émotionnel
Question suivante :
Avez-vous beaucoup de stress quotidien ?

M097
Patient :
Je n’ai plus envie de me lever le matin.
Mots-clés :
désir rester au lit
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Depuis quand avez-vous ce sentiment ?

M098
Patient :
Je me sens souvent inutile et sans valeur.
Mots-clés :
sentiment inutilité
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère
Question suivante :
Qu’est-ce qui vous fait penser cela ?

M099
Patient :
Je pense que tout est fini pour moi.
Mots-clés :
désespoir total
Risque :
Critique 🔴
Symptômes détectés :
Risque suicidaire élevé
Question suivante :
Avez-vous quelqu’un de confiance à qui parler ?

M100
Patient :
Je ne vois plus d’avenir pour moi.
Mots-clés :
absence avenir
Risque :
Critique 🔴
Symptômes détectés :
Dépression sévère / risque suicidaire
Question suivante :
Souhaitez-vous parler à un professionnel de santé ?























🌍 QUESTIONS GÉNÉRALES (Q001 à Q020)

Q001
Patient :
Quel est votre nom ?
Mots-clés :
identité
Objectif :
Identifier le patient
Question suivante :
Quel est votre âge ?

Q002
Patient :
Quel est votre âge ?
Mots-clés :
âge
Objectif :
Adapter le niveau de risque
Question suivante :
Êtes-vous un homme ou une femme ?

Q003
Patient :
Êtes-vous un homme ou une femme ?
Mots-clés :
sexe
Objectif :
Analyse médicale adaptée
Question suivante :
Dans quelle localité vivez-vous ?

Q004
Patient :
Où habitez-vous ?
Mots-clés :
localisation
Objectif :
Orientation sanitaire
Question suivante :
Êtes-vous seul ou en famille ?

Q005
Patient :
Êtes-vous seul ou en famille ?
Mots-clés :
soutien social
Objectif :
Évaluer soutien disponible
Question suivante :
Avez-vous quelqu’un pour vous aider ?

Q006
Patient :
Avez-vous quelqu’un pour vous aider ?
Mots-clés :
assistance
Objectif :
Réseau de soutien
Question suivante :
Depuis quand avez-vous ces symptômes ?

Q007
Patient :
Depuis quand avez-vous ces symptômes ?
Mots-clés :
durée symptômes
Objectif :
Gravité du cas
Question suivante :
Les symptômes sont-ils apparus soudainement ou progressivement ?

Q008
Patient :
Les symptômes sont-ils soudains ou progressifs ?
Mots-clés :
apparition symptômes
Objectif :
Type d’urgence
Question suivante :
Avez-vous déjà consulté un centre de santé ?

Q009
Patient :
Avez-vous déjà consulté un centre de santé ?
Mots-clés :
consultation
Objectif :
Historique médical
Question suivante :
Prenez-vous déjà des médicaments ?

Q010
Patient :
Prenez-vous des médicaments ?
Mots-clés :
traitement
Objectif :
Interactions médicales
Question suivante :
Si oui, lesquels ?

Q011
Patient :
Quels médicaments prenez-vous ?
Mots-clés :
type médicaments
Objectif :
Analyse traitement
Question suivante :
Avez-vous des allergies connues ?

Q012
Patient :
Avez-vous des allergies ?
Mots-clés :
allergies
Objectif :
Sécurité médicale
Question suivante :
Avez-vous déjà été hospitalisé ?

Q013
Patient :
Avez-vous déjà été hospitalisé ?
Mots-clés :
hospitalisation
Objectif :
Historique grave
Question suivante :
Si oui, pour quelle raison ?

Q014
Patient :
Quelle est la raison de votre hospitalisation passée ?
Mots-clés :
cause hospitalisation
Objectif :
Analyse antécédents
Question suivante :
Avez-vous des maladies chroniques ?

Q015
Patient :
Avez-vous des maladies chroniques ?
Mots-clés :
maladie chronique
Objectif :
Facteurs de risque
Question suivante :
Si oui, lesquelles ?

Q016
Patient :
Quelles maladies chroniques avez-vous ?
Mots-clés :
type maladie chronique
Objectif :
Profil médical
Question suivante :
Votre état s’est-il aggravé récemment ?

Q017
Patient :
Votre état s’est-il aggravé ?
Mots-clés :
aggravation
Objectif :
Évolution maladie
Question suivante :
Avez-vous de la fièvre actuellement ?

Q018
Patient :
Avez-vous de la fièvre ?
Mots-clés :
fièvre
Objectif :
Symptôme clé
Question suivante :
Avez-vous des douleurs ?

Q019
Patient :
Avez-vous des douleurs ?
Mots-clés :
douleur
Objectif :
Localisation problème
Question suivante :
Où ressentez-vous la douleur ?

Q020
Patient :
Où ressentez-vous la douleur ?
Mots-clés :
localisation douleur
Objectif :
Diagnostic précis
Question suivante :
Décrivez la douleur (forte, légère, continue, etc.)
Q021
Patient :
Comment décririez-vous la douleur ?
Mots-clés :
type douleur
Objectif :
Qualifier le symptôme
Question suivante :
La douleur est-elle continue ou par crises ?

Q022
Patient :
La douleur est-elle continue ou par crises ?
Mots-clés :
rythme douleur
Objectif :
Évolution du symptôme
Question suivante :
Quelle est l’intensité de la douleur (faible, moyenne, forte) ?

Q023
Patient :
Quelle est l’intensité de la douleur ?
Mots-clés :
intensité douleur
Objectif :
Évaluer gravité
Question suivante :
La douleur augmente-t-elle avec le mouvement ?

Q024
Patient :
La douleur augmente-t-elle avec le mouvement ?
Mots-clés :
douleur mouvement
Objectif :
Orientation diagnostic
Question suivante :
Avez-vous de la fièvre en même temps ?

Q025
Patient :
Avez-vous de la fièvre en même temps ?
Mots-clés :
fièvre associée
Objectif :
Infection possible
Question suivante :
Avez-vous des frissons ?

Q026
Patient :
Avez-vous des frissons ?
Mots-clés :
frissons
Objectif :
Symptôme infectieux
Question suivante :
Avez-vous des nausées ou vomissements ?

Q027
Patient :
Avez-vous des nausées ou vomissements ?
Mots-clés :
nausées vomissements
Objectif :
Trouble digestif ou infection
Question suivante :
Depuis quand cela a commencé ?

Q028
Patient :
Depuis quand cela a commencé ?
Mots-clés :
durée symptômes
Objectif :
Gravité temporelle
Question suivante :
Les symptômes s’aggravent-ils ?

Q029
Patient :
Les symptômes s’aggravent-ils ?
Mots-clés :
aggravation
Objectif :
Évolution maladie
Question suivante :
Avez-vous déjà eu ce problème avant ?

Q030
Patient :
Avez-vous déjà eu ce problème avant ?
Mots-clés :
antécédent symptôme
Objectif :
Récurrence
Question suivante :
Avez-vous pris un traitement ?

Q031
Patient :
Avez-vous pris un traitement ?
Mots-clés :
traitement pris
Objectif :
Historique médical
Question suivante :
Ce traitement a-t-il aidé ?

Q032
Patient :
Le traitement a-t-il aidé ?
Mots-clés :
efficacité traitement
Objectif :
Réponse au traitement
Question suivante :
Avez-vous des allergies médicamenteuses ?

Q033
Patient :
Avez-vous des allergies aux médicaments ?
Mots-clés :
allergie médicaments
Objectif :
Sécurité
Question suivante :
Avez-vous des maladies connues ?

Q034
Patient :
Avez-vous des maladies connues ?
Mots-clés :
maladies connues
Objectif :
Profil médical
Question suivante :
Lesquelles ?

Q035
Patient :
Quelles maladies avez-vous ?
Mots-clés :
type maladie
Objectif :
Détail médical
Question suivante :
Êtes-vous sous suivi médical ?

Q036
Patient :
Êtes-vous suivi par un médecin ?
Mots-clés :
suivi médical
Objectif :
Encadrement santé
Question suivante :
À quelle fréquence consultez-vous ?

Q037
Patient :
À quelle fréquence consultez-vous un centre de santé ?
Mots-clés :
consultation fréquence
Objectif :
Accès aux soins
Question suivante :
Avez-vous accès facilement à un hôpital ?

Q038
Patient :
Avez-vous accès à un hôpital ?
Mots-clés :
accès soins
Objectif :
Accessibilité santé
Question suivante :
Y a-t-il des médicaments disponibles près de chez vous ?

Q039
Patient :
Avez-vous des médicaments disponibles près de vous ?
Mots-clés :
disponibilité médicaments
Objectif :
Ressources locales
Question suivante :
Pouvez-vous payer les soins médicaux ?

Q040
Patient :
Pouvez-vous payer les soins médicaux ?
Mots-clés :
capacité paiement
Objectif :
Accès économique santé
Question suivante :
Avez-vous déjà évité un soin par manque d’argent ?
Q041
Patient :
Avez-vous déjà été hospitalisé récemment ?
Mots-clés :
hospitalisation récente
Objectif :
Historique médical récent
Question suivante :
Si oui, pour quelle raison ?

Q042
Patient :
Pour quelle raison avez-vous été hospitalisé ?
Mots-clés :
cause hospitalisation
Objectif :
Comprendre antécédents
Question suivante :
Avez-vous suivi correctement le traitement prescrit ?

Q043
Patient :
Avez-vous suivi votre traitement correctement ?
Mots-clés :
observance traitement
Objectif :
Efficacité du traitement
Question suivante :
Avez-vous ressenti une amélioration ?

Q044
Patient :
Avez-vous ressenti une amélioration ?
Mots-clés :
amélioration état
Objectif :
Réponse au traitement
Question suivante :
Avez-vous arrêté le traitement ?

Q045
Patient :
Avez-vous arrêté votre traitement ?
Mots-clés :
arrêt traitement
Objectif :
Risque de rechute
Question suivante :
Pourquoi avez-vous arrêté ?

Q046
Patient :
Pourquoi avez-vous arrêté le traitement ?
Mots-clés :
raison arrêt
Objectif :
Barrières aux soins
Question suivante :
Avez-vous accès régulièrement aux médicaments ?

Q047
Patient :
Avez-vous accès aux médicaments ?
Mots-clés :
accès médicaments
Objectif :
Disponibilité soins
Question suivante :
Pouvez-vous vous déplacer facilement ?

Q048
Patient :
Pouvez-vous vous déplacer facilement ?
Mots-clés :
mobilité patient
Objectif :
Accès aux soins
Question suivante :
Avez-vous quelqu’un pour vous accompagner ?

Q049
Patient :
Avez-vous quelqu’un pour vous accompagner ?
Mots-clés :
accompagnement
Objectif :
Soutien social
Question suivante :
Votre famille est-elle au courant de votre état ?

Q050
Patient :
Votre famille est-elle au courant de votre état ?
Mots-clés :
famille informée
Objectif :
Soutien familial
Question suivante :
Vous soutiennent-ils dans vos soins ?

Q051
Patient :
Votre famille vous soutient-elle ?
Mots-clés :
soutien familial
Objectif :
Ressources sociales
Question suivante :
Avez-vous des difficultés financières ?

Q052
Patient :
Avez-vous des difficultés financières ?
Mots-clés :
problèmes financiers
Objectif :
Accès aux soins
Question suivante :
Cela empêche-t-il vos soins ?

Q053
Patient :
Cela empêche-t-il vos soins ?
Mots-clés :
barrière financière santé
Objectif :
Priorité santé
Question suivante :
Avez-vous déjà évité un traitement pour cette raison ?

Q054
Patient :
Avez-vous déjà évité un traitement ?
Mots-clés :
renoncement soins
Objectif :
Risque santé
Question suivante :
Quels soins avez-vous évités ?

Q055
Patient :
Quels soins avez-vous évités ?
Mots-clés :
type soins manqués
Objectif :
Analyse accès santé
Question suivante :
Avez-vous une assurance santé ?

Q056
Patient :
Avez-vous une assurance santé ?
Mots-clés :
assurance santé
Objectif :
Protection médicale
Question suivante :
Depuis combien de temps êtes-vous malade ?

Q057
Patient :
Depuis combien de temps êtes-vous malade ?
Mots-clés :
durée maladie
Objectif :
Chronologie maladie
Question suivante :
Les symptômes sont-ils constants ou variables ?

Q058
Patient :
Les symptômes sont-ils constants ou variables ?
Mots-clés :
évolution symptômes
Objectif :
Analyse évolution
Question suivante :
Quel symptôme vous gêne le plus ?

Q059
Patient :
Quel symptôme vous gêne le plus ?
Mots-clés :
symptôme principal
Objectif :
Priorité clinique
Question suivante :
Ce symptôme s’aggrave-t-il ?

Q060
Patient :
Ce symptôme s’aggrave-t-il ?
Mots-clés :
aggravation principal
Objectif :
Urgence décision
Question suivante :
Avez-vous besoin d’aide immédiate ?
Q061
Patient :
Avez-vous déjà ressenti ces symptômes auparavant ?
Mots-clés :
antécédent symptômes
Objectif :
Récurrence
Question suivante :
Si oui, quand cela s’est-il produit ?

Q062
Patient :
Quand ces symptômes sont-ils apparus pour la première fois ?
Mots-clés :
début symptômes
Objectif :
Chronologie
Question suivante :
Depuis ce moment, sont-ils devenus plus forts ?

Q063
Patient :
Les symptômes sont-ils devenus plus forts ?
Mots-clés :
aggravation
Objectif :
Évolution
Question suivante :
Avez-vous consulté quelqu’un depuis ?

Q064
Patient :
Avez-vous consulté quelqu’un ?
Mots-clés :
consultation
Objectif :
Historique soins
Question suivante :
Quel diagnostic vous a-t-on donné ?

Q065
Patient :
Quel diagnostic vous a-t-on donné ?
Mots-clés :
diagnostic médical
Objectif :
Compréhension médicale
Question suivante :
Avez-vous suivi le traitement recommandé ?

Q066
Patient :
Avez-vous suivi le traitement recommandé ?
Mots-clés :
traitement suivi
Objectif :
Efficacité soins
Question suivante :
Ce traitement a-t-il aidé ?

Q067
Patient :
Ce traitement a-t-il aidé ?
Mots-clés :
résultat traitement
Objectif :
Réponse thérapeutique
Question suivante :
Avez-vous arrêté ce traitement ?

Q068
Patient :
Avez-vous arrêté le traitement ?
Mots-clés :
arrêt traitement
Objectif :
Risque rechute
Question suivante :
Pourquoi l’avez-vous arrêté ?

Q069
Patient :
Pourquoi avez-vous arrêté le traitement ?
Mots-clés :
raison arrêt
Objectif :
Barrières santé
Question suivante :
Avez-vous accès facilement aux soins ?

Q070
Patient :
Avez-vous accès facilement aux soins ?
Mots-clés :
accès santé
Objectif :
Accessibilité
Question suivante :
Combien de temps faut-il pour aller au centre de santé ?

Q071
Patient :
Combien de temps faut-il pour aller au centre de santé ?
Mots-clés :
distance soins
Objectif :
Accessibilité géographique
Question suivante :
Avez-vous des moyens de transport ?

Q072
Patient :
Avez-vous des moyens de transport ?
Mots-clés :
transport
Objectif :
Accès soins
Question suivante :
Avez-vous déjà renoncé à consulter ?

Q073
Patient :
Avez-vous déjà renoncé à consulter ?
Mots-clés :
renoncement soins
Objectif :
Risque santé
Question suivante :
Pour quelle raison ?

Q074
Patient :
Pour quelle raison avez-vous renoncé ?
Mots-clés :
cause renoncement
Objectif :
Barrières soins
Question suivante :
Avez-vous de la douleur actuellement ?

Q075
Patient :
Avez-vous de la douleur actuellement ?
Mots-clés :
douleur actuelle
Objectif :
Symptôme actif
Question suivante :
Où ressentez-vous cette douleur ?

Q076
Patient :
Où ressentez-vous la douleur ?
Mots-clés :
localisation douleur
Objectif :
Diagnostic
Question suivante :
Cette douleur est-elle forte ou faible ?

Q077
Patient :
La douleur est-elle forte ou faible ?
Mots-clés :
intensité douleur
Objectif :
Gravité
Question suivante :
La douleur augmente-t-elle ?

Q078
Patient :
La douleur augmente-t-elle ?
Mots-clés :
aggravation douleur
Objectif :
Évolution
Question suivante :
Avez-vous de la fièvre ?

Q079
Patient :
Avez-vous de la fièvre ?
Mots-clés :
fièvre
Objectif :
Symptôme clé
Question suivante :
Avez-vous des frissons ou sueurs ?

Q080
Patient :
Avez-vous des frissons ou sueurs ?
Mots-clés :
frissons sueurs
Objectif :
Infection possible
Question suivante :
Depuis quand ces symptômes sont-ils présents ?
Q081
Patient :
Depuis quand avez-vous ces symptômes ?
Mots-clés :
durée symptômes
Objectif :
Chronologie
Question suivante :
Les symptômes sont-ils constants ou intermittents ?

Q082
Patient :
Les symptômes sont-ils constants ou intermittents ?
Mots-clés :
type évolution
Objectif :
Nature du problème
Question suivante :
Avez-vous remarqué un déclencheur ?

Q083
Patient :
Avez-vous remarqué un déclencheur ?
Mots-clés :
déclencheur
Objectif :
Cause possible
Question suivante :
Les symptômes apparaissent-ils après une activité précise ?

Q084
Patient :
Les symptômes apparaissent-ils après une activité précise ?
Mots-clés :
activité déclenchement
Objectif :
Analyse comportementale
Question suivante :
Avez-vous changé votre alimentation récemment ?

Q085
Patient :
Avez-vous changé votre alimentation récemment ?
Mots-clés :
changement alimentation
Objectif :
Facteurs nutritionnels
Question suivante :
Buvez-vous suffisamment d’eau chaque jour ?

Q086
Patient :
Buvez-vous suffisamment d’eau chaque jour ?
Mots-clés :
hydratation
Objectif :
État général
Question suivante :
Dormez-vous bien la nuit ?

Q087
Patient :
Dormez-vous bien la nuit ?
Mots-clés :
sommeil
Objectif :
Fatigue / santé mentale
Question suivante :
Combien d’heures dormez-vous par nuit ?

Q088
Patient :
Combien d’heures dormez-vous par nuit ?
Mots-clés :
durée sommeil
Objectif :
Qualité sommeil
Question suivante :
Vous sentez-vous reposé au réveil ?

Q089
Patient :
Vous sentez-vous reposé au réveil ?
Mots-clés :
fatigue matin
Objectif :
Épuisement
Question suivante :
Avez-vous du stress en ce moment ?

Q090
Patient :
Avez-vous du stress en ce moment ?
Mots-clés :
stress
Objectif :
Santé mentale globale
Question suivante :
Qu’est-ce qui vous cause le plus de stress ?

Q091
Patient :
Qu’est-ce qui vous cause le plus de stress ?
Mots-clés :
cause stress
Objectif :
Analyse environnement
Question suivante :
Avez-vous du soutien autour de vous ?

Q092
Patient :
Avez-vous du soutien autour de vous ?
Mots-clés :
soutien social
Objectif :
Réseau social
Question suivante :
Qui vous aide le plus ?

Q093
Patient :
Qui vous aide le plus ?
Mots-clés :
personne soutien
Objectif :
Ressources humaines
Question suivante :
Avez-vous accès à un centre de santé proche ?

Q094
Patient :
Avez-vous accès à un centre de santé proche ?
Mots-clés :
accès santé
Objectif :
Accessibilité
Question suivante :
Combien de temps faut-il pour y aller ?

Q095
Patient :
Combien de temps faut-il pour aller au centre de santé ?
Mots-clés :
distance soins
Objectif :
Accessibilité géographique
Question suivante :
Avez-vous déjà consulté un médecin pour ce problème ?

Q096
Patient :
Avez-vous déjà consulté un médecin ?
Mots-clés :
consultation
Objectif :
Historique médical
Question suivante :
Quel diagnostic vous a-t-on donné ?

Q097
Patient :
Quel diagnostic vous a-t-on donné ?
Mots-clés :
diagnostic
Objectif :
Compréhension maladie
Question suivante :
Avez-vous suivi le traitement ?

Q098
Patient :
Avez-vous suivi le traitement ?
Mots-clés :
traitement
Objectif :
Suivi médical
Question suivante :
Avez-vous arrêté le traitement ?

Q099
Patient :
Avez-vous arrêté le traitement ?
Mots-clés :
arrêt traitement
Objectif :
Risque rechute
Question suivante :
Pourquoi avez-vous arrêté ?

Q100
Patient :
Pourquoi avez-vous arrêté le traitement ?
Mots-clés :
raison arrêt
Objectif :
Barrière soins
Question suivante :
Merci. Souhaitez-vous une orientation médicale maintenant ?






# =============================
# =============================
Merci, alors je veux que tu rendes l'assistant conversationnelle entre patient et bot. donc avant de donnees conseil aupatient l'assistant IA doit d'abord comprendre et recevoir le donnees du patient a partir de ce que le patient dit: pour tout les symptomes ces genres de questions SYMPTÔMES ASSOCIÉS :**
* Avez-vous de la fièvre ?
* Avez-vous des crachats (avec ou sans sang) ?
* Avez-vous des douleurs thoraciques ?, le patient doit d'abord repondre a ces question de lui donner conseil et apres ces reponses avant de donner conseil tu dois lui demander sa residence et apres on lui donne maintenent des conseils. sa residence doit lui permettre de localiser le centre de sante ou hopital et pharmacie pret de lui par exemple: je reside a kakungwe, le bot doit repondre je comprend alors comme tu reside a kakungwe tu peux parcourir l'hopital general de refence d'uvira dans l'avenue Shishi 1 sur RN5 en haut ou contancter +243970096597 tu vas citez d'abord au moins 5 quartiers d'Uvira le plus connu et les centre de sante ou hopital connu u dois utiliser le meme dnumero de telephone d'abord. La nous sommes toujours dans insert_data.py