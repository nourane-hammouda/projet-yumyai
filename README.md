from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données (utilisation de SQLite dans cet exemple)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yumyai.db'  # SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactiver le suivi des modifications

# Initialisation de SQLAlchemy avec Flask
db = SQLAlchemy(app)

# Exemple d'une table utilisateur
class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Utilisateur {self.email}>'

# Créer les tables dans la base de données (si elles n'existent pas)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
