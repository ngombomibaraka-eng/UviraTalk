# admin.py
"""
Tableau de bord administrateur UviraTalk — version sans pyarrow.
Utilise uniquement les composants natifs Streamlit (pas de st.dataframe).
"""

import streamlit as st
from datetime import datetime
from database import Utilisateur, Conversation, Message, DialogueTriage, QAEducation


def show_admin_dashboard(flask_app):
    """Affiche le tableau de bord administrateur."""
    from database import db

    st.title("🛡️ Administration UviraTalk")
    st.caption("Tableau de bord - Suivi des utilisateurs et des conversations")

    # Déconnexion
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("Deconnexion", use_container_width=True):
            st.session_state.user = None
            st.session_state.auth_page = "login"
            st.rerun()

    st.divider()

    # =============================================
    # STATISTIQUES GLOBALES
    # =============================================
    st.header("📊 Statistiques globales")

    with flask_app.app_context():
        nb_users = Utilisateur.query.filter_by(role='patient').count()
        nb_convs = Conversation.query.count()
        nb_msgs = Message.query.count()
        nb_msgs_user = Message.query.filter_by(role='user').count()
        nb_urgences = Message.query.filter(
            Message.urgence.in_(['Critique', 'Très élevée', 'Élevée'])
        ).count()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("👥 Patients", nb_users)
    col2.metric("💬 Conversations", nb_convs)
    col3.metric("✉️ Messages", nb_msgs)
    col4.metric("❓ Questions", nb_msgs_user)
    col5.metric("🚨 Urgences", nb_urgences)

    st.divider()

    # =============================================
    # ONGLETS
    # =============================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Utilisateurs",
        "💬 Conversations",
        "📈 Analyses",
        "🔍 Recherche",
    ])

    # =============================================
    # ONGLET 1 : UTILISATEURS
    # =============================================
    with tab1:
        st.subheader("Liste des patients")

        with flask_app.app_context():
            users = Utilisateur.query.filter_by(role='patient')\
                .order_by(Utilisateur.date_inscription.desc()).all()

            if not users:
                st.info("Aucun utilisateur enregistre pour le moment.")
            else:
                st.caption(f"**{len(users)} patient(s) enregistre(s)**")
                st.markdown("")

                for u in users:
                    nb_conv = Conversation.query.filter_by(user_id=u.id).count()
                    nb_msg = db.session.query(Message)\
                        .join(Conversation)\
                        .filter(Conversation.user_id == u.id).count()

                    with st.container(border=True):
                        col_a, col_b, col_c = st.columns([3, 2, 2])
                        with col_a:
                            st.markdown(f"### 👤 {u.prenom} {u.post_nom or ''}")
                            st.caption(f"📧 {u.email}")
                        with col_b:
                            st.markdown(f"**Age :** {u.age or 'N/A'}")
                            st.markdown(f"**Sexe :** {u.sexe or 'N/A'}")
                        with col_c:
                            st.markdown(f"**Localisation :** {u.localisation or 'N/A'}")
                            st.caption(
                                f"Inscrit : {u.date_inscription.strftime('%d/%m/%Y') if u.date_inscription else 'N/A'}"
                            )
                            st.caption(
                                f"Derniere connexion : {u.derniere_connexion.strftime('%d/%m/%Y %H:%M') if u.derniere_connexion else 'Jamais'}"
                            )

                        st.markdown(
                            f"💬 **{nb_conv}** conversations · "
                            f"✉️ **{nb_msg}** messages"
                        )

    # =============================================
    # ONGLET 2 : CONVERSATIONS
    # =============================================
    with tab2:
        st.subheader("Toutes les conversations")

        with flask_app.app_context():
            convs = Conversation.query.order_by(Conversation.date_debut.desc()).all()

            if not convs:
                st.info("Aucune conversation enregistree.")
            else:
                # Filtre par utilisateur
                users_list = Utilisateur.query.filter_by(role='patient').all()
                options = ["Tous"] + [
                    f"{u.prenom} {u.post_nom or ''} ({u.email})" for u in users_list
                ]
                filtre_user = st.selectbox("Filtrer par utilisateur", options, key="filtre_conv")

                # Filtrer
                filtered = []
                for c in convs:
                    with flask_app.app_context():
                        user = db.session.get(Utilisateur, c.user_id)
                    label = f"{user.prenom} {user.post_nom or ''} ({user.email})" if user else "Inconnu"
                    if filtre_user == "Tous" or filtre_user == label:
                        filtered.append((c, label))

                st.caption(f"**{len(filtered)} conversation(s)**")

                for c, label in filtered:
                    with st.container(border=True):
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"### 💬 Conversation #{c.id}")
                            st.caption(f"👤 {label}")
                        with col_b:
                            st.metric("Messages", c.nb_messages or 0)

                        st.caption(
                            f"Debut : {c.date_debut.strftime('%d/%m/%Y %H:%M') if c.date_debut else 'N/A'}"
                            f" · Fin : {c.date_fin.strftime('%d/%m/%Y %H:%M') if c.date_fin else 'En cours'}"
                        )

                        if st.button(f"🔍 Voir le detail", key=f"detail_conv_{c.id}"):
                            st.session_state[f"view_conv_{c.id}"] = not st.session_state.get(f"view_conv_{c.id}", False)

                        if st.session_state.get(f"view_conv_{c.id}"):
                            show_conversation_detail(c.id, flask_app)

    # =============================================
    # ONGLET 3 : ANALYSES
    # =============================================
    with tab3:
        st.subheader("📈 Analyses des besoins utilisateurs")

        with flask_app.app_context():
            # Top themes
            st.markdown("### 🔝 Top 10 des themes les plus demandes")
            top_themes = db.session.query(
                Message.theme, db.func.count(Message.id).label('count')
            ).filter(
                Message.role == 'user',
                Message.theme.isnot(None)
            ).group_by(Message.theme).order_by(db.desc('count')).limit(10).all()

            if top_themes:
                max_count = max(t[1] for t in top_themes)
                for theme, count in top_themes:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        bar = "█" * int((count / max_count) * 30)
                        st.markdown(f"**{theme}** {bar}")
                    with col2:
                        st.markdown(f"**{count}**")
            else:
                st.info("Aucune donnee disponible pour le moment.")

            st.markdown("---")

            # Urgences
            st.markdown("### 🚨 Urgences detectees par theme")
            urgences = db.session.query(
                Message.theme,
                Message.urgence,
                db.func.count(Message.id).label('count')
            ).filter(
                Message.urgence.isnot(None),
                Message.urgence.in_(['Élevée', 'Critique', 'Très élevée'])
            ).group_by(Message.theme, Message.urgence).all()

            if urgences:
                for theme, urgence, count in urgences:
                    st.markdown(f"- **{theme}** · {urgence} : **{count}** cas")
            else:
                st.info("Aucune urgence detectee.")

            st.markdown("---")

            # Langues
            st.markdown("### 🌍 Repartition par langue")
            langues = db.session.query(
                Message.langue, db.func.count(Message.id).label('count')
            ).filter(
                Message.role == 'user',
                Message.langue.isnot(None)
            ).group_by(Message.langue).all()

            if langues:
                for langue, count in langues:
                    nom = "Francais" if langue == 'fr' else "Kiswahili" if langue == 'sw' else langue
                    st.markdown(f"- **{nom}** : {count} messages")
            else:
                st.info("Aucune donnee de langue.")

    # =============================================
    # ONGLET 4 : RECHERCHE
    # =============================================
    with tab4:
        st.subheader("🔍 Recherche dans les messages")

        query = st.text_input("Rechercher un mot-cle dans les messages",
                              placeholder="Ex : fievre, diarrhee, paludisme...")

        if query and len(query) >= 2:
            with flask_app.app_context():
                results = Message.query.filter(
                    Message.contenu.ilike(f"%{query}%")
                ).order_by(Message.date_envoi.desc()).limit(50).all()

                if results:
                    st.success(f"{len(results)} resultat(s) trouve(s)")

                    for m in results:
                        with flask_app.app_context():
                            user = db.session.query(Utilisateur)\
                                .join(Conversation)\
                                .filter(Conversation.id == m.conversation_id).first()

                        with st.container(border=True):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**{m.role.upper()}**")
                                st.write(m.contenu[:300] + ("..." if len(m.contenu) > 300 else ""))
                            with col2:
                                st.caption(
                                    m.date_envoi.strftime('%d/%m/%Y %H:%M') if m.date_envoi else ''
                                )
                                if user:
                                    st.caption(f"👤 {user.prenom}")

                            if m.theme:
                                st.caption(f"🎯 {m.theme} · ⚠️ {m.urgence or 'N/A'}")
                else:
                    st.info("Aucun resultat.")


