# app.py
"""
Interface Streamlit UviraTalk avec authentification et traçabilité.
100% Python — aucun HTML/CSS/JS.
"""

import os
import streamlit as st
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime, timezone

from database import (
    db, DialogueTriage, QAEducation,
    Utilisateur, Conversation, Message
)
from engine import SmartAIMatcher
from smalltalk import get_welcome_message, get_greeting_response
from advice_engine import get_advice, get_health_center_suggestion
from auth import (
    hash_password, verify_password,
    validate_email, validate_password, validate_profile
)
from admin import show_admin_dashboard

load_dotenv()

# =============================================
# CONFIGURATION
# =============================================
st.set_page_config(
    page_title="UviraTalk - Assistant Sante IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "sqlite:///uviratalk.db"


# =============================================
# CONTEXTE FLASK
# =============================================
@st.cache_resource
def get_flask_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crée les tables manquantes
    return app


flask_app = get_flask_app()


# =============================================
# MOTEUR IA
# =============================================
@st.cache_resource
def initialize_engine():
    with flask_app.app_context():
        count_d = DialogueTriage.query.count()
        count_q = QAEducation.query.count()
        if count_d == 0 and count_q == 0:
            return None, "Base de donnees vide. Lancez : python import_data.py"
        matcher = SmartAIMatcher()
        matcher.build_caches()
        return matcher, f"IA prete : {count_d} dialogues, {count_q} Q&R"


matcher, status_message = initialize_engine()


# =============================================
# SESSION STATE
# =============================================
if "user" not in st.session_state:
    st.session_state.user = None
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"


# =============================================
# FONCTIONS BDD
# =============================================
def get_user_by_email(email):
    with flask_app.app_context():
        return Utilisateur.query.filter_by(email=email.lower().strip()).first()


def create_user(email, password, prenom, post_nom, age, sexe, localisation):
    with flask_app.app_context():
        user = Utilisateur(
            email=email.lower().strip(),
            password_hash=hash_password(password),
            prenom=prenom.strip(),
            post_nom=post_nom.strip(),
            age=int(age),
            sexe=sexe,
            localisation=localisation.strip(),
            role='patient',
        )
        db.session.add(user)
        db.session.commit()
        return user.id


def update_last_login(user_id):
    with flask_app.app_context():
        user = Utilisateur.query.get(user_id)
        if user:
            user.derniere_connexion = datetime.now(timezone.utc)
            db.session.commit()


def start_new_conversation(user_id):
    with flask_app.app_context():
        conv = Conversation(user_id=user_id, nb_messages=0)
        db.session.add(conv)
        db.session.commit()
        return conv.id


def end_conversation(conv_id):
    with flask_app.app_context():
        conv = Conversation.query.get(conv_id)
        if conv:
            conv.date_fin = datetime.now(timezone.utc)
            db.session.commit()


def save_message(conv_id, role, contenu, theme=None, urgence=None,
                 methode=None, langue=None):
    with flask_app.app_context():
        msg = Message(
            conversation_id=conv_id,
            role=role,
            contenu=contenu,
            theme=theme,
            urgence=urgence,
            methode=methode,
            langue=langue,
        )
        db.session.add(msg)
        conv = Conversation.query.get(conv_id)
        if conv:
            conv.nb_messages = (conv.nb_messages or 0) + 1
        db.session.commit()


# =============================================
# PAGE : INSCRIPTION
# =============================================
def page_register():
    st.title("🏥 UviraTalk")
    st.subheader("Creer votre compte")
    st.caption(
        "Vos informations nous permettront de mieux adapter vos besoins "
        "et d'ameliorer notre service. Elles restent **confidentielles**."
    )

    with st.form("register_form"):
        st.markdown("### 🔐 Identifiants")
        email = st.text_input("Email", placeholder="exemple@mail.com")
        password = st.text_input("Mot de passe", type="password",
                                 help="Minimum 6 caracteres")
        password2 = st.text_input("Confirmer le mot de passe", type="password")

        st.markdown("### 👤 Profil")
        col1, col2 = st.columns(2)
        with col1:
            prenom = st.text_input("Prenom *", placeholder="Ex : Marie")
        with col2:
            post_nom = st.text_input("Post-nom *", placeholder="Ex : Kabila")

        col3, col4 = st.columns(2)
        with col3:
            age = st.number_input("Age *", min_value=1, max_value=120, value=25)
        with col4:
            sexe = st.selectbox("Sexe *", ["Homme", "Femme", "Autre"])

        localisation = st.text_input(
            "Localisation *",
            placeholder="Quartier ou village (Ex : Kalimabenge, Uvira)"
        )

        st.markdown(
            "🔒 *En vous inscrivant, vous acceptez que vos donnees soient utilisees "
            "de maniere anonyme pour ameliorer le service de sante communautaire.*"
        )

        submitted = st.form_submit_button("Creer mon compte", use_container_width=True)

        if submitted:
            if password != password2:
                st.error("Les mots de passe ne correspondent pas.")
                return
            if not validate_email(email):
                st.error("Email invalide.")
                return
            ok, msg = validate_password(password)
            if not ok:
                st.error(msg)
                return
            ok, msg = validate_profile(prenom, post_nom, age, sexe, localisation)
            if not ok:
                st.error(msg)
                return
            if get_user_by_email(email):
                st.error("Cet email est deja utilise. Connectez-vous.")
                return

            create_user(email, password, prenom, post_nom, age, sexe, localisation)
            st.success("Compte cree avec succes ! Redirection vers la connexion...")
            st.session_state.auth_page = "login"
            st.rerun()

    st.markdown("---")
    if st.button("J'ai deja un compte → Se connecter"):
        st.session_state.auth_page = "login"
        st.rerun()


# =============================================
# PAGE : CONNEXION
# =============================================
def page_login():
    st.title("🏥 UviraTalk")
    st.subheader("Connexion")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Veuillez remplir tous les champs.")
                return

            user = get_user_by_email(email)
            if not user or not verify_password(password, user.password_hash):
                st.error("Email ou mot de passe incorrect.")
                return

            # Récupérer les infos AVANT de sortir du contexte Flask
            with flask_app.app_context():
                u = Utilisateur.query.get(user.id)
                user_data = {
                    "id": u.id,
                    "email": u.email,
                    "prenom": u.prenom,
                    "post_nom": u.post_nom,
                    "age": u.age,
                    "sexe": u.sexe,
                    "localisation": u.localisation,
                    "role": u.role,
                }

            st.session_state.user = user_data
            update_last_login(user.id)

            # Nouvelle conversation
            conv_id = start_new_conversation(user.id)
            st.session_state.conversation_id = conv_id

            # Message d'accueil personnalisé avec salutation selon l'heure
            greeting = get_greeting_response("fr")  # "Bonjour !", "Bonsoir !"...
            prenom = user_data.get('prenom', '')

            welcome_body = (
                f"Je suis **Docteur IA Uvira**, votre assistant sante virtuel. 🩺\n\n"
                "**Je peux vous aider a :**\n"
                "- Decrire vos symptomes et vous orienter\n"
                "- Repondre a vos questions de sante\n"
                "- Vous informer sur les maladies courantes\n\n"
                "**Langues supportees :** Francais, Kiswahili\n\n"
                "Dites-moi, comment puis-je vous aider aujourd'hui ?"
            )

            welcome_msg = f"**{greeting} {prenom} !** Ravi de vous revoir. {welcome_body}"

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": welcome_msg,
                }
            ]

            st.rerun()

    st.markdown("---")
    if st.button("Pas encore de compte ? S'inscrire"):
        st.session_state.auth_page = "register"
        st.rerun()


