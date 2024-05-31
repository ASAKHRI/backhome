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
def save_request(NAME_CONTRACT_TYPE, FLAG_OWN_CAR, FLAG_OWN_REALTY, CNT_CHILDREN, AMT_INCOME_TOTAL, AMT_CREDIT_x, AMT_ANNUITY_x, AMT_GOODS_PRICE, DAYS_BIRTH, DAYS_EMPLOYED, EXT_SOURCE_1, prediction, decision):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (NAME_CONTRACT_TYPE, FLAG_OWN_CAR, FLAG_OWN_REALTY, CNT_CHILDREN, AMT_INCOME_TOTAL, AMT_CREDIT_x, AMT_ANNUITY_x, AMT_GOODS_PRICE, DAYS_BIRTH, DAYS_EMPLOYED, EXT_SOURCE_1, prediction, decision)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (NAME_CONTRACT_TYPE, FLAG_OWN_CAR, FLAG_OWN_REALTY, CNT_CHILDREN, AMT_INCOME_TOTAL, AMT_CREDIT_x, AMT_ANNUITY_x, AMT_GOODS_PRICE, DAYS_BIRTH, DAYS_EMPLOYED, EXT_SOURCE_1, prediction, decision))
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
    save_request(data['NAME_CONTRACT_TYPE'], data['FLAG_OWN_CAR'], data['FLAG_OWN_REALTY'], data['CNT_CHILDREN'], data['AMT_INCOME_TOTAL'], data['AMT_CREDIT_x'], data['AMT_ANNUITY_x'], data['AMT_GOODS_PRICE'], data['DAYS_BIRTH'], data['DAYS_EMPLOYED'], data['EXT_SOURCE_1'], prediction, decision)
    
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


@app.route('/table_info', methods=['GET'])
def get_table_info():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    tables_info = {}

    # Récupérer les informations sur les tables
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for table in tables:
        table_name = table[0]
        columns = cursor.execute(f"PRAGMA table_info({table_name});").fetchall()
        columns_names = [col[1] for col in columns]
        num_rows = cursor.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()[0]
        data = cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;").fetchall()

        tables_info[table_name] = {
            'columns': len(columns),
            'columns_names': columns_names,
            'rows': num_rows,
            'data': data
        }

    conn.close()
    
    return jsonify(tables_info)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
