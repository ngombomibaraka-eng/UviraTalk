from datetime import datetime
import random
import os
import re
from flask import Flask, request, jsonify, send_file, render_template_string, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Importation depuis nos fichiers locaux
from database import db, User, PhraseMultilingue, Signalement, Article, CentreSante
from intent_matcher import intent_matcher

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-uviratalk-secure-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uviratalk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None

# --- STYLES CSS COMMUNS ---
COMMON_CSS = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #0f766e, #064e3b); margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .login-card { background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.2); width: 100%; max-width: 400px; text-align: center; }
        h2 { color: #0f766e; margin-bottom: 0.5rem; margin-top: 0; }
        p.subtitle { color: #64748b; margin-bottom: 2rem; font-size: 0.9rem; }
        .form-group { margin-bottom: 1rem; text-align: left; }
        label { display: block; margin-bottom: 0.5rem; color: #334155; font-size: 0.9rem; font-weight: 600; }
        input { width: 100%; padding: 12px 15px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; transition: 0.3s; box-sizing: border-box; }
        input:focus { border-color: #0f766e; outline: none; box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.1); }
        button { width: 100%; padding: 14px; background: #0f766e; color: white; border: none; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        button:hover { background: #0d5f56; transform: translateY(-2px); }
        .link { display: block; margin-top: 1.5rem; color: #0f766e; text-decoration: none; font-weight: 600; font-size: 0.9rem; }
        .link:hover { text-decoration: underline; }
        .error-msg { background: #fee2e2; color: #b91c1c; padding: 10px; border-radius: 8px; margin-bottom: 1rem; font-size: 0.9rem; }
        .logo { font-size: 2rem; margin-bottom: 1rem; }
    </style>
"""

# --- FONCTIONS UTILITAIRES ---
def normalize(text):
    if not text: return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def detect_greeting(message):
    msg = normalize(message)
    greetings = ["bonjour", "salut", "hello", "bonsoir", "slt", "bjr", "wapi", "habari", "mambo", "jambo", "mbote"]
    return any(mot in msg for mot in greetings)

def reponse_greeting():
    heure = datetime.now().hour
    if 5 <= heure < 12: return random.choice(["Bonjour ! Comment puis-je vous aider ?", "Bonjour. Avez-vous un symptôme ?"])
    elif 12 <= heure < 17: return random.choice(["Bon après-midi. Comment allez-vous ?", "Bonjour. Je suis là pour vous aider."])
    elif 17 <= heure < 22: return random.choice(["Bonsoir. Avez-vous un problème de santé ?", "Bonsoir. Je vous écoute."])
    else: return random.choice(["Bonne nuit. Une urgence ?", "Je suis là si vous avez besoin d'aide."])

# --- TEMPLATES HTML (Pour les pages d'authentification) ---

LOGIN_HTML = '''
<!DOCTYPE html>
<html><head><title>Connexion Admin</title><meta name="viewport" content="width=device-width,initial-scale=1">
''' + COMMON_CSS + '''
</head><body>
    <div class="login-card">
        <div class="logo">🏥</div>
        <h2>Admin UviraTalk</h2>
        <p class="subtitle">Accès réservé au personnel</p>
        {% with messages = get_flashed_messages() %}
            {% if messages %}<div class="error-msg">{{ messages[0] }}</div>{% endif %}
        {% endwith %}
        <form method="post">
            <div class="form-group"><label>Nom d'utilisateur</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Mot de passe</label><input type="password" name="password" required></div>
            <button type="submit">Se connecter</button>
        </form>
        <a href="/" class="link">← Retour au site</a>
    </div>
</body></html>'''

REGISTER_HTML = '''
<!DOCTYPE html>
<html><head><title>Inscription</title><meta name="viewport" content="width=device-width,initial-scale=1">
''' + COMMON_CSS + '''
</head><body>
    <div class="login-card">
        <div class="logo">🌿</div>
        <h2>Créer un compte</h2>
        <p class="subtitle">Rejoignez la communauté UviraTalk</p>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% for category, msg in messages if category == 'error' %}
                <div class="error-msg">{{ msg }}</div>
            {% endfor %}
        {% endwith %}
        <form method="post">
            <div class="form-group"><label>Nom d'utilisateur</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Mot de passe</label><input type="password" name="password" required></div>
            <button type="submit">S'inscrire</button>
        </form>
        <a href="/user/login" class="link">Déjà un compte ? Se connecter</a>
    </div>
</body></html>'''

USER_LOGIN_HTML = '''
<!DOCTYPE html>
<html><head><title>Connexion Utilisateur</title><meta name="viewport" content="width=device-width,initial-scale=1">
''' + COMMON_CSS + '''
</head><body>
    <div class="login-card">
        <div class="logo">👤</div>
        <h2>Bonjour</h2>
        <p class="subtitle">Connectez-vous pour accéder à votre espace</p>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% for category, msg in messages if category == 'error' %}
                <div class="error-msg">{{ msg }}</div>
            {% endfor %}
        {% endwith %}
        <form method="post">
            <div class="form-group"><label>Nom d'utilisateur</label><input type="text" name="username" required></div>
            <div class="form-group"><label>Mot de passe</label><input type="password" name="password" required></div>
            <button type="submit">Se connecter</button>
        </form>
        <a href="/register" class="link">Pas encore de compte ? S'inscrire</a>
        <a href="/" class="link" style="margin-top:10px; font-weight:400;">Retour accueil</a>
    </div>
</body></html>'''

USER_DASHBOARD_HTML = '''<!DOCTYPE html><html><head><title>Mon Compte</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;background:#f4f4f4;padding:20px}.navbar{background:#0f766e;color:white;padding:15px;display:flex;justify-content:space-between}.container{max-width:800px;margin:20px auto}.card{background:white;padding:20px;margin-bottom:20px;border-radius:12px;box-shadow:0 2px 5px rgba(0,0,0,0.1)}table{width:100%;border-collapse:collapse}th,td{border:1px solid #ddd;padding:8px;text-align:left}th{background-color:#0f766e;color:white}a{color:#0f766e;text-decoration:none;padding:10px 20px;background:#e0f2f1;border-radius:20px;margin-right:10px}.btn-danger{background:#fee2e2;color:#b91c1c}</style></head><body><div class="navbar"><h3>Mon Espace</h3><div><a href="/">Accueil</a><a href="/user/logout" class="btn-danger">Déconnexion</a></div></div><div class="container"><div class="card"><h3>Bonjour, {{ user.username }}</h3></div><div class="card"><h3>Mes Signalements</h3><table><tr><th>Symptôme</th><th>Date</th></tr>{% for s in signalements %}<tr><td>{{ s.symptome }}</td><td>{{ s.date_signalement.strftime('%d/%m/%Y') }}</td></tr>{% endfor %}</table></div></div></body></html>'''

DASHBOARD_HTML = '''<!DOCTYPE html><html><head><title>Dashboard Admin</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:'Segoe UI',Roboto,sans-serif;background:#f0fdf4;padding:20px}.navbar{background:#0f766e;color:white;padding:15px;display:flex;justify-content:space-between}.container{max-width:1000px;margin:20px auto}.card{background:white;padding:20px;margin-bottom:20px;border-radius:12px;box-shadow:0 4px 6px rgba(0,0,0,0.05)}table{width:100%;border-collapse:collapse;margin-top:10px}th,td{border:1px solid #e2e8f0;padding:12px;text-align:left}th{background-color:#f0fdf4;color:#0f766e;font-weight:600}input,textarea,select,button{width:100%;padding:12px;margin:5px 0;border:1px solid #cbd5e1;border-radius:8px}button{background:#0f766e;color:white;border:none;cursor:pointer;font-weight:600}</style></head><body><div class="navbar"><h3>UviraTalk Admin</h3><a href="/admin/logout" style="color:white;text-decoration:none;background:#b91c1c;padding:5px 15px;border-radius:20px">Déconnexion</a></div><div class="container"><div class="card"><h3>Statistiques</h3><p>Utilisateurs: {{ total_users }}</p><p>Signalements: {{ total_signals }}</p></div><div class="card"><h3>Signalements Récents</h3><table><tr><th>Symptôme</th><th>Lieu</th><th>Date</th></tr>{% for s in recent_signals %}<tr><td>{{ s.symptome }}</td><td>{{ s.localisation }}</td><td>{{ s.date_signalement.strftime('%d/%m/%Y') }}</td></tr>{% endfor %}</table></div><div class="card"><h3>Ajouter Article</h3><form method="post" action="/admin/article/new"><input type="text" name="titre" placeholder="Titre" required><textarea name="contenu" placeholder="Contenu" required></textarea><select name="categorie"><option value="actualite">Actualité</option><option value="conseil">Conseil</option></select><button type="submit">Publier</button></form></div></div></body></html>'''

# --- ROUTES ---

@app.route('/')
def index():
    # On sert le fichier index.html statique
    try:
        return send_file('index.html')
    except FileNotFoundError:
        return "Erreur: Fichier index.html introuvable.", 404

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get('message', '')
        if not user_msg: 
            return jsonify({'reponse': "Je n'ai rien reçu.", 'intent': 'error'})
        
        user_norm = normalize(user_msg)
        
        # Gestion simple des confirmations "Oui"
        confirmation_words = ['oui', 'yes', 'ndiyo', 'ehe', 'ya', 'ok', 'daccord']
        if any(mot in user_norm for mot in confirmation_words):
            return jsonify({
                'reponse': "D'accord. Pourriez-vous me décrire ce que vous ressentez ? (Ex: mal de tête, fièvre, toux...)", 
                'intent': 'confirmation'
            })

        # Gestion des salutations
        if detect_greeting(user_msg):
            return jsonify({'reponse': reponse_greeting(), 'intent': 'greeting'})

        # Appel au Matcher IA
        intent, reponse = intent_matcher.match_intent(user_msg)
        
        # Formatage de la réponse pour le Web (remplace \n par <br>)
        reponse_formatee = reponse.replace('\n', '<br>')
        
        return jsonify({
            'reponse': reponse_formatee,
            'intent': intent
        })

    except Exception as e:
        print(f"!!! ERREUR CRITIQUE DANS /api/chat : {e}")
        return jsonify({'reponse': "Désolé, une erreur technique est survenue.", 'intent': 'error'}), 500

@app.route('/api/signalement', methods=['POST'])
def ajouter_signalement():
    try:
        data = request.json
        user_id = current_user.id if current_user.is_authenticated else None
        
        signal = Signalement(
            user_id=user_id, 
            symptome=data.get('symptome'), 
            description=data.get('description'), 
            localisation=data.get('lieu'), 
            latitude=data.get('latitude'), 
            longitude=data.get('longitude')
        )
        db.session.add(signal)
        db.session.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Erreur signalement: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/api/articles')
def get_articles():
    try:
        articles = Article.query.order_by(Article.date_publication.desc()).limit(10).all()
        return jsonify([{
            'titre': a.titre, 
            'contenu': a.contenu, 
            'categorie': a.categorie, 
            'date': a.date_publication.strftime('%d/%m/%Y')
        } for a in articles])
    except: 
        return jsonify([])

@app.route('/api/centres')
def get_centres():
    try:
        centres = CentreSante.query.all()
        return jsonify([{
            'nom': c.nom, 
            'adresse': c.adresse, 
            'latitude': str(c.latitude), 
            'longitude': str(c.longitude), 
            'telephone': c.telephone
        } for c in centres])
    except: 
        return jsonify([])

# --- ROUTES AUTHENTIFICATION ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']) and user.role == 'admin':
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Identifiants invalides')
    return render_template_string(LOGIN_HTML)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin': 
        return redirect(url_for('index'))
    return render_template_string(
        DASHBOARD_HTML, 
        total_users=User.query.count(), 
        total_signals=Signalement.query.count(), 
        recent_signals=Signalement.query.order_by(Signalement.date_signalement.desc()).limit(20).all()
    )

@app.route('/admin/article/new', methods=['POST'])
@login_required
def new_article():
    try:
        article = Article(
            titre=request.form['titre'], 
            contenu=request.form['contenu'], 
            categorie=request.form['categorie'], 
            auteur_id=current_user.id
        )
        db.session.add(article)
        db.session.commit()
        flash('Article publié')
    except Exception as e:
        print(f"Erreur article: {e}")
        flash('Erreur lors de la publication')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            if User.query.filter_by(username=request.form['username']).first(): 
                flash("Nom déjà pris", "error")
            else:
                u = User(
                    username=request.form['username'], 
                    password=generate_password_hash(request.form['password']), 
                    role='user'
                )
                db.session.add(u)
                db.session.commit()
                login_user(u)
                return redirect(url_for('user_dashboard'))
        except Exception as e:
            print(f"Erreur register: {e}")
            flash("Erreur", "error")
    return render_template_string(REGISTER_HTML)

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['username']).first()
        if u and check_password_hash(u.password, request.form['password']): 
            login_user(u)
            return redirect(url_for('user_dashboard'))
        flash("Identifiants incorrects", "error")
    return render_template_string(USER_LOGIN_HTML)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.role == 'admin': 
        return redirect(url_for('admin_dashboard'))
    return render_template_string(
        USER_DASHBOARD_HTML, 
        user=current_user, 
        signalements=Signalement.query.filter_by(user_id=current_user.id).order_by(Signalement.date_signalement.desc()).all()
    )

@app.route('/user/logout')
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('index'))

# --- INITIALISATION DE LA BASE DE DONNÉES ---
def init_db():
    with app.app_context():
        db.create_all()
        
        # Création de l'admin par défaut
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin créé (user: admin, pass: admin123)")
        
        # Insertion des données IA si la table est vide
        # Note : On met un try/except car insert_data.py peut contenir des erreurs de syntaxe
        if PhraseMultilingue.query.count() == 0:
            try:
                # Import local
                from insert_data import insert_data
                print("📥 Insertion des données IA en cours...")
                insert_data()
                print("✅ Données IA insérées avec succès")
            except Exception as e:
                print(f"⚠️ Erreur lors de l'insertion des données : {e}")
                print("⚠️ L'application démarrera sans données d'entraînement.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
    