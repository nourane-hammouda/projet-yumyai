from flask import Blueprint, render_template , jsonify
from flask import jsonify , request 
from app import db
from models import PreferencesUtilisateur
from app.algorithmes import suggest_recipes


# Créer un Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
# endpoints pour les préferences  
@bp.route('/api/preferences/<int:utilisateur_id>', methods=['GET'])
def get_preferences(utilisateur_id):
    preferences = PreferencesUtilisateur.query.filter_by(utilisateur_id=utilisateur_id).first()
    
    if preferences:
        return jsonify({
            'niveau_cuisine': preferences.niveau_cuisine,
            'temps_preparation': preferences.temps_preparation,
            'type_du_repas': preferences.type_du_repas,
            'nombre_de_personne': preferences.nombre_de_personne
        })
    else:
        return jsonify({'message': 'Aucune préférence trouvée pour cet utilisateur.'}), 404

@bp.route('/api/preferences/<int:utilisateur_id>', methods=['POST'])
def update_preferences(utilisateur_id):
    data = request.get_json()

    # Extraire les données envoyées par le frontend
    niveau_cuisine = data.get('niveau_cuisine')
    temps_preparation = data.get('temps_preparation')
    type_du_repas = data.get('type_du_repas')
    nombre_de_personne = data.get('nombre_de_personne')

    # Vérifier que toutes les informations sont présentes
    if not niveau_cuisine or not temps_preparation or not type_du_repas or not nombre_de_personne:
        return jsonify({'message': 'Tous les champs sont nécessaires.'}), 400

    # Vérifier si les préférences existent déjà
    preferences = PreferencesUtilisateur.query.filter_by(utilisateur_id=utilisateur_id).first()

    if preferences:
        # Mise à jour des préférences
        preferences.niveau_cuisine = niveau_cuisine
        preferences.temps_preparation = temps_preparation
        preferences.type_du_repas = type_du_repas
        preferences.nombre_de_personne = nombre_de_personne
    else:
        # Créer de nouvelles préférences pour l'utilisateur
        preferences = PreferencesUtilisateur(
            utilisateur_id=utilisateur_id,
            niveau_cuisine=niveau_cuisine,
            temps_preparation=temps_preparation,
            type_du_repas=type_du_repas,
            nombre_de_personne=nombre_de_personne
        )
        db.session.add(preferences)

    db.session.commit()

    return jsonify({'message': 'Préférences mises à jour avec succès !'}), 200

# endpoints pour les ingrédients dispo 

@bp.route('/api/ingredients/<int:utilisateur_id>', methods=['GET'])
def get_ingredients(utilisateur_id):
    preferences = PreferencesUtilisateur.query.filter_by(utilisateur_id=utilisateur_id).first()
    
    if preferences and preferences.ingredients:
        return jsonify({'ingredients': preferences.ingredients.split(',')})  # Convertir la chaîne d'ingrédients en liste
    else:
        return jsonify({'message': 'Aucun ingrédient trouvé pour cet utilisateur.'}), 404

def update_ingredients(utilisateur_id):
    data = request.get_json()
    ingredients = data.get('ingredients')

    if not ingredients:
        return jsonify({'message': 'Veuillez fournir des ingrédients.'}), 400

    # Mettre à jour ou créer les ingrédients pour l'utilisateur
    preferences = PreferencesUtilisateur.query.filter_by(utilisateur_id=utilisateur_id).first()

    if preferences:
        preferences.ingredients = ingredients  # Met à jour les ingrédients
    else:
        preferences = PreferencesUtilisateur(
            utilisateur_id=utilisateur_id,
            ingredients=ingredients
        )
        db.session.add(preferences)

    db.session.commit()

    return jsonify({'message': 'Ingrédients enregistrés avec succès !'}), 200



# Créer un Blueprint pour les suggestions
suggestions_bp = Blueprint('suggestions', __name__)

@suggestions_bp.route('/api/suggestions/<int:user_id>', methods=['GET'])
def get_suggestions(user_id):
    suggestions = suggest_recipes(user_id)
    if isinstance(suggestions, dict) and 'message' in suggestions:
        return jsonify(suggestions), 404  # Si un message d'erreur est retourné, on renvoie une erreur 404
    return jsonify(suggestions), 200
