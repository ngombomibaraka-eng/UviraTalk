# import_data.py
"""Import des données UviraTalk — version corrigée (gestion des \n internes)"""

import os
import re
import unicodedata
from docx import Document
from flask import Flask
from database import db, DialogueTriage, QAEducation


# =============================================
# CONFIGURATION
# =============================================
BASE_PATH = "DATABASE UviraTalk"
DB_PATH = "sqlite:///uviratalk.db"

FICHIERS_DIALOGUES = [
    ("Dialogue D.docx", "Diarrhée",      "fr/sw"),
    ("Dialogue E.docx", "Santé Enfant",  "fr/sw"),
    ("Dialogue G.docx", "Grossesse",     "fr/sw"),
    ("Dialogue M.docx", "Santé Mentale", "fr/sw"),
    ("Dialogue N.docx", "Nutrition",     "fr/sw"),
    ("Dialogue T.docx", "Tuberculose",   "fr/sw"),
    ("Dialogue U.docx", "Urgences",      "fr/sw"),
    ("Dialogue V.docx", "VIH-SIDA",      "fr/sw"),
    ("Dialogues.docx",  "Paludisme",     "fr/sw"),
]

FICHIER_QA = "Q et R.docx"


# =============================================
# MARQUEURS
# =============================================
PATIENT_MARKERS = [
    "patient", "patiente", "mgonjwa", "parent", "mzazi",
    "mwanamke", "mwanamke mjamzito", "mwanamke mijamzito",
    "mwanamke miamzito",
]
MOTS_CLES_MARKERS = [
    "mots-cles", "mots cles", "maneno muhimu", "maneno muhimo",
    "maneno mnamo muhimu",
]
SYMPTOMES_MARKERS = [
    "symptomes detectes", "symptome detecte", "symptomes",
    "dalili zilizotambulwa", "dalili zilizotambuwa",
    "dalili zilizogunduliwa", "dalili zilizotabulwa", "dalili",
]
QUESTION_MARKERS = [
    "question suivante", "question",
    "swali lifuatalo", "swali linalo", "swali linalofuata",
    "swali linalotarajiwa", "swali",
]
URGENCE_MARKERS = ["urgence", "risque", "dharura", "hatari"]
INTENTION_MARKERS = [
    "intention", "objectif", "situation", "information",
    "nia", "reponse attendue", "jibu linalotarajiwa",
]

CODE_PATTERN = re.compile(r'^([A-Z]\d{3})\s*$')
GARBAGE_PATTERN = re.compile(r'[¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿]{3,}')


