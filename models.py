from flask_sqlalchemy import SQLAlchemy

from app import db

class Utilisateur(db.Model):
    __tablename__ = 'Utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    date_inscription = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    preferences = db.relationship('PreferencesUtilisateur', backref='utilisateur', lazy=True)


class PreferencesUtilisateur(db.Model):
    __tablename__ = 'Preferences_utilisateur'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('Utilisateurs.id'), nullable=False)
    niveau_cuisine = db.Column(db.Enum('Débutant', 'Pas mal', 'Je suis un chef'), nullable=False)
    temps_preparation = db.Column(db.Enum('15 min', '30 min', '1 h', 'j\'ai tout mon temps'), nullable=False)
    type_du_repas = db.Column(db.Enum('Chaud', 'Froid'), nullable=False)
    nombre_de_personne = db.Column(db.Integer, nullable=False)
    date_mise_a_jour = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Recette(db.Model):
    __tablename__ = 'Recettes'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)  # Liste des ingrédients séparés par des virgules
    temps_preparation = db.Column(db.Integer, nullable=False)  # En minutes
    difficulte = db.Column(db.Integer, nullable=False)  # 1 = facile, 2 = moyen, 3 = difficile
    type_du_repas = db.Column(db.String(50), nullable=False)  # 'Chaud', 'Froid', etc.
    image_url = db.Column(db.String(255), nullable=True)  # URL de l'image de la recette

