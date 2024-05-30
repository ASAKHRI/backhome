import sqlite3
from werkzeug.security import generate_password_hash

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('database.db')

# Création du curseur
cursor = conn.cursor()

# Création de la table users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Ajouter des utilisateurs (ajoutez vos propres utilisateurs ici)
users = [
    ('admin', generate_password_hash('admin123')),
    ('user', generate_password_hash('user123'))
]

# Insertion des utilisateurs dans la table
cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

# Création de la table requests
cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_data TEXT NOT NULL,
        prediction REAL NOT NULL,
        decision TEXT NOT NULL
    )
''')

# Sauvegarde des modifications
conn.commit()

# Fermeture de la connexion
conn.close()
