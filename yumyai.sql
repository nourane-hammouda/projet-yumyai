CREATE DATABASE IF NOT EXISTS Yumyai ;
USE Yumyai ;
CREATE TABLE IF NOT EXISTS Utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Mot De Passe VARCHAR(255) NOT NULL,
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS Preferences_utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    niveau_cuisine ENUM('débutant', 'intermédiaire', 'avancé') NOT NULL,
    temps_preparation ENUM('15 min', '30 min', '1 h') NOT NULL,
    ingredients TEXT,
    date_mise_a_jour DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);
CREATE INDEX idx_email ON Utilisateurs(email);
