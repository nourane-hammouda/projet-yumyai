from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config.from_object('config.Config')

    db.init_app(app)

    # Importation des Blueprints
    from app.routes import bp as routes_bp
    from app.preferences import preferences_bp
    from app.ingredients import ingredients_bp
    from app.suggestions import suggestions_bp  # Importer le Blueprint des suggestions
    
    app.register_blueprint(routes_bp)
    app.register_blueprint(preferences_bp)
    app.register_blueprint(ingredients_bp)
    app.register_blueprint(suggestions_bp)  # Enregistrer le Blueprint des suggestions

    return app
