import sqlite3
from werkzeug.security import generate_password_hash
import pandas as pd

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
        NAME_CONTRACT_TYPE TEXT NOT NULL,
        FLAG_OWN_CAR TEXT NOT NULL, 
        FLAG_OWN_REALTY TEXT NOT NULL, 
        CNT_CHILDREN TEXT NOT NULL, 
        AMT_INCOME_TOTAL TEXT NOT NULL, 
        AMT_CREDIT_x TEXT NOT NULL, 
        AMT_ANNUITY_x TEXT NOT NULL, 
        AMT_GOODS_PRICE TEXT NOT NULL, 
        DAYS_BIRTH TEXT NOT NULL, 
        DAYS_EMPLOYED TEXT NOT NULL, 
        EXT_SOURCE_1 TEXT NOT NULL,
        prediction REAL NOT NULL,
        decision TEXT NOT NULL
    )
''')

data = pd.read_csv('data/imputed_data.csv')
table_name = "data"

# Enregistrer chaque DataFrame dans la base de données
data.to_sql(table_name, conn, if_exists='replace', index=False)

# Sauvegarde des modifications
conn.commit()

# Fermeture de la connexion
conn.close()