# =============================================
# UTILITAIRES
# =============================================
def strip_accents(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def clean_text(text: str) -> str:
    if not text:
        return ""
    # Remplacer les sauts de ligne par un espace
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = GARBAGE_PATTERN.sub('', text)
    text = re.sub(r'^[•\-\*\u2022\u25cf\u25aa]\s*', '', text.strip())
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def is_garbage_line(line: str) -> bool:
    if not line or len(line.strip()) < 2:
        return True
    # Ne jamais rejeter un code
    if re.match(r'^[A-Z]\d{1,3}$', line.strip()):
        return False
    letters = sum(1 for c in line if c.isalpha() or c in " '-:,.")
    if len(line) > 0 and letters / len(line) < 0.4:
        return True
    return bool(GARBAGE_PATTERN.search(line))


def match_marker(line: str, markers: list) -> bool:
    if not line:
        return False
    # Si la ligne contient un ':', ne garder que la partie AVANT le ':'
    # pour éviter que "Patient : quelque chose" ne matche à tort
    cleaned = strip_accents(line.lower())
    cleaned = cleaned.replace(':', ' ').strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    for m in markers:
        mm = strip_accents(m.lower()).strip()
        mm = re.sub(r'\s+', ' ', mm)
        if cleaned == mm or cleaned.startswith(mm + ' '):
            return True
    return False


def flatten_paragraphs(paragraphs: list) -> list:
    """
    Aplatit les paragraphes Word :
    - Remplace les \n et \r par des vrais sauts de ligne
    - Chaque sous-ligne devient un élément séparé
    - Filtre les lignes vides
    """
    result = []
    for p in paragraphs:
        text = p.text if hasattr(p, 'text') else str(p)
        # Splitter sur tous types de sauts de ligne
        sub_lines = re.split(r'[\r\n]+', text)
        for sub in sub_lines:
            stripped = sub.strip()
            if stripped:  # Ignorer les vides
                result.append(stripped)
    return result


def split_by_language(lines: list) -> dict:
    sections = {'fr': [], 'sw': []}
    current_lang = 'fr'
    found_sw = False

    for line in lines:
        stripped = line.strip()
        if not found_sw and re.match(
            r'^\s*(?:Kiswahili|Swahili)\s*:?\s*(.*)$',
            stripped, re.IGNORECASE
        ):
            current_lang = 'sw'
            found_sw = True
            continue
        sections[current_lang].append(line)

    return sections


# =============================================
# PARSER DIALOGUES
# =============================================
def parse_dialogue_lines(lines: list, theme: str, langue: str) -> list:
    dialogues = []
    current = None
    section = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        # === 1. Détection du code (AVANT is_garbage_line) ===
        code_match = CODE_PATTERN.match(line)
        if code_match:
            if (current and current.get('phrase_patient')
                    and current.get('question_suivante')):
                dialogues.append(current)
            current = {
                'code': code_match.group(1),
                'theme': theme,
                'langue': langue,
                'phrase_patient': '',
                'mots_cles': [],
                'symptomes_detectes': [],
                'urgence': None,
                'intention': None,
                'question_suivante': '',
            }
            section = None
            continue

        # === 2. Filtre garbage ===
        if is_garbage_line(line):
            continue

        if current is None:
            continue

        # === 3. Marqueurs (ordre important) ===
        if match_marker(line, MOTS_CLES_MARKERS):
            section = 'mots_cles'
            after = line.split(':', 1)[1].strip() if ':' in line else ''
            if after:
                current['mots_cles'].append(clean_text(after))
            continue

        if match_marker(line, SYMPTOMES_MARKERS):
            section = 'symptomes'
            after = line.split(':', 1)[1].strip() if ':' in line else ''
            if after:
                current['symptomes_detectes'].append(clean_text(after))
            continue

        if match_marker(line, QUESTION_MARKERS):
            section = 'question'
            after = line.split(':', 1)[1].strip() if ':' in line else ''
            if after:
                current['question_suivante'] = clean_text(after)
            continue

        if match_marker(line, URGENCE_MARKERS):
            section = 'urgence'
            after = line.split(':', 1)[1].strip() if ':' in line else ''
            after = re.sub(r'^[•\-\*\u2022\u25cf]\s*', '', after)
            if after:
                current['urgence'] = clean_text(after)
            continue

        if match_marker(line, INTENTION_MARKERS):
            section = 'intention'
            after = line.split(':', 1)[1].strip() if ':' in line else ''
            if after:
                current['intention'] = clean_text(after)
            continue

        if match_marker(line, PATIENT_MARKERS):
            section = 'patient'
            after = line.split(':', 1)[1].strip() if ':' in line else ''
            if after:
                current['phrase_patient'] = clean_text(after)
            continue

        # === 4. Contenu ===
        content = clean_text(line)
        if not content:
            continue

        if section == 'patient':
            current['phrase_patient'] = (
                current['phrase_patient'] + ' ' + content
                if current['phrase_patient'] else content
            )
        elif section == 'mots_cles':
            current['mots_cles'].append(content)
        elif section == 'symptomes':
            current['symptomes_detectes'].append(content)
        elif section == 'question':
            current['question_suivante'] = (
                current['question_suivante'] + ' ' + content
                if current['question_suivante'] else content
            )
        elif section == 'urgence' and not current['urgence']:
            current['urgence'] = content
        elif section == 'intention' and not current['intention']:
            current['intention'] = content

    # Dernier élément
    if (current and current.get('phrase_patient')
            and current.get('question_suivante')):
        dialogues.append(current)

    # Joindre les listes
    for d in dialogues:
        d['mots_cles'] = '|'.join(d['mots_cles'])
        d['symptomes_detectes'] = '|'.join(d['symptomes_detectes'])

    return dialogues


# =============================================
# PARSER Q&R
# =============================================
def parse_qa_lines(lines: list, langue: str) -> list:
    qa_list = []
    current_theme = "Général"
    current = None
    section = None

    theme_pattern = re.compile(r'(?:Série|Sehemu|Serie)\s+\d+\s*:\s*(.+)', re.IGNORECASE)
    qa_code_pattern = re.compile(r'^Q(\d+)\s*$')

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        # === 1. Détection du code Q (AVANT tout) ===
        code_match = qa_code_pattern.match(line)
        if code_match:
            if current and current.get('question') and current.get('reponse'):
                qa_list.append(current)
            current = {
                'code': f"Q{code_match.group(1)}",
                'theme': current_theme,
                'langue': langue,
                'question': '',
                'reponse': '',
            }
            section = None
            continue

        if is_garbage_line(line):
            continue

        # === 2. Détection du thème ===
        theme_match = theme_pattern.match(line)
        if theme_match:
            current_theme = clean_text(theme_match.group(1))
            continue

        if current is None:
            continue

        # === 3. Détection Question / Réponse ===
        cleaned = strip_accents(line.lower()).replace(':', ' ').strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)

        # Question
        if cleaned.startswith('question ') or cleaned == 'question' \
                or cleaned.startswith('swali ') or cleaned == 'swali':
            section = 'question'
            after = line.split(':', 1)[1].strip() if ':' in line else ''
            if after:
                current['question'] = clean_text(after)
            continue

        # Réponse
        if cleaned.startswith('reponse ') or cleaned == 'reponse' \
                or cleaned.startswith('jibu ') or cleaned == 'jibu':
            section = 'reponse'
            after = line.split(':', 1)[1].strip() if ':' in line else ''
            if after:
                current['reponse'] = clean_text(after)
            continue

        # === 4. Contenu ===
        content = clean_text(line)
        if section == 'question' and content:
            current['question'] = (
                current['question'] + ' ' + content
                if current['question'] else content
            )
        elif section == 'reponse' and content:
            current['reponse'] = (
                current['reponse'] + ' ' + content
                if current['reponse'] else content
            )

    # Dernier
    if current and current.get('question') and current.get('reponse'):
        qa_list.append(current)

    return qa_list

