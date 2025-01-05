from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
from googletrans import Translator

# Initialiser Google Translator
translator = Translator()

# Charger les variables d'environnement
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

# CONFIGURATION DE L'APPLICATION FLASK

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cuisine_app.db'
db = SQLAlchemy(app)

# Initialisation de LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'connexion'

# MODELE DE L'UTILISATEUR
class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# MODELE POUR LE QUESTIONNAIRE
class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    cooking_level = db.Column(db.String(50), nullable=False)
    prep_time = db.Column(db.String(50), nullable=False)
    cooking_type = db.Column(db.String(50), nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recette(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"<Recette {self.nom}>"

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        if password != confirm_password:
            return "Les mots de passe ne correspondent pas."

        existing_user = Utilisateur.query.filter_by(email=email).first()
        if existing_user:
            return "Un utilisateur avec cet email existe déjà."

        hashed_password = generate_password_hash(password)
        user = Utilisateur(username=username, email=email, password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            login_user(user)
            return redirect(url_for('questionnaire'))
        except IntegrityError:
            db.session.rollback()
            return "Erreur lors de l'inscription."

    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Utilisateur.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('questionnaire'))
        else:
            return "Identifiants incorrects. Essayez à nouveau."

    return render_template('connexion.html')

@app.route('/profil')
@login_required
def profil():
    return render_template('profil.html', username=current_user.username, email=current_user.email)

@app.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():
    if request.method == 'POST':
        cooking_level = request.form['cookingLevel']
        prep_time = request.form['prepTime']
        cooking_type = request.form['cookingType']
        number_of_people = request.form['numberOfPeople']

        questionnaire_data = Questionnaire(
            user_id=current_user.id,
            cooking_level=cooking_level,
            prep_time=prep_time,
            cooking_type=cooking_type,
            number_of_people=number_of_people
        )
        db.session.add(questionnaire_data)
        db.session.commit()

        return redirect(url_for('ingredients'))

    return render_template('questionnaire.html')

@app.route('/ingredients', methods=['GET', 'POST'])
@login_required
def ingredients():
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        return redirect(url_for('generer_recettes', ingredients=ingredients))
    return render_template('ingredients.html')

@app.route('/generer_recettes')
@login_required
def generer_recettes():
    ingredients = request.args.get('ingredients')
    if not ingredients:
        return "Aucun ingrédient fourni.", 400

    recettes = obtenir_recettes_ingredients(ingredients)
    if not recettes:
        message = "Aucune recette trouvée pour ces ingrédients. Essayez d'autres combinaisons."
        return render_template('generer_recettes.html', recettes=[], message=message, ingredients=ingredients)

    return render_template('generer_recettes.html', recettes=recettes, ingredients=ingredients)

@app.route('/deconnexion')
def deconnexion():
    logout_user()
    return redirect(url_for('accueil'))

@app.route('/test_api')
def test_api():
    ingredients = request.args.get('ingredients', 'tomato,chicken,rice')
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "ingredients": ingredients,
        "number": 5,
        "ranking": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        recettes = response.json()
        return jsonify(recettes)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})

def obtenir_recettes_ingredients(ingredients, max_recipes=5):
    # Traduire les ingrédients en anglais
    translated_ingredients = translator.translate(ingredients, src="fr", dest="en").text

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "ingredients": translated_ingredients,
        "number": max_recipes,
        "ranking": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        recettes = response.json()
        return [
            {
                "title": translator.translate(recette["title"], src="en", dest="fr").text,
                "image": recette["image"],
                "sourceUrl": f"https://spoonacular.com/recipes/{recette['title'].replace(' ', '-')}-{recette['id']}"
            } for recette in recettes
        ]
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à l'API Spoonacular : {e}")
        return []

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
