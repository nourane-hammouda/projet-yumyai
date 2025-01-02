import os

class Config:
    DEBUG = True
    SECRET_KEY = 'ma_clé_secrète'
    # config.py

    # Connexion à la base de données MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/Yumyai'  # Change avec tes propres identifiants DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Clé secrète pour la gestion des sessions Flask

