from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import os

# Initialisation des outils
bcrypt = Bcrypt()

# Connexion à la base de données MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["recette"]
user_collection = db["users"]

# Fonction pour créer un utilisateur
def create_user(name, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {"name": name, "email": email, "password": hashed_password}
    user_collection.insert_one(user)

# Fonction pour trouver un utilisateur par email
def find_user_by_email(email):
    return user_collection.find_one({"email": email})
