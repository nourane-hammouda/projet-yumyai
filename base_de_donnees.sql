CREATE DATABASE IF NOT EXISTS Yumyai;
USE Yumyai;

-- Table Utilisateurs
CREATE TABLE IF NOT EXISTS Utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Mot_De_Passe VARCHAR(255) NOT NULL,
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index sur l'email des utilisateurs
CREATE INDEX idx_email ON Utilisateurs(email);

-- Table des Préférences des Utilisateurs
CREATE TABLE IF NOT EXISTS Preferences_utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    niveau_cuisine ENUM('Débutant', 'Pas mal', 'Je suis un chef') NOT NULL,
    temps_preparation ENUM('15 min', '30 min', '1 h', 'jai tout mon temps') NOT NULL,
    type_du_repas ENUM('Chaud', 'Froid') NOT NULL,
    nombre_de_personne INT NOT NULL,
    date_mise_a_jour DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);

-- Table des Ingrédients des Utilisateurs
CREATE TABLE IF NOT EXISTS Ingredients_utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    ingredient VARCHAR(100) NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);

-- Table des Recettes
CREATE TABLE IF NOT EXISTS Recettes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    ingredients VARCHAR(255) NOT NULL,  
    temps_preparation INT NOT NULL, 
    difficulte INT NOT NULL,  
    type_du_repas ENUM('Chaud', 'Froid') NOT NULL,
    image_url VARCHAR(255),  
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table des Ingrédients des Recettes
CREATE TABLE IF NOT EXISTS Ingredients_recette (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recette_id INT NOT NULL,
    ingredient VARCHAR(100) NOT NULL,
    FOREIGN KEY (recette_id) REFERENCES Recettes(id) ON DELETE CASCADE
);

-- Index pour optimiser les recherches par ingrédients
CREATE INDEX idx_ingredients_recette ON Ingredients_recette(ingredient);

