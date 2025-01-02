# app/algorithmes.py
from app.models import Recette, PreferencesUtilisateur

def suggest_recipes(user_id):
    # 1. Récupérer les préférences de l'utilisateur
    preferences = PreferencesUtilisateur.query.filter_by(utilisateur_id=user_id).first()
    if not preferences:
        return {'message': 'Aucune préférence trouvée pour cet utilisateur.'}, 404
    
    # 2. Récupérer les ingrédients de l'utilisateur (en supposant que les ingrédients sont stockés sous forme de chaîne séparée par des virgules)
    ingredients_utilisateur = preferences.ingredients.split(',') if preferences.ingredients else []
    
    # 3. Filtrer les recettes selon les préférences
    recettes = Recette.query.all()
    recettes_suggerees = []

    for recette in recettes:
        # Vérifier si la recette correspond aux préférences de l'utilisateur
        if not check_preferences_match(recette, preferences):
            continue
        
        # Vérifier si l'utilisateur a les ingrédients nécessaires pour cette recette
        if not check_ingredients_match(recette, ingredients_utilisateur):
            continue
        
        # Si la recette passe les filtres, on l'ajoute à la liste
        recettes_suggerees.append({
            'nom': recette.nom,
            'image_url': recette.image_url,
            'ingredients': recette.ingredients.split(','),
            'temps_preparation': recette.temps_preparation,
            'difficulte': recette.difficulte
        })

    return recettes_suggerees

def check_preferences_match(recette, preferences):
    """Vérifie si la recette correspond aux préférences de l'utilisateur"""
    # Vérifier le temps de préparation
    if recette.temps_preparation > convert_preference_to_minutes(preferences.temps_preparation):
        return False
    
    # Vérifier le niveau de difficulté
    if recette.difficulte > convert_difficulty_level(preferences.niveau_cuisine):
        return False
    
    # Vérifier le type de repas
    if preferences.type_du_repas.lower() not in recette.type_du_repas.lower():
        return False
    
    return True

def check_ingredients_match(recette, user_ingredients):
    """Vérifie si l'utilisateur a tous les ingrédients nécessaires pour la recette"""
    recette_ingredients = set(recette.ingredients.split(','))
    user_ingredients_set = set(user_ingredients)
    
    # Si tous les ingrédients de la recette sont dans les ingrédients de l'utilisateur
    return recette_ingredients.issubset(user_ingredients_set)

def convert_preference_to_minutes(temps_preparation):
    """Convertit le temps de préparation préféré en minutes"""
    if temps_preparation == '15 min':
        return 15
    elif temps_preparation == '30 min':
        return 30
    elif temps_preparation == '1 h':
        return 60
    else:  # 'j'ai tout mon temps'
        return 120  # Un grand nombre, juste pour indiquer que le temps est illimité

def convert_difficulty_level(niveau_cuisine):
    """Convertit le niveau de cuisine préféré en un niveau de difficulté"""
    if niveau_cuisine == 'Débutant':
        return 1
    elif niveau_cuisine == 'Pas mal':
        return 2
    else:  # 'Je suis un chef'
        return 3