# =============================================
# PAGE : CHAT
# =============================================
def page_chat():
    user = st.session_state.user

    # --- En-tête ---
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🏥 UviraTalk")
        st.caption(
            f"Connecte : **{user['prenom']} {user.get('post_nom', '')}** "
            f"· {user.get('localisation', '')}"
        )
    with col2:
        if st.button("Deconnexion", use_container_width=True):
            if st.session_state.conversation_id:
                end_conversation(st.session_state.conversation_id)
            st.session_state.user = None
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.session_state.auth_page = "login"
            st.rerun()

    if matcher is None:
        st.error(status_message)
        return

    st.success(status_message)
    st.divider()

    # --- Sidebar ---
    with st.sidebar:
        st.header("💡 Exemples")
        exemples = [
            "Bonjour",
            "Comment vas-tu ?",
            "Que peux-tu faire ?",
            "J'ai la diarrhee",
            "J'ai de la fievre",
            "Mon enfant tousse",
            "Je suis enceinte",
            "Qu'est-ce que le paludisme ?",
            "Je saigne beaucoup",
            "Nina homa",
            "Habari yako",
        ]
        for ex in exemples:
            if st.button(ex, key=f"btn_{ex}"):
                st.session_state.pending_question = ex
                st.rerun()

        st.divider()
        st.header("📊 Statistiques")
        with flask_app.app_context():
            st.metric("Dialogues", DialogueTriage.query.count())
            st.metric("Q&R", QAEducation.query.count())
            st.metric("Utilisateurs", Utilisateur.query.count())

        st.divider()
        if st.button("🗑️ Effacer la conversation"):
            if st.session_state.conversation_id:
                end_conversation(st.session_state.conversation_id)
            new_conv = start_new_conversation(user['id'])
            st.session_state.conversation_id = new_conv
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        f"**{get_greeting_response('fr')} {user['prenom']} !** "
                        "Nouvelle conversation commencee. Comment puis-je vous aider ?"
                    ),
                }
            ]
            st.rerun()

    # --- Affichage des messages ---
    for idx, msg in enumerate(st.session_state.messages):
        avatar = "🩺" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            meta = msg.get("metadata")
            if meta:
                # Alerte urgence
                if meta.get("urgence") in ["Élevée", "Critique", "Très élevée", "Ya juu"]:
                    if meta["urgence"] in ["Critique", "Très élevée"]:
                        st.error(
                            f"⚠️ **URGENCE {meta['urgence'].upper()}**\n\n"
                            f"{meta.get('symptomes', 'Consultez immediatement.')}"
                        )
                    else:
                        st.warning(
                            f"⚠️ **Urgence {meta['urgence']}**\n\n"
                            f"{meta.get('symptomes', 'Consultez rapidement.')}"
                        )

                # Caption technique
                if meta.get("theme"):
                    st.caption(
                        f"Theme : **{meta['theme']}** · "
                        f"Methode : `{meta.get('methode', 'N/A')}`"
                    )

                # Bouton conseils
                if meta.get("type") == "dialogue" and meta.get("theme"):
                    if st.button("📋 Voir les conseils", key=f"advice_{idx}"):
                        st.session_state[f"show_advice_{idx}"] = True

                if st.session_state.get(f"show_advice_{idx}"):
                    advice = get_advice(meta.get("theme"), meta.get("urgence"), "fr")
                    urgence_key = "modere"
                    if meta.get("urgence") in ["Critique", "Très élevée"]:
                        urgence_key = "critique"
                    elif meta.get("urgence") == "Élevée":
                        urgence_key = "eleve"
                    elif meta.get("urgence") == "Faible":
                        urgence_key = "faible"
                    suggestion = get_health_center_suggestion(urgence_key, "fr")
                    if advice:
                        st.info(advice)
                    if suggestion:
                        st.success(suggestion)

    # --- Input ---
    if "pending_question" in st.session_state:
        prompt = st.session_state.pending_question
        del st.session_state.pending_question
    else:
        prompt = st.chat_input("Decrivez vos symptomes ou posez votre question...")

    # --- Traitement ---
    if prompt:
        # Sauvegarder le message utilisateur
        save_message(
            st.session_state.conversation_id,
            "user", prompt
        )
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Appel au moteur
        with flask_app.app_context():
            result = matcher.match_intent(prompt)

        reponse = result.get("reponse", "Desole, je n'ai pas compris.")
        metadata = {
            "methode": result.get("methode"),
            "theme": result.get("theme"),
            "urgence": result.get("urgence"),
            "symptomes": result.get("symptomes"),
            "code": result.get("code"),
            "type": result.get("type"),
        }

        # Sauvegarder la réponse
        save_message(
            st.session_state.conversation_id,
            "assistant", reponse,
            theme=metadata.get("theme"),
            urgence=metadata.get("urgence"),
            methode=metadata.get("methode"),
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": reponse,
            "metadata": metadata,
        })

        st.rerun()


# =============================================
# ROUTAGE
# =============================================
if st.session_state.user is None:
    if st.session_state.auth_page == "login":
        page_login()
    else:
        page_register()
else:
    # Vérifier le rôle : admin → dashboard, patient → chat
    if st.session_state.user.get("role") == "admin":
        show_admin_dashboard(flask_app)
    else:
        page_chat()


# =============================================
# FOOTER
# =============================================
st.divider()
st.caption("UviraTalk — Talents etudiants, solutions locales. © 2026 Hub Tech DRC / UTC-Uvira")