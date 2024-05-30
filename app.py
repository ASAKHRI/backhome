from flask import Flask, request, jsonify
import joblib
import pandas as pd
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Charger le modèle
model = joblib.load('models/pipeline2.joblib')

# Fonction pour vérifier les informations de connexion
def verify_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    if row and check_password_hash(row[0], password):
        return True
    return False

# Fonction pour sauvegarder la requête et la prédiction dans la base de données
def save_request(data, prediction, decision):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (request_data, prediction, decision)
        VALUES (?, ?, ?)
    ''', (str(data), prediction, decision))
    conn.commit()
    conn.close()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    X = pd.DataFrame([data])
    prediction = model.predict_proba(X)[0][0]
    decision = 'approved' if prediction > 0.5 else 'denied'
    
    # Convertir la prédiction en float
    prediction = float(prediction)
    
    # Sauvegarde de la requête et de la prédiction
    save_request(data, prediction, decision)
    
    return jsonify({'probability': prediction, 'decision': decision})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    if verify_user(username, password):
        return jsonify({'login': 'success'})
    else:
        return jsonify({'login': 'failed'}), 401

@app.route('/requests', methods=['GET'])
def get_requests():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
