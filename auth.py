# auth.py
"""
Gestion de l'authentification et des sessions utilisateur pour UviraTalk.
Utilise hashlib (stdlib) pour hasher les mots de passe — pas de dépendance externe.
"""

import hashlib
import os
import secrets
from datetime import datetime, timezone


# =============================================
# HASH DE MOT DE PASSE (sans dépendance externe)
# =============================================
def hash_password(password: str, salt: str = None) -> str:
    """Hash un mot de passe avec SHA-256 + salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100_000
    )
    return f"{salt}${h.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Vérifie un mot de passe contre un hash stocké."""
    try:
        salt, _ = stored_hash.split('$', 1)
    except ValueError:
        return False
    new_hash = hash_password(password, salt)
    return secrets.compare_digest(new_hash, stored_hash)


# =============================================
# VALIDATION
# =============================================
def validate_email(email: str) -> bool:
    import re
    if not email or len(email) > 120:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple:
    """Retourne (ok, message d'erreur)."""
    if not password or len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caracteres."
    if len(password) > 100:
        return False, "Mot de passe trop long (max 100 caracteres)."
    return True, ""


def validate_profile(prenom: str, post_nom: str, age, sexe: str, localisation: str) -> tuple:
    """Valide les informations du profil."""
    if not prenom or len(prenom.strip()) < 2:
        return False, "Le prenom est obligatoire (min 2 caracteres)."
    if not post_nom or len(post_nom.strip()) < 2:
        return False, "Le post-nom est obligatoire (min 2 caracteres)."
    try:
        age_int = int(age)
        if age_int < 1 or age_int > 120:
            return False, "L'age doit etre entre 1 et 120."
    except (ValueError, TypeError):
        return False, "L'age doit etre un nombre valide."
    if sexe not in ['Homme', 'Femme', 'Autre']:
        return False, "Le sexe doit etre Homme, Femme ou Autre."
    if not localisation or len(localisation.strip()) < 2:
        return False, "La localisation est obligatoire."
    return True, ""