# =============================================
# IMPORT
# =============================================
def importer_tout():
    print("\n" + "=" * 60)
    print("IMPORTATION DES DONNEES UVIRATALK")
    print("=" * 60)

    total_dialogues = 0
    total_qa = 0

    print("\nImportation des dialogues de triage...")

    for nom_fichier, theme, _ in FICHIERS_DIALOGUES:
        filepath = os.path.join(BASE_PATH, nom_fichier)
        if not os.path.exists(filepath):
            print(f"   [X] Introuvable : {filepath}")
            continue

        print(f"\n   -> {nom_fichier} [{theme}]")
        doc = Document(filepath)

        # === APLATIR LES PARAGRAPHES (gestion des \n internes) ===
        all_lines = flatten_paragraphs(doc.paragraphs)
        sections = split_by_language(all_lines)
        print(f"      Lignes FR : {len(sections['fr'])} | Lignes SW : {len(sections['sw'])}")

        for langue, lines in sections.items():
            if not lines:
                continue
            dialogues = parse_dialogue_lines(lines, theme, langue)
            added = 0
            for d in dialogues:
                exists = DialogueTriage.query.filter_by(
                    code=d['code'], langue=d['langue'], theme=d['theme']
                ).first()
                if not exists:
                    db.session.add(DialogueTriage(**d))
                    added += 1
            db.session.commit()
            total_dialogues += added
            print(f"      [OK] [{langue.upper()}] {added} dialogues importes")

    print("\nImportation des Q&R d'education...")
    qa_filepath = os.path.join(BASE_PATH, FICHIER_QA)

    if os.path.exists(qa_filepath):
        doc = Document(qa_filepath)
        all_lines = flatten_paragraphs(doc.paragraphs)
        sections = split_by_language(all_lines)
        print(f"   Lignes FR : {len(sections['fr'])} | Lignes SW : {len(sections['sw'])}")

        for langue, lines in sections.items():
            if not lines:
                continue
            qa_list = parse_qa_lines(lines, langue)
            added = 0
            for q in qa_list:
                exists = QAEducation.query.filter_by(
                    code=q['code'], langue=q['langue']
                ).first()
                if not exists:
                    db.session.add(QAEducation(**q))
                    added += 1
            db.session.commit()
            total_qa += added
            print(f"   [OK] [{langue.upper()}] {added} Q&R importees")

    print("\n" + "=" * 60)
    print("RESUME FINAL")
    print("=" * 60)
    print(f"   Dialogues en base : {DialogueTriage.query.count()}")
    print(f"   Q&R en base       : {QAEducation.query.count()}")

    rows = db.session.query(
        DialogueTriage.theme,
        DialogueTriage.langue,
        db.func.count(DialogueTriage.id)
    ).group_by(DialogueTriage.theme, DialogueTriage.langue).all()

    print("\n   Repartition par theme et langue :")
    for theme, langue, count in rows:
        print(f"      - {theme:20s} [{langue}] : {count}")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    

    with app.app_context():
        db.drop_all()
        db.create_all()
        importer_tout()