def show_conversation_detail(conv_id, flask_app):
    """Affiche le detail d'une conversation."""
    from database import db

    with flask_app.app_context():
        conv = db.session.get(Conversation, conv_id)
        if not conv:
            st.error("Conversation introuvable.")
            return

        user = db.session.get(Utilisateur, conv.user_id)
        messages = Message.query.filter_by(conversation_id=conv_id)\
            .order_by(Message.date_envoi).all()

    st.markdown("---")
    st.markdown(f"#### 📋 Detail de la conversation #{conv_id}")

    if user:
        st.markdown(
            f"**Utilisateur** : {user.prenom} {user.post_nom or ''} ({user.email})"
        )
        st.markdown(f"**Localisation** : {user.localisation or 'N/A'}")

    st.markdown(f"**Debut** : {conv.date_debut.strftime('%d/%m/%Y %H:%M') if conv.date_debut else 'N/A'}")
    st.markdown(f"**Fin** : {conv.date_fin.strftime('%d/%m/%Y %H:%M') if conv.date_fin else 'En cours'}")
    st.markdown(f"**Messages** : {len(messages)}")

    st.markdown("")

    for msg in messages:
        role_icon = "👤" if msg.role == "user" else "🩺"
        timestamp = msg.date_envoi.strftime("%H:%M:%S") if msg.date_envoi else ""

        with st.container(border=True):
            st.markdown(f"{role_icon} **{msg.role.title()}** · *{timestamp}*")
            st.write(msg.contenu)

            if msg.theme or msg.urgence or msg.methode:
                badges = []
                if msg.theme:
                    badges.append(f"🎯 {msg.theme}")
                if msg.urgence:
                    badges.append(f"⚠️ {msg.urgence}")
                if msg.methode:
                    badges.append(f"🔧 {msg.methode}")
                st.caption(" · ".join(badges))